"""Round 28: the mark as the real thing, path-traced as the speakers are, and its one-colour versions traced from it.

The owner, 2026-10-17, of the spins: "It still looks odd when ever the meridian "seams" of the globe are viewed straight
on. I want the semi transparent pieces so it looks like acrylic like the speakers. Maybe it's best to actually render the
object like we did the speakers, so it looks real, and then create the monochromatic fill and stroke versions based on
the real thing."

So the globe is built as an object: earth.py's six discs (its three parallels and three meridians, its lean and its
tip, each disc a slab THICK of the radius thick) cut from the Cloud cabinets' own 20 mm tinted cast acrylic, which
makes the globe 800 mm across, and cemented clear where they cross (or, with --slots, slotted through one another, the
meridian facing us whole and each other disc slotted round those before it, GAP clear). It is rendered in Cycles with
the engine's acrylic (studio/engine/materials.py's clear_resin, polished as the cabinets are), so a face is a clear
tint, crossing faces build their tints, and an edge, seen along the whole sheet, its disc's colour at its deepest. The
tints are the cabinets' through glow(), so each passes its own colour freely and an edge glows instead of going black.
The camera is earth.py's own: square on and orthographic, so a render lies exactly over the flat drawings made from the
same discs (slabs, line_body, fill_body).

The ground is the brand's paper (or night) as a backdrop behind the globe, rendered as exactly that colour, so the
render sits on the page like the flat marks do; a dim studio (Poly Haven's, CC0) and a soft key above left show only
in the acrylic's reflections.

Round 28b. The owner: "We could do less transparent acrylic. The individual colors need to pop more. I feel like the old
monochromatic logos were better, they just needed some reshaping." So the render's look is now translucent (--look
translucent, the default): each disc cast in the mark's own hue (earth._C), light scattering --scatter metres into the
sheet (the engine's cast_resin) and --clear of it, a quarter, crossing straight through, as in translucent cast acrylic.
Each disc reads as its own colour at full strength and only hints at the discs behind it. Translucent acrylic shows its
colour by the light that falls on it, so the studio is brighter (--env studio) and a broad fill beside the camera joins
the key (--key 3, --fill 3). Round 28's clear tints are --look clear --env dim --key 2 --fill 0. The one-colour logos
are earth.py's seamed discs again (their spin reshaped there); --flat still makes round 28's traced fill and line.

Round 28d. The owner: "I want both paper and dark to be more transparent, like the same colors as the speakers with
adjustments so they work on dark and light and aren't as transparent as the earlier version." The speakers' horns are
clear resin tinted the line's colours (HORN), and those are the mark's hues near enough, so each disc keeps the mark's
hue but lets more light straight through, 0.6 of it (--clear; 28b let a quarter through), and its face is tinted the
hue's square root (--body through-deep, a little deeper than the root): light crossing a sheet's two faces is tinted
twice, so a disc seen against the paper is the hue itself, the speakers' colour, where a face tinted the hue went dark
and a pale cabinet tint went grey. On dark grounds, the study's n4 ("I liked n4 or n5 without glow for dark"): the rims
glowing at 1 and the faces at 0.15, with no bloom (--dark). "For the spin, it flashes really bright in several spots at
certain positions": each rim turning square to the camera mirrored the studio's softbox, and the fill beside the camera,
whole, so the room is now a plain grey one (--env grey), on dark as on paper (there the studio at a quarter of its
strength still whitened such a rim), and neither light shows in reflections but the key at 0.4 (--shine). And the
equator's edge runs unbroken where it meets the meridians (_equator_owns).

Round 28e. The owner: "the light version of the acrylic globe kind of looks dull and muted in color now." At 0.6
through every disc was seen through the green one facing us, which covers the whole globe, and the tints multiplied,
so on paper the render had a third less colour than 28b's. On light grounds the hues the acrylic follows are now purer
and a touch lighter (--vivid, in OKLCh, the hue kept), each sheet lets 0.45 through (--clear) and the key and fill are
at 4: as colourful as 28b, and lighter. The dark version had kept its colour, so the presets carry the acrylic too
(lighting) and --dark keeps 28d's.

    python3 spinoffs/barkhorn/globe_real.py --still OUT.png [--ground paper|night] [--px 1024] [--samples 128] [--spin DEG]
    python3 spinoffs/barkhorn/globe_real.py --spin-frames DIR [--frames 120] [--px 720] [--samples 24] [--first N --last M]
    python3 spinoffs/barkhorn/globe_real.py --encode DIR OUT          the frames as OUT.mp4 and OUT.webm
    python3 spinoffs/barkhorn/globe_real.py --flat DIR [--flat-spin DIR]   round 28's fill and line, stills and spins

The still is framed as the flat marks are (their SVGs' view box); the spin's frames as mark.py frames its spins (a quarter
of the globe's width clear round it), half a turn in `frames` frames, so they loop. Times on 4 CPUs, round 28d's acrylic:
a 1024 px still at 128 samples about 8 minutes, a 720 px spin frame at 24 samples 22 to 24 s (28b's translucent about 6
minutes and 18 s; round 28's clear, twice those).
"""
import argparse, math, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import earth as E                                        # noqa: E402

