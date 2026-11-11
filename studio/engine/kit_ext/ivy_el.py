"""Poison ivy (Toxicodendron radicans) on an old garden wall, for Poison's habitat (the owner, 2026-11-11: "Why not put
poison in ivy, like poison ivy?").

- wall: an old garden wall, `size` [w, h, t] metres, faced in a Poly Haven brick or stone scan laid at its real size,
  with a coping course on top;
- ivy: the vine climbing the wall's face from its foot: woody stems that wander up and branch, held to the brick by
  short hairy rootlets, and along them leaves in threes on long petioles (the terminal leaflet on its own stalk, the
  two laterals nearly sessile, often with a tooth or two on their outer edge: the "mitten"), glossy mid-green;
- cover: the same plant as ground cover, leaf triplets on short upright petioles rising from runners on the ground.

Nothing here is a scan: Poly Haven has no poison ivy. The leaves are modelled from the plant's botany (leaflets 5-12 cm,
ovate, pointed, entire or coarsely toothed, the laterals asymmetric) and given a procedural glossy-leaf material
(a waxy coat, midrib and veins, light passing through).
"""
import math, random

import bmesh
from mathutils import Matrix, Vector

import assets


# --- the wall ------------------------------------------------------------------------------------------------------
def wall(bpy, name, p, kit):
    """An old garden wall `size` [w, h, t], its face toward -y at `position` (x centre, y of the face, z of its foot),
    faced in `texture` (Poly Haven, real size) with a coping `coping` [overhang, height] on top in `coping_texture`."""
    w, h, t = p.get('size', [8.0, 2.2, 0.35])
    x0, y0, z0 = p.get('position', [0.0, 1.0, 0.0])
    out = []

    def box(nm, cx, cy, cz, sx, sy, sz, mat, cells=None):
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co.x *= sx; v.co.y *= sy; v.co.z *= sz
        if cells:                                                       # dense enough for the scan's displacement
            bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=cells, use_grid_fill=True)
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        me.materials.append(mat)
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (cx, cy, cz); out.append(ob)
        return ob
    face = assets.pbr(bpy, p.get('texture', 'castle_brick_02_red'), p.get('res', '2k'), displace=p.get('displace', 0.008),
                      tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0), name=f'{name}-face')
    box(f'{name}-body', x0, y0 + t / 2, z0 + h / 2 - 0.05, w, t, h + 0.1, face, cells=p.get('cells', 60))
    ov, ch = p.get('coping', [0.04, 0.09])
    cap = assets.pbr(bpy, p.get('coping_texture', 'castle_wall_slates'), p.get('res', '2k'), name=f'{name}-coping')
    box(f'{name}-coping', x0, y0 + t / 2, z0 + h + ch / 2, w + 2 * ov, t + 2 * ov, ch, cap)
    return out


# --- the leaf ------------------------------------------------------------------------------------------------------
def _leaflet(bm, uvl, col, M, L, W, tooth=0.0, side=1, fold=0.22, curl=0.08, nu=3, nt=7):
    """One leaflet in bmesh `bm` under matrix M (its base at the origin, its tip along +y, its face +z): ovate, the tip
    drawn out to a point, folded along the midrib by `fold`, curling back by `curl`; a lateral's outer edge (`side`)
    carries a coarse tooth `tooth` (a fraction of the half-width) a little below the middle. UVs: u across (-1..1), v
    along (0..1), for the veins."""
    rows = []
    for j in range(nt + 1):
        tt = j / nt
        hw = W * (math.sin(math.pi * min(1.0, tt ** 0.75)) ** 0.85) * (1.0 - 0.25 * tt)
        row = []
        for i in range(-nu, nu + 1):
            u = i / nu
            ww = hw
            if tooth and u * side > 0.5:
                ww *= 1.0 + tooth * math.exp(-((tt - 0.42) / 0.07) ** 2) - 0.5 * tooth * math.exp(-((tt - 0.52) / 0.05) ** 2)
            x = u * ww
            z = abs(u) * ww * fold - curl * L * (tt - 0.35) ** 2 + 0.03 * L * math.sin(7 * tt + 3 * u)
            v = bm.verts.new(M @ Vector((x, tt * L, z)))
            row.append((v, (u, tt)))
        rows.append(row)
    for j in range(nt):
        for i in range(2 * nu):
            q = [rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]]
            try:
                f = bm.faces.new([a[0] for a in q])
            except ValueError:
                continue
            f.smooth = True
            for lp, a in zip(f.loops, q):
                lp[uvl].uv = a[1]; lp[col] = (*col_val[0], 1.0)


