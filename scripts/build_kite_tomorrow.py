"""Kite Tomorrow: original four-scene HyperFrames launch film."""
from pathlib import Path
import html,json
P=Path(__file__).resolve().parents[1]/'videos/kite-tomorrow'
(P/'compositions').mkdir(exist_ok=True)
def text(v,x,y,s=32,w=400,c='#161615',anchor='start',id=''):
 return f'<text data-essential="true"'+(f' id="{id}"' if id else '')+f' x="{x}" y="{y}" font-size="{s}" font-weight="{w}" fill="{c}" text-anchor="{anchor}">{html.escape(v)}</text>'
def rect(x,y,w,h,c='#FFF',r=0,stroke='none'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" stroke="{stroke}" stroke-width="2"/>'
def line(x,y,x2,y2,c='#DEDBD6',width=2):return f'<path d="M{x} {y}L{x2} {y2}" stroke="{c}" stroke-width="{width}" fill="none"/>'
def g(id,s,extra=''):return f'<g id="{id}" {extra}>{s}</g>'
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">'+s+'</svg>'
def pill(v,x,y,w,c='#EEEAE4',ink='#161615'):
 return rect(x,y,w,46,c,23)+text(v,x+w/2,y+31,24,500,ink,'middle')
def button(v,x,y,w):return rect(x,y,w,60,'#FFFFFF',9,'#C8C5C1')+text(v,x+w/2,y+39,28,600,anchor='middle')
def circle(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def avatar(v,x,y,c='#E8E4DC',ink='#322B25'):
 return rect(x,y,64,64,c,14)+text(v,x+32,y+44,30,600,ink,'middle')
def label():return text('Illustrative workflow · Fictional company',88,1037,23,400,'#585650')
# Source notes repeated exactly across handoff and draft.
notes=['One inbox for the whole team','Assign an owner to every message','Keep replies and context together']
def note_card(x,y,w=850,h=320):
 s=rect(x,y,w,h,'#F7F5EF',15,'#E4DFD5')+rect(x+28,y+27,48,56,'#FF6D2D',8)+text('↗',x+52,y+65,30,600,anchor='middle')+text('Relay · Release notes',x+98,y+62,31,600)
 for i,v in enumerate(notes):s+=g(f'notes-item-{i}',circle(x+43,y+116+i*58,4,'#615E56')+text(v,x+65,y+126+i*58,30))
 return s
# Fictional product screen: recognizable assignment field is the visual proof.
def inbox(x,y,w=710,h=455,idprefix='inbox'):
 s=rect(x,y,w,h,'#FFF',18,'#D5D5C9')+rect(x,y,164,h,'#F1F1E7',18)
 s+=text('Relay',x+24,y+45,28,650)+text('Team inbox',x+24,y+104,21,550)+text('Assigned',x+24,y+150,20,c='#66665C')+text('All messages',x+190,y+47,28,600)
 s+=line(x+184,y+71,x+w-24,y+71,'#E1E1D8')
 for i,(name,subject) in enumerate([('Alex Chen','Question about our plan'),('Sam Rivera','Onboarding next steps'),('Taylor Kim','Thanks for the demo')]):
  yy=y+113+i*92
  s+=circle(x+204,yy+3,7,'#6F7847')+text(name,x+228,yy,23,600)+text(subject,x+228,yy+31,22,c='#626257')+line(x+184,yy+50,x+w-24,yy+50,'#E7E7DE')
 s+=g(idprefix+'-owner',rect(x+188,y+h-75,w-214,52,'#E6EDC8',9)+text('Owner',x+211,y+h-41,23,500,'#3B4621')+text('Maya',x+w-35,y+h-41,25,650,'#3B4621','end'))
 return s

def page(idprefix,headline=('A shared inbox.','A clearer day.')):
 s=rect(0,0,1640,790,'#F1F2E5',18)+line(0,88,1640,88,'#D4D8C3')
 s+=text('relay',58,58,38,650)+text('Product',1115,54,25,500)+text('How it works',1270,54,25,500)+pill('Get started',1444,25,153,'#28351F','#FFF')
 s+=pill('Introducing the team inbox',58,128,363,'#E1E6CB','#334026')
 s+=g(idprefix+'-hero',text(headline[0],58,282,76,600)+text(headline[1],58,368,76,600))
 s+=text('Bring customer conversations together.',60,431,29,c='#4A5140')+text('Give every message a clear owner.',60,473,29,c='#4A5140')
 s+=rect(58,514,314,68,'#28351F',34)+text('See the shared inbox',215,558,27,550,'#FFF','middle')
 s+=g(idprefix+'-app',inbox(875,135,710,455,idprefix))
 for i,(h,b) in enumerate([('One team inbox','Keep conversations together.'),('Clear ownership','Know who is taking the next step.'),('Shared context','Pick up where your team left off.')]):
  x=58+i*532
  s+=g(idprefix+f'-feature-{i}',line(x,651,x+464,651,'#B6BCA2')+text(h,x,700,30,600)+text(b,x,744,25,c='#505641'))
 return s

CSS='''@font-face{font-family:Onest;src:url('assets/Onest.woff2') format('woff2');font-weight:100 900}*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#F8F6F2}#root{position:relative;width:100%;height:100%;font-family:Onest,sans-serif}.clip{position:absolute;inset:0;width:100%;height:100%}svg{display:block;font-family:Onest,sans-serif}.photo{width:100%;height:100%;object-fit:cover}.layer{position:absolute;inset:0}'''
def write_scene(name,duration,body,js):
 out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>{CSS}</style></head><body><main id="root" data-composition-id="{name}" data-width="1920" data-height="1080" data-duration="{duration}" data-fps="30">{body}</main><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});{js}\nwindow.__timelines['{name}']=tl;</script></body></html>'''
 import re
 out=out.replace('id="root"',f'id="{name}-root"').replace('#root',f'#{name}-root')
 counter=iter(range(20))
 out=re.sub(r'<div class="clip"',lambda m:f'<div id="{name}-layer-{next(counter)}" class="clip"',out)
 (P/'compositions'/f'{name}.html').write_text(out)

# 1. Human + the missing page.
body='<video id="marketer" class="clip photo" src="assets/marketer.mp4" data-start="0" data-duration="3.6" data-playback-rate="0.5" data-track-index="0" muted playsinline></video>'
first=rect(64,71,710,157,'#F8F6F2',5)+text('The product’s',95,132,58,550)+text('ready.',95,197,58,650)
body+='<div class="clip" data-start="0" data-duration="3.6" data-track-index="1">'+svg(g('opening-title',first))+'</div>'
s=rect(0,0,1920,1080,'#F8F6F2')
s+=g('calendar',rect(88,114,441,330,'#FF6D2D',22)+text('ON THE CALENDAR',122,170,24,600)+text('Launch',122,269,70,600)+text('tomorrow.',122,356,70,600))
s+=g('missing-title',text('The page',88,581,80,550)+text('isn’t.',88,674,80,650))
s+=g('blank-page',rect(665,90,1167,871,'#FFF',18,'#DDDAD3')+rect(665,90,1167,78,'#ECE9E4',18)+circle(700,128,7,'#B9B5AD')+circle(727,128,7,'#B9B5AD')+circle(754,128,7,'#B9B5AD')+text('Relay · Launch page',808,139,27,500)+line(665,168,1832,168)+text('Launch page',761,287,51,550)+g('caret',rect(765,338,3,52,'#3E3C38')))
s+=text('A launch scenario',88,1016,23,c='#5F5D57')
body+='<div class="clip" data-start="3.6" data-duration="3.6" data-track-index="1">'+svg(s)+'</div>'
js="""tl.fromTo('#opening-title',{y:12,opacity:0},{y:0,opacity:1,duration:.55,ease:'power2.out'},.12);
tl.fromTo('#calendar',{y:20,opacity:0},{y:0,opacity:1,duration:.45,ease:'power2.out'},3.6);
tl.fromTo('#blank-page',{x:45,opacity:0},{x:0,opacity:1,duration:.5,ease:'power3.out'},3.6);
tl.fromTo('#missing-title',{y:20,opacity:0},{y:0,opacity:1,duration:.42,ease:'power2.out'},3.9);
tl.to('#caret',{opacity:0,duration:.12,repeat:6,yoyo:true,repeatDelay:.28},4.2);"""
write_scene('opening',7.2,body,js)

# 2. A Slack handoff and returned website card. No generic approval labels.
s=rect(0,0,1920,1080,'#F8F6F2')+text('Give Kite the launch page.',88,90,53,550)
s+=rect(88,136,1744,825,'#FFF',20,'#DCD8D0')+rect(88,136,278,825,'#39233C',20)
s+=text('Relay',122,199,33,650,'#FFF')+text('Channels',122,281,24,500,'#D5CCD7')+rect(105,308,244,58,'#6C4E6F',8)+text('# marketing',124,348,29,550,'#FFF')+text('# product',124,414,27,400,'#DED3DF')+text('Apps',122,524,24,500,'#D5CCD7')+text('Kite',124,579,28,550,'#FFF')
s+=text('# marketing',410,202,36,600)+line(367,230,1831,230)
s+=g('request-msg',avatar('M',410,277)+text('Maya',498,302,30,650)+text('Kite, turn these release notes',498,365,43,500,id='request-line-1')+text('into our launch page.',498,422,43,500,id='request-line-2')+g('notes-card',note_card(498,457,1030,302)))
s+=g('returned',avatar('K',410,277,'#FF6D2D')+text('Kite',498,304,31,650)+text('Here’s the page draft.',498,365,40,500)+rect(498,408,1060,346,'#F8F9F1',12,'#DADDD0')+text('relay',533,462,30,650)+text('A shared inbox. A clearer day.',533,528,41,600)+text('Bring customer conversations together.',533,575,29,c='#535B45')+button('Preview',533,632,171)+button('Review',725,632,165))
s+=g('preview-cursor-position',g('preview-cursor','<path d="M0 0L0 36L10 27L18 44L25 40L17 24L31 24Z" fill="#161615" stroke="#FFF" stroke-width="2"/>'),'transform="translate(632 662)"')
s+=label()
body='<div class="clip" data-start="0" data-duration="9.3" data-track-index="0">'+svg(s)+'</div>'
js="""tl.fromTo('#request-msg',{y:22,opacity:0},{y:0,opacity:1,duration:.55,ease:'power3.out'},.05);
tl.fromTo('#request-line-1',{opacity:0},{opacity:1,duration:.35},.4);
tl.fromTo('#request-line-2',{opacity:0},{opacity:1,duration:.35},1.05);
tl.fromTo('#notes-card',{y:15,opacity:0},{y:0,opacity:1,duration:.45},1.6);
for(let i=0;i<3;i++)tl.fromTo('#notes-item-'+i,{opacity:0,y:8},{opacity:1,y:0,duration:.4,ease:'power2.out'},2.2+i*.95);
tl.to('#request-msg',{y:-25,opacity:0,duration:.28,ease:'power2.in'},6.35);
tl.fromTo('#returned',{y:30,opacity:0},{y:0,opacity:1,duration:.4,ease:'power3.out'},6.6);
tl.fromTo('#preview-cursor',{opacity:0,x:38,y:40},{opacity:1,x:0,y:0,duration:.55,ease:'power2.out'},7.4);
tl.to('#preview-cursor',{scale:.86,duration:.1,yoyo:true,repeat:1,svgOrigin:'0 0'},8.5);"""
write_scene('handoff',9.3,body,js)

# 3. The same draft develops, then responds to one clear human instruction.
s=rect(0,0,1920,1080,'#F8F6F2')+text('From release notes to a real draft.',88,86,51,550)
s+=text('Website draft · preview',139,155,24,500,'#57594D')
s+=g('page-position',g('page-surface',page('draft')),'transform="translate(140 183)"')
# Feedback is in a cropped thread, editorially set beside the draft.
feedback=rect(1160,238,674,611,'#FFF',19,'#D8D4CD')+text('# marketing',1200,301,29,600)+line(1160,330,1834,330)+avatar('M',1200,371)+text('Maya',1284,399,28,600)+text('Lead with',1200,492,51,550)+text('shared ownership.',1200,556,51,550)+rect(1200,604,325,56,'#FFF0E5',28)+text('Your direction',1362,642,26,550,anchor='middle')
# Your direction is explicitly an editorial label, outside the Slack-like card in final markup below.
feedback=feedback.replace(rect(1200,604,325,56,'#FFF0E5',28)+text('Your direction',1362,642,26,550,anchor='middle'),'')
feedback+=text('A specific edit. A better draft.',1200,714,29,400,'#5A574F')
s+=g('feedback',feedback)
s+=g('revised-hero',text('Every message.',198,465,76,600)+text('Someone on it.',198,551,76,600))
s+=g('closing-line',rect(650,985,1100,66,'#161615',33)+text('Now we have something to work with.',1200,1029,32,500,'#FFF','middle'))
s+=label()
body='<div class="clip" data-start="0" data-duration="18.5" data-track-index="0">'+svg(s)+'</div>'
js="""tl.fromTo('#page-surface',{y:35,opacity:0},{y:0,opacity:1,duration:.55,ease:'power3.out'},0);
for(let i=0;i<3;i++)tl.fromTo('#draft-feature-'+i,{y:24,opacity:0},{y:0,opacity:1,duration:.48,ease:'power2.out'},1.8+i*1.0);
tl.fromTo('#draft-owner',{opacity:0},{opacity:1,duration:.55},4.8);
tl.to('#page-surface',{scale:.61,x:-70,y:118,transformOrigin:'0 0',duration:.7,ease:'power3.inOut'},8);
tl.fromTo('#feedback',{x:100,opacity:0},{x:0,opacity:1,duration:.55,ease:'power3.out'},8.45);
tl.to('#feedback',{x:60,opacity:0,duration:.4,ease:'power2.in'},12.8);
tl.to('#page-surface',{scale:1,x:0,y:0,duration:.7,ease:'power3.inOut'},13.2);
tl.to('#draft-hero',{opacity:0,y:-10,duration:.3},13.7);
tl.fromTo('#revised-hero',{opacity:0,y:14},{opacity:1,y:0,duration:.5,ease:'power2.out'},14.05);
tl.fromTo('#closing-line',{opacity:0,y:12},{opacity:1,y:0,duration:.4,ease:'power2.out'},15.5);"""
write_scene('draft',18.5,body,js)

# 4. Official wordmark, one CTA. No invented campaign URL.
s=rect(0,0,1920,1080,'#FFF')+g('end-wordmark','<image href="assets/kite-wordmark.png" x="570" y="132" width="780" height="465"/>')
s+=g('end-text',text('Give Kite your next launch.',960,650,62,550,anchor='middle')+rect(637,727,646,108,'#FF6D2D',54)+text('Add Kite to Slack',960,797,43,600,anchor='middle'))
s+=rect(0,1033,1920,47,'#FF6D2D')
body='<div class="clip" data-start="0" data-duration="3" data-track-index="0">'+svg(s)+'</div>'
js="""tl.fromTo('#end-wordmark',{y:20,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},0);
tl.fromTo('#end-text',{y:18,opacity:0},{y:0,opacity:1,duration:.5,ease:'power2.out'},.2);"""
write_scene('ending',3,body,js)

scenes=[('opening',0,7.2),('handoff',7.2,9.3),('draft',16.5,18.5),('ending',35,3)]
mounts=''.join(f'<div id="scene-{n}" class="clip" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-width="1920" data-height="1080" data-start="{t}" data-duration="{d}" data-track-index="1"></div>' for n,t,d in scenes)
root='''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Kite — Tomorrow</title><script src="assets/gsap.min.js"></script><style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#F8F6F2}#root{position:relative;width:100%;height:100%}.clip{position:absolute;inset:0;width:100%;height:100%}</style></head><body><main id="root" data-composition-id="kite-tomorrow" data-width="1920" data-height="1080" data-duration="38" data-fps="30">'''+mounts+'''<audio id="narration" src="assets/voice.wav" data-start="0" data-duration="38" data-track-index="5" data-volume="1"></audio><audio id="music-bed" src="assets/music.wav" data-start="0" data-duration="38" data-track-index="6" data-volume="0.65"></audio><audio id="sound-effects" src="assets/sfx.wav" data-start="0" data-duration="38" data-track-index="7" data-volume="0.6"></audio></main><script>window.__timelines=window.__timelines||{};window.__timelines['kite-tomorrow']=gsap.timeline({paused:true});</script></body></html>'''
(P/'index.html').write_text(root)
print('Built four scenes, 38 seconds, 1920x1080.')
