"""Build Kite's static review package; never renders or submits a paid generation."""
from pathlib import Path
import base64
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'videos/kite'
OUT = ROOT / 'artifacts/kite'
OUT.mkdir(parents=True, exist_ok=True)
(P / 'compositions/frames').mkdir(parents=True, exist_ok=True)
(P / 'assets').mkdir(exist_ok=True)
shutil.copy(P / 'capture/assets/fonts/ef79401ea952b7f0-s.0t4d9turf_6_x.woff2', P / 'assets/Onest.woff2')
shutil.copy(ROOT / 'videos/fold/assets/gsap.min.js', P / 'assets/gsap.min.js')
FONT = base64.b64encode((P / 'assets/Onest.woff2').read_bytes()).decode()
LOGO = base64.b64encode((P / '.media/images/logo_001.png').read_bytes()).decode()

VO = [
 (0,6,'A launch needs more than a caption. It needs the work around it to move.'),
 (6,13,'In your company Slack, give me the job.'),
 (13,21,'I start with a plan: what I will look at, what I will prepare, and what I need you to decide.'),
 (21,31,'Then I research the business and prepare reviewable marketing work, such as a product page, announcement, walkthrough, and email.'),
 (31,37,'When a public change is ready, you approve it.'),
 (37,42,'I’m Kite, the AI marketer in Slack. Add me to your team.'),
]
CUES = [
 (0,2.7,'A launch needs more than a caption.'),
 (2.7,6,'It needs the work around it to move.'),
 (6,9.5,'In your company Slack,'), (9.5,13,'give me the job.'),
 (13,15,'I start with a plan:'), (15,17,'what I will look at,'),
 (17,19,'what I will prepare,'), (19,21,'and what I need you to decide.'),
 (21,23.5,'Then I research the business'), (23.5,27,'and prepare reviewable marketing work,'),
 (27,29,'such as a product page, announcement,'), (29,31,'walkthrough, and email.'),
 (31,34.5,'When a public change is ready,'), (34.5,37,'you approve it.'),
 (37,40.1,'I’m Kite, the AI marketer in Slack.'), (40.1,42,'Add me to your team.'),
]
FRAMES = [
 ('The work around it',0,3,1.5,'Four work cards accumulate; one request has several outputs.','Stack labels remain readable; reflow begins at 3s.',0),
 ('One conversation',3,6,5,'The four surfaces consolidate into one Slack thread.','Hold the resulting thread geometry into the request.',0),
 ('Ask in Slack',6,13,10,'A single illustrative request occupies the thread.','Request settles, then Kite replies at 13s.',1),
 ('Plan: inputs and outputs',13,17,16,'Plan response highlights its inputs and the work to prepare.','Same plan stays visible; attention moves to decision.',2),
 ('Plan: your decision',17,21,20,'The public-change decision is emphasized before work begins.','Replace plan body with research in the same panel.',2),
 ('Research to review',21,27,25,'Source, caveat and a review-ready state stay together.','Four draft tiles emerge from the review card.',3),
 ('Four drafts, one review',27,31,29,'Four output examples return to the conversation.','Recombine into one review card at 30.4s.',3),
 ('Approval stays with you',31,37,35,'Propose first mode; a decision reply is drafted but not sent.','Never show publish success; thread retires at 37s.',4),
 ('Add Kite to Slack',37,42,40.5,'Official wordmark, category and one CTA hold.','Settle by 37.5s; complete lockup holds to 42s.',5),
]

def esc(s): return html.escape(str(s), quote=True)
def text(s,x,y,size=34,weight=400,fill='#0E0E0E',anchor='start'):
 return f'<text data-required="true" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'
def rect(x,y,w,h,fill='#FFFFFF',stroke='#D9D9D9',rx=14):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def label(): return text('Illustrative workflow',108,718,28,500)+text('Sample company',972,718,28,500,anchor='end')
def head(lines):
 return ''.join(text(line,108,790+i*58,54 if len(lines)>1 else 58,600) for i,line in enumerate(lines))
def panel(y=820,h=290):
 return rect(108,y,864,h)+text('# marketing',140,y+43,29,600)+f'<path d="M108 {y+60} H972" stroke="#D9D9D9" stroke-width="2"/>'
