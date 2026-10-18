"""Ice, concept B (round 31b): Jokulsarlon's Diamond Beach at dawn. Black volcanic sand running down to the surf,
the sea out to the horizon, and chunks of glacier ice stranded on the sand and in the wash, the low sun coming through
them as it comes through the speaker's blue acrylic.

Pieces (kit 'ext', module 'ice_b_el'):
- fn 'beach': the black sand, its own shore profile (level round the speaker, then down into the sea), wet and
  mirror-like where the wash reaches, damp above; `texture` a Poly Haven sand for grain and relief.
- fn 'sea': the sea from the shore to the horizon, its wash lace and surf lines worked out from the beach's own
  profile, so the foam sits where the water is shallow.
- fn 'ice': one chunk of glacier ice, `size` [x, y, z] metres, `seed`, `kind` 'clear', 'blue' or 'milky'; cut
  facets worn round by the sea, melt scallops, a band of bubbles and a crack or two inside it.

The shore: sand z = -slope * max(0, y' - y0), y' = y + wiggle * sin(x * freq + phase); the sea stands at `water_z`.
"""
import math, random

import bmesh
import numpy as np
from mathutils import Vector, noise

SHORE = {'y0': 1.4, 'slope': 0.05, 'wiggle': 0.55, 'freq': 0.45, 'phase': 0.7, 'water_z': -0.09}


def _shore(p):
    s = dict(SHORE)
    s.update(p.get('shore', {}))
    return s


def sand_z(x, y, s):
    yy = y + s['wiggle'] * np.sin(x * s['freq'] + s['phase'])
    return -s['slope'] * np.maximum(0.0, yy - s['y0'])


def _axis(lo, hi, flo, fhi, step, grow=1.08):
    """Coordinates from lo to hi: `step` apart between flo and fhi, growing geometrically outside."""
    xs = list(np.arange(flo, fhi + 1e-9, step))
    d, x = step, flo
    while x > lo:
        d *= grow; x -= d; xs.insert(0, max(lo, x))
    d, x = step, fhi
    while x < hi:
        d *= grow; x += d; xs.append(min(hi, x))
    return np.array(xs)


def _hex(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1.0,)


def _grid_object(bpy, name, xs, ys, zfn, mat):
    X, Y = np.meshgrid(xs, ys)
    Z = zfn(X, Y)
    nx, ny = len(xs), len(ys)
    verts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    i = np.arange(nx - 1); j = np.arange(ny - 1)
    I, J = np.meshgrid(i, j)
    a = (J * nx + I).ravel()
    faces = np.stack([a, a + 1, a + nx + 1, a + nx], 1)
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.astype(np.float32).ravel())
    me.loops.add(faces.size); me.loops.foreach_set('vertex_index', faces.astype(np.int32).ravel())
    me.polygons.add(len(faces)); me.polygons.foreach_set('loop_start', (np.arange(len(faces)) * 4).astype(np.int32))
    me.polygons.foreach_set('loop_total', np.full(len(faces), 4, np.int32))
    me.update(calc_edges=True); me.validate()
    me.polygons.foreach_set('use_smooth', np.ones(len(faces), bool))
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return ob


# --- shader helpers ------------------------------------------------------------------------------------------------
class _N:
    """A small node-graph writer: n('Math', operation='MULTIPLY', inputs={0: x, 1: 2.0})."""
    def __init__(self, nt):
        self.nt = nt

    def __call__(self, kind, inputs=None, **attrs):
        n = self.nt.nodes.new('ShaderNode' + kind)
        for k, v in attrs.items():
            setattr(n, k, v)
        for k, v in (inputs or {}).items():
            sock = n.inputs[k]
            if hasattr(v, 'is_output') or hasattr(v, 'links'):
                self.nt.links.new(v, sock)
            else:
                sock.default_value = v
        return n

    def math(self, op, a, b=None, clamp=False):
        n = self('Math', operation=op, use_clamp=clamp)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if hasattr(v, 'is_output'):
                self.nt.links.new(v, n.inputs[i])
            else:
                n.inputs[i].default_value = v
        return n.outputs[0]

    def link(self, a, b):
        self.nt.links.new(a, b)


def _xyz(N, space='Object'):
    tc = N('TexCoord')
    sep = N('SeparateXYZ', inputs={'Vector': tc.outputs[space]})
    return tc, sep


def _shore_depth(N, sep, s):
    """water_z - sand_z at this point's (x, y), in the shader."""
    w = N.math('SINE', N.math('ADD', N.math('MULTIPLY', sep.outputs['X'], s['freq']), s['phase']))
    yy = N.math('ADD', sep.outputs['Y'], N.math('MULTIPLY', w, s['wiggle']))
    drop = N.math('MULTIPLY', N.math('MAXIMUM', N.math('SUBTRACT', yy, s['y0']), 0.0), s['slope'])
    return N.math('ADD', drop, s['water_z']), yy          # depth (m, negative above water), and y'


