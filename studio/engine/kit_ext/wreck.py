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
    bmesh.ops.solidify(rf, geom=rf.faces[:], thickness=0.06)
    for sgn in (1, -1):
        kit._tube(rf, [(0.37, sgn * 0.69, 1.40), (-0.2, sgn * 0.71, 1.42 - 0.6 * sag), (-0.77, sgn * 0.69, 1.40)], 0.04, 1.0, 0.0,
                  8, 4)
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
    envs = nt.nodes.new('ShaderNodeMath'); envs.operation = 'POWER'; envs.inputs[1].default_value = 2.0
    nt.links.new(env.outputs[0], envs.inputs[0])
    env2 = nt.nodes.new('ShaderNodeMath'); env2.operation = 'MULTIPLY'
    nt.links.new(envs.outputs[0], env2.inputs[0]); nt.links.new(hz.outputs['Result'], env2.inputs[1])
    # the noise above a threshold that rises with height: solid at the roots, tongues above, wisps at the tips
    th = nt.nodes.new('ShaderNodeMath'); th.operation = 'MULTIPLY_ADD'
    nt.links.new(sep.outputs['Z'], th.inputs[0]); th.inputs[1].default_value = 0.25; th.inputs[2].default_value = 0.48
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
    tmp.inputs['To Min'].default_value = p.get('cool', 1050.0); tmp.inputs['To Max'].default_value = p.get('hot', 1800.0)
    hot = nt.nodes.new('ShaderNodeMath'); hot.operation = 'MULTIPLY'
    nt.links.new(hz.outputs['Result'], hot.inputs[0]); nt.links.new(cl.outputs['Result'], hot.inputs[1])
    nt.links.new(hot.outputs[0], tmp.inputs['Value'])
    # the emission itself: the black-body colour at that temperature, as bright as the flame is dense (the volume's own
    # black-body emission ignores density, which lit the whole box)
    bb = nt.nodes.new('ShaderNodeBlackbody'); nt.links.new(tmp.outputs['Result'], bb.inputs['Temperature'])
    nt.links.new(bb.outputs['Color'], vol.inputs['Emission Color'])
    es = nt.nodes.new('ShaderNodeMath'); es.operation = 'MULTIPLY'; es.inputs[1].default_value = p.get('strength', 1.0)
    nt.links.new(fire.outputs[0], es.inputs[0]); nt.links.new(es.outputs[0], vol.inputs['Emission Strength'])
    vol.inputs['Blackbody Intensity'].default_value = 0.0
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    me.materials.append(m)
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]


# --- E10: the shell a car fire leaves (round 31b, Smoke E10: the critics on E9's car, "a crude slab", "a flat slab
# with a tube on top", "a clean stand-in model with nothing showing it burns") ---------------------------------------
def _key(x, keys):
    """A smooth piecewise lookup in [(x, value), ...]."""
    if x <= keys[0][0]:
        return keys[0][1]
    for (x0, v0), (x1, v1) in zip(keys, keys[1:]):
        if x <= x1:
            f = (x - x0) / (x1 - x0)
            f = f * f * (3 - 2 * f)
            return v0 + (v1 - v0) * f
    return keys[-1][1]


# a mid-size saloon's lower body, tail (x -2.42) to nose (2.42): the top of the boot, beltline and bonnet; the sill;
# the half width
ZT2 = [(-2.42, 0.64), (-2.30, 0.84), (-2.05, 0.95), (-1.32, 0.985), (-1.0, 0.965), (0.0, 0.955), (0.92, 0.975),
       (1.25, 0.945), (2.0, 0.86), (2.30, 0.77), (2.42, 0.62)]
ZB2 = [(-2.42, 0.42), (-2.30, 0.33), (-2.0, 0.30), (0.0, 0.29), (2.0, 0.30), (2.30, 0.34), (2.42, 0.42)]
HW2 = [(-2.42, 0.78), (-2.30, 0.86), (-2.0, 0.895), (-1.0, 0.912), (0.0, 0.915), (1.0, 0.91), (1.6, 0.90),
       (2.1, 0.875), (2.30, 0.84), (2.42, 0.74)]
