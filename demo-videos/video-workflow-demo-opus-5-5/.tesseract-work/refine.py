"""Refine whisper word times with measured speech islands: rescale each segment
to its measured speech extent, snap pause boundaries to measured gaps, and
interpolate between anchors. Writes transcripts/edit-words-refined.json."""
import json, itertools
from plan import timeline, A
from rms import rms_profile
tl, _ = timeline(); segs = {s['key']: s for s in tl}
words = json.load(open("transcripts/edit-words.json"))
out = []
for key, g in itertools.groupby(words, key=lambda w: w['seg']):
    g = list(g); s = segs[key]
    prof = rms_profile(A + s['file'], s['src_in'], s['src_out'] - s['src_in'], 0.01)
    on = [d > -45 for d in prof]
    isl = []; cur = None; gap = 0
    for i, v in enumerate(on):
        if v:
            if cur is None: cur = [i, i]
            cur[1] = i + 1; gap = 0
        elif cur is not None:
            gap += 1
            if gap >= 20: isl.append(cur); cur = None; gap = 0
    if cur: isl.append(cur)
    isl = [(s['start'] + a * 0.01, s['start'] + b * 0.01) for a, b in isl if (b - a) > 5]
    sp0, sp1 = isl[0][0], isl[-1][1]
    w0, w1 = g[0]['a'], max(w['b'] for w in g)
    f = lambda t: sp0 + (t - w0) * (sp1 - sp0) / (w1 - w0)
    for w in g: w['a'], w['b'] = f(w['a']), f(w['b'])
    anchors = [(w0, sp0)]  # (index-based anchors built below)
    idx_anchor = {0: ('a', sp0), len(g) - 1: ('b', sp1)}
    used = set()
    for (a0, b0), (a1, b1) in zip(isl, isl[1:]):
        gm = (b0 + a1) / 2
        best = None
        for i in range(len(g) - 1):
            if i in used: continue
            bm = (g[i]['b'] + g[i + 1]['a']) / 2
            pen = abs(bm - gm) - (0.25 if g[i]['w'][-1] in ',.?!' else 0)
            if best is None or pen < best[0]: best = (pen, i)
        if best and best[0] < 0.9:
            i = best[1]; used.add(i)
            g[i]['b'] = b0; g[i + 1]['a'] = a1
            g[i]['_endanchor'] = True; g[i + 1]['_startanchor'] = True
    g[0]['_startanchor'] = True; g[0]['a'] = sp0; g[-1]['b'] = sp1; g[-1]['_endanchor'] = True
    # piecewise-linear remap between anchor points using original (rescaled) starts
    pts = []
    for i, w in enumerate(g):
        if w.get('_startanchor'): pts.append((i, 'a'))
        if w.get('_endanchor'): pts.append((i, 'b'))
    # rebuild times: for each run between a start-anchor word i and its end-anchor word j, distribute by char count
    runs = []; i = 0
    while i < len(g):
        j = i
        while not g[j].get('_endanchor'): j += 1
        runs.append((i, j)); i = j + 1
    for i, j in runs:
        a, b = g[i]['a'], g[j]['b']
        lens = [max(2, len(w['w'].strip(',.'))) + 1.5 for w in g[i:j + 1]]
        tot = sum(lens); t = a
        for w, L in zip(g[i:j + 1], lens):
            d = (b - a) * L / tot; w['a'], w['b'] = round(t, 3), round(t + d, 3); t += d
    for w in g:
        w.pop('_startanchor', None); w.pop('_endanchor', None); out.append(w)
json.dump(out, open("transcripts/edit-words-refined.json", "w"), indent=0)
for key, g in itertools.groupby(out, key=lambda w: w['seg']):
    print(key, ' '.join(f"{w['w']}@{w['a']:.2f}" for w in g))
