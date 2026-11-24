"""Light model C for the Tropos fronts and the horn 360 (the owner, 24 Nov 04:02: "5. C"; the coordinator's 21 Nov 08:34
recommendation, critics unanimous on the S1 test, renders/2026-11-21/barkhorn/s1-test/ c): one physical light model.
  - refractive and reflective caustics on, clamp 0, filter_glossy 0;
  - the acrylics' shadow-ray shortcut cut (living_ext.no_glass_shadows, last in the set), then shadow_ray_report: both
    write their counts into the frame's .report.json (`notes`), so each frame carries its own proof;
  - the sweep's painted contact term off (contact strength and core_strength 0): every shadow is cast by the lights;
  - S4b (the coordinator, 24 Nov 09:21): no reflect-only flags. A reflect-only flag (no shadow, no diffuse, unseen by
    transmission, one-sided) becomes a real black card: every ray on, two-sided, casting shadows, out of frame; an
    overhead one (facing down) comes out instead, since as a real card it shades the backdrop and the product (the
    fronts' flags 3 and 5: renders/2026-11-24/barkhorn/light-c/s4/readings.md).
Nothing else changes: each front is A-polished-tallr7/site-front-off-tall-<tint>.shot.json, each turn frame is
horn_turn.frame(tint, n) (the front's shot with the turn's camera and the speaker's turn), each horn-back and amp plate
the FA123 batch's shot file (renders/2026-11-13/barkhorn/fa123/horn-back-<tint>, macro-amp-<tint>), all made model C.

    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR fronts                ->  OUTDIR/front-<tint>.json (8)
    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR turn TINT [N ...]     ->  OUTDIR/turn-<tint>-NN.json (24)
    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR stills [TINT ...]     ->  OUTDIR/horn-back-<tint>.json, amp-<tint>.json
Render each with  python3 studio/engine/render.py SHOT --out PNG --masks  (no LAMPS_ROOT, no Mantle: the two models)."""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import horn_turn                                                          # noqa: E402
FA123 = os.path.join(horn_turn.ROOT, 'renders', '2026-11-13', 'barkhorn', 'fa123', '{name}-{tint}.shot.json')
TINTS = ('acid', 'dust', 'ember', 'fog', 'haze', 'ice', 'poison', 'smoke')
EXT = 'spinoffs/barkhorn/campaign/living/living_ext.py'


def real_flags(s):
    """S4b: every reflect-only flag made a real black card, or taken out if it hangs overhead facing down. Returns
    (made real, taken out) as flag indices; a flag taken out keeps its slot (`off`), so later indices hold."""
    real, out = [], []
    for i, f in enumerate(s['set'].get('flags', [])):
        if not f or f.get('off') or not f.get('reflect_only'):
            continue
        if f.get('normal', (0, 0, 0))[2] < -0.5:
            f['off'] = True; out.append(i)
        else:
            f.pop('reflect_only'); f.update(one_sided=False, camera=True, glossy=True); real.append(i)
    return real, out


# --- a buildable rig (the S4b critics, 24 Nov: the horn lamp passed through flag 2, bg-right through flag 1, flag 4 sat
# 5 cm below the floor, and floor cards ran into the sweep's curve). Cards are trimmed, never moved: off the floor and
# the curve, and back from any lamp's emitting face, from the end nearer the lamp, 1 cm at a time. Pure geometry here;
# the engine's flags_crossing_set audit (render.py) checks the result on the built scene.
FLOOR_GAP = 0.005


def _v(a, b, k=1.0):
    return [a[i] + k * b[i] for i in range(3)]


def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def _dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def _unit(a):
    n = _dot(a, a) ** 0.5
    return [x / n for x in a]


def _card_frame(f):
    """A card's centre, side and up axes and half sizes, as sets._card builds it (the `center_m` form)."""
    n = _unit(f.get('normal', (0, -1, 0)))
    up = [0, 0, 1] if abs(n[2]) < 0.99 else [0, 1, 0]
    side = _unit(_cross(up, n)); up = _unit(_cross(n, side))
    w, h = f.get('size_m', [1.0, 1.0])
    return list(f['center_m']), side, up, w / 2, h / 2


