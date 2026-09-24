# Computer movement studies 02 — exact generation audit

Verified against all 11 persisted requests, the submission/upload code, and the selected-output manifest. The four source-image calls were text-only. Each of the seven image-to-video calls supplied exactly one newly generated PNG through `image_url`. No real reference video, extracted reference frame, reference first/last frame, pose map, or motion-control input was submitted.

The collection called human-movements in the request is stored at `references/human-realism/`. Frames/contact sheets were extracted and inspected locally to form written directions; they were not generation inputs. `reference_observations` is local run metadata outside the submitted `input` object; that JSON file was not uploaded.

Remote check: 11/11 provider image URLs were downloaded and matched their local SHA-256 hashes. This covers all four provider-generated source-image results and all seven uploaded I2V source-image inputs.

Evidence limits: these are persisted client request records and current submission code, not independent provider-side logs. Newly generated means no supplied-media conditioning for the stills, followed by animation conditioned only on each generated still. It does not mean the resulting video is independent of its own source image.

## 01-desktop-reading

Delivered range: 2.166667s to 3.666667s of `01-desktop-typing-veo-standard-v3`. Duration 1.5s.

Source model: `fal-ai/nano-banana-pro`; request `01a0b9cd-4590-7470-a9db-f981cf26a728`. Settings: 2K, 16:9, PNG, one image. No input file and no image reference.

### Exact source-image prompt

```text
Candid realistic unretouched documentary photo, landscape 16:9. An ordinary 43-year-old Black woman with short loosely tied natural curls, freckles and under-eye texture, wearing a faded sage-green cotton overshirt over a grey T-shirt, seated at a walnut laminate desk in a modest office with corkboard and folders. Neutral task-focused face, eyes looking at the desktop monitor on screen-left, not at camera. Medium three-quarter view including face, torso, both full hands and keyboard, camera slightly above desk. Soft ordinary window light, realistic skin pores and cotton creases; no glamour, smile, retouching or dramatic bokeh. IMPORTANT physical pose: A separate very thin matte-black keyboard sits flat on the desk with a thick black padded wrist-rest flush against its near edge. Both forearms lie on the desk; the heels of both palms are visibly resting on the padded support. Hands are low and relaxed, fingers almost extended with only a very shallow curve. Fingertip pads touch the letter keys lightly; knuckles do not arch high. Left hand on left letters, right hand on right letters, thumbs resting near the spacebar. All fingers visible and normal, no curled or dangling fingers. Both wrists supported at the same level as the keys, clearly showing contact with the pad. She is an experienced quiet typist caught between two small key presses. Still image only, no motion blur. Normal desktop monitor and desk geometry, hands fully unobscured.
```

Video model: `fal-ai/veo3.1/image-to-video`; request `01a0b9d4-32d1-7571-b0fe-c9b96763834d`. Settings: duration 6s, 1080p, 16:9, audio false, seed 71912, auto_fix false.

### Exact image-to-video motion prompt

```text
Locked static camera, six seconds of a woman quietly proofreading on her desktop computer, normal speed. Preserve this photograph exactly in character, desk layout, natural skin, clothes and lighting. Both hands are relaxed with their fingertips resting on the keyboard and the heels of her hands supported by the black padded wrist rest. During the first second her right index finger gently presses a key twice with only millimeters of movement; all other fingers remain resting. For the rest of the shot she reads the screen attentively, hands staying relaxed in their original contact positions. Her eyes make tiny reading movements along the monitor and one natural blink. Subtle breathing in the chest, a barely perceptible shoulder settling. Her head remains directed toward the monitor throughout. Quiet unposed concentration, closed relaxed mouth. Continuous single shot, absolutely stationary camera.
```

Negative prompt:

```text
continuous typing, rapid typing, finger flutter, piano fingers, high finger lifts, hovering hands, hands leaving keyboard, hands leaving wrist rest, head nods, looking down, repetitive movements, speaking, smile, beauty filter, camera motion, cuts
```