R = 0.4                                                  # the globe's radius in metres: discs of the cabinets' 20 mm sheet
T = E.THICK * R                                          # each disc's thickness, the mark's slab (0.05 of the radius)
GAP = 0.0005                                             # the slots' clearance each side
SEG = 360                                                # a disc's segments round
NAMES = ['ember', 'ice', 'acid', 'haze', 'poison', 'dust']           # earth.RING's order: N, equator, S, meridians 30, 90, 150
ACRYLIC = {'ember': '#F2A29C', 'dust': '#F2B184', 'acid': '#F2D06B', 'poison': '#B2C9A2', 'ice': '#B5D9EE',
           'haze': '#BEADD8'}                            # the Cloud cabinets' tints after `DEPTH` (product.py's Clouds)
HORN = {'ember': '#C8262B', 'dust': '#E0661C', 'acid': '#F2B705', 'poison': '#4C6A36', 'ice': '#3C86C2',
        'haze': '#5E3F8F'}                               # round 28d: the Clouds' horns, the speakers' own colour (product.py)
DEPTH, POLISH = 0.025, 0.05                              # their depth (m) and roughness, polished cast acrylic
MARK_DEPTH = 0.02                                        # the globe's: a little deeper, so a face holds its colour on paper
ORDER = [4, 3, 5, 1, 0, 2]                               # which disc is whole: the meridian facing us, then the others in turn
GROUNDS = {'paper': E.PAPER, 'night': E.NIGHT}
GLOW = dict(ground='night', env='dim', key=2.0, fill=1.5, neon=(1.0, 0.15),
            body='mark', clear=0.25, vivid=(1.0, 0.0))   # round 28c, the colour mark on dark grounds: fluorescent acrylic,
                                                         # its rims their own colour at full and its faces at 0.15, a dim
                                                         # room, a softer key and fill, and bloom(), on 28b's acrylic
DARK = dict(ground='night', env='grey', key=2.0, fill=1.5, neon=(1.0, 0.15),
            body='through-deep', clear=0.6, vivid=(1.0, 0.0))   # round 28d, on dark: the study's n4 (rims at 1.0), no bloom,
                                                         # in the plain grey room as on paper (the studio's softbox, even
                                                         # at 0.25, whitened a rim turning square to the camera)
LIGHTS = dict(ground='paper', env='grey', key=4.0, fill=4.0, neon=(0.0, 0.0),
              body='through-deep', clear=0.45, vivid=(1.4, 0.05))   # with no preset: the colour mark on paper (round 28e,
                                                         # the owner: "the light version of the acrylic globe kind of looks
                                                         # dull and muted in color now": livelier hues, a little less clear,
                                                         # more light; 28d's 0.6 clear in the hues as they are stays on dark)


def lighting(a):
    """A run's ground, room, key, fill, neon and acrylic (body, clear, vivid): each as given, else the preset's (--glow,
    --dark), else LIGHTS'. (Round 28d: the presets used to replace what was given, so a test of the dark room, --dark
    --env dark, rendered the studio.)"""
    preset = GLOW if a.glow else DARK if a.dark else LIGHTS
    for k in LIGHTS:
        if getattr(a, k) is None:
            setattr(a, k, preset[k])
    return a


def local_discs():
    """Each disc in the globe's own frame (its axis z; longitude 0 toward -y, the camera, and 90 along +x), in
    earth.rings' order: (centre, normal, radius), of the radius."""
    a, e1, e2 = np.array([0.0, 0.0, 1.0]), np.array([0.0, -1.0, 0.0]), np.array([1.0, 0.0, 0.0])
    out = []
    for phi in (E.LAT, 0.0, -E.LAT):
        p = math.radians(phi)
        out.append((math.sin(p) * a, a, math.cos(p)))
    for lam in E.MERIDIANS:
        l = math.radians(lam)
        u = math.cos(l) * e1 + math.sin(l) * e2
        out.append((np.zeros(3), np.cross(u, a), 1.0))
    return out


def orientation():
    """The globe's frame in the world as a 3 x 3 matrix: earth.basis (the lean and the tip) with its screen (x right, y
    up, z toward us) set in a world whose camera looks along +y from -y, z up."""
    a, e1, e2 = E.basis()
    w = lambda v: np.array([v[0], -v[2], v[1]])
    return np.column_stack([w(e2), -w(e1), w(a)])


def _hex_lin(h):
    h = h.lstrip('#')
    c = np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def slabs(spin=0.0, thick=E.THICK, n=720):
    """Each disc of the real globe as earth.py's camera sees it (the unit globe, y up), in earth.rings' order: its near
    face and its far face (ovals), its outline (the slab's silhouette, the hull of the two), its edge (what of the outline
    the near face leaves, where a line of sight enters the disc through its rim and runs along it inside, so the acrylic
    shows its deepest there: a crescent on one side of an oblique disc, from nothing to its whole thickness; edge on, the
    whole band; face on, nothing) and its middle ring in 3D (x, y and depth toward us)."""
    from shapely.geometry import MultiPoint, Polygon
    s_ = math.radians(spin)
    W = orientation() @ np.array([[math.cos(s_), -math.sin(s_), 0], [math.sin(s_), math.cos(s_), 0], [0, 0, 1]])
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    scr = lambda P: (W @ P.T).T[:, [0, 2, 1]] * [1, 1, -1]      # x right, y up, depth toward us (world -y)
    out = []
    for c, nrm, r in local_discs():
        nrm = nrm / np.linalg.norm(nrm)
        u = np.cross(nrm, [1.0, 0.0, 0.0] if abs(nrm[0]) < 0.9 else [0.0, 1.0, 0.0]); u /= np.linalg.norm(u)
        v = np.cross(nrm, u)
        toward = 1.0 if -(W @ nrm)[1] >= 0 else -1.0     # the face nearer the camera
        ring = r * (np.outer(np.cos(a), u) + np.outer(np.sin(a), v))
        near, far = scr(c + toward * thick / 2 * nrm + ring)[:, :2], scr(c - toward * thick / 2 * nrm + ring)[:, :2]
        F = Polygon(near).buffer(0)
        S = MultiPoint(np.vstack([near, far])).convex_hull
        out.append(dict(near=F, far=Polygon(far).buffer(0), outline=S, edge=S.difference(F), ring=scr(c + ring)))
    return out


