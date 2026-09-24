#!/usr/bin/env python3
"""Build "Video Workflow Demo — Opus 5.5" as native Tesseract layers.

Writes .tesseract-work/editable.json (layer structure) and
.tesseract-work/keyframes.json (animation batch). Run .tesseract-work/rebuild.sh
from the project root to regenerate the timeline, commit it, and apply keyframes.

Clocks: every `t`/`edit` value here is EDIT seconds; `src` values are seconds in
the named asset. Each shot is a Group whose transform is the "camera"; its
children (footage, holds, highlights) live in SOURCE-pixel space, so a
highlight stays locked to its text while the camera moves.
"""
import json, os
from plan import timeline

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
TL, TOTAL = timeline()
SEG = {s["key"]: s for s in TL}
END = round(TOTAL, 3)

FONT_CAP = {"fontFamily": "IBM Plex Sans Medm", "fontStyle": "Medium"}   # IBM Plex Sans Medium (verified weight in render)
FONT_CHIP = FONT_CAP
AMBER = [1.0, 0.76, 0.29]
NARR_GAIN = 10 ** (8.0 / 20)   # +8.0 dB on the compressed narration derivatives (about -23.3 LUFS each)
KITE_GAIN = 10 ** (0.6 / 20)   # Kite soundtrack as recorded (about -17 LUFS), +0.6 dB
XF = 0.25                      # crossfade at chapter boundaries

ASSET_MS = {"s2-request": 20000, "s2-timelapse": 16666, "s2-complete": 11933, "s3": 53233,
            "s4": 21866, "s4p2": 26166, "s4p3": 24816, "s5": 35033, "s6": 29766,
            "s7": 52600, "s8": 46983,
            "vo1": 18347, "vo2": 17280, "vo3": 20352, "vo4": 51648, "vo4p3": 32171,
            "vo5": 56768, "vo6": 23253, "vo7": 22464, "vo8": 25451}

_id = [0]
def nid():
    _id[0] += 1
    return _id[0]

def ms(t):
    return int(round(t * 1000))

def rng(a, b):
    return {"start": ms(a), "duration": ms(b) - ms(a)}

def ident(opacity=100):
    return {"anchorPoint": [0, 0], "position": [0, 0], "scale": [100, 100], "rotation": 0, "opacity": opacity}

KEYS = []
EASE_IO = (0.65, 0, 0.35, 1)
EASE_OUT = (0.2, 0.7, 0.3, 1)

def kf(layer_id, prop, keys):
    """keys: (t_local_seconds, value, ease) with ease 'linear' | 'hold' | bezier tuple."""
    frames = []
    for i, (t, v, ease) in enumerate(keys):
        if ease == "linear":
            e = {"type": "linear"}
        else:
            e = {"type": "cubicBezier", "x1": ease[0], "y1": ease[1], "x2": ease[2], "y2": ease[3]}
        frames.append({"id": f"L{layer_id}-{prop}-{i}", "layerTime": ms(t),
                       "value": {"type": "float", "value": float(v)}, "easing": e})
    KEYS.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                 "property": {"layerId": layer_id, "propertyType": prop}, "keyframes": frames})

# ---------------------------------------------------------------- camera
def cam_values(F, k):
    """Group transform (anchor 0,0) that puts source point F at canvas centre at k."""
    return (960 - F[0] * k, 540 - F[1] * k, 100 * k)

def camera(gid, cams):
    """cams: [(t_local, (fx, fy), k)] -> keyframes; the first entry is the rest state."""
    x0, y0, s0 = cam_values(*cams[0][1:])
    tr = {"anchorPoint": [0, 0], "position": [x0, y0], "scale": [s0, s0], "rotation": 0, "opacity": 100}
    if len(cams) > 1:
        ks = {"positionX": [], "positionY": [], "scaleX": [], "scaleY": []}
        for i, (t, F, k) in enumerate(cams):
            x, y, s = cam_values(F, k)
            ease = EASE_IO
            for p, v in (("positionX", x), ("positionY", y), ("scaleX", s), ("scaleY", s)):
                ks[p].append((t, v, "linear" if i == 0 else ease))
        # keyframe easing applies to the segment arriving at that key
        for p, v in ks.items():
            kf(gid, p, v)
    return tr

