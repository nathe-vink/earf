"""The laminated lamps pictured as real objects (the design pass of 2026-10-31): Blender Cycles, run on the system
Python (bpy 5.0).

    python3.11 spinoffs/barkhorn/companions/strata/scene.py SHOT [--scale S] [--samples N] [--out PATH]

What makes the acrylic real here, and why:
- **One object a stack.** The bonded layers are optically one piece (the cement's index matches the sheet's), so the
  render builds each lamp's acrylic as one mesh, revolved from stack.py's layers (the same numbers as the CAD).
  Separate touching solids would render black where their faces meet, and would break the caustics.
- **Calibrated tint: Beer-Lambert by ray length.** Each tint's absorption per channel is worked from A&C's TruCast
  chart (stack.TINTS: transmission at 3 mm, hue from the stand-in colour). The glass is clear where light enters; where
  a ray leaves (it meets the surface from inside), its colour is exp(-a x the length it travelled inside). That is
  exact for any path, camera or light, and Cycles' manifold next-event estimation (MNEE) carries it into the shadow
  caustics (tested 2026-10-31: a volume absorption, by contrast, is ignored by MNEE and throws a white caustic).
- **IOR 1.49.** Surfaces by how they're made: turned and buffed (0.0 roughness, faint swirl marks), the sheet's own cast
  face (0.0), bead-blasted (0.38, rough transmission), fly-cut (0.12, tool marks). Edges broken 0.4 mm.
- **Bond lines** at every layer joint: a hairline, faintly milky where the cement met the polished edge.
- **Faint wear:** hairline scratches on the polished faces, kept subtle.
- **Light:** each LED is a Cycles light flagged as a caustics light, so its light reaches the table through the acrylic as
  real refracted caustics; the visible glow (the opal tube, the COB) is an emitter seen only along mirror paths.
- **A real lens:** 85 mm, f/2.8 to f/4, focus on the lamp; filmic (AgX) tone.
"""
import argparse, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import bpy, bmesh                                                    # noqa: E402
import stack as S                                                    # noqa: E402

MM = 0.001


def hex_lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def absorption(tint, loading=1.0):
    """Per-channel absorption, 1/m, of a TruCast stand-in: its hue scaled so the luminance it passes at 3 mm (after the
    two faces' 8 % reflection) is the chart's figure. `loading` scales the dye (0.25: a quarter-strength custom pour)."""
    code, lt, hue = S.TINTS[tint]
    c = hex_lin(hue)
    y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    k = (lt / 100.0 / 0.92) / y
    T = [min(max(x * k, 1e-4), 0.995) for x in c]
    return [-math.log(t) / 0.003 * loading for t in T]


# --- the acrylic ----------------------------------------------------------------------------------------------------
def profile(L):
    """The stack's outline in (r, z), going up the outside and down the inside, each edge tagged with how it's made."""
    pts, tags = [], []
    out = []
    for l in L:
        out += [(l['ro'], l['z0']), (l['ro'], l['z1'])]
    inner = []
    for l in reversed(L):
        inner += [(l['ri'], l['z1']), (l['ri'], l['z0'])]
    chain = out + inner
    # drop repeats
    for p in chain:
        if not pts or abs(p[0] - pts[-1][0]) > 1e-6 or abs(p[1] - pts[-1][1]) > 1e-6:
            pts.append(p)
    if abs(pts[0][0] - pts[-1][0]) < 1e-6 and abs(pts[0][1] - pts[-1][1]) < 1e-6:
        pts.pop()
    zmin, zmax = L[0]['z0'], L[-1]['z1']
    n_out = len(out)
    for i in range(len(pts)):
        (r0, z0), (r1, z1) = pts[i], pts[(i + 1) % len(pts)]
        outer = i < n_out - 1 and pts[i] in out and pts[(i + 1) % len(pts)] in out
        if abs(r1 - r0) < 1e-6:
            if outer:
                k = next((j for j, l in enumerate(L) if abs(l['z0'] - min(z0, z1)) < 1e-6), 0)
                tags.append('side-s' if L[k].get('finish') == 's' else 'side')
            else:
                k = next((j for j, l in enumerate(L) if abs(l['z0'] - min(z0, z1)) < 1e-6), 0)
                tags.append('bore-s' if L[k].get('finish') == 's' and L[k].get('tint') == 'Clear' else 'bore')
        elif abs(z1 - z0) < 1e-6:
            if abs(z0 - zmin) < 1e-6:
                tags.append('bottom')
            elif abs(z0 - zmax) < 1e-6:
                tags.append('top')
            else:
                tags.append('tread' if outer else 'inner_tread')
        else:
            tags.append('side')
    return pts, tags


