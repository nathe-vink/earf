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


# phase 2 (the coordinator, 2026-11-03 15:26, from the site lane's PICTURES-2026-11-03.md): the site's pictures the 40 do
# not replace. Each is an old rig turned into the final design by shots.py's strata_lit, as the site frames are
FIN = 'studio/shots/barkhorn/finals31/'
S31 = 'studio/shots/barkhorn/studio31/'
SPIN = dict(frames=9, step=10.0, start=-20.0, samples=32, scale=0.75, crop=[0.29, 0.04, 0.71, 0.97])  # spin47.py at 24770e2b
TURN_SAMPLES = 32                         # spin47's, which passed for the site's spin; the rig's 128 would be about 4x


def _final(shots, rig, fl, title, size=None, samples=None, rotate=None):
    s = shots.load(rig)
    blk = s['product'] if 'product' in s else s['products'][0]
    blk['flavour'] = fl
    for i in blk['instances']:
        i['flavour'] = fl
        if rotate is not None:
            i['rotate_z'] = i.get('rotate_z', 0) + rotate
    s = shots.strata_lit(s, glow=20.0)
    if 'rim' in s.get('lights', {}):
        s['lights']['rim']['power_w'] = 0.0               # as site(): the rim lamp made the formed horn read flat
    s['title'] = title
    if size:
        s['size'] = size
    if samples:
        s['render']['samples'] = samples
    return s


def phase2(base, horn):
    os.environ['TROPOS_BASE'] = base
    os.environ['TROPOS_HORN'] = horn
    sys.path.insert(0, HERE)
    import shots
    T = shots.SITE_TINTS                                   # tint: (flavour, the rigs' key)
    out = {}
    # 1. sound first: the front arc in Ice (the home's Sound), then the other tints
    for tint in ['ice'] + [t for t in T if t != 'ice']:
        fl, _ = T[tint]
        for k in range(SPIN['frames']):
            a = SPIN['start'] + k * SPIN['step']
            sh = _final(shots, S31 + f'hero-light-{tint}.json', fl, f'Tropos, the front arc, {tint}, frame {k}', samples=SPIN['samples'], rotate=a)
            sh['size'] = [round(sh['size'][0] * SPIN['scale']), round(sh['size'][1] * SPIN['scale'])]
            sh['render']['crop'] = SPIN['crop']
            out[f'spin-{tint}-{k:02d}'] = sh
    # 2. the dark-ground studio, Ember only (the debut page; the brand lane's invitation and teaser)
    out['studio-dark-ember'] = _final(shots, S31 + 'hero-dark-ember.json', 'cloud-red', 'Tropos, the dark-ground studio, Ember')
    # 3. the amplifier plate close up, one tint (the plate is the same on all eight)
    out['amp-plate-ember'] = _final(shots, FIN + 'amp-red.json', 'cloud-red', 'Tropos, the amplifier plate, horn A\'s back')
    # 4. horn A from behind, x 8: each tint's horn has its own depth, and the polished horn shows it
    for tint, (fl, key) in T.items():
        out[f'horn-back-{tint}'] = _final(shots, FIN + f'horn-back-{key}.json', fl, f'Tropos, horn A from behind, {tint}')
    # 5. the inside, one (Ice): the inside is the same build in every tint
    out['inside-ice'] = _final(shots, FIN + 'inside-blue.json', 'cloud-blue', 'Tropos, inside, Ice')
    # 6. the turning sprite, x 8, 24 frames each, at spin47's samples
    for tint, (fl, key) in T.items():
        for k in range(24):
            out[f'turn-{tint}-{k:02d}'] = _final(shots, FIN + f'turn/{key}-{k:02d}.json', fl, f'Tropos turning, {tint}, frame {k}', samples=TURN_SAMPLES)
    # 7. the close-ups that have rigs (each shown beside a whole-speaker picture): horn mouth, cabinet edge, plate, grip
    for name, rig, fl in (('macro-horn-acid', 'macro-horn-acid', 'cloud-amber'), ('macro-corner-ember', 'macro-corner-ember', 'cloud-red'),
                          ('macro-amp-dust', 'macro-amp-dust', 'cloud-orange'), ('macro-grip-poison', 'macro-grip-poison', 'eucalyptus-y2k-green')):
        out[name] = _final(shots, S31 + f'{rig}.json', fl, f'Tropos, {name}')
    # 8. the audit's other close-ups (the site lane, r47-site-next 7a8b5297): joinery, the back mark, the coin
    # joinery, Ember: tight on the front right vertical corner, where the side wall's polished edge meets the front panel
    # set back 24 behind it; the cabinet-edge macro's studio by daylight, 4:5 (the Cloud's frame: x 0.28, y -0.2137)
    j = _final(shots, S31 + 'macro-corner-ember.json', 'cloud-red', 'Tropos, joinery: two 20 mm walls meeting, Ember', size=[1280, 1600])
    j['camera'] = {'position': [0.58, -0.52, 0.53], 'target': [0.275, -0.205, 0.46], 'lens_mm': 100.0, 'level': True,
                   'fstop': 8.0, 'focus': [0.28, -0.214, 0.46]}
    out['joinery-ember'] = j
    # the back mark, Fog: site()'s back frame (mark variant A, 4f05e0be) square on to the back, the word about two thirds
    # of the frame's width (the mark is 140 mm across at z 0.80 on the back's face, y 0.2063), 4:5. Blind-read at 440 px
    b = shots.site('back', 'fog')
    b['title'] = 'Tropos, the back mark, Fog (variant A)'
    b['size'] = [1280, 1600]
    b['camera'] = {'position': [0.0, 0.79, 0.80], 'target': [0.0, 0.2063, 0.80], 'lens_mm': 100.0, 'level': True,
                   'fstop': 8.0, 'focus': [0.0, 0.2063, 0.80]}
    out['back-mark-fog'] = b
    # the coin, Ember: one coin standing on its edge, turned to the camera, about half the frame, 1:1, on the site's
    # paper seamless. Its reflections come from a studio environment and one broad soft key, not the small square
    # softbox that put the same square on every coin (the owner: "makes them look flat all over again")
    c = shots.load('studio/shots/barkhorn/coin/site-coins-paper.json')
    kit = c['set']['props'][0]
    kit['spots'] = [{'position': [0.0, 0.0, 0.0200], 'flavour': 'ember', 'rotate': [90.0, 0.0, 25.0]}]
    c['sky'] = {'kind': 'hdri', 'file': 'studio_small_03_1k', 'strength': 0.6, 'rotation_deg': 140.0}
    c['lights'] = {'key': {'type': 'area', 'size_m': [1.0, 0.7], 'orbit': {'azimuth_deg': -40, 'elevation_deg': 35, 'distance_m': 1.4},
                           'target': [0.0, 0.0, 0.02], 'irradiance': 2.0, 'color': '#FFF6EC', 'spread_deg': 60}}
    c['camera'] = {'position': [0.10, -0.20, 0.075], 'target': [0.0, 0.0, 0.02], 'lens_mm': 100.0, 'level': False,
                   'fstop': 11.0, 'focus': [0.0, 0.0, 0.02]}
    c['size'] = [1200, 1200]
    c['title'] = 'EARF coin, Ember, on its edge (its own reflection)'
    out['coin-ember'] = c
    # the eight in a row (the owner's note was about the coins plural): each standing on its edge at its own turn, so the
    # environment lands differently on each and no two carry the same reflection; the site's strip (7:1)
    r = json.loads(json.dumps(c))
    turns = [8.0, 52.0, -24.0, 31.0, -47.0, 14.0, 66.0, -9.0]
    r['set']['props'][0]['spots'] = [{'position': [round(-0.175 + 0.05 * k, 4), 0.0, 0.0200], 'flavour': fl, 'rotate': [90.0, 0.0, t]}
                                     for k, (fl, t) in enumerate(zip(['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke'], turns))]
    r['camera'] = {'position': [0.0, -0.62, 0.11], 'target': [0.0, 0.0, 0.02], 'lens_mm': 50.0, 'level': False, 'fstop': 11.0,
                   'focus': [0.0, 0.0, 0.02]}
    r['lights']['key']['orbit']['distance_m'] = 1.8
    r['size'] = [3700, 528]
    r['title'] = 'EARF coins, the eight on their edges (each its own reflection)'
    out['coins-eight'] = r
    return out


