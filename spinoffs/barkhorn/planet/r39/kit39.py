"""Planet EARF, round 39: the pieces round 39 adds to round 38b's room, as kit `ext` pieces by path.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r39/kit39.py", "fn": "mother", ...}
    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r39/kit39.py", "fn": "life", ...}

- `mother`: Mother EARF, the brand's multicolour globe (round 33c on main: six slotted discs of tinted cast acrylic,
  the Poison meridian whole, Dust and Haze the side meridians, Ember, Ice and Acid the parallels at 40 N, the equator
  and 40 S, the axis leaning 23.4 degrees) made at architectural scale and hung over the listening room. 1.3 m across
  in 25 mm cast sheet, slotted round one another as the fab kit cuts them. The meridians are cut round an opal core
  (a 260 mm blown opal sphere with a lamp in it) so the core's light enters each meridian at its inner edge and comes
  out at the polished rim: the rims glow, the faces stay clear tints. The parallels do not reach the core and glow
  less (`rim_par`). It hangs on one black cable from a canopy on the deck.
- `life`: what a night leaves on the surfaces: rocks glasses with ice and a pour, a coupe just poured, a mixing glass
  with a bar spoon, an open bottle and its stopper, votives with a lit candle, a matchbook, napkins, a coat over a chair.
  Every list is in world metres; anything not listed is not built.
"""
import math, os, random, sys

import bmesh
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
KX = os.path.join(ROOT, 'studio', 'engine', 'kit_ext')
if KX not in sys.path:
    sys.path.insert(0, KX)
import planet_r37 as K37                                             # noqa: E402  (round 37's room, its helpers)

K = K37.K                                                            # planet_r36: materials and geometry helpers
LK = K.LK
MT = K.MT
_M = {}

# Mother EARF: the discs (main's globe_colour.DISCS), their tints after 25 mm (the cabinets' deep, lightened as main's
# 1 m piece is) and their rims' glow (companions/common.GLOW)
DISCS = [('m90', 'poison', 90.0), ('m150', 'dust', 150.0), ('m30', 'haze', 30.0),
         ('north', 'ember', 40.0), ('equator', 'ice', 0.0), ('south', 'acid', -40.0)]
DEEP = {'ember': '#E9867C', 'dust': '#EFA066', 'acid': '#EFCB57', 'poison': '#93B583', 'ice': '#8FC3E6', 'haze': '#AA92D6'}
GLOW = {'ember': '#FF4A3A', 'dust': '#FF8A3A', 'acid': '#FFC93A', 'poison': '#6BD45A', 'ice': '#4FB8FF', 'haze': '#9A6BFF'}
LEAN = 23.44


def _add_emission(bpy, base, name, colour, strength):
    """A copy of `base` with an emission added to its surface (a polished rim carrying light out of the sheet)."""
    if name in _M:
        return _M[name]
    m = base.copy(); m.name = name; nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    link = next(l for l in nt.links if l.to_node == out and l.to_socket.name == 'Surface')
    src = link.from_socket
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = LK.lin(colour); em.inputs['Strength'].default_value = strength
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.remove(link)
    nt.links.new(src, add.inputs[0]); nt.links.new(em.outputs[0], add.inputs[1]); nt.links.new(add.outputs[0], out.inputs['Surface'])
    _M[name] = m
    return m