def line_body(colour, spin=0.0, w=0.024, far=E.W_DEPTH):
    """The line version traced from the real thing: every disc seen through the others, as the acrylic shows it. Its
    middle ring a line `w` of the radius wide on the near side of the globe and `far` of that behind it, seen through
    the discs in front (earth._runs splits each at the outline); and its edge, filled where it shows, so the line swells
    where the disc's thickness faces you, and a disc edge on is one band as wide as the sheet is thick."""
    from shapely.geometry import LineString
    from shapely.ops import unary_union
    parts = []
    for q in slabs(spin):
        for front, k in ((True, 1.0), (False, far)):
            for run in E._runs(q['ring'], front):
                if len(run) > 1:
                    parts.append(LineString(run[:, :2]).buffer(w * k / 2, cap_style=1, join_style=1))
        parts.append(q['edge'])
    return f'<path d="{E._poly_d(unary_union(parts))}" fill="{colour}"/>'


def fill_body(colour, spin=0.0, sheet=0.2):
    """The fill traced from the real thing, in one colour: each disc's face a sheet of `sheet` of the colour (so where
    k discs cross, the colour builds as k sheets of tinted acrylic do), and its edge, seen along the disc, the colour
    whole."""
    ss = slabs(spin)
    faces = ''.join(f'<path d="{E._poly_d(q["near"])}" fill="{colour}" fill-opacity="{sheet}"/>' for q in ss)
    edges = ''.join(f'<path d="{E._poly_d(q["edge"])}" fill="{colour}"/>' for q in ss)
    return faces + edges


def flat_svg(style, colour, bg, spin=0.0, e=1 + E.W_LINE / 2, size=None):
    """A flat version (`style` 'line' or 'fill') as a whole SVG on `bg` (None: transparent), the unit globe framed
    2e across as the marks are."""
    body = line_body(colour, spin) if style == 'line' else fill_body(colour, spin)
    wh = f' width="{size}" height="{size}"' if size else ''
    ground = f'<rect x="{-e:.4f}" y="{-e:.4f}" width="{2 * e:.4f}" height="{2 * e:.4f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.4f} {-e:.4f} {2 * e:.4f} {2 * e:.4f}"{wh}>'
            f'{ground}{body}</svg>')


PASS = {'acid': 'RG'}                                     # glow()'s channels passed whole, beside the least absorbed


def glow(hx, keep=0.97, passed=''):
    """A tint that passes its own colour almost freely, as a dyed acrylic does: each channel's absorbance less `keep` of
    the least absorbed channel's, so a face keeps its tint and an edge, seen along the whole disc, glows its colour
    instead of going black. Over a long path only the freest channel is left, so an amber's edge goes red: `passed`
    channels ('RG' for Acid) pass as freely, so its edge stays yellow."""
    c = np.clip(_hex_lin(hx), 1e-4, 1.0)
    a = -np.log(c)
    a = a - keep * a.min()
    for ch in passed:
        a['RGB'.index(ch)] = a.min()
    v = np.exp(-a)
    s = np.where(v <= 0.0031308, 12.92 * v, 1.055 * v ** (1 / 2.4) - 0.055)
    return '#%02X%02X%02X' % tuple(int(round(255 * min(1.0, x))) for x in s)


def _emit(m, hx, strength):
    """A material given off light: its Principled BSDF's emission, `hx` at `strength` for its brightest channel (so a
    rim at 1 is its own colour at full, not clipped toward white: the first proofs at 3 turned orange and yellow alike
    yellow, and blue cyan)."""
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    c = _hex_lin(hx)
    b.inputs['Emission Color'].default_value = (*c, 1.0)
    b.inputs['Emission Strength'].default_value = strength / max(c)
    return m


