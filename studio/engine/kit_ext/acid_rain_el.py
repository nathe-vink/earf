"""Acid rain, real (round 31b, Acid's concept B): the pieces a storm over wet black rock needs, as a camera records them.

- rain: falling drops as a shutter of about 1/60 s records them, thin streaks a few to 15 cm long, aligned with the
  fall (leaning with the wind), scattered through the camera's view from `near` to `far` metres, more of them far off
  as a real volume of rain has. Each streak is a water spindle seen as its trace: mostly clear, refracting and
  catching the light behind it, unseen by shadow and diffuse rays (a drop is too small to shade the set).
      {"shape": "ext", "module": "acid_rain_el", "fn": "rain", "camera": {"position", "target", "lens_mm"},
       "count": 9000, "near": 1.2, "far": 30, "length": [0.04, 0.15], "radius": [0.0005, 0.0011],
       "lean": [0.08, 0.0], "z": [0, 6], "opacity": 0.35, "seed": 3}
- splashes: crowns where drops strike water or rock: a thin ring thrown up into points, beads on its tips, `count` of
  them over `area` [x0, y0, x1, y1] at height `z`, sized `radius` [min, max], clear of `avoid` [[x, y, r]].
- puddle: still water at level `z` over `size` [w, d] centred at `position`: it fills the ground's hollows below that
  level and mirrors what stands above it, its surface ringed by drops (ripple rings `ring` metres across at most,
  `rings` how many per square metre).
- wet_ground: a kit ground (studio/engine/kit.py, the same keys) made wet: its colour darkened by `darken`, a film of
  water over it (a clear coat, `film_rough`), its own roughness times `rough_mul`.
"""
import math, random

import bmesh
from mathutils import Vector

FLOAT_BEADS = False   # round 31b's first finals had the crowns' beads hanging above their tips; they sit on them


