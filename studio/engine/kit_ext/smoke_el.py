"""Smoke's own pieces (round 31b, spinoffs/barkhorn/elements/smoke.py).

woodsmoke: a drifting bank of woodsmoke as a scattering volume, a box `size` [w, d, h] standing at `position`, its
density `density` per metre carved by noise into wisps and banks (`scale` metres a wisp, `detail`, `cut` the share of
the noise left clear, `soft` how gradually it thickens), thinning toward the box's top and its edges (`fade`), its
colour `color` and its forward scattering `anisotropy` (woodsmoke throws light forward, so a sun behind it makes it
glow). `rise` stretches the wisps upward, `lean` [dx, dy] shears them as the smoke drifts. `seed` moves the noise.
"""
import math

import bmesh
from mathutils import Vector, noise


def woodsmoke(bpy, name, p, kit):
    w, d, h = p.get('size', [6.0, 4.0, 3.0])
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((v.co.x * w, v.co.y * d, (v.co.z + 0.5) * h))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))

    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#D8D4CE'))
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.6)
    # the noise, in the box's own coordinates: generated (0..1 over the box), turned to metres, sheared as it drifts
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    rise = p.get('rise', 1.6)
    mp.inputs['Scale'].default_value = (1.0, 1.0, 1.0 / rise)
    mp.inputs['Location'].default_value = (p.get('seed', 0) * 13.7, p.get('seed', 0) * 7.1, 0.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / p.get('scale', 0.8)
    nz.inputs['Detail'].default_value = p.get('detail', 6.0)
    if 'Roughness' in nz.inputs:
        nz.inputs['Roughness'].default_value = p.get('roughness', 0.62)
    nz.inputs['Distortion'].default_value = p.get('distortion', 0.35)
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    fac = nz.outputs['Fac']
    if p.get('detail_weight'):
        # a second, finer octave (curling wisps over the billows), added about its mean
        nz2 = nt.nodes.new('ShaderNodeTexNoise')
        nz2.inputs['Scale'].default_value = 1.0 / p.get('detail_scale', 0.2)
        nz2.inputs['Detail'].default_value = 4.0; nz2.inputs['Distortion'].default_value = 1.2
        nt.links.new(mp.outputs['Vector'], nz2.inputs['Vector'])
        sub = nt.nodes.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = 0.5
        nt.links.new(nz2.outputs['Fac'], sub.inputs[0])
        add = nt.nodes.new('ShaderNodeMath'); add.operation = 'MULTIPLY_ADD'; add.inputs[1].default_value = p['detail_weight']
        nt.links.new(sub.outputs[0], add.inputs[0]); nt.links.new(fac, add.inputs[2])
        fac = add.outputs[0]
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cut = p.get('cut', 0.5); soft = p.get('soft', 0.18)
    cr.elements[0].position = cut; cr.elements[0].color = (0, 0, 0, 1)
    cr.elements[1].position = min(0.999, cut + soft); cr.elements[1].color = (1, 1, 1, 1)
    nt.links.new(fac, ramp.inputs['Fac'])
    # fade toward the top and the sides (generated coords run 0..1 across the box)
    gen = tc.outputs['Generated']
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(gen, sep.inputs['Vector'])
    fade = p.get('fade', [0.15, 0.15, 0.45])          # the share of the box over which density falls to 0: x, y, top

    def edge(sock, f, both=True):
        """1 inside, falling to 0 within `f` of the edge (of both ends, or only the top)."""
        a = nt.nodes.new('ShaderNodeMapRange'); a.clamp = True
        if both:
            # distance from the nearer end: min(v, 1 - v)
            inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
            nt.links.new(sock, inv.inputs[1])
            mn = nt.nodes.new('ShaderNodeMath'); mn.operation = 'MINIMUM'
            nt.links.new(sock, mn.inputs[0]); nt.links.new(inv.outputs[0], mn.inputs[1])
            nt.links.new(mn.outputs[0], a.inputs['Value'])
        else:
            inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
            nt.links.new(sock, inv.inputs[1]); nt.links.new(inv.outputs[0], a.inputs['Value'])
        a.inputs['From Min'].default_value = 0.0; a.inputs['From Max'].default_value = max(1e-3, f)
        return a.outputs['Result']

    ex, ey, ez = edge(sep.outputs['X'], fade[0]), edge(sep.outputs['Y'], fade[1]), edge(sep.outputs['Z'], fade[2], both=False)
    m1 = nt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'; nt.links.new(ex, m1.inputs[0]); nt.links.new(ey, m1.inputs[1])
    m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'; nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(ez, m2.inputs[1])
    m3 = nt.nodes.new('ShaderNodeMath'); m3.operation = 'MULTIPLY'; nt.links.new(m2.outputs[0], m3.inputs[0])
    nt.links.new(ramp.outputs['Color'], m3.inputs[1])
    m4 = nt.nodes.new('ShaderNodeMath'); m4.operation = 'MULTIPLY'; m4.inputs[1].default_value = p.get('density', 0.4)
    nt.links.new(m3.outputs[0], m4.inputs[0])
    # a floor of thin haze under the wisps, so the shafts never stop dead between them
    m5 = nt.nodes.new('ShaderNodeMath'); m5.operation = 'MULTIPLY_ADD'
    nt.links.new(m2.outputs[0], m5.inputs[0]); m5.inputs[1].default_value = p.get('floor', 0.02)
    nt.links.new(m4.outputs[0], m5.inputs[2])
    dens = m5.outputs[0]
    if p.get('ground'):
        # a ground-hugging layer: woodsmoke pools low in still morning air, densest at the ground, gone by ground_h
        oz = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], oz.inputs['Vector'])
        gr = nt.nodes.new('ShaderNodeMapRange'); gr.clamp = True
        gr.inputs['From Min'].default_value = 0.0; gr.inputs['From Max'].default_value = p.get('ground_h', 1.5)
        gr.inputs['To Min'].default_value = p['ground']; gr.inputs['To Max'].default_value = 0.0
        nt.links.new(oz.outputs['Z'], gr.inputs['Value'])
        gm = nt.nodes.new('ShaderNodeMath'); gm.operation = 'MULTIPLY_ADD'
        nt.links.new(m1.outputs[0], gm.inputs[0]); nt.links.new(gr.outputs['Result'], gm.inputs[1]); nt.links.new(dens, gm.inputs[2])
        dens = gm.outputs[0]
    nt.links.new(dens, vol.inputs['Density'])
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    me.materials.append(m)
    ob.visible_shadow = True
    return [ob]


