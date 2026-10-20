"""EARFcoin (round 33, spinoffs/barkhorn/companions/coin.py), as kit pieces a set can place: a coin, a loose stack, the
request column at the decks and the bowl at the door. The models are the fab kit's (companions/out-coin-study, every
face and edge in one GLB; companions/out-coin-column), with their materials in a flavour.

    {"kind": "kit", "shape": "ext", "module": "earf_coin", "fn": "coin", "spots": [[x, y, z], ...], "flavour": "ice"}

- coin: `rim_glow` (a strength) lights each coin's rim from inside in its own colour (companions.common.GLOW), as
  the site's coins glow on night, and `face_glow` (a strength, or one a flavour) its face faintly; `spots` where each coin's back face lies (metres; a spot can be {"position", "flavour", "face", "edge",
  "rotate": [rx, ry, rz] degrees, "flip": true (lying face down)}); `face` blank (the coin alone), engraved (A, the house pick), printed (B:
  the colour globe printed on a Fog coin) or cast (C: a tinted globe set in a clear coin); `edge` plain or reeded;
- every piece: `flavour_materials` {flavour: {material: overrides}} for one tint alone;
- stack: `spots` the stacks' feet; `n` coins each, `flavours` a list cycled from the bottom (or one `flavour`), a
  little `jitter` (mm) and turn between coins as a hand leaves them, `seed`;
- column: `spots` where the request column stands; `coins` the queue's flavours from the bottom (the next song
  first), `out` (mm) how far the lowest is pushed out of its slot at the front, `rotate_z`;
- fan: `spots` where the first coin lies; the coins dealt along a gentle arc, `s` (mm, 30) apart, each resting its
  trailing edge on the one before (the tilt solved from that), `flavours` in order, `arc` its radius (mm, 320; 0 for a
  line), `heading` (deg) the direction it runs;
- bowl: `spots` the bowl's foot; `n` coins in it (spectrum order dealt round it), `bowl` "smoke" (the base's acrylic),
  "clear" or "brass", `d` its width (mm, 220), `seed`.

The flavours are the eight speaker tints (ember, dust, acid, poison, ice, haze, fog, smoke). Every piece takes
`materials` overrides by the model's material names (coin, frost, inlay, print-*, clear, smoke-base, brass). Coins are
lifted 0.02 mm off what they lie on and off each other, as two flat faces touching render black in Cycles.
"""
import math, os, random, sys

from mathutils import Euler, Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(ENGINE))
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)
import product as PR                                                 # noqa: E402

DEFS = {'coin': 'spinoffs/barkhorn/companions/out-coin-study/earf-coin-study.json',
        'column': 'spinoffs/barkhorn/companions/out-coin-column/earf-coin-column.json'}
T = 0.006                     # the coin's thickness (m)
D = 0.040                     # across
GAP = 0.00002                 # a hair between faces that would otherwise touch
FLOOR = 0.0132                # the column's slot floor above its foot (coin.column_parts)
SPECTRUM = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
FACE_PARTS = {'engraved': ['globe-engraved', 'words'],
              'printed': ['print-*', 'underlay', 'words'],
              'cast': ['globe-cast', 'words'],
              'blank': []}                  # the coin alone: the site's colour picker and loader
CLEAR_BODY = ('printed', 'cast')            # B and C are read through a water-clear coin
_CACHE = {}


def _templates(bpy, which):
    key = (which, bpy.context.scene.name)
    if key not in _CACHE:
        pdef = PR.load_def(DEFS[which], ROOT)
        _CACHE[key] = (pdef, PR.import_model(bpy, os.path.join(ROOT, pdef['model']), pdef['origin_mm']))
    return _CACHE[key]


class _Mats:
    """The model's materials, one set a flavour, built when first asked for."""
    def __init__(self, bpy, which, p):
        self.bpy, self.which, self.p, self.sets = bpy, which, p, {}
        self.pdef = _templates(bpy, which)[0]

    def __call__(self, fl, mname):
        if fl not in self.sets:
            over = dict(self.p.get('materials', {}))
            for k, v in self.p.get('flavour_materials', {}).get(fl, {}).items():
                over[k] = {**over.get(k, {}), **v}
            self.sets[fl] = PR.build_materials(self.bpy, self.pdef, fl, over, f'coin-{self.which}-{fl}')
        return self.sets[fl][mname]


def _mname(pdef, pname):
    return next((r['material'] for r in pdef['assign'] if PR._match(pname, r['match'])), None)


def _link(bpy, name, tpl, mat, M):
    ob = bpy.data.objects.new(name, tpl.data)
    bpy.context.scene.collection.objects.link(ob)
    ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = mat
    ob.matrix_world = M
    return ob


