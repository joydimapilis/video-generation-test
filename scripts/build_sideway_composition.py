"""Author Sideway's original phone-to-walk customer story in HyperFrames."""
from pathlib import Path
import json,re,subprocess
P=Path('videos/sideway');F=P/'compositions/frames';F.mkdir(parents=True,exist_ok=True)
BG='#F7F4E8';INK='#202321';BLUE='#275BE8';YELLOW='#F7DF77';MUTED='#606660'
CSS=f'''@font-face{{font-family:'Space Grotesk';src:url('assets/fonts/SpaceGrotesk.ttf') format('truetype');font-weight:100 900;font-style:normal}}*{{box-sizing:border-box}}#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;font-family:'Space Grotesk',sans-serif;color:{INK}}}.pos{{position:absolute}}.paper{{background:{BG}}}.ink{{background:{INK};color:{BG}}}.blue{{color:{BLUE}}}.muted{{color:{MUTED}}}.label{{font-size:25px;font-weight:600;letter-spacing:2px}}.brand{{font-size:61px;font-weight:700;letter-spacing:-3px}}.h1{{font-size:91px;font-weight:600;letter-spacing:-4px;line-height:1.30}}.h2{{font-size:66px;font-weight:600;letter-spacing:-2.7px;line-height:1.06}}.body{{font-size:34px;line-height:1.3}}.button{{background:{BLUE};color:{BG};font-size:36px;font-weight:600;border-radius:60px;display:flex;align-items:center;justify-content:center}}.card{{background:{BG};border:2px solid #C8CABC;border-radius:14px}}.touch{{width:64px;height:64px;border:5px solid {BLUE};border-radius:50%;pointer-events:none;opacity:0}}.caption{{font-size:43px;font-weight:500;line-height:1.25;background:{INK};color:{BG};padding:24px 30px;border-radius:12px;text-align:center}}'''
def el(id,cls,style,content=''):return f'<div id="{id}" class="pos {cls}" style="{style}">{content}</div>'
def initial(pre):
 b=el(pre+'-app','paper','inset:0','')
 b+=el(pre+'-brand','brand','left:72px;top:112px','sideway<span style="color:#275BE8">↗</span>')
 b+=el(pre+'-meta','label muted','left:72px;top:233px','SATURDAY / YOUR NEIGHBORHOOD')
 b+=el(pre+'-title','h2','left:72px;top:315px;width:880px','Your saved places.')
 b+=el(pre+'-sub','body muted','left:72px;top:415px;width:900px','Let’s make a little plan.')
 for i,(letter,name,kind) in enumerate([('01','Morning Coffee','A slow start'),('02','Paper House','Books worth browsing'),('03','Pocket Park','A quiet corner')]):
  y=550+195*i
  b+=el(pre+f'-place{i}','card',f'left:72px;top:{y}px;width:936px;height:165px',f'<div style="position:absolute;left:25px;top:28px;width:104px;height:104px;background:#E4EAFB;border-radius:52px;display:flex;align-items:center;justify-content:center;color:{BLUE};font-size:34px;font-weight:600">{letter}</div><div style="position:absolute;left:159px;top:27px;font-size:42px;font-weight:500">{name}</div><div class="muted" style="position:absolute;left:159px;top:87px;font-size:29px">{kind}</div><div style="position:absolute;right:30px;top:54px;font-size:34px;color:{BLUE}">✓</div>')
 b+=el(pre+'-time-label','body','left:72px;top:1150px','How much time do you have?')
 for i,txt in enumerate(['30 min','60 min','90 min']):b+=el(pre+f'-time{i}','card',f'left:{72+i*320}px;top:1230px;width:296px;height:108px;display:flex;align-items:center;justify-content:center;font-size:35px',txt)
 b+=el(pre+'-selected','','left:392px;top:1230px;width:296px;height:108px;border:4px solid #275BE8;border-radius:14px;background:#E4EAFB;opacity:0', '<div style="padding-top:28px;text-align:center;font-size:35px;color:#275BE8;font-weight:600">60 min</div>')
 b+=el(pre+'-create','button','left:72px;top:1435px;width:936px;height:120px',el(pre+'-create-label','','inset:0;display:flex;align-items:center;justify-content:center','Create a walk ↗')+el(pre+'-building','','inset:0;opacity:0;display:flex;align-items:center;justify-content:center','Building your walk…'))
 return b
