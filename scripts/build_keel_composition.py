"""Generate the KEEL montage composition from one authoritative cut list.

Run from the project directory (hyperframes/keel). Audio levels, the music duck
envelope and the SFX cues are not defined here: they come from assets/audio-plan.json,
which scripts/prepare_keel_assets.py writes, so the mix has one source of truth.
"""
import json
from pathlib import Path

# (id, source role, timeline in, duration, media-start, act)
CUTS = [
    ('a1', 'street',  0.00, 1.60, 0.6, 1), ('a2', 'transit', 1.60, 1.30, 0.4, 1),
    ('a3', 'servers', 2.90, 1.20, 0.3, 1), ('a4', 'typing',  4.10, 1.20, 0.8, 1),
    ('a5', 'street',  5.30, 0.90, 3.2, 1), ('a6', 'transit', 6.20, 0.90, 3.0, 1),
    ('a7', 'servers', 7.10, 0.75, 3.4, 1), ('a8', 'typing',  7.85, 0.45, 4.2, 1),
    ('b1', 'surface', 8.55, 4.05, 0.5, 2), ('b2', 'descend', 12.20, 4.20, 0.4, 2),
    ('b3', 'deep',    16.00, 4.20, 0.6, 2),
    ('c1', 'shed',    19.80, 4.20, 0.6, 3), ('c2', 'plane',  23.60, 4.80, 0.5, 3),
    ('c3', 'keel',    28.00, 4.80, 0.4, 3),
]
FLASH_CUTS = ['a3', 'a5', 'a7']
CROSSFADE = 0.40
# shop_wide carries 92px baked-in letterbox bars; this crops them out.
PLATE_SCALE = {'shed': 1.21}

VO = [('l01', 0.80, 1.813, 'Everything gets faster.'),
      ('l02', 2.80, 2.837, 'Faster to launch. Faster to scale.'),
      ('l03', 5.90, 1.685, 'Faster to forget.'),
      ('l04', 9.00, 3.200, 'But nothing that lasts is built at the surface.'),
      ('l05', 16.30, 2.880, "It's built underneath. Slow. Quiet."),
      ('l06', 20.60, 2.133, 'Where nobody is watching.'),
      ('l07', 26.50, 1.536, "That's where we work.")]

DURATION = 38.0
CLOSE_IN = 32.40

clips, timeline = [], []
for index, (cid, role, at, dur, media, act) in enumerate(CUTS):
    scale = PLATE_SCALE.get(role, 1.0)
    clips.append(
        f'      <div data-hf-id="hf-w{cid}" id="w-{cid}" class="inner">\n'
        f'        <video data-hf-id="hf-v{cid}" id="v-{cid}" class="clip" src="assets/{role}.mp4"\n'
        f'          data-start="{at:.2f}" data-media-start="{media}" data-duration="{dur:.2f}"\n'
        f'          data-track-index="{index}" data-layout-allow-overflow muted playsinline></video>\n'
        f'      </div>')
    if scale != 1.0:
        timeline.append(f"tl.set('#v-{cid}',{{scale:{scale}}},{at:.2f});")
    if act == 1:
        # Whip-slide entry: the wrapper carries the move, never the timed clip.
        timeline.append(
            f"tl.fromTo('#w-{cid}',{{xPercent:{'7' if index % 2 == 0 else '-7'},scale:1.06}},"
            f"{{xPercent:0,scale:1,duration:.16,ease:'power3.out'}},{at:.2f});")
    else:
        # Opposing opacity envelopes; the outgoing clip simply ends under it.
        fade = 0.001 if cid == 'b1' else CROSSFADE
        timeline.append(
            f"tl.fromTo('#w-{cid}',{{opacity:0}},{{opacity:1,duration:{fade},ease:'power1.inOut'}},{at:.2f});")

for cid in FLASH_CUTS:
    at = next(c[2] for c in CUTS if c[0] == cid)
    timeline.append(f"tl.fromTo('#flash',{{opacity:.26}},{{opacity:0,duration:.09,ease:'power2.in'}},{at:.2f});")

