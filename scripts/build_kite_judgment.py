"""Build the original, caption-led Kite brand film with deterministic motion."""
from pathlib import Path
import html,json
R=Path(__file__).resolve().parents[1];P=R/'videos/kite-judgment';F=P/'compositions/frames';F.mkdir(parents=True,exist_ok=True)
BG='#0E0E0E'; WHITE='#FFFFFF'; PAPER='#F3F0E9'; ORANGE='#FF6D2D'; GREY='#B3B3B3'
def text(x,y,s,size=40,color=WHITE,weight=550,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" data-essential="true" {extra}>{html.escape(s)}</text>'
def rect(x,y,w,h,fill,rx=0,extra=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'
def line(x,y,xx,yy,color=GREY,width=3,extra=''):
 return f'<path d="M{x} {y} L{xx} {yy}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" {extra}/>'
def card(kind,w=300,h=220):
 s=rect(7,10,w,h,'#34312D',12)+rect(0,0,w,h,PAPER,12)+text(26,51,kind,34,BG,650)
 if kind=='Research':
  s+=f'<circle cx="60" cy="115" r="25" fill="none" stroke="{ORANGE}" stroke-width="6"/>'+line(79,134,98,153,ORANGE,6)
  s+=line(133,102,w-28,102,'#B5B1A9',8)+line(133,129,w-50,129,'#C9C5BD',8)+line(28,180,w-50,180,'#C9C5BD',7)
 elif kind=='Message':
  s+=text(25,139,'Aa',72,BG,650)+line(144,108,w-28,108,'#B5B1A9',7)+line(144,136,w-40,136,'#C9C5BD',7)+line(27,180,w-27,180,'#C9C5BD',7)
 elif kind=='Page':
  s+=rect(26,80,w-52,91,'#D7D2C8',5)+rect(40,96,105,13,ORANGE,4)+rect(40,122,172,7,'#B5B1A9',3)+rect(40,142,76,15,BG,7)+line(28,192,w-68,192,'#C9C5BD',6)
 elif kind=='Walkthrough':
  s+=rect(26,81,w-52,100,'#D7D2C8',8)+f'<path d="M{w/2-11} 104 L{w/2+23} 128 L{w/2-11} 152 Z" fill="{ORANGE}"/>'+line(30,199,w-31,199,'#B5B1A9',4)
 elif kind=='Email':
  s+=rect(26,84,w-52,105,'none',7,f'stroke="#B5B1A9" stroke-width="3"')+f'<path d="M27 86 L{w/2} 149 L{w-27} 86" fill="none" stroke="{ORANGE}" stroke-width="5"/>'
 return s

def template(cid,dur,body,js):
 return f'''<template>
<style>@font-face{{font-family:Onest;src:url('assets/Onest.woff2') format('woff2');font-weight:100 900;font-display:block}}#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;color:white;font-family:Onest,sans-serif}}.clip{{position:absolute;inset:0}}svg{{width:100%;height:100%;display:block}}text{{font-family:Onest,sans-serif;letter-spacing:-.025em}}</style>
<div id="root" data-composition-id="{cid}" data-duration="{dur}" data-width="1920" data-height="1080">
<div id="{cid}-ground" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="background:{BG}"></div>
<div id="{cid}-art" class="clip" data-start="0" data-duration="{dur}" data-track-index="1"><svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">{body}</svg></div>
</div><script src="assets/gsap.min.js"></script><script>(function(){{const tl=gsap.timeline({{paused:true}});{js}window.__timelines=window.__timelines||{{}};window.__timelines['{cid}']=tl;}})();</script></template>'''
# Scene 1. One idea acquires all of the coordination around it.
body=''
body+='<g id="j1-opening">'+text(120,220,'The idea is',118,WHITE,650)+text(120,354,'the easy part.',118,WHITE,650)+'</g>'
body+='<g id="j1-idea">'+rect(0,0,425,280,ORANGE,16)+text(35,66,'THE IDEA',25,BG,600)+text(35,177,'Launch.',84,BG,650)+line(37,225,385,225,BG,3)+'</g>'
body+='<g id="j1-around">'+text(120,190,'Then comes',105,WHITE,650)+text(120,310,'everything around it.',105,WHITE,650)+'</g>'
body+='<g id="j1-question">'+text(120,190,'Who’s keeping',105,WHITE,650)+text(120,310,'it all moving?',105,ORANGE,650)+'</g>'
# These are abstract connecting threads, not product UI.
body+='<g id="j1-tangles" opacity="0.55"><path d="M285 585 C640 350 875 860 1210 710 S1700 600 1640 470" stroke="#55504A" stroke-width="3" fill="none"/><path d="M350 720 C950 955 935 420 1530 625" stroke="#55504A" stroke-width="3" fill="none"/><path d="M650 540 C550 830 1180 880 1450 530" stroke="#55504A" stroke-width="3" fill="none"/></g>'
body+='<g id="j1-rail">'+line(145,797,1775,797,ORANGE,5)+'</g>'
labels=['Research','Message','Page','Walkthrough','Email']
for i,k in enumerate(labels):body+=f'<g id="j1-card-{i}">{card(k)}</g>'
js='''
// Registry text-stagger entrance adapted to SVG line groups, with brand-safe solid type.
tl.fromTo('#j1-opening',{y:35,opacity:1},{y:0,opacity:1,duration:.65,ease:'power3.out'},0);
tl.fromTo('#j1-idea',{x:1355,y:244,rotation:7,scale:.86,opacity:0},{x:1325,y:220,rotation:4,scale:1,opacity:1,duration:.75,ease:'power3.out'},.25);
tl.to('#j1-opening',{opacity:0,y:-30,duration:.35,ease:'power2.in'},3.25);
tl.to('#j1-idea',{x:1320,y:95,scale:.48,rotation:0,opacity:0,duration:.65,ease:'power3.inOut'},3.25);
tl.fromTo('#j1-around',{opacity:0,y:36},{opacity:1,y:0,duration:.65,ease:'power3.out'},3.6);
tl.fromTo('#j1-tangles',{opacity:0},{opacity:.55,duration:1.2,ease:'power2.out'},4.8);
'''
poses=[(150,510,-9),(500,636,7),(795,447,-6),(1112,631,8),(1465,461,-7)]
for i,(x,y,rot) in enumerate(poses):
 js+=f"tl.fromTo('#j1-card-{i}',{{x:{x+(-60 if i%2==0 else 60)},y:{y+120},rotation:{rot+8},scale:.75,opacity:0}},{{x:{x},y:{y},rotation:{rot},scale:1,opacity:1,duration:.85,ease:'power3.out'}},{4.25+i*.62});\n"
 js+=f"tl.to('#j1-card-{i}',{{x:{x+12},y:{y-15},rotation:{rot-2},duration:1.4,ease:'sine.inOut',repeat:1,yoyo:true}},{7.8+i*.07});\n"
 js+=f"tl.to('#j1-card-{i}',{{x:{140+330*i},y:490,rotation:0,scale:.9,duration:1.1,ease:'power3.inOut'}},{12+i*.10});\n"
js+='''tl.to('#j1-around',{opacity:0,y:-24,duration:.32},9.45);
tl.fromTo('#j1-question',{opacity:0,y:34},{opacity:1,y:0,duration:.65,ease:'power3.out'},9.8);
tl.fromTo('#j1-rail',{scaleX:0,svgOrigin:'145 797',opacity:0},{scaleX:1,opacity:1,duration:1.3,ease:'power3.inOut'},12.0);
tl.to('#j1-tangles',{opacity:0,duration:.6},12);
tl.to('#j1-question',{opacity:0,y:-20,duration:.35},13.5);
'''
(F/'01-friction.html').write_text(template('j-friction',14,body,js))
# Scene 2. Same five objects and same orange route at the cut.
body='<g id="j2-rail">'+line(145,797,1775,797,ORANGE,5)+'</g>'
for i,k in enumerate(labels):body+=f'<g id="j2-card-{i}">{card(k)}</g>'
body+='<g id="j2-intro">'+text(120,190,'Give the work to Kite.',110,WHITE,650)+text(124,294,'Your AI marketer in Slack.',45,GREY,450)+'</g>'
heads=[('context','Business context.'),('plan','A connected plan.'),('drafts','Drafts for your review.')]
for id_,s in heads:body+=f'<g id="j2-title-{id_}">'+text(120,190,s,106,WHITE,650)+'</g>'
# Three distinctive objects, not a decorative dashboard or identical grid.
body+='<g id="j2-context">'+rect(8,10,360,264,'#34312D',12)+rect(0,0,360,264,PAPER,12)+rect(0,0,154,47,ORANGE,10)+text(22,33,'CONTEXT',23,BG,650)+text(30,108,'Product',36,BG,600)+text(30,165,'Audience',36,BG,600)+text(30,222,'Market',36,BG,600)+line(272,92,327,92,'#B8B3AA',6)+line(272,149,327,149,'#B8B3AA',6)+line(272,206,327,206,'#B8B3AA',6)+'</g>'
body+='<g id="j2-plan">'+rect(7,10,350,270,'#34312D',12)+rect(0,0,350,270,'#25221F',12,'stroke="#71685F" stroke-width="2"')+text(28,55,'PLAN',25,ORANGE,650)+line(31,110,31,225,ORANGE,3)
for y,s in [(116,'Priorities'),(171,'Message'),(226,'Next steps')]:body+=f'<circle cx="31" cy="{y-12}" r="6" fill="{ORANGE}"/>'+text(58,y,s,33,WHITE,550)
body+='</g>'
body+='<g id="j2-drafts">'+rect(20,-22,358,264,'#575048',12)+rect(10,-11,358,264,'#ABA397',12)+rect(0,0,358,264,PAPER,12)+text(29,52,'DRAFTS',25,BG,650)
for j,s in enumerate(['Page','Story','Email']):body+=rect(27,77+54*j,304,41,'#E4DFD6',5)+text(43,106+54*j,s,29,BG,600)+line(217,94+54*j,307,94+54*j,ORANGE,4)
body+='</g>'
body+='<g id="j2-context-label">'+text(235,902,'Research the business',32,GREY,450)+'</g>'
body+='<g id="j2-plan-label">'+text(795,902,'Connect the work',32,GREY,450)+'</g>'
body+='<g id="j2-drafts-label">'+text(1315,902,'Bring it back',32,GREY,450)+'</g>'
body+='<g id="j2-dot"><circle cx="0" cy="797" r="12" fill="#FF6D2D"/><circle cx="0" cy="797" r="5" fill="#0E0E0E"/></g>'
js=''
for i in range(5):
 js+=f"tl.fromTo('#j2-card-{i}',{{x:{140+330*i},y:490,rotation:0,scale:.9}},{{x:{140+330*i},y:490,rotation:0,scale:.9,duration:.001}},0);tl.to('#j2-card-{i}',{{x:{670+i*80},y:565,scale:.5,opacity:0,duration:.7,ease:'power3.inOut'}},{3.25+i*.07});\n"
js+='''tl.fromTo('#j2-intro',{y:32,opacity:0},{y:0,opacity:1,duration:.65,ease:'power3.out'},.1);
tl.to('#j2-intro',{opacity:0,y:-25,duration:.4},3.3);
'''
for i,(id_,s) in enumerate(heads):
 a=3.9+i*3.4;b=a+3.1
 js+=f"tl.fromTo('#j2-title-{id_}',{{y:35,opacity:0}},{{y:0,opacity:1,duration:.6,ease:'power3.out'}},{a});"
 if i<2:js+=f"tl.to('#j2-title-{id_}',{{opacity:0,y:-24,duration:.3}},{b});"
 x=[235,785,1320][i]
 js+=f"tl.fromTo('#j2-{id_}',{{x:{x},y:540,scale:.9,opacity:0}},{{x:{x},y:435,scale:1,opacity:1,duration:.8,ease:'power3.out'}},{a+.35});"
 js+=f"tl.fromTo('#j2-{id_}-label',{{opacity:0,y:18}},{{opacity:1,y:0,duration:.65,ease:'power2.out'}},{a+.6});"
js+='''tl.fromTo('#j2-dot',{x:145,opacity:0},{x:400,opacity:1,duration:.9,ease:'power2.inOut'},4.1);
tl.to('#j2-dot',{x:945,duration:1,ease:'power3.inOut'},7.5);
tl.to('#j2-dot',{x:1480,duration:1,ease:'power3.inOut'},10.9);
'''
(F/'02-flow.html').write_text(template('j-flow',16,body,js))
# Scene 3. Editorial decision boundary, then the official lockup. No control or click.
body='<g id="j3-decision">'+text(120,190,'The work moves forward.',105,WHITE,650)
body+='<g id="j3-papers">'+rect(24,-24,426,300,'#575048',12)+rect(12,-12,426,300,'#ABA397',12)+rect(0,0,426,300,PAPER,12)+text(30,63,'Marketing drafts',37,BG,650)
for j,s in enumerate(['Page','Story','Email']):body+=text(32,131+55*j,s,33,BG,500)+line(191,120+55*j,389,120+55*j,'#BDB7AC',7)
body+='</g>'
body+='<g id="j3-route">'+line(700,672,1015,672,ORANGE,5)+'</g>'
body+='<g id="j3-boundary">'+line(1070,448,1070,884,ORANGE,7)+'</g>'
body+='<g id="j3-your-call">'+text(1190,624,'Your call.',103,ORANGE,650)+text(1195,710,'What goes public.',37,WHITE,450)+'</g>'
body+='<g id="j3-subline">'+text(123,299,'The final say stays yours.',48,GREY,450)+'</g></g>'
# PNG's native transparent padding is preserved; no clipping or alteration.
body+='<g id="j3-lockup"><image href="assets/kite-white.png" x="635" y="50" width="650" height="389"/>'+text(960,515,'Move the work forward.',64,WHITE,600,'text-anchor="middle"')+text(960,596,'Keep the final say.',64,WHITE,600,'text-anchor="middle"')+rect(691,692,538,92,ORANGE,46)+text(960,752,'Add Kite to Slack',36,BG,650,'text-anchor="middle"')+text(960,866,'kite.ai',33,GREY,450,'text-anchor="middle"')+'</g>'
js='''tl.fromTo('#j3-decision',{opacity:1},{opacity:1,duration:.001},0);
tl.fromTo('#j3-papers',{x:160,y:510,opacity:0},{x:265,y:510,opacity:1,duration:1.15,ease:'power3.out'},.15);
tl.fromTo('#j3-route',{scaleX:0,svgOrigin:'700 672',opacity:0},{scaleX:1,opacity:1,duration:.95,ease:'power3.inOut'},.35);
tl.fromTo('#j3-boundary',{scaleY:0,svgOrigin:'1070 672',opacity:0},{scaleY:1,opacity:1,duration:.65,ease:'power3.out'},.8);
tl.fromTo('#j3-your-call',{x:35,opacity:0},{x:0,opacity:1,duration:.7,ease:'power3.out'},1.25);
tl.fromTo('#j3-subline',{y:24,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},1.55);
tl.to('#j3-decision',{opacity:0,duration:.001},5.999);
tl.fromTo('#j3-lockup',{opacity:0},{opacity:1,duration:.001},5.999);
'''
(F/'03-judgment.html').write_text(template('j-judgment',10,body,js))
index='''<!doctype html><html><head><meta charset="utf-8"><title>Kite — Keep the final say</title><style>html,body{margin:0;width:100%;height:100%;background:#0E0E0E;overflow:hidden}#root{width:100%;height:100%;position:relative;background:#0E0E0E}.clip{position:absolute;inset:0}</style></head><body><div id="root" data-composition-id="kite-judgment" data-duration="40" data-width="1920" data-height="1080">'''
for name,cid,at,dur in [('01-friction','j-friction',0,14),('02-flow','j-flow',14,16),('03-judgment','j-judgment',30,10)]:
 index+=f'<div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/frames/{name}.html" data-start="{at}" data-duration="{dur}" data-width="1920" data-height="1080" data-track-index="0"></div>'
index+='''<audio id="judgment-score" src="assets/score.wav" data-start="0" data-duration="40" data-volume="1" data-track-index="2"></audio><audio id="judgment-sfx" src="assets/sfx.wav" data-start="0" data-duration="40" data-volume="0.55" data-track-index="3"></audio></div><script src="assets/gsap.min.js"></script><script>window.__timelines=window.__timelines||{};window.__timelines['kite-judgment']=gsap.timeline({paused:true});</script></body></html>'''
(P/'index.html').write_text(index)
(P/'STORYBOARD.md').write_text('''# Keep the final say — production shot plan

40 seconds, 1920×1080, 30fps. Kinetic copy is the narrative; no voiceover or separate subtitles. All objects are editorial illustrations. Native product UI is absent.

## Video direction
One dark field, warm-white work objects, orange shared route. Friction becomes alignment; purposeful stillness marks the human decision. No generic AI effects, customer imagery, counters or implied publication. Opening copy has 3.25 seconds, the next sentence 5.8 seconds, context/plan/drafts titles roughly 3.4 seconds each. Closing lockup holds four seconds.

## Frame 1 — 0–14 seconds
compositions/frames/01-friction.html. The idea is the easy part, accompanied by one orange Launch sheet. Then comes everything around it: Research, Message, Page, Walkthrough, Email arrive in offset positions. Who’s keeping it all moving? An orange route draws; the same objects align.
Handoff: five original cards x=140+330*i, y=490, scale=.9, rotation=0, opacity=1. Orange route x145 to1775, y797, thickness5, opacity1. No velocity at14s. Heading fully faded.

## Frame 2 — 14–30 seconds
compositions/frames/02-flow.html. Same card handoff. Give the work to Kite. Your AI marketer in Slack. At17.9 context appears, at21.3 the plan, at24.7 marketing drafts. The orange dot advances through these editorial stages and stops. End holds three objects and Drafts for your review. Deliberate clean reframe into the next scene.

## Frame 3 — 30–40 seconds
compositions/frames/03-judgment.html. Marketing draft sheets approach a route that stops before an orange boundary. Your call / What goes public appears on the other side. No button, cursor, checkmark, approval toggle, boundary crossing or public result. At36 the objects clear into the official wordmark, Move the work forward / Keep the final say, Add Kite to Slack and kite.ai.

All frames animated in serial under the skill fallback; no external worker delegation requested. Same deterministic core contract used throughout.
''')
(P/'SCRIPT.md').write_text('''# Original on-screen script

The idea is the easy part.
Then comes everything around it.
Who’s keeping it all moving?
Give the work to Kite.
Your AI marketer in Slack.
Business context.
A connected plan.
Drafts for your review.
The work moves forward.
The final say stays yours.
Your call. What goes public.
Move the work forward. Keep the final say.
Add Kite to Slack.
kite.ai

No spoken script. Instrumental-led, all meaning available with sound off. Object labels are generic categories, not Kite UI terminology.
''')
print('Built three original scenes, 40 seconds.')
