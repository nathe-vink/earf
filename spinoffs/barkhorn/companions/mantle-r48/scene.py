"""Mantle round 48: the proposals' renders, path-traced in Cycles from the fab kit's render model (one model, every
shot). Written for realism, not for the studio engine's look:

- the acrylic is a dielectric at IOR 1.49 with a volume that absorbs per channel by Beer-Lambert, calibrated to
  A&C Plastics' TruCast chart (2064 Gray 29.3 % luminous transmission at 1/8 in; 2423 Red 14.1 %), the chart's two
  Fresnel losses taken out (0.923), the hue from round 43's chip photos; the strata are bands of that volume by height,
  the clear laminae a faint green-neutral clear;
- faces are classed as a shop leaves them: the cast sheet's faces glassy, outer edges diamond-polished, the terraces'
  treads buffed, holes, pockets and grooves satin as machined; every edge broken with a 0.5 mm bevel (shading);
- faint wear at grazing light: sparse hairline scratches and dust on the top faces;
- shadow caustics through the acrylic (Cycles' MNEE), tinted shadows, a real lens (focal length, f-number, focus);
- the record is a prop with grooves (a radial anisotropic sheen, the lead-in, the bands, the run-out) and a label;
- the bought arm and cartridge are modelled from their published geometry, finer than the fab kit's envelope.

    python3.11 scene.py SHOT --colour smoke --out PNG [--samples N] [--scale S] [--model out-core]
SHOT: hero, macro, use, closed, stand
"""
import argparse, json, math, os, sys

try:
    import bpy, bmesh
    from mathutils import Vector, Matrix, Euler
except ImportError:          # the label and the post run under the system python3 (PIL); Blender's has none
    bpy = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

# ---- the tints: TruCast luminous transmission at 1/8 in (3.175 mm), hue from round 43's chip photos ----
TINTS = {
    'smoke': dict(name='2064 Gray', lt=0.293, hue='#A5A5A4'),
    'ember': dict(name='2423 Red', lt=0.141, hue='#D4606F'),
}
FRESNEL = 0.923          # two faces of PMMA at normal incidence, n 1.49: (1 - 0.0387)^2


def lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def sigma_tint(key):
    """Absorption per metre, each channel: the chip's internal transmission over 3.175 mm."""
    t = TINTS[key]
    c = lin(t['hue'])
    y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    T = [min(0.999, x * (t['lt'] / FRESNEL) / y) for x in c]
    return [-math.log(x) / 0.003175 for x in T]


SIGMA_CLEAR = [0.35, 0.18, 0.30]      # water-clear PMMA: about 0.1 %/cm, a breath of green edge-on through 470 mm


# ---------------------------------------------------------------- materials
def node_tree(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    return m, nt, out


def bevel(nt, r=0.0005):
    b = nt.nodes.new('ShaderNodeBevel'); b.inputs['Radius'].default_value = r; b.samples = 8
    return b


def wear(nt, strength=1.0, scale=1.0):
    """Hairline scratches (stretched Voronoi edges, three directions) and dust, as a 0..1 mask on top faces."""
    tc = nt.nodes.new('ShaderNodeTexCoord')
    acc = None
    for k, (ang, sx) in enumerate(((0.3, 260), (1.4, 300), (2.5, 220))):
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Rotation'].default_value = (0, 0, ang)
        mp.inputs['Scale'].default_value = (sx * scale, 2.2 * scale, 1)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
        v = nt.nodes.new('ShaderNodeTexVoronoi'); v.feature = 'DISTANCE_TO_EDGE'; v.inputs['Scale'].default_value = 1.0
        v.inputs['Randomness'].default_value = 1.0
        nt.links.new(mp.outputs['Vector'], v.inputs['Vector'])
        r = nt.nodes.new('ShaderNodeMapRange'); r.inputs['From Min'].default_value = 0.0; r.inputs['From Max'].default_value = 0.012
        r.inputs['To Min'].default_value = 1.0; r.inputs['To Max'].default_value = 0.0
        nt.links.new(v.outputs['Distance'], r.inputs['Value'])
        # only some cells carry a scratch
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 9.0 + 3 * k
        nt.links.new(tc.outputs['Object'], n.inputs['Vector'])
        g = nt.nodes.new('ShaderNodeMapRange'); g.inputs['From Min'].default_value = 0.62; g.inputs['From Max'].default_value = 0.7
        nt.links.new(n.outputs['Fac'], g.inputs['Value'])
        mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'
        nt.links.new(r.outputs['Result'], mm.inputs[0]); nt.links.new(g.outputs['Result'], mm.inputs[1])
        if acc is None:
            acc = mm
        else:
            mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'
            nt.links.new(acc.outputs[0], mx.inputs[0]); nt.links.new(mm.outputs[0], mx.inputs[1]); acc = mx
    # dust: sparse specks
    d = nt.nodes.new('ShaderNodeTexVoronoi'); d.inputs['Scale'].default_value = 900.0 * scale
    nt.links.new(tc.outputs['Object'], d.inputs['Vector'])
    dr = nt.nodes.new('ShaderNodeMapRange'); dr.inputs['From Min'].default_value = 0.06; dr.inputs['From Max'].default_value = 0.03
    nt.links.new(d.outputs['Distance'], dr.inputs['Value'])
    dn = nt.nodes.new('ShaderNodeTexNoise'); dn.inputs['Scale'].default_value = 40.0
    nt.links.new(tc.outputs['Object'], dn.inputs['Vector'])
    dg = nt.nodes.new('ShaderNodeMapRange'); dg.inputs['From Min'].default_value = 0.66; dg.inputs['From Max'].default_value = 0.72
    nt.links.new(dn.outputs['Fac'], dg.inputs['Value'])
    dm = nt.nodes.new('ShaderNodeMath'); dm.operation = 'MULTIPLY'
    nt.links.new(dr.outputs['Result'], dm.inputs[0]); nt.links.new(dg.outputs['Result'], dm.inputs[1])
    sc = nt.nodes.new('ShaderNodeMath'); sc.operation = 'MULTIPLY'; sc.inputs[1].default_value = strength
    nt.links.new(acc.outputs[0], sc.inputs[0])
    ds = nt.nodes.new('ShaderNodeMath'); ds.operation = 'MULTIPLY'; ds.inputs[1].default_value = strength
    nt.links.new(dm.outputs[0], ds.inputs[0])
    return sc.outputs[0], ds.outputs[0]


def acrylic(name, bands, tint, rough=0.004, wear_on=True, ring=None):
    """`bands`: [(z0, z1, 'tint'|'clear')] in metres. The material has slots: 0 glassy (cast faces), 1 polished edge,
    2 buffed tread, 3 machined satin. One node tree per slot, the volume shared."""
    st = sigma_tint(tint)
    D = max(st) * 1.0001
    mats = []
    for slot, (r, wr) in enumerate(((rough, True), (0.010, False), (0.045, False), (0.32, False))):
        m, nt, out = node_tree(f'{name}-{slot}')
        b = nt.nodes.new('ShaderNodeBsdfPrincipled')
        b.inputs['Base Color'].default_value = (1, 1, 1, 1)
        b.inputs['Transmission Weight'].default_value = 1.0
        b.inputs['IOR'].default_value = 1.49
        b.inputs['Roughness'].default_value = r
        bv = bevel(nt, 0.0005 if slot != 3 else 0.0003)
        nt.links.new(bv.outputs['Normal'], b.inputs['Normal'])
        if wear_on and wr:
            scr, dust = wear(nt, 1.0)
            ad = nt.nodes.new('ShaderNodeMath'); ad.operation = 'MULTIPLY_ADD'
            nt.links.new(scr, ad.inputs[0]); ad.inputs[1].default_value = 0.10; ad.inputs[2].default_value = r
            nt.links.new(ad.outputs[0], b.inputs['Roughness'])
            # dust: a little diffuse white over the dielectric
            dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); dif.inputs['Color'].default_value = (0.75, 0.74, 0.72, 1)
            mx = nt.nodes.new('ShaderNodeMixShader')
            nt.links.new(dust, mx.inputs['Fac']); nt.links.new(b.outputs['BSDF'], mx.inputs[1]); nt.links.new(dif.outputs['BSDF'], mx.inputs[2])
            surf = mx.outputs['Shader']
        else:
            surf = b.outputs['BSDF']
        nt.links.new(surf, out.inputs['Surface'])
        # the volume: absorption by height (the strata), as constant ramps: one says tinted or clear, one the band's
        # inset from the outline; with `ring`, a tinted lamina is tinted only within `ring` of its own edge
        geo = nt.nodes.new('ShaderNodeNewGeometry')
        sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Position'], sep.inputs['Vector'])
        z0 = min(bb[0] for bb in bands); z1 = max(bb[1] for bb in bands)
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = z0; mr.inputs['From Max'].default_value = z1
        mr.clamp = True
        nt.links.new(sep.outputs['Z'], mr.inputs['Value'])

        def cramp(vals):
            rp = nt.nodes.new('ShaderNodeValToRGB'); rp.color_ramp.interpolation = 'CONSTANT'
            E = rp.color_ramp.elements
            srt = sorted(vals)
            E[0].position = 0.0; E[0].color = (srt[0][1],) * 3 + (1,)
            if len(srt) > 1:
                E[1].position = min(0.999, (srt[1][0] - z0) / (z1 - z0)); E[1].color = (srt[1][1],) * 3 + (1,)
            for zz, v in srt[2:]:
                e = E.new((zz - z0) / (z1 - z0)); e.color = (v,) * 3 + (1,)
            nt.links.new(mr.outputs['Result'], rp.inputs['Fac'])
            return rp
        tr = cramp([(a_, 1.0 if k == 'tint' else 0.0) for a_, b_, k, *_ in bands])
        fac = tr.outputs['Color']
        if ring:
            X0, Y0, X1, Y1, rw = ring
            ir = cramp([(a_, (bb[3] if len(bb) > 3 else 0.0) * 10) for bb in bands for a_ in [bb[0]]])
            def m2(op, x, y):
                n_ = nt.nodes.new('ShaderNodeMath'); n_.operation = op
                for i_, v in enumerate((x, y)):
                    if isinstance(v, float):
                        n_.inputs[i_].default_value = v
                    else:
                        nt.links.new(v, n_.inputs[i_])
                return n_.outputs[0]
            dx = m2('MINIMUM', m2('SUBTRACT', sep.outputs['X'], X0), m2('SUBTRACT', X1, sep.outputs['X']))
            dy = m2('MINIMUM', m2('SUBTRACT', sep.outputs['Y'], Y0), m2('SUBTRACT', Y1, sep.outputs['Y']))
            d_ = m2('MINIMUM', dx, dy)
            sepi = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(ir.outputs['Color'], sepi.inputs['Color'])
            lim = m2('ADD', m2('DIVIDE', sepi.outputs['Red'], 10.0), rw)
            inside = m2('LESS_THAN', d_, lim)
            sept = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(tr.outputs['Color'], sept.inputs['Color'])
            fac = m2('MULTIPLY', sept.outputs['Red'], inside)
        mixc = nt.nodes.new('ShaderNodeMix'); mixc.data_type = 'RGBA'
        mixc.inputs['A'].default_value = tuple(1 - s_ / D for s_ in SIGMA_CLEAR) + (1,)
        mixc.inputs['B'].default_value = tuple(1 - s_ / D for s_ in st) + (1,)
        nt.links.new(fac, mixc.inputs['Factor'])
        ab = nt.nodes.new('ShaderNodeVolumeAbsorption'); ab.inputs['Density'].default_value = D
        nt.links.new(mixc.outputs['Result'], ab.inputs['Color'])
        nt.links.new(ab.outputs['Volume'], out.inputs['Volume'])
        mats.append(m)
    return mats