def _sand_material(bpy, name, p, s):
    import assets
    tex = p.get('texture', 'gravelly_sand')
    maps = assets.texture(tex, p.get('res', '4k'))
    size = p.get('tex_scale') or (assets.size_m(tex) or (2.0, 2.0))[0]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = _N(nt)
    out = N('OutputMaterial'); bs = N('BsdfPrincipled')
    N.link(bs.outputs['BSDF'], out.inputs['Surface'])
    tc, sep = _xyz(N)
    # the texture, laid twice (its own scale, and turned and larger) and blended by a broad noise, so it does not tile
    mp1 = N('Mapping', inputs={'Vector': tc.outputs['Object'], 'Scale': (1 / size, 1 / size, 1 / size)})
    mp2 = N('Mapping', inputs={'Vector': tc.outputs['Object'], 'Scale': (0.71 / size, 0.71 / size, 0.71 / size),
                               'Rotation': (0, 0, 0.9), 'Location': (0.37, 0.61, 0)})
    blend = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 0.35, 'Detail': 2.0})
    bl = N('MapRange', inputs={'Value': blend.outputs['Fac'], 'From Min': 0.42, 'From Max': 0.58})

    def img(key, colour):
        outs = []
        for mp in (mp1, mp2):
            t = N('TexImage'); t.image = bpy.data.images.load(maps[key], check_existing=True)
            if not colour:
                t.image.colorspace_settings.name = 'Non-Color'
            N.link(mp.outputs['Vector'], t.inputs['Vector'])
            outs.append(t.outputs['Color'])
        mx = N('Mix', data_type='RGBA', inputs={'Factor': bl.outputs['Result'], 'A': outs[0], 'B': outs[1]})
        return mx.outputs[2]
    diff = img('diff', True)
    lum = N('RGBToBW', inputs={'Color': diff}).outputs[0]
    # volcanic black: the photographed grain's light and dark, mapped to basalt's near-black with a few pale grains
    ramp = N('ValToRGB', inputs={'Fac': lum}); cr = ramp.color_ramp
    cr.elements[0].position = 0.12; cr.elements[0].color = _hex(p.get('dark', '#0B0B0C'))
    cr.elements[1].position = 0.62; cr.elements[1].color = _hex(p.get('light', '#3A3936'))
    depth, yy = _shore_depth(N, sep, s)
    # wetness from how far above the water this point is: soaked below wet_h, damp to damp_h, broken by noise
    wn = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 1.3, 'Detail': 6.0})
    jit = N.math('MULTIPLY', N.math('SUBTRACT', wn.outputs['Fac'], 0.5), p.get('wet_jitter', 0.05))
    height = N.math('ADD', N.math('MULTIPLY', depth, -1.0), jit)       # height above the water (m)
    wet = N('MapRange', inputs={'Value': height, 'From Min': p.get('wet_h', 0.05), 'From Max': p.get('wet_h', 0.05) - 0.03,
                                'To Min': 0.0, 'To Max': 1.0}, clamp=True).outputs['Result']
    damp = N('MapRange', inputs={'Value': height, 'From Min': p.get('damp_h', 0.16), 'From Max': p.get('wet_h', 0.05),
                                 'To Min': p.get('damp_base', 0.35), 'To Max': 1.0}, clamp=True).outputs['Result']
    if p.get('puddles'):
        # meltwater lying in the floor's hollows: soaked and mirror-like in patches
        sc, th = p['puddles']
        pn = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': sc, 'Detail': 5.0, 'Roughness': 0.6})
        pud = N('MapRange', inputs={'Value': pn.outputs['Fac'], 'From Min': th, 'From Max': th + 0.04}, clamp=True).outputs['Result']
        wet = N.math('MAXIMUM', wet, pud)
        damp = N.math('MAXIMUM', damp, N('MapRange', inputs={'Value': pn.outputs['Fac'], 'From Min': th - 0.12, 'From Max': th}, clamp=True).outputs['Result'])
    if 'reach' in p:
        # the last wave's reach: soaked and mirror-like behind an irregular line across the beach (y' > reach), damp a
        # little before it, a line of spent foam left along it
        r0, rw = p['reach']
        wob = N('TexNoise', inputs={'Vector': N('Mapping', inputs={'Vector': tc.outputs['Object'], 'Scale': (1.0, 0.2, 1.0)}).outputs[0],
                                    'Scale': 0.7, 'Detail': 5.0, 'Roughness': 0.6})
        wob2 = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 2.6, 'Detail': 6.0, 'Roughness': 0.65})
        ry = N.math('ADD', sep.outputs['Y'], N.math('MULTIPLY', N.math('SUBTRACT', wob.outputs['Fac'], 0.5), p.get('reach_wobble', 1.8)))
        ry = N.math('ADD', ry, N.math('MULTIPLY', N.math('SUBTRACT', wob2.outputs['Fac'], 0.5), 0.35))
        rd = N.math('SUBTRACT', ry, r0)                                    # metres beyond the reach line (+ wet side)
        rwet = N('MapRange', inputs={'Value': rd, 'From Min': 0.0, 'From Max': rw}, clamp=True).outputs['Result']
        rdamp = N('MapRange', inputs={'Value': rd, 'From Min': -0.6, 'From Max': 0.0, 'To Min': 0.0, 'To Max': 1.0}, clamp=True).outputs['Result']
        wet = N.math('MAXIMUM', wet, rwet)
        damp = N.math('MAXIMUM', damp, rdamp)
        fl = N('TexVoronoi', feature='DISTANCE_TO_EDGE', inputs={'Vector': tc.outputs['Object'], 'Scale': 40.0})
        fl2 = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 9.0, 'Detail': 6.0})
        band = N.math('SUBTRACT', 1.0, N.math('ABSOLUTE', N.math('DIVIDE', N.math('ADD', rd, 0.03), p.get('residue_w', 0.14))), clamp=True)
        lace = N('MapRange', inputs={'Value': fl.outputs['Distance'], 'From Min': 0.08, 'From Max': 0.0}).outputs['Result']
        lace = N.math('MULTIPLY', lace, N('MapRange', inputs={'Value': fl2.outputs['Fac'], 'From Min': 0.4, 'From Max': 0.6}).outputs['Result'])
        gaps = N('MapRange', inputs={'Value': N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 1.5, 'Detail': 3.0}).outputs['Fac'],
                                     'From Min': 0.42, 'From Max': 0.55}).outputs['Result']
        residue = N.math('MULTIPLY', N.math('MULTIPLY', band, lace), N.math('MULTIPLY', gaps, p.get('residue', 0.9)), clamp=True)
    else:
        residue = 0.0
    darken = N('Mix', data_type='RGBA', blend_type='MULTIPLY',
               inputs={'Factor': N.math('MULTIPLY', damp, 0.75), 'A': ramp.outputs['Color'], 'B': (0.45, 0.45, 0.47, 1.0)})
    foamed = N('Mix', data_type='RGBA', inputs={'Factor': residue, 'A': darken.outputs[2], 'B': _hex('#C9CFCF')})
    N.link(foamed.outputs[2], bs.inputs['Base Color'])
    rough_img = N('RGBToBW', inputs={'Color': img('rough', False)}).outputs[0]
    dry_r = N.math('ADD', N.math('MULTIPLY', rough_img, 0.2), p.get('dry_rough', 0.82))
    damp_r = N('MapRange', inputs={'Value': damp, 'From Min': 0.0, 'From Max': 1.0, 'To Min': 1.0, 'To Max': 0.45}).outputs['Result']
    r = N.math('MULTIPLY', dry_r, damp_r)
    # glassy grains: a few in a hundred catch the low sun as points of light (black volcanic sand glitters)
    gv = N('TexVoronoi', inputs={'Vector': tc.outputs['Object'], 'Scale': 1.0 / p.get('grain_m', 0.0016), 'Randomness': 1.0})
    glint = N('MapRange', inputs={'Value': gv.outputs['Color'], 'From Min': 1.0 - p.get('glint_share', 0.04), 'From Max': 1.0},
              clamp=True).outputs['Result']
    glint = N.math('CEIL', N.math('SUBTRACT', glint, 0.001))
    r = N('Mix', data_type='FLOAT', inputs={'Factor': glint, 'A': r, 'B': p.get('glint_rough', 0.25)}).outputs[0]
    r = N('Mix', data_type='FLOAT', inputs={'Factor': wet, 'A': r, 'B': p.get('wet_rough', 0.06)}).outputs[0]
    r = N('Mix', data_type='FLOAT', inputs={'Factor': residue, 'A': r, 'B': 0.55}).outputs[0]
    N.link(r, bs.inputs['Roughness'])
    N.link(N('Mix', data_type='FLOAT', inputs={'Factor': glint, 'A': p.get('spec', 0.35), 'B': 0.8}).outputs[0],
           bs.inputs['Specular IOR Level'])
    # a water film on the soaked sand: a clear coat that mirrors the sky
    N.link(N.math('MULTIPLY', wet, 1.0), bs.inputs['Coat Weight'])
    bs.inputs['Coat Roughness'].default_value = 0.015; bs.inputs['Coat IOR'].default_value = 1.33
    nm = N('NormalMap', inputs={'Color': img('nor_gl', False)})
    nstr = N('MapRange', inputs={'Value': wet, 'To Min': p.get('bump', 1.0), 'To Max': p.get('bump', 1.0) * 0.35}).outputs['Result']
    N.link(nstr, nm.inputs['Strength'])
    N.link(nm.outputs['Normal'], bs.inputs['Normal'])
    if p.get('displace', 0.0) > 0 and 'disp' in maps:
        dsp = N('Displacement', inputs={'Height': N('RGBToBW', inputs={'Color': img('disp', False)}).outputs[0],
                                        'Midlevel': 0.5, 'Scale': p['displace']})
        N.link(dsp.outputs[0], out.inputs['Displacement'])
        m.displacement_method = 'BOTH'
    return m


