"""Compare actual decoded product boundaries and sampled internal drift."""
import json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path('artifacts/library-loop-9')
def frame(path,at):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(path),'-frames:v','1','-vf','scale=480:270','-f','rawvideo','-pix_fmt','rgb24','-'])
 return np.frombuffer(raw,dtype=np.uint8).reshape(270,480,3).astype(float)
def main():
 prev=frame(ROOT/'outputs/crumb_pastry_kling_v1.mp4',4.5-1/24);rows={}
 for name in ['crumb_continuation_h3max','crumb_continuation_kling']:
  path=ROOT/'outputs'/f'{name}.mp4';first=frame(path,0);mid=frame(path,2.4)
  rows[name]={'boundary_mae_255':float(np.abs(prev-first).mean()),'boundary_luma_shift_255':float(abs(prev.mean()-first.mean())),'first_to_middle_mae_255':float(np.abs(first-mid).mean())}
 (ROOT/'join-metrics.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
