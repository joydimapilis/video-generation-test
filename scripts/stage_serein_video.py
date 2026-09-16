"""Stage only selected, reviewed image-to-video takes for Serein."""
import hashlib,json,subprocess
from pathlib import Path
P=Path('videos/serein');R=Path('artifacts/library-loop-13')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 rows=[]
 for name,run,start,width,rate in [('focus','serein_mouse_focus_kling_v5',1.5,1120,0.75),('relief','serein_mouse_relief_kling_v5',0,1040,1)]:
  src=R/'outputs'/f'{run}.mp4';dst=P/'assets'/f'{name}.mp4'
  subprocess.run(['ffmpeg','-v','error','-ss',str(start),'-i',str(src),'-t','6','-vf',f'setpts=(PTS-STARTPTS)/{rate},fps=24,tpad=stop_mode=clone:stop_duration=0.1,trim=duration=6,scale=1920:1080,crop={width}:1080:350:0','-an','-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p','-y',str(dst)],check=True)
  rows.append({'role':name,'run_id':run,'source':str(src),'source_sha256':sha(src),'derived':str(dst),'derived_sha256':sha(dst),'source_start':start,'playback_rate':rate,'source_duration':6*rate,'duration':6,'timeline_start':0 if name=='focus' else 24,'crop':{'x':350,'y':0,'width':width,'height':1080},'pre_crop_size':[1920,1080],'display_x':800 if name=='focus' else 880,'image_first':True,'reference':'assets/designer-mouse-v2.png','reference_sha256':sha(P/'assets/designer-mouse-v2.png'),'review':'artifacts/library-loop-13/reviews/character-mouse-v2.json'})
 (P/'sources.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