def beach(bpy, name, p, kit):
    s = _shore(p)
    x0, y0, x1, y1 = p.get('extent', [-30.0, -9.0, 30.0, 14.0])
    fx0, fy0, fx1, fy1 = p.get('fine', [-3.5, -5.5, 3.5, 6.0])
    xs = _axis(x0, x1, fx0, fx1, p.get('cell', 0.012))
    ys = _axis(y0, y1, fy0, fy1, p.get('cell', 0.012))
    relief = p.get('relief', 0.04)
    rx = random.Random(p.get('seed', 3)).uniform(-50, 50)

    def zfn(X, Y):
        Z = sand_z(X, Y, s)
        # gentle undulation up the beach, fading to level under the speaker
        r = np.hypot(X, Y)
        t = np.clip((r - 1.0) / 1.5, 0, 1); t = t * t * (3 - 2 * t)
        U = np.vectorize(lambda x, y: noise.noise(Vector((x * 0.4 + rx, y * 0.4, 0.3))))(X, Y) if relief else 0
        return Z + relief * t * U * np.clip((Z - s['water_z'] - 0.03) / 0.15, 0, 1)
    ob = _grid_object(bpy, name, xs, ys, zfn, _sand_material(bpy, name + '-mat', p, s))
    return [ob]


def _ocean(bpy, X, Y, oc):
    """Blender's FFT ocean (Tessendorf) sampled at the grid's points: its displacement (dx, dy, dz) and foam, two
    spectra of different sizes summed so neither one's tiling shows."""
    me = bpy.data.meshes.new('ocean-probe')
    pts = np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1).astype(np.float32)
    ny, nx = X.shape
    I, J = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1)); a = (J * nx + I).ravel()
    faces = np.stack([a, a + 1, a + nx + 1, a + nx], 1)
    me.vertices.add(len(pts)); me.vertices.foreach_set('co', pts.ravel())
    me.loops.add(faces.size); me.loops.foreach_set('vertex_index', faces.astype(np.int32).ravel())
    me.polygons.add(len(faces)); me.polygons.foreach_set('loop_start', (np.arange(len(faces)) * 4).astype(np.int32))
    me.polygons.foreach_set('loop_total', np.full(len(faces), 4, np.int32))
    me.update(calc_edges=True)
    ob = bpy.data.objects.new('ocean-probe', me); bpy.context.scene.collection.objects.link(ob)
    for i, layer in enumerate(oc.get('layers', [{'size': 53.0, 'scale': 0.8, 'seed': 3}, {'size': 131.0, 'scale': 0.6, 'seed': 9}])):
        m = ob.modifiers.new(f'ocean{i}', 'OCEAN')
        m.geometry_mode = 'DISPLACE'; m.resolution = oc.get('resolution', 14); m.spatial_size = int(layer['size'])
        m.wave_scale = layer['scale']; m.choppiness = layer.get('chop', 1.1); m.wind_velocity = layer.get('wind', 9.0)
        m.wave_alignment = layer.get('align', 0.6); m.wave_direction = math.radians(layer.get('dir', -90.0))
        m.random_seed = layer['seed']; m.time = layer.get('time', 7.0); m.damping = 0.4
        if i == 0:
            m.use_foam = True; m.foam_layer_name = 'foam'; m.foam_coverage = oc.get('foam_coverage', 0.35)
    dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); em = e.to_mesh()
    co = np.zeros(len(pts) * 3, np.float32); em.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    foam = np.zeros(len(pts), np.float32)
    if 'foam' in em.attributes:
        a = em.attributes['foam']
        if a.domain == 'POINT' and a.data_type == 'FLOAT':
            a.data.foreach_get('value', foam)
        else:
            tmp = np.zeros(len(a.data) * (4 if 'COLOR' in a.data_type else 1), np.float32)
            a.data.foreach_get('color' if 'COLOR' in a.data_type else 'value', tmp)
            vals = tmp[0::4] if 'COLOR' in a.data_type else tmp
            if a.domain == 'CORNER':
                vi = np.zeros(len(em.loops), np.int32); em.loops.foreach_get('vertex_index', vi)
                np.maximum.at(foam, vi, vals)
            else:
                foam = vals[:len(pts)]
    e.to_mesh_clear(); bpy.data.objects.remove(ob); bpy.data.meshes.remove(me)
    d = co - pts
    sh = X.shape
    return d[:, 0].reshape(sh), d[:, 1].reshape(sh), d[:, 2].reshape(sh), foam.reshape(sh)


def _sea_material(bpy, name, p, s):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = _N(nt)
    out = N('OutputMaterial')
    tc, sep = _xyz(N)
    depth, yy = _shore_depth(N, sep, s)
    water = N('BsdfPrincipled', inputs={'Base Color': _hex('#1A2A2C'), 'Roughness': p.get('rough', 0.025),
                                        'IOR': 1.333, 'Transmission Weight': 1.0, 'Specular IOR Level': 0.5})
    # waves: long swell and short chop as bump, both in world metres
    sw = N('TexWave', wave_type='BANDS', bands_direction='Y', inputs={'Vector': tc.outputs['Object'], 'Scale': 0.09,
                                                                       'Distortion': 6.0, 'Detail': 3.0, 'Detail Scale': 1.5})
    ch = N('TexNoise', inputs={'Vector': N('Mapping', inputs={'Vector': tc.outputs['Object'], 'Scale': (1.0, 2.2, 1.0)}).outputs[0],
                               'Scale': 1.6, 'Detail': 8.0, 'Roughness': 0.55})
    h = N.math('ADD', N.math('MULTIPLY', sw.outputs['Fac'], 0.35), ch.outputs['Fac'])
    bump = N('Bump', inputs={'Height': h, 'Strength': p.get('chop', 0.18), 'Distance': 0.05})
    N.link(bump.outputs['Normal'], water.inputs['Normal'])
    # foam: the wash's lace where the water runs thin over the sand, and the broken surf in lines further out
    lace = N('TexVoronoi', feature='DISTANCE_TO_EDGE', inputs={'Vector': N('Mapping', inputs={
        'Vector': tc.outputs['Object'], 'Scale': (1.0, 1.8, 1.0)}).outputs[0], 'Scale': 3.2, 'Randomness': 1.0})
    lace_n = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 2.5, 'Detail': 6.0})
    lace_v = N('MapRange', inputs={'Value': lace.outputs['Distance'], 'From Min': 0.03, 'From Max': 0.0}).outputs['Result']
    lace_v = N.math('MULTIPLY', lace_v, N('MapRange', inputs={'Value': lace_n.outputs['Fac'], 'From Min': 0.42, 'From Max': 0.62}).outputs['Result'])
    edge = N('MapRange', inputs={'Value': depth, 'From Min': 0.0, 'From Max': p.get('edge_m', 0.012)}).outputs['Result']
    edge = N.math('SUBTRACT', 1.0, edge)                                    # the very rim of the wash: a thin white line
    rim_n = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 6.0, 'Detail': 4.0})
    edge = N.math('MULTIPLY', edge, N('MapRange', inputs={'Value': rim_n.outputs['Fac'], 'From Min': 0.35, 'From Max': 0.6}).outputs['Result'])
    band = N('MapRange', inputs={'Value': depth, 'From Min': p.get('lace_to', 0.09), 'From Max': 0.0}).outputs['Result']
    foam = N.math('MAXIMUM', edge, N.math('MULTIPLY', lace_v, band), clamp=True)
    # surf lines: whitewater in bands at distances from the shore, streaked along them
    dist = N.math('SUBTRACT', yy, s['y0'] + (-s['water_z']) / s['slope'])
    streak = N('TexNoise', inputs={'Vector': N('Mapping', inputs={'Vector': tc.outputs['Object'], 'Scale': (0.25, 2.5, 1.0)}).outputs[0],
                                   'Scale': 1.2, 'Detail': 10.0, 'Roughness': 0.6})
    st = N('MapRange', inputs={'Value': streak.outputs['Fac'], 'From Min': 0.45, 'From Max': 0.7}).outputs['Result']
    for c, w, a in p.get('surf', [[9.0, 1.6, 0.9], [22.0, 3.0, 0.7], [45.0, 5.0, 0.5]]):
        b = N.math('SUBTRACT', 1.0, N.math('ABSOLUTE', N.math('DIVIDE', N.math('SUBTRACT', dist, c), w)), clamp=True)
        foam = N.math('MAXIMUM', foam, N.math('MULTIPLY', N.math('MULTIPLY', b, st), a), clamp=True)
    froth = N('BsdfPrincipled', inputs={'Base Color': _hex('#E4ECEE'), 'Roughness': 0.65, 'Subsurface Weight': 0.3,
                                        'Subsurface Radius': (0.02, 0.025, 0.03)})
    N.link(bump.outputs['Normal'], froth.inputs['Normal'])
    mix = N('MixShader', inputs={'Fac': foam, 1: water.outputs[0], 2: froth.outputs[0]})
    vol = N('VolumeAbsorption', inputs={'Color': _hex(p.get('absorb', '#5E8F8C')), 'Density': p.get('density', 3.0)})
    N.link(mix.outputs[0], out.inputs['Surface']); N.link(vol.outputs[0], out.inputs['Volume'])
    return m


