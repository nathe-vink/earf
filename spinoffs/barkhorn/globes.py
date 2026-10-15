"""EARF's globe and its ident as one thing: five globes, each drawn by one dot in one unbroken line (round 21).

The owner, of round 20's ident: "None. We haven't nailed it yet. See all my previous notes." And of the globe: "The
idea is for the animated thing to be the globe. They should be one and the same. But we need the right globe design
and then we need to work backward from the animation. We can also venture from the globe if we find something else
that embodies the earf brand."

The earlier notes: "overlapping concentric circles that form a larger circle, kind of like a color wheel"; "a
Spirograph type thing where a black dot rotates around several times to create a circle of circles, each adopting a
color as its mini circle is traced"; and of round 20's first version: "too much like a film reel", "the acceleration
changes too much as it draws. It should be on fluid motion", "it shouldn't have to create a stroke outside of each
circle".

So each globe here is a path one dot follows at one steady speed, never stopping and never turning a corner (where two
circles cross it veers through a turn too short to see, and where it must reach another circle it runs on along a line
it has already drawn), and every stroke it leaves is part of a circle. Its last frame is the globe. Each speeds up once,
at the start, and slows once, at the end.

- orbits: the dot orbits pole to pole, each orbit a great circle in a Cloud's colour, so the eight meridians build the
  globe in a colour wheel round its axis (Runge's colour sphere, 1810: the hues round the equator). B3's lens, one
  meridian, once for each Cloud. The far side faint.
- spirograph: eight circles nearly concentric, their centres on a small ring, as a Spirograph's gear draws inside its
  ring; together they form the larger circle.
- rose: eight petals through one centre in one line (a rose curve, r = cos 4/3 t, three turns): round 20's rosette, but
  the dot passes straight through the centre between petals instead of leaving the circles.
- light: six circles, the six hues, overlapping in the middle: as light they add to white (Fog), on paper the tints
  multiply to near black (Smoke), so six circles hold all eight Clouds.
- layers: beyond the globe, one groove spiralling out from the centre, each turn a Cloud in spectrum order, which is
  the Earth's own order from its core: red core, orange, yellow, green land, blue sea, violet sky, white cloud, black
  space. A record's groove, a tree's rings, the ear's cochlea.

    python3 spinoffs/barkhorn/globes.py                    ->  brand/globes.html, brand/globe-<name>[-light].svg
    python3 spinoffs/barkhorn/globes.py --fragment PATH    ->  also the page as an Artifact's body
    python3 spinoffs/barkhorn/globes.py --video [--fonts CSS]  ->  also brand/globe-<name>-<paper|light>.mp4 and the
                                                                   two reels, brand/globes-<paper|light>.mp4
"""
import argparse, base64, json, math, os, shutil, subprocess, sys, tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brand as B                                        # noqa: E402
import ident as I                                        # noqa: E402
import marks as M                                        # noqa: E402

OUT = os.path.join(HERE, 'brand')
TAU = 2 * math.pi
STEP = 0.008                                             # the path's spacing, of the globe's radius


def arc(c, r, a0, sweep, step=STEP):
    """Points on a circle (screen axes, y down: a rising angle runs clockwise), from angle a0 through `sweep`."""
    n = max(2, int(abs(sweep) * r / step))
    a = a0 + np.linspace(0, sweep, n + 1)
    return np.stack([c[0] + r * np.cos(a), c[1] + r * np.sin(a)], 1)


def blend(path, joins, r=0.05):
    """Round each corner at the given indices: the points within `r` of it, either way, give way to a quadratic curve
    with the corner as its control point, so the dot turns through it without a jolt (the turn is shorter than `r`)."""
    path = path.copy()
    for j in joins:
        d = np.cumsum(np.r_[0, np.linalg.norm(np.diff(path, axis=0), axis=1)])
        lo = np.searchsorted(d, d[j] - r); hi = min(len(path) - 1, np.searchsorted(d, d[j] + r))
        if hi - lo < 3:
            continue
        p0, p1, p2 = path[lo], path[j], path[hi]
        u = np.linspace(0, 1, hi - lo + 1)[:, None]
        path[lo:hi + 1] = (1 - u) ** 2 * p0 + 2 * (1 - u) * u * p1 + u ** 2 * p2
    return path


