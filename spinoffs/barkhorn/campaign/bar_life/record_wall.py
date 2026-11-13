"""The bar's record wall, rebuilt (the owner, 13 Nov: "the records are obviously fake"; the coordinator's 20:19 brief).
Takes over every cell the reused room filled with its flat stripes (records-sleeves, records-faceout, taken out
here) and every open cell the old fill_records found, and fills them as a wall of LPs is filled:

- Jackets 315 square: about 70 % 3 to 3.4 mm, 15 % gatefolds 5 to 6.5, 10 % 12-inch singles 1.5 to 2.3 in thin
  sleeves, 5 % doubles and boxes 9 to 13; gaps 0 to 1.5 mm; heights 312 to 316; the fronts within a few mm of their
  neighbours, about 1 in 20 pulled out 15 to 30, 1 in 20 pushed in 10 to 20; about 1 in 10 with its inner sleeve or
  the disc standing 2 to 6 proud.
- Lean: half a degree each, in groups that drift 0.5 to 3 degrees together. About 1 cell in 6 is 60 to 85 % full, its
  last group leaning 6 to 14 degrees into the space; about 1 cell in 12 a flat stack of 5 to 10.
- Spines from tex/spines.jpg (make_spines.py): invented type, the shares of white, cream, black, kraft and printed
  colour of the brief, worn ends. About a third in clear outer sleeves: a glossy skin with vertical streaks.
- Below eye level the jacket tops show the pale inner sleeve between the two card edges.
- About 1 cell in 8 holds something else of a record room: a 7-inch box and singles, books and magazines, storage
  boxes, a face-out sleeve. No other brand, no lamp.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/campaign/bar_life/record_wall.py", "fn": "build",
     "x0", "x1", "z0", "z1", "cell", "y" (the wall's front face), "back" (the cells' back), "skip" [[x0, x1, z0, z1]],
     "eye_z" (below it the tops show), "seed"}
"""
import json, math, os, random, sys
import bmesh
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bar_life import _hex, _plain, _print  # noqa: E402

STATS = {}


def _atlas_mats(bpy):
    """0: the spines' card; 1: the same in a clear outer sleeve (a glossy coat, streaked up and down)."""
    img = bpy.data.images.load(os.path.join(HERE, 'tex', 'spines.jpg'), check_existing=True)
    out = []
    for sleeve in (False, True):
        key = 'rw-spines-sleeved' if sleeve else 'rw-spines'
        m = bpy.data.materials.get(key)
        if not m:
            m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree
            b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
            b.inputs['Roughness'].default_value = 0.62
            tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = img; tex.interpolation = 'Linear'
            nt.links.new(nt.nodes.new('ShaderNodeUVMap').outputs['UV'], tex.inputs['Vector'])
            nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
            if sleeve and 'Coat Weight' in b.inputs:
                b.inputs['Coat Weight'].default_value = 1.0
                # streaks: noise stretched up and down drives the coat's roughness between 0.04 and 0.22
                tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
                mp.inputs['Scale'].default_value = (900.0, 900.0, 6.0)
                nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0; nz.inputs['Detail'].default_value = 3.0
                mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.04; mr.inputs['To Max'].default_value = 0.22
                nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
                nt.links.new(nz.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], b.inputs['Coat Roughness'])
                b.inputs['Roughness'].default_value = 0.5
        out.append(m)
    return out


