"""Build three fresh Crumb sample edits from reviewed round9 footage. No paid calls."""
import json,html,shutil,subprocess,hashlib,wave
from pathlib import Path
import numpy as np
from build_round8_samples import stage,stage_voice
ROOT=Path('artifacts/library-loop-9')
CSS='''*{box-sizing:border-box;margin:0}html,body{width:1920px;height:1080px;overflow:hidden;background:#F5EBDD;color:#30221D;font-family:CrumbSans,sans-serif}@font-face{font-family:CrumbSans;src:url('assets/sans.ttf')}@font-face{font-family:CrumbSans;src:url('assets/bold.ttf');font-weight:700}@font-face{font-family:CrumbSerif;src:url('assets/serif.woff2')}#root,.frame{position:relative;width:1920px;height:1080px;overflow:hidden}.clip{position:absolute}.host{inset:0;width:1920px;height:1080px}.bar{position:absolute;top:0;left:0;right:0;height:124px;padding:28px 84px;display:flex;align-items:center;justify-content:space-between;background:#F5EBDD;z-index:5;border-bottom:2px solid #30221D}.brand{font-family:CrumbSerif,serif;font-size:68px;line-height:1}.category{font-size:27px;letter-spacing:3px;text-transform:uppercase}.foot{position:absolute;left:84px;right:84px;bottom:36px;display:flex;justify-content:space-between;font-size:24px;z-index:6}.eyebrow{font-size:27px;letter-spacing:3px;text-transform:uppercase;color:#943D2B;font-weight:700}.display{font-family:CrumbSerif,serif;font-size:112px;line-height:1.04;font-weight:400;letter-spacing:-2px}.body{font-size:37px;line-height:1.4}.paper{background:#F5EBDD}.rule{height:2px;background:#30221D;width:100%;margin:28px 0}.caption{position:absolute;left:180px;right:180px;bottom:100px;text-align:center;z-index:8}.caption span{display:inline-block;background:#F5EBDD;color:#30221D;padding:14px 30px;font-size:44px;line-height:1.25}.film{width:1920px;height:1080px;object-fit:cover}.person{top:124px;height:956px;object-fit:contain;background:#F5EBDD}.grid{display:grid;grid-template-columns:700px 1fr;gap:90px;padding:205px 84px 110px;height:100%;align-items:center}.intro{display:flex;flex-direction:column;gap:32px}.ticket{padding:42px;background:#FFFAF1;border:2px solid #30221D;box-shadow:16px 18px 0 #E5D4BD;position:relative}.ticket h2{font-size:48px;font-weight:700}.small{font-size:28px;line-height:1.4}.line{display:flex;justify-content:space-between;align-items:center;padding:25px 0;border-bottom:2px solid #D2BCA6;font-size:36px;gap:25px}.slot{display:flex;align-items:center;justify-content:space-between;margin:28px 0;padding:22px;background:#E5D4BD;font-size:36px}.action{padding:27px 24px;text-align:center;color:#FFFAF1;background:#943D2B;font-size:38px;font-weight:700;transform-origin:center}.confirm{position:absolute;inset:0;background:#FFFAF1;display:flex;flex-direction:column;justify-content:center;padding:55px;gap:25px}.confirm h2{font-family:CrumbSerif,serif;font-size:84px;font-weight:400}.check{width:92px;height:92px;border-radius:50%;background:#943D2B;color:#FFFAF1;display:grid;place-items:center;font-size:60px}.stamp{border:2px solid #943D2B;padding:20px;color:#943D2B;font-size:40px;text-align:center}.close-wrap{padding:210px 84px 130px;height:100%;display:grid;grid-template-columns:1.1fr 0.9fr;gap:100px;align-items:center}.close-title{font-family:CrumbSerif,serif;font-size:136px;font-weight:400;line-height:1.02}.steps{display:flex;flex-direction:column}.step{display:flex;gap:32px;align-items:center;padding:26px 0;border-bottom:2px solid #30221D;font-size:39px}.step b{font-family:CrumbSerif,serif;font-size:60px;font-weight:400;color:#943D2B}.foodcopy{position:absolute;left:0;top:124px;bottom:0;width:650px;background:#F5EBDD;padding:116px 65px 120px 84px;display:flex;flex-direction:column;justify-content:center;gap:32px}.foodcopy .display{font-size:105px}.num{font-variant-numeric:tabular-nums}.tablehead{font-size:27px;letter-spacing:1px;text-transform:uppercase;color:#943D2B}.orderrow{display:grid;grid-template-columns:1.3fr .7fr .5fr;gap:20px;padding:25px 0;border-bottom:2px solid #D2BCA6;font-size:33px}.total{display:flex;justify-content:space-between;align-items:center;background:#E5D4BD;margin-top:30px;padding:24px;font-size:36px}.total strong{font-family:CrumbSerif,serif;font-size:64px}'''
def header():return '<div class="bar"><div class="brand">crumb.</div><div class="category">Bakery preorders, made simple.</div></div>'
def footer(label):return f'<div class="foot"><span>{label}</span><span>Fictional service · Sample film</span></div>'
def vid(file,dur,offset=0):return f'<video id="{Path(file).stem}-video" class="clip film" src="assets/{file}" data-start="0" data-duration="{dur}" data-media-start="{offset}" data-track-index="0" muted playsinline></video>'
def scene(p,ident,dur,body,js=''):
 (p/'compositions'/f'{ident}.html').write_text(f'<template><div class="frame" data-composition-id="{ident}" data-width="1920" data-height="1080" data-duration="{dur}">{body}</div><script>var tl=gsap.timeline({{paused:true}});{js}window.__timelines["{ident}"]=tl;</script></template>')
 return ident,dur

