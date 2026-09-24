"""Refresh existing evidence while counting mirrored queue requests only once."""
import json
from pathlib import Path
from amarillo import learning
root=Path(__file__).resolve().parents[2];artifacts=root/'artifacts'
original_collect=learning.collect_experiments
removed=[]
def collect_once(path):
 rows=original_collect(path);ledgers={}
 for p in Path(path).glob('library-loop*/budget.json'):ledgers[p.parent.name]=json.loads(p.read_text())['runs']
 unique={}
 for row in rows:
  folder=row['key'].split('/')[0];request=ledgers[folder][row['id']].get('queue',{}).get('request_id')
  key=('queue',request) if request else ('row',row['key'])
  previous=unique.get(key)
  if previous is None:unique[key]=row
  else:
   # Prefer the original record with local decoded evidence over a budget-only mirror.
   if row['verified_output'] and not previous['verified_output']:
    removed.append(previous['key']);unique[key]=row
   else:removed.append(row['key'])
 return list(unique.values())
learning.collect_experiments=collect_once
result=learning.save_learning(artifacts)
(root/'review_notes/computer-movement-long-learning-refresh.json').write_text(json.dumps({'deduplication':'Same persisted provider queue request ID counted once; separately submitted attempts remain separate.','budget_ledgers_modified':False,'duplicate_mirror_rows_excluded':removed,'unique_video_attempts':len(result['runs']),'new_longer_runs':[{'id':r['id'],'decision':r['decision']} for r in result['runs'] if '-computer-sequence-' in r['id']]},indent=2)+'\n')
print('Saved',len(result['runs']),'unique video attempts;',len(removed),'budget mirror rows excluded.')
