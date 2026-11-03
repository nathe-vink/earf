"""Smoke's habitat, re-composed to sit with the other seven (r48-biomes, the owner's note of 2026-11-01).

    python3.11 spinoffs/barkhorn/biomes/smoke_align.py WORKTREE landscape|portrait --out OUT.png [--samples 128] [--scale 1]

The owner, on seeing the eight habitats side by side: "The smoke image looks like the odd one out now, in terms of
speaker positioning in its setting. Anyway to align it with the rest? Maybe the fire in front is preventing it from
looking right."

The other seven portraits put the speaker at 0.51 of the width (median), 0.41 of the height, its feet on the line at
0.79, seen at about eye level (README, "Smoke aligned"). This takes E12r p19's own shot (the meteor on the overpass at
dusk, from the r31-element-smoke-e10 worktree WORKTREE at d55e7570) and changes only the composition:
- the speaker comes up out of its crater onto the intact road 2.4 m toward the camera, upright, turned to it, its
  feet a few millimetres into the asphalt's dust;
- the crater, the fire, the plume and the trench stay where they were, behind it, so the fire rises behind and over
  its top and the trench runs in from behind;
- nothing in front: the field of slabs thrown forward and the debris spread ahead of the crater are left out;
- the camera is the other habitats': 60 mm from 6.5 m at 0.95 m (landscape), 92 mm (portrait).
The speaker is linked from the speaker lane's asset (assets/horn2/tropos.blend, r33-speaker-horn c77460f0, cover
off): the engine's own model is still built, so the shot's lamps find their parts by name, but hidden, and the linked
Tropos Smoke stands in its place in each lamp's light linking.
"""
import argparse, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, 'assets', 'horn3', 'tropos-strata.blend')   # r33-speaker-horn a6dc9296 (Strata, horn A, uplit plinth, stock tints); not in git
COLLECTION = 'Tropos Strata Smoke'
LIGHT_SCALE = {}                       # --light NAME=FACTOR
BACKLIGHT = [0.0]                      # --backlight irradiance
BLACK_LINING = False                  # --black-lining
SPOT = (0.0, -2.4)                    # where the speaker now stands (the crater is at the origin)
TURN = -22.0                          # its front turned toward the camera's side
# the speaker's box in each frame (fractions, x0 y0 x1 y1 from the top left), measured on the proofs, with a margin
SPEAKER_BOX = {'portrait': [0.355, 0.355, 0.64, 0.80], 'landscape': [0.39, 0.225, 0.60, 0.79]}


def compose(sh, frame):
    inst = sh['product']['instances'][0]
    inst['position'] = [SPOT[0], SPOT[1], -0.006]
    inst['rotate_z'] = TURN
    inst['tilt'] = [0.0, 0.0]
    keep = []
    for p in sh['set']['props']:
        if p.get('fn') == 'slabs' and abs(p.get('y0', 0) - 0.3) < 1e-6:
            continue                                               # the slabs thrown forward of the crater
        if p.get('fn') == 'debris':
            p = dict(p, ahead=0.0, forward=0.0, count=int(p.get('count', 100) * 0.6))
        keep.append(p)
    sh['set']['props'] = keep
    az = math.radians(-12.0)
    d = 6.5
    cam = {'position': [round(SPOT[0] + d * math.sin(az), 4), round(SPOT[1] - d * math.cos(az), 4), 0.95],
           'target': [SPOT[0], SPOT[1], 0.66 if frame == 'landscape' else 0.86],
           'lens_mm': 60 if frame == 'landscape' else 92, 'level': True, 'fstop': 4.0,
           'focus': [SPOT[0], SPOT[1] - 0.21, 0.66], 'clip_end': 3000}
    sh['camera'] = cam
    sh['size'] = [2400, 1600] if frame == 'landscape' else [1200, 1500]
    sh['title'] = 'Smoke in its element, aligned with the other seven (r48)'
    if BACKLIGHT[0] > 0 and 'kicker' in sh.get('lights', {}):
        # the fire's light through the speaker, from behind: a warm panel between the speaker and the crater, lighting
        # only the speaker (the kicker's receivers), so its glass is seen into, not as a block
        rec = sh['lights']['kicker'].get('receivers')
        sh['lights']['fireback'] = {'type': 'area', 'size_m': [1.2, 1.6], 'position': [SPOT[0] + 0.2, SPOT[1] + 1.1, 0.75],
                                    'target': [SPOT[0], SPOT[1], 0.7], 'irradiance': BACKLIGHT[0], 'color': '#FF9A55',
                                    'receivers': rec}
    for k, f in LIGHT_SCALE.items():                 # the shot's fills were set for the old near-black model
        if k in sh.get('lights', {}):
            if f == 0:
                sh['lights'].pop(k)
            else:
                L = sh['lights'][k]
                for key in ('irradiance', 'power_w', 'energy'):
                    if key in L:
                        L[key] = L[key] * f
    # the heat shimmer (a 2D haze in the finish) keeps off the speaker where it now stands, a margin round it
    hz = (sh.get('finish') or {}).get('dream', {}).get('haze')
    if hz:
        hz['exclude'] = [SPEAKER_BOX[frame]]
    return sh


def refinish(raw, out, shot_json, frame):
    """The finish again on a raw render, with the shimmer kept off the speaker (no new render)."""
    sh = json.load(open(shot_json))
    fin = sh['finish']
    fin['dream']['haze']['exclude'] = [SPEAKER_BOX[frame]]
    import finish as Fn
    Fn.post(raw, out, fin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('worktree'); ap.add_argument('frame', choices=['landscape', 'portrait'])
    ap.add_argument('--out', required=True); ap.add_argument('--samples', type=int, default=128)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--refinish', help='a raw render (.raw.png) to finish again, no render')
    ap.add_argument('--black-lining', action='store_true')
    ap.add_argument('--light', action='append', default=[], help='NAME=FACTOR scales a shot lamp (0 drops it)')
    ap.add_argument('--stand', choices=['feet', 'plinth'], default='feet')
    ap.add_argument('--tt', type=float, help="the glass at this transmission through 20 mm (Smoke 2074 is 0.12)")
    ap.add_argument('--uplight', type=float, default=0.0, help='the night uplight (W); 0 is off')
    ap.add_argument('--backlight', type=float, default=0.0, help="the fire's light through the speaker from behind")
    a = ap.parse_args()
    global BLACK_LINING
    BLACK_LINING = a.black_lining
    LIGHT_SCALE.update({k: float(v) for k, v in (x.split('=') for x in a.light)})
    BACKLIGHT[0] = a.backlight
    W = os.path.abspath(a.worktree)
    if a.refinish:
        sys.path.insert(0, os.path.join(W, 'studio', 'engine'))
        return refinish(a.refinish, a.out, os.path.splitext(a.refinish)[0].replace('.raw', '') + '.shot.json', a.frame)
    src = os.path.join(W, 'renders/2026-10-18/barkhorn/element31',
                       'smoke_e12r_p19.shot.json' if a.frame == 'landscape' else 'smoke_e12r_p19-portrait.shot.json')
    sh = compose(json.load(open(src)), a.frame)
    shot = os.path.splitext(os.path.abspath(a.out))[0] + '.in.json'
    json.dump(sh, open(shot, 'w'), indent=1)
    import habitat
    habitat.run(shot, COLLECTION, a.out, a.samples, a.scale, ASSET, root=W, stand=a.stand, tt=a.tt, up=a.uplight)


if __name__ == '__main__':
    main()
