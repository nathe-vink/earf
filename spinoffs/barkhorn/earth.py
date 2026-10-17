"""EARF's globe as a 3D Earth, and the software it moves in (rounds 22 and 23).

The owner, of round 21's five globes: "Get rid of the black and white segments. Also we're kind of losing site of the
fact that it's supposed to look like earth. Maybe movie animation was a bad lead. More like late 90s early 2000s
computer software animation and design", "I want the color to appear after each circle is closed", and: "the logo has
to work in white only, black only, single color, multicolor and animated. That might help put some guide rails on it.
I like the idea of it being a 3 dimensional earth. Maybe three longitudinal and three latitudinal ovular strokes, with
the object tilted in such a way to show its depth. Then you could have those be colored discs without strokes as well."
And three more ideas: "A loading animation where a white circle on a black background rolls left to right revealing
red orange yellow green blue and purple circles, or the inverse with a black circle on a white background", "A cursor
animation where the cursor is a circle and followed by a trail of rainbow circles with some delay on it", and "A
spinning disc silhouette that looks like a coin spinning. It can flash each color and eventually become a globe".

- The globe: a sphere's three parallels (40 N, the equator, 40 S) and three meridians (60 apart), its axis leaning
  23.4 degrees, as the Earth's does and a desk globe's stand holds it, and tipped 16 degrees toward us (22 until round
  27f), so the parallels open into ovals and the far side shows through behind the near. Six rings, one for each
  colour Cloud, drawn in spectrum order: the parallels warm, north to south (Flare, Dust, Acid), the meridians cool,
  west to east (Poison, Ice, Haze). Nothing black or white is in it; Smoke and Fog are the black-only and white-only marks.
- Lines: the six ovals, the far halves lighter and under the near, so even in one colour the near side reads in front
  (the even version, every line one weight, tangles in one colour). Tubes (round 23): the even lines as tubes of
  tinted acrylic, see-through where they cross. Discs: each ring
  filled as a flat disc, no strokes, the discs crossing one another as six sheets of the Clouds' tinted acrylic slotted
  into a globe would, each showing only where nothing nearer covers it, a seam of the ground between facets.
- The software kit: the loader (a white circle rolling across black uncovers the six colours in its wake, and covers
  them again on its way back; or black on paper) and the cursor (a circle with the six colours trailing it, each a
  beat behind).

Round 23. The owner, of round 22's ident: "I like the even lines, but not the animation. I like the discs, but not the
animation. Instead of them being drawn, what else can we try? One idea I had was to have a parent ring or disc move
back and forth similar to a printer, leaving pieces in its wake. Another idea is to have two gyroscopic rings spin on
different axis until they align to reveal the globe. Another is using the disks and/or circles to makes a speaker
kick/reverb effect and shape", "The coin animation wasn't working for me", and of the draw: "It doesn't seem fluid or
quick enough". So four idents, each about two seconds, none drawn, the even lines the default:

- Printer: a disc sweeps across and back six times, like a print head, and leaves the globe behind it band by band.
- Gyroscope: two rings spin on crossed axes, slowing, until they settle as the equator and the meridian facing us;
  the other four open out from them.
- Kick: the globe seen from above its pole is a speaker, rings round one centre; it kicks twice, each kick sending
  three rings of colour out, then tips down to the Earth's tilt.
- Coin: round 22's coin, faster, starting only once it is in view, and looping in the player.

Then the globe moves aside and EARF types in. The theme section shows an icon for each Cloud (icons.py) and the line's
name four ways (Clouds, Atmosphere, Elements, and the colours as chemical elements).

    python3 spinoffs/barkhorn/earth.py                  ->  brand/earth.html, brand/earth-<style>-<colour>.svg,
                                                            brand/earth-lockup-<ground>.svg
    python3 spinoffs/barkhorn/earth.py --fragment PATH  ->  also the page as an Artifact's body
    python3 spinoffs/barkhorn/earth.py --video [--fonts CSS]  ->  also brand/earth-<scene>-<ground>.mp4
"""
import argparse, json, math, os, re, shutil, subprocess, sys, tempfile

import numpy as np
from shapely.geometry import LineString, MultiLineString, MultiPoint, Point, Polygon
from shapely.ops import linemerge, polygonize, unary_union
from shapely import affinity, make_valid, set_precision, union_all

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import marks as M                                        # noqa: E402
import icons as IC                                       # noqa: E402

OUT = os.path.join(HERE, 'brand')
LEAN, ELEV, LAT = 23.44, 16.0, 40.0                      # the axis's lean (the Earth's), its tip toward us, the parallels
# (the tip: 22 until round 27f, when the owner chose 16 from round 27e's angle study, mark.py --angles: the discs'
# tips, where their rims meet the globe's outline past the front disc, reach about half as far, 0.04 of the radius)
MERIDIANS = (30.0, 90.0, 150.0)                          # the meridians' longitudes at rest (90 faces us: the rim)
W_LINE, W_DEPTH, SEAM = 0.075, 0.42, 0.035               # of the globe's radius: the line, the far line's share, the seam
KEEP = 1.0                                               # the one-colour discs' thinnest piece, in seams (round 27l: the
                                                         # owner, "missing segments to the left and right of the butt";
                                                         # at 1.5 it dropped the green disc's rim either side of it)
CLOUDS = [(name, colour) for key, line, num, name, colour in M.SPEAKERS if line == 'Cloud']
HUES = [c for n, c in CLOUDS if n not in ('Fog', 'Smoke')]          # Flare Dust Acid Poison Ice Haze, the spectrum
NAMES = [n for n, c in CLOUDS if n not in ('Fog', 'Smoke')]
_C = dict(CLOUDS)
# the rings' colours, ring by ring (the parallels north to south, then the meridians at 30, 90 and 150). Round 24 (the
# owner: "The horizontal discs should actually be the primary colors") put the primaries on the parallels and the
# secondaries on the meridians, violet facing us. Round 25 (the owner: "Purple is the dominant disc color but it should
# be blue and green. Rearrange discs accordingly"): the meridian facing us, the largest disc, is green, the land, and the equator,
# the widest band, blue, the sea; red north and yellow south; of the two side meridians, the one that shows larger is
# orange and the one that shows less violet. The loader, the cursor and the coin's flashes keep the spectrum (HUES)
RING = [_C['Flare'], _C['Ice'], _C['Acid'], _C['Haze'], _C['Poison'], _C['Dust']]
RING_NAMES = ['Flare', 'Ice', 'Acid', 'Haze', 'Poison', 'Dust']
# the acrylic. Round 24 tinted every disc and laid them in a fixed order, which read as six overlapping ovals; the owner
# (round 25): "The acrylic is meant to be a transparent version of the discs but it looks very different", and "Push it
# further". So the acrylic is the discs' own mosaic, see-through: wherever you look through the globe, the discs crossed
# there are laid front to back, the nearest keeping `face` of what shows, the next `face` of the rest, and so on, the ground
# taking what is left; so the nearest face leads and those behind show through it as ghosts, the discs' own layout and
# colours. After the brand critic's first round (critic/rounds/2026-10-15/brand-acrylic-r1.json): the faces stronger
# (0.45 and 0.55 read as "a pale bubble behind a cage of hoops"), no coloured edges in colour (`edge` 0: they read as
# strokes, which the discs do not have; a thin glint is the owner's to choose), the colours mixed in OKLCh (lightness and
# chroma weighted, the hue a circular mean weighted by chroma), so crossings are clean colours, not the greys and browns
# that mixing in sRGB makes; and in one colour the acrylic is the lines (a tint of one colour stacked to a solid blob).
# After its second round (critic/rounds/2026-10-15/brand-acrylic-r2.json), a cleaner rule: inside the ball the ground takes
# nothing, and the green (the meridian facing you, with the ball it fills) is the backing. Where coloured discs lie in
# front of the green they share all of what shows, the nearest keeping `face`, the next `face` of the rest, the farthest
# what is left, so a single disc shows its own flat colour, as in the discs, and only crossings mix, each a step deeper
# (`dark`, OKLab lightness, a sheet beyond the first), as stacked tinted sheets go; where none does, the green keeps
# `green` of what shows and the back halves behind it share the rest, faint ghosts. So paper and ink match inside the rim
# Its third round (brand-acrylic-r3.json): crossings mixed as stacked tinted sheets, not as paint (_stack): each a step
# deeper than the darkest sheet in it, opposed tints going smoky (`smoke`, OKLab lightness, the less the hues agree);
# `face` 0.5, so a crossing is one colour whichever sheet is in front, as filters are; the green 0.8, so the back
# halves read as the rings' far sides, not dirt
# The owner after it: "For acrylic I was expecting each disc to have a little thickness to it": each disc a slab `thick`
# thick (of the radius), its side, where we see it, a deeper tone of its tint (`side`, OKLab lightness lower; `sideC`,
# the chroma raised), as a polished acrylic edge looks, light running the length of the sheet (slabs)
# Round 27b. The owner: "The acrylic doesn't look right though in terms of having the same corners where discs meet".
# In the discs the nearest disc shows, so where two discs cross they meet along the line their planes share, with sharp
# corners where three meet (the pinwheel at the middle, the red triangle at the top); the acrylic mixed every crossing
# the same whichever disc was in front, so those lines and corners were gone, only the ovals' outlines left, and each
# slab's face stood a little in front of its disc. So now the nearest disc leads (`lead` of what shows) and those behind
# share the rest, nearest first, each keeping `ghost` of what is left: the discs' own pieces and corners, with the discs
# behind showing through them; each sheet behind a step deeper (`deep`, OKLab lightness, at most three); and each
# slab's face lies on its disc, its thickness running back (slabs). (`face`, `green`, `dark` and `smoke` are round 25's
# rule, which the parked idents' player still draws.)
ACRYLIC = dict(paper=dict(face=0.5, edge=0.0, green=0.8, dark=0.04, smoke=0.10, thick=0.05, side=0.10, sideC=0.15,
                          lead=0.8, ghost=0.6, deep=0.02),
               night=dict(face=0.5, edge=0.0, green=0.8, dark=0.04, smoke=0.10, thick=0.05, side=0.10, sideC=0.15,
                          lead=0.8, ghost=0.6, deep=0.02))
ATMOS = 4                                               # the meridian facing us (round 25: Poison, green, the land); in
                                                        # the acrylic, the backing. (Round 24b filled the ball in its
                                                        # colour; round 25, the owner: "this artificial green completing
                                                        # the circle shape that isn't one of the discs", so no fill: the
                                                        # globe is its discs alone)
PAPER, INK, WHITE = '#F2EFEA', '#1C1A18', '#F6F5F2'
# round 23 (the owner: "Could try one where the even lines look like acrylic tubes"): each ring a tube of tinted acrylic,
# a little bolder than the line so its shading reads: a faint tint through its middle (core), deeper along its two
# walls (wall, at wall_at either side, wall_w wide), and a highlight toward the light, up and to the left (hi: its
# offset, width and opacity, of the tube's width); the tint multiplies over what is behind it on paper and glows
# (screen) on ink, so wherever two rings cross, one shows through the other; each ring fading with depth to `far` at
# the back (from depth -fade to +fade; a ring is flat, so its depth runs straight across the picture and a linear
# gradient fades it exactly), so the near side reads in front. Blending in either order comes to the same, so each
# ring's tint is one unbroken loop (no joins to show); the highlights go over every tint, on the near side only,
# coming in from the rim over depth `shine`. Tried and left: every run alike, which tangles; the far runs at half all
# at once, which steps at the rim; a glint through the far wall, which crowds it; solid rods, no walls, which read as
# plastic rather than glass
W_TUBE = 0.105
TUBE = dict(core=0.45, wall=0.8, wall_at=0.36, wall_w=0.28, hi=(-0.16, -0.2, 0.12, 0.9), far=0.5, fade=0.5, shine=0.3)
_GRAD = [0]                                              # gradient ids, unique across a page of many marks
NIGHT = '#121114'                                        # the ink ground
WOBBLE = [0.0, 0.0]                                      # round 27e, the spin: the axis tipped this many degrees toward
                                                         # this direction round it (radians), as a top's wobbles
GRID = 1e-6                                              # round 27e: the overlays snapped to this grid (of the radius).
                                                         # Unsnapped, a face's last clip to the globe's outline could
                                                         # drop a whole cell at a few angles, a hole for one frame
LATERAL = None                                           # round 27g's study (the owner: "What would it look like if
                                                         # the lateral discs intersected like the longitudinal discs
                                                         # do?"): the three lateral discs as great circles through the
                                                         # globe's side axis (longitude 90, across the picture), as the
                                                         # meridians go through the pole, each tilted this many degrees
                                                         # from the equator, its near half up (north first). None: the
                                                         # parallels, 40 N, the equator and 40 S


def basis(lean=LEAN, elev=ELEV):
    """The globe's axis and its longitude 0 and 90 directions on screen (x right, y up, z toward us); with a WOBBLE, all
    three turned so the axis leans that far toward that direction (mark.py's spin sets it frame by frame)."""
    t, e = math.radians(lean), math.radians(elev)

    def rot(v):
        x, y, z = v
        y, z = y * math.cos(e) - z * math.sin(e), y * math.sin(e) + z * math.cos(e)
        return np.array([x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t), z])
    a, e1, e2 = rot((0, 1, 0)), rot((0, 0, 1)), rot((1, 0, 0))
    beta, phi = WOBBLE
    if beta:                                             # Rodrigues: each turned beta about w, square to the axis
        w, b = math.cos(phi) * e1 + math.sin(phi) * e2, math.radians(beta)
        a, e1, e2 = (v * math.cos(b) + np.cross(w, v) * math.sin(b) + w * np.dot(w, v) * (1 - math.cos(b)) for v in (a, e1, e2))
    return a, e1, e2


def rings(spin=0.0, n=360):
    """The six rings, each a closed loop of points with its disc's plane (n . p = d), centre and radius."""
    a, e1, e2 = basis()
    s = np.linspace(0, 2 * math.pi, n, endpoint=False)
    out = []
    if LATERAL is not None:                              # (round 27g's study) great circles through the side axis,
        sp = math.radians(spin)                          # turning with the globe as the meridians do
        fwd, side = math.cos(sp) * e1 + math.sin(sp) * e2, -math.sin(sp) * e1 + math.cos(sp) * e2
        for tilt in LATERAL:
            if tilt is None:                             # a disc left out: a ring of no size, drawn nowhere
                out.append(dict(pts=np.zeros((n, 3)), n=a, d=0.0, c=np.zeros(3), r=0.0)); continue
            t = math.radians(tilt)
            nrm = math.cos(t) * a - math.sin(t) * fwd
            out.append(dict(pts=np.outer(np.cos(s), side) + np.outer(np.sin(s), np.cross(nrm, side)), n=nrm, d=0.0,
                            c=np.zeros(3), r=1.0))
    for phi in ((LAT, 0.0, -LAT) if LATERAL is None else ()):
        p = math.radians(phi)
        pts = math.cos(p) * (np.outer(np.cos(s), e1) + np.outer(np.sin(s), e2)) + math.sin(p) * a
        out.append(dict(pts=pts, n=a, d=math.sin(p), c=math.sin(p) * a, r=math.cos(p)))
    for lam in MERIDIANS:
        l = math.radians(lam + spin)
        u = math.cos(l) * e1 + math.sin(l) * e2
        out.append(dict(pts=np.outer(np.cos(s), u) + np.outer(np.sin(s), a), n=np.cross(u, a), d=0.0, c=np.zeros(3), r=1.0))
    return out


def _runs(pts, front):
    """A closed ring's runs on the near side (z > 0) or the far side, each cut exactly where it crosses the rim."""
    z = pts[:, 2]
    side = z > 0 if front else z <= 0
    if side.all():
        return [np.vstack([pts, pts[:1]])]
    if not side.any():
        return []
    n, k = len(pts), int(np.argmax(~side))              # start from a point off the side, so every run opens on the rim
    out, cur = [], []
    for j in range(1, n + 1):
        i, prev = (k + j) % n, (k + j - 1) % n
        if side[i] != side[prev]:                        # the crossing between them, on the rim
            c = pts[prev] + z[prev] / (z[prev] - z[i]) * (pts[i] - pts[prev])
            if side[i]:
                cur = [c]
            else:
                cur.append(c); out.append(np.array(cur)); cur = []
        if side[i]:
            cur.append(pts[i])
    return [r for r in out if len(r) > 1]


def _d(c):
    c = np.asarray(c)
    return 'M' + 'L'.join(f'{x:.3f} {-y:.3f}' for x, y in c[:, :2])


def _poly_d(g):
    if g.is_empty:
        return ''
    if g.geom_type == 'Polygon':
        return ' '.join(_d(np.array(r.coords)) + 'Z' for r in [g.exterior] + list(g.interiors))
    return ' '.join(_poly_d(x) for x in getattr(g, 'geoms', []) if x.geom_type in ('Polygon', 'MultiPolygon'))


def lines_body(colours, depth=False, spin=0.0, w=W_LINE):
    """The six ovals as SVG paths on the unit globe (y down): every far run first, then every near run over them."""
    rs = rings(spin)
    far = ''.join(f'<path d="{_d(r)}" stroke="{colours[i]}" stroke-width="{w * (W_DEPTH if depth else 1):.4f}"/>'
                  for i, g in enumerate(rs) for r in _runs(g['pts'], False))
    near = ''.join(f'<path d="{_d(r)}" stroke="{colours[i]}" stroke-width="{w:.4f}"/>'
                   for i, g in enumerate(rs) for r in _runs(g['pts'], True))
    return f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">{far}{near}</g>'


def _offset(c, d, closed):
    """A polyline (SVG coordinates) moved d along its normal at every point."""
    if closed:
        prev, nxt = np.roll(c, 1, 0), np.roll(c, -1, 0)
    else:
        prev, nxt = np.vstack([c[:1], c[:-1]]), np.vstack([c[1:], c[-1:]])
    t = nxt - prev
    L = np.hypot(t[:, 0], t[:, 1])[:, None]
    L[L == 0] = 1.0
    return c + np.stack([-t[:, 1], t[:, 0]], 1) / L * d


def _depth_ends(g, z0, z1):
    """Where on the picture (SVG coordinates) the ring's plane is at depths z0 and z1: the ends of a gradient that
    follows its depth; None if the plane faces us or is seen edge on."""
    n, c = g['n'], g['c']
    if abs(n[2]) < 0.03:
        return None
    gx, gy = -n[0] / n[2], -n[1] / n[2]
    m2 = gx * gx + gy * gy
    if m2 < 1e-9:
        return None
    at = lambda zz: (c[0] + gx * (zz - c[2]) / m2, -(c[1] + gy * (zz - c[2]) / m2))
    return at(z0), at(z1)


def tubes_body(colours, ground='paper', spin=0.0, w=W_TUBE, T=None):
    """The six rings as acrylic tubes (TUBE): each ring's tint (core and walls, blended) one unbroken loop fading
    with depth, then every highlight over them, on the near side. A ring seen edge on (no depth gradient) is drawn in
    runs instead, its far runs at T['far'] and its highlight on its near runs."""
    T = {**TUBE, **(T or {})}
    mode, defs, tints, lights = ('screen' if ground == 'night' else 'multiply'), [], [], []
    path = lambda c, closed: 'M' + 'L'.join(f'{x:.4f} {y:.4f}' for x, y in c) + ('Z' if closed else '')

    def grad(ends, colour, a0):
        _GRAD[0] += 1
        (x1, y1), (x2, y2) = ends
        defs.append(f'<linearGradient id="tube{_GRAD[0]}" gradientUnits="userSpaceOnUse" x1="{x1:.4f}" y1="{y1:.4f}" '
                    f'x2="{x2:.4f}" y2="{y2:.4f}"><stop offset="0" stop-color="{colour}" stop-opacity="{a0}"/>'
                    f'<stop offset="1" stop-color="{colour}"/></linearGradient>')
        return f'url(#tube{_GRAD[0]})'

    def tube(c, closed, paint, k):
        tint = f' stroke="{paint}" style="mix-blend-mode:{mode}"'
        tints.append(f'<path d="{path(c, closed)}"{tint} stroke-opacity="{T["core"] * k:.3f}" stroke-width="{w:.4f}"/>')
        tints.extend(f'<path d="{path(_offset(c, sg * T["wall_at"] * w, closed), closed)}"{tint} stroke-opacity="{T["wall"] * k:.3f}" '
                     f'stroke-width="{T["wall_w"] * w:.4f}"/>' for sg in (1, -1))

    def light(c, closed, paint):
        dx, dy, lw, op = T['hi']
        lights.append(f'<path d="{path(c + [dx * w, dy * w], closed)}" stroke="{paint}" stroke-opacity="{op}" stroke-width="{lw * w:.4f}"/>')

    clean = lambda c: c[np.r_[True, np.hypot(*np.diff(c, axis=0).T) > 1e-9]]   # no repeated points: they skew a butt end
    for i, g in enumerate(rings(spin)):
        tint_ends, light_ends = _depth_ends(g, -T['fade'], T['fade']), _depth_ends(g, 0.0, T['shine'])
        if tint_ends:
            c = g['pts'][:, :2] * [1, -1]
            tube(c, True, grad(tint_ends, colours[i], T['far']), 1.0)
            light(c, True, grad(light_ends, '#FFFFFF', 0))
            continue
        for front in (False, True):
            for r in _runs(g['pts'], front):
                closed = len(r) > 2 and np.allclose(r[0], r[-1])
                c = clean(np.asarray(r[:-1] if closed else r)[:, :2] * [1, -1])
                tube(c, closed, colours[i], 1.0 if front else T['far'])
                if front:
                    light(c, closed, '#FFFFFF')
    return (f'<defs>{"".join(defs)}</defs><g fill="none" stroke-linecap="butt" stroke-linejoin="round">'
            f'{"".join(tints)}{"".join(lights)}</g>')


# Round 27k. The owner, of the spin: "each disc flattens when it lines up straight on, instead of reading as a disc
# with thickness." A disc turning edge on narrowed to a line and was gone for a few frames; a slab of acrylic turning
# edge on shows its edge, a band as wide as it is thick. So every disc is now a slab `THICK` thick (the acrylic's own)
# that shows its thickness as it nears edge on (_slab): its face moves toward us by half the thickness it shows and its
# rim shows on the near side, a slab's true picture, the thickness shown fading from all of it edge on to none by the
# time its oval is four times as wide as it is thick (at twice, the disc thinned where another lay close in front of
# its face, as the equator does at the middle), so the disc keeps its thickness and goes through edge on without a
# jump. The rim lies on the globe's surface, so nothing is in front of it. Seamed, the thickness is the ink's, the seam
# added to it. At rest every disc is wider than four times its thickness, so the mark at rest is as it was; only the
# spin's frames near edge on change.
THICK = ACRYLIC['paper']['thick']


def _slab(g, t):
    """A ring's disc as a slab t thick (round 27k), its thickness shown as it nears edge on: shown r = t - w / 4 thick (w
    its oval's width across), so its face (a ring like g) moved r / 2 toward us along its normal and its rim (a polygon,
    on the near side) r wide; r is t edge on and nothing from w = 4t. Returned as (face, rim)."""
    n = np.asarray(g['n'], float)
    if t <= 0 or g['r'] <= 0:
        return g, Polygon()
    m = n * (1.0 if n[2] >= 0 else -1.0)                 # its normal, turned toward us
    L = math.hypot(m[0], m[1])
    if L < 1e-9:                                         # face on
        return g, Polygon()
    P = g['pts']
    r = t - float(np.ptp(P[:, :2] @ (m[:2] / L))) / 4
    if r <= 0:
        return g, Polygon()
    off = r / 2 * m
    face = dict(g, pts=P + off, d=g['d'] + float(n @ off), c=np.asarray(g['c']) + off)
    hull = MultiPoint(np.vstack([face['pts'][:, :2], P[:, :2] - off[:2]])).convex_hull
    return face, hull.difference(Polygon(face['pts'][:, :2]).buffer(0))


