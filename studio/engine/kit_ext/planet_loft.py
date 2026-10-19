"""Planet EARF, round 34 (the loft): the den's room in the owner's new palette, as one kit `ext` piece.

    {"kind": "kit", "shape": "ext", "module": "planet_loft", "fn": "room", ...}

The owner, 2026-10-19: lots of cement, wood beams, steel and iron, and a lot of acrylic, but not rainbow and not cheap;
screens behind large acrylic panels showing "suggestive hands pressed up against fogged glass, the fogged silhouette
of a woman dancing, alien/foreign objects like the movie arrival"; dimly lit, but not hard to see.

The footprint and the den's builders stay (planet_den.py); this module swaps their materials and adds what is new:

- the shell: board-formed concrete walls (tie holes, pour panels), a polished concrete floor, Douglas fir beams across
  the room under a fir plank deck;
- the screens: in reveals cut into the concrete, a 30 mm frosted acrylic panel flush with the wall face and, 100 mm
  behind it, a glowing image plane (screens.py's images), so the diffusion is the panel's own; a blackened-steel angle
  round each reveal; and a lightbox of two frosted panels in the shopfront window, the dancer between them;
- the bar: a fluted concrete front on a blackened-steel kick, a fir top with a clear acrylic band inlaid along its front
  edge, lit from within; the back-bar in blackened steel against the concrete, clear acrylic shelves with polished,
  edge-lit fronts, two steel-lined niches with frosted backs for the Fog pair;
- frosted acrylic pendants; a smoked acrylic partition at the listening room; fir for the joinery, dark leather;
- the shopfront in blackened steel, the name frosted into the glass.

Acrylic only clear, frosted or smoked: the one speaker in each frame is the only colour.
"""
import math, os, random, sys

import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'loft'))
sys.path.insert(0, HERE)
import loft_plan as LP                                               # noqa: E402
import planet_den as D                                               # noqa: E402
import screens as SC                                                 # noqa: E402

R = D.R
lin, principled, emitter, Mesh, _cyl, _lathe = R.lin, R.principled, R.emitter, R.Mesh, R._cyl, R._lathe
_M = R._M
P = D.P                                                              # the den's plan (the footprint)


# --- materials ---------------------------------------------------------------------------------------------------
def concrete(bpy, p, name='concrete-wall'):
    """Board-formed concrete: the scan's tie holes and pour panels, warmed a little, a fine roughness."""
    if name not in _M:
        m = D._pbr(bpy, p.get('concrete_tex', 'concrete_wall_008'), tint=p.get('concrete_tint', '#8C857C'),
                   tint_mix=p.get('concrete_mix', 0.35), rough_mul=1.05, bump=1.4, res='2k')
        _M[name] = m
    return _M[name]


def floor_mat(bpy, p):
    """Polished concrete: a trowelled scan under a sealer whose sheen is worn unevenly."""
    if 'floor-polished' in _M:
        return _M['floor-polished']
    m = D._pbr(bpy, 'acg:' + p.get('floor_acg', 'Concrete044A'), tint=p.get('floor_tint', '#5E5852'),
               tint_mix=p.get('floor_mix', 0.35), scale=2.4, res='2K')
    b = D._bsdf(m); R._set(b, 'Coat Weight', p.get('floor_coat', 0.6))
    nt = m.node_tree; tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 0.7; nz.inputs['Detail'].default_value = 10.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeMapRange'); cr.inputs['To Min'].default_value = 0.08; cr.inputs['To Max'].default_value = 0.35
    nt.links.new(nz.outputs['Fac'], cr.inputs['Value']); nt.links.new(cr.outputs['Result'], b.inputs['Coat Roughness'])
    _M['floor-polished'] = m
    return m