def trunks(bpy, name, p, kit):
    """Pine trunks at real scale: `trees` [[x, y, radius, height, lean_deg, lean_dir_deg, seed], ...], each a tapered,
    slightly irregular column with a flared root, its surface UV-mapped in metres so Poly Haven's bark `texture` lies at
    its real size all round. One mesh, one material."""
    import random
    import assets
    from mathutils import noise
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new('UVMap')
    sides, rings = p.get('sides', 40), p.get('rings', 48)
    for x, y, r0, H, lean, ldir, seed in p['trees']:
        rnd = random.Random(seed)
        off = Vector((rnd.uniform(-50, 50), rnd.uniform(-50, 50), rnd.uniform(-50, 50)))
        lx, ly = math.sin(math.radians(ldir)), math.cos(math.radians(ldir))
        grid = []
        for j in range(rings + 1):
            t = j / rings
            z = H * t ** 1.35                                      # rings closer near the root, where the flare is
            r = r0 * (1.0 - 0.55 * z / H) * (1.0 + 0.8 * math.exp(-z / (r0 * 1.4)))
            sway = math.tan(math.radians(lean)) * z
            row = []
            for i in range(sides):
                a = 2 * math.pi * i / sides
                bumpy = 1.0 + 0.06 * noise.noise(off + Vector((math.cos(a) * 1.3, math.sin(a) * 1.3, z * 0.8)))
                bumpy += 0.12 * math.exp(-z / (r0 * 1.2)) * max(0.0, math.sin(3 * a + seed))     # root buttresses
                row.append(bm.verts.new((x + lx * sway + math.cos(a) * r * bumpy, y + ly * sway + math.sin(a) * r * bumpy, z - 0.08)))
            grid.append((row, z, r))
        for j in range(rings):
            (ra, za, rra), (rb, zb, rrb) = grid[j], grid[j + 1]
            for i in range(sides):
                i2 = (i + 1) % sides
                f = bm.faces.new((ra[i], ra[i2], rb[i2], rb[i]))
                ua, ub = 2 * math.pi * rra, 2 * math.pi * rrb
                for loop, (u, v) in zip(f.loops, ((i / sides * ua, za), ((i + 1) / sides * ua, za),
                                                  ((i + 1) / sides * ub, zb), (i / sides * ub, zb))):
                    loop[uv].uv = (u, v)
        bm.faces.new([row for row in grid[-1][0]])
        # dead branch stubs from a few metres up, as self-pruned pines carry: thin cones angled out and a little down
        for k in range(rnd.randint(*p.get('stubs', (5, 11)))):
            z = rnd.uniform(p.get('stub_from', 3.5), H * 0.8)
            a = rnd.uniform(0, 2 * math.pi)
            r = r0 * (1.0 - 0.55 * z / H)
            L, rb = rnd.uniform(0.15, 0.9), rnd.uniform(0.015, 0.04)
            d = Vector((math.cos(a), math.sin(a), -rnd.uniform(0.05, 0.4))).normalized()
            base = Vector((x + lx * math.tan(math.radians(lean)) * z, y + ly * math.tan(math.radians(lean)) * z, z - 0.08))
            geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=rb, radius2=rb * 0.25, depth=L)
            q = d.to_track_quat('Z', 'Y')
            bmesh.ops.rotate(bm, verts=geom['verts'], cent=Vector((0, 0, 0)), matrix=q.to_matrix())
            bmesh.ops.translate(bm, vec=base + d * (r * 0.8 + L / 2), verts=geom['verts'])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(assets.pbr(bpy, p.get('texture', 'pine_bark'), p.get('res', '2k'), scale=p.get('tex_scale'),
                                   bump=p.get('bump', 1.0), coords='uv', tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0),
                                   displace=p.get('displace', 0.0)))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