def enter(root):return f'tl.fromTo("#{root} .arrive",{{y:36}},{{y:0,duration:.5,stagger:.06,ease:"power3.out"}},.05);'
def dialogue(p,role,take,ident='open',filename='person.mp4'):
 dur=take['out']-take.get('in',0);captions=''
 for i,c in enumerate(take['captions']):
  a,b,txt=c
  captions+=f'<div id="{ident}-caption-{i}" class="clip caption" data-start="{a}" data-duration="{b-a}" data-track-index="3"><span>{html.escape(txt)}</span></div>'
 return scene(p,ident,dur,vid(filename,dur,take.get('in',0)).replace('clip film','clip film person')+header()+captions)
def demo(p,baker,dur):
 if baker:
  heading='Orders in<br>one place.';sub='Stop piecing tomorrow together<br>from messages and scraps.';label='FOR THE BAKERY'
  content='''<div class="eyebrow">Crumb / Baker view</div><h2 style="margin-top:16px">Tomorrow’s preorders</h2><div class="rule"></div><div class="orderrow tablehead"><span>Order</span><span>Pickup</span><span>Qty</span></div><div class="orderrow arrive"><span>Croissants</span><span>8:30</span><span>2</span></div><div class="orderrow arrive"><span>Croissants</span><span>9:00</span><span>4</span></div><div class="orderrow arrive"><span>Croissants</span><span>9:30</span><span>6</span></div><div class="total arrive"><span>Booked for tomorrow</span><strong>12</strong></div>'''
  js='tl.fromTo("#demo .orderrow.arrive",{x:60,opacity:0},{x:0,opacity:1,duration:.45,stagger:.65,ease:"power3.out"},1);tl.fromTo("#demo .total",{y:28,opacity:0},{y:0,opacity:1,duration:.5,ease:"power3.out"},3.4);'
 else:
  heading='Skip the<br>sold-out<br>surprise.';sub='Preorder your pastries.<br>Choose when to collect.';label='FOR YOUR MORNING'
  content='''<div class="order-form"><div class="eyebrow">Crumb / Preorder</div><h2 style="margin-top:16px">Your morning order</h2><div class="rule"></div><div class="line"><span>Butter croissants</span><b>× 2</b></div><div class="line"><span>Pickup</span><b>Tomorrow</b></div><div class="slot"><span>Collection time</span><b>8:30 AM</b></div><div class="action">Reserve my breakfast</div></div><div class="confirm"><div class="check">✓</div><div class="eyebrow">Order confirmed</div><h2>See you<br>in the morning.</h2><div class="body">2 butter croissants<br>Tomorrow · 8:30 AM</div><div class="stamp">Reserved with Crumb</div></div>'''
  js='tl.to("#demo .action",{scale:.96,duration:.16,ease:"power1.in"},2.5);tl.to("#demo .action",{scale:1,duration:.42,ease:"power3.out"},2.66);tl.set("#demo .confirm",{opacity:0},0);tl.set("#demo .order-form",{opacity:0},3.1);tl.set("#demo .confirm",{opacity:1},3.1);tl.fromTo("#demo .confirm",{y:30},{y:0,duration:.4,ease:"power3.out"},3.1);'
 body=f'<div id="demo" class="frame paper">{header()}<div class="grid"><div class="intro"><div class="eyebrow arrive">{label}</div><h1 class="display arrive">{heading}</h1><p class="body arrive">{sub}</p></div><div class="ticket num">{content}</div></div>{footer("Illustrative product demo")}</div>'
 return scene(p,'demo',dur,body,enter('demo')+js)
