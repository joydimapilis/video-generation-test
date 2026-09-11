"""Generate the SEVENTEEN composition from one authoritative cut list.

Run from the project directory (hyperframes/seventeen). Audio levels, the music
duck envelope, the SFX cues and the measured narration schedule are not defined
here: they come from assets/audio-plan.json, which
scripts/prepare_seventeen_assets.py writes, so the mix and the caption timing
have one source of truth. Modeled directly on scripts/build_keel_composition.py.
"""
import json
from pathlib import Path

DURATION = 42.0

# (id, role, start, duration, media-start) - generated-footage cuts.
VIDEO_CUTS = [
    ('c01', 'hero',   0.0,  3.4, 0.3),
    ('c04', 'hands',  9.6,  1.6, 3.0),
    ('c05', 'lookup', 11.2, 2.8, 2.2),
    ('c06', 'rain',   14.0, 2.0, 1.0),
    ('c07', 'coffee', 16.0, 1.8, 1.2),
    ('c08', 'desk',   17.8, 1.8, 1.0),
    ('c11', 'react',  27.2, 4.2, 1.4),
    ('c13', 'exhale', 34.8, 3.4, 1.8),
    ('c14', 'city',   38.2, 1.8, 1.6),
]
CITY_SCALE = 1.36
# Global timeline order for data-track-index (matches the cut table 1-15).
TRACK_INDEX = {'c01': 0, 'a': 1, 'b': 2, 'c04': 3, 'c05': 4, 'c06': 5, 'c07': 6,
               'c08': 7, 'c': 8, 'd': 9, 'c11': 10, 'e': 11, 'c13': 12, 'c14': 13,
               'f': 14}

WIPE_DURATION = 0.18

plan = json.loads(Path('assets/audio-plan.json').read_text())
VO = plan['vo_schedule']  # [{file, start, duration, text}], measured durations.


def vo(index):
    return VO[index]


timeline = []
clips = []


def add_wipe(el_id, at):
    """0.18s paper wipe from the left, reading as a screen repainting."""
    timeline.append(
        f"tl.fromTo('#{el_id}',{{clipPath:'inset(0 100% 0 0)'}},"
        f"{{clipPath:'inset(0 0 0 0)',duration:{WIPE_DURATION},ease:'power2.out'}},{at:.2f});")


def chrome_bar(prefix):
    return (f'        <i data-hf-id="hf-{prefix}cb" id="{prefix}-chrome" class="chrome-bar"></i>\n'
            f'        <div data-hf-id="hf-{prefix}cl" id="{prefix}-chrome-label" class="chrome-label">tuesday.app</div>\n')


# ---------------------------------------------------------------- generated footage
for cid, role, at, dur, media in VIDEO_CUTS:
    idx = TRACK_INDEX[cid]
    scale_attr = ' data-layout-allow-overflow' if role == 'city' else ''
    clips.append(
        f'      <div data-hf-id="hf-w{cid}" id="w-{cid}" class="inner">\n'
        f'        <video data-hf-id="hf-v{cid}" id="v-{cid}" class="clip" src="assets/{role}.mp4"\n'
        f'          data-start="{at:.2f}" data-media-start="{media}" data-duration="{dur:.2f}"\n'
        f'          data-track-index="{idx}"{scale_attr} muted playsinline></video>\n'
        f'      </div>')
    if role == 'city':
        # shed-style crop: shrinks the 140px baked-in letterbox off screen.
        timeline.append(f"tl.set('#v-{cid}',{{scale:{CITY_SCALE}}},{at:.2f});")

# ---------------------------------------------------------------- Screen A - SHIPPED
A_AT, A_DUR = 3.4, 2.6
clips.append(f'''      <div data-hf-id="hf-scra" id="screen-a" class="screen clip"
        data-start="{A_AT}" data-duration="{A_DUR}" data-track-index="{TRACK_INDEX['a']}">
{chrome_bar('a')}        <div data-hf-id="hf-abody" id="a-body" class="metric-block" style="top:380px">
          <div data-hf-id="hf-atitle" id="a-title" class="a-title">SHIPPED</div>
          <div data-hf-id="hf-ameta" id="a-meta" class="a-meta">v1.0 &middot; 2:14 AM</div>
          <div data-hf-id="hf-alive" id="a-live" class="a-live-row">
            <i data-hf-id="hf-adot" id="a-dot" class="a-dot"></i>
            <span data-hf-id="hf-alivelabel" id="a-live-label">live</span>
          </div>
        </div>
      </div>''')