def facets(spin=0.0, thick=0.0):
    """Each disc's visible part: its own oval less every other disc's oval where that disc is nearer (two planes'
    depths differ linearly across the screen, so where one is nearer is a half-plane). Round 27k: with `thick`, each
    disc a slab that thick (_slab); the rim a disc nearly edge on shows lies on the globe's surface, so it shows whole
    and hides what lies under it."""
    rs, rims = zip(*(_slab(g, thick) for g in rings(spin)))
    E = [Polygon(g['pts'][:, :2]).buffer(0) for g in rs]
    out = []
    for i, gi in enumerate(rs):
        vis, ni = E[i], gi['n']
        if abs(ni[2]) < 1e-6:                            # edge on: its rim alone, if it has one
            vis = Polygon()
        else:
            for j, gj in enumerate(rs):
                nj = gj['n']
                if j == i or abs(nj[2]) < 1e-6:
                    continue
                A = -nj[0] / nj[2] + ni[0] / ni[2]
                B = -nj[1] / nj[2] + ni[1] / ni[2]
                C = gj['d'] / nj[2] - gi['d'] / ni[2]
                m = math.hypot(A, B)
                if m < 1e-12:                            # parallel planes: one is nearer everywhere
                    if C > 0:
                        vis = vis.difference(E[j])
                    continue
                ux, uy, c0 = A / m, B / m, -C / m
                px, py, tx, ty, big = ux * c0, uy * c0, -uy, ux, 4.0
                half = Polygon([(px + tx * big, py + ty * big), (px - tx * big, py - ty * big),
                                (px - tx * big + ux * big, py - ty * big + uy * big), (px + tx * big + ux * big, py + ty * big + uy * big)])
                vis = vis.difference(E[j].intersection(half))
        others = [r for j, r in enumerate(rims) if j != i and not r.is_empty]
        if others:
            vis = vis.difference(unary_union(others))
        if not rims[i].is_empty:
            vis = unary_union([vis, rims[i].difference(unary_union(rims[:i]))])
        out.append(vis)
    return out


def _ring():
    """The outer ring (round 28c): the rim of the green disc facing us at rest, the meridian at 90, as a polygon. Its
    disc is tipped with the globe, so the ring falls 4% short of the sphere at the poles, and every disc whose rim
    reaches the sphere there passes it: the parallels by a sliver (the south one at the lower left, its stroke standing
    out past the ring: the owner, "Why is the bottom equator disc stroke sticking out further here, while the other discs
    fit cleanly into the outer circular stroke?"), the side meridians by their caps either side of the south pole."""
    return Polygon(rings(0.0)[4]['pts'][:, :2]).buffer(0)


def _cut(fs):
    """The parallels' facets cut to the outer ring (round 28c), so their slivers past it go and the outline there is the
    ring's; the meridians whole, their caps either side of the butt kept. (Round 28c first cut every piece to the ring;
    the owner: "Never mind on stroking out the butt. It doesn't look as three dimensional when the bottom is cut off.")
    Each first its polygons alone (an overlay can leave lines beside them), and cut at full precision: snapped to the
    grid one by one, two facets' shared edge no longer matched, and the line version drew it twice (a line a hair
    heavier for a frame). The parallels never move in the spin, so their cut is the same in every frame."""
    ring = _ring()
    out = []
    for i, f in enumerate(fs):
        polys = [p for p in getattr(f, 'geoms', [f]) if p.geom_type in ('Polygon', 'MultiPolygon') and not p.is_empty]
        g = unary_union(polys) if polys else Polygon()
        out.append(g.intersection(ring) if i < 3 and polys else g)
    return out


def _parts(fs):
    """The facets' pieces, each a polygon."""
    return [p for f in fs for p in getattr(f, 'geoms', [f]) if p.geom_type == 'Polygon' and p.area > 1e-7]


def _holds(p, seam=SEAM, keep=KEEP):
    """Whether a piece, shrunk by half a seam (its hairlines closed), is still `keep` seams across (round 27c)."""
    q = p.buffer(-seam / 2, join_style=2, mitre_limit=4)
    k = 0.3 * seam
    q = q.buffer(-k, join_style=2, mitre_limit=4).buffer(k, join_style=2, mitre_limit=4)
    return not q.is_empty and not q.buffer(-keep / 2 * seam).is_empty


def _kept(fs, seam=SEAM, keep=KEEP):
    """The pieces the one-colour discs keep (round 27c): each that holds at the seam."""
    return [p for p in _parts(fs) if _holds(p, seam, keep)]


def disc_shapes(spin=0.0, flush=True, seam=SEAM, lap=0.004, keep=KEEP, cut=None, thick=THICK):
    """Each disc's visible part as drawn. In colour the discs are flush (round 24b, the owner: "For the discs, I want
    them to not have strokes, so they are flush. The strokes should be the non-color versions"): each part whole, a
    hair (`lap`) larger than itself so no hairline of the ground shows between two, the globe's own edge kept exact.
    Round 25: the globe is the discs alone, with no ball filled under them (the owner: "this artificial green completing
    the circle shape that isn't one of the discs"), so its outline is theirs. In one colour the seams are the strokes,
    and round 27c (the owner: "The stroke around the monochromatic ones looks odd. Don't think we need it") takes away
    the band round the outline that round 24b kept whole: every part is shrunk by half a seam on every side, the
    outline's sides too, so a seam of the ground lies between any two parts and round the outside alike; a part thinner
    than `keep` seams (a sliver of a disc's tip) is dropped; and the whole is scaled back to the discs' own
    width. (Round 27d trimmed every part to the green disc, the meridian facing us; the owner: "I kind of like it
    untrimmed because it's true to the shape of the combined discs", so the tips stay.) `keep`: the thinnest part kept,
    in seams; 0 in the spin (round 27e), where a part dropped at its threshold would pop out between two frames,
    so it narrows away into the seam instead (and so is a part the hairlines' pass would take whole, as a disc nearly
    edge on, a long strip, would be). Returned as one shape, at index 0. Round 27k: each disc a slab `thick` thick
    (facets; seamed, that much ink between its seams), so turning edge on it shows its edge; and a small cut (`cut`):
    the pieces the full drawing keeps, at its own seam, drawn with the seam `cut`, so every piece of it is still there
    (round 27's cuts dropped what their wider seams would not hold, which bit holes in the outline), save one the cut's
    own seam leaves under a seam across, which would draw as a grey speck (round 27l: the green disc's rim either side of
    the butt, under a pixel wide at 64 px). Round 28c: in the spin (keep 0) the discs have no thickness, so a disc
    turning side on narrows away between its two seams and, side on, is one white stroke across the front of the
    globe, as wide as every other seam (27k's slab left a strip of ink between two seams, which read as a crack, and
    round 28b grew it into its seams, a bar between hairlines; the owner: "It should just be the white stroke on the
    side-on meridian, no? ... at 153 and 27 degrees the white stroke gets smaller and disappears when that's when it
    should be front and center", and then: "This meridian should be a white stroke just like the rest of the white
    strokes"); at rest that changes nothing. And in one colour, at rest and in the spin, the parallels are cut to the
    outer ring (_cut), so their slivers past it go; the meridians' caps stay."""
    fs = facets(spin, thick + (0 if flush else seam) if flush or keep else 0.0)   # (round 28c: no slab in the spin)
    if not flush:                                        # (round 28c: the parallels cut to the outer ring)
        fs = _cut(fs)
    sil = unary_union([f for f in fs if not f.is_empty])
    if not flush and cut:                                # round 27k: a small cut, the full drawing's pieces, seamed wider
        g0 = unary_union([p.buffer(-cut / 2, join_style=2, mitre_limit=4) for p in _kept(fs, seam, keep)
                          if _holds(p, cut, keep)])
        k = 0.3 * seam
        g = g0.buffer(-k, join_style=2, mitre_limit=4).buffer(k, join_style=2, mitre_limit=4).intersection(g0)
        s_ = (sil.bounds[2] - sil.bounds[0]) / (g.bounds[2] - g.bounds[0])
        return [affinity.scale(g, s_, s_, origin=(0, 0)).simplify(0.001)] + [None] * (len(fs) - 1)
    if not flush:
        g0 = unary_union([f.buffer(-seam / 2, join_style=2, mitre_limit=4) for f in fs if not f.is_empty])
        k = 0.3 * seam                                   # (hairlines left where two buffers meet, closed; round 28c: and
        g = g0.buffer(-k, join_style=2, mitre_limit=4).buffer(k, join_style=2, mitre_limit=4).intersection(g0)
        # kept inside the pieces, as the mitred corners overshot them by up to 0.013 of the radius in the spin, into a
        # seam or past the ring)
        if keep:
            g = unary_union([q for q in getattr(g, 'geoms', [g]) if not q.buffer(-keep / 2 * seam).is_empty])
            s_ = (sil.bounds[2] - sil.bounds[0]) / (g.bounds[2] - g.bounds[0])
        else:                                            # (and scaled back by the seam itself: measured, a tip narrowing
            g = unary_union([g] + [q for q in getattr(g0, 'geoms', [g0]) if not q.intersects(g)])
            s_ = 1 / (1 - seam / 2)                      # away at the edge would jolt the whole for a frame)
        return [affinity.scale(g, s_, s_, origin=(0, 0)).simplify(0.001)] + [None] * (len(fs) - 1)
    out = []
    for f in fs:
        if f.is_empty:
            out.append(None); continue
        g = f.buffer(lap, join_style=2, mitre_limit=4).intersection(sil, grid_size=GRID).simplify(0.001)
        parts = [q for q in getattr(g, 'geoms', [g]) if q.geom_type == 'Polygon' and q.area > 1e-6]
        out.append(unary_union(parts) if parts else None)
    return out


# Round 27i. The owner, of the set: "Can we also do stroke versions of these in addition to fill, or will that not work?"
# It works, as the same discs drawn in line. In one colour the discs are opaque, so the stroke version is their visible
# edges: every piece the fill keeps outlined once (where two pieces meet, one line), the outline too, `w` of the radius
# wide, round at the joins and ends (edge_lines; scaled so the stroke's outer edge lies where the fill's does). In colour
# the acrylic is see-through, so its stroke version is the six rims themselves, each in its own colour, the far halves
# under the near, every line `w` wide as one colour's are (round 28e, the owner: "Yes the color line version should be
# in one weight"; until then the far halves thinner, round 22's lines, and the near 0.065). Below 64 px the lines knot
# together, so at 64 px they widen to `small` and under it the fill's small cuts stand in.
STROKE = dict(w=0.05, small={64: 0.07})


def edge_lines(spin=0.0, seam=SEAM, keep=KEEP):
    """The discs' visible edges as lines (round 27i): each piece disc_shapes keeps (one colour, seamed), outlined, the
    edges two pieces share drawn once. Round 28c, in the spin (keep 0): every piece, each disc its face alone (no slab),
    so a disc side on is one line, as heavy as every other (the owner, of round 28's line spin: "I don't like when the
    lines in the line version of the spinning globe changes weights needlessly"); and the parallels cut to the outer
    ring, as the fill's are."""
    fs = _cut(facets(spin, THICK + seam if keep else 0.0))   # (round 28c: the parallels cut to the ring, as the fill)
    lines = union_all([q.boundary for q in (_kept(fs, seam, keep) if keep else _parts(fs))], grid_size=GRID)
    return linemerge(lines) if lines.geom_type == 'MultiLineString' else lines


def strokes_body(colour, spin=0.0, w=STROKE['w'], keep=KEEP):
    """One colour's stroke version (round 27i): edge_lines as one stroked path."""
    k = 1 / (1 + w / 2)
    lines = affinity.scale(edge_lines(spin, keep=keep), k, k, origin=(0, 0))
    d = ' '.join(_d(np.array(q.coords)) for q in getattr(lines, 'geoms', [lines]) if q.length > 0)
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w * k:.4f}" stroke-linejoin="round" '
            f'stroke-linecap="round"/>')


def discs_body(colours, spin=0.0, flush=True, seam=SEAM, keep=KEEP, cut=None):
    """The discs as SVG paths, flush in colour, seamed in one colour (disc_shapes); the discs alone (round 25: no ball
    filled under them)."""
    return ''.join(f'<path d="{_poly_d(g)}" fill="{colours[i]}" fill-rule="evenodd"/>'
                          for i, g in enumerate(disc_shapes(spin, flush, seam=seam, keep=keep, cut=cut)) if g is not None)


def _lighter(c, k):
    """A colour k of the way to white (k < 0: toward black)."""
    c = c.lstrip('#')
    return '#%02X%02X%02X' % tuple(round(v + (255 - v) * k if k >= 0 else v * (1 + k)) for v in (int(c[i:i + 2], 16) for i in (0, 2, 4)))


def _rgb(c):
    c = c.lstrip('#')
    return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], float)


def _hex(v):
    return '#%02X%02X%02X' % tuple(int(round(min(255.0, max(0.0, x)))) for x in v)


def _oklab(c):
    """A colour (hex) in OKLab (Bjorn Ottosson's)."""
    v = _rgb(c) / 255
    v = np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)
    l, m, s_ = (np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566],
                          [0.0883024619, 0.2817188376, 0.6299787005]]) @ v) ** (1 / 3)
    return np.array([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s_, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s_,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s_])