def canopy(bpy, name, p, kit):
    """The pine wood's crowns overhead, out of frame: a layer `size` [w, d] at height `z`, opaque where noise says there
    are branches and open in gaps (`open` the share of sky, `scale` metres a clump), so a sun above cuts shafts through
    the smoke below and dapples the floor. It casts shadows only; the camera never sees it."""
    w, d = p.get('size', [60.0, 60.0])
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (w / 2, d / 2, 0), (-w / 2, d / 2, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    x, y = p.get('position', [0.0, 0.0])[:2]
    ob.location = Vector((x, y, p.get('z', 14.0)))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    df = nt.nodes.new('ShaderNodeBsdfDiffuse'); df.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#1C2016'))
    mix = nt.nodes.new('ShaderNodeMixShader')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('scale', 1.5)
    nz.inputs['Detail'].default_value = 8.0
    if 'Roughness' in nz.inputs:
        nz.inputs['Roughness'].default_value = 0.7
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Location'].default_value = (p.get('seed', 0) * 9.3, 0, 0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    o = p.get('open', 0.3)
    cr.elements[0].color = (0, 0, 0, 1)                                                    # branches
    cr.elements[1].color = (1, 1, 1, 1)                                                    # gaps
    # noise sits around 0.5: put the step at the quantile that leaves `open` of the layer clear
    cr.elements[0].position = 0.5 + (0.5 - o) * 0.22; cr.elements[1].position = cr.elements[0].position + 0.015
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], mix.inputs['Fac'])
    nt.links.new(df.outputs['BSDF'], mix.inputs[1]); nt.links.new(tr.outputs['BSDF'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    me.materials.append(m)
    ob.visible_camera = False
    return [ob]


def burnpile(bpy, name, p, kit):
    """A smouldering burn pile: `logs` of charred pine (cylinders in `texture` bark, darkened) heaped in a low cone of
    radius `radius`, with embers glowing in the gaps (`ember` strength). One mesh for the logs, one for the embers."""
    import random
    import assets
    rnd = random.Random(p.get('seed', 1))
    x0, y0, z0 = p.get('position', [0, 0, 0])
    R = p.get('radius', 0.9)
    bm = bmesh.new(); uv = bm.loops.layers.uv.new('UVMap')
    for i in range(p.get('logs', 14)):
        a = rnd.uniform(0, 2 * math.pi); d = R * math.sqrt(rnd.random()) * 0.7
        L = rnd.uniform(0.8, 1.6); r = rnd.uniform(0.04, 0.09)
        z = r + (1 - d / R) * rnd.uniform(0.05, 0.35)
        yaw = rnd.uniform(0, 2 * math.pi); pitch = math.radians(rnd.uniform(-25, 25))
        geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=r * 0.9, depth=L)
        dv = Vector((math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), math.sin(pitch)))
        q = dv.to_track_quat('Z', 'Y')
        bmesh.ops.rotate(bm, verts=geom['verts'], cent=Vector((0, 0, 0)), matrix=q.to_matrix())
        bmesh.ops.translate(bm, vec=Vector((x0 + math.cos(a) * d, y0 + math.sin(a) * d, z0 + z)), verts=geom['verts'])
    for f in bm.faces:
        for loop in f.loops:
            co = loop.vert.co
            loop[uv].uv = (co.x + co.y, co.z)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(assets.pbr(bpy, p.get('texture', 'pine_bark'), '1k', coords='uv', tint='#0D0B0A', tint_mix=0.8))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    # embers: small glowing chips in the heart of the heap
    em = dict(shape='scatter', material='glow', color='#FF5A14', emit=p.get('ember', 30.0), count=p.get('embers', 140),
              radius=[0.008, 0.025], seed=p.get('seed', 1), position=[x0, y0, z0],
              **{'in': [-R * 0.55, -R * 0.55, 0.0, R * 0.55, R * 0.55, 0.25]})
    return [ob] + kit.piece(bpy, name + '-embers', em)


