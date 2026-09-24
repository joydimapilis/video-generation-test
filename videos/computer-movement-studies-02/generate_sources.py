"""Resume-safe source generation; shares video ledger, excluded from video routing."""
import json,sys,time,urllib.request
from pathlib import Path
sys.path[:0]=['src','scripts']
from amarillo.budget import BudgetLedger
from run_library_loop import request
plan=json.loads(Path('videos/computer-movement-studies-02/source-image-plan.json').read_text())
ledger=BudgetLedger(Path(plan['budget_root'])/'budget.json')
for run in plan['runs']:
 payload={'kind':'source_image','provider':'fal','image_endpoint':run['endpoint'],'image_input':run['input'],'output_path':run['output_path']}
 if ledger.reserve(run['id'],run['estimate_cents'],payload):
  try:
   q=request('https://queue.fal.run/'+run['endpoint'],run['input'])
   ledger.update(run['id'],status='submitted',queue=q,submitted_at=time.time())
   print(run['id'],'submitted',q['request_id'],flush=True)
  except Exception as e:
   ledger.update(run['id'],status='submission_unknown',error=str(e));raise
pending={r['id']:r for r in plan['runs'] if ledger.read()['runs'][r['id']]['status'] in ['submitted','running','generated']}
end=time.monotonic()+600
while pending and time.monotonic()<end:
 for ident,run in list(pending.items()):
  row=ledger.read()['runs'][ident]
  if row['status']!='generated':
   status=request(row['queue']['status_url'])
   if status['status']!='COMPLETED':continue
   result=request(row['queue']['response_url'])
   ledger.update(ident,status='generated',result=result)
  else:result=row['result']
  urllib.request.urlretrieve(result['images'][0]['url'],run['output_path'])
  ledger.update(ident,status='completed',output_path=run['output_path'])
  print(ident,'completed',run['output_path'],flush=True);del pending[ident]
 if pending:time.sleep(5)
print('Remaining:',list(pending),flush=True)
