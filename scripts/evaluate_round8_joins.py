"""Compare actual decoded cut frames; pixel distance is not a quality score."""
import json
import subprocess
from pathlib import Path
import numpy as np

ROOT=Path('artifacts/library-loop-8')


def frame(path,at):
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(at),'-i',str(path),'-frames:v','1','-vf','scale=960:540','-pix_fmt','rgb24','-f','rawvideo','-'])
    return np.frombuffer(raw,np.uint8).reshape(540,960,3).astype(float)


def metrics(a,b):
    return {'rgb_mae_0_to_255':round(float(np.abs(a-b).mean()),4),
            'mean_luma_delta_0_to_255':round(float(abs((a@[.2126,.7152,.0722]).mean()-(b@[.2126,.7152,.0722]).mean())),4),
            'rgb_mean_delta':np.round(b.mean((0,1))-a.mean((0,1)),4).tolist()}


def main():
    out=ROOT/'continuity';out.mkdir(exist_ok=True)
    source=ROOT/'outputs/product_h3_pullback.mp4'
    previous=frame(source,5.5)
    report={'method':'Decoded RGB frames uniformly resized to 960x540 for comparison. Lower MAE means closer pixels, not better human realism or motion. Source at 5.5s is displayed as the final frame before cut at 5.5416667s (24fps). Native frame dimensions and full decode are separately recorded.',
            'previous':str(source),'source_at':5.5,'cut_at':5.5+1/24,
            'independent_macro_restart':metrics(previous,frame(source,0)),
            'previous_tail_motion':metrics(frame(source,5.5-1/24),previous),'candidates':{}}
    for name in ['product_h3_paired','product_kling_paired']:
        path=ROOT/'outputs'/f'{name}.mp4'
        if not path.exists():continue
        meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
        vs=next(s for s in meta['streams'] if s['codec_type']=='video')
        last=(int(vs['nb_frames'])-1)/24
        a,b,c=frame(path,0),frame(path,2.5),frame(path,last)
        report['candidates'][name]={'join':metrics(previous,a),'first_to_second':metrics(a,frame(path,1/24)),
            'first_to_middle':metrics(a,b),'first_to_last':metrics(a,c),
            'last_at':last,'duration':meta['format']['duration']}
        # Actual frames straddling the cut, not evenly sampled midshots.
        pts=[(source,5.5-2/24),(source,5.5-1/24),(source,5.5),(path,0),(path,1/24),(path,2/24)]
        sheet=np.full((576*2,960*3,3),32,dtype=np.uint8)
        labels=[]
        for i,(p,t) in enumerate(pts):
            x=(i%3)*960;y=(i//3)*576
            sheet[y+36:y+576,x:x+960]=frame(p,t).astype('uint8')
            labels.append({'row':i//3,'column':i%3,'source':str(p),'seconds':t})
        subprocess.run(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24',
            '-video_size','2880x1152','-i','-','-frames:v','1',
            str(out/(name+'-joint.jpg'))],input=sheet.tobytes(),check=True)
        (out/(name+'-joint-frames.json')).write_text(json.dumps(labels,indent=2)+'\n')
    (out/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
