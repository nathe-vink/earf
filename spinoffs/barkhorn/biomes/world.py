"""Planet EARF: one world where the eight biomes meet, a Tropos in each tint standing in its own (r48-biomes).

    python3.11 spinoffs/barkhorn/biomes/world.py --out DIR [--width 2048] [--samples 32] [--only 0 3 ...]
                                                  [--lat -90 90] [--save-blend PATH]

Builds the world once (field.py says what grows where), then renders it from one camera at the centre of the ring as
an equirectangular frame, once per biome: each render under that biome's own hour (its sky and sun, from dawn over the
snow to night in the city), cropped to that biome's sector and the blends either side. composite.py lays the eight
together, weighing each pixel by the biome its first hit belongs to (a position pass rendered here once): a day-to-night
time slice, as a photographer makes one from a fixed camera. Physically based within each slice: Cycles, the
multiple-scattering sky, the acrylic at IOR 1.49 with TruCast tints (tints.json), real scale, real volumes.

The speakers are linked, not appended, from assets/tropos-current.blend (tropos_lib.py), one collection per tint; point
--tropos at another .blend with the same collection names to swap the model.
"""
import argparse, json, math, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import numpy as np                                        # noqa: E402
import field as F                                         # noqa: E402

CAM_Z = 1.55                                              # the lens, metres over the centre's dome
TROPOS = os.path.join(HERE, 'assets', 'tropos-current.blend')

# Each biome's hour. sun: elevation and azimuth offset from the sector's centre line (deg); sky: air, aerosols
# (dust), ozone; strength scales the sky; exposure is the photographer's for that slice (EV).
HOURS = [
    dict(name='Ice',    hour='dawn',            sun_el=-1.5, sun_off=-16, air=1.0, dust=1.0, ozone=1.0, strength=1.0, ev=2.6, key=0.15),
    dict(name='Poison', hour='early morning',   sun_el=14.0, sun_off=16,  air=1.0, dust=2.0, ozone=1.0, strength=1.0, ev=0.0, key=0.1),
    dict(name='Fog',    hour='morning',         sun_el=24.0, sun_off=-14, air=1.0, dust=1.2, ozone=1.0, strength=1.0, ev=-0.9, key=0.2),
    dict(name='Haze',   hour='late afternoon',  sun_el=8.0, sun_off=15,  air=1.2, dust=3.0, ozone=1.0, strength=1.0, ev=-0.6, key=0.16),
    dict(name='Dust',   hour='golden hour',     sun_el=5.0,  sun_off=-15, air=1.0, dust=2.5, ozone=1.0, strength=1.0, ev=-0.1, key=0.16),
    dict(name='Acid',   hour='sunset, in rain', sun_el=1.2,  sun_off=17,  air=1.6, dust=6.0, ozone=1.0, strength=0.6, ev=1.2, key=0.07),
    dict(name='Ember',  hour='blue hour',       sun_el=-4.5, sun_off=-15, air=1.0, dust=1.0, ozone=1.6, strength=1.0, ev=3.6, key=0.045),
    dict(name='Smoke',  hour='night',           sun_el=-14., sun_off=15,  air=1.0, dust=1.0, ozone=1.0, strength=1.0, ev=6.0, key=0.035),
]
TINT = {n: n for n in F.NAMES}                            # each biome's Tropos is its own tint


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


# --- the ground ------------------------------------------------------------------------------------------------------
def rings(r0=0.04, r1=4500.0, k=1.0):
    """Ring radii: a centre cap, then geometric steps about k x the angular step (0.25 deg)."""
    out = [0.0, r0]
    step = math.radians(0.25) * 2.0 * k
    while out[-1] < r1:
        out.append(out[-1] * (1 + step) + 0.002)
    return np.array(out)


def terrain(bpy, mats, segs=1440, lod=1.0):
    """Eight wedge meshes (one per sector, sharing their edges) with heights from field.height and the biomes'
    weights as two float colour attributes (wA: 0-3, wB: 4-7)."""
    R = rings(k=lod)
    per = segs // F.N
    objs = []
    for i in range(F.N):
        a0 = F.centre_az(i) - F.SECTOR / 2
        az = np.radians(a0 + np.arange(per + 1) * (F.SECTOR / per))
        rr, aa = np.meshgrid(R[1:], az, indexing='ij')
        x = rr * np.sin(aa); y = rr * np.cos(aa)
        W = F.weights(x, y)
        z = F.height(x, y, W)
        V = np.stack([x, y, z], -1).reshape(-1, 3)
        Wv = W.reshape(-1, 8)
        nr, na = rr.shape
        # the centre point
        V = np.vstack([[0.0, 0.0, float(F.height(np.array([0.0]), np.array([0.0]))[0])], V])
        Wv = np.vstack([np.full(8, 1 / 8), Wv])
        idx = lambda r, a: 1 + r * na + a
        faces = [(0, idx(0, a), idx(0, a + 1)) for a in range(na - 1)]
        rI, aI = np.meshgrid(np.arange(nr - 1), np.arange(na - 1), indexing='ij')
        q = np.stack([idx(rI, aI), idx(rI + 1, aI), idx(rI + 1, aI + 1), idx(rI, aI + 1)], -1).reshape(-1, 4)
        me = bpy.data.meshes.new(f'ground.{F.NAMES[i]}')
        me.from_pydata(V.tolist(), [], faces + [tuple(f) for f in q.tolist()])
        me.update()
        for nm, sl in (('wA', slice(0, 4)), ('wB', slice(4, 8))):
            at = me.color_attributes.new(nm, 'FLOAT_COLOR', 'POINT')
            at.data.foreach_set('color', Wv[:, sl].astype(np.float32).ravel())
        me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
        me.materials.append(mats[i])
        ob = bpy.data.objects.new(f'ground.{F.NAMES[i]}', me)
        bpy.context.scene.collection.objects.link(ob)
        objs.append(ob)
    return objs


