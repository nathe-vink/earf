"""EARF's packaging, path-traced (brand lane, r47): Tropos's crate and horn case, Hemisphere's drums and Core's box.

    python3.11 pack_render.py --shot pair|open|lamps [--samples 128] [--scale 1] [--out out/pack-pair.png]

Built from primitives in metres; the printed faces are the decals that shoot.cjs makes from scenes/decal-*.html
(transparent PNGs), laid over the birch or the board as ink. Sizes are proposals (README, "Packaging"):
- the crate: 720 W x 600 D x 1160 H, 18 mm birch ply on two 100 mm skids, the door at the front hinged at its foot;
  inside, a charcoal felt lining, foam corner blocks and a birch sled the speaker walks out on, wearing its sleeve;
- the horn case: 1420 x 560 x 460, both horns of a pair, ply with a lid;
- Hemisphere's drum: 260 across, 170 tall, through-dyed board in the shade's tint, the globe debossed in the lid;
- Core's box: a 220 mm cube in through-dyed board, the lid lifted, the ball in a moulded pulp cradle.
"""
import argparse, math, os, sys
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
TINTS = {  # the rendered acrylic (site/img/coins-light.jpg), for the boards and the sleeve
    'ember': '#C92118', 'dust': '#E06718', 'acid': '#E2AA15', 'poison': '#367424',
    'ice': '#2584BE', 'haze': '#5B3197', 'fog': '#D5DFE0', 'smoke': '#57545F'}


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Punchy'
    sc.view_settings.exposure = -0.9
    sc.cycles.use_denoising = True
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = lin('#D9D4CC')
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.15
    return sc


