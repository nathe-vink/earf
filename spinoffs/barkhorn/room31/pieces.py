"""Room 31's own pieces (a kit `ext` module, loaded by path: {"kind": "kit", "shape": "ext", "path":
"spinoffs/barkhorn/room31/pieces.py", "fn": NAME, ...}). Each is called as fn(bpy, name, p, kit) and returns its
objects, placed in world metres (z up, the speakers' fronts toward -y). What the scanned library lacks is built here:

- credenza: a walnut credenza, crown-cut veneer bookmatched across its doors, satin lacquer, on a recessed plinth;
- rug: a deep-pile wool rug, its pile a scanned fabric displaced, its edge bound and relaxed onto the floor;
- socket: a wall socket on the skirting's face with a plug in it (where each speaker's mains lead ends);
- books: a stack of cloth-bound books, titles on their spines;
- exterior: the view out of the glazing, a photographed environment on a sphere only the camera (and gloss) sees, so
  the room is lit by the engine's sun and sky while the window shows a real place;
- floor and plaster: photographed oak and plaster laid over the room's own floor and walls.
"""
import math, os, random

import bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def _assets():
    import assets                                            # studio/engine is on the path inside the engine
    return assets


def _principled(m):
    return next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')


def _lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def _obj(bpy, name, bm, mats, smooth=False):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = smooth
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return ob


def _bevel_mod(ob, w, seg=3):
    md = ob.modifiers.new('bevel', 'BEVEL'); md.width = w; md.segments = seg; md.limit_method = 'ANGLE'
    md.harden_normals = False
    return md


