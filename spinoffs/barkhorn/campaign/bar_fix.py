"""The bar set, everything back on its support (2026-11-25: the owner saw Mantle off the counter's back edge; the
coordinator's sweep, spinoffs/barkhorn/coordinator/support-sweep-live-pictures-2026-11-25.json on r46-owner-notes,
found the rest). One pass over each live frame's own rendered shot file, so the set is re-rendered once:

  1. Mantle: the asset's origin is the front-left corner of its 470 x 380 envelope (the plinth 10 mm inside it, local
     +y the back, the middle at local (0.235, 0.190)). planet_bar put that corner at (8.5, 4.32), so the plinth's
     middle stood on the back edge and two feet in the air. Now at (8.5, 3.98), rotate_z 25 kept: the plinth spans
     y 3.993-4.510, 5 cm inside the flat top's back edge (about 4.562). Its lights follow; in mantle-bar so do the
     camera, its Hemisphere and the Ember Core beside it.
  2. The three sleeves 'pulled half out' of the record wall stood 14 cm in front of the shelves, on nothing: each now
     stands on its shelf top, its front corner 5 cm past the lip (81 % of the bottom edge on the shelf), the rest among
     the records it was pulled from, within its cell, turned to the room as before.
  3. mantle-bar's now-playing sleeve and walnut stand stood over the aisle: on the counter behind Mantle's back-left;
     the room's round-36 glasses, which the camera now sees, out.
  4. The desktop hero's second drink stood inside the Ember Core: moved clear, its ice and twist with it. The pale
     'glass' on Mantle's corner in the phone hero is the room's votive (8.55, 3.97): that one votive out.
  5. bar-pendants: the cloth moved off the newspaper; the wooden bowl stands on the flat sleeve, not sunk in it.
  6. Every drink: the orange twist rests on the rim (over it, one end inside, one outside), and the ice floats in
     the drink (about 85 % under), or in a glass too shallow to float it, rests on the glass's floor.
  7. The fruit rests in its bowl. Round 36's 'record out of its sleeve' (life-record, life-sleeve) taken out; the folded napkin and the wool
     throw lie layer on layer (rolls of radius t/2); the napkin clear of the Dust Core; the sleeve stack stacked.

    python3 spinoffs/barkhorn/campaign/bar_fix.py OUTDIR [FRAME ...]
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BAR = os.path.join('renders', '2026-11-11', 'barkhorn', 'product', 'planet-bar')
SRC = {'bar-backbar-portrait': os.path.join(BAR, 'bar-backbar-portrait.shot.json'),
       'fixed9': os.path.join('renders', '2026-11-21', 'barkhorn', 'b1-test', 'fixed9.shot.json'),
       'mantle-bar': os.path.join(BAR, 'mantle-bar.shot.json'),
       'bar-pendants': os.path.join(BAR, 'bar-pendants.shot.json'),
       'bar-hero': os.path.join(BAR, 'bar-hero.shot.json')}

TOP = 1.07                       # the counter's top
OLD, NEW = (8.5, 4.32), (8.5, 3.98)
MANTLE_RZ = 25.0
MANTLE_MID = (0.235, 0.190)      # the plinth's middle from the asset's origin (the envelope's front-left corner)
WALL = dict(x0=3.40, cell=0.36, y=5.72, back=6.08, z0=1.20)   # the record wall (record_wall.build in these shots)
DIVIDER = 0.025                  # keep a pulled-out sleeve this far inside its cell's sides
CORE_SKIRT = 0.075
STAND_AT = (8.40, 4.43)          # mantle-bar: the walnut stand's new place, behind Mantle's back-left on the counter
GLASS_MOVE = {'bar-hero': {(6.31, 4.18): (6.44, 4.15)}}              # the second drink, out of the Ember Core
# (the phone hero's 'pale glass' on Mantle's corner was the room's votive, now out; its drinks stay where they were)
PULL = 0.05                      # a pulled-out sleeve's front corner, this far past the shelf's lip
PENDANT_CLOTH = (6.40, 4.45)
PENDANT_CLOTH_RZ = 0.0          # square to the bar, so it clears the flat sleeve in front of it
THROW_W, THROW_DY = 0.38, -0.01  # the wool throw 4 cm narrower and 1 cm forward: clear of the sleeve stack behind it
FOLD_DZ = -0.0055                # its lowest point stood 5.8 mm over the counter (the ripples): down onto it
ICE = 0.024                      # an ice cube's height (kit box size z)


def _rot(dx, dy, deg):
    a = math.radians(deg)
    return dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)


def _near(a, b, tol=1e-3):
    return abs(a[0] - b[0]) < tol and abs(a[1] - b[1]) < tol


def mantle(s, name, log):
    dx, dy = NEW[0] - OLD[0], NEW[1] - OLD[1]
    hit = False
    for b in s.get('products', []):
        if 'Mantle' in (b.get('collection') or ''):
            for inst in b['instances']:
                if _near(inst['position'], OLD):
                    inst['position'] = [NEW[0], NEW[1]] + inst['position'][2:]; hit = True
    if not hit:
        return
    log.append(f'Mantle {OLD} -> {NEW}')
    # the room's votive at (8.55, 3.97) now stands 6 mm off Mantle's front-left corner and reads, from the phone hero,
    # as a pale candle on the plinth: that one votive out (the room merges all its votives into one mesh)
    s['set']['props'].append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/campaign/bar_life/bar_life.py',
                              'fn': 'remove_near', 'names': ['votives', 'tealights', 'flames'], 'at': [[8.55, 3.97]], 'r': 0.05})
    log.append("the room's votive at (8.55, 3.97), 6 mm off Mantle's corner, out")
    for k, L in s.get('lights', {}).items():
        if k in ('track-mantle', 'mantle-front', 'mantle-side') and 'target' in L:
            L['target'] = [round(L['target'][0] + dx, 4), round(L['target'][1] + dy, 4)] + L['target'][2:]
            log.append(f'light {k} target')
    if name != 'mantle-bar':
        return
    c0 = (OLD[0] + _rot(*MANTLE_MID, MANTLE_RZ)[0], OLD[1] + _rot(*MANTLE_MID, MANTLE_RZ)[1])
    cam = s['camera']
    for k in ('position', 'target', 'focus'):
        if k in cam:
            cam[k] = [round(cam[k][0] + dx, 4), round(cam[k][1] + dy, 4)] + cam[k][2:]
    log.append('camera follows')
    for p in s['set']['props']:
        for key in ('hemispheres', 'cores'):
            for h in (p or {}).get(key, []) or []:
                if math.hypot(h['x'] - c0[0], h['y'] - c0[1]) < 0.6:
                    h['x'] = round(h['x'] + dx, 4); h['y'] = round(h['y'] + dy, 4); log.append(f'{key[:-1]} {h["tint"]} follows')


def pulled_sleeves(s, log, name=''):
    for p in s['set']['props']:
        for bd in (p or {}).get('boards', []) or []:
            r = bd.get('rot', [0, 0, 0])
            if not (abs(r[0] + 4.0) < 1e-6 and abs(bd['y'] - (WALL['y'] - 0.14)) < 1e-3):
                continue
            if name == 'bar-hero' and bd['image'] == 'tex/cover-10.png':
                # turned more to the room, -25 (from -64), so its face reads to the desktop hero's camera at x 6.9, to its
                # left (the coordinator, 13:29; +64, tried first, turned it away)
                r[2] = -25.0; bd['rot'] = r
                log.append('cover-10 turned to rz -25, its face to the hero camera')
            k = round((bd['z'] - WALL['z0']) / WALL['cell'])
            ztop = WALL['z0'] + k * WALL['cell']
            a = math.radians(r[2]); hw = bd['w'] / 2
            hy, hx = hw * abs(math.sin(a)), hw * abs(math.cos(a))
            i = math.floor((bd['x'] - WALL['x0']) / WALL['cell'])
            cx0, cx1 = WALL['x0'] + i * WALL['cell'] + DIVIDER, WALL['x0'] + (i + 1) * WALL['cell'] - DIVIDER
            x = min(max(bd['x'], cx0 + hx), cx1 - hx)
            old = (bd['x'], bd['y'], bd['z'])
            bd['x'], bd['y'], bd['z'] = round(x, 4), round(WALL['y'] + hy - PULL, 4), round(ztop + 0.0005, 4)
            log.append(f'sleeve {bd["image"]} {tuple(round(v, 3) for v in old)} -> ({bd["x"]}, {bd["y"]}, {bd["z"]}) on shelf {k} (top {ztop:.3f})')


def stack(s, log):
    """The four sleeves waiting on the bar: each on the one below (flat boards span z - t .. z), 1 cm further in."""
    for p in s['set']['props']:
        bds = [b for b in (p or {}).get('boards', []) or [] if b['image'] in ('tex/cover-09.png', 'tex/cover-02.png', 'tex/cover-12.png', 'tex/cover-07.png')
               and b.get('rot', [0])[0] == -90.0 and abs(b['y'] - 4.25) < 0.02]
        if len(bds) == 4:
            for j, b in enumerate(bds):
                b['z'] = round(TOP + 0.0005 + b.get('t', 0.003) * (j + 1), 4)
            log.append('sleeve stack stacked (each on the one below); its back corner stays 4 mm past the edge, its middle 15 cm inside')


def mantle_bar_stand(s, log):
    props = s['set']['props']
    for p in props:
        if (p or {}).get('shape') == 'box' and p.get('size') == [0.2, 0.05, 0.022]:
            ox, oy = p['position'][0], p['position'][1]
            p['position'] = [STAND_AT[0], STAND_AT[1], TOP]
            for q in props:
                for bd in (q or {}).get('boards', []) or []:
                    if bd['image'] == 'tex/cover-00.png' and math.hypot(bd['x'] - ox, bd['y'] - oy) < 0.05:
                        bd['x'] = round(STAND_AT[0] + (bd['x'] - ox), 4); bd['y'] = round(STAND_AT[1] + (bd['y'] - oy), 4)
            log.append(f'now-playing stand and sleeve ({ox:.3f}, {oy:.3f}) -> {STAND_AT}')
    for p in props:
        if (p or {}).get('fn') == 'remove':
            p['names'] += [n for n in ('glasses-r36', 'pours-r36') if n not in p['names']]
            log.append("the room's round-36 glasses removed (the camera, moved with Mantle, now sees them)")


def _drink_groups(s):
    """Each drink: its glass's centre, the liquid's top, the shell's floor, and the props that are its ice and twist."""
    out = []
    props = s['set']['props']
    for i, p in enumerate(props):
        if not p:
            continue
        if p.get('fn') == 'water_glass':
            x, y, z = p['position']
            out.append({'c': (x, y), 'foot': z, 'liquid': z + p['fill'], 'floor': z + p.get('base', 0.016), 'ice': p['ice'], 'glass': p})
        elif p.get('shape') == 'lathe' and p.get('material') == 'glass':
            x, y, z = p['position']
            nxt = props[i + 1] if i + 1 < len(props) else {}
            fill = max(q[1] for q in nxt.get('profile', [[0, 0]])) if nxt.get('shape') == 'lathe' else 0.0
            ice = [q for q in props[i + 2:i + 4] if (q or {}).get('shape') == 'box' and q.get('material') == 'frosted']
            out.append({'c': (x, y), 'foot': z, 'liquid': z + fill, 'floor': z + 0.016, 'ice': ice, 'glass': p, 'contents': nxt})
    # twists: tubes whose middle point is within 5 cm of a glass's axis
    for p in props:
        if (p or {}).get('shape') == 'tube' and p.get('material') == 'clay':
            m = p['points'][1]
            g = min(out, key=lambda g: math.hypot(m[0] - g['c'][0], m[1] - g['c'][1]), default=None)
            if g and math.hypot(m[0] - g['c'][0], m[1] - g['c'][1]) < 0.05:
                g['twist'] = p
    return out