def node(nt, kind, loc=(0, 0), **inputs):
    n = nt.nodes.new(kind); n.location = loc
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def mat_basic(name, color, rough=0.5, metal=0.0, sheen=0.0, coat=0.0, bump=0.0, bump_scale=200.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = lin(color)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if sheen:
        p.inputs['Sheen Weight'].default_value = sheen; p.inputs['Sheen Roughness'].default_value = 0.5
    if coat:
        p.inputs['Coat Weight'].default_value = coat
    if bump:
        nz = node(nt, 'ShaderNodeTexNoise', (-600, -300), Scale=bump_scale, Detail=8.0)
        b = node(nt, 'ShaderNodeBump', (-300, -300), Strength=bump, Distance=0.002)
        nt.links.new(nz.outputs['Fac'], b.inputs['Height']); nt.links.new(b.outputs['Normal'], p.inputs['Normal'])
    return m


def mat_birch(name, decal=None, ink=None):
    """Birch ply: a pale wood with a long grain, and a decal's ink over it (its own colours, its alpha as the ink)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']; p.inputs['Roughness'].default_value = 0.62
    tc = node(nt, 'ShaderNodeTexCoord', (-1400, 0))
    mp = node(nt, 'ShaderNodeMapping', (-1200, 0)); mp.inputs['Scale'].default_value = (1.0, 1.0, 9.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    wv = node(nt, 'ShaderNodeTexWave', (-1000, 100), Scale=14.0, Distortion=4.0, Detail=6.0)
    wv.wave_type = 'RINGS'
    nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
    ramp = node(nt, 'ShaderNodeValToRGB', (-800, 100))
    ramp.color_ramp.elements[0].color = lin('#D7BF95'); ramp.color_ramp.elements[1].color = lin('#E9D7B4')
    nt.links.new(wv.outputs['Fac'], ramp.inputs['Fac'])
    nz = node(nt, 'ShaderNodeTexNoise', (-1000, -200), Scale=3.0, Detail=4.0)
    mix0 = node(nt, 'ShaderNodeMix', (-550, 0)); mix0.data_type = 'RGBA'; mix0.blend_type = 'MULTIPLY'
    mix0.inputs['Factor'].default_value = 0.08
    nt.links.new(ramp.outputs['Color'], mix0.inputs['A']); nt.links.new(nz.outputs['Color'], mix0.inputs['B'])
    base = mix0.outputs['Result']
    if decal:
        img = bpy.data.images.load(decal)
        ti = node(nt, 'ShaderNodeTexImage', (-600, -400)); ti.image = img; ti.extension = 'CLIP'
        uv = node(nt, 'ShaderNodeUVMap', (-800, -400)); nt.links.new(uv.outputs['UV'], ti.inputs['Vector'])
        mix = node(nt, 'ShaderNodeMix', (-300, 0)); mix.data_type = 'RGBA'
        nt.links.new(ti.outputs['Alpha'], mix.inputs['Factor'])
        nt.links.new(base, mix.inputs['A']); nt.links.new(ti.outputs['Color'], mix.inputs['B'])
        base = mix.outputs['Result']
    nt.links.new(base, p.inputs['Base Color'])
    bp = node(nt, 'ShaderNodeBump', (-300, -500), Strength=0.08, Distance=0.001)
    nt.links.new(wv.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], p.inputs['Normal'])
    return m


def mat_board(name, tint, decal=None, deboss=None):
    """Through-dyed board: the tint all the way through, a fine paper tooth; white print and a debossed globe."""
    m = mat_basic(name, tint, rough=0.78, bump=0.05, bump_scale=900.0)
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    if decal:
        img = bpy.data.images.load(decal)
        ti = node(nt, 'ShaderNodeTexImage', (-600, 300)); ti.image = img; ti.extension = 'CLIP'
        uv = node(nt, 'ShaderNodeUVMap', (-800, 300)); nt.links.new(uv.outputs['UV'], ti.inputs['Vector'])
        mix = node(nt, 'ShaderNodeMix', (-300, 200)); mix.data_type = 'RGBA'
        mix.inputs['A'].default_value = lin(tint)
        nt.links.new(ti.outputs['Alpha'], mix.inputs['Factor']); nt.links.new(ti.outputs['Color'], mix.inputs['B'])
        nt.links.new(mix.outputs['Result'], p.inputs['Base Color'])
    if deboss:   # blind-debossed: the globe's lines a shade deeper in the board's own tint
        img = bpy.data.images.load(deboss)
        ti = node(nt, 'ShaderNodeTexImage', (-600, -600)); ti.image = img; ti.extension = 'CLIP'
        uv = node(nt, 'ShaderNodeUVMap', (-800, -600)); nt.links.new(uv.outputs['UV'], ti.inputs['Vector'])
        mix = node(nt, 'ShaderNodeMix', (-300, -400)); mix.data_type = 'RGBA'
        mix.inputs['A'].default_value = lin(tint)
        mix.inputs['B'].default_value = tuple(c * 0.62 for c in lin(tint)[:3]) + (1.0,)
        nt.links.new(ti.outputs['Color'], mix.inputs['Factor'])
        nt.links.new(mix.outputs['Result'], p.inputs['Base Color'])
    return m


def mat_acrylic(name, tint, frosted=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = lin(tint)
    p.inputs['Transmission Weight'].default_value = 1.0
    p.inputs['IOR'].default_value = 1.49
    p.inputs['Roughness'].default_value = 0.02 + frosted
    if frosted:   # the frosted liner inside the tinted shell: a milky glow
        p.inputs['Subsurface Weight'].default_value = 0.6
        p.inputs['Subsurface Radius'].default_value = (0.02, 0.02, 0.02)
    return m


def box(name, x0, y0, z0, x1, y1, z1, mat, bevel=0.0, uv_face=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object; o.name = name
    o.scale = (x1 - x0, y1 - y0, z1 - z0); bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod = o.modifiers.new('b', 'BEVEL'); mod.width = bevel; mod.segments = 3
    if uv_face:
        project_face_uv(o, uv_face)
    return o


def project_face_uv(o, axis):
    """UVs for a box's printed faces: project along `axis` ('-y' the front, '+x' the side...) onto 0..1 over the box's
    extent, so a decal's sheet fills that face. Only faces whose normal points along `axis` get the decal; the others'
    UVs land outside 0..1, where CLIP leaves no ink."""
    me = o.data
    if not me.uv_layers:
        me.uv_layers.new()
    uvl = me.uv_layers.active.data
    xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
    sign = -1 if axis[0] == '-' else 1; ax = 'xyz'.index(axis[1])
    for poly in me.polygons:
        n = poly.normal[ax] * sign
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            if n < 0.9:
                uvl[li].uv = (5.0, 5.0); continue
            if ax == 1:   # front or back: u along x (mirrored for the back), v up z
                u = (v.x - min(xs)) / (max(xs) - min(xs)); u = u if sign < 0 else 1 - u
            else:          # a side: u along y
                u = (v.y - min(ys)) / (max(ys) - min(ys)); u = u if sign > 0 else 1 - u
            uvl[li].uv = (u, (v.z - min(zs)) / (max(zs) - min(zs)))


def cylinder(name, r, h, loc, mat, verts=96, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(loc[0], loc[1], loc[2] + h / 2))
    o = bpy.context.object; o.name = name; o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if bevel:
        mod = o.modifiers.new('b', 'BEVEL'); mod.width = bevel; mod.segments = 3
    return o


def drum_uv(o, r, h, z0, wall_decal=True):
    """UVs for a drum: the wall unrolled (u round, v up), the lid's top as a disc in 0..1."""
    me = o.data
    if not me.uv_layers:
        me.uv_layers.new()
    uvl = me.uv_layers.active.data
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            if abs(poly.normal.z) > 0.9:
                uvl[li].uv = (v.x / (2 * r) * 1.25 + 0.5, v.y / (2 * r) * 1.25 + 0.5) if poly.normal.z > 0 else (5, 5)
            elif not wall_decal:
                uvl[li].uv = (5, 5)
            else:   # the wrap's start a little left of the face toward the camera (-y), so the name reads first
                a = (math.atan2(v.y, v.x) / (2 * math.pi) - 0.75 + 0.2) % 1.0
                uvl[li].uv = (a, (v.z + h / 2) / h)


def floor_and_wall(color='#CFC8BD', wall=None, wall_y=3.2, rough=0.85):
    m = mat_basic('ground', color, rough=rough, bump=0.02, bump_scale=60.0)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); bpy.context.object.data.materials.append(m)
    # the wall behind: the floor's own colour, or a limewash of its own
    w = mat_basic('wall', wall, rough=0.95, bump=0.15, bump_scale=8.0) if wall else m
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, wall_y, 0), rotation=(math.pi / 2, 0, 0))
    bpy.context.object.data.materials.append(w)


