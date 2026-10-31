"""Path-traced renders of the six new objects (Blender Cycles). Run with python3.11 (bpy):
  python3.11 render_objects.py --shot moho [--scale 0.4 --samples 32]
Tints are volumes calibrated from TruCast's published light transmission (LT) at 1/8" (3.175 mm), R1 (r46-owner-notes,
read 2026-10-31): Beer-Lambert per channel, keeping each tint's hue, with about 8% lost at the two surfaces. IOR 1.49.
Polished faces are smooth; sawn faces satin. Bonded layers sit 0.15 mm apart, as a bond line does (and coplanar faces
of two solids render black in Cycles). Path-traced caustics (not MNEE, which ignores the tint). Units: meters."""
import argparse, math, os, sys
import bpy, bmesh
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# code, LT at 3.175 mm (TruCast unless noted), the tint's hue (as rendered "in light")
TINTS = {
    'ember': ('2423 Red', 0.141, '#C92118'),
    'dust': ('2422 Amber', 0.591, '#E06718'),
    'acid': ('2208 Yellow', 0.60, '#E2AA15'),     # TruCast not published; Chemcast 90.7%: est.
    'poison': ('2092 Green', 0.186, '#367424'),
    'ice': ('2069 Light Blue', 0.576, '#2584BE'),
    'haze': ('373 Purple', 0.074, '#5B3197'),
    'fog': ('3030 Glass Green', 0.868, '#D5DFE0'),
    'smoke': ('2064 Gray', 0.293, '#57545F'),
    'clear': ('0000 Clear', 0.92, '#F2F6F4'),     # no tint: only the two surfaces' loss
}
# Lighter custom pours for thick parts (est.: a mill pour at a lower dye loading; captioned "custom pour" wherever used)
POUR = {'ember': 0.80, 'smoke': 0.82, 'haze': 0.76, 'poison': 0.80, 'ice': 0.885, 'dust': 0.88, 'acid': 0.885}
T_REF, SURF = 0.003175, 0.92
GAP = 0.0001   # bonded layers sit 0.1 mm apart behind transparent bond faces: an overlap corrupts Cycles' volume stack (rays leave still tinted, so stacks go black), and coplanar faces render black

def srgb_lin(h):
    c = np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def sigma(tint):
    """Absorption per meter for R, G, B so that 3.175 mm transmits the tint's hue at its published LT
    ('ember-pour' etc.: the same hue at the lighter custom pour's LT)."""
    base = tint.replace('-pour', '')
    _, lt, hx = TINTS[base]
    if tint.endswith('-pour'):
        lt = POUR[base]
    c = np.clip(srgb_lin(hx), 1e-4, 1)
    target = min(0.999, lt / SURF)
    Y = lambda t: 0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]
    lo, hi = 0.0, 50.0
    for _ in range(80):
        a = (lo + hi) / 2
        lo, hi = (a, hi) if Y(c ** a) > target else (lo, a)
    T = c ** ((lo + hi) / 2)
    return -np.log(np.clip(T, 1e-6, 1)) / T_REF

def lin(h):
    return tuple(srgb_lin(h)) + (1.0,)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.use_denoising = True
    sc.cycles.caustics_refractive = True
    sc.cycles.caustics_reflective = True
    sc.cycles.max_bounces = 48; sc.cycles.transmission_bounces = 48; sc.cycles.volume_bounces = 4
    sc.cycles.glossy_bounces = 8; sc.cycles.transparent_max_bounces = 128   # every bond face is a transparent bounce
    sc.cycles.blur_glossy = 0.3
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = lin('#16151A')
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.15
    return sc