ROUTE='M 210 560 L 210 140 Q 210 105 245 105 L 660 105 Q 700 105 700 145 L 700 305 Q 700 345 660 345 L 435 345 Q 395 345 395 385 L 395 560 L 210 560'
def map_svg(pre,draw=False):
 # Custom fictional neighborhood map; stroke tracing adapted from installed svg-stroke-trace.
 blocks=''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{c}"/>' for x,y,w,h,c in [(12,15,140,380,'#E6E2D6'),(270,15,350,42,'#E6E2D6'),(270,160,340,120,'#E6E2D6'),(765,15,150,555,'#E6E2D6'),(470,410,245,165,'#D5E3CE'),(15,635,900,80,'#E6E2D6'),(15,435,130,130,'#E6E2D6')])
 b=f'<svg viewBox="0 0 936 720" width="936" height="720" role="img" aria-label="Illustrative route joining three saved places"><rect width="936" height="720" fill="#EEEBDD"/>{blocks}<path d="{ROUTE}" fill="none" stroke="#C7CEEA" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><path id="{pre}-route" d="{ROUTE}" fill="none" stroke="{BLUE}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
 for i,(x,y,label) in enumerate([(210,140,'1'),(700,305,'2'),(395,560,'3')]):b+=f'<g id="{pre}-pin{i}"><circle cx="{x}" cy="{y}" r="39" fill="{BG}" stroke="{BLUE}" stroke-width="6"/><text x="{x}" y="{y+13}" text-anchor="middle" font-family="Space Grotesk" font-size="36" font-weight="600" fill="{BLUE}">{label}</text></g>'
 b+=f'<circle cx="210" cy="560" r="15" fill="{BLUE}" stroke="{BG}" stroke-width="7"/></svg>'
 return b

def route_screen(pre,nav=False):
 b=el(pre+'-route-bg','paper','inset:0')+el(pre+'-route-brand','brand','left:72px;top:112px','sideway<span style="color:#275BE8">↗</span>')
 b+=el(pre+'-route-meta','label muted','left:72px;top:233px','YOUR SATURDAY / 60 MINUTES')
 b+=el(pre+'-route-title','h2','left:72px;top:315px;width:936px','One good walk.')
 b+=el(pre+'-map','','left:72px;top:460px;width:936px;height:720px;border-radius:14px;overflow:hidden',map_svg(pre))
 b+=el(pre+'-coffee-label','paper','left:330px;top:604px;padding:8px 15px;font-size:29px;border-radius:8px','Morning Coffee')
 b+=el(pre+'-books-label','paper','left:426px;top:798px;padding:8px 15px;font-size:29px;border-radius:8px','Paper House')
 b+=el(pre+'-park-label','paper','left:495px;top:1057px;padding:8px 15px;font-size:29px;border-radius:8px','Pocket Park')
 b+=el(pre+'-summary','','left:72px;top:1232px;width:936px;height:128px',f'<div style="font-size:41px;font-weight:600">3 stops · 22 min walking</div><div class="muted" style="font-size:32px;margin-top:14px">38 minutes to linger. Your hour, sorted.</div>')
 b+=el(pre+'-start','button','left:72px;top:1435px;width:936px;height:120px','Start walking ↗')
 return b

def nav_card(pre):
 return el(pre+'-nav','ink','left:72px;top:1338px;width:936px;height:225px;border-radius:14px;padding:30px 36px',f'<div style="color:{YELLOW};font-size:26px;letter-spacing:2px">WALK STARTED</div><div style="font-size:45px;margin-top:10px;font-weight:500">First stop: Morning Coffee</div><div style="font-size:31px;margin-top:8px">8 min away · Let’s go ↗</div>')
