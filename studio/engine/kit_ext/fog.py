"""Fog's own kit pieces (round 31's dioramas: a sky of felt clouds on threads, and cotton-wool fog).

- plush: the Fog icon (three circles on a bar) as a stuffed felt ornament: two felt faces sewn round the edge, plump in
  the middle, the seam a running stitch of thread. `size` metres an icon unit, `thick` its half-thickness as a share of
  the big circle's radius, `stitch` the seam thread's colour (none: no seam), `fuzz` stray fibres (0 none).
- fluff: cotton wool pulled into a bank: overlapping squashed balls (`puffs` [[x, y, z, r], ...] in the piece's frame,
  `squash` their height over width) with a halo of loose fibres (`fuzz`: fibres a square metre of surface, `fibre`
  their length in metres).
- mist: a low fog the light shows in, a scattering volume in a box (`box` [x0, y0, z0, x1, y1, z1]) thick at the floor
  and thinning to nothing at `height`, broken into billows by noise `billow` metres across (`clump` how much); `density`
  per metre at the floor, `color`.

Called by kit.py as fn(bpy, name, p, kit); each returns its objects.
"""
import math, random

import bmesh
from mathutils import Vector

# the icon (spinoffs/barkhorn/marks.py, CLOUD), icon units, y down, centred on its box
_CIRCLES = [(-171.0, 80.0, 115.0), (-11.0, -22.0, 173.0), (187.0, 64.0, 131.0)]
_BAR = (-171.0, 80.0, 187.0, 195.0)
_CY = 0.0


def _inside(x, y, grow=0.0):
    for cx, cy, r in _CIRCLES:
        if (x - cx) ** 2 + (y - cy) ** 2 <= (r + grow) ** 2:
            return True
    x0, y0, x1, y1 = _BAR
    return x0 - grow <= x <= x1 + grow and y0 - grow <= y <= y1 + grow


def _sdf(x, y):
    """Signed distance to the icon's outline (negative inside), icon units."""
    d = min(math.hypot(x - cx, y - cy) - r for cx, cy, r in _CIRCLES)
    x0, y0, x1, y1 = _BAR
    qx, qy = max(x0 - x, x - x1), max(y0 - y, y - y1)
    db = math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0)
    return min(d, db)


