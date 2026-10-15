"""EARF's globe as a 3D Earth, and the software it moves in (round 22).

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
  (the even version, every line one weight, tangles in one colour). Discs: each ring
  filled as a flat disc, no strokes, the discs crossing one another as six sheets of the Clouds' tinted acrylic slotted
  into a globe would, each showing only where nothing nearer covers it, a seam of the ground between facets.
- Animated (the ident): each ring drawn at one steady speed, in the ground's ink, and given its colour only once it
  closes, as a paint bucket only fills a closed shape; then the globe turns once on its axis, as the loading globes
  of 1998 browsers did, and EARF types in beside it.
- The software kit: the loader (a white circle rolling across black uncovers the six colours in its wake, and covers
  them again on its way back; or black on paper), the cursor (a circle with the six colours trailing it, each a beat
  behind), and the coin (a disc spinning on its edge flashes each colour in turn, deals out the three meridians as it
  turns, and the parallels close round them into the globe).

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

OUT = os.path.join(HERE, 'brand')
LEAN, ELEV, LAT = 23.44, 22.0, 40.0                      # the axis's lean (the Earth's), its tip toward us, the parallels
MERIDIANS = (30.0, 90.0, 150.0)                          # the meridians' longitudes at rest (90 faces us: the rim)
W_LINE, W_DEPTH, SEAM = 0.075, 0.42, 0.035               # of the globe's radius: the line, the far line's share, the seam
CLOUDS = [(name, colour) for key, line, num, name, colour in M.SPEAKERS if line == 'Cloud']
HUES = [c for n, c in CLOUDS if n not in ('Fog', 'Smoke')]          # Flare Dust Acid Poison Ice Haze, ring by ring
NAMES = [n for n, c in CLOUDS if n not in ('Fog', 'Smoke')]
PAPER, INK, WHITE = '#F2EFEA', '#1C1A18', '#F6F5F2'
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


def mark_svg(style, colours, size=None, bg=None, label='EARF'):
    """style: lines (the far halves lighter: the mark), even (every line one weight) or discs; colours: six (a ring
    each) or one."""
    if isinstance(colours, str):
        colours = [colours] * 6
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


def lockup_svg(style, colours, word, size=None, bg=None):
    """The globe beside EARF, its diameter one and a half cap heights, centred on the letters."""
    k = 225 / (1 + W_LINE / 2)
    inner = mark_svg(style, colours)
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
    return dict(lean=LEAN, elev=ELEV, lat=LAT, mer=list(MERIDIANS), w=W_LINE, wDepth=W_DEPTH, seam=SEAM, hues=HUES,
                names=NAMES, paper=PAPER, ink=INK, night=NIGHT, white=WHITE, letters=letters(), wordW=M.WORDMARK_W)


RAILS = [('Black only', 'paper', lambda: INK), ('White only', 'night', lambda: WHITE),
         ('One colour', 'paper', lambda: HUES[4]), ('Multicolour', 'paper', lambda: HUES),
         ('Multicolour on ink', 'night', lambda: HUES)]


def rails_html():
    """The guide rails: each style in black only, white only, one colour and multicolour, and the singles."""
    rows = ''
    for style, title in (('lines', 'Lines'), ('discs', 'Discs')):
        cells = ''.join(f'<figure class="rail {g}">{mark_svg(style, f(), label=f"{title}, {t.lower()}")}<figcaption>{t}</figcaption></figure>'
                        for t, g, f in RAILS)
        singles = ''.join(f'<span class="one" title="{n}">{mark_svg(style, c, label=f"{title} in {n}")}</span>'
                          for n, c in zip(NAMES, HUES))
        rows += (f'<div class="railrow"><h3>{title}</h3><div class="rails">{cells}</div>'
                 f'<div class="singles"><span class="lab">Each Cloud in its own colour</span>{singles}</div></div>')
    locks = (f'<figure class="lock paper">{lockup_svg("lines", HUES, INK)}<figcaption>Lockup on paper</figcaption></figure>'
             f'<figure class="lock night">{lockup_svg("lines", HUES, WHITE)}<figcaption>On ink</figcaption></figure>'
             f'<figure class="lock paper">{lockup_svg("discs", INK, INK)}<figcaption>Black only, discs</figcaption></figure>'
             f'<figure class="lock night">{lockup_svg("lines", WHITE, WHITE)}<figcaption>White only</figcaption></figure>')
    return rows + f'<div class="locks">{locks}</div>'


PAGE = r"""<title>EARF Globe</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* a desktop of 2001: platinum grey, white panels with a bevel, Verdana at small sizes; the globe and its software */
:root {
  --page: #DEDCD7; --panel: #F6F5F2; --fg: #1C1A18; --muted: #57534C; --line: #B9B5AD; --hi: #FFFFFF; --lo: #A8A49C;
  --bar: #E9E7E3; --font: Verdana, Tahoma, 'DejaVu Sans', Geneva, sans-serif; color-scheme: light;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --page: #121114; --panel: #1B1A1E; --fg: #ECEAE6; --muted: #A6A29B; --line: #3A383F; --hi: #2C2A31; --lo: #08080A;
  --bar: #232127; color-scheme: dark } }
:root[data-theme="dark"] { --page: #121114; --panel: #1B1A1E; --fg: #ECEAE6; --muted: #A6A29B; --line: #3A383F;
  --hi: #2C2A31; --lo: #08080A; --bar: #232127; color-scheme: dark }
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
.screen canvas, .strip canvas, .pad canvas { display: block; width: 100%; height: 100% }
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
.kit { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px }
.kit .wide { grid-column: 1 / -1 }
.strip { aspect-ratio: 5 / 1 }
.pad { aspect-ratio: 16 / 10; cursor: none; touch-action: none }
.coin { aspect-ratio: 16 / 10 }
.notes { display: grid; gap: 10px; padding: 16px }
.notes h3 { margin-top: 6px }
.notes ul { margin: 0; padding-left: 18px; max-width: 74ch } .notes li { margin: 3px 0 }
@media (max-width: 720px) { .rails { grid-template-columns: repeat(3, minmax(0, 1fr)) } .kit, .locks { grid-template-columns: 1fr }
  .seg button, .btn { padding: 10px 10px } }
body.capture { padding: 0; overflow: hidden } body.capture main { display: none }
#cap { display: none } body.capture #cap { display: block; position: fixed; inset: 0; width: 100vw; height: 100vh }
</style>
<main>
  <header>
    <div class="eyebrow">EARF &middot; Round 22 &middot; the globe</div>
    <h1>A 3D Earth in six colours, and the software it lives in</h1>
    <p class="lede">Three parallels and three meridians on the Earth's own 23.4&deg; tilt, tipped toward you so the far
      side shows through. Each ring is one of the six colour Clouds, and none of them is black or white: Smoke and Fog
      are the black-only and white-only marks. Each ring is drawn at one steady speed and takes its colour once it
      closes. Then the globe turns on its axis, the way browser globes did in 1998.</p>
  </header>

  <section class="win" aria-label="The ident">
    <div class="bar"><i style="background:#D2382F"></i><i style="background:#E9B320"></i><i style="background:#4F7F3A"></i><b>earf.world &mdash; ident</b></div>
    <div class="screen" id="screen"><canvas id="stage" aria-label="The EARF globe drawn ring by ring"></canvas></div>
    <div class="controls">
      <div class="seg" id="style" role="group" aria-label="Style">
        <button aria-pressed="true" data-v="lines">Lines</button><button aria-pressed="false" data-v="even">Even lines</button><button aria-pressed="false" data-v="discs">Discs</button>
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
      <div class="bar"><b>Coin &mdash; spins, flashes each colour, becomes the globe</b></div>
      <div class="coin" style="background:#121114"><canvas id="coin" aria-label="Spinning coin becoming the globe"></canvas></div>
      <div class="controls"><button class="btn" id="coin-replay">Replay</button></div>
    </div>
  </section>

  <section class="win" aria-label="Notes">
    <div class="bar"><b>Notes</b></div>
    <div class="notes">
      <h3>Why it reads as the Earth</h3>
      <ul>
        <li>The axis leans 23.4&deg;, as the Earth's does and as a desk globe's stand holds it. It also tips 22&deg; toward you, so the parallels open into ovals and the far halves show behind the near ones.</li>
        <li>The parallels are warm, north to south: Flare, Dust, Acid. The meridians are cool: Poison, Ice, Haze. Ice is the meridian facing you, so the globe's outline is blue.</li>
        <li>The rings are drawn in that spectrum order. Each one stays in the ground's ink until it closes, then takes its colour all at once, like a paint bucket filling a closed shape.</li>
        <li>The far half of each ring is lighter and sits under the near halves. Even in one colour, the near side reads in front and the globe reads as round. With every line the same weight, the one-colour mark tangles (see Even lines in the player).</li>
      </ul>
      <h3>The rails</h3>
      <ul>
        <li>Black only: paper, print, embossing and a one-colour etch. White only: dark grounds, and the etched mark on the acrylic.</li>
        <li>One colour: each Cloud's own mark, for its speaker, box and page. Avoid Acid on paper, where yellow is too faint; use it on ink.</li>
        <li>Multicolour: the brand at large. Animated: screens only (the ident, the loader, the cursor, the coin).</li>
        <li>Lines for most sizes. Below about 32 px the far halves fade and the near ones still read. Discs are the solid version, for fills, stamps, stickers and the smallest sizes.</li>
        <li>Clear space: a quarter of the globe's width on every side. In the lockup, the globe is one and a half cap heights tall, centred on the letters.</li>
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

// the ident: the rings one by one at one speed, each coloured when it closes; one turn; EARF typed in
const SPEED = 7.2, BEAT = 0.2, LEAD = 0.5, TURN = 3.2, TYPE = 0.11, MOVE = 0.8;
function identPlan() {
  const gs = ringsAt(0), plan = []; let t = LEAD;
  gs.forEach(g => { const d = g.len / SPEED; plan.push([t, t + d]); t += d + BEAT; });
  const turn0 = t + 0.1, move0 = turn0 + TURN - MOVE, word0 = turn0 + TURN + 0.15;
  return { plan, turn0, move0, word0, end: word0 + 4 * TYPE + 1.6 };
}
const IDENT = identPlan();
function identLayout(W, H) {
  const lockW = 450 + 110 + D.wordW, k = Math.min(W * 0.74 / lockW, H * 0.5 / 450), x0 = (W - lockW * k) / 2;
  return { R: 225 * k / (1 + D.w / 2), cx: x0 + 225 * k, cy: H / 2, wx: x0 + 560 * k, wy: H / 2 - 150 * k, k };
}
function drawIdent(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground], L = identLayout(W, H), m = smooth((t - IDENT.move0) / MOVE);
  const hR = Math.min(H * 0.34, W * 0.3), V = view(W, H, W / 2 + (L.cx - W / 2) * m, H / 2 + (L.cy - H / 2) * m, hR + (L.R - hR) * m);
  ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  const drawn = IDENT.plan.map(([a, b]) => clamp((t - a) / (b - a), 0, 1)), done = IDENT.plan.map(([a, b]) => t >= b);
  drawGlobe(ctx, V, { style: o.style, ground: o.ground, drawn, done, spin: 360 * turn((t - IDENT.turn0) / TURN) });
  const nl = Math.floor((t - IDENT.word0) / TYPE) + 1;                     // the letters, one a beat
  ctx.save(); ctx.translate(L.wx, L.wy); ctx.scale(L.k, L.k); ctx.fillStyle = G.ink;
  D.letters.slice(0, clamp(nl, 0, 4)).forEach(d => ctx.fill(new Path2D(d))); ctx.restore();
  return IDENT.end;
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
// three meridians where it passes them; the camera rises to the globe's tilt as the parallels close round them; a turn
const COIN = { spin: 3.0, deal: 1.0, tilt: [3.7, 4.9], grow: [4.4, 4.62, 4.84], turn: [5.4, 8.4], end: 9.2, elev0: 8 };
function coinAng(t) {
  if (t <= COIN.spin) return 360 * t - 90;
  const u = clamp((t - COIN.spin) / COIN.deal, 0, 1);
  return 360 * COIN.spin - 90 + 180 * (1 - (1 - u) * (1 - u));
}
function drawCoin(ctx, W, H, t, o) {
  const G = GROUNDS[o.ground], R = Math.min(W, H) * 0.3, V = view(W, H, W / 2, H / 2, R);
  ctx.fillStyle = G.bg; ctx.fillRect(0, 0, W, H);
  const ang = coinAng(t), thick = 0.07;
  if (t < COIN.spin) {
    ctx.fillStyle = D.hues[clamp(Math.floor(2 * t), 0, 5)];
    coinSilhouette(ctx, V, ang, basis(0, COIN.elev0), thick);
    return COIN.end;
  }
  const rel = ang - 360 * COIN.spin, placed = [-60, 0, 60].map(d => rel >= d), k = placed.filter(Boolean).length;
  const tilt = smooth((t - COIN.tilt[0]) / (COIN.tilt[1] - COIN.tilt[0]));
  const geom = { lean: D.lean * tilt, elev: COIN.elev0 + (D.elev - COIN.elev0) * tilt, grow: COIN.grow.map(g => smooth((t - g) / 0.3)) };
  const spin = 360 * turn((t - COIN.turn[0]) / (COIN.turn[1] - COIN.turn[0]));
  const gs = ringsAt(spin, geom), cols = D.hues.slice(), done = geom.grow.map(g => g > 0).concat(placed);
  if (k < 3 && rel < -72) {                                                // the coin still on its edge: its thickness shows
    drawDiscs(ctx, V, gs, done, cols, G.bg, D.seam * R);
    ctx.fillStyle = D.hues[3]; coinSilhouette(ctx, V, rel, basis(geom.lean, geom.elev), thick);
    return COIN.end;
  }
  if (k < 3) { gs.push(meridianRing(90 + rel, basis(geom.lean, geom.elev))); cols.push(D.hues[3 + k]); done.push(true); }
  drawDiscs(ctx, V, gs, done, cols, G.bg, D.seam * R);
  return COIN.end;
}

const SCENES = { ident: drawIdent, loader: drawLoader, cursor: drawCursor, coin: drawCoin };

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
  const state = { style: 'lines', ground: 'paper', t0: performance.now() };
  const CAPS = {
    lines: 'Lines, the mark: the six ovals with their far halves lighter and under the near ones, so the near side reads in front even in one colour.',
    even: 'Even lines: every line one weight. Fine in colour, where the hues tell the rings apart; in one colour it tangles.',
    discs: 'Discs: each ring filled as a flat disc with no strokes. The discs cross one another like six sheets of the Clouds\' tinted acrylic slotted together, with a seam of the ground between the faces.' };
  const capText = document.getElementById('cap-text');
  function segs(id, key) {
    const el = document.getElementById(id);
    el.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
      el.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      state[key] = b.dataset.v; state.t0 = performance.now(); capText.textContent = CAPS[state.style];
      document.getElementById('screen').style.background = GROUNDS[state.ground].bg; });
  }
  segs('style', 'style'); segs('ground', 'ground'); capText.textContent = CAPS.lines;
  document.getElementById('replay').onclick = () => { state.t0 = performance.now(); };
  const coin = { t0: performance.now() };
  document.getElementById('coin-replay').onclick = () => { coin.t0 = performance.now(); };
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
  const vis = new Map(); const io = new IntersectionObserver(es => es.forEach(e => vis.set(e.target, e.isIntersecting)));
  ['stage', 'load-night', 'load-paper', 'cursor', 'coin'].forEach(id => io.observe(document.getElementById(id)));
  const on = id => vis.get(document.getElementById(id)) !== false;
  function tick(now) {
    const s = now / 1000;
    if (on('stage')) { const { ctx, W, H } = fit(document.getElementById('stage'));
      const t = reduce ? IDENT.end : (now - state.t0) / 1000;
      drawIdent(ctx, W, H, Math.min(t, IDENT.end), state); }
    for (const g of ['night', 'paper']) if (on('load-' + g)) { const { ctx, W, H } = fit(document.getElementById('load-' + g));
      drawLoader(ctx, W, H, reduce ? LOAD.go : s, { ground: g }); }
    if (on('cursor')) { const { ctx, W, H } = fit(document.getElementById('cursor'));
      const live = s - last < 2.5; drawCursor(ctx, W, H, s, { ground: 'night' }, live ? at : (tt => ghost(tt, W, H))); }
    if (on('coin')) { const { ctx, W, H } = fit(document.getElementById('coin'));
      drawCoin(ctx, W, H, reduce ? COIN.end : Math.min((now - coin.t0) / 1000, COIN.end), { ground: 'night' }); }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
</script>
"""


def page():
    return PAGE.replace('__RAILS__', rails_html()).replace('__DATA__', json.dumps(data(), separators=(',', ':')))


def standalone():
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, '
            'initial-scale=1, viewport-fit=cover"></head><body>\n' + page() + '\n</body></html>\n')


SCENE_SET = [('ident', dict(style='lines', ground='paper')), ('ident', dict(style='lines', ground='night')),
             ('ident', dict(style='discs', ground='paper')), ('ident', dict(style='discs', ground='night')),
             ('loader', dict(ground='night')), ('loader', dict(ground='paper')),
             ('cursor', dict(ground='night')), ('coin', dict(ground='night')), ('coin', dict(ground='paper'))]


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
    tag = opts.get('style', '')
    name = f'earth-{scene}' + (f'-{tag}' if scene == 'ident' else '') + f'-{opts["ground"]}.mp4'
    mp4 = os.path.join(out_dir, name)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', mp4], check=True)
    shutil.rmtree(tmp)
    return mp4


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--fragment', help='also write the page as an Artifact body to this path')
    ap.add_argument('--video', action='store_true', help='also write an MP4 of each scene')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    written = []
    for style in ('lines', 'even', 'discs'):
        for tag, cols in [('multi', HUES), ('black', INK), ('white', WHITE)] + [(n.lower(), c) for n, c in zip(NAMES, HUES)]:
            f = f'earth-{style}-{tag}.svg'
            open(os.path.join(OUT, f), 'w').write(mark_svg(style, cols, label=f'EARF globe, {style}, {tag}'))
            written.append(f)
    for g, word, bg in (('paper', INK, PAPER), ('ink', WHITE, NIGHT)):
        open(os.path.join(OUT, f'earth-lockup-{g}.svg'), 'w').write(lockup_svg('lines', HUES, word, bg=bg))
    open(os.path.join(OUT, 'earth-lockup-black.svg'), 'w').write(lockup_svg('lines', INK, INK))
    open(os.path.join(OUT, 'earth-lockup-white.svg'), 'w').write(lockup_svg('lines', WHITE, WHITE))
    open(os.path.join(OUT, 'earth.html'), 'w').write(standalone())
    if a.fragment:
        open(a.fragment, 'w').write(page())
    print(f'brand/earth.html, {len(written)} marks, 4 lockups')
    if a.video:
        for scene, opts in SCENE_SET:
            print(os.path.relpath(video(OUT, scene, opts, loops=2 if scene == 'loader' else 1), HERE))


if __name__ == '__main__':
    main()