def drinks(s, name, log):
    gs = _drink_groups(s)
    for g in gs:
        cx, cy = g['c']
        mv = GLASS_MOVE.get(name, {}).get((round(cx, 2), round(cy, 2)))
        if mv:
            dx, dy = mv[0] - cx, mv[1] - cy
            for q in [g['glass'], g.get('contents')] + list(g['ice']) + [g.get('twist')]:
                if q and 'position' in q:
                    q['position'] = [round(q['position'][0] + dx, 4), round(q['position'][1] + dy, 4)] + q['position'][2:]
            if g.get('twist'):
                g['twist']['points'] = [[round(v[0] + dx, 4), round(v[1] + dy, 4), v[2]] for v in g['twist']['points']]
            cx, cy = mv; g['c'] = mv
            log.append(f'drink ({g["c"][0] - dx:.2f}, {g["c"][1] - dy:.2f}) -> {mv}')
        depth = g['liquid'] - g['floor']
        for j, q in enumerate(g['ice']):
            if depth > ICE * 0.95:           # it floats: about 85 % under
                zb = g['liquid'] - 0.85 * ICE + (0.0015 if j else 0.0)
            else:                            # too shallow to float: on the glass's floor (its tilt lifts a corner)
                zb = g['floor'] + 0.0045 + 0.002 * j
            q['position'] = q['position'][:2] + [round(zb, 4)]
        log.append(f'ice in ({cx:.2f}, {cy:.2f}): {"floating" if depth > ICE * 0.95 else "on the floor"} (liquid top {g["liquid"]:.3f})')
        tw = g.get('twist')
        if tw:
            rim = g['foot'] + 0.092; rr = tw.get('radius', 0.0035)
            m = tw['points'][1]; a = math.atan2(m[1] - cy, m[0] - cx)
            ux, uy = math.cos(a), math.sin(a); tx, ty = -uy, ux        # out from the axis, and along the rim
            pts = [(0.033, -0.012, -0.006), (0.044, 0.0, 0.0), (0.053, 0.012, -0.009)]   # inside, on the rim, outside
            tw['points'] = [[round(cx + r * ux + t * tx, 4), round(cy + r * uy + t * ty, 4), round(rim + rr + 0.002 + dz, 4)] for r, t, dz in pts]
            log.append(f'twist on the rim of ({cx:.2f}, {cy:.2f})')


