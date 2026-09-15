"""Rebuild the unretouched 24-second model/prompt comparison from frozen outputs."""
from html import escape
import hashlib
import json
from pathlib import Path
import shutil

PROJECT = Path('hyperframes/interview-models')


def main():
    assets = PROJECT / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    sources = {
        'veo': Path('artifacts/library-loop-6/outputs/realism_line4_v2.mp4'),
        'kling-contract': Path('artifacts/library-loop-7/outputs/interview_kling3_contract.mp4'),
        'kling-restrained': Path('artifacts/library-loop-7/outputs/interview_kling3_restrained.mp4'),
    }
    for source in sources.values():
        if not source.is_file():
            raise ValueError('Comparison requires an actual output: ' + str(source))
    provenance = []
    for name, source in sources.items():
        target = assets / (name + '.mp4')
        shutil.copy2(source, target)
        provenance.append({'source': str(source), 'asset': str(target),
                           'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    shutil.copy2('hyperframes/crew/assets/CrewSans.ttf', assets / 'CrewSans.ttf')
    shutil.copy2('hyperframes/crew/assets/gsap.min.js', assets / 'gsap.min.js')
    elements = []
    chapters = [('kling-contract', '01 / Same interview, different model', 'Full shot contract'),
                ('kling-restrained', '02 / Test a more restrained performance', 'Shorter performance prompt')]
    for index, (right, title, description) in enumerate(chapters):
        start = index * 12
        elements.append(f'<section id="labels-{index}" class="clip labels" data-start="{start}" data-duration="12" data-track-index="8">'
                        f'<h1>{escape(title)}</h1><div class="left-label">Veo 3.1 Fast / baseline</div>'
                        f'<div class="right-label">Kling 3.0 Pro / {escape(description)}</div></section>')
        for repeat in range(2):
            at = start + repeat * 6
            for side, name in enumerate(('veo', right)):
                elements.append(f'<video id="v-{index}-{repeat}-{side}" class="clip plate side-{side}" '
                                f'src="assets/{name}.mp4" data-start="{at}" data-duration="6" '
                                f'data-track-index="{side}" muted playsinline></video>')
            speaker = 'veo' if repeat == 0 else right
            label = 'Veo / left' if repeat == 0 else 'Kling / right'
            elements.append(f'<audio id="speech-{index}-{repeat}" src="assets/{speaker}.mp4" '
                            f'data-start="{at}" data-duration="6" data-track-index="4" data-volume="1"></audio>')
            elements.append(f'<p id="listen-{index}-{repeat}" class="clip listen" data-start="{at}" '
                            f'data-duration="6" data-track-index="{10 + index * 2 + repeat}">Listening to {label}</p>')
    html = '''<!doctype html><html><head><meta charset="UTF-8"><title>Interview model comparison</title><script src="assets/gsap.min.js"></script><style>
@font-face{font-family:CrewSans;src:url('assets/CrewSans.ttf')}
*{box-sizing:border-box;margin:0}html,body{width:1920px;height:1080px;overflow:hidden;background:#101315;color:#f6f7f8;font-family:CrewSans,Arial,sans-serif}
#root{position:relative;width:1920px;height:1080px}.clip{position:absolute}.labels{inset:0;pointer-events:none}
h1{position:absolute;top:52px;left:64px;font-size:46px;font-weight:400}
.left-label,.right-label{position:absolute;top:145px;width:850px;font-size:28px;color:#d2d9dc}.left-label{left:64px}.right-label{left:1008px}
.plate{top:224px;width:944px;height:531px;object-fit:contain}.side-0{left:8px}.side-1{left:968px}
.listen{left:64px;top:800px;font-size:36px;color:#eddaab}
.context{position:absolute;left:64px;top:870px;font-size:27px;color:#d2d9dc}
footer{position:absolute;left:64px;bottom:66px;font-size:22px;color:#b7bfc4}
</style></head><body><div id="root" data-composition-id="interview-models" data-width="1920" data-height="1080" data-duration="24">'''
    html += '\n'.join(elements)
    html += '''<p class="context">Crew / Shift scheduling. Same product line and starting image. Original audio.</p>
<footer>AI-GENERATED PRESENTER / SINGLE TRIALS / FULL TAKES / NO RETOUCHING</footer></div>
<script>window.__timelines=window.__timelines||{};window.__timelines['interview-models']=gsap.timeline({paused:true});</script></body></html>'''
    (PROJECT / 'index.html').write_text(html)
    (PROJECT / 'sources.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(PROJECT)


if __name__ == '__main__':
    main()
