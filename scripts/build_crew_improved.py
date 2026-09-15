"""Stage the selected revision without changing the original Crew deliverable."""
import json
from pathlib import Path
import shutil
import subprocess

import prepare_crew_assets as audio


PROJECT = Path('hyperframes/crew-improved')
LOOP = Path('artifacts/library-loop-6')


def main():
    selection = json.loads((LOOP / 'realism/selected/selection.json').read_text())
    if not selection['reviewed']:
        raise ValueError('A visually reviewed exit frame is required')
    join = 23 + selection['previous_cut_end']
    if abs(join - 28.125) > .001:
        raise ValueError('Update the editorial schedule for the new exit timestamp')
    assets = PROJECT / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    # Only local, already-paid footage. Keep the original render and project intact.
    for source in Path('hyperframes/crew/assets').iterdir():
        if source.is_file():
            shutil.copy2(source, assets / source.name)
    selected = {'line4': 'realism_line4_v2', 'line5': 'realism_line5_chained',
                'dough': 'realism_dough_v2'}
    for role, run_id in selected.items():
        shutil.copy2(LOOP / 'outputs' / (run_id + '.mp4'), assets / (role + '.mp4'))
    plan = json.loads((assets / 'audio-plan.json').read_text())
    for row in plan['dialogue_tracks']:
        if row['role'] == 'line4':
            row['duration'] = selection['previous_cut_end']
            row['volume'] = .9
        elif row['role'] == 'line5':
            row.update(data_start=join, duration=4.625, volume=.9)
        elif row['role'] == 'line6':
            row['data_start'] = 37.0
    for row in plan['caption_schedule']:
        if row['in'] == 23:
            row['out'] = 28.125
        elif row['in'] == 28.2:
            row.update({'in': join, 'out': 32.75})
            row['text'] = 'It builds the schedule around that, and everyone sees an update.'
        elif row['in'] >= 32.4:
            row['in'] = round(row['in'] + 4.6, 3)
            row['out'] = round(row['out'] + 4.6, 3)
    audio.DURATION = 49.0
    audio.synth_score(assets / 'score.wav')
    points = [{'t': 0, 'v': 0}, {'t': .4, 'v': .42}, {'t': 7.25, 'v': .42},
              {'t': 7.5, 'v': 1}, {'t': 9.05, 'v': 1}, {'t': 9.3, 'v': .42},
              {'t': 21.3, 'v': .42}, {'t': 21.55, 'v': 1}, {'t': 22.75, 'v': 1},
              {'t': 23, 'v': .42},
              # The revision opens a 4.25s hole between line5 and line6 that the
              # original cut did not have, and the score's loudest movement plays
              # underneath it. A full swell here measures 0.63x the quietest spoken
              # line - inside the delivery gate's 0.5x headroom rule - so this one
              # lift stops short of the others.
              {'t': 32.75, 'v': .42}, {'t': 33, 'v': .65},
              {'t': 36.75, 'v': .65}, {'t': 37, 'v': .42}, {'t': 43.2, 'v': .42},
              {'t': 43.5, 'v': 1}, {'t': 47, 'v': 1}, {'t': 49, 'v': 0}]
    plan['music_automation'] = {'version': 1, 'lanes': [{'target': 'volume', 'points': points}]}
    (assets / 'audio-plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    edit = {'duration': 49.0, 'video_cuts': [
        [1, 'hero', 0, 7.3, 0], [2, 'dough', 7.3, 2, 2.5],
        [3, 'line2', 9.3, 3.3, 1.1], [4, 'paper', 12.6, 3.1, .6],
        [5, 'linec', 15.7, 5.6, 0], [6, 'room', 21.3, 1.7, 1.2],
        [7, 'line4', 23, 5.125, 0], [13, 'line5', join, 2, 0],
        [10, 'line6', 37, 6, 0], [11, 'oven', 43, 2.5, 1.8]],
        'screen_a': [30.125, 2.625], 'screen_b': [32.75, 4.25], 'close': [45, 4],
        'brand_windows': [[0, 30.125], [43, 2]],
        'continuous_join': selection,
        'shot_handoffs': [
            {'from': 'hero', 'to': 'dough', 'kind': 'cutaway', 'entry': 'hands already weighted on dough', 'exit': 'hands release, dough remains on bench', 'reason': 'causal tactile insert, not asserted to be the speaker hands'},
            {'from': 'dough', 'to': 'line2', 'kind': 'cutaway', 'entry': 'same anchor interview setup', 'exit': 'sentence continues across paper cutaway'},
            {'from': 'line2', 'to': 'paper', 'kind': 'cutaway', 'entry': 'schedule texture and pencil marks', 'exit': 'same warm room, intentional detail change'},
            {'from': 'paper', 'to': 'linec', 'kind': 'cutaway', 'entry': 'restored interview composition', 'exit': 'end of complaint; no finger counting'},
            {'from': 'linec', 'to': 'room', 'kind': 'cutaway', 'entry': 'bakery environment', 'exit': 'warm interior context'},
            {'from': 'room', 'to': 'line4', 'kind': 'cutaway', 'entry': 'original identity anchor', 'exit': 'selected source frame at 5.125 seconds'},
            {'from': 'line4', 'to': 'line5', 'kind': 'continuous', 'entry': 'actual preceding exit image', 'exit': 'dialogue continues beneath availability screen'},
            {'from': 'line5', 'to': 'screen_a', 'kind': 'cutaway', 'entry': 'authored availability, same narrator sound bridge', 'exit': 'completed available staff list'},
            {'from': 'screen_a', 'to': 'screen_b', 'kind': 'intentional_cut', 'entry': 'same palette, grid and type scale', 'exit': 'schedule populated, availability constraints retained'},
            {'from': 'screen_b', 'to': 'line6', 'kind': 'cutaway', 'entry': 'common identity anchor', 'exit': 'quiet smile after payoff'},
            {'from': 'line6', 'to': 'oven', 'kind': 'cutaway', 'entry': 'warm light and bread motif', 'exit': 'bread clear of oven'},
            {'from': 'oven', 'to': 'close', 'kind': 'intentional_cut', 'entry': 'existing half-second fade to brand', 'exit': 'legible brand hold'}]}
    (PROJECT / 'edit-plan.json').write_text(json.dumps(edit, indent=2) + '\n')
    peak = audio.predict_mix_peak(assets, plan['music_automation'], plan['score_volume'], plan['dialogue_tracks'])
    if peak >= .98:
        raise ValueError(f'Predicted audio clipping: {peak}')
    subprocess.run([str(Path('.venv/bin/python').resolve()),
                    str(Path('scripts/build_crew_composition.py').resolve())], cwd=PROJECT, check=True)
    (LOOP / 'realism/selected-assets.json').write_text(json.dumps({
        'replacements': selected, 'original_preserved': 'artifacts/final_outcome/crew/crew-final.mp4',
        'predicted_audio_peak': peak, 'duration': 49.0}, indent=2) + '\n')
    print('Built revised film; predicted per-channel peak', peak)


if __name__ == '__main__':
    main()