def _from_oklab(lab):
    L, a, b = lab
    l, m, s_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, \
        (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    v = np.array([4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s_, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s_,
                  -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s_])
    v = np.clip(v, 0, 1)
    return _hex(255 * np.where(v <= 0.0031308, 12.92 * v, 1.055 * v ** (1 / 2.4) - 0.055))


def _mix(colours, weights):
    """Colours mixed by weight in OKLCh: lightness and chroma weighted, the hue a circular mean weighted by chroma
    (round 25: mixing in sRGB turns crossings grey and brown); as OKLab."""
    labs = [_oklab(c) for c in colours]
    L = sum(w * q[0] for w, q in zip(weights, labs))
    C = sum(w * math.hypot(q[1], q[2]) for w, q in zip(weights, labs))
    ha = sum(w * q[1] for w, q in zip(weights, labs))             # (a, b) weighted is the chroma-weighted hue vector
    hb = sum(w * q[2] for w, q in zip(weights, labs))
    h = math.atan2(hb, ha)
    return np.array([L, C * math.cos(h), C * math.sin(h)])


def _stack(colours, weights, A, steps=None):
    """Round 25 (the acrylic critic's third round): tinted sheets stacked, as OKLab: a and b the share-weighted mean,
    so opposed tints cancel toward grey; the lightness the darkest sheet's, a step (`dark`) lower for each sheet
    beyond the first and lower still (`smoke`) the less the sheets' hues agree (R, the mean's chroma over the mean
    chroma: 1 for one hue, near 0 for opposites). So a crossing is darker than every sheet in it, as stacked acrylic
    is. One sheet is its own colour. `steps`: how many steps deeper (default one for each sheet beyond the first)."""
    labs = [_oklab(c) for c in colours]
    if len(labs) == 1:
        return labs[0]
    a = sum(w * q[1] for w, q in zip(weights, labs))
    b = sum(w * q[2] for w, q in zip(weights, labs))
    C = sum(w * math.hypot(q[1], q[2]) for w, q in zip(weights, labs))
    R = math.hypot(a, b) / C if C > 1e-9 else 1.0
    n = len(labs) - 1 if steps is None else steps
    return np.array([min(q[0] for q in labs) - A['dark'] * n - A['smoke'] * (1 - R), a, b])


def _depth(g, x, y):
    """The depth (z, toward us) of ring g's plane at (x, y) on the picture."""
    n = g['n']
    return (g['d'] - n[0] * x - n[1] * y) / n[2]


def _side(c, A):
    """A disc's side, as a polished acrylic edge looks: its tint deeper (OKLab lightness lower by `side`, chroma raised
    by `sideC`), as hex."""
    L, a, b = _oklab(c)
    k = 1 + A['sideC']
    return _from_oklab(np.array([L - A['side'], a * k, b * k]))


def slabs(spin=0.0, h=0.025, n=360):
    """Round 25 (the owner: "For acrylic I was expecting each disc to have a little thickness to it"): each ring's disc
    as a slab 2h thick. Round 27b: its face toward us is the disc itself, so its outline and its crossings are the
    discs' own, and its thickness runs back from it, away from us. m its normal turned toward us; `front` the oval of
    its face; `swept` the slab's whole outline on the picture (the hull of its two faces' ovals: an oval swept along a
    line is convex), whose part outside `front` is the side we see; its depth z = al x + be y + g on the face (gf) and
    halfway back (gm, for the side). Round 27k: nearing edge on, a slab shows its thickness (_slab): its face moved
    toward us, its rim (`rim`) on the near side, on the globe's surface, so nearest there; `front` the two together,
    `oval` the face alone; exactly edge on (`edge`), its rim alone."""
    out = []
    for g0 in rings(spin, n):
        g, rim = _slab(g0, 2 * h)
        m = g['n'] * (1.0 if g['n'][2] >= 0 else -1.0)
        oval = Polygon(g['pts'][:, :2]).buffer(0)
        front = unary_union([oval, rim]) if not rim.is_empty else oval
        if abs(m[2]) < 1e-6:
            out.append(None if front.is_empty else dict(front=front, oval=oval, swept=front, rim=front, al=0.0,
                                                         be=0.0, gf=0.0, gm=0.0, back_off=[0.0, 0.0], edge=True))
            continue
        P, off = g['pts'][:, :2], 2 * h * m[:2]
        back = Polygon(P - off).buffer(0)
        K = float(np.dot(m, g['c']))
        out.append(dict(front=front, oval=oval, swept=unary_union([oval, back]).convex_hull, rim=rim, al=-m[0] / m[2],
                        be=-m[1] / m[2], gf=K / m[2], gm=(K - h) / m[2], back_off=(-off).tolist(), edge=False))
    return out


def acrylic_cells(colours, A, spin=0.0):
    """Round 27d (the owner: "clipping on the multicolor one wherever there is overlap"): the slabs' sides stood
    outside the discs and were sorted on their own planes, so wherever two discs crossed they were cut into wedges and
    slivers along lines that were not the discs'. Now the cells are the discs' faces alone, cut by their outlines, by
    the lines where two faces are at one depth (the discs' own crossings) and by each face's crescent (crescents): its
    thickness, seen just inside its edge where a slab's side would show, a deeper tone of its tint, so it ends on the
    discs' own lines like everything else. Each cell with the sheets crossed there, nearest first: (colour, whether it
    is the green's face)."""
    h, S = A['thick'] / 2, []
    for q in slabs(spin, h):
        if q is None:
            S.append(None); continue
        off = -np.asarray(q['back_off'])                 # the crescent on the side where the slab's side shows
        S.append(dict(q, cres=q['oval'].difference(affinity.translate(q['oval'], off[0], off[1]))))
    lines = []
    for q in S:
        if q is not None:
            lines += [LineString(np.asarray(q['front'].exterior.coords)), q['cres'].boundary, q['rim'].boundary]
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            si, sj = S[i], S[j]
            if si is None or sj is None or si['edge'] or sj['edge']:
                continue
            both = si['front'].intersection(sj['front'])
            A_, B_ = si['al'] - sj['al'], si['be'] - sj['be']
            m = math.hypot(A_, B_)
            if both.is_empty or m < 1e-12:
                continue
            u = np.array([A_ / m, B_ / m]); t = np.array([-u[1], u[0]])
            p0 = -(si['gf'] - sj['gf']) / m * u
            seg = LineString([p0 - 3 * t, p0 + 3 * t]).intersection(both.buffer(1e-3))
            if not seg.is_empty:
                lines.append(seg)
    out = []
    for c in polygonize(unary_union(lines)):
        if c.area < 1e-7:
            continue
        q, hit = c.representative_point(), []
        for k, sl in enumerate(S):
            if sl is None or not sl['front'].contains(q):
                continue
            if sl['rim'].contains(q):                    # (round 27k: a rim, on the globe's surface: nearest, its side)
                hit.append((math.inf, _side(colours[k], A), False))
                continue
            col = _side(colours[k], A) if sl['cres'].contains(q) else colours[k]
            hit.append((sl['al'] * q.x + sl['be'] * q.y + sl['gf'], col, k == ATMOS))
        if hit:
            out.append((c, [(col, green) for _, col, green in sorted(hit, key=lambda t: -t[0])]))
    return out


def acrylic_cells25(colours, A, spin=0.0):
    """(Round 25 to 27c, replaced in round 27d.) The discs' slabs cut into cells in each of which the same faces and
    sides are crossed in the same order: cut by every slab's front face and outline and, where two slabs both lie, by
    the lines along which they are at one depth (face or side against face or side)."""
    S = slabs(spin, A['thick'] / 2)
    lines = []
    for q in S:
        if q is not None:
            lines += [LineString(np.asarray(q['front'].exterior.coords)), LineString(np.asarray(q['swept'].exterior.coords))]
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            si, sj = S[i], S[j]
            if si is None or sj is None:
                continue
            both = si['swept'].intersection(sj['swept'])
            A_, B_ = si['al'] - sj['al'], si['be'] - sj['be']
            m = math.hypot(A_, B_)
            if both.is_empty or m < 1e-12:
                continue
            u = np.array([A_ / m, B_ / m]); t = np.array([-u[1], u[0]])
            for gi in (si['gf'], si['gm']):
                for gj in (sj['gf'], sj['gm']):
                    p0 = -(gi - gj) / m * u
                    seg = LineString([p0 - 3 * t, p0 + 3 * t]).intersection(both.buffer(1e-3))
                    if not seg.is_empty:
                        lines.append(seg)
    out = []
    for c in polygonize(unary_union(lines)):
        if c.area < 1e-7:
            continue
        q, hit = c.representative_point(), []
        for k, sl in enumerate(S):
            if sl is None:
                continue
            if sl['front'].contains(q):
                hit.append((sl['al'] * q.x + sl['be'] * q.y + sl['gf'], colours[k], k == ATMOS))
            elif sl['swept'].contains(q):
                hit.append((sl['al'] * q.x + sl['be'] * q.y + sl['gm'], _side(colours[k], A), False))
        if hit:
            out.append((c, [(col, green) for _, col, green in sorted(hit, key=lambda t: -t[0])]))
    return out


def _acrylic(sheets, A):
    """Round 27b: what shows through the sheets crossed at a point, nearest first, each (colour, whether it is the
    green's face): the nearest leads (`lead`), those behind share the rest nearest first (each `ghost` of what is left,
    the last all of it), mixed in OKLCh (_mix); a step deeper (`deep`) for each sheet behind, at most three. So the
    pieces and corners are the discs' own, and the discs behind show through. As OKLab; None where there is no sheet."""
    if not sheets:
        return None
    cols = [c for c, _ in sheets]
    if len(cols) == 1:
        return _oklab(cols[0])
    w, keep, rest = [A['lead']], 1 - A['lead'], len(cols) - 1
    for i in range(rest):
        w.append(keep if i == rest - 1 else keep * A['ghost'])
        keep *= 1 - A['ghost']
    lab = _mix(cols, w)
    lab[0] -= A['deep'] * min(rest, 3)
    return lab


def _acrylic25(sheets, A):
    """Round 25 (the acrylic critic's second and third rounds; replaced in round 27b): what shows through the sheets crossed at a point,
    nearest first, each (colour, whether it is the green's face): the green's face the backing; the sheets in front of
    it sharing all of what shows (the nearest `face`, the next `face` of the rest, the farthest what is left); where none
    is, the green with the sheets behind it faint; where the green is not, the sheets alone. Stacked as tinted sheets
    (_stack: every crossing deeper than its darkest sheet), as OKLab; None where there is no sheet (round 25: no ball)."""
    if not sheets:
        return None
    a = A['face']
    gi = next((i for i, (_, green) in enumerate(sheets) if green), len(sheets))
    front, back = [c for c, _ in sheets[:gi]], [c for c, _ in sheets[gi + 1:]]

    def shares(n, total=1.0):                                         # the nearest a, the next a of the rest, ...; the last what is left
        w, keep = [], total
        for i in range(n):
            w.append(keep if i == n - 1 else keep * a)
            keep *= 1 - a
        return w
    if front:
        return _stack(front, shares(len(front)), A)
    green = sheets[gi][0]
    if not back:
        return _oklab(green)
    # behind the green the back halves count as one sheet, a step deeper at most (two crossed back halves, two steps,
    # came out darker than the crossings in front, against the critic's ghosts 'quieter than the crossings')
    return _stack([green] + back, [A['green']] + shares(len(back), 1 - A['green']), A, steps=1)


def _through(order, colours, a, under):
    """What shows through faces laid front to back (`order`), the nearest keeping `a` of what shows, the next `a` of the
    rest, and so on, `under` (a hex colour) taking what is left; mixed in OKLCh (_mix), as OKLab."""
    w, keep = [], 1.0
    for _ in order:
        w.append(keep * a)
        keep *= 1 - a
    return _mix([colours[k] for k in order] + [under], w + [keep])


def acrylic_body(colours, ground='paper', spin=0.0, n=720):
    """Round 25: the discs as tinted acrylic (ACRYLIC): their mosaic see-through, each cell's colour by the acrylic's rule
    (_acrylic: the green the backing, the coloured discs in front of it sharing what shows, the back halves faint behind
    it), each disc a slab with its side showing (slabs; the globe the discs alone, round 25); cells whose colours are
    within a hair of each other (OKLab 0.012) given one
    colour and merged, so no seam shows inside an even area (the brand critic saw hairlines). With `edge` above 0, each
    disc's edge in its colour: the far halves, each seen through the faces in front of it, then the near halves, whole."""
    A = ACRYLIC['night' if ground == 'night' else 'paper']
    a, w = A['face'], A['edge']
    cells = [(c, lab) for c, sheets in acrylic_cells(colours, A, spin) for lab in [_acrylic(sheets, A)] if lab is not None]
    sil = unary_union([c for c, _ in cells])
    clusters = []                                        # [weighted lab sum, area, cells]
    for c, lab in sorted(cells, key=lambda t: -t[0].area):
        for k in clusters:
            if np.linalg.norm(k[0] / k[1] - lab) < 0.012:
                k[0] += lab * c.area; k[1] += c.area; k[2].append(c); break
        else:
            clusters.append([lab * c.area, c.area, [c]])
    faces = sorted(((unary_union([c.buffer(0.0015, join_style=2) for c in k[2]]).intersection(sil, grid_size=GRID),
                     _from_oklab(k[0] / k[1])) for k in clusters), key=lambda t: -t[0].area)   # the laps: small cells over large
    body = ''.join(f'<path d="{_poly_d(g.simplify(0.0008))}" fill="{col}" fill-rule="evenodd"/>' for g, col in faces)
    if w <= 0:
        return body
    rs, far, near = rings(spin, n), [], []
    for i, g in enumerate(rs):
        pts, runs, cur, key = g['pts'], [], [], None
        for k in range(n):
            p, q = pts[k], pts[(k + 1) % n]
            m = (p + q) / 2
            if m[2] > 0:
                kk = (colours[i], True)
            else:                                        # the far half: through every face crossing in front of it
                hit = sorted(((zj, j) for j, gj in enumerate(rs) if j != i and abs(gj['n'][2]) > 1e-6
                              for zj in [_depth(gj, m[0], m[1])]
                              if zj > m[2] + 1e-6 and np.linalg.norm(np.array([m[0], m[1], zj]) - gj['c']) <= gj['r'] + 1e-9),
                             reverse=True)
                kk = (_from_oklab(_through([j for _, j in hit], colours, a, colours[i])), False)   # (edges: off; kept as before)
            if kk != key:
                if cur:
                    runs.append((key, cur))
                cur, key = [p], kk
            cur.append(q)
        runs.append((key, cur))
        for (col, front), r in runs:
            (near if front else far).append(f'<path d="{_d(np.array(r))}" stroke="{col}"/>')
    g = f'<g fill="none" stroke-width="{w:.4f}" stroke-linecap="butt" stroke-linejoin="round">'
    return body + g + ''.join(far) + '</g>' + g + ''.join(near) + '</g>'


# Round 27. The owner: "Let's go with the acrylic globe and have a color version, a black version, and a white version,
# and a version for each speaker". Until now the acrylic in one colour was the lines, which the brand critic found a
# different object from the ball in all three of its rounds. Now it keeps the ball, two ways:
# - In a speaker's own tint, the discs are stacked sheets of that speaker's acrylic held up to the light. Every disc a
#   line of sight crosses (its face, or its side) is one sheet passing T = c ** (1 / at) of the light (c the tint, in
#   linear light), so `at` sheets make the speaker's own colour, fewer lighter, more deeper. Where a disc's side is
#   nearest, its polished edge counts one sheet more. As in colour, the ground takes nothing inside the ball, so a tint
#   reads the same on paper and on ink; but Smoke shows only on paper and Fog only on ink. `at` is two, or more for a
#   dark tint, so that four sheets (the ball's broad middle, a third of it) are no darker than OKLab lightness `mid`, or
#   than the tint itself where it is darker (Smoke): at two, Poison's, Haze's and Smoke's middles went near black. So
#   Poison is taken at 2.6, Haze at 3, Smoke at 4. Fog's tint is nearly clear, so it is taken at half a sheet, deep
#   enough to show its stacks on ink.
# - In black or white, the inks, flat for print, an etch or an emboss, the discs cancel where they cross, as two films
#   do in one ink: a point is inked where an odd number of discs cover it, so every crossing shows with no tints.
#   (Tried: every disc's outline cut as a seam through a solid ball, which read as any globe icon.)
# After the brand critic's round (critic/rounds/2026-10-16/brand-mark-r1.json; "The XOR cut is the real find"): below
# 64 px the one-ink mark broke into a spiky open ring, its thinnest bands under a pixel, so it has small cuts (SMALL):
# every inked part grown by a spread (of the radius) for the largest size it is drawn at, then scaled back to the
# master's width, which closes the slivers and the rim and keeps the middle oval open. Fog's sheets go to 0.3 (at 0.5
# its middle and its rim were 0.12 apart, the least of the tints, and it read as a blank pale disc).
TINT = dict(at=2.0, mid=0.40, Fog=0.3)
INKS = (INK, WHITE)
SMALL = {16: 0.035, 32: 0.025, 64: 0.02}                  # px across at most: the spread (of the radius)
# Then the owner: "I like discs for monochrome and acrylic for multicolor". So the mark is the acrylic in colour and the
# seamed discs (round 24b's one-colour discs) in black, in white and in each speaker's own colour; the parity cut and
# the tints above stay here as the acrylic's own one-colour forms. The discs' small cuts widen the seams so they stay a
# pixel or more: at the master's 0.035 they go grey at 32 px. At 16 px six discs do not read whatever the seam.
SMALL_SEAM = {16: 0.06, 32: 0.06, 64: 0.05}                 # px across at most: the seam, of the radius (round 27k:
                                                            # the full drawing's pieces at each, so no wider than its
                                                            # thinnest piece holds; round 27: 0.10, 0.08, 0.05, dropping;
                                                            # round 27l: bar the two by the butt, which no seam that
                                                            # still shows at these sizes holds)


def _lin(c):
    v = _rgb(c) / 255
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def _from_lin(v):
    v = np.clip(v, 0, 1)
    return _hex(255 * np.where(v <= 0.0031308, 12.92 * v, 1.055 * v ** (1 / 2.4) - 0.055))


def tint_at(colour):
    """How many of a tint's sheets make its own colour (TINT): two, or more for a dark tint, so four sheets stay no darker
    than OKLab lightness `mid` (or the tint's own); Fog's, half."""
    if colour == _C['Fog']:
        return TINT['Fog']
    c, floor, at = _lin(colour), min(TINT['mid'], _oklab(colour)[0]), TINT['at']
    while _oklab(_from_lin(c ** (4 / at)))[0] < floor - 1e-3 and at < 12:
        at += 0.05
    return round(at, 2)


def acrylic_tint_body(colour, spin=0.0):
    """Round 27: the acrylic in one speaker's tint (TINT): each cell's colour T ** n, n the sheets crossed there (a side
    nearest, one more), cells of one colour merged."""
    T = _lin(colour) ** (1 / tint_at(colour))
    A = ACRYLIC['paper']
    tones = {}
    for c, sheets in acrylic_cells([colour] * 6, A, spin):
        n = len(sheets) + (1 if sheets[0][0] != colour else 0)          # a side shows _side's colour, not the tint
        tones.setdefault(n, []).append(c)
    sil = unary_union([c for cs in tones.values() for c in cs])
    faces = sorted(((unary_union([c.buffer(0.0015, join_style=2) for c in cs]).intersection(sil, grid_size=GRID), _from_lin(T ** n))
                    for n, cs in tones.items()), key=lambda t: -t[0].area)
    return ''.join(f'<path d="{_poly_d(g.simplify(0.0008))}" fill="{col}" fill-rule="evenodd"/>' for g, col in faces)


def acrylic_ink_body(colour, spin=0.0, n=720, px=None):
    """Round 27: the acrylic in one ink: inked where an odd number of discs cover the point (the discs as flat ovals).
    `px`: the largest size it is drawn at; at 64 px or less, the small cut for it (SMALL), scaled back to full width."""
    x = None
    for g in rings(spin, n):
        d = Polygon(g['pts'][:, :2]).buffer(0)
        x = d if x is None else x.symmetric_difference(d)
    x = unary_union([p for p in getattr(x, 'geoms', [x]) if p.area > 1e-5])
    spread = next((SMALL[k] for k in sorted(SMALL) if px and px <= k), 0.0)
    if spread:
        w0 = x.bounds[2] - x.bounds[0]
        x = x.buffer(spread, join_style=1)
        k = w0 / (x.bounds[2] - x.bounds[0])
        x = affinity.scale(x, k, k, origin=(0, 0))
    return f'<path d="{_poly_d(x.simplify(0.0004))}" fill="{colour}" fill-rule="evenodd"/>'


def mark_svg(style, colours, size=None, bg=None, label='EARF', ground='paper', px=None):
    """style: lines (the far halves lighter: the mark), even (every line one weight), discs (round 24b: flush in colour,
    seamed in one colour), acrylic (round 24b: every disc tinted, crossing to the colours between), strokes (round 27i:
    the discs in line) or tubes (round 23);
    on `ground`, paper or night; colours: six (a ring each) or one."""
    one = isinstance(colours, str)
    if one:
        colours = [colours] * 6
    line = colours[0] if one else (WHITE if ground == 'night' else INK)
    if style == 'tubes':
        body, e = tubes_body(colours, ground), 1 + W_TUBE / 2 + 0.02
    elif style == 'acrylic' and not one:
        body, e = acrylic_body(colours, ground), 1 + W_LINE / 2
    elif style == 'acrylic' and colours[0] in INKS:      # round 27: black or white, the discs cancelling where they cross
        body, e = acrylic_ink_body(colours[0], px=px), 1 + W_LINE / 2
    elif style == 'acrylic':                             # round 27: a speaker's own tint, stacked (round 25: the lines)
        body, e = acrylic_tint_body(colours[0]), 1 + W_LINE / 2
    elif style == 'discs':                               # (round 27k: a small cut, the full drawing seamed wider)
        cut = next((SMALL_SEAM[k] for k in sorted(SMALL_SEAM) if one and px and px <= k), None)
        body, e = discs_body(colours, flush=not one, cut=cut), 1 + W_LINE / 2
    elif style == 'strokes' and one:                     # round 27i: the discs' visible edges in line
        w = next((STROKE['small'][k] for k in sorted(STROKE['small']) if px and px <= k), STROKE['w'])
        body, e = strokes_body(colours[0], w=w), 1 + W_LINE / 2
    elif style == 'strokes':                             # round 27i: the acrylic's rims, see-through, in their colours
        k = 1 / (1 + STROKE['w'] / 2)                    # (round 28e: one weight, as one colour's lines)
        body, e = f'<g transform="scale({k:.5f})">{lines_body(colours, w=STROKE["w"])}</g>', 1 + W_LINE / 2
    else:
        body, e = lines_body(colours, depth=style == 'lines'), 1 + W_LINE / 2
    wh = f' width="{size}" height="{size}"' if size else ''
    ground = f'<rect x="{-e:.4f}" y="{-e:.4f}" width="{2 * e:.4f}" height="{2 * e:.4f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.4f} {-e:.4f} {2 * e:.4f} {2 * e:.4f}"{wh} role="img" '
            f'aria-label="{label}"><title>{label}</title>{ground}{body}</svg>')


def _prim_shape(p):
    if p[0] == 'circle':
        return Point(p[1], p[2]).buffer(p[3], resolution=96)
    if p[0] == 'ring':                                   # round 29: the R's bowl, its hole 70 in
        return Point(p[1], p[2]).buffer(p[3], resolution=96).difference(Point(p[1], p[2]).buffer(p[4], resolution=96))
    if p[0] == 'rect':
        return Polygon([(p[1], p[2]), (p[3], p[2]), (p[3], p[4]), (p[1], p[4])])
    return Polygon(p[1:])


def letters():
    """EARF's four letters, each its primitives merged into one solid shape (y down, cap height 300), so the wordmark
    prints in one colour; the R's bowl a ring (round 29), so a hole 70 in shows right of the stem."""
    groups = [M.WORDMARK[0:4], M.WORDMARK[4:7], M.WORDMARK[7:10], M.WORDMARK[10:13]]
    out = []
    for g in groups:
        u = unary_union([_prim_shape(p) for p in g])
        out.append(' '.join('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in np.array(r.coords)) + 'Z'
                            for poly in getattr(u, 'geoms', [u]) for r in [poly.exterior] + list(poly.interiors)))
    return out


def word_svg(word, label='EARF', size=None):
    """EARF alone, its letters solid in one colour, its view box the letters' own (WORDMARK_W by 300), `size` the height in
    px (round 29: the wordmark in one colour, as the globe is in discs; in colour it is acrylic, word_real.py)."""
    wh = f' width="{size * M.WORDMARK_W / 300:.0f}" height="{size}"' if size else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {M.WORDMARK_W} 300"{wh} role="img" aria-label="{label}">'
            f'<title>{label}</title><g fill="{word}">' + ''.join(f'<path d="{d}"/>' for d in letters()) + '</g></svg>')


def lockup_svg(style, colours, word, size=None, bg=None, ground='paper', px=None):
    """The globe beside EARF, its diameter one and a half cap heights, centred on the letters (`px`: the globe's largest
    size, for the one-ink small cuts)."""
    k = 225 / ((1 + W_TUBE / 2 + 0.02) if style == 'tubes' else (1 + W_LINE / 2))
    inner = mark_svg(style, colours, ground=ground, px=px)
    inner = inner[inner.index('</title>') + 8:inner.rindex('</svg>')]
    vw, vh, gap = 450 + 110 + M.WORDMARK_W, 450, 110
    wh = f' width="{size * vw / vh:.0f}" height="{size}"' if size else ''
    ground = f'<rect x="-40" y="-40" width="{vw + 80}" height="{vh + 80}" fill="{bg}"/>' if bg else ''
    vb = '-40 -40 {} {}'.format(vw + 80, vh + 80) if bg else f'0 0 {vw} {vh}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh} role="img" aria-label="EARF"><title>EARF</title>'
            f'{ground}<g transform="translate(225 225) scale({k:.4f})">{inner}</g>'
            f'<g transform="translate({450 + gap} 75)" fill="{word}">'
            + ''.join(f'<path d="{d}"/>' for d in letters()) + '</g></svg>')


def _core_paths():
    import core as K
    return K.core_paths()


def outlines(tol=0.0015):
    """Round 24 (24b): the globe's shapes for a maker (product.py's mark in the front corner), each a list of [ring,
    exterior, holes] on the unit globe, y up: the discs seamed, for one colour (an etch, a tint); the discs flush, for
    colour (a print); and the lines, each ring at one weight (the even style); with the rings' colours (round 25), so a
    print takes them from here."""
    def parts(g, k):                                     # on a 1e-4 grid, each polygon kept valid (a CAD face needs it)
        g = make_valid(set_precision(g, 1e-4))
        return [[k, np.array(q.exterior.coords)[:-1].tolist(), [np.array(h.coords)[:-1].tolist() for h in q.interiors]]
                for q in getattr(g, 'geoms', [g]) if q.geom_type == 'Polygon' and q.area > 1e-6]
    seamed = [q for i, g in enumerate(disc_shapes(flush=False)) if g is not None for q in parts(g.simplify(tol), i)]
    flush = [q for i, g in enumerate(disc_shapes(flush=True, lap=0.0)) if g is not None for q in parts(g.simplify(tol), i)]
    lines = []
    for i, g in enumerate(rings()):
        loop = np.vstack([g['pts'], g['pts'][:1]])[:, :2]
        lines += parts(LineString(loop).buffer(W_LINE / 2, join_style=1).simplify(tol), i)
    return dict(discs=seamed, flush=flush, lines=lines, base=[], ring=RING, atmos=ATMOS)   # base: round 25, no ball filled


def data():
    return dict(lean=LEAN, elev=ELEV, lat=LAT, mer=list(MERIDIANS), w=W_LINE, wDepth=W_DEPTH, seam=SEAM, hues=HUES, wTube=W_TUBE, tube=TUBE,
                ring=RING, atmos=ATMOS, rim=_lighter(RING[ATMOS], -0.4), acrylic=ACRYLIC, core=_core_paths(),
                names=NAMES, paper=PAPER, ink=INK, night=NIGHT, white=WHITE, letters=letters(), wordW=M.WORDMARK_W)


RAILS = [('Black only', 'paper', lambda: INK), ('White only', 'night', lambda: WHITE),
         ('One colour', 'paper', lambda: _C['Ice']), ('Multicolour', 'paper', lambda: RING),
         ('Multicolour on ink', 'night', lambda: RING)]


def rails_html():
    """The guide rails: each style in black only, white only, one colour and multicolour, and the singles."""
    rows = ''
    for style, title in (('discs', 'Discs'), ('acrylic', 'Acrylic'), ('even', 'Lines')):
        cells = ''.join(f'<figure class="rail {g}">{mark_svg(style, f(), label=f"{title}, {t.lower()}", ground=g)}'
                        f'<figcaption>{t}</figcaption></figure>' for t, g, f in RAILS)
        singles = ''.join(f'<span class="one" title="{n}">{mark_svg(style, _C[n], label=f"{title} in {n}")}</span>'
                          for n in RING_NAMES)
        rows += (f'<div class="railrow"><h3>{title}</h3><div class="rails">{cells}</div>'
                 f'<div class="singles"><span class="lab">Each speaker in its own colour</span>{singles}</div></div>')
    locks = (f'<figure class="lock paper">{lockup_svg("discs", RING, INK)}<figcaption>Discs on paper</figcaption></figure>'
             f'<figure class="lock night">{lockup_svg("discs", RING, WHITE, ground="night")}<figcaption>Discs on ink</figcaption></figure>'
             f'<figure class="lock paper">{lockup_svg("acrylic", RING, INK)}<figcaption>Acrylic on paper</figcaption></figure>'
             f'<figure class="lock paper">{lockup_svg("even", RING, INK)}<figcaption>Lines on paper</figcaption></figure>'
             f'<figure class="lock paper">{lockup_svg("discs", INK, INK)}<figcaption>Black only</figcaption></figure>'
             f'<figure class="lock night">{lockup_svg("discs", WHITE, WHITE, ground="night")}<figcaption>White only</figcaption></figure>')
    return rows + f'<div class="locks">{locks}</div>'


# the line's name, three ways (the owner: "Atmosphere is cool, but open to other earth themes. Elements was another
# idea I had"), and a fourth: the same colours as chemical elements, numbered by their atomic numbers
THEMES = [
    ('Clouds', 'Until now', 'Cloud 05 &middot; Ice', 'Things in the sky. The cloud mark stays the line&rsquo;s sign, with the '
     'eight icons under it.', None),
    ('Atmosphere', 'Chosen (round 24)', 'Atmosphere 05 &middot; Ice', 'The same eight names, as what the air holds: light (Flare, Haze), '
     'what it carries (Dust, Fog, Smoke, Poison) and what falls through it (Acid, Ice). The globe already draws one.', None),
    ('Elements', 'Sharper', 'Element 05 &middot; Ice', 'The same eight, read as the elements and their dangers: fire, earth, '
     'water and air, acid and poison. The icons work as hazard signs, which is where the crossbones and the drop come '
     'from.', None),
    ('Elements, literally', 'Furthest', 'Element 27 &middot; Cobalt', 'Each speaker named for a chemical element of its '
     'colour, and numbered by its atomic number. The icons fit half (Sulfur&rsquo;s drop, Chlorine&rsquo;s crossbones, '
     'Iodine&rsquo;s haze, Carbon&rsquo;s smoke); the rest would be redrawn.',
     [('Neon', 10), ('Sodium', 11), ('Sulfur', 16), ('Chlorine', 17), ('Cobalt', 27), ('Iodine', 53), ('Magnesium', 12),
      ('Carbon', 6)]),
]
ON_INK = {'Smoke': '#8A888E'}                            # Smoke's lines lightened, to be seen on ink at all


def core_html():
    """Round 24b: the globe as a Death Star (core.py); round 25: the Earth on it, and its cuts for each size (full, mid
    for 25 to 48 px, small for 24 px and under), in colour and in one colour, and the violet cap."""
    import core as K
    rows = (('On paper', 'paper', None, False, 'full'), ('Mid, 25&ndash;48 px', 'paper', None, False, 'mid'),
            ('Small, 24 px and under', 'paper', None, False, 'small'), ('On ink', 'night', None, False, 'full'),
            ('With a violet cap', 'paper', None, True, 'full'), ('Black only', 'paper', INK, False, 'full'),
            ('Black, mid', 'paper', INK, False, 'mid'), ('Black, small', 'paper', INK, False, 'small'),
            ('White only', 'night', WHITE, False, 'full'), ('White, small', 'night', WHITE, False, 'small'))
    cells = ''.join(f'<figure class="icon {g}">{K.core_svg(g, one, cap, small=cut == "small", mid=cut == "mid", label="The globe as a Death Star, " + t.lower().replace("&ndash;", " to "))}'
                    f'<figcaption>{t}</figcaption></figure>' for t, g, one, cap, cut in rows)
    return f'<div class="iconrow"><div class="cores">{cells}</div></div>'


def theme_html():
    """The eight icons tinted on paper, as lines on ink and in black only; then the line's name four ways."""
    rows = ''
    for title, ground, draw in (('Tinted, on paper', 'paper', lambda n: IC.icon_svg(n, IC.COLOURS[n])),
                                ('Lines, on ink', 'night', lambda n: IC.icon_svg(n, None, line=ON_INK.get(n, IC.COLOURS[n]))),
                                ('Black only', 'paper', lambda n: IC.icon_svg(n, INK, line=PAPER))):
        cells = ''.join(f'<figure class="icon {ground}">{draw(n)}<figcaption>{n}</figcaption></figure>' for n, _ in IC.ICONS)
        rows += f'<div class="iconrow"><h3>{title}</h3><div class="icons">{cells}</div></div>'
    cards = ''
    for name, tag, box, why, chem in THEMES:
        items = [(n, IC.COLOURS[n], '') for n, _ in IC.ICONS] if chem is None else \
                [(c, IC.COLOURS[n], f' {z}') for (n, _), (c, z) in zip(IC.ICONS, chem)]
        lis = ''.join(f'<li><i style="background:{col}"></i>{n}<span>{z}</span></li>' for n, col, z in items)
        cards += (f'<div class="name"><div class="tag">{tag}</div><h3>{name}</h3><div class="box">{box}</div>'
                  f'<p>{why}</p><ol>{lis}</ol></div>')
    return rows + f'<div class="names">{cards}</div>'