def fir(bpy, vertical=False, coat=0.0, coat_rough=0.4, tint=None, mix=None, name=''):
    """Reclaimed Douglas fir, oiled: a weathered plank scan warmed toward honey; `vertical` runs the grain up."""
    key = f'fir-{vertical}-{tint}-{mix}'
    if key not in _M:
        m = D._pbr(bpy, 'brown_planks_09', rot=(0, 90, 0) if vertical else None, tint=tint or '#8A5A34',
                   tint_mix=mix if mix is not None else 0.4, scale=1.0, res='2k')
        b = D._bsdf(m); R._set(b, 'Coat Weight', 0.25); R._set(b, 'Coat Roughness', 0.45)
        _M[key] = m
    return _M[key]


def steel(bpy, aged=True):
    """Blackened steel: a dark plate scan, metallic, its sheen uneven, a brownish patina."""
    if 'steel-black' not in _M:
        m = D._pbr(bpy, 'metal_plate_02', tint='#25221F', tint_mix=0.55, rough_mul=0.8, res='2k')
        b = D._bsdf(m); R._set(b, 'Metallic', 0.75)
        _M['steel-black'] = m
    return _M['steel-black']


def dark_leather(bpy, colour='#2E2420', name='leather-dark'):
    return D.leather(bpy, colour, name) if False else _leather(bpy, colour, name)


def _leather(bpy, colour, name):
    if name not in _M:
        m = D._pbr(bpy, 'brown_leather', tint=colour, tint_mix=0.55, scale=0.5, res='2k')
        b = D._bsdf(m); R._set(b, 'Coat Weight', 0.2); R._set(b, 'Coat Roughness', 0.4); R._set(b, 'Sheen Weight', 0.1)
        _M[name] = m
    return _M[name]


def wool(bpy, colour='#3A3734', name='wool-charcoal'):
    if name not in _M:
        m = D._pbr(bpy, 'velour_velvet', tint=colour, tint_mix=0.9, scale=0.25, res='2k')
        b = D._bsdf(m); R._set(b, 'Sheen Weight', 0.5); R._set(b, 'Specular IOR Level', 0.2)
        _M[name] = m
    return _M[name]


def acrylic(bpy, kind='clear', name=None, glow=0.0, glow_col='#FFC890'):
    """Thick cast acrylic, neutral: 'clear' (water-clear, polished), 'frosted' (rough transmission: what is behind it
    diffuses, as through a sanded panel) or 'smoked' (a grey-brown tint in the mass). A faint volume absorption gives
    thick sections their depth; `glow` lights it from within (an edge-lit band)."""
    name = name or f'acrylic-{kind}-{glow}'
    if name in _M:
        return _M[name]
    col = {'clear': '#FBFCFB', 'frosted': '#F4F2EE', 'smoked': '#5A534D'}[kind]
    rough = {'clear': 0.0, 'frosted': 0.42, 'smoked': 0.03}[kind]
    m = principled(bpy, name, col, rough=rough, trans=1.0, ior=1.49, emit=glow_col if glow else None, strength=glow)
    nt = m.node_tree; out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    va = nt.nodes.new('ShaderNodeVolumeAbsorption')
    va.inputs['Color'].default_value = lin({'clear': '#E9F2EE', 'frosted': '#EEEAE2', 'smoked': '#6E655C'}[kind])
    va.inputs['Density'].default_value = {'clear': 0.6, 'frosted': 1.5, 'smoked': 9.0}[kind]
    nt.links.new(va.outputs['Volume'], out.inputs['Volume'])
    _M[name] = m
    return m


def image_mat(bpy, img, strength, tint='#FFBE84'):
    """A glowing image plane (a screen): the picture's light, warm-neutral, both faces."""
    key = f'screen-{img}-{strength}'
    if key in _M:
        return _M[key]
    path = SC.make()[img]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    tc = nt.nodes.new('ShaderNodeTexCoord'); tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = bpy.data.images.load(path, check_existing=True); tx.extension = 'EXTEND'
    nt.links.new(tc.outputs['UV'], tx.inputs['Vector'])
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0; mul.inputs['B'].default_value = lin(tint)
    nt.links.new(tx.outputs['Color'], mul.inputs['A'])
    nt.links.new(mul.outputs['Result'], em.inputs['Color']); em.inputs['Strength'].default_value = strength
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    _M[key] = m
    return m


