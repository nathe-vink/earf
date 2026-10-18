"""Planet EARF, the listening bar (round 32): the room as one kit `ext` piece, built from the plan
(spinoffs/barkhorn/planet/plan.py), every dimension read from there.

    {"kind": "kit", "shape": "ext", "module": "planet_room", "fn": "room", "clock": "late", ...}

What it builds, in world metres (the plan's frame; z up, the floor at 0):

- the shell: concrete floor (photographed, honed and sealed), the walls with the long street window and the plain door,
  the slab;
- the ceiling: a stretched micro-perforated membrane, back-lit in the colour clock's two colours graded down the
  room, with its perimeter shadow gap and the profiles of its seams;
- the bar: eight 20 mm cast-acrylic panels in spectrum order, each over a white liner with an LED cavity behind it,
  so each glows its own colour evenly (`panel_glow`); a toe-kick in shadow, a bronze footrail, a honed basalt top;
- the back-bar: a base cabinet, edge-lit 10 mm light-guide shelves (the working shelves warm white, the display shelves
  tinted bay by bay to the panel below), a softly lit Fog-white back panel, bottles, and two niches for the Fog pair;
- the booths along the window: upholstered benches, Smoke acrylic tables;
- the lounge: thermoformed Fog screens, the Smoke plinths of the corner pairs, tinted Haze slats over dark absorber on
  the street wall, plain absorber opposite, a wool rug, low side tables;
- the record wall: cubbies of uneven depth, floor to membrane, full of sleeves, and the DJ desk set into it, clad in
  Smoke;
- the street (`street`: true): the sidewalks, the road, the building's facade and the flats above, the side street,
  the block across, street lamps (their light is the shot's), the small neon EARF sign over the door.

Optional settings (all have defaults): clock ('opening', 'sunset', 'late', 'last'), membrane (emission strength),
panel_glow, shelf_glow, backpanel_glow, niche_glow, slat_glow, record_glow, street (bool), neon, windows_lit.
"""
import math, os, random, sys

import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet'))
import plan as P                                                     # noqa: E402

_M = {}


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def _mixhex(a, b, t):
    A, B = lin(a), lin(b)
    return tuple(A[i] * (1 - t) + B[i] * t for i in range(3)) + (1.0,)


def _set(b, k, v):
    if k in b.inputs:
        b.inputs[k].default_value = v


# --- materials -----------------------------------------------------------------------------------------------------
def principled(bpy, name, color, rough=0.5, metal=0.0, coat=0.0, coat_rough=0.05, emit=None, strength=0.0,
               trans=0.0, ior=1.5, spec=0.5, sss=0.0, sheen=0.0, alpha=1.0, bump=None):
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    _set(b, 'Base Color', lin(color) if isinstance(color, str) else color)
    _set(b, 'Roughness', rough); _set(b, 'Metallic', metal); _set(b, 'Specular IOR Level', spec)
    _set(b, 'Coat Weight', coat); _set(b, 'Coat Roughness', coat_rough)
    _set(b, 'Transmission Weight', trans); _set(b, 'IOR', ior); _set(b, 'Alpha', alpha)
    _set(b, 'Subsurface Weight', sss); _set(b, 'Sheen Weight', sheen)
    if emit is not None and strength > 0:
        _set(b, 'Emission Color', lin(emit) if isinstance(emit, str) else emit); _set(b, 'Emission Strength', strength)
    if bump:
        size, s, d = bump
        tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 1.0 / size; nz.inputs['Detail'].default_value = 8.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = s; bp.inputs['Distance'].default_value = d
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    _M[name] = m
    return m


def emitter(bpy, name, color, strength, two_sided=True):
    """A plain emitter (a lit diffuser's face): what it lights it lights in its colour."""
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = lin(color) if isinstance(color, str) else color
    em.inputs['Strength'].default_value = strength
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    _M[name] = m
    return m