def ring_of_circles(n, d, rho, colours):
    """n circles of radius rho, centres on a ring of radius d from the top clockwise, drawn one after another: each
    from where it crosses the one before (the outer crossing) once round, then on along its own line to where it
    crosses the next, and across. The line left: the n circles exactly. Returns path, strokes, fills, joins."""
    th = [-math.pi / 2 + TAU * k / n for k in range(n)]
    cs = [(d * math.cos(t), d * math.sin(t)) for t in th]

    def outer_cross(a, b):
        (ax, ay), (bx, by) = a, b
        mx, my = (ax + bx) / 2, (ay + by) / 2
        dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy)
        h = math.sqrt(rho ** 2 - (L / 2) ** 2)
        p1 = (mx - dy / L * h, my + dx / L * h); p2 = (mx + dy / L * h, my - dx / L * h)
        return p1 if math.hypot(*p1) > math.hypot(*p2) else p2

    X = [outer_cross(cs[k], cs[(k + 1) % n]) for k in range(n)]      # X[k]: where circle k meets circle k+1
    parts, strokes, fills, joins = [], [], [], []
    count = 0                                       # points in the path so far
    for k in range(n):
        c = cs[k]
        a_in = math.atan2(X[k - 1][1] - c[1], X[k - 1][0] - c[0])
        a_out = math.atan2(X[k][1] - c[1], X[k][0] - c[0])
        on = (a_out - a_in) % TAU
        full = arc(c, rho, a_in, TAU)               # once round: its last point is its first
        more = arc(c, rho, a_in + TAU, on)[1:]      # then on along its own line to the next crossing
        if k == 0:
            seg, s0 = np.vstack([full, more]), 0
        else:                                       # it starts at the path's last point, the crossing
            seg, s0 = np.vstack([full[1:], more]), count - 1
        e0 = s0 + len(full) - 1
        strokes.append((s0, e0, k))
        fills.append(dict(ci=k, i0=s0, i1=e0, c=[round(c[0], 5), round(c[1], 5)]))
        parts.append(seg); count += len(seg)
        joins.append(count - 1)                     # where it veers onto the next circle
    return np.vstack(parts), strokes, fills, joins[:-1]


def orbits(tilt=22.0, yaw=11.25, n=8):
    """Eight great circles through the poles, 22.5 degrees of longitude apart, so sixteen meridians round the globe;
    seen from a little above the equator (`tilt`), turned by `yaw` so none is seen edge on. The dot starts at the
    north pole and goes once round each, turning at the pole onto the next."""
    ty, tt = math.radians(yaw), math.radians(tilt)
    pts, front, strokes, joins = [], [], [], []
    for k in range(n):
        lam = math.radians(180.0 * k / n)
        m = max(2, int(TAU / STEP))
        a = np.linspace(0, TAU, m + 1)
        x, y, z = np.sin(a) * math.sin(lam), np.cos(a), np.sin(a) * math.cos(lam)
        x, z = x * math.cos(ty) + z * math.sin(ty), -x * math.sin(ty) + z * math.cos(ty)
        y, z = y * math.cos(tt) - z * math.sin(tt), y * math.sin(tt) + z * math.cos(tt)
        p = np.stack([x, -y], 1)
        i0 = 0 if k == 0 else len(np.vstack(pts)) - 1      # each starts at the pole, where the last ended
        if k:
            p, z = p[1:], z[1:]
        pts.append(p); front.append(z > -1e-9)
        i1 = len(np.vstack(pts)) - 1
        strokes.append((i0, i1, k))
        joins.append(i1)
    path = blend(np.vstack(pts), joins[:-1], r=0.035)
    return dict(path=path, front=np.concatenate(front), strokes=strokes, fills=[], style='lines', fill=False)


