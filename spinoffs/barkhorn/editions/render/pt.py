"""EARF special editions: a small Cycles kit for tinted cast acrylic with things inside it.

Runs on the Python that has bpy (python3.11 here). Units: the scene is in metres; every function takes millimetres.

The physics, kept simple and honest:
- Acrylic is a Principled BSDF, fully transmissive, IOR 1.49, roughness near 0 (polished), with a Volume Absorption
  inside it. The absorption per channel comes from A&C Plastics' TruCast light-transmission chart (TT % at 1/8 in,
  https://www.acplasticsinc.com/wp-content/uploads/2026/08/Trucast-Acrylic-Light-Transmissions-5.26.26-1.pdf,
  accessed 2026-10-31): the internal transmittance TT / 0.92 (two faces' Fresnel loss) is matched in luminance at
  3.175 mm, and split across the channels in the brand's hue for the tint (companions/common.py GLOW).
- An air bubble is a closed mesh with its normals turned inward, wearing the host's material: a ray inside the
  acrylic meets a back face and leaves into air (1.49 -> 1.0), so past 42 degrees it reflects totally and the
  bubble's rim reads silver, as it does in a real casting. The volume stack ends inside it, so air does not absorb.
- An inclusion is an opaque or translucent mesh inside the acrylic. Rays reach it by refraction.
- Caustics are path traced (refractive and reflective caustics on, filter glossy low); no MNEE, which ignores volume
  absorption.
"""
import math
import sys

import bpy
import bmesh
from mathutils import Vector, Matrix

MM = 0.001

# --- tints ------------------------------------------------------------------------------------------------------------
# key: (TruCast code used as the reference, TT % at 1/8 in from A&C's chart, the hue as sRGB hex)
TINTS = {
    'clear':  ('0000', 93.0, '#F2FAF8'),
    'fog':    ('2515', 69.1, '#E9ECEE'),   # light grey transparent
    'ice':    ('2069', 57.6, '#4FB8FF'),   # tinted blue transparent
    'acid':   ('2422', 59.1, '#FFC93A'),   # amber transparent (the nearest light warm yellow on the chart)
    'smoke':  ('2064', 29.3, '#A8A8A8'),   # light grey / smoke: neutral (a warm grey turned amber over long paths)
    'poison': ('2092', 18.6, '#6BD45A'),   # green
    'ember':  ('2283', 12.3, '#FF4A3A'),   # red
    'dust':   ('2119', 5.8, '#FF8A3A'),    # orange
    'haze':   ('2423', 14.1, '#9A6BFF'),   # (violet: no named violet on the chart; the code is a stand-in)
}


def srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_lin(h):
    h = h.lstrip('#')
    return [srgb_to_lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]


def sigma_per_mm(key, thin=1.0):
    """Absorption coefficients (per mm, linear R, G, B) for a tint. `thin` scales them (a lamina cast lighter)."""
    _, tt, hue = TINTS[key]
    t_int = min(tt / 92.0, 0.999)
    if key == 'clear':                                   # cast PMMA itself: a whisper of green-cyan over 100 mm
        return [0.00012 * thin, 0.00006 * thin, 0.00008 * thin]   # cast PMMA: a faint cyan over a metre
    h = hex_lin(hue)
    m = max(h)
    shape = [-math.log(max(c / m, 0.02)) + 0.05 for c in h]     # how much faster each channel goes than the hue's own
    d = 3.175

    def lum(s):
        r, g, b = (math.exp(-s * k * d) for k in shape)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    lo, hi = 0.0, 50.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if lum(mid) > t_int:
            lo = mid
        else:
            hi = mid
    s = (lo + hi) / 2
    return [s * k * thin for k in shape]


# --- scene ------------------------------------------------------------------------------------------------------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.render.engine = 'CYCLES'
    cy = sc.cycles
    cy.device = 'CPU'
    cy.caustics_refractive = True
    cy.caustics_reflective = True
    cy.blur_glossy = 0.2
    cy.max_bounces = 28
    cy.transmission_bounces = 24
    cy.glossy_bounces = 16
    cy.diffuse_bounces = 4
    cy.volume_bounces = 2
    cy.transparent_max_bounces = 16
    cy.use_denoising = True
    cy.denoiser = 'OPENIMAGEDENOISE'
    cy.sample_clamp_indirect = 20.0
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.world = bpy.data.worlds.new('world')
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.02, 0.02, 0.022, 1)
    bg.inputs['Strength'].default_value = 1.0
    return sc


