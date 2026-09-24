"""Build original deterministic campaign film. No generative provider calls."""
from pathlib import Path
import json, shutil
P=Path(__file__).resolve().parent
(P/'compositions/frames').mkdir(parents=True,exist_ok=True)
shutil.copy2(P.parent/'kite-core-demo/assets/gsap.min.js',P/'assets/gsap.min.js')
BASE='''
@font-face{font-family:Onest;src:url('assets/fonts/Onest-latin.woff2') format('woff2');font-weight:100 900}
*{box-sizing:border-box;margin:0;padding:0}#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:Onest;color:#1D1C1D}
.clip{position:absolute;inset:0;width:100%;height:100%}.p-bg{background:#FFFFFF}.p-brand{position:absolute;left:100px;top:68px;width:138px;height:60px;object-fit:contain}.p-foot{position:absolute;left:100px;top:952px;font-size:24px;color:#616061;letter-spacing:.01em}.p-step{position:absolute;right:100px;top:80px;font-size:24px;color:#616061}.p-h{font-size:90px;line-height:1.07;letter-spacing:-4px;font-weight:600}.p-tag{font-size:24px;letter-spacing:2px;font-weight:600}.p-muted{color:#616061}.p-line{display:block}.p-button{display:inline-flex;align-items:center;justify-content:center;background:#347BCD;color:white;border-radius:100px;padding:20px 35px;font-size:30px;font-weight:600}.p-app{width:66px;height:66px;border-radius:14px;object-fit:cover}.p-row{display:flex;align-items:center;gap:20px}.p-rule{height:2px;background:#E5E7EB}.p-chip{border:1px solid #D4DFEC;border-radius:100px;padding:11px 22px;font-size:25px;color:#105DA8}
.p-page{width:1640px;height:630px;position:absolute;background:#F4F1E8;color:#182B32;border:2px solid #DADDDC;border-radius:14px;overflow:hidden;transform-origin:0 0}
.p-browser{height:50px;border-bottom:1px solid #DADDDC;display:flex;align-items:center;gap:9px;padding:0 28px;font-size:20px;background:white;color:#616061}.p-dot{width:8px;height:8px;border-radius:50%;background:#B7BDC0}.p-browser-label{margin-left:18px}
.p-page-body{position:relative;height:580px;padding:35px 58px}.p-relay{font-size:32px;font-weight:800;letter-spacing:-1px}.p-page-title{font-size:86px;line-height:1.02;letter-spacing:-4px;font-weight:600;width:970px;margin-top:35px}.p-page-sub{font-size:30px;line-height:1.35;width:770px;margin-top:24px}.p-page-cta{position:absolute;left:58px;bottom:38px;padding:19px 28px;background:#182B32;color:#F4F1E8;border-radius:100px;font-size:25px}
.p-task-art{position:absolute;right:55px;top:48px;width:440px;height:440px;background:#D4F578;border-radius:12px;padding:42px 32px}.p-art-label{font-size:22px;letter-spacing:2px;color:#182B32;font-weight:600;margin-bottom:34px}.p-task{width:376px;height:70px;background:#F4F1E8;border-radius:8px;display:flex;gap:19px;align-items:center;padding:0 23px;margin-bottom:18px;font-size:24px;color:#182B32}.p-tick{width:22px;height:22px;border:2px solid #182B32;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px}
.p-social{position:absolute;width:560px;height:630px;background:#182B32;color:#F4F1E8;padding:44px;border-radius:14px;transform-origin:0 0}.p-social-title{font-size:70px;line-height:1.03;letter-spacing:-3px;margin-top:53px}.p-social-bar{height:36px;background:#D4F578;border-radius:5px;margin:12px 0}.p-social-body{font-size:29px;line-height:1.25;margin-top:35px}.p-social-foot{position:absolute;left:44px;bottom:37px;font-size:21px;letter-spacing:1px;color:#D4F578}
.p-email{position:absolute;width:430px;height:500px;background:white;border:2px solid #DADDDC;border-radius:14px;overflow:hidden;transform-origin:0 0;color:#182B32}.p-email-chrome{height:60px;padding:18px 28px;background:#F4F1E8;font-size:20px;border-bottom:1px solid #DADDDC}.p-email-body{padding:28px}.p-email-subject{font-size:34px;line-height:1.1;letter-spacing:-1px;margin-top:26px;font-weight:600}.p-email-copy{font-size:25px;line-height:1.4;margin-top:28px}.p-email-cta{display:inline-flex;background:#D4F578;color:#182B32;border-radius:100px;padding:14px 23px;font-size:24px;margin-top:30px}
'''
def logo():return '<img class="p-brand" src="assets/kite.png" alt="Kite">'
def footer():return '<div class="p-foot">Illustrative campaign</div>'
def page(extra=''):
 return f'''<div class="p-page {extra}"><div class="p-browser"><i class="p-dot"></i><i class="p-dot"></i><i class="p-dot"></i><span class="p-browser-label">Relay / campaign preview</span></div><div class="p-page-body"><div class="p-relay">relay</div><div class="p-page-title"><span class="p-line">Make room for</span><span class="p-line">real work.</span></div><div class="p-page-sub">Bring your team’s tasks into one clear plan.</div><div class="p-page-cta">Explore Relay ↗</div><div class="p-task-art"><div class="p-art-label">A CLEARER MONDAY</div><div class="p-task"><span class="p-tick">✓</span>Set the priorities</div><div class="p-task"><span class="p-tick">✓</span>Share the plan</div><div class="p-task"><span class="p-tick">✓</span>Make it happen</div></div></div></div>'''
