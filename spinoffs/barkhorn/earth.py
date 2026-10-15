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
  23.4 degrees, as the Earth's does and a desk globe's stand holds it, and tipped 22 degrees toward us, so the
  parallels open into ovals and the far side shows through behind the near. Six rings, one for each colour Cloud,
  drawn in spectrum order: the parallels warm, north to south (Flare, Dust, Acid), the meridians cool, west to east
  (Poison, Ice, Haze). Nothing black or white is in it; Smoke and Fog are the black-only and white-only marks.
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
import argparse, json, math, os, shutil, subprocess, sys, tempfile

import numpy as np
from shapely.geometry import LineString, MultiLineString, Point, Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import marks as M                                        # noqa: E402
import icons as IC                                       # noqa: E402

OUT = os.path.join(HERE, 'brand')
LEAN, ELEV, LAT = 23.44, 22.0, 40.0                      # the axis's lean (the Earth's), its tip toward us, the parallels
MERIDIANS = (30.0, 90.0, 150.0)                          # the meridians' longitudes at rest (90 faces us: the rim)
W_LINE, W_DEPTH, SEAM = 0.075, 0.42, 0.035               # of the globe's radius: the line, the far line's share, the seam
CLOUDS = [(name, colour) for key, line, num, name, colour in M.SPEAKERS if line == 'Cloud']
HUES = [c for n, c in CLOUDS if n not in ('Fog', 'Smoke')]          # Flare Dust Acid Poison Ice Haze, ring by ring
NAMES = [n for n, c in CLOUDS if n not in ('Fog', 'Smoke')]
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


def basis(lean=LEAN, elev=ELEV):
    """The globe's axis and its longitude 0 and 90 directions on screen (x right, y up, z toward us)."""
    t, e = math.radians(lean), math.radians(elev)

    def rot(v):
        x, y, z = v
        y, z = y * math.cos(e) - z * math.sin(e), y * math.sin(e) + z * math.cos(e)
        return np.array([x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t), z])
    return rot((0, 1, 0)), rot((0, 0, 1)), rot((1, 0, 0))


def rings(spin=0.0, n=360):
    """The six rings, each a closed loop of points with its disc's plane (n . p = d), centre and radius."""
    a, e1, e2 = basis()
    s = np.linspace(0, 2 * math.pi, n, endpoint=False)
    out = []
    for phi in (LAT, 0.0, -LAT):
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


def facets(spin=0.0):
    """Each disc's visible part: its own oval less every other disc's oval where that disc is nearer (two planes'
    depths differ linearly across the screen, so where one is nearer is a half-plane)."""
    rs = rings(spin)
    E = [Polygon(g['pts'][:, :2]).buffer(0) for g in rs]
    out = []
    for i, gi in enumerate(rs):
        vis, ni = E[i], gi['n']
        if abs(ni[2]) < 1e-6:
            out.append(Polygon()); continue
        for j, gj in enumerate(rs):
            nj = gj['n']
            if j == i or abs(nj[2]) < 1e-6:
                continue
            A = -nj[0] / nj[2] + ni[0] / ni[2]
            B = -nj[1] / nj[2] + ni[1] / ni[2]
            C = gj['d'] / nj[2] - gi['d'] / ni[2]
            m = math.hypot(A, B)
            if m < 1e-12:                                # parallel planes: one is nearer everywhere
                if C > 0:
                    vis = vis.difference(E[j])
                continue
            ux, uy, c0 = A / m, B / m, -C / m
            px, py, tx, ty, big = ux * c0, uy * c0, -uy, ux, 4.0
            half = Polygon([(px + tx * big, py + ty * big), (px - tx * big, py - ty * big),
                            (px - tx * big + ux * big, py - ty * big + uy * big), (px + tx * big + ux * big, py + ty * big + uy * big)])
            vis = vis.difference(E[j].intersection(half))
        out.append(vis)
    return out


def discs_body(colours, spin=0.0, seam=SEAM, least=0.004):
    """The discs, each facet drawn back from its edges by half a seam, so the ground shows between them; slivers
    smaller than `least` of the globe's area left out (at a mark's sizes they read as specks on its edge)."""
    out = ''
    for i, f in enumerate(facets(spin)):
        g = f.buffer(-seam / 2, join_style=2, mitre_limit=4).simplify(0.001)
        parts = [q for q in getattr(g, 'geoms', [g]) if q.area > least * math.pi]
        if parts:
            out += f'<path d="{" ".join(_poly_d(q) for q in parts)}" fill="{colours[i]}" fill-rule="evenodd"/>'
    return out