def _quad(c, a, b, ha, hb):
    return [_v(_v(c, a, sa * ha), b, sb * hb) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def _lamp_quad(spec, centre):
    import math
    if 'position' in spec:
        p = list(spec['position'])
    else:
        o = spec.get('orbit', {}); az, el = math.radians(o.get('azimuth_deg', 0)), math.radians(o.get('elevation_deg', 30))
        d = o.get('distance_m', 2.0)
        p = _v(centre, [math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)], d)
    t = list(spec.get('target', centre))
    z = _unit([p[i] - t[i] for i in range(3)])                      # local +Z points away from the target (-Z tracks it)
    y = _unit(_v([0, 0, 1], z, -z[2]))                                # local Y as near world up as it goes
    x = _cross(y, z)
    size = spec.get('size_m', [1.0, 1.0]); size = [size, size] if isinstance(size, (int, float)) else size
    return _quad(p, x, y, size[0] / 2, size[1] / 2)


def _seg_hits_quad(a, b, q):
    n = _cross([q[1][i] - q[0][i] for i in range(3)], [q[3][i] - q[0][i] for i in range(3)])
    da, db = _dot(n, [a[i] - q[0][i] for i in range(3)]), _dot(n, [b[i] - q[0][i] for i in range(3)])
    if da * db > 0 or da == db:
        return False
    x = _v(a, [b[i] - a[i] for i in range(3)], da / (da - db))
    for i in range(4):
        e = [q[(i + 1) % 4][k] - q[i][k] for k in range(3)]
        if _dot(_cross(e, [x[k] - q[i][k] for k in range(3)]), n) < 0:
            return False
    return True


def _quads_meet(p, q):
    return any(_seg_hits_quad(p[i], p[(i + 1) % 4], q) for i in range(4)) or \
           any(_seg_hits_quad(q[i], q[(i + 1) % 4], p) for i in range(4))


def buildable(s, centre=(0.0, -0.009, 0.6475)):           # the Tropos's bounds centre (render.py report `centre`)
    """Trim the set's cards (flags and bounces) so each stays off the floor, off the sweep's curve and clear of every
    lit area lamp's face. Returns what changed: [(card, what, from, to)]."""
    st = s['set']; out = []
    curve_y = st.get('depth', 2.0) - st.get('radius', 1.0) if st.get('kind') == 'sweep' else None
    lamps = {n: _lamp_quad(L, list(centre)) for n, L in (s.get('lights') or {}).items()
             if L and not L.get('off') and L.get('type', 'area') == 'area' and 'size_m' in L
             and (L.get('irradiance', 0) or L.get('power_w', 0) or 0) > 0}
    for kind in ('flags', 'bounces'):
        for i, f in enumerate(st.get(kind, [])):
            if not f or f.get('off') or 'center_m' not in f:
                continue
            name = f'{kind[:-1]}{i}'
            c, side, up, hw, hh = _card_frame(f)
            before = (list(f['center_m']), list(f['size_m']))
            if abs(up[2]) > 0.5:                                         # standing: off the floor (and the cove's
                R = st.get('radius', 1.0)                                    # curve under its foot), trimmed from its foot
                def floor_z(y):
                    return 0.0 if curve_y is None or y <= curve_y else R - max(R * R - (y - curve_y) ** 2, 0.0) ** 0.5
                foot = max(floor_z(c[1] + sg * side[1] * hw) for sg in (-1, 1)) + FLOOR_GAP
                lo = c[2] - hh * abs(up[2])
                if lo < foot:
                    top = c[2] + hh * abs(up[2]); hh = (top - foot) / 2 / abs(up[2]); c[2] = (top + foot) / 2
            elif curve_y is not None:                                    # lying: off the curve, trimmed at its back
                ext = [c[1] + sg * (abs(side[1]) * hw + abs(up[1]) * hh) for sg in (-1, 1)]
                if ext[1] > curve_y - 0.01 and abs(up[1]) > 0.9:
                    hi = curve_y - 0.01; lo_ = ext[0]; hh = (hi - lo_) / 2; c[1] = (hi + lo_) / 2
            for ln, lq in lamps.items():                                 # clear of the lamps' faces, from the nearer end
                lc = [sum(p[k] for p in lq) / 4 for k in range(3)]
                sg = 1 if _dot([lc[k] - c[k] for k in range(3)], side) > 0 else -1
                while hw > 0.05 and _quads_meet(_quad(c, side, up, hw, hh), lq):
                    hw -= 0.005; c = _v(c, side, -sg * 0.005)
            f['center_m'] = [round(x, 4) for x in c]; f['size_m'] = [round(2 * hw, 4), round(2 * hh, 4)]
            if (f['center_m'], f['size_m']) != (before[0], before[1]):
                out.append((f.get('name', name), before, (f['center_m'], f['size_m'])))
    return out