def revolve(name, L, zones, segs=192, bevel=0.4):
    """One mesh revolved from the stack's outline, a material slot per zone (zones: {tag: material})."""
    pts, tags = profile(L)
    names = list(dict.fromkeys(zones[t] for t in tags))
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for (r, z) in pts:
        ring = []
        for j in range(segs):
            a = 2 * math.pi * j / segs
            ring.append(bm.verts.new((r * math.cos(a) * MM, r * math.sin(a) * MM, z * MM)))
        rings.append(ring)
    n = len(pts)
    for i in range(n):
        A, B = rings[i], rings[(i + 1) % n]
        mi = names.index(zones[tags[i]])
        for j in range(segs):
            q = (A[j], A[(j + 1) % segs], B[(j + 1) % segs], B[j])
            try:
                f = bm.faces.new(q)
                f.material_index = mi
                f.smooth = True
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    for nm in names:
        me.materials.append(bpy.data.materials[nm])
    # profile corners sharp, round the axis smooth; the arrises broken
    for e in me.edges:
        pass
    mod = ob.modifiers.new('arris', 'BEVEL'); mod.width = bevel * MM; mod.segments = 2; mod.limit_method = 'ANGLE'
    mod.angle_limit = math.radians(40); mod.harden_normals = False
    sm = ob.modifiers.new('smooth', 'NODES') if False else None
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    try:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    except Exception:
        pass
    ob.select_set(False)
    ob.cycles.is_caustics_caster = True
    return ob


def acrylic_material(name, layers, rough, kind='polished', loading=1.0, scratch=1.0, bond=True):
    """Clear cast acrylic, IOR 1.49, tinted by ray length (see the module's notes). `layers` [(z0, z1, tint)] in mm:
    the tint of a ray leaving through a face is the layer's where it leaves (a radial path stays in its layer)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial')
    glass = N('ShaderNodeBsdfGlass'); glass.inputs['IOR'].default_value = 1.49
    glass.distribution = 'MULTI_GGX'
    lp = N('ShaderNodeLightPath'); geo = N('ShaderNodeNewGeometry'); tc = N('ShaderNodeTexCoord')
    sep = N('ShaderNodeSeparateXYZ'); Lk(tc.outputs['Object'], sep.inputs[0])
    zmm = N('ShaderNodeMath'); zmm.operation = 'MULTIPLY'; zmm.inputs[1].default_value = 1000.0
    Lk(sep.outputs['Z'], zmm.inputs[0])

    def const(v):
        c = N('ShaderNodeValue'); c.outputs[0].default_value = v
        return c.outputs[0]

    def math_(op, a, b=None):
        n = N('ShaderNodeMath'); n.operation = op
        for i, x in enumerate((a, b)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = x
            else:
                Lk(x, n.inputs[i])
        return n.outputs[0]

    # the absorption at the exit point's layer: a per-channel step function of z
    chans = []
    for ch in range(3):
        acc = None
        prev = None
        for (z0, z1, tint) in layers:
            a = absorption(tint, loading)[ch]
            if acc is None:
                acc = const(a); prev = a
            else:
                # step up to this layer's value above z0
                step = math_('GREATER_THAN', zmm.outputs[0], z0 - 1e-3)
                acc = math_('ADD', acc, math_('MULTIPLY', step, a - prev)); prev = a
        chans.append(acc)
    comb = N('ShaderNodeCombineColor')
    for ch, nm in enumerate(('Red', 'Green', 'Blue')):
        e = math_('EXPONENT', math_('MULTIPLY', math_('MULTIPLY', lp.outputs['Ray Length'], -1.0), chans[ch]))
        Lk(e, comb.inputs[nm])
    mix = N('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['A'].default_value = (1, 1, 1, 1)
    Lk(comb.outputs[0], mix.inputs['B']); Lk(geo.outputs['Backfacing'], mix.inputs['Factor'])
    Lk(mix.outputs['Result'], glass.inputs['Color'])
    # roughness: the finish, with faint wear (hairline scratches: a stretched noise, very sparse) on polished faces
    r = const(rough)
    if kind in ('polished', 'cast') and scratch > 0:
        nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900.0; nz.inputs['Detail'].default_value = 2.0
        mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 40.0, 1.0)
        mp.inputs['Rotation'].default_value = (0.3, 0.5, 0.9)
        Lk(tc.outputs['Object'], mp.inputs['Vector']); Lk(mp.outputs['Vector'], nz.inputs['Vector'])
        sc = N('ShaderNodeMapRange'); sc.inputs['From Min'].default_value = 0.72; sc.inputs['From Max'].default_value = 0.78
        sc.inputs['To Max'].default_value = 0.10 * scratch
        Lk(nz.outputs['Fac'], sc.inputs['Value'])
        r = math_('ADD', r, sc.outputs['Result'])
    if kind == 'turned':
        # faint concentric tool marks on a fly-cut face
        rr = math_('SQRT', math_('ADD', math_('POWER', sep.outputs['X'], 2.0), math_('POWER', sep.outputs['Y'], 2.0)))
        w = N('ShaderNodeTexWave'); w.wave_type = 'RINGS'; w.inputs['Scale'].default_value = 2.0
        Lk(tc.outputs['Object'], w.inputs['Vector'])
        r = math_('ADD', r, math_('MULTIPLY', w.outputs['Fac'], 0.06))
    if bond:
        # the bond lines: within 0.06 mm of a layer joint, a hairline of milky scatter, kept inside the one glass BSDF
        # (a mixed-in translucent shader stops Cycles' MNEE treating the acrylic as a caustic caster)
        frac = math_('FRACT', math_('DIVIDE', math_('SUBTRACT', zmm.outputs[0], layers[0][0]), S.T))
        d = math_('MINIMUM', frac, math_('SUBTRACT', 1.0, frac))
        line = math_('LESS_THAN', math_('MULTIPLY', d, S.T), 0.06)
        top = math_('LESS_THAN', zmm.outputs[0], layers[-1][1] - 0.2)
        bot = math_('GREATER_THAN', zmm.outputs[0], layers[0][0] + 0.2)
        line = math_('MULTIPLY', math_('MULTIPLY', line, top), bot)
        r = math_('ADD', r, math_('MULTIPLY', line, 0.35))
        dim = N('ShaderNodeMix'); dim.data_type = 'RGBA'; dim.inputs['B'].default_value = (0.86, 0.86, 0.85, 1)
        Lk(line, dim.inputs['Factor']); Lk(mix.outputs['Result'], dim.inputs['A'])
        Lk(dim.outputs['Result'], glass.inputs['Color'])
    Lk(r, glass.inputs['Roughness'])
    shader = glass.outputs[0]
    Lk(shader, out.inputs['Surface'])
    return m


def principled(name, color, rough, metallic=0.0, aniso=0.0, coat=0.0, bump=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*hex_lin(color), 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metallic
    if aniso:
        b.inputs['Anisotropic'].default_value = aniso
    if coat:
        b.inputs['Coat Weight'].default_value = coat
    if bump:
        nt = m.node_tree
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = bump[0]
        bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = bump[1]; bn.inputs['Distance'].default_value = 0.0002
        nt.links.new(nz.outputs['Fac'], bn.inputs['Height']); nt.links.new(bn.outputs['Normal'], b.inputs['Normal'])
    return m


def anodised(name='anodised', color='#232326'):
    """Black anodised 6061, bead-blasted first: a fine satin with a faint grain."""
    return principled(name, color, 0.42, metallic=0.85, bump=(4000.0, 0.15))


def emitter(name, color, strength, mirror_only=True):
    """A glow seen by the camera (and in mirrors and through the acrylic) but lighting nothing: the light it stands for
    is a Cycles light beside it."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*hex_lin(color), 1); em.inputs['Strength'].default_value = strength
    if mirror_only:
        lp = nt.nodes.new('ShaderNodeLightPath')
        eq = nt.nodes.new('ShaderNodeMath'); eq.operation = 'LESS_THAN'; eq.inputs[1].default_value = 0.5
        nt.links.new(lp.outputs['Diffuse Depth'], eq.inputs[0])
        mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = strength
        nt.links.new(eq.outputs[0], mul.inputs[0]); nt.links.new(mul.outputs[0], em.inputs['Strength'])
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    return m