# --- materials -------------------------------------------------------------------------------------------------------
class NT:
    """A small helper over a node tree."""
    def __init__(self, nt):
        self.nt = nt

    def n(self, kind, **k):
        node = self.nt.nodes.new(kind)
        for a, v in k.items():
            if a.startswith('i_'):
                node.inputs[int(a[2:]) if a[2:].isdigit() else a[2:].replace('__', ' ')].default_value = v
            else:
                setattr(node, a, v)
        return node

    def l(self, a, b):
        self.nt.links.new(a, b)

    def math(self, op, a, b=None, c=None, clamp=False):
        m = self.n('ShaderNodeMath', operation=op, use_clamp=clamp)
        for k, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[k].default_value = v
            else:
                self.l(v, m.inputs[k])
        return m.outputs[0]

    def mix(self, a, b, t, kind='RGBA', blend='MIX'):
        m = self.n('ShaderNodeMix', data_type=kind, blend_type=blend)
        ins = {'RGBA': ('A', 'B'), 'FLOAT': (2, 3), 'VECTOR': (4, 5)}[kind]
        if kind == 'RGBA':
            ia, ib = m.inputs[6], m.inputs[7]
        elif kind == 'FLOAT':
            ia, ib = m.inputs[2], m.inputs[3]
        else:
            ia, ib = m.inputs[4], m.inputs[5]
        for s, v in ((ia, a), (ib, b)):
            if isinstance(v, (tuple, list)):
                s.default_value = (*v, 1.0)[:len(s.default_value)] if kind == 'RGBA' else v
            elif isinstance(v, (int, float)):
                s.default_value = v
            else:
                self.l(v, s)
        if isinstance(t, (int, float)):
            m.inputs[0].default_value = t
        else:
            self.l(t, m.inputs[0])
        return m.outputs[{'RGBA': 2, 'FLOAT': 0, 'VECTOR': 1}[kind]]


def tex_paths(aid, res='2k'):
    import assets
    return assets.texture(aid, res)


def img(bpy, T, path, colour, vec, proj='FLAT'):
    n = T.n('ShaderNodeTexImage')
    n.image = bpy.data.images.load(os.path.abspath(path), check_existing=True)
    if not colour:
        n.image.colorspace_settings.name = 'Non-Color'
    n.projection = proj
    T.l(vec, n.inputs['Vector'])
    return n


def pbr_layer(bpy, T, aid, scale, tint=None, tint_mix=0.0, value=1.0, rough_mul=1.0, rough_add=0.0, bump=1.0,
              res='2k', far=8.0):
    """A ground texture laid in plan (object x, y) at `scale` metres a tile, and again at `far` x that size beyond 30 m
    so it does not tile at range. Returns (colour, roughness, normal, height) sockets."""
    maps = tex_paths(aid, res)
    tc = T.n('ShaderNodeTexCoord')
    pos = tc.outputs['Object']
    r = T.n('ShaderNodeVectorMath', operation='LENGTH'); T.l(pos, r.inputs[0])
    farw = T.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP'); T.l(r.outputs['Value'], farw.inputs[0])
    farw.inputs[1].default_value = 15.0; farw.inputs[2].default_value = 60.0
    out = {}
    for lvl, s in (('near', scale), ('far', scale * far)):
        mp = T.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / s, 1 / s, 1 / s)
        mp.inputs['Rotation'].default_value = (0, 0, 0.7 if lvl == 'far' else 0.0)
        T.l(pos, mp.inputs['Vector'])
        v = mp.outputs['Vector']
        out[lvl] = {k: img(bpy, T, maps[m], k == 'col', v) for k, m in (('col', 'diff'), ('rough', 'rough'), ('nor', 'nor_gl'),
                                                                        ('disp', 'disp')) if m in maps}
    fw = farw.outputs['Result']
    col = T.mix(out['near']['col'].outputs['Color'], out['far']['col'].outputs['Color'], fw)
    if tint and tint_mix > 0:
        col = T.mix(col, lin(tint), tint_mix, blend='COLOR')
    if value != 1.0:
        col = T.mix(col, (value, value, value), 1.0, blend='MULTIPLY')
    rough = T.mix(out['near']['rough'].outputs['Color'], out['far']['rough'].outputs['Color'], fw)
    rr = T.n('ShaderNodeMath', operation='MULTIPLY_ADD', use_clamp=True)
    T.l(rough, rr.inputs[0]); rr.inputs[1].default_value = rough_mul; rr.inputs[2].default_value = rough_add
    nor_c = T.mix(out['near']['nor'].outputs['Color'], out['far']['nor'].outputs['Color'], fw)
    nm = T.n('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = bump; T.l(nor_c, nm.inputs['Color'])
    hgt = T.mix(out['near']['disp'].outputs['Color'], out['far']['disp'].outputs['Color'], fw, kind='FLOAT') \
        if 'disp' in out['near'] else None
    return col, rr.outputs[0], nm.outputs['Normal'], hgt


def biome_bsdf(bpy, T, i):
    """The ground of biome i as one Principled BSDF (its texture at real size, its own wetness, glow or snow)."""
    b = T.n('ShaderNodeBsdfPrincipled')
    name = F.NAMES[i]
    tc = T.n('ShaderNodeTexCoord'); pos = tc.outputs['Object']
    geo = T.n('ShaderNodeNewGeometry')
    sep = T.n('ShaderNodeSeparateXYZ'); T.l(geo.outputs['Normal'], sep.inputs[0])
    flat = sep.outputs['Z']                                   # 1 on level ground, 0 on a cliff
    if name == 'Ice':
        col, rough, nor, h = pbr_layer(bpy, T, 'snow_02', 2.5, value=1.0, bump=0.6)
        rock, rrough, rnor, _ = pbr_layer(bpy, T, 'cliff_side', 6.0, tint='#59606A', tint_mix=0.4, value=0.7)
        steep = T.math('POWER', T.math('SUBTRACT', 1.0, flat, clamp=True), 0.6)
        st = T.n('ShaderNodeMapRange'); T.l(steep, st.inputs[0]); st.inputs[1].default_value = 0.55; st.inputs[2].default_value = 0.75
        col = T.mix(col, rock, st.outputs[0]); rough = T.mix(rough, rrough, st.outputs[0], kind='FLOAT')
        T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
        b.inputs['Subsurface Weight'].default_value = 0.25
        b.inputs['Subsurface Radius'].default_value = (0.6, 0.8, 1.0)
        b.inputs['Subsurface Scale'].default_value = 0.02
    elif name == 'Poison':
        col, rough, nor, h = pbr_layer(bpy, T, 'forrest_ground_01', 2.0, tint='#4A3524', tint_mix=0.15, value=0.85)
        T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
    elif name == 'Fog':
        col, rough, nor, h = pbr_layer(bpy, T, 'aerial_grass_rock', 5.0, tint='#4F6234', tint_mix=0.5, value=0.8)
        rock, rrough, rnor, _ = pbr_layer(bpy, T, 'cliff_side', 8.0, tint='#6B6458', tint_mix=0.3, value=0.8)
        steep = T.math('SUBTRACT', 1.0, flat, clamp=True)
        st = T.n('ShaderNodeMapRange'); T.l(steep, st.inputs[0]); st.inputs[1].default_value = 0.25; st.inputs[2].default_value = 0.45
        col = T.mix(col, rock, st.outputs[0])
        T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
    elif name == 'Haze':
        col, rough, nor, h = pbr_layer(bpy, T, 'withered_grass', 1.6, tint='#9C7A3E', tint_mix=0.5, value=0.8)
        T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
    elif name == 'Dust':
        col, rough, nor, h = pbr_layer(bpy, T, 'aerial_sand', 3.0, tint='#B8693A', tint_mix=0.7, value=0.8, bump=1.0)
        rock, rrough, rnor, _ = pbr_layer(bpy, T, 'cliff_side', 10.0, tint='#9A5232', tint_mix=0.55, value=0.9)
        steep = T.math('SUBTRACT', 1.0, flat, clamp=True)
        st = T.n('ShaderNodeMapRange'); T.l(steep, st.inputs[0]); st.inputs[1].default_value = 0.2; st.inputs[2].default_value = 0.4
        col = T.mix(col, rock, st.outputs[0])
        # strata in the mesas' cliffs: bands by height
        sz = T.n('ShaderNodeSeparateXYZ'); T.l(pos, sz.inputs[0])
        wv = T.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction='Z'); T.l(pos, wv.inputs['Vector'])
        wv.inputs['Scale'].default_value = 0.004; wv.inputs['Distortion'].default_value = 3.0; wv.inputs['Detail'].default_value = 4.0
        band = T.mix((1.0, 1.0, 1.0), lin('#C8A07A'), T.math('MULTIPLY', wv.outputs['Fac'], 0.6))
        col = T.mix(col, T.mix(col, band, 1.0, blend='MULTIPLY'), st.outputs[0])
        T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
    elif name in ('Acid', 'Ember'):
        col, rough, nor, h = pbr_layer(bpy, T, 'dark_rock_02', 2.2, tint='#262626', tint_mix=0.5, value=0.55)
        if name == 'Acid':
            # rain on black rock: wet all over, standing water in the low places (the height map's hollows)
            nz = T.n('ShaderNodeTexNoise'); T.l(pos, nz.inputs['Vector']); nz.inputs['Scale'].default_value = 0.6
            nz.inputs['Detail'].default_value = 6.0
            pud = T.n('ShaderNodeMapRange'); T.l(nz.outputs['Fac'], pud.inputs[0])
            pud.inputs[1].default_value = 0.56; pud.inputs[2].default_value = 0.60
            wet = T.math('MULTIPLY', pud.outputs[0], flat)
            col = T.mix(col, (0.012, 0.012, 0.011), wet)
            rough = T.mix(T.math('MULTIPLY', rough, 0.35), 0.02, wet, kind='FLOAT')
            nor = T.mix(nor, geo.outputs['Normal'], wet, kind='VECTOR')
            b.inputs['Coat Weight'].default_value = 0.6; b.inputs['Coat Roughness'].default_value = 0.05
        T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
        if name == 'Ember':
            # the crust cracked to its glow: Voronoi edges, widened in the low places, hotter where wider
            dn = T.n('ShaderNodeTexNoise'); T.l(pos, dn.inputs['Vector']); dn.inputs['Scale'].default_value = 1.5
            dn.inputs['Detail'].default_value = 4.0
            dv = T.n('ShaderNodeVectorMath', operation='MULTIPLY_ADD'); T.l(dn.outputs['Color'], dv.inputs[0])
            dv.inputs[1].default_value = (0.35, 0.35, 0.35); T.l(pos, dv.inputs[2])
            vo = T.n('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE'); T.l(dv.outputs[0], vo.inputs['Vector'])
            vo.inputs['Scale'].default_value = 0.8; vo.inputs['Randomness'].default_value = 1.0
            wn = T.n('ShaderNodeTexNoise'); T.l(pos, wn.inputs['Vector']); wn.inputs['Scale'].default_value = 0.35
            width = T.math('MULTIPLY_ADD', wn.outputs['Fac'], 0.075, -0.034)
            crack = T.math('SUBTRACT', 1.0, T.math('DIVIDE', vo.outputs['Distance'], T.math('MAXIMUM', width, 0.002)), clamp=True)
            hot = T.math('POWER', crack, 1.5)
            bb = T.n('ShaderNodeBlackbody'); bb.inputs[0].default_value = 1350.0
            T.l(bb.outputs[0], b.inputs['Emission Color'])
            T.l(T.math('MULTIPLY', hot, 9.0), b.inputs['Emission Strength'])
    elif name == 'Smoke':
        col, rough, nor, h = pbr_layer(bpy, T, 'asphalt_02', 3.0, value=0.8)
        T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
    return b.outputs['BSDF']