def _water(bpy, name, opacity=1.0, rough=0.0, tint=(1.0, 1.0, 1.0), scatter=0.0):
    """Clear water: refracting and reflecting (IOR 1.33), mixed with nothing by `opacity` (a streak is a drop's trace,
    so it is mostly the scene behind it). `scatter` of it passes light on diffusely: a drop is a lens that throws the
    light behind it forward over a wide cone, which a thin spindle of glass alone cannot (it shows only what lies
    exactly behind it), so a streak against the light glows as a real one does."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    gl = nt.nodes.new('ShaderNodeBsdfGlass'); gl.inputs['IOR'].default_value = 1.333
    gl.inputs['Roughness'].default_value = rough; gl.inputs['Color'].default_value = (*tint, 1.0)
    if scatter > 0:
        tl = nt.nodes.new('ShaderNodeBsdfTranslucent'); tl.inputs['Color'].default_value = (*tint, 1.0)
        ms = nt.nodes.new('ShaderNodeMixShader'); ms.inputs['Fac'].default_value = scatter
        nt.links.new(gl.outputs['BSDF'], ms.inputs[1]); nt.links.new(tl.outputs['BSDF'], ms.inputs[2])
        gl = ms
    if opacity >= 1.0:
        nt.links.new(gl.outputs[0], out.inputs['Surface'])
        return m
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    mx.inputs['Fac'].default_value = opacity
    nt.links.new(tr.outputs['BSDF'], mx.inputs[1]); nt.links.new(gl.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs['Shader'], out.inputs['Surface'])
    return m


def _object(bpy, name, bm, mat, smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = smooth
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return ob


def _glimpse_only(ob):
    """Seen by the camera, in reflections and through glass; no shadow, no diffuse light, nothing in the haze."""
    for attr in ('visible_shadow', 'visible_diffuse', 'visible_volume_scatter'):
        if hasattr(ob, attr):
            setattr(ob, attr, False)


def _spindle(bm, a, b, r, op=1.0, sides=6, layers=None):
    """A drop's trace from a (top) to b: a thin spindle, full width over its middle, tapering to points at both ends.
    With `layers` (the bmesh's float layers 'rain_op' and 'rain_t'), each vertex carries the streak's opacity and how
    far it is from an end (0 at the tips, 1 in the middle), so the material fades a streak out toward its ends."""
    a, b = Vector(a), Vector(b)
    axis = (b - a).normalized()
    up = Vector((0, 0, 1)) if abs(axis.z) < 0.9 else Vector((1, 0, 0))
    u = axis.cross(up).normalized(); v = axis.cross(u).normalized()
    top = bm.verts.new(a); bot = bm.verts.new(b)
    rings = []
    tv = []
    for t, k in ((0.12, 0.7), (0.5, 1.0), (0.88, 0.85)):
        c = a.lerp(b, t)
        rings.append([bm.verts.new(c + (u * math.cos(2 * math.pi * i / sides) + v * math.sin(2 * math.pi * i / sides)) * r * k)
                      for i in range(sides)])
        tv.append(1.0 - abs(t - 0.5) * 2)
    if layers:
        lo, lt = layers
        for vert, tt in [(top, 0.0), (bot, 0.0)] + [(x, tv[i]) for i, ring in enumerate(rings) for x in ring]:
            vert[lo] = op; vert[lt] = tt
    for i in range(sides):
        j = (i + 1) % sides
        bm.faces.new((top, rings[0][i], rings[0][j]))
        for r0, r1 in zip(rings, rings[1:]):
            bm.faces.new((r0[i], r1[i], r1[j], r0[j]))
        bm.faces.new((rings[-1][j], rings[-1][i], bot))


def _rain_water(bpy, name, rough, scatter):
    """The streaks' water, its opacity per vertex: the streak's own (rain_op) times its fade toward the ends."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    gl = nt.nodes.new('ShaderNodeBsdfGlass'); gl.inputs['IOR'].default_value = 1.333; gl.inputs['Roughness'].default_value = rough
    tl = nt.nodes.new('ShaderNodeBsdfTranslucent')
    ms = nt.nodes.new('ShaderNodeMixShader'); ms.inputs['Fac'].default_value = scatter
    nt.links.new(gl.outputs[0], ms.inputs[1]); nt.links.new(tl.outputs[0], ms.inputs[2])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    ao = nt.nodes.new('ShaderNodeAttribute'); ao.attribute_name = 'rain_op'
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = 'rain_t'
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 0.8
    nt.links.new(at.outputs['Fac'], pw.inputs[0])
    mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'
    nt.links.new(ao.outputs['Fac'], mu.inputs[0]); nt.links.new(pw.outputs[0], mu.inputs[1])
    nt.links.new(mu.outputs[0], mx.inputs['Fac'])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(ms.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    return m


def rain(bpy, name, p, kit):
    """Rain streaks through the camera's view (see the module's notes). `opacity` [min, max] is drawn per streak
    (a number for all alike); `clear` metres: no streak whose lower end is nearer the ground than this (a streak
    ending on the rock reads as a pin standing in it)."""
    sc = bpy.context.scene
    sc.cycles.transparent_max_bounces = max(sc.cycles.transparent_max_bounces, 128)
    cam = p['camera']
    C = Vector(cam['position']); T = Vector(cam['target'])
    fwd = Vector((T.x - C.x, T.y - C.y, 0)).normalized()             # the level camera's axis
    right = fwd.cross(Vector((0, 0, 1))).normalized()
    half = math.atan(18.0 / cam.get('lens_mm', 50.0)) * p.get('margin', 1.25)   # half the horizontal field, and some
    vhalf = math.atan(p.get('frame_h', 24.0) / 2 / cam.get('lens_mm', 50.0)) * p.get('margin', 1.25)
    rnd = random.Random(p.get('seed', 3))
    near, far = p.get('near', 1.2), p.get('far', 30.0)
    z0, z1 = p.get('z', [0.0, 6.0])
    l0, l1 = p.get('length', [0.04, 0.15]); r0, r1 = p.get('radius', [0.0005, 0.0011])
    op = p.get('opacity', 0.35)
    o0, o1 = (op, op) if isinstance(op, (int, float)) else op
    clear = p.get('clear', 0.0)
    lx, ly = p.get('lean', [0.08, 0.0])
    fall = Vector((lx, ly, -1.0)).normalized()
    jit = math.tan(math.radians(p.get('lean_jitter_deg', 0.0)))
    avoid = [tuple(a) for a in p.get('avoid', [])]
    bm = bmesh.new()
    layers = (bm.verts.layers.float.new('rain_op'), bm.verts.layers.float.new('rain_t'))
    n = 0
    for _ in range(p.get('count', 9000) * 12):
        if n >= p.get('count', 9000):
            break
        # depth with density as the volume grows (d squared), so far off holds most of the rain, as it does
        u = rnd.random()
        d = (near ** 3 + u * (far ** 3 - near ** 3)) ** (1 / 3)
        x = math.tan(half) * d * rnd.uniform(-1, 1)
        c = C + fwd * d + right * x
        # within the frame's height at that depth (the level camera's lens shifted onto the target), above the ground
        zc = C.z + (T.z - C.z) * d / max(0.1, (Vector((T.x, T.y, 0)) - Vector((C.x, C.y, 0))).length)
        c.z = zc + math.tan(vhalf) * d * rnd.uniform(-1, 1)
        L = rnd.uniform(l0, l1); r = rnd.uniform(r0, r1)
        if not z0 < c.z < z1 or c.z - L / 2 < clear:
            continue
        tb = p.get('thin_below')                           # [height, share kept]: fewer drops low over the rock
        if tb and c.z < tb[0] and rnd.random() > tb[1]:
            continue
        if any(math.hypot(c.x - ax, c.y - ay) < ar for ax, ay, ar in avoid):
            continue
        # a bigger drop falls faster and is longer in the frame; the far ones a touch thicker, so they hold a pixel
        r *= 1.0 + 0.6 * max(0.0, (d - 8.0) / far)
        f = fall
        if jit:                                            # gusts: each drop's fall a few degrees off the mean
            f = (fall + Vector((rnd.uniform(-jit, jit), rnd.uniform(-jit, jit), 0.0))).normalized()
        _spindle(bm, c - f * L / 2, c + f * L / 2, r, rnd.uniform(o0, o1) ** 1.5 if o1 > o0 else o0, layers=layers)
        n += 1
    ob = _object(bpy, name, bm, _rain_water(bpy, f'{name}-water', p.get('rough', 0.0), p.get('scatter', 0.5)))
    _glimpse_only(ob)
    print(f'{name}: {n} rain streaks')
    return [ob]


def _crown(bm, c, R, h, spikes, rnd):
    """A splash's crown: a thin wall flaring out of the surface, torn at its rim into `spikes` points, a bead on each."""
    rings = []
    seg = spikes * 2
    for t, rk in ((0.0, 0.55), (0.35, 0.8), (0.75, 1.0)):
        rings.append([bm.verts.new((c[0] + R * rk * math.cos(2 * math.pi * i / seg), c[1] + R * rk * math.sin(2 * math.pi * i / seg),
                                    c[2] + h * t)) for i in range(seg)])
    tips = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        hk = (1.0 + rnd.uniform(0.1, 0.5)) if i % 2 == 0 else 0.85
        tips.append(bm.verts.new((c[0] + R * 1.15 * math.cos(a), c[1] + R * 1.15 * math.sin(a), c[2] + h * hk)))
    rings.append(tips)
    for r0, r1 in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new((r0[i], r0[j], r1[j], r1[i]))
    # the wall a little thick, so it refracts
    for i in range(0, seg, 2):
        if rnd.random() < 0.7:
            a = 2 * math.pi * i / seg
            br = R * rnd.uniform(0.12, 0.2)
            up = 0.0 if not FLOAT_BEADS else h * rnd.uniform(0.25, 0.8)   # beads on the crown's tips
            geom = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=br)
            for v in geom['verts']:
                v.co += Vector((c[0] + R * 1.18 * math.cos(a), c[1] + R * 1.18 * math.sin(a), c[2] + h * 1.25 + up))


def splashes(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 5))
    x0, y0, x1, y1 = p.get('area', [-3, -3, 3, 3])
    z = p.get('z', 0.0)
    ra, rb = p.get('radius', [0.008, 0.02])
    avoid = [tuple(a) for a in p.get('avoid', [])]
    bm = bmesh.new()
    n = 0
    for _ in range(p.get('count', 80) * 5):
        if n >= p.get('count', 80):
            break
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if any(math.hypot(x - ax, y - ay) < ar for ax, ay, ar in avoid):
            continue
        R = rnd.uniform(ra, rb)
        _crown(bm, (x, y, z), R, R * rnd.uniform(0.9, 1.6), rnd.choice([7, 8, 9, 10]), rnd)
        n += 1
    ob = _object(bpy, name, bm, _water(bpy, f'{name}-water', p.get('opacity', 0.85), scatter=p.get('scatter', 0.2)))
    _glimpse_only(ob)
    return [ob]