PAGE = r"""<title>EARF Globe</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* a desktop of 2001: platinum grey, white panels with a bevel, Verdana at small sizes; the globe and its software */
:root {
  --page: #DEDCD7; --panel: #F6F5F2; --fg: #1C1A18; --muted: #57534C; --line: #B9B5AD; --hi: #FFFFFF; --lo: #A8A49C;
  --bar: #E9E7E3; --ring: rgba(0,0,0,.3); --font: Verdana, Tahoma, 'DejaVu Sans', Geneva, sans-serif; color-scheme: light;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --page: #121114; --panel: #1B1A1E; --fg: #ECEAE6; --muted: #A6A29B; --line: #3A383F; --hi: #2C2A31; --lo: #08080A;
  --bar: #232127; --ring: rgba(255,255,255,.4); color-scheme: dark } }
:root[data-theme="dark"] { --page: #121114; --panel: #1B1A1E; --fg: #ECEAE6; --muted: #A6A29B; --line: #3A383F;
  --hi: #2C2A31; --lo: #08080A; --bar: #232127; --ring: rgba(255,255,255,.4); color-scheme: dark }
body { margin: 0; background: var(--page); color: var(--fg); font: 14px/1.6 var(--font);
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 28px 56px }
main { max-width: 1080px; margin: 0 auto; display: grid; gap: 26px }
header { display: grid; gap: 8px }
.eyebrow { font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted) }
h1 { margin: 0; font-size: clamp(26px, 4.4vw, 38px); line-height: 1.1; font-weight: 700; letter-spacing: -0.03em; text-wrap: balance }
h2 { margin: 0; font-size: 19px; letter-spacing: -0.02em }
h3 { margin: 0; font-size: 13px; letter-spacing: 0.02em }
p { margin: 0; max-width: 72ch }
.lede { color: var(--muted) }
.win { background: var(--panel); border: 1px solid var(--line); box-shadow: inset 1px 1px 0 var(--hi), inset -1px -1px 0 var(--lo);
  border-radius: 6px; overflow: hidden }
.bar { display: flex; align-items: center; gap: 8px; padding: 6px 10px; background: var(--bar); border-bottom: 1px solid var(--line);
  font-size: 11px; letter-spacing: 0.04em; color: var(--muted) }
.bar i { width: 11px; height: 11px; border-radius: 50%; display: inline-block; box-shadow: inset 0 0 0 1px rgba(0,0,0,.18) }
.bar b { font-weight: 400; margin-left: 4px }
.screen { position: relative; aspect-ratio: 16 / 9; background: #F2EFEA }
.screen canvas, .strip canvas, .pad canvas, .coin canvas { display: block; width: 100%; height: 100% }
.controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding: 10px; border-top: 1px solid var(--line) }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 4px; overflow: hidden; background: var(--panel);
  box-shadow: inset 1px 1px 0 var(--hi) }
.seg button, .btn { font: 12px/1 var(--font); color: var(--fg); background: transparent; border: 0; padding: 9px 12px; cursor: pointer }
.seg button + button { border-left: 1px solid var(--line) }
.seg button[aria-pressed="true"] { background: var(--fg); color: var(--panel) }
.btn { border: 1px solid var(--line); border-radius: 4px; background: var(--panel); box-shadow: inset 1px 1px 0 var(--hi), inset -1px -1px 0 var(--lo) }
button:focus-visible { outline: 2px solid var(--fg); outline-offset: 2px }
.cap { padding: 0 12px 14px; color: var(--muted); font-size: 13px }
.railrow { display: grid; gap: 10px; padding: 14px; border-top: 1px solid var(--line) }
.railrow:first-child { border-top: 0 }
.rails { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px }
.rail, .lock { margin: 0; display: grid; gap: 6px; font-size: 11px; color: var(--muted) }
.rail svg { display: block; width: 100%; height: auto; padding: 14%; box-sizing: border-box; border-radius: 4px }
.paper svg { background: #F2EFEA } .night svg { background: #121114 }
.singles { display: flex; flex-wrap: wrap; gap: 8px; align-items: center }
.singles .lab { font-size: 11px; color: var(--muted); margin-right: 6px }
.one svg { display: block; width: 46px; height: 46px; padding: 6px; background: #F2EFEA; border-radius: 4px }
.locks { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; padding: 14px; border-top: 1px solid var(--line) }
.lock svg { display: block; width: 100%; height: auto; padding: 8% 7%; box-sizing: border-box; border-radius: 4px }
.lead { padding: 14px 14px 0; color: var(--muted); font-size: 13px }
.iconrow { display: grid; gap: 8px; padding: 14px }
.iconrow + .iconrow { padding-top: 0 }
.icons { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 8px }
.cores { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px }
.cores svg { padding: 12% }
.icon { margin: 0; display: grid; gap: 4px; font-size: 11px; color: var(--muted); text-align: center }
.icon svg { display: block; width: 100%; height: auto; padding: 10%; box-sizing: border-box; border-radius: 4px }
.names { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; padding: 14px; border-top: 1px solid var(--line) }
.name { display: grid; gap: 6px; align-content: start; padding: 12px; border: 1px solid var(--line); border-radius: 4px;
  box-shadow: inset 1px 1px 0 var(--hi), inset -1px -1px 0 var(--lo) }
.name .tag { font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
.name .box { font-size: 12px; padding: 4px 8px; border: 1px solid var(--line); border-radius: 3px; justify-self: start }
.name p { font-size: 12px; color: var(--muted) }
.name ol { margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2px 10px; font-size: 12px }
.name li i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 6px; box-shadow: inset 0 0 0 1px var(--ring) }
.name li span { color: var(--muted) }
.kit { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px }
.kit .wide { grid-column: 1 / -1 }
.strip { aspect-ratio: 5 / 1 }
.pad { aspect-ratio: 16 / 10; cursor: none; touch-action: none }
.coin { aspect-ratio: 16 / 10 }
.notes { display: grid; gap: 10px; padding: 16px }
.notes h3 { margin-top: 6px }
.notes ul { margin: 0; padding-left: 18px; max-width: 74ch } .notes li { margin: 3px 0 }
@media (max-width: 720px) { .rails { grid-template-columns: repeat(3, minmax(0, 1fr)) } .kit, .locks { grid-template-columns: 1fr }
  .icons { grid-template-columns: repeat(4, minmax(0, 1fr)) } .names { grid-template-columns: 1fr }
  .cores { grid-template-columns: repeat(2, minmax(0, 1fr)) }
  .seg button, .btn { padding: 10px 10px } }
body.capture { padding: 0; overflow: hidden } body.capture main { display: none }
#cap { display: none } body.capture #cap { display: block; position: fixed; inset: 0; width: 100vw; height: 100vh }
</style>
<main>
  <header>
    <div class="eyebrow">EARF &middot; Round 27 &middot; the globe</div>
    <h1>The acrylic globe is the mark; the idents are parked</h1>
    <p class="lede">Round 27, the owner: &ldquo;Let&rsquo;s go with the acrylic globe and have a color version, a black
      version, and a white version, and a version for each speaker&rdquo;, and then: &ldquo;I like discs for monochrome
      and acrylic for multicolor&rdquo;. So the mark is the acrylic in colour and the seamed discs in black, in white
      and in each speaker&rsquo;s colour; the set is in <code>brand/mark/</code> and on the mark&rsquo;s own page. The
      rails below draw every style in every rail, for reference. The idents and the Planet are
      parked, as the owner chose: their code stays in <code>earth.py</code> and their videos in <code>brand/</code>, but
      this page no longer plays them. What follows is the globe as round 25 and 26 left it.</p>
  </header>

  <!--PARKED-->
  <section class="win" aria-label="The ident">
    <div class="bar"><i style="background:#D2382F"></i><i style="background:#E9B320"></i><i style="background:#4F7F3A"></i><b>earf.world &mdash; ident</b></div>
    <div class="screen" id="screen"><canvas id="stage" aria-label="The EARF globe arriving, then EARF beside it"></canvas></div>
    <div class="controls">
      <div class="seg" id="kind" role="group" aria-label="Ident">
        <button aria-pressed="true" data-v="gyro">Gyroscope</button><button aria-pressed="false" data-v="coin">Coin</button><button aria-pressed="false" data-v="rise">Earthrise</button><button aria-pressed="false" data-v="open">Open</button><button aria-pressed="false" data-v="iris">Iris</button><button aria-pressed="false" data-v="planet">Planet</button><button aria-pressed="false" data-v="roll">Roll</button><button aria-pressed="false" data-v="download">Download</button>
      </div>
      <div class="seg" id="style" role="group" aria-label="Style">
        <button aria-pressed="true" data-v="discs">Discs</button><button aria-pressed="false" data-v="acrylic">Acrylic</button><button aria-pressed="false" data-v="even">Lines</button>
      </div>
      <div class="seg" id="ground" role="group" aria-label="Ground">
        <button aria-pressed="true" data-v="paper">Paper</button><button aria-pressed="false" data-v="night">Ink</button>
      </div>
      <button class="btn" id="replay">Replay</button>
    </div>
    <p class="cap" id="cap-text"></p>
  </section>
  <!--/PARKED-->

  <section class="win" aria-label="Guide rails">
    <div class="bar"><b>Guide rails &mdash; white only, black only, one colour, multicolour</b></div>
    __RAILS__
  </section>

  <section class="win" aria-label="The globe as a Death Star">
    <div class="bar"><b>The globe as a Death Star &mdash; its dish a driver</b></div>
    <p class="lead">The outside is the Earth (round 25): the continents in green on the blue sea, coarse and
      rounded, the Americas facing you, the land kept clear of the dish and no specks. In the North Atlantic a dish that is
      a driver seen from the front: the surround red, the cone orange, the dust cap yellow, as the Earth&rsquo;s core. It is
      21&deg; across, as in round 24b, with a deeper bowl, so its rings sit toward the middle: 24&deg; was tried and pressed
      on every coast. Below 49&nbsp;px a mid cut keeps only the two Americas, and at 24&nbsp;px and under the small cut has
      no land and a 24&deg; dish. In one colour it is knock-outs: the disc solid, the land, the surround and the dust cap
      knocked out to the ground. On each beat the cone pushes out, rebounds and settles, and a ring of sound, knocked out
      of the globe, crosses the Earth (parked in round 27). As an ident, the Planet (round 26, drawn as early Disney would have, parked in round 27):
      a star twinkles, the meteor grows out of it, draws back and falls on an arc, stretching, and splats on the North
      Atlantic; the Earth squashes and springs back, a shock runs over it and the sea ripples; a white cloud pops up puff
      by puff, chars black from the middle out and is eaten away into curling crescents, and the crater springs open, the
      meteor dropping into its core as the violet cap.</p>
    __CORE__
  </section>

  <section class="win" aria-label="Theme">
    <div class="bar"><b>Theme &mdash; Atmosphere, with an icon for each speaker from the marks&rsquo; own circles, bars and triangles</b></div>
    <p class="lead">Each icon is made as the cloud mark is: a few circles, bars and triangles, all filled, then every
      outline drawn over them, like stacked clear acrylic. Poison is two crossing bars with circles at the ends; Acid is
      a circle with a triangle on top.</p>
    __THEME__
  </section>

  <section class="kit" aria-label="The software kit">
    <div class="win wide">
      <div class="bar"><b>Loader &mdash; a white circle uncovers the six; black on paper the same</b></div>
      <div class="strip" style="background:#121114"><canvas id="load-night" aria-label="Loader on ink"></canvas></div>
      <div class="strip" style="background:#F2EFEA"><canvas id="load-paper" aria-label="Loader on paper"></canvas></div>
    </div>
    <div class="win">
      <div class="bar"><b>Cursor &mdash; move over the panel</b></div>
      <div class="pad" id="pad" style="background:#121114"><canvas id="cursor" aria-label="Cursor trail"></canvas></div>
    </div>
    <!--PARKED-->
    <div class="win">
      <div class="bar"><b>The Death Star, kicking &mdash; for the speakers</b></div>
      <div class="coin" style="background:#121114"><canvas id="kickloop" aria-label="The globe as a Death Star, its dish kicking like a speaker"></canvas></div>
    </div>
    <div class="win">
      <div class="bar"><b>The planet, struck &mdash; the meteor stays in its core</b></div>
      <div class="coin" style="background:#F2EFEA"><canvas id="meteor" aria-label="A violet meteor strikes the Earth: a white cloud, black smoke curling away, the sea rippling, then the crater with the meteor in its core"></canvas></div>
    </div>
    <!--/PARKED-->
  </section>

  <section class="win" aria-label="Notes">
    <div class="bar"><b>Notes</b></div>
    <div class="notes">
      <h3>Why it reads as the Earth</h3>
      <ul>
        <li>The axis leans 23.4&deg;, as the Earth's does and as a desk globe's stand holds it. It also tips 16&deg; toward you (22&deg; until round 27f), so the parallels open into ovals and the far halves show behind the near ones.</li>
        <li>The colours (round 25): blue and green lead, as the Earth's sea and land. The meridian facing you, the largest disc, is Poison green; the equator, the widest band, is Ice blue; north Flare red and south Acid yellow; of the side meridians, the one that shows more is Dust orange and the one that shows less Haze violet. Round 24 had violet facing you and the primaries on the parallels.</li>
        <li>Discs in colour are flush (round 24b): no seams, no outline, no light. The globe is its six discs alone (round 25): no fill completes the circle where no disc reaches the rim, so its outline is the discs' own, the green disc's oval with the others' tips reaching past it. The strokes belong to the one-colour versions: there the seams are gaps in the ground, and the outline stays whole.</li>
        <li>Acrylic (round 25) is the discs themselves, see-through, stacked as tinted sheets, each disc a slab a twentieth of the radius thick, its side, where it faces you, a deeper tone of its tint, as a polished acrylic edge looks. The green meridian facing you is the backing, as in the discs. One disc in front shows its own flat colour; where two cross they make one colour darker than either, whichever is in front, as two filters do: red over violet crimson, blue over violet indigo, and the opposite pairs smoky, blue over orange taupe and yellow over violet brown. Where no disc lies in front, the rings' far halves show through the green a little deeper than it, so each ring closes. Where a disc is, the ground takes nothing, so paper and ink match. Stacked in OKLab (a and b averaged, the lightness the darkest sheet's and lower for each sheet more and the less their hues agree); drawn per pixel on the graphics card (without WebGL, the flush discs). No edges (a cage of hoops, the critic found). In one colour (round 27) it keeps the ball: in black or white the discs cancel where they cross, as two films do in one ink, so every crossing shows without a tint; in a speaker's own colour the discs are stacked sheets of that speaker's acrylic held up to the light, lighter at the rim, deeper where more cross.</li>
        <li>Lines are even, every line one weight, the far halves under the near. Round 22's lighter far halves (in <code>brand/earth-lines-*.svg</code>) remain for one colour at small sizes, where even lines tangle.</li>
        <li>Seen from above the pole, the same rings are a speaker: rings round one centre, with the meridians as spokes. Round 23&rsquo;s Kick used that view; round 24b makes the speaker a Death Star&rsquo;s dish instead.</li>
        <li>Round 23's tubes, the printer and the kick, and round 24's lit sphere and cut-open globe, are set aside; the first three stay in <code>earth.py</code> and in round 23's files.</li>
      </ul>
      <h3>The rails</h3>
      <ul>
        <li>The mark (round 27, the owner: "Let's go with the acrylic globe", then "I like discs for monochrome and acrylic for multicolor"): the acrylic in colour; the seamed discs in black, in white and in each speaker's colour, flat, as files in <code>brand/mark/</code>. The acrylic's own one-colour forms (the overlap cut and the tints) and the lines stay below, for reference.</li>
        <li>Black only: paper, print, embossing and a one-colour etch. White only: dark grounds, and the etched mark on the acrylic.</li>
        <li>One colour: each speaker's own mark, for the speaker, its box and its page. Avoid Acid on paper, where yellow is too faint; use it on ink.</li>
        <li>Multicolour: the brand at large. Animated: screens only (the idents, the loader, the cursor).</li>
        <li>Discs, flush, for colour. In one colour, the seamed discs or the even lines; below about 32 px round 22's lighter far halves read better.</li>
        <li>Clear space: a quarter of the globe's width on every side. In the lockup, the globe is one and a half cap heights tall, centred on the letters.</li>
      </ul>
      <h3>The icons</h3>
      <ul>
        <li>Each works in the same rails as the globe: tinted, lines and black only. Fog's tint is nearly white, so on paper its outline carries it.</li>
        <li>Where they could go: beside the mark on the speaker (etched as the mark is), on the end of the box, and as each speaker's tab on the site.</li>
        <li>The names don't have to change to use them. Under Elements the icons read as hazard signs; under Clouds or Atmosphere, as weather.</li>
      </ul>
    </div>
  </section>
</main>
<canvas id="cap"></canvas>
<script>
const D = __DATA__;
const TAU = Math.PI * 2, rad = d => d * Math.PI / 180;
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const smooth = x => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
const cross = (u, v) => [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
const dot = (u, v) => u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
const GROUNDS = { paper: { bg: D.paper, ink: D.ink }, night: { bg: D.night, ink: D.white } };

function basis(lean, elev) {
  const t = rad(lean), e = rad(elev);
  const R = ([x, y, z]) => { const y1 = y * Math.cos(e) - z * Math.sin(e), z1 = y * Math.sin(e) + z * Math.cos(e);
    return [x * Math.cos(t) + y1 * Math.sin(t), -x * Math.sin(t) + y1 * Math.cos(t), z1]; };
  return { a: R([0, 1, 0]), e1: R([0, 0, 1]), e2: R([1, 0, 0]) };
}

// the six rings at a spin (degrees about the axis): points from each one's start (a parallel at its west end,
// sweeping across the near side; a meridian at the north pole, down the near side), each closed, with its plane
function ringsAt(spin, o = {}) {
  const lean = o.lean ?? D.lean, elev = o.elev ?? D.elev, n = o.n ?? 240, grow = o.grow ?? [1, 1, 1];
  const { a, e1, e2 } = basis(lean, elev), out = [];
  [D.lat, 0, -D.lat].forEach((phi, k) => {
    const cp = Math.cos(rad(phi)) * grow[k], sp = Math.sin(rad(phi)), l0 = Math.atan2(e2[0], e1[0]) + Math.PI, pts = [];
    for (let i = 0; i <= n; i++) { const l = l0 + TAU * i / n, c = Math.cos(l), s = Math.sin(l);
      pts.push([0, 1, 2].map(j => cp * (c * e1[j] + s * e2[j]) + sp * a[j])); }
    out.push({ pts, n: a, d: sp, c: a.map(v => v * sp), r: cp });
  });
  D.mer.forEach(m => {
    const l = rad(m + spin), u = [0, 1, 2].map(j => Math.cos(l) * e1[j] + Math.sin(l) * e2[j]);
    const w = u[2] >= 0 ? u : u.map(v => -v), pts = [];
    for (let i = 0; i <= n; i++) { const th = rad(90) - TAU * i / n;
      pts.push([0, 1, 2].map(j => Math.cos(th) * w[j] + Math.sin(th) * a[j])); }
    out.push({ pts, n: cross(u, a), d: 0, c: [0, 0, 0], r: 1 });
  });
  for (const g of out) { g.cum = [0];
    for (let i = 1; i < g.pts.length; i++) g.cum.push(g.cum[i - 1] + Math.hypot(g.pts[i][0] - g.pts[i - 1][0], g.pts[i][1] - g.pts[i - 1][1]));
    g.len = g.cum[g.cum.length - 1]; }
  return out;
}

// a ring drawn up to a share f of its length (on screen), the last point cut to fit
function upto(g, f) {
  if (f >= 1) return g.pts;
  const L = g.len * f; let i = 1;
  while (i < g.cum.length && g.cum[i] < L) i++;
  const s = (L - g.cum[i - 1]) / Math.max(1e-9, g.cum[i] - g.cum[i - 1]), p = g.pts[i - 1], q = g.pts[i];
  return g.pts.slice(0, i).concat([[0, 1, 2].map(j => p[j] + s * (q[j] - p[j]))]);
}

function view(W, H, cx, cy, R) { return { cx, cy, R, X: p => cx + p[0] * R, Y: p => cy - p[1] * R }; }

// one side's runs of a polyline as one path, each run cut exactly at the rim (z = 0)
function sidePath(ctx, V, pts, front) {
  ctx.beginPath(); let pen = false;
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i], inn = (p[2] >= 0) === front;
    if (i > 0) { const q = pts[i - 1], qin = (q[2] >= 0) === front;
      if (qin !== inn) { const s = q[2] / (q[2] - p[2]), c = [q[0] + s * (p[0] - q[0]), q[1] + s * (p[1] - q[1])];
        if (qin) { ctx.lineTo(V.X(c), V.Y(c)); pen = false; } else { ctx.moveTo(V.X(c), V.Y(c)); pen = true; } } }
    if (inn) { if (pen) ctx.lineTo(V.X(p), V.Y(p)); else { ctx.moveTo(V.X(p), V.Y(p)); pen = true; } }
  }
}

// the visible-part test: is a point (x, y, z) behind disc j?
function covers(g, x, y, z) {
  if (Math.abs(g.n[2]) < 1e-4 || g.r <= 0) return false;
  const zj = (g.d - g.n[0] * x - g.n[1] * y) / g.n[2];
  if (zj <= z + 1e-5) return false;
  const dx = x - g.c[0], dy = y - g.c[1], dz = zj - g.c[2];
  return dx * dx + dy * dy + dz * dz <= g.r * g.r;
}
function hidden(gs, skip, x, y, z) { for (const g of gs) if (!skip.includes(g) && covers(g, x, y, z)) return true; return false; }

// a run of 3D points stroked only where no filled disc covers them
function strokeVisible(ctx, V, pts, gs, skip) {
  ctx.beginPath(); let pen = false;
  for (const p of pts) { if (hidden(gs, skip, p[0], p[1], p[2])) { pen = false; continue; }
    if (pen) ctx.lineTo(V.X(p), V.Y(p)); else { ctx.moveTo(V.X(p), V.Y(p)); pen = true; } }
  ctx.stroke();
}

let OFF = null;
function offscreen(w, h) { if (!OFF) OFF = document.createElement('canvas');
  if (OFF.width !== w || OFF.height !== h) { OFF.width = w; OFF.height = h; } return OFF; }

// the discs: each one's oval less every nearer disc's oval (a half-plane apart), then the seams over the edges; round 24b,
// in colour flush (seamW 0): no seams, each part laid a little wider than itself so no hairline of the ground shows
const FLUSH = [[0, 0], [0.6, 0], [-0.6, 0], [0, 0.6], [0, -0.6]];
function drawDiscs(ctx, V, gs, filled, cols, bg, seamW) {
  const on = gs.filter((g, k) => filled[k] && Math.abs(g.n[2]) > 1e-4 && g.r > 1e-3);
  const cv = ctx.canvas, off = offscreen(cv.width, cv.height), o = off.getContext('2d'), T = ctx.getTransform();
  gs.forEach((gi, k) => {
    if (!on.includes(gi)) return;
    o.setTransform(1, 0, 0, 1, 0, 0); o.clearRect(0, 0, off.width, off.height); o.setTransform(T);
    o.globalCompositeOperation = 'source-over'; o.fillStyle = cols[k]; ellipse(o, V, gi.pts); o.fill();
    o.globalCompositeOperation = 'destination-out';
    for (const gj of on) { if (gj === gi || !nearerClip(o, V, gi, gj)) continue; ellipse(o, V, gj.pts); o.fill(); o.restore(); }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    for (const [dx, dy] of seamW > 0 ? [[0, 0]] : FLUSH) ctx.drawImage(off, dx, dy);   // flush: a hair wider each way
    ctx.restore();
  });
  if (!(seamW > 0)) return;
  ctx.strokeStyle = bg; ctx.lineWidth = seamW; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  for (const g of on) strokeVisible(ctx, V, g.pts, on, [g]);           // the rims
  for (let i = 0; i < on.length; i++) for (let j = i + 1; j < on.length; j++) {   // where two discs cross
    const gi = on[i], gj = on[j], dir = cross(gi.n, gj.n), dl = Math.hypot(...dir);
    if (dl < 1e-6) continue;
    const u = dir.map(v => v / dl), a11 = dot(gi.n, gi.n), a12 = dot(gi.n, gj.n), a22 = dot(gj.n, gj.n), det = a11 * a22 - a12 * a12;
    const ka = (gi.d * a22 - gj.d * a12) / det, kb = (gj.d * a11 - gi.d * a12) / det;
    const p0 = [0, 1, 2].map(k => ka * gi.n[k] + kb * gj.n[k]);
    let t0 = -Infinity, t1 = Infinity, ok = true;
    for (const g of [gi, gj]) { const w = [0, 1, 2].map(k => p0[k] - g.c[k]), b = dot(u, w), c = dot(w, w) - g.r * g.r, disc = b * b - c;
      if (disc <= 0) { ok = false; break; } const s = Math.sqrt(disc); t0 = Math.max(t0, -b - s); t1 = Math.min(t1, -b + s); }
    if (!ok || t1 <= t0) continue;
    const pts = []; for (let k = 0; k <= 48; k++) { const t = t0 + (t1 - t0) * k / 48; pts.push([0, 1, 2].map(m => p0[m] + t * u[m])); }
    strokeVisible(ctx, V, pts, on, [gi, gj]);
  }
}
function ellipse(c, V, pts) { c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(V.X(p), V.Y(p)) : c.moveTo(V.X(p), V.Y(p))); c.closePath(); }
// clip to where disc gj is nearer than disc gi (two planes' depths differ linearly across the picture, so it is a
// half-plane); false, and no clip, if it is nearer nowhere; otherwise the caller restores
function nearerClip(o, V, gi, gj) {
  const ni = gi.n, nj = gj.n, A = -nj[0] / nj[2] + ni[0] / ni[2], B = -nj[1] / nj[2] + ni[1] / ni[2], C = gj.d / nj[2] - gi.d / ni[2];
  const m = Math.hypot(A, B);
  if (m <= 1e-9) { if (C <= 0) return false; o.save(); return true; }
  const ux = A / m, uy = B / m, c0 = -C / m, px = ux * c0, py = uy * c0, tx = -uy, ty = ux, b = 4;
  const q = [[px + tx * b, py + ty * b], [px - tx * b, py - ty * b], [px - tx * b + ux * b, py - ty * b + uy * b], [px + tx * b + ux * b, py + ty * b + uy * b]];
  o.save(); o.beginPath(); q.forEach((p, i) => i ? o.lineTo(V.X(p), V.Y(p)) : o.moveTo(V.X(p), V.Y(p))); o.closePath(); o.clip();
  return true;
}

// the globe in a state: drawn[k] (share of ring k drawn), done[k] (closed and coloured), the style and ground
function drawGlobe(ctx, V, s) {
  const gs = ringsAt(s.spin || 0, s.geom || {}), G = GROUNDS[s.ground], cols = s.cols || D.hues;
  const w = D.w * V.R, ink = s.inkCol || G.ink;
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  if (s.style === 'discs') {
    drawDiscs(ctx, V, gs, s.done, cols, G.bg, D.seam * V.R);
    const filled = gs.filter((g, k) => s.done[k]);
    gs.forEach((g, k) => { if (s.done[k] || !(s.drawn[k] > 0)) return;
      ctx.strokeStyle = ink; ctx.lineWidth = w * 0.7; strokeVisible(ctx, V, upto(g, s.drawn[k]), filled, []); });
  } else {
    for (const front of [false, true]) gs.forEach((g, k) => {
      if (!(s.drawn[k] > 0)) return;
      ctx.strokeStyle = s.done[k] ? cols[k] : ink;
      ctx.lineWidth = !front && s.style === 'lines' ? w * D.wDepth : w;
      sidePath(ctx, V, upto(g, s.drawn[k]), front); ctx.stroke(); });
  }
  gs.forEach((g, k) => { if (s.done[k] || !(s.drawn[k] > 0 && s.drawn[k] < 1)) return;   // the pen
    const p = upto(g, s.drawn[k]).at(-1); ctx.fillStyle = ink; ctx.beginPath(); ctx.arc(V.X(p), V.Y(p), w * 0.95, 0, TAU); ctx.fill(); });
}

// round 23: rings for the new idents (a parallel at any latitude; the equator tipped about an axis in its plane)
function parallelRing(phi, B, n = 160) {
  const { a, e1, e2 } = B, cp = Math.cos(rad(phi)), sp = Math.sin(rad(phi)), pts = [];
  for (let i = 0; i <= n; i++) { const l = TAU * i / n, c = Math.cos(l), s = Math.sin(l);
    pts.push([0, 1, 2].map(j => cp * (c * e1[j] + s * e2[j]) + sp * a[j])); }
  return { pts, n: a, d: sp, c: a.map(v => v * sp), r: cp };
}
function tippedRing(beta, B, k, n = 160) {
  const { a, e1, e2 } = B, ax = [0, 1, 2].map(j => k[0] * e1[j] + k[1] * e2[j]);
  const rot = v => { const c = Math.cos(beta), s = Math.sin(beta), kv = cross(ax, v), kd = dot(ax, v);
    return [0, 1, 2].map(j => v[j] * c + kv[j] * s + ax[j] * kd * (1 - c)); };
  const pts = [];
  for (let i = 0; i <= n; i++) { const l = TAU * i / n; pts.push(rot([0, 1, 2].map(j => Math.cos(l) * e1[j] + Math.sin(l) * e2[j]))); }
  return { pts, n: rot(a), d: 0, c: [0, 0, 0], r: 1 };
}
// round 23, the tubes (earth.py TUBE): a ring's runs on one side as screen polylines, each cut at the rim, the run that
// ends where the ring began joined to the one it began with, a ring wholly on one side one closed loop
function sideRuns(V, pts, front) {
  const out = [], P = p => [V.X(p), V.Y(p)], n = pts.length - 1; let cur = null, at0 = false;
  const add = (r, q) => { const l = r[r.length - 1]; if (!l || Math.hypot(q[0] - l[0], q[1] - l[1]) > 1e-6) r.push(q); };
  for (let i = 0; i <= n; i++) {
    const p = pts[i], inn = (p[2] >= 0) === front;
    if (i > 0) { const q = pts[i - 1], qin = (q[2] >= 0) === front;
      if (qin !== inn) { const s = q[2] / (q[2] - p[2]), c = P([q[0] + s * (p[0] - q[0]), q[1] + s * (p[1] - q[1])]);
        if (qin) { add(cur, c); out.push(cur); cur = null; } else cur = [c]; } }
    if (inn) { if (!cur) { cur = []; if (i === 0) at0 = true; } add(cur, P(p)); }
  }
  const loop = Math.hypot(pts[0][0] - pts[n][0], pts[0][1] - pts[n][1], pts[0][2] - pts[n][2]) < 1e-9;
  if (cur && at0 && loop) { if (!out.length) return [{ run: cur.slice(0, -1), closed: true }]; out[0] = cur.concat(out[0].slice(1)); }
  else if (cur) out.push(cur);
  return out.filter(r => r.length > 1).map(run => ({ run, closed: false }));
}
function offsetRun(run, d, closed) {
  const n = run.length;
  return run.map((p, i) => { const a = run[closed ? (i + n - 1) % n : Math.max(0, i - 1)], b = run[closed ? (i + 1) % n : Math.min(n - 1, i + 1)];
    const tx = b[0] - a[0], ty = b[1] - a[1], L = Math.hypot(tx, ty) || 1; return [p[0] - ty / L * d, p[1] + tx / L * d]; });
}
function runPath(ctx, run, closed) { ctx.beginPath(); run.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); if (closed) ctx.closePath(); }
// each ring a tube of tinted acrylic: every far run, then every near run, each its tint (faint through the middle,
// deeper along the walls) blended over what is behind (multiply on paper, screen on ink), then its highlight
// a paint for ring g that follows its depth: alpha a0 at depth z0 to 1 at z1 (a ring is flat, so its depth runs straight
// across the picture); null if its plane faces us or is seen edge on
const rgba = (c, a) => `rgba(${[1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)).join(',')},${a})`;
function depthPaint(ctx, V, g, col, z0, z1, a0) {
  const n = g.n; if (Math.abs(n[2]) < 0.03) return null;
  const gx = -n[0] / n[2], gy = -n[1] / n[2], m2 = gx * gx + gy * gy; if (m2 < 1e-9) return null;
  const at = z => { const k = (z - g.c[2]) / m2; return [V.cx + (g.c[0] + gx * k) * V.R, V.cy - (g.c[1] + gy * k) * V.R]; };
  const [a, b] = [at(z0), at(z1)], p = ctx.createLinearGradient(a[0], a[1], b[0], b[1]);
  p.addColorStop(0, rgba(col, a0)); p.addColorStop(1, rgba(col, 1)); return p;
}
// each ring a tube of tinted acrylic: its tint (faint through the middle, deeper along the walls) one unbroken loop
// fading with depth, blended over what is behind (multiply on paper, screen on ink, either order the same), then every
// highlight over all of them, on the near side only; a ring seen edge on is drawn in runs, its far runs fainter
function drawTubes(ctx, V, items, G) {
  const T = D.tube, w = D.wTube * V.R, mode = G.bg === D.night ? 'screen' : 'multiply', [dx, dy, lw, op] = T.hi;
  ctx.lineCap = 'butt'; ctx.lineJoin = 'round';
  const tube = (run, closed, paint, k) => {
    ctx.save(); ctx.globalCompositeOperation = mode; ctx.strokeStyle = paint;
    ctx.globalAlpha = T.core * k; ctx.lineWidth = w; runPath(ctx, run, closed); ctx.stroke();
    ctx.globalAlpha = T.wall * k; ctx.lineWidth = w * T.wall_w;
    for (const sg of [1, -1]) { runPath(ctx, offsetRun(run, sg * T.wall_at * w, closed), closed); ctx.stroke(); }
    ctx.restore(); };
  const light = (run, closed, paint) => {
    ctx.save(); ctx.globalAlpha = op; ctx.strokeStyle = paint; ctx.lineWidth = lw * w; ctx.translate(dx * w, dy * w);
    runPath(ctx, run, closed); ctx.stroke(); ctx.restore(); };
  const later = [];
  for (const i of items) {
    if (i.g.r <= 1e-3) continue;
    const tp = depthPaint(ctx, V, i.g, i.col, -T.fade, T.fade, T.far);
    if (tp) { const pts = i.g.pts, n = pts.length - 1, loop = Math.hypot(pts[0][0] - pts[n][0], pts[0][1] - pts[n][1]) < 1e-9;
      const run = (loop ? pts.slice(0, -1) : pts).map(p => [V.X(p), V.Y(p)]);
      tube(run, loop, tp, 1); later.push([run, loop, depthPaint(ctx, V, i.g, '#FFFFFF', 0, T.shine, 0)]); continue; }
    for (const front of [false, true]) for (const { run, closed } of sideRuns(V, i.g.pts, front)) {
      tube(run, closed, i.col, front ? 1 : T.far); if (front) later.push([run, closed, '#FFFFFF']); }
  }
  for (const [run, closed, paint] of later) light(run, closed, paint);
}
// rings as a style draws them: even lines (each in its colour, every line one weight, the far halves under the near),
// tubes (round 23), discs (round 24b: flush, no seams, no outline) or acrylic (round 24b: every disc tinted); a ring
// marked `ink` stays a line over the discs, hidden where a nearer disc covers it
function drawRings(ctx, V, items, style, G) {
  const w = D.w * V.R; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  if (style === 'tubes') { drawTubes(ctx, V, items, G); return; }
  if (style === 'acrylic') { drawAcrylic(ctx, V, items, G); return; }
  if (style === 'discs') {
    const ds = items.filter(i => !i.ink && i.g.r > 1e-3);                  // the discs alone (round 25: no ball filled under them)
    drawDiscs(ctx, V, ds.map(i => i.g), ds.map(() => true), ds.map(i => i.col), G.bg, 0);
    for (const i of items) if (i.ink) { ctx.strokeStyle = i.col; ctx.lineWidth = w * 0.8; strokeVisible(ctx, V, i.g.pts, ds.map(d => d.g), []); }
  } else {
    for (const front of [false, true]) for (const i of items) {
      if (i.g.r <= 1e-3) continue;
      ctx.strokeStyle = i.col; ctx.lineWidth = w; sidePath(ctx, V, i.g.pts, front); ctx.stroke(); }
  }
}
const globeItems = (geom, spin = 0) => ringsAt(spin, geom || {}).map((g, k) => ({ g, col: D.ring[k] }));

// round 25, the acrylic (earth.py ACRYLIC): wherever you look through the globe, the discs crossed there laid front to
// back, the nearest keeping `face` of what shows, the next `face` of the rest, the ground taking what is left, mixed in
// stacked as earth.py stacks the SVGs' cells (_stack: OKLab, a and b weighted, every crossing deeper than its darkest sheet).
// Drawn on the graphics card, per pixel, four samples a pixel (WebGL); where there is none, composited on the canvas in
// sRGB (exact in its weights, its crossings a little greyer): what is behind the globe dimmed once for each face it shows
// through, each face's colour dimmed once for each face nearer than it (nearerClip), the dimmed colours added
const OKL = hex => {
  const [r, g, b] = [1, 3, 5].map(i => { const c = parseInt(hex.slice(i, i + 2), 16) / 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); });
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b), m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b),
        s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
          0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s];
};
const fromOKL = ([L, A, B]) => {
  const l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3, m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3, s = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3;
  const v = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
  return 'rgb(' + v.map(c => { c = clamp(c, 0, 1); return Math.round(255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055)); }).join(',') + ')';
};
// colours mixed by weight in OKLCh (earth.py _mix), as a CSS colour
const mixOKL = (cols, ws) => { let L = 0, C = 0, ha = 0, hb = 0;
  cols.forEach((c, i) => { const q = OKL(c); L += ws[i] * q[0]; C += ws[i] * Math.hypot(q[1], q[2]); ha += ws[i] * q[1]; hb += ws[i] * q[2]; });
  const h = Math.atan2(hb, ha); return fromOKL([L, C * Math.cos(h), C * Math.sin(h)]); };
const ACR_VS = 'attribute vec2 aPos; uniform vec2 uHalf; varying vec2 vP; void main() { vP = aPos * uHalf; gl_Position = vec4(aPos, 0.0, 1.0); }';
const ACR_FS = `precision highp float;
varying vec2 vP; uniform vec2 uPx; uniform vec4 uN[6]; uniform vec4 uC[6]; uniform vec3 uLab[6]; uniform vec3 uSide[6]; uniform float uOn[6];
uniform vec3 uBg; uniform float uA; uniform float uAtmos;                         // the facing meridian's index
uniform float uGreen; uniform float uDark; uniform float uSmoke; uniform float uH; // uH: half a slab's thickness
vec3 lin(vec3 c) {
  float l = c.x + 0.3963377774 * c.y + 0.2158037573 * c.z, m = c.x - 0.1055613458 * c.y - 0.0638541728 * c.z, s = c.x - 0.0894841775 * c.y - 1.2914855480 * c.z;
  l = l * l * l; m = m * m * m; s = s * s * s;
  return clamp(vec3(4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                    -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s), 0.0, 1.0);
}
vec4 shade(vec2 p) {
  // each disc a slab (earth.py slabs): where the view first enters it, through its face toward us or through its side
  float z[6]; float hit[6]; float sd[6]; float n = 0.0;
  for (int i = 0; i < 6; i++) {
    z[i] = 0.0; hit[i] = 0.0; sd[i] = 0.0;
    if (uOn[i] > 0.5) {
      vec3 m = uN[i].xyz * (uN[i].z < 0.0 ? -1.0 : 1.0), w0 = vec3(p, 0.0) - uC[i].xyz;
      float r = uC[i].w, a0 = dot(w0, m);
      vec3 u0 = w0 - a0 * m, k = vec3(0.0, 0.0, 1.0) - m.z * m;
      if (m.z > 1e-4) { float zf = (uH - a0) / m.z; vec3 uf = u0 + zf * k; if (dot(uf, uf) <= r * r) { z[i] = zf; hit[i] = 1.0; } }
      if (hit[i] < 0.5) {
        float kk = dot(k, k), b = dot(u0, k), D = b * b - kk * (dot(u0, u0) - r * r);
        if (kk > 1e-8 && D >= 0.0) { float zs = (-b + sqrt(D)) / kk; if (abs(a0 + zs * m.z) <= uH) { z[i] = zs; hit[i] = 1.0; sd[i] = 1.0; } }
      }
      n += hit[i];
    }
  }
  if (n < 0.5) return vec4(0.0);                        // the discs alone: no ball (round 25)
  float zg = -1e9; vec3 green = vec3(0.0);               // the green's face, the backing, where it is
  for (int i = 0; i < 6; i++) { if (float(i) == uAtmos && hit[i] > 0.5 && sd[i] < 0.5) { green = uLab[i]; zg = z[i]; } }
  float nf = 0.0, nb = 0.0;
  for (int i = 0; i < 6; i++) { if (hit[i] > 0.5 && !(float(i) == uAtmos && sd[i] < 0.5)) { if (z[i] > zg) nf += 1.0; else nb += 1.0; } }
  float Lmin = 10.0, C = 0.0, ns = 0.0; vec2 ab = vec2(0.0);            // the sheets stacked (earth.py _stack)
  float tot = nf > 0.5 ? 1.0 : 1.0 - uGreen, cnt = nf > 0.5 ? nf : nb;
  if (nf < 0.5) { float wg = nb > 0.5 ? uGreen : 1.0; Lmin = min(Lmin, green.x); C += wg * length(green.yz); ab += wg * green.yz; ns += 1.0; }
  for (int i = 0; i < 6; i++) {
    bool mine = hit[i] > 0.5 && !(float(i) == uAtmos && sd[i] < 0.5) && ((nf > 0.5) == (z[i] > zg));
    if (mine) {
      float rank = 0.0;
      for (int j = 0; j < 6; j++) { if (j != i && hit[j] > 0.5 && !(float(j) == uAtmos && sd[j] < 0.5) && ((nf > 0.5) == (z[j] > zg)) && z[j] > z[i]) rank += 1.0; }
      float w = tot * (rank > cnt - 1.5 ? pow(1.0 - uA, rank) : uA * pow(1.0 - uA, rank));
      vec3 col = sd[i] > 0.5 ? uSide[i] : uLab[i];
      Lmin = min(Lmin, col.x); C += w * length(col.yz); ab += w * col.yz; ns += 1.0;
    }
  }
  float R = C > 1e-6 ? length(ab) / C : 1.0;
  float steps = nf > 0.5 ? ns - 1.0 : min(ns - 1.0, 1.0);                // behind the green, the back halves one sheet
  float L = ns > 1.5 ? Lmin - uDark * steps - uSmoke * (1.0 - R) : Lmin;
  return vec4(lin(vec3(L, ab)), 1.0);
}
void main() {
  vec4 acc = shade(vP + uPx * vec2(-0.25, -0.25)) + shade(vP + uPx * vec2(0.25, -0.25)) + shade(vP + uPx * vec2(-0.25, 0.25)) + shade(vP + uPx * vec2(0.25, 0.25));
  acc /= 4.0;
  vec3 c = acc.a > 0.0 ? acc.rgb / acc.a : vec3(0.0);
  vec3 e = mix(12.92 * c, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(0.0031308, c));
  gl_FragColor = vec4(e * acc.a, acc.a);
}`;
let AGL;                                                                    // undefined: not tried; false: none
function acrylicGL() {
  if (AGL !== undefined) return AGL;
  AGL = false;
  try {
    const cv = document.createElement('canvas'), gl = cv.getContext('webgl', { premultipliedAlpha: true, preserveDrawingBuffer: true, antialias: false });
    if (!gl) return AGL;
    const sh = (type, src) => { const q = gl.createShader(type); gl.shaderSource(q, src); gl.compileShader(q);
      if (!gl.getShaderParameter(q, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(q)); return q; };
    const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, ACR_VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, ACR_FS)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr));
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const u = n => gl.getUniformLocation(pr, n);
    AGL = { cv, gl, pr, buf, aPos: gl.getAttribLocation(pr, 'aPos'),
            u: { half: u('uHalf'), px: u('uPx'), N: u('uN'), C: u('uC'), lab: u('uLab'), on: u('uOn'), bg: u('uBg'), a: u('uA'),
                 atmos: u('uAtmos'), green: u('uGreen'), dark: u('uDark'), smoke: u('uSmoke'), h: u('uH'), side: u('uSide') } };
  } catch (e) { console.warn('acrylic: no WebGL; compositing in sRGB', e); AGL = false; }
  return AGL;
}
function drawAcrylic(ctx, V, items, G) {
  const A = D.acrylic[G.bg === D.night ? 'night' : 'paper'], a = A.face, on = items.filter(i => i.g.r > 1e-3);   // (edge on, a slab still shows its side)
  const edges = front => { if (!(A.edge > 0)) return; ctx.save(); ctx.lineCap = 'butt'; ctx.lineJoin = 'round'; ctx.lineWidth = A.edge * V.R;
    for (const i of on) { ctx.strokeStyle = i.col; sidePath(ctx, V, i.g.pts, front); ctx.stroke(); } ctx.restore(); };
  const X = on.length <= 6 ? acrylicGL() : false;
  if (X) {
    const T = ctx.getTransform(), k = Math.max(Math.hypot(T.a, T.b), Math.hypot(T.c, T.d)), half = 1.02 + A.thick / 2;
    const size = Math.max(2, Math.min(2048, Math.ceil(2 * half * V.R * k) || 2)), { cv, gl, u } = X;
    if (cv.width !== size || cv.height !== size) { cv.width = size; cv.height = size; }
    const N = new Float32Array(24), Cc = new Float32Array(24), L = new Float32Array(18), Sd = new Float32Array(18), O = new Float32Array(6);
    on.forEach((i, j) => { const g = i.g, q = OKL(i.col); N.set([g.n[0], g.n[1], g.n[2], g.d], 4 * j); Cc.set([g.c[0], g.c[1], g.c[2], g.r], 4 * j);
      L.set(q, 3 * j); Sd.set([q[0] - A.side, q[1] * (1 + A.sideC), q[2] * (1 + A.sideC)], 3 * j); O[j] = 1; });   // the side (earth.py _side)
    gl.viewport(0, 0, size, size); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(X.pr);
    gl.uniform2f(u.half, half, half); gl.uniform2f(u.px, 2 * half / size, 2 * half / size);
    gl.uniform4fv(u.N, N); gl.uniform4fv(u.C, Cc); gl.uniform3fv(u.lab, L); gl.uniform3fv(u.side, Sd); gl.uniform1fv(u.on, O); gl.uniform3fv(u.bg, OKL(G.bg)); gl.uniform1f(u.a, a);
    gl.uniform1f(u.atmos, on.indexOf(items[D.atmos])); gl.uniform1f(u.h, A.thick / 2);
    gl.uniform1f(u.green, A.green); gl.uniform1f(u.dark, A.dark); gl.uniform1f(u.smoke, A.smoke);
    gl.bindBuffer(gl.ARRAY_BUFFER, X.buf); gl.enableVertexAttribArray(X.aPos); gl.vertexAttribPointer(X.aPos, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    edges(false); ctx.drawImage(cv, V.cx - half * V.R, V.cy - half * V.R, 2 * half * V.R, 2 * half * V.R); edges(true);
    return;
  }
  drawRings(ctx, V, items, 'discs', G);                                     // no graphics card: the flush discs, which the
                                                                             // acrylic matches wherever one disc shows
  edges(true);
}

// the printer: a head shuttles across and back, a band lower each pass, and leaves the globe in its wake
const PRINT = { lead: 0.15, pass: 0.3, n: 6 };
function drawPrinter(ctx, V, t, style, G) {
  const items = globeItems(), ext = (1 + D.w) * V.R, h = 2 * ext / PRINT.n, top = V.cy - ext;
  const left = V.cx - ext - h, right = V.cx + ext + h, u = (t - PRINT.lead) / PRINT.pass, k = Math.floor(u), f = smooth(u - k);
  if (k >= PRINT.n) { drawRings(ctx, V, items, style, G); return; }
  const hx = k < 0 ? left : k % 2 ? right - (right - left) * f : left + (right - left) * f;
  if (k >= 0) {
    ctx.save(); ctx.beginPath();
    for (let j = 0; j < k; j++) ctx.rect(left, top + j * h - 0.5, right - left, h + 1);
    if (k % 2) ctx.rect(hx, top + k * h - 0.5, right - hx, h + 1); else ctx.rect(left, top + k * h - 0.5, hx - left, h + 1);
    ctx.clip(); drawRings(ctx, V, items, style, G); ctx.restore();
  }
  ctx.fillStyle = G.ink; ctx.beginPath(); ctx.arc(hx, top + (Math.max(k, 0) + 0.5) * h, h * 0.42, 0, TAU); ctx.fill();
}

// round 24b, the gyroscope (the owner: "The gyroscope is too chaotic"): the globe spins on its axis, as a gyroscope's
// rotor does, the meridians turning about the pole (the parallels, round it, stay), slowing to rest, whole and
// upright; then it tilts to the Earth's 23.4 degrees. (Two gimbals, the parallels rocking as well, were tried and were
// busier: the parallels show their faces as they turn.)
// Round 25: the tilt starts `lap` before the spin ends, so the globe never stops between them (the storyboard's motion
// trace showed it standing still for a moment); after the brand critic's first round, a second's spin and half a turn,
// the least that brings each meridian back to its own place (a full turn swapped the meridian facing you six times).
// After the acrylic critic's third round: slowing quadratically, not cubically (the cubic spin was spent by half time
// and stood still a third of a second before the lean; the quadratic starts slower, so it is calmer too), and the lean
// starting 0.3 before the spin ends
const GYRO = { spin: 1.0, turns: 0.5, lap: 0.3 };
// every ident's tilt (round 25, after the brand critics' first round: 0.55 s read as a drift, the one move only EARF
// makes): 0.4 s, leaning a little past the Earth's 23.4 degrees and settling into it, as a gyroscope finds its axis
// (keys: its share of the way, its share of the lean, each reached smoothly). The third critic: 0.3 s, its settle at
// 0.4 too slow to see, so the lean ended in a creep, not a landing
const TILT = { dur: 0.3, keys: [[0, 0], [0.55, 1.12], [0.8, 0.98], [1, 1]] };
function tiltAt(t) {
  const x = clamp(t / TILT.dur, 0, 1), K = TILT.keys;
  for (let i = 1; i < K.length; i++) if (x <= K[i][0]) return K[i - 1][1] + (K[i][1] - K[i - 1][1]) * smooth((x - K[i - 1][0]) / (K[i][0] - K[i - 1][0]));
  return 1;
}
function rotRing(g, ax, ang) {
  const L = Math.hypot(...ax), k = ax.map(v => v / L), c = Math.cos(ang), s = Math.sin(ang);
  const rot = v => { const kv = cross(k, v), kd = dot(k, v); return [0, 1, 2].map(j => v[j] * c + kv[j] * s + k[j] * kd * (1 - c)); };
  return { ...g, pts: g.pts.map(rot), n: rot(g.n), c: rot(g.c) };
}
function drawGyro(ctx, V, t, style, G) {
  const s = clamp(t / GYRO.spin, 0, 1), e = 1 - Math.pow(1 - s, 2), lean = D.lean * tiltAt(t - GYRO.spin + GYRO.lap);
  const B = basis(lean, D.elev);
  const items = ringsAt(0, { lean, elev: D.elev }).map((g, k) => ({ g: k < 3 ? g : rotRing(g, B.a, TAU * GYRO.turns * (1 - e)), col: D.ring[k] }));
  drawRings(ctx, V, items, style, G);
}

// the kick: seen from above the pole the globe is a speaker, its parallels rings round one centre and its meridians
// spokes; it kicks twice, three rings of colour going out at each hit, then tips down to the Earth's tilt
const KICK = { hits: [0.15, 0.62], tilt: [1.05, 1.9] };
const pulse = x => x < 0 ? 0 : x < 0.045 ? x / 0.045 : Math.exp(-(x - 0.045) / 0.11);
function ripples(ctx, V, t, hits, hue0) {
  hits.forEach((h, j) => { for (let m = 0; m < 3; m++) {
    const p = (t - h - 0.05 * m) / 0.62; if (p <= 0 || p >= 1) continue;
    ctx.globalAlpha = (1 - p) * (1 - p); ctx.strokeStyle = D.hues[(hue0(j) + m) % 6]; ctx.lineWidth = D.w * V.R * (1 - 0.6 * p);
    ctx.beginPath(); ctx.arc(V.cx, V.cy, V.R * (1.06 + 0.85 * p), 0, TAU); ctx.stroke(); } });
  ctx.globalAlpha = 1;
}
function drawKick(ctx, V, t, style, G) {
  const tl = smooth((t - KICK.tilt[0]) / (KICK.tilt[1] - KICK.tilt[0])), geom = { lean: D.lean * tl, elev: 90 + (D.elev - 90) * tl };
  const amp = KICK.hits.reduce((a, h) => a + pulse(t - h), 0);
  ripples(ctx, V, t, KICK.hits, j => 3 * j);
  drawRings(ctx, view(0, 0, V.cx, V.cy, V.R * (1 + 0.09 * amp)), globeItems(geom), style, G);
}
// and looped, for the speakers: a kick each half second, the colours going round
function drawKickLoop(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground], V = view(W, H, W / 2, H / 2, Math.min(W, H) * 0.25), beat = 0.5, n = Math.floor(t / beat);
  ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  const hits = [n - 1, n].map(i => i * beat);
  ripples(ctx, V, t, hits, j => 3 * (n - 1 + j));
  const amp = hits.reduce((a, h) => a + pulse(t - h), 0);
  drawRings(ctx, view(0, 0, V.cx, V.cy, V.R * (1 + 0.09 * amp)), globeItems({ lean: 0, elev: 90 }), o.style || 'even', G);
  return 4.0;
}

// an ident: the globe arrives, holds, moves aside, and EARF is wiped out of the globe's rim beside it (round 25: typed
// in, it came as four one-frame jumps, the harshest changes in the ident); `marks`: an ident's own phases, for the
// storyboard. Each arrival ends `lap` into its tilt
const arrival = (end, lap) => Math.max(end, end - lap + TILT.dur);
const IDENTS = { printer: { dur: 2.05, draw: drawPrinter },
                 gyro: { get dur() { return arrival(GYRO.spin, GYRO.lap); }, draw: drawGyro,
                         marks: () => [[GYRO.spin - GYRO.lap, 'tilt'], [GYRO.spin, 'spun']] },
                 kick: { dur: 1.95, draw: drawKick },
                 coin: { get dur() { return arrival(COIN.spin, COIN.lap); }, draw: (...a) => coinAt(...a),
                         marks: () => [[coinTable().tip, 'tip'], [COIN.spin - COIN.lap, 'tilt']] },
                 rise: { get dur() { return arrival(RISE.up, RISE.lap); }, draw: (...a) => drawRise(...a),
                         marks: () => [[RISE.up - RISE.lap, 'tilt']] },
                 roll: { get dur() { return arrival(ROLL.roll, ROLL.lap); }, draw: (...a) => drawRoll(...a),
                         marks: () => [[ROLL.roll, 'stopped']] },
                 download: { get dur() { return arrival(LOADGIF.passes.length * LOADGIF.each, LOADGIF.lap); }, draw: (...a) => drawDownload(...a),
                             marks: () => [[LOADGIF.passes.length * LOADGIF.each, 'sharp']] },
                 planet: { get dur() { return PLANET.end; }, get last() { return PLANET.last; }, draw: (...a) => drawPlanet(...a),
                           marks: () => [[PLANET.wind.at, 'wind'], [PLANET.hit, 'hit'], [PLANET.char.start, 'char'], [PLANET.crater.at, 'crater']] },
                 iris: { get dur() { return arrival(IRIS.open, IRIS.lap); }, draw: (...a) => drawIris(...a),
                         marks: () => [[IRIS.open - IRIS.lap, 'tilt'], [IRIS.open, 'open']] },
                 open: { get dur() { return arrival(OPEN.lead + 5 * OPEN.stagger + OPEN.each, OPEN.lap); },
                         draw: (...a) => drawOpen(...a), marks: () => [[OPEN.lead + 5 * OPEN.stagger + OPEN.each - OPEN.lap, 'tilt']] } };
// HOLD: round 25's second critic, 0.35 to 0.1 (with the lean's settle, the globe stood still half a second before it
// moved); the third, 0.1 to 0, the move aside starting on the frame the lean lands. The wipe starts `lead` before the
// move ends: the acrylic critic, 0.15 to 0 (it wiped the E while the globe still crowded it); the third ident critic,
// 0 to 0.1 (at 0 the globe stopped dead, then the name jumped in; at 0.1 the rim is already clear of the E). REST: the
// lockup held at the end, round 26 1.3 to 1.0 (the Planet's second critic, "a 1.0 s hold is worth considering at house
// level"; the owner: "Shorten to 1.0 s")
const HOLD = 0, MOVE = 0.5, WIPE = { lead: 0.1, dur: 0.45 }, REST = 1.0;
function identTimes(kind) { const m0 = IDENTS[kind].dur + HOLD, w0 = m0 + MOVE - WIPE.lead; return { move0: m0, word0: w0, end: w0 + WIPE.dur + REST }; }
function identLayout(W, H) {
  const lockW = 450 + 110 + D.wordW, k = Math.min(W * 0.74 / lockW, H * 0.5 / 450), x0 = (W - lockW * k) / 2;
  return { R: 225 * k / (1 + D.w / 2), cx: x0 + 225 * k, cy: H / 2, wx: x0 + 560 * k, wy: H / 2 - 150 * k, k };
}
function drawIdent(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground], L = identLayout(W, H), T = identTimes(o.kind), m = smooth((t - T.move0) / MOVE);
  const hR = Math.min(H * 0.34, W * 0.3), V = view(W, H, W / 2 + (L.cx - W / 2) * m, H / 2 + (L.cy - H / 2) * m, hR + (L.R - hR) * m);
  ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  const I = IDENTS[o.kind];                                                // (a frame's clock can read a hair before a click;
  I.draw(ctx, V, clamp(t, 0, (I.last || I.dur) + 0.01), o.style, G);       // `last`: an ident still moving as it goes aside)
  const wf = 1 - Math.pow(1 - clamp((t - T.word0) / WIPE.dur, 0, 1), 3);    // from the globe's right rim, left to right
  if (wf > 0) { const x0 = L.cx + L.R * (1 + D.w / 2), x1 = L.wx + D.wordW * L.k + 2;
    ctx.save(); ctx.beginPath(); ctx.rect(x0, 0, (x1 - x0) * wf, H); ctx.clip();
    ctx.translate(L.wx, L.wy); ctx.scale(L.k, L.k); ctx.fillStyle = G.ink; D.letters.forEach(d => ctx.fill(new Path2D(d))); ctx.restore(); }
  return T.end;
}

// the loader: a white circle rolling across the ink uncovers the six behind it, and covers them again coming back
const LOAD = { go: 2.6, rest: 0.55 };
function drawLoader(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground], bg = G.bg, ball = G.ink;
  ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
  const r = Math.min(H * 0.17, W / 30), s = 2.9 * r, x0 = W / 2 - 3 * s, y = H / 2, per = 2 * (LOAD.go + LOAD.rest);
  const ph = ((t % per) + per) % per;
  let x;                                                                    // the ball's centre, slot 0 to slot 6 and back
  if (ph < LOAD.go) x = ph / LOAD.go; else if (ph < LOAD.go + LOAD.rest) x = 1;
  else if (ph < 2 * LOAD.go + LOAD.rest) x = 1 - (ph - LOAD.go - LOAD.rest) / LOAD.go; else x = 0;
  const bx = x0 + 6 * s * x;
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, bx, H); ctx.clip();           // what the ball has passed
  D.hues.forEach((c, k) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x0 + k * s, y, r, 0, TAU); ctx.fill(); });
  ctx.restore();
  ctx.fillStyle = ball; ctx.beginPath(); ctx.arc(bx, y, r, 0, TAU); ctx.fill();
  return per;
}

// the cursor: a circle, and the six colours each a beat behind it; a ghost hand moves it when no one does
const TRAIL = 0.075;
function ghost(t, W, H) {
  const T = 9.0, u = ((t % T) + T) % T, cx = W / 2, cy = H / 2, A = Math.min(W, H) * 0.34;
  const P0 = [-1.25, 0.35], P1 = [-0.55, -0.4], C = [0.05, -0.4], r = 0.6, P2 = [1.2, 0.5], P3 = [-0.25, 0.55], Q = [-0.2, -1.0];
  const lerp = (p, q, f) => [p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f];
  const segs = [
    [0.0, 1.0, f => lerp(P0, P1, smooth(f))], [1.0, 1.4, () => P1],
    [1.4, 3.4, f => { const th = Math.PI + TAU * smooth(f); return [C[0] + r * Math.cos(th), C[1] + 0.8 * r * Math.sin(th)]; }],
    [3.4, 3.8, () => P1], [3.8, 4.4, f => lerp(P1, P2, smooth(f))], [4.4, 4.9, () => P2],
    [4.9, 6.7, f => { const e = smooth(f), p = lerp(P2, P3, e); return [p[0], p[1] - 0.35 * Math.sin(TAU * 1.5 * e)]; }],
    [6.7, 7.1, () => P3],
    [7.1, 8.4, f => { const e = smooth(f), m = 1 - e; return [m * m * P3[0] + 2 * m * e * Q[0] + e * e * P0[0], m * m * P3[1] + 2 * m * e * Q[1] + e * e * P0[1]]; }],
    [8.4, 9.0, () => P0]];
  for (const [ta, tb, fn] of segs) if (u >= ta && u < tb) { const p = fn((u - ta) / (tb - ta)); return [cx + A * p[0], cy + A * p[1]]; }
  return [cx + A * P0[0], cy + A * P0[1]];
}
function drawCursor(ctx, W, H, t, o, at) {
  const G = GROUNDS[o.ground], r = Math.max(9, Math.min(W, H) * 0.028);
  ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  for (let k = 6; k >= 1; k--) { const p = at(t - k * TRAIL); ctx.fillStyle = D.hues[k - 1]; ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, TAU); ctx.fill(); }
  const p = at(t); ctx.fillStyle = G.ink; ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, TAU); ctx.fill();
  return 9.0;
}

// round 25, the coin (the owner: "The coin was still supposed to flash between all colors first"): it spins on its
// edge, each half turn showing a new face: the six colours in turn, round the colour wheel from yellow to green (Acid,
// Dust, Flare, Haze, Ice, Poison), and then the globe, whose facing disc is green, so the last colour runs into it. After the
// brand critic's first round: the colours at one steady speed, `half` seconds each (slowing all the way had crammed the
// first into flickers and dragged the last), then it lands on the globe, slowing over a quarter turn (`land`; its speed
// at the start the colours' own). At 0.34 s a half turn the faces flash under three times a second (WCAG 2.3.1: each
// swaps a large area between the ground and a colour); faster wants a flash test first. Its rim, the coin's thickness,
// is its face's colour, flat. The tilt starts `lap` before it lands
// (the second critic: the tilt starts as the landing's last movement dies, lap 0.25, and the third 0.3, so the lean
// lands with the landing; the coin twice as thick, 0.14 of its
// radius, as a real coin's edge is, so edge on it is a bar, not a hairline)
// Round 26, a real coin's physics (the owner, of the coin: "Real coin physics"): it spins on its edge, slowing a
// little as friction takes it (`slow`: each half turn longer, the first `half`, so never under three flashes a second),
// a new colour on each face as before; the globe's face comes round and the coin tips over, rolling round on its rim,
// and the lower it leans the faster it wobbles, as Euler's disk does (the lean falls as the square root of the time
// left over `tip`; the wobble, once the coin can no longer turn its back to you, quickens to `whirl` radians a second),
// its face hardly turning while the wobble whirls (it turns at the wobble's rate times one less the cosine of the lean,
// so not at all when it lies flat), until it lies flat. The view, a little above the coin while it spins (`eps0`
// radians), rises over it as it falls, overhead by `rise` of the way, so it lands face up, facing you, the globe
// upright (its last turn eased into the fall). It starts to tip `at` radians after the globe's face shows edge on, so
// that it turns its back to you no more: six edge-ons in all, never more than three in a second
const COIN = { half: 0.34, slow: 0.06, tip: 0.85, rise: 0.6, at: -1.2, eps0: 0.25, whirl: 34, thick: 0.14, lap: 0.3,
               flash: [2, 1, 0, 5, 4, 3],
               get spin() { return coinTable().end; }, get end() { return arrival(this.spin, this.lap) + 0.6; } };
let CT = null;
function coinTable() {                                       // the coin's motion, worked out once at 2000 steps a second:
  if (CT) return CT;                                         // the wobble's angle phi, the lean alpha (of the face from
  const dt = 1 / 2000, w0 = Math.PI / COIN.half, R = [];    // the table's normal), the view's height eps, the face's turn
  let t = 0, phi = -Math.PI / 2, rho = phi, flips = 0, side = 1, tTip = null, wTip = 0, tc = null, wc = 0;   // rho, the edge-ons
  for (let i = 0; i < 40000; i++) {
    let alpha = Math.PI / 2, eps = COIN.eps0, w = w0 / (1 + COIN.slow * t);
    if (tTip !== null) {
      const tau = Math.min(1, (t - tTip) / COIN.tip);
      alpha = Math.PI / 2 * Math.sqrt(1 - tau);
      eps = COIN.eps0 + (Math.PI / 2 - COIN.eps0) * smooth((t - tTip) / (COIN.tip * COIN.rise));
      if (tc === null && eps > alpha) { tc = t; wc = wTip; }        // (past here the coin cannot turn its back to you)
      w = tc === null ? wTip : wc + (COIN.whirl - wc) * Math.pow(Math.min(1, (t - tc) / (tTip + COIN.tip - tc)), 2);
    }
    const s = Math.cos(alpha) * Math.sin(eps) + Math.sin(alpha) * Math.cos(phi) * Math.cos(eps);
    if (s * side < 0) { side = -side; flips++; }
    R.push([phi, alpha, eps, rho, flips]);
    if (tTip !== null && t - tTip >= COIN.tip) break;
    const ph = Math.atan2(Math.sin(phi), Math.cos(phi));
    if (tTip === null && flips >= COIN.flash.length && ph >= COIN.at && ph < Math.PI / 2) { tTip = t; wTip = w; }
    phi += w * dt; rho += w * (1 - Math.cos(alpha)) * dt; t += dt;
  }
  const last = R[R.length - 1], turn = Math.atan2(Math.sin(last[3]), Math.cos(last[3]));   // the face lands upright: its
  R.forEach((r, i) => { r[3] -= turn * smooth((i * dt - tTip) / COIN.tip); });             // last turn eased into the fall
  CT = { R, dt, end: (R.length - 1) * dt, tip: tTip };
  return CT;
}
function coinAt(ctx, V, t, style, G) {
  const T = coinTable(), items = globeItems({ lean: D.lean * tiltAt(t - COIN.spin + COIN.lap), elev: D.elev });
  if (t >= T.end) { drawRings(ctx, V, items, style, G); return; }
  const f = clamp(t, 0, T.end) / T.dt, i = Math.min(T.R.length - 2, Math.floor(f)), e = f - i, A0 = T.R[i], A1 = T.R[i + 1];
  const [phi, alpha, eps, rho] = [0, 1, 2, 3].map(j => A0[j] + (A1[j] - A0[j]) * e), flips = A0[4];
  const n = [Math.sin(alpha) * Math.sin(phi), Math.cos(alpha), Math.sin(alpha) * Math.cos(phi)];   // the face's normal, on
  const e1 = [Math.cos(phi), 0, -Math.sin(phi)], e2 = cross(n, e1), psi = rho - phi;               // the table (y up)
  const f1 = e1.map((v, j) => Math.cos(psi) * v + Math.sin(psi) * e2[j]), f2 = e1.map((v, j) => -Math.sin(psi) * v + Math.cos(psi) * e2[j]);
  const zv = [0, Math.sin(eps), Math.cos(eps)], yv = [0, Math.cos(eps), -Math.sin(eps)], front = dot(n, zv) >= 0;
  const g1 = front ? f1 : f1.map(v => -v);                                   // (its back is drawn the right way round)
  const L = [V.R * g1[0], -V.R * dot(g1, yv), -V.R * f2[0], V.R * dot(f2, yv)];   // the face's unit disc onto the screen
  const col = flips < COIN.flash.length ? D.hues[COIN.flash[flips]] : null, A = D.acrylic[G.bg === D.night ? 'night' : 'paper'];
  const disc = (dx, dy) => { ctx.save(); ctx.transform(L[0], L[1], L[2], L[3], V.cx + dx, V.cy + dy); ctx.beginPath(); ctx.arc(0, 0, 1, 0, TAU); ctx.restore(); };
  if (style !== 'even') {                                                   // the rim: the coin's thickness behind its face
    const c0 = col || D.ring[D.atmos], q = OKL(c0), k = (front ? -1 : 1) * COIN.thick * V.R;   // (in acrylic its side's deeper
    ctx.fillStyle = style === 'acrylic' ? fromOKL([q[0] - A.side, q[1] * (1 + A.sideC), q[2] * (1 + A.sideC)]) : c0;   // tone)
    for (let j = 1; j <= 12; j++) { disc(n[0] * k * j / 12, -dot(n, yv) * k * j / 12); ctx.fill(); }
  }
  ctx.save(); ctx.transform(L[0], L[1], L[2], L[3], V.cx, V.cy);
  ctx.fillStyle = G.bg; ctx.beginPath(); ctx.arc(0, 0, 1, 0, TAU); ctx.fill();   // the face is solid: no rim through it
  const U = view(0, 0, 0, 0, 1);
  if (!col) drawRings(ctx, U, items, style, G);
  else if (style !== 'even') { ctx.fillStyle = col; ctx.beginPath(); ctx.arc(0, 0, 1, 0, TAU); ctx.fill(); }
  else { ctx.strokeStyle = col; ctx.lineWidth = D.w; ctx.beginPath(); ctx.arc(0, 0, 1 - D.w / 2, 0, TAU); ctx.stroke(); }
  ctx.restore();
}

// round 25, Open (new): the globe begins as the flat globe icon, each of its six discs seen edge on, a line: the
// parallels level bars, the meridians lines through its middle. Each turns about its line and opens into its disc, one
// a beat after another (the equator first, then the meridians, then the parallels), quickly, so the lines become the
// globe; the globe whole and upright, then it tilts. In the discs a disc's edge shows while it is nearly edge on, as
// a sheet's would, and is gone when it is open. After the brand critic's first round: each disc opens in 0.4 s (0.55
// crept), and until it is `whole` open (a share) it is drawn whole, in front of the discs it crosses, as one clean
// band: drawn in its depth while nearly edge on it showed slivers and its far edge through the discs before it
// (the second critic: one bloom, each disc 0.65 s (its 0.6, a hair more to round the peak) and 0.04 apart, so the ball no longer snaps open and no parallel lies
// as a bar on a finished globe; the lean 0.4 into it, so it does not park; the third: the line icon held 0.3 s before
// it opens, long enough to read as the icon that becomes the globe; the lean, 0.3 s since, 0.3 into it, so it lands
// as the last disc opens and nothing parks before the move aside)
const OPEN = { lead: 0.3, each: 0.65, stagger: 0.04, order: [4, 0, 5, 2, 1, 3], lap: 0.3, whole: 0.3 };
function drawOpen(ctx, V, t, style, G) {
  const last = OPEN.lead + 5 * OPEN.stagger + OPEN.each, lean = D.lean * tiltAt(t - last + OPEN.lap);
  const items = ringsAt(0, { lean, elev: D.elev }).map((g, k) => {
    const f = clamp((t - OPEN.lead - OPEN.order[k] * OPEN.stagger) / OPEN.each, 0, 1), e = 1 - Math.pow(1 - f, 3);
    const L = Math.hypot(...g.n), rho = Math.hypot(g.n[0], g.n[1]);
    if (rho < 1e-6) return { g, col: D.ring[k], open: e };
    const ax = [g.n[1] / rho, -g.n[0] / rho, 0];                            // its long axis, in the picture's plane
    return { g: rotRing(g, ax, -Math.asin(clamp(g.n[2] / L, -1, 1)) * (1 - e) * 0.995), col: D.ring[k], open: e };
  });
  const thin = style === 'discs' ? items.filter(i => i.open < OPEN.whole) : [], rest = items.filter(i => !thin.includes(i));
  drawRings(ctx, V, rest, style, G);
  ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';                 // the nearly edge-on discs, whole, in front
  for (const i of thin) { const w = D.w * V.R * (1 - i.open / OPEN.whole);
    ctx.fillStyle = ctx.strokeStyle = i.col; ellipse(ctx, V, i.g.pts); ctx.fill(); if (w > 0.3) { ctx.lineWidth = w; ctx.stroke(); } }
  ctx.restore();
}

// round 25, Roll (new, from the brand critic's first round): the globe rolls in from the right like a ball, upright,
// turning as it travels (its turn its distance over its radius: it does not slip), slowing evenly to a stop at its
// place, and rocks back into its lean, against the roll, as a ball would. `from` how far right it starts, in radii
const ROLL = { roll: 0.9, from: 3.7, lap: 0.0 };
function drawRoll(ctx, V, t, style, G) {
  const s = clamp(t / ROLL.roll, 0, 1), back = ROLL.from * (1 - s) * (1 - s);
  const lean = back * 180 / Math.PI + D.lean * tiltAt(t - ROLL.roll + ROLL.lap);
  drawRings(ctx, view(0, 0, V.cx + back * V.R, V.cy, V.R), globeItems({ lean, elev: D.elev }), style, G);
}

// round 25, Iris (new, the third ident critic's idea): the finished globe, upright, still and full size at its place,
// revealed through a circle opening from its centre to its own outline (cubic ease-out), as a late-90s 'circle out';
// nothing inside moves or scales, and the circle has no stroke. The lean starts `lap` before it is open
const IRIS = { open: 0.3, lap: 0.1 };
function drawIris(ctx, V, t, style, G) {
  const e = 1 - Math.pow(1 - clamp(t / IRIS.open, 0, 1), 3);
  if (e <= 0) return;
  const items = globeItems({ lean: D.lean * tiltAt(t - IRIS.open + IRIS.lap), elev: D.elev });
  if (e >= 1) { drawRings(ctx, V, items, style, G); return; }
  ctx.save(); ctx.beginPath(); ctx.arc(V.cx, V.cy, e * V.R * (1 + D.w), 0, TAU); ctx.clip();
  drawRings(ctx, V, items, style, G); ctx.restore();
}

// round 25, Download (new): the globe arrives as a picture did over a modem in 1999, an interlaced GIF: the whole of it
// coarse at once, in blocks, then each pass finer (the blocks halving), every pass sweeping down over the last, until it
// is sharp; then it tilts. `passes` the blocks' sizes, of the globe's radius
const LOADGIF = { passes: [1 / 4, 1 / 8, 1 / 16, 1 / 32], each: 0.2, lap: 0.1 };
let LOW = null;
function lowres(ctx, V, items, style, G, b) {                               // the globe as blocks b of the radius
  if (!LOW) LOW = document.createElement('canvas');
  const n = Math.max(2, Math.round(2 / b)), o = LOW; if (o.width !== n || o.height !== n) { o.width = n; o.height = n; }
  const lc = o.getContext('2d'); lc.setTransform(1, 0, 0, 1, 0, 0); lc.fillStyle = G.bg; lc.fillRect(0, 0, n, n);
  drawRings(lc, view(n, n, n / 2, n / 2, n / 2), items, style, G);
  ctx.save(); ctx.imageSmoothingEnabled = false; ctx.drawImage(o, V.cx - V.R, V.cy - V.R, 2 * V.R, 2 * V.R); ctx.restore();
}
function drawDownload(ctx, V, t, style, G) {
  t = Math.max(0, t);
  const P = LOADGIF.passes, end = P.length * LOADGIF.each;
  const items = globeItems({ lean: D.lean * tiltAt(t - end + LOADGIF.lap), elev: D.elev }), k = Math.floor(t / LOADGIF.each), f = t / LOADGIF.each - k;
  if (k >= P.length) { drawRings(ctx, V, items, style, G); return; }
  if (k > 0) lowres(ctx, V, items, style, G, P[k - 1]);                     // the last pass, whole
  const sweep = k === 0 ? 1 : f;                                             // the first arrives whole; the rest sweep down
  ctx.save(); ctx.beginPath(); ctx.rect(V.cx - V.R * 1.1, V.cy - V.R * 1.1, V.R * 2.2, V.R * 2.2 * sweep); ctx.clip();
  if (k === 0) { ctx.fillStyle = G.bg; ctx.fill(); }
  lowres(ctx, V, items, style, G, P[k]); ctx.restore();
}

// round 24b, Earthrise (a new idea, after the photograph of the Earth rising over the Moon): the whole globe, upright,
// rises from behind a horizon, slowing as it clears it; then it tilts
const RISE = { up: 1.2, from: 2.3, lap: 0.25 };
function drawRise(ctx, V, t, style, G) {
  const s = clamp(t / RISE.up, 0, 1), e = 1 - Math.pow(1 - s, 3), u = tiltAt(t - RISE.up + RISE.lap);
  const foot = V.cy + V.R * (1 + D.w);                                       // the horizon, where the globe comes to rest
  ctx.save(); ctx.beginPath(); ctx.rect(V.cx - 4 * V.R, foot - 8 * V.R, 8 * V.R, 8 * V.R); ctx.clip();
  drawRings(ctx, view(0, 0, V.cx, V.cy + RISE.from * V.R * (1 - e), V.R), globeItems({ lean: D.lean * u, elev: D.elev }), style, G);
  ctx.restore();
}
function drawCoin(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground]; ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  coinAt(ctx, view(W, H, W / 2, H / 2, Math.min(W, H) * 0.3), t, o.style || 'discs', G);
  return COIN.end;
}

// the globe as a Death Star (core.py), its dish a driver, kicking for the speakers: a beat a second. After the brand
// critic's three rounds, keyed: the push (0.06 s, cubic ease-out) throws the whole driver forward 1.10 times about its
// centre, pops the dish flush (depth to 0, the rings concentric) and swells the dust cap 1.2 times; it holds to 0.13 s;
// pulls back once past rest (at 0.24 s the depth 0.75, the driver 0.95, the cap 0.9: a cone sinking back, eased in and
// out); and rests by 0.42 s. From 0.04 s one ring of sound leaves the rim, knocked out of the globe in the ground's colour
// (seen only where it crosses the Earth, never on the ground), growing to 2.5 times the dish and thinning to nothing by
// 0.45 s; then still to the next beat. The globe and its land never move
const CORE = { beat: 1.0, keys: [[0, null, 1, 1], [0.06, 0, 1.2, 1.1], [0.13, 0, 1.2, 1.1], [0.24, 0.75, 0.9, 0.95], [0.42, null, 1, 1]],
               ring: [0.04, 0.45], grow: 1.5, width: 0.05 };              // keys: time, depth (null: at rest), cap, driver
const easeOut = x => 1 - Math.pow(1 - clamp(x, 0, 1), 3);
function kickAt(t) {                                                         // [depth, cap, driver] t seconds into a beat
  const K = CORE.keys, rest = D.core.dish.depth, v = k => [k[1] === null ? rest : k[1], k[2], k[3]];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) {
    const f = (t - K[i - 1][0]) / (K[i][0] - K[i - 1][0]), e = i === 1 ? easeOut(f) : i === 4 ? easeOut(f) : smooth(f);
    const a = v(K[i - 1]), b = v(K[i]); return a.map((x, j) => x + (b[j] - x) * e); }
  return v(K[K.length - 1]);
}
function dishRing(ctx, f, depth) {                                          // core.py's ring(), y down, the radius 1
  const K = D.core.dish, [x, y] = K.at, d = [x, y, Math.sqrt(Math.max(0, 1 - x * x - y * y))];
  const L = Math.hypot(d[0], d[1]) || 1, u = [-d[1] / L, d[0] / L, 0], v = cross(d, u);
  const a = rad(K.ang), rr = Math.sin(a), c = Math.cos(a) - depth * rr * (1 - f * f), lt = rad(-D.core.lean), cl = Math.cos(lt), sl = Math.sin(lt);
  ctx.beginPath();
  for (let i = 0; i < 120; i++) { const t = TAU * i / 120, q = [0, 1].map(j => c * d[j] + f * rr * (Math.cos(t) * u[j] + Math.sin(t) * v[j]));
    const X = q[0] * cl - q[1] * sl, Y = q[0] * sl + q[1] * cl; i ? ctx.lineTo(X, -Y) : ctx.moveTo(X, -Y); }
  ctx.closePath();
}
let CP = null;
function corePaths() {                                                     // the figure's paths, made once (sea: the sphere
  if (CP) return CP;                                                         // and the land, filled even-odd, is the sea)
  const P = D.core, sea = new Path2D(P.sphere);
  if (P.land) sea.addPath(new Path2D(P.land));
  CP = { sphere: new Path2D(P.sphere), land: P.land ? new Path2D(P.land) : null, trench: P.trench ? new Path2D(P.trench) : null,
         cap: new Path2D(P.cap), sea };
  return CP;
}
function drawCoreKick(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground], P = D.core;
  corePaths();
  ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  const R = Math.min(W, H) * 0.3, tb = ((t % CORE.beat) + CORE.beat) % CORE.beat, [depth, capK, throwK] = kickAt(tb), [cx, cy] = P.centre;
  const about = (k, f) => { ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy); f(); ctx.restore(); };
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(R, R);
  ctx.fillStyle = P.sea; ctx.fill(CP.sphere);
  if (CP.land) { ctx.fillStyle = P.landCol; ctx.fill(CP.land, 'evenodd'); }
  if (CP.trench) { ctx.fillStyle = P.trenchCol; ctx.fill(CP.trench); }
  about(throwK, () => P.rings.forEach(([, col], i) => about(i === 2 ? capK : 1, () => { ctx.fillStyle = col; dishRing(ctx, P.fr[i], depth); ctx.fill(); })));
  ctx.save(); ctx.clip(CP.sphere);                                           // the ring of sound, knocked out of the globe
  for (const lag of [0, CORE.beat]) {
    const p = (tb + lag - CORE.ring[0]) / (CORE.ring[1] - CORE.ring[0]); if (p <= 0 || p >= 1) continue;
    const k = 1 + CORE.grow * easeOut(p);
    about(k, () => { ctx.strokeStyle = G.bg; ctx.lineWidth = CORE.width * (1 - p) / k; dishRing(ctx, 1, P.dish.depth); ctx.stroke(); }); }
  ctx.restore();
  ctx.restore();
  return 4 * CORE.beat;
}

// round 25, the planet (the owner: "it would be cool if the purple was a meteor, creates white cloud, disperses into
// black wisps, then the crater is visible. The water ripples on impact too. Then the purple meteor can stay in the
// core"). Round 26, drawn again as early Disney would have drawn it (the owner: "You gotta really spruce up that planet
// animation. Pixar quality baby. Or at least early Disney"), by the animators' principles. Staging and anticipation: a
// star twinkles where the meteor will come from; the meteor grows out of it and draws back, squashed. Arcs, slow in,
// squash and stretch: it falls on a bowed path, faster as it comes, stretched by its speed, its flame flickering and
// shedding sparks, and on the frame it strikes it splats flat. Timing: a starburst for two frames (one flash, well under
// three a second). Follow-through: the planet squashes along the blow and springs back past round and round again,
// knocked along the blow and back; a shock runs over the globe and the sea ripples, a light crest and a dark trough,
// the rings drawn on the sphere so they foreshorten toward the limb and wrap round it (solid drawing). Overlapping
// action: the cloud pops in puff by puff from its middle out, each past its size and back, and billows, shaded in two
// tones (Fog, lit from the upper left, and a cool shadow); it chars from its middle out, each puff through a beat of a
// middle tone to flat Smoke, and swells; and the smoke is eaten away from its middle out, each puff bitten from its
// inner side by a growing circle, so the crater shows first through a hole at the centre and the last of the smoke is
// crescents curling round it, thinning to nothing (no fades: early Disney's smoke goes by breaking up, and these are
// the mark's own circles); as it clears the crater springs open ring by ring, past its size and back, its bowl sinking
// past its depth, and the meteor drops into the core with a bounce, white-hot, cooling to violet. Round 25's thump is
// gone (the owner: "Drop it"). It plays in colour in every style: round 26 drew it in black and white too, in
// knock-outs, but the owner meant the still figure ("The black and white doesn't need to be animated"), so that is out.
// Times in seconds from the start; sizes of the planet's radius
// After its round 26 critic (critic/rounds/2026-10-16/brand-planet-r2.json): the meteor larger (0.085 to 0.12),
// launched on the glint (the wind-up at 0.24, not 0.34) and striking 0.1 s sooner (0.62), its fall eased in less (2.4
// to 1.8, so it is on its way by 0.43); five fat puffs round the cloud's edge, not eight small (they read as beads);
// the smoke eaten in 0.3 s, not 0.42, then a beat (`hold`) on the clean crater; the ripples to 0.9 rad over 0.55 s
// (1.3 over 0.85 traced the limb, a plate's rim) and the shock to 1.0 rad (1.95 doubled the outline)
const PLANET = { star: { at: 0.04, pop: 0.16, ting: 0.24, size: 0.15 },    // the twinkle: it pops in, glints, gives way
                 wind: { at: 0.24, dur: 0.1, back: 0.1 },                     // the ball grows out of it and draws back
                 hit: 0.62, from: [1.36, -0.98], bow: 0.14, ease: 1.8,       // the strike; the fall's start (from the core),
                 meteor: 0.12, stretch: 1.5, tail: 0.95, contact: 0.034,    // its bow and its ease in; the ball, its
                 flash: 0.06,                                                // stretch at full speed, its flame; the splat
                 squash: { k: 0.075, hz: 3.4, damp: 6.5 }, knock: { dist: 0.07, hz: 2.8, damp: 7.5 },
                 shock: { dur: 0.28, to: 1.0, width: 0.012 },                // (radians from the dish's axis)
                 ripples: { n: 3, gap: 0.15, dur: 0.55, to: 0.9, width: 0.024 },
                 cloud: { size: 0.5, pop: 0.15, stagger: 0.06, drift: 0.16, boil: 0.035 },
                 char: { start: 1.02, dur: 0.12, turn: 0.07 }, smoke: { after: 0.05, eat: 0.3, drift: 0.22, swirl: 0.9, hold: 0.12 },   // (each
                                                                             // puff is eaten from `after` it begins to char)
                 crater: { at: 1.15, pop: 0.2, stagger: 0.055, wob: 0.05, hz: 3.0, damp: 5, sink: 0.5 }, ember: { cool: 0.7 },
                 get end() { return this.char.start + this.char.dur + this.smoke.after + this.smoke.eat + this.smoke.hold; },
                 get last() { return Math.max(this.end, this.hit + 0.02 + (this.ripples.n - 1) * this.ripples.gap + this.ripples.dur,
                                              this.crater.at + 3 * this.crater.stagger + this.ember.cool); } };
const PUFFS = [[0.81, 0.22, 0.32], [0.07, 0.82, 0.34], [-0.79, 0.29, 0.31], [-0.58, -0.58, 0.33], [0.42, -0.73, 0.3],
               [0.42, 0.18, 0.4], [-0.08, 0.46, 0.38], [-0.44, -0.04, 0.4], [-0.02, -0.44, 0.38], [0.38, -0.28, 0.34],
               [0, 0, 0.46]];                                                // the cloud: circles (x, y, r) of its size, back to
                                                                             // front (five fat ones round the edge, unevenly
                                                                             // spaced, five inside, one in the middle on top)
const hash = (i, k) => { const v = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return v - Math.floor(v); };
const backOut = (x, s = 1.7) => { x = clamp(x, 0, 1) - 1; return 1 + (s + 1) * x * x * x + s * x * x; };   // past 1, back
const pip = (ctx, x, y, r) => { if (r > 0) { ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); } };
function planetPal() {                                                      // the Planet's colours (the cloud Fog and the
  const P = D.core, FOG = P.fog, SMOKE = P.smoke;                            // smoke Smoke, the line's clear white and black)
  return { sea: P.sea, land: P.landCol, crest: mixHex(P.sea, FOG, 0.6), trough: mixHex(P.sea, D.ink, 0.28), shock: FOG,
           rings: P.rings.map(r => r[1]), core: P.capCol, coreHot: mixHex(P.capCol, FOG, 0.8), cloud: FOG, shade: mixHex(FOG, P.sea, 0.3),
           smoke: SMOKE, flash: FOG, flashCore: mixHex(FOG, P.rings[2][1], 0.45),
           meteor: P.capCol, meteorHot: mixHex(P.capCol, FOG, 0.45), flame: mixHex(P.capCol, FOG, 0.42), star: P.capCol,
           spark: mixHex(P.capCol, FOG, 0.55) };
}
let FG = null;
function fallGeom() {                                                        // the meteor's arc (a quadratic, bowed up to
  if (FG) return FG;                                                         // the left of its chord), y down
  const Q = PLANET, [cx, cy] = D.core.centre, L = Math.hypot(...Q.from), n = [Q.from[1] / L, -Q.from[0] / L];
  const A = [cx + Q.from[0], cy + Q.from[1]], B = [cx, cy], C = [cx + Q.from[0] / 2 + n[0] * Q.bow * L, cy + Q.from[1] / 2 + n[1] * Q.bow * L];
  const at = u => [0, 1].map(j => (1 - u) * (1 - u) * A[j] + 2 * (1 - u) * u * C[j] + u * u * B[j]);
  const tan = u => [0, 1].map(j => 2 * (1 - u) * (C[j] - A[j]) + 2 * u * (B[j] - C[j]));
  const unit = v => { const l = Math.hypot(v[0], v[1]) || 1; return [v[0] / l, v[1] / l]; };
  const d0 = unit(tan(0));
  FG = { at, tan, unit, d0, end: unit(tan(1)), B, star: [A[0] + d0[0] * Q.wind.back, A[1] + d0[1] * Q.wind.back] };
  return FG;
}
function meteorAt(t) {                                                       // the ball at t: where, which way, its size,
  const Q = PLANET, g = fallGeom(), t0 = Q.wind.at + Q.wind.dur;             // its stretch (along and across its path),
  if (t < Q.wind.at || t >= Q.hit) return null;                              // how far along (u) and how fast (0 to 1)
  if (t < t0) { const w = (t - Q.wind.at) / Q.wind.dur, e = smooth(w), sq = 1 - 0.35 * Math.sin(Math.PI * w);   // winding up
    return { p: [g.star[0] - g.d0[0] * Q.wind.back * e, g.star[1] - g.d0[1] * Q.wind.back * e], d: g.d0, k: backOut(w * 1.7, 2),
             along: sq, across: 1 / Math.sqrt(sq), u: 0, sp: 0 }; }
  if (t >= Q.hit - Q.contact) return { p: g.B, d: g.end, k: 1, along: 0.5, across: 1.55, u: 1, sp: 1 };   // the splat
  const s = (t - t0) / (Q.hit - t0), u = Math.pow(s, Q.ease), tn = g.tan(u);
  const sp = Math.hypot(tn[0], tn[1]) * Math.pow(s, Q.ease - 1) / Math.hypot(...g.tan(1)), along = 1 + Q.stretch * sp;
  return { p: g.at(u), d: g.unit(tn), k: 1, along, across: 1 / Math.sqrt(along), u, sp };
}
function twinkle(ctx, t, pal) {                                              // a four-point sparkle, a lesser one across it
  const Q = PLANET, S = Q.star, g = fallGeom(), a = (t - S.at) / S.pop; if (a <= 0) return;
  const k = backOut(a, 2.2) * (1 - smooth((t - Q.wind.at) / (0.6 * Q.wind.dur))); if (k <= 1e-3) return;
  const b = Math.exp(-Math.pow((t - S.ting) / 0.05, 2)), R = S.size * k;    // b: the glint, its long rays reaching out
  const spark = (r, c) => { ctx.beginPath(); ctx.moveTo(0, -r); ctx.quadraticCurveTo(c, -c, r, 0); ctx.quadraticCurveTo(c, c, 0, r);
    ctx.quadraticCurveTo(-c, c, -r, 0); ctx.quadraticCurveTo(-c, -c, 0, -r); ctx.fill(); };
  ctx.save(); ctx.translate(g.star[0], g.star[1]); ctx.rotate(0.9 * (1 - smooth(a))); ctx.fillStyle = pal.star;
  spark(R * (1 + 0.55 * b), R * 0.12); ctx.rotate(Math.PI / 4); spark(R * 0.5, R * 0.08);
  ctx.fillStyle = pal.meteorHot; pip(ctx, 0, 0, R * 0.15);
  ctx.restore();
}
function flame(ctx, M, t, pal) {                                             // the meteor's flame: two ribbons tapering back
  const Q = PLANET, g = fallGeom(); if (M.sp < 0.03) return;                 // along its arc, flickering, light over dark
  const len = Q.tail * Math.pow(M.sp, 0.8), m = Q.meteor * M.across, N = 28;
  const ribbon = (frac, w0) => { const du = len * frac / Math.max(1e-3, Math.hypot(...g.tan(M.u))), L = [], R = [];
    for (let j = 0; j <= N; j++) { const s = j / N, u = Math.max(0, M.u - du * s), p = j ? g.at(u) : M.p, d = g.unit(g.tan(u));
      const w = w0 * Math.pow(1 - s, 0.85) * (1 + 0.16 * Math.sin(TAU * 2.2 * s - 38 * t)) / 2;
      L.push([p[0] - d[1] * w, p[1] + d[0] * w]); R.push([p[0] + d[1] * w, p[1] - d[0] * w]); }
    ctx.beginPath(); L.forEach(([x, y], j) => j ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); for (let j = N; j >= 0; j--) ctx.lineTo(...R[j]); ctx.closePath(); };
  ribbon(1, 2.3 * m); ctx.fillStyle = pal.flame; ctx.fill(); ribbon(0.6, 1.4 * m); ctx.fillStyle = pal.meteor; ctx.fill();
}
function sparks(ctx, t, pal) {                                               // sparks shed by the flame, drifting off and
  const Q = PLANET, g = fallGeom(), t0 = Q.wind.at + Q.wind.dur;             // shrinking away
  ctx.fillStyle = pal.spark;
  for (let k = 0; k < 8; k++) {
    const uk = 0.1 + 0.1 * k, a = (t - t0 - Math.pow(uk, 1 / Q.ease) * (Q.hit - t0)) / 0.22; if (a <= 0 || a >= 1) continue;
    const p = g.at(uk), d = g.unit(g.tan(uk)), off = (hash(k, 41) < 0.5 ? -1 : 1) * (0.05 + 0.06 * hash(k, 42)) * easeOut(a);
    pip(ctx, p[0] - d[1] * off, p[1] + d[0] * off + 0.04 * a * a, 0.022 * (0.6 + 0.6 * hash(k, 43)) * (1 - a));
  }
}
function ball(ctx, M, pal) {                                                 // the meteor, stretched along its path, its
  const m = PLANET.meteor * M.k;                                             // leading face hot
  ctx.save(); ctx.translate(M.p[0], M.p[1]); ctx.rotate(Math.atan2(M.d[1], M.d[0])); ctx.scale(M.along, M.across);
  ctx.fillStyle = pal.meteor; pip(ctx, 0, 0, m);
  ctx.fillStyle = pal.meteorHot; pip(ctx, m * 0.3, 0, m * 0.58);
  ctx.restore();
}
function capRing(ctx, th) {                                                  // the circle on the sphere th radians from the
  const K = D.core.dish, [x, y] = K.at, d = [x, y, Math.sqrt(Math.max(0, 1 - x * x - y * y))];   // dish's axis, its near
  const L = Math.hypot(d[0], d[1]) || 1, u = [-d[1] / L, d[0] / L, 0], v = cross(d, u);          // side only (y down)
  const lt = rad(-D.core.lean), cl = Math.cos(lt), sl = Math.sin(lt), c = Math.cos(th), s = Math.sin(th);
  ctx.beginPath(); let pen = false;
  for (let i = 0; i <= 160; i++) {
    const a = TAU * i / 160, q = [0, 1, 2].map(j => c * d[j] + s * (Math.cos(a) * u[j] + Math.sin(a) * v[j]));
    if (q[2] < 0) { pen = false; continue; }
    const X = q[0] * cl - q[1] * sl, Y = q[0] * sl + q[1] * cl; pen ? ctx.lineTo(X, -Y) : ctx.moveTo(X, -Y); pen = true;
  }
}
function planetWaves(ctx, since, pal, C) {                                  // the ripples on the sea, and the shock
  const Q = PLANET, th0 = rad(D.core.dish.ang), R = Q.ripples, S = Q.shock;
  ctx.save(); ctx.clip(C.sea, 'evenodd'); ctx.lineCap = 'round';
  for (let i = 0; i < R.n; i++) {
    const p = (since - 0.02 - i * R.gap) / R.dur; if (p <= 0 || p >= 1) continue;
    const th = th0 + (R.to - th0) * (1 - (1 - p) * (1 - p)), w = R.width * (1 - p);
    ctx.strokeStyle = pal.trough; ctx.lineWidth = 0.7 * w; capRing(ctx, th - 0.045); ctx.stroke();
    ctx.strokeStyle = pal.crest; ctx.lineWidth = w; capRing(ctx, th); ctx.stroke();
  }
  ctx.restore();
  const p = since / S.dur; if (p <= 0 || p >= 1) return;
  const th = th0 + (S.to - th0) * easeOut(p);
  ctx.save(); ctx.clip(C.sphere); ctx.lineCap = 'round'; ctx.lineWidth = S.width * Math.pow(1 - p, 1.5);
  ctx.strokeStyle = pal.shock; capRing(ctx, th); ctx.stroke();
  ctx.restore();
}
function planetCrater(ctx, t, pal) {                                         // the crater springing open ring by ring, and
  const P = D.core, Q = PLANET.crater, x = t - Q.at; if (x <= 0) return;    // the meteor dropping into its core
  const depth = P.dish.depth * (1 + Q.sink * Math.exp(-6 * x) * Math.cos(TAU * 2.2 * x));
  const grow = i => { const y = x - i * Q.stagger; return y <= 0 ? 0 : backOut(y / Q.pop, 2) * (1 + Q.wob * Math.exp(-Q.damp * y) * Math.sin(TAU * Q.hz * y)); };
  P.rings.forEach((r, i) => { const k = grow(i); if (k > 0) { ctx.fillStyle = pal.rings[i]; dishRing(ctx, P.fr[i] * k, depth); ctx.fill(); } });
  const y = x - 3 * Q.stagger; if (y <= 0) return;
  const heat = 1 - smooth(y / PLANET.ember.cool), k = 1 + 0.55 * Math.exp(-7 * y) * Math.cos(TAU * 2.6 * y);
  ctx.fillStyle = mixHex(pal.core, pal.coreHot, heat); dishRing(ctx, P.capF * k, depth); ctx.fill();
}
function planetCloud(ctx, t, since, pal, C) {                                // the cloud, its char and its smoke
  const P = D.core, Q = PLANET, K = Q.cloud, Ch = Q.char, Sm = Q.smoke, [cx, cy] = P.centre, S = K.size;
  const puffs = PUFFS.map(([x, y, r], i) => {                                // each puff chars as the front from the middle
    const d = Math.hypot(x, y), t0 = Ch.start + Ch.dur * Math.pow(d / 0.95, 0.8), c = clamp((t - t0) / Ch.turn, 0, 1);   // reaches it
    const e = smooth((t - t0 - Sm.after) / Sm.eat), out = S * (1 + K.drift * easeOut(since / 0.7) + Sm.drift * e);       // (a beat of a
    const rr = r * S * backOut((since - 0.012 - K.stagger * d) / K.pop, 1.8) * (1 + K.boil * Math.sin(TAU * 1.7 * since + TAU * hash(i, 3)))   // middle tone,
               * (1 + 0.12 * Math.sin(Math.PI * c));                                                     // and a swell), then is
    return { i, d, c, e, r: rr, x: cx + x * out, y: cy + y * out, th: d > 1e-6 ? Math.atan2(y, x) : 0 }; });   // eaten away
  const dark = h => h.c >= 0.5, tone = (a, b, h) => mixHex(a, b, smooth(h.c));
  const white = puffs.filter(h => h.r > 1e-4 && !dark(h)), smoke = puffs.filter(h => h.r > 1e-4 && dark(h) && h.e < 1);
  ctx.save(); ctx.clip(C.sphere);
  white.forEach(h => {                                                       // lit from the upper left: its shadow, then its
    ctx.fillStyle = tone(pal.shade, pal.smoke, h); pip(ctx, h.x, h.y, h.r);  // lit part over it
    ctx.fillStyle = tone(pal.cloud, pal.smoke, h); pip(ctx, h.x - 0.1 * h.r, h.y - 0.12 * h.r, 0.86 * h.r); });
  if (smoke.length) {                                                        // the smoke, flat, one mass, eaten from the middle
    const sg = h => hash(h.i, 6) < 0.5 ? -1 : 1;                             // out: each puff by its own circle, biting in from
    const eater = h => { const a = h.th + Math.PI + sg(h) * Sm.swirl * h.e, mid = h.d < 1e-6;   // outside its inner side and
      const o = mid ? 0 : h.r * (1.5 - 0.95 * h.e), R = mid ? 1.1 * h.r * h.e : h.r * (0.5 + 1.1 * h.e);   // growing over it, so
      return [h.x + Math.cos(a) * o, h.y + Math.sin(a) * o, R]; };                                     // it thins to a crescent
    const bitten = (h, draw) => { const [x, y, R] = eater(h); ctx.save();                              // on its outer side,
      if (R > 0) { const p = new Path2D(); p.rect(-3, -3, 6, 6); p.arc(x, y, R, 0, TAU); ctx.clip(p, 'evenodd'); }   // curling as
      draw(); ctx.restore(); };                                                                        // it thins
    smoke.forEach(h => bitten(h, () => { ctx.fillStyle = tone(pal.cloud, pal.smoke, h); pip(ctx, h.x, h.y, h.r); })); }
  ctx.restore();
}
function planetFlash(ctx, since, pal) {                                      // the starburst: two frames, the second smaller
  const [cx, cy] = D.core.centre, R = 0.5 * (since < PLANET.flash / 2 ? 1 : 0.72);
  const star = (R, n, inner, turn) => { ctx.beginPath();
    for (let i = 0; i < 2 * n; i++) { const a = TAU * i / (2 * n) + turn, r = i % 2 ? R * inner : R * (0.8 + 0.4 * hash(i, 31));
      i ? ctx.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r) : ctx.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); }
    ctx.closePath(); };
  star(R, 9, 0.48, 0.2); ctx.fillStyle = pal.flash; ctx.fill();
  star(0.55 * R, 9, 0.5, 0.55); ctx.fillStyle = pal.flashCore; ctx.fill();
}
function drawPlanet(ctx, V, t, style, G) {
  const P = D.core, Q = PLANET, C = corePaths(), pal = planetPal(), since = t - Q.hit, ad = fallGeom().end;
  ctx.save(); ctx.translate(V.cx, V.cy); ctx.scale(V.R, V.R);
  ctx.save();
  if (since > 0) {                                                           // knocked along the blow, and squashed along it
    const kn = Q.knock.dist * Math.exp(-Q.knock.damp * since) * Math.sin(TAU * Q.knock.hz * since);   // (and stretched across),
    const sq = Q.squash.k * Math.exp(-Q.squash.damp * since) * Math.cos(TAU * Q.squash.hz * since);   // each on a damped spring
    const sx = 1 - sq, sy = 1 + 0.6 * sq, [a, b] = ad;
    ctx.translate(a * kn, b * kn);
    ctx.transform(1 + (sx - 1) * a * a + (sy - 1) * b * b, (sx - sy) * a * b, (sx - sy) * a * b, 1 + (sx - 1) * b * b + (sy - 1) * a * a, 0, 0);
  }
  ctx.fillStyle = pal.sea; ctx.fill(C.sphere);
  if (C.land) { ctx.fillStyle = pal.land; ctx.fill(C.land, 'evenodd'); }
  if (since > 0) {
    planetWaves(ctx, since, pal, C);
    planetCrater(ctx, t, pal);
    planetCloud(ctx, t, since, pal, C);
    if (since < Q.flash) planetFlash(ctx, since, pal);
  }
  ctx.restore();
  sparks(ctx, t, pal);                                                       // the sky: the twinkle, the sparks, the meteor
  if (t < Q.wind.at + Q.wind.dur) twinkle(ctx, t, pal);
  const M = meteorAt(t);
  if (M) { flame(ctx, M, t, pal); ball(ctx, M, pal); }
  ctx.restore();
}
function mixHex(a, b, k) {                                                   // two hex colours mixed, k of the way to b
  const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), A = p(a), B = p(b);
  return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, '0')).join('');
}
function drawPlanetLoop(ctx, W, H, t, o) {                                  // the planet struck, looped, for the page
  const G = GROUNDS[o.ground]; ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  const T = PLANET.last + 1.2; drawPlanet(ctx, view(W, H, W / 2, H / 2, Math.min(W, H) * 0.3), ((t % T) + T) % T, 'discs', G);
  return 2 * T;
}

const SCENES = { ident: drawIdent, loader: drawLoader, cursor: drawCursor, coin: drawCoin, kick: drawKickLoop, core: drawCoreKick,
                 planet: drawPlanetLoop };

function fit(cv) {
  const dpr = Math.min(2, window.devicePixelRatio || 1), r = cv.getBoundingClientRect();
  const w = Math.max(1, Math.round(r.width * dpr)), h = Math.max(1, Math.round(r.height * dpr));
  if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
  const ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { ctx, W: r.width, H: r.height };
}

// capture: one frame of one scene, full window, for the videos
window.__frame = (scene, t, o) => {
  document.body.classList.add('capture');
  const cv = document.getElementById('cap'), { ctx, W, H } = fit(cv);
  if (scene === 'cursor') return drawCursor(ctx, W, H, t, o, tt => ghost(tt, W, H));
  return SCENES[scene](ctx, W, H, t, o);
};

if (!location.hash.startsWith('#capture')) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const state = { kind: 'gyro', style: 'discs', ground: 'paper', t0: null };
  const CAPS = {
    printer: 'Printer: a head shuttles across and back, a band lower each pass, and leaves the finished globe in its wake.',
    gyro: 'Gyroscope: the globe spins half a turn on its axis like a gyroscope\'s rotor, slowing until it rests, whole and upright. Then it leans to the Earth\'s 23.4 degrees, a little past and back.',
    kick: 'Kick: seen from above the pole, the globe is a speaker: rings round one centre, the meridians its spokes. It kicks twice, then tips down to the Earth\'s tilt.',
    coin: 'Coin: it spins on its edge as a real coin does, slowing a little, a new face each half turn (never more than three flashes a second): the six colours round the colour wheel, yellow to green. The globe comes round, the coin tips over and rolls on its rim, wobbling faster the lower it leans, as Euler\'s disk does, and lands face up, the globe upright; then it leans.',
    roll: 'Roll: the globe rolls in from the right like a ball, turning as it goes, slows to a stop and rocks back into its lean.',
    rise: 'Earthrise: the whole globe rises from behind a horizon, slowing as it clears it; then it tilts.',
    download: 'Download: the globe arrives as a picture did over a modem in 1999, an interlaced GIF: coarse blocks at once, then each pass finer, sweeping down, until it is sharp; then it tilts.',
    open: 'Open: the globe begins as the flat globe icon, each disc edge on, a line. Each turns about its line and opens into its disc, a beat after the last; then the globe tilts.',
    iris: 'Iris: the finished globe, still and upright, opens out of its own centre in a circle, as a late-90s circle wipe; then it leans.',
    planet: 'Planet: a star twinkles; the meteor grows out of it, draws back and falls on an arc, stretching as it speeds up, and splats on the North Atlantic. A starburst for two frames; the Earth squashes and springs back; a shock runs over it and the sea ripples. A white cloud pops up puff by puff, chars to black from the middle out and is eaten away into curling crescents, and the crater springs open, the meteor dropping into its core, white-hot, cooling to violet.' };
  const capText = document.getElementById('cap-text'), screen = document.getElementById('screen');
  function segs(id, key) {
    const el = document.getElementById(id);
    if (!el) return;                                                   // round 27: the ident parked, off the page
    el.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
      el.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      state[key] = b.dataset.v; state.t0 = performance.now(); capText.textContent = CAPS[state.kind];
      screen.style.background = GROUNDS[state.ground].bg; });
  }
  segs('kind', 'kind'); segs('style', 'style'); segs('ground', 'ground'); if (capText) capText.textContent = CAPS.gyro;
  const replay = document.getElementById('replay'); if (replay) replay.onclick = () => { state.t0 = performance.now(); };
  // the cursor: the pointer's path, kept a moment, so each colour can be where the circle was a beat ago
  const pad = document.getElementById('pad'), hist = []; let last = -1e9;
  pad.addEventListener('pointermove', e => { const r = pad.getBoundingClientRect(), now = performance.now() / 1000;
    if (now - last > 1.2) hist.length = 0;
    hist.push([now, e.clientX - r.left, e.clientY - r.top]); last = now;
    while (hist.length > 2 && hist[1][0] < now - 1) hist.shift(); });
  function at(tt) {
    if (!hist.length) return [0, 0];
    if (tt <= hist[0][0]) return [hist[0][1], hist[0][2]];
    for (let i = hist.length - 1; i > 0; i--) if (hist[i - 1][0] <= tt) {
      const [ta, xa, ya] = hist[i - 1], [tb, xb, yb] = hist[i], f = clamp((tt - ta) / Math.max(1e-6, tb - ta), 0, 1);
      return [xa + (xb - xa) * f, ya + (yb - ya) * f]; }
    return [hist.at(-1)[1], hist.at(-1)[2]];
  }
  // each panel runs only while it is on screen, and the ident starts when it first comes into view, then loops
  const vis = new Map(); const io = new IntersectionObserver(es => es.forEach(e => vis.set(e.target, e.isIntersecting)));
  ['stage', 'load-night', 'load-paper', 'cursor', 'kickloop', 'meteor'].forEach(id => { const el = document.getElementById(id); if (el) io.observe(el); });
  const on = id => vis.get(document.getElementById(id)) === true;
  function tick(now) {
    const s = now / 1000;
    if (on('stage')) { const { ctx, W, H } = fit(document.getElementById('stage'));
      if (state.t0 === null) state.t0 = now;
      const end = identTimes(state.kind).end, t = (now - state.t0) / 1000;
      if (t > end + 0.8) state.t0 = now;                                     // a pause, then again
      drawIdent(ctx, W, H, reduce ? end : Math.min(t, end), state); }
    for (const g of ['night', 'paper']) if (on('load-' + g)) { const { ctx, W, H } = fit(document.getElementById('load-' + g));
      drawLoader(ctx, W, H, reduce ? LOAD.go : s, { ground: g }); }
    if (on('cursor')) { const { ctx, W, H } = fit(document.getElementById('cursor'));
      const live = s - last < 2.5; drawCursor(ctx, W, H, s, { ground: 'night' }, live ? at : (tt => ghost(tt, W, H))); }
    if (on('kickloop')) { const { ctx, W, H } = fit(document.getElementById('kickloop'));
      drawCoreKick(ctx, W, H, reduce ? 0.3 : s, { ground: 'night' }); }
    if (on('meteor')) { const { ctx, W, H } = fit(document.getElementById('meteor'));
      drawPlanetLoop(ctx, W, H, reduce ? PLANET.end : s, { ground: 'paper' }); }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
</script>
"""


