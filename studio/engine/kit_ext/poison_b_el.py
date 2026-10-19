"""Poison B's pieces (round 31b, spinoffs/barkhorn/elements/poison_b.py): the poisons themselves, modelled to real
scale in physically plausible materials, for a redwood forest photographed on location.

- amanita: a fly agaric (Amanita muscaria) at a given age, from the egg-shaped button to the flat, torn old cap: a
  viscid red cap fading to orange at its margin, cream warts (the universal veil's fragments, denser at the centre),
  free white gills, a drooping ring, a stem fibrous and dirtied toward its bulbous base with the volva's rings; or a
  death cap (A. phalloides): an olive cap with radial fibrils, a white ring and a cup-like volva at its foot;
- viper: a green pit viper (Trimeresurus) coiled with its head raised: keeled scales, a pale belly and a pale stripe
  low on the flank, a rust tail tip, amber eyes with vertical slits, a broad triangular head;
- dartfrog: a green-and-black dyeing dart frog (Dendrobates auratus) sitting, its skin wet;
- foxglove and nightshade: a spire of tubular bells, speckled in the throat; a sprig of glossy black berries.
Every piece is placed by `position` and `rotate` (degrees) and `scale` like any kit piece.
"""
import math, random

import bmesh
from mathutils import Matrix, Vector, noise


# --- shared ----------------------------------------------------------------------------------------------------
def _hex(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


def _node_mat(bpy, name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    return m, nt, b


def _noise(nt, scale, detail=4.0, coord='Object', rough=0.6, w=None, stretch=None):
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail
    if 'Roughness' in nz.inputs:
        nz.inputs['Roughness'].default_value = rough
    src = tc.outputs[coord]
    if stretch:
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = stretch
        nt.links.new(src, mp.inputs['Vector']); src = mp.outputs['Vector']
    nt.links.new(src, nz.inputs['Vector'])
    return nz


def _bump(nt, b, height, strength, dist, prev=None):
    bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = strength
    bn.inputs['Distance'].default_value = dist
    nt.links.new(height, bn.inputs['Height'])
    if prev is not None:
        nt.links.new(prev, bn.inputs['Normal'])
    nt.links.new(bn.outputs['Normal'], b.inputs['Normal'])
    return bn.outputs['Normal']


def _ramp(nt, fac, stops):
    r = nt.nodes.new('ShaderNodeValToRGB'); cr = r.color_ramp
    cr.elements[0].position, cr.elements[0].color = stops[0][0], (*_hex(stops[0][1]), 1)
    cr.elements[1].position, cr.elements[1].color = stops[-1][0], (*_hex(stops[-1][1]), 1)
    for pos, col in stops[1:-1]:
        e = cr.elements.new(pos); e.color = (*_hex(col), 1)
    nt.links.new(fac, r.inputs['Fac'])
    return r.outputs['Color']


def _obj(bpy, name, bm, mat, p, smooth=True):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for f in me.polygons:
            f.use_smooth = True
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler = [math.radians(a) for a in p.get('rotate', [0, 0, 0])]
    s = p.get('scale', 1.0)
    ob.scale = (s, s, s) if isinstance(s, (int, float)) else tuple(s)
    return ob


def _lathe(bm, prof, seg, wobble=None):
    """Revolve [r, z] about z; `wobble(theta, z)` scales the radius (a cap that is not quite round)."""
    rings = []
    for r, z in prof:
        if r <= 1e-7:
            rings.append([bm.verts.new((0, 0, z))])
        else:
            ring = []
            for i in range(seg):
                th = 2 * math.pi * i / seg
                k = wobble(th, z) if wobble else 1.0
                ring.append(bm.verts.new((r * k * math.cos(th), r * k * math.sin(th), z)))
            rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1 and len(b) == 1:
                continue
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[i], b[0], a[j]))
            else:
                bm.faces.new((a[i], b[i], b[j], a[j]))
    for ring, top in ((rings[0], False), (rings[-1], True)):
        if len(ring) > 1:
            bm.faces.new(ring if top else ring[::-1])


def _join(bm, build, m=None):
    """Build into a fresh bmesh, move it by `m`, join it into `bm` (fast, whatever bm's size)."""
    import bpy
    t = bmesh.new(); build(t)
    if m is not None:
        for v in t.verts:
            v.co = m @ v.co
    me = bpy.data.meshes.new('_j'); t.to_mesh(me); t.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)


# --- the mushrooms ---------------------------------------------------------------------------------------------
_AGES = {
    # cap shape by age: (height over radius, how far the margin turns under, its upturn, how far the cap is open)
    'button': (1.05, 0.55, 0.0, 0.0),
    'young': (0.7, 0.35, 0.0, 0.4),
    'convex': (0.42, 0.15, 0.0, 0.8),
    'plane': (0.3, 0.06, 0.04, 1.0),
    'old': (0.2, 0.02, 0.14, 1.0),
}


def _cap_profile(R, kind, z0):
    """The cap's outer surface from the rim (r R) to the top, and the margin's turn under it."""
    hr, under, up, _ = _AGES[kind]
    H = hr * R
    pts = []
    n = 26
    for i in range(n + 1):
        t = i / n                                         # 0 at the rim, 1 at the top
        th = t * math.pi / 2
        r = R * math.cos(th) ** (0.9 if kind not in ('plane', 'old') else 0.6)
        z = z0 + H * math.sin(th) ** (1.2 if kind not in ('plane', 'old') else 0.5)
        if up:                                            # an old cap's margin lifts, its centre dips a little
            z += up * R * (1 - t) ** 3 - 0.03 * R * math.exp(-((1 - t) / 0.12) ** 2)
        pts.append((r, z))
    pts[-1] = (0.0, pts[-1][1])
    return pts, H