def _ripples(nt, scale, speed_seed, width, keep_share=0.65):
    """A height field of ripple rings: one ring in each Voronoi cell, at a random radius (its age), fading as it grows."""
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.feature = 'F1'; vo.voronoi_dimensions = '2D'
    vo.inputs['Scale'].default_value = scale; vo.inputs['Randomness'].default_value = 1.0
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Location'].default_value = (speed_seed * 7.31, speed_seed * 3.17, 0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], vo.inputs['Vector'])
    sep = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(vo.outputs['Color'], sep.inputs['Color'])

    def math_(op, a, b=None, v=None):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = op
        for k, x in enumerate((a, b)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[k].default_value = x
            else:
                nt.links.new(x, n.inputs[k])
        return n.outputs['Value']
    age = sep.outputs['Red']                                  # 0..1, the ring's radius in a cell's half-width
    R = math_('MULTIPLY', age, 0.48)
    dist = vo.outputs['Distance']
    off = math_('DIVIDE', math_('SUBTRACT', dist, R), width)  # the distance from the ring, in its widths
    ring = math_('EXPONENT', math_('MULTIPLY', math_('MULTIPLY', off, off), -1.0))
    # a second, fainter ring inside the first, and every ring fading as it grows (an old drop's ring is shallow)
    off2 = math_('DIVIDE', math_('SUBTRACT', dist, math_('MULTIPLY', R, 0.55)), width)
    ring2 = math_('MULTIPLY', math_('EXPONENT', math_('MULTIPLY', math_('MULTIPLY', off2, off2), -1.0)), 0.45)
    fade = math_('POWER', math_('SUBTRACT', 1.0, age), 1.5)
    # some cells have no drop in them at the moment
    keep = math_('GREATER_THAN', sep.outputs['Green'], 1.0 - keep_share)
    return math_('MULTIPLY', math_('MULTIPLY', math_('ADD', ring, ring2), fade), keep)


def _impacts(p, water_at, rnd):
    """The rain's impacts on the water in `impacts['area']` [x0, y0, x1, y1]: `density` per square metre visible at
    once, each at a random age (0 the instant it lands, 1 when its rings have died away), kept only where there is
    water (`water_at(x, y)`). A still at 1/60 s catches most of them as rings, a few as splashes."""
    im = p['impacts']
    x0, y0, x1, y1 = im['area']
    n = int(im.get('density', 120) * (x1 - x0) * (y1 - y0))
    out = []
    for _ in range(n * 3):
        if len(out) >= n:
            break
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if water_at(x, y):
            out.append((x, y, rnd.random(), rnd.uniform(0.6, 1.4)))   # x, y, age, the drop's size
    return out


def _ripple_image(bpy, name, p, impacts):
    """A height map (metres) of the impacts' rings at `px_m` a pixel: each a packet of two or three crests a
    wavelength apart (1 to 2 cm, capillary waves), its radius growing with age to `r_max`, its height falling as the
    packet spreads and dies. Returned as a float image for the water's normals, with its frame [x0, y0, w, h]."""
    import numpy as np
    im = p['impacts']
    x0, y0, x1, y1 = im['area']
    px = im.get('px_m', 0.003)
    W, H = int((x1 - x0) / px), int((y1 - y0) / px)
    h = np.zeros((H, W), np.float32)
    rmax, amp = im.get('r_max', 0.12), im.get('amp_m', 0.0006)
    for x, y, age, k in impacts:
        R = max(0.004, rmax * k * age ** 0.7)
        lam = 0.011 + 0.008 * age                         # the rings spread out as they travel
        reach = R + 2.5 * lam
        cx, cy = (x - x0) / px, (y - y0) / px
        r = int(reach / px) + 1
        ia, ib = max(0, int(cy) - r), min(H, int(cy) + r + 1)
        ja, jb = max(0, int(cx) - r), min(W, int(cx) + r + 1)
        if ia >= ib or ja >= jb:
            continue
        yy, xx = np.mgrid[ia:ib, ja:jb]
        d = np.hypot((xx - cx) * px, (yy - cy) * px)
        q = (d - R) / lam
        env = np.exp(-(q / 1.1) ** 2) * (q < 1.2)         # the leading crest highest, two or three behind it
        a = amp * k * (1.0 - age) ** 1.6 / (1.0 + R / 0.03)
        h[ia:ib, ja:jb] += (a * env * np.cos(2 * np.pi * q)).astype(np.float32)
    img = bpy.data.images.new(f'{name}-rings', W, H, alpha=True, float_buffer=True)
    rgba = np.zeros((H, W, 4), np.float32); rgba[..., 0] = h; rgba[..., 1] = h; rgba[..., 2] = h; rgba[..., 3] = 1.0
    img.colorspace_settings.name = 'Non-Color'
    img.pixels.foreach_set(rgba.ravel())
    img.update()
    print(f'{name}: ring map {W} x {H}, height {float(h.min()) * 1000:.2f} to {float(h.max()) * 1000:.2f} mm')
    return img, (x0, y0, x1 - x0, y1 - y0)


def _splash(bm, x, y, z, age, k, rnd):
    """What a drop looks like a moment after it lands, by its age: a crown thrown up (the first few milliseconds), then
    a jet rising from the crater with a bead on top, then only a droplet or two falling back. Millimetres across."""
    if age < 0.012:                                       # the crown
        R = 0.0025 * k + 0.004 * (age / 0.012)
        _crown(bm, (x, y, z), R, R * rnd.uniform(0.8, 1.3), rnd.choice([7, 8, 9, 10, 11]), rnd)
    elif age < 0.03:                                      # the jet
        hgt = 0.006 + 0.012 * k * rnd.random()
        geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.0014 * k, radius2=0.0007 * k, depth=hgt)
        for v in geom['verts']:
            v.co += Vector((x, y, z + hgt / 2))
        geom = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.0013 * k)
        for v in geom['verts']:
            v.co += Vector((x, y, z + hgt + 0.002 * rnd.random()))
    else:                                                 # droplets falling back
        for _ in range(rnd.choice([1, 1, 2, 3])):
            geom = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=rnd.uniform(0.0006, 0.0013) * k)
            off = Vector((rnd.uniform(-0.012, 0.012), rnd.uniform(-0.012, 0.012), rnd.uniform(0.002, 0.02)))
            for v in geom['verts']:
                v.co += Vector((x, y, z)) + off


