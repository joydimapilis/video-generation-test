"""Fresh Serein film: reviewed image-first humans and exact focus-planning UI."""
from pathlib import Path
import json, re, subprocess
R=Path(__file__).resolve().parents[1]; P=R/'videos/serein'
CSS='''
@font-face{font-family:SereinSerif;src:url('assets/fonts/SourceSerif4.ttf');font-weight:200 900}@font-face{font-family:SereinSans;src:url('assets/fonts/Inter.ttf');font-weight:100 900}
*{box-sizing:border-box}#root{position:relative;width:100%;height:100%;overflow:hidden;color:#183F36;font-family:SereinSans,sans-serif}.clip,.stage{position:absolute;inset:0}.stage{overflow:hidden}.pos{position:absolute}.serif{font-family:SereinSerif,serif;font-weight:450;letter-spacing:-2.5px;line-height:1.02}.serif>div{line-height:1.4}.label{font-size:20px;font-weight:550;letter-spacing:2.5px}.brand{font-family:SereinSerif,serif;font-size:56px;letter-spacing:-2px}.app{position:absolute;left:100px;top:180px;width:1720px;height:720px;background:#F4F1E9;border:2px solid #183F36;border-radius:8px}.appbar{position:absolute;left:0;top:0;width:100%;height:100px;border-bottom:1px solid #96ABA3}.appbrand{position:absolute;left:38px;top:17px;font-family:SereinSerif,serif;font-size:44px;letter-spacing:-1px}.apptag{position:absolute;left:240px;top:40px;font-size:17px;letter-spacing:2px}.today{position:absolute;right:40px;top:36px;font-size:23px}.button{position:absolute;height:66px;display:flex;justify-content:center;align-items:center;background:#183F36;color:#F4F1E9;font-weight:550;font-size:26px;border-radius:6px}.task{position:absolute;left:145px;width:685px;height:114px;border:1px solid #A6B6AD;border-radius:6px;background:#F4F1E9}.task-title{position:absolute;left:24px;top:21px;font-size:29px;font-weight:550;letter-spacing:-.6px}.task-sub{position:absolute;left:24px;top:69px;font-size:21px}.task-time{position:absolute;right:22px;top:69px;font-size:21px}.summary{position:absolute;left:100px;top:270px;width:700px;height:550px;background:#183F36;color:#F4F1E9;border-radius:8px}.summary-label{position:absolute;left:42px;top:40px;font-size:18px;letter-spacing:2.3px}.summary-name{position:absolute;left:42px;top:104px;width:580px;font-family:SereinSerif,serif;font-size:58px;line-height:1.03;letter-spacing:-1px}.summary-time{position:absolute;left:42px;top:287px;font-family:SereinSerif,serif;font-size:67px;letter-spacing:-2px}.summary-duration{position:absolute;left:43px;top:375px;font-size:27px}.summary-rule{position:absolute;left:42px;top:438px;width:616px;height:1px;background:#87A59A}.summary-status{position:absolute;left:43px;top:466px;font-size:22px}.cursor{position:absolute;left:0;top:0;width:46px;height:46px;z-index:20}.pulse{position:absolute;left:-12px;top:-12px;width:38px;height:38px;border:2px solid #183F36;border-radius:50%;opacity:0}.calendar-line{position:absolute;left:980px;width:782px;height:1px;background:#CBD4CD}.hour{position:absolute;left:911px;font-size:19px;color:#385F51}.event{position:absolute;left:1065px;width:650px;height:42px;border-left:4px solid #60877B;border-radius:3px;background:#E2E8E2;font-size:21px;padding:8px 16px}
'''
def e(i,c,s,b):return f'<div id="{i}" {"data-layout-allow-overflow" if i == "s3-ending" else ""} class="{c}" style="{s}">{b}</div>'
def app(p):return e(p+'-app','app','',e(p+'-bar','appbar','',e(p+'-appbrand','appbrand','','serein')+e(p+'-apptag','apptag','','AI FOCUS PLANNER')+e(p+'-today','today','','Wednesday, 16 Sep')))
def summary(p):return e(p+'-summary','summary','',e(p+'-sl','summary-label','','SEREIN / FOCUS RESERVED')+e(p+'-sn','summary-name','','Concept<br>presentation')+e(p+'-st','summary-time','','11:00 — 12:30')+e(p+'-sd','summary-duration','','90 minutes, just for this.')+e(p+'-sr','summary-rule','','')+e(p+'-ss','summary-status','','✓  Calendar updated'))
def write(name,d,b,j):
 (P/'compositions/frames'/f'{name}.html').write_text(f'''<template><div id="root" data-composition-id="{name}" data-start="0" data-duration="{d}" data-width="1920" data-height="1080"><div id="scene-{name}" class="clip" data-start="0" data-duration="{d}" data-track-index="0"><div class="stage">{b}</div></div></div><style>{CSS}</style><script>(()=>{{const tl=gsap.timeline({{paused:true}});{j}window.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;}})();</script></template>''')
