from pathlib import Path
import subprocess,json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
R=Path.cwd();P=R/'videos/kite-feedback';V=P/'renders/kite-feedback.mp4';O=R/'artifacts/final_outcome/kite-feedback';O.mkdir(parents=True,exist_ok=True);S=R/'.context/kite-feedback-encoded';S.mkdir(exist_ok=True)
def run(args):
 if args[0]=='ffmpeg': args.insert(1,'-y')
 return subprocess.run(args,check=True,capture_output=True)
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]).stdout)
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
assert int(v['nb_frames'])==1080 and abs(float(probe['format']['duration'])-36)<.1
run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'])
audio=np.frombuffer(run(['ffmpeg','-v','error','-i',str(V),'-vn','-f','f32le','-ar','48000','-ac','2','-']).stdout,dtype=np.float32).reshape(-1,2)
peak=float(abs(audio).max());assert peak<.99
rms=lambda x:float(np.sqrt(np.mean(x*x)))
last=rms(audio[int(35.8*48000):int(36*48000)]);body=rms(audio[int(30*48000):int(32*48000)]);assert last<body*.2
# chronological encoded frames and cut-boundary samples; no new model calls.
times=sorted(set([i*.5 for i in range(72)]+[11.9667,12,12.0333,23.9667,24,24.0333,28.3667,28.4,31.9667,32,32.0333,35.95]))
for idx,t in enumerate(times):
 f=S/f'frame-{idx:03d}.jpg';run(['ffmpeg','-v','error','-ss',str(t),'-i',str(V),'-frames:v','1','-vf','scale=640:360','-q:v','2',str(f)])
for page in range((len(times)+15)//16):
 subset=times[page*16:(page+1)*16];sheet=Image.new('RGB',(1920,4*386),'#202020');d=ImageDraw.Draw(sheet)
 for n,t in enumerate(subset):
  img=Image.open(S/f'frame-{page*16+n:03d}.jpg');x=(n%3)*640;y=(n//3)*386
  # use 4 columns with 480px tiles to fit 16 chronologically
  x=(n%4)*480;y=(n//4)*296;sheet.paste(img.resize((480,270)),(x,y+26));d.text((x+8,y+6),f'{t:.3f}s',fill='white')
 sheet.crop((0,0,1920,1184)).save(S/f'sheet-{page+1}.jpg',quality=93)
# Dense human interval plus hands cropped from actual encoded MP4.
ht=[28.4+i*.125 for i in range(29)]
for page in range(2):
 sheet=Image.new('RGB',(1920,1184),'#202020');d=ImageDraw.Draw(sheet)
 for n,t in enumerate(ht[page*16:(page+1)*16]):
  f=S/f'human-{page*16+n:02d}.png';run(['ffmpeg','-v','error','-ss',str(t),'-i',str(V),'-frames:v','1','-vf','crop=1060:596:100:285,scale=480:270',str(f)])
  x=(n%4)*480;y=(n//4)*296;sheet.paste(Image.open(f),(x,y+26));d.text((x+8,y+6),f'{t:.3f}s',fill='white')
 sheet.save(S/f'human-sheet-{page+1}.jpg',quality=94)
final=O/'kite-feedback.mp4';shutil.copy2(V,final)
verification={'status':'technical_pass_visual_review_pending','video':{'codec':v['codec_name'],'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'frames':v['nb_frames'],'duration':probe['format']['duration']},'audio':{'codec':a['codec_name'],'sample_rate':a['sample_rate'],'channels':a['channels'],'peak_linear':peak,'final_200ms_rms':last,'body_rms':body,'fade_ratio':last/body,'speech':False,'listening_review':False},'full_decode':'pass','encoded_sample_times':times,'human_sample_times':ht,'encoded_sheets':str(S),'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'final':str(final),'renderer':{'version':'0.8.60','capture':'drawelement','gpu':'hardware','seconds':35.9}}
(O/'verification.json').write_text(json.dumps(verification,indent=2));shutil.copy2(R/'.context/kite-feedback-check-final.json',O/'composition-check.json')
print(json.dumps(verification,indent=2))
