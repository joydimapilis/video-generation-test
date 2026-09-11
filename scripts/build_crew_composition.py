"""Generate the CREW composition from one authoritative cut list.

Run from the project directory (hyperframes/crew). Audio levels, the music duck
envelope, the dialogue audio table and the caption table are not defined here:
they all come from assets/audio-plan.json, which scripts/prepare_crew_assets.py
writes, so the mix and the caption timing have one source of truth. Modeled
directly on scripts/build_rota_composition.py.

This film has NO synthesized narration: the voice is the generated performance
baked into the dialogue plates themselves. Each dialogue plate is staged with
its own audio intact and gets a muted <video> plus a separate <audio> pointing
at the same mp4 (per STORYBOARD.md's dialogue-audio table). Two authored
product screens (not generated ones) carry the product mechanic - real names,
real days, a real schedule filling in - because five loops have established
that no generative model spells reliably.
"""
import json
from pathlib import Path

DURATION = 44.4

# (n, role, start, duration, media-start) - the nine video picture cuts, from
# the cut list. Cuts 8/9 (the two product screens) and cut 12 (the close card)
# are authored separately below; they are not video.
VIDEO_CUTS = [
    (1, 'hero', 0.0, 7.3, 0.0),
    (2, 'dough', 7.3, 2.0, 1.0),
    (3, 'line2', 9.3, 3.3, 1.10),
    (4, 'paper', 12.6, 3.1, 0.6),
    (5, 'linec', 15.7, 5.6, 0.0),
    (6, 'room', 21.3, 1.7, 1.2),
    (7, 'line4', 23.0, 2.6, 0.0),
    (10, 'line6', 32.4, 6.0, 0.0),
    (11, 'oven', 38.4, 2.6, 1.8),
]
SCREEN_A_AT, SCREEN_A_DUR = 25.6, 2.6  # cut 8
SCREEN_B_AT, SCREEN_B_DUR = 28.2, 4.2  # cut 9
CLOSE_AT, CLOSE_DUR = 40.4, 4.0  # cut 12

# Brand mark on footage cuts ONLY - cuts 1-7 (one continuous block, 0.0-25.6)
# and cut 11 (38.4-40.4). Never on SCREEN A, SCREEN B (cuts 8/9, 25.6-32.4) or
# cut 10 (line6, 32.4-38.4) or the close card.
BRAND_WINDOWS = [(0.0, 25.6), (38.4, 2.0)]

LOWER_THIRD_AT, LOWER_THIRD_DUR = 1.2, 4.0  # 1.2s to 5.2s
LOWER_THIRD_SLIDE = 0.3

# SCREEN A rows, from STORYBOARD.md's Availability table.
SCREEN_A_ROWS = [
    ('Mara', 'All week'),
    ('Tomas', 'Mon-Thu'),
    ('Aisha', 'Not Thursday'),
    ('Joel', 'Evenings only'),
]
SCREEN_A_ROW_H = 86
SCREEN_A_TOP = 300
SCREEN_A_STAGGER_START = 0.15
SCREEN_A_STAGGER_STEP = 0.2
SCREEN_A_FADE = 0.22

# SCREEN B grid, from STORYBOARD.md's schedule table. Aisha is absent on
# Thursday and Tomas only appears Mon-Wed, matching what SCREEN A said they
# gave - a viewer who checks will check exactly that.
SCREEN_B_DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI']
SCREEN_B_ROWS = [
    ('OPEN', ['Mara', 'Mara', 'Tomas', 'Mara', 'Mara']),
    ('MID', ['Tomas', 'Aisha', 'Aisha', 'Tomas', 'Aisha']),
    ('CLOSE', ['Joel', 'Joel', 'Joel', 'Joel', 'Joel']),
]
SCREEN_B_LABEL_W = 200
SCREEN_B_GRID_W = 1500
SCREEN_B_COL_W = (SCREEN_B_GRID_W - SCREEN_B_LABEL_W) / 5
SCREEN_B_HEADER_H = 44
SCREEN_B_ROW_H = 96
SCREEN_B_TOP = 300
SCREEN_B_CELL_STAGGER_START = 0.2
SCREEN_B_CELL_STAGGER_STEP = 0.09
SCREEN_B_CELL_FADE = 0.14
SCREEN_B_UPDATED_AT = 2.3
SCREEN_B_UPDATED_FADE = 0.3

plan = json.loads(Path('assets/audio-plan.json').read_text())
DIALOGUE_TRACKS = plan['dialogue_tracks']
CAPTION_SCHEDULE = plan['caption_schedule']

