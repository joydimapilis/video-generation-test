"""Verify delivery against source media, composition checks and the shared ledger."""
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path
import numpy as np

ROOT=Path('artifacts/library-loop-8')
DELIVERY=Path('artifacts/final_outcome/round8')


def pcm(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype='<f4').astype(float)


def frame(path,t):
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{t:.8f}','-i',str(path),'-frames:v','1','-vf','scale=960:540:force_original_aspect_ratio=increase,crop=960:540','-pix_fmt','rgb24','-f','rawvideo','-'])
    return np.frombuffer(raw,np.uint8).reshape(540,960,3).astype(float)


def main():
    results=[]
    builds=json.loads((ROOT/'sample-build.json').read_text())
    selection=json.loads((ROOT/'sample-selection.json').read_text())
    for spec in builds:
        project=Path(spec['project']);name=project.name;path=DELIVERY/(name+'.mp4')
        check=json.loads((ROOT/('check-'+name+'.json')).read_text())
        assert check['ok'] and check['contrast']['checked']>0
        assert not any(v.get('findings') for k,v in check.items() if k in ['lint','runtime','layout','motion','contrast'])
        for source in json.loads((project/'sources.json').read_text()):
            if 'sha256' in source:
                assert hashlib.sha256(Path(source['source']).read_bytes()).hexdigest()==source['sha256']
                assert hashlib.sha256(Path(source['staged']).read_bytes()).hexdigest()==source['sha256']
            if 'derived_sha256' in source:
                assert hashlib.sha256(Path(source['staged']).read_bytes()).hexdigest()==source['derived_sha256']
                assert hashlib.sha256(Path(source['source']).read_bytes()).hexdigest()==source['source_sha256']
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))
        v=next(s for s in probe['streams'] if s['codec_type']=='video')
        assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'24/1')
        assert abs(float(probe['format']['duration'])-spec['duration'])<.06
        decode=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],capture_output=True)
        assert decode.returncode==0 and not decode.stderr,decode.stderr.decode()
        black=subprocess.run(['ffmpeg','-hide_banner','-i',str(path),'-vf','blackdetect=d=0.08:pix_th=0.04','-an','-f','null','-'],capture_output=True)
        assert black.returncode==0 and b'black_start:' not in black.stderr
        sheet=DELIVERY/(name+'-contact.jpg')
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(path),'-vf',f"fps=8/{spec['duration']},scale=480:270,tile=4x2",'-frames:v','1',str(sheet)],check=True)
        wave=pcm(path);speech=None
        stereo=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','2','-ar','48000','-f','f32le','-']),dtype='<f4')
        stereo_peak=float(np.abs(stereo).max())
        assert stereo_peak<1, 'Decoded stereo audio exceeds full scale'
        if name!='cue-object-study':
            take=selection['ugc' if name=='cue-followthrough' else 'interview']
            original=pcm(take['path']);start=4000;end=80000
            a=original[round(take.get('in',0)*16000)+start:round(take.get('in',0)*16000)+end];b=wave[start:end]
            corr=float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))
            assert corr>.98,(name,corr)
            speech={'source':take['path'],'window':[.25,5],'pcm_correlation':corr}
        results.append({'name':name,'path':str(path),'duration':float(probe['format']['duration']),'fps':24,'resolution':'1920x1080',
            'full_decode_ok':True,'black_intervals_detected':False,'source_hashes_match':True,
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'composition_check':str(ROOT/('check-'+name+'.json')),
            'contrast_passes':check['contrast']['passed'],'speech_source_match':speech,'audio_peak_stereo':stereo_peak,'analysis_downmix_peak':float(np.abs(wave).max()),
            'contact_sheet':str(sheet),'composition_sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [project/'index.html',*project.glob('compositions/*.html')]}})
    # Confirm the final product render actually displays the intended source windows.
    rendered=DELIVERY/'cue-object-study.mp4';matches=[]
    for t,source,at in [(1,selection['product']['path'],1),(5.5,selection['product']['path'],5.5),
                        (5.5+1/24,selection['continuation']['path'],0),(8,selection['continuation']['path'],8-(5.5+1/24))]:
        a,b=frame(rendered,t),frame(source,at)
        mae=float(np.abs(a[210:]-b[210:]).mean())
        matches.append({'output_at':t,'source':source,'source_at':at,'lower_frame_rgb_mae':mae})
        assert mae<10,(t,mae)
    ledger=json.loads((ROOT/'budget.json').read_text());reserved=sum(r['reserved_cents'] for r in ledger['runs'].values())
    assert reserved<=ledger['limit_cents']<=1000
    previews=[]
    for port,name in [(3028,'cue-followthrough'),(3029,'cue-object-study'),(3030,'crew-availability')]:
        with urllib.request.urlopen(f'http://localhost:{port}/',timeout=10) as response:
            assert response.status==200
        previews.append(f'http://localhost:{port}/#project/{name}')
    report={'outputs':results,'product_source_frame_matches':matches,'estimated_cents':sum(r['estimate_cents'] for r in ledger['runs'].values()),
            'reserved_cents':reserved,'cap_cents':1000,'previews':previews,
            'limits':'Technical checks and source correspondence, not proof of realistic acting, lip sync, marketing effectiveness, or final user approval.'}
    (ROOT/'delivery-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (DELIVERY/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