def mark_svg(style, colours, size=None, bg=None, label='EARF', ground='paper'):
    """style: lines (the far halves lighter: the mark), even (every line one weight), discs, or tubes (round 23, on
    `ground`, paper or night); colours: six (a ring each) or one."""
    if isinstance(colours, str):
        colours = [colours] * 6
    if style == 'tubes':
        body, e = tubes_body(colours, ground), 1 + W_TUBE / 2 + 0.02
    else:
        body = discs_body(colours) if style == 'discs' else lines_body(colours, depth=style == 'lines')
        e = 1 + W_LINE / 2
    wh = f' width="{size}" height="{size}"' if size else ''
    ground = f'<rect x="{-e:.4f}" y="{-e:.4f}" width="{2 * e:.4f}" height="{2 * e:.4f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.4f} {-e:.4f} {2 * e:.4f} {2 * e:.4f}"{wh} role="img" '
            f'aria-label="{label}"><title>{label}</title>{ground}{body}</svg>')


def _prim_shape(p):
    if p[0] == 'circle':
        return Point(p[1], p[2]).buffer(p[3], resolution=96)
    if p[0] == 'rect':
        return Polygon([(p[1], p[2]), (p[3], p[2]), (p[3], p[4]), (p[1], p[4])])
    return Polygon(p[1:])


def letters():
    """EARF's four letters, each its primitives merged into one solid shape (y down, cap height 300), so the wordmark
    prints in one colour; the R's bowl a solid circle, the globe's own shape."""
    groups = [M.WORDMARK[0:4], M.WORDMARK[4:7], M.WORDMARK[7:10], M.WORDMARK[10:13]]
    out = []
    for g in groups:
        u = unary_union([_prim_shape(p) for p in g])
        out.append(' '.join('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in np.array(r.coords)) + 'Z'
                            for poly in getattr(u, 'geoms', [u]) for r in [poly.exterior] + list(poly.interiors)))
    return out


def lockup_svg(style, colours, word, size=None, bg=None, ground='paper'):
    """The globe beside EARF, its diameter one and a half cap heights, centred on the letters."""
    k = 225 / ((1 + W_TUBE / 2 + 0.02) if style == 'tubes' else (1 + W_LINE / 2))
    inner = mark_svg(style, colours, ground=ground)
    inner = inner[inner.index('</title>') + 8:inner.rindex('</svg>')]
    vw, vh, gap = 450 + 110 + M.WORDMARK_W, 450, 110
    wh = f' width="{size * vw / vh:.0f}" height="{size}"' if size else ''
    ground = f'<rect x="-40" y="-40" width="{vw + 80}" height="{vh + 80}" fill="{bg}"/>' if bg else ''
    vb = '-40 -40 {} {}'.format(vw + 80, vh + 80) if bg else f'0 0 {vw} {vh}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh} role="img" aria-label="EARF"><title>EARF</title>'
            f'{ground}<g transform="translate(225 225) scale({k:.4f})">{inner}</g>'
            f'<g transform="translate({450 + gap} 75)" fill="{word}">'
            + ''.join(f'<path d="{d}"/>' for d in letters()) + '</g></svg>')


def data():
    return dict(lean=LEAN, elev=ELEV, lat=LAT, mer=list(MERIDIANS), w=W_LINE, wDepth=W_DEPTH, seam=SEAM, hues=HUES, wTube=W_TUBE, tube=TUBE,
                names=NAMES, paper=PAPER, ink=INK, night=NIGHT, white=WHITE, letters=letters(), wordW=M.WORDMARK_W)


RAILS = [('Black only', 'paper', lambda: INK), ('White only', 'night', lambda: WHITE),
         ('One colour', 'paper', lambda: HUES[4]), ('Multicolour', 'paper', lambda: HUES),
         ('Multicolour on ink', 'night', lambda: HUES)]


