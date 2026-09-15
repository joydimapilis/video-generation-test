"""Original Tuck film: photographic receipt → exact expense UI → report and human callback."""
from pathlib import Path
import subprocess,re,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'videos/tuck';SK=Path.home()/'.agents/skills/product-launch-video/scripts'
CSS='''
@font-face{font-family:TuckDisplay;src:url('assets/SpaceGrotesk.ttf')}@font-face{font-family:TuckBody;src:url('assets/Inter.ttf')}
*{box-sizing:border-box}#root{position:relative;width:100%;height:100%;overflow:hidden;container-type:size;color:#171A18;font-family:TuckBody,sans-serif}.clip{position:absolute;inset:0}.stage{position:absolute;inset:0;overflow:hidden}.pos{position:absolute}.display{font-family:TuckDisplay,sans-serif;font-weight:600;letter-spacing:-3px;line-height:1.08}.label{font-family:TuckDisplay,sans-serif;font-size:23px;font-weight:600;letter-spacing:2px}.muted{color:#965B16}.app{position:absolute;left:120px;top:190px;width:1680px;height:770px}.skin{position:absolute;inset:0;background:#F5F0E8;border:1.5px solid rgba(150,91,22,.2);border-radius:14px;transform-origin:0 0}.bar{position:absolute;left:0;top:0;width:100%;height:90px;border-bottom:1.5px solid rgba(150,91,22,.2)}.word{position:absolute;left:44px;top:26px;font-size:40px;font-weight:700;letter-spacing:-2px;line-height:1}.button{position:absolute;display:flex;align-items:center;justify-content:center;height:72px;border-radius:100px;background:#965B16;color:#F5F0E8;font:600 27px TuckDisplay,sans-serif;letter-spacing:.5px}.report{position:absolute;left:530px;top:160px;width:860px;height:800px;background:#F5F0E8;border:1.5px solid rgba(150,91,22,.2);border-radius:14px;transform-origin:0 0}.report-top{position:absolute;left:40px;top:35px;font-size:29px;font-weight:700;letter-spacing:1px}.report-title{position:absolute;left:40px;top:113px;font-size:60px}.report-label{position:absolute;left:40px;top:193px;font-size:23px;letter-spacing:1px;color:#965B16}.report-row{position:absolute;left:40px;width:780px;height:83px;border-bottom:1px solid rgba(150,91,22,.2);font-size:35px}.report-row .date{position:absolute;left:402px;top:8px;font-size:24px;color:#965B16}.report-row .amount{position:absolute;right:0;top:0;font-family:TuckDisplay,sans-serif;font-size:35px}.report-total{position:absolute;left:40px;top:561px;width:780px}.report-total .value{position:absolute;right:0;top:0;font-size:78px;letter-spacing:-3px}.report-attachments{position:absolute;left:40px;top:695px;width:780px;padding-top:22px;border-top:1px solid rgba(150,91,22,.2);font-size:27px}.cursor{position:absolute;left:0;top:0;width:54px;height:54px;z-index:8}.pulse{position:absolute;left:-15px;top:-15px;width:40px;height:40px;border:3px solid #965B16;border-radius:50%;opacity:0}.row{position:absolute;left:870px;width:870px;height:95px;border-bottom:1px solid rgba(150,91,22,.2);font-size:31px}.row .merchant{position:absolute;left:18px;top:26px}.row .date{position:absolute;left:415px;top:31px;font-size:25px}.row .amount{position:absolute;right:20px;top:25px;font:600 35px TuckDisplay,sans-serif}.receipt{position:absolute;width:165px;height:240px;background:#F5F0E8;border:1px solid rgba(150,91,22,.2);border-radius:5px;padding:19px 14px;transform-origin:50% 50%}.receipt .shop{font:600 16px TuckDisplay,sans-serif;letter-spacing:.4px}.receipt .r-date{font-size:15px;margin-top:17px;color:#965B16}.receipt .r-amount{font:600 31px TuckDisplay,sans-serif;margin-top:25px}.receipt .line{height:2px;background:rgba(150,91,22,.2);margin-top:16px}.receipt .file{position:absolute;left:14px;bottom:17px;font-size:17px}
'''
def el(id,cl,style,body):return f'<div id="{id}" {"data-layout-allow-overflow" if id == "t1-paper" else ""} class="{cl}" style="{style}">{body}</div>'
def app(p):return el(p+'-app','app','',el(p+'-skin','skin','','')+el(p+'-bar','bar','',el(p+'-word','word display','','tuck')))
def report(p):
 b=el(p+'-rtop','report-top display','','tuck / EXPENSE REPORT')+el(p+'-rtitle','report-title display','','Client visit')+el(p+'-rlabel','report-label','','15 SEP 2026 · USD · EXAMPLE DATA')
 for i,(name,money) in enumerate([('Kindred Cafe','$6.40'),('City Cab','$24.00'),('North Hotel','$148.00')]):b+=el(f'{p}-rrow{i}','report-row',f'top:{277+i*87}px',name+'<span class="date">Sep 15</span><span class="amount">'+money+'</span>')
 b+=el(p+'-rtotal','report-total','', '<div class="label" style="padding-top:27px">TOTAL</div><div class="value display">$178.40</div>')+el(p+'-rfiles','report-attachments','','↳ 3 original receipts attached')
 return el(p+'-report','report','',b)