# line3_pain_v2 (cut 5, linec) runs speech to 21.04, later than talk_c_v1 did;
# extend that caption's out-time so it doesn't drop before speech ends.
for _row in CAPTION_SCHEDULE:
    if _row['in'] == 15.70 and _row['out'] == 21.00:
        _row['out'] = 21.15

timeline = []
clips = []

# ---------------------------------------------------------------- picture cuts
for n, role, at, dur, media in VIDEO_CUTS:
    clips.append(
        f'      <div data-hf-id="hf-w{n}" id="w-c{n}" class="inner">\n'
        f'        <video data-hf-id="hf-v{n}" id="v-c{n}" class="clip" src="assets/{role}.mp4"\n'
        f'          data-start="{at:.2f}" data-media-start="{media}" data-duration="{dur:.2f}"\n'
        f'          data-track-index="{n - 1}" muted playsinline></video>\n'
        f'      </div>')

# ---------------------------------------------------------------- SCREEN A (cut 8, Availability)
a_rows_html = []
for i, (name, value) in enumerate(SCREEN_A_ROWS):
    top = SCREEN_A_TOP + i * SCREEN_A_ROW_H
    a_rows_html.append(
        f'        <div data-hf-id="hf-a-row{i}" id="a-row-{i}" class="a-row" style="top:{top}px">\n'
        f'          <div class="a-row-left"><span class="dot"></span>'
        f'<span class="a-name">{name}</span></div>\n'
        f'          <div class="a-value">{value}</div>\n'
        f'        </div>')
clips.append(f'''      <div data-hf-id="hf-screenA" id="screen-a" class="screen clip"
        data-start="{SCREEN_A_AT}" data-duration="{SCREEN_A_DUR}" data-track-index="7">
        <div data-hf-id="hf-a-mark" id="screen-a-mark" class="screen-mark">Crew</div>
        <div data-hf-id="hf-a-header" id="screen-a-header" class="panel-header-row">
          <div class="panel-heading">AVAILABILITY</div>
          <div class="panel-subheading">Week of 14 April</div>
        </div>
{chr(10).join(a_rows_html)}
      </div>''')
for i in range(len(SCREEN_A_ROWS)):
    at = round(SCREEN_A_AT + SCREEN_A_STAGGER_START + i * SCREEN_A_STAGGER_STEP, 3)
    timeline.append(
        f"tl.fromTo('#a-row-{i}',{{y:16,opacity:0}},{{y:0,opacity:1,duration:{SCREEN_A_FADE},"
        f"ease:'power2.out'}},{at});")

# ---------------------------------------------------------------- SCREEN B (cut 9, the schedule)
b_cells_html = []
idx = 0
for r, (row_label, names) in enumerate(SCREEN_B_ROWS):
    # Local to #screen-b-grid's own box (the container is already positioned
    # at top:SCREEN_B_TOP relative to the screen) - do not add SCREEN_B_TOP
    # again here, or rows render far below the container.
    row_top = SCREEN_B_HEADER_H + r * SCREEN_B_ROW_H
    b_cells_html.append(
        f'        <div class="b-row-label" style="top:{row_top}px;height:{SCREEN_B_ROW_H}px">'
        f'{row_label}</div>')
    for c, name in enumerate(names):
        left = SCREEN_B_LABEL_W + c * SCREEN_B_COL_W
        b_cells_html.append(
            f'        <div data-hf-id="hf-b-cell{idx}" id="b-cell-{idx}" class="b-cell" '
            f'style="top:{row_top}px;left:{left:.1f}px;width:{SCREEN_B_COL_W:.1f}px;'
            f'height:{SCREEN_B_ROW_H}px">{name}</div>')
        idx += 1
b_headers_html = []
for c, day in enumerate(SCREEN_B_DAYS):
    left = SCREEN_B_LABEL_W + c * SCREEN_B_COL_W
    b_headers_html.append(
        f'        <div class="b-day-header" style="left:{left:.1f}px;width:{SCREEN_B_COL_W:.1f}px">'
        f'{day}</div>')
