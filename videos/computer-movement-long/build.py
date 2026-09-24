"""Build three clean editable HyperFrames samples from reviewed take selection."""
import json,shutil,subprocess,hashlib
from pathlib import Path
project=Path(__file__).resolve().parent
root=project.parents[1]
selection=json.loads((project/'selection.json').read_text())
assert selection['reviewed'] is True
assets=project/'assets';assets.mkdir(exist_ok=True)
# Freeze GSAP locally, reusing the repository's existing dependency when present.
existing=next(iter(root.glob('videos/*/assets/gsap.min.js')),None)
if existing: shutil.copy2(existing,assets/'gsap.min.js')
else:
 import urllib.request
 urllib.request.urlretrieve('https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js',assets/'gsap.min.js')
for sample in selection['samples']:
 name=sample['name'];folder=project/name;folder.mkdir(exist_ok=True)
 source=root/sample['source'];shutil.copy2(source,assets/(name+'.mp4'))
 local_assets=folder/'assets';local_assets.mkdir(exist_ok=True)
 shutil.copy2(source,local_assets/(name+'.mp4'));shutil.copy2(assets/'gsap.min.js',local_assets/'gsap.min.js')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)]))
 v=next(s for s in probe['streams'] if s['codec_type']=='video')
 width,height=v['width'],v['height'];duration=sample['duration']
 html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width={width}, height={height}"><title>{name}</title>
<script src="assets/gsap.min.js"></script>
<style>*{{box-sizing:border-box}}html,body{{margin:0;width:{width}px;height:{height}px;overflow:hidden;background:#17191b}}#root{{position:relative;width:100%;height:100%;overflow:hidden}}.clip{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}}</style></head>
<body><div id="root" data-composition-id="main" data-width="{width}" data-height="{height}" data-duration="{duration}">
<video id="sample" class="clip" src="assets/{name}.mp4" data-start="0" data-duration="{duration}" data-media-start="{sample.get('source_start',0)}" data-track-index="0" muted playsinline></video>
</div><script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{paused:true}});</script></body></html>'''
 (folder/'index.html').write_text(html)
 for f in ['hyperframes.json','package.json']:shutil.copy2(project/f,folder/f)
 sample.update({'width':width,'height':height,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fps':v['r_frame_rate']})
# Main project previews sample 01. Each named folder is independently editable/renderable.
first=selection['samples'][0]['name']
main=(project/first/'index.html').read_text().replace('assets/','assets/')
(project/'index.html').write_text(main)
(project/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
print('Built',len(selection['samples']),'samples')
