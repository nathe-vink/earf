"""An impact trench in a road (round 31b, Smoke E8: spinoffs/barkhorn/elements/smoke_impact.py; the owner, 2026-10-20:
"it looked like the speaker slid along the asphalt and ground it up, like an asteroid might").

trench: the gouge itself, a channel along +y from `y0` (the impact point, where it starts shallow) to `y1` (where the
speaker came to rest), `width` metres across its floor, its depth rising to `depth` within `ramp` metres of the impact
and holding, its walls ragged (`ragged` metres of noise), its floor a torn aggregate (`texture`), scorched darker toward
the speaker (`tint`, `tint_mix`). It is the surface the road's two slabs leave open between them.

slabs: the asphalt torn up along both lips: `count` fractured plates, each an irregular slab `thickness` thick, its top
the road's asphalt (`top`), its broken edges and underside the grey sub-base (`under`), heaved up and tilted outward off
the lip by up to `tilt` degrees, larger near the impact's deepest part. `seed`.

debris: chunks of asphalt and aggregate thrown forward and to the sides of the path: `count` of them, finer and sparser
with distance (`reach` metres), lying on the road at random tilt. `seed`.

The tints shift only hue and saturation, so a dark tint on the light aggregate stays light (E12r's proof: "pale cream
slabs, like concrete blocks dumped in a line"); `value` (trench), `top_value` and `under_value` (slabs, debris) scale
the brightness, 1 as before, and `under_tint` names the under face's tint (its brown read as red chips).

E12r's p3 critics: "procedural Voronoi fracture: flat slabs of nearly the same thickness and size, with clean flat faces
and crisp edges, laid in a tidy row", "broken edges would show black binder and grey aggregate over a lighter
crushed-stone layer". Off by default, so E8 renders as it did: `crumble` (slabs, debris) rounds every sharp edge over
`crumble` cm, so the edges catch the light as broken ones do, and lumps the faces by a fine noise; `side` (a texture)
gives the broken edges their own material, the asphalt's binder and stones (`side_value`), the underside staying the
sub-base; for slabs, `spread` how far out from the lip a plate lies (in its widths; 0.25 as before), `flip` the share
turned over onto their backs, `fallen` the share dropped into the trench, and `size_power` biases the sizes toward the
small (1 as before). `top_rough` and `side_rough` scale the roughness of the tops and the broken edges (0.45 and 0.8 as
before; E12r p5: "a glossy, slate-like sheen"). `flat_tops` keeps the crumble's tenting off the tops and undersides
(a road's surface stays flat; E12r p6's tented tops read as "crumpled paper"), and `smooth` shades smooth across edges
gentler than that many degrees (the tents and the jagged edges' facets read as crystals when flat-shaded). Debris's
`band` [y0, y1] strews it across the path between those, `inner` clear of the centre line on both sides. `rough`
(slabs, debris) breaks each piece's edges as a fracture does, uneven but whole (see _plate).

E12r p9 (the owner, 2026-10-22: "The chasm in the road is too linear on both sides. It needs to be more jagged or
crude, while maintaining realism"): `jag` (trench, slabs, road) tears each lip back from `lip` by up to `jag` metres
along an angular line of its own (`jag_seed`), with bites where chunks broke away, less near the impact and more round
the speaker; the trench's walls run up to it, the torn plates lie along it, and road: the deck either side as one
slab `thickness` thick out to `half` metres, open over the gouge along those lips, `ylo` to `yhi` along it, in the
road's material, so the deck's edge is the lip and nothing shows a ruled line.

E12r p10 (p9's notes check: "on the left they line up into a ruler-straight edge"; its critics: "nearly the same
thickness"): for slabs, `thick_var` varies each plate's thickness from (1 - thick_var / 2) to (1 + thick_var) times
`thickness`, and `clump` leaves gaps along each lip where a slow noise falls below `clump` - 0.35 (the row torn in
clumps) and throws the plates that remain out over a wider, uneven band. Both off by default. `drop` (slabs, debris)
lets each piece down onto the set built before it, its lowest corner a little into the surface below (see _drop).

E12r p11 (p10's critics, both: "nearly identical and almost cubic, with flat faces ... a narrow range of sizes", "no
grit, gravel or dust between the pieces", "a broken road comes up as thin, ragged plates"): `dust` (slabs, debris)
greys the faces that look up in drifts (see _dust); for debris, `flat` [lo, hi] its thickness against its size (0.3 to
0.6 as before), `size_power` its sizes from a power law (many small, a few large; uniform as before when left out),
`size_max` the largest (0.16 m as before) and `fine_size` the grit's range (5 to 30 mm as before); for the lips (jag),
`jag_base` and `jag_pow` each corner's tear, up to jag * jag_base with its share of small ones set by jag_pow (0.6 and
1.7 as before: p12's notes check, "the dark furrow on the left has a clean, straight edge"); `under_scale` the
sub-base's texture scale (0.35 as before: on a plate a foot across it read as one flat colour, "plank-like").

E12r p19 (p18, every critic: "flat tan patches with hard edges ... like decals"; hiding the trench took them away, so
they were its own faces): where a lip tore far back, the top 8 cm of the trench's wall is a long shallow slope, and the
asphalt course (`course`, `course_value`) covered all of it as one pale plane that no impact mark reaches (a mark takes
an object's first material). `course_steep` (trench, degrees) keeps the course to faces at least that steep, the broken
edge itself; the shallower ones take the floor's material and its marks. Off by default.

E12r p20 (p19's critic: "the beige fan of 'dust' left of the crater looks like a flat painted-on texture"; p18's: "no
depth, no stepped edge and no loose material in them"): that slope was two faces across, the floor's 28 columns
leaving each wall two. For trench, `wall_res` gives each wall that many columns of its own, closest at the lip; `step`
breaks the road's asphalt off sheer at the lip, that many metres of it, the wall below it the sub-base; `wall_rough`
lumps the sub-base in three sizes, up to that many metres. For debris, `patchy` [metres, lo, hi] keeps a piece where a
slow noise of that size runs above lo, surely above hi, so the rubble lies in drifts (p19: "the small pebbles ... spread
so evenly that they look computer-scattered"). All off by default."""
import math, random

