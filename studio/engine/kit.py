"""The dioramas' kit (round 31): the stuff a model-maker builds a miniature set from, each piece placed in 3D.

A kit piece is a prop in a set's `props`: {"kind": "kit", "shape": ..., "position": [x, y, z], "rotate": [rx, ry, rz]
(degrees), "scale": [sx, sy, sz] or a number, "material": ..., "color": "#...", and by its shape:

- sphere: a ball of radius 1 (scale it to an egg or a mound);
- puffs: a cloud of balls, `puffs` [[x, z, r], ...] laid in the x-z plane, `depth` the balls' thickness along y as a
  share of each radius (felt clouds, a puff of smoke, dust kicked up);
- cylinder or cone: `radius`, `height`, `radius_top` (a cone), standing on its base;
- box: `size` [w, d, h], standing on its base, `ease` its edges;
- extrude: a flat cut-out, `outline` [[x, z], ...] in metres in its own plane, `depth` thick along y, its edges eased
  (paper stars, flames, hills and signs; felt shapes);
- lathe: a turned form, `profile` [[r, z], ...] from the bottom up, revolved about its z axis (a toadstool's cap, a
  bottle, a mesa, a lampshade);
- tube: a soft rope along `points` [[x, y, z], ...] (a smooth curve through them), `radius` (one, or one per point),
  `flat` (thickness over width: 1 round, 0.15 a ribbon), `twist_deg` (a ribbon's turn along its length): a crooked
  branch, a wisp of smoke, a silk river, an aurora;
- drape: a sheet of cloth, `size` [w, h], hanging in its x-z plane from its top edge (`hang`, the default) or lying in
  x-y (`lay`), in `folds` across its width `amplitude` deep (deeper toward the hem when hanging), crumpled by `noise`,
  `thickness` thick: a cave of velvet, a curtain, a river of satin, a rumpled floor;
- scatter: many small pieces in one mesh, `count` of them, `radius` [min, max], laid out `in` a box [x0, y0, z0, x1, y1,
  z1] or rising in a `plume` {"height", "spread": [r0, r1], "lean": [dx, dy], "taper", "power"} from the piece's
  position (embers rising, sparks, dust motes, snow, bubbles), `seed`;
- thread: a fine line from `a` to `b` (world points), `radius` (the string a cloud hangs from);
- ext: a piece a set builds itself, `module` (studio/engine/kit_ext/<module>.py) and `fn`, called as
  fn(bpy, name, p, kit) and returning its objects (it can use this module's helpers and materials).

Photographic pieces (round 31b; studio/engine/assets.py, Poly Haven CC0, fetched and cached):
- ground: a patch of real ground, `texture` (a Poly Haven texture id, e.g. aerial_rocks_02) laid at its real size
  (`tex_scale` metres a tile overrides), `size` [w, d] metres, `displace` metres of true displacement by its height map,
  `relief` metres of broad undulation (level within `flat` [x, y, r], the product's footprint by default; false for
  none), `res` ('1k' to '8k'), `tint` and `tint_mix` to shift its colour;
- asset: a scanned model, `model` (a Poly Haven model id, e.g. boulder_01), placed by `position`, `rotate` (degrees)
  and `scale`, with its own materials;
- scatter_assets: `count` copies of `models` over `area` [x0, y0, x1, y1], none inside an `avoid` circle [x, y, r],
  sized at random within `scale` [min, max], turned at random (`spin`, `tilt_deg`), standing at `z`;
- and `"material": "pbr"` with `texture` on any other shape (tex_scale, displace, tint, tint_mix, rough_mul, bump,
  coords 'object' or 'uv'; an ambientCG set by 'acg:<id>', e.g. 'acg:Lava004', its emission map glowing at
  `emit_map`).

Every piece but a thread is placed by `position`, `rotate` and `scale`; a tube's points, a scatter's box and a drape are
in the piece's own frame.

Materials, each a real thing at miniature scale (`grain` on a piece, and the set's `kit_scale`, multiply the size of
its fibres, weave and grain, so felt reads as felt on a cloud that stands for one a model-maker would cut a few
centimetres across):

- felt, wool, cotton (cotton wool): matte, fuzzy, a soft sheen, a little light through;
- velvet, suede, corduroy: pile fabrics, dark facing you and bright at the rims (sheen), corduroy ribbed;
- satin, silk: smooth woven sheens, a long highlight along the weave;
- tulle, organza: sheer fabrics (`alpha`, how much of the light they stop);
- paper, card, tissue (tissue lets light through: a lantern, a sun lit from behind), clay, sand, flock (moss, grass
  matting: two tones, `tint2`), foil;
- glass, frosted, resin (a coloured cast resin: puddles, drops, candy), gloss (a wet varnish);
- glow: a light, `emit` its strength (embers, windows, a lantern, stars), `color` its colour.

Optional on any piece: `roughness`, `alpha`, `emit`, `tint2`, `grain`.
"""
import importlib, math, os, random, sys