def leftovers(s, log, name=''):
    for p in s['set']['props']:
        if (p or {}).get('fn') == 'remove':
            for n in ('life-record', 'life-sleeve'):
                if n not in p['names']:
                    p['names'].append(n)
            log.append("round 36's record and sleeve removed")
        if (p or {}).get('fn') == 'fold':
            t = p.get('t', 0.01)
            if p.get('rr', 0.016) > t / 2 + 1e-9:
                p['rr'] = round(t / 2, 4); log.append(f'fold at ({p["x"]:.2f}, {p["y"]:.2f}): layers on each other (rr {p["rr"]})')
                if t >= 0.008:                               # the wool throw (the napkin, 4 mm, already lies on the top)
                    p['z'] = round(p['z'] + FOLD_DZ, 4); p['w'] = THROW_W; p['y'] = round(p['y'] + THROW_DY, 4)
                    log.append(f'throw down {-FOLD_DZ * 1000:.1f} mm onto the top, {THROW_W} wide, 1 cm forward: clear of the stack')


def pendants(s, log):
    props = s['set']['props']
    sleeve = None
    for p in props:
        for bd in (p or {}).get('boards', []) or []:
            if bd['image'] == 'tex/cover-09.png' and bd.get('rot') == [-90.0, 0, 0.0]:
                sleeve = bd
    if sleeve:
        sx, sy, sz = sleeve['x'], sleeve['y'] + sleeve['h'] / 2, sleeve['z']     # its middle (flat: h runs along +y)
        bowl = next(p for p in props if (p or {}).get('model') == 'wooden_bowl_01')
        bx, by, bz = bowl['position']
        dx, dy, dz = sx - bx, sy - by, sz - bz
        for p in props:
            if (p or {}).get('model') in ('wooden_bowl_01', 'food_lime_01', 'lemon') and math.hypot(p['position'][0] - bx, p['position'][1] - by) < 0.12:
                p['position'] = [round(p['position'][0] + dx, 4), round(p['position'][1] + dy, 4), round(p['position'][2] + dz, 4)]
        log.append(f'bowl and fruit ({bx:.2f}, {by:.2f}) -> on the sleeve ({sx:.3f}, {sy:.3f}, {sz:.4f})')
    for p in props:
        if (p or {}).get('shape') == 'box' and p.get('material') == 'cotton':
            p['position'] = [PENDANT_CLOTH[0], PENDANT_CLOTH[1], p['position'][2]]; p['rotate'] = [0, 0, PENDANT_CLOTH_RZ]
            log.append(f'cloth -> {PENDANT_CLOTH}, rz {PENDANT_CLOTH_RZ}, off the newspaper and the sleeve')
        for bd in (p or {}).get('boards', []) or []:
            if bd['image'] == 'tex/newspaper.png' and abs(bd['x'] - 6.97) < 1e-3:
                bd['x'] = round(bd['x'] + 0.02, 4); log.append('newspaper 2 cm right, off the sleeve\'s corner')
        if (p or {}).get('fn') == 'fold':
            p['y'] = round(p['y'] - 0.015, 4); log.append('napkin 1.5 cm further from the Dust Core')