ARCH2, ARCH_Z = 0.37, 0.31             # the wheel arches, about the wheel centre's height before the fire
CABIN2 = (-1.22, 0.92)                 # the open top between the C- and A-pillar feet: no glass left


_KIT = None                                                 # the engine's kit, set by sedan2 (its tube sweep)


def kit_tube(bm, pts, r, flat, twist, sides, res):
    _KIT._tube(bm, pts, r, flat, twist, sides, res)


def _bars(bm, pts, r, flat=0.6, sides=8):
    """A pressed-steel member (a flattened tube) through pts."""
    kit_tube(bm, [Vector(p) for p in pts], r, flat, 0.0, sides, 4)


def _charred2(bpy, kit, name, paint, paint_left, seed, ash=0.6):
    """Burnt paint as a car fire leaves it: soot black at the openings, the bonnet's and roof's paint burnt to a pale
    grey ash, rust coming through down the sides in streaks, a little bare steel, the door and bonnet seams dark lines,
    and some of the paint left low on the doors where the fire missed (`paint_left`)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    L = nt.links
    tc = nt.nodes.new('ShaderNodeTexCoord')
    def node(kind, **inputs):
        n = nt.nodes.new(kind)
        for k, v in inputs.items():
            if k == 'op':
                n.operation = v
            else:
                n.inputs[k].default_value = v
        return n
    def nz(scale, det, off, stretch=(1.0, 1.0, 1.0)):
        n = node('ShaderNodeTexNoise', Scale=scale, Detail=det)
        mp = node('ShaderNodeMapping'); mp.inputs['Location'].default_value = (off, off * 0.7, off * 1.3)
        mp.inputs['Scale'].default_value = stretch
        L.new(tc.outputs['Object'], mp.inputs['Vector']); L.new(mp.outputs['Vector'], n.inputs['Vector'])
        return n.outputs['Fac']
    def ramp(fac, stops):
        r = nt.nodes.new('ShaderNodeValToRGB'); cr = r.color_ramp
        cr.elements[0].position, cr.elements[0].color = stops[0][0], kit.M.hex_lin(stops[0][1])
        cr.elements[1].position, cr.elements[1].color = stops[1][0], kit.M.hex_lin(stops[1][1])
        for pos, col in stops[2:]:
            e = cr.elements.new(pos); e.color = kit.M.hex_lin(col)
        L.new(fac, r.inputs['Fac'])
        return r.outputs['Color']
    def band(sock, lo, hi):
        mr = node('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = lo; mr.inputs['From Max'].default_value = hi
        L.new(sock, mr.inputs['Value'])
        return mr.outputs['Result']
    def mix(fac, a, b_):
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        L.new(fac, mx.inputs['Factor'])
        for slot, v in (('A', a), ('B', b_)):
            if isinstance(v, str):
                mx.inputs[slot].default_value = kit.M.hex_lin(v)
            else:
                L.new(v, mx.inputs[slot])
        return mx.outputs['Result']
    def mul(a, b_):
        n = node('ShaderNodeMath', op='MULTIPLY'); L.new(a, n.inputs[0])
        if isinstance(b_, float):
            n.inputs[1].default_value = b_
        else:
            L.new(b_, n.inputs[1])
        return n.outputs[0]
    sep_n = nt.nodes.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Normal'], sep_n.inputs['Vector'])   # object space: the car turns
    sep_p = nt.nodes.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep_p.inputs['Vector'])
    # soot to char grey
    col = ramp(nz(3.0, 8.0, seed), [(0.38, '#0B0A09'), (0.6, '#1E1B18'), (0.75, '#2C2824')])
    # rust in patches where the paint burnt off the steel, a few runs dripping from them
    patch = band(nz(2.4, 6.0, seed + 4.4), 0.56, 0.64)
    drip = band(nz(5.0, 4.0, seed + 6.1, (1.0, 1.0, 0.3)), 0.6, 0.7)
    rust_f = node('ShaderNodeMath', op='MAXIMUM'); L.new(patch, rust_f.inputs[0]); L.new(mul(drip, 0.6), rust_f.inputs[1])
    col = mix(rust_f.outputs[0], col, ramp(nz(6.0, 4.0, seed + 1.9), [(0.3, '#3A2014'), (0.7, '#66381F')]))
    # the paint burnt to pale ash on what faces up (bonnet, roof, boot), patchy
    up = band(sep_n.outputs['Z'], 0.45, 0.8)
    ash_f = mul(up, band(nz(1.4, 5.0, seed + 8.8), 0.62 - 0.3 * ash, 0.7 - 0.3 * ash))
    col = mix(ash_f, col, ramp(nz(9.0, 6.0, seed + 2.6), [(0.35, '#77736C'), (0.65, '#A7A29A')]))
    # a little bare steel
    steel = band(nz(1.6, 6.0, seed + 3.1), 0.66, 0.7)
    col = mix(steel, col, '#5E5B57')
    # the paint that survived, low on the doors
    if paint_left > 0:
        low = band(sep_p.outputs['Z'], 0.62, 0.4)
        keep = mul(low, band(nz(0.9, 3.0, seed + 7.7), 1.0 - paint_left, 1.04 - paint_left))
        col = mix(keep, col, paint)
    # the seams: door shuts down the sides, the bonnet's and boot's edges across the top
    side = band(mul(sep_n.outputs['Y'], sep_n.outputs['Y']), 0.25, 0.6)
    seam = None
    for c, on_side in ((0.92, True), (-0.15, True), (-1.18, True), (0.99, False), (-1.36, False)):
        d = node('ShaderNodeMath', op='SUBTRACT', **{}); L.new(sep_p.outputs['X'], d.inputs[0]); d.inputs[1].default_value = c
        a = node('ShaderNodeMath', op='ABSOLUTE'); L.new(d.outputs[0], a.inputs[0])
        line = band(a.outputs[0], 0.009, 0.0)
        line = mul(line, side if on_side else up)
        if seam is None:
            seam = line
        else:
            mx_ = node('ShaderNodeMath', op='MAXIMUM'); L.new(seam, mx_.inputs[0]); L.new(line, mx_.inputs[1])
            seam = mx_.outputs[0]
    col = mix(seam, col, '#040404')
    L.new(col, b.inputs['Base Color'])
    rough = node('ShaderNodeMapRange'); rough.inputs['To Min'].default_value = 0.92; rough.inputs['To Max'].default_value = 0.55
    L.new(steel, rough.inputs['Value']); L.new(rough.outputs['Result'], b.inputs['Roughness'])
    L.new(mul(steel, 0.7), b.inputs['Metallic'])
    bump = node('ShaderNodeBump', Strength=0.4, Distance=0.004)
    L.new(nz(18.0, 10.0, seed + 2.2), bump.inputs['Height']); L.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def _rust(bpy, kit, name, seed):
    """A rim the fire took the tyre off: rust, soot in its recesses."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 40.0; n.inputs['Detail'].default_value = 8.0
    n.noise_dimensions = '4D'; n.inputs['W'].default_value = seed
    nt.links.new(tc.outputs['Object'], n.inputs['Vector'])
    r = nt.nodes.new('ShaderNodeValToRGB'); cr = r.color_ramp
    cr.elements[0].position, cr.elements[0].color = 0.35, kit.M.hex_lin('#1A120C')
    cr.elements[1].position, cr.elements[1].color = 0.7, kit.M.hex_lin('#7A3E1E')
    e = cr.elements.new(0.55); e.color = kit.M.hex_lin('#4E2814')
    nt.links.new(n.outputs['Fac'], r.inputs['Fac']); nt.links.new(r.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.85; b.inputs['Metallic'].default_value = 0.25
    return m


def _rim(bm, cx, cy, out):
    """A five-spoke steel-alloy wheel, 16 in (0.2 m radius), its axle along y; `out` +1 or -1, the side its face
    looks to."""
    R, Wd = 0.2, 0.17
    for k in range(2):                                      # the barrel's two lips, and the barrel between
        z = cy + out * (Wd / 2 - k * Wd)
        g = bmesh.ops.create_cone(bm, cap_ends=False, segments=36, radius1=R + 0.012, radius2=R + 0.012, depth=0.018,
                                  matrix=Matrix.Translation(Vector((cx, z, ARCH_Z - 0.11))) @ Matrix.Rotation(math.pi / 2, 4, 'X'))
    g = bmesh.ops.create_cone(bm, cap_ends=False, segments=36, radius1=R - 0.01, radius2=R - 0.01, depth=Wd,
                              matrix=Matrix.Translation(Vector((cx, cy, ARCH_Z - 0.11))) @ Matrix.Rotation(math.pi / 2, 4, 'X'))
    c = Vector((cx, cy + out * (Wd / 2 - 0.03), ARCH_Z - 0.11))
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.065, radius2=0.05, depth=0.05,
                              matrix=Matrix.Translation(c) @ Matrix.Rotation(-out * math.pi / 2, 4, 'X'))
    for s in range(5):                                       # the spokes, from the hub to the rim
        a = 2 * math.pi * s / 5 + 0.3
        p0 = c + Vector((0.055 * math.cos(a), 0.0, 0.055 * math.sin(a)))
        p1 = c + Vector(((R - 0.015) * math.cos(a), -out * 0.035, (R - 0.015) * math.sin(a)))
        kit_tube(bm, [p0, (p0 + p1) / 2 + Vector((0, out * 0.006, 0)), p1], 0.022, 0.45, 0.0, 6, 3)
    # the brake disc behind the spokes
    bmesh.ops.create_cone(bm, cap_ends=True, segments=28, radius1=0.15, radius2=0.15, depth=0.026,
                          matrix=Matrix.Translation(Vector((cx, cy - out * 0.02, ARCH_Z - 0.11))) @ Matrix.Rotation(math.pi / 2, 4, 'X'))