# ---------------------------------------------------------------- highlights
def rect_layer(lid, name, a, b, x, y, w, h, fill, stroke=None, stroke_w=0, roundness=0,
               anchor_left=False, opacity=100):
    r = {"size": [w, h], "position": [0, 0], "fillColor": fill, "roundness": roundness}
    if stroke:
        r.update({"strokeEnabled": True, "strokeColor": stroke, "strokeWidth": stroke_w, "strokeJoin": "round"})
    anchor = [0, h / 2] if anchor_left else [w / 2, h / 2]
    return {"type": "Rect", "id": lid, "name": name, "blendMode": "normal", "activeRange": rng(a, b),
            "transform": {"anchorPoint": anchor, "position": [x + anchor[0], y + anchor[1]],
                          "scale": [100, 100], "rotation": 0, "opacity": opacity},
            "rect": r}

def highlight(name, box, at, k, until, fade_at=None, pad=8):
    """Amber highlighter box in SOURCE px, swiping left->right at local time `at`."""
    x, y, w, h = box
    x, y, w, h = x - pad, y - pad, w + 2 * pad, h + 2 * pad
    lid = nid()
    lay = rect_layer(lid, f"Highlight: {name}", at, until, x, y, w, h,
                     fill=AMBER + [0.15], stroke=AMBER + [0.95], stroke_w=3.2 / k,
                     roundness=9 / k, anchor_left=True)
    kf(lid, "scaleX", [(0, 0, "linear"), (0.28, 100, EASE_OUT)])
    ok = [(0, 0, "linear"), (0.12, 100, "linear")]
    if fade_at is not None:
        ok += [(fade_at - at, 100, "linear"), (fade_at - at + 0.2, 0, "linear")]
    kf(lid, "opacity", ok)
    return lay

# ---------------------------------------------------------------- shots
SHOTS = []

def shot(name, asset, src_in, src_out, t0, t1, cams, hls=(), kind="Video", fade_in=0.0):
    """A camera Group containing one footage/hold layer plus highlight overlays.
    cams use EDIT times; hls = [(name, box, at_edit, fade_at_edit|None)]."""
    gid = nid()
    dur = t1 - t0
    local_cams = [(t - t0 if i else 0, F, k) for i, (t, F, k) in enumerate(cams)]
    tr = camera(gid, local_cams)
    k_hl = max(c[2] for c in cams)
    children = []
    for hn, box, at, fade_at in hls:
        children.append(highlight(hn, box, at - t0, k_hl, dur, None if fade_at is None else fade_at - t0))
    fid = nid()
    if kind == "Video":
        media = {"type": "Video", "id": fid, "name": f"{asset} src {src_in:.2f}-{src_out:.2f}s",
                 "blendMode": "normal", "activeRange": rng(0, dur), "sourceRange": rng(src_in, src_out),
                 "sourceIntrinsicDuration": ASSET_MS[asset], "volume": 0.0,
                 "transform": ident(), "source": {"assetId": asset, "fit": "cover"}}
    else:
        media = {"type": "Image", "id": fid, "name": f"Hold {asset}", "blendMode": "normal",
                 "activeRange": rng(0, dur), "transform": ident(), "source": {"assetId": asset, "fit": "cover"}}
    children.append(media)
    grp = {"type": "Group", "id": gid, "name": name, "blendMode": "normal", "activeRange": rng(t0, t1),
           "transform": tr, "layers": children}
    if fade_in:
        kf(gid, "opacity", [(0, 0, "linear"), (fade_in, 100, (0.4, 0, 0.6, 1))])
    SHOTS.append((t0, grp))
    return grp