# each fruit's lowest point onto the bowl's inner surface under it (the bowl's mesh, wooden_bowl_01_2k: its floor and wall
# height by radius), 0.5 mm clear: one lime stood 8 mm over it, the other 3 mm into it, the lemon 35 mm into the wood
FRUIT_DZ = {('food_lime_01', (0, 20, 0)): -0.0106, ('food_lime_01', (30, 0, 90)): -0.0004, ('lemon', (0, 70, 20)): 0.0395}   # then trimmed by the support check's own contact reading


def fruit(s, log):
    """The fruit in the bowl, on it (the support check: one lime 9.5 mm over the bowl, the other and the lemon about
    4 mm into it)."""
    for p in s['set']['props']:
        k = ((p or {}).get('model'), tuple((p or {}).get('rotate') or ()))
        if k in FRUIT_DZ:
            p['position'] = p['position'][:2] + [round(p['position'][2] + FRUIT_DZ[k], 4)]
            log.append(f'{k[0]} {FRUIT_DZ[k] * 1000:+.1f} mm, on the bowl')


def builds(s, log):
    """The desktop hero rendered Tropos from a scratch detail package (barkhorn-cloud.glb 3862f1973f34d0b7, gone); the
    coordinator (07:21, 09:01): the current builds, as fixed9 (cloud f80fab61440e5c87, variants c9409ba32d184d39)."""
    for b in s.get('products', []):
        if 'detail-pkg' in (b.get('def') or ''):
            b['def'] = 'studio/products/barkhorn-cloud.json'; log.append('Tropos from the current cloud build (the scratch detail package is gone)')


def fix(s, name):
    s = copy.deepcopy(s); log = []
    builds(s, log)
    mantle(s, name, log)
    pulled_sleeves(s, log, name)
    stack(s, log)
    if name == 'mantle-bar':
        mantle_bar_stand(s, log)
    drinks(s, name, log)
    fruit(s, log)
    leftovers(s, log, name)
    if name == 'bar-pendants':
        pendants(s, log)
    return s, log


if __name__ == '__main__':
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    for n in (sys.argv[2:] or SRC):
        s, log = fix(json.load(open(os.path.join(ROOT, SRC[n]))), n)
        json.dump(s, open(os.path.join(od, n + '.json'), 'w'), indent=1)
        print(f'{n}:\n  ' + '\n  '.join(log))
