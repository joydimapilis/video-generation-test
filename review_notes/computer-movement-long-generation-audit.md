# Longer computer studies: generation audit

The longer studies reuse the previously generated stills. Their original image requests were text-only. Each new I2V request received exactly one generated PNG plus text/settings. No real reference video, extracted real frame, last frame, pose or motion-control input was submitted. Uploaded PNG bytes match the original generated files by SHA256. This audit uses local persisted requests, not an independent provider-side log.

## Sample 01

Selected video request: `01-computer-sequence-wan-v2`; delivered range 0–15s.

Source: `artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png`

Original source-image generation prompt:

```text
Candid realistic unretouched documentary photo, landscape 16:9. An ordinary 43-year-old Black woman with short loosely tied natural curls, freckles and under-eye texture, wearing a faded sage-green cotton overshirt over a grey T-shirt, seated at a walnut laminate desk in a modest office with corkboard and folders. Neutral task-focused face, eyes looking at the desktop monitor on screen-left, not at camera. Medium three-quarter view including face, torso, both full hands and keyboard, camera slightly above desk. Soft ordinary window light, realistic skin pores and cotton creases; no glamour, smile, retouching or dramatic bokeh. IMPORTANT physical pose: A separate very thin matte-black keyboard sits flat on the desk with a thick black padded wrist-rest flush against its near edge. Both forearms lie on the desk; the heels of both palms are visibly resting on the padded support. Hands are low and relaxed, fingers almost extended with only a very shallow curve. Fingertip pads touch the letter keys lightly; knuckles do not arch high. Left hand on left letters, right hand on right letters, thumbs resting near the spacebar. All fingers visible and normal, no curled or dangling fingers. Both wrists supported at the same level as the keys, clearly showing contact with the pad. She is an experienced quiet typist caught between two small key presses. Still image only, no motion blur. Normal desktop monitor and desk geometry, hands fully unobscured.
```

Image generation input files: **none**.

### 01-computer-sequence-kling-v1

Model: `fal-ai/kling-video/v3/pro/image-to-video`; request ID: `01a0c686-10b9-7013-850c-6822a5180410`.

Only file input: `artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png` in `start_image_url`.

```text
Single continuous 15-second candid shot at normal speed. Camera locked on tripod with absolutely unchanged framing. Preserve the source person, face, hairstyle, age, clothing, lighting, room and device geometry. Ordinary concentrated expression, relaxed closed mouth, natural blinks. Small movements, supported forearms, relaxed low wrists. The woman is editing a short sentence. 0–2 seconds: she reads the monitor with fingertips resting quietly on the keyboard. 2–5 seconds: she types a few words with small independent fingertip presses close to the key surface; the heels of her hands stay on the padded wrist rest. 5–7 seconds: she stops pressing and rereads the screen, leaving fingers relaxed on their keys. 7–9 seconds: the right hand slides a short distance along the keyboard to press two navigation keys, then rests. 9–11 seconds: eyes refocus higher on the screen while hands remain supported and quiet. 11–14 seconds: right hand returns to the letter keys and both hands type one brief correction, irregular quiet finger movements. 14–15 seconds: typing settles; one shoulder relaxes slightly with a breath, gaze still on the screen. Give the pauses time to register. No mouse is present: use only the existing keyboard. Hands stay low throughout; never perform a flourish or hold raised curled fingers.
```

All submitted settings and the uploaded URL are preserved in the companion JSON. No other media inputs.

### 01-computer-sequence-wan-v2

Model: `wan/v2.6/image-to-video`; request ID: `01a0c68f-378a-72d3-ba44-cd5748010be1`.

Only file input: `artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png` in `image_url`.

```text
A single locked-off 15-second documentary shot of this woman quietly editing a document at her desktop. Preserve her exact appearance and room. Her gaze is directed at the monitor. Both wrists are supported on the black wrist cushion. Start with two seconds of reading, fingertips resting on the keys. Then enter a few words with very small, irregular finger presses for three seconds. Stop typing completely and read for three seconds, hands resting against the keyboard. One right fingertip taps a nearby key twice to navigate the document; the hand stays at its home-key position. Read briefly, then type one short correction. Finish resting on the keys, with a small relaxed shoulder settling. The only hand travel is the millimeters needed to press keys. Quiet face, closed mouth, occasional blink, minimal head motion. Forearms stay supported, fingers stay low and relaxed. Normal speed, unchanged camera framing throughout. Silent scene.
```

All submitted settings and the uploaded URL are preserved in the companion JSON. No other media inputs.

Movement clips reviewed for inspiration: 02 typing rhythm/contact, 03 screen-key gaze.

## Sample 02

Selected video request: `02-computer-sequence-kling-v1`; delivered range 0–15s.

Source: `artifacts/library-loop-computer-movement-studies-02/source-images/02-mouse-work.png`

Original source-image generation prompt:

```text
A candid unretouched documentary color photograph of an ordinary adult working at a computer, landscape 16:9, medium shot including entire head, seated torso, both forearms and hands and the input device. Natural daylight, normal exposure, realistic skin pores and fine lines, small asymmetries, ordinary flyaway hairs, genuine cloth weave and creases. Moderate depth of field: face and hands both in focus. Neutral absorbed working expression, closed mouth, eyes unmistakably looking at the computer display rather than the camera. Practical slightly forward seated posture, relaxed unequal shoulders. Neither a fashion portrait nor stock-photo smile, no makeup retouching, no cinematic bokeh, no logos. Anatomically normal five-finger hands with low natural knuckle arcs and short unpainted fingernails. A 51-year-old East Asian man with a salt-and-pepper close-cropped haircut, a few forehead lines and natural textured skin, clean shaven, wearing a rumpled muted burgundy polo shirt. Home office with a grey desk, cream plaster wall, simple window blind and shelves of worn manuals. Medium three-quarter view from the front-right of his desk, modestly elevated to see his right hand. A desktop computer monitor stands screen-left and is turned toward him at ordinary reading height. He looks intently at its middle. His right hand naturally cups a normal dark grey computer mouse on a dull blue fabric mousepad; palm rests on the mouse, thumb touches its left flank, index finger lies gently on the left button, middle finger on the right button, ring/little fingers softly wrap the right side. Mouse body clearly visible beneath the hand. Right forearm and heel of wrist supported on the mousepad/desk. His left hand rests softly beside a separate keyboard, with left forearm on desk. All hand-device contact clear. The mouse is close to his body, not stretched away. Stable ordinary workplace moment.
```

Image generation input files: **none**.

### 02-computer-sequence-kling-v1

Model: `fal-ai/kling-video/v3/pro/image-to-video`; request ID: `01a0c686-1175-7452-9888-02e296c9ef02`.

Only file input: `artifacts/library-loop-computer-movement-studies-02/source-images/02-mouse-work.png` in `start_image_url`.

```text
Single continuous 15-second candid shot at normal speed. Camera locked on tripod with absolutely unchanged framing. Preserve the source person, face, hairstyle, age, clothing, lighting, room and device geometry. Ordinary concentrated expression, relaxed closed mouth, natural blinks. Small movements, supported forearms, relaxed low wrists. The man alternates reading, mouse navigation and entering a short search phrase. 0–2 seconds: read the monitor, right hand comfortably cupping the mouse, left hand resting at keyboard. 2–4 seconds: move the mouse a small distance along the blue pad, index and middle fingers remaining on the buttons; stop and read. 4–6 seconds: right hand leaves the mouse along a low short path and settles gently onto the right letter keys, with forearm supported on desk; left hand stays on left keys. 6–9 seconds: type a short phrase with modest independent fingertip movements, eyes at the monitor. 9–10 seconds: pause with fingertips resting on keys. 10–12 seconds: right hand returns along the same low path and cups the stationary mouse naturally; make one small pointer movement. 12–13 seconds: a quiet reading pause, eyes focused on the display. 13–15 seconds: left hand enters two quiet key presses while right hand rests on mouse, and shoulders settle subtly with breathing. Distinct actions separated by genuine still moments; no repeated clicking, big finger lifts or head turns.
```

All submitted settings and the uploaded URL are preserved in the companion JSON. No other media inputs.

Movement clips reviewed for inspiration: 04 attentive gaze and restrained posture, 05 unequal hand roles; mouse grip itself is an untested extrapolation.

## Sample 03

Selected video request: `03-computer-sequence-wan-v3`; delivered range 0–9s.

Source: `artifacts/library-loop-computer-movement-studies-02/source-images/03-laptop-typing.png`

Original source-image generation prompt:

```text
A candid unretouched documentary color photograph of an ordinary adult working at a computer, landscape 16:9, medium shot including entire head, seated torso, both forearms and hands and the input device. Natural daylight, normal exposure, realistic skin pores and fine lines, small asymmetries, ordinary flyaway hairs, genuine cloth weave and creases. Moderate depth of field: face and hands both in focus. Neutral absorbed working expression, closed mouth, eyes unmistakably looking at the computer display rather than the camera. Practical slightly forward seated posture, relaxed unequal shoulders. Neither a fashion portrait nor stock-photo smile, no makeup retouching, no cinematic bokeh, no logos. Anatomically normal five-finger hands with low natural knuckle arcs and short unpainted fingernails. A 57-year-old woman with a short wavy dark-auburn bob streaked with grey, noticeable smile lines but no smile, and normal slightly uneven complexion. She wears a worn navy-blue linen blouse with sleeves rolled below the elbows. Seated on a simple upholstered chair at a pale birch table in a modest apartment study with a textured warm grey wall and a low bookshelf in the background. Medium side-three-quarter view, slightly above table height, both hands visible, face in three-quarter profile, her plain dark charcoal laptop on screen-left. The laptop screen is tilted at a practical reading angle and shows a dim neutral document without prominent lettering. Gaze goes down-left into the screen. Both forearms rest on table and both palm heels lie lightly on the laptop palm-rest; wrists straight and low. Left fingertips touch left letter keys, right fingertips touch right letter keys, each separate finger softly curved only a few millimeters above its neighboring keys. Laptop has ordinary keyboard and a rectangular trackpad separated below. Photograph a quiet actual typing posture, hands low on keys, no suspended whole hand.
```