def area(name, loc, target, size, power, color='#FFF6EC'):
    bpy.ops.object.light_add(type='AREA', location=loc)
    lt = bpy.context.object; lt.name = name
    lt.data.shape = 'RECTANGLE' if isinstance(size, tuple) else 'SQUARE'
    if isinstance(size, tuple):
        lt.data.size, lt.data.size_y = size
    else:
        lt.data.size = size
    lt.data.energy = power; lt.data.color = lin(color)[:3]
    d = [target[i] - loc[i] for i in range(3)]
    lt.rotation_euler = (0, 0, 0)
    lt.rotation_mode = 'QUATERNION'
    from mathutils import Vector
    lt.rotation_quaternion = Vector(d).to_track_quat('-Z', 'Y')
    return lt


def camera(loc, target, lens=50, fstop=0.0):
    from mathutils import Vector
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object; c.data.lens = lens
    c.rotation_mode = 'QUATERNION'
    c.rotation_quaternion = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y')
    if fstop:
        c.data.dof.use_dof = True; c.data.dof.focus_distance = (Vector(target) - Vector(loc)).length; c.data.dof.aperture_fstop = fstop
    bpy.context.scene.camera = c


# the crate --------------------------------------------------------------------------------------------------------
W, D, H, T, SK = 0.72, 0.60, 1.16, 0.018, 0.10