### Every file input

Source-image generation: **none**.

Image-to-video generation: **one file only**:

- [`artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png`](../artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png)
- Request field: `image_url` (starting/source image, newly generated; not a frame from real footage).
- SHA-256: `f350ac3c82895907cd79345d93fbfe415654c8057fb918e43482810a62ecef31`
- Exact uploaded URL: `https://v3b.fal.media/files/b/0aab0e08/-E-wIlnD88uNRFbO_83eE_01-desktop-typing-v2.png`

No additional first/last frame, reference video, extracted real frame, pose reference, motion map/control, identity image, or reference-notes file.

### Movement inspiration reviewed locally

- `references/human-realism/human-reference-02.mp4`, 0–2s: Uneven finger activity, low wrists, supported forearms.
- `references/human-realism/human-reference-03.mp4`, 0–2.5s and 5–7s: Screen/keyboard gaze checks and return of attention to screen.

The delivered desktop file is a trim of **v3**, using source image **v2**. The subsequent four-second **v4** reading-only request was rejected and is not the delivered video. Source v2 was another text-to-image generation, not an edit of source v1.

## 02-mouse-work

Delivered range: 0.000000s to 6.000000s of `02-mouse-work-veo-standard-v2`. Duration 6s.

Source model: `fal-ai/nano-banana-pro`; request `01a0b9c6-c921-7421-93db-cd001488b26b`. Settings: 2K, 16:9, PNG, one image. No input file and no image reference.

### Exact source-image prompt

```text
A candid unretouched documentary color photograph of an ordinary adult working at a computer, landscape 16:9, medium shot including entire head, seated torso, both forearms and hands and the input device. Natural daylight, normal exposure, realistic skin pores and fine lines, small asymmetries, ordinary flyaway hairs, genuine cloth weave and creases. Moderate depth of field: face and hands both in focus. Neutral absorbed working expression, closed mouth, eyes unmistakably looking at the computer display rather than the camera. Practical slightly forward seated posture, relaxed unequal shoulders. Neither a fashion portrait nor stock-photo smile, no makeup retouching, no cinematic bokeh, no logos. Anatomically normal five-finger hands with low natural knuckle arcs and short unpainted fingernails. A 51-year-old East Asian man with a salt-and-pepper close-cropped haircut, a few forehead lines and natural textured skin, clean shaven, wearing a rumpled muted burgundy polo shirt. Home office with a grey desk, cream plaster wall, simple window blind and shelves of worn manuals. Medium three-quarter view from the front-right of his desk, modestly elevated to see his right hand. A desktop computer monitor stands screen-left and is turned toward him at ordinary reading height. He looks intently at its middle. His right hand naturally cups a normal dark grey computer mouse on a dull blue fabric mousepad; palm rests on the mouse, thumb touches its left flank, index finger lies gently on the left button, middle finger on the right button, ring/little fingers softly wrap the right side. Mouse body clearly visible beneath the hand. Right forearm and heel of wrist supported on the mousepad/desk. His left hand rests softly beside a separate keyboard, with left forearm on desk. All hand-device contact clear. The mouse is close to his body, not stretched away. Stable ordinary workplace moment.
```

Video model: `fal-ai/veo3.1/image-to-video`; request `01a0b9cd-4be6-70a1-8a86-76893405ccb3`. Settings: duration 6s, 1080p, 16:9, audio false, seed 71911, auto_fix false.

### Exact image-to-video motion prompt

```text
Static tripod shot, six seconds at normal real-time speed. Animate the supplied photograph as a quiet candid moment of computer work. The seated man uses the mouse to move the pointer while his eyes follow a small area of the monitor. His right hand keeps its relaxed cupped shape around the mouse for the entire shot: index and middle fingertips lie on their buttons, other fingers and palm maintain contact with the shell. Hand and mouse move together as one supported unit in two very small smooth slides on the blue pad, with a short reading pause between them. The mouse always rests flat on the pad and the wrist rests low on the desk. This is pointer movement only, with the fingers resting quietly rather than clicking. His left hand stays relaxed at the keyboard. One natural blink and a tiny breathing adjustment keep the face and shoulders alive without a head turn. Keep the original face, natural skin, clothing, room and exact camera framing. Work quietly continues at the end.
```