def write(name,d,body,js):
 f=P/'compositions/frames'/f'{name}.html';f.parent.mkdir(parents=True,exist_ok=True)
 f.write_text(f'''<template><div id="root" data-composition-id="{name}" data-start="0" data-duration="{d}" data-width="1920" data-height="1080"><section id="scene-{name}" class="clip" data-start="0" data-duration="{d}"><div class="stage">{body}</div></section></div><style>{CSS}</style><script>(()=>{{const tl=gsap.timeline({{paused:true}});{js}window.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;}})();</script></template>''')
def build():
 # Root-mounted opening photograph starts at x830. This is a graphic split, not a grade overlay.
 b=el('t1-ink','pos','left:0;top:0;width:830px;height:1080px;background:#171A18','')
 b+=el('t1-brand','pos display','left:100px;top:88px;color:#F5F0E8;font-size:54px;font-weight:700','tuck')
 b+=el('t1-count','pos label','left:100px;top:895px;color:#F5F0E8;font-size:22px','01 / THE LITTLE THINGS ADD UP')
 b+=el('t1-first','pos display','left:100px;top:320px;width:650px;color:#F5F0E8;font-size:108px','<div>One small</div><div>receipt.</div>')
 b+=el('t1-second','pos display','left:100px;top:320px;width:650px;color:#F5F0E8;font-size:102px','<div>One more</div><div>thing to do.</div>')
 b+=el('t1-paper','pos','left:0;top:0;width:1920px;height:1080px;background:#F5F0E8;transform-origin:0 0','')
 b+=el('t1-reveal','pos','left:120px;top:292px', '<div class="display" style="font-size:180px;font-weight:700">tuck</div><div class="label muted" style="margin-top:20px;font-size:29px">AI EXPENSE REPORTS</div>')
 b+=el('t1-value','pos display','left:965px;top:330px;font-size:89px;width:835px','<div>Receipts in.</div><div>Report ready.</div>')
 b+=app('t1')
 j="""
 gsap.set('#t1-second,#t1-paper,#t1-reveal,#t1-value,#t1-app',{opacity:0});
 tl.fromTo('#t1-first',{y:35,opacity:0},{y:0,opacity:1,duration:.55,ease:'power3.out'},.1);
 tl.to('#t1-first',{y:-35,opacity:0,duration:.25,ease:'power2.in'},1.8);
 tl.fromTo('#t1-second',{y:40,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},2.0);
 tl.to('#t1-second,#t1-count,#t1-brand',{opacity:0,duration:.25},4.05);
 // Registry modal-morph approach: opacity stays solid, aspect changes affect only blank paper.
 tl.set('#t1-paper',{opacity:1},4.35);
 tl.fromTo('#t1-paper',{x:1225,y:120,scaleX:.25,scaleY:.62,rotation:-24},{x:0,y:0,scaleX:1,scaleY:1,rotation:0,duration:1,ease:'power3.inOut'},4.35);
 tl.fromTo('#t1-reveal',{y:45,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},5.18);
 tl.fromTo('#t1-value',{y:45,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},5.35);
 tl.to('#t1-reveal,#t1-value',{opacity:0,y:-35,duration:.3},6.65);
 tl.fromTo('#t1-app',{y:55,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},6.98);
 tl.to({}, {duration:.01},7.99);
 """
 write('01-receipt',8,b,j)
 b=el('t2-ground','pos','inset:0;background:#F5F0E8','')+app('t2')
 b+=el('t2-heading','pos display','left:120px;top:77px;font-size:65px','From paper to prepared.')
 b+=el('t2-headertext','pos label','left:1380px;top:224px;font-size:23px','CLIENT VISIT / USD')
 ui=el('t2-intake','pos label muted','left:175px;top:326px','ADD RECEIPTS')+el('t2-divider','pos','left:815px;top:322px;width:1px;height:585px;background:rgba(150,91,22,.2)','')
 for i,(shop,money,file) in enumerate([('KINDRED CAFE','$6.40','cafe.jpg'),('CITY CAB','$24.00','cab.jpg'),('NORTH HOTEL','$148.00','hotel.jpg')]):
  card=f'<div class="shop">{shop}</div><div class="r-date">15 SEP 2026</div><div class="line"></div><div class="r-amount">{money}</div><div class="line"></div><div class="file">{file}</div>'
  ui+=el(f't2-receipt{i}','receipt',f'left:{185+i*200}px;top:404px',card)
 ui+=el('t2-selected','pos','left:190px;top:697px;font-size:28px;color:#965B16','3 images selected')
 ui+=el('t2-extract','button','left:400px;top:825px;width:330px','EXTRACT DETAILS')
 ui+=el('t2-reviewlabel','pos label muted','left:885px;top:326px','REVIEW DETAILS')
 ui+=el('t2-empty','pos display','left:885px;top:484px;width:790px;font-size:51px;font-weight:500;color:#965B16','No manual copying.')
 ui+=el('t2-columns','pos label','left:888px;top:398px;width:830px;font-size:19px', '<span>MERCHANT</span><span style="position:absolute;left:397px">DATE</span><span style="position:absolute;right:2px">AMOUNT</span>')
 for i,(name,money) in enumerate([('Kindred Cafe','$6.40'),('City Cab','$24.00'),('North Hotel','$148.00')]):ui+=el(f't2-row{i}','row',f'top:{444+i*97}px',f'<span class="merchant">{name}</span><span class="date">Sep 15</span><span class="amount">{money}</span>')
 ui+=el('t2-total','pos','left:890px;top:757px;width:835px', '<span style="font-size:23px;color:#965B16">TOTAL · 3 RECEIPTS</span><span class="display" style="position:absolute;right:0;top:-12px;font-size:49px">$178.40</span>')
 ui+=el('t2-create','button','left:1300px;top:825px;width:360px','<span id="t2-create-label">CREATE REPORT</span><span id="t2-building" style="position:absolute;opacity:0">PREPARING…</span>')
 ui+=el('t2-reviewhint','pos','left:880px;top:849px;font-size:23px;color:#965B16','Check it once.')
 b+=el('t2-ui','pos','inset:0',ui)+el('t2-cursor','cursor','','<div id="t2-pulse" class="pulse"></div><svg viewBox="0 0 24 24" width="54" height="54"><path d="M3 2.8 20.6 14 12.8 15.5 9 22 3 2.8Z" fill="#F5F0E8" stroke="#171A18" stroke-width="1.4"/></svg>')+report('t2')
 j="""
 gsap.set('#t2-heading,#t2-headertext,#t2-ui,#t2-cursor,#t2-columns,#t2-row0,#t2-row1,#t2-row2,#t2-total,#t2-create,#t2-reviewhint,#t2-report',{opacity:0});
 tl.fromTo('#t2-heading',{y:30,opacity:0},{y:0,opacity:1,duration:.45},.2);
 tl.to('#t2-headertext,#t2-ui',{opacity:1,duration:.3},.35);
 tl.fromTo('#t2-receipt0,#t2-receipt1,#t2-receipt2',{y:75,opacity:0},{y:0,opacity:1,duration:.65,stagger:.12,ease:'power3.out'},.5);
 tl.fromTo('#t2-cursor',{x:815,y:980,opacity:0},{x:542,y:850,opacity:1,duration:.65,ease:'power3.inOut'},1.5);
 tl.to('#t2-extract',{scale:.97,duration:.1},2.2);tl.to('#t2-extract',{scale:1,duration:.15},2.31);
 tl.fromTo('#t2-pulse',{scale:.2,opacity:.8},{scale:1.8,opacity:0,duration:.4,immediateRender:false},2.2);
 tl.to('#t2-empty',{opacity:0,duration:.2},2.4);
 tl.to('#t2-columns',{opacity:1,duration:.3},2.65);
 tl.fromTo('#t2-row0',{x:40,opacity:0},{x:0,opacity:1,duration:.45,ease:'power3.out'},2.9);
 tl.fromTo('#t2-row1',{x:40,opacity:0},{x:0,opacity:1,duration:.45,ease:'power3.out'},3.45);
 tl.fromTo('#t2-row2',{x:40,opacity:0},{x:0,opacity:1,duration:.45,ease:'power3.out'},4.0);
 tl.to('#t2-total,#t2-create,#t2-reviewhint',{opacity:1,duration:.4},4.6);
 tl.to('#t2-cursor',{x:1750,y:570,duration:.7,ease:'power3.inOut'},6.4);
 tl.to('#t2-cursor',{x:1458,y:851,duration:.65,ease:'power3.inOut'},8.5);
 tl.to('#t2-create',{scale:.97,duration:.1},9.2);tl.to('#t2-create',{scale:1,duration:.15},9.3);
 tl.fromTo('#t2-pulse',{scale:.2,opacity:.8},{scale:1.8,opacity:0,duration:.4,immediateRender:false},9.2);
 tl.to('#t2-create-label',{opacity:0,duration:.12},9.3);tl.to('#t2-building',{opacity:1,duration:.12},9.42);
 tl.to('#t2-cursor',{opacity:0,duration:.3},9.8);
 tl.to('#t2-ui,#t2-heading,#t2-headertext,#t2-bar',{opacity:0,duration:.25},10.25);
 tl.to('#t2-skin',{x:410,y:-30,scaleX:860/1680,scaleY:800/770,duration:.85,ease:'power3.inOut'},10.35);
 tl.to('#t2-report',{opacity:1,duration:.35},10.55);
 tl.to('#t2-app',{opacity:0,duration:.25},10.8);
 tl.to({}, {duration:.01},13.99);
 """
 write('02-report',14,b,j)
 b=el('t3-cover','pos','inset:0;background:#F5F0E8','')+report('t3')
 b+=el('t3-heading','pos display','left:120px;top:98px;font-size:79px;width:810px','Paperwork done.')
 b+=el('t3-brand','pos display','left:120px;top:899px;font-size:75px;font-weight:700','tuck')
 b+=el('t3-cta','pos','left:345px;top:924px;font-family:TuckDisplay;font-size:35px;font-weight:600;letter-spacing:-1px','Receipts to ready ↗')
 b+=el('t3-foot','pos label','left:120px;top:1020px;font-size:15px','FICTIONAL PRODUCT · EXAMPLE DATA')
 j="""
 gsap.set('#t3-heading,#t3-brand,#t3-cta,#t3-foot',{opacity:0});
 tl.to('#t3-report',{x:-410,y:90,scale:.72,duration:1,ease:'power3.inOut'},.4);
 tl.fromTo('#t3-cover',{clipPath:'inset(0 0px 0 0)'},{clipPath:'inset(0 870px 0 0)',duration:1,ease:'power3.inOut'},.4);
 tl.fromTo('#t3-heading',{y:40,opacity:0},{y:0,opacity:1,duration:.6,ease:'power3.out'},1.65);
 tl.fromTo('#t3-brand',{y:30,opacity:0},{y:0,opacity:1,duration:.55,ease:'power3.out'},3.95);
 tl.fromTo('#t3-cta',{x:-30,opacity:0},{x:0,opacity:1,duration:.55,ease:'power3.out'},4.3);
 tl.to('#t3-foot',{opacity:1,duration:.3},4.5);
 tl.to({}, {duration:.01},7.99);
 """
 write('03-ready',8,b,j)
 # Orchestrator-owned root assembly and media. No video is nested in another timed element.
 s=(P/'STORYBOARD.md').read_text().replace('status: outline','status: animated').replace('scale.86','scale.72').replace('x120 y245','x120 y250');(P/'STORYBOARD.md').write_text(s)
 subprocess.run(['node',str(SK/'assemble-index.mjs'),'--storyboard',str(P/'STORYBOARD.md'),'--hyperframes',str(P),'--audio-meta',str(P/'audio_meta.json')],check=True)
 f=P/'index.html';s=f.read_text();s=re.sub(r'<script src="https://cdn[^>]+></script>','<script src="assets/gsap.min.js"></script>',s)
 s=s.replace('class="scene"','class="scene clip"').replace('background: #000;','background: #171A18;')
 s=s.replace('    </style>','      .scene { z-index: 2; }\n    </style>')
 media='''
      <video id="tuck-opening" class="clip" src="assets/opening.mp4" data-start="0" data-duration="5.5" data-track-index="20" muted playsinline style="position:absolute;inset:auto;left:830px;top:0;width:1090px;height:1080px;object-fit:cover;z-index:1"></video>
      <video id="tuck-return" class="clip" src="assets/return.mp4" data-start="22" data-duration="8" data-track-index="21" muted playsinline style="position:absolute;inset:auto;left:1050px;top:0;width:870px;height:1080px;object-fit:cover;z-index:1"></video>
'''
 s=s.replace('      <!-- BGM -->',media+'\n      <!-- BGM -->');f.write_text(s)
 sources=[{'path':'assets/receipt-source.mp4','source':'artifacts/library-loop-12/outputs/tuck_receipt_h3max_v2.mp4','sha256':hashlib.sha256((P/'assets/receipt-source.mp4').read_bytes()).hexdigest()},{'path':'assets/opening.mp4','source':'assets/receipt-source.mp4','source_start':.5,'duration':5.5,'transform':'fps24; scale height1080; crop1090x1080 at x550 y0','display_start':0},{'path':'assets/return.mp4','source':'assets/receipt-source.mp4','source_start':6,'source_duration':4,'duration':8,'transform':'fps24; scale height1080; crop870x1080 at x700 y0; clone final frame for4s','display_start':22}]
 (P/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
if __name__=='__main__':build()
