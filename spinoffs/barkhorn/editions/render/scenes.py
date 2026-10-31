"""The editions' scenes, built on pt.py. Usage (on the Python with bpy):

    python3.11 scenes.py -- EDITION SHOT OUT.png [--scale 0.5] [--samples 64]

EDITION: firn | iron | stamper. SHOT: hero | macro.
Geometry is a proposal for the editions (EDITIONS.md); the products' own drawings rule where they differ.
"""
import math
import random
import sys

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import bpy  # noqa: E402
import pt  # noqa: E402
from pt import MM  # noqa: E402

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
    b.inputs['Base Color'].default_value = (0.006, 0.006, 0.007, 1)
    b.inputs['Roughness'].default_value = 0.3
    b.inputs['Anisotropic'].default_value = 0.6
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
    nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    pt.disc('record', r, z0, z0 + t, mat, bevel=0.5)
    pt.disc('label', 50, z0 + t + 0.02, z0 + t + 0.12, pt.principled('label', '#26241F', rough=0.85), bevel=0)
    steel = pt.principled('spindle', '#B8B6B2', rough=0.25, metal=1.0)
    pt.disc('spindle_pin', 3.55, z0 + t, z0 + t + 11.0, steel, bevel=0.6, segs=40)
    return z0 + t


# --- Firn: Moho, the record weight, bubbles by design --------------------------------------------------------------
FIRN = dict(r=40.0, h=36.0, ice=3.0, layers=6, layer=5.0, spindle=(4.0, 12.0))