def stl(path, mat, name=None):
    bpy.ops.wm.stl_import(filepath=path, global_scale=MM)
    ob = bpy.context.selected_objects[0]
    if name:
        ob.name = name
    ob.data.materials.clear(); ob.data.materials.append(mat)
    try:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(30))
    except Exception:
        pass
    ob.select_set(False)
    return ob


def point(name, loc, watts, color, radius=0.004, caustic=True, glossy=False):
    ld = bpy.data.lights.new(name, 'POINT'); ld.energy = watts; ld.color = hex_lin(color)
    ld.shadow_soft_size = radius
    ld.cycles.is_caustics_light = caustic
    ob = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.visible_glossy = glossy
    return ob


def area(name, loc, rot_deg, size, watts, color, spread=180.0, caustic=False, camera=False):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = watts; ld.color = hex_lin(color)
    ld.shape = 'RECTANGLE'; ld.size, ld.size_y = size
    ld.spread = math.radians(spread)
    ld.cycles.is_caustics_light = caustic
    ob = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = [math.radians(a) for a in rot_deg]
    ob.visible_camera = camera
    return ob


def sun(name, direction, strength, color, angle=0.53, caustic=True, dist=15.0, at=(0.0, 0.0, 0.7)):
    """Sunlight travelling along `direction` (x, y, z), `strength` W/m2 at the scene. Cycles' MNEE shadow caustics take
    no sun lamp, so the sun is a small point light `dist` metres off (its disc `angle` degrees across, as the sun's),
    its power set so its irradiance at `at` is `strength`."""
    from mathutils import Vector
    d = Vector(direction).normalized()
    ld = bpy.data.lights.new(name, 'POINT'); ld.color = hex_lin(color)
    ld.energy = strength * 4 * math.pi * dist * dist
    ld.shadow_soft_size = dist * math.tan(math.radians(angle) / 2)
    ld.cycles.is_caustics_light = caustic
    ob = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(at) - d * dist
    return ob


