"""Synthesize the supplied script with the local Kokoro-82M model (offline).
Usage: python synth.py VOICE SPEED OUTDIR  -> one 24 kHz WAV per sentence."""
import json, os, sys
import kokoro_onnx, soundfile as sf
M = os.path.expanduser("~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx")
V = os.path.expanduser("~/.cache/hyperframes/tts/voices/voices-v1.0.bin")
SENTENCES = [
    "For every finished video, the system creates its own reverse-engineering document.",
    "This records how the video was made, including the prompts, structure, methods used, revisions, and key learnings.",
    "The workflow also checks that this file exists before the video can be marked complete.",
]
voice, speed, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
os.makedirs(out, exist_ok=True)
k = kokoro_onnx.Kokoro(M, V)
info = []
for i, s in enumerate(SENTENCES, 1):
    samples, sr = k.create(s, voice=voice, speed=speed, lang="en-us")
    p = os.path.join(out, f"sentence-{i}.wav")
    sf.write(p, samples, sr)
    info.append({"file": p, "text": s, "sampleRate": sr, "seconds": round(len(samples) / sr, 3)})
print(json.dumps({"voice": voice, "speed": speed, "sentences": info}, indent=1))
