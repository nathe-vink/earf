"""Poison without plants (round 31f): the poison cabinet of a Victorian pharmacy (P1) and a chemist's store room (P2).
Kit `ext` pieces ({"shape": "ext", "module": "poison_p_el", "fn": ...}):

- bottles: a row of glass bottles, `items` [[x, y, z, kind, color, height, label, stopper, fill, turn], ...] in the piece's
  frame, turned `rotate`. `kind` hex (a coffin-shaped hexagonal poison bottle, ribbed on its front faces), ribbed (a
  round one, ribbed all round), round (a reagent bottle), square (a modern chemical bottle with a screw cap). Each is a
  hollow shell (the glass a few mm thick, so it reads as a bottle, not a block), its `color` a glass tint, `label` the
  name of a label to wrap round its front (None for none), `stopper` cork|glass|cap|out (out: the cork lies beside it)
  |none, `fill` 0-1 how full of a dark liquid, `turn` degrees about z (the label faces -y unturned).
- shelves: a wall of shelves `size` [w, d, h] with `rows` shelf heights, in a wood (`texture`, a Poly Haven id) or steel.
- scale: a brass apothecary's balance, `size` its height.
- label textures are drawn here (PIL) into the asset cache: victorian (cream or red paper, POISON, a skull and
  crossbones, the drug's name, NOT TO BE TAKEN, aged), ghs (a white label, the red GHS diamond with the skull, the
  chemical, DANGER, UN number), tape (black and yellow hazard stripes).
"""
import math, os, random

import bmesh
from mathutils import Matrix, Vector

import assets
from poison_b_el import _hex, _node_mat, _obj, _join

LABEL_DIR = os.path.join(assets.CACHE, 'labels')
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


# --- labels ----------------------------------------------------------------------------------------------------
def _skull(d, cx, cy, s, ink):
    """A skull and crossbones drawn at (cx, cy), `s` its half-width, in `ink` (on a light ground)."""
    w = max(2, int(s * 0.16))
    for a in (1, -1):                                     # the crossed bones behind it
        x0, y0, x1, y1 = cx - s * 0.95, cy + s * 0.15 - a * s * 0.62, cx + s * 0.95, cy + s * 0.15 + a * s * 0.62
        d.line((x0, y0, x1, y1), fill=ink, width=w)
        for x, y in ((x0, y0), (x1, y1)):
            for dx, dy in ((-0.07, -0.07 * a), (0.07, 0.07 * a)):
                r = s * 0.11
                d.ellipse((x + dx * s - r, y + dy * s - r, x + dx * s + r, y + dy * s + r), fill=ink)
    d.ellipse((cx - s * 0.5, cy - s * 0.75, cx + s * 0.5, cy + s * 0.2), fill=ink)     # the cranium
    d.rounded_rectangle((cx - s * 0.3, cy, cx + s * 0.3, cy + s * 0.42), radius=s * 0.08, fill=ink)   # the jaw
    return w


def _skull_on(d, cx, cy, s, ink, ground):
    _skull(d, cx, cy, s, ink)
    for ex in (-0.2, 0.2):                                # eye sockets, nose, teeth in the ground's colour
        r = s * 0.14
        d.ellipse((cx + ex * s - r, cy - s * 0.38 - r, cx + ex * s + r, cy - s * 0.38 + r), fill=ground)
    d.polygon([(cx, cy - s * 0.16), (cx - s * 0.06, cy - s * 0.02), (cx + s * 0.06, cy - s * 0.02)], fill=ground)
    for tx in (-0.15, -0.05, 0.05, 0.15):
        d.line((cx + tx * s, cy + s * 0.12, cx + tx * s, cy + s * 0.38), fill=ground, width=max(1, int(s * 0.04)))


def _font(path, size):
    from PIL import ImageFont
    return ImageFont.truetype(path, size)


def _centre(d, text, y, font, fill, W):
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=font)
    d.text(((W - (x1 - x0)) / 2 - x0, y), text, font=font, fill=fill)