class Boxes:
    """Boxes into one bmesh, each turned about a pivot on the floor, its front face (-y) mapped to a spine's column
    in the atlas (or its top, for a lying jacket), its other faces to the column's plain edge."""

    def __init__(self, ncol):
        self.bm = bmesh.new(); self.uv = self.bm.loops.layers.uv.new('UVMap'); self.ncol = ncol

    def box(self, x0, x1, y0, y1, z0, z1, mi=0, col=None, ang=0.0, pivot=None, lying=False, rz=0.0, rz_c=None):
        bm = self.bm
        P = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
        M = Matrix.Identity(3)
        if ang:
            M = Matrix.Rotation(math.radians(ang), 3, 'Y')
        vs = []
        for (x, y, z) in P:
            v = Vector((x, y, z))
            if ang:
                c = Vector((pivot[0], 0.0, pivot[1])); d = v - c; d.y = 0.0
                v = c + M @ d; v.y = y
            if rz:
                c = Vector((rz_c[0], rz_c[1], 0.0)); d = v - c; d.z = 0.0
                v = c + Matrix.Rotation(math.radians(rz), 3, 'Z') @ d; v.z = (v.z if ang else z)
            vs.append(bm.verts.new(v))
        # index: x + 2 y + 4 z
        faces = {'front': (0, 1, 5, 4), 'back': (3, 2, 6, 7), 'left': (2, 0, 4, 6), 'right': (1, 3, 7, 5),
                 'bottom': (2, 3, 1, 0), 'top': (4, 5, 7, 6)}
        for kname, idx in faces.items():
            f = bm.faces.new([vs[i] for i in idx]); f.material_index = mi
            if col is None:
                continue
            u0, u1 = col / self.ncol, (col + 1) / self.ncol
            ue = u0 + 0.5 / 16 / self.ncol                   # the column's edge: its plain ground
            for lp, i in zip(f.loops, idx):
                xi, zi = i & 1, (i >> 2) & 1
                if kname == 'front' and not lying:
                    lp[self.uv].uv = (u0 + (u1 - u0) * (0.1 + 0.8 * xi), zi)
                elif kname == 'front' and lying:
                    lp[self.uv].uv = (u0 + (u1 - u0) * (0.1 + 0.8 * zi), xi)
                else:
                    lp[self.uv].uv = (ue, 0.5)


def _thickness(rnd):
    r = rnd.random()
    if r < 0.70:
        return rnd.uniform(0.0030, 0.0034), 'lp'
    if r < 0.85:
        return rnd.uniform(0.0050, 0.0065), 'gate'
    if r < 0.95:
        return rnd.uniform(0.0015, 0.0023), 'thin'
    return rnd.uniform(0.009, 0.013), 'box'


def _design(rnd, idx, kind):
    if kind == 'thin':
        return rnd.choice(idx['thin'])
    r = rnd.random(); acc = 0.0
    for cat, share in (('white', 0.30), ('cream', 0.15), ('black', 0.22), ('kraft', 0.05), ('colour', 0.28)):
        acc += share
        if r < acc:
            return rnd.choice(idx[cat])
    return rnd.choice(idx['colour'])


def _row(rnd, width, fill, part):
    """The records of one cell along its width, in local coordinates: [(u, t, kind, ang)], u from the cell's start.
    `part`: the last group leans into the space left."""
    recs = []; u = 0.0005; limit = width * fill
    g_left = 0; g_ang = 0.0
    lean_n = rnd.randint(4, 12) if part else 0
    while True:
        t, kind = _thickness(rnd)
        if g_left <= 0:
            g_left = rnd.randint(5, 25); g_ang = rnd.uniform(0.5, 3.0)
        ang = g_ang + rnd.gauss(0.0, 0.5)
        h = 0.314
        foot = t / math.cos(math.radians(ang))
        if u + foot + h * math.sin(math.radians(max(ang, 0))) > limit - 0.0005:
            break
        recs.append([u, t, kind, ang]); g_left -= 1
        u += foot + (rnd.random() ** 3) * 0.0015
    if part and recs:                                        # the last group leans into the space, 6 to 14 degrees
        a = rnd.uniform(6.0, 14.0); n = min(lean_n, len(recs))
        u = recs[-n][0]
        for r in recs[-n:]:
            r[3] = a + rnd.gauss(0.0, 0.5); r[0] = u
            u += r[1] / math.cos(math.radians(r[3])) + (rnd.random() ** 2) * 0.001
        # the wedge: the leaning group's top must stay in the cell
        while recs and recs[-1][0] + 0.314 * math.sin(math.radians(recs[-1][3])) + recs[-1][1] > width - 0.001:
            recs.pop()
    return recs


