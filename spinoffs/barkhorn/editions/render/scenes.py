"""The editions' scenes, built on pt.py. Usage (on the Python with bpy):

    python3.11 scenes.py -- EDITION SHOT OUT.png [--scale 0.5] [--samples 64]

EDITION: firn | iron | stamper. SHOT: hero | macro.
Geometry is a proposal for the editions (EDITIONS.md); the products' own drawings rule where they differ.
"""
import math
import os
import random
import sys

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import bpy  # noqa: E402
import pt  # noqa: E402
from pt import MM  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
LIFT = 0.3            # every solid stands 0.3 mm off what it rests on: coplanar faces render black in Cycles


def cut(body, tool):
    """Subtract tool from body (an exact boolean), the tool hidden."""
    m = body.modifiers.new('cut', 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    m.solver = 'EXACT'
    m.object = tool
    tool.hide_render = True
    tool.hide_viewport = True
    # the bevel and normals modifiers come after the cut
    for name in ('bevel', 'wn'):
        if name in body.modifiers:
            body.modifiers.move(body.modifiers.find('cut'), 0)
    return body


# --- props -------------------------------------------------------------------------------------------------------------
def record(z0=LIFT, r=151.0, t=1.6):
    """A black 12 in LP: grooves as a fine ring bump with an anisotropic sheen along them, a matte paper label."""
    mat = bpy.data.materials.new('vinyl')
    nt, out = pt._nodes(mat)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (0.0035, 0.0035, 0.004, 1)
    b.inputs['Roughness'].default_value = 0.16
    b.inputs['Anisotropic'].default_value = 0.0   # a radial tangent's branch cut drew a line across the disc (round 2)
    b.inputs['Specular IOR Level'].default_value = 0.35
    tg = nt.nodes.new('ShaderNodeTangent')
    tg.direction_type = 'RADIAL'
    tg.axis = 'Z'
    nt.links.new(tg.outputs['Tangent'], b.inputs['Tangent'])
    tc = nt.nodes.new('ShaderNodeTexCoord')
    wave = nt.nodes.new('ShaderNodeTexWave')
    wave.wave_type = 'RINGS'
    wave.inputs['Scale'].default_value = 1400.0
    wave.inputs['Distortion'].default_value = 0.0
    nt.links.new(tc.outputs['Object'], wave.inputs['Vector'])
    bm = nt.nodes.new('ShaderNodeBump')
    bm.inputs['Strength'].default_value = 0.15
    nt.links.new(wave.outputs['Fac'], bm.inputs['Height'])
    # no groove bump: at this scale the rings alias into a hard line across the disc (critic rounds 1 and 2); pressed
    # vinyl seen from a metre is a black mirror anyway
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    pt.disc('record', r, z0, z0 + t, mat, bevel=0.5)
    pt.disc('label', 50, z0 + t + 0.02, z0 + t + 0.12, pt.principled('label', '#1E1E1E', rough=0.92, spec=0.2), bevel=0)
    steel = pt.principled('spindle', '#B8B6B2', rough=0.25, metal=1.0)
    pt.disc('spindle_pin', 3.55, z0 + t, z0 + t + 11.0, steel, bevel=0.6, segs=40)
    return z0 + t


# --- Firn: Moho, the record weight, bubbles by design --------------------------------------------------------------
FIRN = dict(r=40.0, h=36.0, ice=3.0, layers=6, layer=5.0, spindle=(4.0, 12.0))


def firn(z0):
    """Moho in clear with an Ice top: six 5 mm clear layers and a 3 mm clear base under a 3 mm Ice lamina (round 1 of
    the critic: an Ice base lamina, seen by total reflection along the base, went navy and hid the lowest voids). At each of the
    five inner bond lines and under the top lamina, lens-shaped air voids from two matching dished pockets: columns of
    them stacked like the air a glacier traps as snow turns to ice."""
    f = FIRN
    zb, zt = z0, z0 + f['h']
    mat = pt.acrylic('firn', 'clear')
    body = pt.disc('moho', f['r'], zb, zt, mat, bevel=1.2, segs=200)
    ice = pt.lamina('ice', 'ice')
    pt.disc('ice_top', f['r'] - 0.05, zt - f['ice'], zt - 0.05, ice, bevel=1.15, segs=200)
    # the spindle's hole from below
    cut(body, pt.disc('spindle', f['spindle'][0], zb - 2, zb + f['spindle'][1], None, segs=48, bevel=0))
    rnd = random.Random(7)
    lines = [zb + f['ice'] + f['layer'] * i for i in range(1, f['layers'])] + [zt - f['ice']]
    cols = [(rnd.uniform(-24, 24), rnd.uniform(-24, 24)) for _ in range(9)]
    cols = [(x, y) for x, y in cols if math.hypot(x, y) > 9][:7]
    n = 0
    for li, z in enumerate(lines):
        for ci, (cx, cy) in enumerate(cols):
            if rnd.random() < 0.18:
                continue
            r = rnd.uniform(2.2, 6.5) * (1.0 - 0.07 * li)
            x, y = cx + rnd.gauss(0, 1.2), cy + rnd.gauss(0, 1.2)
            if math.hypot(x, y) + r > f['r'] - 5:
                continue
            pt.lens_void(f'v{n}', (x, y, z), r, min(0.22 * r, 1.4), mat, segs=56, rings=7)
            n += 1
        for _ in range(rnd.randint(4, 8)):                       # small ones between the columns
            a, d = rnd.uniform(0, 2 * math.pi), rnd.uniform(10, f['r'] - 6)
            r = rnd.uniform(0.7, 1.6)
            pt.lens_void(f'w{n}', (d * math.cos(a), d * math.sin(a), z), r, 0.32 * r, mat, segs=24, rings=4)
            n += 1
    print('firn voids', n)
    return body


def firn_scene(shot):
    pt.reset()
    if shot == 'hero':
        # critic round 1 (5.5): cove darker, overhead and key and right rim down, the card lit, cove rougher, camera up
        # critic round 2 (5.5): (a grey card behind for the lower body was tried and read as a placard); rims and key down; overhead down and
        # softer at its edge (its 40 degree pool drew a hard line across the LP); the glint lower; a dark label
        pt.cove('#0B0B0C', rough=0.75, radius=500)
        top = record()
        firn(top + LIFT)
        pt.area('overhead', (-60, 160, 620), (0, 0, 20), (700, 420), 11, '#FFF4E6', spread=75)
        pt.area('key', (-420, -260, 300), (0, 0, 22), 220, 2, '#FFF1E0')
        pt.area('rimL', (-260, 300, 140), (0, 0, 20), (60, 520), 3, '#E8F0FF')
        pt.area('rimR', (280, 280, 160), (0, 0, 20), (60, 520), 2, '#E8F0FF')
        pt.spot('glint', (300, -260, 180), (0, 0, 36), 60, size_mm=6, angle=12)
        pt.area('card', (0, -520, 40), (0, 0, 14), (600, 160), 4, '#FFFFFF')
        pt.camera((60, -470, 220), (0, 0, 14), lens=85)
    elif shot in ('hero_b', 'macro_b'):
        # a second hero (its own card and rounds): bright-field. The first hero stopped at 5.0 after three rounds, every
        # round naming the same cause: clear acrylic on a black set transmits black. Here a light seamless fills the body,
        # and the camera sits low so the bond-line voids are seen near edge-on, as columns
        # hero_b critic round 1 (5.5): the wall wash aimed higher, out of what the record mirrors; the cove a mid grey;
        # a black flag in front for the label and vinyl; rimR up to feed the trapped voids; key down; the camera lower
        pt.cove('#8E8C89', rough=0.8, radius=700, height=2400, width=5000)
        top = record()
        firn(top + LIFT)
        # hero_b round 2 (5.5): overhead 9 -> 4, key 4.5 -> 2.5, wall 10 -> 7; a black flag on the left; a low fill
        pt.area('overhead', (-40, 120, 520), (0, 0, 20), (600, 360), 4, '#FFF4E6', spread=75)
        pt.area('key', (-460, -220, 220), (0, 0, 20), 240, 2.5, '#FFF1E0')
        pt.area('wall', (0, 500, 200), (0, 900, 520), (900, 500), 7, '#FFFFFF')
        fl2 = pt.block('flagL', 160, 2, 0, 300, pt.principled('flagL', '#111111', rough=1.0, spec=0.0), bevel=0)
        fl2.location = (-0.16, 0.11, 0.0)
        fl2.rotation_euler.z = math.radians(55)
        lo = pt.area('lowfill', (0, -260, 30), (0, 0, 18), (300, 80), 0.8, '#FFF8F0')
        lo.visible_camera = False
        pt.area('rimR', (300, 240, 90), (0, 0, 20), (60, 400), 8, '#E8F0FF')
        pt.spot('glint', (260, -300, 160), (0, 0, 30), 40, size_mm=5, angle=10)
        fl = pt.block('flag', 600, 2, 0, 300, pt.principled('flag', '#0A0A0A', rough=1.0, spec=0.0), bevel=0)
        fl.location = (0.04, -0.52, 0.11)
        pt.camera((40, -420, 120), (0, 0, 18), lens=100)
        if shot == 'macro_b':                              # the detail: the same light, close on the void columns
            bpy.data.objects['cam'].location = (0.012, -0.2, 0.085)
            pt._aim(bpy.data.objects['cam'], pt.Vector((0, 0.005, 0.02)))
            cd = bpy.data.objects['cam'].data
            cd.dof.use_dof = True
            cd.dof.aperture_fstop = 11
            cd.dof.focus_distance = 0.2
    else:
        pt.cove('#0B0B0C', rough=0.75, radius=400)
        top = record()
        firn(top + LIFT)
        pt.area('overhead', (0, 120, 420), (0, 0, 20), (500, 300), 14, '#FFF4E6', spread=40)
        pt.area('back', (40, 260, 30), (0, 0, 18), (300, 90), 7, '#EAF2FF')
        pt.area('key', (-260, -160, 200), (0, 0, 20), 140, 5, '#FFF1E0')
        pt.spot('glint', (300, -120, 300), (0, 0, 30), 30, size_mm=5, angle=10)
        pt.camera((10, -190, 120), (0, 0, 22), lens=100, fstop=11, focus=None)


# --- Iron: Core, the 160 mm ball, an iron meteorite slice at its centre --------------------------------------------
def widmanstatten(name):
    """An etched octahedrite: kamacite bands in three directions (the octahedron's planes as a slice cuts them),
    bright and dark by the etch's angle, with thin taenite borders and plessite between."""
    mat = bpy.data.materials.new(name)
    nt, out = pt._nodes(mat)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Metallic'].default_value = 1.0
    mx_rough = None
    acc_col, acc_r = None, None
    dirs = [0, 60, 120]
    vals = []
    for i, d in enumerate(dirs):
        rot = nt.nodes.new('ShaderNodeVectorRotate')
        rot.rotation_type = 'Z_AXIS'
        rot.inputs['Angle'].default_value = math.radians(d + 7 * i)
        nt.links.new(tc.outputs['Object'], rot.inputs['Vector'])
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 40.0
        nz.inputs['Detail'].default_value = 2.0
        nt.links.new(rot.outputs['Vector'], nz.inputs['Vector'])
        wv = nt.nodes.new('ShaderNodeTexWave')
        wv.wave_type = 'BANDS'
        wv.bands_direction = 'X'
        wv.wave_profile = 'SAW'
        wv.inputs['Scale'].default_value = 34.0 + 9 * i
        wv.inputs['Distortion'].default_value = 1.2
        wv.inputs['Detail'].default_value = 1.5
        wv.inputs['Phase Offset'].default_value = i * 1.7
        nt.links.new(rot.outputs['Vector'], wv.inputs['Vector'])
        vals.append(wv)
    # which direction wins at each point: a coarse Voronoi cell picks one, as grains of each orientation do
    vor = nt.nodes.new('ShaderNodeTexVoronoi')
    vor.inputs['Scale'].default_value = 55.0
    vor.inputs['Randomness'].default_value = 1.0
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    sep = nt.nodes.new('ShaderNodeSeparateColor')
    nt.links.new(vor.outputs['Color'], sep.inputs['Color'])
    m1 = nt.nodes.new('ShaderNodeMix'); m1.data_type = 'FLOAT'
    gt = nt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.5
    nt.links.new(sep.outputs['Red'], gt.inputs[0])
    nt.links.new(gt.outputs['Value'], m1.inputs['Factor'])
    nt.links.new(vals[0].outputs['Fac'], m1.inputs['A'])
    nt.links.new(vals[1].outputs['Fac'], m1.inputs['B'])
    m2 = nt.nodes.new('ShaderNodeMix'); m2.data_type = 'FLOAT'
    gt2 = nt.nodes.new('ShaderNodeMath'); gt2.operation = 'GREATER_THAN'; gt2.inputs[1].default_value = 0.66
    nt.links.new(sep.outputs['Green'], gt2.inputs[0])
    nt.links.new(gt2.outputs['Value'], m2.inputs['Factor'])
    nt.links.new(m1.outputs['Result'], m2.inputs['A'])
    nt.links.new(vals[2].outputs['Fac'], m2.inputs['B'])
    # the pattern is everywhere: blend in the strongest of all three a little so bands cross as they do in a real etch
    mxa = nt.nodes.new('ShaderNodeMath'); mxa.operation = 'MAXIMUM'
    nt.links.new(vals[0].outputs['Fac'], mxa.inputs[0]); nt.links.new(vals[1].outputs['Fac'], mxa.inputs[1])
    mxb = nt.nodes.new('ShaderNodeMath'); mxb.operation = 'MAXIMUM'
    nt.links.new(mxa.outputs['Value'], mxb.inputs[0]); nt.links.new(vals[2].outputs['Fac'], mxb.inputs[1])
    bl = nt.nodes.new('ShaderNodeMix'); bl.data_type = 'FLOAT'; bl.inputs['Factor'].default_value = 0.45
    nt.links.new(m2.outputs['Result'], bl.inputs['A']); nt.links.new(mxb.outputs['Value'], bl.inputs['B'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp
    cr.elements[0].position = 0.0; cr.elements[0].color = (0.30, 0.30, 0.31, 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (0.80, 0.79, 0.76, 1)
    e = cr.elements.new(0.55); e.color = (0.42, 0.42, 0.42, 1)
    e = cr.elements.new(0.62); e.color = (0.86, 0.85, 0.82, 1)
    e = cr.elements.new(0.88); e.color = (0.78, 0.77, 0.74, 1)
    e = cr.elements.new(0.93); e.color = (0.95, 0.93, 0.88, 1)
    nt.links.new(bl.outputs['Result'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    rr = nt.nodes.new('ShaderNodeMapRange')
    rr.inputs['To Min'].default_value = 0.42; rr.inputs['To Max'].default_value = 0.14
    nt.links.new(bl.outputs['Result'], rr.inputs['Value'])
    nt.links.new(rr.outputs['Result'], b.inputs['Roughness'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25
    bp.inputs['Distance'].default_value = 0.00004
    nt.links.new(bl.outputs['Result'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return mat


def etched(name, tex, zc):
    """The etch image on a metal: bright kamacite polished-looking, dark plessite rougher, a faint relief."""
    mat = bpy.data.materials.new(name)
    nt, out = pt._nodes(mat)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Metallic'].default_value = 1.0
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1 / 0.070, 1 / 0.070, 1 / 0.052)
    mp.inputs['Location'].default_value = (0.5, 0.5, 0.5)
    # the slice stands in the XZ plane: map object X, Z to the image's u, v
    sw = nt.nodes.new('ShaderNodeSeparateXYZ'); cb = nt.nodes.new('ShaderNodeCombineXYZ')
    nt.links.new(tc.outputs['Object'], sw.inputs['Vector'])
    nt.links.new(sw.outputs['X'], cb.inputs['X']); nt.links.new(sw.outputs['Z'], cb.inputs['Y'])
    nt.links.new(cb.outputs['Vector'], mp.inputs['Vector'])
    mp.inputs['Scale'].default_value = (1 / 0.070, 1 / 0.052, 1)
    mp.inputs['Location'].default_value = (0.5, 0.5 - zc * MM / 0.052, 0)
    im = nt.nodes.new('ShaderNodeTexImage')
    im.image = bpy.data.images.load(tex)
    im.image.colorspace_settings.name = 'Non-Color'
    im.extension = 'EXTEND'
    nt.links.new(mp.outputs['Vector'], im.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = (0.06, 0.06, 0.06, 1)
    cr.elements[1].position = 0.8; cr.elements[1].color = (0.55, 0.545, 0.53, 1)
    nt.links.new(im.outputs['Color'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    rr = nt.nodes.new('ShaderNodeMapRange')
    rr.inputs['From Min'].default_value = 0.3; rr.inputs['From Max'].default_value = 0.9
    rr.inputs['To Min'].default_value = 0.5; rr.inputs['To Max'].default_value = 0.22
    nt.links.new(im.outputs['Color'], rr.inputs['Value'])
    nt.links.new(rr.outputs['Result'], b.inputs['Roughness'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.3
    bp.inputs['Distance'].default_value = 0.00003
    nt.links.new(im.outputs['Color'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return mat


def slab_outline(rx, ry, seed=4, n=90):
    rnd = random.Random(seed)
    from mathutils import noise, Vector
    off = Vector((rnd.uniform(0, 50), rnd.uniform(0, 50), 0))
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1.0 + 0.10 * noise.fractal(Vector((math.cos(a) * 1.4, math.sin(a) * 1.4, 0)) + off, 0.6, 2.0, 3)
        pts.append((rx * k * math.cos(a), ry * k * math.sin(a)))
    return pts


def prism_xy(name, pts, t, mat, center, rot_x=90.0, offset=0.0, inward=False):
    """A flat slab of outline pts (mm, in its own plane), thickness t, grown outward by offset, stood up (rot_x)."""
    import bmesh
    from mathutils import Matrix, Vector
    bm = bmesh.new()
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    grown = []
    for x, y in pts:
        v = Vector((x - cx, y - cy)); L = v.length
        grown.append((x + v.x / L * offset, y + v.y / L * offset))
    h = t / 2 + offset
    bot = [bm.verts.new((x * MM, y * MM, -h * MM)) for x, y in grown]
    top = [bm.verts.new((x * MM, y * MM, h * MM)) for x, y in grown]
    bm.faces.new(list(reversed(bot)))
    bm.faces.new(top)
    n = len(grown)
    for i in range(n):
        bm.faces.new((bot[i], bot[(i + 1) % n], top[(i + 1) % n], top[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if inward:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(rot_x), 3, 'X'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(center) * MM, verts=bm.verts)
    ob = pt._obj_from_bm(name, bm, mat, smooth=False)
    if not inward:
        pt.bevel_mod(ob, min(0.6, t * 0.2), segs=2)
    return ob


CORE = dict(R=80.0, base=(56.0, 22.0))


def iron(z_base=LIFT):
    """Core in water-clear (Fog): two turned blocks, one bond at the equator, and at the centre a 5 mm etched slice
    of an iron meteorite standing in a dry pocket cut 0.5 mm larger all round. The base, apart, holds the light."""
    R = CORE['R']
    br, bh = CORE['base']
    # the base: black anodised aluminium, a shallow seat, a ring of warm light under the ball
    alu = pt.principled('alu', '#1E1E21', rough=0.38, metal=1.0)
    pt.disc('base', br, z_base, z_base + bh, alu, bevel=2.0, segs=160)
    ring_mat = pt.emitter('ledring', '#FFC890', 2.5)
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=False, segments=120, radius=34 * MM)
    c2 = bmesh.ops.create_circle(bm, cap_ends=False, segments=120, radius=40 * MM)
    ring = pt._obj_from_bm('ledring_ob', bm, None)
    # annulus as a thin torus is simpler and robust
    bpy.data.objects.remove(ring)
    bpy.ops.mesh.primitive_torus_add(major_radius=37 * MM, minor_radius=1.5 * MM, location=(0, 0, (z_base + bh + 0.2) * MM))
    tor = bpy.context.active_object; tor.name = 'ledring'; tor.data.materials.append(ring_mat)
    zc = z_base + bh + math.sqrt(R * R - 36.0 ** 2) + 0.3          # resting on the seat's 36 mm circle
    clear = pt.acrylic('core', 'clear')
    ball = pt.ellipsoid('core', (0, 0, zc), (R, R, R), clear, subdiv=6)
    import widman, os
    tex = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache-widman.png')
    if not os.path.exists(tex):
        widman.make(tex)
    meteor = etched('gibeon', tex, zc)
    out = slab_outline(31, 22)
    prism_xy('slice', out, 5.0, meteor, (0, 0, zc), rot_x=90, offset=0.0)
    prism_xy('pocket', out, 5.0, clear, (0, 0, zc), rot_x=90, offset=0.5, inward=True)
    # the slice's sawn edge: a dark oxidised rim as dealers leave it, a thin band round the outline
    edge = pt.principled('rind', '#1C1814', rough=0.75, metal=0.4, bump=(4000, 0.6, 4))
    sl = bpy.data.objects['slice']
    sl.data.materials.append(edge)
    for p in sl.data.polygons:
        if abs(p.normal.y) < 0.6:
            p.material_index = 1
    return zc


def iron_scene(shot):
    pt.reset()
    pt.cove('#161618' if shot == 'hero' else '#262628', rough=0.45, radius=600)
    zc = iron()
    if shot == 'hero':
        # critic round 1 (5.0): the front light up out of the slice's mirror; a glow on the cove behind for the ball
        # to refract; overhead and key down; a low strip in front for the base's anodised side
        # critic round 2 (5.5): front 12 -> 3; a black flag behind the camera for the etch's dark phase; overhead
        # 18 -> 9; the key moved back so its reflection leaves the slice; rimR 14 -> 7; cove darker; the low strip 3 -> 1.2.
        # The etch itself redrawn (widman.py v2): interlocking lamellae, not overlapping bars
        pt.area('overhead', (-80, 520, 700), (0, 0, zc), 700, 9, '#FFF3E4', shape='DISK')
        pt.area('key', (-700, 120, 460), (0, 0, zc), 300, 18, '#FFF0DE')
        pt.area('front', (0, -1300, zc + 520), (0, 0, zc), (700, 300), 3, '#FFF6EC')
        fl = pt.block('blackflag', 900, 2, 0, 500, pt.principled('blackflag', '#303030', rough=1.0, spec=0.0), bevel=0)
        fl.location = (0.04, -1.15, zc * MM + 0.244 - 0.25 - zc * MM)
        pt.area('glow', (0, 330, 40), (0, 640, 110), (220, 110), 3, '#FFF3E4')
        pt.area('flag', (0, -420, 25), (0, 0, 12), (700, 80), 1.2, '#FFFFFF')
        pt.area('rimL', (-360, 380, 240), (0, 0, zc), (80, 800), 12, '#E6EEFF')
        pt.area('rimR', (380, 360, 260), (0, 0, zc), (80, 800), 7, '#E6EEFF')
        pt.spot('glint', (460, -300, 520), (0, 0, zc + 20), 30, size_mm=8, angle=14)
        pt.camera((40, -900, zc + 150), (0, 0, zc - 22), lens=85)
    else:
        pt.area('overhead', (0, 520, 560), (0, 0, zc), 600, 18, '#FFF3E4', shape='DISK')
        pt.area('key', (-620, -60, zc + 260), (0, 0, zc), 200, 14, '#FFF0DE', shape='DISK')
        pt.area('front', (0, -900, zc + 60), (0, 0, zc), (500, 260), 5, '#FFF6EC')
        pt.area('rimR', (300, 300, zc + 80), (0, 0, zc), (70, 500), 8, '#E6EEFF')
        pt.spot('glint', (220, -260, zc + 260), (0, 0, zc), 50, size_mm=6, angle=10)
        pt.camera((10, -330, zc + 30), (0, 0, zc), lens=100, fstop=11, focus=332)


# --- Stamper: Bedrock, the record stand, a shard of the nickel stamper that pressed Session 00 ----------------------
TILT = 80.0          # the shard leans back 10 degrees in its pocket, so it mirrors the light above the camera
BED = dict(L=300.0, D=80.0, H=72.0, slot=(7.0, 40.0), smoke=3.0)


def stamper_mat():
    mat = bpy.data.materials.new('nickel')
    nt, out = pt._nodes(mat)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (0.64, 0.62, 0.58, 1)
    b.inputs['Metallic'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.14
    b.inputs['Anisotropic'].default_value = 0.7
    b.inputs['Thin Film Thickness'].default_value = 0.0
    b.inputs['Thin Film IOR'].default_value = 1.6
    tg = nt.nodes.new('ShaderNodeTangent'); tg.direction_type = 'RADIAL'; tg.axis = 'Y'
    nt.links.new(tg.outputs['Tangent'], b.inputs['Tangent'])
    tc = nt.nodes.new('ShaderNodeTexCoord')
    wave = nt.nodes.new('ShaderNodeTexWave'); wave.wave_type = 'RINGS'; wave.rings_direction = 'Y'
    wave.inputs['Scale'].default_value = 520.0
    nt.links.new(tc.outputs['Object'], wave.inputs['Vector'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.12
    nt.links.new(wave.outputs['Fac'], bm.inputs['Height'])
    # real grooves are about 0.1 mm apart, below the frame's resolution: the bump is kept faint so it does not beat
    # into moire (critic, stamper round 2); the anisotropic sheen along them carries the look
    bm.inputs['Strength'].default_value = 0.025
    nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return mat


def bedrock(z0=LIFT, sleeve_mat=None, smoke=True):
    """Bedrock in clear with a 3 mm Smoke base stratum: a slot along its top holds a sleeve; in the front, 9 mm behind
    the face, a sector of the stamper (Session 00's lead-in and first track) stands in a pocket 0.2 mm larger."""
    b = BED
    mat = pt.acrylic('bedrock', 'clear')
    if smoke:
        pt.block('smoke', b['L'] - 0.1, b['D'] - 0.1, z0 + 0.05, z0 + b['smoke'], pt.lamina('smoke_l', 'smoke'), bevel=1.45)
    body = pt.block('bedrock', b['L'], b['D'], z0, z0 + b['H'], mat, bevel=1.5)
    sw, sd = b['slot']
    cut(body, pt.block('slot', b['L'] - 30, sw, z0 + b['H'] - sd, z0 + b['H'] + 5, None, bevel=0))
    # the shard: an annular sector of the stamper, r 62..146 mm about a centre below, 34 degrees, 0.3 mm nickel
    import bmesh
    from mathutils import Matrix, Vector
    rc = 123.0                      # the band r 100..146 centred on its middle radius
    pts = []
    for i in range(41):
        a = math.radians(-21 + 42 * i / 40)
        pts.append((146 * math.sin(a), 146 * math.cos(a) - rc))
    for i in range(41):
        a = math.radians(21 - 42 * i / 40)
        pts.append((100 * math.sin(a), 100 * math.cos(a) - rc))
    yf = -b['D'] / 2 + 9.0
    zc = z0 + 34.0
    shard = prism_xy('shard', pts, 0.4, stamper_mat(), (0, yf, zc), rot_x=TILT, offset=0.0)
    pocket = prism_xy('shard_pocket', pts, 0.4, mat, (0, yf, zc), rot_x=TILT, offset=0.2, inward=True)
    # the radial tangent and the groove rings want the record's centre: put the shard's origin there
    from mathutils import Matrix as _M, Vector as _V
    a = math.radians(TILT)
    c = _V((0, yf * MM, zc * MM)) + _V((0, -math.cos(a), math.sin(a))) * 0 + _V((0, rc * MM * math.cos(a) * 0, 0))
    # the record's centre, in the tilted plane rc below the shard's centre
    cen = _V((0, yf * MM, zc * MM)) + _V((0, 0, -rc * MM)).copy()
    cen = _V((0, yf * MM + rc * MM * math.cos(a) * (1 if TILT < 90 else 0) * 0, zc * MM)) + _M.Rotation(math.radians(TILT - 90), 3, 'X') @ _V((0, 0, -rc * MM))
    shard.data.transform(_M.Translation(-cen))
    shard.location = cen
    # a sleeve in the slot: plain card, ink-black, the session's number blind-debossed (not drawn)
    sleeve = pt.block('sleeve', 314, 3.2, z0 + b['H'] - sd + 0.4, z0 + b['H'] - sd + 314, sleeve_mat or pt.principled(
        'sleeve', '#141414', rough=0.7), bevel=0.4, y=0)
    return zc


def stamper_scene(shot):
    pt.reset()
    pt.cove('#A6A6A4' if shot == 'hero' else '#19191B', rough=0.6, radius=700, height=2600, width=5000)
    zc = bedrock()
    if shot == 'hero':
        # critic round 1 (4.5): the glint down; the rims up for the edges; the set's tone was the root of three of its
        # notes (the block read as dark glass because it transmits the dark set), so the cove goes light (the card lets
        # any neutral) and the black sleeve then reads black against it; the front is a strip whose reflection crosses
        # the whole shard as a band. The flag and floor card it asked for were tried in proof: the flag blacked out the set.
        # critic round 2 (4.5): wider and higher so the sleeve reads whole; overhead down; the front up off the shard's
        # face so it carries an edge; the glint up for the grooves; black flags for the block's end faces; a cooler cove
        pt.area('overhead', (-60, 260, 900), (0, 0, 60), (1000, 600), 16, '#FFF3E4')
        pt.area('key', (-560, -420, 380), (0, 0, 30), 320, 18, '#FFF0DE')
        pt.area('front', (-80, -760, 600), (0, -31, 34), (1600, 160), 10, '#FFF6EC')
        for sx in (-1, 1):
            f = pt.block(f'flag{sx}', 150, 2, 0, 450, pt.principled(f'flag{sx}', '#050505', rough=1.0, spec=0.0), bevel=0)
            f.location = (sx * 0.62, -0.08, 0.0)
            f.rotation_euler.z = math.radians(-sx * 30)
        pt.area('rimL', (-420, 420, 260), (0, 0, 120), (90, 900), 28, '#E6EEFF')
        pt.area('rimR', (440, 380, 260), (0, 0, 120), (90, 900), 32, '#E6EEFF')
        pt.spot('glint', (420, -460, 300), (0, -31, 34), 110, size_mm=8, angle=6)
        pt.camera((-330, -760, 190), (0, 0, 160), lens=45)
    else:
        pt.area('overhead', (0, 160, 480), (0, -20, 40), (500, 300), 16, '#FFF3E4')
        pt.area('key', (-280, -300, 180), (0, -30, 34), 180, 10, '#FFF0DE')
        pt.spot('glint', (200, -330, 120), (0, -31, 34), 70, size_mm=5, angle=8)
        pt.area('rimR', (260, 120, 160), (0, -20, 40), (60, 400), 6, '#E6EEFF')
        pt.area('front', (60, -420, 470), (0, -31, 34), (700, 140), 9, '#FFF6EC')
        pt.camera((-60, -380, 66), (0, -31, 34), lens=100, fstop=11)


SCENES = {'firn': firn_scene, 'iron': iron_scene, 'stamper': stamper_scene}

# --- the lamps lane's pass-4 Core rig (r32-lamps-final, studio/shots/barkhorn/lamps-cordless/p4-lamp-orb-*.json, read,
# never written): the same sweep, marble, camera, lights and view as the Core product frames, so Iron reads as "Core,
# with a meteorite inside". Lamps are converted as studio/engine/lights.py does: an area lamp's watts are its
# irradiance x pi x d^2; azimuth 0 is in front (-y), +90 toward +x. Colour 4300 K under the rig's 4300 K white balance
# is neutral here.
def _orbit(target, az, el, d):
    a, e = math.radians(az), math.radians(el)
    return (target[0] + d * math.cos(e) * math.sin(a), target[1] - d * math.cos(e) * math.cos(a), target[2] + d * math.sin(e))


KEY_EL, BGWASH_Z, BGWASH = 42, 250, '#FFE6C4'
FILL_EL, BACK_Z, BACK_E, MARBLE_ROUGH = 12, 200, 1.6, 0.6
BGWASH_SIZE, BGWASH_E, SKY = (3500, 1000), 2.645, '#D8D2C8'


def core_rig(lit=False):
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
    import assets                                          # Poly Haven CC0, cached in studio/assets/cache (not in git)
    pt.cove('#EAE4DA', rough=0.9, width=10000, depth=6000, height=4000, radius=800)
    slab = pt.block('marble', 3000, 4200, 0, 40, assets.pbr(bpy, 'marble_01', '2k', tint='#ECE7DF', tint_mix=0.3,
                                                           rough_mul=MARBLE_ROUGH, name='marble'), bevel=0, y=800)
    sc = bpy.context.scene
    bg = sc.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = tuple(pt.hex_lin(SKY)) + (1,)
    bg.inputs['Strength'].default_value = 0.35
    T = (0, 0, 148)
    def area_e(name, size, loc, target, E, color='#FFFFFF', camera=True, spec=True):
        d = math.dist(loc, target) * MM
        ob = pt.area(name, loc, target, size, E * math.pi * d * d, color)
        ob.visible_camera = camera
        ob.visible_glossy = spec
        return ob
    area_e('key', (3000, 500), _orbit(T, -30, KEY_EL, 2600), T, 0.6)
    area_e('fill', (2500, 2000), _orbit(T, 30, FILL_EL, 3000), T, 0.25)
    area_e('bgwash', BGWASH_SIZE, (0, -400, 3000), (0, 2200, BGWASH_Z), BGWASH_E, BGWASH, camera=False, spec=False)
    area_e('back', (80, 600), (450, 150, BACK_Z), (0, 0, 138), BACK_E, camera=False)
    if lit:
        pass
    sc.view_settings.view_transform = 'Khronos PBR Neutral'
    sc.view_settings.look = 'None'
    sc.view_settings.exposure = 0.15
    return 40.0                                           # the slab's top


def iron_core_scene(shot):
    global KEY_EL, BGWASH_Z, BGWASH, BGWASH_SIZE, BGWASH_E, SKY
    KEY_EL, BGWASH_Z, BGWASH = 50, 0, '#FFFFFF'           # round 2: the wash white, smaller, weaker; the sky cooler
    BGWASH_SIZE, BGWASH_E, SKY = (1400, 700), 1.9, '#DAD8D4'
    pt.reset()
    top = core_rig()
    global CORE
    CORE = dict(R=80.0, base=(60.0, 30.0))                 # Core's own base: 120 across, 30 tall
    zc = iron(z_base=top + LIFT)
    if shot in ('core', 'core_macro'):
        # iron-core critic round 1 (5.0): black flags either side for the ball's silhouette; a softbox behind the camera
        # for the etched kamacite to catch; a white card on the floor for the base's face (set in core_rig's globals:
        # the wash neutral and lower, the key higher)
        for sx in (-1, 1):
            f = pt.block(f'flag{sx}', 400, 2, 0, 700, pt.principled(f'flag{sx}', '#060606', rough=1.0, spec=0.0), bevel=0)
            f.location = (sx * 0.24, 0.0, (top + 0.5) * MM)
            f.rotation_euler.z = math.radians(90)
        d = math.dist((-180, -1500, 300), (0, 0, zc)) * MM
        sb = pt.area('softbox', (-180, -1500, 300), (0, 0, zc), (2600, 1600), 1.1 * math.pi * d * d, '#FFF8F0')
        sb.visible_camera = False
        # the white floor card read as a band across the frame's foot: a low soft strip the camera cannot see instead
        lo = pt.area('lowcard', (0, -300, top + 20), (0, 0, top + 18), (500, 60), 1.5, '#FFF8F0')
        lo.visible_camera = False
        # light linking: the strip lights the base only (the slice mirrored it as a bar across the etch, round 2 proof)
        col = bpy.data.collections.new('lowcard_receivers')
        col.objects.link(bpy.data.objects['base'])
        lo.light_linking.receiver_collection = col
    bpy.data.materials['ledring'].node_tree.nodes['Emission'].inputs['Strength'].default_value = 0.0   # unlit
    if shot == 'core':
        pt.camera((-160, -620, 168), (0, 0, 148), lens=75, fstop=5.6, focus=math.dist((-160, -620, 168), (0, 0, zc)))
    else:                                                  # core_macro: the same light, closer, on the slice
        pt.camera((-60, -330, zc + 6), (0, 0, zc), lens=100, fstop=8, focus=332)
    return zc


SCENES['iron_core'] = iron_core_scene


def black_paper(name='sleeve_paper'):
    """A record sleeve's black board: ambientCG Paper005 (CC0) for its tooth and sheen, its colour black."""
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
    import assets
    m = assets.pbr(bpy, 'acg:Paper005', '2K', scale=0.25, name=name, bump=0.6)
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    for l in list(nt.links):
        if l.to_socket == b.inputs['Base Color']:
            nt.links.remove(l)
    b.inputs['Base Color'].default_value = (0.012, 0.012, 0.013, 1)
    return m


def stamper_core_scene(shot):
    # stamper-core critic round 1 (4.0): the wash white; the fill higher for a sheen on the sleeve; the back light lower
    # and stronger to carry light through the block; the marble rougher; a strip the shard mirrors
    global BGWASH, FILL_EL, BACK_Z, BACK_E, MARBLE_ROUGH
    BGWASH, FILL_EL, BACK_Z, BACK_E, MARBLE_ROUGH = '#FFFFFF', 28, 110, 3.5, 0.85
    pt.reset()
    top = core_rig()
    d = math.dist((430, -900, 130), (0, -31, 75)) * MM
    st = pt.area('strip', (430, -900, 130), (0, -31, 75), (700, 180), 0.35 * math.pi * d * d, '#FFFFFF')
    st.visible_camera = False
    # water-clear, no Smoke base (2026-11-01): seen from above, the light crossed the 3 mm Smoke stratum twice and the
    # whole block read black; the edition is now Bedrock in Fog, the brand's water-clear
    bedrock(z0=top + LIFT, sleeve_mat=black_paper(), smoke=False)
    T = (0, -10, top + 50)
    if shot == 'core':
        pt.camera((-430, -760, top + 620), (0, -10, top + 60), lens=70)
    else:
        pt.area('front', (60, -420, top + 470), (0, -31, top + 34), (700, 140), 9, '#FFF6EC')
        pt.camera((-60, -380, top + 66), (0, -31, top + 34), lens=100, fstop=11)


SCENES['stamper_core'] = stamper_core_scene


if __name__ == '__main__':
    a = pt.args()
    ed, shot, out = a[0], a[1], a[2]
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    samples = int(a[a.index('--samples') + 1]) if '--samples' in a else 256
    exposure = float(a[a.index('--exposure') + 1]) if '--exposure' in a else 0.0
    SCENES[ed](shot)
    w, h = (1600, 2000) if ed == 'iron_core' and shot == 'core' else (1800, 1200)
    pt.render(out, w, h, samples=samples, scale=scale, exposure=exposure or bpy.context.scene.view_settings.exposure)