def puddle(bpy, name, p, kit):
    """Still water at level `z` (see the module's notes). With `impacts`, the rain's rings near the camera are one
    list of impacts at random ages, baked into the water's normals, and the youngest of them are the splashes, so
    every splash sits in its own ring and their phases are spread as a still would catch them; beyond that area the
    procedural rings carry on. `ground` names the ground piece, so impacts land only where there is water."""
    w, d = p.get('size', [8.0, 8.0])
    cx, cy, _ = p.get('position', [0, 0, 0])
    z = p.get('z', 0.004)
    rnd = random.Random(p.get('seed', 9))
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    for v in bm.verts:
        v.co.x = cx + v.co.x * w; v.co.y = cy + v.co.y * d; v.co.z = z
    m = bpy.data.materials.new(f'{name}-water'); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*[c for c in p.get('tint_lin', (0.9, 0.9, 0.82))], 1.0)
    b.inputs['Roughness'].default_value = p.get('roughness', 0.015)
    b.inputs['IOR'].default_value = 1.333
    b.inputs['Transmission Weight'].default_value = 1.0
    big = p.get('ring', 0.12)                                 # the largest ring's width (m)
    keep = p.get('keep', 0.65)
    h1 = _ripples(nt, 1.0 / big, 1.0, 0.035, keep)
    h2 = _ripples(nt, 1.0 / (big * 0.55), 2.0, 0.04, keep)
    kb = p.get('big_rings', 1.0)                         # the large, old rings shallower than the fresh small ones
    if kb != 1.0:
        scaled = []
        for h in (h1, h2):
            mn = nt.nodes.new('ShaderNodeMath'); mn.operation = 'MULTIPLY'; mn.inputs[1].default_value = kb
            nt.links.new(h, mn.inputs[0]); scaled.append(mn.outputs['Value'])
        h1, h2 = scaled
    h3 = _ripples(nt, 1.0 / (big * 0.3), 3.0, 0.05, keep)
    h4 = _ripples(nt, 1.0 / (big * 0.14), 4.0, 0.06, keep)
    add = nt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'
    nt.links.new(h1, add.inputs[0]); nt.links.new(h2, add.inputs[1])
    add2 = nt.nodes.new('ShaderNodeMath'); add2.operation = 'ADD'
    nt.links.new(add.outputs['Value'], add2.inputs[0]); nt.links.new(h3, add2.inputs[1])
    add3 = nt.nodes.new('ShaderNodeMath'); add3.operation = 'ADD'
    nt.links.new(add2.outputs['Value'], add3.inputs[0]); nt.links.new(h4, add3.inputs[1]); add = add3
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = p.get('ripple', 0.5)
    bp.inputs['Distance'].default_value = p.get('ripple_m', 0.0015)
    height = add.outputs['Value']
    obs = []
    if p.get('impacts'):
        ground = bpy.data.objects.get(p.get('ground', 'prop0-kit'))
        def water_at(x, y):
            if ground is None:
                return True
            hit, loc, *_ = ground.ray_cast(ground.matrix_world.inverted() @ Vector((x, y, 2.0)), Vector((0, 0, -1)))
            return (not hit) or (ground.matrix_world @ loc).z < z - p['impacts'].get('margin_m', 0.012)
        imp = _impacts(p, water_at, rnd)
        img, (fx, fy, fw, fh) = _ripple_image(bpy, name, p, imp)
        tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (1.0 / fw, 1.0 / fh, 1.0)
        mp.inputs['Location'].default_value = (-fx / fw, -fy / fh, 0.0)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
        tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = img; tx.extension = 'CLIP'; tx.interpolation = 'Cubic'
        nt.links.new(mp.outputs['Vector'], tx.inputs['Vector'])
        # inside the area the impacts' own rings (metres), outside it the procedural ones (scaled to metres)
        sc = nt.nodes.new('ShaderNodeMath'); sc.operation = 'MULTIPLY'
        sc.inputs[1].default_value = p.get('ripple', 0.5) * p.get('ripple_m', 0.0015)
        nt.links.new(height, sc.inputs[0])
        inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
        nt.links.new(tx.outputs['Alpha'], inv.inputs[1])
        mo = nt.nodes.new('ShaderNodeMath'); mo.operation = 'MULTIPLY'
        nt.links.new(sc.outputs[0], mo.inputs[0]); nt.links.new(inv.outputs[0], mo.inputs[1])
        ia = nt.nodes.new('ShaderNodeMath'); ia.operation = 'MULTIPLY'; ia.inputs[1].default_value = p['impacts'].get('gain', 1.0)
        nt.links.new(tx.outputs['Color'], ia.inputs[0])
        tot = nt.nodes.new('ShaderNodeMath'); tot.operation = 'ADD'
        nt.links.new(mo.outputs[0], tot.inputs[0]); nt.links.new(ia.outputs[0], tot.inputs[1])
        bp.inputs['Strength'].default_value = 1.0; bp.inputs['Distance'].default_value = 1.0
        height = tot.outputs[0]
        # the youngest impacts are still splashing
        young = p['impacts'].get('splash_age', 0.06)
        sb = bmesh.new()
        ns = 0
        for x, y, age, k in imp:
            if age < young:
                _splash(sb, x, y, z, age / young * 0.06, k, rnd)
                ns += 1
        if ns:
            sob = _object(bpy, f'{name}-splashes', sb, _water(bpy, f'{name}-splash-water', 1.0))
            _glimpse_only(sob)
            obs.append(sob)
        else:
            sb.free()
        print(f'{name}: {len(imp)} impacts, {ns} still splashing')
    nt.links.new(height, bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    ob = _object(bpy, name, bm, m, smooth=False)
    if p.get('shadow') is False:
        ob.visible_shadow = False
    return [ob] + obs


def wet_ground(bpy, name, p, kit):
    """A kit ground, wet (see the module's notes)."""
    q = dict(p); q['shape'] = 'ground'; q.pop('module', None); q.pop('fn', None)
    obs = kit.piece(bpy, name, q)
    if p.get('lumps'):
        _lumps(obs[0], p['lumps'], p.get('flat', [0.0, 0.0, 0.9]), p.get('seed', 2), p.get('dips', []))
    _wet(obs, p)
    return obs


def _lumps(ob, lumps, flat, seed, dips=()):
    """Lava's forms on a ground: for each [size_m, height_m, kind] a layer of noise ('fbm' rolling, 'ridged' ropes and
    pressure ridges, 'billow' pillowy pahoehoe), level within `flat` [x, y, r] and rising to full by 2 r."""
    from mathutils import noise
    rnd = random.Random(seed)
    offs = [Vector((rnd.uniform(-500, 500), rnd.uniform(-500, 500), rnd.uniform(-50, 50))) for _ in lumps]
    fx, fy, fr = flat if flat else (0.0, 0.0, 0.0)
    me = ob.data; L = ob.location
    for v in me.vertices:
        wx, wy = v.co.x + L.x, v.co.y + L.y
        dz = 0.0
        for dx, dy, dr, dd in dips:
            q = math.hypot(wx - dx, wy - dy) / dr
            if q < 1.0:
                dz -= dd * (1 - q * q) ** 2
        t = 1.0
        if fr > 0:
            q = min(1.0, max(0.0, (math.hypot(wx - fx, wy - fy) - fr) / fr))
            t = q * q * (3 - 2 * q)
        v.co.z += dz
        if t <= 0:
            continue
        z = 0.0
        for (size, h, *k), o in zip(lumps, offs):
            kind = k[0] if k else 'fbm'
            P = Vector((wx / size, wy / size, 0.0)) + o
            if kind == 'ridged':
                z += h * (noise.ridged_multi_fractal(P, 0.9, 2.0, 3, 0.0, 2.0) - 0.6)
            elif kind == 'billow':
                z += h * (abs(noise.fractal(P, 0.7, 2.0, 3)) - 0.3)
            else:
                z += h * noise.fractal(P, 0.6, 2.0, 4)
        v.co.z += t * z
    me.update()


def ridge(bpy, name, p, kit):
    """Hills far off: a strip of ground `width` x `depth` metres at `position` (its front-centre), its height a ridged
    profile up to `height` (peaks every `spacing` metres or so), dressed in a rock texture; the haze does the rest."""
    from mathutils import noise
    W, D = p.get('width', 600.0), p.get('depth', 120.0)
    H, sp = p.get('height', 25.0), p.get('spacing', 120.0)
    nx, ny = p.get('cells', [300, 60])
    x0, y0, z0 = p.get('position', [0.0, 300.0, 0.0])
    rnd = random.Random(p.get('seed', 21)); o = Vector((rnd.uniform(-99, 99), rnd.uniform(-99, 99), 0))
    bm = bmesh.new()
    grid = []
    for j in range(ny + 1):
        row = []
        for i in range(nx + 1):
            x = x0 - W / 2 + W * i / nx; y = y0 + D * j / ny
            prof = math.sin(math.pi * min(1.0, j / ny * 1.6)) if j / ny < 0.625 else max(0.0, 1.0 - (j / ny - 0.625) / 0.375) * 1.0
            hgt = H * max(0.0, 0.25 + noise.fractal(Vector((x / sp, y / sp * 0.5, 0)) + o, 0.55, 2.0, 6)) * prof
            for gx, gw in p.get('gaps', []):                  # a low pass where the light comes through
                hgt *= 1.0 - 0.85 * math.exp(-((x - gx) / gw) ** 2)
            hgt += p.get('jag', 0.0) * noise.ridged_multi_fractal(Vector((x / 9.0, y / 9.0, 3.0)) + o, 0.8, 2.0, 4, 0.0, 2.0) * min(1.0, hgt / max(1.0, 0.3 * H))
            row.append(bm.verts.new((x, y, z0 + hgt)))
        grid.append(row)
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    q = {'material': 'pbr', 'texture': p.get('texture', 'dark_rock_02'), 'res': p.get('res', '1k'),
         'tex_scale': p.get('tex_scale', 20.0), 'rough_mul': p.get('rough_mul', 0.6), 'position': [0, 0, 0]}
    obs = kit.finish(bpy, name, bm, q, smooth=True)
    _wet(obs, {**p, 'film_rough': p.get('film_rough', 0.2)})
    return obs


def boulder(bpy, name, p, kit):
    """A boulder of black rock: an icosphere torn by noise into a lump (`size` [x, y, z] metres, `rough` how torn,
    `seed`), sunk `sink` of its height into the ground, dressed in a photographed rock texture (`texture`, wet if
    `wet`)."""
    from mathutils import noise
    rnd = random.Random(p.get('seed', 1))
    sx, sy, sz = p.get('size', [1.0, 0.8, 0.6])
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=p.get('subdiv', 5), radius=1.0)
    off = Vector((rnd.uniform(-90, 90), rnd.uniform(-90, 90), rnd.uniform(-90, 90)))
    tr = p.get('rough', 0.35)
    for v in bm.verts:
        n = v.co.normalized()
        k = 1.0 + tr * noise.fractal(off + n * 1.3, 0.6, 2.1, 5) + 0.5 * tr * noise.ridged_multi_fractal(off * 1.7 + n * 3.0, 0.9, 2.0, 4, 0.5, 2.0) * 0.3
        c = n * k
        v.co = Vector((c.x * sx / 2, c.y * sy / 2, c.z * sz / 2))
    # a flat-ish base: what is under the ground stays under it
    sink = p.get('sink', 0.2) * sz
    for v in bm.verts:
        v.co.z += sz / 2 - sink
    q = {'material': 'pbr', 'texture': p.get('texture', 'dark_rock'), 'res': p.get('res', '2k'),
         'tex_scale': p.get('tex_scale'), 'displace': 0.0, 'rough_mul': p.get('rough_mul', 0.5), 'bump': p.get('bump', 1.0),
         'position': p.get('position', [0, 0, 0]), 'rotate': p.get('rotate', [0, 0, rnd.uniform(0, 360)]), 'scale': 1.0}
    obs = kit.finish(bpy, name, bm, q, smooth=True)
    if p.get('wet', True):
        _wet(obs, p)
    return obs