def sun_lamp(name, direction, strength, color, angle=0.53, caustic=True):
    """A sun whose light travels along `direction` (x, y, z)."""
    from mathutils import Vector
    ld = bpy.data.lights.new(name, 'SUN'); ld.energy = strength; ld.color = hex_lin(color); ld.angle = math.radians(angle)
    ld.cycles.is_caustics_light = caustic
    ob = bpy.data.objects.new(name, ld); bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = Vector(direction).normalized().to_track_quat('-Z', 'Y').to_euler()
    return ob


# --- the room ----------------------------------------------------------------------------------------------------------
def plane(name, size, loc, rot_deg, mat, receiver=True):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    ob = bpy.context.object; ob.name = name
    ob.scale = (size[0], size[1], 1); ob.rotation_euler = [math.radians(a) for a in rot_deg]
    ob.data.materials.append(mat)
    ob.cycles.is_caustics_receiver = receiver
    ob.select_set(False)
    return ob


def box_ob(name, x0, y0, z0, x1, y1, z1, mat, receiver=True, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    ob = bpy.context.object; ob.name = name
    ob.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(mat)
    if bevel:
        md = ob.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 3
    ob.cycles.is_caustics_receiver = receiver
    ob.select_set(False)
    return ob


def window_gobo(x, y0, y1, z0, z1, panes=(2, 3), bar=0.045):
    """A window's frame out of frame, so daylight falls in through panes, its bars' shadows on the wall and table."""
    mat = principled('gobo', '#202020', 0.9)
    obs = []
    nx, nz = panes
    for i in range(nx + 1):
        y = y0 + (y1 - y0) * i / nx
        obs.append(box_ob(f'mullion{i}', x - 0.03, y - bar / 2, z0, x + 0.03, y + bar / 2, z1, mat, receiver=False))
    for j in range(nz + 1):
        z = z0 + (z1 - z0) * j / nz
        obs.append(box_ob(f'transom{j}', x - 0.03, y0, z - bar / 2, x + 0.03, y1, z + bar / 2, mat, receiver=False))
    # the wall the window sits in
    big = 3.0
    obs.append(box_ob('wall-l-a', x - 0.1, y0 - big, -1, x, y0, 4, mat, receiver=False))
    obs.append(box_ob('wall-l-b', x - 0.1, y1, -1, x, y1 + big, 4, mat, receiver=False))
    obs.append(box_ob('wall-l-c', x - 0.1, y0, -1, x, y1, z0, mat, receiver=False))
    obs.append(box_ob('wall-l-d', x - 0.1, y0, z1, x, y1, 4, mat, receiver=False))
    for o in obs:
        o.visible_camera = False
    return obs


def world(hdri=None, strength=0.3, rotation=0.0, color='#101014'):
    w = bpy.data.worlds.new('world'); bpy.context.scene.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes['Background']; bg.inputs['Strength'].default_value = strength
    if hdri:
        import assets
        env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(assets.hdri(hdri, '1k'))
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0, 0, math.radians(rotation))
        tc = nt.nodes.new('ShaderNodeTexCoord')
        nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
        nt.links.new(env.outputs['Color'], bg.inputs['Color'])
    else:
        bg.inputs['Color'].default_value = (*hex_lin(color), 1)


def camera(loc, target, lens=85.0, fstop=2.8, focus=None, sensor=36.0):
    cd = bpy.data.cameras.new('cam'); cd.lens = lens; cd.sensor_width = sensor
    ob = bpy.data.objects.new('cam', cd); bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    d = [target[i] - loc[i] for i in range(3)]
    ob.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    f = focus or target
    cd.dof.focus_distance = math.dist(loc, f)
    bpy.context.scene.camera = ob
    return ob


def render_settings(W, H, samples, scale, exposure=0.0, look='None'):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.cycles.samples = samples; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.01
    sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.max_bounces = 24; sc.cycles.transmission_bounces = 24; sc.cycles.glossy_bounces = 8
    sc.cycles.diffuse_bounces = 4; sc.cycles.transparent_max_bounces = 16
    # refractive caustics on: Cycles' MNEE shadow caustics run only with them (tested 2026-10-31); filter_glossy keeps
    # the brute-force part of them quiet
    sc.cycles.caustics_refractive = True; sc.cycles.caustics_reflective = False; sc.cycles.blur_glossy = 1.0
    sc.cycles.sample_clamp_indirect = 8.0
    sc.render.resolution_x = int(W * scale); sc.render.resolution_y = int(H * scale)
    sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'AgX'
    try:
        sc.view_settings.look = look
    except TypeError:
        pass
    sc.view_settings.exposure = exposure
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '8'