def outline(n=360, centre=(10.0, 70.0)):
    """The icon's outline as points round it (icon units, y down): the farthest inside point along each ray from a
    point in the bar (the shape is star-shaped from there)."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        dx, dy = math.cos(a), math.sin(a)
        lo, hi = 0.0, 400.0
        # march out, then refine the last crossing
        r, last = 0.0, 0.0
        while r < 420.0:
            if _inside(centre[0] + dx * r, centre[1] + dy * r):
                last = r
            r += 2.0
        lo, hi = last, last + 2.0
        for _ in range(12):
            m = (lo + hi) / 2
            if _inside(centre[0] + dx * m, centre[1] + dy * m):
                lo = m
            else:
                hi = m
        pts.append((centre[0] + dx * lo, centre[1] + dy * lo))
    return pts


def _pillow(bm, s, thick, res):
    """A pillow on the icon's outline: a grid over its box, the cells inside it kept, each face pushed out by the
    distance to the edge (round at the seam, plump in the middle), the two faces meeting at y = 0 along the outline."""
    x0, x1, y0, y1 = -300.0, 330.0, -200.0, 200.0
    step = res / s                                       # icon units a cell
    nx, ny = int((x1 - x0) / step) + 1, int((y1 - y0) / step) + 1
    R = 173.0 * thick                                    # the plump half-thickness, icon units
    edge = 60.0                                          # how far in from the seam the face reaches full height
    def h(d):                                            # d: depth inside (>= 0)
        t = min(1.0, d / edge)
        return R * math.sqrt(max(0.0, 1.0 - (1.0 - t) ** 2)) * (0.86 + 0.14 * min(1.0, d / 170.0))
    grid = {}
    def vert(i, j, side):
        k = (i, j, side)
        if k not in grid:
            x, y = x0 + i * step, y0 + j * step
            d = -_sdf(x, y)
            if d < 0:                                    # just outside: pull onto the outline
                gx = (_sdf(x + 0.5, y) - _sdf(x - 0.5, y)); gy = (_sdf(x, y + 0.5) - _sdf(x, y - 0.5))
                g = math.hypot(gx, gy) or 1.0
                x, y = x + d * gx / g * -1, y + d * gy / g * -1
                d = 0.0
            yy = h(d) * (1 if side else -1)
            grid[k] = bm.verts.new((x * s, yy * s, -y * s))
        return grid[k]
    inside = [[_sdf(x0 + i * step, y0 + j * step) < 0 for j in range(ny)] for i in range(nx)]
    for i in range(nx - 1):
        for j in range(ny - 1):
            c = [inside[i][j], inside[i + 1][j], inside[i + 1][j + 1], inside[i][j + 1]]
            if not any(c):
                continue
            for side in (0, 1):
                q = [vert(i, j, side), vert(i + 1, j, side), vert(i + 1, j + 1, side), vert(i, j + 1, side)]
                if len({v.index if v.index >= 0 else id(v) for v in q}) < 4 and len(set(map(id, q))) < 4:
                    continue
                try:
                    bm.faces.new(q if side else q[::-1])
                except ValueError:
                    pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=s * 0.6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


def plush(bpy, name, p, kit):
    s = p.get('size', 0.0014)
    thick = p.get('thick', 0.32)
    bm = bmesh.new()
    _pillow(bm, s, thick, p.get('res', 0.008))
    # smooth the grid's stair-steps at the seam
    for _ in range(p.get('smooth', 6)):
        bmesh.ops.smooth_vert(bm, verts=bm.verts[:], factor=0.5, use_axis_x=True, use_axis_y=False, use_axis_z=True)
    obs = kit.finish(bpy, name, bm, p)
    ob = obs[0]
    sub = ob.modifiers.new('sub', 'SUBSURF'); sub.levels = 1; sub.render_levels = 1
    if p.get('stitch'):
        pts = outline(p.get('stitches', 110) * 2)
        # a running stitch: short dashes along the seam, alternate dashes on the faces' edge
        sp = {**p, 'material': 'paper', 'color': p['stitch'], 'shape': 'stitch'}
        mat = kit.material(bpy, 'paper', p['stitch'], {'roughness': 0.9})
        sb = bmesh.new()
        r = p.get('stitch_r', 0.0028)
        inset = p.get('stitch_in', 9.0)
        for k in range(0, len(pts), 2):
            (ax, ay), (bx, by) = pts[k], pts[(k + 1) % len(pts)]
            # pull the dash a little inside, onto the face beside the seam
            def pull(x, y):
                gx = (_sdf(x + 0.5, y) - _sdf(x - 0.5, y)); gy = (_sdf(x, y + 0.5) - _sdf(x, y - 0.5))
                g = math.hypot(gx, gy) or 1.0
                return x - gx / g * inset, y - gy / g * inset
            ax, ay = pull(ax, ay); bx, by = pull(bx, by)
            for side in (-1, 1):
                dd = -_sdf(ax, ay)
                yy = 173.0 * thick * math.sqrt(max(0.0, 1 - (1 - min(1.0, dd / 60.0)) ** 2)) * 0.86 * side
                a = Vector((ax * s, yy * s + side * r * 0.4, -ay * s)); b = Vector((bx * s, yy * s + side * r * 0.4, -by * s))
                kit._tube(sb, [a, (a + b) / 2, b], r, 1.0, 0.0, 6, 2)
        so = kit.finish(bpy, name + '-stitch', sb, {**sp, 'position': p.get('position', [0, 0, 0]),
                                                     'rotate': p.get('rotate', [0, 0, 0]), 'scale': p.get('scale', 1.0)}, True, mat)
        obs += so
    if p.get('fuzz'):
        _hair(bpy, ob, p, p['fuzz'], p.get('fibre', 0.012))
    return obs


def _hair(bpy, ob, p, density, length):
    """Loose fibres over an object's surface (felt's halo, cotton wool's wisps): a hair system, the strands its own
    material's colour."""
    me = ob.data
    area = sum(f.area for f in me.polygons) * (max(ob.scale) ** 2)
    n = int(min(250000, max(200, area * density)))
    mod = ob.modifiers.new('fibres', 'PARTICLE_SYSTEM')
    ps = mod.particle_system; st = ps.settings
    st.type = 'HAIR'; st.count = n; st.hair_length = length
    st.use_advanced_hair = True                          # length is the emitting speed along the normal
    st.emit_from = 'FACE'; st.use_emit_random = True
    st.normal_factor = length; st.factor_random = length * 0.3
    st.brownian_factor = p.get('frizz', 0.0)
    st.hair_step = 5
    st.display_step = 3; st.render_step = 4
    st.child_type = 'NONE'
    st.root_radius = p.get('fibre_r', 0.06); st.tip_radius = 0.0; st.radius_scale = 0.01
    st.use_close_tip = True
    ps.seed = p.get('seed', 3)
    # kink and roughness make strands wander rather than stand like grass
    st.roughness_1 = p.get('rough', 0.9) * length; st.roughness_1_size = 1.0
    st.roughness_2 = p.get('rough2', 0.6) * length; st.roughness_2_size = 1.0; st.roughness_2_threshold = 0.4
    st.roughness_endpoint = p.get('rough_end', 0.6) * length; st.roughness_end_shape = 1.0
    st.length_random = 0.7
    return mod


