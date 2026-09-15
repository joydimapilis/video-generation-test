"""Build three original seekable Fold launch scenes with shared seam geometry."""
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'videos/fold'
CSS='''
@font-face{font-family:FoldDisplay;src:url('assets/BebasNeue.ttf')}@font-face{font-family:FoldSans;src:url('assets/Inter.ttf')}
*{box-sizing:border-box} #root{position:relative;width:100%;height:100%;overflow:hidden;container-type:size;color:#1A1A1A;font-family:FoldSans,sans-serif}
.clip{position:absolute;inset:0}.stage{position:absolute;inset:0;background:#E85D5D;overflow:hidden}.pos{position:absolute}.display{font-family:FoldDisplay,sans-serif;line-height:.95;letter-spacing:2px;font-weight:400}.label{font-size:24px;letter-spacing:2px;font-weight:650}.note{position:absolute;background:#F5F0E8;border-top:6px solid #1A1A1A;padding:25px 30px;font-size:31px;line-height:1.25}.note small{display:block;font-size:17px;letter-spacing:2px;margin-bottom:16px}.window{position:absolute;left:180px;top:210px;width:1560px;height:720px}.skin{position:absolute;inset:0;background:#F5F0E8;transform-origin:0 0}.bar{position:absolute;left:0;top:0;width:100%;height:78px;background:#1A1A1A;color:#F5F0E8}.foldword{position:absolute;left:40px;top:17px;font-size:48px}.brief{position:absolute;left:560px;top:190px;width:800px;height:700px;background:#F5F0E8}.brief .title{position:absolute;left:40px;top:25px;font-size:24px;letter-spacing:1px}.brief .mainline{position:absolute;left:40px;top:160px;font-size:62px;width:720px}.brief .meta{position:absolute;left:40px;top:310px;width:700px;font-size:29px;line-height:1.6}.brief .foot{position:absolute;left:40px;bottom:38px;font-size:21px;letter-spacing:2px}.button{position:absolute;height:70px;display:flex;align-items:center;justify-content:center;font-size:27px;font-weight:650;letter-spacing:1px;background:#1A1A1A;color:#F5F0E8}.cursor{position:absolute;left:0;top:0;width:56px;height:56px;z-index:8}.pulse{position:absolute;left:-15px;top:-15px;width:40px;height:40px;border:3px solid #1A1A1A;border-radius:50%;opacity:0}.panel{position:absolute;width:500px;height:400px;background:#F5F0E8;border-top:6px solid #1A1A1A;padding:30px}.panel .category{font-size:22px;letter-spacing:2px}.panel .body{font-size:36px;line-height:1.25;margin-top:35px}.panel .sub{font-size:23px;line-height:1.5;margin-top:24px;color:#6B6B6B}
'''
def el(id,classes,style,body):return f'<div id="{id}" {"data-layout-allow-overflow" if id in ["f1-cream","f1-coral","f1-note1","f2-ui"] else ""} class="{classes}" style="{style}">{body}</div>'
def window(prefix):return el(prefix+'-window','window','',el(prefix+'-skin','skin','','')+el(prefix+'-bar','bar','',el(prefix+'-word','foldword display','','FOLD')))
def brief(prefix):return el(prefix+'-brief','brief','',el(prefix+'-briefbar','bar','',el(prefix+'-brieftitle','title','','FIELD / CREATIVE BRIEF'))+el(prefix+'-mainline','mainline display','','YOUR EVERYDAY REFILL.')+el(prefix+'-meta','meta','','<div>Everyday commuters.</div><div>Launch page · Social posts · Email</div>')+el(prefix+'-foot','foot','','ONE IDEA. A CLEAR DIRECTION.'))
def write(name,duration,body,js):
 path=P/'compositions/frames'/f'{name}.html';path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'''<template><div id="root" data-composition-id="{name}" data-start="0" data-duration="{duration}" data-width="1920" data-height="1080"><section id="scene-{name}" class="clip" data-start="0" data-duration="{duration}"><div class="stage">{body}</div></section></div><style>{CSS}</style><script>
(()=>{{const tl=gsap.timeline({{paused:true}});{js}\nwindow.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;}})();
</script></template>''')