def crate(x, y, tint='ember', open_door=False, rot=0.0, name='crate', front_art='decal-crate-front.png'):
    """A crate at (x, y), its door facing -y; rot turns it about its centre (radians). Returns its objects."""
    objs = []
    ply = mat_birch('ply-' + name)
    front = mat_birch('front-' + name, decal=os.path.join(OUT, front_art))
    inside = mat_birch('inside-' + name, decal=os.path.join(OUT, 'decal-crate-inside.png'))
    side = mat_birch('side-' + name, decal=os.path.join(OUT, 'decal-crate-side.png'))
    steel = mat_basic('steel-' + name, '#1E1D1F', rough=0.35, metal=1.0)
    felt = mat_basic('felt-' + name, '#2B2A28', rough=1.0, sheen=0.3, bump=0.3, bump_scale=1500.0)
    z0 = SK
    # skids
    for sx in (-W / 2 + 0.06, W / 2 - 0.10):
        objs.append(box('skid', sx, -D / 2, 0, sx + 0.04, D / 2, SK, ply))
    objs.append(box('base', -W / 2, -D / 2, z0, W / 2, D / 2, z0 + T, ply))
    objs.append(box('top', -W / 2, -D / 2, z0 + H - T, W / 2, D / 2, z0 + H, ply))
    objs.append(box('back', -W / 2, D / 2 - T, z0 + T, W / 2, D / 2, z0 + H - T, ply))
    objs.append(box('left', -W / 2, -D / 2 + T, z0 + T, -W / 2 + T, D / 2 - T, z0 + H - T, side, uv_face='-x'))
    objs.append(box('right', W / 2 - T, -D / 2 + T, z0 + T, W / 2, D / 2 - T, z0 + H - T, side, uv_face='+x'))
    # cleats: a frame round each side panel's outside, and across the back
    c = 0.07
    for sxo, sxi in ((-W / 2 - 0.012, -W / 2), (W / 2, W / 2 + 0.012)):
        objs.append(box('cl', sxo, -D / 2, z0, sxi, -D / 2 + c, z0 + H, ply))
        objs.append(box('cl', sxo, D / 2 - c, z0, sxi, D / 2, z0 + H, ply))
        objs.append(box('cl', sxo, -D / 2 + c, z0, sxi, D / 2 - c, z0 + c, ply))
        objs.append(box('cl', sxo, -D / 2 + c, z0 + H - c, sxi, D / 2 - c, z0 + H, ply))
    # black steel corners at the eight corners
    for cx in (-W / 2 - 0.013, W / 2 - 0.047):
        for cz in (z0 - 0.002, z0 + H - 0.058):
            objs.append(box('corner', cx, -D / 2 - 0.004, cz, cx + 0.06, -D / 2 + 0.06, cz + 0.06, steel, bevel=0.003))
            objs.append(box('corner', cx, D / 2 - 0.06, cz, cx + 0.06, D / 2 + 0.004, cz + 0.06, steel, bevel=0.003))
    # the door
    if not open_door:
        objs.append(box('door', -W / 2, -D / 2, z0, W / 2, -D / 2 + T, z0 + H, front, uv_face='-y'))
        for lz in (z0 + 0.25, z0 + H - 0.25):   # two latches each side
            for lx in (-W / 2 - 0.016, W / 2 + 0.002):
                objs.append(box('latch', lx, -D / 2 - 0.012, lz - 0.04, lx + 0.014, -D / 2 + 0.05, lz + 0.04, steel, bevel=0.002))
    else:
        # down, resting on the floor ahead of the crate: hinged at its foot, its inside face up
        ang = math.asin((z0 + T) / H)
        d = box('door', -W / 2, 0, 0, W / 2, H, T, inside)
        # UVs for its up face: the decal's top at the hinge
        me = d.data; uvl = me.uv_layers.active.data
        for poly in me.polygons:
            for li in poly.loop_indices:
                v = me.vertices[me.loops[li].vertex_index].co
                uvl[li].uv = ((v.x + W / 2) / W, v.y / H) if poly.normal.z > 0.9 else (5, 5)
        # its pivot at the hinge: rotate about x so the far end rests on the floor
        # put the hinge edge (local y = H) at the crate's foot: local (0,H,0) after rotation
        hy = H * math.cos(ang); hz = H * math.sin(ang)
        d.location = (0, -D / 2 - hy, 0.0)
        d.rotation_euler = (ang, 0, 0)
        objs.append(d)
        # the felt lining and the foam corner blocks inside
        objs.append(box('felt-back', -W / 2 + T, D / 2 - T - 0.01, z0 + T, W / 2 - T, D / 2 - T, z0 + H - T, felt))
        objs.append(box('felt-l', -W / 2 + T, -D / 2 + 0.01, z0 + T, -W / 2 + T + 0.01, D / 2 - T, z0 + H - T, felt))
        objs.append(box('felt-r', W / 2 - T - 0.01, -D / 2 + 0.01, z0 + T, W / 2 - T, D / 2 - T, z0 + H - T, felt))
        objs.append(box('felt-top', -W / 2 + T, -D / 2 + 0.01, z0 + H - T - 0.01, W / 2 - T, D / 2 - T, z0 + H - T, felt))
        foam = mat_basic('foam-' + name, '#232223', rough=0.9, bump=0.25, bump_scale=300.0)
        for fx in (-W / 2 + T + 0.01, W / 2 - T - 0.01 - 0.07):
            for fz in (z0 + T + 0.04, z0 + H - T - 0.01 - 0.12):
                objs.append(box('foam', fx, -D / 2 + 0.06, fz, fx + 0.07, D / 2 - T - 0.01, fz + 0.12, foam, bevel=0.004))
        # the sled, and the speaker in its sleeve on it
        objs.append(box('sled', -0.30, -D / 2 + 0.03, z0 + T, 0.30, D / 2 - T - 0.02, z0 + T + 0.03, ply, bevel=0.002))
        sleeve = mat_basic('sleeve-' + name, {'ember': '#7A120C'}.get(tint, TINTS[tint]), rough=0.9, sheen=0.4, bump=0.25, bump_scale=900.0)   # the cotton dyed deeper than the acrylic reads
        sl = box('sleeve', -0.285, -0.215, z0 + T + 0.03, 0.285, 0.215, z0 + T + 0.03 + 0.95, sleeve, bevel=0.045)
        sub = sl.modifiers.new('s', 'SUBSURF'); sub.levels = 4; sub.render_levels = 4; sub.subdivision_type = 'SIMPLE'
        # critic round 1 (5.0): the cloth as cloth. Long vertical folds that fade toward the shoulders, and a loose
        # unevenness over them, so the sleeve hangs rather than stands
        folds = bpy.data.textures.new('folds', 'CLOUDS'); folds.noise_scale = 0.05; folds.noise_depth = 2
        stretch = bpy.data.objects.new('fold-axis', None); bpy.context.collection.objects.link(stretch)
        stretch.scale = (1.0, 1.0, 14.0); stretch.location = sl.location     # the noise drawn out up the sleeve: folds that hang
        d1 = sl.modifiers.new('folds', 'DISPLACE'); d1.texture = folds; d1.strength = 0.03
        d1.texture_coords = 'OBJECT'; d1.texture_coords_object = stretch
        tex = bpy.data.textures.new('wr', 'CLOUDS'); tex.noise_scale = 0.12
        d2 = sl.modifiers.new('d', 'DISPLACE'); d2.texture = tex; d2.strength = 0.01
        bpy.context.view_layer.objects.active = sl; bpy.ops.object.shade_smooth()
        objs.append(sl)
        # the woven label: off-white, the wordmark woven in, stitched at both ends
        art = os.path.join(OUT, 'decal-label.png')
        lab = mat_board('label-' + name, '#EFEBE2', decal=art if os.path.exists(art) else None)
        lb = box('label', -0.04, -0.236, z0 + 0.66, 0.04, -0.231, z0 + 0.69, lab, uv_face='-y')
        objs.append(lb)
    root = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(root)
    for o in objs:
        o.parent = root
    root.location = (x, y, 0); root.rotation_euler = (0, 0, rot)
    return root