def build(bpy, tints=None, fuse=True, depth=MARK_DEPTH, look='clear', scatter=0.008, clear=0.2, neon=(0.0, 0.0),
          crossings='equator', milk=0.0, body=None):
    """The six discs, cemented clear (one solid where they cross; `fuse` False: slotted), parented to one empty at the
    origin whose matrix turns the globe. `look` 'clear': clear tinted acrylic, `tints` hex per disc (glow()'s of the
    cabinets' by default). 'translucent': the mark's own hues as translucent cast acrylic, light scattering
    `scatter` metres into it (the engine's cast_resin), `clear` of it crossing straight through. `neon` (round 28c, for
    dark grounds; cemented only): fluorescent acrylic, which gathers light through its faces and gives it out at its
    cut edges, so each disc's rim glows its colour at the first strength and its faces at the second. `crossings`
    (cemented): 'equator' (round 28d), where the equator's edge meets a meridian the crossing is the equator's
    (_equator_owns); 'fused', round 28's, both acrylics where they meet. `milk` (clear): a share of the light scattered
    in the sheet, in its own tint, so a face has some body. `body` (translucent, round 28d): each disc's (surface,
    scatter) colours by name; the mark's hue for both by default."""
    import bmesh
    from mathutils import Matrix, Vector
    import materials as Mt
    tints = tints or {k: glow(v, passed=PASS.get(k, '')) for k, v in ACRYLIC.items()}
    root = bpy.data.objects.new('globe', None)
    bpy.context.scene.collection.objects.link(root)
    lit = fuse and max(neon) > 0

    def slab(name, c, n, r, grow=0.0, thick=T):
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=SEG, radius1=r * R + grow, radius2=r * R + grow,
                              depth=thick)
        if lit:                                          # the rim (the cone's sides, quads) its own material
            for f in bm.faces:
                f.material_index = 1 if len(f.verts) == 4 else 0
        m = Matrix.Translation(Vector(c * R)) @ Vector((0, 0, 1)).rotation_difference(Vector(n)).to_matrix().to_4x4()
        bm.transform(m)
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    discs = local_discs()
    if look == 'translucent':
        def acrylic(name, i, see=None):
            face, deep = (body or {}).get(NAMES[i], (E._C[NAMES[i].title()],) * 2)
            return Mt.make(bpy, name, 'cast_resin', {'color': face, 'deep': deep,
                                                     'radius': scatter, 'roughness': POLISH, 'cloud': 0.0, 'fibre': 0.0,
                                                     'clear': clear if see is None else see})
    else:
        def acrylic(name, i, see=None):
            return Mt.make(bpy, name, 'clear_resin', {'color': tints[NAMES[i]] if milk else '#FFFFFF', 'deep': tints[NAMES[i]],
                                                      'radius': depth, 'roughness': POLISH, 'milk': milk})
    mats = {i: acrylic(f'acrylic-{NAMES[i]}', i) for i in ORDER}
    if lit:
        for i in ORDER:
            _emit(mats[i], E._C[NAMES[i].title()], neon[1])
        rims = {i: _emit(acrylic(f'rim-{NAMES[i]}', i, see=min(clear, 0.25)), E._C[NAMES[i].title()], neon[0])
                for i in ORDER}                          # (round 28d: each rim as dense as 28b's, as in the n4 picked)
    if fuse:                                             # one solid, each face keeping its own disc's acrylic
        parts = {i: slab(f'disc-{NAMES[i]}', *discs[i]) for i in ORDER}
        for i, ob in parts.items():
            ob.data.materials.append(mats[i])
            if lit:
                ob.data.materials.append(rims[i])
        base = parts[ORDER[0]]
        for i in ORDER[1:]:
            mod = base.modifiers.new(f'fuse-{NAMES[i]}', 'BOOLEAN')
            mod.operation, mod.solver, mod.object, mod.material_mode = 'UNION', 'EXACT', parts[i], 'TRANSFER'
            parts[i].hide_render = True
        obs, cutters = [(None, base)], [parts[i] for i in ORDER[1:]]
    else:
        cutters = {i: slab(f'cut-{NAMES[i]}', *discs[i], grow=0.002, thick=T + 2 * GAP) for i in ORDER}
        for c in cutters.values():
            c.hide_render = True
        obs = []
        for k, i in enumerate(ORDER):
            ob = slab(f'disc-{NAMES[i]}', *discs[i])
            for j in ORDER[:k]:
                mod = ob.modifiers.new(f'slot-{NAMES[j]}', 'BOOLEAN')
                mod.operation, mod.solver, mod.object = 'DIFFERENCE', 'EXACT', cutters[j]
            obs.append((i, ob))
        cutters = list(cutters.values())
    dg = bpy.context.evaluated_depsgraph_get()
    for i, ob in obs:
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        ob.modifiers.clear()
        ob.data = me
        me.shade_smooth()
        me.set_sharp_from_angle(angle=math.radians(25))
        if i is not None:
            me.materials.clear(); me.materials.append(mats[i])
        elif crossings == 'equator':
            _equator_owns(me)
        ob.parent = root
    for c in cutters:
        bpy.data.objects.remove(c, do_unlink=True)
    return root


def _root_hex(hx, k=0.5):
    """A colour whose square, light crossing a sheet's two faces each tinted by it, is `hx` (in linear light); with `k`
    above a half, deeper."""
    v = np.clip(_hex_lin(hx), 0.0, 1.0) ** k
    s = np.where(v <= 0.0031308, 12.92 * v, 1.055 * v ** (1 / 2.4) - 0.055)
    return '#%02X%02X%02X' % tuple(int(round(255 * min(1.0, x))) for x in s)


def _vivid_hex(hx, c=1.0, lift=0.0):
    """`hx` in OKLCh with its chroma times `c` and its lightness raised by `lift`, its hue kept; where that leaves sRGB
    the chroma is eased back until it fits (clipping a channel would turn the hue)."""
    L, a, b = E._oklab(hx)
    for k in np.linspace(c, min(c, 1.0), 49):
        l_, m_, s_ = ((L + lift) + 0.3963377774 * a * k + 0.2158037573 * b * k) ** 3, \
            ((L + lift) - 0.1055613458 * a * k - 0.0638541728 * b * k) ** 3, ((L + lift) - 0.0894841775 * a * k - 1.2914855480 * b * k) ** 3
        v = np.array([4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
                      -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
                      -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_])
        if v.min() >= -1e-4 and v.max() <= 1 + 1e-4:
            break
    return E._from_oklab(np.array([L + lift, a * k, b * k]))


