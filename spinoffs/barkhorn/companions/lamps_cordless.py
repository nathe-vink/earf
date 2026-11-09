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


def speaker_deep(tint):
    """The speaker set's dye for a tint (launch/tints-trucast.json), as the colour it passes through 3 mm at the chart's
    figure (strata/scene.absorption's fit), in sRGB hex: the studio engine's `deep` at radius 3 mm."""
    import math
    e = json.load(open(os.path.join(HERE, 'launch', 'tints-trucast.json')))[tint.title()]
    W = (0.2126, 0.7152, 0.0722); lo, hi = 0.0, 50.0
    for _ in range(80):
        k = (lo + hi) / 2
        L = 0.92 * sum(w * math.exp(-k * sp * 3.0) for w, sp in zip(W, e['split']))
        lo, hi = (k, hi) if L > e['cabinet_tt_20mm'] / 100 else (lo, k)
    srgb = lambda x: 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return '#' + ''.join(f'{max(0, min(255, round(255 * srgb(math.exp(-k * sp * 3.0))))):02X}' for sp in e['split'])


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
    # the Ember gate (2026-11-09 20:14, wf_3e232358-ab0):
    # - Hemisphere's mouth read rust: the CAD's 6 mm `liner` shell (R 96-90), clear in v3, took the tinted body through
    #   the product file's `shell|liner|rim` rule (in Smoke a neutral grey, unseen); it is clear acrylic now
    # - Core's top read plum: it reflected the dim sky in front of the set; a real warm paper wall behind the camera,
    #   lit by the studio, gives it a continuous lit surround (out of frame, seen in the glass)
    for p in st['props']:
        if p.get('module') == 'earf_moon' and p.get('fn') == 'dome':
            p['extra_materials'] = {'clear6': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#F7F7F5',
                                               'radius': 0.02, 'roughness': 0.04}}
            # the gate's point 5: the collar's top printed as a void (a true metal, mirroring the dark ceiling); the
            # anodised black as a dielectric of about 3.7 % reflectance (#363638), satin
            p['extra_materials']['anod_black'] = {'preset': 'satin_paint', 'color': '#363638', 'roughness': 0.45,
                                                  'specular': 0.5}
            p['assign'] = [{'match': 'liner', 'material': 'clear6'},
                           {'match': 'collar|clamp|hub|crown|gland', 'material': 'anod_black'}]
    st['props'].append({'kind': 'kit', 'shape': 'box', 'material': 'paper', 'color': '#DCD4C8',
                        'size': [8.0, 0.03, 3.6], 'position': [0.0, -3.4, 0.0]})
    log('dome liner: clear; a warm paper wall behind the camera at y -3.4')
    # the gate's point 4: the table's back edge was off level by about 0.45 deg (the camera yawed 5 deg to its target):
    # the camera faces straight down the set (+y) and the lens shifts sideways instead, so horizontals stay horizontal
    c = s['camera']; dx = c['target'][0] - c['position'][0]; dy = c['target'][1] - c['position'][1]
    W, H = s['size']
    c['shift_x'] = round(dx / dy * c['lens_mm'] / 36.0, 4)          # in sensor widths (sensor_fit HORIZONTAL)
    c['target'] = [c['position'][0], c['target'][1], c['target'][2]]
    log(f"camera: no yaw, lens shift x {c['shift_x']}")
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
        a_ = sys.argv[sys.argv.index('--unlit-real') + 1:]
        tint = a_[a_.index('--tint') + 1] if '--tint' in a_ else 'smoke'
        u = unlit_real(cordless(P4.BUILD['p4-lamps-unlit']()))
        if tint != 'smoke':
            # the coordinator, 19:19: the same picture with only the tint changed (both lamps), Core's ball at that
            # tint's own scatter depth (lamps_pdp_r35.core_materials), as its lit pictures had it
            import lamps_pdp_r35 as P35
            deep = speaker_deep(tint)
            for p in u['set']['props']:
                if p.get('module') == 'earf_moon':
                    p['flavour'] = tint
                    if p.get('fn') == 'orb':
                        p['materials'] = P35.core_materials(tint, p.get('materials'))
                    # round 3's one dye per tint (the speaker's tints-trucast.json): the chart figure through each
                    # shell, Hemisphere's 3 mm tint shell and Core's 9 mm ball at a third (the kit's own Ember,
                    # #CD8553, was a hand value: with the 6 mm shell clear it read copper)
                    m = p.setdefault('materials', {})
                    m['body'] = {**m.get('body', {}), 'deep': deep, 'radius': 0.003 if p.get('fn') == 'dome' else 0.009}
            u['title'] = u['title'].replace('Smoke', tint.title()).replace('smoke', tint)
        sname = 'lamps-unlit-real.json' if tint == 'smoke' else f'lamps-unlit-{tint}-real.json'
        u['render']['samples'] = 128
        json.dump(u, open(os.path.join(SHOTS, sname), 'w'), indent=1)
        out = os.path.join(ROOT, 'renders', '2026-11-09', 'barkhorn', 'lamp-site',
                           a_[0] if a_ and a_[0].endswith('.png') else
                           ('lamps-unlit.png' if tint == 'smoke' else f'lamps-unlit-{tint}.png'))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        extra = ['--scale', a_[a_.index('--scale') + 1]] if '--scale' in a_ else []
        sm = a_[a_.index('--samples') + 1] if '--samples' in a_ else '128'
        subprocess.run(['python3.11', os.path.join(ROOT, 'studio', 'engine', 'render.py'),
                        os.path.join(SHOTS, sname), '--out', out, '--samples', sm] + extra,
                       cwd=ROOT, check=True)
        print('rendered', os.path.relpath(out, ROOT), flush=True)
    if '--site' in sys.argv:
        site()


if __name__ == '__main__':
    main()
