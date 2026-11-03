"""Tropos's roll-out queue (2026-11-03): every deck and site shot that changes with the two open answers, the base (A: its
own feet, no light; D: the lantern built in) and the horn's outside (satin, the owner's spec; polished), written as shot
files with one command, and a render queue in chunks that each fit one tracked task. It writes shot files only; it never
renders.

    python3 spinoffs/barkhorn/campaign/rollout.py --base A --horn satin
    python3 spinoffs/barkhorn/campaign/rollout.py --base D --horn polished --list

writes spinoffs/barkhorn/campaign/rollout/<base>-<horn>/: one JSON per shot, `queue-NN.sh` (each chunk's renders one
after another, about 100 estimated minutes, under the 2-hour task limit) and `README.md` (the list, the sizes, the
estimates). Then run each chunk as its own tracked background task, one at a time:

    bash spinoffs/barkhorn/campaign/rollout/A-satin/queue-01.sh

What changes with the answers (shots.py, `strata_lit`):
- **base A:** the cabinet on its own swivel feet, no plinth and no light;
- **base D:** the same, with the built-in light's parts (option "Built-in light", "Built-in floor", "Floor film"), off in
  every day frame; and a night lantern frame for each tint, from gate 3's D night v2 (`gate2/D-night-ice-v2.shot.json`);
- **horn polished:** the waveguide's outside at roughness 0.05 instead of the satin 0.25.
"""
import argparse, copy, json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LANTERN = 'renders/2026-11-03/barkhorn/base-question/gate2/D-night-ice-v2.shot.json'
HERO = 'renders/2026-11-03/barkhorn/base-question/gate2/A-ice.shot.json'
# the render's own minutes per megapixel per 64 samples on this machine (CPU Cycles), from today's frames: a 1200 x 1500
# frame at 64 samples took 14 to 18 min alone; scaled by pixels and samples, a rough guide, not a promise
MIN_PER_MP64 = 9.0
CHUNK_MIN = 100.0


def build(base, horn):
    os.environ['TROPOS_BASE'] = base
    os.environ['TROPOS_HORN'] = horn
    sys.path.insert(0, HERE)
    import shots                                          # reads the answers at import
    out = {}
    # the deck's hero from gate 2's A (its studio, camera and polish passed 3/3), in Ember at the deck's 2:3: shots.py's
    # deck_hero still builds the old stepped Strata on the lit plinth (base_lit). Its 2:3 crop wants one framing proof
    h = json.load(open(os.path.join(ROOT, HERO)))
    for blk in h['products']:
        blk['flavour'] = 'cloud-red'
        for i in blk['instances']:
            i['flavour'] = 'cloud-red'
            if 'variants' in blk['def']:
                i['options'] = list(shots.D_OPTIONS) if base == 'D' else []
    mats = h.setdefault('materials', {})
    if base == 'D':
        mats.update({k: {'glow': 0.0} for k in shots.D_GLOW})        # off by day
    if horn == 'polished':
        mats['horn-satin'] = {**mats.get('horn-satin', {}), 'roughness': 0.05}
    h.update({'title': f'Tropos, the deck hero, Ember ({base}, {horn} horn)', 'size': [1440, 2160]})
    h['render']['samples'] = 192
    out['deck-hero'] = h
    for name in ('deck-row', 'deck-cover', 'deck-home', 'deck-home-portrait'):
        out[name] = shots.SHOTS[name]()
    for frame in shots.SITE_FRAMES:
        for tint in shots.SITE_TINTS:
            out[f'site-{frame}-{tint}'] = shots.site(frame, tint)
    if base == 'D':
        src = json.load(open(os.path.join(ROOT, LANTERN)))
        for tint, (fl, _) in shots.SITE_TINTS.items():
            s = copy.deepcopy(src)
            for blk in s['products']:
                blk['flavour'] = fl
                for i in blk['instances']:
                    i['flavour'] = fl
            if tint == 'smoke':                           # Smoke at night: 6500 K, neutral, a stop up (gate 2)
                for k in shots.D_GLOW:
                    s['materials'][k]['glow_color'] = '#FFFFFF'
                s['render'].update({'exposure': s['render']['exposure'] + 1.0, 'white_balance_k': 6500, 'white_balance_tint': 0.0})
            if horn == 'polished':
                s['materials']['horn-satin'] = {'roughness': 0.05}
            s['title'] = f'Tropos, the lantern at night, {tint} (D)'
            out[f'lantern-{tint}'] = s
    return out