def amanita(bpy, name, p, kit):
    """A fly agaric (`species` 'muscaria', the default) or a death cap ('phalloides'): `cap` its radius (m), `age` one
    of button, young, convex, plane, old, `height` from the ground to the cap's underside, `stem` radius, `lean` [dx,
    dy] at the top, `torn` 0-1 how ragged an old margin is, `warts` how many, `seed`; `wash` the rain's threshold
    (lower washes more of the veil off; 0.15 default), `ragged` how torn the bulb's veil rings are (0.03), `needles`
    how many conifer needles lie across the cap (0), `orange` an orange-red margin (False)."""
    rnd = random.Random(p.get('seed', 1))
    sp = p.get('species', 'muscaria')
    R = p.get('cap', 0.06); age = p.get('age', 'convex'); hr, under, up, open_ = _AGES[age]
    sr = p.get('stem', R * (0.13 if age != 'button' else 0.3))
    Hs = p.get('height', R * {'button': 0.55, 'young': 1.45, 'convex': 1.75, 'plane': 1.9, 'old': 2.0}[age])
    torn = p.get('torn', 0.0)
    nseg = 96
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    def wob(th, z):                                       # no cap is round: a gentle lobing, and an old one is torn
        k = 1 + 0.03 * math.sin(2 * th + ph[0]) + 0.02 * math.sin(3 * th + ph[1])
        if torn:
            k -= torn * 0.08 * max(0.0, noise.noise(Vector((math.cos(th) * 3, math.sin(th) * 3, ph[2]))) + 0.2)
        return k
    bms = {k: bmesh.new() for k in ('cap', 'gills', 'warts', 'stem', 'ring', 'volva', 'needles')}
    # stem: a bulbous base, tapering up; a button is mostly bulb
    bulb = sr * (1.9 if sp == 'muscaria' else 1.7)
    bh = min(Hs * 0.22, bulb * 2.2)                       # the bulb's height: an egg the stem rises from
    sprof = [(0.0, -0.004), (bulb * 0.55, -0.003), (bulb * 0.92, bh * 0.25), (bulb, bh * 0.5), (bulb * 0.85, bh * 0.8),
             (sr * 1.12, bh * 1.05), (sr * 1.05, bh * 1.4), (sr * 1.0, Hs * 0.55), (sr * 0.86, Hs * 0.95),
             (sr * 0.8, Hs + 0.02 * R), (0.0, Hs + 0.03 * R)]
    sprof = [(r, z) for r, z in sprof if z <= Hs + 0.03 * R + 1e-6]
    _lathe(bms['stem'], sprof, 40)
    z0 = Hs                                               # the cap's margin sits at the stem's top
    if age == 'button':
        z0 = Hs * 0.6
    pts, H = _cap_profile(R, age, z0)
    # the cap: its outer skin, the margin turning under, and its underside up to the stem
    inner = []
    rim_r, rim_z = pts[0]
    for i in range(1, 6):
        t = i / 5
        inner.append((rim_r * (1 - 0.06 * t) - R * under * 0.3 * math.sin(math.pi * t), rim_z - R * (0.02 + under * 0.25) * math.sin(math.pi * t / 2)))
    under_z = rim_z + H * 0.12 + R * 0.05
    prof = [(0.0, under_z + 0.02 * R), (sr * 1.1, under_z), (R * 0.88 * (1 - under * 0.5), rim_z - R * 0.01)] + inner[::-1] + pts
    _lathe(bms['cap'], prof, nseg, wob)
    # the gills: thin radial blades under the cap, from the stem's collar to the margin (free of the stem)
    if age != 'button':
        ng = p.get('gills', 110)
        for g in range(ng):
            th = 2 * math.pi * g / ng + rnd.uniform(-0.01, 0.01)
            r0 = sr * 1.35 if g % 2 == 0 else R * 0.45      # lamellulae: every other gill short
            r1 = R * 0.86 * wob(th, 0)
            depth = R * (0.11 if age in ('convex', 'young') else 0.08)
            def gill(bm, th=th, r0=r0, r1=r1, depth=depth):
                c, s = math.cos(th), math.sin(th); w = R * 0.0055
                vs = []
                for k in range(7):
                    u = k / 6; r = r0 + (r1 - r0) * u
                    zt = under_z + (rim_z - R * 0.015 - under_z) * u ** 1.4 - 0.002 * R
                    d = depth * math.sin(math.pi * min(1.0, 0.15 + u)) * (0.6 + 0.4 * (1 - u))
                    for side in (-1, 1):
                        vs.append(((r * c - side * w * s), (r * s + side * w * c), zt))
                        vs.append(((r * c - side * w * s * 0.3), (r * s + side * w * c * 0.3), zt - d))
                V = [bm.verts.new(v) for v in vs]
                for k in range(6):
                    a = k * 4
                    for q in ((a, a + 4, a + 5, a + 1), (a + 2, a + 3, a + 7, a + 6), (a + 1, a + 5, a + 7, a + 3)):
                        bm.faces.new([V[i] for i in q])
            _join(bms['gills'], gill)
    # warts: the veil's fragments on a fly agaric, thick at the centre, sparse at the margin; none on a death cap
    if sp == 'muscaria':
        nw = p.get('warts', {'button': 150, 'young': 110, 'convex': 85, 'plane': 65, 'old': 40}[age])
        for k in range(nw):
            t = 1 - rnd.random() ** 1.6                   # nearer the top more often
            th0 = rnd.uniform(0, 2 * math.pi)
            if noise.noise(Vector((math.cos(th0) * 2, math.sin(th0) * 2, t * 3 + ph[0]))) > (p['wash'] - 0.35 * (1 - t) if 'wash' in p else 0.15) and age in ('plane', 'old', 'convex'):
                continue                                  # the rain has washed this patch of veil off
            i = min(len(pts) - 2, int(t * (len(pts) - 1)))
            th = th0
            (ra, za), (rb, zb) = pts[i], pts[i + 1]
            u = rnd.random(); r = (ra + (rb - ra) * u) * wob(th, 0); z = za + (zb - za) * u
            nr, nz = (zb - za), -(rb - ra); L = math.hypot(nr, nz) or 1; nr, nz = nr / L, nz / L
            n = Vector((nr * math.cos(th), nr * math.sin(th), nz))
            s = R * rnd.uniform(0.03, 0.085) * (1.2 if age == 'button' else 1.0) * (1.25 - 0.55 * (1 - t))
            def wart(bm, s=s):
                g = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
                for v in g['verts']:
                    j = 1 + 0.35 * rnd.uniform(-1, 1)
                    v.co = Vector((v.co.x * s * j, v.co.y * s * j * rnd.uniform(0.6, 1.0), max(-0.2, v.co.z) * s * 0.4 * j))
            m = Matrix.Translation(Vector((r * math.cos(th), r * math.sin(th), z)) + n * s * 0.1) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4() @ Matrix.Rotation(rnd.uniform(0, 6.28), 4, 'Z')
            _join(bms['warts'], wart, m)
    # needles fallen across the cap: thin flat slivers lying on its surface, 1.5-2.5 cm long
    for k in range(p.get('needles', 0)):
        t = rnd.uniform(0.25, 0.8); th = rnd.uniform(0, 2 * math.pi)
        i = min(len(pts) - 2, int(t * (len(pts) - 1)))
        (ra, za), (rb, zb) = pts[i], pts[i + 1]
        r = ra * wob(th, 0); z = za
        nr, nz = (zb - za), -(rb - ra); L = math.hypot(nr, nz) or 1; nr, nz = nr / L, nz / L
        n = Vector((nr * math.cos(th), nr * math.sin(th), nz))
        ln_, w_ = rnd.uniform(0.015, 0.025), 0.0009
        def needle(bm, ln_=ln_, w_=w_):
            g = bmesh.ops.create_cube(bm, size=1.0)
            for v in g['verts']:
                v.co = Vector((v.co.x * ln_, v.co.y * w_, v.co.z * w_ * 0.5))
        m = Matrix.Translation(Vector((r * math.cos(th), r * math.sin(th), z)) + n * 0.0006) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4() @ Matrix.Rotation(rnd.uniform(0, 6.28), 4, 'Z')
        _join(bms['needles'], needle, m)
    # the ring: a skirt hanging from the stem's top
    if age != 'button':
        zr = Hs * 0.84
        rr = [(sr * 0.92, zr + 0.01 * R), (sr * 1.35, zr - 0.02 * R), (sr * 1.7, zr - 0.1 * R), (sr * 1.75, zr - 0.2 * R),
              (sr * 1.62, zr - 0.205 * R), (sr * 1.55, zr - 0.11 * R), (sr * 1.2, zr - 0.035 * R), (sr * 0.88, zr - 0.012 * R)]
        _lathe(bms['ring'], rr, 48, lambda th, z: 1 + 0.12 * math.sin(5 * th + ph[3]) * max(0.0, (Hs * 0.86 - z) / (0.13 * R)))
    # the volva: rings of veil round a fly agaric's bulb, a loose cup round a death cap's
    if sp == 'muscaria':
        for k in range(3):                                # the veil's torn rings on the top of the bulb
            zv = bh * (0.62 + 0.17 * k)
            rv = bulb * (0.93 - 0.17 * k) if k < 2 else sr * 1.25
            _lathe(bms['volva'], [(rv * 0.97, zv - 0.004 * R), (rv * 1.035, zv), (rv * 1.03, zv + 0.004 * R), (rv * 0.97, zv + 0.003 * R)], 40,
                   lambda th, z, k=k: 1 + p.get('ragged', 0.03) * noise.noise(Vector((math.cos(th) * 6, math.sin(th) * 6, k * 3))))
    else:
        cup = [(bulb * 1.02, -0.003), (bulb * 1.1, bh * 0.5), (bulb * 1.22, bh * 1.05), (bulb * 1.15, bh * 1.1), (bulb * 1.0, bh * 0.55)]
        _lathe(bms['volva'], cup, 40, lambda th, z: 1 + 0.12 * noise.noise(Vector((math.cos(th) * 3, math.sin(th) * 3, z * 40))))
    # lean: the stem bends, the cap tilts with it
    lx, ly = p.get('lean', [0.0, 0.0])
    top = max(Hs, 1e-3)
    for bm in bms.values():
        for v in bm.verts:
            t = max(0.0, min(1.5, v.co.z / top)); v.co.x += lx * t * t; v.co.y += ly * t * t
    mats = _amanita_mats(bpy, name, sp, R, Hs, p.get('orange', False), p.get('dull', 0.0), p.get('matte', False))
    obs = []
    for k, bm in bms.items():
        if len(bm.verts):
            obs.append(_obj(bpy, f'{name}-{k}', bm, mats[k], p))
        else:
            bm.free()
    return obs