def rose():
    """r = cos(4t/3) for three turns: eight petals through the centre, one line. It starts at the centre; the petals
    come in the order the curve gives (each 135 degrees on from the last), each coloured for where it points, so the
    finished rose runs the spectrum clockwise from the top."""
    k = 4 / 3
    t0 = -3 * math.pi / 8                           # from the centre into the top petal
    t = np.linspace(t0, t0 + 6 * math.pi, int(6 * math.pi * 1.2 / STEP) + 1)
    r = np.cos(k * t)
    path = np.stack([-r * np.sin(t), -r * np.cos(t)], 1)   # mirrored, so the petals come clockwise, in spectrum order
    strokes, fills = [], []
    edges = [np.searchsorted(t, t0 + j * 3 * math.pi / 4) for j in range(9)]
    for j in range(8):
        i0, i1 = int(edges[j]), int(min(edges[j + 1], len(t) - 1))
        mid = path[(i0 + i1) // 2]
        ang = (math.degrees(math.atan2(mid[0], -mid[1])) + 360) % 360           # from the top, clockwise
        ci = int(round(ang / 45)) % 8
        strokes.append((i0, i1, ci)); fills.append(dict(ci=ci, i0=i0, i1=i1, c=[0.0, 0.0]))
    return dict(path=path, front=None, strokes=strokes, fills=fills, style='filled', fill=True)


def layers(turns=8, r0=0.0):
    """One groove from the centre out, eight turns, each the band of a Cloud from the core (Flare) to space (Smoke)."""
    T = turns * TAU
    t = np.linspace(0, T, int(turns * math.pi * 1.0 / STEP) + 1)
    r = r0 + (1 - r0) * t / T
    path = np.stack([r * np.sin(t), -r * np.cos(t)], 1)
    strokes, fills = [], []
    for k in range(turns):
        i0, i1 = int(np.searchsorted(t, k * TAU)), int(min(np.searchsorted(t, (k + 1) * TAU), len(t) - 1))
        strokes.append((i0, i1, k)); fills.append(dict(ci=k, i0=i0, i1=i1, c=[0.0, 0.0], layer=True))
    return dict(path=path, front=None, strokes=strokes, fills=fills, style='filled', fill=True)


def cands():
    sp_path, sp_st, sp_fi, sp_j = ring_of_circles(8, 0.30, 0.70, None)
    li_path, li_st, li_fi, li_j = ring_of_circles(6, 0.36, 0.64, None)
    return [
        dict(key='orbits', name='Orbits', line='A dot orbits pole to pole; each orbit is a Cloud, and eight make the globe.',
             story="B3's lens, one meridian, drawn once for each Cloud. The dot orbits the globe over its poles, each orbit a "
                   "great circle in a Cloud's colour, so the hues run round the axis as a colour wheel would round its "
                   "centre: Runge's colour sphere (1810). The far side shows faintly through, as through the acrylic.",
             **orbits(), seconds=7.0),
        dict(key='spirograph', name='Spirograph', line='Eight circles, nearly concentric, drawn as a Spirograph draws.',
             story="Eight circles of one size, their centres on a small ring, as a Spirograph's gear draws inside its ring. "
                   "The dot goes round eight times; each circle takes its colour as it closes, and together they form the "
                   "larger circle.",
             path=blend(sp_path, sp_j, 0.06), front=None, strokes=sp_st, fills=sp_fi, style='lines', fill=True,
             seconds=6.5),
        dict(key='rose', name='Rose', line='Eight petals through one centre, in one unbroken line.',
             story="Round 20's rosette as one curve (r = cos 4/3 t, three turns). The dot passes straight through the centre "
                   "from one petal to the next, so it never leaves the petals and never turns a corner. Each petal is coloured "
                   "for where it points, so the spectrum runs clockwise from the top.",
             **rose(), seconds=6.5),
        dict(key='light', name='Light', line='Six colours of light overlap into white; on paper, into black.',
             story="The six hues as six circles overlapping in the middle. As light they add to white, which is Fog; on paper "
                   "the tints multiply to near black, which is Smoke. So six circles hold all eight Clouds.",
             path=blend(li_path, li_j, 0.06), front=None, strokes=li_st, fills=li_fi, style='filled', fill=True,
             seconds=5.5),
        dict(key='layers', name='Layers', line='Beyond the globe: one groove from the core out, the Earth in its layers.',
             story="One groove spiralling out from the centre, a turn a Cloud. The spectrum order is the Earth's own from its "
                   "core: red core, orange, yellow, green land, blue sea, violet sky, white cloud, black space. A record's "
                   "groove, a tree's rings, the ear's cochlea.",
             **layers(), seconds=6.0),
    ]


def data():
    base = I.data()
    out = []
    for c in cands():
        p = base64.b64encode(np.round(np.asarray(c['path']) * 10000).astype('<i2').tobytes()).decode()
        rec = dict(key=c['key'], name=c['name'], line=c['line'], story=c['story'], style=c['style'], fill=c['fill'],
                   seconds=c['seconds'], path=p,
                   strokes=[list(map(int, s)) for s in c['strokes']], fills=c['fills'])
        if c['front'] is not None:
            rec['front'] = ''.join('1' if f else '0' for f in c['front'])
        out.append(rec)
    keep = ('word', 'letters', 'wordW', 'wordSw', 'clouds', 'paper', 'ink', 'dark', 'frost')
    return dict(cands=out, circles=[dict(name=c['name'], colour=c['colour'], tint=c['tint'], mode=c['mode']) for c in B.wheel()],
                **{k: base[k] for k in keep})


# ---- the static globes, as SVG (the animation's last frame) ----

def line_colour(col, light):
    if not light and col.upper() == '#F6F8F8':
        return '#C9CED0'                                  # Fog's white, a pale grey line on paper
    if light and col.upper() == '#34323A':
        return '#77757D'                                  # Smoke's black, a dim line as light
    return col


def svg(c, light=False, style=None, size=450):
    style = style or c['style']
    wh = B.wheel(); s = size / 2
    P = np.asarray(c['path']) * s
    ground = B.DARK if light else B.PAPER
    ink = B.PAPER if light else B.INK
    body = ''
    if style == 'filled' and c['fills']:
        fills = c['fills']
        layer = any(f.get('layer') for f in fills)
        order = sorted(fills, key=lambda f: -f['i0']) if layer else fills
        g = ''
        for f in order:
            w = wh[f['ci']]
            pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in P[f['i0']:f['i1'] + 1])
            if layer:
                col = w['colour'] if light else ('#FFFFFF' if w['mode'] == 'frost' else w['tint'])
                op = 0.9 if light else 1.0
                g += f'<polygon points="{pts} 0,0" fill="{col}" fill-opacity="{op}"/>'
            elif light:
                if w['mode'] == 'shade':
                    g += f'<polygon points="{pts}" fill="#000" fill-opacity="0.55"/>'
                else:
                    col, op = ('#FFFFFF', 0.55) if w['mode'] == 'frost' else (w['colour'], 0.85)
                    g += f'<polygon points="{pts}" fill="{col}" fill-opacity="{op}" style="mix-blend-mode:screen"/>'
            else:
                if w['mode'] == 'frost':
                    g += f'<polygon points="{pts}" fill="#FFFFFF" fill-opacity="{B.FROST}"/>'
                else:
                    g += f'<polygon points="{pts}" fill="{w["tint"]}" style="mix-blend-mode:multiply"/>'
        body += f'<g style="isolation:isolate">{g}</g>'
    lw = (0.045 if style == 'lines' else 0.014) * s
    front = c.get('front')
    for i0, i1, ci in c['strokes']:
        col = line_colour(wh[ci]['colour'], light) if style == 'lines' else ink
        seg = range(i0, i1 + 1)
        if front is None:
            pts = ' '.join(f'{P[i][0]:.1f},{P[i][1]:.1f}' for i in seg)
            body += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{lw:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'
            continue
        run, fr = [], None
        def flush(run, fr):
            if len(run) < 2:
                return ''
            pts = ' '.join(f'{P[i][0]:.1f},{P[i][1]:.1f}' for i in run)
            return (f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{lw * (1 if fr else 0.6):.2f}" '
                    f'stroke-opacity="{1 if fr else 0.3}" stroke-linecap="round" stroke-linejoin="round"/>')
        backs, fronts = '', ''
        for i in seg:
            f = bool(front[i])
            if fr is None or f == fr:
                run.append(i)
            else:
                if fr: fronts += flush(run + [i], fr)
                else: backs += flush(run + [i], fr)
                run = [i]
            fr = f
        if fr: fronts += flush(run, fr)
        else: backs += flush(run, fr)
        body = backs + body + fronts
    m = lw * 2
    vb = f'{-s - m:g} {-s - m:g} {2 * (s + m):g} {2 * (s + m):g}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{2 * (s + m):g}" height="{2 * (s + m):g}">'
            f'<rect x="{-s - m:g}" y="{-s - m:g}" width="{2 * (s + m):g}" height="{2 * (s + m):g}" fill="{ground}"/>{body}</svg>')


