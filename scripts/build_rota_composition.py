"""Generate the ROTA composition from one authoritative cut list.

Run from the project directory (hyperframes/rota). Audio levels, the music duck
envelope, the dialogue audio table and the caption table are not defined here:
they all come from assets/audio-plan.json, which scripts/prepare_rota_assets.py
writes, so the mix and the caption timing have one source of truth. Modeled
directly on scripts/build_seventeen_composition.py.

This film has NO synthesized narration: the voice is the generated performance
baked into the dialogue plates themselves. Each dialogue plate is staged with
its own audio intact and gets a muted <video> plus a separate <audio> pointing
at the same mp4 (per STORYBOARD.md's dialogue-audio table).
"""
import json
from pathlib import Path

DURATION = 36.6

# (n, role, start, duration, media-start) - picture cuts 1-8, from the cut list.
# Cut 9 (the close card) is authored separately below; it is not a video.
VIDEO_CUTS = [
    (1, 'hero', 0.0, 7.4, 0.0),
    (2, 'dough', 7.4, 2.2, 1.0),
    (3, 'lineb', 9.6, 3.8, 0.0),
    (4, 'rota', 13.4, 3.2, 0.6),
    (5, 'linec', 16.6, 5.8, 0.0),
    (6, 'room', 22.4, 2.2, 1.2),
    (7, 'lined', 24.6, 6.0, 0.0),
    (8, 'oven', 30.6, 2.0, 1.8),
]
CLOSE_AT, CLOSE_DUR = 32.6, 4.0
BRAND_MARK_END = CLOSE_AT  # brand mark on cuts 1-8 only, never on the close card
LOWER_THIRD_AT, LOWER_THIRD_DUR = 1.2, 4.0  # 1.2s to 5.2s
LOWER_THIRD_SLIDE = 0.3

plan = json.loads(Path('assets/audio-plan.json').read_text())
DIALOGUE_TRACKS = plan['dialogue_tracks']
CAPTION_SCHEDULE = plan['caption_schedule']

timeline = []
clips = []

# ---------------------------------------------------------------- picture cuts
for n, role, at, dur, media in VIDEO_CUTS:
    idx = n - 1
    clips.append(
        f'      <div data-hf-id="hf-w{n}" id="w-c{n}" class="inner">\n'
        f'        <video data-hf-id="hf-v{n}" id="v-c{n}" class="clip" src="assets/{role}.mp4"\n'
        f'          data-start="{at:.2f}" data-media-start="{media}" data-duration="{dur:.2f}"\n'
        f'          data-track-index="{idx}" muted playsinline></video>\n'
        f'      </div>')

# ---------------------------------------------------------------- close card (cut 9)
clips.append(f'''      <div data-hf-id="hf-wclose" id="screen-close" class="screen clip"
        data-start="{CLOSE_AT}" data-duration="{CLOSE_DUR}" data-track-index="8">
        <div data-hf-id="hf-closeblock" id="close-block">
          <div data-hf-id="hf-closewrap" id="close-wrap">
            <div data-hf-id="hf-closeword" id="close-word">rota</div>
            <i data-hf-id="hf-closerule" id="close-rule"></i>
          </div>
          <div data-hf-id="hf-closetag" id="close-tag">Shift scheduling for small teams.</div>
        </div>
      </div>''')
timeline.append(
    f"tl.fromTo('#screen-close',{{opacity:0}},{{opacity:1,duration:0.5,ease:'power2.inOut'}},{CLOSE_AT:.2f});")

# ---------------------------------------------------------------- brand mark (cuts 1-8 only)
clips.append(
    f'      <div data-hf-id="hf-brand" id="brand-mark" class="clip"\n'
    f'        data-start="0" data-duration="{BRAND_MARK_END:.2f}" data-track-index="20">rota</div>')

# ---------------------------------------------------------------- lower third (once, 1.2-5.2s)
clips.append(f'''      <div data-hf-id="hf-lt" id="lower-third" class="clip"
        data-start="{LOWER_THIRD_AT}" data-duration="{LOWER_THIRD_DUR}" data-track-index="21">
        <div data-hf-id="hf-ltplate" id="lt-plate">
          <div data-hf-id="hf-ltname" id="lt-name">Mara Osman</div>
          <div data-hf-id="hf-ltrole" id="lt-role">Owner, Second Shift Bakery</div>
        </div>
      </div>''')
timeline.append(
    f"tl.fromTo('#lt-plate',{{y:18,opacity:0}},{{y:0,opacity:1,duration:{LOWER_THIRD_SLIDE},"
    f"ease:'power2.out'}},{LOWER_THIRD_AT:.2f});")
timeline.append(
    f"tl.to('#lt-plate',{{y:18,opacity:0,duration:{LOWER_THIRD_SLIDE},ease:'power2.in'}},"
    f"{LOWER_THIRD_AT + LOWER_THIRD_DUR - LOWER_THIRD_SLIDE:.2f});")

