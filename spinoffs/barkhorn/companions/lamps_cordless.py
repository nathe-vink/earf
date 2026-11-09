"""Core without its cord (the owner, 2026-10-31: "the orb definitely looked better without the cord"; the coordinator:
re-render the site's Core set with the cable hidden, same compositions). Each picture is round 41's pass 4
(lamps_pdp_r41: the same cameras, lights, exposure and samples) with only Core's cable left out: the product's
`cable` part hidden in the single frames, the kit piece's `cable` off in the rows. Lit on its battery, Core has no cord
in use whatever the charging route (CORE-RECHARGE.md decides the charger).

    python3 spinoffs/barkhorn/companions/lamps_cordless.py                        # the shots
    python3 spinoffs/barkhorn/companions/lamps_cordless.py --render [NAME ...]    # render (all when no name), 128 samples
    python3 spinoffs/barkhorn/companions/lamps_cordless.py --site                 # the JPEGs under the site's names
    python3 spinoffs/barkhorn/companions/lamps_cordless.py --render core-dock-ember   # Core on its dock (CORE-RECHARGE.md)

The PNGs keep pass 4's names (p4-...) in renders/2026-10-31/barkhorn/lamps-cordless/, so the site's builder takes them by
pointing its LP4 there first. `--site` also writes the JPEGs as the site names them (web.py: orb-<color>.jpg at 1600,
-card at 640; lamp-orb, lamps-orbs, lamps-unlit at twice their page width and at it) into that folder's site-img/.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import lamps_pdp_r41 as P4                                          # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-cordless')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'lamps-cordless')
COLORS = {'red': 'ember', 'orange': 'dust', 'amber': 'acid', 'green': 'poison', 'blue': 'ice', 'violet': 'haze',
          'ice': 'fog', 'black': 'smoke'}                             # web.py's HABITAT / SPIN_NAME
NAMES = [f'p4-lamp-orb-{f}' for f in COLORS.values()] + ['p4-lamps-orbs', 'p4-lamps-unlit']
DOCK = dict(r=0.075, h=0.008)                 # CORE-RECHARGE.md: the contact dock, 150 x 8, polished black cast acrylic


def cordless(s):
    if 'product' in s:
        s['product']['hide'] = sorted(set(s['product'].get('hide', [])) | {'cable'})
    for p in s.get('set', {}).get('props', []):
        if p.get('module') == 'earf_moon' and p.get('fn') == 'orb':
            p['cable'] = False
    s['title'] = s['title'] + ', cordless (2026-10-31)'
    return s


def on_dock(s):
    """The same frame with Core on its dock (CORE-RECHARGE.md, route b): the dock under the base, the lamp, its light,
    its glints and its pool 8 higher; the dock's cable leaves from its back edge, straight back out of the frame."""
    dz = DOCK['h']
    for inst in s['product']['instances']:
        inst['position'][2] += dz
    for k, L in s['lights'].items():
        if k == 'ball' or k.startswith('pool'):
            L['position'][2] += dz
    for g in s['glints'].values():
        g['at'][2] += dz
    top = s['product']['instances'][0]['position'][2] - dz
    s['set']['props'] += [
        {'kind': 'kit', 'shape': 'cylinder', 'material': 'gloss', 'color': '#121214', 'radius': DOCK['r'], 'height': dz,
         'segments': 128, 'position': [0.0, 0.0, top]},
        {'kind': 'kit', 'shape': 'thread', 'material': 'felt', 'color': '#141414', 'radius': 0.0022,
         'a': [0.0, DOCK['r'] - 0.004, top + 0.0024], 'b': [0.0, 1.2, top + 0.0024]}]
    s['title'] = s['title'].replace('cordless', 'on its dock')
    return s