def _quad_uv(bpy, name, pts, mat):
    """One quad with UVs 0..1 (pts in order: u0v0, u1v0, u1v1, u0v1)."""
    bm = bmesh.new(); vs = [bm.verts.new(p) for p in pts]; f = bm.faces.new(vs); f.normal_update()
    uv = bm.loops.layers.uv.verify()
    for lp, c in zip(f.loops, [(0, 0), (1, 0), (1, 1), (0, 1)]):
        lp[uv].uv = c
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return ob


# --- the shell ----------------------------------------------------------------------------------------------------
def _wall(m, a0, a1, z0, z1, holes, box):
    """A wall's boxes over a0..a1 x z0..z1 with rectangular holes (a, b, zz0, zz1) left out; `box(a, b, za, zb)`."""
    cuts = sorted(holes)
    # columns between the holes, full height; then above and below each hole
    cur = a0
    for a, b, h0, h1 in cuts:
        if a > cur:
            box(cur, a, z0, z1)
        box(a, b, z0, h0); box(a, b, h1, z1)
        cur = b
    if cur < a1:
        box(cur, a1, z0, z1)


def shell(bpy, kit, p, objs):
    W, L, H, T = P.W, P.L, P.CEIL, P.WALL_T
    fl = Mesh('floor'); fl.box(0.0, 0.0, -0.1, L, W, 0.0)
    objs.append(fl.object(bpy, floor_mat(bpy, p)))
    cw = Mesh('concrete-walls')
    holes = {'right': [], 'left': []}
    for nm, wall, a0, a1, z0, z1, img in LP.SCREENS:
        if wall in holes:
            holes[wall].append((a0, a1, z0, z1))
    _wall(cw, 0.0, L, 0.0, H, holes['right'], lambda a, b, za, zb: cw.box(a, -T, za, b, 0.0, zb))
    _wall(cw, 0.0, L, 0.0, H, holes['left'], lambda a, b, za, zb: cw.box(a, W, za, b, W + T, zb))
    cw.box(L, -T, 0.0, L + T, W + T, H)                                       # the back wall
    objs.append(cw.object(bpy, concrete(bpy, p)))
    # the ceiling: a fir plank deck, and the beams across the room under it
    dk = Mesh('ceiling-deck'); dk.box(-0.2, -T, H, L + T, W + T, H + 0.05)
    objs.append(dk.object(bpy, fir(bpy, tint='#5A3C26', mix=0.45)))
    bm_ = Mesh('beams')
    for x in LP.BEAMS_X:
        if x < L - 0.1:
            bm_.box(x - LP.BEAM['w'] / 2, 0.0, H - LP.BEAM['d'], x + LP.BEAM['w'] / 2, W, H)
    objs.append(bm_.object(bpy, fir(bpy), bevel=0.006))


