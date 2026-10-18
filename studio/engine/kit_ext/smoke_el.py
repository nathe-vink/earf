"""Smoke's own pieces (round 31b, spinoffs/barkhorn/elements/smoke.py).

woodsmoke: a drifting bank of woodsmoke as a scattering volume, a box `size` [w, d, h] standing at `position`, its
density `density` per metre carved by noise into wisps and banks (`scale` metres a wisp, `detail`, `cut` the share of
the noise left clear, `soft` how gradually it thickens), thinning toward the box's top and its edges (`fade`), its
colour `color` and its forward scattering `anisotropy` (woodsmoke throws light forward, so a sun behind it makes it
glow). `rise` stretches the wisps upward, `lean` [dx, dy] shears them as the smoke drifts. `seed` moves the noise.
"""
import math

import bmesh
from mathutils import Vector


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
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cut = p.get('cut', 0.5); soft = p.get('soft', 0.18)
    cr.elements[0].position = cut; cr.elements[0].color = (0, 0, 0, 1)
    cr.elements[1].position = min(0.999, cut + soft); cr.elements[1].color = (1, 1, 1, 1)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
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
    nt.links.new(m5.outputs[0], vol.inputs['Density'])
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
                                   bump=p.get('bump', 1.0), coords='uv', tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0)))
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