def _wet(obs, p):
    done = set()
    for ob in obs:
        for m in ob.data.materials:
            if not m or m.name in done:
                continue
            done.add(m.name)
            nt = m.node_tree
            bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
            lk = bs.inputs['Base Color'].links
            if lk:
                mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
                mul.inputs['Factor'].default_value = 1.0
                k = 1.0 - p.get('darken', 0.45)
                mul.inputs['B'].default_value = (k, k, k, 1.0)
                nt.links.new(lk[0].from_socket, mul.inputs['A']); nt.links.new(mul.outputs['Result'], bs.inputs['Base Color'])
            bs.inputs['Coat Weight'].default_value = p.get('film', 1.0)
            bs.inputs['Coat Roughness'].default_value = p.get('film_rough', 0.06)
            if p.get('film_vary'):                         # the film pools: pits dull, crests and flats glossy
                lo, hi = p['film_vary']
                tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
                nz.inputs['Scale'].default_value = 1.0 / p.get('film_size', 0.25); nz.inputs['Detail'].default_value = 6.0
                nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
                mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.35
                mr.inputs['From Max'].default_value = 0.65; mr.inputs['To Min'].default_value = lo; mr.inputs['To Max'].default_value = hi
                nt.links.new(nz.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], bs.inputs['Coat Roughness'])
            bs.inputs['Coat IOR'].default_value = 1.333