def screens(bpy, kit, p, objs):
    """Each screen: a 30 mm frosted panel flush with the wall, a glowing image 100 mm behind it, a dark box behind
    that, a blackened-steel angle round the reveal."""
    W = P.W; T = LP.SCREEN_T; G = LP.SCREEN_GAP; F = LP.SCREEN_FRAME
    fro = acrylic(bpy, 'frosted', 'screen-frosted')
    pan = Mesh('screen-panels'); box = Mesh('screen-boxes'); frm = Mesh('screen-frames')
    for nm, wall, a0, a1, z0, z1, img in LP.SCREENS:
        st = p.get('screen_glow', 1.5) * p.get(f'screen_{nm}', 1.0)
        if wall in ('right', 'left'):
            s = 1 if wall == 'right' else -1                          # the room's side is +y off the right wall
            yf = 0.0 if wall == 'right' else W                        # the wall's face
            pan.box(a0, yf - s * T, z0, a1, yf, z1)
            yi = yf - s * (T + G)
            pts = [(a0, yi, z0), (a1, yi, z0), (a1, yi, z1), (a0, yi, z1)]
            if wall == 'left':
                pts = [(a1, yi, z0), (a0, yi, z0), (a0, yi, z1), (a1, yi, z1)]
            objs.append(_quad_uv(bpy, f'screen-{nm}', pts, image_mat(bpy, img, st)))
            box.box(a0, yi - s * 0.02, z0, a1, yi - s * 0.01, z1)
            for (xa, xb, za, zb) in ((a0 - F, a1 + F, z0 - F, z0), (a0 - F, a1 + F, z1, z1 + F), (a0 - F, a0, z0, z1),
                                     (a1, a1 + F, z0, z1)):
                frm.box(xa, yf, za, xb, yf + s * 0.006, zb)
        else:                                                         # the window's lightbox, two-faced
            B = LP.WINDOW_BOX; x0, x1 = B['x0'], B['x0'] + B['depth']
            pan.box(x0, a0, z0, x0 + T, a1, z1); pan.box(x1 - T, a0, z0, x1, a1, z1)
            xm = (x0 + x1) / 2
            for face, pts in (('street', [(xm - 0.001, a1, z0), (xm - 0.001, a0, z0), (xm - 0.001, a0, z1), (xm - 0.001, a1, z1)]),
                              ('room', [(xm + 0.001, a0, z0), (xm + 0.001, a1, z0), (xm + 0.001, a1, z1), (xm + 0.001, a0, z1)])):
                objs.append(_quad_uv(bpy, f'screen-{nm}-{face}', pts, image_mat(bpy, img, st)))
            for (ya, yb, za, zb) in ((a0 - F, a1 + F, z0 - F, z0), (a0 - F, a1 + F, z1, z1 + F), (a0 - F, a0, z0, z1),
                                     (a1, a1 + F, z0, z1)):
                frm.box(x0 - 0.005, ya, za, x1 + 0.005, yb, zb)
    objs.append(pan.object(bpy, fro))
    objs.append(box.object(bpy, principled(bpy, 'screen-back', '#0A0A0A', rough=0.9)))
    objs.append(frm.object(bpy, steel(bpy)))


# --- the bar ------------------------------------------------------------------------------------------------------
def bar(bpy, kit, p, objs):
    """The den's bar with a fluted concrete front and body, a fir top, a steel kick and footrail, and a clear acrylic
    band inlaid along the top's front edge, lit from within."""
    def wal(bpy, vertical=False, **k):
        return concrete(bpy, p, 'concrete-bar') if vertical else fir(bpy)
    with _patched(walnut=wal, brass=lambda bpy, aged=True: steel(bpy), leather=lambda bpy, *a, **k: dark_leather(bpy)):
        D.bar(bpy, kit, p, objs)
    yF, zt = P.BAR_FRONT, P.BAR_TOP_Z
    il = Mesh('bar-inlay'); y0 = yF - P.TOP_OVER + LP.INLAY['set']
    il.box(P.BAR_X0 - 0.06, y0, zt + P.TOP_T - 0.03, P.BAR_X1 + 0.06, y0 + LP.INLAY['w'], zt + P.TOP_T + 0.0008)
    objs.append(il.object(bpy, acrylic(bpy, 'clear', 'inlay-lit', glow=p.get('inlay_glow', 0.6)), bevel=0.002))


