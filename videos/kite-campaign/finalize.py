"""Deliver only after technical, visual, budget and per-MP4 documentation gates."""
from pathlib import Path
import json,hashlib
from amarillo.delivery import require_reverse_engineering
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
video=R/'artifacts/final_outcome/kite-campaign/kite-campaign.mp4'
tech=json.loads((P/'encoded-technical-checks.json').read_text());review=json.loads((P/'encoded-review.json').read_text());checks=json.loads((P/'check-04.json').read_text());budget=json.loads((P/'budget.json').read_text())
assert checks['ok'] and tech['full_decode_pass'] and review['decision']=='accepted'
assert checks['motion']['enabled'] and checks['contrast']['passed']==checks['contrast']['checked']
assert budget['limit_cents']==1000 and not budget['runs']
doc=require_reverse_engineering(video)
result={'status':'complete','title':'Kite — One brief. A whole campaign.','video':str(video),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration_seconds':36,'resolution':'1920x1080','fps':30,'editable_project':str(P),'brief':str(P/'BRIEF.md'),'production_record':str(P/'kite-campaign.production.json'),'documentation':doc,'technical_checks':tech,'visual_review':review,'budget':{'cap_usd':10,'estimated_provider_cost_usd':0,'reserved_usd':0,'confirmed_provider_charges_usd':0,'paid_requests':0,'ledger':str(P/'budget.json'),'local_compute':'not priced'},'limitations':['Illustrative fictional Relay campaign and authored Slack workflow, not an authenticated Kite execution.','No actual publishing or measured campaign outcomes.','Audio verified numerically and against source, without independent listening.','Human realism and audience effectiveness not tested.'],'reference_review':str(P/'reference-review.json'),'phase2_used':False,'preview':'http://localhost:3077/#project/kite-campaign'}
(R/'assembled_outputs/kite-campaign.json').write_text(json.dumps(result,indent=2))
(R/'review_notes/kite-campaign-final-verification.json').write_text(json.dumps(result,indent=2))
b=P/'BRIEF.md';s=b.read_text().replace('budget_usd: 10','budget_usd: 10\nstatus: complete');b.write_text(s)
print(json.dumps({'status':'complete','video':str(video),'document':doc},indent=2))