import bmesh
from mathutils import Euler, Matrix, Vector, noise


def _mat(bpy, kit, texture, tex_scale, tint=None, tint_mix=0.0, rough=1.0, bump=1.5, value=1.0):
    return kit.piece_material(bpy, {'material': 'pbr', 'texture': texture, 'tex_scale': tex_scale, 'tint': tint,
                                    'tint_mix': tint_mix, 'rough_mul': rough, 'bump': bump, 'value': value})


_LIPS = {}


def _lipf(p):
    """The lips' line: the half-opening at road level on side s (+1 or -1) at y, `lip` torn back by up to `jag` metres
    along an angular line (corners every 0.12 to 0.55 m, a bite where a chunk broke away about one corner in six), a
    crumbled centimetre or two over it, less within `ramp` of the impact and more within 1.5 m of the end where the
    speaker stopped. Without `jag`, `lip` everywhere."""
    lip, jag = p.get('lip', 0.75), p.get('jag', 0.0)
    if not jag:
        return lambda y, s: lip
    y0, y1, ramp = p.get('y0', -20.0), p.get('y1', 0.0), p.get('ramp', 4.0)
    jb, jp = p.get('jag_base', 0.6), p.get('jag_pow', 1.7)       # each corner's tear: up to jag * jag_base, mostly small
    key = (lip, jag, y0, y1, ramp, p.get('jag_seed', 1), jb, jp)
    if key not in _LIPS:
        lines = {}
        for side in (-1, 1):
            rnd = random.Random(p.get('jag_seed', 1) * 1000 + side)
            ys, xs, y = [], [], y0 - 0.6
            while y < y1 + 0.6:
                f = min(1.0, max(0.0, (y - y0) / ramp)) ** 0.5 * (1.0 + 0.5 * max(0.0, 1.0 - (y1 - y) / 1.5))
                r = jag * (rnd.random() ** jp) * jb
                if rnd.random() < 0.17:                          # a chunk broken away
                    r = jag * rnd.uniform(0.75, 1.25)
                ys.append(y); xs.append(r * f)
                y += rnd.uniform(0.12, 0.55)
            lines[side] = (ys, xs, rnd.uniform(0, 100))
        _LIPS[key] = lines
    lines = _LIPS[key]

    def f(y, s):
        ys, xs, o = lines[1 if s > 0 else -1]
        k = max(0, min(len(ys) - 2, next((i for i in range(len(ys) - 1) if ys[i + 1] >= y), len(ys) - 2)))
        t = min(1.0, max(0.0, (y - ys[k]) / max(ys[k + 1] - ys[k], 1e-6)))
        crumb = 0.012 * noise.noise(Vector((y * 23.0, o, 0.5))) + 0.006 * noise.noise(Vector((y * 61.0, o, 1.5)))
        return lip + max(0.0, xs[k] + (xs[k + 1] - xs[k]) * t + crumb)
    return f