def ground_material(bpy, centre):
    """The ground of wedge `centre`: its biome and its two neighbours mixed by the weights (Cycles holds 64 closures
    a shader; eight Principled BSDFs overflowed)."""
    keep = {(centre - 1) % F.N, centre, (centre + 1) % F.N}
    m = bpy.data.materials.new(f'ground.{F.NAMES[centre]}'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); T = NT(nt)
    out = T.n('ShaderNodeOutputMaterial')
    wa = T.n('ShaderNodeAttribute', attribute_name='wA', attribute_type='GEOMETRY')
    wb = T.n('ShaderNodeAttribute', attribute_name='wB', attribute_type='GEOMETRY')
    sa = T.n('ShaderNodeSeparateColor'); T.l(wa.outputs['Color'], sa.inputs[0])
    sb = T.n('ShaderNodeSeparateColor'); T.l(wb.outputs['Color'], sb.inputs[0])
    w = [sa.outputs[0], sa.outputs[1], sa.outputs[2], wa.outputs['Alpha'],
         sb.outputs[0], sb.outputs[1], sb.outputs[2], wb.outputs['Alpha']]
    # break the blends up at the scale of a footstep: each weight pushed by its own noise, then sharpened
    tc = T.n('ShaderNodeTexCoord')
    nz = T.n('ShaderNodeTexNoise', noise_dimensions='3D'); T.l(tc.outputs['Object'], nz.inputs['Vector'])
    nz.inputs['Scale'].default_value = 1.3; nz.inputs['Detail'].default_value = 8.0; nz.inputs['Roughness'].default_value = 0.6
    sep = T.n('ShaderNodeSeparateColor'); T.l(nz.outputs['Color'], sep.inputs[0])
    jit = [sep.outputs[k % 3] for k in range(8)]
    ws = []
    for k in range(8):
        v = T.math('MULTIPLY_ADD', T.math('SUBTRACT', jit[k], 0.5), 0.9, w[k])        # w + 0.9 (n - 0.5)
        v = T.math('MULTIPLY', T.math('SUBTRACT', v, 0.15, clamp=True), 1.6)
        ws.append(T.math('MINIMUM', v, 1.0))
    # mix down the chain: shader_k = mix(shader_{k-1}, bsdf_k, w_k / (w_0 + ... + w_k))
    acc = None; tot = None
    for k in sorted(keep):
        bs = biome_bsdf(bpy, T, k)
        if acc is None:
            acc, tot = bs, ws[k]
            continue
        tot = T.math('ADD', tot, ws[k])
        t = T.math('DIVIDE', ws[k], T.math('MAXIMUM', tot, 1e-4))
        mx = T.n('ShaderNodeMixShader'); T.l(t, mx.inputs[0]); T.l(acc, mx.inputs[1]); T.l(bs, mx.inputs[2])
        acc = mx.outputs[0]
    T.l(acc, out.inputs['Surface'])
    return m