def _hues(c=1.0, lift=0.0):
    """Each disc's hue: the mark's, or livelier (round 28e), its chroma times `c` and its lightness raised by `lift`."""
    return {k: E._C[k.title()] if (c, lift) == (1.0, 0.0) else _vivid_hex(E._C[k.title()], c, lift) for k in NAMES}


def _body(kind, hues):
    """The acrylic's (face, scatter) colours per disc for --body, from `hues` (_hues) where it follows the mark."""
    return {'mark': {k: (hues[k], hues[k]) for k in NAMES},
            'cabinet': {k: (ACRYLIC[k], HORN[k]) for k in NAMES},
            'horn': {k: (HORN[k], HORN[k]) for k in NAMES},
            'through': {k: (_root_hex(hues[k]), hues[k]) for k in NAMES},
            'through-deep': {k: (_root_hex(hues[k], 0.65), hues[k]) for k in NAMES}}[kind]


def _equator_owns(me):
    """Round 28d. The owner, of the render: "Where the edge of the blue disc meets the meridians, can we get rid of those
    double color triangle shapes and just make the whole outside of the intersection edges blue?" Cemented, the two rims
    crossed there as two triangles of each colour: across the cell where they meet, 20 mm square, each rim lies outside
    the other in two opposite corners, by a tenth of a millimetre at most. So the meridians' faces in that cell, in the
    equator's sheet at its edge, take the equator's acrylic (and its rim's, lit), and its edge runs on unbroken. (At the
    40° parallels a meridian stands up to 8 mm past the parallel's edge on one side, its own shape, so those stay.)"""
    slot = {m.name: k for k, m in enumerate(me.materials)}
    swap = {slot[f'{kind}-{NAMES[i]}']: slot[f'{kind}-ice'] for kind in ('acrylic', 'rim') for i in (3, 4, 5)
            if f'{kind}-ice' in slot}
    for f in me.polygons:
        p = f.center                                     # (the globe's own frame: the equator its plane z = 0)
        if f.material_index in swap and abs(p.z) < T / 2 + 1e-5 and math.hypot(p.x, p.y) > R - 0.001:
            f.material_index = swap[f.material_index]


def stage(bpy, ground, px, e, samples, env='dim', adaptive=0.01, key=2.0, fill=0.0, shine=(1.0, 1.0), bounces=96):
    """The camera (earth.py's view, orthographic, the frame 2e radii across), the ground as a backdrop of exactly its
    colour, and the studio seen in the acrylic: a soft key above left, the room round it. `shine` (round 28d): the key's
    and the fill's shares in reflections (lights.lamp_shares). The fill, a broad softbox just beside the camera, was
    mirrored whole by every rim and face that turned toward the camera, and in the spin those flashed white (the owner:
    "it flashes really bright in several spots at certain positions and looks odd")."""
    from mathutils import Vector
    import lights as Lt
    scene = bpy.context.scene
    cd = bpy.data.cameras.new('camera'); cam = bpy.data.objects.new('camera', cd)
    scene.collection.objects.link(cam); scene.camera = cam
    cd.type = 'ORTHO'; cd.ortho_scale = 2 * e * R; cd.clip_start = 0.01; cd.clip_end = 100
    cam.location = (0.0, -6.0, 0.0); cam.rotation_euler = (math.pi / 2, 0.0, 0.0)
    # the ground: a plane far behind, glowing its colour, so the camera and anything seen through the acrylic meet it
    me = bpy.data.meshes.new('ground'); s = 12.0
    me.from_pydata([(-s, 3.0, -s), (s, 3.0, -s), (s, 3.0, s), (-s, 3.0, s)], [], [(0, 1, 2, 3)])
    gob = bpy.data.objects.new('ground', me); scene.collection.objects.link(gob)
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    em.inputs['Color'].default_value = (*_hex_lin(GROUNDS[ground]), 1.0); em.inputs['Strength'].default_value = 1.0
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    me.materials.append(m)
    # the room: a studio photographed (Poly Haven, CC0), seen only in reflections, a plain grey, or a dark room
    Lt.world(bpy, {'studio': {'kind': 'hdri', 'file': 'studio_small_03_1k', 'strength': 0.6},
                   'dim': {'kind': 'hdri', 'file': 'studio_small_03_1k', 'strength': 0.25},
                   'grey': {'kind': 'gradient', 'zenith': '#6E6C68', 'horizon': '#8A8884', 'ground': '#3A3835', 'strength': 1.0},
                   'dark': {'kind': 'gradient', 'zenith': '#2A2927', 'horizon': '#33322F', 'ground': '#1E1D1B', 'strength': 1.0}}[env])
    Lt.area(bpy, 'key', {'type': 'area', 'size_m': [3.2, 2.4], 'target': [0, 0, 0], 'irradiance': key, 'color': '#FFF4E6',
                         'orbit': {'azimuth_deg': -40, 'elevation_deg': 40, 'distance_m': 6.0}, 'specular': shine[0]},
            Vector((0, 0, 0)))
    if fill:                                             # a broad softbox beside the camera: translucent acrylic shows its
        Lt.area(bpy, 'fill', {'type': 'area', 'size_m': [5.0, 5.0], 'target': [0, 0, 0], 'irradiance': fill,   # colour by front light
                              'color': '#FFF8F0', 'orbit': {'azimuth_deg': 15, 'elevation_deg': 8, 'distance_m': 7.0},
                              'specular': shine[1]}, Vector((0, 0, 0)))
    r = scene.render
    r.engine = 'CYCLES'; r.resolution_x = r.resolution_y = px; r.resolution_percentage = 100; r.film_transparent = False
    cy = scene.cycles
    cy.device = 'CPU'; cy.samples = samples; cy.use_adaptive_sampling = True; cy.adaptive_threshold = adaptive
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'; cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    # light trapped in a sheet runs along it by total internal reflection, each reflection a glossy bounce: cut short,
    # an edge seen along its disc goes black (the first proofs, at 8)
    cy.max_bounces = cy.transmission_bounces = cy.glossy_bounces = bounces; cy.diffuse_bounces = 2
    cy.transparent_max_bounces = 32; cy.volume_bounces = 2
    cy.caustics_reflective = False; cy.caustics_refractive = False; cy.sample_clamp_indirect = 10.0; cy.blur_glossy = 0.5
    vs = scene.view_settings; vs.view_transform = 'Standard'; vs.look = 'None'; vs.exposure = 0.0; vs.gamma = 1.0
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.image_settings.color_depth = '8'
    r.use_persistent_data = True