def trench(bpy, name, p, kit):
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    W, D = p.get('width', 1.0) / 2, p.get('depth', 0.35)
    ramp, rag = p.get('ramp', 4.0), p.get('ragged', 0.08)
    lip = p.get('lip', 0.75)                                   # half the opening at road level
    lipf = _lipf(p)
    sd = p.get('seed', 1) * 7.3
    ny = int((y1 - y0) / 0.06); nx = 28
    us = [-1.0 + 2.0 * i / nx for i in range(nx + 1)]           # across: -1 at one lip, +1 at the other
    wres, step, wrough = p.get('wall_res', 0), p.get('step', 0.0), p.get('wall_rough', 0.0)
    if wres:
        # E12r p20: each wall `wall_res` columns across, closest at the lip, where the floor's 28 left a torn-back wall
        # two faces wide (p19's critic: "the beige fan ... looks like a flat painted-on texture")
        a = W / lip
        floor = [u for u in us if abs(u) < a]
        wall = [a + (1.0 - a) * (1.0 - (1.0 - k / wres) ** 1.6) for k in range(wres + 1)]
        if step:
            wall = wall[:-1] + [1.0 - 0.012 * (1.0 - a), 1.0]  # the asphalt's own broken edge, nearly sheer
        us = [-w for w in wall[::-1]] + floor + wall
        nx = len(us) - 1
    bm = bmesh.new()
    rows = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        dep = D * min(1.0, (y - y0) / ramp) ** 0.7
        end = p.get('end', 0.0)
        if end and y > y1 - end:
            dep *= max(0.0, (y1 - y) / end) ** 0.8          # the gouge's end, where the speaker ploughed to rest
        row = []
        lips = (lipf(y, -1), lipf(y, 1))
        for i in range(nx + 1):
            u = us[i]
            # a U: flat floor across the width, walls rising to the lips, ragged where the slabs tore away
            w = abs(u)
            t = max(0.0, (w - W / lip) / (1.0 - W / lip)) if w >= W / lip else 0.0
            z = -dep * (1.0 if w < W / lip else max(0.0, 1.0 - t ** 1.5))
            if step and w >= W / lip and w < 0.9999:
                # E12r p20 (p18's critics: "no depth, no stepped edge"): the road's asphalt broken off sheer at the lip,
                # `step` metres of it, the wall below it the sub-base sloping down to the floor
                z = min(z, -min(step, dep)) if dep > 1e-3 else z
            x = u * lip
            if p.get('jag') and w >= W / lip:                   # the wall runs up to its torn lip, gentler where it tore back
                x = (1 if u > 0 else -1) * (W + (lips[1 if u > 0 else 0] - W) * t)
            n = noise.noise(Vector((x * 6.0 + sd, y * 3.0, 0.0)))
            near = min(1.0, (1.0 - t) / 0.15) if wres and p.get('jag') else 1.0   # the columns by the lip keep to it
            x += rag * n * (0.3 + w) * near * (0.0 if p.get('jag') and w > 0.999 else 1.0)
            z += 0.04 * noise.noise(Vector((x * 9.0, y * 9.0 + sd, 1.0))) * (dep / max(D, 1e-3))
            if wrough and 0.0 < t < 0.98:
                # the sub-base the slabs tore off: lumpy, in three sizes, nothing flat across it
                q = Vector((x, y, sd))
                z += wrough * (noise.noise(q * 7.0) + 0.5 * noise.noise(q * 19.0 + Vector((3.1, 0, 0)))
                               + 0.25 * noise.noise(q * 47.0 + Vector((0, 5.3, 0)))) * min(1.0, dep / max(D, 1e-3) * 2.0)
            # drag marks: grooves along the slide, sharp across it, long along it
            z -= p.get('grooves', 0.0) * abs(noise.noise(Vector((x * 14.0 + sd, y * 0.35, 2.0)))) * (dep / max(D, 1e-3))
            row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    steep = math.cos(math.radians(p['course_steep'])) if p.get('course_steep') else None
    for j in range(ny):
        for i in range(nx):
            f = bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
            # with `jag`, the asphalt course in section along the top of each wall (its 8 cm, binder and stones); with
            # `course_steep`, only where the wall is at least that steep (see the docstring)
            if p.get('jag') and f.calc_center_median().z > -0.08 and abs(0.5 * (us[i] + us[i + 1])) > W / lip:
                f.normal_update()
                if steep is None or abs(f.normal.z) < steep:
                    f.material_index = 1
    mat = _mat(bpy, kit, p.get('texture', 'gravel_concrete'), p.get('tex_scale', 1.2), p.get('tint', '#2E2A26'),
               p.get('tint_mix', 0.35), 1.0, 2.0, p.get('value', 1.0))
    q = {k: v for k, v in p.items() if k in ('position', 'rotate')}
    obs = kit.finish(bpy, name, bm, q, smooth=True, mat=mat)
    if p.get('jag'):
        obs[0].data.materials.append(_mat(bpy, kit, p.get('course', 'asphalt_02'), 1.5, '#0B0B0C', 0.85,
                                          p.get('course_rough', 1.0), value=p.get('course_value', 0.35)))
    return obs