def _nodes(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    return nt, out


def acrylic(name, tint='clear', thin=1.0, rough=0.0, frost=0.0):
    """Polished cast acrylic in a tint. `frost` (0..1) is a bead-blasted face (rough transmission)."""
    mat = bpy.data.materials.new(name)
    nt, out = _nodes(mat)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (1, 1, 1, 1)
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['IOR'].default_value = 1.49
    b.inputs['Roughness'].default_value = max(rough, frost * 0.35)
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    s = sigma_per_mm(tint, thin)
    D = max(s) / MM                                    # Blender: per metre
    ab = nt.nodes.new('ShaderNodeVolumeAbsorption')
    ab.inputs['Density'].default_value = D
    ab.inputs['Color'].default_value = tuple(1.0 - (c / MM) / D for c in s) + (1.0,)
    nt.links.new(ab.outputs['Volume'], out.inputs['Volume'])
    return mat


def principled(name, color, rough=0.5, metal=0.0, sss=0.0, sss_radius=(1, 0.5, 0.3), transmission=0.0, ior=1.45,
               coat=0.0, bump=None, spec=0.5, emission=None):
    mat = bpy.data.materials.new(name)
    nt, out = _nodes(mat)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = tuple(hex_lin(color)) + (1,)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['IOR'].default_value = ior
    b.inputs['Specular IOR Level'].default_value = spec
    b.inputs['Transmission Weight'].default_value = transmission
    b.inputs['Coat Weight'].default_value = coat
    if sss:
        b.inputs['Subsurface Weight'].default_value = sss
        b.inputs['Subsurface Radius'].default_value = sss_radius
        b.inputs['Subsurface Scale'].default_value = 0.002
    if emission:
        b.inputs['Emission Color'].default_value = tuple(hex_lin(emission[0])) + (1,)
        b.inputs['Emission Strength'].default_value = emission[1]
    if bump:                                             # (scale per metre, strength, detail)
        tex = nt.nodes.new('ShaderNodeTexNoise')
        tex.inputs['Scale'].default_value = bump[0]
        tex.inputs['Detail'].default_value = bump[2] if len(bump) > 2 else 6
        bm = nt.nodes.new('ShaderNodeBump')
        bm.inputs['Strength'].default_value = bump[1]
        bm.inputs['Distance'].default_value = 0.0005
        nt.links.new(tex.outputs['Fac'], bm.inputs['Height'])
        nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return mat


def emitter(name, color, strength):
    mat = bpy.data.materials.new(name)
    nt, out = _nodes(mat)
    e = nt.nodes.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = tuple(hex_lin(color)) + (1,)
    e.inputs['Strength'].default_value = strength
    nt.links.new(e.outputs['Emission'], out.inputs['Surface'])
    return mat


# --- meshes -----------------------------------------------------------------------------------------------------------
def _obj_from_bm(name, bm, mat=None, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    if smooth:
        for p in ob.data.polygons:
            p.use_smooth = True
    return ob


def bevel_mod(ob, width_mm, segs=4, angle=40):
    m = ob.modifiers.new('bevel', 'BEVEL')
    m.width = width_mm * MM
    m.segments = segs
    m.limit_method = 'ANGLE'
    m.angle_limit = math.radians(angle)
    m.harden_normals = False
    return m


def disc(name, r, z0, z1, mat, segs=160, bevel=0.8, x=0.0, y=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=segs, radius1=r * MM, radius2=r * MM,
                          depth=(z1 - z0) * MM)
    bmesh.ops.translate(bm, vec=(x * MM, y * MM, (z0 + z1) / 2 * MM), verts=bm.verts)
    ob = _obj_from_bm(name, bm, mat, smooth=False)
    if bevel:
        bevel_mod(ob, bevel)
        ob.modifiers.new('wn', 'WEIGHTED_NORMAL').keep_sharp = True
    _autosmooth(ob)
    return ob


def block(name, sx, sy, z0, z1, mat, bevel=1.0, x=0.0, y=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx * MM, sy * MM, (z1 - z0) * MM), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(x * MM, y * MM, (z0 + z1) / 2 * MM), verts=bm.verts)
    ob = _obj_from_bm(name, bm, mat, smooth=False)
    if bevel:
        bevel_mod(ob, bevel)
        ob.modifiers.new('wn', 'WEIGHTED_NORMAL').keep_sharp = True
    _autosmooth(ob)
    return ob


def _autosmooth(ob):
    for p in ob.data.polygons:
        p.use_smooth = True
    try:
        m = ob.modifiers.new('smooth', 'NODES')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
        ob.modifiers.remove(m)
    except Exception:
        pass


def ellipsoid(name, c, r, mat, rot=(0, 0, 0), inward=False, subdiv=4):
    """An ellipsoid at c (mm) with radii r (mm). inward=True turns it into a void (a bubble) in its host."""
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    bmesh.ops.scale(bm, vec=(r[0] * MM, r[1] * MM, r[2] * MM), verts=bm.verts)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(rot[2]), 3, 'Z') @
                     Matrix.Rotation(math.radians(rot[1]), 3, 'Y') @ Matrix.Rotation(math.radians(rot[0]), 3, 'X'),
                     verts=bm.verts)
    bmesh.ops.translate(bm, vec=(c[0] * MM, c[1] * MM, c[2] * MM), verts=bm.verts)
    if inward:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    return _obj_from_bm(name, bm, mat)