def horn_case(x, y, rot=0.0):
    """The horn case: both horns of a pair, side by side face up; a lid with two black steel handles."""
    Wc, Dc, Hc = 1.42, 0.56, 0.46
    ply = mat_birch('ply-case')
    steel = mat_basic('steel-case', '#1E1D1F', rough=0.45, metal=1.0)
    art = os.path.join(OUT, 'decal-case.png')
    front = mat_birch('front-case', decal=art if os.path.exists(art) else None)
    objs = [box('case', -Wc / 2, -Dc / 2, 0.02, Wc / 2, Dc / 2, Hc - 0.06, front, uv_face='-y'),
            box('lid', -Wc / 2 - 0.004, -Dc / 2 - 0.004, Hc - 0.06, Wc / 2 + 0.004, Dc / 2 + 0.004, Hc, ply, bevel=0.002)]
    for hx in (-0.4, 0.4):
        objs.append(box('handle', hx - 0.09, -0.02, Hc, hx + 0.09, 0.02, Hc + 0.03, steel, bevel=0.006))
    for sx in (-Wc / 2 + 0.05, Wc / 2 - 0.09):
        objs.append(box('foot', sx, -Dc / 2 + 0.04, 0, sx + 0.04, Dc / 2 - 0.04, 0.02, ply))
    for cx in (-Wc / 2 - 0.006, Wc / 2 - 0.05):
        for cz in (0.015, Hc - 0.06):
            objs.append(box('corner', cx, -Dc / 2 - 0.006, cz, cx + 0.056, -Dc / 2 + 0.05, cz + 0.05, steel, bevel=0.003))
    root = bpy.data.objects.new('horn-case', None); bpy.context.collection.objects.link(root)
    for o in objs:
        o.parent = root
    root.location = (x, y, 0); root.rotation_euler = (0, 0, rot)
    return root