# Standard framings
WIDE720 = ((640, 360), 1.5)            # 1280x720 recordings, full frame
WIN = (1582, 881)                      # 3164-wide recordings: window, top edge at canvas 0
WIDE4 = (WIN, 0.67)
KITE = ((632.5, 384), 1.607)           # fullscreen Kite playback inside Step 7.mov (white frame fills canvas)
DOC_K = 0.87                           # Conductor docs: sidebar + document, file tree trimmed at its divider
DOC_X = 1225                           # source x at canvas centre for that framing (left edge ~x122, right ~x2328)
def DOC(y, k=DOC_K):
    return ((DOC_X, max(700, y)), k)

def C(t, fk):  # camera key helper
    return (t, fk[0], fk[1])

# ======== Step 1 — intro (0 - 13.20)
B12, B23, B34, B4C, B4D, B45, B56, B67 = 13.20, 27.90, 44.95, 65.30, 74.40, 88.95, 102.25, 121.40
KITE0, KITE1 = SEG["KITE0"], SEG["KITE1"]
BK = KITE0["start"]
B78 = KITE1["end"]

shot("1a Intro: the request (Step 2 src 7.0-9.6, slowed)", "s2-request", 7.0, 9.6, 0.0, 3.85,
     [C(0, WIDE720), C(3.85, ((600, 402), 1.7))])
shot("1b Intro: storyboard (Step 4 src 0-2.2)", "s4", 0.0, 2.2, 3.85, 6.05,
     [C(3.85, DOC(820)), C(6.05, DOC(820, 0.9))])
shot("1c Intro: verification (Step 5 src 0-1.0)", "s5", 0.0, 1.0, 6.05, 7.05,
     [C(6.05, DOC(760)), C(7.05, DOC(760, 0.9))])
shot("1d Intro: finished Kite video (Step 7 src 12.2-18.35, muted)", "s7", 12.2, 18.35, 7.05, B12,
     [C(7.05, KITE)])

# ======== Step 2 — the request
PROMPT_ROW = (256, 586, 594, 18)
shot("2a Request typed and sent (Step 2 src 0-11.45, real time)", "s2-request", 0.0, 11.45, B12 - XF, 24.40,
     [C(B12 - XF, WIDE720), C(13.95, WIDE720), C(15.35, ((600, 402), 1.7)), C(22.15, ((600, 402), 1.7)),
      C(22.95, WIDE720)],
     hls=[("prompt text", PROMPT_ROW, 15.15, 16.9)], fade_in=XF)
shot("2b Agent run time-lapse (whole 16m46s run, ~530x)", "s2-timelapse", 0.0, 16.66, 24.40, 26.55,
     [C(24.40, WIDE720)])
shot("2c Run complete (Step 2 src 1017.1s, near-freeze)", "s2-complete", 5.10, 5.40, 26.55, B23,
     [C(26.55, WIDE720), C(27.45, ((560, 300), 1.8))],
     hls=[("completion: 83 tool calls, 16m 46s", (256, 152, 206, 72), 26.8, None)])

# ======== Step 3 — reference library
shot("3a Library (Step 3 src 11.5-17.75)", "s3", 11.5, 17.75, B23 - XF, 33.90,
     [C(B23 - XF, WIDE720), C(33.90, ((640, 380), 1.6))], fade_in=XF)
shot("3b Example: AI / VC film (Step 3 src 19.2-21.6)", "s3", 19.2, 21.6, 33.90, 36.30, [C(33.90, WIDE720)])
shot("3c Example: retro computer film (Step 3 src 38.6-41.0)", "s3", 38.6, 41.0, 36.30, 38.70, [C(36.30, WIDE720)])
shot("3d Library (Step 3 src 45.6-51.85)", "s3", 45.6, 51.85, 38.70, B34,
     [C(38.70, WIDE720), C(B34, ((640, 380), 1.6))])

# ======== Step 4 — shot planning
shot("4a Storyboard top (Step 4 src 0-3.3, slowed)", "s4", 0.0, 3.3, B34 - XF, 50.45,
     [C(B34 - XF, WIDE4), C(45.4, WIDE4), C(48.2, DOC(820))], fade_in=XF)