def lens_void(name, c, r, h, mat, segs=48, rings=8):
    """A lens-shaped air void: two shallow spherical caps (radius r in plan, total height h) meeting at a bond line,
    as two matching dished pockets milled into the mating faces trap it. Normals inward (air in acrylic)."""
    bm = bmesh.new()
    R = (r * r + (h / 2) ** 2) / h                       # the sphere each cap is cut from
    verts_rings = []
    top = bm.verts.new((c[0] * MM, c[1] * MM, (c[2] + h / 2) * MM))
    bot = bm.verts.new((c[0] * MM, c[1] * MM, (c[2] - h / 2) * MM))
    for side in (1, -1):
        rs = []
        for i in range(1, rings + 1):
            rr = r * i / rings
            z = math.sqrt(max(R * R - rr * rr, 0)) - (R - h / 2)
            ring = [bm.verts.new(((c[0] + rr * math.cos(2 * math.pi * k / segs)) * MM,
                                  (c[1] + rr * math.sin(2 * math.pi * k / segs)) * MM,
                                  (c[2] + side * z) * MM)) for k in range(segs)]
            rs.append(ring)
        verts_rings.append(rs)
    for side, rs, pole in ((1, verts_rings[0], top), (-1, verts_rings[1], bot)):
        for k in range(segs):
            f = (pole, rs[0][k], rs[0][(k + 1) % segs]) if side > 0 else (pole, rs[0][(k + 1) % segs], rs[0][k])
            bm.faces.new(f)
        for i in range(rings - 1):
            for k in range(segs):
                a, b2 = rs[i][k], rs[i][(k + 1) % segs]
                c2, d = rs[i + 1][(k + 1) % segs], rs[i + 1][k]
                bm.faces.new((a, d, c2, b2) if side > 0 else (a, b2, c2, d))
    # the rim: join the outermost rings
    top_r, bot_r = verts_rings[0][-1], verts_rings[1][-1]
    for k in range(segs):
        bm.faces.new((top_r[k], bot_r[k], bot_r[(k + 1) % segs], top_r[(k + 1) % segs]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.reverse_faces(bm, faces=bm.faces)          # air: normals point into the void
    return _obj_from_bm(name, bm, mat)


def tube_void(name, pts, radius, mat, segs=20, inward=True, closed=False):
    """A round channel (radius mm) along a polyline of points (mm): a drilled or milled channel, sealed, so air."""
    pts = [Vector(p) * MM for p in pts]
    n = len(pts)
    bm = bmesh.new()
    rings = []
    prev_nrm = None
    for i, p in enumerate(pts):
        if closed:
            t = (pts[(i + 1) % n] - pts[(i - 1) % n]).normalized()
        else:
            t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        if prev_nrm is None:
            a = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
            nrm = t.cross(a).normalized()
        else:
            nrm = (prev_nrm - t * prev_nrm.dot(t)).normalized()
        prev_nrm = nrm
        bi = t.cross(nrm)
        rings.append([bm.verts.new(p + (nrm * math.cos(2 * math.pi * k / segs) + bi * math.sin(2 * math.pi * k / segs))
                                   * radius * MM) for k in range(segs)])
    m = n if closed else n - 1
    for i in range(m):
        a, b2 = rings[i], rings[(i + 1) % n]
        for k in range(segs):
            bm.faces.new((a[k], a[(k + 1) % segs], b2[(k + 1) % segs], b2[k]))
    if not closed:
        for ring, p in ((rings[0], pts[0]), (rings[-1], pts[-1])):
            c = bm.verts.new(p)
            for k in range(segs):
                bm.faces.new((c, ring[(k + 1) % segs], ring[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if inward:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    return _obj_from_bm(name, bm, mat)


def rock(name, c, r, mat, seed=1, rough=0.35, subdiv=5, vesicles=0.0, squash=(1, 1, 1)):
    """A rough stone: an icosphere pushed about by noise (and pocked with vesicles, for a cinder)."""
    import random
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    rnd = random.Random(seed)
    from mathutils import noise
    off = Vector((rnd.uniform(0, 100), rnd.uniform(0, 100), rnd.uniform(0, 100)))
    pits = [Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized() for _ in range(int(vesicles))]
    pit_r = [rnd.uniform(0.06, 0.16) for _ in pits]
    for v in bm.verts:
        d = v.co.normalized()
        k = 1.0 + rough * noise.fractal(d * 1.6 + off, 0.6, 2.0, 5) + 0.25 * rough * noise.noise(d * 6 + off)
        for p, pr in zip(pits, pit_r):
            ang = (d - p).length
            if ang < pr:
                k -= 0.12 * (1 - (ang / pr) ** 2)
        v.co = Vector((d.x * k * squash[0], d.y * k * squash[1], d.z * k * squash[2]))
    bmesh.ops.scale(bm, vec=(r * MM, r * MM, r * MM), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(c) * MM, verts=bm.verts)
    return _obj_from_bm(name, bm, mat)


# --- set, lights, camera ----------------------------------------------------------------------------------------------
def cove(color='#1A1A1C', rough=0.55, width=2000, depth=1400, height=1200, radius=350, z=0.0, mat=None):
    """A seamless: a floor curving up into a wall behind (y positive is away from the camera)."""
    bm = bmesh.new()
    prof = []
    for i in range(12):
        prof.append((-depth + (depth - 0) * i / 11 * 0.999 - radius * 0, 0.0))
    prof = [(-depth + i * (depth) / 10, 0.0) for i in range(11)]
    for i in range(1, 17):
        a = math.pi / 2 * i / 16
        prof.append((radius * math.sin(a), radius * (1 - math.cos(a))))
    for i in range(1, 8):
        prof.append((radius, radius + (height - radius) * i / 7))
    xs = [-width / 2 + width * i / 20 for i in range(21)]
    grid = [[bm.verts.new((x * MM, (py + 300) * MM, (pz + z) * MM)) for (py, pz) in prof] for x in xs]
    for i in range(len(xs) - 1):
        for j in range(len(prof) - 1):
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = _obj_from_bm('cove', bm, mat or principled('cove', color, rough=rough, spec=0.0))
    for f in ob.data.polygons:
        if f.normal.z < 0 and f.normal.y > -0.5:
            pass
    return ob


def area(name, loc, target, size, power, color='#FFFFFF', shape='RECTANGLE', spread=180):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.shape = shape
    if isinstance(size, (list, tuple)):
        ld.size, ld.size_y = size[0] * MM, size[1] * MM
    else:
        ld.size = size * MM
        ld.size_y = size * MM
        if shape == 'RECTANGLE':
            pass
    ld.energy = power
    ld.color = hex_lin(color)
    ld.spread = math.radians(spread)
    ob = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(loc) * MM
    _aim(ob, Vector(target) * MM)
    return ob


def spot(name, loc, target, power, size_mm=10, angle=30, blend=0.2, color='#FFFFFF'):
    ld = bpy.data.lights.new(name, 'SPOT')
    ld.energy = power
    ld.shadow_soft_size = size_mm * MM
    ld.spot_size = math.radians(angle)
    ld.spot_blend = blend
    ld.color = hex_lin(color)
    ob = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(loc) * MM
    _aim(ob, Vector(target) * MM)
    return ob


def _aim(ob, target):
    d = target - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def camera(loc, target, lens=85, fstop=None, focus=None, sensor=36, shift=(0, 0)):
    cd = bpy.data.cameras.new('cam')
    cd.lens = lens
    cd.sensor_width = sensor
    cd.clip_start = 0.001
    cd.clip_end = 50
    cd.shift_x, cd.shift_y = shift
    ob = bpy.data.objects.new('cam', cd)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(loc) * MM
    _aim(ob, Vector(target) * MM)
    if fstop:
        cd.dof.use_dof = True
        cd.dof.aperture_fstop = fstop
        cd.dof.focus_distance = (focus if focus else (Vector(target) - Vector(loc)).length) * MM
    bpy.context.scene.camera = ob
    return ob


def render(out, w=1800, h=1200, samples=256, scale=1.0, exposure=0.0, seed=0):
    sc = bpy.context.scene
    sc.render.resolution_x = int(w)
    sc.render.resolution_y = int(h)
    sc.render.resolution_percentage = int(scale * 100)
    sc.cycles.samples = samples
    sc.cycles.seed = seed
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.01
    sc.view_settings.exposure = exposure
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGB'
    sc.render.image_settings.color_depth = '8'
    sc.render.filepath = out
    bpy.context.scene.render.threads_mode = 'AUTO'
    bpy.ops.render.render(write_still=True)
    print('wrote', out)


def args():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    return a


def studio(subject_h=60, ground='#4A4846', key=1.0, overhead=1.0, rims=1.0, card=True, warm='#FFF6EA', cool='#EEF4FF',
           wall_range=None, side=-1):
    """The editions' seamless: a warm grey cove, a big overhead softbox a little behind (the bright face every polished
    top reflects), a soft key on the camera's side, two tall strips behind for edge lines, and a white card low in front
    (so the front faces carry a reflection, not black). Powers scale with the subject's size."""
    s = max(subject_h, 30) / 60.0
    cove(ground, rough=0.6, radius=420)
    area('overhead', (0, 120 * s, 700 * s), (0, 0, 0), (900 * s, 600 * s), 60 * overhead * s * s, warm)
    area('key', (side * 520 * s, -380 * s, 420 * s), (0, 0, subject_h * 0.4), 300 * s, 30 * key * s * s, warm)
    for x in (-1, 1):
        area(f'rim{x}', (x * 300 * s, 360 * s, 180 * s), (0, 0, subject_h * 0.5), (70 * s, 700 * s), 25 * rims * s * s, cool)
    if card:
        ob = block('card', 900 * s, 4, 0, 260 * s, principled('card', '#F4F2EE', rough=0.9), bevel=0, y=-650 * s,
                   x=0)
        ob.location.z = 0.0


def strata(name, layers, z_range):
    """One clear acrylic body whose tint changes by height: `layers` [(z0, z1, tint, thin)] in mm, clear elsewhere.
    A bonded laminate of one polymer has no optical boundary at its bond lines, so it is one solid here; only the
    absorption steps from stratum to stratum (a bond line is invisible when the cement is index-matched and clean)."""
    mat = bpy.data.materials.new(name)
    nt, out = _nodes(mat)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['IOR'].default_value = 1.49
    b.inputs['Roughness'].default_value = 0.0
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    zs0, zs1 = z_range
    bands = [(zs0, zs1, sigma_per_mm('clear'))]
    for z0, z1, t, thin in layers:
        bands.append((z0, z1, sigma_per_mm(t, thin)))
    D = max(max(s) for *_, s in bands) / MM
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = zs0 * MM
    mr.inputs['From Max'].default_value = zs1 * MM
    nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp
    cr.interpolation = 'CONSTANT'
    col = lambda s: tuple(1.0 - (c / MM) / D for c in s) + (1.0,)
    cr.elements[0].position = 0.0
    cr.elements[0].color = col(bands[0][2])
    cr.elements[1].position = 1.0
    cr.elements[1].color = col(bands[0][2])
    for z0, z1, s in bands[1:]:
        e = cr.elements.new(max((z0 - zs0) / (zs1 - zs0), 0.0001))
        e.color = col(s)
        e2 = cr.elements.new(min((z1 - zs0) / (zs1 - zs0), 0.9999))
        e2.color = col(bands[0][2])
    nt.links.new(mr.outputs['Result'], ramp.inputs['Fac'])
    ab = nt.nodes.new('ShaderNodeVolumeAbsorption')
    ab.inputs['Density'].default_value = D
    nt.links.new(ramp.outputs['Color'], ab.inputs['Color'])
    nt.links.new(ab.outputs['Volume'], out.inputs['Volume'])
    return mat


def lamina(name, tint, thin=1.0):
    """A tinted stratum set inside a clear body (inset 0.05 mm from its faces): its surface is a plain transparent
    pass (no refraction, as a clean index-matched bond line has none), its volume adds the tint's absorption on top of
    the clear body's along the stretch of path that crosses it."""
    mat = bpy.data.materials.new(name)
    nt, out = _nodes(mat)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    nt.links.new(tr.outputs['BSDF'], out.inputs['Surface'])
    s = sigma_per_mm(tint, thin)
    c = sigma_per_mm('clear')
    s = [max(a - b, 0.0) for a, b in zip(s, c)]
    D = max(s) / MM
    ab = nt.nodes.new('ShaderNodeVolumeAbsorption')
    ab.inputs['Density'].default_value = D
    ab.inputs['Color'].default_value = tuple(1.0 - (x / MM) / D for x in s) + (1.0,)
    nt.links.new(ab.outputs['Volume'], out.inputs['Volume'])
    return mat
