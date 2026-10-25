"""Round 35's site pictures, ready to swap in once the owner signs (the coordinator, 2026-10-22: "render the site's lamp
pictures in round 35's design"): the product pages' heroes in all eight tints, Ember included (the site's Ember heroes
are round 32f's), and the rows, in the site's style (lamps_site.py: the pale paper studio, exposure 0.15, 4300 K,
1600 x 2000 at 128 spp), in round 35's geometry: Hemisphere (Hemisphere North then) with its fins, Core on its 48 base, and Hemisphere
South, new. The names the site picks up stay (lamp-dome-<flavour>, lamp-orb-<flavour>; lamp-south-<flavour> is new),
in a folder of their own (renders/2026-10-22/barkhorn/lamps-pdp-r35/), so round 34's are untouched.

Built from round 32f's site shots (studio/shots/barkhorn/lamps-site/), as round 34's lamps_pdp.py was; the models come
round 35's way through the kit piece (earf_moon.py). What moves:
- North: the fins and the cap stand 34 above the old cap, so the frame lifts 20 mm.
- Core: the ball sits 18 higher (the base 30 -> 48), so the camera, its focus and the pool lift 18; its one tint layer is
  drawn at 0.75 of the tint's depth (lamps_final.core_piece: the caster deepens the cast by 12/9) and its frost with a
  short scatter.
- South: a frame of its own in the same studio, a pale ceiling over the sweep so its wash reads, the bowl seen from
  below and a little in front; the wash a disc of light on the lid facing up, the glow the liner's, both by the tint's
  gain as the rows (lamps_site.GAIN).

    python3 spinoffs/barkhorn/companions/lamps_pdp_r35.py                           # the shots
    python3 spinoffs/barkhorn/companions/lamps_pdp_r35.py --render NAME [NAME ...] [--samples 128]
    python3 spinoffs/barkhorn/companions/lamps_pdp_r35.py --render                  # every name not yet rendered
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
from lamps_site import GAIN, POOL                                  # noqa: E402

SITE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-site')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-pdp-r35')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'lamps-pdp-r35')
FLAVOURS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
LIFT_ORB = 0.018              # Core's ball, higher by the base's 18
LIFT_DOME = 0.020             # North's frame, for its fins
TITLES = {'dome': 'Hemisphere', 'orb': 'Core', 'south': 'Hemisphere South (dropped 2026-10-25)'}


def site(n):
    s = copy.deepcopy(json.load(open(os.path.join(SITE, n + '.json'))))
    return s[0] if isinstance(s, list) else s


def core_materials(flavour, base=None):
    """Core's ball: one tint layer at 0.75 of the cast's depth, its frost a short scatter (lamps_final.core_piece)."""
    r = {'smoke': 0.012, 'smoked': 0.0055}.get(flavour, 0.005) * 0.75
    m = copy.deepcopy(base or {})
    m.setdefault('body', {})['radius'] = round(r, 5)
    m.setdefault('liner', {})['radius'] = 0.002
    return m


def lift(v, dz):
    return [v[0], v[1], round(v[2] + dz, 4)]


def strip(pos, target, irr, size=(0.08, 0.6)):
    """A tall narrow softbox, unseen, that draws a black part's edge as a line of light (pass 2, the coordinator: the
    critics read the fins, the collar and the base as flat black cut-outs)."""
    # specular only: black anodising shows a light only as its reflection, and a diffuse share greys the paper
    return {'type': 'area', 'size_m': [size[0] * 2.5, size[1] * 1.5], 'position': pos, 'target': target,
            'irradiance': irr * 3.0, 'color': 4300, 'camera': False, 'specular': 1.0, 'diffuse': 0.0}


def dome(flavour):
    s = site('lamp-dome')
    for p in s['set']['props']:
        if p.get('module') == 'earf_moon':
            p['flavour'] = flavour
            # pass 2: the shade glows as the rows' (lamps-domes 0.75 at the rows' framing; the hero's 0.9 read as
            # opaque plastic seen close)
            p['shade_glow'] = round(1.4 * GAIN[flavour] / GAIN['ember'], 3)
    c = s['camera']
    c['target'] = lift(c['target'], LIFT_DOME)
    c['lens_mm'] = 88                                       # pass 2: the lamp fills more of the tall frame
    s['lights']['edge_r'] = strip([0.42, 0.18, 1.56], [0.0, 0.0, 1.53], 1.8)
    s['lights']['edge_l'] = strip([-0.42, 0.22, 1.50], [0.0, 0.0, 1.49], 1.0)
    s['title'] = f'{TITLES["dome"]}, its product page: {flavour.title()} (round 35)'
    return s


def orb(flavour):
    s = site('lamp-orb')
    for p in s['set']['props']:
        if p.get('module') == 'earf_moon':
            p['flavour'] = flavour
            p['shade_glow'] = round(p.get('shade_glow', 0.8) * GAIN[flavour] / GAIN['ember'], 3)
            p['materials'] = core_materials(flavour, p.get('materials'))
    c = s['camera']
    for k in ('position', 'target', 'focus'):
        c[k] = lift(c[k], LIFT_ORB)
    for k, L in s['lights'].items():
        if k.startswith('pool'):
            L['color'] = POOL[flavour]
            L['position'] = lift(L['position'], LIFT_ORB)
        elif 'target' in L and k in ('key', 'fill', 'back'):
            L['target'] = lift(L['target'], LIFT_ORB)
    s['lights']['edge_l'] = strip([-0.42, 0.18, 0.08], [0.0, 0.0, 0.05], 1.2, size=(0.6, 0.06))   # pass 2: the base's edge
    s['title'] = f'{TITLES["orb"]}, its product page: {flavour.title()} (round 35)'
    return s


CEIL, RIM = 2.70, 2.20          # South: the ceiling, and the bowl's rim 500 below it (its rod 450, the canopy 50)
WASH_W, WALL_W, GLOW = 0.8, 0.5, 0.9


def south(flavour):
    """South in the site's studio: the paper sweep and its light as North's hero, a pale ceiling over it (a slab of the
    sweep's colour), the bowl from below and a little in front, its ceiling in shot."""
    s = site('lamp-dome')
    g = GAIN[flavour] / GAIN['ember']
    s['set']['props'] = [
        {'kind': 'kit', 'shape': 'box', 'material': 'paper', 'color': '#EAE4DA', 'size': [6.0, 3.0, 0.05],
         'position': [0.0, 0.2, CEIL]},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'south', 'spots': [[0.0, 0.0, RIM]],
         'flavour': flavour, 'lamp': False, 'shade_glow': round(GLOW * g, 3), 'noshadow': 'lid',
         'materials': {'liner': {'glow_color': '#FFDCB8'}}}]
    T = [0.0, 0.0, RIM - 0.02]
    L = s['lights']
    for k in ('key', 'fill'):
        L[k]['target'] = T
    # the key below the ceiling (the slab shades a key at round 32f's 42 deg), so the ceiling takes only the wash
    L['key']['orbit'] = {'azimuth_deg': -30, 'elevation_deg': 8, 'distance_m': 2.2}
    L['key']['irradiance'] = 0.45
    L['fill']['irradiance'] = 0.15
    L['bgwash'].update(position=[0.0, -0.4, 2.2], target=[0.0, 0.45, 1.2])
    for k in ('rim', 'rim_l'):
        L[k].update(position=[0.35 if k == 'rim' else -0.35, 0.22, RIM - 0.15], target=T)
    L['hubstrip'].update(position=[-0.4, -0.3, RIM - 0.45], target=[0.0, 0.0, RIM - 0.17])
    L['wash'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.17, 0.17], 'position': [0.0, 0.0, RIM + 0.004],
                 'target': [0.0, 0.0, CEIL], 'power_w': round(WASH_W, 3), 'color': 2700, 'camera': False}
    L['bowl'] = {'type': 'point', 'position': [0.0, 0.0, RIM - 0.05], 'power_w': round(WALL_W * g, 3), 'radius_m': 0.05,
                 'color': POOL[flavour], 'camera': False, 'transmission': False, 'specular': 0.0}
    # pass 2: larger and from nearer eye level, so the bowl and its wash read rather than its underside
    s['camera'] = {'position': [-0.22, -1.00, 1.92], 'target': [0.0, 0.0, 2.33], 'lens_mm': 56, 'level': True,
                   'fstop': 5.6, 'focus': [0.0, -0.05, 2.15]}
    L['edge_r'] = strip([0.45, 0.25, 2.05], [0.0, 0.0, 2.05], 1.8, size=(0.08, 0.9))
    L['edge_l'] = strip([-0.45, 0.30, 2.30], [0.0, 0.0, 2.30], 1.0, size=(0.08, 0.9))
    s['title'] = f'{TITLES["south"]}, its product page: {flavour.title()} (round 35)'
    return s