import bmesh
from mathutils import Euler, Matrix, Vector, noise

try:
    from . import materials as M
except ImportError:
    import materials as M

_MATS = {}
SCALE = 1.0          # the set's kit_scale (sets.py sets it from the set's spec before its props are built)


def _set(b, name, value):
    """A Principled input set if this Blender has it (colour sockets take RGBA)."""
    if name in b.inputs:
        s = b.inputs[name]
        if isinstance(value, (int, float)) and hasattr(s.default_value, '__len__'):
            value = (value, value, value, 1.0)
        s.default_value = value


def _mix(hex_a, hex_b, t):
    a, b = M.hex_lin(hex_a), M.hex_lin(hex_b)
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3)) + (1.0,)


def _bump(nt, b, size, strength, dist, kind='noise', detail=8.0, rough=0.7, axis=None, prev=None):
    """A bump from a texture `size` metres across (its features), into the BSDF's normal (chained after `prev`)."""
    tc = nt.nodes.new('ShaderNodeTexCoord')
    if kind == 'wave':
        tx = nt.nodes.new('ShaderNodeTexWave'); tx.wave_type = 'BANDS'; tx.bands_direction = axis or 'X'
        tx.inputs['Scale'].default_value = 1.0 / size; tx.inputs['Distortion'].default_value = 0.6
        out = tx.outputs['Fac']
    elif kind == 'voronoi':
        tx = nt.nodes.new('ShaderNodeTexVoronoi'); tx.feature = 'SMOOTH_F1'
        tx.inputs['Scale'].default_value = 1.0 / size
        out = tx.outputs['Distance']
    else:
        tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = 1.0 / size
        tx.inputs['Detail'].default_value = detail
        if 'Roughness' in tx.inputs:
            tx.inputs['Roughness'].default_value = rough
        out = tx.outputs['Fac']
    nt.links.new(tc.outputs['Object'], tx.inputs['Vector'])
    bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = strength
    bn.inputs['Distance'].default_value = dist
    nt.links.new(out, bn.inputs['Height'])
    if prev is not None:
        nt.links.new(prev, bn.inputs['Normal'])
    nt.links.new(bn.outputs['Normal'], b.inputs['Normal'])
    return bn.outputs['Normal']


def _two_tone(nt, b, color, tint2, size):
    """Base colour wandering between `color` and `tint2` in patches `size` across (moss, sand, felt that is not dyed
    flat)."""
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / size; nz.inputs['Detail'].default_value = 4.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = M.hex_lin(color)
    cr.elements[1].position = 0.65; cr.elements[1].color = M.hex_lin(tint2)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])


