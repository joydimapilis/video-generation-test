"""Fresh Portion film: exact fictional order UI, continuous before/after card handoff.
No previous composition, human media or audio is used as a base.
"""
from pathlib import Path
import json, shutil

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'videos/portion'
ASSETS=PROJECT/'assets'
ORDERS=[{'name':'Studio North','source':'EMAIL','chicken':5,'tofu':3,'note':''},
        {'name':'Book Club','source':'MESSAGE','chicken':2,'tofu':4,'note':'Sauce on the side'},
        {'name':'Workshop','source':'ORDER FORM','chicken':6,'tofu':4,'note':''}]
assert sum(o['chicken'] for o in ORDERS)==13
assert sum(o['tofu'] for o in ORDERS)==11
for name in ['SourceSerif4-Regular.ttf','Inter-Regular.ttf']:
    shutil.copyfile(ROOT/'videos/serein/assets/fonts'/name,ASSETS/'fonts'/name)
shutil.copyfile(ROOT/'videos/sideway/assets/gsap.min.js',ASSETS/'gsap.min.js')
(PROJECT/'orders.json').write_text(json.dumps(ORDERS,indent=2))
cards=''
for i,o in enumerate(ORDERS):
    cards+=f'''<article id="order-{i}" class="order"><div class="order-top"><span class="source-tag">{o['source']}</span><span class="order-name">{o['name']}</span><span class="qty">{o['chicken']+o['tofu']} bowls</span></div><div class="order-items"><span>{o['chicken']} chicken</span><span>{o['tofu']} tofu</span></div><div class="order-note">{o['note'] or 'Lunch delivery'}</div></article>'''
