"""A silent, unretouched A/B reel. One second either side of each repeated join."""
import json
from pathlib import Path
import shutil
import subprocess


PROJECT = Path('hyperframes/crew-comparison')
LOOP = Path('artifacts/library-loop-6/outputs')


def make_join(a, b, target):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.125', '-i', str(a), '-i', str(b),
        '-filter_complex', '[0:v]trim=duration=1,setpts=PTS-STARTPTS,fps=24,setsar=1[a];'
        '[1:v]trim=duration=1,setpts=PTS-STARTPTS,fps=24,setsar=1[b];'
        '[a][b]concat=n=2:v=1:a=0[v]', '-map', '[v]', '-an', '-c:v', 'libx264',
        '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(target)], check=True)


def main():
    assets = PROJECT / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    for name in ('package.json', 'hyperframes.json'):
        shutil.copy2(Path('hyperframes/crew-improved') / name, PROJECT / name)
    for name in ('gsap.min.js', 'CrewSans.ttf'):
        shutil.copy2(Path('hyperframes/crew/assets') / name, assets / name)
    files = {'before-person': LOOP / 'line4_product_v1.mp4',
             'after-person': LOOP / 'realism_line4_v2.mp4',
             'before-hands': Path('artifacts/library-loop-5/outputs/broll_dough_v1.mp4'),
             'after-hands': LOOP / 'realism_dough_v2.mp4'}
    for name, path in files.items():
        shutil.copy2(path, assets / (name + '.mp4'))
    make_join(LOOP / 'line4_product_v1.mp4', LOOP / 'line5_how_v1.mp4', assets / 'before-join.mp4')
    make_join(LOOP / 'realism_line4_v2.mp4', LOOP / 'realism_line5_chained.mp4', assets / 'after-join.mp4')
    make_join(LOOP / 'realism_line4_v2.mp4', LOOP / 'realism_line5_control.mp4', assets / 'control-join.mp4')
    chapters = [
        (0, 6, 'before-person', 'after-person', 'Original prompt', 'Revised prompt', '01 / Human performance', 'Same reference, seed and model. Full takes; no retouching.'),
        (6, 6, 'before-hands', 'after-hands', 'Original action', 'Revised action', '02 / Hands and physical contact', 'Full takes. The final film uses only the first press-and-release.'),
        (12, 4, 'before-join', 'after-join', 'Original shared anchor', 'Previous exit frame', '03 / Shot continuity', 'One second before and after each cut, repeated twice.'),
        (16, 4, 'control-join', 'after-join', 'Shared-anchor control', 'Previous exit frame', '04 / Reference-only control', 'Same improved prompt, seed and outgoing shot; different input reference.')]
    elements = []
    for index, (start, duration, left, right, label_a, label_b, title, note) in enumerate(chapters):
        elements.append(f'<section id="chapter-{index}" class="clip labels" data-start="{start}" data-duration="{duration}" data-track-index="{10 + index}">'
                        f'<div class="left-label">{label_a}</div><div class="right-label">{label_b}</div>'
                        f'<h1>{title}</h1><p>{note}</p></section>')
        repetitions = 2 if index >= 2 else 1
        for side, name in enumerate((left, right)):
            for repeat in range(repetitions):
                at = start + repeat * 2 if repetitions == 2 else start
                dur = 2 if repetitions == 2 else duration
                elements.append(f'<video id="v-{index}-{side}-{repeat}" class="clip plate side-{side}" src="assets/{name}.mp4" '
                    f'data-start="{at}" data-duration="{dur}" data-track-index="{side}" muted playsinline></video>')
    html = '''<!doctype html><html><head><meta charset="UTF-8"><script src="assets/gsap.min.js"></script><style>
    @font-face{font-family:CrewSans;src:url('assets/CrewSans.ttf')}
    *{box-sizing:border-box;margin:0}html,body,#root{width:1920px;height:1080px;overflow:hidden;background:#101315;color:#f6f7f8;font-family:CrewSans,Arial,sans-serif}
    #root{position:relative}.clip{position:absolute}.plate{top:180px;width:960px;height:540px;object-fit:contain}.side-0{left:0}.side-1{left:960px}
    .labels{inset:0;pointer-events:none}.left-label,.right-label{position:absolute;top:94px;width:840px;font-size:34px}.left-label{left:64px}.right-label{left:1024px}
    h1{position:absolute;left:64px;top:785px;font-size:44px;font-weight:400}p{position:absolute;left:64px;top:857px;font-size:28px;color:#c5cbd0}
    footer{position:absolute;left:64px;bottom:52px;font-size:22px;color:#b7bfc4}
    </style></head><body><div id="root" data-composition-id="crew-comparison" data-width="1920" data-height="1080" data-duration="20">'''
    html += '\n'.join(elements) + '''<footer>SILENT VISUAL COMPARISON / AI-GENERATED FOOTAGE / SINGLE-TAKE PILOT</footer></div>
    <script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});tl.to({t:0},{t:20,duration:20,ease:'none'});window.__timelines['crew-comparison']=tl;</script></body></html>'''
    (PROJECT / 'index.html').write_text(html)
    (PROJECT / 'comparison-plan.json').write_text(json.dumps(chapters, indent=2) + '\n')
    print(PROJECT)


if __name__ == '__main__':
    main()