def simple_mat(bpy, name, color, rough=0.6, emit=None, emit_strength=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*lin(color), 1)
    b.inputs['Roughness'].default_value = rough
    if emit:
        b.inputs['Emission Color'].default_value = (*lin(emit), 1); b.inputs['Emission Strength'].default_value = emit_strength
    return m


def bark_material(bpy, aid='bark_brown_02', tint='#7A3B22', mix=0.45, scale=1.4):
    m = bpy.data.materials.new('redwood-bark'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); T = NT(nt)
    out = T.n('ShaderNodeOutputMaterial'); b = T.n('ShaderNodeBsdfPrincipled')
    maps = tex_paths(aid)
    tc = T.n('ShaderNodeTexCoord')
    mp = T.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / scale, 1 / scale, 1 / (scale * 2.5))
    T.l(tc.outputs['Object'], mp.inputs['Vector'])
    c = img(bpy, T, maps['diff'], True, mp.outputs['Vector'], 'BOX'); c.projection_blend = 0.3
    r = img(bpy, T, maps['rough'], False, mp.outputs['Vector'], 'BOX')
    n = img(bpy, T, maps['nor_gl'], False, mp.outputs['Vector'], 'BOX')
    col = T.mix(c.outputs['Color'], lin(tint), mix, blend='COLOR')
    T.l(col, b.inputs['Base Color']); T.l(r.outputs['Color'], b.inputs['Roughness'])
    nm = T.n('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 1.5; T.l(n.outputs['Color'], nm.inputs['Color'])
    T.l(nm.outputs['Normal'], b.inputs['Normal'])
    T.l(b.outputs[0], out.inputs['Surface'])
    return m


# --- what grows and stands in each biome ------------------------------------------------------------------------------
def rng_points(rng, n, rmin, rmax, i, spread=1.0, minsep=0.0, avoid_speaker=1.2):
    """n points in biome i's sector between rmin and rmax (area-uniform), kept where the field says it is i's ground."""
    pts = []
    tries = 0
    while len(pts) < n and tries < n * 60:
        tries += 1
        r = math.sqrt(rng.uniform(rmin ** 2, rmax ** 2))
        a = math.radians(F.centre_az(i) + rng.uniform(-1, 1) * (F.SECTOR / 2 + F.BAND) * spread)
        x, y = r * math.sin(a), r * math.cos(a)
        w = F.weights(np.array([x]), np.array([y]))[0, i]
        if rng.random() > w ** 1.5:
            continue
        sx, sy = F.speaker_spot(i)
        if math.hypot(x - sx, y - sy) < avoid_speaker:
            continue
        if minsep and any((x - p[0]) ** 2 + (y - p[1]) ** 2 < minsep ** 2 for p in pts):
            continue
        pts.append((x, y))
    return pts


def ground_z(x, y):
    return float(F.height(np.array([x]), np.array([y]))[0])


def redwoods(bpy, rng):
    """Coast redwoods: straight columns 2 to 4.5 m through, rising out of frame, fluted at the foot."""
    import bmesh
    mat = bark_material(bpy)
    crowns = []
    pts = rng_points(rng, 34, 6.0, 90.0, 1, minsep=5.0, avoid_speaker=3.0)
    pts += rng_points(rng, 50, 90.0, 260.0, 1, minsep=9.0)
    objs = []
    for k, (x, y) in enumerate(pts):
        r = math.hypot(x, y)
        d = rng.uniform(1.6, 4.2) if r < 90 else rng.uniform(1.4, 3.0)
        hgt = rng.uniform(70, 95)
        bm = bmesh.new()
        seg, rows = 40, 24
        prev = None
        gz = ground_z(x, y)
        for j in range(rows + 1):
            t = j / rows
            z = -1.0 + hgt * t ** 1.6
            rad = d / 2 * (1.0 - 0.55 * (z / hgt)) * (1 + 0.6 * math.exp(-max(z, 0) / 1.5))
            ring = []
            for s in range(seg):
                a = 2 * math.pi * s / seg
                flute = 1 + 0.06 * math.sin(a * 7 + k) * math.exp(-max(z, 0) / 3.0)
                ring.append(bm.verts.new((x + rad * flute * math.cos(a), y + rad * flute * math.sin(a), gz + z)))
            if prev:
                for s in range(seg):
                    bm.faces.new((prev[s], prev[(s + 1) % seg], ring[(s + 1) % seg], ring[s]))
            prev = ring
        me = bpy.data.meshes.new(f'redwood{k}'); bm.to_mesh(me); bm.free()
        me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
        me.materials.append(mat)
        ob = bpy.data.objects.new(f'redwood{k}', me); bpy.context.scene.collection.objects.link(ob); objs.append(ob)
        crowns.append((x, y, gz + hgt * rng.uniform(0.30, 0.42), d))
    # the crowns: the fir scan stretched to a redwood's narrow spire, from about a third of the way up
    tops = asset_instances(bpy, 'fir_tree_01', [(c[0], c[1]) for c in crowns], (1.0, 1.0), rng)
    for k, e in enumerate(tops):
        x, y, z, d = crowns[k]
        e.location.z = z
        s_ = (50.0 / 18.8) * rng.uniform(0.8, 1.1)
        e.scale = (s_ * 0.55 * d / 3.0, s_ * 0.55 * d / 3.0, s_)
    return objs


def city(bpy, rng):
    """The city's edge at night: blocks from two storeys to towers, their windows lit at random, streetlights."""
    import bmesh
    win = bpy.data.materials.new('facade'); win.use_nodes = True
    nt = win.node_tree; nt.nodes.clear(); T = NT(nt)
    out = T.n('ShaderNodeOutputMaterial'); b = T.n('ShaderNodeBsdfPrincipled')
    tc = T.n('ShaderNodeTexCoord'); ob_info = T.n('ShaderNodeObjectInfo')
    # windows on a 3.4 m x 3.2 m grid in object space, lit by a hash of the cell
    sep = T.n('ShaderNodeSeparateXYZ'); T.l(tc.outputs['Object'], sep.inputs[0])
    u = T.math('ADD', sep.outputs['X'], sep.outputs['Y'])
    cu = T.math('DIVIDE', u, 3.2); cz = T.math('DIVIDE', sep.outputs['Z'], 3.4)
    fu = T.math('FRACT', cu); fz = T.math('FRACT', cz)
    inwin = T.math('MULTIPLY', T.math('MULTIPLY', T.math('GREATER_THAN', fu, 0.18), T.math('LESS_THAN', fu, 0.82)),
                   T.math('MULTIPLY', T.math('GREATER_THAN', fz, 0.25), T.math('LESS_THAN', fz, 0.8)))
    cell = T.n('ShaderNodeCombineXYZ'); T.l(T.math('FLOOR', cu), cell.inputs[0]); T.l(T.math('FLOOR', cz), cell.inputs[1])
    T.l(ob_info.outputs['Random'], cell.inputs[2])
    wh = T.n('ShaderNodeTexWhiteNoise', noise_dimensions='3D'); T.l(cell.outputs[0], wh.inputs['Vector'])
    lit = T.math('GREATER_THAN', wh.outputs['Value'], 0.72)
    warm = T.mix(lin('#FFB36B'), lin('#CFE3FF'), T.math('GREATER_THAN', wh.outputs['Value'], 0.93))
    e = T.math('MULTIPLY', inwin, lit)
    T.l(warm, b.inputs['Emission Color'])
    T.l(T.math('MULTIPLY', e, T.math('MULTIPLY_ADD', wh.outputs['Value'], 2.5, 0.4)), b.inputs['Emission Strength'])
    T.l(T.mix(lin('#3A3B3E'), lin('#0C0D10'), inwin), b.inputs['Base Color'])
    T.l(T.mix(0.8, 0.08, inwin, kind='FLOAT'), b.inputs['Roughness'])
    T.l(b.outputs[0], out.inputs['Surface'])
    objs = []
    pts = rng_points(rng, 40, 55.0, 180.0, 7, minsep=18.0, spread=0.8)
    pts += rng_points(rng, 140, 180.0, 1200.0, 7, minsep=40.0, spread=0.8)
    for k, (x, y) in enumerate(pts):
        r = math.hypot(x, y)
        w_ = rng.uniform(10, 30) * (1 + r / 600); dpt = rng.uniform(10, 26) * (1 + r / 600)
        h = rng.choice([7, 10, 14, 20, 28, 36, 48, 70, 95, 130]) * (0.6 if r < 70 else 1.0) * (1.0 + r / 700)
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co.x *= w_; v.co.y *= dpt; v.co.z = (v.co.z + 0.5) * h - 1.0
        me = bpy.data.meshes.new(f'block{k}'); bm.to_mesh(me); bm.free(); me.materials.append(win)
        ob = bpy.data.objects.new(f'block{k}', me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (x, y, ground_z(x, y)); ob.rotation_euler = (0, 0, math.atan2(x, y) + rng.uniform(-0.2, 0.2))
        objs.append(ob)
    # streetlights along the near road, sodium and LED; the first just behind the speaker, to its left
    a7 = math.radians(F.centre_az(7) - 9.0)
    near = [(6.2 * math.sin(a7), 6.2 * math.cos(a7))]
    for k, (x, y) in enumerate(near + rng_points(rng, 8, 12.0, 45.0, 7, minsep=7.0, spread=0.7)):
        z0 = ground_z(x, y)
        pole = simple_mat(bpy, 'pole', '#2A2B2D', 0.5)
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.09, radius2=0.06, depth=8.0)
        me = bpy.data.meshes.new('pole'); bm.to_mesh(me); bm.free(); me.materials.append(pole)
        ob = bpy.data.objects.new('pole', me); bpy.context.scene.collection.objects.link(ob); ob.location = (x, y, z0 + 4.0)
        ld = bpy.data.lights.new('street', 'POINT'); ld.energy = 900.0; ld.shadow_soft_size = 0.15
        ld.color = lin('#FFB060') if k % 3 else lin('#DDE6FF')
        lo = bpy.data.objects.new('street', ld); bpy.context.scene.collection.objects.link(lo); lo.location = (x, y, z0 + 7.9)
        objs.append(ob)
    return objs


FLORA = os.path.join(HERE, 'assets', 'flora.blend')
_FLORA = {}


def asset_instances(bpy, aid, pts, scale=(0.8, 1.2), rng=None, z_off=0.0, rot=True):
    """Copies of a plant or rock from flora.blend (flora_lib.py), as collection instances on the ground."""
    if not _FLORA:
        with bpy.data.libraries.load(FLORA, link=True) as (src, dst):
            dst.collections = list(src.collections)
        _FLORA.update({c.name.split('.', 1)[1]: c for c in dst.collections if c})
    out = []
    for k, (x, y) in enumerate(pts):
        e = bpy.data.objects.new(f'{aid}.{k}', None)
        e.instance_type = 'COLLECTION'; e.instance_collection = _FLORA[aid]
        e.location = (x, y, ground_z(x, y) + z_off)
        e.rotation_euler = (0, 0, math.radians(rng.uniform(0, 360)) if rot else 0)
        e.scale = (rng.uniform(*scale),) * 3
        bpy.context.scene.collection.objects.link(e)
        out.append(e)
    return out


def flora(bpy, rng):
    objs = []
    objs += asset_instances(bpy, 'fir_tree_01', rng_points(rng, 40, 9.0, 140.0, 0, minsep=4.0), (0.9, 1.6), rng)
    objs += asset_instances(bpy, 'fern_02', rng_points(rng, 70, 1.2, 14.0, 1, minsep=0.8, avoid_speaker=0.9), (0.9, 1.6), rng)
    objs += asset_instances(bpy, 'island_tree_01', rng_points(rng, 14, 25.0, 300.0, 3, minsep=20.0), (0.7, 1.1), rng)
    objs += asset_instances(bpy, 'didelta_spinosa', rng_points(rng, 25, 4.0, 60.0, 4, minsep=3.0), (0.7, 1.3), rng)
    objs += asset_instances(bpy, 'namaqualand_boulder_02', rng_points(rng, 10, 6.0, 80.0, 4, minsep=6.0), (0.6, 1.4), rng)
    objs += asset_instances(bpy, 'rock_07', rng_points(rng, 10, 5.0, 22.0, 2, minsep=4.0), (0.8, 1.6), rng)
    objs += asset_instances(bpy, 'grass_medium_01', rng_points(rng, 260, 1.0, 22.0, 2, minsep=0.35, avoid_speaker=0.6), (0.8, 1.3), rng)
    objs += asset_instances(bpy, 'grass_medium_01', rng_points(rng, 200, 1.0, 18.0, 3, minsep=0.4, avoid_speaker=0.6), (0.8, 1.3), rng)
    return objs


# --- air ------------------------------------------------------------------------------------------------------------
# density (1/m) of the air near the ground in each biome, its scale height (m), and its colour
AIR = {'Ice': (0.00008, 400, '#F4F8FF'), 'Poison': (0.0015, 40, '#F2F0E8'), 'Fog': (0.00012, 400, '#FFFFFF'),
       'Haze': (0.00025, 700, '#F0DCC8'), 'Dust': (0.00008, 600, '#F0D8B8'), 'Acid': (0.0012, 400, '#C9CCB8'),
       'Ember': (0.0003, 300, '#D9D3D0'), 'Smoke': (0.0008, 200, '#B7B2AE')}


def air(bpy):
    """One volume over the whole world: each biome's air by its azimuth (blended like the sky), thinning with height;
    the Fog's sea of cloud below the headland. Absorbs a little (smoke, rain) and scatters forward."""
    import bmesh
    m = bpy.data.materials.new('air'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); T = NT(nt)
    out = T.n('ShaderNodeOutputMaterial')
    vol = T.n('ShaderNodeVolumePrincipled'); vol.inputs['Anisotropy'].default_value = 0.55
    tc = T.n('ShaderNodeTexCoord'); pos = tc.outputs['Object']
    sep = T.n('ShaderNodeSeparateXYZ'); T.l(pos, sep.inputs[0])
    az = T.math('ARCTAN2', sep.outputs['X'], sep.outputs['Y'])
    azd = T.math('MODULO', T.math('ADD', T.math('MULTIPLY', az, 180 / math.pi), 360.0), 360.0)
    dens = None; colr = None
    wsum = None
    for i, nm in enumerate(F.NAMES):
        d0, hs, c = AIR[nm]
        # angular distance to the sector centre, folded
        dd = T.math('SUBTRACT', T.math('MODULO', T.math('ADD', T.math('SUBTRACT', azd, F.centre_az(i)), 540.0), 360.0), 180.0)
        dd = T.math('ABSOLUTE', dd)
        mr = T.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP'); T.l(dd, mr.inputs[0])
        mr.inputs[1].default_value = F.SECTOR / 2 + F.BAND; mr.inputs[2].default_value = F.SECTOR / 2 - F.BAND
        w = mr.outputs[0]
        fall = T.math('EXPONENT', T.math('DIVIDE', T.math('MAXIMUM', sep.outputs['Z'], -50.0), -hs))
        di = T.math('MULTIPLY', w, T.math('MULTIPLY', fall, d0))
        ci = T.mix((0, 0, 0), lin(c), w)
        dens = di if dens is None else T.math('ADD', dens, di)
        colr = ci if colr is None else T.mix(colr, ci, 1.0, blend='ADD')
    # the fog's sea: below 2 m under the headland's foot, dense, its top rolling
    r = T.n('ShaderNodeVectorMath', operation='LENGTH'); T.l(pos, r.inputs[0])
    nz = T.n('ShaderNodeTexNoise'); T.l(pos, nz.inputs['Vector']); nz.inputs['Scale'].default_value = 0.004
    nz.inputs['Detail'].default_value = 6.0
    top = T.math('MULTIPLY_ADD', nz.outputs['Fac'], 14.0, -16.0)
    below = T.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP'); T.l(T.math('SUBTRACT', top, sep.outputs['Z']), below.inputs[0])
    below.inputs[1].default_value = 0.0; below.inputs[2].default_value = 6.0
    fogw_ = T.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP')
    dd = T.math('ABSOLUTE', T.math('SUBTRACT', T.math('MODULO', T.math('ADD', T.math('SUBTRACT', azd, F.centre_az(2)), 540.0), 360.0), 180.0))
    T.l(dd, fogw_.inputs[0]); fogw_.inputs[1].default_value = 60.0; fogw_.inputs[2].default_value = 30.0
    sea = T.math('MULTIPLY', T.math('MULTIPLY', below.outputs[0], fogw_.outputs[0]), 0.06)
    dens = T.math('ADD', dens, sea)
    colr = T.mix(colr, (1.0, 1.0, 1.0), T.math('MINIMUM', T.math('MULTIPLY', sea, 40.0), 1.0))
    T.l(dens, vol.inputs['Density']); T.l(colr, vol.inputs['Color'])
    vol.inputs['Absorption Color'].default_value = (0.02, 0.02, 0.02, 1)
    T.l(vol.outputs[0], out.inputs['Volume'])
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=96, radius1=4600, radius2=4600, depth=1700)
    for v in bm.verts:
        v.co.z += 1700 / 2 - 120
    me = bpy.data.meshes.new('air'); bm.to_mesh(me); bm.free(); me.materials.append(m)
    ob = bpy.data.objects.new('air', me); bpy.context.scene.collection.objects.link(ob)
    ob['volume'] = True
    return ob