def pill(s,x,y,w): return rect(x,y,w,48,'#FF6D2D','#FF6D2D',24)+text(s,x+w/2,y+33,28,600,anchor='middle')

def svg(n):
 a=['<rect width="1080" height="1920" fill="#FFFFFF"/>']
 a.append('<path d="M108 400 H972 M108 1520 H972" stroke="#ECECEC" stroke-width="2"/>')
 if n<8:a.append(label())
 if n in [0,1]:
  a.append(head(['One request.','The work around it.']))
  if n==0:
   for i,s in enumerate(['Product page','Announcement','Walkthrough','Email']):
    x=108+i*24;y=870+i*48
    a.extend([rect(x,y,788,60,'#FFF5EE'),text(s,x+22,y+38,34,500)])
  else:
   a.extend([panel(875,195),text('You',140,974,30,600),text('Message Kite',140,1025,38,400,'#535353')])
 elif n==2:
  a.extend([head(['Ask in Slack']),panel(),text('You',140,935,31,600),text('Kite, help us prepare',140,991,42,500),text('the launch.',140,1045,42,500)])
 elif n in [3,4]:
  a.extend([head(['Plan first']),panel(820,310),text('Kite',140,913,30,600)])
  rows=[('Inputs','Website and launch brief'),('Prepare','Product page, announcement,'),('Decide','Approve public changes')]
  for i,(k,v) in enumerate(rows):
   y=[957,1007,1099][i]
   if i==(2 if n==4 else 0):a.append(rect(127,y-32,826,44,'#FFF0E5','#FFF0E5',5))
   a.extend([text(k,140,y,30,600),text(v,300,y,32)])
   if i==1:a.append(text('walkthrough, email',300,1048,32))
 elif n==5:
  a.extend([head(['Reviewable work,','in the conversation']),rect(108,860,864,270),text('Kite · Research summary',140,905,32,600),text('Source: sample launch brief',140,949,31),text('Confirm audience and launch date.',140,992,33),text('Illustrative inputs; not verified findings.',140,1034,29,400,'#535353'),pill('Prepared for review',140,1063,326)])
 elif n==6:
  a.append(head(['Reviewable work,','in the conversation']))
  for i,s in enumerate(['Product page','Announcement','Walkthrough','Email']):
   x=108+(i%2)*440;y=862+(i//2)*86
   a.extend([rect(x,y,424,72,'#FFF5EE'),text(s,x+22,y+47,34,500)])
  a.append(pill('Prepared for review',377,1063,326))
 elif n==7:
  a.extend([head(['Public changes stay with you.']),panel(820,310),text('Propose first',942,863,28,500,anchor='end'),text('Kite · Ready for your review',140,925,34,600),text('Not published',140,970,31,600),text('Your decision',140,1016,28,500),rect(132,1031,816,57,'#FAFAFA'),text('Approve the product page.',151,1070,34),text('Draft reply — not sent',942,1117,26,400,'#535353',anchor='end')])
 else:
  a.extend([f'<image data-required="true" href="data:image/png;base64,{LOGO}" x="250" y="690" width="580" height="346"/>',text('AI marketer in Slack',540,1040,47,500,anchor='middle'),rect(281,1070,518,75,'#FF6D2D','#FF6D2D',38),text('Add Kite to Slack',540,1120,42,600,anchor='middle')])
 sample=next(c[2] for c in CUES if c[0]<=FRAMES[n][3]<c[1])
 # Every preview shows an actual verbatim subtitle cue. Timing will follow TTS.
 a.extend([rect(108,1160,864,62,'#0E0E0E','#0E0E0E',10),text(sample,540,1201,32,500,'#FFFFFF','middle')])
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920" role="img" aria-label="'+esc(FRAMES[n][0])+'">'+''.join(a)+'</svg>'

style=f"@font-face{{font-family:Onest;src:url(data:font/woff2;base64,{FONT}) format('woff2');font-weight:100 900}}svg{{font-family:Onest,sans-serif;display:block}}"
sketches=[svg(n) for n in range(9)]
story=['---\nformat: 1080x1920\nduration: 42s\nmessage: "Ask, plan, review — public changes remain subject to your decision in Propose first mode"\narc: "Ask → Plan → Reviewable work → Approval"\naudience: "Marketing buyers who want work to stay in Slack"\nmode: collaborative\nmusic: quiet modern pulse and soft percussion\n---\n\n# Nine-frame storyboard\n\nStatic proposal, not approved or animated. Nine keyframes represent seven shots. Approval covers this board and COPY.md. All supplemental UI labels and behaviors remain proposed; PRODUCT_VERIFICATION.md must be completed before final rendering. Review exact crop views in review.html.\n']
hosts=[]
for n,(title,start,end,at,scene,transition,vi) in enumerate(FRAMES):
 ident=f'kite-{n+1:02}'
 filename=f'{n+1:02}-sketch.html'
 comp=f'<template><style>{style}#{ident}{{width:100%;height:100%;overflow:hidden}}</style><div id="{ident}" data-composition-id="{ident}" data-width="1080" data-height="1920" data-duration="{end-start}">{sketches[n]}</div><script>window.__timelines["{ident}"]=gsap.timeline({{paused:true}});</script></template>'
 (P/'compositions/frames'/filename).write_text(comp)
 story.append(f'## Frame {n+1} — {title}\n\n- scene: {scene}\n- duration: {end-start}s\n- timestamp: {start:02d}–{end:02d}s\n- poster: 0\n- transition_in: cut\n- status: outline\n- sketch_ready: yes\n- approval: pending\n- src: compositions/frames/{filename}\n- voiceover: "{VO[vi][2]}"\n- asset_candidates: '+('assets/Onest.woff2 — captured official typography; .media/images/logo_001.png — official newsroom wordmark' if n==8 else 'assets/Onest.woff2 — captured official typography; original deterministic sample UI')+f'\n\nNarrative role: {scene}\n\nTransition intention: {transition}\n\nLayout: essential content x108–972, y690–1230; caption y1160–1222. No people. Actual keyframe shown at {at}s. Captions and all UI text are listed in COPY.md.\n')
 hosts.append(f'<div id="{ident}-host" class="clip" data-start="{start}" data-duration="{end-start}" data-composition-id="{ident}" data-composition-src="compositions/frames/{filename}" data-track-index="0"></div>')
(P/'STORYBOARD.md').write_text('\n'.join(story))
(P/'index.html').write_text('<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>html,body{margin:0;width:1080px;height:1920px;overflow:hidden}#root{width:100%;height:100%}.clip{position:absolute;inset:0}</style></head><body><div id="root" data-composition-id="kite-board" data-width="1080" data-height="1920" data-duration="42">'+''.join(hosts)+'</div><script>window.__timelines["kite-board"]=gsap.timeline({paused:true});</script></body></html>')
script=['# SCRIPT — Kite: Ask, plan, review\n\n**Voice:** Proposed local Kokoro af_heart; not generated.\n\n**Voice direction:** Calm and matter-of-fact. Exact supplied wording, no added claims.\n']
for i,(s,e,line) in enumerate(VO):script.append(f'## Line {i+1}\n\n**Time:** {s}–{e}s\n\n**Delivery:** Clear natural phrasing; respect the prescribed shot window.\n\n    {line}\n')
(P/'SCRIPT.md').write_text('\n'.join(script))
copy=[(P/'COPY_REVIEW_POLICY.md').read_text().rstrip()+'\n\nVerification evidence and outstanding checks: [PRODUCT_VERIFICATION.md](PRODUCT_VERIFICATION.md).\n\n## Spoken voiceover\n']
copy+= [f'- **{s:02d}–{e:02d}s:** {v}' for s,e,v in VO]
copy+=['\n## Burned-in captions\n\nVerbatim phrase groups. Times are planning guides; final synchronization must use measured speech. Every word in the voiceover occurs exactly once below.\n']
copy += [f'- **{s:g}–{e:g}s:** {v}' for s,e,v in CUES]
copy+=['\n## Screen text, labels and CTA\n\nThe following is an exhaustive per-frame inventory extracted from the sketches. Repeated strings remain repeated here to make the screen review literal. Official logo artwork reads Kite. No destination URL, performance number, customer name or testimonial is shown.\n']
import re
for n,s in enumerate(sketches):
 strings=[html.unescape(t) for t in re.findall(r'<text[^>]*>(.*?)</text>',s)]
 copy.append(f'### Frame {n+1} — {FRAMES[n][0]}\n\n'+'\n'.join('- '+x for x in strings))
copy.append('\n## Source of the fictional research input\n\nThe sample launch brief consists only of the supplied request and four deliverable types. Audience and launch date are unspecified; the research card asks to confirm them. These are gaps, not external business findings.\n\n## Review-only material\n\nPage titles, shot timestamps, crop controls, explanatory notes and approval checklist live outside the video frames and are not burned in.\n\n## Approval needed\n\nApprove the nine-frame creative direction and the verbatim voiceover/headline copy.\n\nBefore final rendering:\n\n* Confirm the campaign CTA destination.\n* Verify whether the illustrated review/approval UI reflects the current Kite product experience.\n* Confirm or replace proposed UI labels such as “Propose first,” “Prepared for review,” “Ready for your review,” “Not published,” and “Draft reply — not sent.”\n* Confirm that the approval interaction shown does not imply that anything has already been published.\n* Replace any proposed UI behavior that differs from the current product with an accurate reconstruction.\n')
(P/'COPY.md').write_text('\n'.join(copy))
data={'version':1,'status':'pending_product_verification_and_storyboard_copy_approval','product_verification':{'status':'incomplete','evidence':'PRODUCT_VERIFICATION.md','policy':'COPY_REVIEW_POLICY.md','final_render_ready':False},'duration_seconds':42,'width':1080,'height':1920,'shots':7,'keyframes':9,'voiceover':[{'start':s,'end':e,'text':v} for s,e,v in VO],'captions':[{'start':s,'end':e,'text':v} for s,e,v in CUES],'frames':[{'index':i+1,'title':f[0],'start':f[1],'end':f[2],'key_time':f[3]} for i,f in enumerate(FRAMES)]}
(P/'storyboard.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
ledger=P/'budget.json'
if not ledger.exists():ledger.write_text(json.dumps({'currency':'USD','cap':10,'committed_generation_cost':0,'reserved':0,'remaining':10,'jobs':[],'planned_routes':{'S1-S7':'HyperFrames local deterministic UI','narration':'local Kokoro, pending','music':'local deterministic synthesis, pending'},'note':'No paid generation. Local compute excluded.'},indent=2)+'\n')

cards=[]
for n,f in enumerate(FRAMES):
 cards.append(f'<article><div class="meta">FRAME {n+1:02} <span>{f[1]:02}–{f[2]:02}s</span></div><h2>{esc(f[0])}</h2><div class="viewport"><div class="canvas">{sketches[n]}</div></div><p>{esc(f[4])}</p><p class="motion">{esc(f[5])}</p><details><summary>Voiceover · {VO[f[6]][0]}–{VO[f[6]][1]}s</summary><p>{esc(VO[f[6]][2])}</p></details></article>')
review='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kite — nine-frame storyboard review</title><style>'''+style+'''
*{box-sizing:border-box}body{margin:0;background:#f1f0ee;color:#181818;font-family:Onest,sans-serif}header,main,footer{max-width:1500px;margin:auto;padding:35px 42px}header{padding-bottom:12px}.kicker{font-size:12px;font-weight:700;letter-spacing:.14em;color:#8f350e}h1{font-size:42px;letter-spacing:-.05em;margin:12px 0}header p{max-width:850px;line-height:1.6}nav{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0}button,a.button{padding:10px 17px;border:1px solid #bbb;border-radius:30px;background:transparent;color:#181818;cursor:pointer;font:inherit;font-size:13px;text-decoration:none}button.active{background:#181818;color:white;border-color:#181818}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}article{min-width:0;border-top:1px solid #aaa;padding-top:16px}.meta{font-size:11px;letter-spacing:.12em;display:flex;justify-content:space-between}h2{font-size:20px;letter-spacing:-.03em;margin:12px 0 18px}.viewport{position:relative;width:100%;overflow:hidden;background:white;aspect-ratio:9/16;border:1px solid #ddd}.canvas{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:top left}.canvas svg{width:1080px;height:1920px}.square .viewport{aspect-ratio:1}.wide .viewport{aspect-ratio:16/9}article p{font-size:13px;line-height:1.6;margin:12px 0 6px}.motion{color:#666}summary{cursor:pointer;font-size:12px;margin-top:15px}footer{font-size:13px;line-height:1.7}a{color:#8f350e}#notice{font-size:12px;color:#555}.guides .canvas:after{content:"";position:absolute;left:108px;top:690px;width:864px;height:540px;border:3px dashed #2881C1;pointer-events:none}.guides .canvas:before{content:"";position:absolute;left:0;top:656.25px;width:1080px;height:607.5px;border-block:3px dashed #FF6D2D;pointer-events:none}@media(max-width:900px){.grid{grid-template-columns:1fr}header,main,footer{padding:22px}.viewport{max-width:540px}h1{font-size:32px}}@media print{nav,details{display:none}header,main,footer{padding:15px}h1{font-size:28px}.grid{gap:12px}article{break-inside:avoid}article p{font-size:10px}h2{font-size:14px}body{background:white}}
</style></head><body class="wide"><header><div class="kicker">KITE / CONCEPT 02 / PREPRODUCTION</div><h1>Ask, plan, review.</h1><p>A 42-second screen-led film. Nine keyframes, seven shots, exact supplied narration. These are static composition sketches for approval; no final motion or audio has been generated.</p><p><strong>Product verification pending.</strong> All supplemental UI labels and behaviors are proposed. This includes Propose first, Prepared for review, Ready for your review, Not published, and the decision reply. Verify them against the current product before final rendering; replace any mismatch while preserving the brief’s message. Nothing may imply a public action was sent or published. <a href="PRODUCT_VERIFICATION.md">See verification record.</a></p><nav><button data-mode="portrait">9:16 master</button><button data-mode="square">1:1 crop</button><button class="active" data-mode="wide">16:9 crop</button><button id="guides">Show safe guides</button><a class="button" href="COPY.md">Exact copy</a><a class="button" href="PRODUCTION_PLAN.md">Production plan & references</a></nav><p id="notice">Centered 16:9 crop: the same artwork, with no text repositioning. Switch to 9:16 to see the full composition. No approval is implied by viewing this board.</p></header><main class="grid">'''+''.join(cards)+'''</main><footer><strong>Approval needed</strong><p>Approve the nine-frame creative direction and the verbatim voiceover/headline copy.</p><p>Before final rendering:</p><ul><li>Confirm the campaign CTA destination.</li><li>Verify whether the illustrated review/approval UI reflects the current Kite product experience.</li><li>Confirm or replace proposed UI labels such as “Propose first,” “Prepared for review,” “Ready for your review,” “Not published,” and “Draft reply — not sent.”</li><li>Confirm that the approval interaction shown does not imply that anything has already been published.</li><li>Replace any proposed UI behavior that differs from the current product with an accurate reconstruction.</li></ul><p>Brand sources: <a href="https://kite.ai/newsroom">official Kite newsroom</a> and captured Onest from <a href="https://kite.ai/">kite.ai</a>. Approval behavior: <a href="https://docs.kite.ai/slack/approvals">current Kite documentation</a>. Library footage is inspiration only. Spend: $0 / $10.</p><p>All essential content is designed inside x108–972, y690–1230. Static crop geometry can be checked now; final moving crops, voice timing, audio levels and product-owner sign-off remain pending.</p></footer><script>
let mode='wide';function fit(){const y={portrait:0,square:420,wide:656.25}[mode];document.querySelectorAll('.viewport').forEach(v=>{v.querySelector('.canvas').style.transform=`scale(${v.clientWidth/1080}) translateY(-${y}px)`})}document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{mode=b.dataset.mode;document.body.classList.remove('portrait','square','wide');document.body.classList.add(mode);document.querySelectorAll('[data-mode]').forEach(x=>x.classList.toggle('active',x===b));document.getElementById('notice').textContent={portrait:'Full 1080×1920 master. The central composition preserves every important element in both crop checks.',square:'Centered 1080×1080 crop. Same artwork and caption positions.',wide:'Centered 1080×607.5 crop (16:9). Same artwork and caption positions.'}[mode];fit()});document.getElementById('guides').onclick=()=>document.body.classList.toggle('guides');new ResizeObserver(fit).observe(document.querySelector('main'));window.addEventListener('load',fit);document.fonts.ready.then(fit);
</script></body></html>'''
(P/'review.html').write_text(review)
print('Wrote nine sketches, review.html, STORYBOARD.md, SCRIPT.md, COPY.md, storyboard.json and persistent budget.json')