shot("4b Storyboard scroll through the four frames (Step 4 src 3.3-16.4, 2.1x)", "s4", 3.3, 16.4, 50.45, 56.80,
     [C(50.45, DOC(900))])
HEAD_Y = 300  # every Frame heading lands on this canvas row (match cut)
shot("4c1 Frame 1 heading (hold, Step 4 src 5.00)", "hold-f1", 0, 0, 56.80, 60.00,
     [C(56.80, DOC(881 + (540 - HEAD_Y) / DOC_K))],
     hls=[("Frame 1 — Small brief, big possibility", (659, 881, 690, 36), 59.12, None)], kind="Image")
shot("4c2 Frame 2 heading (hold, Step 4 src 10.20)", "hold-f2", 0, 0, 60.00, 61.15,
     [C(60.00, DOC(879 + (540 - HEAD_Y) / DOC_K))],
     hls=[("Frame 2 — One idea to build on", (659, 879, 586, 36), 60.04, None)], kind="Image")
shot("4c3 Frame 3 heading (hold, Step 4 src 13.00)", "hold-f3", 0, 0, 61.15, B4C,
     [C(61.15, DOC(912 + (540 - HEAD_Y) / DOC_K))],
     hls=[("Frame 3 — The campaign takes shape", (659, 912, 717, 36), 61.19, None)], kind="Image")

# ======== Step 4 — choosing the method
shot("4d Shot routing JSON (Step 4 Part 2 src 6.0-15.35)", "s4p2", 6.0, 15.35, B4C - XF, B4D,
     [C(B4C - XF, WIDE4), C(65.55, WIDE4), C(67.0, DOC(760))],
     hls=[("method: HyperFrames HTML + GSAP", (819, 517, 551, 23), 67.55, None),
          ("reason: exact typography, deterministic layout", (724, 557, 1492, 59), 69.85, None),
          ("paid_generation: false", (819, 638, 367, 22), 72.10, None)], fade_in=XF)
shot("4e fal.ai model catalogue (hold, Step 4 Part 3 src 0.50)", "hold-fal", 0, 0, B4D, 78.05,
     [C(B4D, WIDE4), C(77.1, ((1100, 760), 0.85))],
     hls=[("fal logo", (144, 338, 121, 47), 77.45, None)], kind="Image")
shot("4f fal model grid (Step 4 Part 3 src 1.2-5.9)", "s4p3", 1.2, 5.9, 78.05, 82.75,
     [C(78.05, (WIN, 0.75))])
shot("4g fal model grid, page 2 (Step 4 Part 3 src 15.1-21.3)", "s4p3", 15.1, 21.3, 82.75, B45,
     [C(82.75, (WIN, 0.75))])

# ======== Step 5 — assembly and checks
VER_TOP = DOC(760)
VER_REVIEW = DOC(1010)
shot("5a Final verification JSON, top (hold, Step 5 src 0.80)", "hold-ver-top", 0, 0, B45 - XF, 94.00,
     [C(B45 - XF, WIDE4), C(89.3, WIDE4), C(91.0, VER_TOP)],
     hls=[("video: final kite-campaign.mp4", (772, 476, 1066, 64), 92.90, None)], kind="Image", fade_in=XF)
shot("5b Scroll to the review (Step 5 src 2.0-11.8, 4.6x)", "s5", 2.0, 11.8, 94.00, 96.15,
     [C(94.00, VER_REVIEW)])
shot("5c Visual review entries (hold, Step 5 src 14.00)", "hold-ver-review", 0, 0, 96.15, 99.75,
     [C(96.15, VER_REVIEW)],
     hls=[("timing", (800, 855, 1364, 23), 96.45, None),
          ("transitions: fades and clean cuts", (738, 935, 1132, 23), 96.95, None),
          ("audio", (800, 1175, 1380, 23), 97.65, None),
          ("ending (final output)", (800, 1095, 1380, 23), 98.55, None)], kind="Image")