add_wipe('screen-a', A_AT)
timeline.append(f"tl.to('#a-dot',{{scale:1.6,duration:.18,ease:'power2.out'}},{A_AT + 0.5:.2f});")
timeline.append(f"tl.to('#a-dot',{{scale:1,duration:.24,ease:'power2.inOut'}},{A_AT + 0.68:.2f});")

# ---------------------------------------------------------------- shared B/D/E metric screen
SPARK_LEFT, SPARK_TOP, SPARK_W, SPARK_H = 410, 860, 1100, 120


def sparkline_svg(prefix, points, path_length=1000):
    return (f'          <svg data-hf-id="hf-{prefix}spark" id="{prefix}-spark" class="sparkline"\n'
            f'            width="{SPARK_W}" height="{SPARK_H}" viewBox="0 0 {SPARK_W} {SPARK_H}">\n'
            f'            <polyline data-hf-id="hf-{prefix}sparkline" id="{prefix}-sparkline"\n'
            f'              points="{points}" pathLength="{path_length}"\n'
            f'              fill="none" stroke="var(--flat)" stroke-width="2"\n'
            f'              style="stroke-dasharray:{path_length};stroke-dashoffset:{path_length}"/>\n'
            f'          </svg>')


def metric_screen(letter, at, dur, number_html_id, number_initial, number_color_var,
                   extra_line_html='', sparkline_points='0,60 1100,60'):
    key = letter.lower()
    idx = TRACK_INDEX[key]
    return f'''      <div data-hf-id="hf-scr{key}" id="screen-{key}" class="screen clip"
        data-start="{at}" data-duration="{dur}" data-track-index="{idx}">
{chrome_bar(key)}        <div data-hf-id="hf-{key}body" id="{key}-body" class="metric-block" style="top:300px">
          <div data-hf-id="hf-{key}label" id="{key}-label" class="metric-label">ACTIVE USERS</div>
          <div data-hf-id="hf-{key}num" id="{number_html_id}" class="metric-number"
            style="color:{number_color_var}">{number_initial}</div>
          <div data-hf-id="hf-{key}sub" id="{key}-sub" class="metric-sub">LAST 7 DAYS</div>
{extra_line_html}        </div>
        <div data-hf-id="hf-{key}sparkwrap" id="{key}-sparkwrap" class="sparkline-wrap"
          style="left:{SPARK_LEFT}px;top:{SPARK_TOP}px">
{sparkline_svg(key, sparkline_points)}
        </div>
      </div>'''


def draw_sparkline(prefix, at, dur):
    timeline.append(
        f"tl.fromTo('#{prefix}-sparkline',{{strokeDashoffset:1000}},"
        f"{{strokeDashoffset:0,duration:{dur},ease:'none'}},{at:.2f});")


# Screen B - ACTIVE USERS 0
B_AT, B_DUR = 6.0, 3.6
clips.append(metric_screen('B', B_AT, B_DUR, 'b-number', '0', 'var(--flat)'))
add_wipe('screen-b', B_AT)
draw_sparkline('b', B_AT, 1.6)

# Screen D - ONE (identical layout to B; the number holds at 0, then swaps to 1)
D_AT, D_DUR = 24.0, 3.2
D_SWAP = D_AT + 0.7
clips.append(metric_screen('D', D_AT, D_DUR, 'd-number', '0', 'var(--flat)',
                           sparkline_points='0,60 1020,60 1020,40 1100,40'))
add_wipe('screen-d', D_AT)
draw_sparkline('d', D_AT, D_SWAP - D_AT + 0.22)
# The 0->1 swap is a discrete state change, not a continuous tween value, so it
# is read from a table each frame via onUpdate (same pure-function-of-time
# pattern as the captions and the SHIP LOG count) rather than a tl.call, which
# is not guaranteed to fire on an arbitrary direct seek (e.g. `snapshot --at`).
timeline.append(
    "var dLast=null;"
    f"tl.to({{t:0}},{{t:1,duration:{D_DUR},ease:'none',onUpdate:function(){{"
    f"var now=this.targets()[0].t*{D_DUR}+{D_AT};"
    f"var swapped=now>={D_SWAP:.2f};if(swapped===dLast){{return;}}dLast=swapped;"
    "var el=document.getElementById('d-number');"
    "el.textContent=swapped?'1':'0';el.style.color=swapped?'var(--accent)':'var(--flat)';"
    f"}}}},{D_AT:.2f});")
