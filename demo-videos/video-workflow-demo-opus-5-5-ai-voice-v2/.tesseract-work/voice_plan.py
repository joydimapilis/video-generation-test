"""AI-voice timeline: sentence placement (edit seconds) and word timings.

Pauses copy the Save-the-Learnings AI-voice reference: 0.50 s / 0.55 s between
sentences inside a chapter (speech to speech); the original edit's gaps between chapters. The Kite video plays unchanged.
"""
import json, os, re, subprocess
from rms import rms_profile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
M = "/Users/joydimapilis/.cache/hyperframes/whisper/models/ggml-small.en.bin"
FIRST_WORD = 0.51
GAP_IN = 0.50                # speech-to-speech pause after a chapter's first sentence (reference: 0.50 s)
GAP_IN_LATER = 0.55          # ...and after later sentences (reference: 0.55 s)
GAP_AFTER = {"V4b-1": 0.75,  # sentence-level override: chapter 03 -> 04 changes inside this take
             "V1": 0.75, "V2": 1.40, "V3": 0.80, "V4a": 0.60, "V4b": 0.60, "V4c": 0.72, "V5": 0.80, "V6": 0.80}
KITE_LEAD = 0.50            # after "...that workflow." before the Kite video starts
KITE_DUR = 35.957           # Step 7.mov 9.000-9.722 + 11.665-46.900
AFTER_KITE = 1.02           # Kite end -> first word of Step 8 (as in the original edit)
END_TAIL = 1.40             # last word end -> end of video

def speech_extent(fn):
    prof = rms_profile(fn, 0, 30, 0.01)
    on = [i for i, d in enumerate(prof) if d > -50]
    return on[0] * 0.01, (on[-1] + 1) * 0.01

def words_for(fn):
    """Whisper tokens -> words, rescaled to the measured speech extent, pauses snapped to measured gaps."""
    w16 = os.path.join(HERE, "transcripts", "tmp16.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", fn, "-ar", "16000", "-ac", "1", w16], check=True)
    subprocess.run(["whisper-cli", "-m", M, "-f", w16, "-ojf", "-of", w16[:-4], "-np"], capture_output=True)
    d = json.load(open(w16[:-4] + ".json"))
    words = []
    for seg in d["transcription"]:
        for t in seg["tokens"]:
            tx = t["text"]
            if tx.startswith("[") or tx.startswith("<"): continue
            a, b = t["offsets"]["from"] / 1000, t["offsets"]["to"] / 1000
            if tx.startswith(" ") or not words: words.append({"w": tx.strip(), "a": a, "b": b})
            else: words[-1]["w"] += tx; words[-1]["b"] = b
    s0, s1 = speech_extent(fn)
    w0, w1 = words[0]["a"], words[-1]["b"]
    for w in words:
        w["a"] = s0 + (w["a"] - w0) * (s1 - s0) / (w1 - w0)
        w["b"] = s0 + (w["b"] - w0) * (s1 - s0) / (w1 - w0)
    # snap internal pauses (>=0.12 s below -45 dB) to the nearest word boundary
    prof = rms_profile(fn, 0, 30, 0.01)
    gaps, run = [], None
    for i, v in enumerate(prof):
        if v < -45:
            run = i if run is None else run
        else:
            if run is not None and (i - run) >= 12 and run * 0.01 > s0 + 0.05: gaps.append((run * 0.01, i * 0.01))
            run = None
    for g0, g1 in gaps:
        gm = (g0 + g1) / 2
        i = min(range(len(words) - 1), key=lambda k: abs((words[k]["b"] + words[k + 1]["a"]) / 2 - gm)
                - (0.3 if words[k]["w"][-1] in ",.:;?!-" else 0))
        words[i]["b"] = g0; words[i + 1]["a"] = g1
    # repair words the snap left inverted (start after end): size them from their length
    for k, w in enumerate(words):
        if w["a"] >= w["b"]:
            lo = words[k - 1]["a"] + 0.05 if k else s0
            w["a"] = max(lo, w["b"] - max(0.12, 0.065 * len(re.sub(r"[^A-Za-z0-9]", "", w["w"]))))
            if k: words[k - 1]["b"] = min(words[k - 1]["b"], w["a"])
    return words, s0, s1

def build():
    man = json.load(open(os.path.join(ROOT, "Assets/AI-Voice/manifest.json")))
    sents = man["sentences"]
    t = None; out = []; allw = []
    keys = [s["key"] for s in sents]
    for n, s in enumerate(sents):
        fn = os.path.join(ROOT, s["file"])
        words, s0, s1 = words_for(fn)
        if t is None:
            start = FIRST_WORD - s0
        else:
            start = t
            if s["key"] == "V8":
                if s["idx"] == 1:
                    start = kite_end + AFTER_KITE - s0
        # file placed so its speech begins at `start + s0`
        e = dict(s, start=round(start, 3), end=round(start + s["duration"], 3), speech0=round(start + s0, 3), speech1=round(start + s1, 3))
        out.append(e)
        for w in words:
            allw.append({"w": w["w"], "a": round(start + w["a"], 3), "b": round(start + w["b"], 3), "sent": f"{s['key']}-{s['idx']}", "seg": s["key"]})
        last_in_step = n == len(sents) - 1 or sents[n + 1]["key"] != s["key"]
        within = GAP_IN if s["idx"] == 1 else GAP_IN_LATER
        gap = GAP_AFTER.get(f"{s['key']}-{s['idx']}", GAP_AFTER.get(s["key"], within) if last_in_step else within)
        t = e["speech1"] + gap  # next file's speech starts here...
        if n + 1 < len(sents):
            nxt = os.path.join(ROOT, sents[n + 1]["file"])
            t -= speech_extent(nxt)[0]  # ...so shift by its leading silence
        if s["key"] == "V7":
            kite_start = e["speech1"] + KITE_LEAD
            kite_end = kite_start + KITE_DUR
    end = out[-1]["speech1"] + END_TAIL
    res = {"sentences": out, "kite": {"start": round(kite_start, 3), "end": round(kite_end, 3)}, "end": round(end, 3)}
    json.dump(res, open(os.path.join(HERE, "voice_timeline.json"), "w"), indent=1)
    json.dump(allw, open(os.path.join(HERE, "transcripts", "ai-voice-edit-words.json"), "w"), indent=0)
    return res, allw

if __name__ == "__main__":
    res, allw = build()
    for s in res["sentences"]:
        print(f"{s['key']}-{s['idx']}: {s['speech0']:7.2f}-{s['speech1']:7.2f}  {s['text'][:50]}")
    print("kite", res["kite"], "end", res["end"])