def _waves(X, Y, s, p):
    """The sea's surface over the still water level, and its whitewater (0 to 1): a few crests rolling in, each
    steep on its shoreward face, their heights wandering along the shore."""
    yy = Y + s['wiggle'] * np.sin(X * s['freq'] + s['phase'])
    dist = yy - (s['y0'] + (-s['water_z']) / s['slope'])                  # metres out from the still waterline
    Z = np.zeros_like(X); F = np.zeros_like(X)
    rx = random.Random(p.get('seed', 5))
    for crest in p.get('crests', [[5.5, 0.10, 0.5, 2.2, 0.85], [13.0, 0.22, 0.9, 4.0, 0.7],
                                   [27.0, 0.30, 1.4, 6.0, 0.45], [48.0, 0.30, 2.0, 9.0, 0.25]]):
        c, H, wf, wb, fa = crest[:5]
        skew = crest[5] if len(crest) > 5 else 0.0                       # a crest running at an angle to the shore
        o = rx.uniform(-100, 100)
        along = np.vectorize(lambda x: noise.noise(Vector((x * 0.07 + o, o, 0.5))) + 0.6 * noise.noise(Vector((x * 0.31 + o, 2 * o, 0.5))))(X[0])[None, :]
        h = H * np.clip(0.65 + p.get('break', 1.2) * along, 0.1, 1.8)
        d = dist - c - 1.2 * along - skew * X
        w = np.where(d < 0, wf, wb)
        Z += h * np.exp(-(d / w) ** 2)
        # whitewater: on the crest's front and spilling down its back, broken along the shore
        f = np.clip(1 - np.abs((d - wb * 0.35) / (wb * 0.9 + wf)), 0, 1) * np.clip(0.4 + along * 1.4, 0, 1)
        F = np.maximum(F, fa * f)
    near = np.clip((dist + 0.1) / 1.5, 0, 1)                              # the water lies flat where it meets the sand
    return Z * near, F * near


def _ocean(bpy, X, Y, oc):
    """Blender's FFT ocean (Tessendorf) sampled at the grid's points: its displacement (dx, dy, dz) and foam, two
    spectra of different sizes summed so neither one's tiling shows."""
    me = bpy.data.meshes.new('ocean-probe')
    pts = np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1).astype(np.float32)
    ny, nx = X.shape
    I, J = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1)); a = (J * nx + I).ravel()
    faces = np.stack([a, a + 1, a + nx + 1, a + nx], 1)
    me.vertices.add(len(pts)); me.vertices.foreach_set('co', pts.ravel())
    me.loops.add(faces.size); me.loops.foreach_set('vertex_index', faces.astype(np.int32).ravel())
    me.polygons.add(len(faces)); me.polygons.foreach_set('loop_start', (np.arange(len(faces)) * 4).astype(np.int32))
    me.polygons.foreach_set('loop_total', np.full(len(faces), 4, np.int32))
    me.update(calc_edges=True)
    ob = bpy.data.objects.new('ocean-probe', me); bpy.context.scene.collection.objects.link(ob)
    for i, layer in enumerate(oc.get('layers', [{'size': 53.0, 'scale': 0.8, 'seed': 3}, {'size': 131.0, 'scale': 0.6, 'seed': 9}])):
        m = ob.modifiers.new(f'ocean{i}', 'OCEAN')
        m.geometry_mode = 'DISPLACE'; m.resolution = oc.get('resolution', 14); m.spatial_size = int(layer['size'])
        m.wave_scale = layer['scale']; m.choppiness = layer.get('chop', 1.1); m.wind_velocity = layer.get('wind', 9.0)
        m.wave_alignment = layer.get('align', 0.6); m.wave_direction = math.radians(layer.get('dir', -90.0))
        m.random_seed = layer['seed']; m.time = layer.get('time', 7.0); m.damping = 0.4
        if i == 0:
            m.use_foam = True; m.foam_layer_name = 'foam'; m.foam_coverage = oc.get('foam_coverage', 0.35)
    dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); em = e.to_mesh()
    co = np.zeros(len(pts) * 3, np.float32); em.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    foam = np.zeros(len(pts), np.float32)
    if 'foam' in em.attributes:
        a = em.attributes['foam']
        if a.domain == 'POINT' and a.data_type == 'FLOAT':
            a.data.foreach_get('value', foam)
        else:
            tmp = np.zeros(len(a.data) * (4 if 'COLOR' in a.data_type else 1), np.float32)
            a.data.foreach_get('color' if 'COLOR' in a.data_type else 'value', tmp)
            vals = tmp[0::4] if 'COLOR' in a.data_type else tmp
            if a.domain == 'CORNER':
                vi = np.zeros(len(em.loops), np.int32); em.loops.foreach_get('vertex_index', vi)
                np.maximum.at(foam, vi, vals)
            else:
                foam = vals[:len(pts)]
    e.to_mesh_clear(); bpy.data.objects.remove(ob); bpy.data.meshes.remove(me)
    d = co - pts
    sh = X.shape
    return d[:, 0].reshape(sh), d[:, 1].reshape(sh), d[:, 2].reshape(sh), foam.reshape(sh)


