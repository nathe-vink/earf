"""Support check (2026-11-25, the bar's Mantle off the counter's back edge): for each product block and each set prop,
what it stands on, by ray casts down from just under its lowest point.

For a group (a product block's objects, or a prop's), its footprint is the convex hull of all its vertices seen from
above, and its contact is the vertices within 3 mm of its lowest point. A sample grid (1 cm) over the footprint and every
contact vertex is cast straight down from 0.1 mm under the lowest point; a sample is supported when it hits a surface
within 5 mm. Reported per group: its lowest z, what it stands on, the share of contact and of footprint supported, the
largest overhang (how far an unsupported footprint sample lies from the nearest supported one), and the edge margin
(how far the footprint's outline can grow, in 1 cm steps up to 10 cm, and still have support under every point of it).
A group whose lowest point has nothing within 5 mm under it (a hanging lamp, a wall board) is listed as not standing.

    python3 studio/engine/render.py SHOT.json --support --out OUT.png     (writes OUT.support.json; no render)"""
import math, re

GAP = 0.005          # a sample within 5 mm of a surface below is supported
LIFT = 0.004         # casts start 4 mm over the lowest point, so a base sitting exactly on a top (or sunk up to 4 mm) finds it
SINK = 0.0015        # sunk deeper than this is a fault too (it reads as a thing set into the surface)
CONTACT = 0.003      # the contact: vertices within 3 mm of the lowest point
STEP = 0.01          # the footprint's sample grid
MARGIN_MAX = 0.10    # the edge margin is searched up to 10 cm


def _verts(objs):
    out = []
    for o in objs:
        if o.type != 'MESH' or not o.data or not len(o.data.vertices):
            continue
        mw = o.matrix_world
        out += [mw @ v.co for v in o.data.vertices]
    return out