col_val = [(0.5, 0.5, 0.5)]


def _frame(origin, fwd, up):
    """A matrix whose +y is `fwd` and +z as near `up` as fwd allows, at `origin`."""
    y = fwd.normalized(); x = y.cross(up).normalized(); z = x.cross(y).normalized()
    return Matrix(((x.x, y.x, z.x, origin.x), (x.y, y.y, z.y, origin.y), (x.z, y.z, z.z, origin.z), (0, 0, 0, 1)))


def _triplet(bm, uvl, col, rnd, base, petiole_dir, face_dir, size):
    """A poison ivy leaf: a petiole from `base` along `petiole_dir`, and at its end three leaflets facing `face_dir`
    (the terminal on a stalk a fifth of its length, the two laterals at about 60 degrees, smaller, toothed outside).
    Returns the petiole's end."""
    pl = size * rnd.uniform(0.9, 1.6)
    tip = base + petiole_dir.normalized() * pl
    fwd = petiole_dir.normalized()
    up = face_dir.normalized()
    lw = size * rnd.uniform(0.5, 0.62)
    col_val[0] = (rnd.random(), rnd.random(), rnd.random())             # per leaf: hue, value, gloss jitter
    T = _frame(tip + fwd * size * 0.2, fwd, up)
    _leaflet(bm, uvl, col, T, size, lw * 0.5, tooth=rnd.choice([0.0, 0.0, 0.15]), side=1)
    for s in (-1, 1):
        a = math.radians(rnd.uniform(55, 75)) * s
        d = Matrix.Rotation(a, 3, up) @ fwd
        _leaflet(bm, uvl, col, _frame(tip, d, up), size * rnd.uniform(0.7, 0.85), lw * 0.5,
                 tooth=rnd.choice([0.0, 0.25, 0.35]), side=-s, fold=0.18, curl=0.06)
    return tip