# round 27 (the owner, of the idents and the Planet: "Park them"): the page leaves out what is between <!--PARKED-->
# and <!--/PARKED--> (the ident player, the Death Star's kick and the Planet's loop); False puts them back
PARKED = True


def page():
    body = re.sub(r'\s*<!--PARKED-->.*?<!--/PARKED-->', '', PAGE, flags=re.S) if PARKED else PAGE
    return body.replace('__RAILS__', rails_html()).replace('__CORE__', core_html()).replace('__THEME__', theme_html()).replace('__DATA__', json.dumps(data(), separators=(',', ':')))


def standalone():
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, '
            'initial-scale=1, viewport-fit=cover"></head><body>\n' + page() + '\n</body></html>\n')


# round 25: the seven idents (the Coin, the Gyroscope, Earthrise, Open, Iris, Roll and Download) in the discs and the acrylic, each
# on paper and on night, and in the lines; the Planet in colour on both; the Death Star
# kicking; the loader and the cursor as round 22 made them (round 23's printer, kick and tubes MP4s stay)
SCENE_SET = [('ident', dict(kind=k, style=st, ground=g)) for k in ('coin', 'gyro', 'rise', 'open', 'iris', 'roll', 'download')
             for st, g in (('discs', 'paper'), ('discs', 'night'), ('acrylic', 'paper'), ('acrylic', 'night'), ('even', 'paper'))] + [
             ('ident', dict(kind='planet', style='discs', ground='paper')), ('ident', dict(kind='planet', style='discs', ground='night')),
             ('core', dict(ground='night')), ('core', dict(ground='paper')),
             ('loader', dict(ground='night')), ('loader', dict(ground='paper')), ('cursor', dict(ground='night'))]