def build():
 b=el('f1-cream','pos','inset:0;background:#F5F0E8','')+el('f1-coral','pos','left:1180px;top:0;width:740px;height:1080px;background:#E85D5D','')
 b+=el('f1-kicker','pos label','left:120px;top:110px','A CAMPAIGN STARTS SOMEWHERE.')
 b+=el('f1-good','pos display','left:112px;top:300px;font-size:250px','GOOD IDEA.')
 b+=el('f1-every','pos display','left:112px;top:300px;font-size:225px','EVERYWHERE.')
 notes=[(120,640,520,180,'01 / THE PRODUCT','Refillable bottle.'),(1240,130,535,200,'02 / THE AUDIENCE','For everyday commuters.'),(1170,725,610,205,'03 / THE FEEL','Make it feel less preachy.'),(220,85,510,145,'VOICE NOTE','A useful everyday habit.'),(700,780,420,175,'IN YOUR HEAD','Keep it simple.'),(785,70,365,170,'CAMPAIGN','FIELD / LAUNCH')]
 for i,(x,y,w,h,tag,line) in enumerate(notes):b+=el(f'f1-note{i}','note',f'left:{x}px;top:{y}px;width:{w}px;height:{h}px',f'<small>{tag}</small>{line}')
 b+=el('f1-reveal','pos','left:120px;top:235px;width:920px',el('f1-brand','display','font-size:230px','FOLD')+el('f1-purpose','label','margin-top:28px;font-size:30px','AI CREATIVE BRIEFS')+el('f1-tag','', 'font-size:39px;margin-top:36px','From scattered to started.'))
 b+=window('f1')
 j="""
 gsap.set('#f1-every,#f1-reveal,#f1-window',{opacity:0},0);
 tl.fromTo('#f1-good',{y:-60},{y:0,duration:.7,ease:'power3.out'},0);
 tl.fromTo('#f1-note0',{y:450,rotation:-10},{y:0,rotation:-3,duration:.65,ease:'power3.out'},.22);
 tl.to('#f1-good',{y:-70,opacity:0,duration:.2},1.22);
 tl.fromTo('#f1-every',{y:100,opacity:0},{y:0,opacity:1,duration:.45,ease:'power3.out'},1.35);
 tl.to('#f1-kicker',{opacity:0,duration:.18},1.25);
 """
 for i in range(1,6):j+=f"tl.fromTo('#f1-note{i}',{{y:{-500 if i%2 else 500},rotation:{(-1)**i*22},opacity:0}},{{y:0,rotation:{[0,4,-3,-4,5,3][i]},opacity:1,duration:.6,ease:'power3.out'}},{1.4+i*.15});\n"
 j+="tl.to('#f1-every',{x:-150,opacity:0,duration:.4,ease:'power3.in'},3.5);tl.to('#f1-cream',{x:-1920,duration:1,ease:'power3.inOut'},3.65);tl.to('#f1-coral',{x:740,duration:.8},3.65);"
 for i,(x,y,w,h,_,_) in enumerate(notes):j+=f"tl.to('#f1-note{i}',{{x:{1190-x+i*10},y:{400-y+i*10},rotation:0,opacity:{1 if i==0 else 0},duration:.85,ease:'power3.inOut'}},{3.55+i*.045});\n"
 j+="""
 tl.fromTo('#f1-reveal',{y:65,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},4.15);
 // Adapted registry modal-morph: measured paper bounds; text never stretches.
 tl.to('#f1-reveal',{x:-140,opacity:0,duration:.45,ease:'power3.in'},6.45);
 tl.to('#f1-note0',{opacity:0,duration:.18},6.57);
 tl.set('#f1-window',{opacity:1},6.55);
 tl.fromTo('#f1-window',{x:1010,y:190,scaleX:520/1560,scaleY:180/720,transformOrigin:'0 0'},
  {x:0,y:0,scaleX:1,scaleY:1,duration:1.05,ease:'power3.inOut'},6.55);
 tl.fromTo('#f1-bar',{opacity:0},{opacity:1,duration:.25},7.62);
 tl.to({}, {duration:.01},8.99);
 """
 write('01-everywhere',9,b,j)
 # Product: two deliberate controls, clearly observed results.
 b=window('f2')
 b+=el('f2-heading','pos display','left:180px;top:87px;font-size:73px','GIVE IT A DIRECTION.')
 b+=el('f2-campaign','pos label','left:1320px;top:238px;color:#F5F0E8;font-size:21px','FIELD / CAMPAIGN')
 ui=el('f2-leftlabel','pos label','left:240px;top:340px','YOUR NOTES')+el('f2-divider','pos','left:820px;top:330px;width:2px;height:530px;background:#E8E0D4','')
 for i,line in enumerate(['Refillable bottle.','For everyday commuters.','Make it feel less preachy.']):ui+=el(f'f2-note{i}','note',f'left:240px;top:{395+i*115}px;width:530px;height:94px;border-top:0;border-left:4px solid #E85D5D;font-size:28px;padding:27px 22px;background:#E8E0D4',line)
 ui+=el('f2-organize','button','left:440px;top:800px;width:280px','ORGANIZE ↗')
 ui+=el('f2-rightlabel','pos label','left:880px;top:340px','CREATIVE BRIEF')
 ui+=el('f2-placeholder','pos','left:880px;top:435px;width:760px;font-size:35px;line-height:1.5;color:#6B6B6B','Your idea, with a little direction.')
 ui+=el('f2-audience','pos','left:880px;top:413px;width:760px', '<div class="label" style="font-size:19px;color:#6B6B6B">AUDIENCE</div><div style="font-size:31px;margin-top:12px">Everyday commuters</div>')
 ui+=el('f2-message','pos','left:880px;top:523px;width:760px','<div class="label" style="font-size:19px;color:#6B6B6B">CORE MESSAGE</div>'+el('f2-formalcopy','display','font-size:56px;margin-top:14px','REFILL. REUSE. KEEP MOVING.')+el('f2-humancopy','pos display','left:0;top:38px;font-size:56px;width:760px','YOUR EVERYDAY REFILL.'))
 ui+=el('f2-make','pos','left:880px;top:656px;width:760px','<div class="label" style="font-size:19px;color:#6B6B6B">DELIVERABLES</div><div style="font-size:27px;margin-top:12px">Launch page · Social posts · Email</div>')
 ui+=el('f2-tone','pos label','left:880px;top:825px;font-size:21px','TONE')+el('f2-formal','button','left:1000px;top:800px;width:245px;background:#E8E0D4;color:#1A1A1A','FORMAL')+el('f2-human','button','left:1280px;top:800px;width:250px;background:#F5F0E8;color:#1A1A1A;border:2px solid #1A1A1A','HUMAN')
 b+=el('f2-ui','pos','inset:0',ui)
 # Simulated-cursor registry pointer + pulse, adapted without decorative shadow.
 b+=el('f2-cursor','cursor','', '<div id="f2-pulse" class="pulse"></div><svg viewBox="0 0 24 24" width="56" height="56"><path d="M3 2.8 20.6 14 12.8 15.5 9 22 3 2.8Z" fill="#F5F0E8" stroke="#1A1A1A" stroke-width="1.4"/></svg>')
 b+=brief('f2')
 j="""
 gsap.set('#f2-ui,#f2-heading,#f2-campaign,#f2-cursor,#f2-brief,#f2-audience,#f2-message,#f2-make,#f2-humancopy',{opacity:0},0);
 tl.fromTo('#f2-heading',{y:30,opacity:0},{y:0,opacity:1,duration:.5},.15);
 tl.to('#f2-campaign,#f2-ui',{opacity:1,duration:.35},.3);
 tl.fromTo('#f2-note0,#f2-note1,#f2-note2',{x:-50},{x:0,stagger:.1,duration:.45,ease:'power3.out'},.4);
 tl.fromTo('#f2-cursor',{x:760,y:975,opacity:0},{x:565,y:825,opacity:1,duration:.6,ease:'power3.inOut'},1.0);
 tl.to('#f2-organize',{backgroundColor:'#E85D5D',color:'#1A1A1A',duration:.12},1.7);
 tl.fromTo('#f2-pulse',{scale:.2,opacity:.8},{scale:1.8,opacity:0,duration:.4,immediateRender:false},1.7);
 tl.to('#f2-placeholder',{opacity:0,duration:.15},2.1);
 tl.fromTo('#f2-audience',{y:25,opacity:0},{y:0,opacity:1,duration:.4},2.35);
 tl.fromTo('#f2-message',{y:25,opacity:0},{y:0,opacity:1,duration:.4},3.45);
 tl.fromTo('#f2-make',{y:25,opacity:0},{y:0,opacity:1,duration:.4},4.35);
 tl.to('#f2-cursor',{x:1390,y:825,duration:.85,ease:'power3.inOut'},6.5);
 tl.fromTo('#f2-pulse',{scale:.2,opacity:.8},{scale:1.8,opacity:0,duration:.4,immediateRender:false},7.4);
 tl.to('#f2-human',{backgroundColor:'#E85D5D',duration:.15},7.4);
 tl.to('#f2-formal',{backgroundColor:'#F5F0E8',color:'#6B6B6B',duration:.15},7.4);
 tl.to('#f2-formalcopy',{opacity:0,duration:.18},7.5);
 tl.fromTo('#f2-humancopy',{y:25,opacity:0},{y:0,opacity:1,duration:.45,ease:'power3.out'},7.72);
 tl.to('#f2-cursor',{x:1760,y:1000,opacity:0,duration:.4},9.2);
 tl.to('#f2-ui,#f2-heading,#f2-campaign',{opacity:0,y:-25,duration:.35},9.85);
 tl.to('#f2-bar',{opacity:0,duration:.2},10.0);
 tl.to('#f2-skin',{x:380,y:-20,scaleX:800/1560,scaleY:700/720,duration:.85,ease:'power3.inOut'},10.15);
 tl.to('#f2-brief',{opacity:1,duration:.25},11.0);
 tl.to('#f2-window',{opacity:0,duration:.15},11.15);
 tl.to({}, {duration:.01},11.99);
 """
 write('02-direction',12,b,j)
 b=brief('f3')
 panels=[('AUDIENCE','Everyday commuters.','A useful everyday habit.'),('MESSAGE','Your everyday refill.','Refillable bottle. Less preachy.'),('MAKE','One campaign.','Launch page · Social posts · Email')]
 board=''
 for i,(title,body,sub) in enumerate(panels):board+=el(f'f3-panel{i}','panel',f'left:{180+i*530}px;top:290px',f'<div class="category">0{i+1} / {title}</div><div class="body">{body}</div><div class="sub">{sub}</div>')
 b+=el('f3-board','pos','left:0;top:0;width:1920px;height:700px',board)
 b+=el('f3-boardtitle','pos label','left:180px;top:180px;font-size:30px','FIELD / THE CREATIVE DIRECTION')
 b+=el('f3-less','pos display','left:174px;top:100px;font-size:148px','LESS SCATTERED.')+el('f3-more','pos display','left:174px;top:242px;font-size:148px','MORE STARTED.')
 b+=el('f3-cta','pos','left:180px;top:840px;width:1560px;height:124px;background:#1A1A1A;color:#F5F0E8',el('f3-fold','pos display','left:35px;top:29px;font-size:74px','FOLD')+el('f3-call','pos','right:36px;top:43px;font-size:31px;letter-spacing:2px','SHAPE YOUR NEXT IDEA ↗'))
 b+=el('f3-disclosure','pos label','left:180px;top:995px;font-size:17px','FICTIONAL PRODUCT CONCEPT')
 j="""
 gsap.set('#f3-board,#f3-boardtitle,#f3-less,#f3-more,#f3-cta,#f3-disclosure',{opacity:0},0);
 tl.to('#f3-briefbar,#f3-mainline,#f3-meta,#f3-foot',{opacity:0,duration:.16},.28);
 tl.to('#f3-brief',{scaleX:1.95,scaleY:.57,transformOrigin:'50% 50%',opacity:0,duration:.65,ease:'power3.inOut'},.45);
 tl.to('#f3-board',{opacity:1,duration:.25},.8);
 tl.fromTo('#f3-panel0',{x:530,rotationY:75,transformOrigin:'100% 50%'},{x:0,rotationY:0,duration:.9,ease:'power3.out'},.65);
 tl.fromTo('#f3-panel2',{x:-530,rotationY:-75,transformOrigin:'0% 50%'},{x:0,rotationY:0,duration:.9,ease:'power3.out'},.65);
 tl.fromTo('#f3-boardtitle',{y:25,opacity:0},{y:0,opacity:1,duration:.45},1.25);
 tl.to('#f3-boardtitle',{opacity:0,y:-30,duration:.3},3.2);
 tl.to('#f3-board',{y:165,duration:.8,ease:'power3.inOut'},3.4);
 tl.to('#f3-panel0,#f3-panel1,#f3-panel2',{height:320,duration:.8,ease:'power3.inOut'},3.4);
 tl.fromTo('#f3-less',{y:-85,opacity:0},{y:0,opacity:1,duration:.65,ease:'power3.out'},3.7);
 tl.fromTo('#f3-more',{y:60,opacity:0},{y:0,opacity:1,duration:.65,ease:'power3.out'},4.1);
 tl.fromTo('#f3-cta',{scaleX:.05,opacity:0,transformOrigin:'0 50%'},{scaleX:1,opacity:1,duration:.65,ease:'power3.inOut'},5.5);
 tl.fromTo('#f3-fold,#f3-call',{opacity:0},{opacity:1,duration:.25},6.1);
 tl.to('#f3-disclosure',{opacity:1,duration:.25},6.3);
 tl.to({}, {duration:.01},9.99);
 """
 write('03-started',10,b,j)
 # Canonical production timing and status.
 s=(P/'STORYBOARD.md').read_text().replace('duration: 30s','duration: 31s').replace('status: outline','status: animated').replace('6.5–8s','6.5–9s').replace('presses at 2.0s','presses at 1.7s').replace('Click 7.2s','Click 7.4s')
 s=s.replace('Simple authored Field bottle outline occupies the message panel; clearly a creative brief, not an auto-generated campaign claim.','The original bottle idea remains as text in the message panel; the result is explicitly a creative brief.')
 (P/'STORYBOARD.md').write_text(s);q=P/'BRIEF.md';q.write_text(q.read_text().replace('30s','31s'))
if __name__=='__main__':build()