def backbar(bpy, kit, p, objs):
    """Blackened steel against the concrete: a steel base with a fir counter, steel uprights and cornice, clear
    acrylic shelves with polished, edge-lit fronts, two steel-lined niches with frosted, softly lit backs."""
    W, y0 = P.W, P.BACKBAR_Y
    x0, x1 = P.BAR_X0 - 0.30, P.BAR_X1 + 0.30
    niches = [(nx, nx + nw) for nx, nw in P.NICHES]

    def runs(a, b, gap=0.04):
        out, cur = [], a
        for n0, n1 in niches:
            out.append((cur, n0 - gap)); cur = n1 + gap
        out.append((cur, b))
        return out
    base = Mesh('backbar-base'); tops = Mesh('backbar-top'); up = Mesh('backbar-steel')
    for a, b in runs(x0, x1):
        base.box(a, y0 + 0.02, 0.0, b, W, P.BASE_H)
        tops.box(a - 0.01, y0 - 0.03, P.BASE_H, b + 0.01, W, P.BASE_H + 0.05)
    objs.append(base.object(bpy, steel(bpy), bevel=0.002))
    objs.append(tops.object(bpy, fir(bpy), bevel=0.004))
    bays = [x0]
    for a, b in runs(x0, x1):
        nb = max(1, round((b - a) / 1.1))
        bays += [a + (b - a) * k / nb for k in range(1, nb)] + [b]
    for xb in bays:
        up.box(xb - 0.012, y0 + 0.05, P.BASE_H + 0.05, xb + 0.012, W - 0.01, P.BACKBAR_TOP)
    for n0, n1 in niches:                                              # the niches: steel-lined
        for xa in (n0 - 0.03, n1):
            up.box(xa, y0, 0.0, xa + 0.03, W, P.BACKBAR_TOP)
        up.box(n0 - 0.03, y0, P.NICHE_Z0 + P.NICHE_H, n1 + 0.03, W, P.NICHE_Z0 + P.NICHE_H + 0.03)
        up.box(n0, y0, 0.0, n1, W, P.NICHE_Z0)
    up.box(x0 - 0.02, y0 - 0.02, P.BACKBAR_TOP, x1 + 0.02, W, P.BACKBAR_TOP + 0.08)       # the cornice, a steel channel
    objs.append(up.object(bpy, steel(bpy), bevel=0.0015))
    # the niches' backs: frosted acrylic over a soft glow
    nb_ = Mesh('niche-frost'); ng = Mesh('niche-glow')
    for n0, n1 in niches:
        nb_.box(n0, W - 0.045, P.NICHE_Z0, n1, W - 0.015, P.NICHE_Z0 + P.NICHE_H)
        ng.box(n0 + 0.01, W - 0.008, P.NICHE_Z0 + 0.01, n1 - 0.01, W - 0.004, P.NICHE_Z0 + P.NICHE_H - 0.01)
    objs.append(nb_.object(bpy, acrylic(bpy, 'frosted', 'niche-frosted')))
    objs.append(ng.object(bpy, emitter(bpy, 'niche-glow', '#FFB474', p.get('niche_glow', 0.6))))
    # the shelves: 25 mm clear acrylic, their polished fronts edge-lit (a warm line in the edge)
    sh = Mesh('backbar-shelves'); ed = Mesh('backbar-shelf-edges')
    T = LP.ACRYLIC_SHELF_T
    for z in P.SHELVES_Z:
        for a, b in runs(x0, x1):
            sh.box(a + 0.015, y0 + 0.06, z - T, b - 0.015, W - 0.01, z)
            ed.box(a + 0.015, y0 + 0.058, z - T + 0.004, b - 0.015, y0 + 0.0605, z - 0.004)
    objs.append(sh.object(bpy, acrylic(bpy, 'clear', 'shelf-clear'), bevel=0.002))
    objs.append(ed.object(bpy, emitter(bpy, 'shelf-edge', p.get('shelf_color', '#FFB878'), p.get('shelf_glow', 4.0))))
    _bottles(bpy, p, objs, runs(x0, x1))