def _amanita_mats(bpy, name, sp, R, Hs, orange=False, dull=0.0, matte=False):
    key = (sp,)
    out = {}
    # the cap: viscid (a wet, thin coat), red with orange toward the margin and blotchy, a little light through it
    m, nt, b = _node_mat(bpy, f'{name}-capmat')
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    # radial position on the cap: the distance from the axis, over R
    vl = nt.nodes.new('ShaderNodeVectorMath'); vl.operation = 'MULTIPLY'; vl.inputs[1].default_value = (1, 1, 0)
    nt.links.new(tc.outputs['Object'], vl.inputs[0])
    ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; nt.links.new(vl.outputs['Vector'], ln.inputs[0])
    dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = R
    nt.links.new(ln.outputs['Value'], dv.inputs[0])
    nz = _noise(nt, 1.0 / (R * 0.5), 3.0)
    mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'
    nt.links.new(nz.outputs['Fac'], mix.inputs[0]); mix.inputs[1].default_value = 0.35
    nt.links.new(dv.outputs['Value'], mix.inputs[2])
    if sp == 'muscaria':
        col = _ramp(nt, mix.outputs['Value'], [(0.15, '#3A0101'), (0.5, '#6A0302'), (0.9, '#8A0A03'), (1.2, '#A8300A')] if not orange
                    else [(0.15, '#4A0402'), (0.45, '#7A0803'), (0.8, '#A01C05'), (1.1, '#C4420E')])
        b.inputs['Subsurface Weight'].default_value = 0.12
    else:
        # olive-green to yellowish at the margin, with dark radial fibrils
        col = _ramp(nt, mix.outputs['Value'], [(0.1, '#3C4018'), (0.5, '#5A5E28'), (0.9, '#7E8044'), (1.2, '#A3A06A')])
        b.inputs['Subsurface Weight'].default_value = 0.08
    if dull:                                              # weathered: the red toward a brown, as an old cap goes
        dm = nt.nodes.new('ShaderNodeMix'); dm.data_type = 'RGBA'; dm.inputs['Factor'].default_value = dull
        nt.links.new(col, dm.inputs['A']); dm.inputs['B'].default_value = (*_hex('#4A2414'), 1); col = dm.outputs['Result']
    nt.links.new(col, b.inputs['Base Color'])
    b.inputs['Subsurface Radius'].default_value = (0.003, 0.0012, 0.0006)
    b.inputs['Roughness'].default_value = 0.55
    b.inputs['Coat Weight'].default_value = 0.15; b.inputs['Coat Roughness'].default_value = 0.25
    if matte:                                             # a dried cap: no viscid coat, a soft sheen at most
        b.inputs['Roughness'].default_value = 0.68; b.inputs['Coat Weight'].default_value = 0.04
    fib = _noise(nt, 1.0 / (R * 0.06), 6.0, stretch=(1.0, 1.0, 1.0))
    n1 = _bump(nt, b, fib.outputs['Fac'], 0.25, R * 0.004)
    # the striate margin: fine radial grooves in the outer fifth of the cap
    gr = nt.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'RADIAL'
    nt.links.new(tc.outputs['Object'], gr.inputs['Vector'])
    wv = nt.nodes.new('ShaderNodeMath'); wv.operation = 'SINE'
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 2 * math.pi * 90
    nt.links.new(gr.outputs['Fac'], mul.inputs[0]); nt.links.new(mul.outputs['Value'], wv.inputs[0])
    edge = nt.nodes.new('ShaderNodeMapRange'); edge.inputs['From Min'].default_value = 0.78; edge.inputs['From Max'].default_value = 0.98
    nt.links.new(dv.outputs['Value'], edge.inputs['Value'])
    st = nt.nodes.new('ShaderNodeMath'); st.operation = 'MULTIPLY'
    nt.links.new(wv.outputs['Value'], st.inputs[0]); nt.links.new(edge.outputs['Result'], st.inputs[1])
    _bump(nt, b, st.outputs['Value'], 0.35 if sp == 'muscaria' else 0.0, R * 0.003, prev=n1)
    out['cap'] = m
    # warts: cream, dirty, crumbly
    m, nt, b = _node_mat(bpy, f'{name}-wartmat')
    nz = _noise(nt, 1.0 / (R * 0.03), 5.0)
    nt.links.new(_ramp(nt, nz.outputs['Fac'], [(0.3, '#CFC09A'), (0.6, '#E4DABA'), (0.8, '#A89668')] if not dull
                       else [(0.3, '#A89A78'), (0.6, '#BDB090'), (0.8, '#857452')]), b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.85; b.inputs['Subsurface Weight'].default_value = 0.1
    _bump(nt, b, nz.outputs['Fac'], 0.6, R * 0.003)
    out['warts'] = m
    # gills: white, a little translucent
    m, nt, b = _node_mat(bpy, f'{name}-gillmat')
    b.inputs['Base Color'].default_value = (*_hex('#EDE9DC'), 1); b.inputs['Roughness'].default_value = 0.7
    b.inputs['Subsurface Weight'].default_value = 0.3; b.inputs['Subsurface Radius'].default_value = (0.002, 0.002, 0.0015)
    out['gills'] = m
    # stem, ring, volva: white, fibrous along the stem, the soil's stain rising from the base
    for k in ('stem', 'ring', 'volva'):
        m, nt, b = _node_mat(bpy, f'{name}-{k}mat')
        tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
        nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
        hz = nt.nodes.new('ShaderNodeMath'); hz.operation = 'DIVIDE'; hz.inputs[1].default_value = max(Hs, 1e-3)
        nt.links.new(sep.outputs['Z'], hz.inputs[0])
        nz = _noise(nt, 1.0 / (R * 0.08), 4.0)
        mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MULTIPLY_ADD'
        nt.links.new(nz.outputs['Fac'], mx.inputs[0]); mx.inputs[1].default_value = 0.25; nt.links.new(hz.outputs['Value'], mx.inputs[2])
        cols = [(0.05, '#5A4A32'), (0.2, '#A39478'), (0.38, '#D6CCB2'), (1.0, '#E6DEC8')]
        if k == 'volva' and sp != 'muscaria':
            cols = [(0.0, '#7A6A4E'), (0.25, '#CFC6AE'), (1.0, '#EDE8DA')]
        nt.links.new(_ramp(nt, mx.outputs['Value'], cols), b.inputs['Base Color'])
        b.inputs['Roughness'].default_value = 0.72; b.inputs['Subsurface Weight'].default_value = 0.15
        b.inputs['Subsurface Radius'].default_value = (0.003, 0.003, 0.002)
        fib = _noise(nt, 1.0 / (R * 0.04), 6.0, stretch=(14.0, 14.0, 0.5))
        _bump(nt, b, fib.outputs['Fac'], 0.7, R * 0.004)
        out[k] = m
    # needles: redwood needles gone brown
    m, nt, b = _node_mat(bpy, f'{name}-needlemat')
    b.inputs['Base Color'].default_value = (*_hex('#6A4A2A'), 1); b.inputs['Roughness'].default_value = 0.6
    out['needles'] = m
    return out


# --- the viper -------------------------------------------------------------------------------------------------
def _coil_path(p):
    """The body's centreline: a flat coil of `turns` turns from `r_out` inward, lying on z 0, then the neck rising in
    an S to the head at `head` [x, y, z] (in the piece's frame), the snout along `look` (degrees about z)."""
    turns, r_out, r_in = p.get('turns', 1.6), p.get('r_out', 0.16), p.get('r_in', 0.07)
    pts = []
    n = int(70 * turns)
    for i in range(n + 1):
        t = i / n
        th = -2 * math.pi * turns * t
        r = (r_out + (r_in - r_out) * t) * (1 + 0.07 * math.sin(3 * th + 0.7) + 0.04 * math.sin(5 * th))
        z = p.get('girth', 0.02) * 0.82 + p.get('girth', 0.02) * 1.5 * max(0.0, t - 0.5) / 0.5   # inner turns ride up onto the outer
        pts.append(Vector((r * math.cos(th), r * math.sin(th), z)))
    hx, hy, hz = p.get('head', [0.05, -0.06, 0.16])
    a = pts[-1]
    look = math.radians(p.get('look', -60))
    d = Vector((math.cos(look), math.sin(look), 0))
    ctrl = [a, a + Vector((0, 0, hz * 0.55)) - d * 0.05, Vector((hx, hy, hz)) - d * 0.09 + Vector((0, 0, 0.03)),
            Vector((hx, hy, hz))]
    for i in range(1, 25):                                    # a cubic Bezier for the S of the neck
        u = i / 24
        q = ((1 - u) ** 3) * ctrl[0] + 3 * ((1 - u) ** 2) * u * ctrl[1] + 3 * (1 - u) * u * u * ctrl[2] + u ** 3 * ctrl[3]
        pts.append(q)
    return pts, d


def viper(bpy, name, p, kit):
    """A coiled green pit viper: `length` about 0.7 m (its coil `turns`, `r_out`, `r_in`), its body `girth` (radius,
    m) at its thickest, its head raised to `head` [x, y, z] (in the piece's frame), looking along `look` degrees.
    Colours: `green`, `belly`, `stripe`, `tail` (the rust tip). The tail's thin end is the coil's outer end."""
    g = p.get('girth', 0.017)
    if p.get('drop'):                                     # lie on whatever is below: the highest hit under the coil
        p = dict(p); x, y, z = p['position']
        bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
        best = None; rr = p.get('r_out', 0.16)
        for dx, dy in ((0, 0), (rr * 0.7, 0), (-rr * 0.7, 0), (0, rr * 0.7), (0, -rr * 0.7)):
            hit, loc, *_ = bpy.context.scene.ray_cast(dg, Vector((x + dx, y + dy, z + 2.0)), Vector((0, 0, -1)), distance=4.0)
            if hit:
                best = loc.z if best is None else max(best, loc.z)
        if best is not None:
            p['position'] = [x, y, best - g * 0.25]
    pts, look = _coil_path(p)
    N = len(pts)
    # radius along the body: a thin tail at the coil's outside, thickest a third of the way in, thinning to the neck
    def rad(t):
        if t < 0.18:
            return g * (0.12 + 0.88 * (t / 0.18) ** 0.8)
        if t < 0.82:
            return g * (1.0 - 0.15 * ((t - 0.45) / 0.37) ** 2)
        return g * (0.85 - 0.38 * (t - 0.82) / 0.18)
    radii = [rad(i / (N - 1)) for i in range(N)]
    bm = bmesh.new()
    kit._tube(bm, [tuple(v) for v in pts], radii, 0.82, 0.0, 28, 4)
    # the head: a broad triangular wedge, flat on top, the snout tapering, at the neck's end along `look`
    head = bmesh.new()
    hp = pts[-1]
    hd = (pts[-1] - pts[-4]).normalized()
    hd.z *= 0.3; hd.normalize()
    side = hd.cross(Vector((0, 0, 1))).normalized(); up = side.cross(hd).normalized()
    HL, HW, HH = g * 3.0, g * 2.15, g * 0.95
    seg_u, seg_v = 20, 24
    rows = []
    for i in range(seg_u + 1):
        u = i / seg_u                                          # 0 at the neck, 1 at the snout
        w = HW * (0.55 + 0.45 * math.sin(math.pi * min(1.0, u / 0.6) / 2) ** 0.7 - 0.6 * max(0.0, u - 0.35) ** 1.3)
        h = HH * (0.95 - 0.35 * u ** 1.5)
        c = hp + hd * (HL * u - g * 0.4)
        ring = []
        for j in range(seg_v):
            a = 2 * math.pi * j / seg_v
            cy, cz = math.cos(a), math.sin(a)
            cz = (cz ** 0.6 if cz > 0 else -((-cz) ** 0.8)) * (0.75 if cz > 0 else 1.0)   # a flat crown, a rounder jaw
            pz = h * cz * (1.0 - 0.25 * abs(cy) ** 3)
            ring.append(head.verts.new(c + side * (w * cy) + up * pz))
        rows.append(ring)
    for a_, b_ in zip(rows, rows[1:]):
        for j in range(seg_v):
            k = (j + 1) % seg_v
            head.faces.new((a_[j], a_[k], b_[k], b_[j]))
    tip = head.verts.new(hp + hd * (HL * 1.06 - g * 0.4))
    for j in range(seg_v):
        head.faces.new((rows[-1][j], rows[-1][(j + 1) % seg_v], tip))
    head.faces.new(rows[0][::-1])
    # the eyes: amber, glossy, set high on the sides, forward of the middle
    eyes = bmesh.new()
    for s in (-1, 1):
        ec = hp + hd * (HL * 0.62 - g * 0.4) + side * s * HW * 0.8 + up * HH * 0.25
        kit._sphere(eyes, tuple(ec), (g * 0.24,) * 3, 24)
    obs = []
    m_body = _viper_mat(bpy, f'{name}-skin', p, g)
    for nm, b_ in (('body', bm), ('head', head)):
        obs.append(_obj(bpy, f'{name}-{nm}', b_, m_body, p))
    m_eye, nt, b = _node_mat(bpy, f'{name}-eye')
    # amber iris with a vertical slit: the slit by the object's x (the eye's own frame is the snake's, near enough)
    b.inputs['Base Color'].default_value = (*_hex('#C8901A'), 1)
    b.inputs['Roughness'].default_value = 0.05; b.inputs['Coat Weight'].default_value = 1.0
    b.inputs['Coat Roughness'].default_value = 0.02
    obs.append(_obj(bpy, f'{name}-eyes', eyes, m_eye, p))
    # the pupils: thin black slits on each eye's outer face
    pup = bmesh.new()
    for s in (-1, 1):
        ec = hp + hd * (HL * 0.62 - g * 0.4) + side * s * HW * 0.8 + up * HH * 0.25 + side * s * g * 0.21
        m = Matrix.Translation(ec) @ Matrix((hd, up, side)).transposed().to_4x4()
        _join(pup, lambda t: kit._sphere(t, (0, 0, 0), (g * 0.04, g * 0.17, g * 0.04), 12), m)
    m_pup, nt, b = _node_mat(bpy, f'{name}-pupil')
    b.inputs['Base Color'].default_value = (0.005, 0.005, 0.004, 1); b.inputs['Roughness'].default_value = 0.1
    obs.append(_obj(bpy, f'{name}-pupils', pup, m_pup, p))
    return obs


def _viper_mat(bpy, name, p, g):
    """Keeled scales (Voronoi cells about a scale wide, raised and ridged), green on top, pale belly and a pale
    flank stripe by the surface's facing (its normal), the tail's tip rust by the distance from its end (object
    position on the coil's outside), a waxy sheen."""
    m, nt, b = _node_mat(bpy, name)
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(geo.outputs['Normal'], sep.inputs['Vector'])
    # facing: -1 belly, 0 flank, +1 back
    nzc = sep.outputs['Z']
    base = _ramp(nt, nzc, [(0.0, p.get('belly', '#A8B064')), (0.38, p.get('stripe', '#C8D290')),
                           (0.47, p.get('green', '#3E7A22')), (0.75, p.get('green', '#3A7020')), (1.0, p.get('green2', '#2E5A18'))])
    # the ramp works on 0..1; map z from [-1, 1]
    mp = nt.nodes.new('ShaderNodeMapRange'); mp.inputs['From Min'].default_value = -1.0; mp.inputs['From Max'].default_value = 1.0
    nt.links.new(nzc, mp.inputs['Value'])
    nt.links.new(mp.outputs['Result'], base.node.inputs['Fac'])
    # the scales
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.feature = 'F1'; vor.inputs['Scale'].default_value = 1.0 / (g * 0.17)
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    vor2 = nt.nodes.new('ShaderNodeTexVoronoi'); vor2.feature = 'DISTANCE_TO_EDGE'; vor2.inputs['Scale'].default_value = 1.0 / (g * 0.17)
    nt.links.new(tc.outputs['Object'], vor2.inputs['Vector'])
    # darker in the seams between scales, each scale's own shade a little different
    seam = nt.nodes.new('ShaderNodeMapRange'); seam.inputs['From Min'].default_value = 0.0; seam.inputs['From Max'].default_value = 0.08
    seam.inputs['To Min'].default_value = 0.6; seam.inputs['To Max'].default_value = 1.0
    nt.links.new(vor2.outputs['Distance'], seam.inputs['Value'])
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1.0
    nt.links.new(base, mul.inputs['A'])
    sv = nt.nodes.new('ShaderNodeCombineXYZ')
    for k in ('X', 'Y', 'Z'):
        nt.links.new(seam.outputs['Result'], sv.inputs[k])
    nt.links.new(sv.outputs['Vector'], mul.inputs['B'])
    col = mul.outputs['Result']
    # the tail's rust tip: the coil's outermost part, by distance from the axis
    vl = nt.nodes.new('ShaderNodeVectorMath'); vl.operation = 'MULTIPLY'; vl.inputs[1].default_value = (1, 1, 0)
    nt.links.new(tc.outputs['Object'], vl.inputs[0])
    ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; nt.links.new(vl.outputs['Vector'], ln.inputs[0])
    ang = nt.nodes.new('ShaderNodeVectorMath'); ang.operation = 'DOT_PRODUCT'
    nt.links.new(tc.outputs['Object'], ang.inputs[0]); ang.inputs[1].default_value = (1, 0, 0)
    r_out = p.get('r_out', 0.16)
    tipm = nt.nodes.new('ShaderNodeMapRange'); tipm.interpolation_type = 'SMOOTHSTEP'
    tipm.inputs['From Min'].default_value = r_out - 0.01; tipm.inputs['From Max'].default_value = r_out + 0.008
    nt.links.new(ln.outputs['Value'], tipm.inputs['Value'])
    tipa = nt.nodes.new('ShaderNodeMapRange'); tipa.interpolation_type = 'SMOOTHSTEP'
    tipa.inputs['From Min'].default_value = r_out * 0.55; tipa.inputs['From Max'].default_value = r_out * 0.95
    nt.links.new(ang.outputs['Value'], tipa.inputs['Value'])
    tf = nt.nodes.new('ShaderNodeMath'); tf.operation = 'MULTIPLY'
    nt.links.new(tipm.outputs['Result'], tf.inputs[0]); nt.links.new(tipa.outputs['Result'], tf.inputs[1])
    sepz = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sepz.inputs['Vector'])
    low = nt.nodes.new('ShaderNodeMapRange'); low.inputs['From Min'].default_value = g * 1.6; low.inputs['From Max'].default_value = g * 2.2
    low.inputs['To Min'].default_value = 1.0; low.inputs['To Max'].default_value = 0.0
    nt.links.new(sepz.outputs['Z'], low.inputs['Value'])
    tf2 = nt.nodes.new('ShaderNodeMath'); tf2.operation = 'MULTIPLY'
    nt.links.new(tf.outputs['Value'], tf2.inputs[0]); nt.links.new(low.outputs['Result'], tf2.inputs[1]); tf = tf2
    tmix = nt.nodes.new('ShaderNodeMix'); tmix.data_type = 'RGBA'
    nt.links.new(tf.outputs['Value'], tmix.inputs['Factor']); nt.links.new(col, tmix.inputs['A'])
    tmix.inputs['B'].default_value = (*_hex(p.get('tail', '#8A3A1A')), 1)
    nt.links.new(tmix.outputs['Result'], b.inputs['Base Color'])
    # keeled scales: each cell domed, with a ridge along the body (stretched noise)
    dome = nt.nodes.new('ShaderNodeMath'); dome.operation = 'POWER'; dome.inputs[1].default_value = 0.6
    nt.links.new(vor2.outputs['Distance'], dome.inputs[0])
    n1 = _bump(nt, b, dome.outputs['Value'], 1.0, g * 0.035)
    b.inputs['Roughness'].default_value = 0.45
    b.inputs['Coat Weight'].default_value = 0.1; b.inputs['Coat Roughness'].default_value = 0.2
    b.inputs['Subsurface Weight'].default_value = 0.2
    b.inputs['Subsurface Radius'].default_value = (0.002, 0.004, 0.0008)
    b.inputs['Sheen Weight'].default_value = 0.15
    return m