def social(extra=''):
 return f'''<div class="p-social {extra}"><div class="p-relay">relay</div><div class="p-social-title">Less chasing.<span class="p-line">More doing.</span></div><div style="margin-top:38px"><div class="p-social-bar" style="width:100%"></div><div class="p-social-bar" style="width:75%"></div><div class="p-social-bar" style="width:49%"></div></div><div class="p-social-body">Make room for real work.</div><div class="p-social-foot">YOUR TEAM. ONE CLEAR PLAN.</div></div>'''
def email(extra=''):
 return f'''<div class="p-email {extra}"><div class="p-email-chrome">LAUNCH EMAIL / DRAFT</div><div class="p-email-body"><div class="p-relay">relay</div><div class="p-email-subject">Your next clear Monday.</div><div class="p-email-copy">Meet Relay.<span class="p-line">One clear plan for your team.</span></div><div class="p-email-cta">Explore Relay ↗</div></div></div>'''
def write(id,dur,markup,css,js):
 # Prefix every authored class and selector to keep assembled siblings isolated.
 allcss=(BASE+css).replace('p-','f'+id+'-')
 markup=markup.replace('p-','f'+id+'-').replace('kite-slack-apf'+id+'-icon.png','kite-slack-app-icon.png')
 js=js.replace('p-','f'+id+'-')
 out=f'''<template>
<style>{allcss}</style>
<div id="root" data-composition-id="{id}" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
<div id="f{id}-background" class="clip f{id}-bg" data-start="0" data-duration="{dur}" data-track-index="0"></div>
<div id="f{id}-content" class="clip" data-start="0" data-duration="{dur}" data-track-index="1">{markup}</div>
</div>
<script src="assets/gsap.min.js"></script>
<script>
(function(){{
const tl=gsap.timeline({{paused:true}});
const rise=(s,t,d=.65)=>tl.fromTo(s,{{opacity:0,y:35}},{{opacity:1,y:0,duration:d,stagger:.09,ease:'power3.out'}},t);
{js}
window.__timelines=window.__timelines||{{}};window.__timelines['{id}']=tl;
}})();
</script>
</template>'''
 (P/f'compositions/frames/{id}.html').write_text(out)