def _hull(pts):
    """Convex hull of 2D points (monotone chain), counter-clockwise."""
    pts = sorted(set((round(p[0], 5), round(p[1], 5)) for p in pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _inside(h, x, y):
    n = len(h)
    for i in range(n):
        (x0, y0), (x1, y1) = h[i], h[(i + 1) % n]
        if (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0) < -1e-9:
            return False
    return True


_TREE = {}


def _tree(bpy):
    """One BVH tree of every renderable mesh in the scene (world space, evaluated), built once, and each triangle's
    object: scene.ray_cast rebuilds its tree on every call, hours for a room."""
    if 'bvh' in _TREE:
        return _TREE['bvh'], _TREE['owner']
    from mathutils.bvhtree import BVHTree
    dg = bpy.context.evaluated_depsgraph_get()
    V, T, owner = [], [], []
    for o in bpy.data.objects:
        if o.type != 'MESH' or o.hide_render or o.get('engine_light') or o.get('engine_light_body'):
            continue
        oe = o.evaluated_get(dg)
        try:
            me = oe.to_mesh()
        except RuntimeError:
            continue
        me.calc_loop_triangles()
        mw = oe.matrix_world; b = len(V)
        V += [mw @ v.co for v in me.vertices]
        for t in me.loop_triangles:
            T.append((t.vertices[0] + b, t.vertices[1] + b, t.vertices[2] + b)); owner.append(o.name)
        oe.to_mesh_clear()
    _TREE['bvh'] = BVHTree.FromPolygons(V, T, all_triangles=True); _TREE['owner'] = owner
    return _TREE['bvh'], owner


def _cast(bpy, scene, own, x, y, z):
    """The first surface straight down from (x, y, z) that is not the group's own: (gap, object name) or (None, None)."""
    from mathutils import Vector
    bvh, owner = _tree(bpy)
    o = Vector((x, y, z)); d = Vector((0, 0, -1))
    for _ in range(16):
        loc, _n, idx, dist = bvh.ray_cast(o, d, 0.5)
        if loc is None:
            return None, None
        if owner[idx] not in own:
            return z - loc.z, owner[idx]
        o = Vector((x, y, loc.z - 1e-5))
    return None, None


def check(bpy, scene, groups):
    """groups: [(label, [objects])]. Returns one dict per group."""
    res = []
    for label, objs in groups:
        vs = _verts(objs)
        if not vs:
            continue
        own = {o.name for o in objs}
        z0 = min(v.z for v in vs); zc = z0 + LIFT
        h = _hull([(v.x, v.y) for v in vs])
        if len(h) < 3:
            continue
        contact = [(v.x, v.y) for v in vs if v.z < z0 + CONTACT]
        if len(contact) > 400:
            contact = contact[::len(contact) // 400 + 1]
        on = {}; gaps = []
        def sup(x, y):
            g, nm = _cast(bpy, scene, own, x, y, zc)
            if g is not None:
                g -= LIFT                                    # the gap from the lowest point; negative: sunk into it
                gaps.append((g, nm))
            ok = g is not None and -SINK <= g <= GAP
            if ok:
                on[nm] = on.get(nm, 0) + 1
            return ok
        c_ok = [sup(x, y) for x, y in contact]
        xs = [p[0] for p in h]; ys = [p[1] for p in h]
        grid = [(x0 + STEP / 2 + i * STEP, y0 + STEP / 2 + j * STEP)
                for x0, y0 in [(min(xs), min(ys))]
                for i in range(int((max(xs) - x0) / STEP) + 1) for j in range(int((max(ys) - y0) / STEP) + 1)]
        grid = [p for p in grid if _inside(h, *p)] or [((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)]
        g_ok = [sup(x, y) for x, y in grid]
        good = [p for p, k in zip(grid, g_ok) if k]; bad = [p for p, k in zip(grid, g_ok) if not k]
        over = max((min(math.hypot(b[0] - g[0], b[1] - g[1]) for g in good) for b in bad), default=0.0) if good else None
        # the edge margin: the outline pushed out along each edge's outward normal (samples every 2 cm on each edge)
        margin = None
        if all(g_ok):
            edge = []
            n = len(h)
            for i in range(n):
                (ax, ay), (bx, by) = h[i], h[(i + 1) % n]
                L = math.hypot(bx - ax, by - ay)
                if L < 1e-6:
                    continue
                nx, ny = (by - ay) / L, -(bx - ax) / L        # outward for a counter-clockwise hull
                for k in range(int(L / 0.02) + 1):
                    t = min(1.0, k * 0.02 / L)
                    edge.append((ax + t * (bx - ax), ay + t * (by - ay), nx, ny))
            margin = 0.0
            for s in range(1, int(MARGIN_MAX / STEP) + 1):
                d = s * STEP
                if all((lambda r: r[0] is not None and -SINK <= r[0] - LIFT <= GAP)(_cast(bpy, scene, own, x + d * nx, y + d * ny, zc)) for x, y, nx, ny in edge):
                    margin = d
                else:
                    break
        top = sorted(on.items(), key=lambda kv: -kv[1])[:3]
        res.append({'group': label, 'z_min': round(z0, 4),
                    'footprint_xy': [[round(min(xs), 3), round(min(ys), 3)], [round(max(xs), 3), round(max(ys), 3)]],
                    'standing': any(c_ok),
                    'gap_below_m': round(min(gaps)[0], 4) if gaps else None, 'below': min(gaps)[1] if gaps else None,
                    'sunk_m': round(-min(gaps)[0], 4) if gaps and min(gaps)[0] < -SINK else 0.0,
                    'on': [nm for nm, _ in top],
                    'contact_supported': round(sum(c_ok) / len(c_ok), 3),
                    'footprint_supported': round(sum(g_ok) / len(g_ok), 3),
                    'overhang_m': None if over is None else round(over, 3),
                    'edge_margin_m': margin if margin is None else round(margin, 3),
                    'margin_capped': margin is not None and margin >= MARGIN_MAX - 1e-9})
    return res


def split(label, objs, pad=0.02):
    """A product block's objects split into the pieces that stand apart (bounding boxes, grown by `pad`, that touch):
    each instance of a pair on its own."""
    from mathutils import Vector
    bb = []
    for o in objs:
        if o.type != 'MESH':
            bb.append(None); continue
        ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
        bb.append(([min(w[i] for w in ws) - pad for i in range(3)], [max(w[i] for w in ws) + pad for i in range(3)]))
    par = list(range(len(objs)))
    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    idx = [i for i, b in enumerate(bb) if b]
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            (l1, h1), (l2, h2) = bb[idx[a]], bb[idx[b]]
            if all(l1[k] <= h2[k] and l2[k] <= h1[k] for k in range(3)):
                par[f(idx[a])] = f(idx[b])
    cl = {}
    for i in idx:
        cl.setdefault(f(i), []).append(objs[i])
    parts = sorted(cl.values(), key=lambda g: (min((o.matrix_world.translation.x for o in g)), len(g)))
    if all(len(g) == 1 for g in parts):                 # one object per piece (a board each): every piece its own
        return [(f'{label} #{i} {g[0].name}' if len(parts) > 1 else label, g) for i, g in enumerate(parts)]
    big = [g for g in parts if len(g) > 1 or len(parts) == 1]
    small = [g for g in parts if not (len(g) > 1 or len(parts) == 1)]
    # a lone piece (a screw) joins the nearest larger piece
    for g in small:
        c = g[0].matrix_world.translation
        best = min(big, key=lambda G: min((o.matrix_world.translation - c).length for o in G)) if big else None
        if best is not None:
            best.extend(g)
        else:
            big.append(g)
    return [(f'{label} #{i}' if len(big) > 1 else label, g) for i, g in enumerate(big)]


def groups_from_scene(bpy, product_groups, skip_props=(), props=None):
    """The product blocks as given, and each set prop's objects (tagged engine_prop by sets.props), a prop that builds
    many things (an ext: the lamps, the boards) split into its separate pieces; props in `skip_props` (the room, the
    record wall: the surfaces themselves) are not checked. Objects no prop made (templates, lamps) are left out."""
    by = {}
    for o in bpy.data.objects:
        if o.type != 'MESH' or o.hide_render or 'engine_prop' not in o:
            continue
        i = int(o['engine_prop'])
        if i in skip_props:
            continue
        by.setdefault(i, []).append(o)
    out = list(product_groups)
    for i in sorted(by):
        p = (props or [None] * (i + 1))[i] if props and i < len(props) else None
        lbl = f'prop{i} ' + ((p.get('fn') or p.get('shape') or p.get('kind')) if p else '')
        if (p or {}).get('fn') == 'boards':                 # each sleeve, card and paper on its own
            out += [(f'{lbl.strip()} {o.name}', [o]) for o in sorted(by[i], key=lambda o: o.name)]
        else:
            out += split(lbl.strip(), by[i]) if (p or {}).get('shape') == 'ext' else [(lbl.strip(), by[i])]
    return out