shot("5d Status complete (hold, Step 5 src 0.80)", "hold-ver-top", 0, 0, 99.75, B56,
     [C(99.75, VER_TOP)],
     hls=[("status: complete", (772, 397, 317, 23), 100.95, None)], kind="Image")

# ======== Step 6 — reverse-engineering document
shot("6a Reverse-engineering doc title (Step 6 src 0-2.8, slowed)", "s6", 0.0, 2.8, B56 - XF, 107.45,
     [C(B56 - XF, WIDE4), C(102.6, WIDE4), C(104.3, DOC(700))],
     hls=[("kite-campaign.reverse-engineering.md", (1142, 271, 436, 26), 105.45, None)], fade_in=XF)
shot("6b Doc scroll to Final learnings (Step 6 src 2.8-9.3)", "s6", 2.8, 9.3, 107.45, 115.00,
     [C(107.45, DOC(700)), C(107.8, DOC(700)), C(109.4, DOC(1000))],
     hls=[("Final learnings", (659, 959, 276, 36), 114.40, None)])
shot("6c Verification: documentation checked (hold, Step 5 src 0.80)", "hold-ver-top", 0, 0, 115.00, B67,
     [C(115.00, DOC(1000))],
     hls=[("reverse_engineering path", (738, 1076, 1396, 64), 117.75, None),
          ("documentation_complete: true", (804, 1238, 460, 20), 120.00, None)], kind="Image")

# ======== Step 7 — final video
shot("7a Final video in Conductor (Step 7 src 0.3-4.69)", "s7", 0.3, 4.69, B67 - XF, BK,
     [C(B67 - XF, WIDE720), C(121.9, WIDE720), C(124.3, ((520, 330), 1.9))], fade_in=XF)

kite_layers = []
for part in (KITE0, KITE1):
    x, y, s = cam_values(*KITE)
    kite_layers.append({"type": "Video", "id": nid(),
                        "name": f"Kite final video playback (Step 7 src {part['src_in']:.2f}-{part['src_out']:.2f}s, with its soundtrack)",
                        "blendMode": "normal", "activeRange": rng(part["start"], part["end"]),
                        "sourceRange": rng(part["src_in"], part["src_out"]),
                        "sourceIntrinsicDuration": ASSET_MS["s7"], "volume": 0.0,
                        "transform": {"anchorPoint": [0, 0], "position": [x, y], "scale": [s, s], "rotation": 0, "opacity": 100},
                        "source": {"assetId": "s7", "fit": "cover"}})

kite_dur = KITE1["end"] - KITE0["start"]
kite_audio_id = nid()
kite_audio = {"type": "Audio", "id": kite_audio_id,
              "name": "Kite video soundtrack (Step 7.mov audio 9.00-9.726 + 11.6655-46.90, pause removed)",
              "activeRange": rng(KITE0["start"], KITE1["end"]), "sourceRange": rng(0, kite_dur),
              "sourceIntrinsicDuration": 35957, "windowMs": 50, "source": {"assetId": "kite-audio"},
              "volume": KITE_GAIN, "captionsEnabled": False}
kf(kite_audio_id, "volume", [(0, 0, "linear"), (0.02, KITE_GAIN, "linear"),
                             (kite_dur - 0.05, KITE_GAIN, "linear"), (kite_dur, 0, "linear")])

# ======== Step 8 — next phase
S8_START = B78 - 0.5
shot("8a Human-realism page (Step 8 src 0-4.34)", "s8", 0.0, B78 - S8_START + 165.60 - B78, S8_START, 165.60,
     [C(S8_START, WIDE4), C(165.60, (WIN, 0.72))],
     hls=[("breadcrumb: Human-realism", (1059, 283, 193, 21), 162.70, None)], fade_in=0.5)
shot("8b Generated take: woman at laptop (Step 8 src 17.0-18.55)", "s8", 17.0, 18.55, 165.60, 167.15,
     [C(165.60, ((1836, 1018), 1.25)), C(167.15, ((1836, 1018), 1.32))])
