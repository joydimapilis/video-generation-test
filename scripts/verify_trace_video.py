"""Verify the delivered Trace MP4, its new source footage, and authored audio mix."""
import hashlib, json, subprocess
from pathlib import Path
import numpy as np
R=Path('artifacts/library-loop-10');P=Path('hyperframes/trace');O=Path('artifacts/final_outcome/trace');V=O/'trace.mp4'
def run(*args):return subprocess.check_output(args)
def pcm(p):return np.frombuffer(run('ffmpeg','-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-'),dtype='<f4').reshape(-1,2)
def frame(p,t,w,h,filters=''):
 filt=(filters+',' if filters else '')+f'scale={w}:{h}'
 return np.frombuffer(run('ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf',filt,'-pix_fmt','rgb24','-f','rawvideo','-'),dtype=np.uint8).reshape(h,w,3).astype(float)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 check=json.loads((R/'check.json').read_text());assert check['ok']
 assert not any(check[k]['findings'] for k in ['lint','runtime','layout','contrast'])
 meta=json.loads(run('ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V)))
 v=next(s for s in meta['streams'] if s['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'24/1')
 assert int(v['nb_frames'])==792 and abs(float(meta['format']['duration'])-33)<.05
 decode=subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr
 b=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.08:pix_th=0.08','-an','-f','null','-'],capture_output=True)
 black=[x for x in b.stderr.decode().splitlines() if 'black_start:' in x];assert not black,black
 actual=pcm(V);expected=sum(pcm(P/'assets'/f) for f in ['voice.wav','score.wav','clicks.wav']);n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n].ravel(),expected[:n].ravel())[0,1]);assert corr>.99,corr
 peak=float(abs(actual).max());assert peak<.9999
 lines=[]
 for line in json.loads((P/'audio-plan.json').read_text())['schedule']:
  a=round(line['start']*48000);z=round((line['start']+line['duration'])*48000)
  c=float(np.corrcoef(actual[a:z].ravel(),expected[a:z].ravel())[0,1]);assert c>.99
  lines.append({'start':line['start'],'text':line['text'],'mix_correlation_at_zero_offset':c})
 source=P/'assets/hands.mp4';provenance=json.loads((P/'sources.json').read_text());assert digest(source)==provenance[0]['sha256']==digest(provenance[0]['source'])
 assert provenance[0]['source'].startswith('artifacts/library-loop-10/outputs/')
 # Actual render's crop compared to decoded source at declared source offset.
 hand=[]
 for at in [7.0,8.0,9.0]:
  actualframe=frame(V,at,530,400,'crop=1060:800:860:200')
  src=frame(source,at-6.5+1,530,400,'scale=1400:800,crop=1060:800:170:0')
  mae=float(abs(actualframe-src).mean());assert mae<9,(at,mae)
  hand.append({'timeline_time':at,'source_time':at-6.5+1,'mae_255':mae})
 # Boundary regression checks from encoded pixels: no hand bleed and no empty CTA cut.
 entry=frame(V,9.5,1920,1080)
 bleed_error=float(abs(entry[300:900,1780:1900]-np.array([8,15,34])).mean());assert bleed_error<3,bleed_error
 join_error=float(abs(frame(V,27,960,540)-frame(V,26.95,960,540)).mean());assert join_error<4,join_error
 end_a=frame(V,31.5,960,540);end_b=frame(V,32.95,960,540);end_diff=float(abs(end_a-end_b).mean());assert end_diff<1
 budget=json.loads((R/'budget.json').read_text());estimated=sum(x['estimate_cents'] for x in budget['runs'].values());reserved=sum(x['reserved_cents'] for x in budget['runs'].values());assert reserved<=budget['limit_cents']==1000
 assert all(x['status']=='completed' for x in budget['runs'].values())
 result={'path':str(V),'duration_seconds':33,'dimensions':[1920,1080],'fps':24,'frames':792,'sha256':digest(V),'composition_sha256':digest(P/'index.html'),'cut_checks':{'hand_bleed_background_mae_255':bleed_error,'report_to_cta_entry_mae_255':join_error},'bytes':V.stat().st_size,'full_decode':True,'black_intervals':black,'audio_peak':peak,'audio_mix_correlation':corr,'narration':lines,'generated_source_timing':hand,'end_hold_frame_difference_mae_255':end_diff,'composition_checks':{'lint':0,'runtime':0,'layout':0,'contrast_passed':check['contrast']['passed'],'contrast_total':check['contrast']['checked'],'motion_note':'check motion audit disabled by CLI; separate keyframes, cursor geometry and sampled frames reviewed'},'budget':{'estimate_cents':estimated,'reserved_cents':reserved,'cap_cents':1000,'completed_requests':len(budget['runs'])},'limitations':['Qualitative sampled visual review, not an exhaustive motion or audience test.','No independent listening test. Local narration mix alignment verified numerically.','Selected generated plate is 1344x768, cropped into a 1060x800 region; authored output is 1920x1080.']}
 for path in [R/'delivery-verification.json',O/'verification.json']:path.write_text(json.dumps(result,indent=2)+'\n')
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf','fps=12/33,scale=480:270,tile=4x3','-frames:v','1',str(O/'trace-frames.jpg'))
 run('ffmpeg','-v','error','-y','-ss','4.8','-i',str(V),'-frames:v','1',str(O/'trace-poster.jpg'))
 # Short seam filmstrips from encoded frames, not preview DOM.
 times=[2.95,3.1,3.25,6.45,6.5,6.6,9.45,9.5,9.7,18.25,18.4,18.65,26.95,27.0,27.2,27.6]
 indices=[round(t*24) for t in times]
 selection='+'.join(f'eq(n\\,{n})' for n in indices)
 run('ffmpeg','-v','error','-y','-i',str(V),'-vf',f'select={selection},scale=480:270,tile=4x4','-frames:v','1',str(O/'trace-transitions.jpg'))
 (O/'transition-times.json').write_text(json.dumps({'order':'left-to-right, top-to-bottom','times':[n/24 for n in indices]},indent=2)+'\n')
 (O/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Trace — Keep the context</title><style>body{margin:60px auto;max-width:1120px;padding:0 24px;background:#080f22;color:#edf3ff;font:18px system-ui}h1{font-size:54px;letter-spacing:-2px;margin-bottom:12px}p{color:#b9c9e5;line-height:1.6}video{width:100%;margin:28px 0;background:#080f22}a{color:#a8bdff}.button{display:inline-block;background:#3759ef;color:white;padding:14px 20px;text-decoration:none;border-radius:7px}small{display:block;margin-top:32px;color:#a8b9d5}</style><h1>Trace. Keep the context.</h1><p>A new product film for a fictional browser bug-reporting tool. Watch one checkout failure turn into a report with the steps, screenshot and browser context.</p><video controls preload="metadata" poster="trace-poster.jpg" src="trace.mp4"></video><a class="button" href="trace.mp4" download>Download MP4</a><p>33 seconds · 1920 × 1080 · 24 fps · No interviews</p><p>$1.36 estimated generation cost across three tests; $1.57 reserved under the $10 cap. Fresh footage, UI, narration and music.</p><small><a href="../../../docs/TRACE_SCORECARD.md">Model scorecard</a> · <a href="../../../docs/TRACE_RUNBOOK.md">Rebuild and learnings</a> · <a href="verification.json">Delivery checks</a></small></html>''')
 print(json.dumps({'duration':33,'decode':'pass','audio_correlation':corr,'audio_peak':peak,'source_timing':hand,'cost_usd':estimated/100},indent=2))
if __name__=='__main__':main()
