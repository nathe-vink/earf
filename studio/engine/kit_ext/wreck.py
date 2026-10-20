"""A burnt-out car and its fire (round 31b, Smoke E7: spinoffs/barkhorn/elements/smoke_bridge.py).

sedan: a mid-size saloon burnt to a shell, from real proportions (4.8 m long, 1.83 wide, 1.45 high, a 2.8 m wheelbase,
1.58 m track): the lower body lofted from rounded sections, the cabin's pillars and a sagging roof with no glass, charred
seats and a dash inside, bare rims standing in puddles of melted tyre. Its paint is gone to soot, rust and bare steel
(noise patches, `paint` showing through where `paint_left` says), its front crumpled by `crumple` metres. Placed by
`position` [x, y] and `heading` degrees (0: its nose toward +x).

flame: fire as an emitting volume, a box `size` [w, d, h] standing at `position`: density carved by stretched noise into
tongues that taper and break up as they rise, glowing by black-body temperature from about 1400 K at the roots to dull
red at the tips (`hot`, `cool` kelvin), `strength` its brightness, `seed`.
"""
import math, random

import bmesh
from mathutils import Matrix, Vector, noise

L, W, H = 4.8, 1.83, 1.45
WHEELBASE, TRACK, RIM = 2.8, 1.58, 0.225


