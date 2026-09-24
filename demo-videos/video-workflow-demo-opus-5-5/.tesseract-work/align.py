"""Per-segment whisper token timing mapped to the edit clock, with segment
starts snapped to measured speech onsets. Writes transcripts/edit-words.json."""
import json, subprocess, os
from plan import timeline, A
from rms import rms_profile
M = "/Users/joydimapilis/.cache/hyperframes/whisper/models/ggml-small.en.bin"
tl, total = timeline()
allw = []
for s in tl:
    if s['key'].startswith('KITE'): continue
    wav = f"transcripts/seg-{s['key']}.wav"
    subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-ss",str(s['src_in']),"-to",str(s['src_out']),"-i",A+s['file'],"-ac","1","-ar","16000",wav],check=True)
    subprocess.run(["whisper-cli","-m",M,"-f",wav,"-ojf","-of",wav[:-4],"-np"],capture_output=True)
    d = json.load(open(wav[:-4]+".json"))
    prof = rms_profile(A+s['file'], s['src_in'], s['src_out']-s['src_in'], 0.01)
    onsets = [i*0.01 for i in range(1,len(prof)) if prof[i] > -40 and max(prof[max(0,i-12):i]) < -44]
    words = []
    for seg in d['transcription']:
        first = True
        for t in seg['tokens']:
            tx = t['text']
            if tx.startswith('[') or tx.startswith('<'): continue
            a, b = t['offsets']['from']/1000, t['offsets']['to']/1000
            if tx.startswith(' ') or not words:
                if first:
                    cand = [o for o in onsets if o >= a - 0.6]
                    if cand: a = max(a, cand[0]) if cand[0] - a < 0.8 else a
                words.append({"w": tx.strip(), "a": a, "b": b, "seg": s['key']}); first = False
            else:
                words[-1]["w"] += tx; words[-1]["b"] = b
    for w in words:
        w["a"] = round(s['start'] + w["a"], 3); w["b"] = round(s['start'] + w["b"], 3)
    allw += words
json.dump(allw, open("transcripts/edit-words.json","w"), indent=0)
line=""
for w in allw:
    line += f"{w['w']}@{w['a']:.2f} "
print(line)