def video(out_dir, scene, opts, fps=30, w=1280, h=720, loops=1):
    """One scene to an MP4, frame by frame through the page's __frame."""
    tmp = tempfile.mkdtemp(prefix='earth-')
    html = os.path.join(tmp, 'earth.html')
    open(html, 'w').write(standalone())
    js = os.path.join(tmp, 'cap.js')
    o = json.dumps(opts)
    open(js, 'w').write(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {w}, height: {h} }}, deviceScaleFactor: 1 }});
  await p.goto('file://{html}#capture', {{ waitUntil: 'load' }});
  const end = await p.evaluate(([s, o]) => window.__frame(s, 0, o), ['{scene}', {o}]);
  const n = Math.round(end * {loops} * {fps});
  for (let i = 0; i < n; i++) {{
    await p.evaluate(([s, t, o]) => window.__frame(s, t, o), ['{scene}', i / {fps}, {o}]);
    await p.screenshot({{ path: '{tmp}/f' + String(i).padStart(4, '0') + '.png' }});
  }}
  await b.close(); console.log(n);
}})();
""")
    r = subprocess.run(['node', js], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])
    parts = [scene, opts.get('kind'), opts.get('style') if scene == 'ident' else None, opts['ground']]
    name = 'earth-' + '-'.join(x for x in parts if x) + '.mp4'
    mp4 = os.path.join(out_dir, name)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', mp4], check=True)
    shutil.rmtree(tmp)
    return mp4


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--fragment', help='also write the page as an Artifact body to this path')
    ap.add_argument('--video', action='store_true', help='also write an MP4 of each scene')
    ap.add_argument('--only', nargs='*', default=[], help='with --video, only the scenes named, or whose options mention one of these (e.g. core, gyro, acrylic)')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    written = []
    for style in ('lines', 'even', 'discs', 'acrylic'):                 # (round 23's tubes stay as they were)
        sets = [('multi', RING), ('ink', RING), ('black', INK), ('white', WHITE)] + [(n.lower(), c) for n, c in zip(NAMES, HUES)]
        if style == 'acrylic':                                           # round 27: every speaker its own, Fog and Smoke too
            sets += [('fog', _C['Fog']), ('smoke', _C['Smoke'])]
        for tag, cols in sets:
            f = f'earth-{style}-{tag}.svg'                                   # (round 25: 'ink', the multicolour on ink)
            open(os.path.join(OUT, f), 'w').write(mark_svg(style, cols, label=f'EARF globe, {style}, {tag}',
                                                           ground='night' if tag in ('white', 'ink') else 'paper'))
            written.append(f)
    for g, word, bg in (('paper', INK, PAPER), ('ink', WHITE, NIGHT)):
        open(os.path.join(OUT, f'earth-lockup-{g}.svg'), 'w').write(lockup_svg('discs', RING, word, bg=bg, ground='night' if g == 'ink' else 'paper'))
    open(os.path.join(OUT, 'earth-lockup-black.svg'), 'w').write(lockup_svg('discs', INK, INK))
    open(os.path.join(OUT, 'earth-lockup-white.svg'), 'w').write(lockup_svg('discs', WHITE, WHITE, ground='night'))
    json.dump(outlines(), open(os.path.join(OUT, 'earth-outlines.json'), 'w'), separators=(',', ':'))   # round 24: for product.py
    open(os.path.join(OUT, 'earth.html'), 'w').write(standalone())
    if a.fragment:
        open(a.fragment, 'w').write(page())
    print(f'brand/earth.html, {len(written)} marks, 4 lockups')
    if a.video:
        for scene, opts in SCENE_SET:
            if a.only and not any(w == scene or w in json.dumps(opts) for w in a.only):
                continue
            print(os.path.relpath(video(OUT, scene, opts, loops=2 if scene in ('loader', 'core') else 1), HERE))


if __name__ == '__main__':
    main()