def unlit_real(s, log=print):
    """lamps-unlit with nothing in frame hidden from the camera (the coordinator, 2026-11-09 19:13; launch/shotcast.py):
    - thru_orb and thru_dome, small hidden lamps behind each lamp's glass shining at the camera, cannot leave the frame
      and still do their job: they go;
    - the bounce (in front of the lens, 100 % of the frame) and the back light (9.9 %) slide away from their targets
      along the line through them, grown to hold their angle there (an irradiance holds), until out of frame;
    - ruling 1 (no specular multipliers): the background wash is seen in reflections again (its specular 0 goes).
    The edges lamp stays: a specular-only lamp, dimmed as a whole, out of frame (ruling 1's exception)."""
    sys.path.insert(0, os.path.join(HERE, 'launch'))
    import shotcast as SCAST
    st = s['set']; depth = st.get('depth', 1e9) - 0.2; ceiling = st.get('height', 1e9) - 0.1
    for k in ('thru_orb', 'thru_dome'):
        s['lights'].pop(k, None); log(f'{k}: removed (cannot leave the frame)')
    for k in ('bounce', 'back'):
        p0 = list(s['lights'][k]['position'])
        f = SCAST.slide_out(s, k, depth=depth, ceiling=ceiling)
        if f is None:
            s['lights'].pop(k); log(f'{k}: removed (cannot leave the set out of frame)')
        else:
            log(f"{k}: {p0} -> {s['lights'][k]['position']}, x{f:.1f}, size {s['lights'][k]['size_m']}")
    s['lights']['bgwash'].pop('specular', None); log('bgwash: specular 0 removed (ruling 1)')
    bad = [r for r in SCAST.hidden(s) if r[3] > 0]
    assert not bad, bad
    s['title'] = s['title'] + ', nothing hidden in frame (2026-11-09)'
    return s


def site():
    from PIL import Image
    out = os.path.join(RENDERS, 'site-img'); os.makedirs(out, exist_ok=True)

    def save(src, name, width, q):
        im = Image.open(os.path.join(RENDERS, src + '.png')).convert('RGB')
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(os.path.join(out, name), quality=q, optimize=True, progressive=True)
        print(os.path.relpath(os.path.join(out, name), ROOT))
    for k, f in COLORS.items():
        save(f'p4-lamp-orb-{f}', f'orb-{k}.jpg', 1600, 84); save(f'p4-lamp-orb-{f}', f'orb-{k}-card.jpg', 640, 82)
    for name, src, w in (('lamp-orb', 'p4-lamp-orb-ember', 800), ('lamps-orbs', 'p4-lamps-orbs', 1200),
                         ('lamps-unlit', 'p4-lamps-unlit', 800)):
        save(src, f'{name}.jpg', 2 * w, 84); save(src, f'{name}-{w}.jpg', w, 84)


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for n in NAMES:
        s = cordless(P4.BUILD[n]())
        s['render']['samples'] = 128
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    d = on_dock(cordless(P4.BUILD['p4-lamp-orb-ember']()))
    d['render']['samples'] = 128
    json.dump(d, open(os.path.join(SHOTS, 'core-dock-ember.json'), 'w'), indent=1)
    print(len(NAMES) + 1, 'shots in', os.path.relpath(SHOTS, ROOT), flush=True)
    if '--render' in sys.argv:
        want = [x for x in sys.argv[sys.argv.index('--render') + 1:] if x in NAMES + ['core-dock-ember']] or NAMES
        os.makedirs(RENDERS, exist_ok=True)
        for n in want:
            subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                            '--out', os.path.join(RENDERS, n + '.png'), '--samples', '128'], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', n, flush=True)
    if '--unlit-real' in sys.argv:
        # the coordinator's 19:13 rule: lamps-unlit again with nothing in frame hidden (unlit_real)
        u = unlit_real(cordless(P4.BUILD['p4-lamps-unlit']()))
        u['render']['samples'] = 128
        json.dump(u, open(os.path.join(SHOTS, 'lamps-unlit-real.json'), 'w'), indent=1)
        a_ = sys.argv[sys.argv.index('--unlit-real') + 1:]
        out = os.path.join(ROOT, 'renders', '2026-11-09', 'barkhorn', 'lamp-site',
                           a_[0] if a_ and a_[0].endswith('.png') else 'lamps-unlit.png')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        extra = ['--scale', a_[a_.index('--scale') + 1]] if '--scale' in a_ else []
        sm = a_[a_.index('--samples') + 1] if '--samples' in a_ else '128'
        subprocess.run(['python3.11', os.path.join(ROOT, 'studio', 'engine', 'render.py'),
                        os.path.join(SHOTS, 'lamps-unlit-real.json'), '--out', out, '--samples', sm] + extra,
                       cwd=ROOT, check=True)
        print('rendered', os.path.relpath(out, ROOT), flush=True)
    if '--site' in sys.argv:
        site()


if __name__ == '__main__':
    main()