timeline.append(f"tl.fromTo('#d-number',{{scale:1}},{{scale:1.08,duration:.11,ease:'power2.out'}},{D_SWAP:.2f});")
timeline.append(f"tl.to('#d-number',{{scale:1,duration:.11,ease:'power2.in'}},{D_SWAP + 0.11:.2f});")

# Screen E - TWELVE (identical layout again; 1 ticks to 12 over 1.6s, +11 THIS WEEK after)
E_AT, E_DUR = 31.4, 3.4
E_TICK_END = E_AT + 1.6
extra = (f'          <div data-hf-id="hf-eweek" id="e-week" class="metric-week">+11 THIS WEEK</div>\n')
clips.append(metric_screen('E', E_AT, E_DUR, 'e-number', '1', 'var(--accent)', extra_line_html=extra,
                           sparkline_points='0,60 733,60 1100,10'))
add_wipe('screen-e', E_AT)
draw_sparkline('e', E_AT, 1.6)
timeline.append(
    "var eTick={n:1};"
    f"tl.to(eTick,{{n:12,duration:1.6,ease:'none',onUpdate:function(){{"
    "document.getElementById('e-number').textContent=Math.round(eTick.n);"
    f"}}}},{E_AT:.2f});")
timeline.append(
    f"tl.fromTo('#e-week',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.32,ease:'power2.out'}},"
    f"{E_TICK_END + 0.4:.2f});")

# ---------------------------------------------------------------- Screen C - SHIP LOG
C_AT, C_DUR = 19.6, 4.4
STAGGER_SPAN = 2.6
ROW_H = 44
ROWS = 16
row_interval = STAGGER_SPAN / ROWS
rows_html = []
for i in range(ROWS):
    version = f'v1.{i + 1}'
    rows_html.append(
        f'''          <div data-hf-id="hf-crow{i}" id="c-row{i}" class="ship-row" style="top:{i * ROW_H}px">
            <span data-hf-id="hf-crowv{i}" id="c-row{i}-v" class="ship-version">{version}</span>
            <span data-hf-id="hf-crows{i}" id="c-row{i}-s" class="ship-status">shipped</span>
            <span data-hf-id="hf-crowz{i}" id="c-row{i}-z" class="ship-zero">0</span>
          </div>''')
    row_at = C_AT + i * row_interval
    timeline.append(
        f"tl.fromTo('#c-row{i}',{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.14,ease:'power2.out'}},{row_at:.2f});")

clips.append(f'''      <div data-hf-id="hf-scrc" id="screen-c" class="screen clip"
        data-start="{C_AT}" data-duration="{C_DUR}" data-track-index="{TRACK_INDEX['c']}">
{chrome_bar('c')}        <div data-hf-id="hf-crelcount" id="c-relcount" class="ship-count">0 RELEASES</div>
        <div data-hf-id="hf-clist" id="c-list" class="ship-list">
{chr(10).join(rows_html)}
        </div>
      </div>''')
add_wipe('screen-c', C_AT)
timeline.append(
    "var C_ROW_TIMES=" + json.dumps([round(C_AT + i * row_interval, 3) for i in range(ROWS)]) + ",cRelLast=null;"
    f"tl.to({{t:0}},{{t:1,duration:{C_DUR},ease:'none',onUpdate:function(){{"
    "var now=this.targets()[0].t*" + f"{C_DUR}+{C_AT}" + ";"
    "var count=0;for(var i=0;i<C_ROW_TIMES.length;i++){if(now>=C_ROW_TIMES[i]){count=i+1;}}"
    "if(count===cRelLast){return;}cRelLast=count;"
    "document.getElementById('c-relcount').textContent=count+' RELEASES';"
    f"}}}},{C_AT:.2f});")

