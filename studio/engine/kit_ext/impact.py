"""An impact trench in a road (round 31b, Smoke E8: spinoffs/barkhorn/elements/smoke_impact.py; the owner, 2026-10-20:
"it looked like the speaker slid along the asphalt and ground it up, like an asteroid might").

trench: the gouge itself, a channel along +y from `y0` (the impact point, where it starts shallow) to `y1` (where the
speaker came to rest), `width` metres across its floor, its depth rising to `depth` within `ramp` metres of the impact
and holding, its walls ragged (`ragged` metres of noise), its floor a torn aggregate (`texture`), scorched darker toward
the speaker (`tint`, `tint_mix`). It is the surface the road's two slabs leave open between them.

slabs: the asphalt torn up along both lips: `count` fractured plates, each an irregular slab `thickness` thick, its top
the road's asphalt (`top`), its broken edges and underside the grey sub-base (`under`), heaved up and tilted outward off
the lip by up to `tilt` degrees, larger near the impact's deepest part. `seed`.

debris: chunks of asphalt and aggregate thrown forward and to the sides of the path: `count` of them, finer and sparser
with distance (`reach` metres), lying on the road at random tilt. `seed`.

The tints shift only hue and saturation, so a dark tint on the light aggregate stays light (E12r's proof: "pale cream
slabs, like concrete blocks dumped in a line"); `value` (trench), `top_value` and `under_value` (slabs, debris) scale
the brightness, 1 as before, and `under_tint` names the under face's tint (its brown read as red chips).

E12r's p3 critics: "procedural Voronoi fracture: flat slabs of nearly the same thickness and size, with clean flat faces
and crisp edges, laid in a tidy row", "broken edges would show black binder and grey aggregate over a lighter
crushed-stone layer". Off by default, so E8 renders as it did: `crumble` (slabs, debris) rounds every sharp edge over
`crumble` cm, so the edges catch the light as broken ones do, and lumps the faces by a fine noise; `side` (a texture)
gives the broken edges their own material, the asphalt's binder and stones (`side_value`), the underside staying the
sub-base; for slabs, `spread` how far out from the lip a plate lies (in its widths; 0.25 as before), `flip` the share
turned over onto their backs, `fallen` the share dropped into the trench, and `size_power` biases the sizes toward the
small (1 as before)."""
import math, random

import bmesh
from mathutils import Euler, Matrix, Vector, noise


def _mat(bpy, kit, texture, tex_scale, tint=None, tint_mix=0.0, rough=1.0, bump=1.5, value=1.0):
    return kit.piece_material(bpy, {'material': 'pbr', 'texture': texture, 'tex_scale': tex_scale, 'tint': tint,
                                    'tint_mix': tint_mix, 'rough_mul': rough, 'bump': bump, 'value': value})


def trench(bpy, name, p, kit):
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    W, D = p.get('width', 1.0) / 2, p.get('depth', 0.35)
    ramp, rag = p.get('ramp', 4.0), p.get('ragged', 0.08)
    lip = p.get('lip', 0.75)                                   # half the opening at road level
    sd = p.get('seed', 1) * 7.3
    ny = int((y1 - y0) / 0.06); nx = 28
    bm = bmesh.new()
    rows = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        dep = D * min(1.0, (y - y0) / ramp) ** 0.7
        end = p.get('end', 0.0)
        if end and y > y1 - end:
            dep *= max(0.0, (y1 - y) / end) ** 0.8          # the gouge's end, where the speaker ploughed to rest
        row = []
        for i in range(nx + 1):
            u = -1.0 + 2.0 * i / nx                            # across: -1 at one lip, +1 at the other
            # a U: flat floor across the width, walls rising to the lips, ragged where the slabs tore away
            w = abs(u)
            z = -dep * (1.0 if w < W / lip else max(0.0, 1.0 - ((w - W / lip) / (1.0 - W / lip)) ** 1.5))
            x = u * lip
            n = noise.noise(Vector((x * 6.0 + sd, y * 3.0, 0.0)))
            x += rag * n * (0.3 + w)
            z += 0.04 * noise.noise(Vector((x * 9.0, y * 9.0 + sd, 1.0))) * (dep / max(D, 1e-3))
            # drag marks: grooves along the slide, sharp across it, long along it
            z -= p.get('grooves', 0.0) * abs(noise.noise(Vector((x * 14.0 + sd, y * 0.35, 2.0)))) * (dep / max(D, 1e-3))
            row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    mat = _mat(bpy, kit, p.get('texture', 'gravel_concrete'), p.get('tex_scale', 1.2), p.get('tint', '#2E2A26'),
               p.get('tint_mix', 0.35), 1.0, 2.0, p.get('value', 1.0))
    q = {k: v for k, v in p.items() if k in ('position', 'rotate')}
    return kit.finish(bpy, name, bm, q, smooth=True, mat=mat)