def sedan2(bpy, name, p, kit):
    """E10's burnt saloon: the lower body lofted section by section with its wheel arches cut and its cabin open to
    the sky (the glass gone), the steel 1.8 cm thick at every edge; flattened pillars and a thin roof sagging where the
    fire softened it; inside, the seat frames and their springs, the steering wheel and the dash's crossbar; five-spoke
    rims standing in their melted tyres; burnt paint with ash on top, rust down the sides and the seams dark. Placed as
    `sedan` is (`position` [x, y], `heading`); `paint`, `paint_left`, `crumple` (the nose pushed in), `sag` (m),
    `seed`."""
    global _KIT
    _KIT = kit
    rnd = random.Random(p.get('seed', 1))
    seed = p.get('seed', 1) * 1.37
    xw = (WHEELBASE / 2, -WHEELBASE / 2)
    xs = []
    x = -2.42
    while x < 2.42:
        xs.append(x)
        near = min(abs(x - w) for w in xw) < ARCH2 + 0.06 or any(abs(x - c) < 0.05 for c in CABIN2)
        x += 0.02 if near else 0.06
    xs.append(2.42)
    bm = bmesh.new()
    rings = []
    for x in xs:
        zb = _key(x, ZB2)
        for w in xw:
            if abs(x - w) < ARCH2:
                zb = max(zb, ARCH_Z + math.sqrt(ARCH2 ** 2 - (x - w) ** 2))
        rings.append([bm.verts.new(v) for v in _section(x, _key(x, HW2), zb, _key(x, ZT2))])
    m = len(rings[0])
    top = (7, 8)                                            # the ring's flat top: open over the cabin
    for i, (a, b) in enumerate(zip(rings, rings[1:])):
        xm = (xs[i] + xs[i + 1]) / 2
        for k in range(m):
            if (k, (k + 1) % m) == top and CABIN2[0] < xm < CABIN2[1]:
                continue
            bm.faces.new((a[k], a[(k + 1) % m], b[(k + 1) % m], b[k]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])      # the tail and the nose
    cr = p.get('crumple', 0.2)
    for v in bm.verts:                                      # dents all over; the nose pushed in; the bonnet bowed up
        d = noise.noise_vector(v.co * 2.2 + Vector((seed, seed, seed))) * 0.02
        front = max(0.0, (v.co.x - 1.7) / 0.72)
        d += Vector((-cr * front ** 1.5, 0.0, -0.4 * cr * front ** 2)) + noise.noise_vector(v.co * 5.0) * 0.05 * front
        if 1.0 < v.co.x < 2.3 and v.co.z > 0.8:
            d.z += 0.035 * math.sin(math.pi * (v.co.x - 1.0) / 1.3) * (1 - (v.co.y / 0.9) ** 2)
        v.co += d
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.018)
    obs = []
    char = _charred2(bpy, kit, name + '-char', p.get('paint', '#2A2D31'), p.get('paint_left', 0.0), seed)
    metal = _charred2(bpy, kit, name + '-metal', '#202020', 0.0, seed + 5.0, ash=0.0)
    def emit(b_, tag, mat):
        me = bpy.data.meshes.new(f'{name}-{tag}'); b_.to_mesh(me); b_.free()
        if tag in ('body', 'roof'):                          # pressed panels, not facets
            for f in me.polygons:
                f.use_smooth = True
        ob = bpy.data.objects.new(f'{name}-{tag}', me); me.materials.append(mat); obs.append(ob)
    emit(bm, 'body', char)
    # the pillars, pressed steel, and the roof between them, sagging and buckled
    cab = bmesh.new()
    sag = p.get('sag', 0.09)
    for s in (1, -1):
        _bars(cab, [(0.93, s * 0.82, 0.96), (0.62, s * 0.74, 1.22), (0.35, s * 0.665, 1.41)], 0.04)      # A
        _bars(cab, [(-0.15, s * 0.885, 0.95), (-0.16, s * 0.79, 1.2), (-0.18, s * 0.675, 1.425 - 0.4 * sag)], 0.05)  # B
        _bars(cab, [(-1.22, s * 0.84, 0.97), (-1.0, s * 0.76, 1.22), (-0.79, s * 0.665, 1.40)], 0.06)    # C
        _bars(cab, [(0.36, s * 0.675, 1.41), (-0.2, s * 0.69, 1.425 - 0.6 * sag), (-0.80, s * 0.675, 1.40)], 0.035)  # rails
    _bars(cab, [(0.37, 0.66, 1.405), (0.37, 0.0, 1.43), (0.37, -0.66, 1.405)], 0.03)   # the windscreen's header
    _bars(cab, [(-0.80, 0.66, 1.395), (-0.80, 0.0, 1.42), (-0.80, -0.66, 1.395)], 0.03)
    rf = bmesh.new()
    grid = []
    for i in range(9):
        xx = 0.36 - 1.16 * i / 8
        row = []
        for j in range(9):
            yy = -0.66 + 1.32 * j / 8
            z = 1.425 - 0.045 * (abs(yy) / 0.66) ** 2 - sag * math.sin(math.pi * i / 8) * math.sin(math.pi * j / 8)
            z += 0.012 * noise.noise(Vector((xx * 4, yy * 4, seed)))
            row.append(rf.verts.new((xx, yy, z)))
        grid.append(row)
    for i in range(8):
        for j in range(8):
            rf.faces.new((grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]))
    bmesh.ops.solidify(rf, geom=rf.faces[:], thickness=0.012)
    emit(rf, 'roof', char)
    emit(cab, 'cabin', char)
    # inside: what the fire leaves of the seats (their frames and springs), the steering wheel, the dash's crossbar
    inner = bmesh.new()
    for s in (1, -1):
        y0, y1 = s * 0.12, s * 0.62
        base = [(-0.08, y0, 0.5), (0.42, y0, 0.52), (0.42, y1, 0.52), (-0.08, y1, 0.5), (-0.08, y0, 0.5)]
        for a, b_ in zip(base, base[1:]):
            _bars(inner, [a, b_], 0.012, 1.0, 6)
        for y in (y0, y1):
            _bars(inner, [(-0.08, y, 0.5), (-0.17, y, 0.78), (-0.26, y, 1.06)], 0.014, 1.0, 6)
        _bars(inner, [(-0.26, y0, 1.06), (-0.26, (y0 + y1) / 2, 1.08), (-0.26, y1, 1.06)], 0.014, 1.0, 6)
        for q in range(5):                                  # the springs, zigzag across the seat
            xq = -0.02 + 0.1 * q
            pts = [(xq + (0.025 if t % 2 else -0.025), y0 + (y1 - y0) * t / 8, 0.5 + 0.01 * rnd.random()) for t in range(9)]
            _bars(inner, pts, 0.005, 1.0, 5)
    for a, b_ in (((-1.15, 0.7, 0.47), (-0.62, 0.7, 0.49)), ((-1.15, -0.7, 0.47), (-0.62, -0.7, 0.49)),
                  ((-0.62, 0.7, 0.49), (-0.62, -0.7, 0.49)), ((-1.15, 0.7, 0.47), (-1.2, 0.7, 0.95)),
                  ((-1.15, -0.7, 0.47), (-1.2, -0.7, 0.95)), ((-1.2, 0.7, 0.95), (-1.2, -0.7, 0.95))):
        _bars(inner, [a, b_], 0.013, 1.0, 6)
    g = bmesh.ops.create_circle(inner, cap_ends=False, segments=28, radius=0.18)        # the steering wheel's rim
    ring = [v.co.copy() for v in g['verts']]
    for v in g['verts']:
        inner.verts.remove(v)
    tilt = Matrix.Rotation(math.radians(62), 3, 'Y')
    wc = Vector((0.5, 0.37, 0.84))
    _bars(inner, [tilt @ c + wc for c in ring] + [tilt @ ring[0] + wc], 0.016, 1.0, 6)
    _bars(inner, [wc, wc + Vector((0.3, 0.0, -0.08))], 0.022, 1.0, 6)                  # the column
    _bars(inner, [(0.8, 0.82, 0.88), (0.8, 0.0, 0.9), (0.8, -0.82, 0.88)], 0.03, 1.0, 8)   # the dash's crossbar
    emit(inner, 'inside', metal)
    # the wheels: rims standing in what is left of their tyres
    rust = _rust(bpy, kit, name + '-rust', seed)
    tar_m = _flat(bpy, kit, name + '-tar', '#050505', 0.35)
    for wx in xw:
        for wy in (TRACK / 2, -TRACK / 2):
            rb = bmesh.new()
            _rim(rb, wx, wy, 1 if wy > 0 else -1)
            emit(rb, 'rim', rust)
            tb = bmesh.new()
            g = bmesh.ops.create_cone(tb, cap_ends=True, segments=24, radius1=0.33 + 0.05 * rnd.random(), radius2=0.29,
                                      depth=0.02)
            for v in g['verts']:
                v.co.x *= 1.0 + 0.25 * noise.noise(v.co * 6 + Vector((wx, wy, 0)))
            bmesh.ops.translate(tb, vec=Vector((wx, wy, 0.01)), verts=tb.verts[:])
            emit(tb, 'tar', tar_m)
    # the body down on its rims (the tyres gone), placed and turned
    x, y = p.get('position', [0.0, 0.0])[:2]
    hd = math.radians(p.get('heading', 0.0))
    for ob in obs:
        bpy.context.scene.collection.objects.link(ob)
        ob.location = Vector((x, y, -0.13 if any(k in ob.name for k in ('body', 'cabin', 'inside', 'roof')) else 0.0))
        ob.rotation_euler.z = hd
    return obs