# --- the lamps -----------------------------------------------------------------------------------------------------
def core_sample(stackmix=None, lit=True, glow=1.0, base=(0.0, 0.0, 0.0), loading=1.0):
    """Core Sample at `base` (m): the column, the foot from its CAD, the filament lit or not."""
    P = dict(S.CS)
    if stackmix:
        P['stack'] = stackmix
    L = S.core_sample(P)
    lay = [(l['z0'], l['z1'], l['tint']) for l in L]
    mats = {
        'side': acrylic_material('cs-side', lay, 0.0, 'polished', loading),
        'side-s': acrylic_material('cs-satin', lay, 0.42, 'blasted', loading),
        'top': acrylic_material('cs-top', lay, 0.0, 'polished', loading, bond=False),
        'bore': acrylic_material('cs-bore', lay, 0.02, 'polished', loading, scratch=0.0),
        'bore-s': acrylic_material('cs-bore-satin', lay, 0.45, 'blasted', loading, scratch=0.0),
        'bottom': acrylic_material('cs-bottom', lay, 0.12, 'turned', loading, bond=False),
    }
    zones = {'side': 'cs-side', 'side-s': 'cs-satin', 'top': 'cs-top', 'bore': 'cs-bore', 'bore-s': 'cs-bore-satin', 'inner_tread': 'cs-bore', 'bottom': 'cs-bottom',
             'tread': 'cs-side'}
    col = revolve('column', L, zones, segs=256)
    out = os.path.join(HERE, 'out-core-sample', 'stl')
    an = anodised()
    obs = [col]
    for nm, mat in (('foot', an), ('cover', an), ('knob', principled('steel', '#C9C9C6', 0.22, 1.0, bump=(2500.0, 0.6))),
                    ('jack', principled('nickel', '#B9B6AE', 0.3, 1.0)), ('bumpers', principled('rubber', '#141414', 0.7))):
        obs.append(stl(os.path.join(out, f'{nm}.stl'), mat, nm))
    # the filament: the opal tube, glowing to the eye; the light it gives, five lights up its axis
    # the opal tube is the light: an emitter for every ray (its light reaches the table through the bore's and the
    # skin's polished faces as path-traced refractive caustics; MNEE did not converge on an upright cylinder here)
    tube = stl(os.path.join(out, 'tube.stl'), emitter('filament', '#FFC48A', 2.6 * glow if lit else 0.0, mirror_only=False), 'tube')
    if not lit:
        tube.data.materials[0] = principled('opal-off', '#E8E4DC', 0.5)
        tube.visible_shadow = True; tube.visible_diffuse = True
    obs.append(tube)
    for o in obs:
        o.location = (o.location[0] + base[0], o.location[1] + base[1], o.location[2] + base[2])
        if o.type == 'MESH' and o.name != 'column':
            o.cycles.is_caustics_receiver = True
    return obs


# --- the shots -----------------------------------------------------------------------------------------------------
def set_room(table_z, wall_y=0.95, wall='beige_wall_001', top='oak_veneer_01'):
    import assets
    wallm = assets.pbr(bpy, wall, '2k', scale=1.2, name='wall', tint='#CFC8BC', tint_mix=0.35)
    topm = assets.pbr(bpy, top, '2k', name='tabletop')
    floorm = principled('floor', '#3A3029', 0.6)
    plane('wall', (4.3, 4), (0.85, wall_y, 1.5), (90, 0, 0), wallm)           # it ends at the window's wall (x -1.3)
    plane('floor', (4.3, 6), (0.85, 0, 0), (0, 0, 0), floorm)
    box_ob('table', -0.55, -0.40, table_z - 0.03, 0.55, 0.38, table_z, topm, bevel=0.002)
    box_ob('table-leg', -0.5, -0.35, 0, -0.46, -0.31, table_z - 0.03, topm)