def close(p,baker,dur):
 title='A list before<br>the oven.' if baker else 'Breakfast,<br>already<br>sorted.'
 steps=['Collect preorders','See what to bake','Prepare for pickup'] if baker else ['Pick your pastries','Choose your time','Collect at the bakery']
 body=f'<div id="closing" class="frame paper">{header()}<div class="close-wrap"><div class="intro"><div class="eyebrow arrive">{"LESS ORDER CHASING" if baker else "MORE MORNING. LESS GUESSWORK."}</div><h1 class="close-title arrive">{title}</h1></div><div><div class="steps">'+''.join(f'<div class="step arrive"><b>0{i+1}</b><span>{t}</span></div>' for i,t in enumerate(steps))+f'</div><p class="body" style="margin-top:40px">Bakery preorders with Crumb.</p></div></div>{footer("Crumb / Tomorrow starts here")}</div>'
 return scene(p,'close',dur,body,enter('closing'))
def food(p,file,dur,offset,cont=False):
 # Same left panel and composition across the generated joint protects layout continuity.
 title='Save the<br>good part.';sub='Preorder your croissants.<br>Choose a pickup time.'
 body=vid(file,dur,offset)+header()+f'<div class="foodcopy"><div class="eyebrow">Tomorrow, reserved.</div><h1 class="display">{title}</h1><div class="rule"></div><p class="body">{sub}</p></div>'
 return scene(p,'continuation' if cont else 'open',dur,body)