def rock(bpy, name, p, kit):
    """A scanned rock (a Poly Haven model), placed, turned and scaled, darkened toward black lava and wet."""
    import assets
    root = assets.place(bpy, p['model'], p.get('res', '2k'), tuple(p.get('position', [0, 0, 0])),
                        tuple(p.get('rotate', [0, 0, 0])), p.get('scale', 1.0), name)
    meshes = [o for o in root.children_recursive if o.type == 'MESH']
    seen = set()
    for o in meshes:
        for m in o.data.materials:
            if m and m.name not in seen:
                seen.add(m.name)
                _desaturate(m, p.get('desaturate', 0.7))
    _wet([o for o in meshes], p)
    return [root] + meshes


def _desaturate(m, k):
    nt = m.node_tree
    bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bs or not bs.inputs['Base Color'].links or k <= 0:
        return
    hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = 1.0 - k
    src = bs.inputs['Base Color'].links[0].from_socket
    nt.links.new(src, hs.inputs['Color']); nt.links.new(hs.outputs['Color'], bs.inputs['Base Color'])


def rocks(bpy, name, p, kit):
    """Scanned rocks scattered over `area` (assets.scatter's keys: models, count, area, avoid, scale, z, seed, tilt_deg),
    darkened toward black lava and wet, like `rock`."""
    import assets
    made = assets.scatter(bpy, p['models'], p.get('res', '1k'), p.get('count', 20), tuple(p.get('area', [-3, -3, 3, 3])),
                          [tuple(a) for a in p.get('avoid', [])], tuple(p.get('scale', [0.8, 1.2])), p.get('z', 0.0),
                          p.get('seed', 1), True, p.get('tilt_deg', 10.0))
    meshes = [o for r in made for o in r.children_recursive if o.type == 'MESH']
    seen = set()
    for o in meshes:
        for m in o.data.materials:
            if m and m.name not in seen:
                seen.add(m.name)
                _desaturate(m, p.get('desaturate', 0.7))
    _wet(meshes, p)
    return made + meshes


def haze_box(bpy, name, p, kit):
    """A second box of haze (the shot's `haze` is one): `box_m` [x0, y0, z0, x1, y1, z1], `density`, `anisotropy`,
    `color`. Two boxes let the far hills sit deep in haze while the low sun reaches the set along a path kept clear of
    the far box (one box deep enough for the hills put 500 m of haze between the sun and the speaker)."""
    x0, y0, z0, x1, y1, z1 = p['box_m']
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector((x0 + (v.co.x + 0.5) * (x1 - x0), y0 + (v.co.y + 0.5) * (y1 - y0), z0 + (v.co.z + 0.5) * (z1 - z0)))
    m = bpy.data.materials.new(f'{name}-haze'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Density'].default_value = p.get('density', 0.01); vs.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.4)
    h = p.get('color', '#FFFFFF').lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    vs.inputs['Color'].default_value = (*[((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c], 1.0)
    nt.links.new(vs.outputs['Volume'], out.inputs['Volume'])
    return [_object(bpy, name, bm, m, smooth=False)]
