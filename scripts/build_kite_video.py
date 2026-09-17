"""Author Kite's seven-shot, seekable HyperFrames film from the approved brief."""
from pathlib import Path
import html,json,shutil

ROOT=Path(__file__).resolve().parents[1];P=ROOT/'videos/kite'
def e(v):return html.escape(str(v),quote=True)
def txt(s,x,y,size=34,weight=400,color='#0E0E0E',anchor='start',id=None):
 return f'<text data-essential="true"'+(f' id="{id}"' if id else '')+f' x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{e(s)}</text>'
def rect(x,y,w,h,fill='#FFFFFF',stroke='#DDDAD7',r=14):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def group(id,body):return f'<g id="{id}">{body}</g>'
def head(lines):return ''.join(txt(v,108,790+i*57,54 if len(lines)>1 else 58,600) for i,v in enumerate(lines))
def shell(y=837,h=280):
 return rect(108,y,864,h)+rect(109,y+1,9,h-2,'#E9E3EA','#E9E3EA',4)+txt('# marketing',140,y+42,29,600)+f'<path d="M120 {y+61} H970" stroke="#E7E4E1" stroke-width="2"/>'
def button(s,x,y,w):return rect(x,y,w,49,'#FFFFFF','#C7C4C1',7)+txt(s,x+w/2,y+33,28,600,anchor='middle')
def svg(body):return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">'+body+'</svg>'

shutil.copy(P/'.media/images/logo_001.png',P/'assets/kite-wordmark.png')
shots=[]
# 01: accumulated work surfaces settle, then converge into the same conversation.
s=head(['One request.','The work around it.'])
for i,title in enumerate(['Product page','Announcement','Walkthrough','Email']):
 x=108+i*24;y=870+i*48
 s+=group(f'work-{i}',rect(x,y,788,60,'#FFF4EC')+txt(title,x+24,y+39,34,500))
s+=group('open-thread',shell(862,252)+txt('You',145,965,30,600)+rect(139,984,799,93,'#FCFBFA')+txt('Message Kite',162,1039,36,400,'#66615D'))
shots.append((0,6,s))
# 02: the exact request is typed once, then held.
s=head(['Ask in Slack'])+shell()+txt('You',145,947,31,600)
s+=group('request',txt('Kite, help us prepare',145,1001,42,500,id='request-first')+txt('the launch.',145,1054,42,500,id='request-last'))
shots.append((6,13,s))
# 03: plan before work, one highlight at a time. Thread remains anchored.
s=head(['Plan first'])+shell(837,294)+txt('Kite',145,935,30,600)
for i,(key,value,y) in enumerate([('Inputs','Website and launch brief',979),('Prepare','Product page, announcement,',1025),('Decide','Approve public changes',1110)]):
 s+=group(f'plan-row-{i}',group(f'plan-highlight-{i}',rect(128,y-32,821,43,'#FFF0E5','#FFF0E5',6))+txt(key,145,y,30,600)+txt(value,301,y,32))
 if i==1:s+=txt('walkthrough, email',301,1065,32)
