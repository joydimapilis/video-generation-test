# Save the Learnings — Tesseract editing test

Open **Save-the-Learnings.mp4** to review the 20-second, 1920×1080, 30 fps edit.
**Save-the-Learnings.tsrct** is the matching portable editable Tesseract project.
All required media and font bytes are embedded, and original source copies are
preserved in `Assets/`. `Captions.srt` is an optional subtitle sidecar; the MP4
already contains the captions. `Previews/Final-encoded-filmstrip.png` shows the
export in chronological one-second samples.

The edit uses only the supplied screen recording and narration. It trims empty
head/tail audio, retains natural internal pauses and original speaking speed,
repositions the screen, holds original frames to make sections readable, and
adds eleven editable phrase captions. One short vertical pan brings the
“Final learnings” heading into view. No generated footage, added music, sound
effects, fabricated UI, or rewritten narration.

Checks: all 600 video frames decode; H.264 video and stereo AAC audio; source
copies match attachments byte-for-byte; caption text matches the supplied
script; native filmstrips and final encoded samples visually inspected.
Narration comparison correlation: 0.9966, with the export about 21 ms earlier
than the expected source trim (less than one frame). No clipped decoded samples.
Final audio: -16.42 LUFS integrated, -1.33 dBTP. Kept the modest +2.2 dB gain
instead of further compressing the original recording to raise loudness.

Review limit: the agent could not independently listen or watch real-time
playback. Speech and caption timing were assessed using local transcription,
waveforms, frame inspection, and signal comparison. Please listen to the MP4
for natural pacing and voice quality. The source does not show the completion
check executing, so that statement remains narration over the supplied document.

`Save-the-Learnings.reverse-engineering.md` records the cut, source ranges,
methods, correction, and limitations. Retained editable JSON, actions, local
transcripts, and verification reports are in `.tesseract-work/`.

To export again from the Reykjavik workspace root:

```sh
./scripts/tsrct export --project save-the-learnings/Save-the-Learnings.tsrct --fps 30 --resolution 1080p --output save-the-learnings/Save-the-Learnings.mp4
```