# --- the dart frog ---------------------------------------------------------------------------------------------
def dartfrog(bpy, name, p, kit):
    """A dyeing dart frog sitting, `size` (snout to vent, m, about 0.035), facing +y in its frame: green blotches on
    black, glossy wet skin."""
    s = p.get('size', 0.035)
    if p.get('drop'):                                     # sit on whatever is below
        p = dict(p); x, y, z = p['position']
        bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
        hit, loc, *_ = bpy.context.scene.ray_cast(dg, Vector((x, y, z + 1.0)), Vector((0, 0, -1)), distance=2.0)
        if hit:
            p['position'] = [x, y, loc.z - s * 0.02]
    bm = bmesh.new()
    # body: a plump ellipsoid tilted up at the front; head merged forward
    kit._sphere(bm, (0, 0, s * 0.32), (s * 0.34, s * 0.5, s * 0.28), 40)
    _join(bm, lambda t: kit._sphere(t, (0, 0, 0), (s * 0.3, s * 0.28, s * 0.2), 32),
          Matrix.Translation((0, s * 0.42, s * 0.42)) @ Matrix.Rotation(math.radians(-15), 4, 'X'))
    # legs: tubes from hip and shoulder, folded, with toe pads
    def leg(pts, r):
        _join(bm, lambda t: kit._tube(t, pts, r, 1.0, 0.0, 10, 4))
    for sx in (-1, 1):
        # hind leg: thigh out and forward, shin back, foot forward
        leg([(sx * s * 0.25, -s * 0.25, s * 0.25), (sx * s * 0.5, -s * 0.05, s * 0.15), (sx * s * 0.45, -s * 0.35, s * 0.06),
             (sx * s * 0.55, -s * 0.05, s * 0.02)], [s * 0.1, s * 0.08, s * 0.05, s * 0.035])
        # foreleg: down from the shoulder to the ground in front
        leg([(sx * s * 0.22, s * 0.3, s * 0.3), (sx * s * 0.32, s * 0.45, s * 0.15), (sx * s * 0.3, s * 0.58, s * 0.02)],
            [s * 0.06, s * 0.045, s * 0.035])
        for k in range(4):                                     # toe pads
            a = math.radians(-50 + 33 * k) * sx
            for base, L in (((sx * s * 0.3, s * 0.58, s * 0.015), s * 0.09), ((sx * s * 0.55, -s * 0.05, s * 0.015), s * 0.13)):
                tip = (base[0] + math.sin(a) * L * sx, base[1] + math.cos(a) * L, s * 0.012)
                leg([base, tip], [s * 0.016, s * 0.012])
                _join(bm, lambda t, tip=tip: kit._sphere(t, tip, (s * 0.022, s * 0.022, s * 0.014), 10))
    eyes = bmesh.new()
    for sx in (-1, 1):
        kit._sphere(eyes, (sx * s * 0.2, s * 0.5, s * 0.5), (s * 0.085,) * 3, 20)
    m, nt, b = _node_mat(bpy, f'{name}-skin')
    nz = _noise(nt, 1.0 / (s * 0.22), 3.0, rough=0.5)
    cut = nt.nodes.new('ShaderNodeMapRange'); cut.interpolation_type = 'SMOOTHSTEP'
    cut.inputs['From Min'].default_value = 0.47; cut.inputs['From Max'].default_value = 0.53
    nt.links.new(nz.outputs['Fac'], cut.inputs['Value'])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
    nt.links.new(cut.outputs['Result'], mx.inputs['Factor'])
    mx.inputs['A'].default_value = (*_hex('#0A0C0A'), 1); mx.inputs['B'].default_value = (*_hex(p.get('green', '#3FD27A')), 1)
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.25; b.inputs['Coat Weight'].default_value = 0.8; b.inputs['Coat Roughness'].default_value = 0.05
    b.inputs['Subsurface Weight'].default_value = 0.1
    gr = _noise(nt, 1.0 / (s * 0.03), 3.0)
    _bump(nt, b, gr.outputs['Fac'], 0.25, s * 0.004)
    me, nte, be = _node_mat(bpy, f'{name}-eye')
    be.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1); be.inputs['Roughness'].default_value = 0.03
    be.inputs['Coat Weight'].default_value = 1.0
    return [_obj(bpy, f'{name}-body', bm, m, p), _obj(bpy, f'{name}-eyes', eyes, me, p)]