def _one(bpy, name, M, fl, face, edge, mats):
    """One coin at matrix M (its back face's centre), in flavour fl."""
    pdef, tpl = _templates(bpy, 'coin')
    want = [f'body-{edge}'] + FACE_PARTS[face]
    objs = []
    for pname, t in tpl.items():
        if not any(PR._match(pname, w) for w in want):
            continue
        mname = _mname(pdef, pname)
        f = 'fog' if (pname.startswith('body') and face in CLEAR_BODY) else fl
        objs.append(_link(bpy, f'{name}-{pname}', t, mats(f, mname), M))
    return objs


def _matrix(pos, rot=(0, 0, 0), flip=False):
    M = Matrix.Translation(Vector(pos)) @ Euler([math.radians(a) for a in rot], 'XYZ').to_matrix().to_4x4()
    if flip:                                              # face down: turned over about x, its back face up at T
        M = M @ Matrix.Translation((0, 0, T)) @ Matrix.Rotation(math.pi, 4, 'X')
    return M


def _spots(p):
    for i, s in enumerate(p.get('spots', [p.get('position', [0, 0, 0])])):
        yield i, (s if isinstance(s, dict) else {'position': s})


GLOW = {'ember': '#FF4A3A', 'dust': '#FF8A3A', 'acid': '#FFC93A', 'poison': '#6BD45A', 'ice': '#4FB8FF',
        'haze': '#9A6BFF', 'fog': '#FFF4E4', 'smoke': '#C8C0D8'}      # companions/common.py GLOW


def _rim(bpy, kit, name, M, fl, strength, face=0.0):
    """A thin band of light inside the coin's edge, 0.3 in from it, its middle 4 of the 6, with a black band just inside
    it so it shines out through the rim only (lit both ways, it flooded the face and mirrored in it as triangles); and,
    `face` above 0, a faint disc of the same light in the middle of the coin, so its face reads its colour on night (as
    round 30's coins' faces did)."""
    import bmesh
    objs = []
    # both under the rounded rim (it starts 1.5 in), where the rim's curve hides them from above; the shield nearly
    # the rim's whole height there, so no light gets round it into the face
    r0, r1 = D / 2 - 0.00045, D / 2 - 0.00025
    for nm, (a, b), (z0, z1), mat in (
            ('glow', (r0, r1), (0.0012, T - 0.0012), kit.material(bpy, 'glow', GLOW[fl], {'emit': strength})),
            ('shield', (r0 - 0.00014, r0 - 0.00004), (0.00036, T - 0.00036), kit.material(bpy, 'gloss', '#050505', {'roughness': 0.6}))):
        bm = bmesh.new()
        kit._lathe(bm, [(a, z0), (b, z0), (b, z1), (a, z1), (a, z0)], seg=128)
        ob = kit.finish(bpy, f'{name}-{nm}', bm, {}, smooth=True, mat=mat)[0]
        ob.matrix_world = M
        ob.visible_shadow = False
        objs.append(ob)
    if face:                         # below 0: a black disc, the face held dark (Smoke: the rim's light, trapped
        bm = bmesh.new()             # between the polished faces, otherwise fills the whole coin)
        rf = D / 2 - 0.0016
        kit._lathe(bm, [(0.0, T / 2 - 0.0002), (rf, T / 2 - 0.0002), (rf, T / 2 + 0.0002), (0.0, T / 2 + 0.0002)], seg=128)
        mat = (kit.material(bpy, 'glow', GLOW[fl], {'emit': face}) if face > 0
               else kit.material(bpy, 'felt', '#050505'))
        ob = kit.finish(bpy, f'{name}-face', bm, {}, smooth=True, mat=mat)[0]
        ob.matrix_world = M
        ob.visible_shadow = False
        objs.append(ob)
    return objs


def coin(bpy, name, p, kit):
    mats = _Mats(bpy, 'coin', p)
    objs = []
    for i, s in _spots(p):
        pos = list(s['position']); pos[2] += GAP
        M = _matrix(pos, s.get('rotate', p.get('rotate', (0, 0, s.get('rotate_z', 0)))), s.get('flip', p.get('flip', False)))
        fl = s.get('flavour', p.get('flavour', 'ice'))
        objs += _one(bpy, f'{name}#{i}', M, fl, s.get('face', p.get('face', 'engraved')), s.get('edge', p.get('edge', 'plain')), mats)
        rg = s.get('rim_glow', p.get('rim_glow'))
        rg = rg.get(fl, 0.0) if isinstance(rg, dict) else rg
        if rg:
            fg = s.get('face_glow', p.get('face_glow', 0.0))
            fg = fg.get(fl, 0.0) if isinstance(fg, dict) else fg
            objs += _rim(bpy, kit, f'{name}-rim#{i}', M, fl, rg, fg)
    return objs


