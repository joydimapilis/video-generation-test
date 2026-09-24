#!/usr/bin/env python3
"""Build the Opus 5.5 AI-voice edit of "Save the Learnings" as native Tesseract layers.

Same picture design as ../save-the-learnings-opus-5-5, re-timed to a local
Kokoro TTS read of the script. The supplied voice recording is NOT used.

Writes .tesseract-work/editable.json (layer structure) and
.tesseract-work/keyframes.json (animation action batch). Run from the
project root, then commit + apply (see README.md in the project folder).

All times in this file are milliseconds on the EDIT clock unless named src_*.
Source-pixel coordinates refer to the 3164x1930 screen recording.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
SRC_W, SRC_H = 3164, 1930
COVER = W / SRC_W                      # k that fits the full recording width (0.60683)
COVER_YOFF = (SRC_H * COVER - H) / 2   # vertical crop of the black margins at that k
END_MS = 20200

FONT = {"fontFamily": "IBM Plex Sans", "fontStyle": "Regular"}
AMBER = [1.0, 0.74, 0.28]

# ---------------------------------------------------------------- narration
# AI voice: Kokoro-82M (af_heart, speed 0.92), one mastered 48 kHz WAV per
# sentence, placed with chosen sentence pauses (speech-to-speech 0.50 s, 0.55 s).
VOICE = [  # (asset id, edit start ms, file duration ms, speech on ms, speech off ms)
    ("voice-1", 450, 5035, 60, 4960),
    ("voice-2", 5870, 6805, 40, 6730),
    ("voice-3", 13100, 4843, 50, 4760),
]

# ---------------------------------------------------------------- picture
# Doc-space framing: 1 source px = 1 canvas px ("k=1"), doc column centred.
DOC_CX_SRC = 1470       # source x mapped to canvas x 960
HEAD_SCREEN_Y = 210     # every list heading lands on this canvas y (match cut)
HEAD_SCREEN_X = 659 - DOC_CX_SRC + 960  # = 149, where headings start on screen

# Word onsets on the edit clock (from waveform energy + local whisper):
# reverse 3.51, This 5.91, prompts 8.67, structure 9.27, methods 9.99,
# revisions 10.95, key 11.85, The 13.15, this 14.92, before ~15.72, can ~16.50.
CUT_PROMPTS = 8610      # 60 ms before "prompts"
CUT_STRUCTURE = 9210    # before "structure"
CUT_METHODS = 9930      # before "methods"
CUT_REVISIONS = 10890   # before "revisions"
CUT_LEARNINGS = 11790   # before "key learnings"
SCROLL_START = 5400     # as "document." ends, before "This"


def local_of(sx, sy):
    """Video/Image layer-local space is source pixels (verified by calibration)."""
    return [sx, sy]


def frame_transform(k, src_pt, screen_pt, opacity=100):
    """Transform mapping source point src_pt to screen_pt at k canvas px/source px."""
    s = 100 * k
    return {"anchorPoint": local_of(*src_pt), "position": list(screen_pt),
            "scale": [s, s], "rotation": 0, "opacity": opacity}


def ident(opacity=100):
    return {"anchorPoint": [0, 0], "position": [0, 0], "scale": [100, 100],
            "rotation": 0, "opacity": opacity}


def rng(start, dur):
    return {"start": int(round(start)), "duration": int(round(dur))}


layers = []  # built front-to-back later; collect by role first
keyframe_actions = []


def kf(layer_id, prop, keys):
    """keys: list of (id_suffix, t_ms_layer_local, value, easing)."""
    frames = []
    for suffix, t, v, ease in keys:
        e = {"type": "linear"} if ease == "linear" else (
            {"type": "cubicBezier", "x1": ease[0], "y1": ease[1], "x2": ease[2], "y2": ease[3]})
        frames.append({"id": f"L{layer_id}-{prop}-{suffix}", "layerTime": int(round(t)),
                       "value": {"type": "float", "value": float(v)}, "easing": e})
    keyframe_actions.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                             "property": {"layerId": layer_id, "propertyType": prop},
                             "keyframes": frames})


EASE_IO = (0.65, 0, 0.35, 1)      # camera moves
EASE_OUT = (0.2, 0.7, 0.3, 1)     # highlight arrivals


def video(id_, name, act_start, act_dur, src_start, src_dur, transform):
    return {"type": "Video", "id": id_, "name": name, "blendMode": "normal",
            "activeRange": rng(act_start, act_dur), "sourceRange": rng(src_start, src_dur),
            "sourceIntrinsicDuration": 29766, "volume": 0.0,
            "transform": transform, "source": {"assetId": "screen", "fit": "cover"}}


def image(id_, name, act_start, act_dur, asset, transform):
    return {"type": "Image", "id": id_, "name": name, "blendMode": "normal",
            "activeRange": rng(act_start, act_dur), "transform": transform,
            "source": {"assetId": asset, "fit": "cover"}}


def rect(id_, name, act_start, act_dur, x, y, w, h, fill, stroke=None, stroke_w=0,
         roundness=0, anchor_left=False, opacity=100):
    r = {"size": [w, h], "position": [0, 0], "fillColor": fill, "roundness": roundness}  # position = top-left
    if stroke:
        r.update({"strokeEnabled": True, "strokeColor": stroke, "strokeWidth": stroke_w,
                  "strokeJoin": "round"})
    anchor = [0, h / 2] if anchor_left else [w / 2, h / 2]
    pos = [x + anchor[0], y + anchor[1]]
    return {"type": "Rect", "id": id_, "name": name, "blendMode": "normal",
            "activeRange": rng(act_start, act_dur),
            "transform": {"anchorPoint": anchor, "position": pos, "scale": [100, 100],
                          "rotation": 0, "opacity": opacity},
            "rect": r}


def highlight(id_, name, act_start, act_dur, x, y, w, h, swipe_at, fade_out_at=None):
    """Amber highlighter swipe: grows left-to-right, holds, optional fade."""
    lay = rect(id_, name, act_start, act_dur, x, y, w, h,
               fill=AMBER + [0.16], stroke=AMBER + [0.95], stroke_w=3, roundness=10,
               anchor_left=True)
    t0 = swipe_at - act_start
    kf(id_, "scaleX", [("a", t0, 0, "linear"), ("b", t0 + 260, 100, EASE_OUT)])
    kf(id_, "opacity", [("a", t0, 0, "linear"), ("b", t0 + 120, 100, "linear")] +
       ([("c", fade_out_at - act_start, 100, "linear"),
         ("d", fade_out_at - act_start + 200, 0, "linear")] if fade_out_at else []))
    return lay


# ---- Beat 1: title (0 - 5.4s). Original frames 0-2.8s, gently slowed to 0.52x
# (the page is static; only the pointer drifts) while the camera pushes from the
# whole app to the document title and file path.
TITLE_A = (DOC_CX_SRC, 283)          # path bar row in the source
TITLE_SCREEN = (960, 150)
title = video(10, "Title view (src 0-2.8s, slowed)", 0, SCROLL_START, 0, 2800,
              frame_transform(1.0, TITLE_A, TITLE_SCREEN))
wide_pos = [TITLE_A[0] * COVER, TITLE_A[1] * COVER - COVER_YOFF]  # identity cover framing
kf(10, "scaleX", [("a", 650, 100 * COVER, "linear"), ("b", 3150, 100, EASE_IO)])
kf(10, "scaleY", [("a", 650, 100 * COVER, "linear"), ("b", 3150, 100, EASE_IO)])
kf(10, "positionX", [("a", 650, wide_pos[0], "linear"), ("b", 3150, TITLE_SCREEN[0], EASE_IO)])
kf(10, "positionY", [("a", 650, wide_pos[1], "linear"), ("b", 3150, TITLE_SCREEN[1], EASE_IO)])

# Filename in the breadcrumb: source x 1142-1574, y 268-300 -> k=1 screen.
hl_title = highlight(40, "Highlight: reverse-engineering file path", 3380, SCROLL_START - 3380,
                     1142 - DOC_CX_SRC + 960 - 12, 268 - 283 + 150 - 10, 432 + 24, 32 + 20,
                     swipe_at=3460, fade_out_at=5150)

# ---- Beat 2: the real scroll through the document (src 2.8-7.1s at ~1.34x),
# camera drifting down so it lands with "Prompts" on the heading line.
SCROLL_DUR = CUT_PROMPTS - SCROLL_START
PROMPTS_HEAD_Y = 562
scroll = video(11, "Document scroll (src 2.8-7.1s, 1.34x)", SCROLL_START, SCROLL_DUR, 2800, 4300,
               frame_transform(1.0, TITLE_A, TITLE_SCREEN))
land_y = TITLE_A[1] - PROMPTS_HEAD_Y + HEAD_SCREEN_Y
kf(11, "positionY", [("a", 250, TITLE_SCREEN[1], "linear"), ("b", 1500, land_y, EASE_IO)])

# ---- Beat 3: one original frame per spoken item, heading always at the same
# spot (match cut), with the same highlighter swipe.
HEADS = [  # (layer id, name, asset, heading source y, heading width px, cut in, cut out)
    (12, "Prompts", "hold-prompts", PROMPTS_HEAD_Y, 156, CUT_PROMPTS, CUT_STRUCTURE),
    (13, "Structure", "hold-structure", 727, 179, CUT_STRUCTURE, CUT_METHODS),
    (14, "Models and methods", "hold-methods", 714, 395, CUT_METHODS, CUT_REVISIONS),
    (15, "Revisions", "hold-revisions", 545, 178, CUT_REVISIONS, CUT_LEARNINGS),
]
holds, head_hls = [], []
for i, (lid, nm, asset, hy, hw, a, b) in enumerate(HEADS):
    holds.append(image(lid, f"Hold: {nm} (original frame)", a, b - a, asset,
                       frame_transform(1.0, (DOC_CX_SRC, hy), (960, HEAD_SCREEN_Y))))
    head_hls.append(highlight(41 + i, f"Highlight: {nm} heading", a, b - a,
                              HEAD_SCREEN_X - 16, HEAD_SCREEN_Y - 12, hw + 32, 35 + 24,
                              swipe_at=a + 40))

# ---- Beat 4: "key learnings" -> the file tree. Live original frames (static
# page) inside a camera group that pans/zooms to the file in the sidebar.
LEARN_HEAD_Y = 959
FIN_DUR = END_MS - CUT_LEARNINGS
# Children use k=1 doc space: screen = src - (DOC_CX_SRC-960, LEARN_HEAD_Y-HEAD_SCREEN_Y)
OX, OY = DOC_CX_SRC - 960, LEARN_HEAD_Y - HEAD_SCREEN_Y
fin_video = video(16, "Final view (src 9.0s+, live)", 0, FIN_DUR, 9000, FIN_DUR,
                  frame_transform(1.0, (DOC_CX_SRC, LEARN_HEAD_Y), (960, HEAD_SCREEN_Y)))
T = lambda t: t - CUT_LEARNINGS  # edit time -> group-local time
hl_learn = highlight(45, "Highlight: Final learnings heading", 0, T(13300),
                     HEAD_SCREEN_X - 16, HEAD_SCREEN_Y - 12, 275 + 32, 35 + 24,
                     swipe_at=40, fade_out_at=T(13050))
# File-tree rows (source px): reverse-engineering file row y 552-604,
# "artifacts / final_outcome" folder row y 500-548; x 2380-3024.
FILE_ROW = (2382, 552, 640, 52)
hl_file = highlight(46, "Highlight: reverse-engineering file in file tree",
                    T(14800), FIN_DUR - T(14800),
                    FILE_ROW[0] - OX, FILE_ROW[1] - OY, FILE_ROW[2], FILE_ROW[3],
                    swipe_at=T(14860))  # on "this file"; group-local clock
# On "before the video can be marked complete" grow the box up over the
# artifacts/final_outcome folder that holds the file.
grow_t = T(15680) - T(14800)  # on "before the video"
# rectSize grows down from the rect top-left, so move the layer up by the growth.
keyframe_actions.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
    "property": {"layerId": 46, "propertyType": "rectSize"},
    "keyframes": [
        {"id": "L46-rectSize-a", "layerTime": grow_t, "value": {"type": "vector2", "value": [FILE_ROW[2], FILE_ROW[3]]}, "easing": {"type": "linear"}},
        {"id": "L46-rectSize-b", "layerTime": grow_t + 380, "value": {"type": "vector2", "value": [FILE_ROW[2], FILE_ROW[3] * 2]},
         "easing": {"type": "cubicBezier", "x1": EASE_OUT[0], "y1": EASE_OUT[1], "x2": EASE_OUT[2], "y2": EASE_OUT[3]}}]})
fy = hl_file["transform"]["position"][1]
kf(46, "positionY", [("a", grow_t, fy, "linear"), ("b", grow_t + 380, fy - FILE_ROW[3], EASE_OUT)])

# Camera: k=1 on "Final learnings" -> k=1.4 framing the file tree.
CAM_K, CAM_SRC, CAM_SCREEN = 1.4, (2380, 560), (960, 540)
cam_anchor = [CAM_SRC[0] - OX, CAM_SRC[1] - OY]
fin_group = {"type": "Group", "id": 30, "name": "Finale camera (learnings -> file tree)",
             "blendMode": "normal", "activeRange": rng(CUT_LEARNINGS, FIN_DUR),
             "transform": {"anchorPoint": cam_anchor, "position": list(cam_anchor),
                           "scale": [100, 100], "rotation": 0, "opacity": 100},
             "layers": [hl_file, hl_learn, fin_video]}
c0, c1 = T(13050), T(14350)
kf(30, "scaleX", [("a", c0, 100, "linear"), ("b", c1, CAM_K * 100, EASE_IO)])
kf(30, "scaleY", [("a", c0, 100, "linear"), ("b", c1, CAM_K * 100, EASE_IO)])
kf(30, "positionX", [("a", c0, cam_anchor[0], "linear"), ("b", c1, CAM_SCREEN[0], EASE_IO)])
kf(30, "positionY", [("a", c0, cam_anchor[1], "linear"), ("b", c1, CAM_SCREEN[1], EASE_IO)])

# ---- Captions: phrase captions from the supplied script, timed to the voice.
CAPTIONS = [
    (450, 2250, "For every finished video,"),
    (2250, 3470, "the system creates its own"),
    (3470, 5750, "reverse-engineering document."),
    (5850, 8000, "This records how the video was made,"),
    (8000, CUT_STRUCTURE, "including the prompts,"),
    (CUT_STRUCTURE, CUT_REVISIONS, "structure, methods used,"),
    (CUT_REVISIONS, 13000, "revisions, and key learnings."),
    (13080, 14720, "The workflow also checks"),
    (14720, 15680, "that this file exists"),
    (15680, 16450, "before the video"),
    (16450, 18500, "can be marked complete."),
]
CAP_SIZE, CAP_Y, CAP_H = 48, 942, 88
CHAR_W = 0.50 * CAP_SIZE  # measured average advance for these phrases (checked in render)
caption_layers = []
for i, (a, b, text) in enumerate(CAPTIONS):
    tid, bid = 100 + i * 2, 101 + i * 2
    pill_w = round(len(text) * CHAR_W + 84)
    caption_layers.append({
        "type": "Text", "id": tid, "name": f"Caption {i + 1}", "blendMode": "normal",
        "activeRange": rng(a, b - a), "transform": ident(),
        "sourceText": dict(FONT, text=text, fontSize=CAP_SIZE, fillColor=[1, 1, 1, 1],
                           strokeWidth=0, justification="center", boxText=True,
                           boxPosition=[160, CAP_Y + 14], boxSize=[1600, CAP_H],
                           verticalAlign="top")})
    caption_layers.append(rect(bid, f"Caption {i + 1} backing", a, b - a,
                               960 - pill_w / 2, CAP_Y, pill_w, CAP_H,
                               fill=[0.035, 0.035, 0.045, 1.0], roundness=16))

# ---- Caption scrim: soft bottom gradient so document text never competes
# with the caption pill. Fades out after the last caption.
SCRIM_H, SCRIM_END = 250, 19050
scrim = rect(95, "Caption scrim (bottom gradient)", 0, SCRIM_END, 0, H - SCRIM_H, W, SCRIM_H,
             fill=[0, 0, 0, 0])
scrim["rect"]["fillPaint"] = {"type": "gradient", "gradientType": "linear",
                              "start": [0, 0], "end": [0, SCRIM_H],
                              "stops": [{"offset": 0, "color": [0, 0, 0, 0]},
                                        {"offset": 0.55, "color": [0, 0, 0, 0.55]},
                                        {"offset": 1, "color": [0, 0, 0, 0.8]}]}
kf(95, "opacity", [("a", 18600, 100, "linear"), ("b", SCRIM_END, 0, (0.4, 0, 0.6, 1))])

# ---- Ending: short fade to black over the held final frame.
fade = rect(90, "End fade", END_MS - 600, 600, 0, 0, W, H, fill=[0, 0, 0, 1])
kf(90, "opacity", [("a", 100, 0, "linear"), ("b", 600, 100, (0.4, 0, 0.6, 1))])

# ---- AI voice layers: one Audio layer per synthesized sentence, 10 ms edge
# ramps inside the files' silence. The mono WAVs play on both stereo channels
# (+3 dB program loudness), so the layers sit at -2.2 dB (~-15.6 LUFS final).
VOICE_GAIN = 10 ** (-2.2 / 20)
audio_layers = []
for i, (aid, start, dur, on, off) in enumerate(VOICE):
    lid = 200 + i
    audio_layers.append({"type": "Audio", "id": lid, "name": f"AI voice sentence {i + 1} (Kokoro af_heart)",
                         "activeRange": rng(start, dur), "sourceRange": rng(0, dur),
                         "sourceIntrinsicDuration": dur, "windowMs": 50,
                         "source": {"assetId": aid}, "volume": VOICE_GAIN, "captionsEnabled": False})
    kf(lid, "volume", [("in0", 0, 0, "linear"), ("in1", 10, VOICE_GAIN, "linear"),
                       ("out0", dur - 10, VOICE_GAIN, "linear"), ("out1", dur, 0, "linear")])
assert VOICE[-1][1] + VOICE[-1][2] < END_MS

# Sibling order: index 0 is frontmost.
layers = ([fade] + caption_layers + [scrim, hl_title] + head_hls + [fin_group] + holds +
          [scroll, title] + audio_layers)

base = json.load(open(os.path.join(HERE, "editable-v0.json")))
base["dimensions"] = {"width": W, "height": H}
base["duration"] = END_MS / 1000
base["composition"]["name"] = "Save the Learnings - Opus 5.5 (AI voice)"
base["composition"]["layers"] = layers
json.dump(base, open(os.path.join(HERE, "editable.json"), "w"), indent=1)
json.dump(keyframe_actions, open(os.path.join(HERE, "keyframes.json"), "w"), indent=1)
json.dump({"captions": [{"startMs": a, "endMs": b, "text": x} for a, b, x in CAPTIONS]},
          open(os.path.join(HERE, "captions.json"), "w"), indent=1)
print("layers", len(layers), "keyframe actions", len(keyframe_actions))