clips.append(f'''      <div data-hf-id="hf-screenB" id="screen-b" class="screen clip"
        data-start="{SCREEN_B_AT}" data-duration="{SCREEN_B_DUR}" data-track-index="8">
        <div data-hf-id="hf-b-mark" id="screen-b-mark" class="screen-mark">Crew</div>
        <div data-hf-id="hf-b-header" id="screen-b-header" class="panel-header-row single">
          <div class="panel-heading">THIS WEEK'S SCHEDULE</div>
        </div>
        <div data-hf-id="hf-b-grid" id="screen-b-grid" style="top:{SCREEN_B_TOP}px;
          left:{(1920 - SCREEN_B_GRID_W) / 2:.1f}px;width:{SCREEN_B_GRID_W}px;
          height:{SCREEN_B_HEADER_H + 3 * SCREEN_B_ROW_H}px">
{chr(10).join(b_headers_html)}
{chr(10).join(b_cells_html)}
        </div>
        <div data-hf-id="hf-b-updated" id="screen-b-updated" class="updated-line">
          <span class="dot"></span><span>Updated - everyone notified</span>
        </div>
      </div>''')
idx = 0
for r, (row_label, names) in enumerate(SCREEN_B_ROWS):
    for c in range(len(names)):
        at = round(SCREEN_B_AT + SCREEN_B_CELL_STAGGER_START + idx * SCREEN_B_CELL_STAGGER_STEP, 3)
        timeline.append(
            f"tl.fromTo('#b-cell-{idx}',{{opacity:0}},{{opacity:1,duration:{SCREEN_B_CELL_FADE},"
            f"ease:'power2.out'}},{at});")
        idx += 1
timeline.append(
    f"tl.fromTo('#screen-b-updated',{{opacity:0}},{{opacity:1,duration:{SCREEN_B_UPDATED_FADE},"
    f"ease:'power2.out'}},{round(SCREEN_B_AT + SCREEN_B_UPDATED_AT, 3)});")

# ---------------------------------------------------------------- close card (cut 12)
clips.append(f'''      <div data-hf-id="hf-wclose" id="screen-close" class="screen close-screen clip"
        data-start="{CLOSE_AT}" data-duration="{CLOSE_DUR}" data-track-index="11">
        <div data-hf-id="hf-closeblock" id="close-block">
          <div data-hf-id="hf-closewrap" id="close-wrap">
            <div data-hf-id="hf-closeword" id="close-word">Crew</div>
            <i data-hf-id="hf-closerule" id="close-rule"></i>
          </div>
          <div data-hf-id="hf-closetag" id="close-tag">Staff scheduling for small teams.</div>
        </div>
      </div>''')
timeline.append(
    f"tl.fromTo('#screen-close',{{opacity:0}},{{opacity:1,duration:0.5,ease:'power2.inOut'}},{CLOSE_AT:.2f});")

