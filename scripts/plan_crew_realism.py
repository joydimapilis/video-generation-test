"""Compile the bounded Crew pilot. No API calls; baseline requests stay untouched."""
import argparse
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path

from amarillo.shot_plan import ShotState, interview_prompt, route_shot, validate_join, adapt_interview_input


STATE = ShotState(
    identity='the reference bakery owner, greying dark hair tied back',
    wardrobe='cream long-sleeve shirt, flour-dusted charcoal apron, brown straps, lavalier unchanged',
    environment='same wood and tile bakery, bread shelves and window on screen right',
    lighting='unchanged warm morning daylight from screen right, stable exposure and white balance',
    framing='eye-level medium close-up with the original headroom and lens perspective',
    camera='locked tripod, no zoom, no pan',
    screen_position='seated center-left', travel_direction='stationary',
    pose='shoulders relaxed, head upright, mouth closed, gaze slightly camera-right',
    prop_state='microphone clipped to the same apron strap; hands empty below frame',
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--continuation-frame', type=Path)
    parser.add_argument('--control', action='store_true')
    parser.add_argument('--estimate-cents', type=int,
                        help='Fresh quote required if learned routing changes the endpoint.')
    args = parser.parse_args()
    baseline = json.loads(Path('configs/crew_round1.json').read_text())['runs']
    original = deepcopy(baseline[2 if args.continuation_frame or args.control else 1])
    original.update(id='realism_line5_control' if args.control else
                    'realism_line5_chained' if args.continuation_frame else 'realism_line4_v2', version=2)
    original['input']['prompt'] = interview_prompt(STATE, STATE, original['line'])
    original['input']['negative_prompt'] += ', beauty retouching, waxy skin, exaggerated eyebrows, finger counting, floating hair'
    endpoint = route_shot('interview', has_reference=True)
    if endpoint != original['endpoint']:
        if args.estimate_cents is None or args.estimate_cents <= 0:
            raise ValueError('Learned route changed to ' + endpoint + '; supply a fresh --estimate-cents quote')
        original['estimate_cents'] = args.estimate_cents
    original['endpoint'] = endpoint
    original['shot_plan'] = {'entry': asdict(STATE), 'exit': asdict(STATE),
                             'exit_is_requested_not_verified': True}
    runs = [original]
    if args.continuation_frame:
        if not args.continuation_frame.is_file():
            raise ValueError('Review and select a real exit frame before compiling continuation')
        validate_join(STATE, STATE, 'continuous')
        original['input']['image_url'] = 'local:' + str(args.continuation_frame)
        original['shot_plan']['join'] = 'continuous'
        original['shot_plan']['previous'] = 'realism_line4_v2'
    elif not args.control:
        hands = deepcopy(next(r for r in json.loads(Path('configs/rota_round1.json').read_text())['runs']
                              if r['id'] == 'broll_dough_v1'))
        hands.update(id='realism_dough_v2', version=2)
        hands['input']['prompt'] = (
            'One uninterrupted documentary close-up of a baker\'s two flour-dusted hands and '
            'one round of bread dough on a worn wooden bench. No face. Camera locked in '
            'a tight three-quarter view, warm morning side light from screen right, shallow '
            'depth of field. Real hand skin with creases, short nails and light flour in '
            'the creases, no jewelry. ONE measured action: palms settle on the near half '
            'of the dough, lean weight gently forward, compressing it against the bench; '
            'fingers remain curved together as the palms release; the elastic dough '
            'partly rebounds and stays on the bench. Finish with hands resting lightly '
            'alongside the dough for a brief beat. Bench stays fixed, flour smears where '
            'skin contacts it; no magical flour cloud. Wrists and forearms carry the '
            'force, no floating contact. No second kneading cycle, twisting, fast motion, '
            'extra hands, changing dough count, text or logos.'
        )
        hands['hypothesis'] = 'Compare a single preparation/contact/release chain with repeated turning and tucking; same model and settings, unseeded baseline.'
        runs.append(hands)
    original['input'] = adapt_interview_input(original['endpoint'], original['input'])
    target = Path('configs/crew_realism_' + ('control' if args.control else 'continuation' if args.continuation_frame else 'round1') + '.json')
    target.write_text(json.dumps({'experiment': 'crew-realism', 'budget_root': 'artifacts/library-loop-6',
        'runs': runs}, indent=2) + '\n')
    print(target)


if __name__ == '__main__':
    main()
