#!/usr/bin/env python3
"""Re-time the original-voice edit onto the AI-voice narration.

Inputs (all in .tesseract-work/):
  editable.json / keyframes.json  - the original edit on the ORIGINAL clock (from build_edit.py)
  transcripts/original-voice-edit-words.json - word times of the original narration (original clock)
  transcripts/ai-voice-edit-words.json, voice_timeline.json - AI narration placement (from voice_plan.py)
Outputs: editable.json / keyframes.json on the NEW clock, plus captions.json.

Every picture event is mapped through a piecewise-linear warp anchored on matching
words, so cuts, camera moves and highlights keep landing on the same words. The
Kite video section is a pure shift (plays at its real speed). Footage that played in
real time stays real time (its source range is re-derived). The original narration
layers and captions are dropped; AI narration and new captions are added.
"""
import json, os, re, difflib, bisect

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda p: json.load(open(os.path.join(HERE, p)))
doc, keys = J("editable.json"), J("keyframes.json")
old_w, new_w = J("transcripts/original-voice-edit-words.json"), J("transcripts/ai-voice-edit-words.json")
vt = J("voice_timeline.json")
from plan import timeline as old_timeline
OLD_TL, OLD_END = old_timeline()
OLD = {s["key"]: s for s in OLD_TL}
OLD_KITE0, OLD_KITE1 = OLD["KITE0"]["start"], OLD["KITE1"]["end"]
NEW_KITE0, NEW_KITE1, NEW_END = vt["kite"]["start"], vt["kite"]["end"], vt["end"]

norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
def first(words, seg, token, after=0.0):
    return next(w for w in words if w["seg"] == seg and norm(w["w"]) == token and w["a"] >= after)