def _plate(bm, rnd, w, d, t):
    """An irregular plate: a polygon of 6 to 9 corners, `t` thick, its edges jagged."""
    k = rnd.randint(6, 9)
    pts = []
    for i in range(k):
        a = 2 * math.pi * (i + rnd.uniform(-0.3, 0.3)) / k
        r = rnd.uniform(0.65, 1.0)
        pts.append((w / 2 * r * math.cos(a), d / 2 * r * math.sin(a)))
    top = [bm.verts.new((x, y, t / 2 + rnd.uniform(-0.006, 0.006))) for x, y in pts]
    bot = [bm.verts.new((x * rnd.uniform(0.9, 1.05), y * rnd.uniform(0.9, 1.05), -t / 2)) for x, y in pts]
    ft = bm.faces.new(top); fb = bm.faces.new(bot[::-1])
    sides = []
    for i in range(k):
        sides.append(bm.faces.new((top[i], bot[i], bot[(i + 1) % k], top[(i + 1) % k])))
    # crumbled, not cut: the broken edges subdivided and pushed in and out, the aggregate showing through
    res = bmesh.ops.subdivide_edges(bm, edges=list({e for f in sides for e in f.edges}), cuts=2, use_grid_fill=False)
    sc = max(w, d)
    for v in [g for g in res['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co.x += sc * 0.08 * rnd.uniform(-1, 1); v.co.y += sc * 0.08 * rnd.uniform(-1, 1)
        v.co.z += t * 0.25 * rnd.uniform(-1, 1)
    return ft, fb, sides


def _place(bm, verts, rot, loc):
    m = Euler([math.radians(a) for a in rot]).to_matrix()
    for v in verts:
        v.co = m @ v.co + Vector(loc)


def _faces(ft, fb, sides, top, p):
    """A piece's faces to their materials: its top the road's asphalt (when it has one), its underside the sub-base, its
    broken edges the sub-base too or, with `side`, their own."""
    ft.material_index = 0 if top else 1
    fb.material_index = 1
    for f in sides:
        f.material_index = 2 if p.get('side') else 1


def _materials(bpy, kit, me, p):
    me.materials.append(_mat(bpy, kit, p.get('top', 'asphalt_02'), 4.0, '#09090A', 0.85, 0.45,
                             value=p.get('top_value', 1.0)))
    me.materials.append(_mat(bpy, kit, p.get('under', 'gravel_concrete'), 0.35, p.get('under_tint', '#211F1D'), 0.75,
                             value=p.get('under_value', 1.0)))
    if p.get('side'):
        me.materials.append(_mat(bpy, kit, p['side'], p.get('side_scale', 1.5), '#0B0B0C', 0.85, 0.8,
                                 value=p.get('side_value', 1.0)))


def _crumble(bm, cm, seed):
    """Every sharp edge rounded over `cm` centimetres, so the broken edges catch the light along their length, and each
    face tented a little from a point near its middle, so none is a flat plane."""
    sharp = [e for e in bm.edges if e.is_manifold and e.calc_face_angle(0.0) > math.radians(35.0)]
    bmesh.ops.bevel(bm, geom=sharp, offset=cm * 0.01, offset_type='OFFSET', segments=2, profile=0.5, affect='EDGES',
                    clamp_overlap=True)
    big = [f for f in bm.faces if len(f.verts) > 5 and f.calc_area() > (cm * 0.03) ** 2]
    bm.normal_update()
    res = bmesh.ops.poke(bm, faces=big)
    o = Vector((seed * 1.7, seed * 2.3, seed * 0.9))
    for v in res['verts']:
        n = v.normal.copy()
        v.co += n * (cm * 0.006 * noise.noise(v.co * 7.0 + o))
    bm.normal_update()


def slabs(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    lip, t = p.get('lip', 0.75), p.get('thickness', 0.08)
    D, ramp = p.get('depth', 0.35), p.get('ramp', 4.0)
    spread, flip, fallen, sp = p.get('spread', 0.25), p.get('flip', 0.0), p.get('fallen', 0.0), p.get('size_power', 1.0)
    bm = bmesh.new()
    for k in range(p.get('count', 40)):
        y = rnd.uniform(y0 + 0.5, y1 - 0.2)
        s = 1 if rnd.random() < 0.5 else -1
        f = min(1.0, (y - y0) / ramp)                          # bigger, steeper plates where the trench is deep
        sz = p.get('size', 1.0)
        w, d = sz * (0.25 + 0.45 * rnd.random() ** sp) * (0.5 + f), sz * (0.3 + 0.5 * rnd.random() ** sp) * (0.5 + f)
        before = len(bm.verts)
        ft, fb, sides = _plate(bm, rnd, w, d, t)
        _faces(ft, fb, sides, True, p)
        bm.verts.ensure_lookup_table()
        new = [bm.verts[i] for i in range(before, len(bm.verts))]   # new verts come last (wrappers are not stable)
        tilt = rnd.uniform(p.get('tilt_min', 15.0), p.get('tilt', 55.0)) * f
        x = s * (lip + w * spread * rnd.uniform(0.2, 1.0))
        z = 0.02 + 0.5 * w * math.sin(math.radians(tilt)) * 0.4 - (0.0 if rnd.random() < 0.7 else 0.1)
        if fallen and rnd.random() < fallen and abs(y) > 0.8:   # dropped into the trench (clear of the speaker at 0)
            x = s * rnd.uniform(0.0, lip * 0.75)
            z = -D * f + t * 0.5 + 0.02 + 0.3 * w * math.sin(math.radians(tilt))
        if flip and rnd.random() < flip:                       # thrown over onto its back
            tilt = 180.0 - tilt * 0.5
        _place(bm, new, (rnd.uniform(-8, 8), s * tilt, rnd.uniform(-25, 25)), (x, y, z))
    if p.get('crumble'):
        _crumble(bm, p['crumble'], p.get('seed', 1))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    _materials(bpy, kit, me, p)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]


def debris(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 2))
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    reach = p.get('reach', 6.0)
    bm = bmesh.new()
    for k in range(p.get('count', 300)):
        # along the path, thrown sideways (and some forward past the speaker); size falls with distance thrown
        fwd = p.get('forward', 0.0)
        if rnd.random() < fwd:
            # thrown ahead of where it came to rest: a fan opening with distance
            ahead = p.get('ahead', 6.0) * rnd.random() ** 1.6
            y = y1 + 0.3 + ahead
            r = (0.2 + 0.5 * ahead) * rnd.random()
        else:
            y = rnd.uniform(y0 + 1.0, y1 + 0.5)
            r = reach * rnd.random() ** 2.2
        x = (1 if rnd.random() < 0.5 else -1) * ((p.get('inner', 0.8) if y < y1 else 0.0) + r)
        size = max(0.012, 0.16 * max(0.0, 1.0 - r / max(reach, r + 0.01)) ** 1.6 * rnd.uniform(0.3, 1.0))
        if p.get('fine'):
            size = rnd.uniform(0.005, 0.03) * (1.0 - 0.5 * min(1.0, r / reach))
        before = len(bm.verts)
        ft, fb, sides = _plate(bm, rnd, size * rnd.uniform(0.8, 1.6), size * rnd.uniform(0.8, 1.6),
                               size * rnd.uniform(0.3, 0.6))
        bm.verts.ensure_lookup_table()
        new = [bm.verts[i] for i in range(before, len(bm.verts))]   # new verts come last (wrappers are not stable)
        _place(bm, new, (rnd.uniform(-40, 40), rnd.uniform(-40, 40), rnd.uniform(0, 360)), (x, y, p.get('z', 0.0) + size * 0.2))
        _faces(ft, fb, sides, rnd.random() < 0.6, p)
    if p.get('crumble'):
        _crumble(bm, p['crumble'], p.get('seed', 2))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    _materials(bpy, kit, me, p)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]


