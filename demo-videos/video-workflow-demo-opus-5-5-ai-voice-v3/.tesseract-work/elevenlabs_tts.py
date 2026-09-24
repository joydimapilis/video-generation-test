#!/usr/bin/env python3
"""Narrate the script with ElevenLabs (one request per sentence).

Reads ELEVENLABS_API_KEY from the environment (never written to disk or logs).
For each sentence it calls /v1/text-to-speech/{voice}/with-timestamps, passing the
neighbouring sentences of the same chapter as previous_text / next_text so the
intonation flows across sentence files. Saves the MP3 exactly as returned, a WAV
decode, and ElevenLabs' character alignment (used for word timings).
Existing files are skipped, so re-runs cost no characters. Use --force KEY to redo one.
Run from the project root.
"""
import base64, json, os, subprocess, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_lines import STEPS

VOICE_ID, VOICE_NAME = "hpp4J3VqNfWAUOO0d1Us", "Bella - Professional, Bright, Warm"
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True, "speed": 1.0}
FMT = "mp3_44100_128"
OUT = "Assets/AI-Voice"
force = set(sys.argv[sys.argv.index("--force") + 1:]) if "--force" in sys.argv else set()

key = os.environ.get("ELEVENLABS_API_KEY", "")
if not key.startswith("sk_"):
    sys.exit("ELEVENLABS_API_KEY missing or not an sk_ secret key")

manifest = []
for chapter, lines in STEPS:
    texts = [t for t, _ in lines]
    for i, (text, say) in enumerate(lines):
        name = f"{chapter}-{i + 1}"
        mp3, wav, aln = f"{OUT}/elevenlabs-mp3/{name}.mp3", f"{OUT}/sentences/{name}.wav", f"{OUT}/alignment/{name}.json"
        os.makedirs(os.path.dirname(mp3), exist_ok=True)
        body = {"text": say or text, "model_id": MODEL, "voice_settings": SETTINGS}
        if i > 0: body["previous_text"] = " ".join(texts[:i])
        if i + 1 < len(texts): body["next_text"] = " ".join(texts[i + 1:])
        if not os.path.exists(mp3) or name in force:
            req = urllib.request.Request(
                f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format={FMT}",
                data=json.dumps(body).encode(), method="POST",
                headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    res = json.load(r); req_id = r.headers.get("request-id")
            except urllib.error.HTTPError as e:
                sys.exit(f"{name}: HTTP {e.code} {e.read().decode()[:400]}")
            open(mp3, "wb").write(base64.b64decode(res["audio_base64"]))
            json.dump({"alignment": res.get("alignment"), "normalized_alignment": res.get("normalized_alignment"),
                       "request_id": req_id}, open(aln, "w"))
            print("synthesized", name, flush=True)
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", mp3, "-ac", "1", "-c:a", "pcm_s24le", wav], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav],
                                   capture_output=True, text=True).stdout)
        manifest.append({"key": chapter, "idx": i + 1, "text": text, "said": say or text, "file": wav,
                         "mp3": mp3, "alignment": aln, "duration": round(dur, 3)})
json.dump({"service": "ElevenLabs", "voice_id": VOICE_ID, "voice": VOICE_NAME, "model": MODEL,
           "voice_settings": SETTINGS, "output_format": FMT, "context": "previous_text/next_text = rest of the chapter",
           "sentences": manifest}, open(f"{OUT}/manifest.json", "w"), indent=1)
print("sentences", len(manifest), "total seconds", round(sum(m["duration"] for m in manifest), 2))