def plume(bpy):
    """Ember's volcano: a column of ash and steam over its crater, lit from below by the vent."""
    import bmesh
    _, (cx, cy) = F.volcano(np.array([0.0]), np.array([0.0]))
    top = ground_z(cx, cy)
    m = bpy.data.materials.new('plume'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); T = NT(nt)
    out = T.n('ShaderNodeOutputMaterial'); vol = T.n('ShaderNodeVolumePrincipled')
    tc = T.n('ShaderNodeTexCoord'); g = tc.outputs['Generated']
    sep = T.n('ShaderNodeSeparateXYZ'); T.l(g, sep.inputs[0])
    cxv = T.math('SUBTRACT', sep.outputs['X'], 0.5); cyv = T.math('SUBTRACT', sep.outputs['Y'], 0.5)
    rr = T.math('SQRT', T.math('ADD', T.math('MULTIPLY', cxv, cxv), T.math('MULTIPLY', cyv, cyv)))
    width = T.math('MULTIPLY_ADD', sep.outputs['Z'], 0.32, 0.08)
    nz = T.n('ShaderNodeTexNoise'); T.l(tc.outputs['Object'], nz.inputs['Vector']); nz.inputs['Scale'].default_value = 0.004
    nz.inputs['Detail'].default_value = 8.0
    edge = T.math('SUBTRACT', 1.0, T.math('DIVIDE', rr, T.math('MULTIPLY_ADD', nz.outputs['Fac'], 0.25, width)), clamp=True)
    d = T.math('MULTIPLY', T.math('POWER', edge, 1.6), 0.0025)
    T.l(d, vol.inputs['Density']); vol.inputs['Color'].default_value = (*lin('#9A948F'), 1)
    vol.inputs['Absorption Color'].default_value = (0.25, 0.25, 0.25, 1)
    T.l(vol.outputs[0], out.inputs['Volume'])
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    me = bpy.data.meshes.new('plume'); bm.to_mesh(me); bm.free(); me.materials.append(m)
    ob = bpy.data.objects.new('plume', me); bpy.context.scene.collection.objects.link(ob)
    ob.scale = (900, 900, 1300); ob.location = (cx, cy, top - 30 + 650)
    ob['volume'] = True
    # the vent's glow, under its plume
    ld = bpy.data.lights.new('vent', 'POINT'); ld.energy = 3e6; ld.shadow_soft_size = 60.0; ld.color = lin('#FF6A22')
    lo = bpy.data.objects.new('vent', ld); bpy.context.scene.collection.objects.link(lo); lo.location = (cx, cy, top + 25)
    return ob


