"""The bar set's support table, today against after bar_fix.py, from render.py --support's .support.json files.
    python3 support_table.py SUPDIR TODAYDIR FIXEDDIR > support.md
SUPDIR holds FRAME-today.support.json and FRAME-after.support.json; the shot files name each prop."""
import json, os, re, sys

SUP, TODAY, FIXED = sys.argv[1:4]
SHOTS = {'bar-backbar-portrait': 'renders/2026-11-11/barkhorn/product/planet-bar/bar-backbar-portrait.shot.json',
         'fixed9': 'renders/2026-11-21/barkhorn/b1-test/fixed9.shot.json',
         'mantle-bar': 'renders/2026-11-11/barkhorn/product/planet-bar/mantle-bar.shot.json',
         'bar-pendants': 'renders/2026-11-11/barkhorn/product/planet-bar/bar-pendants.shot.json',
         'bar-hero': 'renders/2026-11-11/barkhorn/product/planet-bar/bar-hero.shot.json',
         'bar-backbar': 'renders/2026-11-11/barkhorn/product/planet-bar/bar-backbar.shot.json',
         'core-bar-table': 'renders/2026-11-11/barkhorn/product/planet-bar/core-bar-table.shot.json'}


def what(shot, grp):
    m = re.match(r'prop(\d+)', grp)
    if not m:
        return grp.replace('.json', '')
    p = shot['set']['props'][int(m.group(1))]
    if p.get('fn') == 'boards':
        k = int(grp.rsplit('-', 1)[-1])
        return 'board ' + p['boards'][k]['image'].split('/')[-1].replace('.png', '')
    if p.get('fn') == 'lamps':
        return 'lamp ' + grp.split(' ', 1)[1]
    if p.get('fn') == 'water_glass':
        return f"glass, fill {p['fill'] * 1000:.0f} mm"
    if p.get('shape') == 'lathe':
        return 'glass' if p.get('material') == 'glass' else 'drink (liquid)'
    if p.get('shape') == 'box' and p.get('material') == 'frosted':
        return 'ice cube'
    if p.get('shape') == 'tube':
        return 'orange twist'
    return p.get('model') or p.get('fn') or f"{p.get('shape')} {p.get('material', '')}".strip()


def cell(g):
    if g is None:
        return '-'
    if not g['standing'] and (g['gap_below_m'] is None or g['gap_below_m'] > 0.2 or (g['z_min'] > 1.2 and g['gap_below_m'] > 0.05)):
        return 'hangs (lamp)' if g['z_min'] > 1.2 else f"nothing under it ({g['gap_below_m']} m)"
    s = f"on {g['below'] if g['below'] else '?'}"
    gap = g['gap_below_m']
    if g.get('sunk_m'):
        s += f", **sunk {g['sunk_m'] * 1000:.1f} mm**"
    elif gap is not None and gap > 0.005:
        s += f", **{gap * 1000:.0f} mm above it**"
    s += f", contact {g['contact_supported'] * 100:.0f} %"
    return s


print('# Bar set: what each thing stands on, today and after bar_fix.py\n')
print('From `render.py --support` (studio/engine/support.py): ray casts straight down from 4 mm over each thing\'s lowest '
      'point, a hit counted only on a face turned up. "contact" is the share of its lowest vertices (within 3 mm of the '
      'bottom) with a top under them within 5 mm; a board resting on a tilt, a glass on its rounded foot or a sleeve '
      'leaning on its back edge touches with part of its bottom by design. Sunk: its bottom below the top under it. The '
      'room itself (counter, walls, shelves, stools) is the support and is not listed; lamps that hang are listed as '
      'hanging. The two Tropos stand on their bays\' oak floors (contact 72-89 %: the feet\'s rounded pads).\n')
for n in SHOTS:
    shot = json.load(open(SHOTS[n]))
    A = {g['group']: g for g in json.load(open(os.path.join(SUP, n + '-today.support.json')))['groups']}
    bf = os.path.join(SUP, n + '-after.support.json')
    B = {g['group']: g for g in json.load(open(bf))['groups']} if os.path.exists(bf) else {}
    print(f'## {n}' + ('' if B else ' (not re-rendered; today only)') + '\n')
    print('| thing | today | after |\n|---|---|---|')
    for k in sorted(set(A) | set(B), key=lambda k: (not k.startswith(('Mantle', 'barkhorn')), k)):
        g = B.get(k) or A[k]
        if g['z_min'] > 2.6 or 'softbox' in k or 'variants' in k or g['z_min'] < 0.05:
            continue
        a, b = cell(A.get(k)), cell(B.get(k)) if B else ''
        if a.startswith('hangs') and (not B or b.startswith('hangs')):
            continue
        print(f'| {what(shot, k)} | {a} | {b} |')
    print()