def contour_core(lit=True, tint=None, glow=1.0, base=(0.0, 0.0, 0.0), loading=1.0):
    """Contour Core at `base` (m): the terraced ball, its globe lit or not, the base from its CAD."""
    P = dict(S.CC)
    if tint:
        P['tint'] = tint
    L = S.contour_core(P)
    lay = [(l['z0'], l['z1'], l['tint']) for l in L]
    mats = {'side': acrylic_material('cc-edge', lay, 0.0, 'polished', loading),
            'tread': acrylic_material('cc-face', lay, 0.0, 'cast', loading, scratch=0.6),
            'bore': acrylic_material('cc-inner', lay, 0.75, 'blasted', loading, scratch=0.0)}
    zones = {'side': 'cc-edge', 'side-s': 'cc-edge', 'bore-s': 'cc-inner', 'tread': 'cc-face', 'top': 'cc-face', 'bottom': 'cc-face',
             'bore': 'cc-inner', 'inner_tread': 'cc-face'}
    ball = revolve('ball', L, zones, segs=288)
    out = os.path.join(HERE, 'out-contour-core', 'stl')
    an = anodised()
    obs = [ball]
    for nm, mat in (('base', an), ('holder', an), ('seat', principled('silicone', '#111111', 0.6)),
                    ('knob', principled('steel', '#C9C9C6', 0.22, 1.0, bump=(2500.0, 0.6))),
                    ('jack', principled('nickel', '#B9B6AE', 0.3, 1.0)), ('bumpers', principled('rubber', '#141414', 0.7))):
        obs.append(stl(os.path.join(out, f'{nm}.stl'), mat, nm))
    zc = (P['base_top'] + P['n'] * S.T / 2 - P['skip'] * S.T) * MM
    glob = stl(os.path.join(out, 'globe.stl'), emitter('globe-glow', '#FFC48A', 2.4 * glow, mirror_only=False) if lit else
               principled('opal-off', '#ECE8E0', 0.45), 'globe')
    obs.append(glob)
    for o in obs:
        o.location = (o.location[0] + base[0], o.location[1] + base[1], o.location[2] + base[2])
        if o.type == 'MESH' and o.name != 'ball':
            o.cycles.is_caustics_receiver = True
    return obs


