"""Join reviewed pocket action to its exact-frame I2V continuation, locally."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];out=R/'artifacts/final_outcome/sideway-coffee-left-hand';out.mkdir(parents=True,exist_ok=True)
a=R/'artifacts/library-loop-14/outputs/sideway_arrival_left_pocket_v4.mp4';b=R/'artifacts/library-loop-14/outputs/sideway_arrival_pocket_settle_v5.mp4'
# 62 original frames at 32fps, then 98 continuation frames. No slow motion or freeze.
subprocess.run(['ffmpeg','-v','error','-y','-i',str(a),'-i',str(b),'-filter_complex','[0:v]trim=start_frame=0:end_frame=62,setpts=PTS-STARTPTS[a];[1:v]trim=start_frame=0:end_frame=98,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-an','-c:v','libx264','-crf','17','-preset','slow','-pix_fmt','yuv420p','-r','32','-movflags','+faststart',str(out/'sideway-coffee-left-hand-revised.mp4')],check=True)
selection={'duration_seconds':5,'fps':32,'join_seconds':1.9375,'clips':[{'source':str(a.relative_to(R)),'start_seconds':0,'duration_seconds':1.9375,'frames':62},{'source':str(b.relative_to(R)),'start_seconds':0,'duration_seconds':3.0625,'frames':98}],'source_image_for_continuation':'videos/sideway-human-realism-test/coffee-left-hand/pocket-continuation-source.png','retiming':False,'crossfade':False,'audio':'intentionally silent','full_film_replaced':False}
(R/'videos/sideway-human-realism-test/coffee-left-hand/revision-selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print(out/'sideway-coffee-left-hand-revised.mp4')