# --- the speakers --------------------------------------------------------------------------------------------------
def speakers(bpy, path=TROPOS, turn=(12, -14, 16, -12, 14, -16, 12, -14)):
    """Link each tint's collection from the Tropos .blend and stand an instance of it on its spot, facing the camera
    and turned a little, its feet a few millimetres into the ground."""
    with bpy.data.libraries.load(path, link=True) as (src, dst):
        dst.collections = [f'Tropos.{n}' for n in F.NAMES if f'Tropos.{n}' in src.collections]
    cols = {c.name.split('.', 1)[1]: c for c in dst.collections if c}
    out = []
    for i, nm in enumerate(F.NAMES[:int(os.environ.get('SPK_N', 8))]):
        x, y = F.speaker_spot(i)
        e = bpy.data.objects.new(f'tropos.{nm}', None)
        e.instance_type = 'COLLECTION'; e.instance_collection = cols[TINT[nm]]
        e.location = (x, y, ground_z(x, y) - 0.006)
        e.rotation_euler = (0, 0, -math.radians(F.centre_az(i)) + math.radians(turn[i]))
        bpy.context.scene.collection.objects.link(e)
        out.append(e)
    return out


# --- sky and camera ----------------------------------------------------------------------------------------------------
def set_hour(bpy, i, world=None):
    """The world for biome i's hour: the multiple-scattering sky with its sun, from the sector the biome holds."""
    h = HOURS[i]
    w = world or bpy.data.worlds.new('sky')
    w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear(); T = NT(nt)
    out = T.n('ShaderNodeOutputWorld')
    sky = T.n('ShaderNodeTexSky', sky_type='MULTIPLE_SCATTERING')
    sky.sun_disc = True; sky.sun_size = math.radians(0.545); sky.sun_intensity = 1.0
    sky.sun_elevation = math.radians(h['sun_el'])
    az = F.centre_az(i) + h['sun_off']
    # Blender's sky: rotation 0 puts the sun toward +y? measured: see README (checked on the proof)
    sky.sun_rotation = math.radians((-az + 90.0) % 360.0)
    sky.altitude = 50.0; sky.air_density = h['air']; sky.aerosol_density = h['dust']; sky.ozone_density = h['ozone']
    bg = T.n('ShaderNodeBackground'); T.l(sky.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = h['strength']
    if h['name'] == 'Smoke':
        # a city's night: the sky glows sodium from below, a little moonlight above
        grad = T.n('ShaderNodeTexCoord'); sep = T.n('ShaderNodeSeparateXYZ'); T.l(grad.outputs['Generated'], sep.inputs[0])
        up = T.math('POWER', T.math('SUBTRACT', 1.0, T.math('MAXIMUM', sep.outputs['Z'], 0.0), clamp=True), 6.0)
        glow = T.mix(lin('#0B1220'), lin('#7A4A2A'), up)
        add = T.n('ShaderNodeBackground'); T.l(glow, add.inputs['Color']); add.inputs['Strength'].default_value = 0.004
        ad = T.n('ShaderNodeAddShader'); T.l(bg.outputs[0], ad.inputs[0]); T.l(add.outputs[0], ad.inputs[1])
        T.l(ad.outputs[0], out.inputs['Surface'])
    elif h['name'] == 'Acid':
        # overcast: the sky's own colour under a grey lid that lets the low sun through at the horizon
        grad = T.n('ShaderNodeTexCoord'); sep = T.n('ShaderNodeSeparateXYZ'); T.l(grad.outputs['Generated'], sep.inputs[0])
        lid = T.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP'); T.l(sep.outputs['Z'], lid.inputs[0])
        lid.inputs[1].default_value = 0.02; lid.inputs[2].default_value = 0.25
        nz = T.n('ShaderNodeTexNoise'); T.l(grad.outputs['Generated'], nz.inputs['Vector']); nz.inputs['Scale'].default_value = 1.2
        nz.inputs['Detail'].default_value = 3.0
        lidc = T.n('ShaderNodeMapRange'); T.l(nz.outputs['Fac'], lidc.inputs[0])
        lidc.inputs[1].default_value = 0.3; lidc.inputs[2].default_value = 0.7
        cloud = T.mix(lin('#34362F'), lin('#3C3D35'), lidc.outputs[0])
        col = T.mix(sky.outputs['Color'], T.mix(cloud, cloud, 0.0), T.math('MULTIPLY', lid.outputs[0], 0.97))
        T.l(col, bg.inputs['Color'])
        T.l(bg.outputs[0], out.inputs['Surface'])
    else:
        T.l(bg.outputs[0], out.inputs['Surface'])
    bpy.context.scene.world = w
    return w


def camera(bpy, yaw_deg=0.0, lat=(-90, 90)):
    cd = bpy.data.cameras.new('pano'); cd.type = 'PANO'; cd.panorama_type = 'EQUIRECTANGULAR'
    cd.latitude_min = math.radians(lat[0]); cd.latitude_max = math.radians(lat[1])
    cd.longitude_min = -math.pi; cd.longitude_max = math.pi
    cd.clip_start = 0.05; cd.clip_end = 20000
    ob = bpy.data.objects.new('pano', cd); bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, 0, CAM_Z)
    aim(ob, yaw_deg)
    bpy.context.scene.camera = ob
    return ob