write('01-brief',8,logo()+'''
<div class="p-hook"><div class="p-hook-title"><div class="p-word">One brief.</div><div class="p-word p-blue">A whole</div><div class="p-word p-blue">campaign.</div></div><div class="p-outcome"><div class="p-sheet"><div class="p-tag">THE START</div><div class="p-sheet-title">A simple<br>brief.</div><div class="p-sheet-line"></div><div class="p-sheet-line" style="width:65%"></div></div><div class="p-channel p-ch1">Landing page ↗</div><div class="p-channel p-ch2">Social post ↗</div><div class="p-channel p-ch3">Launch email ↗</div></div></div>
<div class="p-demo"><div class="p-demo-title p-h">Start with the goal.</div><div class="p-message"><div class="p-channel-head"># marketing <span>with Kite</span></div><div class="p-message-body"><div class="p-avatar">Y</div><div class="p-copy"><div class="p-sender">You <span>just now</span></div><div class="p-briefline">Launch Relay to small teams.</div><div class="p-briefmore">Help them turn scattered tasks into a clear plan.</div><div class="p-deliverables">Landing page <span>·</span> Social post <span>·</span> Email</div></div><div class="p-send p-button">Send to Kite ↑</div><div class="p-sent p-row"><img class="p-app" src="assets/kite-slack-app-icon.png" alt="Kite app"><span>Brief shared with Kite</span></div></div></div></div>
'''+footer(),'''
.p-hook-title{position:absolute;left:100px;top:258px;font-size:122px;line-height:1.08;letter-spacing:-6px;font-weight:600}.p-blue{color:#347BCD}.p-outcome{position:absolute;left:1110px;top:245px;width:690px;height:600px}.p-sheet{width:460px;height:380px;background:#EEF2F8;border:1px solid #D4DFEC;border-radius:14px;padding:40px}.p-sheet-title{font-size:65px;line-height:1.08;letter-spacing:-3px;margin-top:22px}.p-sheet-line{height:6px;width:88%;background:#B6CDE5;margin-top:24px}.p-channel{position:absolute;left:220px;top:330px;background:#347BCD;color:white;width:440px;height:76px;border-radius:12px;display:flex;align-items:center;padding-left:30px;font-size:32px}.p-ch2{top:421px}.p-ch3{top:512px}.p-demo-title{position:absolute;left:100px;top:183px}.p-message{position:absolute;left:190px;top:329px;width:1540px;height:534px;border:2px solid #D4DFEC;border-radius:14px;background:white;overflow:hidden}.p-channel-head{height:84px;border-bottom:2px solid #E5E7EB;padding:22px 36px;font-size:32px;font-weight:600}.p-channel-head span{font-size:25px;color:#616061;font-weight:400;margin-left:16px}.p-message-body{position:relative;padding:37px;height:446px}.p-avatar{position:absolute;left:37px;top:36px;width:62px;height:62px;border-radius:12px;background:#EEF2F8;display:grid;place-items:center;font-size:28px}.p-copy{margin-left:88px}.p-sender{font-size:29px;font-weight:600}.p-sender span{font-size:22px;font-weight:400;margin-left:13px;color:#616061}.p-briefline{font-size:44px;letter-spacing:-1.3px;margin-top:23px}.p-briefmore{font-size:34px;line-height:1.4;margin-top:10px}.p-deliverables{font-size:28px;color:#105DA8;margin-top:26px}.p-deliverables span{margin:0 12px}.p-send{position:absolute;right:35px;bottom:24px}.p-sent{position:absolute;left:125px;bottom:21px;font-size:27px}.p-sent .p-app{width:45px;height:45px}
''','''
rise('.p-word',.12,.7);rise('.p-sheet',.1);rise('.p-ch1',.65);rise('.p-ch2',.95);rise('.p-ch3',1.25);
tl.to('.p-hook',{opacity:0,duration:.2},2.45);
tl.fromTo('.p-demo',{opacity:0},{opacity:1,duration:.2},2.65);
rise('.p-demo-title',2.65);rise('.p-message',2.75);rise('.p-briefline',3.05);rise('.p-briefmore',3.45);rise('.p-deliverables',3.8);rise('.p-send',4.25);
tl.to('.p-send',{scale:.94,duration:.12},5.15).to('.p-send',{scale:1,duration:.2},5.28).to('.p-send',{opacity:0,duration:.2},5.65);rise('.p-sent',5.65);
''')