def _sea_material(bpy, name, p, s):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = _N(nt)
    out = N('OutputMaterial')
    tc, sep = _xyz(N)
    depth, yy = _shore_depth(N, sep, s)
    water = N('BsdfPrincipled', inputs={'Base Color': _hex('#1A2A2C'), 'Roughness': p.get('rough', 0.03),
                                        'IOR': 1.333, 'Transmission Weight': 1.0, 'Specular IOR Level': 0.5})
    # chop: short wind ripples over the modelled swell, in world metres
    ch = N('TexNoise', inputs={'Vector': N('Mapping', inputs={'Vector': tc.outputs['Object'], 'Scale': (1.0, 2.0, 1.0)}).outputs[0],
                               'Scale': 1.4, 'Detail': 10.0, 'Roughness': 0.55})
    ch2 = N('TexWave', wave_type='BANDS', bands_direction='X', inputs={'Vector': tc.outputs['Object'], 'Scale': 0.35,
                                                                        'Distortion': 4.0, 'Detail': 4.0, 'Detail Scale': 2.0})
    h = N.math('ADD', ch.outputs['Fac'], N.math('MULTIPLY', ch2.outputs['Fac'], 0.5))
    bump = N('Bump', inputs={'Height': h, 'Strength': p.get('chop', 0.2), 'Distance': 0.04})
    N.link(bump.outputs['Normal'], water.inputs['Normal'])
    # the wash's lace where the water runs thin over the sand, and a thin white rim at its edge
    lace = N('TexVoronoi', feature='DISTANCE_TO_EDGE', inputs={'Vector': N('Mapping', inputs={
        'Vector': tc.outputs['Object'], 'Scale': (1.0, 1.8, 1.0)}).outputs[0], 'Scale': 3.2, 'Randomness': 1.0})
    lace_n = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 2.5, 'Detail': 6.0})
    lace_v = N('MapRange', inputs={'Value': lace.outputs['Distance'], 'From Min': p.get('lace_w', 0.08), 'From Max': 0.0}).outputs['Result']
    lace_v = N.math('MULTIPLY', lace_v, N('MapRange', inputs={'Value': lace_n.outputs['Fac'], 'From Min': 0.4, 'From Max': 0.6}).outputs['Result'])
    edge = N('MapRange', inputs={'Value': depth, 'From Min': 0.0, 'From Max': p.get('edge_m', 0.03)}).outputs['Result']
    edge = N.math('SUBTRACT', 1.0, edge)
    rim_n = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 6.0, 'Detail': 4.0})
    edge = N.math('MULTIPLY', edge, N('MapRange', inputs={'Value': rim_n.outputs['Fac'], 'From Min': 0.35, 'From Max': 0.6}).outputs['Result'])
    band = N('MapRange', inputs={'Value': depth, 'From Min': p.get('lace_to', 0.12), 'From Max': 0.0}).outputs['Result']
    foam = N.math('MAXIMUM', edge, N.math('MULTIPLY', lace_v, band), clamp=True)
    # the breakers' whitewater (from the mesh, `foam`), torn into streaks and lace
    at = N('Attribute', attribute_name='foam')
    streak = N('TexNoise', inputs={'Vector': N('Mapping', inputs={'Vector': tc.outputs['Object'], 'Scale': (0.5, 2.2, 1.0)}).outputs[0],
                                   'Scale': 2.0, 'Detail': 12.0, 'Roughness': 0.62})
    lace2 = N('TexVoronoi', feature='DISTANCE_TO_EDGE', inputs={'Vector': tc.outputs['Object'], 'Scale': 1.6})
    tear = N.math('ADD', N.math('MULTIPLY', streak.outputs['Fac'], 1.0), N.math('MULTIPLY', lace2.outputs['Distance'], -1.2))
    wf = N('MapRange', inputs={'Value': N.math('ADD', at.outputs['Fac'], N.math('MULTIPLY', N.math('SUBTRACT', tear, 0.35), 0.9)),
                               'From Min': 0.35, 'From Max': 0.6}).outputs['Result']
    foam = N.math('MAXIMUM', foam, wf, clamp=True)
    froth0 = N('BsdfPrincipled', inputs={'Base Color': _hex('#EEF3F4'), 'Roughness': 0.6, 'Subsurface Weight': 0.35,
                                         'Subsurface Radius': (0.02, 0.025, 0.03)})
    N.link(bump.outputs['Normal'], froth0.inputs['Normal'])
    # foam is thin: the low sun behind it comes through
    tl = N('BsdfTranslucent', inputs={'Color': _hex('#F4F1EA')})
    froth = N('MixShader', inputs={'Fac': p.get('foam_translucent', 0.45), 1: froth0.outputs[0], 2: tl.outputs[0]})
    mix = N('MixShader', inputs={'Fac': foam, 1: water.outputs[0], 2: froth.outputs[0]})
    vol = N('VolumeAbsorption', inputs={'Color': _hex(p.get('absorb', '#5E8F8C')), 'Density': p.get('density', 3.0)})
    N.link(mix.outputs[0], out.inputs['Surface']); N.link(vol.outputs[0], out.inputs['Volume'])
    return m


def sea(bpy, name, p, kit):
    """The sea as a closed body of water: its surface modelled (the breakers rolling in) from the beach out to the
    horizon, a floor 3 m down, and walls between."""
    s = _shore(p)
    x0, y0, x1, y1 = p.get('extent', [-420.0, 0.5, 420.0, 420.0])
    xs = _axis(x0, x1, -9.0, 9.0, p.get('cell', 0.04), 1.06)
    ys = _axis(y0, y1, y0, 14.0, p.get('cell', 0.04), 1.05)
    X, Y = np.meshgrid(xs, ys)
    Z, F = _waves(X, Y, s, p)
    oc = p.get('ocean')
    if oc:
        DX, DY, DZ, OF = _ocean(bpy, X, Y, oc)
        yy = Y + s['wiggle'] * np.sin(X * s['freq'] + s['phase'])
        dist = yy - (s['y0'] + (-s['water_z']) / s['slope'])
        k = np.clip((dist + 0.2) / oc.get('shoal_m', 6.0), 0, 1) ** 1.5      # the sea calms as it shoals onto the beach
        X = X + DX * k; Y = Y + DY * k; Z = Z + DZ * k
        F = np.maximum(F, np.clip(OF * oc.get('foam_gain', 1.0), 0, 1) * k)
    Z = Z + s['water_z']
    nx, ny = len(xs), len(ys)
    top = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    bot = top.copy(); bot[:, 2] = s['water_z'] - 3.0
    verts = np.concatenate([top, bot])
    n = nx * ny
    I, J = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1))
    a = (J * nx + I).ravel()
    faces = [np.stack([a, a + 1, a + nx + 1, a + nx], 1), np.stack([a + n, a + nx + n, a + nx + 1 + n, a + 1 + n], 1)]
    ring = ([j * nx for j in range(ny)][::-1] + list(range(nx)) + [j * nx + nx - 1 for j in range(ny)] + list(range(n - nx, n))[::-1])
    ring = [r for i, r in enumerate(ring) if i == 0 or r != ring[i - 1]]
    side = []
    for i in range(len(ring)):
        p0, p1 = ring[i], ring[(i + 1) % len(ring)]
        if p0 != p1:
            side.append([p0, p0 + n, p1 + n, p1])
    faces.append(np.array(side))
    faces = np.concatenate(faces)
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.astype(np.float32).ravel())
    me.loops.add(faces.size); me.loops.foreach_set('vertex_index', faces.astype(np.int32).ravel())
    me.polygons.add(len(faces)); me.polygons.foreach_set('loop_start', (np.arange(len(faces)) * 4).astype(np.int32))
    me.polygons.foreach_set('loop_total', np.full(len(faces), 4, np.int32))
    me.update(calc_edges=True); me.validate()
    me.polygons.foreach_set('use_smooth', np.ones(len(faces), bool))
    at = me.attributes.new('foam', 'FLOAT', 'POINT')
    at.data.foreach_set('value', np.concatenate([F.ravel(), np.zeros(n)]).astype(np.float32))
    me.materials.append(_sea_material(bpy, name + '-mat', p, s))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