ROWS = ('lamps-domes', 'lamps-orbs', 'lamps-unlit')


def row(n):
    """Round 32f's rows in round 35's geometry: the Orbs' (Core's) cameras and pools lift with the ball."""
    s = site(n)
    for p in s['set']['props']:
        if p.get('module') == 'earf_moon' and p.get('fn') == 'orb':
            p['materials'] = core_materials(p.get('flavour', 'smoke'), p.get('materials'))
    if n in ('lamps-orbs',):
        c = s['camera']
        for k in ('position', 'target', 'focus'):
            if k in c:
                c[k] = lift(c[k], LIFT_ORB)
        for k, L in s['lights'].items():
            if k.startswith('pool'):
                L['position'] = lift(L['position'], LIFT_ORB)
    s['title'] = s['title'].replace('Dome and Orb', 'Hemisphere and Core') + ' (round 35)'
    return s


BUILD = {f'lamp-{lamp}-{f}': (lambda lamp=lamp, f=f: {'dome': dome, 'orb': orb, 'south': south}[lamp](f))
         for lamp in ('dome', 'orb', 'south') for f in FLAVOURS}
BUILD.update({n: (lambda n=n: row(n)) for n in ROWS})


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in BUILD.items():
        s = f()
        s['render']['samples'] = 128
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    print(len(BUILD), 'shots in', os.path.relpath(SHOTS, ROOT))
    if '--render' in sys.argv:
        a = sys.argv[sys.argv.index('--render') + 1:]
        want = [x for x in a if x in BUILD] or list(BUILD)
        spp = a[a.index('--samples') + 1] if '--samples' in a else '128'
        os.makedirs(RENDERS, exist_ok=True)
        for n in want:
            out = os.path.join(RENDERS, n + '.png')
            if os.path.exists(out) and not [x for x in a if x in BUILD]:
                continue                                  # a full run skips what is done; a named render redoes it
            subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'),
                            os.path.join(SHOTS, n + '.json'), '--out', out, '--samples', spp], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', n, flush=True)


if __name__ == '__main__':
    main()
