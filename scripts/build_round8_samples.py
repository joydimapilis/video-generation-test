"""Stage reviewed takes and build three reproducible HyperFrames concept films.

Selection is explicit in the local manifest; this script never buys generations.
Run from the repository root after selecting sources in library-loop-8.
"""
import hashlib
import html
import json
import shutil
import subprocess
import wave
from pathlib import Path
import numpy as np

ROOT = Path('artifacts/library-loop-8')
PROJECTS = Path('hyperframes')

def command(*args):
    subprocess.run(list(map(str, args)), check=True)


def stage(project, src, name):
    src = Path(src)
    dst = project / 'assets' / name
    shutil.copyfile(src, dst)
    return {'source': str(src), 'staged': str(dst), 'sha256': hashlib.sha256(src.read_bytes()).hexdigest()}


def stage_voice(project, src):
    """Decode AAC once to avoid browser priming differences; leave headroom."""
    raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vn',
                                   '-ac','2','-ar','48000','-f','f32le','-'])
    samples = np.frombuffer(raw,dtype='<f4').astype(float)
    peak = float(np.abs(samples).max())
    gain = min(1., .8 / peak) if peak else 1.
    dst = project/'assets/voice.wav'
    with wave.open(str(dst),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(48000)
        f.writeframes((samples*gain*32767).astype('<i2').tobytes())
    return {'staged':str(dst),'source':str(src),'source_sha256':hashlib.sha256(Path(src).read_bytes()).hexdigest(),
            'derived_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
            'operation':'FFmpeg decoded stereo PCM at 48kHz, linear gain only; WAV preserves source start alignment',
            'linear_gain':gain,'source_peak':peak}


def score(path, duration, variant, start_music):
    """Original sparse plucked score, deterministic; music starts after speech."""
    sr = 48000
    mix = np.zeros((round(duration * sr), 2))
    def add(at, notes, length=1.8, level=.04):
        at = round(at * sr)
        t = np.arange(round(length * sr)) / sr
        y = sum(np.sin(2*np.pi*(440*2**((n-69)/12))*t) for n in notes)
        y *= np.minimum(t/.012,1)*np.exp(-t*3)*level
        n = min(len(y),len(mix)-at)
        if n > 0: mix[at:at+n] += y[:n,None] * np.array([1,.9])
    notes = [50,57,62,66] if variant == 'cue' else [48,55,60,64]
    for i, at in enumerate(np.arange(start_music, duration-.6, .6)):
        add(at,[notes[i%4]+12],level=.055 if i%4==0 else .028)
        if i%4==0: add(at,[notes[0]-12,notes[1]],length=2.3,level=.02)
    t = np.arange(len(mix))/sr
    mix *= np.clip((duration-t)/.8,0,1)[:,None]
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((np.clip(mix,-.9,.9)*32767).astype('<i2').tobytes())


BASE = '''*{box-sizing:border-box;margin:0}html,body{width:1920px;height:1080px;overflow:hidden;background:#f3f1e9;color:#182d26;font-family:LabSans,Arial,sans-serif}
@font-face{font-family:LabSans;src:url('assets/CrewSans.ttf')}@font-face{font-family:LabSans;src:url('assets/CrewSans-Bold.ttf');font-weight:700}
@font-face{font-family:LabSerif;src:url('assets/CrewSerif.woff2')}
#root{position:relative;width:1920px;height:1080px}.clip{position:absolute}.host{inset:0;width:1920px;height:1080px;overflow:hidden}
'''


def scene(project, ident, duration, markup, css='', js=''):
    root = ident + '-root'
    text = f'''<template><style>@font-face{{font-family:LabSerif;src:url('assets/CrewSerif.woff2')}}#{root}{{position:relative;width:1920px;height:1080px;overflow:hidden}}{css}</style>
<div id="{root}" data-composition-id="{ident}" data-width="1920" data-height="1080" data-duration="{duration}">{markup}</div>
<script>var tl=gsap.timeline({{paused:true}});{js}window.__timelines['{ident}']=tl;</script></template>'''
    (project/'compositions'/f'{ident}.html').write_text(text)
    return ident


def host(ident, start, duration, lane):
    return f'<div id="{ident}-host" class="clip host" data-composition-id="{ident}" data-composition-src="compositions/{ident}.html" data-start="{start}" data-duration="{duration}" data-width="1920" data-height="1080" data-track-index="{lane}"></div>'


def video(ident, file, duration, start=0, offset=0, cls='footage'):
    return f'<video id="{ident}" class="clip {cls}" src="assets/{file}" data-start="{start}" data-duration="{duration}" data-media-start="{offset}" data-track-index="0" muted playsinline></video>'


def audio(ident,file,start,duration,offset=0,volume=1):
    return f'<audio id="{ident}" src="assets/{file}" data-start="{start}" data-duration="{duration}" data-media-start="{offset}" data-volume="{volume}" data-track-index="{11 if 'score' in ident else 10}"></audio>'


def cursor(ident):
    # Adapted from installed HyperFrames simulated-cursor component.
    return f'<div id="{ident}" class="pointer"><div class="pulse"></div><svg viewBox="0 0 24 24" width="56" height="56"><path d="M3 2.8 20.6 14 12.8 15.5 9 22 3 2.8Z" fill="#182d26" stroke="#f3f1e9" stroke-width="1.4"/></svg></div>'


CURSOR_CSS = '.pointer{position:absolute;left:0;top:0;width:56px;height:56px;z-index:9}.pulse{position:absolute;left:8px;top:8px;width:30px;height:30px;border:3px solid #276447;border-radius:50%;opacity:0}'


def documentary(project, prefix, source, duration, brand, subtitles, offset=0):
    ident=prefix+'-person'
    markup=video(ident+'-video',source,duration,offset=offset)
    markup+=f'<div class="brand">{brand}</div><div class="disclosure">FICTIONAL CONCEPT · AI PRESENTER</div>'
    for i,(at,end,line) in enumerate(subtitles):
        markup+=f'<div id="{ident}-sub-{i}" class="clip subtitle" data-start="{at}" data-duration="{end-at}" data-track-index="2">{html.escape(line)}</div>'
    css=f'''#{ident}-root{{background:#edece6}}.footage{{inset:0;width:1920px;height:1080px;object-fit:cover}}.brand{{position:absolute;left:78px;top:62px;font-size:58px;line-height:1;background:#f3f1e9;color:#182d26;padding:18px 28px;border-radius:10px;font-weight:700}}.disclosure{{position:absolute;right:62px;top:62px;font-size:22px;color:#182d26;background:#f3f1e9;padding:12px 18px;border-radius:6px}}.subtitle{{left:240px;bottom:60px;width:1440px;text-align:center;background:#182d26;color:#f3f1e9;font-size:42px;line-height:1.25;padding:18px 30px;border-radius:10px}}'''
    return scene(project,ident,duration,markup,css)


def close(project,prefix,brand,line,sub,duration):
    ident=prefix+'-close'
    words=''.join(f'<span>{html.escape(w)}</span>' for w in line.split())
    markup=f'<div class="close-layout"><div class="brand">{brand}</div><h1>{words}</h1><p>{sub}</p><div class="rule"></div><footer>FICTIONAL PRODUCT CONCEPT</footer></div>'
    css=f'''#{ident}-root{{background:#182d26;color:#f3f1e9}}.close-layout{{height:100%;padding:88px 110px;display:flex;flex-direction:column;justify-content:center;gap:34px}}.brand{{font-size:46px;font-weight:700;color:#d4e99c}}h1{{max-width:1580px;font-size:138px;line-height:1.06;font-weight:400;letter-spacing:-5px}}h1 span{{display:inline-block;margin-right:.23em}}p{{font-size:36px;color:#d4e99c}}.rule{{width:100%;height:2px;background:#d4e99c;margin-top:40px;transform-origin:left}}footer{{font-size:22px;color:#f3f1e9;letter-spacing:3px}}'''
    js=f"tl.fromTo('h1 span',{{opacity:0,y:48}},{{opacity:1,y:0,duration:.54,stagger:.07,ease:'power3.out'}},.15);tl.fromTo('.rule',{{scaleX:0}},{{scaleX:1,duration:.8,ease:'power2.out'}},.25);"
    return scene(project,ident,duration,markup,css,js)


def ui_cue(project,prefix,duration):
    ident=prefix+'-demo'
    markup='''<div class="layout"><header><b>cue.</b><span>FROM THE CALL TO THE NEXT STEP</span></header><h1>Give the idea somewhere to go.</h1><div class="window"><div class="toolbar"><b>Launch notes</b><span>Today, 10:30</span></div><div id="note"><div class="eyebrow">YOU SAID</div><p>“I'll send the first draft on Friday.”</p><div class="wave">''' + ''.join(f'<i style="height:{15+int(abs(np.sin(i*.8))*38)}px"></i>' for i in range(32))+'''</div></div><div id="task"><div class="eyebrow">NEXT ACTION</div><h2>Send the first draft</h2><div class="fields"><div><small>Owner</small><strong>You</strong></div><div><small>Due</small><strong>Friday</strong></div></div><div id="save">Save action</div><div id="saved">✓ Saved to your action list</div></div>'''+cursor(ident+'-cursor')+'''</div><footer>ILLUSTRATIVE INTERFACE · ONE CLEAR ACTION, WITH AN OWNER AND A DATE</footer></div>'''
    css=f'''#{ident}-root{{background:#f3f1e9;color:#182d26}}.layout{{padding:58px 96px;height:100%;display:flex;flex-direction:column;gap:34px}}header{{display:flex;justify-content:space-between;align-items:center;font-size:25px;letter-spacing:2px}}header b{{font-size:50px;letter-spacing:-2px}}h1{{font-family:LabSerif,Georgia,serif;font-size:82px;font-weight:400;line-height:1.1}}.window{{position:relative;height:660px;background:#fffef9;border:2px solid #9cafa1;border-radius:18px;overflow:hidden;margin:4px 60px}}.toolbar{{height:96px;border-bottom:2px solid #d5ded3;display:flex;align-items:center;justify-content:space-between;padding:0 46px;font-size:28px}}.toolbar b{{font-size:36px}}#note,#task{{position:absolute;top:136px;left:56px;right:56px;height:420px}}.eyebrow{{font-size:24px;letter-spacing:3px;color:#376448}}#note p{{font-size:58px;max-width:1300px;line-height:1.2;margin-top:32px}}.wave{{display:flex;align-items:center;gap:10px;height:80px;margin-top:45px}}.wave i{{display:block;width:10px;background:#376448;border-radius:5px}}#task h2{{font-size:58px;font-weight:400;margin-top:16px}}.fields{{display:flex;gap:170px;margin-top:28px}}.fields div{{display:flex;flex-direction:column;gap:9px}}small{{font-size:24px}}strong{{font-size:38px}}#save{{position:absolute;top:264px;right:0;width:274px;height:78px;border-radius:12px;background:#182d26;color:#f3f1e9;display:flex;align-items:center;justify-content:center;font-size:30px}}#saved{{position:absolute;top:294px;left:0;font-size:32px;color:#276447}}footer{{font-size:21px;letter-spacing:1px;color:#376448}}{CURSOR_CSS}'''
    js=f"""tl.fromTo('#note',{{opacity:1}},{{opacity:0,duration:.25}},2.1);
tl.fromTo('#task',{{opacity:0,y:22}},{{opacity:1,y:0,duration:.4,ease:'power3.out'}},2.4);
tl.fromTo('#{ident}-cursor',{{opacity:0,x:1400,y:580}},{{opacity:1,x:1270,y:430,duration:.7,ease:'power2.inOut'}},3.5);
tl.to('#save',{{scale:.96,duration:.1,yoyo:true,repeat:1}},4.25);
tl.fromTo('#{ident}-cursor .pulse',{{opacity:.8,scale:.2}},{{opacity:0,scale:3,duration:.45,ease:'power2.out'}},4.3);
tl.fromTo('#saved',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.25}},4.5);
tl.to('#{ident}-cursor',{{opacity:0,duration:.25}},4.9);"""
    return scene(project,ident,duration,markup,css,js)


def ui_crew(project,prefix,duration):
    ident=prefix+'-demo'
    markup='''<div class="layout"><header><b>crew.</b><span>LESS CHASING. A CLEARER WEEK.</span></header><h1>Availability, before the rota.</h1><div class="proof"><div class="phone"><div class="phone-head">Your availability</div><p>Week of 14 September</p><div class="day"><span>Monday</span><b>Available</b></div><div class="day"><span>Tuesday</span><b>Available</b></div><div class="day"><span>Wednesday</span><b>Unavailable</b></div><div id="send">Share availability</div><div id="sent">✓ Shared with your team</div></div><div class="schedule"><div class="schedule-head"><b>This week's team</b><span>MON / TUE / WED</span></div>'''+''.join(f'<div class="person"><strong>{name}</strong><div class="slots"><i>{slots[0]}</i><i>{slots[1]}</i><i>{slots[2]}</i></div></div>' for name,slots in [('Alex',['✓','✓','—']),('Sam',['✓','—','✓']),('Jo',['—','✓','✓'])])+'''<div id="ready">Now build a rota around real availability.</div></div>'''+cursor(ident+'-cursor')+'''</div><footer>ILLUSTRATIVE INTERFACE · FICTIONAL TEAM</footer></div>'''
    css=f'''#{ident}-root{{background:#f3f1e9;color:#182d26}}.layout{{height:100%;padding:58px 96px;display:flex;flex-direction:column;gap:30px}}header{{display:flex;justify-content:space-between;align-items:center;font-size:25px;letter-spacing:2px}}header b{{font-size:50px;letter-spacing:-2px}}h1{{font-family:LabSerif,Georgia,serif;font-size:90px;font-weight:400;line-height:1.1}}.proof{{position:relative;display:flex;gap:100px;margin-top:10px;align-items:center;height:650px}}.phone{{position:relative;width:510px;height:620px;border:3px solid #182d26;border-radius:32px;background:#fffef9;padding:38px 32px;flex-shrink:0}}.phone-head{{font-size:37px;font-weight:700}}.phone p{{font-size:23px;margin-top:10px;margin-bottom:28px;color:#376448}}.day{{height:74px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #aebfb0;font-size:25px}}.day b{{font-weight:400;color:#276447}}#send{{margin-top:30px;background:#182d26;color:#f3f1e9;padding:20px;border-radius:10px;text-align:center;font-size:28px}}#sent{{margin-top:23px;font-size:25px;color:#276447}}.schedule{{flex:1;border-top:3px solid #182d26;border-bottom:2px solid #182d26;padding:25px 0}}.schedule-head{{display:flex;justify-content:space-between;font-size:24px;padding-bottom:25px}}.schedule-head b{{font-size:37px}}.schedule-head span{{padding-top:10px;letter-spacing:2px}}.person{{height:97px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid #aebfb0}}.person strong{{font-size:33px;font-weight:400}}.slots{{display:flex;gap:20px}}.slots i{{width:150px;background:#d4e99c;border-radius:6px;text-align:center;font-size:34px;font-style:normal;padding:9px}}#ready{{font-size:30px;margin-top:24px}}footer{{font-size:21px;letter-spacing:1px;color:#376448}}{CURSOR_CSS}'''
    js=f"""tl.fromTo('.slots',{{opacity:0}},{{opacity:1,duration:.3,stagger:.1}},3.35);
tl.fromTo('#{ident}-cursor',{{opacity:0,x:900,y:610}},{{opacity:1,x:260,y:464,duration:.75,ease:'power2.inOut'}},2.1);
tl.to('#send',{{scale:.96,duration:.1,yoyo:true,repeat:1}},2.9);
tl.fromTo('#{ident}-cursor .pulse',{{opacity:.8,scale:.2}},{{opacity:0,scale:3,duration:.45,ease:'power2.out'}},2.95);
tl.fromTo('#sent',{{opacity:0}},{{opacity:1,duration:.25}},3.2);
tl.fromTo('#ready',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.3}},4);
tl.to('#{ident}-cursor',{{opacity:0,duration:.2}},3.6);"""
    return scene(project,ident,duration,markup,css,js)


def product(project,prefix,file,duration,title,sub,offset=0):
    ident=prefix+'-product'
    markup=video(ident+'-video',file,duration,offset=offset)+f'<div class="rail"><h1>{title}</h1><p>{sub}</p></div>'
    css=f'''#{ident}-root{{background:#202422;color:#f3f1e9}}.footage{{inset:0;width:1920px;height:1080px;object-fit:cover}}.rail{{position:absolute;left:76px;top:65px;max-width:680px;background:#182d26;padding:25px 34px;border-radius:12px}}h1{{font-size:62px;line-height:1.08;font-weight:400}}p{{font-size:26px;margin-top:15px;color:#d4e99c}}'''
    return scene(project,ident,duration,markup,css)


def assemble(project,name,duration,scenes,audios,provenance):
    markup=''.join(host(i,s,d,n) for n,(i,s,d) in enumerate(scenes))+''.join(audios)
    text=f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{name}</title><script src="assets/gsap.min.js"></script><style>{BASE}</style></head><body><div id="root" data-composition-id="{name}" data-width="1920" data-height="1080" data-duration="{duration}">{markup}</div><script>window.__timelines["{name}"]=gsap.timeline({{paused:true}});</script></body></html>'
    (project/'index.html').write_text(text)
    (project/'sources.json').write_text(json.dumps(provenance,indent=2)+'\n')
    board='---\nmode: autonomous\nstatus: built\n---\n\n'
    for i,(ident,start,length) in enumerate(scenes,1):
        board+=f'## Frame {i}\nstatus: built\nsrc: compositions/{ident}.html\nstart: {start}\nduration: {length}\nmotion: authored cut; text-stagger or cursor-click-ripple where applicable; source camera motion unchanged\n\n'
    (project/'STORYBOARD.md').write_text(board)
    return {'project':str(project),'duration':duration,'scenes':scenes}


def main():
    selection_path=ROOT/'sample-selection.json'
    if not selection_path.exists():
        selection_path=Path('assembled_outputs/round8_samples.json')
    selected=json.loads(selection_path.read_text())
    outputs=[]
    for name in ['cue-followthrough','cue-object-study','crew-availability']:
        project=PROJECTS/name;(project/'assets').mkdir(exist_ok=True);(project/'compositions').mkdir(exist_ok=True)
        provenance=[]
        for asset in ['CrewSans.ttf','CrewSans-Bold.ttf','CrewSerif.woff2','gsap.min.js']:
            provenance.append(stage(project,PROJECTS/'crew/assets'/asset,asset))
        if name=='cue-followthrough':
            take=selected['ugc'];hook_end=take['out']-take.get('in',0)
            provenance.append(stage(project,take['path'],'hook.mp4'))
            provenance.append(stage_voice(project,take['path']))
            provenance.append(stage(project,selected['product']['path'],'product.mp4'))
            duration=18;demo_start=hook_end+2.5;demo_dur=15-demo_start
            a=documentary(project,'follow','hook.mp4',hook_end,'cue.',[(0,2.3,'I remember the idea.'),(3.25,hook_end,'I forget what I promised to do.')],take.get('in',0))
            b=product(project,'follow','product.mp4',2.5,'Meet Cue.','A place for the next idea.',selected['product'].get('in',0))
            c=ui_cue(project,'follow',demo_dur)
            d=close(project,'follow','cue.','Remember it. Do it.','From a spoken idea to a clear next action.',3)
            scenes=[(a,0,hook_end),(b,hook_end,2.5),(c,demo_start,demo_dur),(d,15,3)]
            score(project/'assets/score.wav',duration,'cue',hook_end)
            sounds=[audio('follow-voice','voice.wav',0,hook_end,take.get('in',0)),audio('follow-score','score.wav',0,duration)]
        elif name=='cue-object-study':
            a_take=selected['product'];b_take=selected['continuation'];a_end=a_take['out']-a_take.get('in',0);b_dur=b_take['out']-b_take.get('in',0)
            duration=a_end+b_dur+3
            provenance.append(stage(project,a_take['path'],'product.mp4'));provenance.append(stage(project,b_take['path'],'continuation.mp4'))
            a=product(project,'object-a','product.mp4',a_end,'A small place for a big idea.','cue. / VOICE RECORDER CONCEPT',a_take.get('in',0))
            b=product(project,'object-b','continuation.mp4',b_dur,'One button. Your next thought.','cue. / VOICE RECORDER CONCEPT',b_take.get('in',0))
            c=close(project,'object','cue.','Keep the thought.','Make room for what comes next.',3)
            scenes=[(a,0,a_end),(b,a_end,b_dur),(c,a_end+b_dur,3)]
            score(project/'assets/score.wav',duration,'cue',0)
            sounds=[audio('object-score','score.wav',0,duration)]
        else:
            take=selected['interview'];hook_end=take['out']-take.get('in',0);duration=18
            provenance.append(stage(project,take['path'],'interview.mp4'))
            provenance.append(stage_voice(project,take['path']))
            a=documentary(project,'availability','interview.mp4',hook_end,'crew.',[(0,1.5,'We use Crew now.'),(2.1,hook_end,'Everyone puts their availability on their phone.')],take.get('in',0))
            b=ui_crew(project,'availability',15-hook_end)
            c=close(project,'availability','crew.','Know who is free.','Availability first. The rota follows.',3)
            scenes=[(a,0,hook_end),(b,hook_end,15-hook_end),(c,15,3)]
            score(project/'assets/score.wav',duration,'crew',hook_end)
            sounds=[audio('availability-voice','voice.wav',0,hook_end,take.get('in',0)),audio('availability-score','score.wav',0,duration)]
        provenance.append({'staged':str(project/'assets/score.wav'),'source':'original deterministic synthesis in scripts/build_round8_samples.py','music_starts_after_dialogue':name!='cue-object-study'})
        outputs.append(assemble(project,name,duration,scenes,sounds,provenance))
    (ROOT/'sample-build.json').write_text(json.dumps(outputs,indent=2)+'\n')
    print(json.dumps(outputs,indent=2))


if __name__=='__main__': main()