def material(bpy, kind, color, opts=None):
    """The kit's materials, one per (kind, colour, options, scale)."""
    o = dict(opts or {})
    g = SCALE * o.get('grain', 1.0)
    key = (kind, color, round(g, 4), tuple(sorted((k, str(v)) for k, v in o.items())))
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new(f'kit-{kind}-{color}'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    _set(b, 'Base Color', M.hex_lin(color))
    if kind in ('felt', 'cotton', 'wool'):
        _set(b, 'Roughness', 0.96 if kind != 'wool' else 1.0); _set(b, 'Specular IOR Level', 0.12)
        _set(b, 'Sheen Weight', {'felt': 1.0, 'cotton': 0.7, 'wool': 1.0}[kind]); _set(b, 'Sheen Roughness', 0.6 if kind != 'wool' else 0.45)
        _set(b, 'Subsurface Weight', {'felt': 0.06, 'cotton': 0.22, 'wool': 0.14}[kind])
        _set(b, 'Subsurface Radius', Vector((0.004, 0.003, 0.002)) * g)
        f, s, d = {'felt': (0.0011, 0.45, 0.0016), 'cotton': (0.0018, 0.75, 0.003), 'wool': (0.0016, 0.6, 0.003)}[kind]
        n = _bump(nt, b, f * g, s, d * g)
        if kind == 'wool':                                # the yarn's twist and clumps over the fibres
            _bump(nt, b, 0.012 * g, 0.35, 0.006 * g, prev=n)
    elif kind in ('velvet', 'suede', 'corduroy'):
        _set(b, 'Base Color', _mix(color, '#000000', 0.25 if kind != 'suede' else 0.1))
        _set(b, 'Roughness', 0.88 if kind != 'suede' else 0.95); _set(b, 'Specular IOR Level', 0.08)
        _set(b, 'Sheen Weight', 1.0 if kind != 'suede' else 0.6); _set(b, 'Sheen Roughness', 0.22 if kind != 'suede' else 0.5)
        _set(b, 'Sheen Tint', _mix(color, '#FFFFFF', 0.45))
        n = _bump(nt, b, 0.0006 * g, 0.22, 0.0008 * g)
        if kind == 'corduroy':
            _bump(nt, b, 0.003 * g, 0.5, 0.0015 * g, kind='wave', axis=o.get('rib', 'X'), prev=n)
    elif kind in ('satin', 'silk'):
        _set(b, 'Roughness', 0.3 if kind == 'satin' else 0.24); _set(b, 'Specular IOR Level', 0.55)
        _set(b, 'Anisotropic', 0.75); _set(b, 'Sheen Weight', 0.35); _set(b, 'Sheen Roughness', 0.3)
        _set(b, 'Sheen Tint', _mix(color, '#FFFFFF', 0.5))
        _bump(nt, b, 0.0004 * g, 0.05, 0.0002 * g)
    elif kind in ('tulle', 'organza'):
        _set(b, 'Roughness', 0.8 if kind == 'tulle' else 0.35); _set(b, 'Specular IOR Level', 0.2 if kind == 'tulle' else 0.5)
        _set(b, 'Alpha', o.get('alpha', 0.22 if kind == 'tulle' else 0.35)); _set(b, 'Sheen Weight', 0.5)
    elif kind in ('paper', 'card', 'tissue'):
        _set(b, 'Roughness', {'paper': 0.82, 'card': 0.7, 'tissue': 0.85}[kind]); _set(b, 'Specular IOR Level', 0.25)
        if kind == 'tissue':                              # light comes through: a lantern, a paper sun lit from behind
            _set(b, 'Transmission Weight', 0.55); _set(b, 'Subsurface Weight', 0.2)
        _bump(nt, b, 0.004 * g, 0.07, 0.0006 * g)
    elif kind == 'clay':
        _set(b, 'Roughness', 0.68); _set(b, 'Specular IOR Level', 0.3); _set(b, 'Subsurface Weight', 0.04)
        n = _bump(nt, b, 0.008 * g, 0.18, 0.0025 * g, detail=3.0)   # thumb-pressed, not machined
        _bump(nt, b, 0.0008 * g, 0.08, 0.0003 * g, prev=n)
    elif kind in ('sand', 'flock'):
        _set(b, 'Roughness', 1.0); _set(b, 'Specular IOR Level', 0.1 if kind == 'sand' else 0.05)
        if kind == 'flock':
            _set(b, 'Sheen Weight', 0.8); _set(b, 'Sheen Roughness', 0.4)
        _two_tone(nt, b, color, o.get('tint2', color), (0.02 if kind == 'flock' else 0.03) * g)
        _bump(nt, b, (0.0005 if kind == 'sand' else 0.0015) * g, 0.7, (0.0006 if kind == 'sand' else 0.003) * g, detail=2.0)
    elif kind == 'foil':
        _set(b, 'Metallic', 1.0); _set(b, 'Roughness', 0.22)
        _bump(nt, b, 0.01 * g, 0.35, 0.002 * g, kind='voronoi')
    elif kind in ('glass', 'frosted', 'resin'):
        _set(b, 'Transmission Weight', 1.0 if kind != 'resin' else 0.9)
        _set(b, 'Roughness', {'glass': 0.02, 'frosted': 0.35, 'resin': 0.06}[kind])
        _set(b, 'IOR', 1.5 if kind != 'resin' else 1.54); _set(b, 'Specular IOR Level', 0.5)
        if kind == 'resin':
            _set(b, 'Coat Weight', 0.5); _set(b, 'Coat Roughness', 0.02)
    elif kind == 'gloss':
        _set(b, 'Roughness', 0.05); _set(b, 'Coat Weight', 0.7); _set(b, 'Coat Roughness', 0.03)
    elif kind == 'glow':
        _set(b, 'Roughness', 0.9); _set(b, 'Emission Color', M.hex_lin(color)); _set(b, 'Emission Strength', o.get('emit', 8.0))
    else:
        raise ValueError(f'kit: no material {kind!r}')
    if 'roughness' in o:
        _set(b, 'Roughness', o['roughness'])
    if 'alpha' in o and kind not in ('tulle', 'organza'):
        _set(b, 'Alpha', o['alpha'])
    if 'emit' in o and kind != 'glow':                    # anything can glow a little: a lit paper sun, a hot coal
        _set(b, 'Emission Color', M.hex_lin(o.get('emit_color', color))); _set(b, 'Emission Strength', o['emit'])
    _MATS[key] = m
    return m


# --- shapes --------------------------------------------------------------------------------------------------------
def _sphere(bm, centre, radii, seg=40):
    geom = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=1.0)
    for v in geom['verts']:
        v.co = Vector((centre[0] + v.co.x * radii[0], centre[1] + v.co.y * radii[1], centre[2] + v.co.z * radii[2]))