def encode(frames, out):
    """A directory of spin frames (f0000.png ...) as a seamless loop, OUT.mp4 and OUT.webm, as mark.spin encodes."""
    import subprocess
    import mark as K
    src = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(K.SPIN['fps']), '-i', os.path.join(frames, 'f%04d.png')]
    subprocess.run(src + ['-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', out + '.mp4'], check=True)
    subprocess.run(src + ['-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '30', '-row-mt', '1', '-pix_fmt', 'yuv420p',
                          '-fflags', '+bitexact', '-flags:v', '+bitexact', out + '.webm'], check=True)
    return [out + '.mp4', out + '.webm']


def bloom(path, radius=0.012, strength=0.8, threshold=0.35):
    """A glow round what is bright, as a lens and an eye spread a bright light (round 28c, for the neon on dark): the
    light above `threshold` (linear, by its brightest channel) blurred `radius` of the picture's width and added back at
    `strength`. A PNG in place, or every frame f*.png of a directory."""
    import glob
    from PIL import Image
    from scipy.ndimage import gaussian_filter
    files = sorted(glob.glob(os.path.join(path, 'f*.png'))) if os.path.isdir(path) else [path]
    for f in files:
        v = np.asarray(Image.open(f).convert('RGB'), float) / 255
        lin = np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)
        hot = lin * np.clip(lin.max(axis=2, keepdims=True) - threshold, 0, None) / (1 - threshold)
        s = radius * v.shape[1]
        out = np.clip(lin + strength * np.stack([gaussian_filter(hot[..., c], s) for c in range(3)], axis=2), 0, 1)
        out = np.where(out <= 0.0031308, 12.92 * out, 1.055 * out ** (1 / 2.4) - 0.055)
        Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(f)
    return files


def _even_ground(path, ground, tol=2):
    """A render with its ground made exactly the ground's colour (the denoiser leaves it a level or two off): the
    pixels within `tol` of it that reach the picture's edge, so the file sits on a page of that colour without a seam."""
    from PIL import Image
    from scipy.ndimage import label
    v = np.asarray(Image.open(path).convert('RGB')).astype(int)
    g = np.array([int(ground[i:i + 2], 16) for i in (1, 3, 5)])
    lab, _ = label(np.abs(v - g).max(axis=2) <= tol)
    edge = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    v[np.isin(lab, edge[edge > 0])] = g
    return Image.fromarray(v.astype(np.uint8))


def mark_files(paper, night, spin=None, w=2048, out=os.path.join(HERE, 'brand', 'mark')):
    """The render as the colour mark (round 28c; the owner, asked whether it should be: "Yes"), into brand/mark: the
    still on paper and on night (`paper`, `night`; round 28d's --dark), each on its ground made even, as earf-globe-render.png and
    -render-night.png; the lockups, earf-lockup-render.png and -render-night.png, `w` px wide, laid out as
    earth.lockup_svg lays them (the globe a 450 square, EARF 110 past it, in ink or white) with a quarter of the globe
    clear round them; and `spin`'s MP4 and WebM (the paper spin, a path without its extension) as -render-spin."""
    import shutil, subprocess, tempfile
    from PIL import Image
    import marks as M
    vw, vh, gap, m = 450 + 110 + M.WORDMARK_W, 450, 110, 450 / 4
    files = []
    for src, tag, ground, word in ((paper, '', E.PAPER, E.INK), (night, '-night', E.NIGHT, E.WHITE)):
        globe = _even_ground(src, ground)
        f = os.path.join(out, f'earf-globe-render{tag}.png')
        globe.save(f)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-m} {-m} {vw + 2 * m} {vh + 2 * m}">'
               f'<rect x="{-m}" y="{-m}" width="{vw + 2 * m}" height="{vh + 2 * m}" fill="{ground}"/>'
               f'<g transform="translate({450 + gap} 75)" fill="{word}">'
               + ''.join(f'<path d="{d}"/>' for d in E.letters()) + '</g></svg>')
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, 'l.svg'), 'w').write(svg)
            subprocess.run(['rsvg-convert', '-w', str(w), os.path.join(tmp, 'l.svg'), '-o', os.path.join(tmp, 'l.png')],
                           check=True)
            lock = Image.open(os.path.join(tmp, 'l.png')).convert('RGB')
        s = w / (vw + 2 * m)
        lock.paste(globe.resize((round(450 * s), round(450 * s)), Image.LANCZOS), (round(m * s), round(m * s)))
        lf = os.path.join(out, f'earf-lockup-render{tag}.png')
        lock.save(lf)
        files += [f, lf]
    if spin:
        for ext in ('.mp4', '.webm'):
            shutil.copyfile(spin + ext, os.path.join(out, 'earf-globe-render-spin' + ext))
            files.append(os.path.join(out, 'earf-globe-render-spin' + ext))
    return files


