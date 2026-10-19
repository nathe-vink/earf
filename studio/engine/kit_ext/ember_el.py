"""Ember's own pieces for round 31b (spinoffs/barkhorn/elements/ember.py): a lava field as one piece of ground.

    {"kind": "kit", "shape": "ext", "module": "ember_el", "fn": "terrain", ...}

terrain: one heightfield of rock, `size` [w, d] metres centred on `position`, `cell` metres between vertices, laid with
a photographed rock texture (`rock`, a Poly Haven id, true displacement `displace`), with:
- `relief`: broad undulation (metres), fading to level ground within `flat` [x, y, r] (where the product stands);
- `cliff`: {"y0", "rise", "height", "rough"}: the ground rising behind y0 over `rise` metres to `height`, broken up by
  noise `rough` metres (a crater wall, a lava-field scarp);
- `channels`: [{"points": [[x, y], ...], "width", "depth", "bank", "lava": "flow"|"pool"}]: rivers carved into the rock,
  their floors level at -depth, their banks rounded over `bank` metres; their floors take the lava material;
- `pools`: [[x, y, r, depth], ...]: round pools of lava, the same way;
- `falls`: [{"points": [[x, y], ...], "width", "notch"}]: notches cut `notch` deep into the cliff's face along a path
  from its top down to a channel; their faces take the molten lava material (a lava fall).
Materials: `rock` (+ `rock_res`, `rock_tint`, `rock_tint_mix`), `flow` (an ambientCG lava id, its emission map glowing at
`flow_emit`, tiles `flow_scale` metres) and `molten` (`molten_emit`, `molten_scale`).
"""
import math

import numpy as np
from mathutils import Vector, noise


def _seg_dist(px, py, pts):
    """Distance from points (arrays) to a polyline, and the parameter along it (0 to 1)."""
    best = np.full(px.shape, 1e9); tpar = np.zeros(px.shape)
    L = [0.0]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L.append(L[-1] + math.hypot(bx - ax, by - ay))
    for i, ((ax, ay), (bx, by)) in enumerate(zip(pts, pts[1:])):
        dx, dy = bx - ax, by - ay
        l2 = dx * dx + dy * dy or 1e-9
        t = np.clip(((px - ax) * dx + (py - ay) * dy) / l2, 0, 1)
        d = np.hypot(px - (ax + t * dx), py - (ay + t * dy))
        m = d < best
        best = np.where(m, d, best)
        tpar = np.where(m, (L[i] + t * math.sqrt(l2)) / L[-1], tpar)
    return best, tpar


def _smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def _fbm(x, y, scale, octaves=4, seed=0.0):
    out = np.zeros(x.shape)
    amp, f = 1.0, 1.0 / scale
    flat_x, flat_y = x.ravel(), y.ravel()
    for o in range(octaves):
        vals = np.fromiter((noise.noise(Vector((a * f, b * f, seed + o * 7.31))) for a, b in zip(flat_x, flat_y)),
                           float, flat_x.size)
        out += amp * vals.reshape(x.shape)
        amp *= 0.5; f *= 2.0
    return out


LAVA_RAMP = [(0.0, '#000000'), (0.3, '#200100'), (0.5, '#B01800'), (0.72, '#FF5A06'), (0.86, '#FFB040'),
             (1.0, '#FFE6A8')]