# ---------------------------------------------------------------- brand mark (footage cuts only:
# cuts 1-7 as one continuous block, then cut 11 - never on the screens, cut 10 or the close card)
for i, (at, dur) in enumerate(BRAND_WINDOWS):
    clips.append(
        f'      <div data-hf-id="hf-brand{i}" id="brand-mark-{i}" class="clip brand-mark"\n'
        f'        data-start="{at:.2f}" data-duration="{dur:.2f}" data-track-index="20">Crew</div>')

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
# pure function of the clock, empty string between spans). Rendered over BOTH footage and the
# dark product screens, so #cap carries a z-index above the screens (see CSS).
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
      body{{font-family:CrewSans,Arial,sans-serif}}
      @font-face{{font-family:CrewSerif;src:url('assets/CrewSerif.woff2') format('woff2')}}
      @font-face{{font-family:CrewSans;src:url('assets/CrewSans.ttf')}}
      @font-face{{font-family:CrewSans;src:url('assets/CrewSans-Bold.ttf');font-weight:700}}
      :root{{--crumb:#f3ede3;--crust:#3a2a1d;--proof:#1f5b3f;--panel:#1a1410;
        --panel-ink:#f0e9de;--panel-dim:#9b8e80;--panel-line:#332a22;--paper:#ffffff;
        --shadow:rgba(24,16,10,.55);--footer-text:#c9ced3;--footer-bg:rgba(10,12,15,.9)}}
      #root{{width:1920px;height:1080px;overflow:hidden;position:relative;background:#000}}
      .inner{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}}
      .clip{{position:absolute;inset:0;width:1920px;height:1080px}}
      video.clip{{object-fit:cover}}

      .screen{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;background:var(--panel)}}
      .screen-mark{{position:absolute;top:72px;left:72px;font-family:CrewSerif,serif;font-size:30px;
        color:var(--panel-dim)}}
      .panel-header-row{{position:absolute;top:168px;left:72px;right:72px;display:flex;
        justify-content:space-between;align-items:baseline}}
      .panel-header-row.single{{justify-content:flex-start}}
      .panel-heading{{font-family:CrewSans,Arial,sans-serif;font-size:26px;letter-spacing:.18em;
        color:var(--panel-dim)}}
      .panel-subheading{{font-family:CrewSans,Arial,sans-serif;font-size:24px;color:var(--panel-dim)}}

      .a-row{{position:absolute;left:{(1920 - 1300) / 2:.1f}px;width:1300px;height:{SCREEN_A_ROW_H}px;
        display:flex;align-items:center;justify-content:space-between;
        border-bottom:1px solid var(--panel-line)}}
      .a-row-left{{display:flex;align-items:center;gap:24px}}
      .dot{{width:10px;height:10px;border-radius:50%;background:var(--proof);display:inline-block;
        flex:none}}
      .a-name{{font-family:CrewSans,Arial,sans-serif;font-size:34px;color:var(--panel-ink)}}
      .a-value{{font-family:CrewSans,Arial,sans-serif;font-size:30px;color:var(--panel-dim);
        text-align:right}}

      #screen-b-grid{{position:absolute}}
      .b-day-header{{position:absolute;top:0;height:{SCREEN_B_HEADER_H}px;text-align:center;
        font-family:CrewSans,Arial,sans-serif;font-size:24px;color:var(--panel-dim);
        border-bottom:1px solid var(--panel-line);display:flex;align-items:center;
        justify-content:center}}
      .b-row-label{{position:absolute;left:0;width:{SCREEN_B_LABEL_W}px;display:flex;
        align-items:center;font-family:CrewSans,Arial,sans-serif;font-size:24px;
        color:var(--panel-dim)}}
      .b-cell{{position:absolute;display:flex;align-items:center;justify-content:center;
        font-family:CrewSans,Arial,sans-serif;font-size:30px;color:var(--panel-ink)}}
      .updated-line{{position:absolute;left:0;right:0;top:670px;text-align:center;display:flex;
        align-items:center;justify-content:center;gap:14px;font-family:CrewSans,Arial,sans-serif;
        font-size:28px;color:var(--panel-ink)}}

      .close-screen{{background:var(--crumb)}}
      #close-block{{position:absolute;left:0;right:0;top:412px;text-align:center}}
      #close-wrap{{display:inline-block;text-align:center}}
      #close-word{{font-family:CrewSerif,serif;font-size:140px;color:var(--crust);line-height:1}}
      #close-rule{{display:block;width:100%;height:2px;background:var(--proof);margin-top:14px;
        font-style:normal}}
      #close-tag{{margin-top:40px;font-family:CrewSans,Arial,sans-serif;font-size:32px;
        color:var(--crust)}}

      .brand-mark{{font-family:CrewSerif,serif;font-size:34px;color:var(--paper);opacity:.62;
        padding:64px 0 0 96px;z-index:30;pointer-events:none}}

      #lower-third{{z-index:35;pointer-events:none}}
      #lt-plate{{position:absolute;left:96px;bottom:260px;background:var(--crumb);
        padding:24px 32px;min-width:420px}}
      #lt-name{{font-family:CrewSans,Arial,sans-serif;font-weight:700;font-size:40px;color:var(--crust)}}
      #lt-role{{font-family:CrewSans,Arial,sans-serif;font-size:27px;color:var(--crust);
        opacity:.7;margin-top:6px}}

      #cap{{position:absolute;bottom:120px;left:0;right:0;margin:0 auto;max-width:1480px;
        text-align:center;z-index:40;font-family:Arial,sans-serif;font-weight:700;
        font-size:46px;line-height:1.3;color:var(--paper);
        text-shadow:0 2px 10px var(--shadow),0 1px 3px var(--shadow)}}

      #footer{{position:absolute;right:64px;bottom:48px;z-index:100;font-size:19px;
        color:var(--footer-text);background:var(--footer-bg);padding:8px 14px}}
    </style>
  </head>
  <body>
    <div data-hf-id="hf-root" id="root" data-composition-id="crew" data-start="0" data-duration="{DURATION}" data-width="1920" data-height="1080">
{chr(10).join(clips)}

      <div data-hf-id="hf-cap" id="cap"></div>
      <div data-hf-id="hf-foot" id="footer">ORIGINAL CONCEPT / AI-GENERATED FILM</div>

{chr(10).join(audio)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + line for line in timeline)}
      window.__timelines['crew'] = tl;
    </script>
  </body>
</html>
'''
Path('index.html').write_text(html)
print(f'{len(VIDEO_CUTS)} video cuts + 2 screens + 1 close card, {len(DIALOGUE_TRACKS)} dialogue audio tracks, '
      f'{len(CAPTION_SCHEDULE)} caption rows, {len(timeline)} tween statements, {DURATION}s')