def _leaf_mat(bpy, name, p):
    """A glossy leaf: base colour varied per leaf between `greens`, a waxy coat, lighter midrib and veins (from the UVs)
    in the colour and the bump, and some light passing through (a translucent lobe mixed in)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = 'leafcol'
    sep = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(at.outputs['Color'], sep.inputs['Color'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    gs = p.get('greens', ['#2E5216', '#3F6B1F', '#557F27', '#6B8A2E'])
    while len(cr.elements) < len(gs):
        cr.elements.new(0.5)
    for k, g in enumerate(gs):
        cr.elements[k].position = k / (len(gs) - 1); cr.elements[k].color = (*_lin(g), 1)
    nt.links.new(sep.outputs['Red'], ramp.inputs['Fac'])
    uv = nt.nodes.new('ShaderNodeUVMap'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(uv.outputs['UV'], sp.inputs['Vector'])
    # the midrib: |u| small; the veins: lines running out and forward from it
    au = nt.nodes.new('ShaderNodeMath'); au.operation = 'ABSOLUTE'; nt.links.new(sp.outputs['X'], au.inputs[0])
    rib = nt.nodes.new('ShaderNodeMapRange'); rib.inputs['From Min'].default_value = 0.05; rib.inputs['From Max'].default_value = 0.0
    nt.links.new(au.outputs[0], rib.inputs['Value'])
    vv = nt.nodes.new('ShaderNodeMath'); vv.operation = 'MULTIPLY_ADD'
    nt.links.new(au.outputs[0], vv.inputs[0]); vv.inputs[1].default_value = -0.35; nt.links.new(sp.outputs['Y'], vv.inputs[2])
    sn = nt.nodes.new('ShaderNodeMath'); sn.operation = 'MULTIPLY'; nt.links.new(vv.outputs[0], sn.inputs[0]); sn.inputs[1].default_value = 9 * 2 * math.pi
    sw = nt.nodes.new('ShaderNodeMath'); sw.operation = 'SINE'; nt.links.new(sn.outputs[0], sw.inputs[0])
    vein = nt.nodes.new('ShaderNodeMapRange'); vein.inputs['From Min'].default_value = 0.93; vein.inputs['From Max'].default_value = 1.0
    nt.links.new(sw.outputs[0], vein.inputs['Value'])
    vm = nt.nodes.new('ShaderNodeMath'); vm.operation = 'MAXIMUM'; nt.links.new(rib.outputs['Result'], vm.inputs[0])
    vs = nt.nodes.new('ShaderNodeMath'); vs.operation = 'MULTIPLY'; nt.links.new(vein.outputs['Result'], vs.inputs[0]); vs.inputs[1].default_value = 0.6
    nt.links.new(vs.outputs[0], vm.inputs[1])
    mixc = nt.nodes.new('ShaderNodeMix'); mixc.data_type = 'RGBA'; mixc.blend_type = 'MIX'
    nt.links.new(vm.outputs[0], mixc.inputs['Factor']); nt.links.new(ramp.outputs['Color'], mixc.inputs[6])
    mixc.inputs[7].default_value = (*_lin(p.get('vein', '#8FA552')), 1)
    vfac = nt.nodes.new('ShaderNodeMath'); vfac.operation = 'MULTIPLY'; nt.links.new(vm.outputs[0], vfac.inputs[0]); vfac.inputs[1].default_value = 0.35
    mixv = nt.nodes.new('ShaderNodeMix'); mixv.data_type = 'RGBA'
    nt.links.new(vfac.outputs[0], mixv.inputs['Factor']); nt.links.new(ramp.outputs['Color'], mixv.inputs[6]); nt.links.new(mixc.outputs[2], mixv.inputs[7])
    nt.links.new(mixv.outputs[2], bs.inputs['Base Color'])
    rr = nt.nodes.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = p.get('rough', [0.25, 0.42])[0]
    rr.inputs['To Max'].default_value = p.get('rough', [0.25, 0.42])[1]; nt.links.new(sep.outputs['Blue'], rr.inputs['Value'])
    nt.links.new(rr.outputs['Result'], bs.inputs['Roughness'])
    bs.inputs['Coat Weight'].default_value = p.get('coat', 0.35); bs.inputs['Coat Roughness'].default_value = 0.12
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.25; bump.inputs['Distance'].default_value = 0.0005
    inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; nt.links.new(vm.outputs[0], inv.inputs[1])
    nt.links.new(inv.outputs[0], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
    tl = nt.nodes.new('ShaderNodeBsdfTranslucent'); nt.links.new(mixv.outputs[2], tl.inputs['Color'])
    mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = p.get('translucent', 0.22)
    nt.links.new(bs.outputs[0], mx.inputs[1]); nt.links.new(tl.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    return m


def _lin(h):
    h = h.lstrip('#'); c = [int(h[k:k + 2], 16) / 255 for k in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def _stem_mat(bpy, name, color, rough=0.75):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*_lin(color), 1)
    b.inputs['Roughness'].default_value = rough
    return m


def _tube(bm, pts, radii, sides=6):
    """A tube through `pts` (Vectors) with `radii`, into bm."""
    rings = []
    for k, (pt, r) in enumerate(zip(pts, radii)):
        d = (pts[min(k + 1, len(pts) - 1)] - pts[max(k - 1, 0)]).normalized()
        a = d.orthogonal().normalized(); b = d.cross(a)
        rings.append([bm.verts.new(pt + (a * math.cos(2 * math.pi * s / sides) + b * math.sin(2 * math.pi * s / sides)) * r)
                      for s in range(sides)])
    for k in range(len(rings) - 1):
        for s in range(sides):
            f = bm.faces.new([rings[k][s], rings[k][(s + 1) % sides], rings[k + 1][(s + 1) % sides], rings[k + 1][s]])
            f.smooth = True


def _objects(bpy, name, leaf_bm, stem_bm, hair_bm, p):
    out = []
    for nm, bm, mat in ((f'{name}-leaves', leaf_bm, _leaf_mat(bpy, f'{name}-leaf', p)),
                        (f'{name}-stems', stem_bm, _stem_mat(bpy, f'{name}-stem', p.get('stem', '#4A3222'))),
                        (f'{name}-rootlets', hair_bm, _stem_mat(bpy, f'{name}-rootlet', p.get('rootlet', '#6B4A30'), 0.9))):
        if bm is None or not bm.verts:
            continue
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free(); me.materials.append(mat)
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob); out.append(ob)
    return out


def _new_leaf_bm():
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap'); col = bm.loops.layers.float_color.new('leafcol')
    return bm, uvl, col


# --- the vine on the wall ------------------------------------------------------------------------------------------
def ivy(bpy, name, p, kit):
    """Vines climbing the wall's face (the plane y = `face_y`, facing -y) from roots along its foot at the x positions
    `roots` [[x, spread, height], ...]: each wanders up to about `height`, branching, its stems `stem_r` thick at the
    root thinning upward, held off the brick by rootlets; leaves every `node` metres, `leaf` metres a leaflet, facing out
    and a little up, kept clear of `clear` boxes [x0, z0, x1, z1] on the face (where the speaker stands before it)."""
    rnd = random.Random(p.get('seed', 1))
    fy = p.get('face_y', 1.0); node = p.get('node', 0.11); size = p.get('leaf', 0.08)
    clear = p.get('clear', [])
    top = p.get('top', 2.2)
    lbm, uvl, col = _new_leaf_bm(); sbm = bmesh.new(); hbm = bmesh.new()
    n_leaves = 0

    def clear_at(x, z):
        return any(a <= x <= c and b <= z <= d for a, b, c, d in clear)

    def grow(x, z, heading, r, length, depth, down=False):
        nonlocal n_leaves
        pts, radii = [Vector((x, fy - r - 0.004, z))], [r]
        s = 0.0; step = 0.035; next_node = node * rnd.uniform(0.3, 1.0); side = 1
        while s < length and (z > 0.05 if down else z < top - 0.02):
            heading += rnd.gauss(0, 0.14)
            if down:                                                        # hanging: mostly downward
                heading = math.pi + max(-0.9, min(0.9, (heading - math.pi) * 0.92))
            else:
                heading = max(-1.25, min(1.25, heading * 0.92))            # mostly upward, wandering
            x += math.sin(heading) * step; z += math.cos(heading) * step; s += step
            rr = max(0.0015, r * (1 - 0.7 * s / length))
            pts.append(Vector((x, fy - rr - 0.004 + 0.003 * math.sin(s * 9), z))); radii.append(rr)
            if rnd.random() < 0.25:                                         # rootlets: short brown hairs to the brick
                for _ in range(2):
                    a = Vector((x + rnd.uniform(-rr, rr), fy - rr * 0.5, z + rnd.uniform(-0.01, 0.01)))
                    b = a + Vector((rnd.uniform(-0.012, 0.012), rr * 0.5 + 0.004, rnd.uniform(-0.015, 0.0)))
                    _tube(hbm, [a, b], [0.0006, 0.0003], sides=3)
            if s >= next_node:
                next_node += node * rnd.uniform(0.7, 1.3); side = -side
                if not clear_at(x, z):
                    base = pts[-1] + Vector((0, -rr, 0))
                    out_d = Vector((side * rnd.uniform(0.3, 0.8), -rnd.uniform(0.6, 1.0), rnd.uniform(0.1, 0.5)))
                    face = Vector((rnd.uniform(-0.3, 0.3), -1.0, rnd.uniform(0.3, 0.9)))
                    tip = _triplet(lbm, uvl, col, rnd, base, out_d, face, size * rnd.uniform(0.75, 1.25))
                    _tube(sbm, [base, base.lerp(tip, 0.5) + Vector((0, 0, 0.01)), tip], [0.0016, 0.0013, 0.001], sides=4)
                    n_leaves += 1
            if depth < 3 and rnd.random() < p.get('branch', 0.035):
                grow(x, z, heading + rnd.choice([-1, 1]) * rnd.uniform(0.6, 1.1), rr * 0.8, length * rnd.uniform(0.35, 0.7), depth + 1, down)
        if len(pts) > 1:
            _tube(sbm, pts, radii)
    for hx, spread, h in p.get('hang', []):                            # spilling over the coping, hanging down the face
        for k in range(p.get('per_hang', 3)):
            grow(hx + rnd.uniform(-spread, spread), top - 0.03, math.pi + rnd.gauss(0, 0.25), p.get('stem_r', 0.008) * 0.6,
                 h * rnd.uniform(0.6, 1.1), 1, down=True)
    for rx, spread, h in p.get('roots', [[0.0, 0.5, 2.0]]):
        for k in range(p.get('per_root', 3)):
            grow(rx + rnd.uniform(-spread, spread), -0.02, rnd.gauss(0, 0.3), p.get('stem_r', 0.008) * rnd.uniform(0.6, 1.2),
                 h * rnd.uniform(0.7, 1.15), 0)
    out = _objects(bpy, name, lbm, sbm, hbm, p)
    print(f'ivy {name}: {n_leaves} leaves')
    return out


# --- the same plant as ground cover --------------------------------------------------------------------------------
def cover(bpy, name, p, kit):
    """Ground cover over `area` [x0, y0, x1, y1]: about `count` leaf triplets on upright petioles `height` [min, max]
    tall, in clumps along runners, none inside the `avoid` circles [x, y, r] or the `keep_out` boxes [x0, y0, x1, y1]
    (the line from the camera to the speaker's front), their runners on the ground (z 0)."""
    rnd = random.Random(p.get('seed', 3))
    x0, y0, x1, y1 = p.get('area', [-3, -1, 3, 1]); size = p.get('leaf', 0.07)
    avoid = p.get('avoid', []); keep = p.get('keep_out', [])
    lbm, uvl, col = _new_leaf_bm(); sbm = bmesh.new()
    n = 0; tries = 0
    while n < p.get('count', 300) and tries < p.get('count', 300) * 30:
        tries += 1
        cx, cy = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if any((cx - a) ** 2 + (cy - b) ** 2 < r * r for a, b, r in avoid) or any(a <= cx <= c and b <= cy <= d for a, b, c, d in keep):
            continue
        hd = rnd.uniform(0, 2 * math.pi)                                    # a runner, a few plants along it
        run = [Vector((cx, cy, 0.002))]
        for k in range(rnd.randint(3, 7)):
            hd += rnd.gauss(0, 0.4)
            q = run[-1] + Vector((math.cos(hd), math.sin(hd), 0)) * rnd.uniform(0.06, 0.12)
            if any((q.x - a) ** 2 + (q.y - b) ** 2 < r * r for a, b, r in avoid) or any(a <= q.x <= c and b <= q.y <= d for a, b, c, d in keep):
                break
            run.append(q)
            hgt = rnd.uniform(*p.get('height', [0.06, 0.22]))
            top = q + Vector((rnd.uniform(-0.03, 0.03), rnd.uniform(-0.03, 0.03), hgt))
            _tube(sbm, [q, q.lerp(top, 0.6) + Vector((0, 0, 0.01)), top], [0.0012, 0.001, 0.0008], sides=4)
            d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(0.05, 0.35)))
            face = Vector((rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4) - 0.3, 1.0))
            _triplet(lbm, uvl, col, rnd, top, d, face, size * rnd.uniform(0.7, 1.3)); n += 1
        if len(run) > 1:
            _tube(sbm, run, [p.get('runner_r', 0.004)] * len(run), sides=6)
    out = _objects(bpy, name, lbm, sbm, None, dict(p, stem=p.get('stem', '#5A3B26')))   # brown runners, petioles
    print(f'ivy cover {name}: {n} leaves')
    return out