shot("8c Hands close-up (Step 8 src 6.0-7.45)", "s8", 6.0, 7.45, 167.15, 168.60,
     [C(167.15, ((1760, 872), 1.7)), C(168.60, ((1760, 872), 1.76))])
shot("8d Eyes close-up (Step 8 src 18.55-19.40)", "s8", 18.55, 19.40, 168.60, 169.45,
     [C(168.60, ((2060, 875), 2.2)), C(169.45, ((2060, 875), 2.28))])
shot("8e Page, longer samples (Step 8 src 38.3-45.56)", "s8", 38.3, 38.3 + END - 169.45, 169.45, END,
     [C(169.45, (WIN, 0.67)), C(END, (WIN, 0.72))])

# ---------------------------------------------------------------- captions
CAP_Y_LOW, CAP_Y_HIGH = 958, 715
RAISED = [(0.0, 3.85), (B12 - XF, 24.40)]   # when the prompt box itself sits at the bottom
CAPTIONS = [
    (0.45, 1.20, "Hi everyone."),
    (1.20, 3.90, "I built a system that takes a video idea,"),
    (3.90, 5.95, "plans and generates the shots,"),
    (5.95, 7.00, "reviews the results,"),
    (7.00, 9.60, "and turns everything into a finished video."),
    (9.95, 11.85, "For this demo, I'll quickly show you"),
    (11.85, 13.10, "the process and the final output."),
    (13.70, 16.15, "The process starts with a simple request."),
    (16.35, 17.95, "Instead of giving Conductor"),
    (17.95, 19.20, "a long prompt every time,"),
    (19.20, 21.00, "I moved the recurring instructions"),
    (21.00, 22.10, "into the workflow."),
    (22.55, 24.40, "Now I can give it a short request,"),
    (24.40, 26.85, "and the system handles the rest of the process."),
    (28.15, 30.60, "The first thing the system does"),
    (30.60, 32.30, "is look at this existing video library."),
    (32.45, 34.60, "This library gives the system examples"),
    (34.60, 36.35, "of different video styles,"),
    (36.35, 38.75, "pacing, transitions, and storytelling."),
    (39.25, 41.40, "It uses those references as inspiration"),
    (41.40, 42.60, "to plan a new video,"),
    (42.60, 44.45, "rather than copying one directly."),
    (45.20, 47.00, "After reviewing the references,"),
    (47.00, 50.20, "the system breaks the idea into individual shots."),
    (50.40, 52.45, "For this video, it created four shots"),
    (52.45, 54.40, "with their own purpose, timing,"),
    (54.40, 56.40, "copy, and visual direction."),
    (56.80, 58.85, "Here, I am showing three of them:"),
    (58.85, 60.00, "the initial brief,"),
    (60.00, 61.15, "the campaign idea,"),
    (61.15, 62.80, "and how that idea expands"),
    (62.80, 65.05, "into different marketing assets."),
    (65.55, 68.35, "For this project, the system chose HyperFrames"),
    (68.35, 69.80, "because the video needed"),
    (69.80, 72.00, "precise text, UI, and layout"),
    (72.00, 74.30, "instead of generative footage."),
    (74.60, 76.90, "For other videos, it can use models"),
    (76.90, 78.15, "available through Fal"),
    (78.15, 80.05, "when the shot needs things like"),
    (80.05, 82.60, "cinematic movement or generated footage."),
    (83.05, 84.85, "The idea is to choose the method"),
    (84.85, 86.10, "that best fits the shot,"),
    (86.10, 87.80, "instead of using the same model"),
    (87.80, 88.80, "for everything."),
    (89.30, 91.30, "Once the individual shots are ready,"),
    (91.30, 94.00, "they're combined into the final video."),
    (94.10, 96.40, "The workflow then checks things like"),
    (96.40, 98.00, "timing, transitions, audio,"),
    (98.00, 99.70, "and the final output"),
    (99.70, 102.00, "before considering the video complete."),
    (102.50, 104.10, "For every finished video,"),
    (104.10, 105.40, "the system creates its own"),
    (105.40, 107.10, "reverse-engineering document."),
    (107.50, 110.05, "This records how the video was made,"),
    (110.05, 112.65, "including the prompts, structure,"),
    (112.65, 114.10, "methods used, revisions,"),
    (114.10, 115.45, "and key learnings."),
    (115.80, 117.30, "The workflow also checks"),
    (117.30, 118.55, "that this file exists"),
    (118.55, 121.05, "before the video can be marked complete."),
    (121.65, 123.25, "And this is the final video"),
    (123.25, 125.25, "produced through that workflow."),
    (162.45, 164.55, "The next phase I'm working on"),
    (164.55, 165.75, "is making people look"),
    (165.75, 167.15, "and move more naturally,"),
    (167.15, 168.60, "especially their hands,"),
    (168.60, 170.40, "eye movement, and longer scenes."),
    (171.05, 173.15, "I'm keeping that research separate for now"),
    (173.15, 175.50, "while I continue testing and improving it."),
]
CAP_SIZE, CAP_H = 44, 74
CHAR_W = 0.525 * CAP_SIZE
caption_layers = []
for i, (a, b, text) in enumerate(CAPTIONS):
    raised = any(r0 <= a < r1 for r0, r1 in RAISED)
    y = CAP_Y_HIGH if raised else CAP_Y_LOW
    tid, bid = nid(), nid()
    pill_w = round(len(text) * CHAR_W + 72)
    caption_layers.append({
        "type": "Text", "id": tid, "name": f"Caption {i + 1:02d}", "blendMode": "normal",
        "activeRange": rng(a, b), "transform": ident(),
        "sourceText": dict(FONT_CAP, text=text, fontSize=CAP_SIZE, fillColor=[1, 1, 1, 1], strokeWidth=0,
                           justification="center", boxText=True, boxPosition=[160, y + 13],
                           boxSize=[1600, CAP_H], verticalAlign="top")})
    caption_layers.append(rect_layer(bid, f"Caption {i + 1:02d} backing", a, b, 960 - pill_w / 2, y, pill_w, CAP_H,
                                     fill=[0.045, 0.045, 0.055, 0.92], roundness=18))

