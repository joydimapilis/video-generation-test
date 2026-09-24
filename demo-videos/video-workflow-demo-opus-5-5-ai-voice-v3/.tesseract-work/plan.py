"""Shared edit plan: narration takes (source seconds) and the Kite playback.

Every narration segment is butted against the next, so every pause in the edit
is the speaker's own room tone (no digital silence inside the voice track).
"""
A = "../Assets/Source/Audio/"
VOICE = [  # (key, asset, file, src_in, src_out, note)
    ("V1",  "vo1",   "Step 1.m4a",            1.80, 15.00, "Step 1, only take"),
    ("V2",  "vo2",   "Step 2.m4a",            1.70, 16.15, "Step 2, only take (tail extended for the completion hold)"),
    ("V3",  "vo3",   "Step 3.m4a",            2.00, 19.05, "Step 3, only take"),
    ("V4a", "vo4",   "Step 4 and part 2.m4a", 2.15, 14.15, "Step 4 sentences 1-2"),
    ("V4b", "vo4",   "Step 4 and part 2.m4a", 31.62, 49.25, "Step 4 'Here I'm showing' retake + HyperFrames line"),
    ("V4c", "vo4p3", "Step 4_Part 3.m4a",     15.72, 30.28, "Step 4 'For other videos' + 'The idea is'"),
    ("V5",  "vo5",   "Step 5.m4a",            40.95, 54.10, "Step 5, third (last) complete take"),
    ("V6",  "vo6",   "Step 6.m4a",            1.75, 20.90, "Step 6, only take"),
    ("V7",  "vo7",   "Step 7.m4a",            1.85, 5.95, "Step 7, first take ('produced through')"),
    ("KITE", None, None, None, None, "Kite final video playback from Step 7.mov"),
    ("V8",  "vo8",   "Step 8.m4a",            9.85, 23.40, "Step 8, second take (after 'Okay.')"),
]
# Kite final video inside Step 7.mov: plays 9.00-9.722, paused (cut out), resumes 11.665-46.90.
KITE_PARTS = [(9.00, 9.722), (11.665, 46.90)]  # pause fade starts 9.722; playback resumes 11.665 (sound: Assets/Derived/Kite-soundtrack-pause-removed.wav)
KITE_LEAD = 0.25     # beat between "...that workflow." and the fullscreen video
KITE_TAIL = 0.45     # after the video ends, before Step 8 narration head
START_PAD = 0.0
END_PAD = 1.2        # hold after the last word's tail before the end

def timeline():
    t = START_PAD; out = []
    for key, asset, fn, a, b, note in VOICE:
        if key == "KITE":
            t += KITE_LEAD
            for i, (s, e) in enumerate(KITE_PARTS):
                out.append(dict(key=f"KITE{i}", src_in=s, src_out=e, start=t, end=t + (e - s)))
                t += e - s
            t += KITE_TAIL
            continue
        out.append(dict(key=key, asset=asset, file=fn, src_in=a, src_out=b, start=t, end=t + b - a, note=note))
        t += b - a
    return out, t + END_PAD

if __name__ == "__main__":
    tl, total = timeline()
    for s in tl:
        print(f"{s['key']:6} edit {s['start']:7.2f}-{s['end']:7.2f}  src {s['src_in']:.2f}-{s['src_out']:.2f}")
    print("total", round(total, 2))