def _bottles(bpy, p, objs, runs):
    W = P.W; rnd = random.Random(34)
    bodies = R._bottle_meshes(bpy)
    glass = {}
    spirits = ['#B5651D', '#C87A2A', '#8E4A1A', '#D49A3A', '#7A3A14', '#E8E4D8', '#5A2A12', '#A0521C', '#EEF0EC']
    labels = [R.label_mat(bpy, f'label-loft-{i}', c, rnd) for i, c in
              enumerate(['#EFE8DA', '#D9C9A6', '#E6DCC8', '#2A2420', '#E9E3D3', '#1F2A24', '#C8A15A', '#F4F1EA', '#3A3633'])]
    caps = [principled(bpy, 'cap-black', '#151413', rough=0.4), principled(bpy, 'cap-gold', '#B08A4E', rough=0.3, metal=1.0),
            principled(bpy, 'cap-wood', '#6A4A30', rough=0.6)]
    levels = [P.BASE_H + 0.05] + P.SHELVES_Z
    tops = P.SHELVES_Z + [P.BACKBAR_TOP]
    for li, z in enumerate(levels):
        free = tops[li] - LP.ACRYLIC_SHELF_T - z if li < len(P.SHELVES_Z) else P.BACKBAR_TOP - z
        for a, b in runs:
            x = a + 0.08
            while x < b - 0.08:
                k = rnd.choice(list(bodies)); body, label, cap, r = bodies[k]
                if x + 2 * r > b - 0.05:
                    break
                if rnd.random() < 0.16:
                    x += rnd.uniform(0.07, 0.16); continue
                sr, shz = rnd.uniform(0.92, 1.1), rnd.uniform(0.9, 1.1)
                if 0.36 * shz > free - 0.03:
                    shz = (free - 0.04) / 0.36
                cx = x + r * 1.1; cy = W - 0.14 - rnd.uniform(0.0, 0.02) - (0.13 if rnd.random() < 0.4 else 0.0)
                c = rnd.choice(spirits)
                if c not in glass:
                    glass[c] = principled(bpy, f'bottle-glass-loft-{c}', c, rough=0.02, trans=1.0, ior=1.45)
                rot = rnd.uniform(-0.4, 0.4) - math.pi * 0.15
                for me, mm in ((body, glass[c]), (label, rnd.choice(labels)), (cap, rnd.choice(caps))):
                    ob = bpy.data.objects.new(f'{me.name}@loft{li}.{x:.2f}', me)
                    ob.location = (cx, cy, z); ob.rotation_euler.z = rot; ob.scale = (sr, sr, shz)
                    bpy.context.scene.collection.objects.link(ob)
                    if not me.materials:
                        me.materials.append(mm)
                    ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = mm
                    objs.append(ob)
                x += 2.2 * r * sr + rnd.uniform(0.01, 0.03)


# --- small things -------------------------------------------------------------------------------------------------
def pendants(bpy, kit, p, objs):
    """Frosted acrylic cylinders over the bar: 180 mm across, 320 tall, 15 mm walls, a steel cap, a cloth cord; the
    lamp inside lights the tube from within."""
    tube = Mesh('pendant-tubes'); cap = Mesh('pendant-caps'); cord = Mesh('pendant-cords'); glow = Mesh('pendant-lamps')
    y = P.BAR_FRONT + 0.18; zr = P.PENDANT_RIM
    for x in P.PENDANTS:
        _lathe(tube.bm, [(0.075, 0.0), (0.09, 0.0), (0.09, 0.32), (0.075, 0.32)], seg=48, z0=zr, cx=x, cy=y)
        _cyl(cap.bm, x, y, zr + 0.32, 0.092, 0.02, seg=48)
        _cyl(cord.bm, x, y, zr + 0.34, 0.003, P.CEIL - LP.BEAM['d'] - zr - 0.34, seg=8)
        _cyl(glow.bm, x, y, zr + 0.18, 0.025, 0.06, seg=16)
    objs.append(tube.object(bpy, acrylic(bpy, 'frosted', 'pendant-frosted', glow=p.get('pendant_glow', 0.35)), smooth=True))
    objs.append(cap.object(bpy, steel(bpy), smooth=True))
    objs.append(cord.object(bpy, principled(bpy, 'cord', '#1A1612', rough=0.7), smooth=True))
    objs.append(glow.object(bpy, emitter(bpy, 'pendant-lamp', '#FFC27A', p.get('pendant_lamp', 4.0)), smooth=True))