def _lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def lava_material(bpy, aid='acg:Lava004', res='2k', scale=2.0, strength=4.0, crust=0.08, ramp=None, gain=1.0,
                  coords='Object', name='lava', rough=None, specular=None):
    """Lava from an ambientCG set, with its colour held: the set's emission map's brightness drives a ramp from black
    crust through deep red and orange to a yellow-white core (`ramp` [(pos, hex), ...], the brightness times `gain`),
    emitted at `strength`; the crust's own colour map, darkened to `crust`, is all that reflects (so lamps near the lava
    light the rock, not a pink lava). Normal and roughness from the set."""
    import assets
    maps = assets.ambientcg(aid[4:] if aid.startswith('acg:') else aid, res.upper())
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    sc = scale if isinstance(scale, (list, tuple)) else (scale,) * 3     # per axis: stretch a fall's texture along z
    mp.inputs['Scale'].default_value = tuple(1.0 / v for v in sc)
    nt.links.new(tc.outputs['UV' if coords == 'UV' else 'Object'], mp.inputs['Vector'])

    def tex(key, colour):
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(maps[key], check_existing=True)
        n.image.colorspace_settings.name = 'sRGB' if colour else 'Non-Color'
        n.projection = 'BOX' if coords != 'UV' else 'FLAT'; n.projection_blend = 0.25
        nt.links.new(mp.outputs['Vector'], n.inputs['Vector']); return n
    d = tex('diff', True)
    dark = nt.nodes.new('ShaderNodeMix'); dark.data_type = 'RGBA'; dark.blend_type = 'MULTIPLY'
    dark.inputs['Factor'].default_value = 1.0; dark.inputs['B'].default_value = (crust, crust * 0.8, crust * 0.7, 1.0)
    nt.links.new(d.outputs['Color'], dark.inputs['A']); nt.links.new(dark.outputs['Result'], bs.inputs['Base Color'])
    e = tex('emit', True)
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(e.outputs['Color'], bw.inputs['Color'])
    g = nt.nodes.new('ShaderNodeMath'); g.operation = 'MULTIPLY'; g.inputs[1].default_value = gain; g.use_clamp = True
    nt.links.new(bw.outputs['Val'], g.inputs[0])
    cr = nt.nodes.new('ShaderNodeValToRGB'); els = cr.color_ramp.elements
    pts = ramp or LAVA_RAMP
    els[0].position, els[0].color = pts[0][0], _lin(pts[0][1])
    els[1].position, els[1].color = pts[-1][0], _lin(pts[-1][1])
    for pos, hx in pts[1:-1]:
        el = els.new(pos); el.color = _lin(hx)
    nt.links.new(g.outputs['Value'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = strength
    if rough is not None:                                         # a matte crust: cooled lava is not glassy
        bs.inputs['Roughness'].default_value = rough
    elif 'rough' in maps:
        nt.links.new(tex('rough', False).outputs['Color'], bs.inputs['Roughness'])
    if specular is not None and 'Specular IOR Level' in bs.inputs:
        bs.inputs['Specular IOR Level'].default_value = specular
    if 'nor_gl' in maps:
        nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(tex('nor_gl', False).outputs['Color'], nm.inputs['Color'])
        nt.links.new(nm.outputs['Normal'], bs.inputs['Normal'])
    return m


def fall(bpy, name, p, kit):
    """A lava fall: a ribbon (kit's tube: `points`, `radius`, `flat`) of molten lava (lava_material: `lava`, `scale`,
    `strength`, `gain`), its texture running down it."""
    import bmesh
    bm = bmesh.new()
    kit._tube(bm, p['points'], p.get('radius', 0.3), p.get('flat', 0.25), 0.0, p.get('sides', 20), p.get('samples', 12))
    # `tex_scale`: the texture's tile; a bare `scale` (kept for concept A) also scales the object in kit.finish
    mat = lava_material(bpy, p.get('lava', 'acg:Lava004'), p.get('lava_res', '2k'), p.get('tex_scale', p.get('scale', 1.2)),
                        p.get('strength', 4.0), gain=p.get('gain', 1.0), ramp=p.get('ramp'), name=f'{name}-lava',
                        rough=p.get('crust_rough'), specular=p.get('crust_spec'))
    return kit.finish(bpy, name, bm, p, mat=mat)


def darken(m, albedo):
    """Scale a material's base colour by `albedo` (a photographed rock set is mid-grey; basalt is near-black, ~0.04):
    a multiply between whatever feeds the Principled BSDF's Base Color and the socket."""
    nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    sock = bs.inputs['Base Color']
    if not sock.links:
        return m
    src = sock.links[0].from_socket
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0; mul.inputs['B'].default_value = (albedo, albedo, albedo, 1.0)
    nt.links.new(src, mul.inputs['A']); nt.links.new(mul.outputs['Result'], sock)
    return m


def terrain(bpy, name, p, kit):
    import assets
    w, d = p.get('size', [16.0, 16.0])
    cx, cy, cz = p.get('position', [0.0, 0.0, 0.0])
    cell = p.get('cell', 0.025)
    nx, ny = int(w / cell) + 1, int(d / cell) + 1
    xs = np.linspace(cx - w / 2, cx + w / 2, nx); ys = np.linspace(cy - d / 2, cy + d / 2, ny)
    X, Y = np.meshgrid(xs, ys)
    # broad relief, level where the product stands
    fx, fy, fr = p.get('flat', [0.0, 0.0, 0.8])
    level = _smooth(fr, fr * 2.2, np.hypot(X - fx, Y - fy))
    Z = p.get('relief', 0.08) * _fbm(X, Y, 2.5, 4, 1.0) * level
    # pahoehoe: ropes and folds across the flow, in patches, as cooling skin wrinkles
    rp = p.get('ropes')
    if rp:
        a = math.radians(rp.get('dir', 0.0))
        u = X * math.cos(a) + Y * math.sin(a)                       # along the flow
        v = -X * math.sin(a) + Y * math.cos(a)
        bend = 0.25 * _fbm(X, Y, 1.0, 2, 31.0)                      # the ropes arc, as lobes do
        ropes = np.sin(2 * math.pi * (u + bend + 0.08 * v * v / max(rp.get('lobe', 1.0), 1e-3)) / rp.get('wave', 0.12))
        patch = np.clip(0.5 + 1.5 * _fbm(X, Y, 1.6, 2, 37.0), 0, 1)
        Z = Z + rp.get('amp', 0.015) * ropes * patch * level
        # lobes: the flow's toes, bulging plates of a few centimetres
        Z = Z + rp.get('lobes', 0.06) * np.clip(_fbm(X, Y, 0.7, 3, 41.0), 0, None) * level
    # the cliff behind
    c = p.get('cliff')
    if c:
        rise = _smooth(c['y0'], c['y0'] + c['rise'], Y + 0.6 * _fbm(X, Y, 3.0, 2, 5.0))
        zc = rise * (c['height'] + c.get('rough', 0.4) * _fbm(X, Y, 1.2, 5, 9.0))
        if c.get('layers'):                                       # stacked flows: ledges and steep risers
            L = c['layers'] * (1 + 0.15 * _fbm(X, Y, 6.0, 2, 11.0))
            k = zc / L
            fl = np.floor(k); fr = k - fl
            zc = (fl + _smooth(c.get('riser', 0.65), 1.0, fr)) * L
        Z = Z + zc
    # volcanic cones: [x, y, r, h, crater_r] smooth shoulders, a crater cut in the top
    for (vx, vy, vr, vh, cr) in p.get('cones', []):
        d = np.hypot(X - vx, Y - vy) * (1 + 0.08 * _fbm(X, Y, 4.0, 3, 51.0))
        cone = vh * (1 - _smooth(0.0, vr, d)) ** 1.6
        if cr:
            cone = cone - 0.35 * vh * (1 - _smooth(cr * 0.6, cr, d))
        Z = Z + cone
    lava = np.zeros(X.shape, dtype=np.int8)                 # 0 rock, 1 flow, 2 molten
    for ch in p.get('channels', []):
        dist, _ = _seg_dist(X, Y, ch['points'])
        wd = ch['width'] * (1 + 0.25 * _fbm(X, Y, 1.5, 2, 13.0))
        s = _smooth(wd, wd + ch.get('bank', 0.25), dist)
        Z = np.minimum(Z, -ch['depth'] * (1 - s) + Z * s)
        if not p.get('lava_below'):
            lava = np.where((dist < wd) & (lava == 0), 1 if ch.get('lava', 'flow') == 'flow' else 2, lava)
    for (px, py, r, dep) in p.get('pools', []):
        dist = np.hypot(X - px, Y - py) * (1 + 0.15 * _fbm(X, Y, 0.8, 2, 17.0))
        s = _smooth(r, r + 0.3, dist)
        Z = np.minimum(Z, -dep * (1 - s) + Z * s)
        if not p.get('lava_below'):
            lava = np.where(dist < r, 2, lava)
    for f in p.get('falls', []):
        dist, _ = _seg_dist(X, Y, f['points'])
        wd = f['width'] * (1 + 0.3 * _fbm(X, Y, 0.7, 2, 21.0))
        s = _smooth(wd, wd + 0.2, dist)
        Z = Z - f.get('notch', 0.15) * (1 - s)
        lava = np.where(dist < wd, 2, lava)
    Z = Z + cz
    # the mesh
    verts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    idx = np.arange(nx * ny).reshape(ny, nx)
    a, b, c2, d2 = idx[:-1, :-1].ravel(), idx[:-1, 1:].ravel(), idx[1:, 1:].ravel(), idx[1:, :-1].ravel()
    faces = np.column_stack([a, b, c2, d2])
    lf = np.maximum.reduce([lava[:-1, :-1].ravel(), lava[:-1, 1:].ravel(), lava[1:, 1:].ravel(), lava[1:, :-1].ravel()])
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.astype(np.float32).ravel())
    me.loops.add(faces.size); me.loops.foreach_set('vertex_index', faces.astype(np.int32).ravel())
    me.polygons.add(len(faces))
    me.polygons.foreach_set('loop_start', (np.arange(len(faces)) * 4).astype(np.int32))
    me.polygons.foreach_set('loop_total', np.full(len(faces), 4, dtype=np.int32))
    me.polygons.foreach_set('material_index', lf.astype(np.int32))
    me.polygons.foreach_set('use_smooth', np.ones(len(faces), dtype=bool))
    me.update(calc_edges=True); me.validate()
    res = p.get('res', '2k')
    me.materials.append(assets.pbr(bpy, p.get('rock', 'dark_rock'), p.get('rock_res', res), scale=p.get('rock_scale'),
                                   displace=p.get('displace', 0.03), tint=p.get('rock_tint'),
                                   tint_mix=p.get('rock_tint_mix', 0.0), rough_mul=p.get('rough_mul', 1.0),
                                   name=f'{name}-rock'))
    if p.get('albedo'):
        darken(me.materials[0], p['albedo'])
    me.materials.append(lava_material(bpy, p.get('flow', 'acg:Lava001'), p.get('lava_res', res), p.get('flow_scale', 1.5),
                                      p.get('flow_emit', 4.0), gain=p.get('flow_gain', 1.0), name=f'{name}-flow'))
    me.materials.append(lava_material(bpy, p.get('molten', 'acg:Lava004'), p.get('lava_res', res), p.get('molten_scale', 2.0),
                                      p.get('molten_emit', 4.0), gain=p.get('molten_gain', 1.0), name=f'{name}-molten'))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


def columns(bpy, name, p, kit):
    """Basalt columns, packed as they crack in cooling lava: hexagonal prisms on a jittered hex grid over `area`
    [x0, y0, x1, y1], `r` metres across the flats (half), heights from `heights` [front, back] rising toward +y with
    noise `rough` (metres) and a stepped break (`steps`), each top tipped a little and its edges eased; skipping any
    within `gaps` [[x, y, r], ...] (where a lava fall pours through). One mesh, one photographed rock material."""
    import assets, bmesh, random
    rnd = random.Random(p.get('seed', 0))
    x0, y0, x1, y1 = p['area']
    r = p.get('r', 0.4)
    h0, h1 = p.get('heights', [1.5, 3.0])
    dx, dy = r * math.sqrt(3), r * 1.5
    bm = bmesh.new()
    row = 0
    y = y0
    while y <= y1:
        x = x0 + (row % 2) * dx / 2
        while x <= x1:
            jx, jy = rnd.uniform(-0.12, 0.12) * r, rnd.uniform(-0.12, 0.12) * r
            cxp, cyp = x + jx, y + jy
            if not any(math.hypot(cxp - gx, cyp - gy) < gr for gx, gy, gr in p.get('gaps', [])):
                t = (y - y0) / max(y1 - y0, 1e-6)
                h = h0 + (h1 - h0) * t + p.get('rough', 0.4) * noise.noise(Vector((cxp * 0.6, cyp * 0.6, 3.3)))
                if p.get('steps'):
                    h = round(h / p['steps']) * p['steps'] + rnd.uniform(-0.06, 0.06)
                rr = r * rnd.uniform(*p.get('r_jitter', [0.9, 1.0]))
                a0 = rnd.uniform(-0.15, 0.15)
                tx, ty = rnd.uniform(-0.08, 0.08), rnd.uniform(-0.08, 0.08)
                # the column as a stack of segments: basalt cracks across as well as along (cross-joints), each
                # segment shifted and turned a little, its ends chamfered by the bevel below
                z = -0.3
                hh = max(0.05, h)
                while z < hh - 0.02:
                    seg = rnd.uniform(*p.get('joints', [0.35, 0.9]))
                    zt = min(hh, z + seg) if hh - (z + seg) > 0.15 else hh
                    ox, oy, da = rnd.uniform(-0.012, 0.012), rnd.uniform(-0.012, 0.012), rnd.uniform(-0.03, 0.03)
                    bot, top = [], []
                    for k in range(6):
                        a = a0 + da + math.pi / 6 + k * math.pi / 3
                        vx, vy = rr * math.cos(a) * rnd.uniform(0.96, 1.0), rr * math.sin(a) * rnd.uniform(0.96, 1.0)
                        bot.append(bm.verts.new((cxp + ox + vx, cyp + oy + vy, z + 0.004)))
                        tz = zt + (tx * vx + ty * vy if zt >= hh else 0.0)
                        top.append(bm.verts.new((cxp + ox + vx, cyp + oy + vy, tz)))
                    for k in range(6):
                        bm.faces.new((bot[k], bot[(k + 1) % 6], top[(k + 1) % 6], top[k]))
                    bm.faces.new(top); bm.faces.new(bot[::-1])
                    z = zt
            x += dx
        y += dy; row += 1
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=p.get('ease', 0.03), segments=2, affect='EDGES', clamp_overlap=True)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(assets.pbr(bpy, p.get('rock', 'dark_rock_02'), p.get('res', '2k'), scale=p.get('rock_scale'),
                                   displace=p.get('displace', 0.02), tint=p.get('tint'), tint_mix=p.get('tint_mix', 0.0),
                                   rough_mul=p.get('rough_mul', 1.0), name=f'{name}-rock'))
    if p.get('albedo'):
        darken(me.materials[0], p['albedo'])
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return [ob]