def music(path,duration,start,silent=[]):
 sr=48000;t=np.arange(round(duration*sr))/sr;mix=np.zeros((len(t),2));notes=[60,64,67,72,67,64,62,67]
 for i,at in enumerate(np.arange(start,duration-0.5,.5)):
  x=np.arange(round(1.5*sr))/sr;f=440*2**((notes[i%len(notes)]-69)/12)
  y=(np.sin(2*np.pi*f*x)+.23*np.sin(4*np.pi*f*x))*np.minimum(x/.008,1)*np.exp(-4*x)*(.07 if i%4==0 else .035)
  pos=round(at*sr);n=min(len(y),len(t)-pos);mix[pos:pos+n]+=y[:n,None]*np.array([1,.94])
 mix*=np.minimum((duration-t)/.7,1)[:,None]
 for a,b in silent:
  envelope=np.where(t<a,np.clip((a-t)/.3,0,1),np.where(t<b,0,np.clip((t-b)/.15,0,1)))
  mix*=envelope[:,None]
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((mix*32767).astype('<i2').tobytes())
def main():
 selection_path=ROOT/'selection.json'
 if not selection_path.exists():selection_path=Path('assembled_outputs/crumb_samples.json')
 select=json.loads(selection_path.read_text());build=[]
 for name in ['crumb-customer','crumb-baker','crumb-morning']:
  p=Path('hyperframes')/name;(p/'assets').mkdir(exist_ok=True);(p/'compositions').mkdir(exist_ok=True);sources=[]
  for old,new in [('CrewSans.ttf','sans.ttf'),('CrewSans-Bold.ttf','bold.ttf'),('CrewSerif.woff2','serif.woff2'),('gsap.min.js','gsap.min.js')]:sources.append(stage(p,Path('hyperframes/crew/assets')/old,new))
  aud='';baker=name=='crumb-baker'
  if name!='crumb-morning':
   take=select['interview' if baker else 'ugc'];sources.append(stage(p,take['path'],'person.mp4'));sources.append(stage_voice(p,take['path']))
   first=dialogue(p,'interview' if baker else 'ugc',take);speechdur=first[1]
   scenes=[first,demo(p,baker,8),close(p,baker,6)]
   aud=f'<audio id="speech-audio" src="assets/voice.wav" data-start="0" data-duration="{speechdur}" data-media-start="{take.get("in",0)}" data-track-index="10"></audio>'
   musicstart=speechdur
   if baker and 'return' in select:
    ret=select['return'];sources.append(stage(p,ret['path'],'return.mp4'))
    v=stage_voice(p,ret['path']);(p/'assets/voice.wav').rename(p/'assets/return.wav');v['staged']=str(p/'assets/return.wav');sources.append(v);stage_voice(p,take['path'])
    return_scene=dialogue(p,'interview',ret,'return','return.mp4')
    scenes=[first,demo(p,True,8),return_scene,close(p,True,4)]
    return_at=speechdur+8
    aud+=f'<audio id="return-audio" src="assets/return.wav" data-start="{return_at}" data-duration="{return_scene[1]}" data-media-start="{ret.get("in",0)}" data-track-index="10"></audio>'
  else:
   a=select['product'];b=select['continuation'];sources.append(stage(p,a['path'],'pastry.mp4'));sources.append(stage(p,b['path'],'continued.mp4'))
   scenes=[food(p,'pastry.mp4',a['out']-a.get('in',0),a.get('in',0)),food(p,'continued.mp4',b['out']-b.get('in',0),b.get('in',0),True),demo(p,False,6),close(p,False,4)];musicstart=0
  at=0;hosts='';times=[]
  for i,(ident,dur) in enumerate(scenes):
   hosts+=f'<div id="{ident}-host" class="clip host" data-composition-id="{ident}" data-composition-src="compositions/{ident}.html" data-start="{at}" data-duration="{dur}" data-width="1920" data-height="1080" data-track-index="{i}"></div>'
   times.append(dict(id=ident,start=at,duration=dur));at+=dur
  music(p/'assets/music.wav',at,musicstart, [(return_at,return_at+return_scene[1])] if baker and 'return' in select else []);aud+=f'<audio id="music-audio" src="assets/music.wav" data-start="0" data-duration="{at}" data-track-index="11"></audio>'
  sources.append(dict(source='original round9 deterministic music synthesis',staged=str(p/'assets/music.wav'),start=musicstart))
  (p/'index.html').write_text(f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{name}</title><script src="assets/gsap.min.js"></script><style>{CSS}</style></head><body><div id="root" data-composition-id="{name}" data-width="1920" data-height="1080" data-duration="{at}">{hosts}{aud}</div><script>window.__timelines["{name}"]=gsap.timeline({{paused:true}});</script></body></html>')
  (p/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
  (p/'STORYBOARD.md').write_text('# Crumb / final shot plan\n\n'+ '\n'.join(f'## Frame {i+1}\nstatus: built\nsrc: compositions/{s["id"]}.html\nstart: {s["start"]}\nduration: {s["duration"]}\nmotion: GSAP easing-and-stagger adapter + press-release-spring where UI confirms; generated source motion otherwise\n' for i,s in enumerate(times)))
  build.append(dict(name=name,project=str(p),duration=at,scenes=times,source_selection=select))
 (ROOT/'build.json').write_text(json.dumps(build,indent=2)+'\n');print(json.dumps(build,indent=2))
if __name__=='__main__':main()