def metal(name, col, rough, aniso=0.0, bev=0.0004, bump=0.0):
    m, nt, out = node_tree(name)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = tuple(lin(col)) + (1,)
    b.inputs['Metallic'].default_value = 1.0
    b.inputs['Roughness'].default_value = rough
    if aniso:
        b.inputs['Anisotropic'].default_value = aniso
    bv = bevel(nt, bev)
    if bump:
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 3000.0
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.00002
        nt.links.new(n.outputs['Fac'], bp.inputs['Height']); nt.links.new(bv.outputs['Normal'], bp.inputs['Normal'])
        nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    else:
        nt.links.new(bv.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def dielectric(name, col, rough, spec=0.5, bev=0.0004, coat=0.0, sss=0.0):
    m, nt, out = node_tree(name)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = tuple(lin(col)) + (1,)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec
    if coat:
        b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.05
    if sss:
        b.inputs['Subsurface Weight'].default_value = sss; b.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.2)
        b.inputs['Subsurface Scale'].default_value = 0.004
    bv = bevel(nt, bev)
    nt.links.new(bv.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def vinyl_material(label_png):
    """Vinyl with grooves: a radial anisotropic sheen (the tangent round the spindle), the grooved bands rougher
    across than along, the land between tracks and the run-out smoother; the label an image."""
    m, nt, out = node_tree('vinyl')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (0.006, 0.006, 0.0065, 1)
    b.inputs['Roughness'].default_value = 0.30
    b.inputs['Anisotropic'].default_value = 0.9
    b.inputs['Specular IOR Level'].default_value = 0.32
    tg = nt.nodes.new('ShaderNodeTangent'); tg.direction_type = 'RADIAL'; tg.axis = 'Z'
    nt.links.new(tg.outputs['Tangent'], b.inputs['Tangent'])
    tc = nt.nodes.new('ShaderNodeTexCoord')
    # radius from the record's centre (object coords: the record object is centred)
    vl = nt.nodes.new('ShaderNodeVectorMath'); vl.operation = 'LENGTH'
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    cmb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(sep.outputs['X'], cmb.inputs['X']); nt.links.new(sep.outputs['Y'], cmb.inputs['Y'])
    nt.links.new(cmb.outputs['Vector'], vl.inputs[0])
    # bands: grooved 0.06..0.146, gaps (land) at a few radii, run-out under 0.06 (smooth), lead-in 0.146..0.1505
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'LINEAR'
    E = ramp.color_ramp.elements
    E[0].position = 0.0; E[0].color = (0.09, 0, 0, 1)
    E[1].position = 0.0560 / 0.16; E[1].color = (0.09, 0, 0, 1)
    pts = [(0.0600, 0.30), (0.0832, 0.30), (0.0838, 0.10), (0.0845, 0.30), (0.1031, 0.30), (0.1037, 0.10), (0.1044, 0.30),
           (0.1213, 0.30), (0.1219, 0.10), (0.1226, 0.30), (0.1455, 0.30), (0.1462, 0.14), (0.1505, 0.14)]
    for r, v in pts:
        e = E.new(r / 0.16); e.color = (v, 0, 0, 1)
    mr = nt.nodes.new('ShaderNodeMath'); mr.operation = 'DIVIDE'; mr.inputs[1].default_value = 0.16
    nt.links.new(vl.outputs['Value'], mr.inputs[0]); nt.links.new(mr.outputs[0], ramp.inputs['Fac'])
    sepc = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(ramp.outputs['Color'], sepc.inputs['Color'])
    nt.links.new(sepc.outputs['Red'], b.inputs['Roughness'])
    # the groove's fine relief: a ring wave as a bump
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.inputs['Scale'].default_value = 1.0
    wv.inputs['Distortion'].default_value = 0.0
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (400, 400, 400)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.05; bp.inputs['Distance'].default_value = 0.00001
    nt.links.new(wv.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    # the label
    img = bpy.data.images.load(label_png)
    it = nt.nodes.new('ShaderNodeTexImage'); it.image = img
    mpl = nt.nodes.new('ShaderNodeMapping'); mpl.inputs['Scale'].default_value = (1 / 0.1, 1 / 0.1, 1); mpl.inputs['Location'].default_value = (0.5, 0.5, 0)
    # uv = obj.xy / 0.1 + 0.5
    vm = nt.nodes.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY_ADD'
    vm.inputs[1].default_value = (10.0, 10.0, 0.0); vm.inputs[2].default_value = (0.5, 0.5, 0.0)
    nt.links.new(tc.outputs['Object'], vm.inputs[0]); nt.links.new(vm.outputs['Vector'], it.inputs['Vector'])
    lb = nt.nodes.new('ShaderNodeBsdfPrincipled'); lb.inputs['Roughness'].default_value = 0.62
    lb.inputs['Specular IOR Level'].default_value = 0.35
    nt.links.new(it.outputs['Color'], lb.inputs['Base Color'])
    lr = nt.nodes.new('ShaderNodeMath'); lr.operation = 'LESS_THAN'; lr.inputs[1].default_value = 0.0500
    nt.links.new(vl.outputs['Value'], lr.inputs[0])
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lr.outputs[0], mx.inputs['Fac']); nt.links.new(b.outputs['BSDF'], mx.inputs[1]); nt.links.new(lb.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs['Shader'], out.inputs['Surface'])
    return m


def sleeve_object():
    art = os.path.join(HERE, 'out-core', 'render', 'sleeve.png')
    if not os.path.exists(art):
        import subprocess
        subprocess.run(['python3', os.path.abspath(__file__), '--sleeve', art], check=True)
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.active_object; o.name = 'sleeve'; o.scale = (0.315, 0.003, 0.315)
    bpy.ops.object.transform_apply(scale=True)
    m, nt, out = node_tree('sleeve')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.inputs['Roughness'].default_value = 0.55
    b.inputs['Specular IOR Level'].default_value = 0.4
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vm = nt.nodes.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY_ADD'
    vm.inputs[1].default_value = (1 / 0.315, 1 / 0.315, 1 / 0.315); vm.inputs[2].default_value = (0.5, 0.5, 0.5)
    nt.links.new(tc.outputs['Object'], vm.inputs[0])
    sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(vm.outputs['Vector'], sp.inputs['Vector'])
    cb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(sp.outputs['X'], cb.inputs['X']); nt.links.new(sp.outputs['Z'], cb.inputs['Y'])
    it = nt.nodes.new('ShaderNodeTexImage'); it.image = bpy.data.images.load(art)
    nt.links.new(cb.outputs['Vector'], it.inputs['Vector']); nt.links.new(it.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    o.data.materials.append(m)
    bv = o.modifiers.new('bev', 'BEVEL'); bv.width = 0.0008; bv.segments = 2
    return o


def make_sleeve(path):
    """The sleeve of the record playing (a prop): contour lines in two inks on an off-white board, small type."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import random
    S = 2000
    im = Image.new('RGB', (S, S), (226, 220, 206))
    d = ImageDraw.Draw(im)
    rnd = random.Random(4)
    cx, cy = S * 0.42, S * 0.58
    for k in range(46):
        r = 60 + k * 34
        pts = []
        for i in range(181):
            a = 2 * math.pi * i / 180
            w = 1 + 0.18 * math.sin(3 * a + k * 0.21) + 0.08 * math.sin(7 * a - k * 0.13)
            pts.append((cx + r * w * math.cos(a) * 1.15, cy + r * w * math.sin(a) * 0.82))
        d.line(pts, fill=(176, 64, 44) if k % 5 == 0 else (58, 54, 50), width=6 if k % 5 == 0 else 3)
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 96)
    f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 44)
    d.rectangle([0, 0, S, 300], fill=(226, 220, 206))
    d.text((120, 110), 'STRATA', font=f, fill=(40, 36, 32))
    d.text((S - 760, 140), 'Four studies in slow light', font=f2, fill=(40, 36, 32))
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(path)


def make_label(path):
    from PIL import Image, ImageDraw, ImageFont
    S = 1600
    im = Image.new('RGB', (S, S), (196, 188, 172))
    d = ImageDraw.Draw(im)
    fdir = '/usr/share/fonts/truetype/dejavu/'
    f1 = ImageFont.truetype(fdir + 'DejaVuSans-Bold.ttf', 120)
    f2 = ImageFont.truetype(fdir + 'DejaVuSans.ttf', 44)
    f3 = ImageFont.truetype(fdir + 'DejaVuSans.ttf', 34)
    c = S / 2
    # a thin printed ring and the type, as a plain test-pressing label
    d.ellipse([c - 760, c - 760, c + 760, c + 760], outline=(60, 56, 52), width=6)
    d.ellipse([c - 700, c - 700, c + 700, c + 700], outline=(150, 70, 52), width=3)
    for txt, f, y in (('STRATA', f1, c - 380), ('SIDE A  ·  33⅓ RPM', f2, c - 210), ('1. Lithosphere   2. Asthenosphere', f3, c + 200),
                      ('3. Transition Zone   4. Lower Mantle', f3, c + 260), ('TEST PRESSING  ·  NOT FOR SALE', f3, c + 420)):
        w = d.textlength(txt, font=f)
        d.text((c - w / 2, y), txt, font=f, fill=(42, 38, 34))
    im.save(path)


# ---------------------------------------------------------------- geometry helpers
def classify_faces(obj, bands_inset, edge_band=0.0012):
    """Material slots by how a shop leaves each face: 0 the sheet's cast face (horizontal, on the very top), 1 a
    polished outer edge, 2 a buffed tread (horizontal, not the top), 3 machined (holes, pockets, grooves, undersides
    of cut-outs)."""
    me = obj.data
    bm = bmesh.new(); bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    xs = [v.co.x for v in bm.verts]; ys = [v.co.y for v in bm.verts]; zs = [v.co.z for v in bm.verts]
    x0, x1, y0, y1, ztop, zbot = min(xs), max(xs), min(ys), max(ys), max(zs), min(zs)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for f in bm.faces:
        n = f.normal; c = f.calc_center_median()
        if abs(n.z) > 0.7:
            if n.z > 0 and abs(c.z - ztop) < 1e-4:
                f.material_index = 0
            elif n.z < 0 and abs(c.z - zbot) < 1e-4:
                f.material_index = 0
            else:
                # a tread if it lies in the outer ring of the terraces, else a pocket's floor
                dx = min(c.x - x0, x1 - c.x); dy = min(c.y - y0, y1 - c.y)
                f.material_index = 2 if min(dx, dy) < bands_inset + 0.004 else 3
        else:
            dx = min(c.x - x0, x1 - c.x); dy = min(c.y - y0, y1 - c.y)
            outward = (c.x - cx) * n.x / max(abs(c.x - cx), 1e-6) * (abs(c.x - cx) > 0) + (c.y - cy) * n.y / max(abs(c.y - cy), 1e-6)
            near = min(dx, dy) < bands_inset + 0.003
            f.material_index = 1 if (near and outward > 0.2) else 3
    bm.to_mesh(me); bm.free()


def round_platter_faces(obj):
    me = obj.data
    bm = bmesh.new(); bm.from_mesh(me)
    zs = [v.co.z for v in bm.verts]
    ztop, zbot = max(zs), min(zs)
    xs = [v.co.x for v in bm.verts]; ys = [v.co.y for v in bm.verts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    R = (max(xs) - min(xs)) / 2
    for f in bm.faces:
        c = f.calc_center_median(); n = f.normal
        r = math.hypot(c.x - cx, c.y - cy)
        if abs(n.z) > 0.7:
            f.material_index = 0 if (abs(c.z - ztop) < 1e-4 or abs(c.z - zbot) < 1e-4) else 3
        else:
            f.material_index = 1 if r > R - 0.002 else 3
    bm.to_mesh(me); bm.free()


def add_mesh(name, verts, faces, mat=None, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    if mat:
        o.data.materials.append(mat)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return o


def cylinder(name, r, h, loc, mat, rot=None, seg=64, bev=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=seg, radius=r, depth=h, location=loc)
    o = bpy.context.active_object; o.name = name
    if rot:
        o.rotation_euler = rot
    o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if bev:
        m = o.modifiers.new('bev', 'BEVEL'); m.width = bev; m.segments = 3; m.limit_method = 'ANGLE'
    return o


def boxo(name, size, loc, mat, rot=None, bev=0.0004):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = size
    if rot:
        o.rotation_euler = rot
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    if bev:
        m = o.modifiers.new('bev', 'BEVEL'); m.width = bev; m.segments = 3
    return o


def lathe(name, prof, mat, loc, rot=(0, 0, 0), seg=96):
    """A turned part from an (r, z) profile, revolved about its local z."""
    verts, faces = [], []
    n = len(prof)
    for k in range(seg):
        a = 2 * math.pi * k / seg
        for r, z in prof:
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for k in range(seg):
        k2 = (k + 1) % seg
        for i in range(n - 1):
            faces.append((k * n + i, k * n + i + 1, k2 * n + i + 1, k2 * n + i))
    o = add_mesh(name, verts, faces, mat)
    o.location = loc; o.rotation_euler = rot
    return o


# ---------------------------------------------------------------- the arm and cartridge
def rega_arm(meta, mats, lowered=False, cue_up=False):
    """Rega RB330 from its published geometry: effective length 236.5, offset 21.55 deg, pivot 222 from the spindle;
    the rest of its form from photographs (a one-piece tapered tube with its headshell and finger lift, the bearing
    housing on a round pillar, a stainless counterweight on a stub, the cue lift and the rest on the arm's base).
    Returns the parent empty."""
    A = [c / 1000 for c in meta['A']]
    top = meta['top'] / 1000
    h = (meta['record_z'] + 21.0) / 1000 if not lowered else (meta['record_z'] + 17.5) / 1000
    S = [c / 1000 for c in meta['S']]
    root = bpy.data.objects.new('rb330', None); bpy.context.collection.objects.link(root)
    root.location = (A[0], A[1], 0)
    # the arm's direction: at rest, toward the rest; lowered, onto the record's lead-in groove at r 0.146
    if lowered:
        # the stylus at radius 0.140 on the arm's arc
        L = 0.2365; dx, dy = S[0] - A[0], S[1] - A[1]; dd = math.hypot(dx, dy); r = 0.140
        a = (L * L - r * r + dd * dd) / (2 * dd); hh = math.sqrt(L * L - a * a)
        bx, by = A[0] + a * dx / dd, A[1] + a * dy / dd
        st = min([(bx + hh * dy / dd, by - hh * dx / dd), (bx - hh * dy / dd, by + hh * dx / dd)], key=lambda p: p[1])
        ang = math.atan2(st[1] - A[1], st[0] - A[0])
    else:
        ang = math.radians(meta['rest_deg'])
    blk, alu, stl, rub = mats['arm'], mats['alu'], mats['steel'], mats['rubber']
    z0 = top
    # base: a black anodised round base with the pillar, the nut's flat
    lathe('arm-base', [(0, 0), (0.0225, 0), (0.0225, 0.004), (0.0215, 0.0048), (0.014, 0.0055), (0.013, 0.0065), (0.013, h - z0 - 0.012),
                       (0.0125, h - z0 - 0.0115), (0, h - z0 - 0.0115)], blk, (A[0], A[1], z0))
    # bearing housing: a block across the pillar's top with its horizontal axle caps (polished)
    hs = boxo('arm-yoke', (0.030, 0.022, 0.014), (A[0], A[1], h - 0.004), blk, rot=(0, 0, ang), bev=0.0018)
    for s in (-1, 1):
        nx, ny = -math.sin(ang), math.cos(ang)
        cylinder('arm-axle', 0.0042, 0.003, (A[0] + s * 0.0125 * nx, A[1] + s * 0.0125 * ny, h - 0.004), alu,
                 rot=(math.pi / 2, 0, ang), seg=32, bev=0.0003)
    # the tube: tapered from 0.0080 radius at the bearing to 0.0045 by the headshell, a slight oval
    L = 0.2365
    tube_len = L - 0.042
    prof = [(0.0, 0.0)]
    for i in range(0, 21):
        t = i / 20
        prof.append((0.0082 - 0.0036 * t ** 0.8, t * tube_len))
    prof.append((0.0, tube_len))
    tube = lathe('arm-tube', prof, blk, (A[0], A[1], h), rot=(0, math.pi / 2, 0), seg=48)
    tube.rotation_mode = 'XYZ'
    tube.rotation_euler = (0, math.pi / 2, 0)
    tube.parent = None
    # rotate about z by ang: apply via a parent empty at the pivot
    piv = bpy.data.objects.new('arm-pivot', None); bpy.context.collection.objects.link(piv)
    piv.location = (A[0], A[1], h); piv.rotation_euler = (0, 0, ang)
    tube.location = (0, 0, 0); tube.parent = piv
    # tilt a hair down toward the stylus when lowered (the tube level when VTA is right)
    # headshell: a flat plate at the tube's end, turned by the offset, with the finger lift
    hx = tube_len
    head = boxo('arm-head', (0.040, 0.019, 0.0028), (0, 0, 0), blk, bev=0.0008)
    head.parent = piv; head.location = (hx + 0.012, 0.0, -0.0042); head.rotation_euler = (0, 0, -math.radians(21.55))
    # finger lift: a bent strip out of the headshell's side
    fl = boxo('arm-lift-tab', (0.022, 0.0035, 0.0018), (0, 0, 0), blk, bev=0.0006)
    fl.parent = piv; fl.location = (hx + 0.010, -0.019, -0.0018); fl.rotation_euler = (math.radians(-18), 0, -math.radians(55))
    # counterweight: stainless, turned, on a black stub behind the pivot
    stub = cylinder('arm-stub', 0.0048, 0.040, (0, 0, 0), blk, rot=(0, math.pi / 2, 0), seg=32)
    stub.parent = piv; stub.location = (-0.026, 0, 0)
    cw = lathe('arm-cw', [(0.0, 0), (0.0145, 0), (0.0160, 0.0012), (0.0160, 0.0218), (0.0145, 0.0230), (0.0, 0.0230)], stl, (0, 0, 0))
    cw.parent = piv; cw.location = (-0.034, 0, 0); cw.rotation_euler = (0, -math.pi / 2, 0)
    # a black decoupling ring on the weight's face
    ring = lathe('arm-cw-ring', [(0.0052, 0), (0.0105, 0), (0.0105, 0.002), (0.0052, 0.002)], rub, (0, 0, 0))
    ring.parent = piv; ring.location = (-0.0335, 0, 0); ring.rotation_euler = (0, -math.pi / 2, 0)
    # bias adjuster: a small knurled slider on the housing's side
    bias = cylinder('arm-bias', 0.0028, 0.006, (0, 0, 0), alu, seg=24)
    bias.parent = piv; bias.location = (-0.008, 0.012, 0.0045)
    # the cue lift: a pillar beside the arm with its platform under the tube, a lever with a ball knob
    nx, ny = math.sin(ang), -math.cos(ang)              # the tube's right
    ux, uy = math.cos(ang), math.sin(ang)
    lx, ly = A[0] + 0.050 * ux + 0.020 * nx, A[1] + 0.050 * uy + 0.020 * ny
    cue_top = h - 0.0105 + (0.004 if cue_up else 0.0)
    lathe('cue-post', [(0, 0), (0.0068, 0), (0.0068, 0.003), (0.0052, 0.004), (0.0052, cue_top - z0 - 0.002), (0, cue_top - z0 - 0.002)],
          blk, (lx, ly, z0))
    plat = boxo('cue-bar', (0.030, 0.0045, 0.0030), (lx - 0.012 * nx, ly - 0.012 * ny, cue_top), blk, rot=(0, 0, ang + math.pi / 2), bev=0.0007)
    lev_ang = ang + math.radians(-70)
    lev = boxo('cue-lever', (0.032, 0.0030, 0.0030), (lx + 0.016 * math.cos(lev_ang), ly + 0.016 * math.sin(lev_ang), z0 + 0.016),
               blk, rot=(0, math.radians(10 if not cue_up else -15), lev_ang), bev=0.0008)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0034, location=(lx + 0.032 * math.cos(lev_ang), ly + 0.032 * math.sin(lev_ang),
                                                                  z0 + 0.016 + (0.003 if not cue_up else -0.004)))
    kn = bpy.context.active_object; kn.name = 'cue-knob'; kn.data.materials.append(blk); bpy.ops.object.shade_smooth()
    # the arm rest: a short post with a clip, where the tube rests at rest
    if not lowered:
        rx, ry = A[0] + 0.105 * ux + 0.016 * nx, A[1] + 0.105 * uy + 0.016 * ny
    # the lead: a black cable down from the base, unseen; the cartridge
    cart = cartridge(mats, piv, hx + 0.012)
    return piv


def cartridge(mats, piv, hx):
    """Ortofon 2M: a black body 18 wide, its front sloped, the stylus housing forward and below, an aluminium
    cantilever with the diamond; two M2.5 screws through the headshell."""
    blk, alu, stl, red = mats['cart'], mats['alu'], mats['steel'], mats['cart-accent']
    off = -math.radians(21.55)
    e = bpy.data.objects.new('cart-frame', None); bpy.context.collection.objects.link(e)
    e.parent = piv; e.location = (hx, 0, -0.0056); e.rotation_euler = (0, 0, off)
    # body: a trapezoid prism (top 0.022 long, bottom 0.019), 0.018 wide, 0.0155 tall
    v = [(-0.012, -0.009, 0), (0.010, -0.009, 0), (0.010, 0.009, 0), (-0.012, 0.009, 0),
         (-0.012, -0.009, -0.0155), (0.0065, -0.009, -0.0155), (0.0065, 0.009, -0.0155), (-0.012, 0.009, -0.0155)]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    body = add_mesh('cart-body', v, f, blk, smooth=False)
    body.parent = e
    bm_ = body.modifiers.new('bev', 'BEVEL'); bm_.width = 0.0016; bm_.segments = 4
    # stylus housing: a small block under the front
    sh = boxo('cart-stylus', (0.010, 0.007, 0.004), (0, 0, 0), mats['cart-accent'], bev=0.0012)
    sh.parent = e; sh.location = (0.0055, 0, -0.0170)
    # cantilever and diamond
    cl = cylinder('cart-cantilever', 0.00028, 0.0055, (0, 0, 0), alu, rot=(0, math.radians(90 + 22), 0), seg=12)
    cl.parent = e; cl.location = (0.0115, 0, -0.0186)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.0002, depth=0.0007, location=(0, 0, 0))
    dm = bpy.context.active_object; dm.name = 'cart-diamond'; dm.data.materials.append(mats['diamond'])
    dm.parent = e; dm.location = (0.0138, 0, -0.0196); dm.rotation_euler = (math.pi, 0, 0)
    # screws
    for s in (-1, 1):
        sc = cylinder('cart-screw', 0.0021, 0.0012, (0, 0, 0), stl, seg=24)
        sc.parent = e; sc.location = (-0.002, s * 0.0063, 0.0034)
    # printed maker's mark on the side: a thin pale band
    return e


# ---------------------------------------------------------------- the hand (the in-use shot)
def hand(mats, at, yaw):
    """A right hand's index finger and thumb on the cue lever, the rest of the hand curled out of frame: built with a
    skin modifier on a bone-like skeleton, subdivided, in a skin material with subsurface scattering."""
    # joints in the hand's frame (metres): x toward the fingertip, y to the thumb side, z up
    pts, edges, radii = [], [], []

    def chain(seq):
        i0 = len(pts)
        for p, r in seq:
            pts.append(p); radii.append(r)
        for k in range(len(seq) - 1):
            edges.append((i0 + k, i0 + k + 1))
        return i0
    wrist = chain([((-0.13, 0.00, 0.050), 0.026), ((-0.085, 0.004, 0.040), 0.030)])
    palm = chain([((-0.085, 0.004, 0.040), 0.030), ((-0.040, 0.006, 0.030), 0.030)])
    edges.append((wrist + 1, palm))
    idx = chain([((-0.040, 0.016, 0.028), 0.0095), ((-0.008, 0.016, 0.018), 0.0085), ((0.012, 0.014, 0.008), 0.0078), ((0.026, 0.012, 0.0005), 0.0070)])
    edges.append((palm + 1, idx))
    mid = chain([((-0.042, -0.002, 0.028), 0.0098), ((-0.020, -0.006, 0.000), 0.0090), ((-0.030, -0.006, -0.018), 0.0082), ((-0.046, -0.004, -0.020), 0.0075)])
    edges.append((palm + 1, mid))
    ring = chain([((-0.046, -0.018, 0.026), 0.0092), ((-0.028, -0.022, 0.002), 0.0085), ((-0.038, -0.022, -0.016), 0.0078), ((-0.052, -0.020, -0.018), 0.0070)])
    edges.append((palm + 1, ring))
    pinky = chain([((-0.052, -0.032, 0.026), 0.0080), ((-0.040, -0.036, 0.006), 0.0072), ((-0.048, -0.035, -0.008), 0.0066), ((-0.060, -0.033, -0.010), 0.0060)])
    edges.append((palm + 1, pinky))
    th = chain([((-0.075, 0.022, 0.034), 0.0140), ((-0.045, 0.036, 0.020), 0.0112), ((-0.022, 0.040, 0.010), 0.0098), ((-0.006, 0.038, 0.004), 0.0088)])
    edges.append((palm, th))
    me = bpy.data.meshes.new('hand'); me.from_pydata(pts, edges, []); me.update()
    o = bpy.data.objects.new('hand', me); bpy.context.collection.objects.link(o)
    sk = o.modifiers.new('skin', 'SKIN')
    for i, v in enumerate(me.skin_vertices[0].data):
        v.radius = (radii[i], radii[i] * 0.86)
    me.skin_vertices[0].data[0].use_root = True
    sub = o.modifiers.new('sub', 'SUBSURF'); sub.levels = 3; sub.render_levels = 3
    o.data.materials.append(mats['skin'])
    o.location = at; o.rotation_euler = (0, math.radians(8), yaw)
    for p in me.polygons:
        p.use_smooth = True
    # a cuff of a dark knit sleeve over the wrist
    cuff = cylinder('sleeve', 0.034, 0.10, (0, 0, 0), mats['knit'], rot=(0, math.pi / 2, 0), seg=48)
    cuff.parent = o; cuff.location = (-0.17, 0, 0.052)
    return o


# ---------------------------------------------------------------- the scene
def build(args):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    model = os.path.join(HERE, args.model)
    meta = json.load(open(os.path.join(model, 'render', 'meta.json')))
    bpy.ops.import_scene.gltf(filepath=os.path.join(model, 'render', [f for f in os.listdir(os.path.join(model, 'render')) if f.endswith('.glb')][0]))
    objs = {o.name: o for o in bpy.data.objects if o.type == 'MESH'}
    bpy.context.view_layer.update()
    for o in objs.values():                       # free them of the importer's root, keeping where they are
        mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw

    tint = args.colour
    mm = 1e-3
    bands_deck = [(l['z0'] * mm, l['z1'] * mm, l['kind'], l['inset'] * mm) for l in meta['lams']]
    bands_cover = [(l['z0'] * mm, l['z1'] * mm, l['kind']) for l in meta['cover'] + meta['cover_top']]
    pz0 = meta['pz0'] * mm
    pl = meta['P']['platter_lams']
    bands_platter, z = [], pz0 - 0.00015
    for k, t in pl:
        bands_platter.append((z, z + t * mm, k)); z += t * mm

    M = {}
    rw = meta['P'].get('tint_ring')
    if 'deck-L1-stack' in objs:
        M['deck'] = acrylic('deck', bands_deck, tint, ring=(0.0, 0.0, meta['W1'] * mm, meta['D1'] * mm, rw * mm) if rw else None)
        M['cover'] = acrylic('cover', bands_cover, tint)
    M['platter'] = acrylic('platter', bands_platter, tint, wear_on=False)
    M['brass'] = metal('brass', '#C8A15E', 0.22, bump=0.15)
    M['brass-brushed'] = metal('brass-brushed', '#C9A563', 0.30, aniso=0.6)
    M['steel'] = metal('steel', '#D0D0CC', 0.12)
    M['alu'] = metal('alu', '#C4C6C7', 0.38, bump=0.3)
    M['alu-blast'] = metal('alu-blast', '#8E9092', 0.55, bump=0.4)
    M['alu-black'] = dielectric('alu-black', '#1A1A1C', 0.42, spec=0.45, coat=0.0)
    M['arm'] = dielectric('arm', '#121213', 0.42, spec=0.3)
    M['rubber'] = dielectric('rubber', '#141414', 0.7, spec=0.25)
    M['felt'] = dielectric('felt', '#2A2A2A', 0.95, spec=0.05)
    M['cart'] = dielectric('cart', '#0D0D0E', 0.25, spec=0.6)
    M['cart-accent'] = dielectric('cart-accent', '#101011', 0.4, spec=0.5)
    M['diamond'] = dielectric('diamond', '#FFFFFF', 0.0, spec=1.0)
    M['etch'] = dielectric('etch', '#8E8D89', 0.9, spec=0.15)
    M['skin'] = dielectric('skin', '#C99A7E', 0.42, spec=0.45, sss=0.35)
    M['knit'] = dielectric('knit', '#2B2D33', 0.9, spec=0.1)

    finish = {'deck-L1-stack': 'deck', 'cover-C1-stack': 'cover', 'platter-disc': 'platter', 'platter-hub': 'brass',
              'platter-screws': 'steel', 'spindle': 'steel', 'bearing-housing': 'brass', 'bearing-nut': 'brass', 'bushes': 'brass',
              'ball': 'steel', 'thrust-plate': 'steel', 'motor-plate': 'alu-black', 'motor': 'alu-black', 'motor-grommets': 'rubber',
              'pulley': 'alu', 'belt': 'rubber', 'arm-puck': 'alu-blast', 'feet': 'brass', 'foot-pads': 'rubber', 'foot-studs': 'steel',
              'phono-stage': 'alu-black', 'phono-runners': 'felt', 'back-plate': 'brass-brushed', 'back-hardware': 'steel',
              'dowels': 'steel', 'mark': 'etch'}
    # proposal A's parts (mantle_strata.py)
    if 'plinth-L1-stack' in objs:
        bands_pl = [(l['z0'] * mm, l['z1'] * mm, l['kind'], l['inset'] * mm) for l in meta['lams']]
        o0 = meta['P']['margin'] * mm
        M['plinth'] = acrylic('plinth', bands_pl, tint, ring=(o0, o0, o0 + (meta['W0']) * mm, o0 + meta['D0'] * mm, rw * mm))
        bands_b = [(l['z0'] * mm, l['z1'] * mm, l['kind'], 0.0) for l in meta['base']]
        M['base'] = acrylic('base', bands_b, tint, ring=(0.0, 0.0, meta['Wb'] * mm, meta['Db'] * mm, rw * mm))
        M['lid'] = acrylic('lid', [(0.0, 0.5, 'tint')], tint, rough=0.004)
        M['post'] = acrylic('post', [(0.0, 0.5, 'clear')], tint, wear_on=False)
        M['strip'], nt_, out_ = node_tree('strip')
        em = nt_.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.62, 0.30, 1); em.inputs['Strength'].default_value = args.strip
        nt_.links.new(em.outputs['Emission'], out_.inputs['Surface'])
        finish.update({'plinth-L1-stack': 'plinth', 'base-L1-stack': 'base', 'studs': 'steel', 'phono-pads': 'felt', 'hinges': 'arm',
                       'hinge-blocks': 'lid', 'led-strip': 'strip'})
        for k in range(1, 5):
            finish[f'post-{k}'] = 'post'
        for k in ('top', 'front', 'back', 'left', 'right'):
            finish[f'lid-{k}'] = 'lid'
    for n, o in objs.items():
        o.data.materials.clear()
        if n in ('arm', 'cartridge'):
            o.hide_render = True; continue
        if (n.startswith('lid-') or n == 'hinges') and args.shot != 'closed':
            o.hide_render = True
        f = finish.get(n)
        if f in ('deck', 'cover', 'platter', 'plinth', 'base', 'lid', 'post'):
            for m in M[f]:
                o.data.materials.append(m)
            if f in ('platter', 'post'):
                round_platter_faces(o)
            elif f == 'lid':
                pass
            else:
                classify_faces(o, (meta['o'] * mm if f in ('deck', 'plinth') else 0.0) + (0.03 if f == 'cover' else 0.0))
            for p in o.data.polygons:
                p.use_smooth = False
            o['caustic'] = True
        elif f:
            o.data.materials.append(M[f])
    # the cover: on, off (hidden), or stood on its back edge beside the deck (the frame for the sleeve)
    cov = objs.get('cover-C1-stack') or bpy.data.objects.new('nocover', None)
    if args.shot in ('hero', 'macro', 'use') and cov.type == 'MESH':
        cov.hide_render = args.shot != 'use'
    if args.shot in ('use', 'stand') and cov.type == 'MESH':
        # stand it on its back long edge to the left of the deck, its open side forward
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action='DESELECT'); cov.select_set(True); bpy.context.view_layer.objects.active = cov
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        # the importer's meshes are Y-up under a turned root: turn the object as it stands in the world
        R0 = cov.matrix_world.to_3x3()
        R = Matrix.Rotation(math.radians(18), 3, 'Z') @ Matrix.Rotation(math.radians(-90), 3, 'X') @ R0
        cov.matrix_world = Matrix.Translation(cov.matrix_world.translation) @ R.to_4x4()
        bpy.context.view_layer.update()
        zmin = min((cov.matrix_world @ v.co).z for v in cov.data.vertices)
        cov.location = (-0.26, 0.33, cov.location.z - zmin + 0.0002)
        bpy.context.view_layer.update()
        # the sleeve playing, standing in it against the top lamina, leaning back 4 degrees
        sl = sleeve_object()
        sl.rotation_euler = (math.radians(-4), 0, math.radians(18))
        th = (meta['height'] - meta['top']) * mm
        back = Vector((0, 1, 0)); back.rotate(Euler((0, 0, math.radians(18))))
        sl.location = cov.location + back * (th / 2 - 0.012) + Vector((0, 0, 0.0115 + 0.1575 - cov.location.z + 0.0002))
    for n in ('dowels',):
        pass

    # the record (a prop): 0.1505 radius, 1.8 thick, its edge bead
    label = os.path.join(HERE, 'out-core', 'render', 'label.png')  # shared by both proposals
    if not os.path.exists(label):
        import subprocess
        subprocess.run(['python3', os.path.abspath(__file__), '--label', label], check=True)
    S = [c * mm for c in meta['S']]
    rz = meta['pz1'] * mm
    rec = lathe('record', [(0.0036, 0), (0.1495, 0), (0.1505, 0.0006), (0.1505, 0.0013), (0.1490, 0.0018), (0.050, 0.0016),
                           (0.0495, 0.0019), (0.0036, 0.0019)], vinyl_material(label), (S[0], S[1], rz), seg=192)
    rec.rotation_euler = (0, 0, math.radians(args.label_deg))
    if args.shot == 'stand' or args.shot == 'closed':
        rec.hide_render = args.shot == 'closed'

    # the arm and cartridge, finer than the kit's envelope
    rega_arm(meta, M, lowered=args.shot == 'use', cue_up=False)
    if args.shot == 'use':
        # playing: the record and the platter turn at 33 1/3 (3.49 rad/s); a 1/8 s shutter blurs the label
        sc_ = bpy.context.scene
        sc_.render.fps = 24
        piv = bpy.data.objects.new('turn', None); bpy.context.collection.objects.link(piv)
        piv.location = (S[0], S[1], 0)
        bpy.context.view_layer.update()
        for n in ('record', 'platter-disc', 'platter-hub', 'platter-screws'):
            o = bpy.data.objects[n]
            o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
        bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
        piv.rotation_euler = (0, 0, 0); piv.keyframe_insert('rotation_euler', frame=0)
        piv.rotation_euler = (0, 0, -4 * 3.49 / 24); piv.keyframe_insert('rotation_euler', frame=4)
        sc_.frame_set(2)
        sc_.render.use_motion_blur = True
        sc_.render.motion_blur_shutter = 3.0          # 3 frames at 24 fps = 1/8 s

    if args.shot == 'use':
        # a sleeve in the stood cover
        pass

    setup_world(args, meta)
    return meta


def setup_world(args, meta):
    sc = bpy.context.scene
    mm = 1e-3
    W1, D1 = meta['W1'] * mm, meta['D1'] * mm
    cx, cy = W1 / 2, D1 / 2
    world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    # the sweep: a mid warm-grey paper, a long curve behind
    paper = dielectric('paper', args.paper, 0.78, spec=0.3)
    nt = paper.node_tree
    b = [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'][0]
    tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = 900.0; tx.inputs['Detail'].default_value = 8
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08; bp.inputs['Distance'].default_value = 0.0002
    nt.links.new(tx.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    prof = []
    for i in range(0, 25):
        a = math.pi / 2 * i / 24
        prof.append((0.9 - 0.6 * math.sin(a) * 0 + 0.0, 0))
    verts, faces = [], []
    xs = [-2.5, 3.0]
    yz = [(-2.0, 0.0), (0.9, 0.0)] + [(0.9 + 0.7 * math.sin(math.pi / 2 * i / 16), 0.7 - 0.7 * math.cos(math.pi / 2 * i / 16)) for i in range(1, 17)] + [(1.6, 2.5)]
    for x in xs:
        for y, z in yz:
            verts.append((x + cx, y + cy, z))
    n = len(yz)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    sweep = add_mesh('sweep', verts, faces, paper)
    sub = sweep.modifiers.new('s', 'SUBSURF'); sub.levels = 2; sub.render_levels = 2
    sweep['receiver'] = True

    def area(name, size, loc, target, power, col=(1.0, 0.97, 0.93), spread=None, shape='RECTANGLE', caust=True):
        ld = bpy.data.lights.new(name, 'AREA'); ld.shape = shape
        ld.size = size[0]; ld.size_y = size[1]; ld.energy = power; ld.color = col
        if spread:
            ld.spread = math.radians(spread)
        o = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(o)
        o.location = loc
        d = Vector(target) - Vector(loc)
        o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        ld.cycles.is_caustics_light = caust
        return o

    T = (cx, cy, 0.06)
    if args.shot in ('hero', 'macro', 'closed', 'stand'):
        bg.inputs['Color'].default_value = (0.02, 0.02, 0.022, 1); bg.inputs['Strength'].default_value = 1.0
        # key: a large softbox high front-left, a 40 deg grid so it shapes rather than floods
        area('key', (1.2, 0.9), (cx - 1.1, cy - 0.9, 1.25), T, 140, spread=32)
        # a strip behind right: rims the terraces and lights through the clear strata
        area('strip', (1.6, 0.18), (cx + 0.35, cy + 1.05, 0.30), (cx, cy, 0.05), 90, col=(1.0, 0.98, 0.95), spread=60)
        # a low bank at the left at the strata's height: light along the clear strata, so the inside is lit
        area('side', (0.9, 0.10), (cx - 0.95, cy + 0.10, 0.045), (cx, cy, 0.045), 160, col=(1.0, 0.98, 0.95), spread=50)
        # a low fill card right, very weak
        area('fill', (1.0, 0.6), (cx + 1.3, cy - 0.6, 0.35), T, 12, col=(0.95, 0.97, 1.0), caust=False)
        # a top scrim for the glassy tops' reflection, graded by its spread
        area('top', (0.9, 0.6), (cx + 0.15, cy - 0.15, 1.4), T, 22, spread=25)
        # black flags: a big one over the camera's right and one overhead behind, so gloss reads dark, edges bright
        flag = dielectric('flag', '#050505', 0.9, spec=0.05)
        for nm, size, loc in (('flag-r', (1.6, 1.2), (cx + 1.2, cy - 0.2, 0.9)), ('flag-top', (1.4, 1.0), (cx - 0.1, cy + 0.6, 1.3))):
            fo = boxo(nm, (size[0], size[1], 0.01), loc, flag, bev=0)
            fo.rotation_euler = (Vector(T) - Vector(loc)).to_track_quat('Z', 'Y').to_euler()
            fo.visible_camera = False
        # a hard little sun for the caustics: through the clear strata onto the sweep (shadow caustics, MNEE)
        sun = bpy.data.lights.new('spot', 'SPOT'); sun.energy = args.spot; sun.spot_size = math.radians(30); sun.shadow_soft_size = 0.004
        sun.color = (1.0, 0.95, 0.88); sun.cycles.is_caustics_light = True
        so = bpy.data.objects.new('spot', sun); bpy.context.collection.objects.link(so)
        so.location = (cx + 1.2, cy + 1.6, 0.85)
        so.rotation_euler = (Vector(T) - so.location).to_track_quat('-Z', 'Y').to_euler()
    else:
        # the in-use room: late afternoon through a window at the left, a warm lamp right, the room's HDRI dim behind
        env = bpy.data.images.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE)))) , 'studio', 'assets', 'hdri', 'st_fagans_interior_1k.hdr'))
        et = world.node_tree.nodes.new('ShaderNodeTexEnvironment'); et.image = env
        world.node_tree.links.new(et.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.35
        area('window', (1.4, 1.6), (cx - 1.6, cy + 0.2, 1.1), T, 260, col=(1.0, 0.92, 0.80), spread=40)
        area('bounce', (1.0, 1.0), (cx + 1.0, cy - 1.0, 0.7), T, 25, col=(1.0, 0.96, 0.9), caust=False)
        area('strip', (0.8, 0.12), (cx + 0.55, cy + 0.30, 0.10), (cx, cy, 0.05), 40, col=(1.0, 0.9, 0.8), spread=60)
        # a walnut sideboard's top under it and a plaster wall behind, both Poly Haven scans (CC0), instead of paper
        sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
        import assets as PH
        sweep.hide_render = True
        top = boxo('sideboard', (1.6, 0.52, 0.04), (cx - 0.15, cy + 0.03, -0.02), PH.pbr(bpy, 'smoked_walnut_veneer', '2k', rough_mul=0.8, name='walnut'), bev=0.002)
        front = boxo('sideboard-body', (1.6, 0.50, 0.70), (cx - 0.15, cy + 0.04, -0.39), PH.pbr(bpy, 'smoked_walnut_veneer', '2k', name='walnut2'), bev=0.002)
        wall = boxo('wall', (5.0, 0.05, 3.0), (cx, cy + 0.42, 1.0), PH.pbr(bpy, 'beige_wall_001', '2k', bump=0.25, name='plaster'), bev=0)
        floor = boxo('floor', (6.0, 6.0, 0.02), (cx, cy, -0.75), dielectric('floorc', '#5A4A3C', 0.6), bev=0)

    # mark casters and receivers for MNEE
    for o in bpy.data.objects:
        if o.type == 'MESH':
            o.visible_shadow = True
            if o.get('caustic'):
                o.cycles.is_caustics_caster = True
            if o.get('receiver'):
                o.cycles.is_caustics_receiver = True

    # camera
    cam = bpy.data.cameras.new('cam'); co = bpy.data.objects.new('cam', cam); bpy.context.collection.objects.link(co)
    sc.camera = co
    shots = {
        'hero': dict(pos=(cx + 0.78, cy - 1.32, 0.62), tgt=(cx - 0.005, cy + 0.01, 0.075), lens=85, f=8.0, focus=(cx + 0.06, cy - 0.10, 0.08)),
        'closed': dict(pos=(cx + 0.78, cy - 1.32, 0.52), tgt=(cx, cy + 0.01, 0.085), lens=85, f=8.0, focus=(cx + 0.05, cy - 0.15, 0.09)),
        'macro': dict(pos=(meta['A'][0] * mm + 0.27, meta['A'][1] * mm - 0.50, meta['top'] * mm + 0.15),
                      tgt=(meta['A'][0] * mm - 0.07, meta['A'][1] * mm - 0.13, meta['top'] * mm - 0.010), lens=100, f=8.0,
                      focus=(meta['A'][0] * mm - 0.02, meta['A'][1] * mm - 0.12, meta['top'] * mm)),
        'macro-stylus': dict(pos=(meta['stylus'][0] * mm + 0.17, meta['stylus'][1] * mm - 0.25, meta['record_z'] * mm + 0.075),
                             tgt=(meta['stylus'][0] * mm - 0.01, meta['stylus'][1] * mm + 0.01, meta['record_z'] * mm - 0.012), lens=100, f=11.0,
                             focus=(meta['stylus'][0] * mm, meta['stylus'][1] * mm, meta['record_z'] * mm)),
        'use': dict(pos=(cx + 0.62, cy - 1.12, 0.40), tgt=(cx - 0.17, cy + 0.06, 0.12), lens=50, f=5.6, focus=None),
        'stand': dict(pos=(cx + 0.30, cy - 1.6, 0.55), tgt=(cx - 0.20, cy + 0.10, 0.12), lens=60, f=8.0, focus=(cx, cy - 0.1, 0.08)),
    }
    s = shots[args.shot]
    co.location = s['pos']
    co.rotation_euler = (Vector(s['tgt']) - Vector(s['pos'])).to_track_quat('-Z', 'Y').to_euler()
    cam.lens = s['lens']; cam.sensor_width = 36
    cam.dof.use_dof = True; cam.dof.aperture_fstop = s['f']; cam.dof.aperture_blades = 9; cam.dof.aperture_rotation = 0.2
    if s['focus'] is None:
        A = meta['A']
        s['focus'] = (A[0] * mm + 0.03, A[1] * mm - 0.05, meta['top'] * mm + 0.02)
    fe = bpy.data.objects.new('focus', None); bpy.context.collection.objects.link(fe); fe.location = s['focus']
    cam.dof.focus_object = fe

    if args.shot == 'use_hand':
        # the hand on the cue lever
        A = meta['A']
        ang = math.radians(meta['rest_deg'])
        hand(bpy.data.materials and {'skin': bpy.data.materials['skin'], 'knit': bpy.data.materials['knit']},
             (A[0] * mm + 0.075, A[1] * mm - 0.035, meta['top'] * mm + 0.020), math.radians(-150))

    r = sc.render
    r.engine = 'CYCLES'
    cy_ = sc.cycles
    cy_.device = 'CPU'; cy_.samples = args.samples; cy_.use_adaptive_sampling = True; cy_.adaptive_threshold = 0.01
    cy_.use_denoising = True; cy_.denoiser = 'OPENIMAGEDENOISE'
    cy_.max_bounces = 24; cy_.transmission_bounces = 24; cy_.glossy_bounces = 12; cy_.volume_bounces = 2
    cy_.caustics_reflective = False; cy_.caustics_refractive = False
    cy_.sample_clamp_indirect = 8.0
    cy_.use_light_tree = True
    r.resolution_x = int(args.size[0] * args.scale); r.resolution_y = int(args.size[1] * args.scale)
    r.film_transparent = False
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.view_settings.exposure = args.exposure
    r.image_settings.file_format = 'PNG'; r.image_settings.color_depth = '16'


def wood_material():
    m, nt, out = node_tree('walnut')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (2.0, 60.0, 2.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.inputs['Scale'].default_value = 3.0
    wv.inputs['Distortion'].default_value = 6.0; wv.inputs['Detail'].default_value = 4
    nt.links.new(mp.outputs['Vector'], wv.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = tuple(lin('#3A2418')) + (1,); ramp.color_ramp.elements[1].color = tuple(lin('#6B4630')) + (1,)
    nt.links.new(wv.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.42; b.inputs['Coat Weight'].default_value = 0.3; b.inputs['Coat Roughness'].default_value = 0.25
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def post(path, grain=0.012, vignette=0.12):
    """A real camera's last mile: a light vignette and luminance grain, then 8-bit."""
    import numpy as np
    from PIL import Image
    im = np.asarray(Image.open(path)).astype(np.float32)
    if im.max() > 255:
        im = im / 257.0
    h, w = im.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2)
    im = im * (1 - vignette * r ** 2)[..., None]
    rng = np.random.default_rng(7)
    g = rng.normal(0, 1, (h, w)).astype(np.float32)
    lum = im.mean(axis=2, keepdims=True) / 255
    im = im + (grain * 255 * np.sqrt(np.clip(lum, 0.02, 1)))[..., 0][..., None] * g[..., None]
    Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)[..., :3]).save(path, optimize=True)


if __name__ == '__main__' and bpy is None:
    if sys.argv[1] == '--label':
        make_label(sys.argv[2])
    elif sys.argv[1] == '--sleeve':
        make_sleeve(sys.argv[2])
    elif sys.argv[1] == '--post':
        post(sys.argv[2])
    sys.exit(0)

if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument('shot'); ap.add_argument('--colour', default='smoke'); ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=256); ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--size', type=int, nargs=2, default=(2400, 1600)); ap.add_argument('--model', default='out-core')
    ap.add_argument('--paper', default='#2A2826'); ap.add_argument('--exposure', type=float, default=0.0)
    ap.add_argument('--spot', type=float, default=12.0); ap.add_argument('--label-deg', type=float, default=35.0)
    ap.add_argument('--blend', default=None); ap.add_argument('--strip', type=float, default=0.0)
    a = ap.parse_args(argv)
    build(a)
    if a.blend:
        bpy.ops.wm.save_as_mainfile(filepath=a.blend)
    bpy.context.scene.render.filepath = a.out
    bpy.ops.render.render(write_still=True)
    import subprocess
    subprocess.run(['python3', os.path.abspath(__file__), '--post', a.out], check=True)
    print('wrote', a.out)
