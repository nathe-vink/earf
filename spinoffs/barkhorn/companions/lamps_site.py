"""Round 32f, the site set again with the owner's changes (black hardware, the plug-in Orb, the tints matched lit), in
the names the site picks up (renders/2026-10-19/barkhorn/lamps-site/). The frames are round 32e's finals
(studio/shots/barkhorn/crystal-promo/final/, the duels' winners), the products now black and cast to the speakers' hues;
the Orbs plug in, their cables dressed straight back (the kit piece's default). One frame is new: the cartridge, half
out of the back of a lit Orb.

    python3 spinoffs/barkhorn/companions/lamps_site.py                     # the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/lamps_site.py --render [names] [--scale 1.0]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FINAL = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'crystal-promo', 'final')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-site')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'lamps-site')
NAMES = {'lamp-dome': 'dome-hero', 'lamp-orb': 'orb-hero', 'lamps-orbs': 'orbs', 'lamps-domes': 'domes',
         'lamp-catch': 'catch', 'lamps-unlit': 'unlit'}


def final(n):
    return json.load(open(os.path.join(FINAL, n + '.json')))


def cartridge():
    """The battery cartridge slid half out of the back of a lit Ember Orb, from behind and low, on the pale stone."""
    s = final('orb-hero')
    s['title'] = 'Orb: the battery cartridge'
    s['size'] = [1800, 1200]
    for p in s['set']['props']:
        if p.get('module') == 'earf_moon':
            p.update(cable=False, cartridge='out', cartridge_out=0.045)
    # from above enough that the horizon (and the sky past the stone) is out of frame, the whole ball in
    s['camera'] = {'position': [0.40, 0.70, 0.34], 'target': [0.0, 0.04, 0.07], 'lens_mm': 60, 'level': False,
                   'fstop': 8.0, 'focus': [0.0, 0.06, 0.05]}
    L = s['lights']
    L['key'].update(orbit={'azimuth_deg': 150, 'elevation_deg': 50, 'distance_m': 2.6}, target=[0.0, 0.05, 0.03])
    L['fill'].update(orbit={'azimuth_deg': 200, 'elevation_deg': 15, 'distance_m': 3.0}, target=[0.0, 0.05, 0.03])
    # the strip that drew the base's edge from behind now draws it from the front-left, toward the camera's side
    L['back'].update(position=[0.30, 0.05, 0.10], target=[0.0, 0.06, 0.03])
    # the paper behind is now the front of the sweep: the wash moves to light what the camera sees
    L['bgwash'].update(position=[0.0, 1.6, 3.0], target=[0.0, -1.0, 0.25])
    return s


def unlit():
    """Round 32e's unlit pair, the Orb cordless (its cartridge in, no cable: the short run of cable showed as a hook at
    this angle); the light through the ball raised and softened, as its pool on the oak mirrored in the polished black
    drum and read as brass."""
    s = final('unlit')
    for p in s['set']['props']:
        if p.get('fn') == 'orb':
            p.update(cable=False, cartridge='in')
    s['lights']['thru_orb'].update(target=[-0.05, -1.45, 0.45], irradiance=1.5)
    return s


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, src in NAMES.items():
        s = unlit() if n == 'lamps-unlit' else final(src)
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n, '<-', src)
    json.dump(cartridge(), open(os.path.join(SHOTS, 'lamp-cartridge.json'), 'w'), indent=1)
    print('lamp-cartridge')


def render(names, scale, out=RENDERS):
    py = os.environ.get('PY', 'python3')
    os.makedirs(out, exist_ok=True)
    for n in names:
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                        '--out', os.path.join(out, n + '.png'), '--scale', str(scale)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(n, flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    all_ = list(NAMES) + ['lamp-cartridge']
    if '--render' in a:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        render([x for x in a if x in all_] or all_, scale, out)
    else:
        build()