# --- ice -----------------------------------------------------------------------------------------------------------
ICE = {'clear': {'absorb': '#6CBCE2', 'density': 1.1, 'scatter': 0.05, 'scatter_var': 5.0, 'rough': 0.02},
       'blue': {'absorb': '#4FAAD8', 'density': 1.7, 'scatter': 0.05, 'scatter_var': 4.0, 'rough': 0.02},
       'milky': {'absorb': '#8CC4EE', 'density': 1.2, 'scatter': 14.0, 'scatter_var': 10.0, 'rough': 0.12}}


def _ice_material(bpy, name, kind, p):
    k = dict(ICE[kind]); k.update(p.get('ice', {}))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = _N(nt)
    out = N('OutputMaterial')
    tc = N('TexCoord')
    bs = N('BsdfPrincipled', inputs={'Base Color': (1, 1, 1, 1), 'Transmission Weight': 1.0, 'IOR': 1.31,
                                     'Specular IOR Level': 0.5, 'Coat Weight': p.get('wet', 0.6), 'Coat Roughness': 0.03,
                                     'Coat IOR': 1.33})
    # roughness: wet glass in the hollows, frost and melt-haze in patches on the faces
    rn = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 4.0, 'Detail': 6.0})
    rr = N('MapRange', inputs={'Value': rn.outputs['Fac'], 'From Min': 0.45, 'From Max': 0.7,
                               'To Min': k['rough'], 'To Max': k['rough'] + p.get('frost', 0.07)}).outputs['Result']
    N.link(rr, bs.inputs['Roughness'])
    # melt scallops at the small scale, and a fine pitting
    sc = N('TexVoronoi', feature='SMOOTH_F1', inputs={'Vector': tc.outputs['Object'], 'Scale': 22.0, 'Smoothness': 0.4})
    pit = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 140.0, 'Detail': 4.0})
    b1 = N('Bump', inputs={'Height': sc.outputs['Distance'], 'Strength': 0.25, 'Distance': 0.01})
    b2 = N('Bump', inputs={'Height': pit.outputs['Fac'], 'Strength': 0.06, 'Distance': 0.002, 'Normal': b1.outputs['Normal']})
    N.link(b2.outputs['Normal'], bs.inputs['Normal'])
    # shadow rays pass through, tinted, so the ice throws blue light (the volume tints them further) instead of black
    tr = N('BsdfTransparent', inputs={'Color': (0.92, 0.95, 0.98, 1)})
    lp = N('LightPath')
    mix = N('MixShader', inputs={'Fac': lp.outputs['Is Shadow Ray'], 1: bs.outputs[0], 2: tr.outputs[0]})
    N.link(mix.outputs[0], out.inputs['Surface'])
    # the body: blue by absorption (the red end goes first), clouded by bubbles in drifts
    dn = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': p.get('cloud_scale', 3.0), 'Detail': 4.0})
    dv = N('MapRange', inputs={'Value': dn.outputs['Fac'], 'From Min': p.get('cloud_from', 0.56), 'From Max': p.get('cloud_to', 0.68),
                               'To Min': k['scatter'], 'To Max': k['scatter'] + k['scatter_var']}).outputs['Result']
    vol = N('VolumePrincipled', inputs={'Color': (1, 1, 1, 1), 'Density': dv, 'Anisotropy': 0.35,
                                        'Absorption Color': _hex(k['absorb'])})
    # Principled Volume's absorption scales with density: add a pure absorber for the ice's own blue
    ab = N('VolumeAbsorption', inputs={'Color': _hex(k['absorb']), 'Density': k['density']})
    av = N('AddShader', inputs={0: vol.outputs[0], 1: ab.outputs[0]})
    N.link(av.outputs[0], out.inputs['Volume'])
    return m