# --- foxglove and nightshade -------------------------------------------------------------------------------------
def _petal_mat(bpy, name, col, throat='#F2DCEB', spots='#5A1438'):
    m, nt, b = _node_mat(bpy, name)
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    b.inputs['Base Color'].default_value = (*_hex(col), 1)
    b.inputs['Roughness'].default_value = 0.55; b.inputs['Subsurface Weight'].default_value = 0.35
    b.inputs['Subsurface Radius'].default_value = (0.004, 0.0015, 0.003)
    b.inputs['Sheen Weight'].default_value = 0.3
    return m


def foxglove(bpy, name, p, kit):
    """A foxglove spire `height` tall: a stem bending by `lean`, `bells` tubular bells hung on one side down its upper
    part (largest lowest), buds at the tip, a rosette of leaves at its foot. `droop` 0-1 hangs the bells' mouths down
    (unset: out and down at 45 deg), `crowd` above 1 packs them toward the bottom, `pedicel` the stalk each hangs on (m)."""
    rnd = random.Random(p.get('seed', 3))
    H = p.get('height', 1.2); lx, ly = p.get('lean', [0.03, 0.0]); side = math.radians(p.get('side', -90))
    stem, bells, inner, buds, leaves = bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new()
    def axis(t):
        return Vector((lx * t * t, ly * t * t, H * t))
    kit._tube(stem, [tuple(axis(t)) for t in (0.0, 0.3, 0.6, 0.85, 1.0)], [H * 0.008, H * 0.0065, H * 0.005, H * 0.0035, H * 0.002], 1.0, 0.0, 10, 8)
    n = p.get('bells', 22); br = p.get('bell', 0.017)
    for i in range(n):
        t = 0.42 + 0.48 * (i / (n - 1)) ** p.get('crowd', 1.0)
        size = br * (1.0 - 0.5 * (i / n) ** 1.3)
        a = side + rnd.uniform(-0.8, 0.8)
        out = Vector((math.cos(a), math.sin(a), 0.0))
        L = size * 2.8
        dr = p.get('droop')
        d = (out * 0.75 + Vector((0, 0, -0.65))).normalized() if dr is None else (out * (1 - dr) + Vector((0, 0, -dr))).normalized()
        base = axis(t) + out * p.get('pedicel', H * 0.004)
        m = Matrix.Translation(base) @ (-d).to_track_quat('Z', 'Y').to_matrix().to_4x4()
        # a bell along local -z from its base at the stem (z 0) to its mouth (z -L): tubular, flared at the lip
        prof = [(0.0, 0.0), (size * 0.32, -L * 0.05), (size * 0.55, -L * 0.3), (size * 0.72, -L * 0.7), (size * 0.95, -L * 0.95),
                (size * 1.05, -L), (size * 0.85, -L * 0.98), (size * 0.62, -L * 0.85)]
        _join(bells, lambda t_, prof=prof: _lathe(t_, prof, 28, lambda th, z: 1 + 0.12 * math.cos(th) * max(0.0, -z / L - 0.6)), m)
        # the throat: a pale disc set inside, freckled by its material
        _join(inner, lambda t_, size=size, L=L: _lathe(t_, [(0.0, -L * 0.6), (size * 0.6, -L * 0.85), (size * 0.6, -L * 0.86), (0.0, -L * 0.62)], 20), m)
        # a short pedicel
    for i in range(p.get('buds', 7)):
        t = 0.91 + 0.08 * i / 7
        a = rnd.uniform(0, 6.28)
        c = axis(t) + Vector((math.cos(a), math.sin(a), 0)) * H * 0.006
        sz = br * (0.45 - 0.04 * i)
        _join(buds, lambda t_, sz=sz: kit._sphere(t_, (0, 0, 0), (sz * 0.6, sz * 0.6, sz * 1.1), 14), Matrix.Translation(c))
    for i in range(p.get('leaves', 9)):
        a = 2 * math.pi * i / 9 + rnd.uniform(-0.3, 0.3)
        Ll = H * rnd.uniform(0.18, 0.26)
        dv = Vector((math.cos(a), math.sin(a), 0.22)).normalized()
        m = Matrix.Translation(dv * Ll * 0.5) @ dv.to_track_quat('Z', 'X').to_matrix().to_4x4()
        _join(leaves, lambda t_, Ll=Ll: kit._sphere(t_, (0, 0, 0), (Ll * 0.2, Ll * 0.035, Ll * 0.55), 20), m)
    # materials
    m_bell = _petal_mat(bpy, f'{name}-bell', p.get('color', '#9C3F8C'))
    m_in, nt, b = _node_mat(bpy, f'{name}-throat')
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 1.0 / (br * 0.18)
    tc = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    sp = nt.nodes.new('ShaderNodeMapRange'); sp.inputs['From Min'].default_value = 0.18; sp.inputs['From Max'].default_value = 0.24
    nt.links.new(vor.outputs['Distance'], sp.inputs['Value'])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; nt.links.new(sp.outputs['Result'], mx.inputs['Factor'])
    mx.inputs['A'].default_value = (*_hex('#4A0E30'), 1); mx.inputs['B'].default_value = (*_hex('#EED8E6'), 1)
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.6
    b.inputs['Subsurface Weight'].default_value = 0.3
    m_leaf, nt, b = _node_mat(bpy, f'{name}-leaf')
    b.inputs['Base Color'].default_value = (*_hex('#3C5A26'), 1); b.inputs['Roughness'].default_value = 0.65
    b.inputs['Sheen Weight'].default_value = 0.6; b.inputs['Sheen Roughness'].default_value = 0.5   # downy
    b.inputs['Subsurface Weight'].default_value = 0.15
    nz = _noise(nt, 1.0 / 0.004, 6.0); _bump(nt, b, nz.outputs['Fac'], 0.3, 0.0008)
    return [_obj(bpy, f'{name}-stem', stem, m_leaf, p), _obj(bpy, f'{name}-bells', bells, m_bell, p),
            _obj(bpy, f'{name}-throats', inner, m_in, p), _obj(bpy, f'{name}-buds', buds, m_leaf, p),
            _obj(bpy, f'{name}-leaves', leaves, m_leaf, p)]


