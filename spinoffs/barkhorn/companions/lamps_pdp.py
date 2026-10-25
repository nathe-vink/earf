"""The lamps' product pages (round 34, the site as a shop; the owner, 2026-10-22: "product detail pages where users can
browse colors"): each lamp's hero in every colour, so picking a colour on its page changes the lamp in the picture.
Round 32f's heroes (lamps_site.py: lamp-dome, lamp-orb) were Ember; these are the same frames in the other seven
tints, each tint's glow and pool as the rows were set (lamps_site.GAIN, POOL), in the names the site picks up
(renders/2026-10-22/barkhorn/lamps-pdp/lamp-dome-<flavour>.png, lamp-orb-<flavour>.png).

    python3 spinoffs/barkhorn/companions/lamps_pdp.py                  # the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/lamps_pdp.py --render [names] [--samples 128]

Round 35 (the lamps final, r32-lamps-final): `--r35` builds and renders the same pages in round 35's design (Hemisphere
North (now just Hemisphere) with its fins, Core on its 48 base, Hemisphere South (dropped 2026-10-25); all eight tints, Ember included, and the rows) into
renders/2026-10-22/barkhorn/lamps-pdp-r35/, through lamps_pdp_r35.py:

    python3 spinoffs/barkhorn/companions/lamps_pdp.py --r35 --render lamp-orb-dust [more names] [--samples 128]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
from lamps_site import GAIN, POOL                                  # noqa: E402

SITE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-site')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-pdp')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'lamps-pdp')
FLAVOURS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']


def tinted(lamp, flavour):
    """The site's hero of `lamp` (dome or orb) in `flavour`: its shade or ball in that tint, glowing by the tint's gain
    against Ember's, and the Orb's pool on the stone in the tint's light."""
    s = copy.deepcopy(json.load(open(os.path.join(SITE, f'lamp-{lamp}.json'))))
    s = s[0] if isinstance(s, list) else s
    for p in s['set']['props']:
        if p.get('module') == 'earf_moon':
            p['flavour'] = flavour
            p['shade_glow'] = round(p.get('shade_glow', 0.8) * GAIN[flavour] / GAIN['ember'], 3)
    for k, L in s['lights'].items():
        if k.startswith('pool'):
            L['color'] = POOL[flavour]
    s['title'] = f'{lamp.title()}, its product page: {flavour.title()}'
    return s


def names():
    return [f'lamp-{lamp}-{f}' for lamp in ('dome', 'orb') for f in FLAVOURS if f != 'ember']


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for n in names():
        _, lamp, f = n.split('-')
        json.dump(tinted(lamp, f), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(os.path.relpath(os.path.join(SHOTS, n + '.json'), ROOT))
    if '--render' in sys.argv:
        want = [a for a in sys.argv[sys.argv.index('--render') + 1:] if not a.startswith('--') and a in names()] or names()
        spp = sys.argv[sys.argv.index('--samples') + 1] if '--samples' in sys.argv else '128'
        os.makedirs(RENDERS, exist_ok=True)
        for n in want:
            out = os.path.join(RENDERS, n + '.png')
            if os.path.exists(out):
                continue
            subprocess.run([os.environ.get('PY', 'python3.11'), os.path.join(ROOT, 'studio', 'engine', 'render.py'),
                            os.path.join(SHOTS, n + '.json'), '--out', out, '--samples', spp], cwd=ROOT, check=True)
            print('rendered', n, flush=True)


if __name__ == '__main__':
    if '--r35' in sys.argv:
        import lamps_pdp_r35                                     # noqa: E402
        lamps_pdp_r35.main()
    else:
        main()