Negative prompt:

```text
raised index finger, finger tapping, clicking, fingers leaving mouse, floating hand, mouse lifting off pad, exaggerated gestures, head bobbing, looking at camera, speech, beauty retouching, camera movement, cuts
```

### Every file input

Source-image generation: **none**.

Image-to-video generation: **one file only**:

- [`artifacts/library-loop-computer-movement-studies-02/source-images/02-mouse-work.png`](../artifacts/library-loop-computer-movement-studies-02/source-images/02-mouse-work.png)
- Request field: `image_url` (starting/source image, newly generated; not a frame from real footage).
- SHA-256: `08434a07e8d353ae95b87aa899343d0079bb2d460d69a0ba7310d82b294b546c`
- Exact uploaded URL: `https://v3b.fal.media/files/b/0aab0ddb/_RUnRvEPp_lO7i-qmOspW_02-mouse-work.png`

No additional first/last frame, reference video, extracted real frame, pose reference, motion map/control, identity image, or reference-notes file.

### Movement inspiration reviewed locally

- `references/human-realism/human-reference-04.mp4`, 0–2.8s: Attentive gaze and restrained head/shoulder movement.
- `references/human-realism/human-reference-05.mp4`, 0–3s and 7–9s: Unequal hand roles and local repositioning. External mouse grip/click was an extrapolation, not directly observed.

## 03-laptop-typing

Delivered range: 0.000000s to 6.000000s of `03-laptop-typing-veo-standard-v1`. Duration 6s.

Source model: `fal-ai/nano-banana-pro`; request `01a0b9c6-cb71-7663-8c28-6f4801d66351`. Settings: 2K, 16:9, PNG, one image. No input file and no image reference.

### Exact source-image prompt

```text
A candid unretouched documentary color photograph of an ordinary adult working at a computer, landscape 16:9, medium shot including entire head, seated torso, both forearms and hands and the input device. Natural daylight, normal exposure, realistic skin pores and fine lines, small asymmetries, ordinary flyaway hairs, genuine cloth weave and creases. Moderate depth of field: face and hands both in focus. Neutral absorbed working expression, closed mouth, eyes unmistakably looking at the computer display rather than the camera. Practical slightly forward seated posture, relaxed unequal shoulders. Neither a fashion portrait nor stock-photo smile, no makeup retouching, no cinematic bokeh, no logos. Anatomically normal five-finger hands with low natural knuckle arcs and short unpainted fingernails. A 57-year-old woman with a short wavy dark-auburn bob streaked with grey, noticeable smile lines but no smile, and normal slightly uneven complexion. She wears a worn navy-blue linen blouse with sleeves rolled below the elbows. Seated on a simple upholstered chair at a pale birch table in a modest apartment study with a textured warm grey wall and a low bookshelf in the background. Medium side-three-quarter view, slightly above table height, both hands visible, face in three-quarter profile, her plain dark charcoal laptop on screen-left. The laptop screen is tilted at a practical reading angle and shows a dim neutral document without prominent lettering. Gaze goes down-left into the screen. Both forearms rest on table and both palm heels lie lightly on the laptop palm-rest; wrists straight and low. Left fingertips touch left letter keys, right fingertips touch right letter keys, each separate finger softly curved only a few millimeters above its neighboring keys. Laptop has ordinary keyboard and a rectangular trackpad separated below. Photograph a quiet actual typing posture, hands low on keys, no suspended whole hand.
```

Video model: `fal-ai/veo3.1/image-to-video`; request `01a0b9c8-8350-72c2-8b9d-2e00edcf9f6f`. Settings: duration 6s, 1080p, 16:9, audio false, seed 71902, auto_fix false.

