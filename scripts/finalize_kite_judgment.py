"""Decode, verify and package the finished brand film."""
from pathlib import Path
import subprocess,json,hashlib,shutil
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];P=R/'videos/kite-judgment';D=R/'artifacts/final_outcome/kite-judgment';movie=D/'kite-judgment.mp4'
m=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]))
v=next(s for s in m['streams'] if s['codec_type']=='video');a=next(s for s in m['streams'] if s['codec_type']=='audio')
assert(v['width'],v['height'])==(1920,1080)
assert v['avg_frame_rate']=='30/1' and int(v['nb_read_frames'])==1200
assert abs(float(m['format']['duration'])-40)<.04
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
levels=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-sn','-dn','-f','null','-'],capture_output=True,text=True,check=True).stderr
(D/'audio-levels.txt').write_text(levels)
times=[0,1.5,8,11,13.9667,14,19,22.5,27,33,36.1,39.5]
sheet=Image.new('RGB',(1600,972),'#222');dr=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 f=D/f'frame-{t}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(movie),'-frames:v','1',str(f)],check=True)
 x=i%4*400;y=i//4*244;im=Image.open(f).resize((400,225));sheet.paste(im,(x,y+19));dr.text((x+8,y+2),f'{t}s',fill='white')
sheet=sheet.crop((0,0,1600,732));sheet.save(D/'contact-sheet.jpg',quality=94);Image.open(D/'frame-11.png').convert('RGB').save(D/'poster.jpg',quality=95)
check=json.loads((R/'artifacts/kite-judgment/check-final.json').read_text());assert check['ok']
ver={'verified':True,'duration_seconds':40,'width':1920,'height':1080,'fps':30,'frames':1200,'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'full_decode':'passed','composition_check':True,'generation_cost_usd':0,'voiceover':False}
(D/'verification.json').write_text(json.dumps(ver,indent=2))
(D/'budget.json').write_text(json.dumps({'ceiling_usd':10,'total_generation_cost_usd':0,'paid_generation_calls':0,'visuals':'HyperFrames SVG and GSAP','music':'Original deterministic local synthesis','sfx':'Original deterministic local synthesis'},indent=2))
report='''# Kite — Keep the final say

40-second, 1920×1080, 30fps finished brand film. Original copy and motion treatment inspired by the supplied concept. Scattered research, message and asset objects find one route through context, a plan and reviewable drafts. The work stops before a human decision boundary; nothing is shown sent or published. No presenter or product UI appears.

## Creative and audio

Large, paced typography carries the complete message with sound off. No voiceover or separate subtitle track is required. Original local 96 BPM electronic score: sparse keys, a quiet pulse as the pieces align, and a warm restrained ending. Soft object sounds, no notification or success fanfare. Three editable HyperFrames scenes with GSAP and SVG, registry text-stagger entrance mechanics adapted to solid brand type. No generated stock footage or AI imagery.

## Current brand verification

The [Kite newsroom](https://kite.ai/newsroom) supplies the official white wordmark and palette: Orange #FF6D2D, Night #0E0E0E, White #FFFFFF, Grey #B3B3B3. The current site's CSS confirms Onest heading typography. Logo aspect ratio and artwork are preserved. The end card is an original composition following those public assets; no supplied approved end-card template or formal brand/legal approval is claimed.

The current site's Add me to Slack link goes to https://kite.ai/welcome?src=home-close-add-to-slack. The player CTA uses https://kite.ai/welcome without inventing campaign tracking. The MP4 displays kite.ai as its human-readable destination.

Public product evidence: [Kite homepage](https://kite.ai/) and [approval documentation](https://docs.kite.ai/slack/approvals). The decision-boundary story represents the review-first workflow in the user's concept. It is not a claim about every configurable autonomy mode. All object labels are editorial illustrations, not native UI statuses.

## Library influence

- Bloom — World's first on-brand AI: large economical typography, a simple repeated visual system, restraint in the closing message.
- Notion — Introducing Custom Agents: concrete labelled objects make invisible work visible and carry the transition.

Reviewed full-run contact sheets and denser chronological opening samples from the available library. No reference footage or audio is used. Source paths and sheets: artifacts/kite-judgment/references/manifest.json.

## Verification and corrections

Corrected an exact-cut initialization issue in the five-object handoff, increased the message-card letterform contrast, and removed empty first/cut frames. The color review was repeated with standard capture and PNG-decoded frames. Both capture routes produced the same small RGB difference in the encoded orange; the larger apparent shift came from JPEG review extraction. Final measured orange is RGB(255,107,38) versus source RGB(255,109,45). Standard capture is retained. Required HyperFrames runtime/layout/contrast/motion checks pass; object alignment and scene joins were visually inspected. Final MP4: 1,200 frames, 40.000s, H.264/AAC, 1080p30; complete FFmpeg decoding passed. SHA-256 and technical details in verification.json.

No customer data, testimonials, metrics, time-saved claims, revenue claims or implied public action. Audience comprehension and 3-second view rate have not been tested. Any controlled test must hold audience, placement and first-frame conditions fixed; retention alone does not establish comprehension or business impact.

## Cost and editable sources

Total generation cost: $0, against the $10 ceiling. No paid model calls. Tools: HyperFrames 0.8.46, GSAP, Python/NumPy/SoundFile and FFmpeg.

Editable project: videos/kite-judgment. Builders: scripts/build_kite_judgment.py and scripts/prepare_kite_judgment_audio.py. Regenerate sources, run npm run check in the project, then npm run render. Original previous films remain intact.

Remaining limitation: campaign-specific tracking and a supplied approved end-card template were unavailable; this deliverable uses the verified public onboarding destination and an original brand-consistent end card.
'''
(D/'REPORT.md').write_text(report);(P/'DELIVERY_REPORT.md').write_text(report)
(P/'README.md').write_text('# Kite — Keep the final say\n\n40-second finished brand film. See DELIVERY_REPORT.md for production, verification and rebuild instructions.\n\nFinal: ../../artifacts/final_outcome/kite-judgment/kite-judgment.mp4\n')
(P/'BRIEF.md').write_text((P/'BRIEF.md').read_text().replace('status: production','status: rendered'))
(D/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kite — Keep the final say</title><style>body{margin:0;background:#0e0e0e;color:white;font:16px system-ui}main{max-width:1200px;margin:32px auto;padding:0 20px}video{width:100%;background:#0e0e0e;display:block}a{color:#ff9563}p{line-height:1.65}</style><main><video controls playsinline preload="metadata" src="kite-judgment.mp4" poster="poster.jpg"></video><p>Kite — Keep the final say · 40 seconds · 1080p<br><a href="kite-judgment.mp4" download>Download MP4</a> · <a href="https://kite.ai/welcome">Add Kite to Slack</a> · <a href="REPORT.md">Production notes</a></p></main></html>''')
(R/'assembled_outputs/kite-judgment.json').write_text(json.dumps({'name':'Kite — Keep the final say','video':str(movie.relative_to(R)),'player':str((D/'review.html').relative_to(R)),'editable_project':str(P.relative_to(R)),'duration_seconds':40,'generation_cost_usd':0,'resolution':[1920,1080],'cta_destination':'https://kite.ai/welcome','verification':str((D/'verification.json').relative_to(R))},indent=2))
(R/'review_notes/kite-judgment.md').write_text('''# Kite — Keep the final say: production review

Deterministic brand-film route accepted after visual inspection and framework checks. Captions-first type pacing carries the story without voice. Library objects/typography provided useful evidence without requiring generative media. An exact sub-composition cut exposed the difference between tl.set at zero and fromTo immediate initialization: preserve matching first-frame positions via explicit fromTo poses. Orange decorative letterforms on warm paper needed darker ink to meet contrast. Both native and standard capture produced RGB(255,107,38) for source Orange #FF6D2D; the larger apparent shift was in JPEG extraction, not uniquely the native capture. Use PNG-decoded review frames to avoid misleading JPEG matrix differences. Standard capture was retained. Brand-critical exports need a source-versus-encoded pixel spot check, not only a visual contact sheet. No paid generation was necessary. Audience outcomes remain untested; these are production findings, not performance results.
''')
print(json.dumps(ver,indent=2))