def _plate(bm, rnd, w, d, t, rough=0.0):
    """An irregular plate: a polygon of 6 to 9 corners, `t` thick, its edges jagged. With `rough`, a lopsided polygon of 5
    to 9 corners, its top and underside flat, its broken edges a fine grid pushed in and out by a smooth noise up to
    `rough` of its size (a fracture's face, uneven but whole: the jagged edges' random corners read as crystals, and a
    rounder outline of more corners as "bricks or paving blocks")."""
    if rough:
        return _rough_plate(bm, rnd, w, d, t, rough)
    k = rnd.randint(6, 9)
    pts = []
    for i in range(k):
        a = 2 * math.pi * (i + rnd.uniform(-0.3, 0.3)) / k
        r = rnd.uniform(0.65, 1.0)
        pts.append((w / 2 * r * math.cos(a), d / 2 * r * math.sin(a)))
    top = [bm.verts.new((x, y, t / 2 + rnd.uniform(-0.006, 0.006))) for x, y in pts]
    bot = [bm.verts.new((x * rnd.uniform(0.9, 1.05), y * rnd.uniform(0.9, 1.05), -t / 2)) for x, y in pts]
    ft = bm.faces.new(top); fb = bm.faces.new(bot[::-1])
    sides = []
    for i in range(k):
        sides.append(bm.faces.new((top[i], bot[i], bot[(i + 1) % k], top[(i + 1) % k])))
    # crumbled, not cut: the broken edges subdivided and pushed in and out, the aggregate showing through
    res = bmesh.ops.subdivide_edges(bm, edges=_edges(sides), cuts=2, use_grid_fill=False)
    sc = max(w, d)
    for v in [g for g in res['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co.x += sc * 0.08 * rnd.uniform(-1, 1); v.co.y += sc * 0.08 * rnd.uniform(-1, 1)
        v.co.z += t * 0.25 * rnd.uniform(-1, 1)
    return ft, fb, sides


def _edges(faces):
    """The faces' edges, each once, in the order the faces give them. A set of them iterates in the order of their memory
    addresses, which differ from one process to the next, and the plates' jitter is drawn per new vertex in the order
    the subdivision makes them: so each machine built its own rubble, and E12r p19's strips from different helpers
    disagreed over it where they overlapped (ghosts in the stitched final's foreground)."""
    seen, out = set(), []
    for f in faces:
        for e in f.edges:
            if e not in seen:
                seen.add(e); out.append(e)
    return out


def _rough_plate(bm, rnd, w, d, t, rough):
    v0 = len(bm.verts)
    k = rnd.randint(5, 9)                                       # few corners, far apart: a broken piece is angular
    pts = []
    for i in range(k):
        a = 2 * math.pi * (i + rnd.uniform(-0.4, 0.4)) / k
        r = rnd.uniform(0.5, 1.0)                               # and lopsided, not a rounded block (p7: "bricks")
        pts.append((w / 2 * r * math.cos(a), d / 2 * r * math.sin(a)))
    top = [bm.verts.new((x, y, t / 2)) for x, y in pts]
    bot = [bm.verts.new((x * rnd.uniform(0.92, 1.04), y * rnd.uniform(0.92, 1.04), -t / 2)) for x, y in pts]
    ft = bm.faces.new(top); fb = bm.faces.new(bot[::-1])
    sides = [bm.faces.new((top[i], bot[i], bot[(i + 1) % k], top[(i + 1) % k])) for i in range(k)]
    bmesh.ops.subdivide_edges(bm, edges=_edges(sides), cuts=3, use_grid_fill=True)
    bm.verts.ensure_lookup_table()
    new = [bm.verts[i] for i in range(v0, len(bm.verts))]
    sc = max(w, d)
    o = Vector((rnd.uniform(0, 100), rnd.uniform(0, 100), rnd.uniform(0, 100)))
    for v in new:
        q = v.co / sc
        n = noise.noise_vector(q * 3.0 + o) + 0.35 * noise.noise_vector(q * 9.0 + o * 1.7)
        v.co.x += rough * sc * n.x; v.co.y += rough * sc * n.y
        if abs(abs(v.co.z) - t / 2) > 1e-6:                        # the edge's face, not the top's or underside's rim
            v.co.z += 0.12 * t * n.z
    faces = {f for v in new for f in v.link_faces}
    return ft, fb, [f for f in faces if f != ft and f != fb]


def _place(bm, verts, rot, loc):
    m = Euler([math.radians(a) for a in rot]).to_matrix()
    for v in verts:
        v.co = m @ v.co + Vector(loc)


def _drop(bpy, p, verts, sink):
    """With `drop`, a piece let down onto the set built before it (E12r p10: rubble round the speaker's foot laid at
    road level floated over the trench): its lowest corner set `sink` metres into the first surface of a set piece (an
    object named prop...) found straight down from above that corner, in the frame the piece is turned and placed in.
    A corner over nothing stays where it was; a flat decal (scorch's plane, four corners) is looked through."""
    low = min(verts, key=lambda v: v.co.z)
    a = math.radians(p.get('rotate_z', 0.0)); px, py, pz = p.get('position', [0.0, 0.0, 0.0])
    x, y = low.co.x, low.co.y
    o = Vector((x * math.cos(a) - y * math.sin(a) + px, x * math.sin(a) + y * math.cos(a) + py, 6.0))
    dg = bpy.context.evaluated_depsgraph_get()
    for _ in range(6):
        hit, loc, _n, _i, ob, _m = bpy.context.scene.ray_cast(dg, o, Vector((0.0, 0.0, -1.0)), distance=30.0)
        if not hit:
            return
        if ob.name.startswith('prop') and len(getattr(ob.data, 'vertices', ())) > 4:   # not a decal's plane (scorch)
            dz = (loc.z - pz) - sink - low.co.z
            for v in verts:
                v.co.z += dz
            return
        o = loc + Vector((0.0, 0.0, -1e-3))


def _faces(ft, fb, sides, top, p):
    """A piece's faces to their materials: its top the road's asphalt (when it has one), its underside the sub-base, its
    broken edges the sub-base too or, with `side`, their own."""
    ft.material_index = 0 if top else 1
    fb.material_index = 1
    for f in sides:
        f.material_index = 2 if p.get('side') else 1


def _materials(bpy, kit, me, p):
    mats = [_mat(bpy, kit, p.get('top', 'asphalt_02'), 4.0, '#09090A', 0.85, p.get('top_rough', 0.45), value=p.get('top_value', 1.0)),
            _mat(bpy, kit, p.get('under', 'gravel_concrete'), p.get('under_scale', 0.35), p.get('under_tint', '#211F1D'), 0.75,
                 value=p.get('under_value', 1.0))]
    if p.get('side'):
        mats.append(_mat(bpy, kit, p['side'], p.get('side_scale', 1.5), '#0B0B0C', 0.85, p.get('side_rough', 0.8),
                         value=p.get('side_value', 1.0)))
    for m in mats:
        me.materials.append(_dust(bpy, kit, m, p['dust'], p.get('dust_color', '#8C867E'), p.get('seed', 1)) if p.get('dust') else m)


def _dust(bpy, kit, m, amount, color, seed):
    """`dust` (slabs, debris): the grey powder a blow throws over everything near it (E12r p10, both critics: "no grit,
    gravel or dust anywhere", "all dusted grey"): the faces that look up take `dust_color` in drifts, by a noise, up to
    `dust` of the way, and go matte where it lies. On a copy of the material, so the road's own stays clean."""
    m = m.copy()
    nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bs is None:
        return m

    def smooth(v, lo, hi):
        n = N('ShaderNodeMapRange'); n.interpolation_type = 'SMOOTHSTEP'; n.clamp = True
        n.inputs['From Min'].default_value = lo; n.inputs['From Max'].default_value = hi
        L(v, n.inputs['Value']); return n.outputs['Result']

    def mul(a, b):
        n = N('ShaderNodeMath'); n.operation = 'MULTIPLY'
        for i, x in enumerate((a, b)):
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = x
            else:
                L(x, n.inputs[i])
        return n.outputs[0]

    geo = N('ShaderNodeNewGeometry'); sep = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Normal'], sep.inputs[0])
    nz = N('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'
    nz.inputs['Scale'].default_value = 7.0; nz.inputs['Detail'].default_value = 6.0; nz.inputs['W'].default_value = seed * 0.37
    L(geo.outputs['Position'], nz.inputs['Vector'])
    f = mul(mul(smooth(sep.outputs['Z'], 0.25, 0.85), smooth(nz.outputs['Fac'], 0.36, 0.6)), amount)
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L(f, mx.inputs['Factor'])
    src = bs.inputs['Base Color']
    if src.links:
        L(src.links[0].from_socket, mx.inputs[6])
    else:
        mx.inputs[6].default_value = src.default_value
    mx.inputs[7].default_value = kit.M.hex_lin(color)
    L(mx.outputs[2], src)
    rr = bs.inputs['Roughness']
    if rr.links:
        mr = N('ShaderNodeMath'); mr.operation = 'MAXIMUM'
        L(rr.links[0].from_socket, mr.inputs[0]); L(f, mr.inputs[1]); L(mr.outputs[0], rr)
    return m


def _crumble(bm, cm, seed, flat_tops=False):
    """Every sharp edge rounded over `cm` centimetres, so the broken edges catch the light along their length, and each
    face tented a little from a point near its middle, so none is a flat plane (with `flat_tops`, the broken edges'
    faces only: those with the edges' own material, index 2)."""
    sharp = [e for e in bm.edges if e.is_manifold and e.calc_face_angle(0.0) > math.radians(35.0)]
    bmesh.ops.bevel(bm, geom=sharp, offset=cm * 0.01, offset_type='OFFSET', segments=2, profile=0.5, affect='EDGES',
                    clamp_overlap=True)
    big = [f for f in bm.faces if len(f.verts) > 5 and f.calc_area() > (cm * 0.03) ** 2
           and (not flat_tops or f.material_index == 2)]
    bm.normal_update()
    res = bmesh.ops.poke(bm, faces=big)
    o = Vector((seed * 1.7, seed * 2.3, seed * 0.9))
    for v in res['verts']:
        n = v.normal.copy()
        v.co += n * (cm * 0.006 * noise.noise(v.co * 7.0 + o))
    bm.normal_update()


def _smooth(bm, deg):
    """Smooth shading across every edge gentler than `deg` degrees; the sharper ones (and the open ones) stay sharp."""
    a = math.radians(deg)
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        e.smooth = e.is_manifold and e.calc_face_angle(0.0) <= a


def slabs(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 1))
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    lip, t = p.get('lip', 0.75), p.get('thickness', 0.08)
    D, ramp = p.get('depth', 0.35), p.get('ramp', 4.0)
    spread, flip, fallen, sp = p.get('spread', 0.25), p.get('flip', 0.0), p.get('fallen', 0.0), p.get('size_power', 1.0)
    lipf = _lipf(p)
    bm = bmesh.new()
    tv, clump = p.get('thick_var', 0.0), p.get('clump', 0.0)
    if p.get('drop'):
        bpy.context.view_layer.update()
    for k in range(p.get('count', 40)):
        y = rnd.uniform(y0 + 0.5, y1 - 0.2)
        s = 1 if rnd.random() < 0.5 else -1
        if clump and noise.noise(Vector((y * 0.9, s * 3.7, p.get('seed', 1) * 0.61))) < clump - 0.35:
            continue                                           # a gap in the row: the lip tore in clumps, not evenly
        f = min(1.0, (y - y0) / ramp)                          # bigger, steeper plates where the trench is deep
        sz = p.get('size', 1.0)
        w, d = sz * (0.25 + 0.45 * rnd.random() ** sp) * (0.5 + f), sz * (0.3 + 0.5 * rnd.random() ** sp) * (0.5 + f)
        tk = t * rnd.uniform(1.0 - 0.5 * tv, 1.0 + tv) if tv else t
        before = len(bm.verts)
        ft, fb, sides = _plate(bm, rnd, w, d, tk, p.get('rough', 0.0))
        _faces(ft, fb, sides, True, p)
        bm.verts.ensure_lookup_table()
        new = [bm.verts[i] for i in range(before, len(bm.verts))]   # new verts come last (wrappers are not stable)
        tilt = rnd.uniform(p.get('tilt_min', 15.0), p.get('tilt', 55.0)) * f
        x = s * (lipf(y, s) + w * spread * (rnd.uniform(0.2, 1.0) if not clump else rnd.random() ** 0.6 * 1.6))
        z = 0.02 + 0.5 * w * math.sin(math.radians(tilt)) * 0.4 - (0.0 if rnd.random() < 0.7 else 0.1) + (tk - t) * 0.5
        if fallen and rnd.random() < fallen and abs(y) > 0.8:   # dropped into the trench (clear of the speaker at 0)
            x = s * rnd.uniform(0.0, lip * 0.75)
            z = -D * f + t * 0.5 + 0.02 + 0.3 * w * math.sin(math.radians(tilt))
        if flip and rnd.random() < flip:                       # thrown over onto its back
            tilt = 180.0 - tilt * 0.5
        _place(bm, new, (rnd.uniform(-8, 8), s * tilt, rnd.uniform(-25, 25)), (x, y, z))
        if p.get('drop'):
            _drop(bpy, p, new, tk * 0.3)
    if p.get('crumble'):
        _crumble(bm, p['crumble'], p.get('seed', 1), p.get('flat_tops', False))
    if p.get('smooth'):
        _smooth(bm, p['smooth'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    _materials(bpy, kit, me, p)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]


def debris(bpy, name, p, kit):
    rnd = random.Random(p.get('seed', 2))
    y0, y1 = p.get('y0', -20.0), p.get('y1', 0.0)
    reach = p.get('reach', 6.0)
    bm = bmesh.new()
    if p.get('drop'):
        bpy.context.view_layer.update()
    for k in range(p.get('count', 300)):
        # along the path, thrown sideways (and some forward past the speaker); size falls with distance thrown
        fwd = p.get('forward', 0.0)
        if rnd.random() < fwd:
            # thrown ahead of where it came to rest: a fan opening with distance
            ahead = p.get('ahead', 6.0) * rnd.random() ** 1.6
            y = y1 + 0.3 + ahead
            r = (0.2 + 0.5 * ahead) * rnd.random()
        elif p.get('band'):                                    # a strip across the path, `inner` clear either side
            y = rnd.uniform(*p['band'])
            r = reach * rnd.random() ** 2.2
        else:
            y = rnd.uniform(y0 + 1.0, y1 + 0.5)
            r = reach * rnd.random() ** 2.2
        x = (1 if rnd.random() < 0.5 else -1) * ((p.get('inner', 0.8) if y < y1 or p.get('band') else 0.0) + r)
        if p.get('patchy'):
            # E12r p20 (p19's critic: "the small pebbles ... spread so evenly that they look computer-scattered"): a piece
            # kept where a slow noise runs high, so the rubble lies in drifts with bare road between
            sc, lo, hi = p['patchy']
            v = noise.noise(Vector((x / sc, y / sc, p.get('seed', 2) * 0.37)))
            keep = min(1.0, max(0.0, (v - lo) / max(hi - lo, 1e-6)))
            if rnd.random() > keep * keep * (3 - 2 * keep):
                continue
        mult = (0.12 + 0.88 * rnd.random() ** p['size_power']) if 'size_power' in p else rnd.uniform(0.3, 1.0)
        size = max(0.012, p.get('size_max', 0.16) * max(0.0, 1.0 - r / max(reach, r + 0.01)) ** 1.6 * mult)
        if p.get('fine'):
            size = rnd.uniform(*p.get('fine_size', [0.005, 0.03])) * (1.0 - 0.5 * min(1.0, r / reach))
        before = len(bm.verts)
        ft, fb, sides = _plate(bm, rnd, size * rnd.uniform(0.8, 1.6), size * rnd.uniform(0.8, 1.6),
                               size * rnd.uniform(*p.get('flat', [0.3, 0.6])), p.get('rough', 0.0))
        bm.verts.ensure_lookup_table()
        new = [bm.verts[i] for i in range(before, len(bm.verts))]   # new verts come last (wrappers are not stable)
        _place(bm, new, (rnd.uniform(-40, 40), rnd.uniform(-40, 40), rnd.uniform(0, 360)), (x, y, p.get('z', 0.0) + size * 0.2))
        if p.get('drop'):
            _drop(bpy, p, new, size * 0.15)
        _faces(ft, fb, sides, rnd.random() < 0.6, p)
    if p.get('crumble'):
        _crumble(bm, p['crumble'], p.get('seed', 2), p.get('flat_tops', False))
    if p.get('smooth'):
        _smooth(bm, p['smooth'])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    _materials(bpy, kit, me, p)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0]))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    return [ob]