def main():
 b=e('s1-ground','pos','left:0;top:0;width:800px;height:1080px;background:#183F36','')
 b+=e('s1-brand','pos brand','left:96px;top:66px;color:#F4F1E9','serein')
 b+=e('s1-heading','pos serif','left:96px;top:267px;width:648px;font-size:103px;color:#F4F1E9','<div>A full day.</div><div id="s1-line2" style="margin-top:20px">No room<br>to focus.</div>')
 b+=e('s1-room','pos serif','left:96px;top:300px;width:630px;font-size:129px;color:#F4F1E9','<div>Make</div><div>room.</div>')
 b+=e('s1-label','pos label','left:100px;top:798px;color:#F4F1E9','YOUR AI FOCUS PLANNER')
 b+=e('s1-paper','pos','left:0;top:0;width:1920px;height:1080px;background:#F4F1E9;transform-origin:0 0','')
 b+=app('s1')
 j="""
 gsap.set('#s1-room,#s1-paper,#s1-app',{opacity:0});
 tl.fromTo('#s1-heading',{y:25,opacity:0},{y:0,opacity:1,duration:.65,ease:'power3.out'},.05);
 tl.fromTo('#s1-line2',{y:20,opacity:0},{y:0,opacity:1,duration:.55,ease:'power3.out'},1.15);
 tl.fromTo('#s1-label',{y:20,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},2.45);
 tl.to('#s1-heading',{opacity:0,y:-30,duration:.35,ease:'power2.in'},3.45);
 tl.fromTo('#s1-room',{y:35,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},3.8);
 tl.to('#s1-brand,#s1-room,#s1-label',{opacity:0,duration:.25},5.15);
 tl.set('#s1-paper',{opacity:1},5.45);
 tl.fromTo('#s1-paper',{x:100,y:770,scaleX:590/1920,scaleY:90/1080},{x:0,y:0,scaleX:1,scaleY:1,duration:.55,ease:'power3.inOut'},5.45);
 tl.fromTo('#s1-app',{y:80,opacity:0},{y:0,opacity:1,duration:.7,ease:'power3.out'},6.55);
 tl.to({}, {duration:.01},7.99);
 """;write('01-full-day',8,b,j)
 b=e('s2-ground','pos','inset:0;background:#F4F1E9','')+app('s2')
 b+=e('s2-title','pos serif','left:100px;top:69px;font-size:62px','Give the important work a place.')
 content=e('s2-listlabel','pos label','left:146px;top:318px','YOUR PRIORITIES')+e('s2-cal-label','pos label','left:980px;top:318px','TODAY / YOUR CALENDAR')
 for i,(name,due,mins) in enumerate([('Concept presentation','Due tomorrow','90 min'),('Send revised estimate','Due Friday','30 min'),('Sort material samples','Due next week','45 min')]):
  content+=e(f's2-task{i}','task',f'top:{363+i*132}px;'+('border:2px solid #183F36;background:#D5E9EF' if i==0 else ''),e(f's2-tasktitle{i}','task-title','',name)+e(f's2-tasksub{i}','task-sub','',due)+e(f's2-tasktime{i}','task-time','',mins))
 content+=e('s2-find','button','left:145px;top:790px;width:685px','<span id="s2-findtext">Find focus time</span><span id="s2-finding" style="position:absolute;opacity:0">Checking your calendar…</span>')
 for i in range(7):
  content+=e(f's2-line{i}','calendar-line',f'top:{376+i*72}px','')+e(f's2-hour{i}','hour',f'top:{364+i*72}px',f'{9+i:02d}:00')
 content+=e('s2-meeting1','event','top:448px','10:00  Client call')+e('s2-meeting2','event','top:736px','14:00  Team review')
 content+=e('s2-found-note','pos','left:1012px;top:672px;width:700px;font-size:23px','A clear window before tomorrow’s deadline.')
 content+=e('s2-protect','button','left:1295px;top:805px;width:420px','<span id="s2-protecttext">Protect this time</span><span id="s2-scheduled" style="position:absolute;opacity:0">✓  Scheduled</span>')
 b+=e('s2-ui','pos','inset:0',content)
 # This plane is the same visual object that expands into the summary card.
 b+=e('s2-focus','pos','left:1065px;top:520px;width:650px;height:108px;background:#D5E9EF;border:2px solid #183F36;border-radius:6px;transform-origin:0 0','')
 b+=e('s2-focuscopy','pos','left:1088px;top:535px;width:600px', '<div style="font-size:27px;font-weight:550">Concept presentation</div><div style="font-size:21px;margin-top:14px">11:00–12:30 · 90 min <span id="s2-protected" style="float:right;opacity:0">✓ Protected</span></div>')
 b+=e('s2-cursor','cursor','','<div id="s2-pulse" class="pulse"></div><svg viewBox="0 0 24 24" width="46" height="46"><path d="M3 2.8 20.6 14 12.8 15.5 9 22 3 2.8Z" fill="#F4F1E9" stroke="#183F36" stroke-width="1.5"/></svg>')
 b+=summary('s2')
 j="""
 gsap.set('#s2-title,#s2-ui,#s2-focus,#s2-focuscopy,#s2-found-note,#s2-protect,#s2-summary,#s2-cursor',{opacity:0});
 tl.fromTo('#s2-title',{y:25,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},.15);
 tl.to('#s2-ui',{opacity:1,duration:.45},.3);
 tl.fromTo('#s2-task0,#s2-task1,#s2-task2',{y:20,opacity:0},{y:0,opacity:1,duration:.55,stagger:.3,ease:'power3.out'},.65);
 tl.fromTo('#s2-cursor',{x:1800,y:980,opacity:0},{x:461,y:813,opacity:1,duration:.85,ease:'power3.inOut'},4.5);
 tl.to('#s2-find',{scale:.978,duration:.1},5.4);tl.to('#s2-find',{scale:1,duration:.16},5.5);
 tl.fromTo('#s2-pulse',{opacity:.85,scale:.2},{opacity:0,scale:2,duration:.45,immediateRender:false},5.4);
 tl.to('#s2-findtext',{opacity:0,duration:.1},5.5);tl.to('#s2-finding',{opacity:1,duration:.15},5.6);
 tl.fromTo('#s2-focus',{scaleY:.02,opacity:0},{scaleY:1,opacity:1,duration:.7,ease:'power3.out'},6.15);
 tl.to('#s2-focuscopy',{opacity:1,duration:.35},6.5);
 tl.to('#s2-found-note',{opacity:1,duration:.4},7.0);
 tl.to('#s2-finding',{opacity:0,duration:.1},7.0);tl.to('#s2-findtext',{opacity:1,duration:.15},7.1);
 tl.to('#s2-protect',{opacity:1,duration:.4},8.1);
 tl.to('#s2-cursor',{x:1751,y:655,duration:.75,ease:'power3.inOut'},7.3);
 tl.to('#s2-cursor',{x:1460,y:825,duration:.7,ease:'power3.inOut'},11.45);
 tl.to('#s2-protect',{scale:.978,duration:.1},12.2);tl.to('#s2-protect',{scale:1,duration:.16},12.3);
 tl.fromTo('#s2-pulse',{opacity:.85,scale:.2},{opacity:0,scale:2,duration:.45,immediateRender:false},12.2);
 tl.to('#s2-protecttext',{opacity:0,duration:.1},12.3);tl.to('#s2-scheduled,#s2-protected',{opacity:1,duration:.15},12.4);
 tl.to('#s2-focus',{backgroundColor:'#183F36',duration:.3},12.35);tl.to('#s2-focuscopy',{color:'#F4F1E9',duration:.3},12.35);
 tl.to('#s2-cursor',{opacity:0,duration:.25},12.8);
 tl.to('#s2-title,#s2-ui,#s2-bar,#s2-focuscopy',{opacity:0,duration:.3},13.0);
 tl.to('#s2-app',{opacity:0,duration:.35},13.1);
 tl.to('#s2-focus',{x:-965,y:-250,scaleX:700/650,scaleY:550/108,borderRadius:7,duration:.85,ease:'power3.inOut'},13.35);
 tl.to('#s2-summary',{opacity:1,duration:.35},14.1);
 tl.to('#s2-focus',{opacity:0,duration:.2},14.45);
 tl.to({}, {duration:.01},15.99);
 """;write('02-find-space',16,b,j)
 b=e('s3-cover','pos','inset:0;background:#F4F1E9','')+summary('s3')
 b+=e('s3-heading','pos serif','left:100px;top:95px;width:715px;font-size:79px','Room to begin.')
 b+=e('s3-smallbrand','pos brand','left:100px;top:869px;font-size:57px','serein')
 b+=e('s3-ending','pos','inset:0;background:#F4F1E9','')
 b+=e('s3-finalbrand','pos serif','left:100px;top:278px;font-size:193px','serein')
 b+=e('s3-finallabel','pos label','left:111px;top:506px;font-size:23px','YOUR AI FOCUS PLANNER')
 b+=e('s3-finalcopy','pos serif','left:960px;top:307px;width:805px;font-size:100px','<div>Make room.</div><div>For what matters.</div>')
 b+=e('s3-rule','pos','left:100px;top:738px;width:1720px;height:2px;background:#183F36','')
 b+=e('s3-finalcta','pos','left:105px;top:791px;font-size:29px','Plan with intention. Begin with focus. ↗')
 b+=e('s3-disclosure','pos label','left:105px;top:997px;font-size:15px;letter-spacing:1.5px','FICTIONAL PRODUCT CONCEPT · ILLUSTRATIVE WORKFLOW')
 j="""
 gsap.set('#s3-heading,#s3-smallbrand,#s3-ending,#s3-finalbrand,#s3-finallabel,#s3-finalcopy,#s3-rule,#s3-finalcta,#s3-disclosure',{opacity:0});
 tl.fromTo('#s3-cover',{clipPath:'inset(0 0px 0 0)'},{clipPath:'inset(0 1040px 0 0)',duration:.85,ease:'power3.inOut'},.2);
 tl.fromTo('#s3-heading',{y:25,opacity:0},{y:0,opacity:1,duration:.55,ease:'power3.out'},.9);
 tl.fromTo('#s3-smallbrand',{y:20,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},2.5);
 tl.to('#s3-summary,#s3-heading,#s3-smallbrand',{opacity:0,duration:.3},4.7);
 tl.fromTo('#s3-ending',{x:-1920,opacity:1},{x:0,opacity:1,duration:.85,ease:'power3.inOut'},4.85);
 tl.fromTo('#s3-finalbrand,#s3-finallabel',{y:30,opacity:0},{y:0,opacity:1,duration:.65,stagger:.12,ease:'power3.out'},5.05);
 tl.fromTo('#s3-finalcopy',{y:30,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},5.45);
 tl.fromTo('#s3-rule',{scaleX:0,transformOrigin:'0 50%',opacity:0},{scaleX:1,opacity:1,duration:.6,ease:'power3.out'},5.9);
 tl.to('#s3-finalcta,#s3-disclosure',{opacity:1,duration:.4},6.15);
 tl.to({}, {duration:.01},7.99);
 """;write('03-room-to-begin',8,b,j)
 (P/'STORYBOARD.md').write_text((P/'STORYBOARD.md').read_text().replace('status: outline','status: animated'))
 subprocess.run(['node',str(Path.home()/'.agents/skills/product-launch-video/scripts/assemble-index.mjs'),'--storyboard',str(P/'STORYBOARD.md'),'--hyperframes',str(P),'--audio-meta',str(P/'audio_meta.json')],check=True)
 f=P/'index.html';s=f.read_text();s=re.sub(r'<script src="https://cdn[^>]+></script>','<script src="assets/gsap.min.js"></script>',s)
 s=s.replace('width: 1920px;\n        height: 1080px;','width: 100%;\n        height: 100%;')
 s=s.replace('class="scene"','class="scene clip"').replace('background: #000;','background: #F4F1E9;')
 s=s.replace('    </style>','      .scene { z-index: 2; }\n    </style>')
 media='''<video id="serein-focus" class="clip" src="assets/focus.mp4" data-start="0" data-duration="6" data-track-index="20" muted playsinline style="position:absolute;inset:auto;left:800px;top:0;width:1120px;height:1080px;object-fit:cover;z-index:1"></video>
<video id="serein-relief" class="clip" src="assets/relief.mp4" data-start="24" data-duration="6" data-track-index="21" muted playsinline style="position:absolute;inset:auto;left:880px;top:0;width:1040px;height:1080px;object-fit:cover;z-index:1"></video>'''
 s=s.replace('      <!-- BGM -->',media+'\n      <!-- BGM -->');f.write_text(s)
if __name__=='__main__':main()