def real_bounces_and_panels(s, bounce='real', strip='real'):
    """S4b for the rest of a rig (the coordinator, 24 Nov 17:38; the amp rig): a reflect-only bounce card (one-sided,
    no shadow, no diffuse) becomes a real two-sided white card, or comes out (`bounce` 'real' or 'out'); a panel that
    only reflects or hides from the camera (diffuse 0, camera off) becomes a real light, lighting and reflecting and
    seen by the camera, or comes out (`strip`). Returns what changed."""
    out = []
    for i, f in enumerate(s['set'].get('bounces', [])):
        if f and not f.get('off') and f.get('reflect_only'):
            if bounce == 'out':
                f['off'] = True
            else:
                f.pop('reflect_only'); f.update(one_sided=False, camera=True, glossy=True)
            out.append((f'bounce{i}', bounce))
    for n, L in (s.get('lights') or {}).items():
        if L and not L.get('off') and L.get('type') == 'panel' and (not L.get('camera') or L.get('diffuse', True) in (0, 0.0, False)):
            if strip == 'out':
                L['off'] = True
            else:
                L.update(diffuse=1.0, specular=1.0, camera=True)
            out.append((n, strip))
    return out


def model_c(s, title):
    s = copy.deepcopy(s)
    s['render'].update(caustics_refractive=True, caustics_reflective=True, filter_glossy=0.0, clamp=0)
    s['set'].setdefault('props', []).extend([{'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_glass_shadows'},
                                             {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'shadow_ray_report'}])
    s['set']['contact'] = {**(s['set'].get('contact') or {}), 'strength': 0.0, 'core_strength': 0.0}
    real_flags(s)
    real_bounces_and_panels(s)
    buildable(s)
    s['title'] = title
    return s


if __name__ == '__main__':
    od, what = sys.argv[1], sys.argv[2]
    os.makedirs(od, exist_ok=True)
    if what == 'fronts':
        for t in TINTS:
            s = json.load(open(horn_turn.FRONT.format(tint=t)))
            json.dump(model_c(s, f'Tropos front, {t}, light model C'), open(os.path.join(od, f'front-{t}.json'), 'w'), indent=1)
            print('front', t)
    elif what == 'turn':
        t = sys.argv[3]; frames = [int(x) for x in sys.argv[4:]] or list(range(24))
        for n in frames:
            s = model_c(horn_turn.frame(t, n), f'Tropos turning on the house ground, {t}, frame {n}, light model C')
            json.dump(s, open(os.path.join(od, f'turn-{t}-{n:02d}.json'), 'w'), indent=1)
        print('turn', t, len(frames), 'frames')
    elif what == 'stills':
        for t in sys.argv[3:] or TINTS:
            for name, out, what_ in (('horn-back', 'horn-back', 'horn A from behind'), ('macro-amp', 'amp', 'the amplifier plate')):
                s = model_c(json.load(open(FA123.format(name=name, tint=t))), f'Tropos, {what_}, {t}, light model C')
                json.dump(s, open(os.path.join(od, f'{out}-{t}.json'), 'w'), indent=1)
            print('stills', t)