# ---------------------------------------------------------------- anchors
anchors = [(0.0, 0.0)]
for seg in ["V1", "V2", "V3", "V4a", "V4b", "V4c", "V5", "V6", "V7"]:
    o = [w for w in old_w if w["seg"] == seg]; n = [w for w in new_w if w["seg"] == seg]
    sm = difflib.SequenceMatcher(a=[norm(w["w"]) for w in o], b=[norm(w["w"]) for w in n], autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            anchors.append((o[blk.a + k]["a"], n[blk.b + k]["a"]))
    anchors.append((o[-1]["b"], n[-1]["b"]))
anchors += [(OLD_KITE0, NEW_KITE0), (OLD_KITE1, NEW_KITE1)]
# Step 8: the AI voice reads the script wording, so the list beats are re-keyed by hand.
V8n = [w for w in new_w if w["seg"] == "V8"]
anchors += [
    (first(old_w, "V8", "the")["a"], V8n[0]["a"]),
    (165.60, first(new_w, "V8", "especially")["a"] - 0.10),  # page -> generated take
    (167.15, first(new_w, "V8", "hands")["a"] - 0.10),       # -> hands close-up
    (168.60, first(new_w, "V8", "eye")["a"] - 0.08),         # -> eyes close-up
    (169.45, first(new_w, "V8", "and", first(new_w, "V8", "eye")["a"])["a"] - 0.08),  # -> page ("and longer scenes")
    (first(old_w, "V8", "keeping")["a"], first(new_w, "V8", "keeping")["a"]),
    (OLD_END, NEW_END),
]
anchors.sort()
# keep a monotonic, well-spaced set (drops whisper jitter)
clean = [anchors[0]]
for a, b in anchors[1:]:
    if a - clean[-1][0] >= 0.90 and b - clean[-1][1] >= 0.50:
        clean.append((a, b))
if clean[-1] != (OLD_END, NEW_END):
    clean[-1] = (OLD_END, NEW_END)
# Pin the words that trigger a highlight or cut, so those land exactly on the voice.
PINS = [("V2", "simple"), ("V2", "short"), ("V3", "examples"), ("V3", "pacing"), ("V4b", "initial"),
        ("V4b", "campaign"), ("V4b", "expands"), ("V4b", "precise"), ("V4b", "instead"), ("V4c", "fal"),
        ("V4c", "cinematic"), ("V4c", "idea"), ("V5", "final"), ("V5", "timing"), ("V5", "transitions"),
        ("V5", "audio"), ("V5", "output"), ("V5", "considering"), ("V6", "reverse"), ("V6", "key"),
        ("V6", "file"), ("V6", "marked")]
OLD_ALIAS = {"fal": "file"}  # the original voice's "Fal" was transcribed as "file"
NEW_ALIAS = {"fal": ["fal", "fall", "file"]}  # whisper's spelling of the AI's /fæl/
pins = []
for seg, tok in PINS:
    try:
        nw_ = next((w for t in NEW_ALIAS.get(tok, [tok]) for w in new_w if w["seg"] == seg and norm(w["w"]) == t), None)
        if nw_ is None: raise StopIteration
        pins.append((first(old_w, seg, OLD_ALIAS.get(tok, tok))["a"], nw_["a"]))
    except StopIteration:
        print("pin not found", seg, tok)
clean = sorted([(x, y) for x, y in clean if all(abs(x - px) > 0.45 for px, _ in pins)] + pins)
AX = [a for a, _ in clean]; AY = [b for _, b in clean]
for (x0, y0), (x1, y1) in zip(clean, clean[1:]):
    if y1 <= y0: print("NONMONO", x0, y0, x1, y1)
assert all(y1 > y0 for y0, y1 in zip(AY, AY[1:])), "warp not monotonic"

def f(t):
    i = max(0, min(len(AX) - 2, bisect.bisect_right(AX, t) - 1))
    x0, x1, y0, y1 = AX[i], AX[i + 1], AY[i], AY[i + 1]
    return y0 + (t - x0) * (y1 - y0) / (x1 - x0)

# ---------------------------------------------------------------- warp layers
REALTIME_END_ANCHORED = {"2a"}   # keep the send click on "short request"
by_id, new_abs = {}, {}
kept = []
def is_old_audio_or_caption(L):
    return L["name"].startswith("Narration") or L["name"].startswith("Caption")

def warp_layer(L, parent_old, parent_new):
    a_old = parent_old + L["activeRange"]["start"] / 1000
    b_old = a_old + L["activeRange"]["duration"] / 1000
    a_new, b_new = f(a_old), f(b_old)
    by_id[L["id"]] = (a_old, a_new)
    L["activeRange"] = {"start": int(round((a_new - parent_new) * 1000)), "duration": int(round((b_new - a_new) * 1000))}
    if L["type"] == "Video" and "sourceRange" in L:
        sr = L["sourceRange"]; src_d = sr["duration"] / 1000; old_d = b_old - a_old; new_d = b_new - a_new
        if abs(src_d / old_d - 1) < 0.02:  # real-time footage stays real time
            intr = L["sourceIntrinsicDuration"] / 1000
            s0 = sr["start"] / 1000
            tag = L.get("_shot", "")
            if tag in REALTIME_END_ANCHORED:
                s0 = s0 + src_d - new_d
            s0 = max(0.0, min(s0, intr - new_d))
            if s0 >= 0 and s0 + new_d <= intr:
                L["sourceRange"] = {"start": int(round(s0 * 1000)), "duration": int(round(new_d * 1000))}
    for C in L.get("layers", []):
        C["_shot"] = L["name"].split(" ")[0]
        warp_layer(C, a_old, a_new)
        C.pop("_shot", None)
    L.pop("_shot", None)

layers = [L for L in doc["composition"]["layers"] if not is_old_audio_or_caption(L)]
for L in layers:
    warp_layer(L, 0.0, 0.0)

# Step 8 breadcrumb highlight lands on "human realism"
human = first(new_w, "V8", "human")["a"]
for L in layers:
    if L["name"].startswith("8a"):
        g_new = L["activeRange"]["start"] / 1000
        for C in L["layers"]:
            if C["name"].startswith("Highlight: breadcrumb"):
                end_abs = g_new + (C["activeRange"]["start"] + C["activeRange"]["duration"]) / 1000
                C["activeRange"] = {"start": int(round((human - 0.05 - g_new) * 1000)),
                                    "duration": int(round((end_abs - (human - 0.05)) * 1000))}
                by_id[C["id"]] = (None, human - 0.05)

# ---------------------------------------------------------------- warp keyframes
out_keys = []
for act in keys:
    lid = act["property"]["layerId"]
    if lid not in by_id:
        continue  # belonged to a dropped layer (old narration)
    a_old, a_new = by_id[lid]
    if a_old is None:  # re-placed highlight: keep its relative animation
        out_keys.append(act); continue
    for k in act["keyframes"]:
        k["layerTime"] = int(round((f(a_old + k["layerTime"] / 1000) - a_new) * 1000))
    out_keys.append(act)

# ---------------------------------------------------------------- AI narration
next_id = max(by_id) + 1000
man_gain = 10 ** (-2.2 / 20)  # as in the reference: mastered mono sentences sit at -2.2 dB (mono plays on both channels)
audio = []
for s in vt["sentences"]:
    lid = next_id; next_id += 1
    d = s["end"] - s["start"]
    base = os.path.basename(s["file"])[:-4]
    audio.append({"type": "Audio", "id": lid, "name": f"AI narration {base}: {s['text'][:60]}",
                  "activeRange": {"start": int(round(s["start"] * 1000)), "duration": int(round(d * 1000))},
                  "sourceRange": {"start": 0, "duration": int(round(d * 1000))},
                  "sourceIntrinsicDuration": int(round(d * 1000)), "windowMs": 50,
                  "source": {"assetId": f"tts-{base}"}, "volume": man_gain, "captionsEnabled": False})
    out_keys.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                     "property": {"layerId": lid, "propertyType": "volume"},
                     "keyframes": [{"id": f"L{lid}-volume-{i}", "layerTime": int(round(t * 1000)),
                                    "value": {"type": "float", "value": v}, "easing": {"type": "linear"}}
                                   for i, (t, v) in enumerate([(0, 0), (0.01, man_gain), (d - 0.02, man_gain), (d, 0)])]})