def _annulus(bm, r_in, r_out, t, seg=144):
    """An annulus (or a disc when r_in is 0) in the XY plane, `t` thick about z = 0; faces: 0 the flats and the inner
    edge, 1 the outer rim."""
    def ring(r, z):
        return [bm.verts.new((r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)]
    ot, ob = ring(r_out, t / 2), ring(r_out, -t / 2)
    rim = []
    for i in range(seg):
        j = (i + 1) % seg
        rim.append(bm.faces.new([ob[i], ob[j], ot[j], ot[i]]))
    if r_in > 0:
        it, ib = ring(r_in, t / 2), ring(r_in, -t / 2)
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new([ot[i], ot[j], it[j], it[i]])
            bm.faces.new([ib[i], ib[j], ob[j], ob[i]])
            bm.faces.new([it[i], it[j], ib[j], ib[i]])
    else:
        bm.faces.new(ot); bm.faces.new(list(reversed(ob)))
    for f in rim:
        f.material_index = 1
    bm.normal_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


def _disc_matrix(kind, a, R):
    """The disc's placement in the globe's own frame (axis z): a meridian at longitude `a`, or a parallel at latitude `a`."""
    if kind == 'm':
        return Matrix.Rotation(math.radians(a - 90), 4, 'Z') @ Matrix.Rotation(math.radians(90), 4, 'X'), R
    z, r = R * math.sin(math.radians(a)), R * math.cos(math.radians(a))
    return Matrix.Translation((0, 0, z)), r


def mother(bpy, name, p, kit):
    """Mother EARF, hung: `centre` [x, y, z], `size` (m across), `t` (sheet), `core` (the opal's radius), `rim` (the
    meridians' rim glow), `rim_par` (the parallels'), `core_glow`, `core_w` (the lamp in it), `ceiling` (z of the canopy),
    `heading` (degrees: the side the axis leans toward)."""
    cx, cy, cz = p.get('centre', [11.12, 3.05, 2.76])
    R = p.get('size', 1.30) / 2; T = p.get('t', 0.025); rc = p.get('core', 0.13); gap = 0.0008
    W = (Matrix.Translation((cx, cy, cz)) @ Matrix.Rotation(math.radians(p.get('heading', 0.0)), 4, 'Z')
         @ Matrix.Rotation(math.radians(LEAN), 4, 'X'))
    objs, made = [], []
    for key, tint, a in DISCS:
        kind = 'm' if key.startswith('m') else 'p'
        M, r = _disc_matrix(kind, a, R)
        body = K.resin(bpy, DEEP[tint], f'mother-{tint}', radius=p.get('radius', 0.08), rough=0.02)
        glow = p.get('rim', 6.0) * (1.0 if kind == 'm' else p.get('rim_par', 0.45))
        rim = _add_emission(bpy, body, f'mother-rim-{tint}-{glow}', GLOW[tint], glow)
        # built in world coordinates (identity matrices), its materials in place before the slots are cut, so the
        # boolean keeps the rim's index
        bm = bmesh.new(); _annulus(bm, rc + 0.004 if kind == 'm' else 0.0, r, T)
        bmesh.ops.transform(bm, matrix=W @ M, verts=bm.verts[:])
        me = bpy.data.meshes.new(f'{name}-{key}'); bm.to_mesh(me); bm.free()
        me.materials.append(body); me.materials.append(rim)
        ob = bpy.data.objects.new(f'{name}-{key}', me); bpy.context.scene.collection.objects.link(ob)
        # slotted round every disc before it, as the fab kit cuts them (main's globe_mono.discs)
        for prev_M, prev_r in made:
            cb = bmesh.new(); _annulus(cb, 0.0, prev_r + 0.002, T + 2 * gap, seg=144)
            for f in cb.faces:
                f.material_index = 0
            bmesh.ops.transform(cb, matrix=W @ prev_M, verts=cb.verts[:])
            cme = bpy.data.meshes.new('cutter'); cb.to_mesh(cme); cb.free()
            cme.materials.append(body)
            cut = bpy.data.objects.new('cutter', cme); bpy.context.scene.collection.objects.link(cut)
            md = ob.modifiers.new('slot', 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.object = cut; md.solver = 'EXACT'
            if hasattr(md, 'material_mode'):
                md.material_mode = 'INDEX'
            dg = bpy.context.evaluated_depsgraph_get(); dg.update()
            new = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
            ob.modifiers.remove(md); old = ob.data; ob.data = new; bpy.data.meshes.remove(old)
            bpy.data.objects.remove(cut); bpy.data.meshes.remove(cme)
        made.append((M, r))
        if len(ob.data.materials) < 2:
            ob.data.materials.clear(); ob.data.materials.append(body); ob.data.materials.append(rim)
        for f in ob.data.polygons:
            f.use_smooth = False
        objs.append(ob)
    # the opal core and its lamp (hidden from the camera, from glossy rays and from transmission: Planet's rule)
    co = K.Mesh(f'{name}-core'); bmesh.ops.create_uvsphere(co.bm, u_segments=64, v_segments=32, radius=rc)
    bmesh.ops.translate(co.bm, verts=co.bm.verts[:], vec=(cx, cy, cz))
    opal = MT.make(bpy, 'mother-opal', 'frosted', {'color': '#F6F2EA', 'absorb': '#F2E8D8', 'roughness': 0.6, 'radius': 0.03,
                                                   'clear': 0.05, 'glow': p.get('core_glow', 1.2), 'glow_color': '#FFC890'})
    objs.append(co.object(bpy, opal, smooth=True))
    if p.get('core_w', 25.0) > 0:
        K._lamp(bpy, f'{name}-lamp', (cx, cy, cz), p.get('core_w', 25.0), kelvin=2700, size=0.06)
    # one black cable to a canopy on the deck, and the canopy
    top = p.get('ceiling', 3.40)
    cb = K.Mesh(f'{name}-cable'); K._cyl(cb.bm, cx, cy, cz + rc - 0.01, 0.003, top - cz - rc, seg=12)
    K._cyl(cb.bm, cx, cy, top - 0.025, 0.07, 0.025, seg=48)
    objs.append(cb.object(bpy, K.principled(bpy, 'mother-black', '#121212', rough=0.35, metal=0.6), smooth=True))
    return objs


# --- signs of life -----------------------------------------------------------------------------------------------------
def _glass(bpy):
    if 'glass' not in _M:
        _M['glass'] = K.principled(bpy, 'glass-39', '#FFFFFF', rough=0.005, trans=1.0, ior=1.5)
    return _M['glass']


def _liquid(bpy, hexc, name):
    key = 'liq-' + name
    if key not in _M:
        m = K.principled(bpy, key, '#FFFFFF', rough=0.0, trans=1.0, ior=1.34)
        nt = m.node_tree; out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        va = nt.nodes.new('ShaderNodeVolumeAbsorption'); va.inputs['Color'].default_value = LK.lin(hexc)
        va.inputs['Density'].default_value = 14.0
        nt.links.new(va.outputs['Volume'], out.inputs['Volume'])
        _M[key] = m
    return _M[key]


def _ice(bpy):
    if 'ice' not in _M:
        _M['ice'] = K.principled(bpy, 'ice-39', '#FFFFFF', rough=0.08, trans=1.0, ior=1.31, bump=(0.004, 0.02, 0.0004))
    return _M['ice']


ROCKS = [(0, 0), (0.042, 0), (0.0435, 0.092), (0.0395, 0.092), (0.0375, 0.018), (0, 0.018)]
COUPE = [(0, 0), (0.040, 0), (0.040, 0.004), (0.006, 0.010), (0.0045, 0.098), (0.032, 0.110), (0.057, 0.142),
         (0.0545, 0.142), (0.030, 0.114), (0, 0.108)]
MIXING = [(0, 0), (0.046, 0), (0.048, 0.006), (0.049, 0.140), (0.046, 0.140), (0.045, 0.012), (0, 0.012)]


def _cube(bm, c, s, rnd):
    g = bmesh.ops.create_cube(bm, size=s)
    a, b = rnd.uniform(0, 1.5), rnd.uniform(-0.25, 0.25)
    R = Matrix.Translation(c) @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(b, 4, 'X')
    bmesh.ops.transform(bm, matrix=R, verts=g['verts'])


def life(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 39))
    objs = []
    gl = K.Mesh(f'{name}-glass'); ic = K.Mesh(f'{name}-ice')
    pours = {}
    for x, y, z, fill, n_ice, col in p.get('rocks', []):       # rocks glasses: a pour, and ice above it
        K._lathe(gl.bm, ROCKS, seg=48, z0=z + 0.0002, cx=x, cy=y)
        h = max(0.004, fill)
        pm = pours.setdefault(col, K.Mesh(f'{name}-pour-{col[1:]}'))
        K._cyl(pm.bm, x, y, z + 0.0185, 0.0372, h, seg=48)
        for k in range(n_ice):
            if n_ice == 1:                                        # one large clear cube, as a good bar serves it
                _cube(ic.bm, Vector((x, y, z + 0.0185 + 0.026)), 0.050, rnd)
            else:
                a = 2 * math.pi * k / n_ice + rnd.uniform(-0.3, 0.3)
                _cube(ic.bm, Vector((x + 0.016 * math.cos(a), y + 0.016 * math.sin(a), z + 0.0185 + 0.016 + 0.012 * (k % 2))), 0.026, rnd)
    for x, y, z, fill, col in p.get('coupes', []):              # coupes, a pour in the bowl
        K._lathe(gl.bm, COUPE, seg=56, z0=z + 0.0002, cx=x, cy=y)
        if fill > 0:
            zb = z + 0.1095; top = zb + fill * 0.031
            rt = 0.031 + (0.0545 - 0.031) * fill
            prof = [(0, 0), (0.012, 0.002), (0.024, 0.008), (rt - 0.0005, top - zb), (0, top - zb)]
            pm = pours.setdefault(col, K.Mesh(f'{name}-pour-{col[1:]}'))
            K._lathe(pm.bm, prof, seg=56, z0=zb, cx=x, cy=y)
    for x, y, z, fill, col in p.get('mixing', []):              # a mixing glass, stirred, the bar spoon standing in it
        K._lathe(gl.bm, MIXING, seg=56, z0=z + 0.0002, cx=x, cy=y)
        pm = pours.setdefault(col, K.Mesh(f'{name}-pour-{col[1:]}'))
        K._cyl(pm.bm, x, y, z + 0.0125, 0.0445, fill, seg=56)
        for k in range(7):
            a = 2 * math.pi * k / 7
            _cube(ic.bm, Vector((x + 0.022 * math.cos(a), y + 0.022 * math.sin(a), z + 0.013 + fill - 0.006)), 0.024, rnd)
        sp = K.Mesh(f'{name}-spoon'); K._cyl(sp.bm, 0, 0, 0, 0.0018, 0.30, seg=10)
        bmesh.ops.transform(sp.bm, matrix=Matrix.Translation((x + 0.02, y - 0.01, z + 0.02)) @ Matrix.Rotation(math.radians(-14), 4, 'X'),
                            verts=sp.bm.verts[:])
        objs.append(sp.object(bpy, K.principled(bpy, 'spoon-steel', '#C8C8C4', metal=1.0, rough=0.18), smooth=True))
    if gl.bm.verts:
        objs.append(gl.object(bpy, _glass(bpy), smooth=True))
    else:
        gl.bm.free()
    if ic.bm.verts:
        objs.append(ic.object(bpy, _ice(bpy), bevel=0.004, seg=2))
    else:
        ic.bm.free()
    for col, pm in pours.items():
        objs.append(pm.object(bpy, _liquid(bpy, col, col[1:]), smooth=True))
    for x, y, z, a, label in p.get('bottles', []):               # an open bottle, its stopper beside it
        prof = [(0, 0), (0.040, 0), (0.042, 0.004), (0.042, 0.20), (0.036, 0.225), (0.016, 0.25), (0.0135, 0.262),
                (0.0135, 0.30), (0.0115, 0.30), (0.0115, 0.27), (0, 0.27)]
        bt = K.Mesh(f'{name}-bottle'); K._lathe(bt.bm, prof, seg=56, z0=z + 0.0002, cx=x, cy=y)
        objs.append(bt.object(bpy, K.principled(bpy, 'bottle-glass', '#FFFFFF', rough=0.01, trans=1.0, ior=1.5), smooth=True))
        lq = K.Mesh(f'{name}-bottle-pour'); K._cyl(lq.bm, x, y, z + 0.006, 0.0385, 0.13, seg=56)
        objs.append(lq.object(bpy, _liquid(bpy, '#B8641C', 'whisky'), smooth=True))
        lb = K.Mesh(f'{name}-label'); K._lathe(lb.bm, [(0.0423, 0.07), (0.0423, 0.15)], seg=56, z0=z, cx=x, cy=y)
        objs.append(lb.object(bpy, K.principled(bpy, 'label-paper', label, rough=0.7), smooth=True))
        st = K.Mesh(f'{name}-stopper')
        K._cyl(st.bm, x + 0.09 * math.cos(math.radians(a)), y + 0.09 * math.sin(math.radians(a)), z, 0.016, 0.018, seg=32)
        objs.append(st.object(bpy, K.principled(bpy, 'stopper-wood', '#4A3020', rough=0.5), bevel=0.003))
    for i, (x, y, z) in enumerate(p.get('votives', [])):         # a votive: a squat glass, a white candle, a flame
        vg = K.Mesh(f'{name}-votive{i}')
        K._lathe(vg.bm, [(0, 0), (0.034, 0), (0.035, 0.065), (0.032, 0.065), (0.031, 0.006), (0, 0.006)], seg=48, z0=z + 0.0002, cx=x, cy=y)
        objs.append(vg.object(bpy, K.principled(bpy, 'votive-glass', '#F2EEE6', rough=0.08, trans=1.0, ior=1.5), smooth=True))
        wx = K.Mesh(f'{name}-wax{i}'); K._cyl(wx.bm, x, y, z + 0.006, 0.027, 0.032, seg=40)
        objs.append(wx.object(bpy, MT.make(bpy, f'wax39-{i}', 'frosted', {'color': '#F3EDE2', 'absorb': '#F0E2C8', 'roughness': 0.6,
                                                                            'radius': 0.01, 'clear': 0.05, 'glow': p.get('wax_glow', 0.6), 'glow_color': '#FFB060'}), smooth=True))
        fl = K.Mesh(f'{name}-flame{i}')
        K._lathe(fl.bm, [(0.0, 0.0), (0.0035, 0.002), (0.0045, 0.006), (0.003, 0.012), (0.0, 0.020)], seg=16, z0=z + 0.040, cx=x, cy=y)
        objs.append(fl.object(bpy, LK.emitter(bpy, 'flame-39', '#FFB45A', p.get('flame', 40.0)), smooth=True))
        K._lamp(bpy, f'{name}-candle{i}', (x, y, z + 0.050), p.get('candle_w', 1.2), kelvin=1900, size=0.005)
    for i, (x, y, z, a) in enumerate(p.get('matchbooks', [])):
        mb = K.Mesh(f'{name}-matches{i}'); K._obox(mb.bm, x, y, z + 0.0002, 0.050, 0.038, 0.006, math.radians(a))
        objs.append(mb.object(bpy, K.principled(bpy, 'matchbook', '#1B1A19', rough=0.6), bevel=0.0008, seg=2))
        st = K.Mesh(f'{name}-matchstrip{i}'); K._obox(st.bm, x + 0.022 * math.cos(math.radians(a)), y + 0.022 * math.sin(math.radians(a)),
                                                      z + 0.0062, 0.004, 0.034, 0.0006, math.radians(a))
        objs.append(st.object(bpy, K.principled(bpy, 'match-strip', '#6A4A38', rough=0.9)))
    for i, (x, y, z, a) in enumerate(p.get('napkins', [])):
        nk = K.Mesh(f'{name}-napkin{i}'); K._obox(nk.bm, x, y, z + 0.0002, 0.11, 0.11, 0.0015, math.radians(a))
        objs.append(nk.object(bpy, K.principled(bpy, 'napkin', '#E9E4DA', rough=0.85), bevel=0.0005, seg=1))
    for i, (x, y, z, face, w) in enumerate(p.get('coats', [])):  # a coat folded over a chair back, hanging both sides
        objs.append(_coat(bpy, f'{name}-coat{i}', x, y, z, math.radians(face), w, p.get('coat_col', '#5A4636'), i))
    return objs


def _coat(bpy, nm, x, y, z, face, w, col, i):
    """A wool coat folded over a back rail at (x, y, z): a draped slab, both sides hanging, soft folds."""
    bm = bmesh.new()
    nu, nv = 14, 22
    hang_f, hang_b = 0.42, 0.30                                          # the length hanging each side
    verts = []
    for iv in range(nv + 1):
        s = iv / nv * (hang_f + hang_b + 0.10)                           # along the drape, over the rail
        row = []
        for iu in range(nu + 1):
            u = (iu / nu - 0.5) * w
            if s < hang_b:                                               # the back side, hanging
                dz, dy = -(hang_b - s), -0.045
            elif s < hang_b + 0.10:                                      # over the rail
                t = (s - hang_b) / 0.10 * math.pi
                dz, dy = 0.03 * math.sin(t), -0.045 * math.cos(t)
            else:                                                        # the front, hanging, flaring a little
                d = s - hang_b - 0.10
                dz, dy = -d, 0.045 + 0.10 * (d / hang_f) ** 2
            fold = 0.012 * math.sin(u * 31 + i) * min(1.0, abs(dz) * 5)
            row.append(bm.verts.new((u, dy + fold, dz)))
        verts.append(row)
    for iv in range(nv):
        for iu in range(nu):
            bm.faces.new([verts[iv][iu], verts[iv][iu + 1], verts[iv + 1][iu + 1], verts[iv + 1][iu]])
    bmesh.ops.transform(bm, matrix=Matrix.Translation((x, y, z)) @ Matrix.Rotation(face, 4, 'Z'), verts=bm.verts[:])
    me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(LK.wool(bpy, col, f'wool-coat-39-{i}'))
    ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
    so = ob.modifiers.new('thick', 'SOLIDIFY'); so.thickness = 0.012
    sd = ob.modifiers.new('soft', 'SUBSURF'); sd.levels = 1; sd.render_levels = 2
    return ob


# --- materials the room already has, given a scan's wear (built last, after the room) --------------------------------
def _scan_node(bpy, nt, path, colour, scale):
    """An image texture of `path` box-projected on object coordinates at `scale` metres a tile."""
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1 / scale, 1 / scale, 1 / scale)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(path, check_existing=True)
    im.image.colorspace_settings.name = 'sRGB' if colour else 'Non-Color'
    im.projection = 'BOX'; im.projection_blend = 0.3
    nt.links.new(mp.outputs['Vector'], im.inputs['Vector'])
    return im