shots.append((13,21,s))
# 04: no invented research findings. Source and caveat stay on the same card.
s=head(['Reviewable work,','in the conversation'])
s+=group('research',rect(108,867,864,210)+txt('Kite · Research summary',140,912,32,600)+txt('Source: sample launch brief',140,956,31)+txt('Confirm audience and launch date.',140,999,33)+txt('Illustrative inputs; not verified findings.',140,1041,29,400,'#535353'))
s+=group('review-note',txt('Prepared for review',140,1126,32,600))
shots.append((21,27,s))
# 05: four examples return to one website-draft card with documented controls.
s=head(['Reviewable work,','in the conversation'])
for i,title in enumerate(['Product page','Announcement','Walkthrough','Email']):
 x=108+(i%2)*440;y=880+(i//2)*94
 s+=group(f'output-{i}',rect(x,y,424,78,'#FFF4EC')+txt(title,x+23,y+50,34,500))
s+=group('unified-draft',rect(108,883,864,180)+txt('Kite · Product page',143,936,34,600)+button('Preview',143,977,162)+button('Review',324,977,155))
s+=txt('Prepared for review',140,1126,32,600)
shots.append((27,31,s))
# 06: only a typed, unsent publication instruction. Mode and state are editorial.
s=head(['Public changes stay with you.'])+txt('Propose first mode',108,830,28,500,'#535353')
s+=shell(854,245)+txt('Product page',142,959,34,600)+button('Preview',538,929,164)+button('Review',720,929,161)
s+=rect(140,992,802,78,'#FCFBFA')+txt('Publish it.',161,1043,37,500,id='approval-draft')
s+=txt('Illustrative draft — not sent',140,1133,30,500,'#535353')
shots.append((31,37,s))
# 07: original official wordmark and a single CTA. No invented install URL.
s=group('end-lockup','<image data-essential="true" href="assets/kite-wordmark.png" x="250" y="690" width="580" height="346"/>'+txt('AI marketer in Slack',540,1033,47,500,anchor='middle')+rect(278,1066,524,79,'#FF6D2D','#FF6D2D',39)+txt('Add Kite to Slack',540,1119,42,600,anchor='middle'))
shots.append((37,42,s))

caps=json.loads((P/'captions.json').read_text())
elements=[]
elements.append('<div id="scene-labels" class="clip" data-start="0" data-duration="37" data-track-index="2">'+svg(txt('Illustrative workflow',108,718,28,500)+txt('Sample company',972,718,28,500,anchor='end'))+'</div>')
for i,(start,end,body) in enumerate(shots):
 elements.append(f'<section id="shot-{i+1}" class="clip" data-start="{start}" data-duration="{end-start}" data-track-index="1">{svg(body)}</section>')
for i,c in enumerate(caps):
 elements.append(f'<div id="caption-{i}" class="clip captions" data-start="{c["start"]:.5f}" data-duration="{c["end"]-c["start"]:.5f}" data-track-index="3"><div class="caption">{e(c["text"])}</div></div>')
elements.append('<audio id="kite-mix" src="assets/mix.wav" data-start="0" data-duration="42" data-volume="1" data-track-index="4"></audio>')

js='''const tl=gsap.timeline({paused:true});
// The registry thread-message-stack was inspected; its message-bubble layout and
// moving background do not fit this persistent, source-labelled product screen.
// These fixed card positions preserve the approved crop-safe geometry.
for(let i=0;i<4;i++){
 tl.fromTo('#work-'+i,{opacity:0,y:20},{opacity:1,y:0,duration:.36,ease:'power2.out'},.42+i*.31);
 tl.to('#work-'+i+' text',{opacity:0,duration:.12},3.2);
 tl.to('#work-'+i,{y:48*(1.5-i),x:24*(1.5-i),opacity:0,duration:.48,ease:'power2.inOut'},3.35+i*.06);
}
tl.fromTo('#open-thread',{opacity:0,y:9},{opacity:1,y:0,duration:.46,ease:'power2.out'},3.76);
const requestA='Kite, help us prepare',requestB='the launch.';
function setRequest(t){
 const count=Math.max(0,Math.min(33,Math.floor((t-6.35)*17)));
 document.getElementById('request-first').textContent=requestA.slice(0,count);
 document.getElementById('request-last').textContent=requestB.slice(0,Math.max(0,count-requestA.length-1));
}
function setDecision(t){document.getElementById('approval-draft').textContent='Publish it.'.slice(0,Math.max(0,Math.min(11,Math.floor((t-33.8)*9))));}
for(let i=0;i<3;i++){
 const a=[13.5,16.6,19.0][i],b=[16.4,18.8,21][i];
 tl.fromTo('#plan-highlight-'+i,{opacity:0},{opacity:1,duration:.23},a);
 if(i<2)tl.to('#plan-highlight-'+i,{opacity:0,duration:.2},b);
}
tl.fromTo('#research',{opacity:0,y:10},{opacity:1,y:0,duration:.4,ease:'power2.out'},21);
tl.fromTo('#review-note',{opacity:0,y:7},{opacity:1,y:0,duration:.3},25.8);
for(let i=0;i<4;i++){
 tl.fromTo('#output-'+i,{opacity:0,y:9},{opacity:1,y:0,duration:.3,ease:'power2.out'},27+i*.12);
 tl.to('#output-'+i,{opacity:0,x:(i%2? -35:35),y:(i>1?-20:20),duration:.35,ease:'power2.inOut'},30.1);
}
tl.fromTo('#unified-draft',{opacity:0,y:5},{opacity:1,y:0,duration:.38},30.4);
tl.fromTo('#end-lockup',{opacity:1,y:10},{opacity:1,y:0,duration:.45,ease:'power2.out'},37);
tl.eventCallback('onUpdate',()=>{setRequest(tl.time());setDecision(tl.time());});
setRequest(0);setDecision(0);
window.__timelines['kite-film']=tl;
'''
css='''@font-face{font-family:Onest;src:url('assets/Onest.woff2') format('woff2');font-weight:100 900}
*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#FFFFFF}
#root{position:relative;width:100%;height:100%;background:#FFFFFF;font-family:Onest,sans-serif}
.clip{position:absolute;inset:0;width:100%;height:100%}svg{display:block;font-family:Onest,sans-serif}
.caption{position:absolute;left:108px;top:1163px;width:864px;min-height:62px;padding:12px 18px;border-radius:10px;background:#0E0E0E;color:#FFFFFF;text-align:center;font-size:32px;font-weight:500;line-height:38px}
.ornament{position:absolute;left:108px;width:864px;height:2px;background:#EEE9E5}.ornament.top{top:400px}.ornament.bottom{top:1520px}
'''
(P/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Kite — Ask, plan, review</title><script src="assets/gsap.min.js"></script><style>'+css+'</style></head><body><main id="root" data-composition-id="kite-film" data-width="1080" data-height="1920" data-duration="42" data-fps="30"><div class="ornament top"></div><div class="ornament bottom"></div>'+''.join(elements)+'</main><script>'+js+'</script></body></html>')
import re
inventory=[]
for i,(_,_,s) in enumerate(shots):inventory.append({'shot':i+1,'screen_text':[html.unescape(x) for x in re.findall(r'<text[^>]*>(.*?)</text>',s)]})
(P/'final-copy.json').write_text(json.dumps({'voiceover':json.loads((P/'storyboard.json').read_text())['voiceover'],'captions':caps,'global_labels':['Illustrative workflow','Sample company'],'shots':inventory,'note':'Review-ready and unsent-state text are editorial explanations, not claims of native status labels. No publication or send occurs.'},ensure_ascii=False,indent=2)+'\n')
print('Built 42-second film, seven shots, measured caption cues and exact voiceover.')