# ---------------------------------------------------------------- captions (single element,
# pure function of the clock, empty string between spans)
timeline.append("var CAPS=" + json.dumps(CAPTION_SCHEDULE) + ",capLast=null;")
timeline.append(
    "tl.to({t:0},{t:1,duration:" + str(DURATION) + ",ease:'none',onUpdate:function(){"
    "var now=this.targets()[0].t*" + str(DURATION) + ";"
    "var active=null;for(var i=0;i<CAPS.length;i++){if(now>=CAPS[i]['in']&&now<CAPS[i].out){active=CAPS[i];}}"
    "var key=active?active.text:'';if(key===capLast){return;}capLast=key;"
    "document.getElementById('cap').textContent=key;"
    "}},0);")

# ---------------------------------------------------------------- audio: dialogue (kept audio,
# generated performance) plus one quiet score
audio = []
for i, row in enumerate(DIALOGUE_TRACKS):
    audio.append(
        f'      <audio data-hf-id="hf-a{row["track"].lower()}" id="a-{row["track"].lower()}" '
        f'src="assets/{row["src"]}" data-start="{row["data_start"]}" '
        f'data-media-start="{row["media_start"]}" data-duration="{row["duration"]}" '
        f'data-volume="1" data-track-index="{30 + i}"></audio>')
audio.append(
    f'      <audio data-hf-id="hf-ascore" id="a-score" src="assets/score.wav" data-start="0" '
    f'data-duration="{DURATION}" data-volume="{plan["score_volume"]}" data-track-index="40" '
    f"data-automation='{json.dumps(plan['music_automation'])}'></audio>")

html = f'''<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <script src="assets/gsap.min.js"></script>
    <style>
      *{{margin:0;padding:0;box-sizing:border-box}}
      html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#000}}
      body{{font-family:RotaSans,Arial,sans-serif}}
      @font-face{{font-family:RotaSerif;src:url('assets/RotaSerif.woff2') format('woff2')}}
      @font-face{{font-family:RotaSans;src:url('assets/RotaSans.ttf')}}
      @font-face{{font-family:RotaSans;src:url('assets/RotaSans-Bold.ttf');font-weight:700}}
      :root{{--crumb:#f3ede3;--crust:#3a2a1d;--proof:#1f5b3f;--paper:#ffffff;
        --shadow:rgba(24,16,10,.55);--footer-text:#c9ced3;--footer-bg:rgba(10,12,15,.9)}}
      #root{{width:1920px;height:1080px;overflow:hidden;position:relative;background:#000}}
      .inner{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}}
      .clip{{position:absolute;inset:0;width:1920px;height:1080px}}
      video.clip{{object-fit:cover}}

      .screen{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;background:var(--crumb)}}

      #close-block{{position:absolute;left:0;right:0;top:412px;text-align:center}}
      #close-wrap{{display:inline-block;text-align:center}}
      #close-word{{font-family:RotaSerif,serif;font-size:140px;color:var(--crust);line-height:1}}
      #close-rule{{display:block;width:100%;height:2px;background:var(--proof);margin-top:14px;
        font-style:normal}}
      #close-tag{{margin-top:40px;font-size:32px;color:var(--crust)}}

      #brand-mark{{font-family:RotaSerif,serif;font-size:34px;color:var(--paper);opacity:.62;
        padding:64px 0 0 96px;z-index:30;pointer-events:none}}

      #lower-third{{z-index:35;pointer-events:none}}
      #lt-plate{{position:absolute;left:96px;bottom:260px;background:var(--crumb);
        padding:24px 32px;min-width:420px}}
      #lt-name{{font-family:RotaSans,Arial,sans-serif;font-weight:700;font-size:40px;color:var(--crust)}}
      #lt-role{{font-family:RotaSans,Arial,sans-serif;font-size:27px;color:var(--crust);
        opacity:.7;margin-top:6px}}

      #cap{{position:absolute;bottom:120px;left:0;right:0;margin:0 auto;max-width:1480px;
        text-align:center;z-index:40;font-family:RotaSans,Arial,sans-serif;font-weight:700;
        font-size:46px;line-height:1.3;color:var(--paper);
        text-shadow:0 2px 10px var(--shadow),0 1px 3px var(--shadow)}}

      #footer{{position:absolute;right:64px;bottom:48px;z-index:100;font-size:19px;
        color:var(--footer-text);background:var(--footer-bg);padding:8px 14px}}
    </style>
  </head>
  <body>
    <div data-hf-id="hf-root" id="root" data-composition-id="rota" data-start="0" data-duration="{DURATION}" data-width="1920" data-height="1080">
{chr(10).join(clips)}

      <div data-hf-id="hf-cap" id="cap"></div>
      <div data-hf-id="hf-foot" id="footer">ORIGINAL CONCEPT / AI-GENERATED FILM</div>

{chr(10).join(audio)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + line for line in timeline)}
      window.__timelines['rota'] = tl;
    </script>
  </body>
</html>
'''
Path('index.html').write_text(html)
print(f'{len(VIDEO_CUTS)} video cuts + 1 close card, {len(DIALOGUE_TRACKS)} dialogue audio tracks, '
      f'{len(CAPTION_SCHEDULE)} caption rows, {len(timeline)} tween statements, {DURATION}s')