def rails_html():
    """The guide rails: each style in black only, white only, one colour and multicolour, and the singles."""
    rows = ''
    for style, title in (('even', 'Lines'), ('tubes', 'Tubes'), ('discs', 'Discs')):
        cells = ''.join(f'<figure class="rail {g}">{mark_svg(style, f(), label=f"{title}, {t.lower()}", ground=g)}'
                        f'<figcaption>{t}</figcaption></figure>' for t, g, f in RAILS)
        singles = ''.join(f'<span class="one" title="{n}">{mark_svg(style, c, label=f"{title} in {n}")}</span>'
                          for n, c in zip(NAMES, HUES))
        rows += (f'<div class="railrow"><h3>{title}</h3><div class="rails">{cells}</div>'
                 f'<div class="singles"><span class="lab">Each Cloud in its own colour</span>{singles}</div></div>')
    locks = (f'<figure class="lock paper">{lockup_svg("even", HUES, INK)}<figcaption>Lockup on paper</figcaption></figure>'
             f'<figure class="lock night">{lockup_svg("even", HUES, WHITE)}<figcaption>On ink</figcaption></figure>'
             f'<figure class="lock paper">{lockup_svg("discs", INK, INK)}<figcaption>Black only, discs</figcaption></figure>'
             f'<figure class="lock night">{lockup_svg("even", WHITE, WHITE)}<figcaption>White only</figcaption></figure>'
             f'<figure class="lock paper">{lockup_svg("tubes", HUES, INK)}<figcaption>Tubes on paper</figcaption></figure>'
             f'<figure class="lock night">{lockup_svg("tubes", HUES, WHITE, ground="night")}<figcaption>Tubes on ink</figcaption></figure>')
    return rows + f'<div class="locks">{locks}</div>'


