"""Rebuild exact generation provenance from persisted submitted payloads."""
from pathlib import Path
import hashlib,json,urllib.request
from datetime import datetime,timezone
p=Path(__file__).resolve().parent; root=p.parents[1]
old=json.loads((root/'review_notes/computer-movement-studies-02-generation-audit.json').read_text())
hist=json.loads((p/'budget-continuity.json').read_text())
assert hashlib.sha256((root/hist['original_ledger']).read_bytes()).hexdigest()==hist['original_sha256']
sources=json.loads((p/'source-reviews.json').read_text())['sources']
records=[]
for source in sources:
 num=source['sample'];path=root/source['file'];sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==source['sha256']
 image=next(x for x in old['all_attempts'] if x.get('output_path')==source['file'] and x['stage']=='text-to-image')
 assert image['input_files']==[]
 ledger=json.loads((root/f'artifacts/library-loop-computer-long-{num}/budget.json').read_text())
 requests=[]
 for rid,row in ledger['runs'].items():
  if '-computer-sequence-' not in rid:continue
  submitted=row['resolved_input'];original=row['payload']['input']
  fields=[k for k,v in submitted.items() if k.endswith('_url') or k in ['elements','image_urls','video_urls','pose','motion_control']]
  expected='image_url' if row['payload']['endpoint'].startswith('wan/') else 'start_image_url'
  assert fields==[expected],fields
  assert original[expected]=='local:'+source['file']
  with urllib.request.urlopen(submitted[expected],timeout=60) as r: remote_sha=hashlib.sha256(r.read()).hexdigest()
  assert remote_sha==sha
  requests.append({'id':rid,'endpoint':row['payload']['endpoint'],'request_id':row['queue']['request_id'],'status':row['status'],'input_files':[{'file':source['file'],'sha256':sha,'field':expected,'uploaded_url':submitted[expected],'uploaded_bytes_match':True}],'submitted_model_input':submitted,'human_reference_video_inputs':[],'human_reference_extracted_frame_inputs':[],'human_reference_first_last_frames':[],'pose_reference_inputs':[],'motion_control_inputs':[],'output_path':row.get('output_path')})
 records.append({'sample':num,'source_image':source,'source_image_generation_request':image,'new_source_image_generated_this_turn':False,'video_requests':requests})
audit={'audited_at_utc':datetime.now(timezone.utc).isoformat(),'basis':'Persisted resolved_input, queue IDs, source-image generation records and remote uploaded-byte SHA256 checks. Not an independent provider-side log.','source_media':'Reused independently generated Nano Banana Pro stills; their original generation inputs were text only.','reference_media_in_generation':False,'real_extracted_frames_used_only_for_local_observation':True,'video_inputs':0,'last_frame_inputs':0,'pose_inputs':0,'motion_control_inputs':0,'original_budget_preserved':True,'samples':records,'selected_samples':json.loads((p/'selection.json').read_text())['samples'],'reference_observations':json.loads((p/'reference-observations.json').read_text())}
(root/'review_notes/computer-movement-long-generation-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
lines=['# Longer computer studies: generation audit','','The longer studies reuse the previously generated stills. Their original image requests were text-only. Each new I2V request received exactly one generated PNG plus text/settings. No real reference video, extracted real frame, last frame, pose or motion-control input was submitted. Uploaded PNG bytes match the original generated files by SHA256. This audit uses local persisted requests, not an independent provider-side log.','']
for rec in records:
 chosen=next(x for x in audit['selected_samples'] if x['name'].startswith(rec['sample']))
 lines += [f'## Sample {rec["sample"]}', '',f'Selected video request: `{chosen["run_id"]}`; delivered range {chosen.get("source_start",0)}–{chosen.get("source_start",0)+chosen["duration"]:g}s.', '',f'Source: `{rec["source_image"]["file"]}`','', 'Original source-image generation prompt:','', '```text',rec['source_image_generation_request']['submitted_model_input']['prompt'],'```','', 'Image generation input files: **none**.','']
 for r in rec['video_requests']:
  lines += [f'### {r["id"]}', '',f'Model: `{r["endpoint"]}`; request ID: `{r["request_id"]}`.', '',f'Only file input: `{r["input_files"][0]["file"]}` in `{r["input_files"][0]["field"]}`.','', '```text',r['submitted_model_input']['prompt'],'```','', 'All submitted settings and the uploaded URL are preserved in the companion JSON. No other media inputs.','']
 lines += ['Movement clips reviewed for inspiration: '+', '.join(audit['reference_observations']['application'][rec['sample']])+'.','']
lines += ['Reference time ranges and observed-versus-hypothesized motion are preserved in `videos/computer-movement-long/reference-observations.json`. Mouse/trackpad choreography is an extrapolation from supported hand movement, not a motion capture or direct copy.']
(root/'review_notes/computer-movement-long-generation-audit.md').write_text('\n'.join(lines)+'\n')
print('Verified',sum(len(x['video_requests']) for x in records),'single-generated-image video requests; no real reference media inputs.')
