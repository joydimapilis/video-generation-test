"""Synthesize every script sentence locally with Kokoro v1.0 (voice af_heart)."""
import json, os, sys
import kokoro_onnx, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from script_lines import STEPS
C = os.path.expanduser("~/.cache/hyperframes/tts")
VOICE, SPEED = "af_heart", 1.0
model = kokoro_onnx.Kokoro(f"{C}/models/kokoro-v1.0.onnx", f"{C}/voices/voices-v1.0.bin")
out = "Assets/AI-Voice/sentences"; os.makedirs(out, exist_ok=True)
manifest = []
for key, lines in STEPS:
    for i, (text, say) in enumerate(lines):
        samples, sr = model.create(say or text, voice=VOICE, speed=SPEED, lang="en-us")
        fn = f"{out}/{key}-{i + 1}.wav"
        sf.write(fn, samples, sr)
        manifest.append({"key": key, "idx": i + 1, "text": text, "said": say or text, "file": fn,
                         "duration": round(len(samples) / sr, 3), "sampleRate": sr})
        print(fn, round(len(samples) / sr, 2))
json.dump({"model": "kokoro-v1.0.onnx", "voice": VOICE, "speed": SPEED, "sentences": manifest},
          open("Assets/AI-Voice/manifest.json", "w"), indent=1)