def fluff(bpy, name, p, kit):
    bm = bmesh.new()
    sq = p.get('squash', 0.6)
    for x, y, z, r in p['puffs']:
        kit._sphere(bm, (x, y, z), (r, r * p.get('deep', 0.9), r * sq), 28)
    obs = kit.finish(bpy, name, bm, p)
    if p.get('fuzz'):
        _hair(bpy, obs[0], p, p['fuzz'], p.get('fibre', 0.03))
    return obs


def mist(bpy, name, p, kit):
    x0, y0, z0, x1, y1, z1 = p.get('box', [-3, -3, 0, 3, 3, 0.6])
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); v = nt.nodes.new('ShaderNodeVolumeScatter')
    v.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.25)
    v.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#FFFFFF'))
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    # height falloff: 1 at the floor to 0 at `height`, smooth (object coords: the box is placed at the origin)
    hz = nt.nodes.new('ShaderNodeMapRange'); hz.interpolation_type = 'SMOOTHERSTEP'
    hz.inputs['From Min'].default_value = p.get('floor', z0); hz.inputs['From Max'].default_value = p.get('height', z1)
    hz.inputs['To Min'].default_value = 1.0; hz.inputs['To Max'].default_value = 0.0
    nt.links.new(sep.outputs['Z'], hz.inputs['Value'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('billow', 0.4)
    nz.inputs['Detail'].default_value = 4.0
    if 'Roughness' in nz.inputs:
        nz.inputs['Roughness'].default_value = 0.55
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    cl = p.get('clump', 0.6)
    nr = nt.nodes.new('ShaderNodeMapRange'); nr.interpolation_type = 'SMOOTHSTEP'
    nr.inputs['From Min'].default_value = 0.5 - 0.25 * cl; nr.inputs['From Max'].default_value = 0.5 + 0.12 * cl
    nr.inputs['To Min'].default_value = 1.0 - cl; nr.inputs['To Max'].default_value = 1.0
    nt.links.new(nz.outputs['Fac'], nr.inputs['Value'])
    # the noise also lifts the fog's top unevenly: the height falloff read at z minus a billow
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    nt.links.new(hz.outputs['Result'], mul.inputs[0]); nt.links.new(nr.outputs['Result'], mul.inputs[1])
    den = nt.nodes.new('ShaderNodeMath'); den.operation = 'MULTIPLY'; den.inputs[1].default_value = p.get('density', 2.0)
    nt.links.new(mul.outputs['Value'], den.inputs[0]); nt.links.new(den.outputs['Value'], v.inputs['Density'])
    nt.links.new(v.outputs['Volume'], out.inputs['Volume'])
    m.cycles.volume_step_rate = p.get('step', 2.0)
    bm = bmesh.new()
    g = bmesh.ops.create_cube(bm, size=1.0)
    for vv in g['verts']:
        vv.co = Vector(((x0 + x1) / 2 + vv.co.x * (x1 - x0), (y0 + y1) / 2 + vv.co.y * (y1 - y0), (z0 + z1) / 2 + vv.co.z * (z1 - z0)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(m)
    # named 'zz-...', so a lamp's receivers can leave the fog out ('[!sz]*' and 's[!w]*': all but it and the sweep)
    ob = bpy.data.objects.new('zz-' + name, me); bpy.context.scene.collection.objects.link(ob)
    ob.visible_shadow = p.get('shadow', True)
    return [ob]


def _volume_mat(bpy, kit, name, p, radial=True):
    """Cotton wool as a volume: dense in the middle of each ball, eaten into fibrous wisps toward its surface."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); v = nt.nodes.new('ShaderNodeVolumePrincipled')
    v.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#FFFFFF'))
    v.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.2)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    # radial: 0 at the ball's centre, 1 at its surface (Generated runs 0..1 over the object's box)
    sub = nt.nodes.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    nt.links.new(tc.outputs['Generated'], sub.inputs[0])
    ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; nt.links.new(sub.outputs['Vector'], ln.inputs[0])
    r2 = nt.nodes.new('ShaderNodeMath'); r2.operation = 'MULTIPLY'; r2.inputs[1].default_value = 2.0
    nt.links.new(ln.outputs['Value'], r2.inputs[0])
    # fibres: a stretched, distorted noise in object space, `fibre` metres across
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('fibre', 0.05)
    nz.inputs['Detail'].default_value = 8.0; nz.inputs['Distortion'].default_value = p.get('distort', 1.2)
    if 'Roughness' in nz.inputs:
        nz.inputs['Roughness'].default_value = 0.62
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    # the surface eaten away: density where 1 + (noise - 0.5) * 4 fray exceeds the radius (the edge frays into wisps)
    a = nt.nodes.new('ShaderNodeMath'); a.operation = 'MULTIPLY_ADD'
    a.inputs[1].default_value = 4.0 * p.get('fray', 0.55); a.inputs[2].default_value = 1.0 - 2.0 * p.get('fray', 0.55)
    nt.links.new(nz.outputs['Fac'], a.inputs[0])
    d = nt.nodes.new('ShaderNodeMath'); d.operation = 'SUBTRACT'
    nt.links.new(a.outputs['Value'], d.inputs[0]); nt.links.new(r2.outputs['Value'], d.inputs[1])
    sm = nt.nodes.new('ShaderNodeMapRange'); sm.interpolation_type = 'SMOOTHSTEP'
    sm.inputs['From Min'].default_value = 0.0; sm.inputs['From Max'].default_value = p.get('soft', 0.25)
    sm.inputs['To Max'].default_value = p.get('density', 40.0)
    nt.links.new(d.outputs['Value'], sm.inputs['Value'])
    nt.links.new(sm.outputs['Result'], v.inputs['Density'])
    nt.links.new(v.outputs['Volume'], out.inputs['Volume'])
    m.cycles.volume_step_rate = p.get('step', 1.0)
    return m


def tufts(bpy, name, p, kit):
    """Cotton wool pulled into tufts: each of `puffs` [[x, y, z, r], ...] a squashed ball of scattering fibres, dense
    inside and fraying at its edge (`density` per metre inside, `fibre` metres across a clump, `fray`, `squash`)."""
    obs = []
    sq = p.get('squash', 0.65)
    m = _volume_mat(bpy, kit, name + '-wool', p)
    base = Vector(p.get('position', [0, 0, 0]))
    for i, (x, y, z, r) in enumerate(p['puffs']):
        bm = bmesh.new()
        kit._ico(bm, (0, 0, 0), 1.0, 2)
        me = bpy.data.meshes.new(f'{name}-{i}'); bm.to_mesh(me); bm.free()
        me.materials.append(m)
        ob = bpy.data.objects.new(f'{name}-{i}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = base + Vector((x, y, z)); ob.scale = (r * 1.1, r * p.get('deep', 0.9) * 1.1, r * sq * 1.1)
        ob.rotation_euler = (0, 0, (i * 1.7) % 3.14)
        obs.append(ob)
    return obs


def wool(bpy, name, p, kit):
    """Cotton wool pulled into a bank: balls (`puffs` [[x, y, z, r], ...], `squash` their height over width) melted
    together and torn into lumps by a displacement (`lumps` metres across, `tear` how deep as a share of the radius),
    deep-scattering so light glows through its edges, with loose fibres teased out of it (`fuzz` a square metre,
    `fibre` long)."""
    bm = bmesh.new()
    sq = p.get('squash', 0.6)
    for x, y, z, r in p['puffs']:
        g = bmesh.ops.create_icosphere(bm, subdivisions=p.get('subdiv', 4), radius=1.0)
        for v in g['verts']:
            v.co = Vector((x + v.co.x * r, y + v.co.y * r * p.get('deep', 0.9), z + v.co.z * r * sq))
    mat = kit.material(bpy, 'cotton', p.get('color', '#FBFBFA'), {'grain': p.get('grain', 1.0)}).copy()
    b = mat.node_tree.nodes['Principled BSDF']
    kit._set(b, 'Subsurface Weight', p.get('sss', 0.6))
    kit._set(b, 'Subsurface Radius', Vector((1.0, 0.95, 0.9)) * p.get('sss_r', 0.05))
    kit._set(b, 'Subsurface Scale', 1.0)
    obs = kit.finish(bpy, name, bm, p, True, mat)
    ob = obs[0]
    # one closed skin over the balls (overlapping shells trap the light scattering inside them)
    rm = ob.modifiers.new('skin', 'REMESH'); rm.mode = 'VOXEL'; rm.voxel_size = p.get('voxel', 0.012); rm.use_smooth_shade = True
    tx = bpy.data.textures.new(name + '-lumps', 'CLOUDS'); tx.noise_scale = p.get('lumps', 0.07); tx.noise_depth = 3
    tx.noise_basis = 'ORIGINAL_PERLIN'
    dm = ob.modifiers.new('lumps', 'DISPLACE'); dm.texture = tx; dm.texture_coords = 'OBJECT'
    rr = sum(q[3] for q in p['puffs']) / len(p['puffs'])
    dm.strength = rr * p.get('tear', 0.35); dm.mid_level = 0.55
    if p.get('fuzz'):
        mod = _hair(bpy, ob, p, p['fuzz'], p.get('fibre', 0.03))
        st = mod.particle_system.settings
        st.normal_factor = p.get('fibre', 0.03) * 0.35; st.tangent_factor = p.get('fibre', 0.03); st.tangent_phase = 0.0
        st.phase_factor_random = 2.0
        st.child_type = 'INTERPOLATED'; st.child_percent = 3; st.rendered_child_count = p.get('children', 6)
        st.child_radius = 0.02; st.clump_factor = 0.4
        st.roughness_1 = 0.02; st.roughness_2 = 0.03; st.roughness_endpoint = 0.02
        hm = kit.material(bpy, 'cotton', p.get('color', '#FBFBFA'), {'grain': p.get('grain', 1.0), 'fibres': 1}).copy()
        kit._set(hm.node_tree.nodes['Principled BSDF'], 'Subsurface Weight', 0.0)
        ob.data.materials.append(hm); st.material_slot = hm.name
    return obs


def ladder(bpy, name, p, kit):
    """A model-maker's ladder of balsa strip: two rails from the foot `a` to the top `b` (world points), `width` apart,
    rungs every `step`, the strip `strip` square."""
    a, b = Vector(p['a']), Vector(p['b'])
    w, step, t = p.get('width', 0.16), p.get('step', 0.11), p.get('strip', 0.014)
    up = (b - a).normalized()
    side = up.cross(Vector((0, 0, 1))).cross(up)            # placeholder, replaced below
    side = Vector(p.get('across', (1, 0, 0))); side = (side - up * side.dot(up)).normalized()
    L = (b - a).length
    bm = bmesh.new()
    def strip(p0, p1, th):
        d = p1 - p0; ln = d.length
        g = bmesh.ops.create_cube(bm, size=1.0)
        q = d.to_track_quat('Z', 'Y')
        for v in g['verts']:
            v.co = Vector((v.co.x * th, v.co.y * th, v.co.z * ln))
        bmesh.ops.rotate(bm, verts=g['verts'], cent=Vector((0, 0, 0)), matrix=q.to_matrix())
        bmesh.ops.translate(bm, vec=(p0 + p1) / 2, verts=g['verts'])
    for s_ in (-0.5, 0.5):
        strip(a + side * w * s_, b + side * w * s_, t)
    n = int(L / step)
    for i in range(1, n):
        c = a + up * (i * step)
        strip(c - side * (w / 2 + t * 0.3), c + side * (w / 2 + t * 0.3), t * 0.7)
    q = {**p, 'position': [0, 0, 0], 'rotate': [0, 0, 0], 'scale': 1.0}
    q.pop('shape', None)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(kit.piece_material(bpy, p))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]