def acrylic(tint, edge='polished'):
    """edge: 'polished' (glass), 'saw' (satin glass) or 'bond' (an index-matched cemented joint: no refraction, the same
    volume; Cycles has no nested-IOR priority, so a real bond's near-invisibility is modelled as a transparent face)."""
    name = f'acr-{tint}-{edge}'
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    if edge == 'bond':   # tested 2026-10-31: a transparent bond face turns a stack black in bands; a glass face over a
        bpy.data.materials.remove(m)   # 0.1 mm gap reads as a laminate, faint countable lines (the hybrid shader keeps
        return acrylic(tint, 'polished')   # shadows and inner rays straight, so no TIR darkening)
    if False:
        nt.nodes.remove(nt.nodes['Principled BSDF'])
        tb = nt.nodes.new('ShaderNodeBsdfTransparent')
        nt.links.new(tb.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
        s_ = sigma(tint); D = float(s_.max())
        v = nt.nodes.new('ShaderNodeVolumeAbsorption')
        v.inputs['Color'].default_value = tuple(1 - s_ / D) + (1.0,); v.inputs['Density'].default_value = D
        nt.links.new(v.outputs[0], nt.nodes['Material Output'].inputs['Volume'])
        return m
    p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (1, 1, 1, 1)
    p.inputs['Transmission Weight'].default_value = 1.0
    p.inputs['IOR'].default_value = 1.49
    p.inputs['Roughness'].default_value = 0.0 if edge == 'polished' else 0.32
    # Light paths: shadow and diffuse rays pass a transparent face, so the volume colors the shadow by the true path
    # length (Cycles cannot sample a light through refraction cleanly; MNEE ignores volumes). Camera and glossy rays
    # see the glass.
    lp = nt.nodes.new('ShaderNodeLightPath'); mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'
    nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); nt.links.new(lp.outputs['Is Glossy Ray'], mx.inputs[1])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(mx.outputs[0], mix.inputs['Fac']); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(p.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
    s = sigma(tint); D = float(s.max())
    v = nt.nodes.new('ShaderNodeVolumeAbsorption')
    v.inputs['Color'].default_value = tuple(1 - s / D) + (1.0,)
    v.inputs['Density'].default_value = D
    nt.links.new(v.outputs[0], nt.nodes['Material Output'].inputs['Volume'])
    return m

def basic(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0, noise=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = lin(color)
    p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    if emit:
        p.inputs['Emission Color'].default_value = lin(emit); p.inputs['Emission Strength'].default_value = strength
    if noise:
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 400
        b = nt.nodes.new('ShaderNodeBump'); b.inputs['Strength'].default_value = noise
        nt.links.new(n.outputs['Fac'], b.inputs['Height']); nt.links.new(b.outputs['Normal'], p.inputs['Normal'])
    return m

def emitter(name, color, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = lin(color); e.inputs['Strength'].default_value = strength
    nt.links.new(e.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
    return m

def mesh_obj(name, bm, mats):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    for m in mats: o.data.materials.append(m)
    for poly in o.data.polygons: poly.use_smooth = False
    return o

USE_MNEE = False   # Cycles' MNEE shadow caustics ignore volume absorption (a tinted disc throws a white caustic; the
                   # lamps lane, 2026-10-31). Path-traced caustics (caustics_refractive) carry the tint, so they are used instead.

def caustic(o, caster=True, receiver=False):
    if not USE_MNEE:
        return
    for a, v in (('is_caustics_caster', caster), ('is_caustics_receiver', receiver)):
        try: setattr(o, a, v)
        except Exception: pass

def ring(name, r_out, r_in, z0, h, mat, seg=160, side_mat=None, bond_top=None, bond_bottom=None):
    """A disc or annulus. Caps and walls have their own vertices, so smooth walls don't bend the caps' edge normals."""
    bm = bmesh.new()
    P = lambda r, z: [bm.verts.new((r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)]
    ow0, ow1 = P(r_out, z0), P(r_out, z0 + h)
    for i in range(seg):
        j = (i + 1) % seg
        f = bm.faces.new((ow0[i], ow0[j], ow1[j], ow1[i])); f.material_index = 1; f.smooth = True
    oc0, oc1 = P(r_out, z0), P(r_out, z0 + h)
    if r_in > 0:
        iw0, iw1 = P(r_in, z0), P(r_in, z0 + h)
        for i in range(seg):
            j = (i + 1) % seg
            f = bm.faces.new((iw0[j], iw0[i], iw1[i], iw1[j])); f.material_index = 0; f.smooth = True
        ic0, ic1 = P(r_in, z0), P(r_in, z0 + h)
        for i in range(seg):
            j = (i + 1) % seg
            f = bm.faces.new((oc0[j], oc0[i], ic0[i], ic0[j])); f.material_index = 3
            f = bm.faces.new((oc1[i], oc1[j], ic1[j], ic1[i])); f.material_index = 2
    else:
        f = bm.faces.new(list(reversed(oc0))); f.material_index = 3
        f = bm.faces.new(oc1); f.material_index = 2
    bm.normal_update()
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    for m in (mat, side_mat or mat, bond_top or mat, bond_bottom or mat):
        o.data.materials.append(m)
    caustic(o)
    return o

def slab(name, x0, y0, z0, x1, y1, z1, face_mat, side_mat=None, bond_top=None, bond_bottom=None):
    bm = bmesh.new()
    v = [bm.verts.new(c) for c in ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1))]
    for idx, kind in (((3, 2, 1, 0), 'bot'), ((4, 5, 6, 7), 'top'), ((0, 1, 5, 4), 's'), ((1, 2, 6, 5), 's'), ((2, 3, 7, 6), 's'), ((3, 0, 4, 7), 's')):
        f = bm.faces.new([v[i] for i in idx])
        f.material_index = {'bot': 3 if bond_bottom else 0, 'top': 2 if bond_top else 0, 's': 1 if side_mat else 0}[kind]
    o = mesh_obj(name, bm, [face_mat, side_mat or face_mat, bond_top or face_mat, bond_bottom or face_mat])
    caustic(o)
    return o

def extrude_poly(name, pts, z0, h, mat, axis='z', cap_mat=None):
    """A prism from a 2D outline (x, y) between z0 and z0+h. cap_mat: the two caps' material (e.g. a bond)."""
    bm = bmesh.new()
    b = [bm.verts.new((x, y, z0)) for x, y in pts]; t = [bm.verts.new((x, y, z0 + h)) for x, y in pts]
    n = len(pts)
    bm.faces.new(list(reversed(b))); bm.faces.new(t)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((b[i], b[j], t[j], t[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if cap_mat:
        for f in bm.faces:
            if len(f.verts) > 4: f.material_index = 1
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    o = mesh_obj(name, bm, [mat] + ([cap_mat] if cap_mat else [])); caustic(o)
    return o

def sweep(color='#ECE8E1', rough=0.9, w=6.0, depth=4.0, height=3.0, R=0.6, y_wall=1.2, z0=0.0):
    """A seamless paper sweep: floor to wall through a cove of radius R."""
    prof = [(-depth, 0.0)]
    for i in range(17):
        a = -math.pi / 2 + (math.pi / 2) * i / 16
        prof.append((y_wall - R + R * math.cos(a) + 0.0, R + R * math.sin(a)))
    prof.append((y_wall, height))
    bm = bmesh.new()
    rows = [[bm.verts.new((x, y, z + z0)) for (y, z) in prof] for x in (-w / 2, w / 2)]
    for i in range(len(prof) - 1):
        bm.faces.new((rows[0][i], rows[1][i], rows[1][i + 1], rows[0][i + 1]))
    o = mesh_obj('sweep', bm, [basic('paper', color, rough)])
    for p in o.data.polygons: p.use_smooth = True
    caustic(o, False, True)
    return o

def area(name, loc, target, size, power, color='#FFF3E6', shape='RECTANGLE', size_y=None, caustics=True):
    L = bpy.data.lights.new(name, 'AREA'); L.energy = power; L.color = lin(color)[:3]
    L.shape = shape; L.size = size
    if size_y: L.size_y = size_y
    try: L.cycles.is_caustics_light = caustics and USE_MNEE
    except Exception: pass
    o = bpy.data.objects.new(name, L); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    try: o.visible_camera = False
    except Exception: pass
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o

def spot(name, loc, target, power, angle=25, radius=0.004, color='#FFF1E0'):
    L = bpy.data.lights.new(name, 'SPOT'); L.energy = power; L.color = lin(color)[:3]
    L.spot_size = math.radians(angle); L.spot_blend = 0.3; L.shadow_soft_size = radius
    try: L.cycles.is_caustics_light = USE_MNEE
    except Exception: pass
    o = bpy.data.objects.new(name, L); bpy.context.scene.collection.objects.link(o)
    o.location = loc; d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o

def camera(loc, target, lens=50, fstop=0.0, focus=None):
    c = bpy.data.cameras.new('cam'); c.lens = lens
    if fstop:
        c.dof.use_dof = True; c.dof.aperture_fstop = fstop; c.dof.focus_distance = focus or (Vector(target) - Vector(loc)).length
    o = bpy.data.objects.new('cam', c); bpy.context.scene.collection.objects.link(o)
    o.location = loc; d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = o
    return o

# ---------------------------------------------------------------------------------------------------------- the shots
def shot_moho(sc):
    sweep('#A69E94', 0.85, z0=-0.075, y_wall=0.9, R=0.4)   # critic r1 c5: darker, so the clear top separates
    sc.view_settings.look = 'AgX - Base Contrast'           # critic r1 c6
    # Mantle, as far as the frame needs it: the plinth and platter in Dust (2422), the record, the spindle
    slab('plinth', -0.235, -0.19, -0.075, 0.235, 0.19, -0.049, acrylic('dust-pour'))
    ring('platter', 0.155, 0, -0.047, 0.025, acrylic('dust-pour'))
    rec = basic('vinyl', '#0C0B0E', 0.14)   # critic r1 c4 (grooves as bump, anisotropic sheen) tried: at this distance it greyed the whole disc, so not kept
    ring('record', 0.1524, 0.0036, -0.0021, 0.0020, rec)
    ring('label', 0.0505, 0.0036, -0.0002, 0.0001, basic('label', '#2C3442', 0.65))
    ring('label-ring', 0.040, 0.0385, -0.0001, 0.00005, basic('label-ink', '#C9C2B6', 0.6))
    ring('spindle', 0.0036, 0, -0.047, 0.060, basic('steel', '#C9CCCF', 0.15, 1.0))
    t = ['dust-pour', 'acid-pour', 'ice-pour', 'clear']
    for i, tn in enumerate(t):
        ring(f'moho{i}', 0.033, 0.0125, i * 0.0127 + GAP / 2, 0.0127 - GAP, acrylic(tn),
             bond_top=acrylic(tn, 'bond') if i < 3 else None, bond_bottom=acrylic(tn, 'bond') if i > 0 else None)
    ring('brass', 0.01245, 0.0039, 0.0002, 4 * 0.0127 - 0.0006, basic('brass', '#B8923F', 0.22, 1.0))
    sc.render.resolution_x, sc.render.resolution_y = 1800, 1200
    win = area('window', (-0.9, 1.3, 0.35), (0, 0, 0.02), 0.9, 1400, '#FFF4E6'); win.visible_glossy = False   # flagged off the record's mirror   # daylight from behind left: edges glow, shadows fall forward
    area('key', (0.75, -0.6, 0.30), (0, 0, 0.025), 0.8, 90, '#EEF2F8')     # critic r1 c3: lower, stronger
    flag = slab('flag', -1.0, 0.30, -0.07, 1.0, 0.32, 0.6, basic('flag', '#0A0A0B', 0.9))   # c5: a black flag that only the record and polished tops mirror
    for v in ('visible_camera', 'visible_shadow', 'visible_diffuse', 'visible_transmission'): setattr(flag, v, False)
    card = slab('fillcard', -0.32, -0.30, -0.002, -0.30, -0.10, 0.25, basic('card', '#F4F1EC', 0.9)); card.visible_camera = False
    rim = area('rim', (-0.17, 0.30, 0.07), (0, 0, 0.025), 0.12, 180, '#FFE8D0'); rim.visible_glossy = False   # its mirror image on the record greyed the vinyl   # critic r1 c1: straight through the layers at camera
    camera((0.28, -0.50, 0.13), (0.0, 0.0, 0.034), lens=100, fstop=8)       # critic r1 c2: the puck on the lower third

def shot_lithos(sc):
    # a room corner: oak floor, two plaster walls, a stack of books for scale, window light from the left
    slab('floor', -1.5, -2.5, -0.03, 1.5, 0.8, 0.0, basic('oak', '#9A7650', 0.5, noise=0.04))
    slab('wallB', -1.5, 0.8, 0, 1.5, 0.85, 3, basic('plaster', '#DCD5CA', 0.9, noise=0.1))
    slab('wallL', -1.55, -2.5, 0, -1.5, 0.85, 3, basic('plaster2', '#DCD5CA', 0.9, noise=0.1))
    ring('base', 0.16, 0, 0, 0.02, basic('steel-black', '#1B1A1C', 0.35, 0.8))
    counts = [11, 8, 12, 9, 16, 7, 14, 10]
    tints = ['smoke-pour', 'haze-pour', 'ice-pour', 'poison-pour', 'acid-pour', 'dust-pour', 'clear', 'ember-pour']   # bottom to top
    P = 0.0127
    z = 0.02
    guides = []
    def guide(z):
        ring(f'guide{len(guides)}', 0.055, 0.0385, z + GAP / 2, 0.0056 - GAP, acrylic('fog'),
             bond_top=acrylic('fog', 'bond'), bond_bottom=acrylic('fog', 'bond') if z > 0.021 else None)
        guides.append(z)
    for b, (n, tn) in enumerate(zip(counts, tints)):
        guide(z); z += 0.0056
        satin = acrylic(tn, 'saw') if b % 2 else None   # as Core Sample: bands buffed clear or bead-blasted satin
        ring(f'band{b}', 0.055, 0.038, z + GAP / 2, n * P - GAP, acrylic(tn), side_mat=satin, bond_top=acrylic(tn, 'bond'), bond_bottom=acrylic(tn, 'bond'))
        z += n * P
    guide(z); z += 0.0056
    top = z
    ring('opal', 0.037, 0.034, 0.02, top - 0.02, basic('mask', '#EDEAE4', 0.5))   # the filament's opal tube, masked between the guides
    for i, gz in enumerate(guides):
        ring(f'slot{i}', 0.0372, 0.0368, gz + 0.0006, 0.0044, emitter(f'slot{i}', '#FFB46E', 220))
    ring('uplight', 0.03, 0, top - 0.004, 0.002, emitter('up', '#FFD2A0', 80))
    for i, (w, d, h, c) in enumerate([(0.24, 0.17, 0.035, '#3E4A5A'), (0.22, 0.16, 0.03, '#C8BBA4'), (0.2, 0.15, 0.028, '#7A2E25'), (0.19, 0.13, 0.025, '#2E2B28')]):
        zb = sum(x[2] for x in [(0.24, 0.17, 0.035), (0.22, 0.16, 0.03), (0.2, 0.15, 0.028), (0.19, 0.13, 0.025)][:i])
        o = slab(f'book{i}', -w / 2, -d / 2, zb, w / 2, d / 2, zb + h, basic(f'bk{i}', c, 0.7))
        o.location = (0.34, -0.12, 0); o.rotation_euler = (0, 0, 0.3 + 0.08 * i)
    sc.render.resolution_x, sc.render.resolution_y = 1200, 1800
    area('window', (-1.45, -0.6, 1.5), (0.0, 0.0, 0.6), 1.4, 420, '#FFF1E2', size_y=1.0)
    area('fill', (1.2, -2.2, 1.0), (0, 0, 0.6), 1.2, 40, '#DDE6F2')
    camera((0.75, -2.05, 0.85), (0.08, 0, 0.6), lens=42, fstop=0)

def shot_ionos(sc):
    sc.world.node_tree.nodes['Background'].inputs['Color'].default_value = lin('#D9D3CA')
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.55   # the room around the sideboard
    sweep('#D6CFC4', 0.85, z0=-0.04, y_wall=0.6, R=0.3)
    slab('sideboard', -0.6, -0.3, -0.04, 0.6, 0.25, 0.0, basic('limestone', '#E4DED3', 0.55, noise=0.08))
    card = slab('card', -0.3, -0.75, 0.0, 0.3, -0.74, 0.4, basic('card', '#F4F1EC', 0.9)); card.visible_camera = False
    tn = 'ice-pour'
    W, D, L = 0.2, 0.11, 0.0127
    x0, y0 = -W / 2, -D / 2
    for i in range(9):
        z0 = i * L + GAP / 2; z1 = (i + 1) * L - GAP / 2
        bt = 'fog' if i == 4 else tn
        mat = acrylic(bt); b = acrylic(bt, 'bond')
        slab(f'layer{i}', x0, y0, z0, x0 + W, y0 + D, z1, mat, bond_top=b if i < 8 else None, bond_bottom=b if i > 0 else None)
    # the top disc, the tuner: 24 detent marks round its rim, read against a lit index at the front edge
    ring('disc', 0.05, 0, 9 * L + 0.0004, 0.0127, acrylic('ice-pour'))
    for k in range(24):
        a = 2 * math.pi * k / 24
        o = slab(f'tick{k}', -0.0006, -0.004, 0, 0.0006, 0.0, 0.0004, basic('etch', '#F3F1EC', 0.4))
        o.rotation_euler = (0, 0, a); o.location = (0.046 * math.sin(a), -0.046 * math.cos(a) + 0.0, 9 * L + 0.0131)
    slab('index', -0.0012, y0 + 0.004, 9 * L - 0.0003, 0.0012, y0 + 0.01, 9 * L + 0.0002, emitter('index', '#FFD9B0', 25))
    slab('backplate', -0.045, y0 + D + 0.0002, 0.004, 0.045, y0 + D + 0.0032, 0.030, basic('alu', '#8E9196', 0.35, 1.0))
    # the machined pocket, honestly: the electronics in a black anodized tray, in the bottom two layers, seen through the block
    slab('tray', -0.06, -0.035, 0.003, 0.06, 0.045, 0.024, basic('tray', '#1C1B1E', 0.4, 0.6))
    sc.render.resolution_x, sc.render.resolution_y = 1800, 1200
    area('window', (-1.1, 0.9, 0.7), (0, 0, 0.06), 0.9, 500, '#FFF4E6')
    area('rim', (0.6, 0.7, 0.35), (0, 0, 0.12), 0.5, 260, '#FFE8D0')
    area('key', (0.5, -0.9, 0.8), (0, 0, 0.06), 0.8, 25, '#EEF2F8')
    camera((0.30, -0.56, 0.31), (0.0, -0.005, 0.075), lens=70, fstop=5.6)

def shot_cairn(sc):
    sweep('#C9C2B6', 0.9)
    slabs = [(0.16, 0.12, 0.0, 'fog'), (0.14, 0.11, 0.008, 'fog'), (0.12, 0.10, -0.006, 'dust'), (0.10, 0.09, 0.009, 'fog'), (0.08, 0.08, -0.004, 'fog')]
    cols = ['#3A3634', '#5C5650', '#C8BBA4', '#2F3B4A', '#8A7F70', '#1E1E22']
    rng = np.random.default_rng(3)
    books = [(float(rng.uniform(0.024, 0.038)), float(rng.uniform(0.2, 0.245)), float(rng.uniform(0.13, 0.155))) for _ in cols]
    span = sum(b[0] + 0.001 for b in books)
    for side, sgn in (('L', -1), ('R', 1)):
        cx = sgn * (span / 2 + 0.08)
        for i, (w, d, off, tn) in enumerate(slabs):
            z0 = i * 0.0127 + GAP / 2
            x = cx - sgn * off
            slab(f'c{side}{i}', x - w / 2, -d / 2, z0, x + w / 2, d / 2, (i + 1) * 0.0127 - GAP / 2, acrylic(tn), None,
                 bond_top=acrylic(tn, 'bond') if i < 4 else None, bond_bottom=acrylic(tn, 'bond') if i > 0 else None)
    x = -span / 2
    for (th, hgt, dp), c in zip(books, cols):
        slab(f'book{c}', x, -dp / 2, 0.0, x + th, dp / 2, hgt, basic(f'cloth{c}', c, 0.75))
        x += th + 0.001
    sc.render.resolution_x, sc.render.resolution_y = 1800, 1200
    area('window', (-1.2, 0.9, 0.35), (-span / 2 - 0.08, 0, 0.02), 0.7, 260, '#FFF4E6')
    area('key', (0.4, -1.0, 0.9), (-0.15, 0, 0.04), 1.0, 12, '#EEF2F8')
    camera((-0.02, -0.46, 0.21), (-span / 2 - 0.05, 0, 0.04), lens=50, fstop=8)

def shot_bedrock(sc):
    sc.world.node_tree.nodes['Background'].inputs['Color'].default_value = lin('#D9D3CA')
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.4
    sweep('#C9C2B6', 0.85, w=10.0, depth=6.0)
    prof = [(0, 0), (0.30, 0), (0.30, 0.15), (0.25, 0.15), (0.25, 0.185), (0.18, 0.185), (0.18, 0.215), (0.09, 0.215), (0.09, 0.23), (0, 0.23)]
    tn = 'dust'
    for xi in (-0.235, 0.235 - 0.0254):
        for l in range(2):
            x0 = xi + l * 0.0127 + GAP / 2
            pts = [(y - 0.15, z) for y, z in prof]
            o = extrude_poly(f'plate{xi}{l}', pts, 0, 0.0127 - GAP, acrylic(tn))
            o.rotation_euler = (math.pi / 2, 0, math.pi / 2); o.location = (x0, 0, 0)
    steel = basic('steel', '#BFC3C7', 0.25, 1.0)
    for ry, rz in ((-0.11, 0.03), (0.11, 0.03), (0.0, 0.12)):
        o = ring(f'rail{ry}{rz}', 0.01, 0, -0.2096, 0.4192, steel)
        o.rotation_euler = (0, math.pi / 2, 0); o.location = (0, ry, rz)
    rng = np.random.default_rng(7)
    cols = ['#D8D2C6', '#2B2B30', '#B23A2A', '#E4C36A', '#3E5A78', '#ECE8E1', '#6B5A4A', '#1F3B2F', '#C9C3B6', '#8E8A84']
    x = -0.19
    while x < 0.19:
        th = 0.0034; lean = float(rng.uniform(-0.05, 0.05))
        o = slab(f'lp{x:.3f}', -th / 2, -0.1575, 0.0, th / 2, 0.1575, 0.315, basic(f'sl{x:.3f}', cols[int(rng.integers(len(cols)))], 0.8))
        o.location = (x, 0.0, 0.02); o.rotation_euler = (0, lean, 0)
        x += th + 0.0015
    sc.render.resolution_x, sc.render.resolution_y = 1800, 1200
    area('key', (-1.2, -1.0, 1.3), (0, 0, 0.15), 1.4, 120)
    spot('sun', (-1.1, 0.9, 0.55), (-0.2, -0.1, 0.05), 900, 26, 0.004, '#FFF0DA')   # low daylight from behind: the plates throw amber forward
    area('fill', (1.0, -1.4, 0.6), (0, 0, 0.15), 1.2, 40, '#E6ECF5')
    camera((-0.95, -0.75, 0.42), (0.05, 0, 0.14), lens=50, fstop=0)

def shot_relief(sc):
    from contours import layers
    wall = slab('wall', -2, 0.0, -1, 2, 0.05, 2.5, basic('plaster', '#D9D3C8', 0.9, noise=0.2))
    caustic(wall, False, True)
    k = 0.001; th = 0.0056
    slab('backing', -0.3, -0.006, 0.9, 0.3, 0.0, 1.5, basic('white-back', '#F2F0EC', 0.6))
    base_m = acrylic('fog')
    slab('base', -0.3, -0.006 - th + GAP / 2, 0.9, 0.3, -0.006 - GAP / 2, 1.5, base_m)
    for lev, loops in layers():   # each contour island a prism (the terrain is all hills, so no loop has a hole)
        for li, l in enumerate(loops):
            pts = [(float(x) * k, float(y) * k) for x, y in l[::2]]
            if len(pts) > 2:
                area_ = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
                if area_ < 0: pts = pts[::-1]
            o = extrude_poly(f'lev{lev}-{li}', pts, 0, th - GAP, base_m)
            o.rotation_euler = (math.pi / 2, 0, 0)
            o.location = (0, -0.006 - th - (lev - 1) * th + 0.0, 1.2)
    sc.render.resolution_x, sc.render.resolution_y = 1800, 1200
    area('bar', (0.0, -0.075, 1.53), (0.0, -0.01, 0.95), 0.6, 120, '#FFEEDC', size_y=0.015)   # its LED bar: a line of light just above the top edge, washing down
    area('room', (1.2, -2.2, 1.3), (0, 0, 1.2), 2.0, 60, '#E8EEF6')
    camera((0.55, -1.55, 1.25), (0.0, -0.03, 1.2), lens=50, fstop=0)

def shot_meridian(sc):
    wall = slab('wall', -2, 0.0, -1, 2, 0.05, 3.0, basic('plaster', '#E4DED4', 0.9, noise=0.15))
    cz = 1.45
    def disc(name, r, depth, h, mat, x=0.0, z=cz, r_in=0.0):
        o = ring(name, r, r_in, 0, h, mat)
        o.rotation_euler = (math.pi / 2, 0, 0); o.location = (x, -depth, z)   # thickness runs toward the room
        return o
    disc('face', 0.18, 0.030, 0.0056, acrylic('fog'))
    for i in range(12):   # the marks, cut into the face: thin clear bars standing proud
        a = math.radians(90 - i * 30)
        o = slab(f'mark{i}', -0.0015, -0.0006, -0.006, 0.0015, 0.0, 0.006, acrylic('fog'))
        o.rotation_euler = (0, -a + math.pi / 2, 0)   # radial bars
        o.location = (0.166 * math.cos(a), -0.0356, cz + 0.166 * math.sin(a))
    disc('housing', 0.028, 0.004, 0.024, basic('black-alu', '#18171A', 0.4, 0.7))
    ah, am = math.radians(90 - (2 + 10 / 60) * 30), math.radians(90 - 10 * 6)   # ten past two
    brass = basic('brass', '#B8923F', 0.25, 1.0)
    for nm, ang, rr, depth, tn, cw in (('hour', ah, 0.070, 0.040, 'acid', 0.009), ('minute', am, 0.115, 0.046, 'ice', 0.011)):
        disc(nm, 0.055, depth, 0.0032, acrylic(tn), x=rr * math.cos(ang), z=cz + rr * math.sin(ang))
        L = rr + 0.03
        arm = slab(f'{nm}-arm', -0.03, -0.0028, -0.006, L, 0.0, 0.006, acrylic('fog'))
        arm.rotation_euler = (0, -ang, 0); arm.location = (0, -depth + 0.0028 + 0.0002, cz)
        disc(f'{nm}-weight', cw, depth - 0.0002, 0.006, brass, x=-0.03 * math.cos(ang), z=cz - 0.03 * math.sin(ang))
    disc('hub', 0.006, 0.052, 0.008, brass)
    sc.render.resolution_x, sc.render.resolution_y = 1800, 1200
    area('key', (-1.2, -1.6, 2.0), (0, 0, cz), 1.2, 35)
    spot('rake', (-0.9, -0.55, 2.0), (0.05, -0.03, cz), 380, 20, 0.006, '#FFF1E0')
    area('fill', (1.2, -1.6, 1.3), (0, 0, cz), 1.2, 14, '#E6ECF5')
    camera((0.26, -0.98, 1.38), (0.02, -0.03, cz - 0.005), lens=55, fstop=0)

SHOTS = dict(moho=shot_moho, lithos=shot_lithos, ionos=shot_ionos, cairn=shot_cairn, bedrock=shot_bedrock, relief=shot_relief, meridian=shot_meridian)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--shot', required=True); ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--samples', type=int, default=192); ap.add_argument('--out', default=None)
    a = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
    sc = reset(); SHOTS[a.shot](sc)
    sc.render.resolution_percentage = int(a.scale * 100)
    sc.cycles.samples = a.samples
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = a.out or os.path.join(HERE, 'renders', f'{a.shot}.png')
    bpy.ops.render.render(write_still=True)
    print('wrote', sc.render.filepath)

if __name__ == '__main__':
    main()