captions = ['      <div data-hf-id="hf-cap" id="cap"></div>']
# Opacity is tweened; the words come from a table read as a pure function of time,
# so a forward or reverse seek always resolves to the same caption.
for index, (name, at, length, text) in enumerate(VO):
    next_at = VO[index + 1][1] if index + 1 < len(VO) else DURATION
    end = min(at + length + 0.24, next_at - 0.30)
    timeline.append(
        f"tl.fromTo('#cap',{{opacity:0,y:12}},{{opacity:1,y:0,duration:.2,ease:'power2.out'}},{at - 0.10:.2f});")
    if end > at + 0.3:
        timeline.append(f"tl.to('#cap',{{opacity:0,duration:.2,ease:'power2.in'}},{end:.2f});")
CAPTION_TABLE = [{'at': at, 'text': text} for _, at, _, text in VO]

audio = [
    f'      <audio data-hf-id="hf-avo" id="a-vo" src="assets/voice.wav" data-start="0" '
    f'data-duration="{DURATION}" data-volume="1" data-track-index="60"></audio>']
plan = json.loads(Path('assets/audio-plan.json').read_text())
audio.append(
    f'      <audio data-hf-id="hf-amu" id="a-score" src="assets/score.wav" data-start="0" '
    f'data-duration="{DURATION}" data-volume="{plan["score_volume"]}" data-track-index="61" '
    f"data-automation='{json.dumps(plan['music_automation'])}'></audio>")
for tag, cue in enumerate(plan['sfx_cues']):
    audio.append(
        f'      <audio data-hf-id="hf-ax{tag}" id="a-sfx{tag}" src="assets/{cue["src"]}" '
        f'data-start="{cue["at"]}" data-duration="{cue["duration"]}" '
        f'data-volume="{cue["volume"]}" data-track-index="{70 + tag}"></audio>')

timeline.append(
    "var CAPS=" + json.dumps(CAPTION_TABLE) + ",capState={t:0},capLast=null;")
timeline.append(
    "tl.to(capState,{t:" + str(DURATION) + ",duration:" + str(DURATION) + ",ease:'none',onUpdate:function(){"
    "var text='';for(var i=0;i<CAPS.length;i++){if(capState.t>=CAPS[i].at-0.34){text=CAPS[i].text;}}"
    "if(text===capLast){return;}capLast=text;document.getElementById('cap').textContent=text;}},0);")
timeline += [
    # The turn: the only empty frame in the film.
    "tl.fromTo('#blackout',{opacity:0},{opacity:1,duration:.2,ease:'power2.in'},8.05);",
    "tl.to('#blackout',{opacity:0,duration:.32,ease:'power2.out'},8.5);",
    "tl.fromTo('#close',{opacity:0},{opacity:1,duration:.42,ease:'power2.inOut'},32.40);",
    "tl.fromTo('#close-mark',{opacity:0,y:26},{opacity:1,y:0,duration:.5,ease:'power4.out'},32.90);",
    "tl.fromTo('#close-rule',{scaleX:0},{scaleX:1,duration:.55,ease:'power2.out'},33.50);",
    "tl.fromTo('#close-tag',{opacity:0,y:12},{opacity:1,y:0,duration:.42,ease:'power2.out'},33.95);",
    "tl.fromTo('#close-kick',{opacity:0},{opacity:1,duration:.4,ease:'power2.out'},34.60);",
]