# the line's name, three ways (the owner: "Atmosphere is cool, but open to other earth themes. Elements was another
# idea I had"), and a fourth: the same colours as chemical elements, numbered by their atomic numbers
THEMES = [
    ('Clouds', 'Now', 'Cloud 05 &middot; Ice', 'Things in the sky. The cloud mark stays the line&rsquo;s sign, with the '
     'eight icons under it.', None),
    ('Atmosphere', 'Wider', 'Atmosphere 05 &middot; Ice', 'The same eight names, as what the air holds: light (Flare, Haze), '
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
  .seg button, .btn { padding: 10px 10px } }
body.capture { padding: 0; overflow: hidden } body.capture main { display: none }
#cap { display: none } body.capture #cap { display: block; position: fixed; inset: 0; width: 100vw; height: 100vh }
</style>
<main>
  <header>
    <div class="eyebrow">EARF &middot; Round 23 &middot; the globe</div>
    <h1>The globe arrives four ways, and the Clouds get icons</h1>
    <p class="lede">The same 3D Earth: three parallels and three meridians on the Earth's 23.4&deg; tilt, each ring one of
      the six colour Clouds, in even lines, as acrylic tubes or as discs. It is no longer drawn. A printer head lays it down band by band,
      two gyroscope rings spin into it, it kicks like a speaker seen from above, or a spinning coin deals it out. Each
      takes about two seconds before EARF types in.</p>
  </header>

  <section class="win" aria-label="The ident">
    <div class="bar"><i style="background:#D2382F"></i><i style="background:#E9B320"></i><i style="background:#4F7F3A"></i><b>earf.world &mdash; ident</b></div>
    <div class="screen" id="screen"><canvas id="stage" aria-label="The EARF globe drawn ring by ring"></canvas></div>
    <div class="controls">
      <div class="seg" id="kind" role="group" aria-label="Ident">
        <button aria-pressed="true" data-v="printer">Printer</button><button aria-pressed="false" data-v="gyro">Gyroscope</button><button aria-pressed="false" data-v="kick">Kick</button><button aria-pressed="false" data-v="coin">Coin</button>
      </div>
      <div class="seg" id="style" role="group" aria-label="Style">
        <button aria-pressed="true" data-v="even">Lines</button><button aria-pressed="false" data-v="tubes">Tubes</button><button aria-pressed="false" data-v="discs">Discs</button>
      </div>
      <div class="seg" id="ground" role="group" aria-label="Ground">
        <button aria-pressed="true" data-v="paper">Paper</button><button aria-pressed="false" data-v="night">Ink</button>
      </div>
      <button class="btn" id="replay">Replay</button>
    </div>
    <p class="cap" id="cap-text"></p>
  </section>

  <section class="win" aria-label="Guide rails">
    <div class="bar"><b>Guide rails &mdash; white only, black only, one colour, multicolour</b></div>
    __RAILS__
  </section>

  <section class="win" aria-label="Theme">
    <div class="bar"><b>Theme &mdash; an icon for each Cloud, from the marks&rsquo; own circles, bars and triangles</b></div>
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
    <div class="win">
      <div class="bar"><b>Kick, looped &mdash; for the speakers</b></div>
      <div class="coin" style="background:#121114"><canvas id="kickloop" aria-label="The globe from above the pole kicking like a speaker"></canvas></div>
    </div>
  </section>

  <section class="win" aria-label="Notes">
    <div class="bar"><b>Notes</b></div>
    <div class="notes">
      <h3>Why it reads as the Earth</h3>
      <ul>
        <li>The axis leans 23.4&deg;, as the Earth's does and as a desk globe's stand holds it. It also tips 22&deg; toward you, so the parallels open into ovals and the far halves show behind the near ones.</li>
        <li>The parallels are warm, north to south: Flare, Dust, Acid. The meridians are cool: Poison, Ice, Haze. Ice is the meridian facing you, so the globe's outline is blue.</li>
        <li>Lines are even, every line one weight, the far halves under the near. Round 22's lighter far halves (in <code>brand/earth-lines-*.svg</code>) remain for one colour at small sizes, where even lines tangle.</li>
        <li>Seen from above the pole, the same rings are a speaker: rings round one centre, with the meridians as spokes. The Kick uses that view, and the looped kick could mark the speakers themselves.</li>
        <li>Tubes: each ring a tube of tinted acrylic, faint through the middle and deeper along its walls, with a highlight toward the light. On paper the tint darkens what is behind it, as coloured acrylic does; on ink it glows. Where two rings cross, one shows through the other, and the far halves are at half strength so the near side reads in front. It is for screens and large sizes, like the animation; the flat lines stay the mark for print.</li>
      </ul>
      <h3>The rails</h3>
      <ul>
        <li>Black only: paper, print, embossing and a one-colour etch. White only: dark grounds, and the etched mark on the acrylic.</li>
        <li>One colour: each Cloud's own mark, for its speaker, box and page. Avoid Acid on paper, where yellow is too faint; use it on ink.</li>
        <li>Multicolour: the brand at large. Animated: screens only (the idents, the loader, the cursor).</li>
        <li>Even lines for most sizes. Below about 32 px, or in one colour, round 22's lighter far halves read better. Discs are the solid version, for fills, stamps, stickers and the smallest sizes.</li>
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

// the discs: each one's oval less every nearer disc's oval (a half-plane apart), then the seams over the edges
function drawDiscs(ctx, V, gs, filled, cols, bg, seamW) {
  const on = gs.filter((g, k) => filled[k] && Math.abs(g.n[2]) > 1e-4 && g.r > 1e-3);
  const cv = ctx.canvas, off = offscreen(cv.width, cv.height), o = off.getContext('2d'), T = ctx.getTransform();
  gs.forEach((gi, k) => {
    if (!on.includes(gi)) return;
    o.setTransform(1, 0, 0, 1, 0, 0); o.clearRect(0, 0, off.width, off.height); o.setTransform(T);
    o.globalCompositeOperation = 'source-over'; o.fillStyle = cols[k]; ellipse(o, V, gi.pts); o.fill();
    o.globalCompositeOperation = 'destination-out';
    for (const gj of on) { if (gj === gi) continue;
      const ni = gi.n, nj = gj.n, A = -nj[0] / nj[2] + ni[0] / ni[2], B = -nj[1] / nj[2] + ni[1] / ni[2], C = gj.d / nj[2] - gi.d / ni[2];
      const m = Math.hypot(A, B); o.save();
      if (m > 1e-9) { const ux = A / m, uy = B / m, c0 = -C / m, px = ux * c0, py = uy * c0, tx = -uy, ty = ux, b = 4;
        const q = [[px + tx * b, py + ty * b], [px - tx * b, py - ty * b], [px - tx * b + ux * b, py - ty * b + uy * b], [px + tx * b + ux * b, py + ty * b + uy * b]];
        o.beginPath(); q.forEach((p, i) => i ? o.lineTo(V.X(p), V.Y(p)) : o.moveTo(V.X(p), V.Y(p))); o.closePath(); o.clip();
      } else if (C <= 0) { o.restore(); continue; }
      ellipse(o, V, gj.pts); o.fill(); o.restore(); }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(off, 0, 0); ctx.restore();
  });
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
// tubes (round 23) or discs (filled, seamed); a ring marked `ink` stays a line over the discs, hidden where a nearer
// disc covers it
function drawRings(ctx, V, items, style, G) {
  const w = D.w * V.R; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  if (style === 'tubes') { drawTubes(ctx, V, items, G); return; }
  if (style === 'discs') {
    const ds = items.filter(i => !i.ink && i.g.r > 1e-3);
    drawDiscs(ctx, V, ds.map(i => i.g), ds.map(() => true), ds.map(i => i.col), G.bg, D.seam * V.R);
    for (const i of items) if (i.ink) { ctx.strokeStyle = i.col; ctx.lineWidth = w * 0.8; strokeVisible(ctx, V, i.g.pts, ds.map(d => d.g), []); }
  } else {
    for (const front of [false, true]) for (const i of items) {
      if (i.g.r <= 1e-3) continue;
      ctx.strokeStyle = i.col; ctx.lineWidth = w; sidePath(ctx, V, i.g.pts, front); ctx.stroke(); }
  }
}
const globeItems = (geom, spin = 0) => ringsAt(spin, geom || {}).map((g, k) => ({ g, col: D.hues[k] }));

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

// the gyroscope: two rings spin on two axes, slow and settle as the equator and the rim; the other four unfold from them
const GYRO = { spin: 1.5, unfold: 0.45 };
function drawGyro(ctx, V, t, style, G) {
  const B = basis(D.lean, D.elev), s = clamp(t / GYRO.spin, 0, 1), e = 1 - Math.pow(1 - s, 3), u = smooth((t - GYRO.spin) / GYRO.unfold);
  const items = [{ g: tippedRing(rad(540) * (1 - e), B, [Math.SQRT1_2, Math.SQRT1_2]), col: D.hues[1] },
                 { g: meridianRing(90 + 720 * (1 - e), B), col: D.hues[4] }];
  if (u > 0) items.push({ g: parallelRing(40 * u, B), col: D.hues[0] }, { g: parallelRing(-40 * u, B), col: D.hues[2] },
                        { g: meridianRing(90 - 60 * u, B), col: D.hues[3] }, { g: meridianRing(90 + 60 * u, B), col: D.hues[5] });
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

// an ident: the globe arrives, holds, moves aside, and EARF types in beside it
const IDENTS = { printer: { dur: 2.05, draw: drawPrinter }, gyro: { dur: 2.0, draw: drawGyro }, kick: { dur: 1.95, draw: drawKick },
                 coin: { dur: 3.15, draw: (c, V, t, s, G) => coinAt(c, V, t, s, G, false) } };
const HOLD = 0.35, MOVE = 0.5, TYPE = 0.07;
function identTimes(kind) { const m0 = IDENTS[kind].dur + HOLD; return { move0: m0, word0: m0 + MOVE, end: m0 + MOVE + 4 * TYPE + 1.3 }; }
function identLayout(W, H) {
  const lockW = 450 + 110 + D.wordW, k = Math.min(W * 0.74 / lockW, H * 0.5 / 450), x0 = (W - lockW * k) / 2;
  return { R: 225 * k / (1 + D.w / 2), cx: x0 + 225 * k, cy: H / 2, wx: x0 + 560 * k, wy: H / 2 - 150 * k, k };
}
function drawIdent(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground], L = identLayout(W, H), T = identTimes(o.kind), m = smooth((t - T.move0) / MOVE);
  const hR = Math.min(H * 0.34, W * 0.3), V = view(W, H, W / 2 + (L.cx - W / 2) * m, H / 2 + (L.cy - H / 2) * m, hR + (L.R - hR) * m);
  ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  IDENTS[o.kind].draw(ctx, V, Math.min(t, IDENTS[o.kind].dur + 0.01), o.style, G);
  const nl = Math.floor((t - T.word0) / TYPE) + 1;
  ctx.save(); ctx.translate(L.wx, L.wy); ctx.scale(L.k, L.k); ctx.fillStyle = G.ink;
  D.letters.slice(0, clamp(nl, 0, 4)).forEach(d => ctx.fill(new Path2D(d))); ctx.restore();
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

// a turn at one speed, eased in and out briefly (u from 0 to 1)
function turn(u, ease = 0.12) {
  u = clamp(u, 0, 1); const k = 2 * ease * (1 - ease);
  return u < ease ? u * u / k : u > 1 - ease ? 1 - (1 - u) * (1 - u) / k : (u - ease / 2) / (1 - ease);
}

function meridianRing(lam, B) {
  const { a, e1, e2 } = B, l = rad(lam), u = [0, 1, 2].map(j => Math.cos(l) * e1[j] + Math.sin(l) * e2[j]), pts = [];
  for (let i = 0; i <= 120; i++) { const q = TAU * i / 120; pts.push([0, 1, 2].map(j => Math.cos(q) * u[j] + Math.sin(q) * a[j])); }
  return { pts, n: cross(u, a), d: 0, c: [0, 0, 0], r: 1 };
}
function hull(P) {
  P = P.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]);
  const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]), lo = [], up = [];
  for (const p of P) { while (lo.length >= 2 && cr(lo.at(-2), lo.at(-1), p) <= 0) lo.pop(); lo.push(p); }
  for (const p of P.reverse()) { while (up.length >= 2 && cr(up.at(-2), up.at(-1), p) <= 0) up.pop(); up.push(p); }
  return lo.slice(0, -1).concat(up.slice(0, -1));
}
// a coin of some thickness turned th degrees from face on about the axis: its silhouette, the hull of its two faces
function coinSilhouette(ctx, V, th, B, thick) {
  const c = Math.cos(rad(th)), s = Math.sin(rad(th)), { a, e1, e2 } = B, P = [];
  const h = [0, 1, 2].map(j => c * e2[j] - s * e1[j]), nm = [0, 1, 2].map(j => s * e2[j] + c * e1[j]);
  for (const sh of [-1, 1]) for (let i = 0; i < 120; i++) { const q = TAU * i / 120;
    const p = [0, 1, 2].map(j => Math.cos(q) * h[j] + Math.sin(q) * a[j] + sh * thick / 2 * nm[j]); P.push([V.X(p), V.Y(p)]); }
  const Hh = hull(P); ctx.beginPath(); Hh.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath(); ctx.fill();
}