def lava_surface(bpy, name, p, kit):
    """A level surface of lava under carved rock (terrain with `lava_below`): `size` [w, d] at `position`, gently
    domed and rippled (`ripple` metres), so the rock's own banks make its shorelines where they dip below it."""
    import bmesh
    w, d = p.get('size', [10.0, 10.0]); cell = p.get('cell', 0.05)
    nx, ny = int(w / cell), int(d / cell)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=nx, y_segments=ny, size=0.5)
    rip = p.get('ripple', 0.01)
    for v in bm.verts:
        v.co.x *= w; v.co.y *= d
        v.co.z = rip * noise.noise(Vector((v.co.x * 1.3, v.co.y * 1.3, 2.2)))
    mat = lava_material(bpy, p.get('lava', 'acg:Lava001'), p.get('lava_res', '2k'), p.get('tex_scale', p.get('scale', 1.5)),
                        p.get('strength', 8.0), gain=p.get('gain', 1.0), crust=p.get('crust', 0.08), ramp=p.get('ramp'),
                        name=f'{name}-lava',
                        rough=p.get('crust_rough'), specular=p.get('crust_spec'))
    return kit.finish(bpy, name, bm, p, mat=mat)


def sparks(bpy, name, p, kit):
    """Sparks lifting off lava, as a camera at 1/30 s sees them: short glowing streaks along rising, drifting paths,
    `count` of them over `area` [x0, y0, x1, y1] (where the lava is), most low and near the heat, a few high; sizes
    varied, lengths `streak` [min, max] metres, `emit` their strength, `color`."""
    import bmesh, random
    from mathutils import Matrix
    rnd = random.Random(p.get('seed', 1))
    x0, y0, x1, y1 = p['area']
    bm = bmesh.new()
    for _ in range(p.get('count', 60)):
        h = p.get('height', 2.5) * rnd.random() ** 2.2
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        lx, ly = p.get('drift', [0.3, 0.1])
        c = Vector((x + lx * h * h * 0.3 + 0.15 * math.sin(h * 3 + x), y + ly * h * h * 0.3, 0.05 + h))
        dirv = Vector((lx * h * 0.6 + rnd.uniform(-0.3, 0.3), ly * h * 0.6 + rnd.uniform(-0.3, 0.3), 1.0)).normalized()
        L = rnd.uniform(*p.get('streak', [0.01, 0.06])) * (1.0 - 0.5 * h / max(p.get('height', 2.5), 1e-3))
        r = rnd.uniform(*p.get('radius', [0.0008, 0.0025]))
        geom = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=r * 0.6, radius2=r, depth=L)
        rot = dirv.to_track_quat('Z', 'Y').to_matrix()
        bmesh.ops.rotate(bm, verts=geom['verts'], cent=Vector((0, 0, 0)), matrix=rot)
        bmesh.ops.translate(bm, vec=c, verts=geom['verts'])
    q = {**p, 'material': 'glow', 'color': p.get('color', '#FF8A30'), 'emit': p.get('emit', 25.0), 'shadow': False}
    q.pop('position', None)
    return kit.finish(bpy, name, bm, q, mat=kit.piece_material(bpy, q))