FLATS = [('line', E.INK, E.PAPER, 'black'), ('fill', E.INK, E.PAPER, 'black'), ('line', E.WHITE, E.NIGHT, 'white'),
         ('fill', E.WHITE, E.NIGHT, 'white')]


def flat_files(out, px=1024):
    """The flat versions as files: earf-real-<line|fill>-<black|white>.svg, transparent, and a PNG of each on its
    ground."""
    import subprocess
    os.makedirs(out, exist_ok=True)
    files = []
    for style, ink, bg, tag in FLATS:
        f = os.path.join(out, f'earf-real-{style}-{tag}')
        open(f + '.svg', 'w').write(flat_svg(style, ink, None))
        open(f + '.ground.svg', 'w').write(flat_svg(style, ink, bg))
        subprocess.run(['rsvg-convert', '-w', str(px), '-h', str(px), f + '.ground.svg', '-o', f + '.png'], check=True)
        os.unlink(f + '.ground.svg')
        files += [f + '.svg', f + '.png']
    return files


def _flat_frame(job):
    import subprocess
    import mark as K
    path, style, ink, bg, spin = job
    open(path[:-4] + '.svg', 'w').write(flat_svg(style, ink, bg, spin=spin, e=1 + 2 * K.SPIN['clear']))
    subprocess.run(['rsvg-convert', '-w', str(K.SPIN['px']), '-h', str(K.SPIN['px']), path[:-4] + '.svg', '-o', path], check=True)
    os.unlink(path[:-4] + '.svg')


def flat_spins(out, frames=120):
    """The flat versions spinning, black on paper: earf-real-<line|fill>-black-spin.mp4 and .webm, half a turn."""
    import tempfile
    from multiprocessing import Pool
    import mark as K
    os.makedirs(out, exist_ok=True)
    files = []
    for style, ink, bg, tag in FLATS[:2]:
        with tempfile.TemporaryDirectory() as tmp:
            jobs = [(os.path.join(tmp, f'f{k:04d}.png'), style, ink, bg, K.SPIN['turn'] * k / frames) for k in range(frames)]
            with Pool() as pool:
                pool.map(_flat_frame, jobs)
            files += encode(tmp, os.path.join(out, f'earf-real-{style}-{tag}-spin'))
    return files


