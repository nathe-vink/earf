"""Hiddencast (2026-11-09, the coordinator's 18:37 rule): every object in a shot that the camera cannot see, with the
share of the frame it covers by ray-cast (shots.card_coverage: a 96 x 96 grid of rays through the frame, lens shift
included, padded 3 % past each edge, against the object's rectangle). Any such object in frame is a violation, but for
a practical's bulb inside its own fitting.

    python3 spinoffs/barkhorn/campaign/hiddencast.py SHOT.json [SHOT.json ...]  [--md]

Hidden objects: set flags and bounces without `camera` (reflect-only ones included: they must be out of frame too),
panel lamps without `camera`, and area lamps (Cycles hides a lamp from the camera). A lamp's rectangle is its
`size_m` at its position (or orbit about its target), facing its target."""
import json, math, sys

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import shots  # noqa: E402


CENTRE = [0.0, -0.004, 0.647]      # Tropos's bounds centre at the origin (out-cloud: x 0-560, y -0.1-427.6, z -12-1283.1 mm)


def _lamp_rect(L, centre=CENTRE):
    """As studio/engine/lights.py places it: an orbit about the product's bounds centre (render.py), facing its target."""
    t = L.get('target', centre)
    if 'orbit' in L:
        o = L['orbit']; az, el = math.radians(o.get('azimuth_deg', 0)), math.radians(o.get('elevation_deg', 30))
        d = o.get('distance_m', 2.0)
        p = [centre[0] + d * math.cos(el) * math.sin(az), centre[1] - d * math.cos(el) * math.cos(az), centre[2] + d * math.sin(el)]
    elif 'position' in L:
        p = L['position']
    else:
        return None
    n = [t[i] - p[i] for i in range(3)]; m = math.sqrt(sum(x * x for x in n)) or 1.0
    w, h = L.get('size_m', [0.5, 0.5]) if isinstance(L.get('size_m'), list) else [L.get('size_m', 0.5)] * 2
    return {'center_m': p, 'size_m': [w, h], 'normal': [x / m for x in n]}


def hidden(s):
    rows = []
    st = s.get('set', {}) or {}
    for key in ('flags', 'bounces'):
        for c in st.get(key, []) or []:
            if c.get('camera'):
                continue
            kind = ('reflect-only ' if c.get('reflect_only') else 'hidden ') + key[:-1]
            rows.append((kind, c.get('name', ''), c['center_m'], shots.card_coverage(s, c)))
    for k, L in (s.get('lights') or {}).items():
        on = any(float(L.get(x, 0) or 0) > 0 for x in ('irradiance', 'power_w', 'strength', 'power'))
        if L.get('type') in ('panel', 'area', 'flag') and not L.get('camera'):
            r = _lamp_rect(L)
            if r:
                rows.append(({'panel': 'panel', 'area': 'area lamp', 'flag': 'lamp-rig flag'}[L['type']] + ('' if on or L['type'] == 'flag' else ' (off)'), k,
                             [round(x, 2) for x in r['center_m']], shots.card_coverage(s, r)))
    return rows


if __name__ == '__main__':
    md = '--md' in sys.argv
    for f in [a for a in sys.argv[1:] if a != '--md']:
        s = json.load(open(f))
        rows = hidden(s)
        bad = [r for r in rows if r[3] > 0 and '(off)' not in r[0]]
        name = f.rsplit('/', 1)[-1]
        if md:
            print(f"| {name} | {len(rows)} | {len(bad)} | " + '; '.join(f"{r[0]} {r[1]} at {r[2]}: {r[3] * 100:.1f} %" for r in bad) + ' |')
        else:
            print(name, f'{len(rows)} hidden, {len(bad)} in frame')
            for r in bad:
                print(f'   IN FRAME {r[3] * 100:5.1f} %  {r[0]} {r[1]} at {r[2]}')