def ribbon(bpy, name, p, kit):
    """A ribbon of smoke (incense, a cigar, a sculpted studio column): each of `strands` a scattering volume inside a
    tube along a smooth curve through its `points` (world metres), `radii` one per point (or one), `density` per metre
    at its core. Each strand is `layers` nested tubes, so the density steps up toward the core instead of stopping at a
    hard wall; noise (`scale` metres, `cut`, `soft`, stretched upward by `rise`) tears the wider parts into curls,
    `laminar` metres from each strand's start stay smooth (the unbroken thread above an incense stick). It thins out
    between `fade` [z0, z1] (world z). `wobble` pushes each layer's wall in and out by that share of its radius (at
    `wobble_freq` per metre), so the outline is ragged, not a hose; `break_scale` metres of broad noise (above
    `break_cut`, never below `break_floor`) thins and thickens it along its length; `fade_in` [z0, z1] lets it
    thicken from nothing (a studio column whose source is unseen). `grid` fills a voxel grid from each tube (`voxel`
    metres) instead of shading inside the mesh. `color`, `anisotropy` as
    woodsmoke's."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#D8D8DA'))
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.6)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.0, 1.0, 1.0 / p.get('rise', 2.0))
    mp.inputs['Location'].default_value = (p.get('seed', 0) * 13.7, p.get('seed', 0) * 7.1, 0.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / p.get('scale', 0.05)
    nz.inputs['Detail'].default_value = p.get('detail', 4.0)
    nz.inputs['Distortion'].default_value = p.get('distortion', 0.6)
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cut = p.get('cut', 0.4); soft = p.get('soft', 0.25)
    cr.elements[0].position = cut; cr.elements[0].color = (0, 0, 0, 1)
    cr.elements[1].position = min(0.999, cut + soft); cr.elements[1].color = (1, 1, 1, 1)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    # the laminar thread: no noise for its first metres (z above the strand's start, carried in the object's origin)
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    lam = nt.nodes.new('ShaderNodeMapRange'); lam.clamp = True
    lam.inputs['From Min'].default_value = p.get('laminar', 0.0)
    lam.inputs['From Max'].default_value = p.get('laminar', 0.0) + p.get('laminar_blend', 0.12)
    nt.links.new(sep.outputs['Z'], lam.inputs['Value'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'FLOAT'
    nt.links.new(lam.outputs['Result'], mix.inputs['Factor'])
    mix.inputs['A'].default_value = 1.0
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(ramp.outputs['Color'], bw.inputs['Color'])
    nt.links.new(bw.outputs['Val'], mix.inputs['B'])
    # the fade toward the top, in world z
    gz = nt.nodes.new('ShaderNodeNewGeometry')
    wz = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(gz.outputs['Position'], wz.inputs['Vector'])
    fd = nt.nodes.new('ShaderNodeMapRange'); fd.clamp = True
    z0, z1 = p.get('fade', [10.0, 11.0])
    fd.inputs['From Min'].default_value = z0; fd.inputs['From Max'].default_value = z1
    fd.inputs['To Min'].default_value = 1.0; fd.inputs['To Max'].default_value = 0.0
    nt.links.new(wz.outputs['Z'], fd.inputs['Value'])
    m1 = nt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'
    nt.links.new(mix.outputs['Result'], m1.inputs[0]); nt.links.new(fd.outputs['Result'], m1.inputs[1])
    if p.get('fade_in'):
        # thickening from nothing between fade_in [z0, z1] (world z): a column whose source is unseen
        fi = nt.nodes.new('ShaderNodeMapRange'); fi.clamp = True
        fi.inputs['From Min'].default_value, fi.inputs['From Max'].default_value = p['fade_in']
        nt.links.new(wz.outputs['Z'], fi.inputs['Value'])
        mi = nt.nodes.new('ShaderNodeMath'); mi.operation = 'MULTIPLY'
        nt.links.new(m1.outputs[0], mi.inputs[0]); nt.links.new(fi.outputs['Result'], mi.inputs[1])
        m1 = mi
    if p.get('break_scale'):
        # thinning and thickening along the strand: a broad noise in world space, so the ribbon breaks into wisps
        bz = nt.nodes.new('ShaderNodeTexNoise'); bz.inputs['Scale'].default_value = 1.0 / p['break_scale']
        bz.inputs['Detail'].default_value = 2.0
        sh = nt.nodes.new('ShaderNodeVectorMath'); sh.operation = 'ADD'
        sh.inputs[1].default_value = (p.get('seed', 0) * 3.7, p.get('seed', 0) * 1.9, 0.0)
        nt.links.new(gz.outputs['Position'], sh.inputs[0]); nt.links.new(sh.outputs['Vector'], bz.inputs['Vector'])
        br = nt.nodes.new('ShaderNodeMapRange'); br.clamp = True
        br.inputs['From Min'].default_value = p.get('break_cut', 0.4)
        br.inputs['From Max'].default_value = p.get('break_cut', 0.4) + 0.25
        br.inputs['To Min'].default_value = p.get('break_floor', 0.15)
        nt.links.new(bz.outputs['Fac'], br.inputs['Value'])
        mb = nt.nodes.new('ShaderNodeMath'); mb.operation = 'MULTIPLY'
        nt.links.new(m1.outputs[0], mb.inputs[0]); nt.links.new(br.outputs['Result'], mb.inputs[1])
        m1 = mb
    # each layer's density per metre rides on its object's colour alpha (x 100), so one material serves every layer
    dn = nt.nodes.new('ShaderNodeObjectInfo')
    m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
    nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(dn.outputs['Alpha'], m2.inputs[1])
    m3 = nt.nodes.new('ShaderNodeMath'); m3.operation = 'MULTIPLY'; m3.inputs[1].default_value = 100.0
    nt.links.new(m2.outputs[0], m3.inputs[0])
    nt.links.new(m3.outputs[0], vol.inputs['Density'])
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])

    obs = []
    layers = p.get('layers', 3)
    for si, s in enumerate(p['strands']):
        pts = [Vector(v) for v in s['points']]
        o = pts[0].copy()
        radii = s.get('radii', p.get('radius', 0.01))
        radii = radii if isinstance(radii, (list, tuple)) else [radii] * len(pts)
        for li in range(layers):
            f = 1.0 - li / layers
            bm = bmesh.new()
            kit._tube(bm, [tuple(v - o) for v in pts], [r * f for r in radii], 1.0, 0.0, 12, p.get('res', 10))
            wob = p.get('wobble', 0.0)
            if wob:
                bm.verts.index_update()
                # an irregular outline: each layer's wall pushed in and out by noise, scaled to the local radius
                nring = len(bm.verts) // 12
                for v in bm.verts:
                    t = min(1.0, (v.index // 12) / max(1, nring - 1))
                    x = t * (len(radii) - 1); i = min(int(x), len(radii) - 2); fr = x - i
                    r = (radii[i] * (1 - fr) + radii[i + 1] * fr) * f
                    v.co += noise.noise_vector(v.co * p.get('wobble_freq', 12.0) + Vector((si * 3.1, li * 5.3, p.get('seed', 0)))) * r * wob
            me = bpy.data.meshes.new(f'{name}-{si}-{li}'); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new(f'{name}-{si}-{li}', me); bpy.context.scene.collection.objects.link(ob)
            ob.location = o
            # density per metre at this layer: the core's share, carried in the object's colour alpha (x 100)
            ob.color = (1, 1, 1, s.get('density', p.get('density', 40.0)) / layers / 100.0)
            if p.get('grid'):
                # as a voxel grid (a Volume object filled from the tube): no mesh walls for a ray to cross, so nothing
                # behind the smoke is seen through a mis-tracked volume boundary (a surface behind showed lit)
                ob.hide_render = True; ob.hide_viewport = True
                vd = bpy.data.volumes.new(f'{name}-{si}-{li}-grid')
                vo = bpy.data.objects.new(f'{name}-{si}-{li}-grid', vd); bpy.context.scene.collection.objects.link(vo)
                md = vo.modifiers.new('fill', 'MESH_TO_VOLUME'); md.object = ob
                md.resolution_mode = 'VOXEL_SIZE'; md.voxel_size = p.get('voxel', 0.01); md.density = 1.0
                vo.color = ob.color
                vd.materials.append(m)
                obs.append(vo)
                continue
            me.materials.append(m)
            obs.append(ob)
    return obs


def occluder(bpy, name, p, kit):
    """A disc that only casts shadow: unseen by the camera, in reflections and through glass, it blocks the sky over the
    ground under the speaker so the floor darkens where the cabinet meets it (its contact shadow), as the cabinet's
    clear acrylic base does not. `radius`, `position` (its centre), `segments`."""
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=p.get('segments', 32), radius=p.get('radius', 0.4))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0.05]))
    ob.scale = Vector((p.get('sx', 1.0), p.get('sy', 1.0), 1.0))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
    b.inputs['Roughness'].default_value = 1.0
    me.materials.append(m)
    ob.visible_camera = False; ob.visible_glossy = False; ob.visible_transmission = False
    ob.visible_volume_scatter = False
    return [ob]


def ridge(bpy, name, p, kit):
    """A distant fold of land: a strip `width` metres wide and `depth` deep at `position` [x, y], its crest rising
    `height` [min, max] metres along a noise profile (`scale` metres a swell, `seed`), falling away behind; matte in
    `color`, a touch lighter and bluer the further it stands (aerial perspective is the set's haze). `gullies` metres of
    ridged noise cut into it (`gully_scale` metres apart) give a near fold its relief."""
    w = p.get('width', 3000.0); d = p.get('depth', 80.0)
    h0, h1 = p.get('height', [10.0, 30.0]); sc = p.get('scale', 300.0); sd = p.get('seed', 1) * 17.3
    nx, ny = p.get('cells', [600, 8])
    bm = bmesh.new()
    rows = []
    for j in range(ny + 1):
        fy = j / ny
        row = []
        for i in range(nx + 1):
            x = -w / 2 + w * i / nx
            n = 0.5 + 0.5 * noise.noise(Vector((x / sc + sd, sd, 0.0)))
            n2 = 0.5 + 0.5 * noise.noise(Vector((x / (sc * 0.25) + sd, sd + 3.0, 0.0)))
            crest = h0 + (h1 - h0) * (0.8 * n + 0.2 * n2)
            if p.get('gullies'):
                # gullies and rock: a fine ridged noise cut into the slope, deepest on the face toward the camera
                g = 1.0 - abs(noise.noise(Vector((x / p.get('gully_scale', 18.0) + sd, sd + 7.0, fy * 3.0))))
                crest -= p['gullies'] * g ** 3
            # a rounded profile: up from the front edge to the crest at a third of the depth, down behind
            prof = math.sin(math.pi * min(1.0, fy / 0.35) / 2) if fy < 0.35 else max(0.0, 1.0 - (fy - 0.35) / 0.65 * 0.6)
            row.append(bm.verts.new((x, -d / 2 + d * fy, crest * prof - 1.0)))
        rows.append(row)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    x, y = p.get('position', [0.0, 300.0])[:2]
    ob.location = Vector((x, y, 0.0))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    # mottled scrub and bare earth: two tones by noise
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 1.0 / p.get('mottle', 12.0); nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    r = nt.nodes.new('ShaderNodeValToRGB'); cr = r.color_ramp
    cr.elements[0].position = 0.4; cr.elements[0].color = kit.M.hex_lin(p.get('color2', '#4E4A44'))
    cr.elements[1].position = 0.6; cr.elements[1].color = kit.M.hex_lin(p.get('color', '#7A766F'))
    nt.links.new(nz.outputs['Fac'], r.inputs['Fac']); nt.links.new(r.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.95
    me.materials.append(m)
    return [ob]