def aim(ob, yaw_deg):
    """Point the panorama's centre at azimuth yaw (clockwise from +y). Blender's equirectangular centre looks along
    the camera's -z; so stand the camera up (x 90 deg) and turn it."""
    ob.rotation_euler = (math.radians(90), 0, -math.radians(yaw_deg))


# --- render ------------------------------------------------------------------------------------------------------------
def setup_render(bpy, W, H, samples):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; cy = sc.cycles
    cy.device = 'CPU'; cy.samples = samples
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'; cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    cy.max_bounces = 10; cy.diffuse_bounces = 3; cy.glossy_bounces = 6; cy.transmission_bounces = 10
    cy.transparent_max_bounces = 16; cy.volume_bounces = 1
    cy.sample_clamp_indirect = 8.0
    cy.caustics_reflective = False; cy.caustics_refractive = False
    sc.render.resolution_x = W; sc.render.resolution_y = H; sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '16'
    sc.render.image_settings.exr_codec = 'ZIP'
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
    sc.render.film_transparent = False


def position_pass(bpy, out_path, W, H, frac):
    """Where each pixel's ray first lands (world position, and 1 in alpha for ground or any object, 0 for sky), for the
    compositor's weights. Volumes off, every surface an emitter of its own position."""
    sc = bpy.context.scene
    m = bpy.data.materials.new('pos'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); T = NT(nt)
    o = T.n('ShaderNodeOutputMaterial'); em = T.n('ShaderNodeEmission'); geo = T.n('ShaderNodeNewGeometry')
    T.l(geo.outputs['Position'], em.inputs['Color']); T.l(em.outputs[0], o.inputs['Surface'])
    vl = sc.view_layers[0]
    vl.material_override = m
    hidden = []
    for ob in sc.objects:
        if ob.get('volume') or ob.type == 'LIGHT':
            ob.hide_render = True; hidden.append(ob)
    sc.render.film_transparent = True
    cy = sc.cycles
    keep = (cy.samples, cy.use_denoising, cy.max_bounces, cy.use_adaptive_sampling)
    cy.samples = 1; cy.use_denoising = False; cy.max_bounces = 0; cy.use_adaptive_sampling = False
    sc.render.filter_size = 0.01
    sc.render.use_border = False
    sc.render.filepath = out_path
    sc.render.image_settings.color_depth = '32'
    bpy.ops.render.render(write_still=True)
    vl.material_override = None
    for ob in hidden:
        ob.hide_render = False
    sc.render.film_transparent = False
    sc.render.filter_size = 1.5
    sc.render.image_settings.color_depth = '16'
    cy.samples, cy.use_denoising, cy.max_bounces, cy.use_adaptive_sampling = keep


