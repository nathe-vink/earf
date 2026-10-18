"""Ice's own kit pieces (round 31's frozen grotto, spinoffs/barkhorn/dioramas/ice.py).

- crystal: a shard of cast glass, the convex hull of points scattered in an upright ellipsoid (`size` [w, d, h]), its
  facets flat, sitting on its position (an ice boulder, a column of the grotto's wall); `seed`, `points`.
- snowflake: a folded-and-cut paper snowflake, six arms with pointed side branches, `radius` (centre to a tip), `arm`
  (an arm's half-width as a share of the radius), `branches` [[at, length], ...] along each arm as shares of the
  radius, `depth` its thickness, standing in its x-z plane.
"""
import math, random

import bmesh
from mathutils import Vector


def crystal(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    w, d, h = p.get('size', [0.4, 0.4, 1.0])
    bm = bmesh.new()
    for _ in range(p.get('points', 18)):
        a = rnd.uniform(0, 2 * math.pi); z = rnd.uniform(0.0, 1.0)
        # wider low down, a point or a broken top above
        r = math.sqrt(max(0.0, 1.0 - (2 * z - 1) ** 2 * 0.55)) * (1.0 - 0.55 * z ** 2) * rnd.uniform(0.75, 1.0)
        bm.verts.new((math.cos(a) * r * w / 2, math.sin(a) * r * d / 2, z * h))
    for a in range(6):                                    # a flat foot to stand on
        t = 2 * math.pi * (a + rnd.random() * 0.4) / 6
        bm.verts.new((math.cos(t) * w * 0.42, math.sin(t) * d * 0.42, 0.0))
    bmesh.ops.convex_hull(bm, input=bm.verts[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return kit.finish(bpy, name, bm, p, smooth=False)


def snowflake_outline(radius, arm=0.07, branches=((0.42, 0.26), (0.66, 0.17)), tip=0.06):
    """The flake's outline [[x, z], ...] counter-clockwise: each arm out along one side, round its point, back."""
    w = arm * radius
    def half(sign):
        pts = []
        for at, ln in branches:
            b0, bw, L = at * radius, w * 1.6, ln * radius
            pts += [(b0, w), (b0 + bw / 2 + L * 0.5, w + L * 0.866), (b0 + bw, w)]
        pts += [(radius * (1 - tip) - w, w)]
        return [(x, sign * y) for x, y in pts]
    arm_pts = [(w * 1.732, -w)] + half(-1) + [(radius, 0.0)] + half(1)[::-1]
    out = []
    for k in range(6):
        c, s = math.cos(k * math.pi / 3), math.sin(k * math.pi / 3)
        out += [(x * c - y * s, x * s + y * c) for x, y in arm_pts]
    return out


def snowflake(bpy, name, p, kit):
    r = p.get('radius', 0.2)
    br = p.get('branches', [[0.42, 0.26], [0.66, 0.17]])
    outline = snowflake_outline(r, p.get('arm', 0.07), br)
    bm = bmesh.new()
    kit._extrude(bm, outline, p.get('depth', 0.004), p.get('ease', 0.0008))
    return kit.finish(bpy, name, bm, p, smooth=False)


def drift(bpy, name, p, kit):
    """A drift of cotton wool: `count` balls heaped in a half-dome `size` [w, d, h] (bigger and denser at its heart,
    small tufts at its skirt), every ball a little squashed, so it reads as pulled cotton, not a pile of spheres."""
    rnd = random.Random(p.get('seed', 1))
    w, d, h = p.get('size', [1.0, 0.6, 0.3])
    r0, r1 = p.get('radius', [0.03, 0.12])
    # one unit ball, copied: bmesh's create ops slow down with the size of the mesh they add to
    tmp = bmesh.new(); bmesh.ops.create_uvsphere(tmp, u_segments=20, v_segments=10, radius=1.0)
    tmp.verts.index_update()
    unit = [v.co.copy() for v in tmp.verts]; tris = [[v.index for v in f.verts] for f in tmp.faces]; tmp.free()
    bm = bmesh.new()
    for _ in range(p.get('count', 60)):
        a = rnd.uniform(0, 2 * math.pi); q = math.sqrt(rnd.random())
        x, y = math.cos(a) * q * w / 2, math.sin(a) * q * d / 2
        heart = 1.0 - q ** 2
        r = r0 + (r1 - r0) * heart * rnd.uniform(0.6, 1.0)
        z = h * math.sqrt(max(heart, 0.0)) * rnd.uniform(0.75, 0.95) - r * 0.45
        sx, sy, sz = rnd.uniform(1.0, 1.35), rnd.uniform(0.9, 1.2), rnd.uniform(0.7, 0.9)
        vs = [bm.verts.new((x + c.x * r * sx, y + c.y * r * sy, z + c.z * r * sz)) for c in unit]
        for f in tris:
            bm.faces.new([vs[i] for i in f])
    return kit.finish(bpy, name, bm, p, smooth=True)


def pool(bpy, name, p, kit):
    """The glow under the ice: a disc `radius` across whose light falls smoothly from its heart (`color`, `emit`) through
    `edge` to nothing at its rim (`power` shapes the fall), so the frosted lake above it glows like lit ice, not a spot."""
    R = p.get('radius', 3.0)
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=96, radius=R)
    m = bpy.data.materials.new(name + '-glow'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    tc = nt.nodes.new('ShaderNodeTexCoord'); ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'
    nt.links.new(tc.outputs['Object'], ln.inputs[0])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.0; mr.inputs['From Max'].default_value = R
    nt.links.new(ln.outputs['Value'], mr.inputs['Value'])
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = p.get('power', 0.8)
    nt.links.new(mr.outputs['Result'], pw.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    hl = kit.M.hex_lin
    cr.elements[0].position = 0.0; cr.elements[0].color = (*hl(p.get('color', '#9EDBFF'))[:3], 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (0, 0, 0, 1)
    e = cr.elements.new(0.45); e.color = (*hl(p.get('edge', '#2C6FB0'))[:3], 1)
    nt.links.new(pw.outputs['Value'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], em.inputs['Color'])
    em.inputs['Strength'].default_value = p.get('emit', 4.0)
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    return kit.finish(bpy, name, bm, p, smooth=True, mat=m)


def lake(bpy, name, p, kit):
    """A frozen lake of cast glass: a slab `size` [w, d, h] whose top is clear in places and frosted in drifts of
    rime (its roughness wandering with a noise `patch` metres across between `rough` [min, max]), with a faint swell
    and fine scratches in its surface, so it reads as ice, not a polished floor."""
    w, d, h = p.get('size', [10.0, 8.0, 0.06])
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((v.co.x * w, v.co.y * d, (v.co.z - 0.5) * h))
    m = bpy.data.materials.new(name + '-ice'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    hl = kit.M.hex_lin
    b.inputs['Base Color'].default_value = hl(p.get('color', '#C4E2F4'))
    b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.31
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('patch', 0.6)
    nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    r0, r1 = p.get('rough', [0.06, 0.45])
    ramp = nt.nodes.new('ShaderNodeMapRange'); ramp.inputs['From Min'].default_value = 0.35; ramp.inputs['From Max'].default_value = 0.65
    ramp.inputs['To Min'].default_value = r0; ramp.inputs['To Max'].default_value = r1
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Value']); nt.links.new(ramp.outputs['Result'], b.inputs['Roughness'])
    # the swell, then the scratches (long thin wave bands, stretched)
    sw = nt.nodes.new('ShaderNodeTexNoise'); sw.inputs['Scale'].default_value = 1.0 / p.get('swell', 0.5)
    nt.links.new(tc.outputs['Object'], sw.inputs['Vector'])
    b1 = nt.nodes.new('ShaderNodeBump'); b1.inputs['Strength'].default_value = p.get('swell_strength', 0.08)
    b1.inputs['Distance'].default_value = 0.01; nt.links.new(sw.outputs['Fac'], b1.inputs['Height'])
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 0.04, 1.0)
    mp.inputs['Rotation'].default_value = (0.0, 0.0, 0.5)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    sc = nt.nodes.new('ShaderNodeTexNoise'); sc.inputs['Scale'].default_value = 60.0; sc.inputs['Detail'].default_value = 2.0
    nt.links.new(mp.outputs['Vector'], sc.inputs['Vector'])
    b2 = nt.nodes.new('ShaderNodeBump'); b2.inputs['Strength'].default_value = p.get('scratch', 0.12)
    b2.inputs['Distance'].default_value = 0.002
    nt.links.new(sc.outputs['Fac'], b2.inputs['Height']); nt.links.new(b1.outputs['Normal'], b2.inputs['Normal'])
    nt.links.new(b2.outputs['Normal'], b.inputs['Normal'])
    return kit.finish(bpy, name, bm, p, smooth=False, mat=m)


def footprint(bpy, name, p, kit):
    """A big furry footprint pressed in snow, lying flat: a broad sole and five round toes, `length` heel to toe,
    `side` 1 for a right foot, -1 a left, `depth` thick."""
    L = p.get('length', 0.4); side = p.get('side', 1)
    W = L * 0.48
    bm = bmesh.new()
    sole = []
    for i in range(28):
        t = 2 * math.pi * i / 28
        x, y = math.cos(t) * W / 2, math.sin(t) * L * 0.36
        x *= 0.78 + 0.22 * (math.sin(t) + 1) / 2      # the heel narrower than the ball
        x += side * 0.05 * L * math.sin(t)            # the ball turned out, as a foot is
        sole.append((x, y - L * 0.08))
    kit._extrude(bm, sole, p.get('depth', 0.006), 0.0)
    for k, (tx, r) in enumerate([(-0.42, 0.065), (-0.21, 0.075), (0.0, 0.08), (0.21, 0.075), (0.44, 0.09)]):
        cx = tx * W * side * 1.1; cy = L * 0.33 + L * 0.07 * (1 - abs(tx) * 1.8)
        toe = bmesh.new()
        kit._extrude(toe, [(cx + math.cos(2 * math.pi * i / 16) * r * L, cy + math.sin(2 * math.pi * i / 16) * r * L) for i in range(16)],
                     p.get('depth', 0.006) * 0.7, 0.0)      # thinner than the sole, so no face lies on another
        me = bpy.data.meshes.new('tmp'); toe.to_mesh(me); toe.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
    # lay it flat: the outline was drawn in x-z, depth along y; turn y into z
    for v in bm.verts:
        v.co = Vector((v.co.x, v.co.z, v.co.y))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return kit.finish(bpy, name, bm, p, smooth=False)