write('02-direction',8,'''
<div class="p-brand-tile">'''+logo()+'''</div><div class="p-step">BRIEF → DIRECTION</div><div class="p-title p-h">A clear direction.</div>
<div class="p-reply"><div class="p-row"><img class="p-app" src="assets/kite-slack-app-icon.png" alt="Kite app"><div><div class="p-kite">Kite</div><div class="p-replytext">Here’s the campaign idea.</div></div></div><div class="p-chips"><span class="p-chip">Small teams</span><span class="p-chip">Less task chaos</span></div></div>
<div class="p-idea"><div class="p-relay">relay <span>/ CAMPAIGN DIRECTION</span></div><div class="p-idea-title"><span class="p-line p-idea-a">Make room for</span><span class="p-line p-idea-b">real work.</span></div><div class="p-idea-foot">One message. Every channel.</div></div><div class="p-intents"><span>A page to explore</span><span>A post to discover</span><span>An email to act</span></div>
''', '''
.p-bg{background:#347BCD}.p-brand-tile{position:absolute;left:100px;top:62px;width:165px;height:79px;border-radius:12px;background:white}.p-brand-tile .p-brand{left:19px;top:14px;width:126px;height:52px}.p-step{color:#FFFFFF}.p-title{position:absolute;left:100px;top:193px;color:white}.p-reply{position:absolute;left:100px;top:340px;width:1720px;height:432px;background:white;border-radius:14px;padding:60px}.p-kite{font-size:32px;font-weight:600}.p-replytext{font-size:48px;margin-top:15px;letter-spacing:-1px}.p-chips{display:flex;gap:14px;margin-top:50px;margin-left:87px}.p-idea{position:absolute;left:100px;top:340px;width:1720px;height:450px;border-radius:14px;background:#F4F1E8;padding:34px 60px;color:#182B32}.p-idea .p-relay span{font-size:20px;letter-spacing:2px;font-weight:400;margin-left:25px}.p-idea-title{font-size:102px;line-height:1.38;letter-spacing:-5px;margin-top:20px;font-weight:600}.p-idea-b{background:#D4F578;width:580px;padding:0 10px;margin-left:-10px}.p-idea-foot{position:absolute;right:65px;bottom:50px;font-size:34px;width:320px;line-height:1.3}.p-intents{position:absolute;left:100px;top:843px;width:1720px;display:flex;justify-content:space-between;color:white;font-size:29px}
''','''
rise('.p-title',.1);rise('.p-reply',.2);rise('.p-chips',.85);
tl.to('.p-reply',{opacity:0,duration:.25},2.2);
tl.fromTo('.p-idea',{opacity:0,y:35},{opacity:1,y:0,duration:.65,ease:'power3.out'},2.4);
rise('.p-idea-a',2.65);rise('.p-idea-b',3.2);rise('.p-idea-foot',4.3);rise('.p-intents span',5.1);
''')

write('03-campaign',12,logo()+'''
<div class="p-step">DIRECTION → CAMPAIGN</div><div class="p-title-first p-h">The campaign takes shape.</div><div class="p-title-last p-h">One idea. Fully connected.</div>
'''+page('p-page-main')+social('p-social-main')+email('p-email-main')+'''
<div class="p-stage-label p-label1">01 / LANDING PAGE</div><div class="p-stage-label p-label2">02 / SOCIAL POST</div><div class="p-stage-label p-label3">03 / LAUNCH EMAIL</div><div class="p-summary">A landing page. A social post. A launch email.</div>
'''+footer(),'''
.p-title-first,.p-title-last{position:absolute;left:100px;top:170px;font-size:76px}.p-page-main{left:140px;top:300px}.p-social-main{left:1180px;top:290px}.p-email-main{left:1388px;top:322px}.p-stage-label{position:absolute;font-size:24px;letter-spacing:1.5px;font-weight:600;color:#105DA8;top:835px}.p-label1{left:100px}.p-label2{left:995px}.p-label3{left:1388px}.p-summary{position:absolute;left:100px;top:894px;font-size:30px;color:#616061}
''','''
rise('.p-title-first',.1);rise('.p-page-main',.15);rise('.p-page-title',.4);rise('.p-task',.85);
tl.to('.p-page-main',{x:-40,y:70,scale:.55,duration:1.05,ease:'power3.inOut'},4);
tl.fromTo('.p-social-main',{opacity:0,x:100},{opacity:1,x:0,duration:.8,ease:'power3.out'},4.35);
rise('.p-social-title',4.6);rise('.p-social-bar',5.0);
tl.to('.p-page-main',{x:-40,y:80,scale:.51,duration:.9,ease:'power3.inOut'},7.6);
tl.to('.p-social-main',{x:-185,y:32,scale:.65,duration:.9,ease:'power3.inOut'},7.6);
tl.fromTo('.p-email-main',{opacity:0,x:120},{opacity:1,x:0,duration:.85,ease:'power3.out'},7.95);
tl.to('.p-title-first',{opacity:0,duration:.2},7.5);rise('.p-title-last',7.8);rise('.p-stage-label',8.8);rise('.p-summary',9.45);
''')