def firn(z0):
    """Moho in clear with an Ice base and top: six 5 mm clear layers between two 3 mm Ice laminae. At each of the
    five inner bond lines and under the top lamina, lens-shaped air voids from two matching dished pockets: columns of
    them stacked like the air a glacier traps as snow turns to ice."""
    f = FIRN
    zb, zt = z0, z0 + f['h']
    mat = pt.acrylic('firn', 'clear')
    body = pt.disc('moho', f['r'], zb, zt, mat, bevel=1.2, segs=200)
    ice = pt.lamina('ice', 'ice')
    pt.disc('ice_base', f['r'] - 0.05, zb + 0.05, zb + f['ice'], ice, bevel=1.15, segs=200)
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
        pt.cove('#2C2C2F', rough=0.5, radius=500)
        top = record()
        firn(top + LIFT)
        pt.area('overhead', (-60, 160, 620), (0, 0, 20), (700, 420), 26, '#FFF4E6')
        pt.area('key', (-420, -260, 300), (0, 0, 22), 220, 9, '#FFF1E0')
        pt.area('rimL', (-260, 300, 140), (0, 0, 20), (60, 520), 7, '#E8F0FF')
        pt.area('rimR', (280, 280, 160), (0, 0, 20), (60, 520), 9, '#E8F0FF')
        pt.spot('glint', (380, -200, 420), (0, 0, 36), 60, size_mm=6, angle=12)
        pt.block('card', 600, 4, 0, 160, pt.principled('card', '#EEEAE4', rough=0.9), bevel=0, y=-520)
        pt.camera((60, -470, 170), (0, 0, 14), lens=85)
    else:
        pt.cove('#2A2A2D', rough=0.5, radius=400)
        top = record()
        firn(top + LIFT)
        pt.area('overhead', (0, 120, 420), (0, 0, 20), (500, 300), 14, '#FFF4E6')
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
    cr.elements[0].position = 0.3; cr.elements[0].color = (0.20, 0.195, 0.19, 1)
    cr.elements[1].position = 0.85; cr.elements[1].color = (0.92, 0.90, 0.86, 1)
    nt.links.new(im.outputs['Color'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    rr = nt.nodes.new('ShaderNodeMapRange')
    rr.inputs['From Min'].default_value = 0.3; rr.inputs['From Max'].default_value = 0.9
    rr.inputs['To Min'].default_value = 0.6; rr.inputs['To Max'].default_value = 0.22
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
    edge = pt.principled('rind', '#3A332C', rough=0.6, metal=0.6)
    sl = bpy.data.objects['slice']
    sl.data.materials.append(edge)
    for p in sl.data.polygons:
        if abs(p.normal.y) < 0.6:
            p.material_index = 1
    return zc


def iron_scene(shot):
    pt.reset()
    pt.cove('#262628', rough=0.45, radius=600)
    zc = iron()
    if shot == 'hero':
        pt.area('overhead', (-80, 520, 700), (0, 0, zc), 700, 30, '#FFF3E4', shape='DISK')
        pt.area('key', (-700, -220, 460), (0, 0, zc), 300, 26, '#FFF0DE')
        pt.area('front', (0, -1300, zc + 120), (0, 0, zc), (700, 300), 12, '#FFF6EC')
        pt.area('rimL', (-360, 380, 240), (0, 0, zc), (80, 800), 12, '#E6EEFF')
        pt.area('rimR', (380, 360, 260), (0, 0, zc), (80, 800), 14, '#E6EEFF')
        pt.spot('glint', (460, -300, 520), (0, 0, zc + 20), 120, size_mm=8, angle=14)
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
    b.inputs['Roughness'].default_value = 0.035
    b.inputs['Anisotropic'].default_value = 0.45
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
    nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return mat


def bedrock(z0=LIFT):
    """Bedrock in clear with a 3 mm Smoke base stratum: a slot along its top holds a sleeve; in the front, 9 mm behind
    the face, a sector of the stamper (Session 00's lead-in and first track) stands in a pocket 0.2 mm larger."""
    b = BED
    mat = pt.acrylic('bedrock', 'clear')
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
    sleeve = pt.block('sleeve', 314, 3.2, z0 + b['H'] - sd + 0.4, z0 + b['H'] - sd + 314, pt.principled(
        'sleeve', '#141414', rough=0.7), bevel=0.4, y=0)
    return zc


def stamper_scene(shot):
    pt.reset()
    pt.cove('#19191B', rough=0.4, radius=700, height=1600)
    zc = bedrock()
    if shot == 'hero':
        pt.area('overhead', (-60, 260, 900), (0, 0, 60), (1000, 600), 34, '#FFF3E4')
        pt.area('key', (-560, -420, 380), (0, 0, 30), 320, 26, '#FFF0DE')
        pt.area('rimL', (-420, 420, 260), (0, 0, 120), (90, 900), 14, '#E6EEFF')
        pt.area('rimR', (440, 380, 260), (0, 0, 120), (90, 900), 16, '#E6EEFF')
        pt.spot('glint', (420, -460, 300), (0, -31, 34), 220, size_mm=8, angle=12)
        pt.area('front', (-80, -760, 560), (0, -31, 34), (900, 300), 12, '#FFF6EC')
        pt.camera((-260, -600, 125), (0, 0, 52), lens=70)
    else:
        pt.area('overhead', (0, 160, 480), (0, -20, 40), (500, 300), 16, '#FFF3E4')
        pt.area('key', (-280, -300, 180), (0, -30, 34), 180, 10, '#FFF0DE')
        pt.spot('glint', (200, -330, 120), (0, -31, 34), 70, size_mm=5, angle=8)
        pt.area('rimR', (260, 120, 160), (0, -20, 40), (60, 400), 6, '#E6EEFF')
        pt.area('front', (60, -420, 470), (0, -31, 34), (700, 140), 9, '#FFF6EC')
        pt.camera((-60, -380, 66), (0, -31, 34), lens=100, fstop=11)


SCENES = {'firn': firn_scene, 'iron': iron_scene, 'stamper': stamper_scene}

if __name__ == '__main__':
    a = pt.args()
    ed, shot, out = a[0], a[1], a[2]
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    samples = int(a[a.index('--samples') + 1]) if '--samples' in a else 256
    exposure = float(a[a.index('--exposure') + 1]) if '--exposure' in a else 0.0
    SCENES[ed](shot)
    pt.render(out, 1800, 1200, samples=samples, scale=scale, exposure=exposure)