# ---------------------------------------------------------------- chapter chips
CHIPS = [
    (B12 + 0.2, 17.0, "01", "The request"),
    (B23 + 0.1, 31.6, "02", "Reference library"),
    (B34 + 0.1, 48.6, "03", "Shot planning"),
    (B4C + 0.1, 68.9, "04", "Choosing the method"),
    (B45 + 0.1, 92.6, "05", "Assembly and checks"),
    (B56 + 0.1, 105.9, "06", "Reverse-engineering doc"),
    (B67 + 0.1, 124.9, "07", "Final video"),
    (B78 + 0.1, 165.4, "Next", "Human realism"),
]
chip_layers = []
def chip(a, b, num, label, right=False):
    gid, bg, bar, t1, t2 = nid(), nid(), nid(), nid(), nid()
    size = 26
    num_w = len(num) * 0.62 * size
    lab_w = len(label) * 0.56 * size
    w = round(20 + num_w + 18 + lab_w + 24)
    x0 = W - 44 - w if right else 44
    y0 = 38
    kids = [
        {"type": "Text", "id": t2, "name": f"Chip label: {label}", "blendMode": "normal", "activeRange": rng(0, b - a),
         "transform": ident(), "sourceText": dict(FONT_CHIP, text=label, fontSize=size, fillColor=[1, 1, 1, 1],
                                                  strokeWidth=0, justification="left", boxText=True,
                                                  boxPosition=[x0 + 20 + num_w + 18, y0 + 11], boxSize=[lab_w + 60, 40],
                                                  verticalAlign="top")},
        {"type": "Text", "id": t1, "name": f"Chip number: {num}", "blendMode": "normal", "activeRange": rng(0, b - a),
         "transform": ident(), "sourceText": dict(FONT_CHIP, text=num, fontSize=size, fillColor=AMBER + [1],
                                                  strokeWidth=0, justification="left", boxText=True,
                                                  boxPosition=[x0 + 20, y0 + 11], boxSize=[num_w + 40, 40],
                                                  verticalAlign="top")},
        rect_layer(bg, "Chip backing", 0, b - a, x0, y0, w, 56, fill=[0.05, 0.05, 0.06, 0.86], roundness=14),
    ]
    g = {"type": "Group", "id": gid, "name": f"Chapter chip: {num} {label}", "blendMode": "normal",
         "activeRange": rng(a, b), "transform": ident(), "layers": kids}
    kf(gid, "opacity", [(0, 0, "linear"), (0.25, 100, (0.4, 0, 0.6, 1)),
                        (b - a - 0.3, 100, "linear"), (b - a, 0, (0.4, 0, 0.6, 1))])
    return g