### Exact image-to-video motion prompt

```text
A locked-off six-second documentary shot at real-time speed. Preserve this woman, her age, skin texture, grey-streaked bob, navy linen blouse, laptop and room exactly as established by the new input photograph. She types a short passage while looking at the laptop screen. Fingers press neighboring keys independently in small irregular groups close to the keyboard surface; some fingertips stay resting on keys while others press. Both forearms remain supported on the table and the wrists keep their low working position. Brief hesitations separate words but she continues working rather than making a finishing gesture. Her eyes refocus subtly on different lines of the laptop screen, with one ordinary blink. One small breath slightly changes her shoulders and sleeve folds, without leaning back or nodding. At the end she is still seated and typing comfortably. The laptop and all background edges remain fixed in the frame.
```

Negative prompt:

```text
floating wrists, lifted hands, exaggerated finger curling, hand gestures, head bobbing, looking at camera, talking, beauty retouching, camera movement, zoom, slow motion, cuts
```

### Every file input

Source-image generation: **none**.

Image-to-video generation: **one file only**:

- [`artifacts/library-loop-computer-movement-studies-02/source-images/03-laptop-typing.png`](../artifacts/library-loop-computer-movement-studies-02/source-images/03-laptop-typing.png)
- Request field: `image_url` (starting/source image, newly generated; not a frame from real footage).
- SHA-256: `a7372c80e86fc20a9ba737303ef58f9808da1ac20e892fa26fe92d09e0f9741f`
- Exact uploaded URL: `https://v3b.fal.media/files/b/0aab0dbb/iFp3oaFy6KE3GRtXUQ-RG_03-laptop-typing.png`

No additional first/last frame, reference video, extracted real frame, pose reference, motion map/control, identity image, or reference-notes file.

### Movement inspiration reviewed locally

- `references/human-realism/human-reference-02.mp4`, 0–2s: Localized independent typing and low wrists.
- `references/human-realism/human-reference-05.mp4`, 0–3s and 7–9s: Forward posture and unequal hand timing.
- `references/human-realism/human-reference-04.mp4`, 0–2.8s: Subtle body adjustment and screen attention.

## All attempts, including rejected takes

| Request | Stage | File inputs | Delivered? |
| --- | --- | --- | --- |
| `01-desktop-typing-source-v1` | text-to-image | None | No |
| `02-mouse-work-source-v1` | text-to-image | None | Selected lineage |
| `03-laptop-typing-source-v1` | text-to-image | None | Selected lineage |
| `01-desktop-typing-veo-standard-v1` | image-to-video | `artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing.png` | No |
| `02-mouse-work-veo-standard-v1` | image-to-video | `artifacts/library-loop-computer-movement-studies-02/source-images/02-mouse-work.png` | No |
| `03-laptop-typing-veo-standard-v1` | image-to-video | `artifacts/library-loop-computer-movement-studies-02/source-images/03-laptop-typing.png` | Selected lineage |
| `02-mouse-work-veo-standard-v2` | image-to-video | `artifacts/library-loop-computer-movement-studies-02/source-images/02-mouse-work.png` | Selected lineage |
| `01-desktop-typing-source-v2` | text-to-image | None | Selected lineage |
| `01-desktop-typing-veo-standard-v2` | image-to-video | `artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png` | No |
| `01-desktop-typing-veo-standard-v3` | image-to-video | `artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png` | Selected lineage |
| `01-desktop-reading-veo-standard-v4` | image-to-video | `artifacts/library-loop-computer-movement-studies-02/source-images/01-desktop-typing-v2.png` | No |

Complete exact payloads for all 11 attempts, queue IDs, remote hash checks, and reference observations: [machine-readable audit](computer-movement-studies-02-generation-audit.json).

Review method: chronological extracted frames/contact sheets; 8fps detail for reference 02/05 and 2fps context for 03/04. This was sampled visual inspection, not continuous playback. No training, fine-tuning, pose extraction, or direct motion transfer was performed.