def nightshade(bpy, name, p, kit):
    """A sprig of deadly nightshade (Atropa belladonna): a stalk `height` tall, glossy black berries `berry` in radius,
    each seated in a green star of calyx, a few leaves."""
    rnd = random.Random(p.get('seed', 5))
    H = p.get('height', 0.35); br = p.get('berry', 0.007)
    stalk, berries, calyx, leaves = bmesh.new(), bmesh.new(), bmesh.new(), bmesh.new()
    lx, ly = p.get('lean', [0.05, 0.0])
    kit._tube(stalk, [(0, 0, 0), (lx * 0.3, ly * 0.3, H * 0.5), (lx, ly, H)], [0.003, 0.0025, 0.0015], 1.0, 0.0, 8, 8)
    for i in range(p.get('berries', 5)):
        t = rnd.uniform(0.4, 0.95)
        base = Vector((lx * t * t, ly * t * t, H * t))
        a = rnd.uniform(0, 6.28); d = Vector((math.cos(a), math.sin(a), -0.6)).normalized()
        L = rnd.uniform(0.015, 0.03); c = base + d * L
        _join(stalk, lambda t_, base=base, c=c: kit._tube(t_, [tuple(base), tuple((base + c) / 2 + Vector((0, 0, 0.004))), tuple(c + Vector((0, 0, br)))], [0.0012, 0.001, 0.0008], 1.0, 0.0, 6, 6))
        r = br * rnd.uniform(0.85, 1.15)
        kit._sphere(berries, tuple(c), (r, r, r * 0.95), 24)
        for k in range(5):
            ph = 2 * math.pi * k / 5 + a
            dd = Vector((math.cos(ph), math.sin(ph), 0.5)).normalized()
            m = Matrix.Translation(c + Vector((0, 0, r * 0.7)) + dd * r * 0.3) @ dd.to_track_quat('Z', 'Y').to_matrix().to_4x4()
            _join(calyx, lambda t_, r=r: kit._sphere(t_, (0, 0, 0), (r * 0.25, r * 0.06, r * 0.6), 10), m)
    for i in range(p.get('leaves', 4)):
        a = rnd.uniform(0, 6.28); Ll = H * rnd.uniform(0.25, 0.35)
        t = rnd.uniform(0.2, 0.7); base = Vector((lx * t * t, ly * t * t, H * t))
        dv = Vector((math.cos(a), math.sin(a), 0.3)).normalized()
        m = Matrix.Translation(base + dv * Ll * 0.5) @ dv.to_track_quat('Z', 'X').to_matrix().to_4x4()
        _join(leaves, lambda t_, Ll=Ll: kit._sphere(t_, (0, 0, 0), (Ll * 0.28, Ll * 0.02, Ll * 0.5), 18), m)
    m_b, nt, b = _node_mat(bpy, f'{name}-berry')
    b.inputs['Base Color'].default_value = (*_hex('#120A14'), 1); b.inputs['Roughness'].default_value = 0.08
    b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Coat Roughness'].default_value = 0.03
    m_g, nt, b = _node_mat(bpy, f'{name}-green')
    b.inputs['Base Color'].default_value = (*_hex('#3E5A28'), 1); b.inputs['Roughness'].default_value = 0.6
    b.inputs['Subsurface Weight'].default_value = 0.15
    return [_obj(bpy, f'{name}-stalk', stalk, m_g, p), _obj(bpy, f'{name}-berries', berries, m_b, p),
            _obj(bpy, f'{name}-calyx', calyx, m_g, p), _obj(bpy, f'{name}-leaves', leaves, m_g, p)]