def lit_acrylic(bpy, name, color, glow, deep=None, rough=0.04):
    """Back-lit tinted cast acrylic over a white liner: its colour glows from within, evenly (the liner diffuses the
    LEDs 75 mm behind it), under a polished face that mirrors the room. Emission plus a clear coat: the light the
    panel sends into the room is its colour's."""
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    _set(b, 'Base Color', lin(deep or color)); _set(b, 'Roughness', 0.35); _set(b, 'Specular IOR Level', 0.0)
    _set(b, 'Coat Weight', 1.0); _set(b, 'Coat Roughness', rough); _set(b, 'Coat IOR', 1.49)
    # the glow, a little brighter at the panel's middle than at its frame (the liner's light falls off to the edges)
    tc = nt.nodes.new('ShaderNodeTexCoord'); gr = nt.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.2, 1.2, 1.2)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    sub = nt.nodes.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.6, 0.6, 0.6)
    nt.links.new(mp.outputs['Vector'], sub.inputs[0]); nt.links.new(sub.outputs['Vector'], gr.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.82; mr.inputs['To Max'].default_value = 1.0
    nt.links.new(gr.outputs['Fac'], mr.inputs['Value'])
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = glow
    nt.links.new(mr.outputs['Result'], mul.inputs[0])
    _set(b, 'Emission Color', lin(color)); nt.links.new(mul.outputs['Value'], b.inputs['Emission Strength'])
    _M[name] = m
    return m


def stone(bpy, name='basalt'):
    """Honed basalt: near black, a fine grey speckle and a faint cloud, honed (a soft sheen, not a mirror)."""
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 6.0
    vz = nt.nodes.new('ShaderNodeTexVoronoi'); vz.inputs['Scale'].default_value = 900.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector']); nt.links.new(tc.outputs['Object'], vz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = 0.35; cr.elements[0].color = lin('#141416')
    cr.elements[1].position = 0.75; cr.elements[1].color = lin('#26272A')
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    spk = nt.nodes.new('ShaderNodeMath'); spk.operation = 'GREATER_THAN'; spk.inputs[1].default_value = 0.93
    nt.links.new(vz.outputs['Distance'], spk.inputs[0])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['B'].default_value = lin('#55565A')
    nt.links.new(spk.outputs['Value'], mix.inputs['Factor']); nt.links.new(ramp.outputs['Color'], mix.inputs['A'])
    nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    _set(b, 'Roughness', 0.32); _set(b, 'Specular IOR Level', 0.5)
    rn = nt.nodes.new('ShaderNodeTexNoise'); rn.inputs['Scale'].default_value = 40.0
    nt.links.new(tc.outputs['Object'], rn.inputs['Vector'])
    rm = nt.nodes.new('ShaderNodeMapRange'); rm.inputs['To Min'].default_value = 0.26; rm.inputs['To Max'].default_value = 0.40
    nt.links.new(rn.outputs['Fac'], rm.inputs['Value']); nt.links.new(rm.outputs['Result'], b.inputs['Roughness'])
    _M[name] = m
    return m


def colour_attr_mat(bpy, name, rough=0.55, coat=0.0, spec=0.4):
    """A material whose base colour is the mesh's own `col` attribute (a sleeve's spine, a label)."""
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = 'col'
    nt.links.new(at.outputs['Color'], b.inputs['Base Color'])
    _set(b, 'Roughness', rough); _set(b, 'Coat Weight', coat); _set(b, 'Specular IOR Level', spec)
    _M[name] = m
    return m


def membrane_mat(bpy, a, b_, strength, x0, x1):
    """The back-lit membrane: emission graded from colour a at the door to colour b at the record wall, a translucent
    white face (it is a stretched foil), and a faint unevenness where the LEDs above are nearer."""
    m = bpy.data.materials.new('membrane'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = x0; mr.inputs['From Max'].default_value = x1
    mr.interpolation_type = 'SMOOTHSTEP'
    nt.links.new(sep.outputs['X'], mr.inputs['Value'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = a; mix.inputs['B'].default_value = b_
    nt.links.new(mr.outputs['Result'], mix.inputs['Factor'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 2.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nr = nt.nodes.new('ShaderNodeMapRange'); nr.inputs['To Min'].default_value = 0.9 * strength; nr.inputs['To Max'].default_value = 1.1 * strength
    nt.links.new(nz.outputs['Fac'], nr.inputs['Value'])
    em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(mix.outputs['Result'], em.inputs['Color'])
    nt.links.new(nr.outputs['Result'], em.inputs['Strength'])
    df = nt.nodes.new('ShaderNodeBsdfDiffuse'); df.inputs['Color'].default_value = (0.75, 0.75, 0.75, 1)
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(em.outputs['Emission'], add.inputs[0]); nt.links.new(df.outputs['BSDF'], add.inputs[1])
    nt.links.new(add.outputs['Shader'], out.inputs['Surface'])
    return m


# --- geometry ------------------------------------------------------------------------------------------------------
class Mesh:
    """Boxes (and other faces) gathered into one object per material; `col` per box when the material reads it."""

    def __init__(self, name):
        self.name = name; self.bm = bmesh.new(); self.col = None

    def box(self, x0, y0, z0, x1, y1, z1, col=None, skip=()):
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
        bm = self.bm
        vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
        faces = {'-z': (0, 3, 2, 1), '+z': (4, 5, 6, 7), '-y': (0, 1, 5, 4), '+x': (1, 2, 6, 5), '+y': (2, 3, 7, 6),
                 '-x': (3, 0, 4, 7)}
        out = []
        for k, f in faces.items():
            if k in skip:
                continue
            fa = bm.faces.new([vs[i] for i in f]); fa.normal_update(); out.append(fa)
        if col is not None:
            if self.col is None:
                self.col = bm.loops.layers.float_color.new('col')
            for fa in out:
                for lp in fa.loops:
                    lp[self.col] = col
        return out

    def quad(self, pts):
        fa = self.bm.faces.new([self.bm.verts.new(p) for p in pts]); fa.normal_update()
        return fa

    def object(self, bpy, mat, smooth=False, coll=None):
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        for f in me.polygons:
            f.use_smooth = smooth
        me.materials.append(mat)
        ob = bpy.data.objects.new(self.name, me); bpy.context.scene.collection.objects.link(ob)
        return ob


def _lathe(bm, prof, seg=32, z0=0.0, cx=0.0, cy=0.0):
    rings = []
    for r, z in prof:
        ring = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            ring.append(bm.verts.new((cx + r * math.cos(a), cy + r * math.sin(a), z0 + z)))
        rings.append(ring)
    for k in range(len(rings) - 1):
        for i in range(seg):
            j = (i + 1) % seg
            f = bm.faces.new([rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]]); f.normal_update()
    top = bm.faces.new(rings[-1]); top.normal_update()
    bot = bm.faces.new(list(reversed(rings[0]))); bot.normal_update()


def _cyl(bm, cx, cy, z0, r, h, seg=32, axis='z'):
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h)
    for v in g['verts']:
        x, y, z = v.co
        if axis == 'z':
            v.co = Vector((cx + x, cy + y, z0 + h / 2 + z))
        elif axis == 'x':
            v.co = Vector((z0 + h / 2 + z, cx + x, cy + y))
        else:
            v.co = Vector((cx + x, z0 + h / 2 + z, cy + y))
    return g


# --- the pieces ----------------------------------------------------------------------------------------------------
def _pbr(bpy, kit, tex, **k):
    import assets
    key = f'pbr-{tex}-{sorted(k.items())}'
    if key not in _M:
        _M[key] = assets.pbr(bpy, tex, k.pop('res', '2k'), **k)
    return _M[key]


def shell(bpy, kit, p, objs):
    L, D, H, T = P.L, P.D, P.SLAB, P.WALL_T
    floor = Mesh('floor'); floor.box(-T, -T, -0.2, L + T, D + T, 0.0)
    fm = _pbr(bpy, kit, p.get('floor_tex', 'concrete_floor_worn_001'), res='4k', tint=p.get('floor_tint', '#6B6862'),
              tint_mix=p.get('floor_tint_mix', 0.55), rough_mul=0.55)
    _set(next(n for n in fm.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), 'Coat Weight', p.get('floor_coat', 0.35))
    objs.append(floor.object(bpy, fm))
    # the walls: concrete, painted out dark inside (the room's light comes from its acrylic, not its walls)
    walls = Mesh('walls')
    W = P.WINDOW; Dr = P.DOOR
    # y = 0, the long street wall, the window cut out
    walls.box(-T, -T, 0, W['x0'], 0, H)
    walls.box(W['x1'], -T, 0, L + T, 0, H)
    walls.box(W['x0'], -T, 0, W['x1'], 0, W['sill'])
    walls.box(W['x0'], -T, W['head'], W['x1'], 0, H)
    # y = D, the party wall
    walls.box(-T, D, 0, L + T, D + T, H)
    # x = 0, the side street, the door cut out
    walls.box(-T, 0, 0, 0, Dr['y0'], H)
    walls.box(-T, Dr['y1'], 0, 0, D, H)
    walls.box(-T, Dr['y0'], Dr['h'], 0, Dr['y1'], H)
    # x = L, the back wall
    walls.box(L, 0, 0, L + T, D, H)
    walls.box(-T, -T, H, L + T, D + T, H + 0.25)                    # the slab
    wm = principled(bpy, 'wall-paint', p.get('wall', '#2A2826'), rough=0.85, spec=0.3, bump=(0.02, 0.05, 0.002))
    objs.append(walls.object(bpy, wm))


def ceiling(bpy, kit, p, objs):
    L, D, z, g = P.L, P.D, P.MEMBRANE, P.MEMBRANE_GAP
    a, b = P.CLOCK[p.get('clock', 'late')]
    s = p.get('membrane', 0.35)
    ca, cb = (_mixhex(P.COLOURS[a], '#FFFFFF', p.get('membrane_white', 0.25)),
              _mixhex(P.COLOURS[b], '#FFFFFF', p.get('membrane_white', 0.25)))
    if a == 'smoke':                                               # last call: the membrane dimmed to a warm grey
        ca = cb = _mixhex('#6E6A66', '#000000', 0.0)
        s *= p.get('last_dim', 0.25)
    mem = Mesh('membrane')
    mem.quad([(g, g, z), (g, D - g, z), (L - g, D - g, z), (L - g, g, z)])        # facing down
    objs.append(mem.object(bpy, membrane_mat(bpy, ca, cb, s, 0.0, L)))
    # the perimeter: a dark plaster soffit band and the shadow gap above it, and the seams' profiles every 4.6 m
    edge = Mesh('membrane-edge')
    edge.box(0, 0, z, L, g, z + 0.02); edge.box(0, D - g, z, L, D, z + 0.02)
    edge.box(0, g, z, g, D - g, z + 0.02); edge.box(L - g, g, z, L, D - g, z + 0.02)
    for xs in (6.10, 12.20):                                                 # two seams, across the room
        edge.box(xs - 0.008, g, z - 0.004, xs + 0.008, D - g, z + 0.004)
    edge.box(-0.01, -0.01, z + 0.02, L + 0.01, D + 0.01, z + 0.03)           # the plenum's closure (black)
    objs.append(edge.object(bpy, principled(bpy, 'profile', '#1A1A1B', rough=0.5, metal=0.6)))


def window_and_door(bpy, kit, p, objs):
    W, Dr = P.WINDOW, P.DOOR
    fr = Mesh('window-frame'); f = W['frame']
    for xm in [W['x0'], *W['mullions'], W['x1']]:
        fr.box(xm - f / 2, -0.12, W['sill'], xm + f / 2, -0.05, W['head'])
    fr.box(W['x0'], -0.12, W['sill'], W['x1'], -0.05, W['sill'] + f)
    fr.box(W['x0'], -0.12, W['head'] - f, W['x1'], -0.05, W['head'])
    fr.box(W['x0'], -0.12, 2.55, W['x1'], -0.05, 2.55 + f)                   # the transom bar
    fr.box(W['x0'] - 0.02, -0.30, W['sill'] - 0.02, W['x1'] + 0.02, 0.02, W['sill'])   # the sill
    objs.append(fr.object(bpy, principled(bpy, 'bronze-anodised', '#2E2A25', rough=0.38, metal=0.9)))
    gl = Mesh('glass'); gl.box(W['x0'], -0.09, W['sill'], W['x1'], -0.08, W['head'])
    objs.append(gl.object(bpy, principled(bpy, 'window-glass', '#FFFFFF', rough=0.0, trans=1.0, ior=1.5)))
    # the plain door: blackened steel, a pull, a slot of a window at eye height left out (it is plain)
    dr = Mesh('door'); dr.box(-0.10, Dr['y0'] + 0.01, 0.0, -0.05, Dr['y1'] - 0.01, Dr['h'] - 0.01)
    objs.append(dr.object(bpy, principled(bpy, 'blackened-steel', '#1C1B1A', rough=0.42, metal=0.85,
                                          bump=(0.03, 0.08, 0.001))))
    pull = Mesh('door-pull')
    pull.box(-0.045, Dr['y1'] - 0.13, 0.95, -0.03, Dr['y1'] - 0.11, 1.25)
    objs.append(pull.object(bpy, principled(bpy, 'bronze', '#8A6A44', rough=0.3, metal=1.0)))


def bar(bpy, kit, p, objs):
    x0, yF = P.BAR_X0, P.BAR_FRONT
    zt = P.BAR_TOP_Z
    glow = p.get('panel_glow', 2.2)
    for i, c in enumerate(P.PANELS):
        a = x0 + i * P.PANEL_W
        pan = Mesh(f'bar-panel-{c}')
        # a 3 mm reveal between panels, the panel from the toe-kick to the top's underside
        pan.box(a + 0.0015, yF, P.KICK, a + P.PANEL_W - 0.0015, yF + P.PANEL_T, zt - 0.006)
        g = glow * {'fog': 0.55, 'smoke': 0.45, 'acid': 0.8, 'ice': 1.0, 'poison': 1.25, 'haze': 1.3}.get(c, 1.0)
        col = P.COLOURS[c] if c not in ('fog',) else '#F2F0EA'
        deep = {'smoke': '#141316', 'fog': '#DAD8D2'}.get(c, P.COLOURS[c])
        emit_col = {'smoke': '#5A5660'}.get(c, col)
        objs.append(pan.object(bpy, lit_acrylic(bpy, f'bar-acrylic-{c}', emit_col, g, deep=deep)))
    # the frame behind: the liner's returns, the cavity's body, the counter
    body = Mesh('bar-body')
    body.box(x0, yF + P.PANEL_T, 0.0, P.BAR_X1, yF + P.BAR_DEPTH, zt - 0.006)
    body.box(x0 - 0.04, yF - 0.002, 0.0, x0, yF + P.BAR_DEPTH, zt - 0.006)                # end caps (Smoke)
    body.box(P.BAR_X1, yF - 0.002, 0.0, P.BAR_X1 + 0.04, yF + P.BAR_DEPTH, zt - 0.006)
    objs.append(body.object(bpy, principled(bpy, 'smoke-acrylic', '#0E0D10', rough=0.06, coat=1.0, coat_rough=0.03)))
    kick = Mesh('bar-kick'); kick.box(x0, yF + P.KICK_SET, 0.0, P.BAR_X1, yF + P.PANEL_T + 0.1, P.KICK)
    objs.append(kick.object(bpy, principled(bpy, 'kick', '#0A0A0A', rough=0.7)))
    top = Mesh('bar-top')
    top.box(x0 - 0.10, yF - P.TOP_OVER, zt, P.BAR_X1 + 0.10, yF + P.BAR_DEPTH + 0.04, zt + P.TOP_T)
    objs.append(top.object(bpy, stone(bpy)))
    # the footrail: 50 mm bronze on brackets
    fr = Mesh('footrail'); fy = yF - P.FOOTRAIL['off']; fz = P.FOOTRAIL['z']
    _cyl(fr.bm, fy, fz, x0 + 0.1, P.FOOTRAIL['d'] / 2, P.BAR_X1 - x0 - 0.2, seg=24, axis='x')
    for k in range(9):
        bx = x0 + 0.15 + k * (P.BAR_X1 - x0 - 0.3) / 8
        _cyl(fr.bm, bx, fy + 0.0, fz - 0.006, 0.008, P.FOOTRAIL['off'] + 0.006, seg=10, axis='y')
        fr.box(bx - 0.012, fy, 0.0, bx + 0.012, fy + 0.024, fz)
    objs.append(fr.object(bpy, principled(bpy, 'bronze', '#8A6A44', rough=0.3, metal=1.0), smooth=True))


def _bottle_meshes(bpy):
    """Four bottles (a whisky square-shouldered, a tall gin, a squat cognac, a long-neck wine/amaro) as lathed bodies,
    labels and caps, shared by every copy."""
    kinds = {
        'whisky': [(0.0, 0.0), (0.040, 0.0), (0.042, 0.004), (0.042, 0.20), (0.036, 0.225), (0.015, 0.245),
                   (0.0135, 0.29), (0.0, 0.29)],
        'gin': [(0.0, 0.0), (0.036, 0.0), (0.038, 0.004), (0.038, 0.24), (0.030, 0.262), (0.013, 0.28), (0.012, 0.32),
                (0.0, 0.32)],
        'cognac': [(0.0, 0.0), (0.050, 0.0), (0.056, 0.03), (0.058, 0.10), (0.050, 0.15), (0.020, 0.18), (0.016, 0.215),
                   (0.0, 0.215)],
        'amaro': [(0.0, 0.0), (0.036, 0.0), (0.037, 0.004), (0.037, 0.19), (0.030, 0.225), (0.0135, 0.26),
                  (0.0125, 0.335), (0.0, 0.335)],
    }
    out = {}
    for k, prof in kinds.items():
        bm = bmesh.new(); _lathe(bm, prof, seg=28)
        body = bpy.data.meshes.new(f'bottle-{k}'); bm.to_mesh(body); bm.free()
        for f in body.polygons:
            f.use_smooth = True
        r = max(r for r, z in prof if z < 0.2)
        zl0, zl1 = (0.05, 0.15) if k != 'cognac' else (0.05, 0.10)
        bm = bmesh.new()
        ring = [(r + 0.0012, zl0), (r + 0.0012, zl1)]
        segs = 28
        vs = [[bm.verts.new(((r + 0.0012) * math.cos(a), (r + 0.0012) * math.sin(a), z))
               for a in [math.pi * 0.45 + 1.4 * math.pi * i / segs for i in range(segs + 1)]] for _, z in ring]
        for i in range(segs):
            f = bm.faces.new([vs[0][i], vs[0][i + 1], vs[1][i + 1], vs[1][i]]); f.normal_update()
        label = bpy.data.meshes.new(f'label-{k}'); bm.to_mesh(label); bm.free()
        for f in label.polygons:
            f.use_smooth = True
        top = prof[-1][1]; rn = prof[-2][0]
        bm = bmesh.new(); _cyl(bm, 0, 0, top - 0.03, rn + 0.002, 0.034, seg=20)
        cap = bpy.data.meshes.new(f'cap-{k}'); bm.to_mesh(cap); bm.free()
        out[k] = (body, label, cap, r)
    return out


def backbar(bpy, kit, p, objs):
    y0, D = P.BACKBAR_Y, P.D
    x0, x1 = P.BAR_X0 - 0.35, P.BAR_X1 + 0.35
    rnd = random.Random(32)
    carc = Mesh('backbar-carcass')
    # the base cabinet, its doors in Smoke acrylic, with the niches cut out
    niches = [(nx, nx + nw) for nx, nw in P.NICHES]
    def solid_runs(a, b):
        runs, cur = [], a
        for n0, n1 in niches:
            runs.append((cur, n0)); cur = n1
        runs.append((cur, b))
        return runs
    for a, b in solid_runs(x0, x1):
        carc.box(a, y0, 0.0, b, D, P.BASE_H)
    # the counter's top: the same basalt
    tops = Mesh('backbar-top')
    for a, b in solid_runs(x0, x1):
        tops.box(a, y0 - 0.02, P.BASE_H, b, D, P.BASE_H + 0.03)
    objs.append(tops.object(bpy, stone(bpy)))
    # the uprights between the bays (Smoke), the head, the niches' surrounds
    bays = [x0] + [P.BAR_X0 + i * P.PANEL_W for i in range(1, len(P.PANELS))] + [x1]
    for xb in bays:
        carc.box(xb - 0.02, y0 + 0.02, P.BASE_H + 0.03, xb + 0.02, D, P.SHELF_TOP_Z)
    carc.box(x0, y0, P.SHELF_TOP_Z, x1, D, P.SHELF_TOP_Z + 0.12)
    for n0, n1 in niches:
        carc.box(n0 - 0.03, y0, 0.0, n0, D, P.NICHE_Z0 + P.NICHE_H + 0.03)
        carc.box(n1, y0, 0.0, n1 + 0.03, D, P.NICHE_Z0 + P.NICHE_H + 0.03)
        carc.box(n0 - 0.03, y0, P.NICHE_Z0 + P.NICHE_H, n1 + 0.03, D, P.NICHE_Z0 + P.NICHE_H + 0.03)
        carc.box(n0, y0, 0.0, n1, D, P.NICHE_Z0)
    objs.append(carc.object(bpy, principled(bpy, 'smoke-acrylic', '#0E0D10', rough=0.06, coat=1.0, coat_rough=0.03)))
    # the back panel: Fog-white acrylic, softly back-lit, the bottles in silhouette against it
    bk = Mesh('backbar-backpanel')
    for i in range(len(bays) - 1):
        a, b = bays[i] + 0.02, bays[i + 1] - 0.02
        segs = [(a, b)]
        for n0, n1 in niches:
            if n0 < b and n1 > a:
                segs = [(a, n0 - 0.03), (n1 + 0.03, b)]
        for s0, s1 in segs:
            if s1 - s0 > 0.05:
                bk.box(s0, D - 0.03, P.BASE_H + 0.03, s1, D - 0.01, P.SHELF_TOP_Z)
    objs.append(bk.object(bpy, lit_acrylic(bpy, 'backpanel', p.get('backpanel_color', '#F3E6D2'),
                                           p.get('backpanel_glow', 0.45), deep='#E8E2D8', rough=0.25)))
    # the niches' linings: white, lit from their heads
    for k, (n0, n1) in enumerate(niches):
        ln = Mesh(f'niche-{k}')
        ln.box(n0, D - 0.03, P.NICHE_Z0, n1, D - 0.01, P.NICHE_Z0 + P.NICHE_H)
        objs.append(ln.object(bpy, lit_acrylic(bpy, 'niche-lining', '#FFF1DE', p.get('niche_glow', 0.35),
                                               deep='#EDE8E0', rough=0.3)))
    # the shelves: 10 mm light-guide acrylic, edge-lit from a channel at the back, so their faces and the front
    # edge glow; the lower ones warm white, the display ones tinted bay by bay
    bodies = _bottle_meshes(bpy)
    glass = {}
    def glass_mat(c, k):
        key = (c, k)
        if key not in glass:
            glass[key] = principled(bpy, f'bottle-glass-{c}-{k}', c, rough=0.02, trans=1.0, ior=1.45)
        return glass[key]
    labels = [principled(bpy, f'label-{i}', c, rough=0.6) for i, c in
              enumerate(['#EFE8DA', '#D9C9A6', '#E6DCC8', '#7A2A22', '#E9E3D3', '#2F3B33', '#C8A15A', '#F4F1EA',
                         '#CDBB98', '#F0EBE0'])]
    caps = [principled(bpy, 'cap-black', '#151413', rough=0.4), principled(bpy, 'cap-gold', '#B08A4E', rough=0.3, metal=1.0),
            principled(bpy, 'cap-wood', '#6A4A30', rough=0.6), principled(bpy, 'cap-silver', '#BFC1C2', rough=0.25, metal=1.0)]
    spirits = ['#C87A2A', '#B5651D', '#E8E4D8', '#F2EEE6', '#8E4A1A', '#D49A3A', '#5E7A3A', '#7A1E1A', '#E6D9B8']
    shelf_levels = [P.BASE_H + 0.03] + P.SHELVES_Z
    for li, z in enumerate(shelf_levels):
        working = li <= P.WORKING_SHELVES - 1
        for i in range(len(bays) - 1):
            a, b = bays[i] + 0.02, bays[i + 1] - 0.02
            if any(n0 - 0.03 < b and n1 + 0.03 > a and z < P.NICHE_Z0 + P.NICHE_H + 0.03 for n0, n1 in niches):
                spans = []
                for n0, n1 in niches:
                    if n0 < b and n1 > a:
                        spans = [(a, n0 - 0.03), (n1 + 0.03, b)]
            else:
                spans = [(a, b)]
            bay_col = P.PANELS[min(max(i - 1, 0), len(P.PANELS) - 1)] if 0 < i <= len(P.PANELS) else 'fog'
            if li > 0:
                sh = Mesh(f'shelf-{li}-{i}')
                for s0, s1 in spans:
                    if s1 - s0 > 0.1:
                        sh.box(s0, y0 + 0.04, z - P.SHELF_T, s1, D - 0.03, z)
                if working:
                    m = lit_acrylic(bpy, 'shelf-warm', '#FFE7C6', p.get('shelf_glow', 1.6), deep='#F4EFE6', rough=0.05)
                else:
                    c = P.COLOURS[bay_col] if bay_col not in ('fog', 'smoke') else '#E9ECEF'
                    m = lit_acrylic(bpy, f'shelf-{bay_col}', c, p.get('shelf_glow', 1.6) * 0.8, deep=c, rough=0.05)
                objs.append(sh.object(bpy, m))
            # the bottles on this level
            if z + 0.34 > P.SHELF_TOP_Z:
                continue
            for s0, s1 in spans:
                x = s0 + 0.05
                while x < s1 - 0.05:
                    k = rnd.choice(list(bodies))
                    body, label, cap, r = bodies[k]
                    if x + 2 * r > s1 - 0.02:
                        break
                    cx = x + r; cy = y0 + 0.10 + rnd.uniform(-0.01, 0.02) + (0.16 if rnd.random() < 0.35 else 0.0)
                    gcol = rnd.choice(spirits) if k != 'gin' else rnd.choice(['#EEF2EE', '#E2EEF0', '#F2EEE6'])
                    gm = glass_mat(gcol, k)
                    for me, mm in ((body, gm), (label, rnd.choice(labels)), (cap, rnd.choice(caps))):
                        ob = bpy.data.objects.new(f'{me.name}@{li}.{i}.{x:.2f}', me)
                        ob.location = (cx, cy, z); ob.rotation_euler.z = rnd.uniform(-0.5, 0.5) + math.pi * 1.5
                        bpy.context.scene.collection.objects.link(ob)
                        if not me.materials:
                            me.materials.append(mm)
                        ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = mm
                        objs.append(ob)
                    x += 2 * r + rnd.uniform(0.012, 0.04)


def booths(bpy, kit, p, objs):
    up = kit.material(bpy, 'velvet', p.get('booth_color', '#3B2A2A'), {'grain': 1.0})
    bench = Mesh('booth-benches'); tops = Mesh('booth-tables'); legs = Mesh('booth-legs')
    liner = Mesh('booth-liner')
    yW = 0.0
    for x0 in P.BOOTHS:
        x1 = x0 + P.BOOTH_LEN
        for side in (0, 1):
            bx0, bx1 = (x0, x0 + P.BENCH_D) if side == 0 else (x1 - P.BENCH_D, x1)
            yb0, yb1 = yW + 0.08, yW + P.BOOTH_DEPTH
            bench.box(bx0 + 0.02, yb0, 0.06, bx1 - 0.02, yb1, P.BENCH_SEAT - 0.08)               # the base
            bench.box(bx0, yb0, P.BENCH_SEAT - 0.08, bx1, yb1, P.BENCH_SEAT)                      # the seat cushion
            back = (bx0, bx0 + 0.16) if side == 1 else (bx1 - 0.16, bx1)
            back = (bx1 - 0.16, bx1) if side == 0 else (bx0, bx0 + 0.16)
            # the backs face the table
            bxb0, bxb1 = (bx0, bx0 + 0.16) if side == 0 else (bx1 - 0.16, bx1)
            bench.box(bxb0, yb0, P.BENCH_SEAT, bxb1, yb1, P.BENCH_BACK)
        # the table between, a Smoke acrylic top on a blackened steel pedestal
        tx0, tx1 = x0 + P.BENCH_D + 0.08, x1 - P.BENCH_D - 0.08
        tops.box(tx0, yW + 0.15, P.TABLE['h'] - 0.025, tx1, yW + 0.15 + P.TABLE['d'], P.TABLE['h'])
        cx, cy = (tx0 + tx1) / 2, yW + 0.15 + P.TABLE['d'] / 2
        _cyl(legs.bm, cx, cy, 0.0, 0.04, P.TABLE['h'] - 0.025, seg=20)
        legs.box(cx - 0.22, cy - 0.30, 0.0, cx + 0.22, cy + 0.30, 0.012)
    liner.box(P.BOOTHS[0] - 0.05, 0.0, 0.0, P.BOOTHS[-1] + P.BOOTH_LEN + 0.05, 0.08, P.WINDOW['sill'])
    objs.append(bench.object(bpy, up))
    objs.append(tops.object(bpy, principled(bpy, 'smoke-acrylic', '#0E0D10', rough=0.06, coat=1.0, coat_rough=0.03)))
    objs.append(legs.object(bpy, principled(bpy, 'blackened-steel', '#1C1B1A', rough=0.42, metal=0.85), smooth=True))
    objs.append(liner.object(bpy, principled(bpy, 'smoke-acrylic', '#0E0D10', rough=0.06, coat=1.0, coat_rough=0.03)))


def lounge(bpy, kit, p, objs):
    L, D = P.L, P.D
    # the screens: thermoformed Fog acrylic, frosted and micro-perforated, a gentle wave in plan
    scr = Mesh('screens')
    for ya, yb in ((0.0 + 1.75, P.SCREEN_OPEN[0]), (P.SCREEN_OPEN[1], D - 1.75)):
        n = 28
        for k in range(n):
            y1, y2 = ya + (yb - ya) * k / n, ya + (yb - ya) * (k + 1) / n
            dx1 = 0.06 * math.sin(2 * math.pi * k / n * 2); dx2 = 0.06 * math.sin(2 * math.pi * (k + 1) / n * 2)
            x = P.SCREEN_X
            scr.quad([(x + dx1, y1, 0.0), (x + dx2, y2, 0.0), (x + dx2, y2, P.SCREEN_H), (x + dx1, y1, P.SCREEN_H)])
    objs.append(scr.object(bpy, principled(bpy, 'fog-frosted', '#F2F3F2', rough=0.28, trans=0.95, ior=1.49), smooth=True))
    # the plinths (Smoke), one under each corner speaker
    pl = Mesh('plinths')
    for role, colour, x, y, z, rot in P.speakers():
        if role == 'backbar':
            continue
        a = math.radians(rot); w, d = P.PLINTH['w'] / 2, P.PLINTH['d'] / 2
        c, s = math.cos(a), math.sin(a)
        corners = [(x + c * u - s * v, y + s * u + c * v) for u, v in ((-w, -d), (w, -d), (w, d), (-w, d))]
        bm = pl.bm
        vb = [bm.verts.new((cx, cy, 0.0)) for cx, cy in corners]
        vt = [bm.verts.new((cx, cy, P.PLINTH['h'])) for cx, cy in corners]
        for f in ([vb[3], vb[2], vb[1], vb[0]], vt, *[[vb[i], vb[(i + 1) % 4], vt[(i + 1) % 4], vt[i]] for i in range(4)]):
            fa = bm.faces.new(f); fa.normal_update()
    objs.append(pl.object(bpy, principled(bpy, 'smoke-acrylic', '#0E0D10', rough=0.06, coat=1.0, coat_rough=0.03)))
    # the street wall: dark absorber, tinted Haze slats 75 mm in front of it, lit in the gap from below
    S = P.SLATS
    ab = Mesh('absorber'); ab.box(S['x0'] - 0.05, 0.0, 0.0, S['x1'] + 0.05, P.ABSORBER_T, P.MEMBRANE)
    ab.box(P.SCREEN_X + 0.4, D - P.ABSORBER_T, 0.0, L - 1.4, D, P.MEMBRANE)                    # the plain absorber opposite
    objs.append(ab.object(bpy, kit.material(bpy, 'felt', p.get('absorber', '#1B1A1F'))))
    sl = Mesh('slats'); yf = P.ABSORBER_T + S['gap']
    x = S['x0']
    while x + S['w'] <= S['x1']:
        sl.box(x, yf, S['z0'], x + S['w'], yf + S['t'], S['z1']); x += S['pitch']
    c = P.COLOURS[S['colour']]
    objs.append(sl.object(bpy, lit_acrylic(bpy, 'slat-acrylic', c, p.get('slat_glow', 0.25), deep=c, rough=0.05)))
    led = Mesh('slat-led')
    led.box(S['x0'], P.ABSORBER_T + 0.005, S['z0'] - 0.02, S['x1'], yf - 0.005, S['z0'] - 0.012)
    led.box(S['x0'], P.ABSORBER_T + 0.005, S['z1'] + 0.012, S['x1'], yf - 0.005, S['z1'] + 0.02)
    objs.append(led.object(bpy, emitter(bpy, 'slat-led', c, p.get('slat_led', 12.0))))
    # a wool rug under the chairs, and three low side tables (Smoke acrylic drums)
    rug = Mesh('rug'); rug.box(12.55, 1.70, 0.0, 15.65, 7.45, 0.012)
    objs.append(rug.object(bpy, _pbr(bpy, kit, p.get('rug_tex', 'poly_wool_herringbone'), res='2k',
                                     tint=p.get('rug_tint', '#4A4038'), tint_mix=0.85, scale=0.3)))
    st = Mesh('side-tables')
    for x, y in P.SIDE_TABLES:
        _cyl(st.bm, x, y, 0.012, 0.22, 0.42, seg=40)
    objs.append(st.object(bpy, principled(bpy, 'smoke-acrylic', '#0E0D10', rough=0.06, coat=1.0, coat_rough=0.03),
                          smooth=True))


def record_wall(bpy, kit, p, objs):
    L, D = P.L, P.D
    rnd = random.Random(7)
    y0, y1, cell = P.REC_Y0, P.REC_Y1, P.REC_CELL
    ncols = int((y1 - y0) / cell); y0 = (y0 + y1) / 2 - ncols * cell / 2
    nrows = int((P.REC_Z1 - 0.05) / cell)
    boards = Mesh('record-boards'); sleeves = Mesh('sleeves'); glowing = Mesh('record-strip')
    pal = ['#1A1A1A', '#EDE7DA', '#C23B22', '#2B4C7E', '#E3B23C', '#5B7F4A', '#D8D2C4', '#3A2E2A', '#8A2D3B',
           '#F2EEE6', '#2F2F33', '#B88A5A', '#6D8FA6', '#E46A2E', '#9C9A93', '#141414', '#4E3B6A', '#C9C1AE']
    dj = P.DJ
    for ci in range(ncols):
        ya, yb = y0 + ci * cell, y0 + (ci + 1) * cell
        depth = rnd.choice([0.30, 0.36, 0.42, 0.48, 0.55])
        xf = L - depth
        boards.box(xf, ya, 0.0, L, ya + 0.018, P.REC_Z1)
        for ri in range(nrows + 1):
            z = 0.05 + ri * cell
            in_dj = dj['y0'] < (ya + yb) / 2 < dj['y1'] and z < dj['recess_z']
            if in_dj:
                continue
            boards.box(xf, ya, z - 0.018, L, yb, z)
            if ri == nrows:
                continue
            # the sleeves, spines out, leaning a little, a gap here and there
            s = ya + 0.02
            lean = rnd.uniform(-0.06, 0.06)
            while s < yb - 0.02:
                t = rnd.uniform(0.0025, 0.0045)
                if rnd.random() < 0.03:
                    s += rnd.uniform(0.02, 0.06); continue
                col = lin(rnd.choice(pal)) if rnd.random() < 0.7 else _mixhex(rnd.choice(pal), '#FFFFFF', rnd.random() * 0.5)
                h = 0.315 + rnd.uniform(-0.004, 0.003)
                sx = xf + 0.012 + rnd.uniform(0.0, 0.012)
                sleeves.box(sx, s, z, sx + 0.31, s + t, z + h, col=col)
                s += t + 0.0003
        boards.box(xf, yb - 0.018, 0.0, L, yb, P.REC_Z1)
        if ci == ncols - 1:
            pass
    boards.box(L - 0.02, y0, 0.0, L, y0 + ncols * cell, P.REC_Z1)                  # the back
    objs.append(boards.object(bpy, _pbr(bpy, kit, p.get('rec_wood', 'black_oak_veneer'), res='2k', tint='#2A221C',
                                        tint_mix=0.35)))
    objs.append(sleeves.object(bpy, colour_attr_mat(bpy, 'sleeve-card', rough=0.62)))
    # a picture light's strip along the top of the wall, hidden in the membrane's gap
    glowing.box(L - 0.62, y0, P.REC_Z1 - 0.012, L - 0.58, y0 + ncols * cell, P.REC_Z1 - 0.004)
    objs.append(glowing.object(bpy, emitter(bpy, 'record-strip', '#FFE2BA', p.get('record_glow', 0.0))))
    # the DJ desk: a massive block clad in Smoke, set into the wall's recess
    desk = Mesh('dj-desk')
    desk.box(L - dj['desk_d'], dj['y0'], 0.0, L, dj['y1'], dj['desk_z'])
    objs.append(desk.object(bpy, principled(bpy, 'smoke-acrylic', '#0E0D10', rough=0.06, coat=1.0, coat_rough=0.03)))
    # the recess's back: Ice acrylic, back-lit, so Cumulus and the DJ stand in silhouette against it
    bkl = Mesh('dj-backlight'); bkl.box(L - 0.03, dj['y0'], dj['desk_z'], L - 0.01, dj['y1'], dj['recess_z'])
    objs.append(bkl.object(bpy, lit_acrylic(bpy, 'dj-acrylic', p.get('dj_color', P.COLOURS['ice']), p.get('dj_glow', 0.6),
                                            deep=P.COLOURS['ice'], rough=0.08)))
    rec = Mesh('dj-recess')
    rec.box(L - dj['desk_d'] - 0.02, dj['y0'], dj['recess_z'], L, dj['y1'], dj['recess_z'] + 0.04)
    objs.append(rec.object(bpy, kit.material(bpy, 'felt', '#1B1A1F')))
    # a rotary mixer beside Cumulus (aluminium, its knobs)
    mx = Mesh('mixer'); mxc = L - 0.36; myc = dj['y1'] - 0.38
    mx.box(mxc - 0.16, myc - 0.2, dj['desk_z'], mxc + 0.16, myc + 0.2, dj['desk_z'] + 0.09)
    objs.append(mx.object(bpy, principled(bpy, 'mixer-alu', '#A9A9A6', rough=0.35, metal=1.0)))
    kn = Mesh('mixer-knobs')
    for i in range(4):
        for j in range(3):
            _cyl(kn.bm, mxc - 0.1 + j * 0.1, myc - 0.15 + i * 0.1, dj['desk_z'] + 0.09, 0.016, 0.02, seg=16)
    objs.append(kn.object(bpy, principled(bpy, 'knob', '#1A1A1A', rough=0.4), smooth=True))


def street(bpy, kit, p, objs):
    """Outside: the long street's sidewalk and road (y < 0), the side street (x < 0), the building's facade and flats
    above, and the block across the street."""
    L, D, T = P.L, P.D, P.WALL_T
    sw = Mesh('sidewalk'); sw.box(-12.0, -3.9, -0.2, L + 12.0, -T, 0.0); sw.box(-3.9, -3.9, -0.2, -T, D + 12.0, 0.0)
    objs.append(sw.object(bpy, _pbr(bpy, kit, 'concrete_pavement', res='2k', tint='#77746F', tint_mix=0.3)))
    curb = Mesh('curb'); curb.box(-12.0, -4.05, -0.2, L + 12.0, -3.9, 0.0); curb.box(-4.05, -4.05, -0.2, -3.9, D + 12.0, 0.0)
    objs.append(curb.object(bpy, principled(bpy, 'curb', '#8A8781', rough=0.8)))
    rd = Mesh('road'); rd.box(-40.0, -16.0, -0.35, L + 40.0, -4.05, -0.15); rd.box(-16.0, -16.0, -0.35, -4.05, D + 40.0, -0.15)
    objs.append(rd.object(bpy, _pbr(bpy, kit, 'asphalt_02', res='2k', tint='#3A3A3C', tint_mix=0.4, rough_mul=0.7)))
    across = Mesh('sidewalk-across'); across.box(-40.0, -20.0, -0.2, L + 40.0, -16.0, 0.0)
    objs.append(across.object(bpy, _pbr(bpy, kit, 'concrete_pavement', res='2k', tint='#77746F', tint_mix=0.3)))
    # the building: a three-storey corner building, stucco, the shop below; the flats' windows
    fac = Mesh('facade')
    H0, H1 = P.SLAB + 0.25, 12.5
    fac.box(-T, -T, H0, L + T, D + T, H1)                              # the floors above (a solid block)
    fac.box(-T - 0.02, -T - 0.02, H0 - 0.35, L + T + 0.02, -T + 0.15, H0 + 0.15)   # a cornice over the shop
    fac.box(-T - 0.02, -T - 0.02, H0 - 0.35, -T + 0.15, D + T, H0 + 0.15)
    objs.append(fac.object(bpy, _pbr(bpy, kit, 'white_stucco', res='2k', tint='#7D8580', tint_mix=0.55)))
    # the shop's own face below the cornice: painted smoke black, a skin over the shell's solid parts
    skin = Mesh('shopskin'); W, Dr = P.WINDOW, P.DOOR
    skin.box(-T - 0.005, -T - 0.005, 0.0, W['x0'], -T, H0 - 0.35)
    skin.box(W['x1'], -T - 0.005, 0.0, L + T, -T, H0 - 0.35)
    skin.box(W['x0'], -T - 0.005, 0.0, W['x1'], -T, W['sill'])
    skin.box(W['x0'], -T - 0.005, W['head'], W['x1'], -T, H0 - 0.35)
    skin.box(-T - 0.005, -T, 0.0, -T, Dr['y0'], H0 - 0.35)
    skin.box(-T - 0.005, Dr['y1'], 0.0, -T, D + T, H0 - 0.35)
    skin.box(-T - 0.005, Dr['y0'], Dr['h'], -T, Dr['y1'], H0 - 0.35)
    objs.append(skin.object(bpy, principled(bpy, 'shop-paint', '#1E1E20', rough=0.55)))
    # the flats' windows: recessed dark glass with a frame; some lit warm behind blinds
    rnd = random.Random(5)
    wins_dark = Mesh('flat-windows'); wins_lit = Mesh('flat-windows-lit'); frames = Mesh('flat-frames')
    lit_share = p.get('windows_lit', 0.35)
    for storey in (0, 1):
        z0 = H0 + 1.0 + storey * 3.6
        for xw in [1.2 + 2.3 * k for k in range(8)]:
            (wins_lit if rnd.random() < lit_share else wins_dark).box(xw, -T - 0.02, z0, xw + 1.2, -T - 0.01, z0 + 1.9)
            frames.box(xw - 0.08, -T - 0.08, z0 - 0.12, xw + 1.28, -T - 0.02, z0)
        for yw in [1.5 + 2.4 * k for k in range(3)]:
            (wins_lit if rnd.random() < lit_share else wins_dark).box(-T - 0.02, yw, z0, -T - 0.01, yw + 1.2, z0 + 1.9)
    objs.append(wins_dark.object(bpy, principled(bpy, 'dark-glass', '#0A0B0D', rough=0.03, spec=0.6)))
    objs.append(wins_lit.object(bpy, emitter(bpy, 'lit-blind', '#FFC98A', p.get('flat_glow', 0.6))))
    objs.append(frames.object(bpy, principled(bpy, 'sill-paint', '#D8D4CA', rough=0.6)))
    # the block across the long street: a row of storefronts and flats, some windows lit
    acr = Mesh('across'); acr_w = Mesh('across-lit'); acr_d = Mesh('across-dark')
    xb = -30.0
    while xb < L + 30.0:
        w = rnd.uniform(7.0, 11.0); h = rnd.uniform(9.0, 14.0)
        acr.box(xb, -32.0, 0.0, xb + w - 0.15, -20.0, h)
        for storey in range(int((h - 4.0) / 3.4)):
            z0 = 4.6 + storey * 3.4
            for k in range(int((w - 1) / 2.2)):
                xw = xb + 0.8 + k * 2.2
                (acr_w if rnd.random() < lit_share * 0.8 else acr_d).box(xw, -20.02, z0, xw + 1.1, -20.0, z0 + 1.8)
        (acr_w if rnd.random() < 0.6 else acr_d).box(xb + 0.6, -20.02, 0.4, xb + w - 0.8, -20.0, 3.2)
        xb += w
    objs.append(acr.object(bpy, _pbr(bpy, kit, 'white_stucco_02', res='1k', tint='#8C8780', tint_mix=0.5)))
    objs.append(acr_w.object(bpy, emitter(bpy, 'across-lit', '#FFCB90', p.get('across_glow', 0.8))))
    objs.append(acr_d.object(bpy, principled(bpy, 'dark-glass', '#0A0B0D', rough=0.03, spec=0.6)))
    # the small neon EARF sign over the door: four letters as glowing tubes on a bracket (a stand-in for the
    # wordmark's own tubes)
    neon = Mesh('neon'); N = P.NEON
    w = N['w']; h = 0.14; x = -T - 0.06
    lw = w / 4
    for i in range(4):
        y0 = N['y'] - w / 2 + i * lw + 0.02; y1 = y0 + lw - 0.04
        z0, z1 = N['z'] - h / 2, N['z'] + h / 2
        t = 0.008
        neon.box(x - t, y0, z0, x + t, y0 + 2 * t, z1)                    # the stems of E, A, R, F, simplified
        if i in (0, 3):
            neon.box(x - t, y0, z1 - 2 * t, x + t, y1, z1); neon.box(x - t, y0, (z0 + z1) / 2 - t, x + t, y1 - 0.02, (z0 + z1) / 2 + t)
            if i == 0:
                neon.box(x - t, y0, z0, x + t, y1, z0 + 2 * t)
        if i == 1:
            neon.box(x - t, y1 - 2 * t, z0, x + t, y1, z1); neon.box(x - t, y0, z1 - 2 * t, x + t, y1, z1)
            neon.box(x - t, y0, (z0 + z1) / 2 - t, x + t, y1, (z0 + z1) / 2 + t)
        if i == 2:
            neon.box(x - t, y0, z1 - 2 * t, x + t, y1, z1); neon.box(x - t, y1 - 2 * t, (z0 + z1) / 2, x + t, y1, z1)
            neon.box(x - t, y0, (z0 + z1) / 2 - t, x + t, y1, (z0 + z1) / 2 + t)
            neon.box(x - t, y1 - 2 * t, z0, x + t, y1, (z0 + z1) / 2)
    objs.append(neon.object(bpy, emitter(bpy, 'neon', p.get('neon_color', '#FF5A3C'), p.get('neon', 18.0))))


def room(bpy, name, p, kit):
    objs = []
    shell(bpy, kit, p, objs)
    ceiling(bpy, kit, p, objs)
    window_and_door(bpy, kit, p, objs)
    bar(bpy, kit, p, objs)
    backbar(bpy, kit, p, objs)
    booths(bpy, kit, p, objs)
    lounge(bpy, kit, p, objs)
    record_wall(bpy, kit, p, objs)
    if p.get('street', True):
        street(bpy, kit, p, objs)
    return objs