def drum(x, y, z, tint, name, lid_off=False):
    r, h, lid = 0.13, 0.17, 0.045
    deco = os.path.join(OUT, 'decal-drum.png')
    globe = os.path.join(HERE, '..', 'brand', 'mark', 'earf-globe-white-stroke.png')
    wall = mat_board('drum-' + name, TINTS[tint], decal=deco)
    top = mat_board('lid-' + name, TINTS[tint], deboss=globe)
    o = cylinder('drum-' + name, r, h - lid + 0.004, (x, y, z), wall)
    drum_uv(o, r, h - lid + 0.004, z)
    if not lid_off:
        l = cylinder('lid-' + name, r + 0.003, lid, (x, y, z + h - lid), top, bevel=0.0015)
        drum_uv(l, r + 0.003, lid, z, wall_decal=False)
    return o


def core_box(x, y, tint='ember', rot=0.2):
    s = 0.22
    deco = os.path.join(OUT, 'decal-core.png')
    board = mat_board('core-box', TINTS[tint], decal=deco)
    plain = mat_board('core-lid', TINTS[tint])
    pulp = mat_basic('pulp', '#B9B2A6', rough=0.95, bump=0.4, bump_scale=120.0)
    objs = []
    walls = [box('cb-f', -s / 2, -s / 2, 0, s / 2, -s / 2 + 0.003, s - 0.06, board, uv_face='-y'),
             box('cb-b', -s / 2, s / 2 - 0.003, 0, s / 2, s / 2, s - 0.06, plain),
             box('cb-l', -s / 2, -s / 2 + 0.003, 0, -s / 2 + 0.003, s / 2 - 0.003, s - 0.06, plain),
             box('cb-r', s / 2 - 0.003, -s / 2 + 0.003, 0, s / 2, s / 2 - 0.003, s - 0.06, plain)]
    objs += walls
    objs.append(box('cradle', -s / 2 + 0.004, -s / 2 + 0.004, 0.002, s / 2 - 0.004, s / 2 - 0.004, 0.10, pulp, bevel=0.01))
    # the ball, seated in the cradle: tinted shell over a frosted liner
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=0.08, location=(0, 0, 0.10 + 0.045))
    ball = bpy.context.object; bpy.ops.object.shade_smooth(); ball.data.materials.append(mat_acrylic('ball', TINTS[tint], frosted=0.08))
    objs.append(ball)
    root = bpy.data.objects.new('core-box', None); bpy.context.collection.objects.link(root)
    for o in objs:
        o.parent = root
    root.location = (x, y, 0); root.rotation_euler = (0, 0, rot)
    # the lid, lifted off and leaning against the box's side
    lid = box('cb-lid', -s / 2 - 0.004, -s / 2 - 0.004, 0, s / 2 + 0.004, s / 2 + 0.004, 0.07, board)
    lid.location = (x + 0.30, y + 0.06, 0.0)
    lid.rotation_euler = (0, 0, rot - 0.5)
    return root


