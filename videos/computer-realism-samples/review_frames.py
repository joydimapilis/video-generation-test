"""Extract chronological full-frame, face and hand evidence, without changing source."""
import json,subprocess,argparse
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('video',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--fps',type=int,default=8);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(a.video)]))
v=next(x for x in meta['streams'] if x['codec_type']=='video');w,h=v['width'],v['height']
# Broad crops cover the three right-facing subject / left-screen setups.
crops={'full':(0,0,w,h),'hands':(int(.25*w),int(.55*h),int(.73*w),int(.94*h)),'face':(int(.49*w),0,int(.82*w),int(.47*h))}
if a.video.name.startswith('02-'):
 crops['hands']=(int(.27*w),int(.44*h),int(.70*w),int(.98*h))
 crops['face']=(int(.59*w),0,int(.94*w),int(.55*h))
manifest={'source':str(a.video),'fps':a.fps,'method':'chronological sampled frames, not continuous real-time playback','sheets':[],'crops':crops}
for kind,(x,y,x2,y2) in crops.items():
 folder=a.out/kind;folder.mkdir(exist_ok=True)
 filt=f'fps={a.fps},crop={x2-x}:{y2-y}:{x}:{y},scale=384:216:force_original_aspect_ratio=decrease,pad=384:216:(ow-iw)/2:(oh-ih)/2'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(a.video),'-vf',filt,str(folder/'frame-%03d.jpg')],check=True)
 frames=sorted(folder.glob('frame-*.jpg'))
 for start in range(0,len(frames),16):
  sheet=Image.new('RGB',(1536,944),'#17191b');d=ImageDraw.Draw(sheet)
  for i,frame in enumerate(frames[start:start+16]):
   xx=(i%4)*384;yy=(i//4)*236
   sheet.paste(Image.open(frame),(xx,yy+20));d.text((xx+5,yy+3),f'{kind} | {(start+i)/a.fps:.3f}s',fill='white')
  path=folder/f'sheet-{start//16+1}.jpg';sheet.save(path,quality=91);manifest['sheets'].append(str(path))
(a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(a.out)