def partition(bpy, kit, p, objs):
    """Two smoked acrylic panels in blackened-steel frames either side of the listening room's opening."""
    X0 = P.LOUNGE_X0 + 0.20; W = P.W; Pt = LP.PARTITION
    pa = Mesh('partition-acrylic'); fr = Mesh('partition-frames')
    for ya, yb in ((0.18, 0.18 + Pt['w']), (W - 0.18 - Pt['w'], W - 0.18)):
        pa.box(X0 - Pt['t'] / 2, ya + 0.03, 0.06, X0 + Pt['t'] / 2, yb - 0.03, Pt['z1'] - 0.03)
        for (a, b, za, zb) in ((ya, yb, 0.0, 0.06), (ya, yb, Pt['z1'] - 0.03, Pt['z1']), (ya, ya + 0.03, 0.0, Pt['z1']),
                               (yb - 0.03, yb, 0.0, Pt['z1'])):
            fr.box(X0 - 0.025, a, za, X0 + 0.025, b, zb)
    objs.append(pa.object(bpy, acrylic(bpy, 'smoked', 'partition-smoked'), bevel=0.003))
    objs.append(fr.object(bpy, steel(bpy)))


class _patched:
    """Swap the den's material functions (and plan values) while one of its builders runs."""

    def __init__(self, plan=None, **fns):
        self.fns = fns; self.plan = plan or {}; self.old = {}; self.oldp = {}

    def __enter__(self):
        for k, f in self.fns.items():
            self.old[k] = getattr(D, k); setattr(D, k, f)
        for k, v in self.plan.items():
            self.oldp[k] = getattr(P, k); setattr(P, k, v)

    def __exit__(self, *a):
        for k, f in self.old.items():
            setattr(D, k, f)
        for k, v in self.oldp.items():
            setattr(P, k, v)


def room(bpy, name, p, kit):
    objs = []
    p = {**p, 'lounge_slats': False}
    shell(bpy, kit, p, objs)
    screens(bpy, kit, p, objs)
    wood = dict(walnut=lambda bpy, vertical=False, **k: fir(bpy, vertical=vertical),
                brass=lambda bpy, aged=True: steel(bpy),
                leather=lambda bpy, *a, **k: dark_leather(bpy),
                velvet=lambda bpy, colour, name: wool(bpy),
                shade_mat=lambda bpy, p: acrylic(bpy, 'frosted', 'shade-frosted', glow=p.get('shade_glow', 0.4)),
                storefront_mat=lambda bpy, p: steel(bpy),
                sign_mat=lambda bpy, p: principled(bpy, 'frost-etch', '#E9E7E2', rough=0.7, spec=0.3,
                                                    emit='#FFF0DC', strength=p.get('etch_glow', 0.05)),
                _curtain=lambda *a, **k: None)
    with _patched(**wood):
        D.shopfront(bpy, kit, p, objs)
        bar(bpy, kit, p, objs)
        D.banquette(bpy, kit, p, objs)
        with _patched(plan={'SCONCES_RIGHT': LP.SCONCES_RIGHT, 'SCONCES_LEFT_LOUNGE': LP.SCONCES_LEFT_LOUNGE}):
            D.sconces(bpy, kit, p, objs)
        D.lounge(bpy, kit, p, objs)
        D.record_wall(bpy, kit, p, objs)
        if p.get('props', True):
            D.candles(bpy, kit, p, objs)
            D.glassware(bpy, kit, p, objs)
        if p.get('street', True):
            D.street(bpy, kit, p, objs)
    backbar(bpy, kit, p, objs)
    pendants(bpy, kit, p, objs)
    partition(bpy, kit, p, objs)
    return objs