def sparks_mixed(bpy, name, p, kit):
    """Sparks in three generations: a few young bright yellow ones, more orange, and dim deep-red ones dying, each set
    its own `sparks` piece with its share of `count` and its own seed."""
    out = []
    for i, (share, col, emit, scale) in enumerate(((0.2, '#FF9A30', 1.2, 1.3), (0.45, '#FF6A18', 1.0, 1.0),
                                                   (0.35, '#E0300A', 0.45, 0.7))):
        q = {**p, 'count': max(1, int(p.get('count', 40) * share)), 'color': col, 'emit': p.get('emit', 20.0) * emit,
             'seed': p.get('seed', 1) * 10 + i,
             'streak': [v * scale for v in p.get('streak', [0.01, 0.06])]}
        out += sparks(bpy, f'{name}-{i}', q, kit)
    return out


def steam(bpy, name, p, kit):
    """Steam over lava: a box (`box` [x0, y0, z0, x1, y1, z1]) of scattering volume whose density is billowing noise
    (`scale` metres), thinning with height and toward the box's sides, so it has no edges; `density` at its thickest,
    `color`, `anisotropy`."""
    import bmesh
    x0, y0, z0, x1, y1, z1 = p['box']
    bm = bmesh.new()
    geom = bmesh.ops.create_cube(bm, size=1.0)
    for v in geom['verts']:
        v.co = Vector(((v.co.x + 0.5) * (x1 - x0) + x0, (v.co.y + 0.5) * (y1 - y0) + y0, (v.co.z + 0.5) * (z1 - z0) + z0))
    m = bpy.data.materials.new(f'{name}-steam'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = _lin(p.get('color', '#FFFFFF'))
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.4)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('scale', 0.8)
    nz.inputs['Detail'].default_value = 6.0
    if 'Roughness' in nz.inputs:
        nz.inputs['Roughness'].default_value = 0.6
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    # billows: noise pushed through a ramp so it has gaps; times a falloff from the box's centre line and with height
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.45; cr.color_ramp.elements[1].position = 0.75
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
    gen = nt.nodes.new('ShaderNodeTexGradient'); gen.gradient_type = 'SPHERICAL'
    mp = nt.nodes.new('ShaderNodeMapping')
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, z0
    mp.inputs['Location'].default_value = (-cx, -cy, -cz)
    mp.inputs['Scale'].default_value = (2.0 / (x1 - x0), 2.0 / (y1 - y0), 1.0 / (z1 - z0))
    tcw = nt.nodes.new('ShaderNodeTexCoord')
    nt.links.new(tcw.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], gen.inputs['Vector'])
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    nt.links.new(cr.outputs['Color'], mul.inputs[0]); nt.links.new(gen.outputs['Fac'], mul.inputs[1])
    dens = nt.nodes.new('ShaderNodeMath'); dens.operation = 'MULTIPLY'; dens.inputs[1].default_value = p.get('density', 0.3)
    nt.links.new(mul.outputs['Value'], dens.inputs[0]); nt.links.new(dens.outputs['Value'], vol.inputs['Density'])
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    q = {**p}; q.pop('position', None)
    return kit.finish(bpy, name, bm, q, smooth=False, mat=m)


