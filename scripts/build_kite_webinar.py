"""Original screen-led Kite film: a webinar request stays in one Slack thread."""
from pathlib import Path
import html,json
R=Path(__file__).resolve().parents[1];P=R/'videos/kite-webinar'
def t(v,x,y,s=30,w=400,c='#151513',anchor='start',id=''):
 return f'<text data-essential="true"'+(f' id="{id}"' if id else '')+f' x="{x}" y="{y}" font-size="{s}" font-weight="{w}" fill="{c}" text-anchor="{anchor}">{html.escape(v)}</text>'
def r(x,y,w,h,c='#FFFFFF',rad=0,stroke='none'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{c}" stroke="{stroke}" stroke-width="2"/>'
def g(id,s,attr=''):return f'<g id="{id}" {attr}>{s}</g>'
def rule(x,y,x2,y2,c='#DDD9D1'):return f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="2"/>'
def circ(x,y,rad,c):return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{c}"/>'
def button(v,x,y,w):return r(x,y,w,58,'#FFFFFF',8,'#C7C2B9')+t(v,x+w/2,y+38,28,600,anchor='middle')
def av(v,x,y,color='#EAE5DC'):return r(x,y,58,58,color,13)+t(v,x+29,y+39,29,600,anchor='middle')
def sender(v,x,y,color='#EAE5DC'):return av(v[0],x,y,color)+t(v,x+82,y+34,29,650)
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'+s+'</svg>'
# Persistent shell gives every action a stable place.
shell=r(0,0,1920,1080,'#F6F3ED')+t('Illustrative workflow',72,63,23,500,'#57534C')+t('Sample company',1848,63,23,500,'#57534C','end')
shell+=r(72,102,1776,833,'#FFF',22,'#D8D3CB')+r(72,102,264,833,'#332136',22)+t('Sample company',101,161,26,650,'#FFF')
shell+=t('Channels',101,261,23,500,'#D7CDD9')+r(90,286,228,57,'#6A4B6F',8)+t('# marketing',109,324,27,550,'#FFF')+t('# team',109,389,26,400,'#D7CDD9')+t('Apps',101,523,23,500,'#D7CDD9')+t('Kite',109,579,28,600,'#FFF')
shell+=t('# marketing',385,165,35,650)+t('Thread',1775,165,26,500,'#66615A','end')+rule(336,203,1847,203)
states=[]
# Cold-open on the task itself. New input, not the prior film's headline.
s=t('Message Kite',437,290,30,600)+r(412,326,1360,411,'#FFFFFF',15,'#BDB6AB')
s+=t('Kite, get Thursday’s webinar ready.',448,411,47,500,id='typed-a')+t('Signup page + invite. Drafts only.',448,476,43,500,id='typed-b')
s+=r(448,522,536,83,'#F3EFE6',12)+r(468,541,40,45,'#FF6D2D',7)+t('Session brief',532,574,31,550)+t('Attached',923,574,24,400,'#625C51','end')
s+=g('request-send',r(1660,648,76,60,'#27482D',10)+'<path d="M1684 664L1711 678L1684 694Z" fill="#FFF"/>')
states.append(('compose',0,4.5,s))
# Request and plan share one thread. No task dashboard or invented initiative approval.
s=sender('You',401,247)+t('Get Thursday’s webinar ready.',483,339,39,500)+t('Signup page + invite. Drafts only.',483,390,36)+r(483,419,373,58,'#F3EFE6',9)+t('Session brief',510,458,28,550)
s+=g('plan-block',sender('Kite',401,529,'#FF6D2D')+t('I’ll use the brief to:',483,619,39,500))
for i,v in enumerate(['Pull out the session details','Build the signup-page draft','Write the invitation for your review']):
 s+=g(f'plan-step-{i}',circ(502,676+i*67,18,'#F5E1D2')+t(str(i+1),502,685+i*67,22,650,anchor='middle')+t(v,542,689+i*67,33,450))
states.append(('plan',4.5,10,s))
# Attachment: the details below must survive into both drafts.
s=r(428,243,1320,604,'#FAF8F3',16,'#DAD3C7')+t('Session brief',470,310,40,650)+rule(470,342,1705,342)
s+=t('A better first week',470,424,64,600)+t('A practical onboarding session for team leads.',470,482,32,c='#57564C')
s+=g('brief-details',r(470,528,550,81,'#E8EEE4',12)+t('Thursday · 2 PM UTC',745,580,34,550,'#24443E','middle')+t('What we’ll cover',470,669,29,600)+t('Clear owners. A simple onboarding checklist.',470,723,36,500))
s+=t('Source supplied with the request',470,802,24,400,'#666156')
states.append(('brief',10,14,s))
# Result arrives as the documented website draft card.
s=sender('Kite',401,247,'#FF6D2D')+t('The signup-page draft is here.',483,338,40,500)
s+=r(483,382,1190,425,'#F0F5EF',14,'#CDD9CE')+t('WEBINAR',525,440,24,650,'#3B655B')+t('A better first week.',525,519,66,600,'#173F36')+t('Thursday · 2 PM UTC',525,577,32,500,'#345C52')+t('Clear owners. A simple onboarding checklist.',525,629,31,c='#345C52')+button('Preview',525,690,176)+button('Review',723,690,176)
states.append(('page-card',14,16.5,s))
# Concrete page preview. Intentional full product view inside the context of Slack.
s=t('Website draft · preview',412,248,24,500,'#625D54')+r(412,272,1360,587,'#EBF1E7',17)
s+=t('Sample company',458,320,25,600,'#365D50')+rule(458,346,1726,346,'#B9CABC')
s+=g('web-hero',t('A better',458,465,83,600,'#173F36')+t('first week.',458,558,83,600,'#173F36')+t('Onboarding that starts with a clear plan.',460,624,30,400,'#345C52')+r(458,674,348,70,'#173F36',35)+t('Reserve your seat',632,719,29,600,'#FFF','middle'))
s+=g('web-agenda',r(1130,385,593,398,'#FFF',17)+t('THURSDAY · 2 PM UTC',1175,442,27,600,'#345C52')+t('For team leads',1175,502,40,550,'#173F36')+rule(1175,535,1680,535,'#D3DDD1')+t('01',1175,594,25,600,'#527368')+t('Set clear owners',1234,594,31,500,'#173F36')+t('02',1175,653,25,600,'#527368')+t('Build a simple checklist',1234,653,31,500,'#173F36')+t('03',1175,712,25,600,'#527368')+t('Make the next step obvious',1234,712,29,500,'#173F36'))
states.append(('web-preview',16.5,21,s))
# Copy arrives as text, as documented; not an invented email-client integration.
s=sender('Kite',401,244,'#FF6D2D')+t('And the invitation draft:',483,331,38,500)
s+=r(483,372,1245,453,'#FCFAF5',15,'#DDD6C8')+t('SUBJECT',526,426,23,600,'#665C4C')+t('Thursday: a better first week',526,490,44,550)
s+=rule(526,528,1680,528)+t('Give new teammates a clearer start.',526,594,34,500)+t('Join our practical session for team leads:',526,648,33)+t('clear owners, a simple checklist, and the next step.',526,701,32)+t('Thursday · 2 PM UTC',526,769,29,600,'#345C52')
states.append(('invitation',21,27,s))
# Human review and a visible revision. No send/publish action is depicted.
s=sender('You',401,252)+t('Make the invite more practical.',483,343,43,500)+t('Lead with the checklist.',483,404,43,550)
s+=g('revision-result',sender('Kite',401,490,'#FF6D2D')+r(483,571,1245,248,'#FCFAF5',14,'#DDD6C8')+t('REVISED SUBJECT',526,631,23,650,'#665C4C')+g('revised-copy',r(516,655,1145,85,'#FBE7D5',11)+t('Your first-week onboarding checklist',538,714,43,600))+t('Thursday · 2 PM UTC',526,784,28,500,'#345C52'))
states.append(('review',27,32,s))
# Both requested outputs return to the thread. Editorial state qualifier is outside product UI.
s=sender('Kite',401,244,'#FF6D2D')+t('Both drafts are in this thread.',483,330,39,550)
s+=g('final-page',r(483,368,1245,205,'#F0F5EF',13,'#CDD9CE')+t('Signup page',522,421,27,650,'#345C52')+t('A better first week.',522,484,43,600,'#173F36')+button('Preview',1305,466,165)+button('Review',1490,466,165))
s+=g('final-invite',r(483,595,1245,217,'#FCFAF5',13,'#DDD6C8')+t('Invitation draft',522,648,27,650,'#665C4C')+t('Your first-week onboarding checklist',522,709,42,550)+t('Thursday · 2 PM UTC',522,766,28,500,'#345C52'))
states.append(('together',32,35,s))

# Single workflow scene with state groups, one registered paused timeline.
body='<section id="workflow" class="clip" data-start="0" data-duration="35" data-track-index="0">'+svg(shell+''.join(g(id,s) for id,a,b,s in states))+'</section>'
# Adapted registry simulated-cursor path, no decorative glow. Timed separately; transforms on child.
cursor='<div id="pointer" class="pointer"><div id="click-ring"></div><svg viewBox="0 0 24 24" width="44" height="44"><path d="M3 2.8 20.6 14 12.8 15.5 9 22 3 2.8Z" fill="#151513" stroke="#FFF" stroke-width="1.4"/></svg></div>'
body+='<div id="cursor-layer" class="clip" data-start="14.4" data-duration="2.1" data-track-index="2">'+cursor+'</div>'
s=r(0,0,1920,1080,'#FFF')+g('end-brand','<image href="assets/kite-wordmark.png" x="635" y="88" width="650" height="387"/>')+g('end-copy',t('What’s next on your list?',960,601,72,550,anchor='middle')+r(640,694,640,103,'#FF6D2D',52)+t('Add Kite to Slack',960,761,42,600,anchor='middle'))+r(0,1019,1920,61,'#FF6D2D')
body+='<section id="ending" class="clip" data-start="35" data-duration="4" data-track-index="0">'+svg(s)+'</section>'
for i,c in enumerate(json.loads((P/'captions.json').read_text())):
 body+=f'<div id="caption-{i}" class="clip caption-layer" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="3"><div class="caption">{html.escape(c["text"])}</div></div>'
body+='<audio id="narration" src="assets/voice.wav" data-start="0" data-duration="39" data-track-index="4" data-volume="1"></audio><audio id="music-bed" src="assets/music.wav" data-start="0" data-duration="39" data-track-index="5" data-volume="0.75"></audio><audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="39" data-track-index="6" data-volume="0.6"></audio>'
css='''@font-face{font-family:Onest;src:url('assets/Onest.woff2') format('woff2');font-weight:100 900}*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#F6F3ED}#root{position:relative;width:100%;height:100%;font-family:Onest,sans-serif}.clip{position:absolute;inset:0;width:100%;height:100%}svg{display:block;font-family:Onest,sans-serif}.caption-layer{display:flex;align-items:flex-end;justify-content:center;padding-bottom:28px}.caption{padding:15px 29px;background:#151513;color:#FFFFFF;font-size:31px;font-weight:500;line-height:39px;border-radius:35px}.pointer{position:absolute;left:0;top:0;width:44px;height:44px;pointer-events:none}#click-ring{position:absolute;left:4px;top:4px;width:26px;height:26px;border:2px solid #151513;border-radius:50%;opacity:0}'''
js='const tl=gsap.timeline({paused:true});\n'
for id,a,b,s in states:
 if a==0:js+=f"tl.set('#{id}',{{opacity:1}},0);\n"
 else:js+=f"tl.fromTo('#{id}',{{opacity:0,y:16}},{{opacity:1,y:0,duration:.32,ease:'power2.out'}},{a});\n"
 if b<35:js+=f"tl.to('#{id}',{{opacity:0,y:-9,duration:.20,ease:'power2.in'}},{b-.20});\n"
# The exact characters derive from seek time, not a wall clock or callback accumulation.
js+="""const a='Kite, get Thursday’s webinar ready.',b='Signup page + invite. Drafts only.';
function typeRequest(){const q=tl.time();document.getElementById('typed-a').textContent=a.slice(0,Math.max(0,Math.floor((q-.15)*27)));document.getElementById('typed-b').textContent=b.slice(0,Math.max(0,Math.floor((q-1.45)*27)));}
tl.eventCallback('onUpdate',typeRequest);typeRequest();
tl.fromTo('#request-send',{opacity:.25},{opacity:1,duration:.3},2.8);
tl.to('#request-send',{scale:.94,svgOrigin:'1698 678',duration:.1,yoyo:true,repeat:1},3.9);
tl.fromTo('#plan-block',{opacity:0,y:14},{opacity:1,y:0,duration:.35},5.1);
for(let i=0;i<3;i++)tl.fromTo('#plan-step-'+i,{opacity:0,x:20},{opacity:1,x:0,duration:.35,ease:'power2.out'},5.8+i*.9);
tl.fromTo('#brief-details',{opacity:0,y:12},{opacity:1,y:0,duration:.4},10.7);
tl.fromTo('#pointer',{opacity:0,x:1050,y:810},{opacity:1,x:568,y:711,duration:.70,ease:'power2.inOut'},14.65);
tl.fromTo('#click-ring',{opacity:.8,scale:.3},{opacity:0,scale:1.8,duration:.32,ease:'power2.out'},15.75);
tl.to('#pointer',{opacity:0,duration:.15},16.28);
tl.fromTo('#web-hero',{opacity:0,x:-25},{opacity:1,x:0,duration:.5,ease:'power2.out'},16.6);
tl.fromTo('#web-agenda',{opacity:0,x:28},{opacity:1,x:0,duration:.5,ease:'power2.out'},17.5);
tl.fromTo('#revision-result',{opacity:0,y:20},{opacity:1,y:0,duration:.45,ease:'power2.out'},29.3);
tl.fromTo('#revised-copy',{opacity:0},{opacity:1,duration:.45},30.05);
tl.fromTo('#final-page',{opacity:0,y:16},{opacity:1,y:0,duration:.4},32.15);
tl.fromTo('#final-invite',{opacity:0,y:16},{opacity:1,y:0,duration:.4},32.65);
tl.fromTo('#end-brand',{opacity:0,y:22},{opacity:1,y:0,duration:.5,ease:'power2.out'},35);
tl.fromTo('#end-copy',{opacity:0,y:18},{opacity:1,y:0,duration:.5,ease:'power2.out'},35.35);
window.__timelines=window.__timelines||{};window.__timelines['kite-webinar']=tl;
"""
(P/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Kite — The webinar request</title><script src="assets/gsap.min.js"></script><style>'+css+'</style></head><body><main id="root" data-composition-id="kite-webinar" data-width="1920" data-height="1080" data-duration="39" data-fps="30">'+body+'</main><script>'+js+'</script></body></html>')
(P/'copy.json').write_text(json.dumps({'states':[{'id':i,'start':a,'end':b} for i,a,b,s in states],'voiceover':json.loads((P/'captions.json').read_text()),'labels':['Illustrative workflow','Sample company'],'product':'Illustrative reconstruction; copy and geometry proposed, documented Preview/Review and thread revision behavior.','publication':'None; the task explicitly requests drafts only.'},indent=2,ensure_ascii=False))
print('Built original 39-second screen-led film.')
