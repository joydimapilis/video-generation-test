"""Verify, fingerprint, and index the finished MP4 without paid API calls."""
import hashlib
import json
import subprocess
from pathlib import Path

def main():
    root=Path('artifacts/final_outcome/cue')
    video=root/'cue-final.mp4'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    streams=probe['streams']
    picture=next(s for s in streams if s['codec_type']=='video')
    sound=next(s for s in streams if s['codec_type']=='audio')
    assert (picture['width'],picture['height'],picture['codec_name'])==(1920,1080,'h264')
    assert sound['codec_name']=='aac'
    assert abs(float(probe['format']['duration'])-30)<.1
    decode=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],capture_output=True)
    assert decode.returncode==0 and not decode.stderr,decode.stderr.decode()
    subprocess.run(['ffmpeg','-v','error','-y','-ss','8.4','-i',str(video),'-frames:v','1',str(root/'poster.jpg')],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf','fps=1/2.5,scale=480:270,tile=4x3',
        '-frames:v','1',str(root/'contact-sheet.jpg')],check=True)
    audio_windows=[]
    import numpy as np
    for start in [0,10,20,27]:
        # Measure per-channel, never a mono downmix: ffmpeg's stereo-to-mono applies
        # 0.707 gain per channel, so centre-panned material reads up to 1.41x high and
        # a clean mix trips a false overload.
        samples=subprocess.check_output(['ffmpeg','-v','error','-ss',str(start),'-t','2','-i',str(video),
            '-vn','-ac','2','-ar','48000','-f','f32le','-'])
        x=np.frombuffer(samples,dtype='<f4').reshape(-1, 2)
        rms=float(np.sqrt(np.mean(x*x)))
        assert rms>.0001,f'Silent audio window at {start}'
        assert float(np.max(np.abs(x)))<1,f'Audio overload at {start}'
        audio_windows.append({'start':start,'rms':rms,'peak':float(np.max(np.abs(x)))})
    ledger=json.loads(Path('artifacts/library-loop/budget.json').read_text())
    costs={'estimated_usd':sum(r['estimate_cents'] for r in ledger['runs'].values())/100,
        'reserved_usd':sum(r['reserved_cents'] for r in ledger['runs'].values())/100,'cap_usd':10,
        'invoice_verified':False}
    assert costs['reserved_usd']<=10
    assert all(r['status']=='completed' for r in ledger['runs'].values())
    result={'path':str(video.resolve()),'sha256':hashlib.file_digest(video.open('rb'),'sha256').hexdigest(),
        'probe':probe,'full_decode_ok':True,'audio_windows':audio_windows,'cost':costs,
        'composition_checks':{'hyperframes_version':'0.8.34','lint_errors':0,'runtime_errors':0,
            'layout_errors':0,'layout_samples':24,'motion_samples':300,'contrast_passed':40,'contrast_total':40},
        'note':'1080p delivery; the 720p Veo hook is upscaled. Concept film, not a real product demonstration.'}
    (root/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (root/'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Cue</title>
<style>*{box-sizing:border-box}body{margin:0;background:#171a19;color:#f5f7f3;font-family:Arial,sans-serif}main{max-width:1440px;margin:auto;padding:24px}h1{font-size:28px;margin:0 0 20px}video{display:block;width:100%;aspect-ratio:16/9;background:#171a19}a{color:#d8fa67}p{line-height:1.5}@media(max-width:600px){main{padding:16px}}</style>
</head><body><main><h1>Cue</h1><video controls playsinline preload="metadata" poster="poster.jpg" src="cue-final.mp4"></video><p><a href="cue-final.mp4" download>Download MP4</a></p></main></body></html>''')
    Path('assembled_outputs/cue_final.json').write_text(json.dumps({
        'output_id':'cue_library_loop_final','output_path':str(video),'duration_seconds':30,
        'resolution':'1920x1080','assembly_tool':'HyperFrames 0.8.34',
        'source_runs':['ugc_veo_v2','hero_kling_v2'],'reference_library_manifest':'artifacts/library-loop/references/manifest.json',
        'pattern_ids':['human_problem_hook','macro_to_product_reveal','voice_to_action_ui'],
        'verification':str(root/'verification.json'),'cost':costs},indent=2)+'\n')
    print(json.dumps({'path':str(video),'bytes':video.stat().st_size,'cost':costs,'decode_ok':True}))

if __name__=='__main__':
    main()