def shot_core_sample(lit, stackmix=None, out=None, scale=1.0, samples=512, tag='', which='sample', tint=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    tz = 0.62
    set_room(tz)
    if which == 'contour':
        contour_core(lit=lit, tint=tint, base=(0.0, 0.0, tz), glow=1.7 if lit else 1.0)
    else:
        core_sample(stackmix=stackmix, lit=lit, base=(0.0, 0.0, tz), glow=1.8 if lit else 1.0)
    import assets
    # critic r1 c6 / r2 c7: no vase, no plate cut by the frame
    # critic r1 c5: a white card low and to the front left, out of frame, for one highlight on the foot's edge
    box_ob('card', -0.30, -0.30, tz, -0.10, -0.295, tz + 0.08, principled('card', '#F2F0EA', 0.8))
    book = principled('cloth', '#3E4A3F', 0.8, bump=(800.0, 0.3))
    # critic r2 c6: the books whole in the frame, behind the lamp's plane
    box_ob('book', -0.30, 0.04, tz, -0.10, 0.19, tz + 0.032, book, bevel=0.002)
    box_ob('book2', -0.28, 0.06, tz + 0.032, -0.12, 0.18, tz + 0.054, principled('cloth2', '#B8A98E', 0.85), bevel=0.002)
    if lit:
        world(hdri='kiara_9_dusk', strength=0.05, rotation=200)
        # critic r1: c1 the fill down 70 %, c7 cool (#9FB0CC), c4 a 15 x 60 strip rim light behind at 120 deg camera
        # right, c2 the lamp's glow 1.7 (in core_sample), c3 exposure down 0.6
        # critic r2: c1 the fill down a further 60 %; c4 a 10 x 60 kicker low behind-left on the foot; c5 a tall thin
        # sheen strip camera-right (replacing r1's rim strip, whose specular ticks read as CG on the terraced ball)
        from mathutils import Vector

        def aim(ob, z):
            ob.rotation_euler = (Vector((0, 0, z)) - Vector(ob.location)).to_track_quat('-Z', 'Y').to_euler()
        area('room-fill', (-1.2, -1.0, 1.9), (55, 0, -40), (1.0, 1.0), 0.7, '#9FB0CC')
        kick = area('kicker', (-0.40, 1.2, tz + 0.08), (0, 0, 0), (0.6, 0.10), 1.2, '#FFF4E8'); aim(kick, tz + 0.01)
        sheen = area('sheen', (0.87, -0.5, tz + 0.12), (0, 0, 0), (0.15, 1.2), 0.5, '#FFF4E8'); aim(sheen, tz + 0.09)
        render_settings(1600, 1067, samples, scale, exposure=0.8, look='AgX - Medium High Contrast')
    else:
        world(hdri='kiara_9_dusk', strength=0.6, rotation=200)
        window_gobo(-1.3, -1.3, 0.9, 0.75, 2.4)
        # daylight: the window's sky as a large soft source (its coloured shadows converge as refractive caustics), and a
        # weak low sun for the sun patches
        win = area('window-sky', (-1.25, -0.2, 1.55), (0, -90, 0), (1.5, 2.0), 260.0, '#DCE6F5')
        sun_lamp('sun', (0.80, -0.35, -0.42), strength=1.2, color='#FFE7C8', angle=1.0)
        render_settings(1600, 1067, samples, scale, exposure=-0.3)
    camera((0.22, -0.98, tz + 0.30), (0.0, 0.0, tz + 0.085), lens=85, fstop=2.8 if lit else 4.0)
    bpy.context.scene.render.filepath = out
    bpy.ops.render.render(write_still=True)


def terrace(lit=True, tint=None, glow=1.0, rim_z=1.45, loading=1.0, kind='terrace'):
    """Terrace hung with its rim at `rim_z` (m): the shade, the engine and the canopy from the CAD, the COB lit or not.
    Returns the canopy's top z (m) so the room can put its ceiling there."""
    P = dict(S.HL if kind == 'halo' else S.HT)
    if tint and kind != 'halo':
        P['tint'] = tint
    L = S.halo(P) if kind == 'halo' else S.terrace(P)
    lay = [(l['z0'], l['z1'], l['tint']) for l in L]
    mats = {
        'side': acrylic_material('tr-edge', lay, 0.0, 'polished', loading),
        'side-s': acrylic_material('tr-satin', lay, 0.42, 'blasted', loading),
        'tread': acrylic_material('tr-face', lay, 0.0, 'cast', loading, scratch=0.6),
        'bore': acrylic_material('tr-blast', lay, 0.38, 'blasted', loading),
        'inner_tread': acrylic_material('tr-under', lay, 0.0, 'cast', loading, scratch=0.3),
    }
    zones = {'side': 'tr-edge', 'side-s': 'tr-satin', 'bore-s': 'tr-blast', 'tread': 'tr-face', 'top': 'tr-face', 'bottom': 'tr-under',
             'bore': 'tr-blast', 'inner_tread': 'tr-under'}
    shade = revolve('shade', L, zones, segs=288)
    out = os.path.join(HERE, f'out-{kind}', 'stl')
    an = anodised()
    steel = principled('steel', '#C9C9C6', 0.22, 1.0, bump=(2500.0, 0.6))
    obs = [shade]
    names = ['flange', 'core', 'cap', 'gasket', 'reflector', 'cob', 'cord', 'cable', 'grips', 'canopy', 'thumbscrews'] + \
            [f'fin-{i}' for i in range(1, 8)]
    mat = {'thumbscrews': steel, 'cable': principled('cable', '#9A9A98', 0.35, 1.0), 'gasket': principled('silicone', '#111111', 0.6),
           'reflector': principled('satin-al', '#CFCFCB', 0.35, 1.0), 'cord': principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)),
           'grips': principled('nylon', '#0E0E0E', 0.45), 'cob': emitter('cob', '#FFD9A8', 40.0 if lit else 0.0)}
    for nm in names:
        obs.append(stl(os.path.join(out, f'{nm}.stl'), mat.get(nm, an), nm))
    top = L[-1]['z1']
    cob_z = top - (30.0 if kind == 'halo' else 36.0)
    if lit:
        # the louvred aperture: a disc of light 50 across under the COB, cut off at about 30 deg (the honeycomb)
        ap = area('aperture', (0, 0, (cob_z - 14) * MM), (0, 0, 0), (0.05, 0.05), 6.0 * glow, '#FFD2A0', spread=60.0, caustic=True)
        ap.data.shape = 'DISK'; ap.data.size = 0.05
        # the satin reflector's spill: about a quarter of the light, wide, onto the rings' blasted inner edges
        obs += [ap, point('spill', (0, 0, (cob_z - 24) * MM), 6.0 * glow, '#FFD2A0', radius=0.02)]
        glowdisc = bpy.data.meshes.new('louvre')
        bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=0.025)
        bm.to_mesh(glowdisc); bm.free()
        lv = bpy.data.objects.new('louvre', glowdisc); bpy.context.scene.collection.objects.link(lv)
        lv.location = (0, 0, (cob_z - 14.2) * MM); lv.data.materials.append(emitter('louvre-glow', '#FFD9A8', 25.0))
        lv.visible_shadow = False; lv.visible_diffuse = False
        obs.append(lv)
    off = rim_z
    for o in obs:
        o.location = (o.location[0], o.location[1], o.location[2] + off)
        if o.type == 'MESH' and o.name != 'shade':
            o.cycles.is_caustics_receiver = True
    bpy.context.view_layer.update()
    canopy = bpy.data.objects['canopy']
    top_m = max((canopy.matrix_world @ v.co).z for v in canopy.data.vertices)
    return top_m