def shot_pair(sc):
    # critic rounds 1 and 2 (5.5, 5.5): the hero crate the brightest face, its partner set back and flagged off the key,
    # the case clear of both, a darker floor and wall on a cove, a lower, longer lens
    sc.view_settings.look = 'AgX - Base Contrast'; sc.view_settings.exposure = -0.85
    sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.04
    floor_and_wall(color='#8C857B', wall='#7A7268', wall_y=2.8, rough=0.55)
    crate(-0.35, 0.0, rot=0.14, name='c1')
    crate(0.40, 1.5, rot=-0.26, name='c2', front_art='decal-crate-front-2.png')
    horn_case(1.55, -0.95, rot=-0.30)
    area('key', (-2.6, -2.8, 2.5), (-0.35, 0, 0.7), 1.0, 1000)
    area('fill', (3.4, -2.6, 1.4), (0, 0, 0.6), 3.0, 40, '#EEF2FA')
    area('top', (0, 0.5, 4.5), (0, 0, 0), 3.0, 60)
    flag = mat_basic('flag', '#050505', rough=1.0)
    f = box('flag-wall', -4, 2.2, 2.2, 4, 2.22, 3.4, flag); f.visible_camera = False
    g = box('flag-partner', -1.9, 0.2, 0.8, -1.3, 0.22, 2.0, flag); g.visible_camera = False   # keeps the key off the partner's face
    camera((1.8, -7.6, 0.70), (0.5, 0.2, 0.65), lens=66, fstop=4)


def shot_open(sc):
    # critic rounds 1 and 2 (5.0, 5.0): the red held deep, the felt dark, the door whole in frame and lighter than the
    # floor, a raking key, a warm glow from the crate's ceiling onto the sleeve
    sc.view_settings.look = 'AgX - Base Contrast'; sc.view_settings.exposure = -1.0
    sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.04
    floor_and_wall(color='#9E978C', wall='#8E867B', wall_y=2.2, rough=0.7)
    crate(0.0, 0.3, open_door=True, name='c1')
    area('key', (-2.4, -0.6, 2.4), (0, 0, 0.6), 0.8, 650)
    area('fill', (3.0, -2.2, 1.2), (0, 0, 0.6), 2.6, 30, '#EEF2FA')
    glow = area('glow', (0.0, 0.25, 1.22), (0, 0.25, 0.3), 0.3, 40, '#FFD9B0'); glow.visible_camera = False
    area('top', (0, 0.5, 4.5), (0, 0, 0), 3.0, 50)
    camera((1.1, -4.3, 1.25), (0.0, -0.4, 0.52), lens=52, fstop=4)


def shot_lamps(sc):
    floor_and_wall('#D3CCC1')
    order = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
    for i, t in enumerate(order):    # the eight drums in the spectrum's order, on a shallow arc
        a = (i - 3.5) * 0.235
        drum(1.25 * math.sin(a), 1.25 * (1 - math.cos(a)) + 0.05, 0.0, t, t)
    core_box(0.12, -0.36, tint='ember', rot=0.30)
    area('key', (-1.8, -2.0, 2.0), (0, 0, 0.1), 1.6, 380)
    area('fill', (2.2, -1.4, 0.8), (0, 0, 0.1), 1.8, 90, '#EEF2FA')
    area('top', (0.3, 0.3, 2.6), (0, 0, 0), 2.0, 80)
    camera((0.3, -2.7, 1.0), (0.0, 0.2, 0.12), lens=45, fstop=8)


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--shot', default='pair'); a.add_argument('--samples', type=int, default=128)
    a.add_argument('--scale', type=float, default=1.0); a.add_argument('--out')
    args = a.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    sc = reset()
    {'pair': shot_pair, 'open': shot_open, 'lamps': shot_lamps}[args.shot](sc)
    sc.render.resolution_x, sc.render.resolution_y = int(1800 * args.scale), int(1200 * args.scale)
    sc.cycles.samples = args.samples
    sc.render.filepath = args.out or os.path.join(OUT, f'pack-{args.shot}.png')
    bpy.ops.render.render(write_still=True)
    print('wrote', sc.render.filepath)


if __name__ == '__main__':
    main()