def _box_uv(bm, x0, y0, z0, x1, y1, z1, u_axis='x', mirror=False, uoff=0.0, voff=0.0):
    """A box with UVs in metres on every face: grain (u) along `u_axis` on the faces that hold it, along z elsewhere;
    `mirror` flips u (a bookmatched leaf), `uoff`/`voff` shift the leaf on the flitch."""
    vs = [bm.verts.new(v) for v in [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                                     (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    uv = bm.loops.layers.uv.verify()
    out = []
    for f in faces:
        face = bm.faces.new([vs[i] for i in f])
        n = face.normal
        for lp in face.loops:
            co = lp.vert.co
            if abs(n.y) > 0.5:          # front/back: grain along x
                u, v = co.x, co.z
            elif abs(n.z) > 0.5:        # top/bottom: grain along x
                u, v = co.x, co.y
            else:                       # ends: grain along y
                u, v = co.y, co.z
            if mirror:
                u = -u
            lp[uv].uv = (u + uoff, v + voff)
        out.append(face)
    return out


# --- materials ---------------------------------------------------------------------------------------------------
def walnut(bpy, tex='walnut_veneer', lift=1.25, coat=0.9, coat_rough=0.22, res='4k', name='walnut-veneer'):
    """Scanned walnut veneer under a satin lacquer: the scan's colour lifted by `lift`, a clear coat over it."""
    A = _assets()
    m = A.pbr(bpy, tex, res, coords='uv', name=name)
    nt = m.node_tree; b = _principled(m)
    lk = next((l for l in nt.links if l.to_socket == b.inputs['Base Color']), None)
    if lk and lift != 1.0:
        mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
        mul.inputs['Factor'].default_value = 1.0; mul.inputs['B'].default_value = (lift, lift * 0.97, lift * 0.93, 1.0)
        src = lk.from_socket; nt.links.remove(lk)
        nt.links.new(src, mul.inputs['A']); nt.links.new(mul.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = coat_rough
    b.inputs['Coat IOR'].default_value = 1.5
    return m


def _plain(bpy, name, color, rough=0.5, spec=0.5, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = _principled(m)
    b.inputs['Base Color'].default_value = _lin(color); b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec; b.inputs['Metallic'].default_value = metal
    if coat:
        b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.1
    return m


# --- credenza ----------------------------------------------------------------------------------------------------
def credenza(bpy, name, p, kit):
    """A walnut credenza: `position` [x, y] its centre on the floor (back to the wall), `size` [w, d, h], `doors` its
    door count (bookmatched leaves, 3 mm reveals), on a black plinth `plinth` [h, inset]; `texture` the veneer."""
    x, y = p['position'][:2]; w, d, h = p.get('size', [1.6, 0.45, 0.56])
    ph, pin = p.get('plinth', [0.09, 0.03])
    n = p.get('doors', 3); gap = p.get('gap', 0.003); top_t = p.get('top', 0.025); side_t = 0.02
    wal = walnut(bpy, p.get('texture', 'walnut_veneer'), p.get('lift', 1.25), res=p.get('res', '4k'))
    black = _plain(bpy, name + '-plinth', p.get('plinth_color', '#2B1D14'), rough=0.6, spec=0.3)
    shadow = _plain(bpy, name + '-inner', '#2A1A10', rough=0.8, spec=0.2)
    objs = []
    x0, x1 = x - w / 2, x + w / 2; yb = y + d / 2; yf = y - d / 2
    # plinth, recessed
    bm = bmesh.new(); _box_uv(bm, x0 + pin, yf + pin, 0.0, x1 - pin, yb - 0.01, ph)
    objs.append(_obj(bpy, name + '-plinth', bm, [black]))
    # carcass: top, two ends, bottom (one flitch: the top's grain runs on into the ends)
    bm = bmesh.new()
    _box_uv(bm, x0, yf, h - top_t, x1, yb, h, voff=0.13)
    _box_uv(bm, x0, yf, ph, x0 + side_t, yb, h - top_t, voff=0.31)
    _box_uv(bm, x1 - side_t, yf, ph, x1, yb, h - top_t, mirror=True, voff=0.31)
    ob = _obj(bpy, name + '-carcass', bm, [wal]); _bevel_mod(ob, 0.0015, 2); objs.append(ob)
    # the recess behind the doors (dark, so the reveals read as shadow)
    bm = bmesh.new(); _box_uv(bm, x0 + side_t, yf + 0.012, ph, x1 - side_t, yb - 0.02, h - top_t)
    objs.append(_obj(bpy, name + '-inner', bm, [shadow]))
    # doors: one flitch cut in sequence, alternate leaves flipped (bookmatched), grain continuous across the reveals
    dw = (w - 2 * side_t - (n + 1) * gap) / n; dz0 = ph + gap; dz1 = h - top_t - gap
    bm = bmesh.new()
    for i in range(n):
        a = x0 + side_t + gap + i * (dw + gap)
        # leaf i: its u runs from the flitch's centre line outward, mirrored on every other leaf
        mirror = (i % 2 == 1)
        centre = a + dw if not mirror else a
        _box_uv(bm, a, yf, dz0, a + dw, yf + 0.019, dz1, mirror=mirror, uoff=(-centre if not mirror else centre) + 0.4)
    ob = _obj(bpy, name + '-doors', bm, [wal]); _bevel_mod(ob, 0.0012, 2); objs.append(ob)
    # finger pulls: a shallow shadow groove under the top on each door
    bm = bmesh.new()
    for i in range(n):
        a = x0 + side_t + gap + i * (dw + gap)
        _box_uv(bm, a + 0.004, yf - 0.0006, dz1 - 0.022, a + dw - 0.004, yf + 0.004, dz1 - 0.004)
    objs.append(_obj(bpy, name + '-pulls', bm, [shadow]))
    return objs


# --- rug -----------------------------------------------------------------------------------------------------------
def rug(bpy, name, p, kit):
    """A deep-pile rug: `position` [x, y] its centre, `size` [w, d], `pile` its height (m), `texture` a scanned fabric
    (displaced by `displace`), `tint`/`tint_mix` its colour; the edge bound and rolled onto the floor over `edge` m,
    wavering a little."""
    A = _assets()
    x, y = p['position'][:2]; w, d = p.get('size', [2.4, 1.7]); t = p.get('pile', 0.016); e = p.get('edge', 0.025)
    rot = math.radians(p.get('rotate_z', 0.0))
    cell = p.get('cell', 0.006)
    nx, ny = int(w / cell), int(d / cell)
    rnd = random.Random(p.get('seed', 3))
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    bm = bmesh.new()
    grid = []
    for j in range(ny + 1):
        row = []
        for i in range(nx + 1):
            u, v = i / nx, j / ny
            px, py = (u - 0.5) * w, (v - 0.5) * d
            dist = min(px + w / 2, w / 2 - px, py + d / 2, d / 2 - py)          # to the nearest edge
            q = min(1.0, dist / e)
            z = t * math.sin(q * math.pi / 2) ** 0.7
            # a soft waver along the edges, as a rug relaxes onto a floor
            z += 0.003 * (1 - q) * math.sin(px * 3.1 + ph[0]) * math.sin(py * 2.3 + ph[1])
            z = max(0.0005, z)
            row.append(bm.verts.new((px, py, z)))
        grid.append(row)
    uv = bm.loops.layers.uv.verify()
    for j in range(ny):
        for i in range(nx):
            f = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
            for lp in f.loops:
                lp[uv].uv = (lp.vert.co.x, lp.vert.co.y)
    m = A.pbr(bpy, p.get('texture', 'curly_teddy_natural'), p.get('res', '2k'), scale=p.get('tex_scale'),
              displace=p.get('displace', 0.004), tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0),
              bump=p.get('bump', 1.0), coords='object', name=name + '-mat')
    b = _principled(m)
    if p.get('value', 1.0) != 1.0:                             # the wool's own value (COLOR tint keeps the scan's)
        nt = m.node_tree; lk = next((l for l in nt.links if l.to_socket == b.inputs['Base Color']), None)
        mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
        mul.inputs['Factor'].default_value = 1.0; v = p['value']; mul.inputs['B'].default_value = (v, v, v, 1.0)
        nt.links.new(lk.from_socket, mul.inputs['A']); nt.links.new(mul.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Sheen Weight'].default_value = p.get('sheen', 0.6); b.inputs['Sheen Roughness'].default_value = 0.5
    b.inputs['Specular IOR Level'].default_value = 0.15
    ob = _obj(bpy, name, bm, [m], smooth=True)
    ob.location = (x, y, 0.0); ob.rotation_euler.z = rot
    return [ob]


# --- socket ----------------------------------------------------------------------------------------------------------
def socket(bpy, name, p, kit):
    """A wall socket: an 86 mm square plate on the wall at `position` [x, y_wall, z] (its face toward -y), a plug in it
    with its lead running down (`lead` adds a short drop, the cable prop does the rest)."""
    x, yw, z = p['position']; s = p.get('size', 0.086); t = 0.009
    plate = _plain(bpy, name + '-plate', p.get('color', '#EEEBE4'), rough=0.35, spec=0.5)
    plug = _plain(bpy, name + '-plug', '#161616', rough=0.45, spec=0.4)
    bm = bmesh.new(); _box_uv(bm, x - s / 2, yw - t, z - s / 2, x + s / 2, yw, z + s / 2)
    ob = _obj(bpy, name + '-plate', bm, [plate]); _bevel_mod(ob, 0.002, 3); objs = [ob]
    bm = bmesh.new(); _box_uv(bm, x - 0.021, yw - t - 0.028, z - 0.024, x + 0.021, yw - t, z + 0.018)
    ob = _obj(bpy, name + '-plug', bm, [plug]); _bevel_mod(ob, 0.004, 3); objs.append(ob)
    return objs


# --- books -----------------------------------------------------------------------------------------------------------
def _spine_png(path, w_px, h_px, ground, ink, title, author):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('RGB', (w_px, h_px), ground); d = ImageDraw.Draw(im)
    fonts = ['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf']
    fp = next((f for f in fonts if os.path.exists(f)), None)
    size = int(h_px * 0.42)
    f = ImageFont.truetype(fp, size) if fp else ImageFont.load_default()
    fa = ImageFont.truetype(fp, int(size * 0.7)) if fp else f
    d.text((int(w_px * 0.06), h_px // 2), title, fill=ink, font=f, anchor='lm')
    d.text((int(w_px * 0.94), h_px // 2), author, fill=ink, font=fa, anchor='rm')
    im.save(path)


def books(bpy, name, p, kit):
    """A stack of cloth-bound books lying flat, spines toward -y: `position` [x, y, z] the stack's foot, `books` a list
    of [w, d, t, cloth hex, ink hex, title, author] (metres), each turned a degree or two."""
    A = _assets()
    x, y, z = p['position']; rnd = random.Random(p.get('seed', 5))
    cache = os.path.join(ROOT, 'studio', 'assets', 'cache', 'room31'); os.makedirs(cache, exist_ok=True)
    paper = _plain(bpy, name + '-pages', '#EDE6D6', rough=0.85, spec=0.2)
    objs = []
    for i, (bw, bd, bt, cloth, ink, title, author) in enumerate(p['books']):
        png = os.path.join(cache, f'{name}-{i}.png')
        _spine_png(png, 1600, max(40, int(1600 * bt / bw)), cloth, ink, title, author)
        m = bpy.data.materials.new(f'{name}-cloth{i}'); m.use_nodes = True; nt = m.node_tree; b = _principled(m)
        tc = nt.nodes.new('ShaderNodeTexCoord'); img = nt.nodes.new('ShaderNodeTexImage')
        img.image = bpy.data.images.load(png, check_existing=True); img.extension = 'EXTEND'
        nt.links.new(tc.outputs['UV'], img.inputs['Vector']); nt.links.new(img.outputs['Color'], b.inputs['Base Color'])
        b.inputs['Roughness'].default_value = 0.8; b.inputs['Sheen Weight'].default_value = 0.3
        # cloth weave as a fine bump
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900.0
        bn = nt.nodes.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = 0.15
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector']); nt.links.new(nz.outputs['Fac'], bn.inputs['Height'])
        nt.links.new(bn.outputs['Normal'], b.inputs['Normal'])
        bm = bmesh.new()
        # boards (the cover) wrap the block; the block of pages shows at the fore-edge, head and tail
        fs = _box_uv(bm, -bw / 2, -bd / 2, 0, bw / 2, bd / 2, bt)
        uvl = bm.loops.layers.uv.verify()
        for f in fs:
            if f.normal.y < -0.5:                                  # the spine: the title image across it
                for lp in f.loops:
                    lp[uvl].uv = ((lp.vert.co.x + bw / 2) / bw, lp.vert.co.z / bt)
            else:
                for lp in f.loops:
                    lp[uvl].uv = (0.02, 0.5)                          # cloth colour, clear of the lettering
        ob = _obj(bpy, f'{name}-{i}', bm, [m]); _bevel_mod(ob, min(0.002, bt / 6), 2)
        # pages: set in from the boards at the fore-edge and ends
        bm = bmesh.new(); _box_uv(bm, -bw / 2 + 0.003, -bd / 2 + 0.006, 0.0025, bw / 2 - 0.003, bd / 2 + 0.0005, bt - 0.0025)
        pg = _obj(bpy, f'{name}-{i}-pages', bm, [paper])
        zz = z + sum(q[2] for q in p['books'][:i])
        for o in (ob, pg):
            o.location = (x + rnd.uniform(-0.012, 0.012), y + rnd.uniform(-0.008, 0.008), zz)
            o.rotation_euler.z = math.radians(rnd.uniform(-2.5, 2.5))
        objs += [ob, pg]
    return objs


# --- the view out --------------------------------------------------------------------------------------------------
def exterior(bpy, name, p, kit):
    """The view out of the glazing: a photographed environment (`hdri`, a Poly Haven id) on a sphere `radius` m round
    `centre`, turned `rotation_deg` (as the engine turns a sky), at `strength`; seen by the camera and in gloss only, so
    it lights nothing (the engine's sun and sky light the room) and a window shows a real place. `blur` softens it as
    a lens focused on the room would."""
    A = _assets()
    path = A.hdri(p['hdri'], p.get('res', '8k'))
    c = Vector(p.get('centre', [0.0, -2.0, 1.2])); r = p.get('radius', 60.0)
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=48, radius=r)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Strength'].default_value = p.get('strength', 1.0)
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    # direction from the sphere's centre (the world's lookup is by direction; parallax at 60 m is nil)
    sub = nt.nodes.new('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = tuple(c)
    nt.links.new(geo.outputs['Position'], sub.inputs[0])
    if p.get('blur', 0) > 0:                                     # jitter the lookup: a soft, out-of-focus view
        wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '4D'
        nt.links.new(geo.outputs['Position'], wn.inputs['Vector'])
        sc = nt.nodes.new('ShaderNodeVectorMath'); sc.operation = 'MULTIPLY_ADD'
        nt.links.new(wn.outputs['Color'], sc.inputs[0]); sc.inputs[1].default_value = (p['blur'] * r,) * 3
        sc.inputs[2].default_value = (-p['blur'] * r / 2,) * 3
        add = nt.nodes.new('ShaderNodeVectorMath'); add.operation = 'ADD'
        nt.links.new(sub.outputs['Vector'], add.inputs[0]); nt.links.new(sc.outputs['Vector'], add.inputs[1])
        vec = add.outputs['Vector']
    else:
        vec = sub.outputs['Vector']
    rot = nt.nodes.new('ShaderNodeVectorRotate'); rot.rotation_type = 'Z_AXIS'; rot.invert = True
    rot.inputs['Angle'].default_value = math.radians(p.get('rotation_deg', 0.0))
    nt.links.new(vec, rot.inputs['Vector'])
    env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(path, check_existing=True)
    nt.links.new(rot.outputs['Vector'], env.inputs['Vector'])
    col = env.outputs['Color']
    if p.get('tint'):
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
        mx.inputs['Factor'].default_value = 1.0; mx.inputs['B'].default_value = _lin(p['tint'])
        nt.links.new(col, mx.inputs['A']); col = mx.outputs['Result']
    nt.links.new(col, em.inputs['Color']); nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    ob = _obj(bpy, name, bm, [m], smooth=True)
    ob.location = c
    for f in ob.data.polygons:
        f.flip()                                                 # faces inward
    ob.visible_diffuse = False; ob.visible_shadow = False; ob.visible_transmission = p.get('through_glass', True)
    ob.visible_volume_scatter = False; ob.visible_glossy = p.get('glossy', True); ob.visible_camera = True
    return [ob]


# --- the room's surfaces, photographed ---------------------------------------------------------------------------------
def floor(bpy, name, p, kit):
    """Photographed oak boards over the room's floor: a plane `rect` [x0, y0, x1, y1] a hair above it, the texture
    `texture` at its real size (or `tex_scale`), turned `rotate_deg` (boards along x at 90), under an oiled satin
    finish (`rough_mul`, `coat`)."""
    A = _assets()
    x0, y0, x1, y1 = p['rect']; z = p.get('z', 0.0004)
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]]
    bm.faces.new(vs)
    m = A.pbr(bpy, p.get('texture', 'laminate_floor_02'), p.get('res', '4k'), scale=p.get('tex_scale'),
              rough_mul=p.get('rough_mul', 1.0), bump=p.get('bump', 1.0), tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0),
              coords='object', name=name + '-mat')
    nt = m.node_tree
    mp = next(n for n in nt.nodes if n.type == 'MAPPING')
    mp.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(p.get('rotate_deg', 0.0)))
    mp.inputs['Location'].default_value = tuple(p.get('offset', [0.0, 0.0, 0.0]))
    b = _principled(m)
    if p.get('coat'):
        b.inputs['Coat Weight'].default_value = p['coat']; b.inputs['Coat Roughness'].default_value = p.get('coat_rough', 0.3)
    if p.get('value', 1.0) != 1.0:
        lk = next((l for l in nt.links if l.to_socket == b.inputs['Base Color']), None)
        mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
        mul.inputs['Factor'].default_value = 1.0; v = p['value']; mul.inputs['B'].default_value = (v, v, v, 1.0)
        nt.links.new(lk.from_socket, mul.inputs['A']); nt.links.new(mul.outputs['Result'], b.inputs['Base Color'])
    ob = _obj(bpy, name, bm, [m])
    return [ob]


def plaster(bpy, name, p, kit):
    """Photographed plaster over the room's walls: lays a texture (`texture`, tinted toward `color` by `tint_mix`) on
    every object whose name starts 'wall-' by replacing its plaster material (so openings and reveals keep their
    shape). Run it after the room is built (it is a prop, and props come after the walls)."""
    A = _assets()
    m = A.pbr(bpy, p.get('texture', 'beige_wall_001'), p.get('res', '4k'), scale=p.get('tex_scale'),
              tint=p.get('color'), tint_mix=p.get('tint_mix', 0.0), bump=p.get('bump', 1.0),
              rough_mul=p.get('rough_mul', 1.0), coords='object', name=name + '-mat')
    nt = m.node_tree; b = _principled(m)
    if p.get('value', 1.0) != 1.0:
        lk = next((l for l in nt.links if l.to_socket == b.inputs['Base Color']), None)
        mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
        mul.inputs['Factor'].default_value = 1.0; v = p['value']; mul.inputs['B'].default_value = (v, v, v, 1.0)
        nt.links.new(lk.from_socket, mul.inputs['A']); nt.links.new(mul.outputs['Result'], b.inputs['Base Color'])
    n = 0
    for ob in bpy.data.objects:
        if ob.type == 'MESH' and ob.name.startswith('wall-'):
            for i, slot in enumerate(ob.material_slots):
                if slot.material and slot.material.name.startswith('wall'):
                    ob.material_slots[i].material = m; n += 1
            if not ob.material_slots:
                ob.data.materials.append(m); n += 1
    print(f'room31 plaster: {n} wall slots')
    return []


# --- a scanned model, recoloured ----------------------------------------------------------------------------------------
def recolour(bpy, name, p, kit):
    """A scanned model (`model`, a Poly Haven id) placed as the kit's `asset` places it, with the base colour of its
    materials whose names contain `match` multiplied toward `color` (a black leather re-dyed cognac, say) by `mix`, and
    their roughness scaled by `rough_mul`."""
    A = _assets()
    root = A.place(bpy, p['model'], p.get('res', '2k'), tuple(p.get('position', [0, 0, 0])), tuple(p.get('rotate', [0, 0, 0])),
                   p.get('scale', 1.0), name)
    seen = set()
    for o in [root] + list(root.children_recursive):
        if o.type != 'MESH':
            continue
        for m in o.data.materials:
            if not m or m.name in seen or not any(k in m.name.lower() for k in p.get('match', ['leather'])):
                continue
            seen.add(m.name)
            nt = m.node_tree; b = _principled(m)
            lk = next((l for l in nt.links if l.to_socket == b.inputs['Base Color']), None)
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = p.get('blend', 'COLOR')
            mx.inputs['Factor'].default_value = p.get('mix', 1.0); mx.inputs['B'].default_value = _lin(p['color'])
            if lk:
                nt.links.new(lk.from_socket, mx.inputs['A'])
            else:
                mx.inputs['A'].default_value = b.inputs['Base Color'].default_value
            out = mx.outputs['Result']
            if p.get('value', 1.0) != 1.0:
                mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
                mul.inputs['Factor'].default_value = 1.0; v = p['value']; mul.inputs['B'].default_value = (v, v, v, 1.0)
                nt.links.new(out, mul.inputs['A']); out = mul.outputs['Result']
            nt.links.new(out, b.inputs['Base Color'])
    print(f'room31 recolour {p["model"]}: {sorted(seen)}')
    return [root]