def turn(root, spin):
    """The globe at `spin` degrees on its own axis (earth.rings' meridians at their longitudes plus spin)."""
    from mathutils import Matrix
    M = Matrix([list(row) for row in orientation()]).to_4x4()
    root.matrix_world = M @ Matrix.Rotation(math.radians(spin), 4, 'Z')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--still', help='one frame, framed as the flat marks are, to this PNG')
    ap.add_argument('--spin-frames', help='the half turn, framed as the spins are, as f0000.png ... in this directory')
    ap.add_argument('--spin', type=float, default=0.0, help='with --still, the globe turned this far on its axis')
    ap.add_argument('--frames', type=int, default=120)
    ap.add_argument('--ground', choices=sorted(GROUNDS), help="paper, or the preset's")
    ap.add_argument('--px', type=int)
    ap.add_argument('--samples', type=int)
    ap.add_argument('--env', choices=['studio', 'dim', 'grey', 'dark'],
                    help="the room seen in the acrylic: round 28d's plain grey, on paper and on dark, as the studio's softbox "
                         "flashed in each rim turning toward the camera (round 28b: studio)")
    ap.add_argument('--tint', default='glow', choices=['cabinet', 'glow', 'horn', 'horn-glow'],
                    help="glow()'s tints of the cabinets', the cabinets' own, or the horns' (round 28d), raw or through glow()")
    ap.add_argument('--slots', action='store_true', help='the discs slotted through one another, not cemented clear')
    ap.add_argument('--depth', type=float, default=MARK_DEPTH, help='the path (m) after which the acrylic is its tint')
    ap.add_argument('--look', default='translucent', choices=['clear', 'translucent'],
                    help="translucent in the mark's hues (round 28b), or clear tinted (round 28: with --env dim --key 2 --fill 0)")
    ap.add_argument('--scatter', type=float, default=0.012, help='translucent: how far (m) light scatters into the acrylic')
    ap.add_argument('--clear', type=float,
                    help="translucent: the share of light crossing straight through (0.45, or the preset's; round 28b: 0.25)")
    ap.add_argument('--key', type=float, help="the key's irradiance (W/m2 at the globe; 4, or the preset's)")
    ap.add_argument('--fill', type=float, help="a front fill's irradiance (0: none; 4, or the preset's)")
    ap.add_argument('--milk', type=float, default=0.0, help='clear: a share of the light scattered in the sheet (round 28d)')
    ap.add_argument('--body', choices=['mark', 'cabinet', 'horn', 'through', 'through-deep'],
                    help="translucent: the surface and the scatter both the mark's hue (round 28b); the surface the cabinets' tint and "
                         "the scatter the horns' colour (cabinet); both the horns' (horn); or the surface the mark's hue's square "
                         "root, so a disc seen through over the paper is the mark's hue (through; through-deep a little deeper, "
                         "or the preset's)")
    ap.add_argument('--vivid', type=float, nargs=2, metavar=('CHROMA', 'LIFT'),
                    help="the hues the body follows, livelier (round 28e): their chroma times CHROMA, their lightness raised by "
                         "LIFT (OKLCh; 1.4 0.05, or the preset's)")
    ap.add_argument('--crossings', default='equator', choices=['equator', 'fused'],
                    help="the equator's edge unbroken where it meets the meridians (round 28d), or both acrylics there (round 28)")
    ap.add_argument('--shine', type=float, nargs=2, default=(0.4, 0.0), metavar=('KEY', 'FILL'),
                    help="the key's and the fill's shares in reflections (round 28d; until then 1 1)")
    ap.add_argument('--bounces', type=int, default=96, help='how far light runs along a sheet inside it (glossy and transmission bounces)')
    ap.add_argument('--neon', type=float, nargs=2, metavar=('RIM', 'FACE'),
                    help="fluorescent acrylic for dark grounds (round 28c): the rims and the faces give off light at these "
                         "strengths (none, or the preset's)")
    ap.add_argument('--bloom', help='a glow round what is bright, on this PNG or every frame of this directory, in place')
    ap.add_argument('--glow', action='store_true',
                    help='the colour mark for dark grounds (round 28c): GLOW where not given, and bloom() on each frame')
    ap.add_argument('--dark', action='store_true', help='the colour mark for dark grounds (round 28d): DARK where not given, no bloom')
    ap.add_argument('--mark', nargs=3, metavar=('PAPER', 'NIGHT', 'SPIN'),
                    help='the render as the colour mark, into brand/mark: the stills, the lockups and the paper spin (no extension)')
    ap.add_argument('--first', type=int, default=0, help='with --spin-frames, start at this frame (a resumed run)')
    ap.add_argument('--last', type=int, help='with --spin-frames, stop before this frame')
    ap.add_argument('--adaptive', type=float, help='the noise Cycles stops sampling at (0.01 a still, 0.02 the spin)')
    ap.add_argument('--encode', nargs=2, metavar=('FRAMES', 'OUT'), help='spin frames to OUT.mp4 and OUT.webm, as mark.py encodes')
    ap.add_argument('--flat', help='the flat line and fill versions, black on paper and white on night, as SVG and PNG here')
    ap.add_argument('--flat-spin', help='the flat versions spinning, black on paper, as MP4 and WebM here')
    a = ap.parse_args()
    if a.encode:
        for f in encode(*a.encode):
            print(f)
    if a.flat:
        for f in flat_files(a.flat):
            print(f)
    if a.flat_spin:
        for f in flat_spins(a.flat_spin):
            print(f)
    if a.bloom:
        print(f'{len(bloom(a.bloom))} bloomed')
    if a.mark:
        for f in mark_files(*a.mark):
            print(f)
    if not (a.still or a.spin_frames):
        return
    lighting(a)
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.preferences.addon_enable(module='cycles')
    t0 = time.time()
    base = HORN if a.tint.startswith('horn') else ACRYLIC
    root = build(bpy, base if a.tint in ('cabinet', 'horn') else {k: glow(v, passed=PASS.get(k, '')) for k, v in base.items()},
                 not a.slots, a.depth, a.look, a.scatter, a.clear, tuple(a.neon), a.crossings, a.milk,
                 _body(a.body, _hues(*a.vivid)))
    if a.still:
        stage(bpy, a.ground, a.px or 1024, 1 + E.W_LINE / 2, a.samples or 128, a.env, a.adaptive or 0.01, a.key, a.fill,
              tuple(a.shine), a.bounces)
        turn(root, a.spin)
        bpy.context.scene.render.filepath = os.path.abspath(a.still)
        bpy.ops.render.render(write_still=True)
        if a.glow:
            bloom(a.still)
        print(f'{a.still}  {time.time() - t0:.0f} s')
    if a.spin_frames:
        os.makedirs(a.spin_frames, exist_ok=True)
        import mark as K
        stage(bpy, a.ground, a.px or K.SPIN['px'], 1 + 2 * K.SPIN['clear'], a.samples or 24, a.env, a.adaptive or 0.02,
              a.key, a.fill, tuple(a.shine), a.bounces)
        for k in range(a.first, a.last or a.frames):
            t1 = time.time()
            turn(root, K.SPIN['turn'] * k / a.frames)
            bpy.context.scene.render.filepath = os.path.join(os.path.abspath(a.spin_frames), f'f{k:04d}.png')
            bpy.ops.render.render(write_still=True)
            if a.glow:
                bloom(bpy.context.scene.render.filepath)
            print(f'frame {k}  {time.time() - t1:.0f} s', flush=True)


if __name__ == '__main__':
    main()