def _darken(m, f):
    """Scale a material's base colour by `f` (a darker stain), whether it is a value or a texture."""
    if not m.use_nodes or 'Principled BSDF' not in m.node_tree.nodes:
        return
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; inp = b.inputs['Base Color']
    if inp.is_linked:
        src = inp.links[0].from_socket
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
        mx.inputs[7].default_value = (f, f, f, 1.0)
        nt.links.new(src, mx.inputs[6]); nt.links.new(mx.outputs[2], inp)
    else:
        c = inp.default_value; inp.default_value = (c[0] * f, c[1] * f, c[2] * f, c[3])


def retouch(bpy, name, p, kit):
    """`zinc`: the bar top's sheen worn unevenly (the scan's roughness, `zinc_rough` [lo, hi]) and its tone mottled by it
    (`zinc_mottle`), at `zinc_scale` metres a tile; rotated so no two edges of the tile line up with the counter."""
    import assets
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
    out = []
    for key, f in dict({'zinc': 0.6}, **p.get('darken', {})).items():   # a darker stain or patina, by material name
        for m in [m for m in bpy.data.materials if key in m.name]:
            _darken(m, f)
    m = bpy.data.materials.get('zinc')
    if m and p.get('zinc', True):
        t = assets.texture(p.get('zinc_scan', 'metal_plate_02'), '2k', maps=('diff', 'rough'))
        nt = m.node_tree; b = nt.nodes['Principled BSDF']
        r = _scan_node(bpy, nt, t['rough'], False, p.get('zinc_scale', 1.7))
        mr = nt.nodes.new('ShaderNodeMapRange'); lo, hi = p.get('zinc_rough', [0.16, 0.48])
        mr.inputs['To Min'].default_value = lo; mr.inputs['To Max'].default_value = hi
        nt.links.new(r.outputs['Color'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])
        d = _scan_node(bpy, nt, t['diff'], True, p.get('zinc_scale', 1.7))
        bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(d.outputs['Color'], bw.inputs['Color'])
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
        mx.inputs['Factor'].default_value = p.get('zinc_mottle', 0.35)
        mx.inputs[6].default_value = b.inputs['Base Color'].default_value[:]
        cr = nt.nodes.new('ShaderNodeMapRange'); cr.inputs['To Min'].default_value = 0.65; cr.inputs['To Max'].default_value = 1.25
        nt.links.new(bw.outputs['Val'], cr.inputs['Value'])
        cc = nt.nodes.new('ShaderNodeCombineColor')
        for k in ('Red', 'Green', 'Blue'):
            nt.links.new(cr.outputs['Result'], cc.inputs[k])
        nt.links.new(cc.outputs['Color'], mx.inputs[7]); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    return out