# ---------------------------------------------------------------- Screen F - CLOSE
F_AT, F_DUR = 40.0, 2.0
clips.append(f'''      <div data-hf-id="hf-scrf" id="screen-f" class="screen clip screen-night"
        data-start="{F_AT}" data-duration="{F_DUR}" data-track-index="{TRACK_INDEX['f']}">
        <div data-hf-id="hf-fmark" id="f-mark">tuesday<span data-hf-id="hf-fdot" id="f-dot">.</span></div>
        <i data-hf-id="hf-frule" id="f-rule"></i>
        <div data-hf-id="hf-ftag" id="f-tag">Ship it anyway.</div>
      </div>''')
timeline.append(f"tl.fromTo('#screen-f',{{opacity:0}},{{opacity:1,duration:.5,ease:'power2.inOut'}},{F_AT:.2f});")

# ---------------------------------------------------------------- captions (single element)
# l01 (index 0) -> lower-left, l03 (index 2) -> lower-left, l07 (index 6) -> lower-centre.
CAPTION_TABLE = []
for i, spec in enumerate(VO):
    if i not in (0, 2, 6):
        continue
    align = 'left' if i in (0, 2) else 'center'
    end = spec['start'] + spec['duration'] + 0.24
    if i == 0:
        end = min(end, 3.20)
    CAPTION_TABLE.append({'at': spec['start'], 'end': round(end, 3), 'text': spec['text'], 'align': align})

timeline.append("var CAPS=" + json.dumps(CAPTION_TABLE) + ",capLast=null;")
timeline.append(
    "tl.to({t:0},{t:1,duration:" + str(DURATION) + ",ease:'none',onUpdate:function(){"
    "var now=this.targets()[0].t*" + str(DURATION) + ";"
    "var active=null;for(var i=0;i<CAPS.length;i++){if(now>=CAPS[i].at&&now<CAPS[i].end){active=CAPS[i];}}"
    "var key=active?active.text+active.align:'';if(key===capLast){return;}capLast=key;"
    "var el=document.getElementById('cap');"
    "if(!active){el.textContent='';return;}"
    "el.textContent=active.text;"
    "if(active.align==='center'){el.style.left='0';el.style.right='0';el.style.textAlign='center';}"
    "else{el.style.left='96px';el.style.right='auto';el.style.textAlign='left';}"
    "}},0);")

# ---------------------------------------------------------------- audio
audio = [
    f'      <audio data-hf-id="hf-avo" id="a-vo" src="assets/voice.wav" data-start="0" '
    f'data-duration="{DURATION}" data-volume="1" data-track-index="60"></audio>']
audio.append(
    f'      <audio data-hf-id="hf-amu" id="a-score" src="assets/score.wav" data-start="0" '
    f'data-duration="{DURATION}" data-volume="{plan["score_volume"]}" data-track-index="61" '
    f"data-automation='{json.dumps(plan['music_automation'])}'></audio>")
for tag, cue in enumerate(plan['sfx_cues']):
    audio.append(
        f'      <audio data-hf-id="hf-ax{tag}" id="a-sfx{tag}" src="assets/{cue["src"]}" '
        f'data-start="{cue["at"]}" data-duration="{cue["duration"]}" '
        f'data-volume="{cue["volume"]}" data-track-index="{70 + tag}"></audio>')

# Contrast fixes (measured with `hyperframes check`):
#   --flat  : the zero state must stay grey rather than red - nothing is broken -
#     but at #c2c8ce it measured 1.51:1 on paper and the viewer has to be able
#     to read the zeros, since "shipped ... 0" is the beat.
#   --muted : the 22px chrome label measured 3.34:1 and needs 4.5:1.
#   footer  : the footer sits on a dark rgba(10,12,15,.9) chip and measured
#     4.22:1 using --muted. It must not follow --muted's new (darker) value,
#     which would make it worse on dark, so it takes an explicit light colour
#     of its own rather than the shared muted token.
FLAT = '#848c94'
MUTED = '#5f686f'
FOOTER_TEXT = '#c9ced3'