def minutes(s):
    w, h = s.get('size', [1200, 1500])
    return MIN_PER_MP64 * (w * h / 1e6) * s.get('render', {}).get('samples', 64) / 64.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True, choices=['A', 'D'])
    ap.add_argument('--horn', required=True, choices=['satin', 'polished'])
    ap.add_argument('--date', default='2026-11-04', help="the renders' folder date")
    ap.add_argument('--list', action='store_true', help='print the list only; write nothing')
    ap.add_argument('--chunks', default=None, help="after writing, print the commands for these chunks, e.g. '1-4' or '2,5,7'")
    ap.add_argument('--split', type=int, default=0, help='propose a split of the chunks across N containers (the deck first, in container 1)')
    a = ap.parse_args()
    # each answer pair in its own process, so shots.py reads its own answers at import
    if os.environ.get('TROPOS_ROLLOUT_CHILD') != '1':
        env = {**os.environ, 'TROPOS_ROLLOUT_CHILD': '1'}
        sys.exit(subprocess.call([sys.executable, __file__] + sys.argv[1:], env=env))
    shots_ = build(a.base, a.horn)
    tag = f'{a.base}-{a.horn}'
    rows = [(n, s.get('size'), s.get('render', {}).get('samples'), minutes(s)) for n, s in shots_.items()]
    total = sum(r[3] for r in rows)
    print(f'{tag}: {len(rows)} shots, about {total / 60:.1f} h of rendering')
    if a.list:
        for n, size, smp, m in rows:
            print(f'  {n:28s} {size[0]} x {size[1]}  {smp} samples  ~{m:.0f} min')
        return
    od = os.path.join(HERE, 'rollout', tag)
    os.makedirs(od, exist_ok=True)
    rd = f'renders/{a.date}/barkhorn/rollout/{tag}'
    chunks, cur, cm = [], [], 0.0
    for n, s in shots_.items():
        json.dump(s, open(os.path.join(od, f'{n}.json'), 'w'), indent=1)
        m = minutes(s)
        if cur and cm + m > CHUNK_MIN:
            chunks.append(cur); cur, cm = [], 0.0
        cur.append(n); cm += m
    if cur:
        chunks.append(cur)
    for k, names in enumerate(chunks, 1):
        lines = ['#!/bin/bash', f'# {tag}, chunk {k} of {len(chunks)}: one render after another (run it as one tracked task)',
                 'set -e', 'cd "$(git rev-parse --show-toplevel)"', f'mkdir -p {rd}']
        for n in names:
            lines.append(f'python3 studio/engine/render.py spinoffs/barkhorn/campaign/rollout/{tag}/{n}.json --out {rd}/{n}.png')
        open(os.path.join(od, f'queue-{k:02d}.sh'), 'w').write('\n'.join(lines) + '\n')
    md = [f'# Roll-out: base {a.base}, horn {a.horn}', '',
          f'{len(rows)} shots, about {total / 60:.1f} h of rendering in {len(chunks)} chunks. Written by `rollout.py --base {a.base} '
          f'--horn {a.horn}`. Run each `queue-NN.sh` as its own tracked task, one at a time. The PNGs go to `{rd}/`.', '',
          '| shot | size | samples | est. min | chunk |', '|---|---|---|---|---|']
    where = {n: k for k, names in enumerate(chunks, 1) for n in names}
    for n, size, smp, m in rows:
        md.append(f'| {n} | {size[0]} x {size[1]} | {smp} | {m:.0f} | {where[n]:02d} |')
    open(os.path.join(od, 'README.md'), 'w').write('\n'.join(md) + '\n')
    print(f'wrote {od}: {len(rows)} shot files, {len(chunks)} queue chunks')
    cmin = [sum(minutes(shots_[n]) for n in names) for names in chunks]
    if a.split:
        # the deck's chunks to container 1 first, then each chunk to the container with the least time so far
        load = [0.0] * a.split; own = [[] for _ in range(a.split)]
        deck = [k for k, names in enumerate(chunks) if all(n.startswith('deck-') for n in names)]
        for k in deck:
            own[0].append(k + 1); load[0] += cmin[k]
        for k in sorted((k for k in range(len(chunks)) if k not in deck), key=lambda k: -cmin[k]):   # largest first
            c = min(range(a.split), key=lambda i: load[i])
            own[c].append(k + 1); load[c] += cmin[k]
        own = [sorted(o) for o in own]
        print(f'split across {a.split} containers:')
        for i in range(a.split):
            print(f'  container {i + 1}: chunks {",".join(str(x) for x in own[i])}  ~{load[i] / 60:.1f} h')
    if a.chunks:
        pick = []
        for part in a.chunks.split(','):
            lo, _, hi = part.partition('-')
            pick += list(range(int(lo), int(hi or lo) + 1))
        for k in pick:
            print(f'bash spinoffs/barkhorn/campaign/rollout/{tag}/queue-{k:02d}.sh   # {", ".join(chunks[k - 1])}  ~{cmin[k - 1]:.0f} min')


if __name__ == '__main__':
    main()
