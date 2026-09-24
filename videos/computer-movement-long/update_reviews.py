"""Persist subjective observations into the existing loop scorecards."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
r=json.loads((root/'review_notes/computer-movement-long.json').read_text())
for row in r['runs']:
 p=root/('artifacts/library-loop-computer-long-'+row['run_id'][:2]+'/scorecard.json')
 x=json.loads(p.read_text());x['runs']=[a for a in x['runs'] if a['id']!=row['run_id']]
 x['runs'].append({'id':row['run_id'],'decision':'reject' if row['decision']=='rejected' else 'provisional','scores':{},'review':' '.join(row['observations']+row.get('limitations',[])),'review_method':r['method'],'source_review':'review_notes/computer-movement-long.json'})
 p.write_text(json.dumps(x,indent=2)+'\n')