def _air_material(bpy, name):
    """Air inside the ice (bubbles, a crack): an interface from ice into air, bright where it turns light back."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = _N(nt)
    out = N('OutputMaterial')
    g = N('BsdfGlass', inputs={'IOR': 1.0 / 1.31, 'Roughness': 0.04, 'Color': (1, 1, 1, 1)})
    tr = N('BsdfTransparent'); lp = N('LightPath')
    mix = N('MixShader', inputs={'Fac': lp.outputs['Is Shadow Ray'], 1: g.outputs[0], 2: tr.outputs[0]})
    N.link(mix.outputs[0], out.inputs['Surface'])
    return m


def _chunk_mesh(bm, size, seed, subdiv, facets, worn, scallop, p_lumps=0.1):
    rnd = random.Random(seed)
    geom = bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    V = np.array([v.co[:] for v in bm.verts])
    S = np.array(size) / 2.0
    P = V * S
    off = Vector((rnd.uniform(-90, 90), rnd.uniform(-90, 90), rnd.uniform(-90, 90)))
    # broad lumps
    n = np.array([noise.noise(Vector(v) * 1.4 + off) for v in V])
    P *= (1.0 + p_lumps * n)[:, None]
    # fracture planes, the chunk calved and broken: flat faces
    planes = []
    for _ in range(facets):
        d = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 0.7))).normalized()
        nrm = np.array(d[:])
        sup = np.max(P @ nrm)
        planes.append((nrm, sup * rnd.uniform(0.55, 0.85)))
    planes.append((np.array([0.0, 0.0, -1.0]), S[2] * 0.62))          # its bed, where it sits
    for nrm, dd in planes:
        h = P @ nrm - dd
        P -= np.maximum(h, 0)[:, None] * nrm[None, :]
    # worn round by the sea: relax toward neighbours, which softens the facets' edges
    nb = [[] for _ in bm.verts]
    for e in bm.edges:
        a, b = e.verts[0].index, e.verts[1].index
        nb[a].append(b); nb[b].append(a)
    nbm = max(len(x) for x in nb)
    idx = np.array([x + [x[0]] * (nbm - len(x)) for x in nb])
    for _ in range(worn):
        P = 0.5 * P + 0.5 * P[idx].mean(1)
    # melt scallops: shallow cups between sharp ridges (Voronoi cells over the surface)
    if scallop > 0:
        cells = P[np.array(rnd.sample(range(len(P)), min(len(P), 160)))]
        dmin = np.full(len(P), 1e9)
        for c in np.array_split(cells, 8):
            dmin = np.minimum(dmin, np.min(np.linalg.norm(P[:, None, :] - c[None, :, :], axis=2), 1))
        cell = np.median(dmin) * 2.2 + 1e-6
        cup = scallop * (1.0 - np.clip(dmin / cell, 0, 1) ** 2)
        nrm = P / (np.linalg.norm(P, axis=1)[:, None] + 1e-9)
        P -= nrm * cup[:, None]
    zmin = P[:, 2].min()
    for v, q in zip(bm.verts, P):
        v.co = Vector((q[0], q[1], q[2] - zmin))
    return planes, zmin


def ice(bpy, name, p, kit):
    """One chunk of glacier ice standing at `position` (its bed at the position's z), turned by `rotate`."""
    size = p.get('size', [0.6, 0.5, 0.45]); seed = p.get('seed', 1); kind = p.get('ice_kind', 'clear')
    bm = bmesh.new()
    planes, zmin = _chunk_mesh(bm, size, seed, p.get('subdiv', 5), p.get('facets', 12), p.get('worn', 1),
                               p.get('scallop', min(size) * 0.025), p.get('lumps', 0.1))
    obs = kit.finish(bpy, name, bm, p, smooth=True, mat=_ice_material(bpy, name + '-ice', kind, p))
    ob = obs[0]
    ob.data.polygons.foreach_set('use_smooth', np.ones(len(ob.data.polygons), bool))
    S = np.array(size) / 2.0
    rnd = random.Random(seed * 7 + 1)
    air = _air_material(bpy, name + '-air')

    from mathutils.bvhtree import BVHTree
    bmt = bmesh.new(); bmt.from_mesh(ob.data); tree = BVHTree.FromBMesh(bmt); bmt.free()

    def inside(q, margin=0.012):
        """Inside the chunk as it was finally shaped, at least `margin` from its surface."""
        loc, nrm, _, dist = tree.find_nearest(Vector(q))
        return loc is not None and (Vector(q) - loc).dot(nrm) < 0 and dist > margin
    # bubbles: drifts of them along a few layers (the glacier's old snow), and a scatter between
    nb = p.get('bubbles', int(min(2500, 250 * np.prod(size) / 0.1)))
    if nb:
        bmb = bmesh.new()
        layers = [(Vector((rnd.gauss(0, 0.3), rnd.gauss(0, 0.3), 1)).normalized(), rnd.uniform(-0.4, 0.4)) for _ in range(3)]
        made, tries = 0, 0
        while made < nb and tries < nb * 40:
            tries += 1
            q = Vector((rnd.uniform(-1, 1) * S[0], rnd.uniform(-1, 1) * S[1], rnd.uniform(0, 2) * S[2]))
            if rnd.random() < 0.75:
                ln, lo = rnd.choice(layers)
                d = (q - Vector((0, 0, S[2]))).dot(ln) - lo * S[2]
                if abs(d) > rnd.gauss(0, 0.012) + 0.008:
                    continue
            if not inside(q[:], 0.006):
                continue
            r = rnd.uniform(0.0006, 0.0028) * (3.0 if rnd.random() < 0.04 else 1.0)
            geom = bmesh.ops.create_icosphere(bmb, subdivisions=1, radius=r)
            sq = rnd.uniform(0.6, 1.0)
            for v in geom['verts']:
                v.co = Vector((v.co.x, v.co.y, v.co.z * sq)) + q
            made += 1
        obs += kit.finish(bpy, name + '-bubbles', bmb, p, smooth=True, mat=air)
    # cracks: a thin sheet of air or two, inside, catching the light
    for c in range(p.get('cracks', 1)):
        bmc = bmesh.new()
        ctr = Vector((rnd.uniform(-0.2, 0.2) * S[0], rnd.uniform(-0.2, 0.2) * S[1], S[2] * rnd.uniform(0.7, 1.2)))
        nrm = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 0.6))).normalized()
        u = nrm.orthogonal().normalized(); w = nrm.cross(u)
        R = min(S) * rnd.uniform(0.35, 0.6)
        ring = []
        for i in range(36):
            a = 2 * math.pi * i / 36
            rr = R * (0.65 + 0.35 * noise.noise(Vector((math.cos(a) * 2, math.sin(a) * 2, c * 3.1 + seed))) + 0.2 * rnd.random())
            pt = ctr + u * (rr * math.cos(a)) + w * (rr * math.sin(a))
            pt += nrm * 0.02 * noise.noise(pt * 8)
            ring.append(pt)
        for _ in range(6):
            if all(inside(q[:], 0.01) for q in ring) and inside(ctr[:], 0.01):
                break
            ring = [ctr + (q - ctr) * 0.75 for q in ring]
        else:
            continue
        top = [bmc.verts.new(q + nrm * 0.0004) for q in ring]
        bot = [bmc.verts.new(q - nrm * 0.0004) for q in ring]
        bmc.faces.new(top); bmc.faces.new(bot[::-1])
        for i in range(36):
            j = (i + 1) % 36
            bmc.faces.new((top[j], top[i], bot[i], bot[j]))
        bmesh.ops.recalc_face_normals(bmc, faces=bmc.faces[:])
        obs += kit.finish(bpy, f'{name}-crack{c}', bmc, p, smooth=False, mat=air)
    return obs