def moss_pad(bpy, name, p, kit):
    """A cushion of moss `radius` across, domed, its edge broken: a mound in ambientCG Moss004, displaced."""
    import assets
    rnd = random.Random(p.get('seed', 1)); R = p.get('radius', 0.15)
    bm = bmesh.new()
    g = bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=24, radius=1.0)
    for v in g['verts']:
        th = math.atan2(v.co.y, v.co.x)
        k = 1 + 0.18 * noise.noise(Vector((math.cos(th) * 2.5, math.sin(th) * 2.5, p.get('seed', 1))))
        v.co = Vector((v.co.x * R * k, v.co.y * R * k, max(v.co.z, -0.2) * R * 0.35))
    m = assets.pbr(bpy, 'acg:Moss004', '2k', scale=0.25, displace=0.008, name=f'{name}-moss')
    return [_obj(bpy, name, bm, m, p)]


# --- redwood sorrel ----------------------------------------------------------------------------------------------
def _heart(n=40):
    """A heart's outline (the classic curve), its point at the origin, its notch along +y, about 1 long."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x / 34.0, (y + 17) / 34.0))
    return pts


def _sorrel_plant(bm, rnd, size):
    """One redwood sorrel plant: `leaves` trifoliate leaves on petioles from one point, each leaflet a folded heart."""
    heart = _heart()
    for k in range(rnd.randint(3, 6)):
        a = rnd.uniform(0, 2 * math.pi); h = size * rnd.uniform(0.55, 1.1)
        lean = rnd.uniform(0.2, 0.5)
        top = Vector((math.cos(a) * h * lean, math.sin(a) * h * lean, h))
        _join(bm, lambda t, top=top: _tube_simple(t, [Vector((0, 0, 0)), top * 0.5 + Vector((0, 0, h * 0.05)), top], size * 0.012))
        L = size * rnd.uniform(0.36, 0.5); droop = rnd.uniform(0.05, 0.3)
        for j in range(3):
            phi = a + 2 * math.pi * j / 3 + rnd.uniform(-0.15, 0.15)
            d = Vector((math.cos(phi), math.sin(phi), -droop)).normalized()
            side = Vector((-math.sin(phi), math.cos(phi), 0))
            nrm = side.cross(d).normalized()
            if nrm.z < 0:
                nrm = -nrm
            fold = rnd.uniform(0.15, 0.35)
            def leaflet(t, d=d, side=side, nrm=nrm, fold=fold):
                c = t.verts.new(top + d * L * 0.45 + nrm * L * 0.02)
                ring = []
                for x, y in heart:
                    p = top + d * (y * L) + side * (x * L) + nrm * (abs(x) * L * fold)
                    ring.append(t.verts.new(p))
                for i in range(len(ring)):
                    t.faces.new((c, ring[i], ring[(i + 1) % len(ring)]))
            _join(bm, leaflet)


def _tube_simple(bm, pts, r, sides=5):
    rings = []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        a = d.cross(Vector((1, 0, 0)) if abs(d.x) < 0.9 else Vector((0, 1, 0))).normalized(); b = d.cross(a)
        rings.append([bm.verts.new(p + (a * math.cos(2 * math.pi * k / sides) + b * math.sin(2 * math.pi * k / sides)) * r) for k in range(sides)])
    for ra, rb in zip(rings, rings[1:]):
        for k in range(sides):
            bm.faces.new((ra[k], ra[(k + 1) % sides], rb[(k + 1) % sides], rb[k]))


def sorrel(bpy, name, p, kit):
    """A carpet of redwood sorrel (Oxalis oregana) strewn over the objects whose names hold any of `on`: `variants`
    plants `size` tall (m) made once into a collection, instanced `density` per square metre in patches (`patch`
    metres, `patch_cut`), within and avoiding circles as poison_el's strew. Leaves a soft green, paler at the midrib,
    light through them."""
    import importlib, sys, os
    rnd = random.Random(p.get('seed', 1))
    col = bpy.data.collections.new(f'{name}-plants')
    m, nt, b = _node_mat(bpy, f'{name}-leaf')
    nz = _noise(nt, 1.0 / 0.03, 3.0)
    nt.links.new(_ramp(nt, nz.outputs['Fac'], [(0.3, '#3F6A22'), (0.6, '#52822C'), (0.8, '#6A9238')]), b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.55; b.inputs['Subsurface Weight'].default_value = 0.25
    b.inputs['Subsurface Radius'].default_value = (0.002, 0.004, 0.001)
    if 'Transmission Weight' in b.inputs:
        b.inputs['Transmission Weight'].default_value = 0.15
    vn = _noise(nt, 1.0 / 0.004, 5.0); _bump(nt, b, vn.outputs['Fac'], 0.2, 0.0003)
    for v in range(p.get('variants', 6)):
        bm = bmesh.new(); _sorrel_plant(bm, rnd, p.get('size', 0.1) * rnd.uniform(0.8, 1.2))
        me = bpy.data.meshes.new(f'{name}-v{v}'); bm.to_mesh(me); bm.free()
        for f in me.polygons:
            f.use_smooth = True
        me.materials.append(m)
        ob = bpy.data.objects.new(f'{name}-v{v}', me); col.objects.link(ob)
    d = os.path.dirname(os.path.abspath(__file__))
    if d not in sys.path:
        sys.path.insert(0, d)
    pe = importlib.import_module('poison_el')
    for o in list(bpy.context.scene.objects):
        if o.type == 'MESH' and any(k in o.name for k in p['on']):
            md = o.modifiers.new(name, 'NODES'); md.node_group = pe._strew_group(bpy, name, p, col, o.location)
    return []