def minutes(s):
    w, h = s.get('size', [1200, 1500])
    c = s.get('render', {}).get('crop')
    area = (c[2] - c[0]) * (c[3] - c[1]) if c else 1.0      # a cropped render traces only its region
    return MIN_PER_MP64 * (w * h / 1e6) * area * s.get('render', {}).get('samples', 64) / 64.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True, choices=['A', 'D'])
    ap.add_argument('--horn', required=True, choices=['satin', 'polished'])
    ap.add_argument('--date', default='2026-11-04', help="the renders' folder date")
    ap.add_argument('--list', action='store_true', help='print the list only; write nothing')
    ap.add_argument('--phase', type=int, default=1, choices=[1, 2], help='1: the deck and the 40 site frames; 2: the rest of the site (phase2())')
    ap.add_argument('--hold', default='', help="leave out the shots whose names contain any of these, comma-separated (e.g. 'smoke' while Smoke's sheet is open)")
    ap.add_argument('--chunks', default=None, help="after writing, print the commands for these chunks, e.g. '1-4' or '2,5,7'")
    ap.add_argument('--split', type=int, default=0, help='propose a split of the chunks across N containers (the deck first, in container 1)')
    a = ap.parse_args()
    # each answer pair in its own process, so shots.py reads its own answers at import
    if os.environ.get('TROPOS_ROLLOUT_CHILD') != '1':
        env = {**os.environ, 'TROPOS_ROLLOUT_CHILD': '1'}
        sys.exit(subprocess.call([sys.executable, __file__] + sys.argv[1:], env=env))
    shots_ = build(a.base, a.horn) if a.phase == 1 else phase2(a.base, a.horn)
    held = [n for n in shots_ if any(h and h in n for h in a.hold.split(','))]
    for n in held:
        shots_.pop(n)
    if held:
        print(f'held back ({len(held)}): {", ".join(held)}')
    tag = f'{a.base}-{a.horn}' + ('' if a.phase == 1 else '-p2')
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
        for k in [k for k in pick if 1 <= k <= len(chunks)]:
            print(f'bash spinoffs/barkhorn/campaign/rollout/{tag}/queue-{k:02d}.sh   # {", ".join(chunks[k - 1])}  ~{cmin[k - 1]:.0f} min')


if __name__ == '__main__':
    main()