html='''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:PortionSerif;src:url('assets/fonts/SourceSerif4-Regular.ttf');ascent-override:90%;descent-override:15%;line-gap-override:0%}@font-face{font-family:PortionSans;src:url('assets/fonts/Inter-Regular.ttf')}
*{box-sizing:border-box;margin:0}html,body{width:100%;height:100%;overflow:hidden;background:#F4F0E5}body{font-family:PortionSans,sans-serif;color:#193D30}#root{position:relative;width:100%;height:100%;overflow:hidden;background:#F4F0E5}.clip{position:absolute;inset:0;width:100%;height:100%}.plate{object-fit:cover;z-index:0}.serif{font-family:PortionSerif,serif;font-weight:400;letter-spacing:-.045em}.eyebrow{font-size:23px;letter-spacing:.14em}.wordmark{font-size:51px;letter-spacing:-.065em;font-weight:600}.mark{display:inline-flex;align-items:center;justify-content:center;width:52px;height:52px;border:2px solid currentColor;border-radius:50%;margin-right:17px;font-size:34px;letter-spacing:-.13em;vertical-align:middle}.human-copy{position:absolute;inset:0;width:630px;background:#F4F0E5;padding:87px 72px}.human-copy .eyebrow{position:absolute;top:97px}.human-copy .hook{position:absolute;top:245px;left:72px;font-size:95px;line-height:1.16;width:550px}.human-copy .hook p{margin:0}.human-copy .sub{position:absolute;top:649px;left:77px;font-size:31px;line-height:1.5;width:445px}.folio{position:absolute;bottom:73px;left:77px;font-size:21px;letter-spacing:.03em}.small-line{width:70px;height:3px;background:#AA533A;margin-bottom:23px}#opening{z-index:1}#opening-copy .before-word{color:#AA533A}
#workflow{z-index:3}#workflow-inner{position:absolute;inset:0;background:#F4F0E5}.before-heading{position:absolute;left:90px;top:76px}.before-heading h2{font-size:78px;line-height:1.15;margin-top:25px}.before-heading .eyebrow{color:#AA533A}.order{position:absolute;width:610px;height:164px;padding:24px 28px;background:#FFFCF5;border:2px solid #C5C7B6;border-radius:10px;box-shadow:0 12px 25px #193D3010;z-index:4}.order-top{display:flex;align-items:center;gap:14px}.source-tag{font-size:13px;letter-spacing:.055em;background:#EADAD2;color:#673A2B;padding:7px 8px;border-radius:4px}.order-name{font-size:27px;letter-spacing:-.025em}.qty{font-size:22px;margin-left:auto;white-space:nowrap}.order-items{display:flex;gap:27px;font-size:25px;margin-top:15px}.order-note{font-size:20px;margin-top:10px;color:#665F4F}#order-0{left:138px;top:322px}#order-1{left:210px;top:526px}#order-2{left:92px;top:730px}
#manual{position:absolute;left:927px;top:314px;width:875px;height:626px;background:#FFFDF8;border:2px solid #A9B7AD;border-radius:12px;overflow:hidden}.sheet-bar{height:77px;background:#E3E7DE;padding:23px 30px;font-size:23px}.sheet-caption{padding:24px 31px;font-size:22px;color:#665F4F}.sheet-table{margin:4px 30px;display:grid;grid-template-columns:2.1fr 1fr 1fr}.cell{height:89px;border-right:1px solid #CCD2C9;border-bottom:1px solid #CCD2C9;display:flex;align-items:center;padding:20px;font-size:25px}.cell.head{height:70px;font-size:20px;background:#F1F2EB}.cell.active{box-shadow:inset 0 0 0 3px #AA533A}.sheet-footer{position:absolute;left:31px;bottom:30px;font-size:21px;color:#7E4734}#copy-toast{position:absolute;left:520px;top:470px;background:#193D30;color:#FFFDF8;font-size:21px;padding:12px 21px;border-radius:8px;z-index:8}
#app-chrome{position:absolute;inset:0;z-index:1}#app-logo{position:absolute;left:89px;top:61px}#app-description{position:absolute;left:394px;top:86px;font-size:26px;color:#475F4F}#app-headline{position:absolute;left:90px;top:160px;font-size:76px;line-height:1.15}#app-frame{position:absolute;left:88px;top:290px;width:1744px;height:699px;border:2px solid #BBC8B6;border-radius:16px;background:#FAF9F2}#inbox-label{position:absolute;left:120px;top:329px;font-size:23px}#inbox-label span{margin-left:12px;padding:5px 12px;background:#D4E2AC;border-radius:30px;font-size:18px}#app-divider{position:absolute;left:767px;top:323px;height:634px;width:1px;background:#D7DCCD}#kitchen-title{position:absolute;left:819px;top:329px;font-size:33px}#date-label{position:absolute;right:137px;top:336px;font-size:23px;color:#62715F}
#empty-state{position:absolute;left:845px;top:478px;width:891px;text-align:center}#empty-state h3{font-size:44px;font-weight:400;letter-spacing:-.035em}#empty-state p{font-size:27px;color:#5B6D5B;line-height:1.6;margin-top:20px}#build-btn{position:absolute;left:1054px;top:704px;width:521px;height:90px;border-radius:12px;background:#193D30;color:#F4F0E5;display:flex;justify-content:center;align-items:center;font-size:31px;box-shadow:0 7px 0 #CDD5BD}#build-btn b{font-weight:400;margin-left:25px;font-size:37px}#progress{position:absolute;left:944px;top:526px;width:692px;text-align:center;font-size:33px}#progress-track{height:5px;background:#DCE5CC;margin-top:30px;overflow:hidden}#progress-fill{height:100%;width:100%;background:#193D30;transform-origin:left}
#result{position:absolute;left:816px;top:408px;width:972px;height:530px}#total-block{display:flex;align-items:baseline;gap:22px}#total-number{font-size:117px;line-height:1;letter-spacing:-.07em}#total-label{font-size:36px;letter-spacing:-.03em}#checked{margin-left:auto;color:#446238;font-size:22px;display:flex;align-items:center;gap:12px}.check-circle{width:30px;height:30px;border-radius:50%;background:#D4E2AC;display:inline-flex;align-items:center;justify-content:center}.split{display:flex;gap:19px;margin-top:28px}.prep-item{width:50%;height:143px;padding:22px 29px;border-radius:12px;background:#E8EDD9}.prep-item .name{font-size:28px}.prep-item .number{float:right;font-size:63px;line-height:1;letter-spacing:-.055em}.breakdown{font-size:18px;margin-top:23px;color:#4B5D43}.packing-note{position:relative;margin-top:23px;width:100%;height:99px;border:1px solid #B6C49F;background:#F0F2E6;border-radius:10px;padding:17px 25px}.packing-note .label{font-size:17px;letter-spacing:.06em}.packing-note .content{font-size:28px;margin-top:7px}.packing-note .attribution{position:absolute;right:24px;top:40px;font-size:22px;color:#55694D}#send-btn{position:absolute;right:0;bottom:0;width:344px;height: seventy; height: seventy; height:76px;border-radius:10px;background:#193D30;color:#F4F0E5;display:flex;align-items:center;justify-content:center;font-size:27px}#result-footnote{position:absolute;bottom:24px;left:4px;font-size:22px;color:#557048}
#cursor{position:absolute;left:0;top:0;width:50px;height:50px;z-index:12;pointer-events:none}#cursor svg{width:50px;height:50px}#cursor-pulse{position:absolute;left:-10px;top:-10px;width:38px;height:38px;border:3px solid #AA533A;border-radius:50%;opacity:0}
#after-copy{z-index:2}#after-copy .hook{top:261px}#after-copy .sub{top:610px}#ready{z-index:7;pointer-events:none}#ready-badge{position:absolute;left:1175px;top:820px;width:584px;height:130px;border-radius:14px;background:#D4E2AC;color:#193D30;padding:25px 29px;display:flex;gap:22px;align-items:center;box-shadow:0 8px 22px #193D3010}#ready-icon{font-size:43px;width:57px;height:57px;display:flex;align-items:center;justify-content:center;border:2px solid #668557;border-radius:50%}#ready-title{font-size:30px;letter-spacing:-.035em}#ready-sub{font-size:22px;margin-top:8px}
#ending{z-index:10}#ending-inner{position:absolute;inset:0;background:#193D30;color:#F4F0E5}#end-logo{position:absolute;left:95px;top:80px}#end-head{position:absolute;left:91px;top:318px;font-size:142px;line-height:1.16}#end-head .accent{color:#D4E2AC}#end-cta{position:absolute;left:102px;top:777px;font-size:31px}#end-line{position:absolute;left:102px;top:744px;width:73px;height:2px;background:#D4E2AC}#end-sheet{position:absolute;left:1322px;top:281px;width:474px;height:533px;padding:37px;background:#F4F0E5;color:#193D30;border-radius:5px;box-shadow:16px 17px 0 #D4E2AC}.end-sheet-label{font-size:19px;letter-spacing:.12em}.end-sheet-number{font-size:132px;margin-top:31px;line-height:1.15}.end-sheet-bowls{font-size:28px;margin-top:11px}.end-sheet-rule{height:1px;background:#AEB9A1;margin-top:33px;margin-bottom:27px}.end-sheet-row{font-size:24px;margin:16px 0;display:flex;justify-content:space-between}#end-footer{position:absolute;right:107px;bottom:76px;font-size:21px;color:#D4E2AC}
</style></head><body><div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="36">
<video id="before-video" class="clip plate" src="assets/before.mp4" data-start="0" data-duration="5.3" data-media-start="0.3" muted playsinline></video>
<section id="opening" class="clip" data-start="0" data-duration="5.3"><div id="opening-copy" class="human-copy"><div class="eyebrow before-word">BEFORE / LUNCH PREP</div><div class="hook serif"><p>24 lunches.</p><p>Still copying</p><p>orders.</p></div><div class="sub"><div class="small-line"></div>The kitchen is waiting.</div><div class="folio">THREE ORDERS. THREE PLACES.</div></div></section>
<video id="after-video" class="clip plate" src="assets/after.mp4" data-start="25.6" data-duration="6" data-media-start="0" muted playsinline></video>
<section id="after-copy" class="clip" data-start="25.6" data-duration="6.2"><div class="human-copy"><div class="eyebrow">AFTER / LUNCH PREP</div><div class="hook serif"><p>Back to</p><p>the kitchen.</p></div><div class="sub"><div class="small-line"></div>Orders sorted.<p>Time to pack.</p></div></div></section>
<section id="workflow" class="clip" data-start="4.6" data-duration="21.4"><div id="workflow-inner">
<div class="before-heading"><div class="eyebrow">THE MANUAL PART</div><h2 class="serif">Copy. Paste. Check. Repeat.</h2></div>
<div id="manual"><div class="sheet-bar">Lunch prep.xlsx</div><div class="sheet-caption">Copying each order by hand</div><div class="sheet-table"><div class="cell head">Order</div><div class="cell head">Chicken</div><div class="cell head">Tofu</div><div class="cell">Studio North</div><div class="cell active"><span id="typed-5">5</span></div><div class="cell"><span id="typed-3">3</span></div><div class="cell">Book Club</div><div class="cell"><span id="typed-2">2</span></div><div class="cell"></div><div class="cell">Workshop</div><div class="cell"></div><div class="cell"></div></div><div class="sheet-footer">Still to check: packing notes</div></div>
<div id="copy-toast">Copied</div>
<div id="app-chrome"><div id="app-logo" class="wordmark"><span class="mark">p</span>portion</div><div id="app-description">Catering orders → kitchen prep</div><h2 id="app-headline" class="serif">Orders in. Prep ready.</h2><div id="app-frame"></div><div id="inbox-label">Order inbox <span>3 orders</span></div><div id="app-divider"></div><div id="kitchen-title">Kitchen prep</div><div id="date-label">TODAY / LUNCH</div>
<div id="empty-state"><h3>Bring the orders together.</h3><p>One prep list, with the counts<p>and packing notes already gathered.</p></p></div><div id="build-btn">Build prep list <b>↗</b></div><div id="progress">Checking 3 orders…<div id="progress-track"><div id="progress-fill"></div></div></div>
<div id="result"><div id="total-block"><span id="total-number">24</span><span id="total-label">bowls to prep</span><span id="checked"><span class="check-circle">✓</span>3 orders checked</span></div><div class="split"><div class="prep-item"><span class="number">13</span><div class="name">Chicken</div><div class="breakdown">5 + 2 + 6 across the three orders</div></div><div class="prep-item"><span class="number">11</span><div class="name">Tofu</div><div class="breakdown">3 + 4 + 4 across the three orders</div></div></div><div class="packing-note"><div class="label">PACKING NOTE</div><div class="content">Sauce on the side</div><div class="attribution">Book Club · 6 bowls</div></div><div id="result-footnote">All three orders accounted for.</div><div id="send-btn">Send to kitchen ↗</div></div></div>
__CARDS__
<!-- Cursor shape and click-ring behavior adapted from installed simulated-cursor registry component. -->
<div id="cursor"><div id="cursor-pulse"></div><svg viewBox="0 0 24 24"><path d="M3 2.8 20.6 14 12.8 15.5 9 22 3 2.8Z" fill="#193D30" stroke="#FFFDF8" stroke-width="1.4"/></svg></div>
</div></section>
<section id="ready" class="clip" data-start="23.7" data-duration="8.1"><div id="ready-badge"><div id="ready-icon">✓</div><div><div id="ready-title">Prep sheet ready</div><div id="ready-sub">24 bowls · 3 orders</div></div></div></section>
<section id="ending" class="clip" data-start="31.2" data-duration="4.8"><div id="ending-inner"><div id="end-logo" class="wordmark"><span class="mark">p</span>portion</div><div id="end-head" class="serif"><p>24 lunches.</p><p class="accent">One prep list.</p></div><div id="end-line"></div><div id="end-cta">Get back to the kitchen. ↗</div><div id="end-sheet"><div class="end-sheet-label">KITCHEN PREP / READY</div><div class="end-sheet-number serif">24</div><div class="end-sheet-bowls">bowls for lunch</div><div class="end-sheet-rule"></div><div class="end-sheet-row"><span>Chicken</span><span>13</span></div><div class="end-sheet-row"><span>Tofu</span><span>11</span></div></div><div id="end-footer">ORDERS IN. PREP READY.</div></div></section>
<audio id="portion-original-score" src="assets/score.wav" data-start="0" data-duration="36" data-volume="1"></audio><audio id="portion-ui-sfx" src="assets/ui-sfx.wav" data-start="0" data-duration="36" data-volume="1"></audio>
</div><script>
const tl=gsap.timeline({paused:true});
tl.fromTo('#opening-copy .hook p',{y:26,opacity:0},{y:0,opacity:1,duration:.65,stagger:.12,ease:'power3.out'},.12);
tl.fromTo('#opening-copy .sub',{y:15,opacity:0},{y:0,opacity:1,duration:.5},1.2);
tl.to('#opening-copy > div',{opacity:0,duration:.2},4.5);
tl.fromTo('#workflow-inner',{y:1080},{y:0,duration:.65,ease:'power3.inOut'},4.6);
tl.set('#order-0',{rotation:-2},0).set('#order-1',{rotation:1.8},0).set('#order-2',{rotation:-1.1},0);
tl.set(['#typed-5','#typed-3','#typed-2','#copy-toast','#app-chrome','#cursor','#progress','#result'],{opacity:0},0);
tl.set('#cursor-pulse',{opacity:0,scale:.3},0);tl.set('#cursor',{x:433,y:407},0).to('#cursor',{opacity:1,duration:.25},5.35);
function move(x,y,at,d=.48){tl.to('#cursor',{x,y,duration:d,ease:'power2.inOut'},at)}
function click(at){tl.fromTo('#cursor-pulse',{scale:.3,opacity:.8},{scale:1.8,opacity:0,duration:.4,ease:'power2.out',immediateRender:false},at);tl.to('#cursor',{scale:.9,duration:.09},at).to('#cursor',{scale:1,duration:.14},at+.09)}
click(5.75);tl.fromTo('#copy-toast',{opacity:0,y:0},{opacity:1,y:-8,duration:.18},5.8).to('#copy-toast',{opacity:0,duration:.18},6.3);
move(1450,549,6.0);click(6.55);tl.set('#typed-5',{opacity:1},6.55);
move(513,416,6.85);click(7.35);move(1640,549,7.52);click(8.02);tl.set('#typed-3',{opacity:1},8.02);
move(481,615,8.25);click(8.7);move(1450,638,8.82);click(9.3);tl.set('#typed-2',{opacity:1},9.3);
tl.to(['#manual','.before-heading'],{opacity:0,y:-36,duration:.4,ease:'power2.in'},9.85);
tl.to('#app-chrome',{opacity:1,duration:.65},10.12);
[0,1,2].forEach((i)=>tl.to('#order-'+i,{x:120-[138,210,92][i],y:[398,580,762][i]-[322,526,730][i],rotation:0,duration:.85,ease:'power3.inOut'},10.05+i*.09));
move(1646,865,10.03,.85);tl.to('#cursor',{opacity:0,duration:.2},11.1);
tl.to('#cursor',{opacity:1,duration:.25},13.05);move(1390,749,13.25,.6);click(14.05);
tl.to('#build-btn',{scale:.97,duration:.1},14.05).to('#build-btn',{scale:1,duration:.16},14.15);
tl.to(['#empty-state','#build-btn'],{opacity:0,duration:.24},14.3);tl.to('#progress',{opacity:1,duration:.24},14.55);
tl.fromTo('#progress-fill',{scaleX:0},{scaleX:1,duration:1.5,ease:'power2.inOut'},14.6);
tl.to('#cursor',{opacity:0,duration:.25},14.5);tl.to('#progress',{opacity:0,duration:.25},16.22);
tl.fromTo('#result',{y:18,opacity:0},{y:0,opacity:1,duration:.55,ease:'power2.out'},16.5);
tl.fromTo('.packing-note',{y:12,opacity:0},{y:0,opacity:1,duration:.5},18.65);
tl.fromTo('#send-btn',{opacity:0},{opacity:1,duration:.4},21.15);
tl.to('#cursor',{opacity:1,duration:.2},22.1);move(1598,899,22.1,.65);click(22.98);
tl.to('#send-btn',{scale:.96,duration:.1},22.98).to('#send-btn',{scale:1,duration:.14},23.081);
tl.to(['#send-btn','#result-footnote','#cursor'],{opacity:0,duration:.25},23.45);
tl.fromTo('#ready-badge',{opacity:0,y:16},{opacity:1,y:0,duration:.42,ease:'power2.out'},23.7);
tl.to('#workflow-inner',{opacity:0,duration:.4},25.6);
tl.to('#ready-badge',{x:-1102,y:-13,scale:.84,transformOrigin:'left top',duration:.75,ease:'power3.inOut'},25.6);
tl.fromTo('#after-copy .eyebrow',{opacity:0},{opacity:1,duration:.3},26.0);
tl.fromTo('#after-copy .hook',{y:22,opacity:0},{y:0,opacity:1,duration:.65,ease:'power3.out'},26.0);
tl.fromTo('#after-copy .sub',{y:15,opacity:0},{y:0,opacity:1,duration:.55},26.6);
tl.fromTo('#ending-inner',{y:1080},{y:0,duration:.65,ease:'power3.inOut'},31.2);
tl.fromTo('#end-head p',{y:25,opacity:0},{y:0,opacity:1,stagger:.12,duration:.6,ease:'power3.out'},31.8);
tl.fromTo('#end-sheet',{y:28,rotation:3,opacity:0},{y:0,rotation:0,opacity:1,duration:.75,ease:'power3.out'},31.92);
tl.fromTo(['#end-line','#end-cta'],{y:15,opacity:0},{y:0,opacity:1,duration:.5,stagger:.1},32.45);
window.__timelines['main']=tl;
</script></body></html>'''
# Keep markup valid and reproducible.
html=html.replace('__CARDS__',cards).replace('height: seventy; height: seventy; ','')
html=html.replace('<p>One prep list, with the counts<p>and packing notes already gathered.</p></p>','<p>One prep list, with the counts</p><p style="margin-top:0">and packing notes already gathered.</p>')
(PROJECT/'index.html').write_text(html)
(PROJECT/'meta.json').write_text(json.dumps({'id':'portion','name':'Portion — Orders in. Prep ready.'},indent=2))
print('Wrote new 36-second Portion composition and validated 24 = 13 + 11.')