def _section(x, hw, zb, zt, n=14):
    """A rounded body section at x: the sill at zb, the beltline (or the hood or deck) at zt, tumblehome above."""
    pts = []
    rb, rt = 0.09, 0.14
    corners = [(hw - rb, zb + rb, rb, -90, 0), (hw * 0.94 - rt, zt - rt, rt, 0, 90),
               (-(hw * 0.94 - rt), zt - rt, rt, 90, 180), (-(hw - rb), zb + rb, rb, 180, 270)]
    for cy, cz, r, a0, a1 in corners:
        for k in range(n // 4 + 1):
            a = math.radians(a0 + (a1 - a0) * k / (n // 4))
            pts.append(Vector((x, cy + r * math.cos(a), cz + r * math.sin(a))))
    return pts


def _loft(bm, sections):
    rings = [[bm.verts.new(p) for p in s] for s in sections]
    m = len(rings[0])
    for a, b in zip(rings, rings[1:]):
        for k in range(m):
            bm.faces.new((a[k], a[(k + 1) % m], b[(k + 1) % m], b[k]))
    bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    return rings


def _charred(bpy, kit, name, paint, paint_left, seed):
    """Burnt paint: soot, rust and bare steel in noise patches, a little of the paint left where the fire missed."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    def nz(scale, det, off):
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale
        n.inputs['Detail'].default_value = det
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Location'].default_value = (off, off * 0.7, off * 1.3)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
        return n.outputs['Fac']
    def ramp(fac, stops):
        r = nt.nodes.new('ShaderNodeValToRGB'); cr = r.color_ramp
        cr.elements[0].position, cr.elements[0].color = stops[0][0], kit.M.hex_lin(stops[0][1])
        cr.elements[1].position, cr.elements[1].color = stops[1][0], kit.M.hex_lin(stops[1][1])
        for pos, col in stops[2:]:
            e = cr.elements.new(pos); e.color = kit.M.hex_lin(col)
        nt.links.new(fac, r.inputs['Fac'])
        return r.outputs['Color']
    soot_rust = ramp(nz(3.0, 8.0, seed), [(0.42, '#0C0B0A'), (0.62, '#4A2B1B'), (0.55, '#1E1611'), (0.72, '#6A3A22')])
    steel = nz(1.6, 6.0, seed + 3.1)
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.58; mr.inputs['From Max'].default_value = 0.66
    nt.links.new(steel, mr.inputs['Value']); nt.links.new(mr.outputs['Result'], mix.inputs['Factor'])
    nt.links.new(soot_rust, mix.inputs['A']); mix.inputs['B'].default_value = kit.M.hex_lin('#5E5B57')
    col = mix.outputs['Result']
    if paint_left > 0:
        pm = nt.nodes.new('ShaderNodeMix'); pm.data_type = 'RGBA'
        pr = nt.nodes.new('ShaderNodeMapRange')
        pr.inputs['From Min'].default_value = 1.0 - paint_left; pr.inputs['From Max'].default_value = 1.0 - paint_left + 0.04
        nt.links.new(nz(0.8, 3.0, seed + 7.7), pr.inputs['Value']); nt.links.new(pr.outputs['Result'], pm.inputs['Factor'])
        nt.links.new(col, pm.inputs['A']); pm.inputs['B'].default_value = kit.M.hex_lin(paint)
        col = pm.outputs['Result']
    nt.links.new(col, b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.82
    met = nt.nodes.new('ShaderNodeMath'); met.operation = 'MULTIPLY'; met.inputs[1].default_value = 0.7
    nt.links.new(mr.outputs['Result'], met.inputs[0]); nt.links.new(met.outputs[0], b.inputs['Metallic'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35
    nt.links.new(nz(14.0, 10.0, seed + 2.2), bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def _flat(bpy, kit, name, color, rough=0.9, metallic=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = kit.M.hex_lin(color)
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metallic
    return m


def sedan(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    seed = p.get('seed', 1) * 1.37
    bm = bmesh.new()
    # the lower body: sill, beltline, hood and boot, lofted from the tail (x -2.4) to the nose (x 2.4)
    prof = [(-2.40, 0.80, 0.36, 0.80), (-2.30, 0.88, 0.30, 0.95), (-1.6, 0.91, 0.30, 1.00), (-0.9, 0.915, 0.30, 0.98),
            (0.0, 0.915, 0.30, 0.96), (0.9, 0.91, 0.30, 0.93), (1.6, 0.90, 0.31, 0.86), (2.2, 0.86, 0.33, 0.78),
            (2.40, 0.78, 0.36, 0.68)]
    secs = []
    for i in range(len(prof) - 1):
        for k in range(4):
            f = k / 4
            a, b = prof[i], prof[i + 1]
            secs.append(_section(*[a[j] + (b[j] - a[j]) * f for j in range(4)]))
    secs.append(_section(*prof[-1]))
    _loft(bm, secs)
    # crumple: the panels dented all over, the nose pushed in
    cr = p.get('crumple', 0.25)
    for v in bm.verts:
        d = noise.noise_vector(v.co * 2.2 + Vector((seed, seed, seed))) * 0.025
        front = max(0.0, (v.co.x - 1.7) / 0.7)
        d += Vector((-cr * front ** 1.5, 0.0, -0.4 * cr * front ** 2)) + noise.noise_vector(v.co * 5.0) * 0.06 * front
        v.co += d
    me = bpy.data.meshes.new(name + '-body'); bm.to_mesh(me); bm.free()
    obs = []
    char = _charred(bpy, kit, name + '-char', p.get('paint', '#2A2D31'), p.get('paint_left', 0.0), seed)
    ob = bpy.data.objects.new(name + '-body', me); me.materials.append(char); obs.append(ob)
    # the cabin: A, B and C pillars and a roof sagging where the fire softened it; no glass
    cab = bmesh.new()
    pillars = [((1.0, 0.82, 0.96), (0.35, 0.68, 1.41)), ((-0.2, 0.89, 0.97), (-0.2, 0.70, 1.43)),
               ((-1.3, 0.83, 0.99), (-0.75, 0.68, 1.41))]
    for (a, b) in pillars:
        for s in (1, -1):
            kit._tube(cab, [(a[0], s * a[1], a[2]), ((a[0] + b[0]) / 2, s * (a[1] + b[1]) / 2 + s * 0.02, (a[2] + b[2]) / 2),
                            (b[0], s * b[1], b[2])], 0.045, 0.6, 0.0, 8, 4)
    rf = bmesh.new()
    roof = []
    sag = p.get('sag', 0.08)
    for i in range(7):
        x = 0.35 - 1.1 * i / 6
        row = []
        for j in range(7):
            y = -0.68 + 1.36 * j / 6
            z = 1.43 - 0.05 * (abs(y) / 0.68) ** 2 - sag * math.sin(math.pi * i / 6) * math.sin(math.pi * j / 6)
            row.append(rf.verts.new((x, y, z + 0.01 * rnd.uniform(-1, 1))))
        roof.append(row)
    for i in range(6):
        for j in range(6):
            rf.faces.new((roof[i][j], roof[i][j + 1], roof[i + 1][j + 1], roof[i + 1][j]))
    bmesh.ops.solidify(rf, geom=rf.faces[:], thickness=0.02)
    rme = bpy.data.meshes.new(name + '-roof'); rf.to_mesh(rme); rf.free()
    rob = bpy.data.objects.new(name + '-roof', rme); rme.materials.append(char); obs.append(rob)
    me = bpy.data.meshes.new(name + '-cabin'); cab.to_mesh(me); cab.free()
    ob = bpy.data.objects.new(name + '-cabin', me); me.materials.append(char); obs.append(ob)
    # inside: charred seat frames and the dash
    inner = bmesh.new()
    for (cx, cy, sx, sy, sz, z0) in [(0.25, 0.4, 0.5, 0.5, 0.12, 0.55), (0.25, -0.4, 0.5, 0.5, 0.12, 0.55),
                                    (-0.05, 0.4, 0.1, 0.48, 0.55, 0.6), (-0.05, -0.4, 0.1, 0.48, 0.55, 0.6),
                                    (-0.85, 0.0, 0.55, 1.4, 0.14, 0.55), (-1.1, 0.0, 0.12, 1.4, 0.45, 0.62),
                                    (0.85, 0.0, 0.35, 1.6, 0.22, 0.75)]:
        g = bmesh.ops.create_cube(inner, size=1.0)
        for v in g['verts']:
            v.co = Vector((cx + v.co.x * sx, cy + v.co.y * sy, z0 + (v.co.z + 0.5) * sz))
    me = bpy.data.meshes.new(name + '-inside'); inner.to_mesh(me); inner.free()
    ob = bpy.data.objects.new(name + '-inside', me); me.materials.append(_flat(bpy, kit, name + '-ash', '#0E0D0C', 0.95))
    obs.append(ob)
    # the wheels: bare rims, the tyres burnt away to puddles of melted rubber under them
    rim_m = _flat(bpy, kit, name + '-rim', '#4C4A47', 0.5, 0.8)
    tar_m = _flat(bpy, kit, name + '-tar', '#050505', 0.35)
    for wx in (WHEELBASE / 2 - 0.05, -WHEELBASE / 2 - 0.05):
        for wy in (TRACK / 2, -TRACK / 2):
            rb = bmesh.new()
            g = bmesh.ops.create_cone(rb, cap_ends=True, segments=32, radius1=RIM, radius2=RIM, depth=0.2)
            bmesh.ops.rotate(rb, verts=g['verts'], cent=Vector(), matrix=Matrix.Rotation(math.pi / 2, 3, 'X'))
            # spokes as a dark hub disc inset on the outer face
            h = bmesh.ops.create_cone(rb, cap_ends=True, segments=16, radius1=0.07, radius2=0.07, depth=0.22)
            bmesh.ops.rotate(rb, verts=h['verts'], cent=Vector(), matrix=Matrix.Rotation(math.pi / 2, 3, 'X'))
            bmesh.ops.translate(rb, vec=Vector((wx, wy, RIM - 0.02)), verts=rb.verts[:])
            me = bpy.data.meshes.new(name + '-rim'); rb.to_mesh(me); rb.free()
            ob = bpy.data.objects.new(name + '-rim', me); me.materials.append(rim_m); obs.append(ob)
            tb = bmesh.new()
            g = bmesh.ops.create_cone(tb, cap_ends=True, segments=24, radius1=0.34 + 0.05 * rnd.random(), radius2=0.3,
                                      depth=0.025)
            for v in g['verts']:
                v.co.x *= 1.0 + 0.25 * noise.noise(v.co * 6 + Vector((wx, wy, 0)))
            bmesh.ops.translate(tb, vec=Vector((wx, wy, 0.0125)), verts=tb.verts[:])
            me = bpy.data.meshes.new(name + '-tar'); tb.to_mesh(me); tb.free()
            ob = bpy.data.objects.new(name + '-tar', me); me.materials.append(tar_m); obs.append(ob)
    # the body sits low on its rims: the suspension gone soft in the fire
    x, y = p.get('position', [0.0, 0.0])[:2]
    hd = math.radians(p.get('heading', 0.0))
    for ob in obs:
        bpy.context.scene.collection.objects.link(ob)
        ob.location = Vector((x, y, -0.06 if any(k in ob.name for k in ('body', 'cabin', 'inside', 'roof')) else 0.0))
        ob.rotation_euler.z = hd
    return obs


def flame(bpy, name, p, kit):
    w, d, h = p.get('size', [1.2, 0.8, 1.2])
    bm = bmesh.new()
    g = bmesh.ops.create_cube(bm, size=1.0)
    for v in g['verts']:
        v.co = Vector((v.co.x * w, v.co.y * d, (v.co.z + 0.5) * h))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = (0.02, 0.02, 0.02, 1)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    # tongues: noise stretched upward and drifting with height
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 1.0, 0.35)
    mp.inputs['Location'].default_value = (p.get('seed', 0) * 3.3, p.get('seed', 0) * 1.7, 0.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('scale', 0.18)
    nz.inputs['Detail'].default_value = 6.0; nz.inputs['Distortion'].default_value = 1.4
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    # the envelope: full at the roots, narrowing and fading with height, falling off toward the sides
    hz = nt.nodes.new('ShaderNodeMapRange'); hz.inputs['From Min'].default_value = 0.0; hz.inputs['From Max'].default_value = 1.0
    hz.inputs['To Min'].default_value = 1.0; hz.inputs['To Max'].default_value = 0.0
    nt.links.new(sep.outputs['Z'], hz.inputs['Value'])
    def side(sock):
        a = nt.nodes.new('ShaderNodeMath'); a.operation = 'SUBTRACT'; a.inputs[1].default_value = 0.5
        nt.links.new(sock, a.inputs[0])
        b = nt.nodes.new('ShaderNodeMath'); b.operation = 'ABSOLUTE'; nt.links.new(a.outputs[0], b.inputs[0])
        c = nt.nodes.new('ShaderNodeMapRange'); c.inputs['From Min'].default_value = 0.5; c.inputs['From Max'].default_value = 0.15
        nt.links.new(b.outputs[0], c.inputs['Value'])
        return c.outputs['Result']
    env = nt.nodes.new('ShaderNodeMath'); env.operation = 'MULTIPLY'
    nt.links.new(side(sep.outputs['X']), env.inputs[0]); nt.links.new(side(sep.outputs['Y']), env.inputs[1])
    env2 = nt.nodes.new('ShaderNodeMath'); env2.operation = 'MULTIPLY'
    nt.links.new(env.outputs[0], env2.inputs[0]); nt.links.new(hz.outputs['Result'], env2.inputs[1])
    # the noise above a threshold that rises with height: solid at the roots, tongues above, wisps at the tips
    th = nt.nodes.new('ShaderNodeMath'); th.operation = 'MULTIPLY_ADD'
    nt.links.new(sep.outputs['Z'], th.inputs[0]); th.inputs[1].default_value = 0.35; th.inputs[2].default_value = 0.35
    sub = nt.nodes.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'
    nt.links.new(nz.outputs['Fac'], sub.inputs[0]); nt.links.new(th.outputs[0], sub.inputs[1])
    cl = nt.nodes.new('ShaderNodeMapRange'); cl.inputs['From Min'].default_value = 0.0; cl.inputs['From Max'].default_value = 0.12
    nt.links.new(sub.outputs[0], cl.inputs['Value'])
    fire = nt.nodes.new('ShaderNodeMath'); fire.operation = 'MULTIPLY'
    nt.links.new(cl.outputs['Result'], fire.inputs[0]); nt.links.new(env2.outputs[0], fire.inputs[1])
    dens = nt.nodes.new('ShaderNodeMath'); dens.operation = 'MULTIPLY'; dens.inputs[1].default_value = p.get('density', 6.0)
    nt.links.new(fire.outputs[0], dens.inputs[0]); nt.links.new(dens.outputs[0], vol.inputs['Density'])
    # temperature: hot at the roots and in the cores, cooling to dull red at the tips
    tmp = nt.nodes.new('ShaderNodeMapRange'); tmp.inputs['From Min'].default_value = 0.0; tmp.inputs['From Max'].default_value = 1.0
    tmp.inputs['To Min'].default_value = p.get('cool', 750.0); tmp.inputs['To Max'].default_value = p.get('hot', 1450.0)
    hot = nt.nodes.new('ShaderNodeMath'); hot.operation = 'MULTIPLY'
    nt.links.new(hz.outputs['Result'], hot.inputs[0]); nt.links.new(cl.outputs['Result'], hot.inputs[1])
    nt.links.new(hot.outputs[0], tmp.inputs['Value'])
    nt.links.new(tmp.outputs['Result'], vol.inputs['Temperature'])
    vol.inputs['Blackbody Intensity'].default_value = p.get('strength', 1.0)
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    me.materials.append(m)
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]