Image generation input files: **none**.

### 03-computer-sequence-kling-v1

Model: `fal-ai/kling-video/v3/pro/image-to-video`; request ID: `01a0c686-1832-74e2-acbc-f88355d2c034`.

Only file input: `artifacts/library-loop-computer-movement-studies-02/source-images/03-laptop-typing.png` in `start_image_url`.

```text
Single continuous 15-second candid shot at normal speed. Camera locked on tripod with absolutely unchanged framing. Preserve the source person, face, hairstyle, age, clothing, lighting, room and device geometry. Ordinary concentrated expression, relaxed closed mouth, natural blinks. Small movements, supported forearms, relaxed low wrists. The woman reads and edits a document on her laptop. 0–2 seconds: eyes read the laptop screen, hands resting low on keys. 2–5 seconds: type a few words with small uneven individual finger presses, forearms supported on table. 5–6 seconds: pause, fingertips resting on keys. 6–9 seconds: right hand glides a short distance down to the rectangular trackpad below the letter keys; index fingertip visibly rests on the pad and makes one short smooth scroll, wrist heel supported on palm rest; left hand stays at keyboard. 9–11 seconds: hand rests on the trackpad while her eyes follow the screen, without a head nod. 11–14 seconds: right hand returns to its letter-key position and both hands enter a short correction with low fingertips. 14–15 seconds: hands relax in contact with keys and one small seated weight adjustment settles her shoulders. Keep mouth calmly closed. Make the transitions unhurried and physically connected, not a repeating typing loop.
```

All submitted settings and the uploaded URL are preserved in the companion JSON. No other media inputs.

### 03-computer-sequence-wan-v2

Model: `wan/v2.6/image-to-video`; request ID: `01a0c68f-381d-7373-bdec-b542f876d495`.

Only file input: `artifacts/library-loop-computer-movement-studies-02/source-images/03-laptop-typing.png` in `image_url`.

```text
A single locked-off 15-second documentary shot of this woman quietly working on her laptop. Preserve her exact appearance and room. Start by reading the laptop screen for two seconds, hands resting naturally on the keyboard. Type a few words with small irregular finger presses, then pause completely to read. Around the middle of the shot, her right hand slides down onto the laptop trackpad, keeping the heel of the hand supported on the palm rest. Her index finger lies flat on the trackpad and makes one short gentle scroll. The other fingers remain relaxed and close together; the left hand rests on the keys. Read for a moment with her right hand resting on the pad. Slide that hand back to the letter keys and type a brief correction, then rest both hands low on the keyboard. One small shoulder settling, otherwise quiet posture. Eyes stay directed toward the screen with only one brief keyboard glance. Relaxed closed mouth, natural blink, minimal head movement. Camera perfectly still, normal speed. Silent scene.
```

All submitted settings and the uploaded URL are preserved in the companion JSON. No other media inputs.

### 03-computer-sequence-wan-v3

Model: `wan/v2.6/image-to-video`; request ID: `01a0c694-a2ec-7240-b670-c7064251acd8`.

Only file input: `artifacts/library-loop-computer-movement-studies-02/source-images/03-laptop-typing.png` in `image_url`.

```text
One continuous 15-second candid shot. Locked camera. The woman quietly edits a document on her laptop. Her eyes read the laptop screen; her forearms rest on the table and her fingertips rest on the letter keys. Hold this attentive reading pause for the first three seconds. Type a short phrase with tiny, irregular individual key presses for about three seconds. Pause completely to check the screen for three seconds, with fingers resting where they stopped. Press one nearby key with a small finger movement, then enter a short correction for two seconds. Finish quietly reading the screen with resting hands and a barely perceptible shoulder settling. Both hands remain over their own halves of the letter keyboard throughout; all movements are localized to individual fingers, with relaxed low knuckles. One brief glance at the keyboard, then eyes return to the screen. Ordinary calm expression, closed mouth, natural blink. Preserve her identity, face, hair, clothing, lighting, furniture and laptop. Normal speed. Silent scene.
```

All submitted settings and the uploaded URL are preserved in the companion JSON. No other media inputs.

Movement clips reviewed for inspiration: 02 low localized typing, 05 forward posture/unequal timing, 04 subtle body adjustment.

Reference time ranges and observed-versus-hypothesized motion are preserved in `videos/computer-movement-long/reference-observations.json`. Mouse/trackpad choreography is an extrapolation from supported hand movement, not a motion capture or direct copy.