def write(name,dur,body,js):
 (F/f'{name}.html').write_text(f'<template><div id="root" data-composition-id="{name}" data-duration="{dur}" data-width="1080" data-height="1920"><style>{CSS}</style><div id="scene-{name}-layer" class="clip" data-start="0" data-duration="{dur}" style="position:absolute;inset:0">{body}</div><script>const tl=gsap.timeline({{paused:true}});{js}window.__timelines["{name}"]=tl;</script></div></template>')
def main():
 b=el('s1-hook','paper','left:60px;top:94px;width:770px;height:300px;padding:26px 35px;border-radius:14px','<div class="h1">Saved for</div><div class="h1">someday.</div>')
 b+=el('s1-saves','paper','left:60px;top:1438px;width:690px;height:98px;border-radius:14px;padding:25px 30px;font-size:33px','Coffee. Books. A quiet corner.')
 b+=el('s1-story-label','paper label','left:60px;top:96px;padding:20px 26px;border-radius:12px','A SMALL SATURDAY STORY')
 b+=el('s1-caption1','caption','left:80px;top:1630px;width:920px','I’d save all these places,')+el('s1-caption2','caption','left:80px;top:1630px;width:920px','then forget about them.')
 b+=el('s1-intro-brand','paper','left:60px;top:95px;width:860px;height:245px;padding:24px 32px;border-radius:14px','<div class="brand">sideway<span class="blue">↗</span></div><div style="font-size:37px;line-height:1.2;margin-top:16px">Your saved places. One good walk.</div>')
 b+=el('s1-app-surface','','inset:0',initial('s1'))
 j="""gsap.set('#s1-story-label,#s1-caption1,#s1-caption2,#s1-intro-brand',{opacity:0});
 tl.fromTo('#s1-hook',{y:20,opacity:0},{y:0,opacity:1,duration:.55,ease:'power3.out'},.05);
 tl.fromTo('#s1-saves',{y:25,opacity:0},{y:0,opacity:1,duration:.45},.9);
 tl.to('#s1-hook,#s1-saves',{opacity:0,duration:.16},2.82);
 tl.to('#s1-story-label',{opacity:1,duration:.2},3.05);tl.to('#s1-story-label',{opacity:0,duration:.15},5.82);
 tl.set('#s1-caption1',{opacity:1},3.02);tl.set('#s1-caption1',{opacity:0},4.55);tl.set('#s1-caption2',{opacity:1},4.55);tl.set('#s1-caption2',{opacity:0},5.9);
 tl.fromTo('#s1-intro-brand',{y:20,opacity:0},{y:0,opacity:1,duration:.4,ease:'power3.out'},6.1);
 tl.to('#s1-intro-brand',{opacity:0,duration:.15},8.5);
 gsap.set('#s1-app-surface',{x:650,y:1050,scale:.12,opacity:0,transformOrigin:'0 0'});tl.set('#s1-app-surface',{opacity:1},8.55);tl.to('#s1-app-surface',{x:0,y:0,scale:1,duration:1.15,ease:'power3.inOut'},8.55);
 tl.to({}, {duration:.01},9.99);"""
 write('01-someday',10,b,j)
 b=el('s2-initial','','inset:0',initial('s2'))+el('s2-route-screen','','inset:0',route_screen('s2'))+nav_card('s2')
 for name,x,y in [('time',508,1252),('create',508,1463),('start',508,1463)]:b+=el('s2-touch-'+name,'touch',f'left:{x}px;top:{y}px')
 j="""gsap.set('#s2-route-screen',{x:1080});gsap.set('#s2-nav',{opacity:0});
 tl.fromTo('#s2-touch-time',{scale:.3,opacity:0},{scale:1,opacity:.9,duration:.18},1.05);tl.to('#s2-touch-time',{scale:1.45,opacity:0,duration:.32},1.23);
 tl.set('#s2-time1',{opacity:0},1.2);tl.to('#s2-selected',{opacity:1,duration:.15},1.2);
 tl.fromTo('#s2-touch-create',{scale:.3,opacity:0},{scale:1,opacity:.9,duration:.18},3.05);tl.to('#s2-touch-create',{scale:1.45,opacity:0,duration:.32},3.23);
 tl.to('#s2-create',{scale:.985,duration:.11},3.18);tl.to('#s2-create',{scale:1,duration:.15},3.3);
 tl.to('#s2-create-label',{opacity:0,duration:.12},3.3);tl.to('#s2-building',{opacity:1,duration:.15},3.4);
 tl.to('#s2-initial',{opacity:0,duration:.25},4.15);tl.to('#s2-route-screen',{x:0,duration:.65,ease:'power3.inOut'},4.15);
 const path=document.getElementById('s2-route');const len=path.getTotalLength();gsap.set(path,{strokeDasharray:len,strokeDashoffset:len});
 gsap.set('#s2-pin0,#s2-pin1,#s2-pin2,#s2-coffee-label,#s2-books-label,#s2-park-label,#s2-summary,#s2-start',{opacity:0});
 tl.to(path,{strokeDashoffset:0,duration:4.2,ease:'none'},5.05);
 tl.to('#s2-pin0,#s2-coffee-label',{opacity:1,duration:.3},5.3);tl.to('#s2-pin1,#s2-books-label',{opacity:1,duration:.3},6.85);tl.to('#s2-pin2,#s2-park-label',{opacity:1,duration:.3},8.3);
 tl.fromTo('#s2-summary',{y:20,opacity:0},{y:0,opacity:1,duration:.5},9.5);
 tl.fromTo('#s2-start',{y:20,opacity:0},{y:0,opacity:1,duration:.4},11.1);
 tl.fromTo('#s2-touch-start',{scale:.3,opacity:0},{scale:1,opacity:.9,duration:.18},13.05);tl.to('#s2-touch-start',{scale:1.45,opacity:0,duration:.32},13.23);
 tl.to('#s2-start',{scale:.985,duration:.12},13.18);tl.to('#s2-start',{scale:1,duration:.15},13.3);
 tl.to('#s2-start,#s2-summary',{opacity:0,duration:.2},13.45);
 tl.fromTo('#s2-nav',{y:30,opacity:0},{y:0,opacity:1,duration:.45,ease:'power3.out'},13.65);
 tl.to({}, {duration:.01},15.99);"""
 write('02-one-walk',16,b,j)
 b=el('s3-cover','','inset:0',route_screen('s3'))+nav_card('s3')
 b+=el('s3-arrived','ink','left:72px;top:1338px;width:936px;height:225px;border-radius:14px;padding:30px 36px',f'<div style="color:{YELLOW};font-size:26px;letter-spacing:2px">MORNING COFFEE / ARRIVED</div><div style="font-size:48px;margin-top:14px;font-weight:500">First stop, made it.</div><div style="font-size:31px;margin-top:8px">A saved place. A real Saturday.</div>')
 b+=el('s3-caption','caption','left:80px;top:1640px;width:920px','<div>Sideway maps them out for me.</div><div>Way easier.</div>')
 end=el('s3-end-bg','paper','inset:0')+el('s3-end-brand','brand','left:72px;top:166px;font-size:91px','sideway<span class="blue">↗</span>')
 end+=el('s3-end-kicker','label muted','left:76px;top:309px','YOUR SAVED PLACES, OUT IN THE WORLD')
 end+=el('s3-end-route','','left:92px;top:520px;width:880px;height:300px','<svg width="880" height="300" viewBox="0 0 880 300"><path id="s3-end-path" d="M 70 220 L70 80 Q70 50 100 50 L430 50 Q470 50 470 90 L470 180 Q470 220 510 220 L800 220" fill="none" stroke="#275BE8" stroke-width="13" stroke-linejoin="round" stroke-linecap="round"/><circle cx="70" cy="220" r="20" fill="#275BE8"/><circle cx="470" cy="95" r="20" fill="#275BE8"/><circle cx="800" cy="220" r="35" fill="#275BE8"/><path d="M782 219 l13 14 23 -28" fill="none" stroke="#F7F4E8" stroke-width="7"/></svg>')
 end+=el('s3-end-copy','h1','left:72px;top:900px;width:936px;font-size:112px;line-height:1.3','<div>Less saving.</div><div>More going.</div>')
 end+=el('s3-end-cta','button','left:72px;top:1270px;width:936px;height:125px','Make a little plan ↗')
 end+=el('s3-end-small','body muted','left:76px;top:1485px;font-size:31px','Saved places → a walk that fits.')
 b+=el('s3-ending','','inset:0',end)
 j="""gsap.set('#s3-summary,#s3-start',{opacity:0});gsap.set('#s3-arrived,#s3-caption',{opacity:0});gsap.set('#s3-ending',{y:1920});
 tl.to('#s3-cover',{y:-1920,duration:.8,ease:'power3.inOut'},.2);
 tl.to('#s3-nav',{opacity:0,duration:.25},1.15);tl.to('#s3-arrived',{opacity:1,duration:.35},1.25);
 tl.set('#s3-caption',{opacity:1},1.5);tl.set('#s3-caption',{opacity:0},4.55);
 tl.to('#s3-arrived',{opacity:0,duration:.2},5.4);
 tl.to('#s3-ending',{y:0,duration:.8,ease:'power3.inOut'},5.55);
 tl.fromTo('#s3-end-brand,#s3-end-kicker',{y:25,opacity:0},{y:0,opacity:1,duration:.5,stagger:.1,ease:'power3.out'},6.05);
 const path=document.getElementById('s3-end-path');const len=path.getTotalLength();gsap.set(path,{strokeDasharray:len,strokeDashoffset:len});tl.to(path,{strokeDashoffset:0,duration:1.2,ease:'power2.out'},6.25);
 tl.fromTo('#s3-end-copy',{y:30,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},6.75);
 tl.fromTo('#s3-end-cta,#s3-end-small',{y:20,opacity:0},{y:0,opacity:1,duration:.45,stagger:.12},7.5);
 tl.to({}, {duration:.01},9.99);"""
 write('03-go',10,b,j)
 (P/'STORYBOARD.md').write_text((P/'STORYBOARD.md').read_text().replace('status: outline','status: animated'))
 subprocess.run(['node',str(Path.home()/'.agents/skills/product-launch-video/scripts/assemble-index.mjs'),'--storyboard',str(P/'STORYBOARD.md'),'--hyperframes',str(P)],check=True)
 f=P/'index.html';s=f.read_text();s=re.sub(r'<script src="https://cdn[^>]+></script>','<script src="assets/gsap.min.js"></script>',s);s=s.replace('width: 1080px;\n        height: 1920px;','width: 100%;\n        height: 100%;').replace('class="scene"','class="scene clip"').replace('background: #000;',f'background: {BG};');s=s.replace('    </style>','      .scene {z-index:2;}\n    </style>')
 media=''
 for id,src,start,dur,offset in [('phone-a','phone',0,3,0),('story','story',3,3,0),('phone-b','phone',6,4,1),('arrival','arrival',26,6,0)]:media+=f'<video id="sideway-{id}" class="clip" src="assets/{src}.mp4" data-start="{start}" data-duration="{dur}" data-media-start="{offset}" data-playback-rate="{0.5 if id == "phone-b" else 1}" data-track-index="20" muted playsinline style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;z-index:1"></video>\n'
 media+='<audio id="sideway-speech" src="assets/speech.wav" data-start="0" data-duration="36" data-track-index="30" data-volume="1"></audio><audio id="sideway-score" src="assets/score.wav" data-start="0" data-duration="36" data-track-index="31" data-volume="1"></audio>'
 s=s.replace('      <!-- BGM -->',media+'\n      <!-- BGM -->') if '      <!-- BGM -->' in s else s.replace('    </div>\n\n    <script>',media+'\n    </div>\n\n    <script>');f.write_text(s)
 (P/'index.motion.json').write_text(json.dumps({'duration':36,'assertions':[{'kind':'appearsBy','selector':'#s1-hook','bySec':.8},{'kind':'appearsBy','selector':'#s2-selected','bySec':11.5},{'kind':'appearsBy','selector':'#s2-nav','bySec':24.5},{'kind':'appearsBy','selector':'#s3-end-copy','bySec':33.6},{'kind':'appearsBy','selector':'#s2-pin2','bySec':19},{'kind':'staysInFrame','selector':'#s3-end-cta'}]},indent=2)+'\n')
if __name__=='__main__':main()