// the coin: spins on its edge, a colour a half turn (Flare to Haze); on one more half turn, slowing, it deals out the
// three meridians where it passes them; the view rises to the globe's tilt as the parallels close round them; a turn
const COIN = { rate: 600, spin: 1.8, deal: 0.6, tilt: [2.2, 3.0], grow: [2.55, 2.7, 2.85], turn: [3.4, 5.4], end: 6.0, elev0: 8 };
function coinAng(t) {
  if (t <= COIN.spin) return COIN.rate * t - 90;
  const u = clamp((t - COIN.spin) / COIN.deal, 0, 1);
  return COIN.rate * COIN.spin - 90 + 180 * (1 - (1 - u) * (1 - u));
}
function coinAt(ctx, V, t, style, G, turning = true) {
  const ang = coinAng(t), thick = 0.07;
  if (t < COIN.spin) {
    ctx.fillStyle = D.hues[clamp(Math.floor((ang + 90) / 180), 0, 5)];
    coinSilhouette(ctx, V, ang, basis(0, COIN.elev0), thick); return;
  }
  const rel = ang - COIN.rate * COIN.spin, placed = [-60, 0, 60].map(d => rel >= d), k = placed.filter(Boolean).length;
  const tilt = smooth((t - COIN.tilt[0]) / (COIN.tilt[1] - COIN.tilt[0]));
  const geom = { lean: D.lean * tilt, elev: COIN.elev0 + (D.elev - COIN.elev0) * tilt, grow: COIN.grow.map(g => smooth((t - g) / 0.3)) };
  const spin = turning ? 360 * turn((t - COIN.turn[0]) / (COIN.turn[1] - COIN.turn[0])) : 0, B = basis(geom.lean, geom.elev);
  const items = ringsAt(spin, geom).map((g, i) => ({ g, col: D.hues[i], on: i < 3 ? geom.grow[i] > 0 : placed[i - 3] })).filter(i => i.on);
  if (k < 3 && rel < -72) {                                                // still on its edge: its thickness shows
    drawRings(ctx, V, items, style, G); ctx.fillStyle = D.hues[3]; coinSilhouette(ctx, V, rel, B, thick); return;
  }
  if (k < 3) items.push({ g: meridianRing(90 + rel, B), col: D.hues[3 + k] });
  drawRings(ctx, V, items, style, G);
}
function drawCoin(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground]; ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  coinAt(ctx, view(W, H, W / 2, H / 2, Math.min(W, H) * 0.3), t, o.style || 'discs', G);
  return COIN.end;
}