def build(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1313))
    meta = json.load(open(os.path.join(HERE, 'tex', 'spines.json')))
    idx, ncol = meta['index'], meta['n']
    cell, x0w, z0w, yf, yb = p['cell'], p['x0'], p['z0'], p['y'], p['back']
    ncx = int(round((p['x1'] - x0w) / cell)); ncz = int(round((p['z1'] - z0w) / cell))
    # 1. the cells: those the room filled, and those open to their back the old fill found
    cells = set()
    for o in list(bpy.data.objects):
        if o.name.split('.')[0] in ('records-sleeves', 'records-faceout') and o.type == 'MESH':
            mw = o.matrix_world
            for v in o.data.vertices:
                w = mw @ v.co
                i = int((w.x - x0w) // cell); k = int((w.z - z0w) // cell)
                if 0 <= i < ncx and 0 <= k < ncz:
                    cells.add((i, k))
    dg = bpy.context.evaluated_depsgraph_get()
    for i in range(ncx):
        for k in range(ncz):
            cx, z = x0w + (i + 0.5) * cell, z0w + k * cell
            if (i, k) in cells or any(s[0] < cx < s[1] and s[2] < z + cell / 2 < s[3] for s in p.get('skip', [])):
                continue
            hit = bpy.context.scene.ray_cast(dg, Vector((cx, yf - 0.6, z + 0.16)), Vector((0, 1, 0)), distance=0.6 + (yb - yf) * 0.55)
            if not hit[0]:
                cells.add((i, k))
    gone = []
    for o in list(bpy.data.objects):
        if o.name.split('.')[0] in ('records-sleeves', 'records-faceout'):
            gone.append(o.name); bpy.data.objects.remove(o, do_unlink=True)
    print('RECORD WALL took over', len(cells), 'cells; removed', gone)

    B = Boxes(ncol)
    mats = _atlas_mats(bpy) + [_plain(bpy, '#CFC9BA', 0.7), _plain(bpy, '#0E0E0E', 0.28)]   # 2 inner sleeve, 3 disc
    other = []                                               # (kind, xa, xb, z)
    order = sorted(cells); rnd.shuffle(order)
    n_other = max(1, round(len(order) * 0.125)); n_part = round(len(order) / 6); n_flat = round(len(order) / 12)
    kinds = {}
    for c in order[:n_other]:
        kinds[c] = 'other'
    for c in order[n_other:n_other + n_part]:
        kinds[c] = 'part'
    for c in order[n_other + n_part:n_other + n_part + n_flat]:
        kinds[c] = 'flat'
    full_counts, shares = [], {'lp': 0, 'gate': 0, 'thin': 0, 'box': 0}
    eye = p.get('eye_z', 1.6)
    for (i, k) in sorted(cells):
        xa = x0w + i * cell + 0.0115; xb = x0w + (i + 1) * cell - 0.0115; z = z0w + k * cell + 0.0002
        kind = kinds.get((i, k), 'full')
        if kind == 'other':
            other.append((xa, xb, z)); continue
        W = xb - xa
        base_y = yf + 0.012 + rnd.uniform(0.0, 0.006)
        if kind == 'flat':                                   # a flat stack, slightly askew, records upright behind? no room: alone
            n = rnd.randint(5, 10); zz = z
            for j in range(n):
                t, kd = _thickness(rnd); t = min(t, 0.007); shares[kd] += 1
                col = _design(rnd, idx, kd)
                cxs, cys = (xa + xb) / 2 + rnd.uniform(-0.006, 0.006), base_y + 0.157 + rnd.uniform(-0.005, 0.005)
                B.box(cxs - 0.1575, cxs + 0.1575, cys - 0.1575, cys + 0.1575, zz, zz + t, mi=1 if rnd.random() < 0.33 else 0,
                      col=col, lying=True, rz=rnd.uniform(-3.0, 3.0), rz_c=(cxs, cys))
                zz += t + 0.0003
            continue
        fill = rnd.uniform(0.60, 0.85) if kind == 'part' else rnd.uniform(0.985, 1.0)
        recs = _row(rnd, W, fill, kind == 'part')
        mirror = rnd.random() < 0.5
        off = 0.0
        for (u, t, kd, ang) in recs:
            shares[kd] += 1
            col = _design(rnd, idx, kd)
            h = rnd.uniform(0.312, 0.316)
            off = max(-0.004, min(0.004, off + rnd.gauss(0.0, 0.0015)))
            r = rnd.random()
            dy = -rnd.uniform(0.015, 0.030) if r < 0.05 else (rnd.uniform(0.010, 0.020) if r < 0.10 else 0.0)
            y0 = base_y + off + dy; y1 = min(y0 + 0.315, yb - 0.002)
            if mirror:                                       # filled from the right, leaning to the left
                xr = xb - u; xl = xr - t; a = -ang; piv = (xl, z)
            else:
                xl = xa + u; xr = xl + t; a = ang; piv = (xr, z)
            mi = 1 if (rnd.random() < 0.33 and kd != 'box') else 0
            B.box(xl, xr, y0, y1, z, z + h, mi=mi, col=col, ang=a, pivot=piv)
            if t > 0.0025 and rnd.random() < 0.10:           # the inner sleeve or the disc standing proud
                pr = rnd.uniform(0.002, 0.006)
                if rnd.random() < 0.6:
                    B.box(xl + t * 0.3, xr - t * 0.3, y0 + 0.006, y1 - 0.006, z + 0.004, z + h + pr, mi=2, ang=a, pivot=piv)
                else:
                    B.box(xl + t * 0.4, xr - t * 0.4, y0 + 0.012, y1 - 0.012, z + 0.006, z + h + pr, mi=3, ang=a, pivot=piv)
            elif z + h < eye and t > 0.0025:                 # below the eye: the pale inner sleeve between the card edges
                B.box(xl + t * 0.28, xr - t * 0.28, y0 + 0.004, y1 - 0.004, z + h - 0.003, z + h + 0.0004, mi=2, ang=a, pivot=piv)
        if kind == 'full':
            full_counts.append(len(recs))
    bmesh.ops.recalc_face_normals(B.bm, faces=B.bm.faces[:])
    me = bpy.data.meshes.new(name); B.bm.to_mesh(me); B.bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    out = [ob] + _others(bpy, name, other, rnd, yf, yb, idx, ncol, p.get('eye_z', 1.6))
    n = sum(shares.values())
    STATS.update(cells=len(cells), full=len(full_counts), part=n_part, flat=n_flat, other=len(other),
                 per_full=(min(full_counts), round(sum(full_counts) / len(full_counts), 1), max(full_counts)) if full_counts else None,
                 shares={k: round(v / n, 3) for k, v in shares.items()}, records=n)
    print('RECORD WALL', json.dumps(STATS))
    return out


def _others(bpy, name, cells, rnd, yf, yb, idx, ncol, eye):
    """The cells that hold something else of a record room, in turn: a 7-inch box and singles, books and magazines,
    storage boxes, a face-out sleeve in front of records."""
    objs = []
    cloth = ['#5A2A22', '#2E3A2E', '#6E5A3E', '#3A2E26', '#7A6448', '#2A2A30', '#5E4A36', '#8A3A2A', '#CFC6B2', '#1E1E1E']
    mags = ['#C8102E', '#D9D3C4', '#1F4E9C', '#A8801E', '#141414', '#D9531E', '#2B6E4F']
    plain = {}
    def mat(h, r=0.7):
        return plain.setdefault((h, r), _plain(bpy, h, r))
    bm = bmesh.new(); used = []
    def box(x0, x1, y0, y1, z0, z1, m):
        if m not in used:
            used.append(m)
        g = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((x1 - x0, y1 - y0, z1 - z0)), verts=g['verts'])
        bmesh.ops.translate(bm, vec=Vector(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)), verts=g['verts'])
        for f in {f for v in g['verts'] for f in v.link_faces}:
            f.material_index = used.index(m)
    kinds = ['seven', 'books', 'boxes', 'face']
    for j, (xa, xb, z) in enumerate(cells):
        kind = kinds[j % 4]
        y0 = yf + 0.02
        if kind == 'seven':                                  # a 7-inch box, open top, singles in it; singles beside
            bx = xa + 0.004 if j % 8 < 4 else xb - 0.004 - 0.19
            box(bx, bx + 0.19, y0 + 0.02, y0 + 0.25, z, z + 0.16, mat(rnd.choice(['#1A1A1A', '#B89A6E', '#D2CCBE']), 0.8))
            s = (bx + 0.19 + 0.006) if bx < (xa + xb) / 2 else xa + 0.004
            e = xb - 0.004 if bx < (xa + xb) / 2 else bx - 0.006
            while s < e - 0.003:
                t = rnd.uniform(0.0012, 0.0022)
                box(s, s + t, y0 + 0.03, y0 + 0.21, z, z + 0.18, mat(rnd.choice(['#D6D0C2', '#141414', '#D9C9A0', '#B3202A', '#1F4E9C', '#D4CEBF'])))
                s += t + rnd.uniform(0.0002, 0.001)
        elif kind == 'books':                                # books, and magazines lying flat on one end
            s = xa + 0.004; e = xb - (0.0 if j % 3 else 0.12)
            while s < e - 0.02:
                t = rnd.uniform(0.018, 0.045); h = rnd.uniform(0.21, 0.31)
                box(s, s + t, yb - rnd.uniform(0.17, 0.24), yb - 0.01, z, z + h, mat(rnd.choice(cloth), 0.75))
                s += t + 0.0008
            if not j % 3 == 0:
                continue
            zz = z
            for _ in range(rnd.randint(6, 14)):
                t = rnd.uniform(0.003, 0.006)
                box(e + 0.004, xb - 0.004, yb - 0.24, yb - 0.01, zz, zz + t, mat(rnd.choice(mags), 0.35))
                zz += t
        elif kind == 'boxes':                                # storage boxes with lids, kraft or black
            c = rnd.choice(['#A8865E', '#141414', '#9C7A52', '#D2CCBE'])
            if rnd.random() < 0.5:
                box(xa + 0.004, xb - 0.004, y0, yb - 0.01, z, z + 0.26, mat(c, 0.85))
                box(xa + 0.002, xb - 0.002, y0 - 0.002, yb - 0.008, z + 0.26, z + 0.30, mat(c, 0.8))
            else:
                m_ = (xa + xb) / 2
                for a, b in ((xa + 0.004, m_ - 0.003), (m_ + 0.003, xb - 0.004)):
                    hh = rnd.uniform(0.2, 0.29)
                    box(a, b, y0, yb - 0.01, z, z + hh, mat(c, 0.85)); box(a - 0.002, b + 0.002, y0 - 0.002, yb - 0.008, z + hh, z + hh + 0.035, mat(c, 0.8))
        else:                                                # a face-out sleeve leaning on records behind it
            cv = rnd.choice([3, 5, 7, 9, 11, 12, 13, 15, 16, 2])
            path = f'tex/cover-{cv:02d}.png'
            if not os.path.exists(os.path.join(HERE, path)):
                path = 'tex/cover-03.png'
            from bar_life import boards
            objs += boards(bpy, f'{name}-face{j}', {'boards': [{'image': path, 'w': 0.315, 'h': 0.315, 't': 0.003,
                                                               'x': (xa + xb) / 2, 'y': yf + 0.05, 'z': z, 'rot': [-6.0, 0, 0],
                                                               'ground': '#D6CFC0', 'rough': 0.6}]}, None)
            s = xa + 0.003
            while s < xb - 0.006:
                t = rnd.uniform(0.003, 0.0045)
                box(s, s + t, yf + 0.09, yb - 0.004, z, z + 0.314, mat(rnd.choice(['#D9D3C4', '#141414', '#D6C8A6', '#22356F', '#6E1F2B']), 0.6))
                s += t + 0.0005
    me = bpy.data.meshes.new(f'{name}-other'); bm.to_mesh(me); bm.free()
    for m in used:
        me.materials.append(m)
    ob = bpy.data.objects.new(f'{name}-other', me); bpy.context.scene.collection.objects.link(ob)
    return objs + [ob]