def basalt(bpy, m, albedo=0.12, saturation=0.25, rough_mul=1.0):
    """A copy of a scanned rock's material regraded to black basalt: its colour desaturated to `saturation` and scaled
    to `albedo`, its roughness scaled by `rough_mul`; the scan's own detail (colour variation, normal, roughness) stays."""
    m = m.copy(); nt = m.node_tree
    bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bs is None:
        return m
    sock = bs.inputs['Base Color']
    if sock.links:
        src = sock.links[0].from_socket
        hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = saturation
        nt.links.new(src, hs.inputs['Color'])
        mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
        mul.inputs['Factor'].default_value = 1.0; mul.inputs['B'].default_value = (albedo, albedo, albedo, 1.0)
        nt.links.new(hs.outputs['Color'], mul.inputs['A']); nt.links.new(mul.outputs['Result'], sock)
    else:
        c = sock.default_value
        sock.default_value = (c[0] * albedo, c[1] * albedo, c[2] * albedo, 1.0)
    r = bs.inputs['Roughness']
    if rough_mul != 1.0:
        mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = rough_mul
        mm.use_clamp = True
        if r.links:
            nt.links.new(r.links[0].from_socket, mm.inputs[0])
        else:
            mm.inputs[0].default_value = r.default_value
        nt.links.new(mm.outputs['Value'], r)
    return m