write('04-review',8,logo()+'''
<div class="p-step">CAMPAIGN → YOUR REVIEW</div><div class="p-reviewcopy"><div class="p-h p-reviewtitle">Your campaign.<span class="p-line">Ready to review.</span></div><div class="p-reviewmessage"><div class="p-row"><img class="p-app" src="assets/kite-slack-app-icon.png" alt="Kite app"><span>Kite</span></div><div class="p-reviewtext">The page, post and email are ready.</div><div class="p-button">Review campaign ↗</div></div><div class="p-decision">You decide what goes live.</div></div>
<div class="p-lockup"><img class="p-final-logo" src="assets/kite.png" alt="Kite"><div class="p-final-title">Your AI marketer.</div><div class="p-final-sub">Start with a brief.</div><div class="p-url">kite.ai <span>↗</span></div><div class="p-underline"></div></div>
<div class="p-proof">'''+page('p-final-page')+social('p-final-social')+email('p-final-email')+'''<div class="p-prooflabel">ONE BRIEF. A WHOLE CAMPAIGN.</div></div>
'''+footer(),'''
.p-reviewtitle{position:absolute;left:100px;top:226px;font-size:77px;line-height:1.12;letter-spacing:-3.6px}.p-reviewmessage{position:absolute;left:100px;top:452px;width:710px;border-top:2px solid #D4DFEC;padding-top:25px}.p-reviewmessage .p-row{font-size:29px;font-weight:600}.p-reviewmessage .p-app{width:48px;height:48px}.p-reviewtext{font-size:32px;line-height:1.3;margin:23px 0;width:650px}.p-reviewmessage .p-button{font-size:28px;padding:16px 29px}.p-decision{position:absolute;left:100px;top:800px;font-size:30px;color:#616061}.p-lockup{position:absolute;left:100px;top:243px}.p-final-logo{width:340px;height:146px;object-fit:contain}.p-final-title{font-size:74px;letter-spacing:-3px;font-weight:500;margin-top:40px}.p-final-sub{font-size:42px;margin-top:22px;color:#616061}.p-url{font-size:42px;color:#105DA8;margin-top:48px}.p-url span{margin-left:20px}.p-underline{width:173px;height:3px;background:#347BCD;margin-top:12px;transform-origin:0 50%}.p-proof{position:absolute;left:870px;top:285px;width:950px;height:580px}.p-final-page{left:0;top:0;transform:scale(.55)}.p-final-page .p-page-cta{display:none}.p-final-social{left:90px;top:235px;transform:scale(.46)}.p-final-email{left:410px;top:235px;transform:scale(.66)}.p-prooflabel{position:absolute;left:0;top:602px;font-size:23px;letter-spacing:1.7px;color:#105DA8}
''','''
rise('.p-reviewtitle',.1);rise('.p-reviewmessage',.3);rise('.p-proof',.25);rise('.p-decision',1.5);
tl.to('.p-reviewcopy',{opacity:0,duration:.25},3.2);
tl.fromTo('.p-lockup',{opacity:0,y:30},{opacity:1,y:0,duration:.7,ease:'power3.out'},3.55);
rise('.p-final-title',3.85);rise('.p-final-sub',4.2);rise('.p-url',4.6);
tl.fromTo('.p-underline',{scaleX:0},{scaleX:1,duration:.6,ease:'power3.out'},5.4);
''')
# Preserve planned narrative separately from worker result status.
s=P/'STORYBOARD.md';s.write_text(s.read_text().replace('status: outline','status: animated'))
print('Built four scenes')