def _step(face):
    return T + GAP + (0.00006 if face == 'printed' else 0.0)


def stack(bpy, name, p, kit):
    mats = _Mats(bpy, 'coin', p)
    rnd = random.Random(p.get('seed', 3))
    face, edge = p.get('face', 'engraved'), p.get('edge', 'plain')
    fls = p.get('flavours') or [p.get('flavour', 'ice')]
    jit = p.get('jitter', 1.2) / 1000
    objs = []
    for i, s in _spots(p):
        x, y, z = s['position']
        z += GAP + (0.00006 if face == 'printed' else 0.0)
        for k in range(s.get('n', p.get('n', 6))):
            dx, dy = rnd.uniform(-jit, jit), rnd.uniform(-jit, jit)
            M = _matrix((x + dx, y + dy, z + k * _step(face)), (0, 0, rnd.uniform(0, 360)))
            objs += _one(bpy, f'{name}#{i}.{k}', M, fls[k % len(fls)], face, edge, mats)
    return objs


def column(bpy, name, p, kit):
    """The request column, its queue stacked from the slot's floor up; the lowest pushed `out` mm at the front."""
    pdef, tpl = _templates(bpy, 'column')
    cm = _Mats(bpy, 'column', p)
    mats = _Mats(bpy, 'coin', p)
    face, edge = p.get('face', 'engraved'), p.get('edge', 'plain')
    rnd = random.Random(p.get('seed', 5))
    objs = []
    for i, s in _spots(p):
        T0 = Matrix.Translation(Vector(s['position'])) @ Matrix.Rotation(math.radians(s.get('rotate_z', p.get('rotate_z', 0))), 4, 'Z')
        for pname, t in tpl.items():
            mname = _mname(pdef, pname)
            if mname:
                objs.append(_link(bpy, f'{name}-{pname}#{i}', t, cm('fog', mname), T0))
        for k, fl in enumerate(s.get('coins', p.get('coins', []))):
            out = (s.get('out', p.get('out', 0.0)) / 1000) if k == 0 else 0.0
            M = T0 @ _matrix((rnd.uniform(-0.0004, 0.0004), -out + rnd.uniform(-0.0004, 0.0004),
                              FLOOR + GAP + k * _step(face)), (0, 0, rnd.uniform(0, 360)))
            objs += _one(bpy, f'{name}-coin#{i}.{k}', M, fl, face, edge, mats)
    return objs


def fan(bpy, name, p, kit):
    """Coins dealt in a row, each lying with its leading edge on the table and its trailing edge on the coin before (as
    chips spread on a felt): the first flat, each next tipped so that its raised rim meets the top face of the last."""
    mats = _Mats(bpy, 'coin', p)
    face, edge = p.get('face', 'engraved'), p.get('edge', 'plain')
    fls = p.get('flavours') or SPECTRUM
    s_ = p.get('s', 30.0) / 1000
    Ra = p.get('arc', 320.0) / 1000
    rnd = random.Random(p.get('seed', 7))
    objs = []
    for i, sp in _spots(p):
        x0, y0, z0 = sp['position']
        h0 = math.radians(sp.get('heading', p.get('heading', 0.0)))
        a_prev, lo_prev = 0.0, None          # the last coin's tilt, and its low edge's distance along the row
        for k, fl in enumerate(fls):
            # the low edge's place along the row: the first coin's centre at 0, its leading edge at D/2
            lo = D / 2 + k * s_
            if k == 0:
                a = 0.0
            else:
                # D sin a = (lo_prev - lo + D cos a) tan a_prev + T / cos a_prev  (the raised rim on the last's top)
                a = a_prev
                for _ in range(30):
                    a = math.asin(min(0.9, ((lo_prev - lo + D * math.cos(a)) * math.tan(a_prev) + T / math.cos(a_prev) + 0.0001) / D))
            # the centre of the coin's back face, along the row from the first's centre
            u = lo - (D / 2) * math.cos(a)
            zc = (D / 2) * math.sin(a)
            th = h0 + (u / Ra if Ra else 0.0)
            if Ra:
                cx, cy = Ra * math.sin(u / Ra), Ra - Ra * math.cos(u / Ra)
                cx, cy = cx * math.cos(h0) - cy * math.sin(h0), cx * math.sin(h0) + cy * math.cos(h0)
            else:
                cx, cy = u * math.cos(h0), u * math.sin(h0)
            # tipped about the row's normal so it rises toward the coin before (-along the row)
            M = (Matrix.Translation(Vector((x0 + cx, y0 + cy, z0 + zc + GAP))) @ Matrix.Rotation(th, 4, 'Z')
                 @ Matrix.Rotation(a, 4, 'Y') @ Matrix.Rotation(math.radians(sp.get('spin', p.get('spin', 0.0)) + rnd.uniform(-6, 6)), 4, 'Z'))
            objs += _one(bpy, f'{name}#{i}.{k}', M, fl, face, edge, mats)
            a_prev, lo_prev = a, lo
    return objs


