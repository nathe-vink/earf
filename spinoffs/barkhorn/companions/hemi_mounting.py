"""Hemisphere's two mountings side by side, for the owner's question (round 43, 2026-10-31; certification.md): the
plug-in swag (a ceiling hook, the cord swagged back to the wall and down to a plug, the fine steel suspension cable
beside the cord, no canopy) against the hardwired version (the black canopy, as on the site). Ember, in the studio
rig of the product pictures (lamps_pdp_r41's dome: the sweep, the key, the fill, the wash).

The ceiling stands where the model's canopy top lands (776 mm over the rim), so neither cord is stretched; the swag's
cord and cable end at the hook, a small black cup where the canopy would be.

    python3 spinoffs/barkhorn/companions/hemi_mounting.py            # write the shot
    python3 spinoffs/barkhorn/companions/hemi_mounting.py --render [--scale S --samples N]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import lamps_pdp_r41 as P4                                          # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'hemi-mounting')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'hemi-mounting')
RIM = 1.40
CEIL = RIM + 0.776                       # the canopy's top over the rim (earf_moon CANOPY_TOP_MM)
XS, XH = -0.42, 0.42                     # the swag, the hardwired
HOOK = [[0, 0], [0.005, 0], [0.005, 0.022], [0.016, 0.03], [0.016, 0.05], [0, 0.05]]   # a hook's cup, 32 across


def shot():
    base = P4.dome('ember')
    s = {k: copy.deepcopy(base[k]) for k in ('sky', 'render')}
    s['render']['samples'] = 128
    wall_y = 0.45
    s['set'] = {'kind': 'sweep', 'color': '#EAE4DA', 'width': 10.0, 'front': 6.0, 'depth': wall_y, 'radius': 0.3,
                'height': 4.0, 'props': [
                    # the ceiling: a white slab from the camera's side to the wall
                    {'kind': 'kit', 'shape': 'box', 'material': 'paper', 'color': '#EEE9E0',
                     'position': [0.0, -1.0, CEIL], 'size': [6.0, 2.9, 0.04]},
                    # both lamps, their own lamps off (the COB is a spot below each, as in the product pictures)
                    {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'flavour': 'ember',
                     'lamp': False, 'shade_glow': 0.25, 'hide': 'reflector',
                     'spots': [{'position': [XS, 0.0, RIM], 'hide': 'reflector|canopy', 'options': ['suspension']},
                               {'position': [XH, 0.0, RIM]}]},
                    # the swag's hook, where the canopy would be
                    {'kind': 'kit', 'shape': 'lathe', 'material': 'gloss', 'color': '#16161A', 'roughness': 0.35,
                     'position': [XS, 0.0, CEIL - 0.05], 'profile': HOOK},
                    # the cord swagged back to a wall hook and down to a plug (the plug end first, below the frame)
                    {'kind': 'cable', 'position': [0.0, 0.0], 'd': 0.006, 'color': '#141414', 'plug': [0.06, 0.016],
                     'points': [[XS - 0.62, wall_y - 0.02, 0.25], [XS - 0.62, wall_y - 0.02, 1.2],
                                [XS - 0.62, wall_y - 0.02, CEIL - 0.08], [XS - 0.32, 0.25, CEIL - 0.30],
                                [XS - 0.04, 0.03, CEIL - 0.07], [XS, 0.0, CEIL - 0.045]]},
                    {'kind': 'kit', 'shape': 'lathe', 'material': 'gloss', 'color': '#16161A', 'roughness': 0.35,
                     'position': [XS - 0.62, wall_y - 0.02, CEIL - 0.12], 'profile': HOOK},
                ]}
    cob = base['lights']['cob']
    s['lights'] = {k: copy.deepcopy(base['lights'][k]) for k in ('key', 'fill')}
    for k in ('key', 'fill'):
        s['lights'][k]['target'] = [0.0, 0.0, 1.6]
    s['lights']['bgwash'] = {'type': 'area', 'size_m': [3.5, 0.6], 'position': [0.0, -0.6, CEIL - 0.1],
                             'target': [0.0, wall_y, 1.3], 'irradiance': 2.4, 'color': '#FFE0A4', 'camera': False,
                             'specular': 0.0}
    for n, x in (('swag', XS), ('wired', XH)):
        s['lights'][f'cob_{n}'] = dict(cob, position=[x, 0.0, RIM + 0.06], target=[x, 0.0, 0.0])
    s['materials'] = {'liner': {'glow': 1.4, 'glow_color': '#FFDCB8'}}
    s['title'] = 'Hemisphere in Ember: the plug-in swag (left) and the hardwired canopy (right)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [-0.12, -2.6, 1.55], 'target': [-0.12, 0.0, 1.78], 'lens_mm': 50, 'level': True,
                   'fstop': 8.0, 'focus': [0.0, 0.0, 1.7]}
    return s


def main():
    os.makedirs(SHOTS, exist_ok=True)
    path = os.path.join(SHOTS, 'hemi-mounting.json')
    with open(path, 'w') as f:
        json.dump(shot(), f, indent=1)
    print('wrote', os.path.relpath(path, ROOT))
    a = sys.argv[1:]
    if '--render' in a:
        os.makedirs(RENDERS, exist_ok=True)
        extra = []
        for k in ('--scale', '--samples'):
            if k in a:
                extra += [k, a[a.index(k) + 1]]
        out = a[a.index('--out') + 1] if '--out' in a else os.path.join(RENDERS, 'hemi-mounting.png')
        subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), path, '--out', out] + extra,
                       cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