def rock(bpy, name, p, kit):
    """A scanned rock (Poly Haven `model`), placed by `position`, `rotate` (degrees) and `scale`, its materials regraded
    to basalt (`albedo`, `saturation`, `rough_mul`)."""
    import assets
    root = assets.place(bpy, p['model'], p.get('res', '2k'), tuple(p.get('position', [0, 0, 0])),
                        tuple(p.get('rotate', [0, 0, 0])), p.get('scale', 1.0), name)
    done = {}
    stack = [root]
    while stack:
        o = stack.pop(); stack += list(o.children)
        if o.type == 'MESH':
            for i, m in enumerate(o.data.materials):
                if m is None:
                    continue
                if m.name not in done:
                    done[m.name] = basalt(bpy, m, p.get('albedo', 0.12), p.get('saturation', 0.25), p.get('rough_mul', 1.0))
                o.data.materials[i] = done[m.name]
    return [root]


def rubble(bpy, name, p, kit):
    """Scanned rocks scattered over `area` [x0, y0, x1, y1] (`models`, `count`, `scale` [min, max], `avoid`, `seed`,
    sunk `z`, tilted at random up to `tilt_deg`), their materials regraded to basalt (`albedo`, `saturation`,
    `rough_mul`): clinker and slabs on a lava field."""
    import assets
    made = assets.scatter(bpy, p['models'], p.get('res', '1k'), p.get('count', 20), tuple(p['area']),
                          [tuple(a) for a in p.get('avoid', [])], tuple(p.get('scale', [0.5, 1.5])), p.get('z', 0.0),
                          p.get('seed', 1), True, p.get('tilt_deg', 25.0))
    done = {}
    objs = list(made)
    for root in made:
        for o in [root] + list(root.children_recursive):
            if o.type == 'MESH':
                for i, m in enumerate(o.data.materials):
                    if m is None:
                        continue
                    if m.name not in done:
                        done[m.name] = basalt(bpy, m, p.get('albedo', 0.05), p.get('saturation', 0.1), p.get('rough_mul', 0.7))
                    o.data.materials[i] = done[m.name]
    return objs