def knob(bpy):
    """A low granite knob under the camera, the one ground all eight share (the little planet's centre)."""
    import bmesh
    m = bpy.data.materials.new('granite'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); T = NT(nt)
    o = T.n('ShaderNodeOutputMaterial'); b = T.n('ShaderNodeBsdfPrincipled')
    col, rough, nor, _ = pbr_layer(bpy, T, 'cliff_side', 2.5, tint='#6E6A64', tint_mix=0.45, value=0.75, far=1.0)
    T.l(col, b.inputs['Base Color']); T.l(rough, b.inputs['Roughness']); T.l(nor, b.inputs['Normal'])
    T.l(b.outputs[0], o.inputs['Surface'])
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=32, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co
        a = math.atan2(y, x)
        rr = 1.15 * (1 + 0.12 * math.sin(3 * a + 1) + 0.07 * math.sin(7 * a + 2) + 0.04 * math.sin(13 * a))
        v.co.x, v.co.y = x * rr, y * rr
        v.co.z = (z * 0.16 if z > 0 else z * 0.4) + 0.0
    me = bpy.data.meshes.new('knob'); bm.to_mesh(me); bm.free(); me.materials.append(m)
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    ob = bpy.data.objects.new('knob', me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (0, 0, ground_z(0.0, 0.0) - 0.08)
    return ob


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--width', type=int, default=2048)
    ap.add_argument('--samples', type=int, default=32)
    ap.add_argument('--only', type=int, nargs='*')
    ap.add_argument('--lat', type=float, nargs=2, default=(-90.0, 90.0))
    ap.add_argument('--half', type=float, default=54.0, help='degrees each side of a sector centre each slice renders')
    ap.add_argument('--tropos', default=TROPOS)
    ap.add_argument('--lod', type=float, default=1.0)
    ap.add_argument('--no-flora', action='store_true')
    ap.add_argument('--save-blend')
    ap.add_argument('--threads', type=int, default=0)
    a = ap.parse_args()
    import bpy
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.preferences.addon_enable(module='cycles')
    rng = np.random.default_rng(7)
    import random
    R = random.Random(7)
    terrain(bpy, [ground_material(bpy, i) for i in range(F.N)], lod=a.lod)
    print('ground', round(time.time() - t0, 1))
    if not os.environ.get('NO_WOOD'):
        redwoods(bpy, R)
    if not os.environ.get('NO_CITY'):
        city(bpy, R)
    if not a.no_flora:
        flora(bpy, R)
    print('scatter', round(time.time() - t0, 1))
    if not os.environ.get("NO_AIR"):
        air(bpy); plume(bpy)
    knob(bpy)
    if not os.environ.get('NO_SPK'):
        speakers(bpy, a.tropos)
    W = a.width; H = int(round(W * (a.lat[1] - a.lat[0]) / 360.0))
    setup_render(bpy, W, H, a.samples)
    if a.threads:
        bpy.context.scene.render.threads_mode = 'FIXED'; bpy.context.scene.render.threads = a.threads
    cam = camera(bpy, 0.0, a.lat)
    os.makedirs(a.out, exist_ok=True)
    meta = {'width': W, 'height': H, 'lat': list(a.lat), 'cam_z': CAM_Z, 'half': a.half, 'samples': a.samples,
            'hours': HOURS, 'slices': {}}
    if a.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.save_blend))
    pp = os.path.join(a.out, 'position.exr')
    if not os.path.exists(pp):
        aim(cam, 0.0)
        position_pass(bpy, pp, W, H, None)
    print('built', round(time.time() - t0, 1))
    sc = bpy.context.scene
    world = None
    for i in (a.only if a.only is not None else range(F.N)):
        t1 = time.time()
        world = set_hour(bpy, i, world)
        sc.view_settings.exposure = 0.0
        # the slice: the camera turned to the sector, a border round the image's centre
        aim(cam, F.centre_az(i))
        sc.render.use_border = True; sc.render.use_crop_to_border = False
        f = a.half / 360.0
        sc.render.border_min_x, sc.render.border_max_x = 0.5 - f, 0.5 + f
        sc.render.border_min_y, sc.render.border_max_y = 0.0, 1.0
        p = os.path.join(a.out, f'slice-{i}-{F.NAMES[i].lower()}.exr')
        sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        meta['slices'][str(i)] = {'file': os.path.basename(p), 'yaw': F.centre_az(i), 'seconds': round(time.time() - t1, 1)}
        print(F.NAMES[i], round(time.time() - t1, 1), flush=True)
        json.dump(meta, open(os.path.join(a.out, 'meta.json'), 'w'), indent=1)
    print('done', round(time.time() - t0, 1))


if __name__ == '__main__':
    main()