def _age(img, seed, amount=1.0):
    """Paper gone old: a stain at the edges, foxing, a little grain."""
    from PIL import Image, ImageFilter
    import numpy as np
    rnd = np.random.default_rng(seed)
    a = np.asarray(img).astype(float) / 255.0
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    edge = np.minimum.reduce([xx / W, 1 - xx / W, yy / H, 1 - yy / H])
    stain = np.clip(1 - edge / 0.12, 0, 1) ** 1.5 * 0.35 * amount
    blot = Image.fromarray((rnd.random((H // 8, W // 8)) * 255).astype('uint8')).resize((W, H)).filter(ImageFilter.GaussianBlur(6))
    blot = np.asarray(blot).astype(float) / 255.0
    stain = stain + np.clip(blot - 0.62, 0, 1) * 0.9 * amount
    brown = np.array([0.42, 0.30, 0.16])
    a = a * (1 - stain[..., None]) + brown * stain[..., None] * 0.6 + a * 0.0
    a += (rnd.random((H, W, 1)) - 0.5) * 0.04
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))


VICTORIAN = {   # name: (ground, ink, drug, seed)
    'v-arsenic': ('#E6D9B8', '#1A1410', 'ARSENIC', 1), 'v-laudanum': ('#B8261E', '#F1E6CC', 'LAUDANUM', 2),
    'v-strychnine': ('#E9DEC2', '#7A1410', 'STRYCHNINE', 3), 'v-belladonna': ('#DCCBA6', '#1A1410', 'TINCT. BELLADONNA', 4),
    'v-cyanide': ('#C42A20', '#EFE4CA', 'CYANIDE OF POTASSIUM', 5), 'v-oxalic': ('#E3D5B2', '#1A1410', 'OXALIC ACID', 6),
    'v-sublimate': ('#ECE2C8', '#8A1A12', 'CORROSIVE SUBLIMATE', 7), 'v-aconite': ('#D9C79E', '#1A1410', 'TINCT. ACONITE', 8),
}
GHS = {   # name: (chemical, UN number)
    'g-cyanide': ('SODIUM CYANIDE', 'UN 1689'), 'g-arsenic': ('ARSENIC TRIOXIDE', 'UN 1561'),
    'g-mercury': ('MERCURY(II) CHLORIDE', 'UN 1624'), 'g-paraquat': ('PARAQUAT DICHLORIDE', 'UN 2781'),
    'g-thallium': ('THALLIUM SULFATE', 'UN 1707'), 'g-strychnine': ('STRYCHNINE', 'UN 1692'),
}


def label_path(name):
    """The label's texture, drawn on first use."""
    from PIL import Image, ImageDraw
    os.makedirs(LABEL_DIR, exist_ok=True)
    path = os.path.join(LABEL_DIR, f'{name}.png')
    if os.path.exists(path):
        return path
    if name in VICTORIAN:
        ground, ink, drug, seed = VICTORIAN[name]
        W, H = 640, 420
        img = Image.new('RGB', (W, H), ground); d = ImageDraw.Draw(img)
        d.rectangle((14, 14, W - 15, H - 15), outline=ink, width=6); d.rectangle((28, 28, W - 29, H - 29), outline=ink, width=2)
        _centre(d, 'POISON', 36, _font(SERIF, 104), ink, W)
        _skull_on(d, W / 2, 238, 62, ink, ground)
        f = _font(SERIF, 44 if len(drug) < 12 else 30)
        _centre(d, drug, 306, f, ink, W)
        _centre(d, 'NOT TO BE TAKEN', 362, _font(SERIF, 26), ink, W)
        img = _age(img, seed)
    elif name in GHS:
        chem, un = GHS[name]
        W, H = 640, 420
        img = Image.new('RGB', (W, H), '#F4F4F0'); d = ImageDraw.Draw(img)
        cx, cy, r = 150, 210, 128                         # the GHS diamond: red border, white field, black skull
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill='#D2141C')
        rr = r - 16
        d.polygon([(cx, cy - rr), (cx + rr, cy), (cx, cy + rr), (cx - rr, cy)], fill='#FFFFFF')
        _skull_on(d, cx, cy + 4, 50, '#000000', '#FFFFFF')
        size = 44
        while size > 18:                                  # the chemical's name fits the space beside the diamond
            f = _font(SANS, size)
            if d.textbbox((0, 0), chem, font=f)[2] <= W - 320:
                break
            size -= 2
        d.text((300, 70), chem, font=f, fill='#111111')
        d.text((300, 140), 'DANGER', font=_font(SANS, 58), fill='#C0141A')
        d.text((300, 220), 'Fatal if swallowed', font=_font(SANS, 26), fill='#222222')
        d.text((300, 258), 'or inhaled.', font=_font(SANS, 26), fill='#222222')
        d.text((300, 320), un + '   6.1', font=_font(SANS, 30), fill='#222222')
        img = _age(img, hash(name) % 1000, 0.35)
    elif name == 'tape':
        W, H = 512, 64
        img = Image.new('RGB', (W, H), '#E8C21A'); d = ImageDraw.Draw(img)
        for x in range(-H, W + H, 64):
            d.polygon([(x, 0), (x + 32, 0), (x + 32 - H, H), (x - H, H)], fill='#141414')
        img = _age(img, 9, 0.5)
    else:
        raise ValueError(name)
    img.save(path)
    return path


def _image_mat(bpy, name, path, rough=0.75, sss=0.0):
    m, nt, b = _node_mat(bpy, name)
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(path, check_existing=True)
    tex.extension = 'CLIP'
    nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough
    if sss:
        b.inputs['Subsurface Weight'].default_value = sss
    return m


# --- glass -----------------------------------------------------------------------------------------------------
def _glass(bpy, name, color, rough=0.02):
    m, nt, b = _node_mat(bpy, name)
    b.inputs['Base Color'].default_value = (*_hex(color), 1)
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['Roughness'].default_value = rough
    b.inputs['IOR'].default_value = 1.52
    return m


def _liquid(bpy, name, color):
    m, nt, b = _node_mat(bpy, name)
    b.inputs['Base Color'].default_value = (*_hex(color), 1)
    b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['Roughness'].default_value = 0.02
    b.inputs['IOR'].default_value = 1.34
    return m


def _plain(bpy, name, color, rough=0.6, metal=0.0):
    m, nt, b = _node_mat(bpy, name)
    b.inputs['Base Color'].default_value = (*_hex(color), 1)
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m


def _profile(kind, H, R):
    """The outside of a bottle from its base up, [r, z]; the shoulder, neck and lip by kind."""
    if kind == 'square':
        return [(R * 0.94, 0.0), (R, H * 0.02), (R, H * 0.74), (R * 0.9, H * 0.8), (R * 0.42, H * 0.86),
                (R * 0.36, H * 0.88), (R * 0.36, H * 0.97)]
    if kind == 'round':
        return [(R * 0.94, 0.0), (R, H * 0.02), (R, H * 0.66), (R * 0.82, H * 0.76), (R * 0.4, H * 0.84),
                (R * 0.3, H * 0.86), (R * 0.3, H * 0.95), (R * 0.36, H * 0.97), (R * 0.34, H * 1.0)]
    return [(R * 0.94, 0.0), (R, H * 0.02), (R, H * 0.68), (R * 0.84, H * 0.77), (R * 0.36, H * 0.86),
            (R * 0.24, H * 0.88), (R * 0.24, H * 0.96), (R * 0.3, H * 0.975), (R * 0.28, H * 1.0)]


def _shape_k(kind, th, z, H):
    """The cross-section's radius factor at angle th: a hexagon or ribs on the body, round at the neck."""
    body = max(0.0, min(1.0, (H * 0.74 - z) / (H * 0.08)))
    if kind == 'hex' or kind == 'square':
        n = 6 if kind == 'hex' else 4
        a = (th + math.pi / n) % (2 * math.pi / n) - math.pi / n
        poly = math.cos(math.pi / n) / math.cos(a)
        poly = min(poly, 1.0 + (0.04 if kind == 'hex' else 0.02))
        k = poly
        if kind == 'hex' and abs(math.sin(th)) < 0.75 and math.sin(th) < 0:   # ribs on the front faces
            k += 0.012 * max(0.0, math.cos(26 * th)) ** 4
        return 1 + (k - 1) * body
    if kind == 'ribbed':
        return 1 + 0.03 * max(0.0, math.cos(22 * th)) ** 3 * body
    return 1.0


def _bottle_mesh(bm, kind, H, R, wall=0.0025, seg=72):
    """A hollow bottle: the outside up to the lip, over it, and the inside back down (both lathed with the shape)."""
    out = _profile(kind, H, R)
    inn = [(max(r - wall, 0.002), z + (wall if i == 0 else 0)) for i, (r, z) in enumerate(out)]
    rings = []
    prof = out + [(r, z) for r, z in reversed(inn)]
    for r, z in prof:
        ring = []
        for i in range(seg):
            th = 2 * math.pi * i / seg
            k = _shape_k(kind, th, z, H)
            ring.append(bm.verts.new((r * k * math.cos(th), r * k * math.sin(th), z)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg
            bm.faces.new((a[i], a[j], b[j], b[i]))
    # the floors, outside and in
    c0 = bm.verts.new((0, 0, 0.0)); c1 = bm.verts.new((0, 0, wall))
    for i in range(seg):
        j = (i + 1) % seg
        bm.faces.new((c0, rings[0][j], rings[0][i]))
        bm.faces.new((c1, rings[-1][i], rings[-1][j]))


def _label_mesh(bm, kind, H, R, h_frac=(0.18, 0.6), span=1.25, seg=24):
    """A paper label wrapped on the front (-y) of the bottle's body, just proud of the glass; UVs 0-1 across it."""
    uv = bm.loops.layers.uv.new('UVMap')
    z0, z1 = H * h_frac[0], H * h_frac[1]
    rows = []
    for j, z in enumerate((z0, z1)):
        row = []
        for i in range(seg + 1):
            u = i / seg
            th = -math.pi / 2 + (u - 0.5) * span
            k = _shape_k(kind, th, z, H)
            r = R * k + 0.0007
            row.append(bm.verts.new((r * math.cos(th), r * math.sin(th), z)))
        rows.append(row)
    for i in range(seg):
        f = bm.faces.new((rows[0][i], rows[0][i + 1], rows[1][i + 1], rows[1][i]))
        for loop, (u, v) in zip(f.loops, ((i / seg, 0), ((i + 1) / seg, 0), ((i + 1) / seg, 1), (i / seg, 1))):
            loop[uv].uv = (u, v)


def bottles(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    base = Matrix.Translation(Vector(p.get('position', [0, 0, 0]))) @ Matrix.Rotation(math.radians(p.get('rotate', [0, 0, 0])[2]), 4, 'Z')
    glass_m, label_m = {}, {}
    out = []
    for k_, it in enumerate(p['items']):
        x, y, z, kind, color, H, label, stopper, fill, turn = (list(it) + [None] * 10)[:10]
        R = H * {'hex': 0.2, 'ribbed': 0.22, 'round': 0.26, 'square': 0.22}[kind]
        spin = Matrix.Rotation(math.radians((turn or 0.0) + rnd.uniform(-14, 14)), 4, 'Z')
        m = base @ Matrix.Translation(Vector((x, y, z))) @ spin
        if color not in glass_m:
            glass_m[color] = _glass(bpy, f'{name}-glass-{color}', color)
        bm = bmesh.new(); _bottle_mesh(bm, kind, H, R)
        for v in bm.verts:
            v.co = m @ v.co
        ob = _obj(bpy, f'{name}-b{k_}', bm, glass_m[color], {})
        ob.location = (0, 0, 0); out.append(ob)
        if fill:
            lb = bmesh.new()
            prof = [(r - 0.0032, zz) for r, zz in _profile(kind, H, R) if zz <= H * fill]
            prof = [(0.0, 0.003)] + [(r, max(zz, 0.003)) for r, zz in prof] + [(0.0, prof[-1][1])]
            from poison_b_el import _lathe
            _lathe(lb, prof, 48, lambda th, zz, kind=kind, H=H: _shape_k(kind, th, zz, H))
            for v in lb.verts:
                v.co = m @ v.co
            lo = _obj(bpy, f'{name}-l{k_}', lb, _liquid(bpy, f'{name}-liq{k_}', p.get('liquid', '#3A2410')), {})
            lo.location = (0, 0, 0); out.append(lo)
        if label:
            if label not in label_m:
                label_m[label] = _image_mat(bpy, f'{name}-lab-{label}', label_path(label), 0.8, 0.05)
            lbm = bmesh.new()
            _label_mesh(lbm, kind, H, R, (0.16, 0.6) if kind != 'square' else (0.14, 0.64), 1.3 if kind != 'hex' else 1.0)
            for v in lbm.verts:
                v.co = m @ v.co
            lo = _obj(bpy, f'{name}-lab{k_}', lbm, label_m[label], {}, smooth=True)
            lo.location = (0, 0, 0); out.append(lo)
        top = _profile(kind, H, R)[-1]
        if stopper in ('cork', 'out', 'glass', 'cap'):
            sb = bmesh.new()
            rn = top[0] * (0.92 if stopper != 'cap' else 1.12)
            if stopper == 'glass':
                from poison_b_el import _lathe
                _lathe(sb, [(0.0, H * 0.94), (rn * 0.8, H * 0.94), (rn * 0.9, H * 1.0), (rn * 1.7, H * 1.04),
                            (rn * 1.6, H * 1.1), (0.0, H * 1.12)], 32)
                mat = glass_m[color]
            else:
                hh = H * (0.09 if stopper != 'cap' else 0.07)
                g = bmesh.ops.create_cone(sb, cap_ends=True, segments=24, radius1=rn, radius2=rn * (1.06 if stopper != 'cap' else 1.0), depth=hh)
                bmesh.ops.translate(sb, vec=Vector((0, 0, H * 0.97 + hh * 0.2)), verts=g['verts'])
                mat = _plain(bpy, f'{name}-cork', '#9A7A52', 0.85) if stopper != 'cap' else _plain(bpy, f'{name}-cap', p.get('cap', '#1C1C1C'), 0.5)
            mm = m
            if stopper == 'out':                          # the cork lies on the shelf beside it
                mm = m @ Matrix.Translation(Vector((R * 1.9, -R * 0.6, rn - H * 0.97))) @ Matrix.Rotation(math.pi / 2, 4, 'X')
            for v in sb.verts:
                v.co = mm @ v.co
            so = _obj(bpy, f'{name}-s{k_}', sb, mat, {})
            so.location = (0, 0, 0); out.append(so)
    return out


# --- furniture -------------------------------------------------------------------------------------------------
def shelves(bpy, name, p, kit):
    """A wall of shelves: two sides, a back, `rows` boards (heights from its base), in a wood or steel."""
    w, d, h = p.get('size', [3.0, 0.3, 1.6])
    t = p.get('board', 0.025)
    if p.get('texture'):
        mat = assets.pbr(bpy, p['texture'], p.get('res', '2k'), scale=p.get('tex_scale'), tint=p.get('tint'),
                         tint_mix=p.get('tint_mix', 0.0), coords='object')
    else:
        mat = _plain(bpy, f'{name}-mat', p.get('color', '#3A2414'), p.get('roughness', 0.5), p.get('metal', 0.0))
    bm = bmesh.new()
    def box(cx, cy, cz, sx, sy, sz):
        g = bmesh.ops.create_cube(bm, size=1.0)
        for v in g['verts']:
            v.co = Vector((cx + v.co.x * sx, cy + v.co.y * sy, cz + v.co.z * sz))
    box(-w / 2 + t / 2, 0, h / 2, t, d, h); box(w / 2 - t / 2, 0, h / 2, t, d, h)
    if p.get('back', True):
        box(0, d / 2 - 0.006, h / 2, w, 0.012, h)
    for z in p.get('rows', [0.0, 0.4, 0.8, 1.2, h - t]):
        box(0, 0, z + t / 2, w - 2 * t, d, t)
        if p.get('lip'):                                  # a moulded lip on each shelf's front edge
            box(0, -d / 2 + 0.008, z + t + 0.012, w - 2 * t, 0.016, 0.024)
    for x in p.get('uprights', []):
        box(x, 0, h / 2, t, d, h)
    m = Matrix.Translation(Vector(p.get('position', [0, 0, 0]))) @ Matrix.Rotation(math.radians(p.get('rotate', [0, 0, 0])[2]), 4, 'Z')
    for v in bm.verts:
        v.co = m @ v.co
    ob = _obj(bpy, name, bm, mat, {}, smooth=False)
    ob.location = (0, 0, 0)
    return [ob]


def scale(bpy, name, p, kit):
    """A brass apothecary's balance: a turned pillar on a base, a beam with two hanging pans."""
    S = p.get('size', 0.38)
    brass = _plain(bpy, f'{name}-brass', '#B08A3A', 0.32, 1.0)
    bm = bmesh.new()
    from poison_b_el import _lathe
    _join(bm, lambda t: _lathe(t, [(0.0, 0.0), (S * 0.3, 0.0), (S * 0.3, S * 0.04), (S * 0.12, S * 0.07), (S * 0.04, S * 0.1),
                                   (S * 0.035, S * 0.82), (S * 0.06, S * 0.86), (0.0, S * 0.9)], 40))
    def bar(a, b, r):
        def build(t):
            g = bmesh.ops.create_cone(t, cap_ends=True, segments=12, radius1=r, radius2=r, depth=(Vector(b) - Vector(a)).length)
            q = (Vector(b) - Vector(a)).to_track_quat('Z', 'Y')
            bmesh.ops.rotate(t, verts=g['verts'], cent=Vector((0, 0, 0)), matrix=q.to_matrix())
            bmesh.ops.translate(t, vec=(Vector(a) + Vector(b)) / 2, verts=g['verts'])
        _join(bm, build)
    tilt = p.get('tilt', 0.04)
    L = S * 0.62
    bar((-L, 0, S * 0.84 + tilt * S), (L, 0, S * 0.84 - tilt * S), S * 0.012)
    for sx in (-1, 1):
        px, pz = sx * L, S * 0.84 - sx * tilt * S
        for a in range(3):                                # three chains to each pan
            th = 2 * math.pi * a / 3
            bar((px, 0, pz), (px + math.cos(th) * S * 0.2, math.sin(th) * S * 0.2, pz - S * 0.42), S * 0.003)
        _join(bm, lambda t, px=px, pz=pz: _lathe(t, [(0.0, pz - S * 0.46), (S * 0.22, pz - S * 0.43), (S * 0.23, pz - S * 0.41),
                                                    (S * 0.21, pz - S * 0.42), (0.0, pz - S * 0.45)], 36))
    m = Matrix.Translation(Vector(p.get('position', [0, 0, 0]))) @ Matrix.Rotation(math.radians(p.get('rotate', [0, 0, 0])[2]), 4, 'Z')
    for v in bm.verts:
        v.co = m @ v.co
    ob = _obj(bpy, name, bm, brass, {})
    ob.location = (0, 0, 0)
    return [ob]


def tape(bpy, name, p, kit):
    """Hazard tape laid on the floor: a strip `length` x `width` from `position` along `angle` degrees."""
    L, W = p.get('length', 3.0), p.get('width', 0.05)
    mat = _image_mat(bpy, f'{name}-tape', label_path('tape'), 0.6)
    tex = mat.node_tree.nodes['Image Texture']; tex.extension = 'REPEAT'
    bm = bmesh.new(); uv = bm.loops.layers.uv.new('UVMap')
    vs = [bm.verts.new(c) for c in ((0, -W / 2, 0), (L, -W / 2, 0), (L, W / 2, 0), (0, W / 2, 0))]
    f = bm.faces.new(vs)
    rep = L / (W * 8)
    for loop, (u, v) in zip(f.loops, ((0, 0), (rep, 0), (rep, 1), (0, 1))):
        loop[uv].uv = (u, v)
    m = Matrix.Translation(Vector(p.get('position', [0, 0, 0.002]))) @ Matrix.Rotation(math.radians(p.get('angle', 0)), 4, 'Z')
    for v in bm.verts:
        v.co = m @ v.co
    ob = _obj(bpy, name, bm, mat, {}, smooth=False)
    ob.location = (0, 0, 0)
    return [ob]


# --- outdoors (round 31g) --------------------------------------------------------------------------------------
def plume_at(bpy, name, p, kit):
    """Smoke's plume (smoke_b_el.plume), its foot at height `z` instead of the ground (a vent down in a crater): the
    volume's shading is in its object's own frame, so moving the object moves the plume with it."""
    import smoke_b_el
    obs = smoke_b_el.plume(bpy, name, p, kit)
    for ob in obs:
        ob.location.z += p.get('z', 0.0)
    return obs


def algae_water(bpy, name, p, kit):
    """A still lake choked with a cyanobacteria bloom: a plane `size` [w, d] at `position`, dark glossy water under a
    paint-like scum of vivid green that gathers in swirls and streaks (warped noise, stretched along `drift` degrees),
    thick and matte where it has massed, thinning to an oily film and open water (`cover` 0-1 how much is scum). The
    scum's greens `greens` [deep, mid, bright]; `streak` how stretched the swirls are."""
    w, d = p.get('size', [80.0, 80.0])
    m, nt, b = _node_mat(bpy, f'{name}-mat'); L = nt.links.new
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Rotation'].default_value = (0, 0, math.radians(p.get('drift', 25.0)))
    st = p.get('streak', 3.0)
    mp.inputs['Scale'].default_value = (1.0 / st, 1.0, 1.0)
    L(tc.outputs['Object'], mp.inputs['Vector'])
    def noise(scale, detail, dist, rough=0.6):
        n = nt.nodes.new('ShaderNodeTexNoise')
        n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail
        n.inputs['Distortion'].default_value = dist; n.inputs['Roughness'].default_value = rough
        L(mp.outputs['Vector'], n.inputs['Vector'])
        return n
    big = noise(p.get('scale', 0.18), 6.0, 2.5)            # the masses and their swirling edges
    fine = noise(2.2, 8.0, 0.8)                           # clots and pinholes in the scum
    mix = nt.nodes.new('ShaderNodeMath'); mix.operation = 'MULTIPLY_ADD'
    L(fine.outputs['Fac'], mix.inputs[0]); mix.inputs[1].default_value = 0.25; L(big.outputs['Fac'], mix.inputs[2])
    if p.get('clots', 0.0):                               # the scum broken into irregular clots and rafts
        cl = noise(p.get('clot_scale', 1.4), 10.0, 1.4, 0.7)
        k = p['clots']
        a_ = nt.nodes.new('ShaderNodeMath'); a_.operation = 'MULTIPLY'
        L(mix.outputs['Value'], a_.inputs[0]); a_.inputs[1].default_value = 1.0 - k
        b_ = nt.nodes.new('ShaderNodeMath'); b_.operation = 'MULTIPLY_ADD'
        L(cl.outputs['Fac'], b_.inputs[0]); b_.inputs[1].default_value = k; L(a_.outputs['Value'], b_.inputs[2])
        mix = b_
    cover = p.get('cover', 0.6)
    cut = nt.nodes.new('ShaderNodeMapRange'); cut.interpolation_type = 'SMOOTHSTEP'
    cut.inputs['From Min'].default_value = 0.78 - cover * 0.45; cut.inputs['From Max'].default_value = 0.86 - cover * 0.45
    L(mix.outputs['Value'], cut.inputs['Value'])
    deep, midc, bright = p.get('greens', ['#1E4A12', '#3F8A1E', '#7DBE2A'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    el = ramp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*_hex(deep), 1)
    el[1].position = 1.0; el[1].color = (*_hex(bright), 1)
    e = el.new(0.5); e.color = (*_hex(midc), 1)
    tone = nt.nodes.new('ShaderNodeMapRange'); L(fine.outputs['Fac'], tone.inputs['Value'])
    tone.inputs['From Min'].default_value = 0.3; tone.inputs['From Max'].default_value = 0.75
    L(tone.outputs['Result'], ramp.inputs['Fac'])
    # open water: dark, glossy, a little green-brown
    water = (*_hex(p.get('water', '#141A10')), 1)
    col = nt.nodes.new('ShaderNodeMix'); col.data_type = 'RGBA'
    L(cut.outputs['Result'], col.inputs['Factor']); col.inputs['A'].default_value = water; L(ramp.outputs['Color'], col.inputs['B'])
    L(col.outputs['Result'], b.inputs['Base Color'])
    rgh = nt.nodes.new('ShaderNodeMapRange'); L(cut.outputs['Result'], rgh.inputs['Value'])
    rgh.inputs['To Min'].default_value = 0.03; rgh.inputs['To Max'].default_value = p.get('scum_rough', 0.55)
    L(rgh.outputs['Result'], b.inputs['Roughness'])
    b.inputs['Specular IOR Level'].default_value = 0.5
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35; bump.inputs['Distance'].default_value = 0.004
    hgt = nt.nodes.new('ShaderNodeMath'); hgt.operation = 'MULTIPLY'
    L(cut.outputs['Result'], hgt.inputs[0]); L(fine.outputs['Fac'], hgt.inputs[1])
    L(hgt.outputs['Value'], bump.inputs['Height']); L(bump.outputs['Normal'], b.inputs['Normal'])
    if p.get('float'):                                    # the scum alone, floating on real water: open where it thins
        out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        op = nt.nodes.new('ShaderNodeMapRange'); L(cut.outputs['Result'], op.inputs['Value'])
        op.inputs['From Min'].default_value, op.inputs['From Max'].default_value = p.get('edge', [0.15, 0.5])
        fac = op.outputs['Result']
        if p.get('lane'):                                 # [x, half-width]: open water along a line of constant x
            lx, lw = p['lane']
            sx = nt.nodes.new('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sx.inputs['Vector'])
            dx = nt.nodes.new('ShaderNodeMath'); dx.operation = 'SUBTRACT'; L(sx.outputs['X'], dx.inputs[0])
            dx.inputs[1].default_value = lx - p.get('position', [0, 0, 0])[0]
            ab = nt.nodes.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; L(dx.outputs['Value'], ab.inputs[0])
            ln = nt.nodes.new('ShaderNodeMapRange'); ln.interpolation_type = 'SMOOTHSTEP'; L(ab.outputs['Value'], ln.inputs['Value'])
            ln.inputs['From Min'].default_value = lw; ln.inputs['From Max'].default_value = lw * 2.5
            lm = nt.nodes.new('ShaderNodeMath'); lm.operation = 'MULTIPLY'; L(fac, lm.inputs[0]); L(ln.outputs['Result'], lm.inputs[1])
            fac = lm.outputs['Value']
        L(fac, mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(b.outputs['BSDF'], mx.inputs[2])
        L(mx.outputs['Shader'], out.inputs['Surface'])
    bm = bmesh.new()
    vs = [bm.verts.new(c) for c in ((-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (w / 2, d / 2, 0), (-w / 2, d / 2, 0))]
    bm.faces.new(vs)
    ob = _obj(bpy, name, bm, m, {'position': p.get('position', [0, 0, 0])}, smooth=False)
    return [ob]


SIGNS = {'algae': ('TOXIC ALGAE', 'AVOID CONTACT', 'with the water. Keep children', 'and dogs out of the lake.'),
         'gas': ('TOXIC GAS', 'VOLCANIC FUMES', 'Do not stop or leave the path.', 'Gases can kill in minutes.')}


def sign_path(kind='algae'):
    """A warning sign's face: weathered white enamel, a red DANGER band, the warning (generic, no agency's mark)."""
    from PIL import Image, ImageDraw
    os.makedirs(LABEL_DIR, exist_ok=True)
    path = os.path.join(LABEL_DIR, f'sign-{kind}-3.png')
    if os.path.exists(path):
        return path
    # as real bloom signs set it: the hazard the biggest words, under a short DANGER band
    W, H = 900, 640
    img = Image.new('RGB', (W, H), '#EDEBE2'); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W - 1, 130), fill='#C3161C')
    d.rectangle((10, 10, W - 11, H - 11), outline='#1A1A1A', width=8)
    _centre(d, 'DANGER', 18, _font(SANS, 96), '#FFFFFF', W)
    a, b, c, e = SIGNS[kind]
    size = 150
    while size > 40 and d.textbbox((0, 0), a, font=_font(SANS, size))[2] > W - 70:
        size -= 4
    _centre(d, a, 160, _font(SANS, size), '#1A1A1A', W)
    cx, cy, r = 130, 450, 80                              # a warning triangle
    d.polygon([(cx, cy - r), (cx + r * 1.05, cy + r * 0.75), (cx - r * 1.05, cy + r * 0.75)], fill='#1A1A1A')
    d.polygon([(cx, cy - r + 20), (cx + r * 0.8, cy + r * 0.6), (cx - r * 0.8, cy + r * 0.6)], fill='#F2C31A')
    d.text((cx - 10, cy - 42), '!', font=_font(SANS, 90), fill='#1A1A1A')
    def fit(text, y, size, fill):                         # each line shrunk to the space right of the triangle
        while size > 14 and d.textbbox((0, 0), text, font=_font(SANS, size))[2] > W - 250 - 36:
            size -= 2
        d.text((250, y), text, font=_font(SANS, size), fill=fill)
    fit(b, 365, 74, '#1A1A1A')
    fit(c, 470, 32, '#222222')
    fit(e, 512, 32, '#222222')
    img = _age(img, 21, 3.5)                              # weathered hard: the type faded and spotted, not vector-crisp
    img.save(path)
    return path


def sign(bpy, name, p, kit):
    """A weathered warning sign on a timber post at the water's edge: the board `size` [w, h] m, its foot at
    `position`, turned `rotate` (degrees about z; the face looks along -y unturned), leaning `lean` degrees."""
    bw, bh = p.get('size', [0.6, 0.43])
    post_h = p.get('post', 1.25)
    wood = assets.pbr(bpy, p.get('wood', 'weathered_planks'), '2k', scale=0.5, coords='object')
    face = _image_mat(bpy, f'{name}-face', sign_path(p.get('warning', 'algae')), 0.55)
    bm = bmesh.new()
    g = bmesh.ops.create_cube(bm, size=1.0)
    for v in g['verts']:
        v.co = Vector((v.co.x * 0.08, v.co.y * 0.08 + 0.05, (v.co.z + 0.5) * post_h))
    fb = bmesh.new(); uv = fb.loops.layers.uv.new('UVMap')
    z0 = post_h - bh - 0.04
    vs = [fb.verts.new(c) for c in ((-bw / 2, -0.001, z0), (bw / 2, -0.001, z0), (bw / 2, -0.001, z0 + bh), (-bw / 2, -0.001, z0 + bh))]
    f = fb.faces.new(vs)
    for loop, (u, v) in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        loop[uv].uv = (u, v)
    back = bmesh.new()
    g2 = bmesh.ops.create_cube(back, size=1.0)
    for v in g2['verts']:
        v.co = Vector((v.co.x * bw, v.co.y * 0.012 + 0.006, z0 + (v.co.z + 0.5) * bh))
    bolts = bmesh.new()                                   # the coach bolts through the board into the post
    if p.get('bolts'):
        for bz in (z0 + 0.05, z0 + bh - 0.05):
            g3 = bmesh.ops.create_cone(bolts, cap_ends=True, segments=12, radius1=0.011, radius2=0.009, depth=0.006)
            for v in g3['verts']:
                v.co = Vector((v.co.x, v.co.z - 0.004, v.co.y + bz))
    M = (Matrix.Translation(Vector(p.get('position', [0, 0, 0]))) @ Matrix.Rotation(math.radians(p.get('rotate', [0, 0, 0])[2]), 4, 'Z')
         @ Matrix.Rotation(math.radians(p.get('lean', 4.0)), 4, 'X'))
    out = []
    parts = [(bm, wood, False), (back, wood, False), (fb, face, False)]
    if p.get('bolts'):
        parts.append((bolts, _plain(bpy, f'{name}-bolt', '#3A2A1E', 0.7, 0.6), True))
    for k, (b_, mat, sm) in enumerate(parts):
        for v in b_.verts:
            v.co = M @ v.co
        ob = _obj(bpy, f'{name}-{k}', b_, mat, {}, smooth=sm); ob.location = (0, 0, 0); out.append(ob)
    return out


def scan(bpy, name, p, kit):
    """A scanned model placed like piece('asset'), less the parts whose names contain any of `drop` (as the pier's
    gantry, modular_wooden_pier_section_05)."""
    root = assets.place(bpy, p['model'], p.get('res', '2k'), tuple(p.get('position', [0, 0, 0])),
                        tuple(p.get('rotate', [0, 0, 0])), p.get('scale', 1.0), name)
    drop = p.get('drop', [])
    for o in list(root.children_recursive):
        if any(d in o.name for d in drop):
            bpy.data.objects.remove(o, do_unlink=True)
    return [root]


def scum_rings(bpy, name, p, kit):
    """Scum banked up round what stands in the bloom (the wind piles it against posts and stumps): for each
    [x, y, r] in `items`, a ragged annulus of thick, wet scum (`color`) from r out to r + `width`, lying on the water
    at `z`."""
    rnd = random.Random(p.get('seed', 1))
    m, nt, b = _node_mat(bpy, f'{name}-mat')
    b.inputs['Base Color'].default_value = (*_hex(p.get('color', '#9AB02C')), 1)
    b.inputs['Roughness'].default_value = p.get('roughness', 0.35)
    bm = bmesh.new()
    z, wid, seg = p.get('z', 0.004), p.get('width', 0.35), 40
    for x, y, r in p.get('items', []):
        inner, outer = [], []
        ph = rnd.uniform(0, 6.28)
        for k in range(seg):
            a = 2 * math.pi * k / seg
            ro = r + wid * (0.6 + 0.4 * math.sin(3 * a + ph) * rnd.uniform(0.6, 1.0))
            inner.append(bm.verts.new((x + r * math.cos(a), y + r * math.sin(a), z)))
            outer.append(bm.verts.new((x + ro * math.cos(a), y + ro * math.sin(a), z)))
        for k in range(seg):
            j = (k + 1) % seg
            bm.faces.new((inner[k], inner[j], outer[j], outer[k]))
    return [_obj(bpy, name, bm, m, {'position': [0, 0, 0]}, smooth=True)]


def wetline(bpy, name, p, kit):
    """Wet bases on everything standing in the water: every scanned model's materials (those named in `models`) are
    darkened and glossed below world height `top` (m), most at the waterline `z`, a darker band just above it. Place
    it after the pieces it wets."""
    done = 0
    for m in bpy.data.materials:
        if not m.use_nodes or not any(k in m.name for k in p.get('models', [])):
            continue
        nt = m.node_tree; L = nt.links.new
        b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if b is None:
            continue
        geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
        L(geo.outputs['Position'], sep.inputs['Vector'])
        wet = nt.nodes.new('ShaderNodeMapRange'); wet.interpolation_type = 'SMOOTHSTEP'
        L(sep.outputs['Z'], wet.inputs['Value'])
        wet.inputs['From Min'].default_value = p.get('z', 0.0) + p.get('top', 0.07)
        wet.inputs['From Max'].default_value = p.get('z', 0.0)
        mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
        L(wet.outputs['Result'], mul.inputs['Factor'])
        mul.inputs['B'].default_value = (*_hex(p.get('color', '#4A4A30')), 1)
        src = b.inputs['Base Color'].links[0].from_socket if b.inputs['Base Color'].is_linked else None
        if src is not None:
            L(src, mul.inputs['A'])
        else:
            mul.inputs['A'].default_value = b.inputs['Base Color'].default_value
        L(mul.outputs['Result'], b.inputs['Base Color'])
        rs = b.inputs['Roughness'].links[0].from_socket if b.inputs['Roughness'].is_linked else None
        rmix = nt.nodes.new('ShaderNodeMix'); rmix.data_type = 'FLOAT'
        L(wet.outputs['Result'], rmix.inputs['Factor'])
        if rs is not None:
            L(rs, rmix.inputs['A'])
        else:
            rmix.inputs['A'].default_value = b.inputs['Roughness'].default_value
        rmix.inputs['B'].default_value = p.get('wet_rough', 0.25)
        L(rmix.outputs['Result'], b.inputs['Roughness'])
        done += 1
    print(f'wetline: {done} materials wetted')
    return []