def scorch(bpy, name, p, kit):
    """Scorch on the road: a plane a hair above it, soot-black where noise and a falloff from the path's centre line say
    so and clear elsewhere, so the blackening frays out into the asphalt instead of ending at an edge. `size` [w, l],
    `strength` the blackness at its heart, `scale` metres a patch."""
    w, l = p.get('size', [3.0, 20.0])
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0.0)) for x, y in ((-w / 2, -l / 2), (w / 2, -l / 2), (w / 2, l / 2), (-w / 2, l / 2))]
    bm.faces.new(vs)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0.003]))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = kit.M.hex_lin(p.get('color', '#0C0A09'))
    bsdf.inputs['Roughness'].default_value = 0.9
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    # falloff across the path (x), strongest on its centre line, and toward both ends (y)
    def band(sock, lo, hi):
        a = nt.nodes.new('ShaderNodeMath'); a.operation = 'SUBTRACT'; a.inputs[1].default_value = 0.5
        nt.links.new(sock, a.inputs[0])
        b = nt.nodes.new('ShaderNodeMath'); b.operation = 'ABSOLUTE'; nt.links.new(a.outputs[0], b.inputs[0])
        c = nt.nodes.new('ShaderNodeMapRange'); c.inputs['From Min'].default_value = hi; c.inputs['From Max'].default_value = lo
        nt.links.new(b.outputs[0], c.inputs['Value'])
        return c.outputs['Result']
    fx, fy = band(sep.outputs['X'], 0.05, 0.5), band(sep.outputs['Y'], 0.3, 0.5)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('scale', 0.6)
    nz.inputs['Detail'].default_value = 8.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    m1 = nt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'; nt.links.new(fx, m1.inputs[0]); nt.links.new(fy, m1.inputs[1])
    m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
    nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(nz.outputs['Fac'], m2.inputs[1])
    ramp = nt.nodes.new('ShaderNodeMapRange'); ramp.inputs['From Min'].default_value = 0.15
    ramp.inputs['From Max'].default_value = 0.45; ramp.inputs['To Max'].default_value = p.get('strength', 0.85)
    nt.links.new(m2.outputs[0], ramp.inputs['Value'])
    nt.links.new(ramp.outputs['Result'], mix.inputs['Fac'])
    nt.links.new(tr.outputs['BSDF'], mix.inputs[1]); nt.links.new(bsdf.outputs['BSDF'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    me.materials.append(m)
    ob.visible_shadow = False
    return [ob]