def _ico(bm, centre, r, subdiv=1):
    geom = bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    for v in geom['verts']:
        v.co = Vector(centre) + v.co * r


def _extrude(bm, outline, depth, ease=0.0):
    vs = [bm.verts.new((x, -depth / 2, z)) for x, z in outline]
    f = bm.faces.new(vs)
    bmesh.ops.recalc_face_normals(bm, faces=[f])
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    moved = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=Vector((0, depth, 0)), verts=moved)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    if ease > 0:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=min(ease, depth * 0.45), segments=2, affect='EDGES')


def _lathe(bm, profile, seg=64):
    """Rings of the profile's [r, z] revolved about z; the ends closed where their radius is not 0."""
    rings = []
    for r, z in profile:
        if r <= 1e-6:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            rings.append([bm.verts.new((r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)])
    for a, b in zip(rings, rings[1:]):
        if len(a) == 1 and len(b) == 1:
            continue
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[i], b[0], a[j]))
            else:
                bm.faces.new((a[i], b[i], b[j], a[j]))
    for ring, top in ((rings[0], False), (rings[-1], True)):
        if len(ring) > 1:
            bm.faces.new(ring if top else ring[::-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


def _catmull(pts, res=8):
    """A smooth curve through the points (centripetal enough for a sketch): res samples a span."""
    P = [Vector(p) for p in pts]
    if len(P) < 3:
        return [P[0].lerp(P[-1], t / (res * 2)) for t in range(res * 2 + 1)], [0.0] + [t / (res * 2) for t in range(1, res * 2 + 1)]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out, ts = [], []
    n = len(P) - 3
    for i in range(n):
        p0, p1, p2, p3 = P[i:i + 4]
        for k in range(res if i < n - 1 else res + 1):
            t = k / res
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
            ts.append((i + t) / n)
    return out, ts


def _tube(bm, pts, radius, flat=1.0, twist_deg=0.0, sides=16, res=8):
    """A rope along a smooth curve through `pts`, its section an ellipse (width 2 r, thickness 2 r flat), carried along
    the curve without twisting except as `twist_deg` asks; capped."""
    C, ts = _catmull(pts, res)
    radii = radius if isinstance(radius, (list, tuple)) else [radius] * len(pts)
    def r_at(t):
        x = t * (len(radii) - 1); i = min(int(x), len(radii) - 2); f = x - i
        return radii[i] * (1 - f) + radii[i + 1] * f
    T = [(C[min(i + 1, len(C) - 1)] - C[max(i - 1, 0)]).normalized() for i in range(len(C))]
    up = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
    Nv = (up - T[0] * up.dot(T[0])).normalized()
    rings = []
    for i, (c, t) in enumerate(zip(C, ts)):
        if i:
            # parallel transport: rotate the normal by the turn from the last tangent to this one
            ax = T[i - 1].cross(T[i])
            if ax.length > 1e-8:
                ang = math.asin(max(-1.0, min(1.0, ax.length)))
                Nv = (Matrix.Rotation(ang, 3, ax.normalized()) @ Nv)
            Nv = (Nv - T[i] * Nv.dot(T[i])).normalized()
        a = math.radians(twist_deg) * t
        n1 = Nv * math.cos(a) + T[i].cross(Nv) * math.sin(a); b1 = T[i].cross(n1)
        r = r_at(t)
        rings.append([bm.verts.new(c + n1 * (r * math.cos(2 * math.pi * k / sides)) + b1 * (r * flat * math.sin(2 * math.pi * k / sides))) for k in range(sides)])
    for a_, b_ in zip(rings, rings[1:]):
        for k in range(sides):
            bm.faces.new((a_[k], a_[(k + 1) % sides], b_[(k + 1) % sides], b_[k]))
    bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


def _drape(bm, p):
    """A sheet of cloth in folds, as a grid displaced: hanging in x-z from its top edge, or lying in x-y."""
    w, h = p.get('size', [1.0, 1.0])
    folds, amp, nz = p.get('folds', 6), p.get('amplitude', 0.05), p.get('noise', 0.3)
    lay = p.get('orient', 'hang') == 'lay'
    res = p.get('res', 96)
    nu, nv = res, max(8, int(res * h / max(w, 1e-6)))
    rnd = random.Random(p.get('seed', 0)); ph = [rnd.uniform(0, 6.283) for _ in range(4)]
    off = Vector((rnd.uniform(-50, 50), rnd.uniform(-50, 50), rnd.uniform(-50, 50)))
    grid = []
    for j in range(nv + 1):
        row = []
        v = j / nv
        for i in range(nu + 1):
            u = i / nu
            x = (u - 0.5) * w
            depthwise = v if not lay else 1.0                # a hanging sheet's folds open toward its hem
            a = amp * (0.35 + 0.65 * depthwise)
            d = a * (math.sin(2 * math.pi * folds * u + ph[0] + 1.3 * math.sin(3.0 * v + ph[1]))
                     + 0.35 * math.sin(2 * math.pi * folds * 2.3 * u + ph[2] + 2.0 * v))
            d += nz * amp * 2.0 * noise.noise(off + Vector((u * 3.0 * w / max(h, 1e-6), v * 3.0, 0)))
            if lay:
                d += amp * (1.35 + 2.0 * nz)                  # a lying sheet rests on its plane, its ripples above it
                row.append(bm.verts.new((x, (v - 0.5) * h, d)))
            else:
                row.append(bm.verts.new((x, d, -v * h)))
        grid.append(row)
    for j in range(nv):
        for i in range(nu):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    t = p.get('thickness', 0.004)
    if t > 0:
        r = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
        moved = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        for v in moved:
            v.co += Vector((0, 0, -t)) if lay else Vector((0, t, 0))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


def _scatter(bm, p):
    """Small balls: in a box, or rising in a plume from the origin (denser and bigger low down, spreading and leaning as
    they rise)."""
    rnd = random.Random(p.get('seed', 1))
    r0, r1 = p.get('radius', [0.004, 0.012])
    n = p.get('count', 200)
    sub = p.get('subdiv', 1)
    if 'plume' in p:
        pl = p['plume']; H = pl.get('height', 2.0); s0, s1 = pl.get('spread', [0.1, 0.8]); lx, ly = pl.get('lean', [0.0, 0.0])
        taper, power = pl.get('taper', 0.6), pl.get('power', 1.6)
        for _ in range(n):
            t = rnd.random() ** power
            sp = s0 + (s1 - s0) * t
            a = rnd.uniform(0, 2 * math.pi); d = sp * math.sqrt(rnd.random())
            c = (math.cos(a) * d + lx * t * t, math.sin(a) * d + ly * t * t, H * t)
            _ico(bm, c, rnd.uniform(r0, r1) * (1 - taper * t), sub)
    else:
        x0, y0, z0, x1, y1, z1 = p.get('in', [-1, -1, 0, 1, 1, 1])
        for _ in range(n):
            _ico(bm, (rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(z0, z1)), rnd.uniform(r0, r1), sub)


def _ext(bpy, name, p):
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kit_ext')
    if d not in sys.path:
        sys.path.insert(0, d)
    mod = importlib.import_module(p['module'])
    return getattr(mod, p.get('fn', 'piece'))(bpy, name, p, sys.modules[__name__])


def finish(bpy, name, bm, p, smooth=True, mat=None):
    """A bmesh made an object with the piece's material and placement (an ext module's pieces can end with this)."""
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for f in me.polygons:
            f.use_smooth = True
    me.materials.append(mat or piece_material(bpy, p))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    if p.get('shape') != 'thread':
        ob.location = Vector(p.get('position', [0, 0, 0]))
        ob.rotation_euler = Euler([math.radians(a) for a in p.get('rotate', [0, 0, 0])])
        s = p.get('scale', 1.0)
        ob.scale = (s, s, s) if isinstance(s, (int, float)) else tuple(s)
    if p.get('shadow') is False:                          # a glow that lights the set without blocking it
        ob.visible_shadow = False
    return [ob]


def piece_material(bpy, p):
    if p.get('material') == 'pbr':                                   # a photographed texture set (assets.py)
        import assets
        # the texture's resolution is `tex_res`; `res` means it too only when it reads as one ('2k'), since a tube's or a
        # drape's `res` is its mesh resolution (a pbr tube with res 12 crashed here)
        res = p.get('tex_res') or (p['res'] if isinstance(p.get('res'), str) else '2k')
        return assets.pbr(bpy, p['texture'], res, scale=p.get('tex_scale'), displace=p.get('displace', 0.0),
                          tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), rough_mul=p.get('rough_mul', 1.0),
                          bump=p.get('bump', 1.0), coords=p.get('coords', 'object'), emit=p.get('emit_map', 0.0))
    opts = {k: p[k] for k in ('roughness', 'alpha', 'emit', 'emit_color', 'tint2', 'grain', 'rib') if k in p}
    return material(bpy, p.get('material', 'felt'), p.get('color', '#D9D4CB'), opts)


def _photographic(bpy, name, p):
    """The photographic pieces (assets.py, Poly Haven): a patch of textured ground, a scanned model, or many."""
    import assets
    shape = p['shape']
    if shape == 'ground':
        ob = assets.ground(bpy, name, p['texture'], tuple(p.get('size', [8.0, 8.0])), p.get('res', '2k'),
                           tuple(p.get('position', [0, 0, 0])), p.get('cells'), p.get('displace', 0.03), p.get('tint'),
                           p.get('tint_mix', 0.0), p.get('tex_scale'), p.get('rough_mul', 1.0), p.get('bump', 1.0), p.get('relief'),
                           tuple(p.get('flat', [0.0, 0.0, 0.9])) if p.get('flat') is not False else None)
        ob.rotation_euler.z = math.radians(p.get('rotate', [0, 0, 0])[2] if isinstance(p.get('rotate'), list) else p.get('rotate', 0))
        return [ob]
    if shape == 'asset':
        return [assets.place(bpy, p['model'], p.get('res', '2k'), tuple(p.get('position', [0, 0, 0])),
                             tuple(p.get('rotate', [0, 0, 0])), p.get('scale', 1.0), name)]
    return assets.scatter(bpy, p['models'], p.get('res', '2k'), p.get('count', 20), tuple(p.get('area', [-3, -3, 3, 3])),
                          [tuple(a) for a in p.get('avoid', [])], tuple(p.get('scale', [0.8, 1.2])), p.get('z', 0.0),
                          p.get('seed', 1), p.get('spin', True), p.get('tilt_deg', 0.0))


def piece(bpy, name, p):
    """One kit piece, placed; returns its objects."""
    shape = p.get('shape', 'sphere')
    if shape == 'ext':
        return _ext(bpy, name, p)
    if shape in ('ground', 'asset', 'scatter_assets'):
        return _photographic(bpy, name, p)
    bm = bmesh.new()
    smooth = True
    if shape == 'sphere':
        _sphere(bm, (0, 0, 0), (1, 1, 1), p.get('segments', 40))
    elif shape == 'puffs':
        d = p.get('depth', 0.7)
        for x, z, r in p['puffs']:
            _sphere(bm, (x, 0.0, z), (r, r * d, r))
    elif shape in ('cylinder', 'cone'):
        r, h = p.get('radius', 0.1), p.get('height', 0.2)
        rt = p.get('radius_top', r if shape == 'cylinder' else 0.0)
        geom = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=p.get('segments', 48), radius1=r, radius2=rt, depth=h)
        bmesh.ops.translate(bm, vec=Vector((0, 0, h / 2)), verts=geom['verts'])
        smooth = shape == 'cylinder' or rt > 0
    elif shape == 'box':
        w, dd, h = p.get('size', [0.2, 0.2, 0.2])
        geom = bmesh.ops.create_cube(bm, size=1.0)
        for v in geom['verts']:
            v.co = Vector((v.co.x * w, v.co.y * dd, (v.co.z + 0.5) * h))
        if p.get('ease', 0) > 0:
            bmesh.ops.bevel(bm, geom=bm.edges[:], offset=p['ease'], segments=2, affect='EDGES')
        smooth = False
    elif shape == 'extrude':
        _extrude(bm, p['outline'], p.get('depth', 0.006), p.get('ease', 0.0015))
        smooth = False
    elif shape == 'lathe':
        _lathe(bm, p['profile'], p.get('segments', 64))
    elif shape == 'tube':
        _tube(bm, p['points'], p.get('radius', 0.02), p.get('flat', 1.0), p.get('twist_deg', 0.0), p.get('sides', 16), p.get('res', 8))
    elif shape == 'drape':
        _drape(bm, p)
    elif shape == 'scatter':
        _scatter(bm, p)
    elif shape == 'thread':
        a, b = Vector(p['a']), Vector(p['b'])
        L = (b - a).length
        geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=p.get('radius', 0.0012), radius2=p.get('radius', 0.0012), depth=L)
        q = (b - a).to_track_quat('Z', 'Y')
        bmesh.ops.rotate(bm, verts=geom['verts'], cent=Vector((0, 0, 0)), matrix=q.to_matrix())
        bmesh.ops.translate(bm, vec=(a + b) / 2, verts=geom['verts'])
    else:
        raise ValueError(f'kit: no shape {shape!r}')
    return finish(bpy, name, bm, p, smooth)