for a, b, n, l in CHIPS:
    chip_layers.append(chip(a, b, n, l))
chip_layers.append(chip(24.50, 26.50, "»", "Sped up", right=True))

# ---------------------------------------------------------------- end fade
fade_id = nid()
fade = rect_layer(fade_id, "End fade to black", END - 0.9, END, 0, 0, W, H, fill=[0, 0, 0, 1])
kf(fade_id, "opacity", [(0, 0, "linear"), (0.9, 100, (0.4, 0, 0.6, 1))])
open_id = nid()
fade_open = rect_layer(open_id, "Opening fade from black", 0, 0.4, 0, 0, W, H, fill=[0, 0, 0, 1])
kf(open_id, "opacity", [(0, 100, "linear"), (0.4, 0, (0.4, 0, 0.6, 1))])

# ---------------------------------------------------------------- narration
audio_layers = []
for s in TL:
    if s["key"].startswith("KITE"):
        continue
    lid = nid()
    d = s["src_out"] - s["src_in"]
    audio_layers.append({"type": "Audio", "id": lid,
                         "name": f"Narration {s['key']}: {s['file']} src {s['src_in']:.2f}-{s['src_out']:.2f}s ({s['note']})",
                         "activeRange": rng(s["start"], s["end"]), "sourceRange": rng(s["src_in"], s["src_out"]),
                         "sourceIntrinsicDuration": ASSET_MS[s["asset"]], "windowMs": 50,
                         "source": {"assetId": s["asset"]}, "volume": NARR_GAIN, "captionsEnabled": False})
    last = s["key"] == "V8"
    keys = [(0, 0, "linear"), (0.03, NARR_GAIN, "linear")]
    keys += [(d - (0.6 if last else 0.03), NARR_GAIN, "linear"), (d, 0, "linear")]
    kf(lid, "volume", keys)

# Sibling order: index 0 is frontmost; later shots sit in front of earlier ones for crossfades.
shot_layers = [g for _, g in sorted(SHOTS, key=lambda x: -x[0])]
step8 = [g for g in shot_layers if g["name"].startswith("8")]
others = [g for g in shot_layers if not g["name"].startswith("8")]
layers = [fade, fade_open] + chip_layers + caption_layers + step8 + kite_layers[::-1] + others + audio_layers + [kite_audio]

base = json.load(open(os.path.join(HERE, "editable-v0.json")))
base["dimensions"] = {"width": W, "height": H}
base["duration"] = END
base["composition"]["name"] = "Video Workflow Demo - Opus 5.5"
base["composition"]["layers"] = layers
json.dump(base, open(os.path.join(HERE, "editable.json"), "w"), indent=1)
json.dump(KEYS, open(os.path.join(HERE, "keyframes.json"), "w"), indent=1)
json.dump({"captions": [{"startMs": ms(a), "endMs": ms(b), "text": x} for a, b, x in CAPTIONS]},
          open(os.path.join(HERE, "captions.json"), "w"), indent=1)
print("duration", END, "layers", len(layers), "ids", _id[0], "keyframe actions", len(KEYS))