const SCENES = { ident: drawIdent, loader: drawLoader, cursor: drawCursor, coin: drawCoin, kick: drawKickLoop };

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
  const state = { kind: 'printer', style: 'even', ground: 'paper', t0: null };
  const CAPS = {
    printer: 'Printer: a head shuttles across and back, a band lower each pass, and leaves the finished globe in its wake.',
    gyro: 'Gyroscope: two rings spin on two axes and settle as the equator and the rim. The other four unfold out of them.',
    kick: 'Kick: seen from above the pole, the globe is a speaker: rings round one centre, the meridians its spokes. It kicks twice, then tips down to the Earth\'s tilt.',
    coin: 'Coin: a disc spins on its edge, a colour each half turn. On one more turn it deals out the meridians, and the parallels close round them.' };
  const capText = document.getElementById('cap-text'), screen = document.getElementById('screen');
  function segs(id, key) {
    const el = document.getElementById(id);
    el.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
      el.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      state[key] = b.dataset.v; state.t0 = performance.now(); capText.textContent = CAPS[state.kind];
      screen.style.background = GROUNDS[state.ground].bg; });
  }
  segs('kind', 'kind'); segs('style', 'style'); segs('ground', 'ground'); capText.textContent = CAPS.printer;
  document.getElementById('replay').onclick = () => { state.t0 = performance.now(); };
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
  ['stage', 'load-night', 'load-paper', 'cursor', 'kickloop'].forEach(id => io.observe(document.getElementById(id)));
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
      drawKickLoop(ctx, W, H, reduce ? 0.3 : s, { ground: 'night', style: 'even' }); }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