html = f'''<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <script src="assets/gsap.min.js"></script>
    <style>
      *{{margin:0;padding:0;box-sizing:border-box}}
      html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#0a0c0f}}
      body{{font-family:SeventeenSans,Arial,sans-serif}}
      @font-face{{font-family:SeventeenSans;src:url('assets/SeventeenSans.ttf')}}
      @font-face{{font-family:SeventeenSans;src:url('assets/SeventeenSans-Bold.ttf');font-weight:700}}
      :root{{--night:#0a0c0f;--paper:#f4f2ed;--ink:#14181d;--muted:{MUTED};--accent:#2f6df0;--flat:{FLAT}}}
      #root{{width:1920px;height:1080px;overflow:hidden;position:relative;background:var(--night)}}
      .inner{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}}
      .clip{{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover}}

      .screen{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;background:var(--paper)}}
      .screen-night{{background:var(--night)}}
      .chrome-bar{{position:absolute;top:0;left:0;right:0;height:1px;background:var(--muted);font-style:normal}}
      .chrome-label{{position:absolute;top:22px;left:72px;font-size:22px;color:var(--muted)}}

      .metric-block{{position:absolute;left:0;right:0;text-align:center}}
      .metric-label{{font-size:30px;color:var(--muted);letter-spacing:.16em}}
      .metric-number{{font-size:240px;font-weight:700;line-height:1;margin-top:14px;
        font-variant-numeric:tabular-nums}}
      .metric-sub{{font-size:26px;color:var(--muted);margin-top:36px}}
      .metric-week{{font-size:26px;color:var(--accent);margin-top:16px;opacity:0}}
      .sparkline-wrap{{position:absolute;width:{SPARK_W}px;height:{SPARK_H}px}}

      .a-title{{font-size:128px;font-weight:700;color:var(--ink);line-height:1;text-align:center}}
      .a-meta{{font-size:28px;color:var(--muted);text-align:center;margin-top:26px}}
      .a-live-row{{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:22px}}
      .a-dot{{display:block;width:10px;height:10px;border-radius:50%;background:var(--accent);
        font-style:normal}}
      #a-live-label{{font-size:26px;color:var(--muted)}}

      .ship-count{{position:absolute;top:22px;right:72px;font-size:28px;color:var(--muted);
        font-variant-numeric:tabular-nums}}
      .ship-list{{position:absolute;top:78px;left:72px;width:1200px;height:{ROWS * ROW_H}px}}
      .ship-row{{position:absolute;left:0;right:0;height:{ROW_H}px;display:flex;align-items:center}}
      .ship-version{{font-size:30px;color:var(--ink);width:160px;font-variant-numeric:tabular-nums}}
      .ship-status{{font-size:26px;color:var(--muted);flex:1;text-align:center}}
      .ship-zero{{font-size:30px;color:var(--flat);width:80px;text-align:right;
        font-variant-numeric:tabular-nums}}

      #f-mark{{position:absolute;left:0;right:0;top:392px;text-align:center;font-size:132px;
        font-weight:700;color:#fff;line-height:1}}
      #f-dot{{color:var(--accent)}}
      #f-rule{{position:absolute;left:50%;top:566px;width:280px;margin-left:-140px;height:1px;
        background:var(--accent);font-style:normal}}
      #f-tag{{position:absolute;left:0;right:0;top:614px;text-align:center;font-size:40px;color:#fff}}

      #cap{{position:absolute;bottom:150px;left:96px;right:auto;z-index:40;font-weight:700;
        font-size:64px;line-height:1.28;color:#fff;
        text-shadow:0 2px 12px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.65);max-width:1400px}}
      #footer{{position:absolute;right:64px;bottom:48px;z-index:100;font-size:19px;color:{FOOTER_TEXT};
        background:rgba(10,12,15,.9);padding:8px 14px}}
    </style>
  </head>
  <body>
    <div data-hf-id="hf-root" id="root" data-composition-id="seventeen" data-start="0" data-duration="{DURATION}" data-width="1920" data-height="1080">
{chr(10).join(clips)}

      <div data-hf-id="hf-cap" id="cap"></div>
      <div data-hf-id="hf-foot" id="footer">ORIGINAL CONCEPT / AI-GENERATED FILM</div>

{chr(10).join(audio)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + line for line in timeline)}
      window.__timelines['seventeen'] = tl;
    </script>
  </body>
</html>
'''
Path('index.html').write_text(html)
print(f'{len(VIDEO_CUTS)} video cuts, 6 authored screens, {len(CAPTION_TABLE)} captions, '
      f'{len(timeline)} tween statements, {DURATION}s')
