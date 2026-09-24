"""Small, reusable shot contract. Prompts request continuity; images condition it.

Technique provenance and limitations: docs/CREW_REALISM_REPORT.md.
"""
from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .learning import recommend


@dataclass(frozen=True)
class ShotState:
    identity: str
    wardrobe: str
    environment: str
    lighting: str
    framing: str
    camera: str
    screen_position: str
    travel_direction: str
    pose: str
    prop_state: str


def validate_join(previous: ShotState, entry: ShotState, kind: str):
    if kind not in {'continuous', 'cutaway', 'intentional_cut'}:
        raise ValueError(f'Unknown join: {kind}')
    if kind == 'continuous':
        differences = [key for key, value in asdict(previous).items()
                       if value != asdict(entry)[key]]
        if differences:
            raise ValueError('Continuity mismatch: ' + ', '.join(differences))


def interview_prompt(entry: ShotState, exit: ShotState, line: str):
    if entry.identity != exit.identity or entry.wardrobe != exit.wardrobe:
        raise ValueError('A continuous interview cannot change identity or wardrobe')
    return (
        f'Continue the supplied camera frame as one documentary interview take. '
        f'SUBJECT: {entry.identity}; {entry.wardrobe}. Preserve the visible face, age, '
        'hairline, nose, asymmetry and skin texture of the reference; do not beautify or '
        'add new facial marks. Fine lines and uneven skin reflect the existing side light. '
        f'SET: {entry.environment}. LIGHT: {entry.lighting}. '
        f'CAMERA: {entry.framing}; {entry.camera}. '
        f'ENTRY: {entry.screen_position}; travel {entry.travel_direction}; '
        f'{entry.pose}; props {entry.prop_state}. '
        'PERFORMANCE: eyes attend to the same interviewer just camera-right, with tiny '
        'refocusing movements and unforced irregular blinking. Quiet breath moves the '
        'shoulders; one slight head inclination accompanies the thought, then settles. '
        'Hands rest low in her lap, not rigid; no finger-counting or presenting objects. '
        'Sleeve folds respond only to body movement; stray hairs remain settled in still air. '
        'Understated conversational delivery, not a broad smile or theatrical eyebrow lift. '
        f'AUDIO: say exactly once in natural British English: "{line}" '
        'Begin promptly, complete the thought without restarting, then let the lips '
        'close naturally for a brief listening pause. Quiet bakery room tone, no music. '
        f'EXIT: {exit.pose}; {exit.screen_position}; travel {exit.travel_direction}; '
        f'props {exit.prop_state}. Same light, set and camera throughout. '
        'No cuts, subtitles, titles, logos or graphic overlays.'
    )


def route_shot(use_case, *, has_reference=False, continuous=False,
               evidence_path=Path('artifacts/learning/core.json')):
    if use_case == 'exact_ui':
        return 'hyperframes'
    if use_case in {'interview', 'ugc_dialogue'} and not has_reference:
        raise ValueError('Establish a reviewed identity reference before recurring dialogue')
    if continuous and not has_reference:
        raise ValueError('Continuous action needs an actual entry reference')
    if evidence_path is not None and Path(evidence_path).is_file():
        case = {'hands': 'industrial_human', 'ugc_dialogue': 'ugc'}.get(use_case, use_case)
        data = json.loads(Path(evidence_path).read_text())
        route = recommend(data['runs'], case, has_reference=has_reference,
                          audio=use_case in {'interview', 'ugc_dialogue'})
        if route['endpoint']:
            return route['endpoint']
        raise ValueError('No compatible reviewed route; plan a bounded test for ' + use_case)
    if use_case in {'interview', 'ugc_dialogue'}:
        if not has_reference:
            raise ValueError('Establish a reviewed identity reference before recurring dialogue')
        return 'fal-ai/veo3.1/fast/image-to-video'
    if use_case == 'hands':
        if continuous and not has_reference:
            raise ValueError('Continuous action needs an actual entry reference')
        return 'fal-ai/kling-video/v3/pro/' + ('image-to-video' if has_reference else 'text-to-video')
    if use_case == 'exact_ui':
        return 'hyperframes'
    raise ValueError(f'Unreviewed use case: {use_case}')


def adapt_interview_input(endpoint, payload):
    """Keep schema differences explicit when evidence changes the selected model."""
    if endpoint == 'fal-ai/veo3.1/fast/image-to-video':
        return dict(payload)
    duration = str(payload['duration']).removesuffix('s')
    if endpoint == 'minimax/h3/image-to-video':
        seconds = int(duration)
        if not 5 <= seconds <= 15:
            raise ValueError('H3 duration must be between 5 and 15 seconds')
        return {'prompt': payload['prompt'], 'duration': seconds,
                'image_url': payload['image_url'], 'resolution': '768P',
                'prompt_expansion_mode': 'fast',
                **({'seed': payload['seed']} if 'seed' in payload else {})}
    common = {'prompt': payload['prompt'], 'duration': duration, 'generate_audio': True}
    if endpoint == 'fal-ai/kling-video/v3/pro/image-to-video':
        return {**common, 'start_image_url': payload['image_url'],
                'negative_prompt': payload.get('negative_prompt', 'blur, distort, and low quality')}
    if endpoint == 'bytedance/seedance-2.5/image-to-video':
        return {**common, 'image_url': payload['image_url'], 'resolution': '720p',
                'aspect_ratio': '16:9', **({'seed': payload['seed']} if 'seed' in payload else {})}
    raise ValueError('Endpoint needs a validated input adapter before generation: ' + endpoint)
