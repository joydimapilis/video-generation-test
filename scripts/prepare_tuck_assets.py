"""Restage Tuck's selected fresh plate and local tools; no paid calls."""
import shutil,subprocess,urllib.request
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'videos/tuck';A=P/'assets'
def main():
 A.mkdir(exist_ok=True);source=R/'artifacts/library-loop-12/outputs/tuck_receipt_h3max_v2.mp4'
 if not source.exists():raise FileNotFoundError('Resume configs/tuck_round2.json using its existing ledger before restaging.')
 shutil.copyfile(source,A/'receipt-source.mp4');shutil.copyfile(R/'hyperframes/motion5/assets/gsap.min.js',A/'gsap.min.js')
 for name,url in [('SpaceGrotesk.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf'),('Inter.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf')]:
  if not(A/name).exists():urllib.request.urlretrieve(url,A/name)
 for name,start,length,filters in [('opening',.5,5.5,'fps=24,scale=-2:1080,crop=1090:1080:550:0'),('return',6,4,'fps=24,scale=-2:1080,crop=870:1080:700:0,tpad=stop_mode=clone:stop_duration=4')]:
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-t',str(length),'-i',str(A/'receipt-source.mp4'),'-vf',filters,'-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',str(A/f'{name}.mp4')],check=True)
if __name__=='__main__':main()