# ---------------------------------------------------------------- captions
old_caps = [L for L in doc["composition"]["layers"] if L["name"].startswith("Caption") and L["type"] == "Text"]
texts = [L["sourceText"]["text"] for L in old_caps]
texts = [t.replace("Here, I am showing", "Here, I'm showing") for t in texts]
i8 = next(i for i, t in enumerate(texts) if t.startswith("The next phase"))
texts = texts[:i8] + ["The next phase I'm working on", "is human realism,", "especially improving natural movement,",
                      "hands, eye direction,", "and longer scenes with people.",
                      "I'm keeping that research separate for now", "while I continue testing and improving it."]
say_norm = lambda t: [norm(x) for x in re.sub(r"HyperFrames", "hyper frames", re.sub(r"\bUI\b", "u i", re.sub("-", " ", t))).split() if norm(x)]
cap_tokens, cap_of = [], []
for ci, t in enumerate(texts):
    for tok in say_norm(t):
        cap_tokens.append(tok); cap_of.append(ci)
nw = [w for w in new_w]
sm = difflib.SequenceMatcher(a=cap_tokens, b=[norm(w["w"]) for w in nw], autojunk=False)
span = {}
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        ci = cap_of[blk.a + k]; w = nw[blk.b + k]
        lo, hi = span.get(ci, (w["a"], w["b"]))
        span[ci] = (min(lo, w["a"]), max(hi, w["b"]))
assert len(span) == len(texts), (len(span), len(texts), [t for i, t in enumerate(texts) if i not in span])
caps = []
for ci, t in enumerate(texts):
    a, b = span[ci]
    caps.append([a - 0.08, b + 0.30, t])
for i in range(len(caps) - 1):
    nxt = caps[i + 1][0]
    if nxt - caps[i][1] < 0.45:  # close small gaps so captions hand off cleanly
        caps[i][1] = nxt
    caps[i][1] = min(caps[i][1], nxt)

raised = [(f(0.0), f(3.85)), (f(12.95), f(24.40))]
FONT = {"fontFamily": "IBM Plex Sans Medm", "fontStyle": "Medium"}
CAP_SIZE, CAP_H, CHAR_W = 44, 74, 0.525 * 44
cap_layers = []
for i, (a, b, t) in enumerate(caps):
    y = 715 if any(r0 <= a < r1 for r0, r1 in raised) else 958
    tid, bid = next_id, next_id + 1; next_id += 2
    w = round(len(t) * CHAR_W + 72)
    rng = {"start": int(round(a * 1000)), "duration": int(round((b - a) * 1000))}
    cap_layers.append({"type": "Text", "id": tid, "name": f"Caption {i + 1:02d}", "blendMode": "normal", "activeRange": rng,
                       "transform": {"anchorPoint": [0, 0], "position": [0, 0], "scale": [100, 100], "rotation": 0, "opacity": 100},
                       "sourceText": dict(FONT, text=t, fontSize=CAP_SIZE, fillColor=[1, 1, 1, 1], strokeWidth=0,
                                          justification="center", boxText=True, boxPosition=[160, y + 13],
                                          boxSize=[1600, CAP_H], verticalAlign="top")})
    cap_layers.append({"type": "Rect", "id": bid, "name": f"Caption {i + 1:02d} backing", "blendMode": "normal", "activeRange": rng,
                       "transform": {"anchorPoint": [w / 2, CAP_H / 2], "position": [960, y + CAP_H / 2], "scale": [100, 100], "rotation": 0, "opacity": 100},
                       "rect": {"size": [w, CAP_H], "position": [0, 0], "fillColor": [0.045, 0.045, 0.055, 0.92], "roundness": 18}})

# order: fades + chips first, then captions, then the rest (pictures), then audio
front = [L for L in layers if L["name"].startswith(("End fade", "Opening fade", "Chapter chip"))]
rest = [L for L in layers if L not in front]
doc["composition"]["layers"] = front + cap_layers + rest + audio
doc["duration"] = round(NEW_END, 3)
doc["composition"]["name"] = "Video Workflow Demo - Opus 5.5 - AI voice"
json.dump(doc, open(os.path.join(HERE, "editable.json"), "w"), indent=1)
json.dump(out_keys, open(os.path.join(HERE, "keyframes.json"), "w"), indent=1)
json.dump({"captions": [{"startMs": int(round(a * 1000)), "endMs": int(round(b * 1000)), "text": t} for a, b, t in caps]},
          open(os.path.join(HERE, "captions.json"), "w"), indent=1)
json.dump({"anchors_old_to_new": clean}, open(os.path.join(HERE, "warp-anchors.json"), "w"), indent=0)
slopes = [(AY[i + 1] - AY[i]) / (AX[i + 1] - AX[i]) for i in range(len(AX) - 1)]
print(f"anchors {len(clean)}  slope min {min(slopes):.2f} max {max(slopes):.2f}  end {NEW_END}  captions {len(caps)}  keyframe actions {len(out_keys)}")
for (x0, y0), (x1, y1), s in zip(clean, clean[1:], slopes):
    if s < 0.6 or s > 1.6:
        print(f"  steep segment old {x0:.2f}-{x1:.2f} -> new {y0:.2f}-{y1:.2f} slope {s:.2f}")