# --- the cave (concept B's other half: inside a blue glacier ice cave) ----------------------------------------------
def _cave_ice_material(bpy, name, p, outer=False):
    """Thick glacier ice seen from inside: wet and glossy where melt runs, refractive, deep blue by absorption. Its
    outer face (under the snow) is frosted, so what comes through the ice is the daylight, diffused: the wall glows.
    Diffuse and shadow rays pass straight through (tinted by the volume), so the daylight outside reaches the cave as
    blue light without caustics. Absorption only: a scattering volume this thick cost minutes a proof."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = _N(nt)
    out = N('OutputMaterial'); tc = N('TexCoord')
    bs = N('BsdfPrincipled', inputs={'Base Color': (1, 1, 1, 1), 'Transmission Weight': 1.0, 'IOR': 1.31,
                                     'Specular IOR Level': 0.5, 'Coat Weight': 0.0 if outer else p.get('wet', 0.5),
                                     'Coat Roughness': 0.02, 'Coat IOR': 1.33})
    rn = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 1.2, 'Detail': 6.0})
    lo, hi = (p.get('outer_rough', [0.35, 0.6]) if outer else [0.03, p.get('frost', 0.2)])
    N.link(N('MapRange', inputs={'Value': rn.outputs['Fac'], 'From Min': 0.4, 'From Max': 0.7, 'To Min': lo,
                                 'To Max': hi}).outputs['Result'], bs.inputs['Roughness'])
    pit = N('TexNoise', inputs={'Vector': tc.outputs['Object'], 'Scale': 60.0, 'Detail': 4.0})
    b2 = N('Bump', inputs={'Height': pit.outputs['Fac'], 'Strength': 0.08, 'Distance': 0.003})
    N.link(b2.outputs['Normal'], bs.inputs['Normal'])
    if outer:
        # under the snow: the daylight comes through diffused, as through firn (a translucent face, lit from outside)
        tl = N('BsdfTranslucent', inputs={'Color': _hex(p.get('firn', '#F2F6FA'))})
        N.link(tl.outputs[0], out.inputs['Surface'])
    else:
        tr = N('BsdfTransparent', inputs={'Color': (0.95, 0.97, 0.99, 1)})
        lp = N('LightPath')
        passes = N.math('MAXIMUM', lp.outputs['Is Shadow Ray'], lp.outputs['Is Diffuse Ray'])
        mix = N('MixShader', inputs={'Fac': passes, 1: bs.outputs[0], 2: tr.outputs[0]})
        N.link(mix.outputs[0], out.inputs['Surface'])
    ab = N('VolumeAbsorption', inputs={'Color': _hex(p.get('absorb', '#3E93DC')), 'Density': p.get('density', 1.4)})
    N.link(ab.outputs[0], out.inputs['Volume'])
    return m


def cave(bpy, name, p, kit):
    """A tunnel through glacier ice: an arch `width` x `height` (m) along y from `y_range`, its centreline bending by
    `bend` [y_start, dx_at_end] beyond the speaker, its inner face scalloped by melt (`scallop` [cell m, depth m]),
    the ice `thickness` [min, max] m thick, a `hole` [y, x, r] through the roof. One closed solid."""
    y0, y1 = p.get('y_range', [-10.0, 16.0])
    W, Hh = p.get('width', 4.6), p.get('height', 3.3)
    dy = p.get('step', 0.05)
    ys = np.arange(y0, y1 + 1e-9, dy)
    nth = p.get('around', 260)
    th = np.linspace(-0.22, math.pi + 0.22, nth)
    by, bdx = p.get('bend', [3.0, 4.0])
    cx = np.where(ys > by, bdx * ((ys - by) / (y1 - by)) ** 2, 0.0)
    rnd = random.Random(p.get('seed', 7)); off = rnd.uniform(-50, 50)
    TH, Y = np.meshgrid(th, ys)
    CX = cx[:, None] * np.ones_like(TH)
    c, s = np.cos(TH), np.sin(TH)
    # a rounded arch with steep walls: a superellipse, the walls running a little below the floor
    ex = 0.75
    ux = np.sign(c) * np.abs(c) ** ex
    uz = np.sign(s) * np.abs(s) ** 0.85
    # its size wanders along the tunnel, and big lumps of melt-out on the faces
    lump = np.vectorize(lambda a, b: noise.noise(Vector((a * 0.45 + off, b * 0.45, 0.3))))
    lump2 = np.vectorize(lambda a, b: noise.noise(Vector((a * 1.3 + off, b * 1.3, 2.1))))
    arc = TH * (W + Hh) / 2.0                                        # roughly metres round the arch
    L = 1.0 + p.get('lumps', [0.14, 0.02])[0] * lump(Y, arc) + p.get('lumps', [0.14, 0.02])[1] * lump2(Y, arc)
    wid = (W / 2) * (1.0 + 0.12 * np.vectorize(lambda a: noise.noise(Vector((a * 0.15 + off, 5.0, 0.0))))(Y))
    hgt = Hh * (1.0 + 0.10 * np.vectorize(lambda a: noise.noise(Vector((a * 0.12 + off, 9.0, 0.0))))(Y))
    IX = CX + wid * ux * L
    IZ = hgt * uz * L
    # normal direction (outward, into the ice), in the section's plane
    nx_, nz_ = ux / (wid + 1e-9), uz / (hgt + 1e-9)
    nn = np.hypot(nx_, nz_) + 1e-9; nx_, nz_ = nx_ / nn, nz_ / nn
    # melt scallops: shallow cups in a jittered grid over (y, arc), deepest at their centres, sharp ridges between
    cell, depth = p.get('scallop', [0.38, 0.05])
    gy, ga = Y / cell, arc / cell
    best = np.full(Y.shape, 9.0)
    jr = np.random.RandomState(p.get('seed', 7))
    J = jr.uniform(-0.5, 0.5, (2, 4096))
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            ci, cj = np.floor(gy) + di, np.floor(ga) + dj
            h = ((ci.astype(np.int64) * 73856093) ^ (cj.astype(np.int64) * 19349663)) % 4096
            py, pa = ci + 0.5 + 0.8 * J[0][h], cj + 0.5 + 0.8 * J[1][h]
            best = np.minimum(best, (gy - py) ** 2 + (ga - pa) ** 2)
    cup = depth * (1.0 - np.clip(np.sqrt(best) / 0.75, 0, 1) ** 2)
    IX += nx_ * cup; IZ += nz_ * cup
    tmin, tmax = p.get('thickness', [0.9, 2.2])
    T = tmin + (tmax - tmin) * np.clip(0.5 + lump(Y * 0.7 + 3.0, arc * 0.7), 0, 1)
    if p.get('hole'):                                                # the roof thins toward the hole (a moulin's throat)
        hy, hx, hry, hrx = p['hole']
        qq = np.hypot((Y - hy) / (hry * 1.8), (IX - hx) / (hrx * 2.2))
        T = T * (1.0 - 0.75 * np.exp(-qq ** 2) * (IZ > hgt * 0.4))
    OX, OZ = IX + nx_ * T, IZ + nz_ * T
    ny, nt = Y.shape
    inner = np.stack([IX.ravel(), Y.ravel(), IZ.ravel()], 1)
    outer = np.stack([OX.ravel(), Y.ravel(), OZ.ravel()], 1)
    verts = np.concatenate([inner, outer]); n = len(inner)
    # which faces are kept: all but the roof hole
    keep = np.ones((ny - 1, nt - 1), bool)
    if p.get('hole'):
        hy, hx, hry, hrx = p['hole']                                   # its centre and its radii along y and x
        fy = (Y[:-1, :-1] + Y[1:, 1:]) / 2; fx = (IX[:-1, :-1] + IX[1:, 1:]) / 2; fz = (IZ[:-1, :-1] + IZ[1:, 1:]) / 2
        q = np.hypot((fy - hy) / hry, (fx - hx) / hrx) + 0.25 * np.vectorize(lambda a, b: noise.noise(Vector((a * 2.0, b * 2.0, 4.0))))(fy, fx)
        keep &= ~((q < 1.0) & (fz > hgt[:-1, :-1] * 0.5))
    jj, ii = np.nonzero(keep)
    a = jj * nt + ii
    fin = np.stack([a, a + nt, a + nt + 1, a + 1], 1)               # facing into the tunnel
    fout = np.stack([a + n, a + 1 + n, a + nt + 1 + n, a + nt + n], 1)
    side = []
    K = np.pad(keep, 1, constant_values=False)
    for j, i in zip(jj, ii):
        v00, v01, v10, v11 = j * nt + i, j * nt + i + 1, (j + 1) * nt + i, (j + 1) * nt + i + 1
        if not K[j + 1, i]:                                          # edge at theta i (v00-v10)
            side.append([v00, v00 + n, v10 + n, v10])
        if not K[j + 1, i + 2]:                                      # edge at theta i+1 (v01-v11)
            side.append([v01, v11, v11 + n, v01 + n])
        if not K[j, i + 1]:                                          # edge at row j (v00-v01)
            side.append([v00, v01, v01 + n, v00 + n])
        if not K[j + 2, i + 1]:                                      # edge at row j+1 (v10-v11)
            side.append([v10, v10 + n, v11 + n, v11])
    faces = np.concatenate([fin, fout, np.array(side, np.int64)])
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.astype(np.float32).ravel())
    me.loops.add(faces.size); me.loops.foreach_set('vertex_index', faces.astype(np.int32).ravel())
    me.polygons.add(len(faces)); me.polygons.foreach_set('loop_start', (np.arange(len(faces)) * 4).astype(np.int32))
    me.polygons.foreach_set('loop_total', np.full(len(faces), 4, np.int32))
    me.update(calc_edges=True); me.validate()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); bm.to_mesh(me); bm.free()
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), bool))
    me.materials.append(_cave_ice_material(bpy, name + '-ice', p.get('ice', {})))
    me.materials.append(_cave_ice_material(bpy, name + '-ice-outer', p.get('ice', {}), outer=True))
    mi = np.zeros(len(me.polygons), np.int32); mi[len(fin):len(fin) + len(fout)] = 1
    me.polygons.foreach_set('material_index', mi)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]