</script>
"""


def page():
    return PAGE.replace('__RAILS__', rails_html()).replace('__THEME__', theme_html()).replace('__DATA__', json.dumps(data(), separators=(',', ':')))


def standalone():
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, '
            'initial-scale=1, viewport-fit=cover"></head><body>\n' + page() + '\n</body></html>\n')


SCENE_SET = [('ident', dict(kind=k, style=st, ground=g)) for k in ('printer', 'gyro', 'kick', 'coin')
             for st, g in (('even', 'paper'), ('discs', 'night'), ('tubes', 'night'))] + [
             ('kick', dict(style='even', ground='night')), ('loader', dict(ground='night')), ('loader', dict(ground='paper')),
             ('cursor', dict(ground='night'))]


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
    ap.add_argument('--only', nargs='*', default=[], help='with --video, only the scenes whose options mention one of these (e.g. tubes)')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    written = []
    for style in ('lines', 'even', 'tubes', 'discs'):
        for tag, cols in [('multi', HUES), ('black', INK), ('white', WHITE)] + [(n.lower(), c) for n, c in zip(NAMES, HUES)]:
            f = f'earth-{style}-{tag}.svg'
            open(os.path.join(OUT, f), 'w').write(mark_svg(style, cols, label=f'EARF globe, {style}, {tag}',
                                                           ground='night' if tag == 'white' else 'paper'))
            written.append(f)
    for g, word, bg in (('paper', INK, PAPER), ('ink', WHITE, NIGHT)):
        open(os.path.join(OUT, f'earth-lockup-{g}.svg'), 'w').write(lockup_svg('even', HUES, word, bg=bg))
    open(os.path.join(OUT, 'earth-lockup-black.svg'), 'w').write(lockup_svg('even', INK, INK))
    open(os.path.join(OUT, 'earth-lockup-white.svg'), 'w').write(lockup_svg('even', WHITE, WHITE))
    open(os.path.join(OUT, 'earth.html'), 'w').write(standalone())
    if a.fragment:
        open(a.fragment, 'w').write(page())
    print(f'brand/earth.html, {len(written)} marks, 4 lockups')
    if a.video:
        for scene, opts in SCENE_SET:
            if a.only and not any(w in json.dumps(opts) for w in a.only):
                continue
            print(os.path.relpath(video(OUT, scene, opts, loops=2 if scene == 'loader' else 1), HERE))


if __name__ == '__main__':
    main()