PAGE = r"""<title>EARF Globe</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=swap">
<style>
/* a screening room for five globes: the stage plays one; the strip below shows all five as they end */
:root {
  --page: #E9E5DE; --fg: #1C1A18; --muted: #5E5A53; --line: #CFC9BF; --screen: #F2EFEA; --screen-edge: #D9D3C9;
  --sans: 'Instrument Sans', Arial, sans-serif; --mono: 'IBM Plex Mono', 'Courier New', monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --page: #141311; --fg: #ECE8E1; --muted: #A39E95; --line: #34312C; --screen-edge: #2A2824; color-scheme: dark } }
:root[data-theme="dark"] { --page: #141311; --fg: #ECE8E1; --muted: #A39E95; --line: #34312C; --screen-edge: #2A2824;
  color-scheme: dark }
body { margin: 0; background: var(--page); color: var(--fg); font-family: var(--sans); font-size: 16px; line-height: 1.5;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 28px 48px }
main { max-width: 1080px; margin: 0 auto; display: grid; gap: 22px }
header { display: grid; gap: 6px }
.eyebrow { font-family: var(--mono); font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
h1 { margin: 0; font-size: clamp(30px, 5vw, 44px); line-height: 1.05; font-weight: 600; letter-spacing: -0.02em; text-wrap: balance }
header p { margin: 0; max-width: 64ch; color: var(--muted) }
.screen { position: relative; width: 100%; aspect-ratio: 16 / 9; background: var(--screen); border: 1px solid var(--screen-edge);
  border-radius: 4px; overflow: hidden }
.screen canvas { display: block; width: 100%; height: 100% }
.controls { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between }
.sets { display: flex; flex-wrap: wrap; gap: 12px }
.seg { display: inline-flex; flex-wrap: wrap; border: 1px solid var(--fg); border-radius: 22px; overflow: hidden }
.seg button, .play { font: 500 14px/1 var(--sans); color: var(--fg); background: transparent; border: 0; padding: 10px 14px; cursor: pointer }
.seg button[aria-pressed="true"] { background: var(--fg); color: var(--page) }
.play { border: 1px solid var(--fg); border-radius: 999px; display: inline-flex; gap: 8px; align-items: center }
.play svg { width: 12px; height: 12px; fill: currentColor }
button:focus-visible { outline: 2px solid var(--fg); outline-offset: 3px }
.now { display: grid; gap: 4px; border-top: 1px solid var(--line); padding-top: 16px }
.now h2 { margin: 0; font-size: 22px; font-weight: 600; letter-spacing: -0.01em }
.now .lede { margin: 0; font-weight: 500 }
.now p { margin: 0; max-width: 70ch; color: var(--muted) }
.strip { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; padding: 0; margin: 0; list-style: none }
.strip button { width: 100%; display: grid; gap: 6px; padding: 8px; border: 1px solid var(--line); border-radius: 6px;
  background: transparent; color: var(--fg); cursor: pointer; font: 500 13px/1.2 var(--sans); text-align: left }
.strip button[aria-pressed="true"] { border-color: var(--fg) }
.strip canvas { width: 100%; aspect-ratio: 1; display: block; border-radius: 3px }
@media (max-width: 640px) { .strip { grid-template-columns: repeat(3, minmax(0, 1fr)) } }
@media (max-width: 480px) { .seg button { padding: 9px 10px; font-size: 13px } }
.legend { display: flex; flex-wrap: wrap; gap: 10px 22px; padding: 0; margin: 0; list-style: none }
.legend li { display: flex; gap: 8px; align-items: center; font-size: 14px }
.legend .sw { width: 16px; height: 16px; border-radius: 50%; border: 2px solid var(--fg); box-sizing: border-box; flex: none }
.legend .num { font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; color: var(--muted) }
.notes { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px 28px; border-top: 1px solid var(--line); padding-top: 18px }
.notes h3 { margin: 0 0 4px; font-family: var(--mono); font-size: 12px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
.notes p { margin: 0; font-size: 15px; min-width: 0 }
html.capture body { padding: 0 }
html.capture main > :not(.screen) { display: none }
html.capture main { max-width: none; gap: 0 }
html.capture .screen { border: 0; border-radius: 0; width: 100vw; height: 100vh; aspect-ratio: auto }
</style>

<main>
  <header>
    <div class="eyebrow">EARF</div>
    <h1>The globe, as it draws itself</h1>
    <p>Five globes, each drawn by one dot in one unbroken line at one steady speed. Every stroke belongs to a circle, and
      the last frame is the logo, so the globe and its ident are one thing.</p>
  </header>
  <div class="screen"><canvas id="stage" aria-label="A dot draws EARF's globe in one line, each circle taking a Cloud's colour, then the word EARF beside it"></canvas></div>
  <div class="controls">
    <div class="sets">
      <div class="seg" role="group" aria-label="Globe" id="cands"></div>
      <div class="seg" role="group" aria-label="Ground">
        <button type="button" id="g-paper" aria-pressed="true">Paper</button>
        <button type="button" id="g-light" aria-pressed="false">Light</button>
      </div>
      <div class="seg" role="group" aria-label="Style">
        <button type="button" id="s-lines" aria-pressed="true">Lines</button>
        <button type="button" id="s-filled" aria-pressed="false">Filled</button>
      </div>
    </div>
    <button type="button" class="play" id="play"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1l9 5-9 5z"/></svg>Play again</button>
  </div>
  <section class="now" aria-live="polite">
    <h2 id="now-name"></h2>
    <p class="lede" id="now-line"></p>
    <p id="now-story"></p>
  </section>
  <ul class="strip" id="strip"></ul>
  <ul class="legend" id="legend"></ul>
  <section class="notes">
    <div><h3>One line</h3><p>Where two circles cross, the dot veers through a turn too short to see. Where it must reach
      another circle, it runs on along a line it has already drawn. So it never stops, never turns a corner, and never
      leaves a stroke outside a circle.</p></div>
    <div><h3>One speed</h3><p>The dot keeps one speed the whole way, measured along the line. It speeds up once as it
      starts and slows once as it ends.</p></div>
    <div><h3>Lines and filled</h3><p>Lines: each circle drawn in its Cloud's colour. Filled: each circle's tint sweeps in
      behind the dot. On paper the tints multiply where they overlap, as tinted acrylic does. As light, the colours add
      towards white.</p></div>
  </section>
</main>

<script>
const D = __DATA__;
const cv = document.getElementById('stage');
let ctx = cv.getContext('2d');
const VW = 1920, VH = 1080, TAU = 2 * Math.PI, PEN = 0.042;
let cand = 0, ground = 'paper', style = null, TL = null, t0 = performance.now(), shown = 0, raf = 0;
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (location.hash.startsWith('#capture')) document.documentElement.classList.add('capture');

const clamp01 = x => Math.max(0, Math.min(1, x));
const sine = x => x <= 0 ? 0 : x >= 1 ? 1 : (1 - Math.cos(Math.PI * x)) / 2;
const out = x => x <= 0 ? 0 : x >= 1 ? 1 : Math.sin(Math.PI * x / 2);
const lerp = (a, b, k) => a + (b - a) * k;
const span = (t, w) => clamp01((t - w[0]) / (w[1] - w[0]));
function cruise(x, a = 0.05) {
  if (x <= 0) return 0;
  if (x >= 1) return 1;
  const v = 1 / (1 - a), ramp = u => v * (u / 2 - a / (2 * Math.PI) * Math.sin(Math.PI * u / a));
  return x < a ? ramp(x) : x > 1 - a ? 1 - ramp(1 - x) : v * (x - a / 2);
}

// each globe's path as points, with the length run along it (the dot's steady speed is measured on it)
for (const c of D.cands) {
  const q = new Int16Array(Uint8Array.from(atob(c.path), ch => ch.charCodeAt(0)).buffer);   // x, y in 1/10000s
  const n = q.length / 2, X = new Float32Array(n), Y = new Float32Array(n), L = new Float32Array(n);
  for (let i = 0; i < n; i++) { X[i] = q[2 * i] / 1e4; Y[i] = q[2 * i + 1] / 1e4; if (i) L[i] = L[i - 1] + Math.hypot(X[i] - X[i - 1], Y[i] - Y[i - 1]); }
  Object.assign(c, { n, X, Y, L, total: L[n - 1] });
  c.front = c.front ? Uint8Array.from(c.front, ch => ch === '1') : null;
}

function timeline(c) {
  const T = { appear: [0.15, 0.5], draw: [0.3, 0.3 + c.seconds] };
  const t = T.draw[1];
  Object.assign(T, { slide: [t - 0.05, t + 0.9], word: [t + 0.55, t + 2.0], tag: [t + 1.8, t + 2.5], end: t + 2.9 });
  return T;
}

// where the dot is: the index it has passed and its point, for a length s along the path
function at(c, s) {
  let lo = 0, hi = c.n - 1;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (c.L[m] <= s) lo = m; else hi = m; }
  const seg = c.L[hi] - c.L[lo], f = seg > 0 ? clamp01((s - c.L[lo]) / seg) : 0;
  return { i: lo, x: lerp(c.X[lo], c.X[hi], f), y: lerp(c.Y[lo], c.Y[hi], f), front: c.front ? c.front[lo] : 1 };
}

function lineColour(col) {
  if (ground === 'paper' && col.toUpperCase() === '#F6F8F8') return '#C9CED0';
  if (ground === 'light' && col.toUpperCase() === '#34323A') return '#77757D';
  return col;
}

function paint(w, k = 1) {
  const light = ground === 'light';
  if (light && w.mode === 'shade') { ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 0.55 * k; ctx.fillStyle = '#000'; }
  else if (light) { ctx.globalCompositeOperation = 'screen'; ctx.globalAlpha = w.mode === 'frost' ? 0.55 : 0.85; ctx.fillStyle = w.mode === 'frost' ? '#FFF' : w.colour; }
  else if (w.mode === 'frost') { ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = D.frost * k; ctx.fillStyle = '#FFF'; }
  else { ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = 1; ctx.fillStyle = w.tint; }
}

function trace(c, i0, i1, pen) {               // the path from i0 to i1, ending at the dot if it is inside
  ctx.moveTo(c.X[i0], c.Y[i0]);
  for (let i = i0 + 1; i <= i1; i++) ctx.lineTo(c.X[i], c.Y[i]);
  if (pen) ctx.lineTo(pen.x, pen.y);
}

function drawGlobe(c, p, penR, full) {
  const light = ground === 'light', st = style || c.style, now = full ? c.n : p.i;
  // the fills: each sweeps in from its centre behind the dot (layers: the bands, outer first, each inner on top)
  if (st === 'filled' && c.fills.length) {
    const layer = c.fills.some(f => f.layer);
    const list = layer ? [...c.fills].reverse() : c.fills;
    ctx.save();
    for (const f of list) {
      if (now <= f.i0) continue;
      const done = now >= f.i1, w = D.circles[f.ci];
      ctx.beginPath(); ctx.moveTo(f.c[0], f.c[1]);
      trace(c, f.i0, done ? f.i1 : now, done ? null : p); ctx.closePath();
      if (layer) {
        ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = light ? 0.9 : 1;
        ctx.fillStyle = light ? w.colour : (w.mode === 'frost' ? '#FFF' : w.tint);
      } else paint(w);
      ctx.fill();
    }
    ctx.restore();
  }
  // the lines: each circle's own colour (lines), or one line (filled); the far side of the orbits faint
  ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const lw = st === 'lines' ? 0.045 : 0.014;
  const passes = c.front ? [0, 1] : [1];
  for (const pass of passes) {
    for (const [i0, i1, ci] of c.strokes) {
      if (now <= i0) continue;
      const end = Math.min(i1, now), inside = !full && now < i1;
      ctx.strokeStyle = st === 'lines' ? lineColour(D.circles[ci].colour) : (light ? D.paper : D.ink);
      ctx.globalAlpha = pass ? (st === 'lines' || !light ? 1 : 0.85) : 0.3;
      ctx.lineWidth = pass ? lw : lw * 0.6;
      if (!c.front) { ctx.beginPath(); trace(c, i0, end, inside ? p : null); ctx.stroke(); continue; }
      ctx.beginPath();
      let on = false;
      for (let i = i0; i <= end; i++) {
        const f = c.front[i] === pass;
        if (f && !on) { ctx.moveTo(c.X[i], c.Y[i]); on = true; } else if (f) ctx.lineTo(c.X[i], c.Y[i]); else on = false;
      }
      if (inside && on && (p.front ? 1 : 0) === pass) ctx.lineTo(p.x, p.y);
      ctx.stroke();
    }
  }
  ctx.restore();
  if (penR > 0) {
    ctx.save(); ctx.fillStyle = light ? D.paper : D.ink;
    if (c.front && !p.front) ctx.globalAlpha = 0.45;
    ctx.beginPath(); ctx.arc(p.x, p.y, penR * (c.front && !p.front ? 0.7 : 1), 0, TAU); ctx.fill(); ctx.restore();
  }
}

function layout() {
  const s = 0.78, ww = 450 + 110 + D.wordW, x0 = (VW - ww * s) / 2;
  return { solo: { cx: VW / 2, cy: VH / 2, R: 330 }, lock: { cx: x0 + 225 * s, cy: VH / 2, R: 225 * s },
           word: { x: x0 + (450 + 110) * s, s, capTop: VH / 2 - (300 * s + 30 + 21) / 2 } };
}

function outline(p) {
  ctx.beginPath();
  if (p.c) { ctx.arc(p.c[0], p.c[1], p.r, -Math.PI / 2, 1.5 * Math.PI); return TAU * p.r; }
  let L = 0;
  p.pts.forEach((q, i) => { if (i) L += Math.hypot(q[0] - p.pts[i - 1][0], q[1] - p.pts[i - 1][1]); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); });
  const a = p.pts[p.pts.length - 1], b = p.pts[0]; L += Math.hypot(a[0] - b[0], a[1] - b[1]); ctx.closePath();
  return L;
}

function drawWord(k, Ly) {
  if (k <= 0) return;
  ctx.save(); ctx.translate(Ly.word.x, Ly.word.capTop); ctx.scale(Ly.word.s, Ly.word.s);
  ctx.strokeStyle = ground === 'light' ? D.paper : D.ink; ctx.lineWidth = D.wordSw; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  D.word.forEach((p, i) => {
    const q = cruise(clamp01((k - D.letters[i] * 0.16) / 0.52), 0.25);
    if (q <= 0) return;
    const L = outline(p);
    ctx.setLineDash(q >= 1 ? [] : [L * q, L + 1]); ctx.stroke();
  });
  ctx.restore();
}

function drawTag(k, Ly) {
  if (k <= 0) return;
  const text = 'NEATURE-INSPIRED LOUDSPEAKERS', size = 30, track = 0.12 * size;
  ctx.save(); ctx.globalAlpha = k; ctx.fillStyle = ground === 'light' ? D.paper : D.ink;
  ctx.font = `500 ${size}px 'IBM Plex Mono', 'Courier New', monospace`; ctx.textBaseline = 'alphabetic';
  let x = Ly.word.x - 2, y = Ly.word.capTop + 300 * Ly.word.s + 30 + 21 + (1 - k) * 10;
  for (const ch of text) { ctx.fillText(ch, x, y); x += ctx.measureText(ch).width + track; }
  ctx.restore();
}

function render(t) {
  shown = t;
  const c = D.cands[cand], Ly = layout();
  const s = cruise(span(t, TL.draw)) * c.total, p = at(c, s);
  const lift = 1 - sine(clamp01((span(t, TL.draw) - 0.94) / 0.06));
  const penR = PEN * out(span(t, TL.appear)) * lift;
  const slide = sine(span(t, TL.slide));
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
  ctx.fillStyle = ground === 'light' ? D.dark : D.paper; ctx.fillRect(0, 0, cv.width, cv.height);
  const k = cv.width / VW; ctx.scale(k, k);
  const cx = lerp(Ly.solo.cx, Ly.lock.cx, slide), cy = lerp(Ly.solo.cy, Ly.lock.cy, slide), R = lerp(Ly.solo.R, Ly.lock.R, slide);
  ctx.save(); ctx.translate(cx, cy); ctx.scale(R, R); drawGlobe(c, p, penR, span(t, TL.draw) >= 1); ctx.restore();
  drawWord(span(t, TL.word), Ly); drawTag(out(span(t, TL.tag)), Ly);
  ctx.restore();
}

// the strip: each globe as it ends, small, on the current ground
function thumbs() {
  const real = ctx, was = cand;
  document.querySelectorAll('#strip canvas').forEach((tc, i) => {
    const r = tc.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
    tc.width = Math.round((r.width || 160) * dpr); tc.height = tc.width;
    ctx = tc.getContext('2d');
    ctx.fillStyle = ground === 'light' ? D.dark : D.paper; ctx.fillRect(0, 0, tc.width, tc.height);
    ctx.save(); ctx.translate(tc.width / 2, tc.height / 2); ctx.scale(tc.width * 0.44, tc.width * 0.44);
    cand = i; drawGlobe(D.cands[i], { i: D.cands[i].n - 1, x: 0, y: 0, front: 1 }, 0, true);
    ctx.restore();
  });
  ctx = real; cand = was;
}

function size() {
  const dpr = Math.min(2, window.devicePixelRatio || 1), w = cv.clientWidth || 960;
  cv.width = Math.round(w * dpr); cv.height = Math.round(w * dpr * VH / VW);
}
function loop(now) {
  const t = (now - t0) / 1000;
  render(Math.min(t, TL.end));
  if (t < TL.end) raf = requestAnimationFrame(loop);
}
function play() { cancelAnimationFrame(raf); t0 = performance.now(); raf = requestAnimationFrame(loop); }

function set(ci, g, s) {
  cand = ci; ground = g; style = s; TL = timeline(D.cands[ci]);
  const c = D.cands[ci], st = style || c.style;
  document.querySelectorAll('#cands button').forEach((b, i) => b.setAttribute('aria-pressed', String(i === ci)));
  document.querySelectorAll('#strip button').forEach((b, i) => b.setAttribute('aria-pressed', String(i === ci)));
  for (const id of ['paper', 'light']) document.getElementById('g-' + id).setAttribute('aria-pressed', String(id === g));
  for (const id of ['lines', 'filled']) {
    const b = document.getElementById('s-' + id);
    b.setAttribute('aria-pressed', String(id === st)); b.disabled = id === 'filled' && !c.fill;
  }
  document.getElementById('now-name').textContent = c.name;
  document.getElementById('now-line').textContent = c.line;
  document.getElementById('now-story').textContent = c.story;
}
function choose(ci, g, s) { set(ci, g, s); thumbs(); reduce ? render(TL.end) : play(); }

document.getElementById('cands').innerHTML = D.cands.map((c, i) => `<button type="button" aria-pressed="${i === 0}">${c.name}</button>`).join('');
document.getElementById('strip').innerHTML = D.cands.map(c => `<li><button type="button" aria-label="${c.name}"><canvas></canvas>${c.name}</button></li>`).join('');
document.querySelectorAll('#cands button').forEach((b, i) => b.addEventListener('click', () => choose(i, ground, null)));
document.querySelectorAll('#strip button').forEach((b, i) => b.addEventListener('click', () => choose(i, ground, null)));
document.getElementById('g-paper').addEventListener('click', () => choose(cand, 'paper', style));
document.getElementById('g-light').addEventListener('click', () => choose(cand, 'light', style));
document.getElementById('s-lines').addEventListener('click', () => choose(cand, ground, 'lines'));
document.getElementById('s-filled').addEventListener('click', () => choose(cand, ground, 'filled'));
document.getElementById('play').addEventListener('click', play);
document.getElementById('legend').innerHTML = D.clouds.map(c =>
  `<li><span class="sw" style="background:${c.colour}"></span><span class="num">${c.num}</span>${c.name}</li>`).join('');
window.addEventListener('resize', () => { size(); render(shown); thumbs(); });
window.__frame = (t, ci, g, s) => { set(ci ?? cand, g || ground, s === undefined ? style : s); render(t); return TL.end; };
window.__cands = D.cands.map(c => c.key);

set(0, 'paper', null); size();
(document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => {
  if (document.documentElement.classList.contains('capture')) { size(); render(0); return; }
  thumbs(); reduce ? render(TL.end) : play();
});
</script>
"""