def shot_terrace(lit, tint=None, out=None, scale=1.0, samples=512, kind='terrace'):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    import assets
    tz = 0.75
    rim = tz + (0.66 if kind == 'halo' else 0.62)
    ceil = terrace(lit=lit, tint=tint, rim_z=rim, kind=kind, glow=1.6 if lit else 1.0)
    wallm = assets.pbr(bpy, 'beige_wall_001', '2k', scale=1.2, name='wall', tint='#CFC8BC', tint_mix=0.35)
    plane('wall', (4.3, 4), (0.85, 1.6, 1.5), (90, 0, 0), wallm)
    plane('floor', (4.3, 6), (0.85, 0, 0), (0, 0, 0), principled('floor', '#2E2622', 0.55))
    plane('ceiling', (4.3, 6), (0.85, 0, ceil), (180, 0, 0), principled('ceiling', '#E9E6E0', 0.9))
    # critic r1 c2: walnut (Poly Haven's walnut set read pale grey here, so its oak toned to walnut)
    topm = assets.pbr(bpy, 'oak_veneer_01', '2k', name='tabletop', tint='#3E2618', tint_mix=0.62)
    plane('wall-left', (6, 4), (-1.3, 0, 1.5), (90, 0, 90), wallm)
    box_ob('table', -0.95, -0.48, tz - 0.035, 0.95, 0.48, tz, topm, bevel=0.003)
    for x in (-0.85, 0.85):
        for y in (-0.38, 0.38):
            box_ob(f'leg{x}{y}', x - 0.025, y - 0.025, 0, x + 0.025, y + 0.025, tz - 0.035, topm)
    # critic r1 c1: no runner, no plate: the pears on bare walnut, the one scale cue
    try:
        assets.place(bpy, 'food_pears_asian_01', '2k', location=(-0.12, -0.04, tz), rotation_deg=(0, 0, 40))
    except Exception as e:
        print('pears skipped', e)
    if lit:
        # critic r1 (Terrace): c5 the dusk world 0.15, c6 the cool fill x1.8, c7 a kicker on the fins, c4 exposure -0.3
        world(hdri='kiara_9_dusk', strength=0.15, rotation=200)
        area('room-fill', (1.6, -1.6, 2.2), (60, 0, 50), (1.0, 1.0), 2.5, '#9FB0CC')
        from mathutils import Vector
        kick = area('fin-kicker', (-0.3, 0.6, rim + 0.5), (0, 0, 0), (0.3, 0.3), 15.0, '#FFF2E6')
        kick.rotation_euler = (Vector((0, 0, rim + 0.17)) - Vector(kick.location)).to_track_quat('-Z', 'Y').to_euler()
        render_settings(1200, 1500, samples, scale, exposure=0.3)
    else:
        world(hdri='kiara_9_dusk', strength=0.7, rotation=200)
        window_gobo(-1.3, -1.6, 1.4, 0.8, 2.3)
        win = area('window-sky', (-1.25, 0.0, 1.55), (0, -90, 0), (1.5, 3.0), 300.0, '#DCE6F5')
        sun_lamp('sun', (0.80, -0.25, -0.55), strength=1.2, color='#FFE7C8', angle=1.0)
        render_settings(1200, 1500, samples, scale, exposure=-0.2)
    # standing eye height, a little above the shade, so the terraces read as rings; the table's pool below
    # critic r1 c8: 70 mm, the shade's top near the frame's top and the pears near its foot
    camera((0.36, -1.75, 1.80), (0.0, 0.0, tz + 0.42), lens=70, fstop=4.0, focus=(0, -0.10, rim + 0.08))
    bpy.context.scene.render.filepath = out
    bpy.ops.render.render(write_still=True)


SHOTS = {
    'contour-core-lit': lambda a: shot_core_sample(True, which='contour', tint='Dust', out=a.out, scale=a.scale, samples=a.samples),
    'contour-core-day': lambda a: shot_core_sample(False, which='contour', tint='Dust', out=a.out, scale=a.scale, samples=a.samples),
    'halo-lit': lambda a: shot_terrace(True, kind='halo', out=a.out, scale=a.scale, samples=a.samples),
    'halo-day': lambda a: shot_terrace(False, kind='halo', out=a.out, scale=a.scale, samples=a.samples),
    'terrace-lit': lambda a: shot_terrace(True, tint='Dust', out=a.out, scale=a.scale, samples=a.samples),
    'terrace-lit-ember': lambda a: shot_terrace(True, tint='Ember', out=a.out, scale=a.scale, samples=a.samples),
    'terrace-day': lambda a: shot_terrace(False, tint='Dust', out=a.out, scale=a.scale, samples=a.samples),
    'core-sample-lit': lambda a: shot_core_sample(True, out=a.out, scale=a.scale, samples=a.samples),
    'core-sample-day': lambda a: shot_core_sample(False, out=a.out, scale=a.scale, samples=a.samples),
}


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument('shot', choices=list(SHOTS))
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--samples', type=int, default=512)
    ap.add_argument('--out', default=None)
    a = ap.parse_args(argv)
    a.out = os.path.abspath(a.out or os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'strata', f'{a.shot}.png'))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    SHOTS[a.shot](a)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