def bowl(bpy, name, p, kit):
    """A shallow turned bowl at the door, `n` coins in it in the eight tints: a layer laid on its floor and up its
    curve, and a few on top, turned and tipped as poured coins lie."""
    import bmesh
    mats = _Mats(bpy, 'coin', p)
    rnd = random.Random(p.get('seed', 11))
    face, edge = p.get('face', 'engraved'), p.get('edge', 'plain')
    Dm = p.get('d', 220) / 1000
    R = Dm / 2
    H = 0.05                                     # the bowl's height
    Rs = (R ** 2 + H ** 2) / (2 * H)             # its inside a spherical cap R wide and H deep, wall 6
    wall, foot = 0.006, 0.010
    prof_in = [(R * k / 12, foot + Rs - math.sqrt(max(Rs ** 2 - (R * k / 12) ** 2, 0)) * 1.0) for k in range(13)]
    prof_in = [(r, foot + (Rs - math.sqrt(max(Rs ** 2 - r ** 2, 0)))) for r, _ in prof_in]
    prof = [(0.0, 0.0), (R * 0.45, 0.0), (R * 0.47, 0.003)]
    prof += [(R + wall * (0.3 + 0.7 * k / 12), foot + H * (k / 12) ** 1.6 * 0.98) for k in range(3, 13)]
    prof += [(R + wall * 0.5, foot + H + 0.002), (R, foot + H)]
    prof += list(reversed(prof_in))[:-1] + [(0.0, foot)]
    kind = p.get('bowl', 'smoke')
    bmat = {'smoke': ('smoke-base', 'fog'), 'clear': ('clear', 'fog')}.get(kind)
    col = _Mats(bpy, 'column', p)
    objs = []
    for i, s in _spots(p):
        x0, y0, z0 = s['position']
        bm = bmesh.new()
        kit._lathe(bm, prof, seg=96)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        if bmat:
            mat = col(bmat[1], bmat[0])
        else:
            mat = kit.material(bpy, 'foil', '#B8945A', {'roughness': 0.3})
        objs += kit.finish(bpy, f'{name}-bowl#{i}', bm, {'position': [x0, y0, z0]}, smooth=True, mat=mat)

        def surface(r):
            return foot + (Rs - math.sqrt(max(Rs ** 2 - r ** 2, 0)))

        n = s.get('n', p.get('n', 40))
        placed = []
        k = 0
        tries = 0
        while k < n and tries < 4000:
            tries += 1
            layer = 0 if k < n * 0.75 else 1
            r = math.sqrt(rnd.random()) * (R - 0.024)
            a = rnd.uniform(0, 2 * math.pi)
            cx, cy = r * math.cos(a), r * math.sin(a)
            near = [q for q in placed if math.hypot(q[0] - cx, q[1] - cy) < (0.036 if q[3] == layer else 0.02)]
            if layer == 0 and near:
                continue
            under = [q for q in placed if math.hypot(q[0] - cx, q[1] - cy) < 0.04]
            if layer == 1 and (len(under) < 2 or near):
                continue
            z = surface(r) + 0.0004
            slope = math.atan2(surface(r + 0.001) - surface(r), 0.001)
            if layer == 1:
                z = max(q[2] for q in under) + T + 0.001
            tilt = slope + (math.radians(rnd.uniform(3, 10)) if layer == 1 else 0.0)
            # tip the coin up the bowl's side, toward the centre, about the tangent
            M = (Matrix.Translation(Vector((x0 + cx, y0 + cy, z0 + z))) @ Matrix.Rotation(a, 4, 'Z')
                 @ Matrix.Rotation(-tilt, 4, 'Y') @ Matrix.Rotation(rnd.uniform(0, 2 * math.pi), 4, 'Z'))
            fl = SPECTRUM[k % len(SPECTRUM)]
            objs += _one(bpy, f'{name}-coin#{i}.{k}', M, fl, face, edge, mats)
            placed.append((cx, cy, z, layer))
            k += 1
    return objs