def page():
    return PAGE.replace('__DATA__', json.dumps(data(), separators=(',', ':')))


def standalone():
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, '
            'initial-scale=1, viewport-fit=cover"></head><body>\n' + page() + '\n</body></html>\n')


def video(out_dir, ci, key, ground, fonts=None, fps=30, w=1280, h=720):
    """One globe's ident to an MP4, frame by frame through the page's __frame (as ident.py's)."""
    tmp = tempfile.mkdtemp(prefix='globe-')
    html = os.path.join(tmp, 'globes.html')
    doc = standalone()
    if fonts:
        doc = doc.replace('</head>', '<style>' + open(fonts).read() + '</style></head>')
    open(html, 'w').write(doc)
    js = os.path.join(tmp, 'cap.js')
    open(js, 'w').write(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {w}, height: {h} }}, deviceScaleFactor: 1 }});
  await p.goto('file://{html}#capture', {{ waitUntil: 'networkidle' }});
  await p.evaluate(() => document.fonts.ready);
  const end = await p.evaluate(([c, g]) => window.__frame(0, c, g, null), [{ci}, '{ground}']);
  const n = Math.ceil((end + 0.6) * {fps});
  for (let i = 0; i < n; i++) {{
    await p.evaluate(([t, c, g]) => window.__frame(t, c, g, null), [i / {fps}, {ci}, '{ground}']);
    await p.screenshot({{ path: '{tmp}/f' + String(i).padStart(4, '0') + '.png' }});
  }}
  await b.close(); console.log(n);
}})();
""")
    r = subprocess.run(['node', js], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])
    mp4 = os.path.join(out_dir, f'globe-{key}-{ground}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', mp4], check=True)
    shutil.rmtree(tmp)
    return mp4


def reel(out_dir, keys, ground):
    """The five idents of one ground end to end."""
    lst = os.path.join(out_dir, f'.reel-{ground}.txt')
    open(lst, 'w').write(''.join(f"file '{os.path.join(out_dir, f'globe-{k}-{ground}.mp4')}'\n" for k in keys))
    mp4 = os.path.join(out_dir, f'globes-{ground}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                    '-movflags', '+faststart', mp4], check=True)
    os.remove(lst)
    return mp4


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--fragment', help='also write the page as an Artifact body to this path')
    ap.add_argument('--video', action='store_true', help='also write an MP4 of each globe on each ground, and the reels')
    ap.add_argument('--fonts', help='a local @font-face sheet for the videos, where Google Fonts cannot be reached')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    cs = cands()
    for c in cs:
        for light in (False, True):
            open(os.path.join(OUT, f'globe-{c["key"]}' + ('-light' if light else '') + '.svg'), 'w').write(svg(c, light))
    open(os.path.join(OUT, 'globes.html'), 'w').write(standalone())
    if a.fragment:
        open(a.fragment, 'w').write(page())
    print('brand/globes.html, ' + ', '.join(f'brand/globe-{c["key"]}[-light].svg' for c in cs))
    if a.video:
        keys = [c['key'] for c in cs]
        for g in ('paper', 'light'):
            for i, k in enumerate(keys):
                print(os.path.relpath(video(OUT, i, k, g, a.fonts), HERE))
            print(os.path.relpath(reel(OUT, keys, g), HERE))


if __name__ == '__main__':
    main()