# --- a spray of the vine close to the lens --------------------------------------------------------------------------
def spray(bpy, name, p, kit):
    """One length of the vine near the camera, so the leaves in threes read plainly: from `start` along `heading_deg`
    (in the ground plane, 0 = +x) for `length` metres, arching up to `rise`, `count` leaves of leaflets `leaf` metres on
    petioles turned so their faces look toward `face_to` (the camera)."""
    rnd = random.Random(p.get('seed', 9))
    st = Vector(p.get('start', [0.0, -2.0, 0.0])); hd = math.radians(p.get('heading_deg', 30.0))
    L = p.get('length', 0.7); rise = p.get('rise', 0.25); ft = Vector(p.get('face_to', [1.5, -5.6, 0.8]))
    lbm, uvl, col = _new_leaf_bm(); sbm = bmesh.new()
    pts = []
    n = 24
    for k in range(n + 1):
        t = k / n
        pts.append(st + Vector((math.cos(hd), math.sin(hd), 0)) * L * t + Vector((0, 0, rise * math.sin(math.pi * min(1.0, t * 1.3)) + 0.004)))
    _tube(sbm, pts, [p.get('stem_r', 0.005) * (1 - 0.5 * k / n) for k in range(n + 1)], sides=8)
    for k in range(p.get('count', 7)):
        t = (k + 0.5) / p.get('count', 7)
        base = pts[int(t * n)]
        to_cam = (ft - base).normalized()
        out_d = Vector((rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), rnd.uniform(0.4, 0.9))) + to_cam * 0.4
        face = to_cam + Vector((0, 0, 0.6)) + Vector((rnd.uniform(-0.2, 0.2), rnd.uniform(-0.2, 0.2), 0))
        tip = _triplet(lbm, uvl, col, rnd, base, out_d, face, p.get('leaf', 0.1) * rnd.uniform(0.85, 1.15))
        _tube(sbm, [base, base.lerp(tip, 0.5) + Vector((0, 0, 0.015)), tip], [0.0025, 0.002, 0.0014], sides=6)
    out = _objects(bpy, name, lbm, sbm, None, dict(p, stem=p.get('stem', '#5A3B26')))
    print(f'ivy spray {name}: {p.get("count", 7)} leaves')
    return out