html = f'''<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <script src="assets/gsap.min.js"></script>
    <style>
      *{{margin:0;padding:0;box-sizing:border-box}}
      html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#05070a}}
      body{{font-family:KeelSans,Arial,sans-serif}}
      @font-face{{font-family:KeelSerif;src:url('assets/KeelSerif.ttf')}}
      @font-face{{font-family:KeelSerif;src:url('assets/KeelSerif-Bold.ttf');font-weight:700}}
      @font-face{{font-family:KeelSans;src:url('assets/KeelSans.ttf')}}
      @font-face{{font-family:KeelSans;src:url('assets/KeelSans-Bold.ttf');font-weight:700}}
      #root{{width:1920px;height:1080px;overflow:hidden;position:relative}}
      .inner{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}}
      .clip{{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover}}
      #flash{{position:absolute;inset:0;z-index:30;background:#9fe8ff;opacity:0;pointer-events:none}}
      #blackout{{position:absolute;inset:0;z-index:31;background:#05070a;opacity:0;pointer-events:none}}
      #capscrim{{position:absolute;left:0;right:0;bottom:0;height:340px;z-index:32;pointer-events:none;
        background:linear-gradient(0deg,rgba(5,7,10,.86) 0%,rgba(5,7,10,.42) 46%,rgba(5,7,10,0) 100%)}}
      #cap{{position:absolute;left:240px;right:240px;bottom:148px;z-index:33;text-align:center;
        font-family:KeelSans,Arial,sans-serif;font-size:44px;line-height:1.35;color:#f2efe9;opacity:0}}
      #footer{{position:absolute;right:72px;bottom:64px;z-index:36;font-family:KeelSans,Arial,sans-serif;
        font-size:19px;letter-spacing:.18em;color:#cfcbc3;background:rgba(5,7,10,.9);padding:8px 14px}}
      #close{{position:absolute;inset:0;z-index:35;background:#05070a;opacity:0}}
      #close-glow{{position:absolute;left:50%;top:50%;width:1600px;height:1600px;margin:-800px 0 0 -800px;
        background:radial-gradient(circle,rgba(200,162,92,.11) 0%,rgba(200,162,92,0) 60%)}}
      #close-mark{{position:absolute;left:0;right:0;top:392px;text-align:center;font-family:KeelSerif,Georgia,serif;
        font-weight:700;font-size:172px;letter-spacing:.02em;line-height:1;color:#f2efe9;opacity:0}}
      #close-rule{{position:absolute;left:50%;top:606px;width:360px;margin-left:-180px;height:1px;background:#c8a25c}}
      #close-tag{{position:absolute;left:0;right:0;top:654px;text-align:center;font-family:KeelSerif,Georgia,serif;
        font-size:46px;letter-spacing:.01em;color:#f2efe9;opacity:0}}
      #close-kick{{position:absolute;left:0;right:0;top:744px;text-align:center;font-family:KeelSans,Arial,sans-serif;
        font-size:21px;letter-spacing:.24em;color:#8d8880;opacity:0}}
    </style>
  </head>
  <body>
    <div data-hf-id="hf-root" id="root" data-composition-id="keel" data-start="0" data-duration="{DURATION}" data-width="1920" data-height="1080">
{chr(10).join(clips)}

      <div data-hf-id="hf-flash" id="flash"></div>
      <div data-hf-id="hf-black" id="blackout"></div>
      <div data-hf-id="hf-scrim" id="capscrim"></div>
{chr(10).join(captions)}
      <div data-hf-id="hf-foot" id="footer">ORIGINAL CONCEPT / AI-GENERATED FILM</div>

      <div data-hf-id="hf-close" id="close">
        <div data-hf-id="hf-cg" id="close-glow" data-layout-allow-overflow></div>
        <div data-hf-id="hf-cm" id="close-mark">KEEL</div>
        <i data-hf-id="hf-cr" id="close-rule"></i>
        <div data-hf-id="hf-ct" id="close-tag">Built below the waterline.</div>
        <div data-hf-id="hf-ck" id="close-kick">LONG-HORIZON INFRASTRUCTURE</div>
      </div>

{chr(10).join(audio)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + line for line in timeline)}
      window.__timelines['keel'] = tl;
    </script>
  </body>
</html>
'''
Path('index.html').write_text(html)
print(f'{len(CUTS)} cuts, {len(VO)} captions, {len(timeline)} tween statements, {DURATION}s')