def road(bpy, name, p, kit):
    """The deck either side of the gouge as one slab (E12r p9): `half` metres out each side, `thickness` thick under the
    road's surface at 0, from `ylo` to `yhi` along the gouge's line, open between its torn lips (`lip`, `jag`) from `y0`
    to `y1`; one object, so its texture runs on unbroken where the deck's boxes met in ruled lines. In the road's
    material (the piece's own `material` and texture keys)."""
    lipf = _lipf(p)
    y0, y1, half, t = p.get('y0', -20.0), p.get('y1', 0.0), p.get('half', 10.0), p.get('thickness', 0.3)
    ylo, yhi = p.get('ylo', y0 - 20.0), p.get('yhi', y1 + 20.0)
    ys = sorted(set([ylo, yhi] + [y0 + (y1 - y0) * k / int((y1 - y0) / 0.03) for k in range(int((y1 - y0) / 0.03) + 1)]
                    + [ylo + (y0 - ylo) * k / 20 for k in range(20)] + [y1 + (yhi - y1) * k / 20 for k in range(1, 20)]))
    bm = bmesh.new()

    def strip(xa, xb, ya, yb):
        """One quad of the top, its underside and nothing between: the slab's sides are its outer edge and the lips."""
        top = [bm.verts.new(c) for c in ((xa[0], ya, 0.0), (xb[0], ya, 0.0), (xb[1], yb, 0.0), (xa[1], yb, 0.0))]
        bm.faces.new(top)
    rows = [(y, lipf(y, -1), lipf(y, 1), y0 <= y <= y1) for y in ys]
    for (ya, la, ra, ina), (yb, lb, rb, inb) in zip(rows, rows[1:]):
        strip((-half, -half), (-la, -lb), ya, yb)                # each side, its inner edge on the lip line
        strip((ra, rb), (half, half), ya, yb)
        if not (ina and inb):                                    # and across between them, before and after the gouge
            strip((-la, -lb), (ra, rb), ya, yb)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    # thickness: the top kept, a copy dropped to the underside, the open edges joined as the slab's sides
    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:], use_keep_orig=True)
    for v in [g for g in res['geom'] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z -= t
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mat = kit.piece_material(bpy, {k: v for k, v in p.items() if k in ('material', 'texture', 'tex_scale', 'tint',
                                                                       'tint_mix', 'rough_mul', 'bump', 'value')})
    q = {k: v for k, v in p.items() if k in ('position', 'rotate')}
    return kit.finish(bpy, name, bm, q, smooth=False, mat=mat)


def scorch(bpy, name, p, kit):
    """Scorch on the road: a plane a hair above it, soot-black where noise and a falloff from the path's centre line say
    so and clear elsewhere, so the blackening frays out into the asphalt instead of ending at an edge. `size` [w, l],
    `strength` the blackness at its heart, `scale` metres a patch."""
    w, l = p.get('size', [3.0, 20.0])
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, 0.0)) for x, y in ((-w / 2, -l / 2), (w / 2, -l / 2), (w / 2, l / 2), (-w / 2, l / 2))]
    bm.faces.new(vs)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(p.get('position', [0, 0, 0.003]))
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = kit.M.hex_lin(p.get('color', '#0C0A09'))
    bsdf.inputs['Roughness'].default_value = 0.9
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    # falloff across the path (x), strongest on its centre line, and toward both ends (y)
    def band(sock, lo, hi):
        a = nt.nodes.new('ShaderNodeMath'); a.operation = 'SUBTRACT'; a.inputs[1].default_value = 0.5
        nt.links.new(sock, a.inputs[0])
        b = nt.nodes.new('ShaderNodeMath'); b.operation = 'ABSOLUTE'; nt.links.new(a.outputs[0], b.inputs[0])
        c = nt.nodes.new('ShaderNodeMapRange'); c.inputs['From Min'].default_value = hi; c.inputs['From Max'].default_value = lo
        nt.links.new(b.outputs[0], c.inputs['Value'])
        return c.outputs['Result']
    fx, fy = band(sep.outputs['X'], 0.05, 0.5), band(sep.outputs['Y'], 0.3, 0.5)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0 / p.get('scale', 0.6)
    nz.inputs['Detail'].default_value = 8.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    m1 = nt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'; nt.links.new(fx, m1.inputs[0]); nt.links.new(fy, m1.inputs[1])
    m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
    nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(nz.outputs['Fac'], m2.inputs[1])
    ramp = nt.nodes.new('ShaderNodeMapRange'); ramp.inputs['From Min'].default_value = 0.15
    ramp.inputs['From Max'].default_value = 0.45; ramp.inputs['To Max'].default_value = p.get('strength', 0.85)
    nt.links.new(m2.outputs[0], ramp.inputs['Value'])
    nt.links.new(ramp.outputs['Result'], mix.inputs['Fac'])
    nt.links.new(tr.outputs['BSDF'], mix.inputs[1]); nt.links.new(bsdf.outputs['BSDF'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
    me.materials.append(m)
    ob.visible_shadow = False
    return [ob]
