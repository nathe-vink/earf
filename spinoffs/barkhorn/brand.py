"""EARF's logo in the Clouds' colours (round 18, the owner: "a version of the logo and letters that includes all of the
speaker colors, either as unfilled strokes or as the colored in portions of each shape that happens as a result of the
overlapping strokes"). The globe and the wordmark from marks.py, three ways:

- strokes: no fills, each shape's outline in a speaker's colour (on paper, and on ink, where Fog's white shows and
  Smoke's black would not);
- acrylic: each shape filled with a speaker's colour, the fills multiplied where they overlap, as tinted acrylic
  sheets laid one over another do (the Clouds' own material), the ink outlines over them;
- glass: every region the overlapping outlines cut out filled with its own colour, no two that touch alike, the ink
  outlines over them, as a leaded window is;
- wheel (round 20, the owner: "I wonder if the earth can be formed a different way, like overlapping concentric circles
  that form a larger circle, kind of like a color wheel"): the globe as the eight Clouds' circles round one centre,
  each passing through it, together one larger circle; in the acrylics' own tints laid over one another, or as light
  on a dark ground. ident.py animates it.

    python3 spinoffs/barkhorn/brand.py      ->  brand/<variant>.svg and brand/sheet.html (needs shapely for glass)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import marks as M                                         # noqa: E402

OUT = os.path.join(HERE, 'brand')
PAPER, INK = '#F2EFEA', M.INK
CLOUDS = [(name, colour) for key, line, num, name, colour in M.SPEAKERS if line == 'Cloud']   # the spectrum, Flare to Smoke
PAPER_SET = [c for n, c in CLOUDS if n != 'Fog']          # Fog's white is lost on paper; it shows on ink
INK_SET = [c for n, c in CLOUDS if n != 'Smoke']          # and Smoke's black on ink


def globe_prims():
    """The globe's shapes as plain primitives, each with whether the sphere clips it."""
    sphere, meridians, band = M.GLOBE
    return [(p, False) for p in sphere[0]] + [(p, True) for p in meridians[0]] + [(p, True) for p in band[0]]


def word_prims(dx, k=1.0):
    return [(M.place([p], k=k, dx=dx)[0], False) for p in M.WORDMARK]


def lockup(globe_k=450 / 704):
    """The lockup's shapes on one artboard: the globe (1.5 cap heights across) left, the wordmark right, as
    marks.lockup_svg sets them. Returns [(primitive, clipped by the sphere), ...], the sphere's (cx, cy, r) and the
    artboard (x0, y0, w, h)."""
    g = globe_k
    gx, gy = 225, 150                                    # the globe's centre: the letters' cap height is 300
    out = []
    for p, clip in globe_prims():
        q = M.place([p], k=g, dx=gx, dy=gy)[0]
        out.append((q, clip))
    out += word_prims(450 + 110)
    return out, (gx, gy, M.GLOBE_R * g), (-30, -100, 450 + 110 + M.WORDMARK_W + 60, 500)


def svg_el(p, attrs):
    return M._el(p, attrs)


def stroke_width(p):
    return M.U * 0.8


def page(body, vb, bg):
    x0, y0, w, h = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}">'
            f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def clip_defs(sphere, uid):
    cx, cy, r = sphere
    return f'<defs><clipPath id="{uid}"><circle cx="{cx:g}" cy="{cy:g}" r="{r:g}"/></clipPath></defs>'


def strokes(on_ink=False):
    prims, sphere, vb = lockup()
    colours = INK_SET if on_ink else PAPER_SET
    body = clip_defs(sphere, 'cut')
    for i, (p, clip) in enumerate(prims):
        el = svg_el(p, f'fill="none" stroke="{colours[i % len(colours)]}" stroke-width="{stroke_width(p):g}" stroke-linejoin="round"')
        body += f'<g clip-path="url(#cut)">{el}</g>' if clip else el
    return page(body, vb, INK if on_ink else PAPER)


def acrylic(outline=True):
    prims, sphere, vb = lockup()
    colours = PAPER_SET
    body = clip_defs(sphere, 'cut') + '<g style="isolation:isolate">'
    for i, (p, clip) in enumerate(prims):
        el = svg_el(p, f'fill="{colours[i % len(colours)]}" fill-opacity="0.78" style="mix-blend-mode:multiply"')
        body += f'<g clip-path="url(#cut)">{el}</g>' if clip else el
    body += '</g>'
    if outline:
        for p, clip in prims:
            el = svg_el(p, f'fill="none" stroke="{INK}" stroke-width="{stroke_width(p):g}" stroke-linejoin="round"')
            body += f'<g clip-path="url(#cut)">{el}</g>' if clip else el
    return page(body, vb, PAPER)


def _shape(p, sphere=None):
    """A primitive as a shapely polygon (clipped by the sphere, itself a polygon, where asked). The sphere is one
    polygon throughout, so the shapes it clips share its edges exactly and leave no slivers."""
    from shapely.geometry import Point, Polygon, box
    if p[0] == 'circle' and sphere is not None and (p[1], p[2], p[3]) == sphere[:3]:
        return sphere[3]
    if p[0] == 'circle':
        g = Point(p[1], p[2]).buffer(p[3], 256)
    elif p[0] == 'rect':
        g = box(p[1], p[2], p[3], p[4])
    elif p[0] == 'dee':
        r = (p[4] - p[2]) / 2
        half = Point(p[3], p[2] + r).buffer(r, 256).intersection(box(p[3], p[2], p[3] + r, p[4]))
        g = box(p[1], p[2], p[3], p[4]).union(half)
    else:
        g = Polygon(p[1:])
    if sphere is not None:
        g = g.intersection(sphere[3])
    return g


def glass():
    """Every face of the outlines' arrangement filled, no two faces that share an edge alike (a greedy colouring)."""
    from shapely.geometry import mapping
    from shapely.ops import polygonize, unary_union
    from shapely.geometry import Point
    prims, sphere, vb = lockup()
    ball = sphere + (Point(sphere[0], sphere[1]).buffer(sphere[2], 256),)
    shapes = [_shape(p, ball) if clip or (p[0] == 'circle' and (p[1], p[2], p[3]) == sphere) else _shape(p) for p, clip in prims]
    union = unary_union(shapes)
    faces = [f for f in polygonize(unary_union([s.boundary for s in shapes]))
             if f.area > 30 and union.buffer(1e-6).contains(f.representative_point())]    # no hairline slivers
    faces.sort(key=lambda f: (round(f.centroid.x, 1), round(f.centroid.y, 1)))
    colours = [c for n, c in CLOUDS]
    picked = []
    for i, f in enumerate(faces):
        near = {picked[j] for j in range(i) if f.boundary.intersection(faces[j].boundary).length > 1.0}   # an edge shared
        order = [(i + k) % len(colours) for k in range(len(colours))]   # spread the colours round the word
        picked.append(next((c for c in order if c not in near), order[0]))
    body = clip_defs(sphere, 'cut')
    for f, ci in zip(faces, picked):
        rings = [f.exterior] + list(f.interiors)
        d = ' '.join('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in r.coords) + ' Z' for r in rings)
        body += f'<path d="{d}" fill="{colours[ci]}" fill-rule="evenodd"/>'
    for p, clip in prims:
        el = svg_el(p, f'fill="none" stroke="{INK}" stroke-width="{stroke_width(p):g}" stroke-linejoin="round"')
        body += f'<g clip-path="url(#cut)">{el}</g>' if clip else el
    return page(body, vb, PAPER), len(faces)


# the wheel (round 20): the eight Clouds' circles round a centre, each passing through it, so together they form one
# larger circle with no hub and no rim (the owner, of a first try with both: "It's too much like a film reel"). Radii
# are of that larger circle, 1: each circle's is 1/2 and its centre is 1/2 out, at -90 + 45 i degrees (from the top,
# clockwise on screen). On paper each is filled with its Cloud's own acrylic tint (the colour product.py gives the sheet
# through 25 mm), the tints multiplied where they overlap as the sheets would be laid one on another, Fog's frosted
# white over what lies under it; as light, on a dark ground, the speakers' colours add towards white and Smoke's black
# shades what it covers.
FLAVOUR = {'red': 'cloud-red', 'orange': 'cloud-orange', 'amber': 'cloud-amber', 'green': 'eucalyptus-y2k-green',
           'blue': 'cloud-blue', 'violet': 'cloud-violet', 'ice': 'birch-y2k-ice', 'black': 'cloud-black'}
FROST = 0.7                                                      # Fog's white, laid over what is beneath
WHEEL_SW = 0.022                                                 # the circles' outline, of the larger circle's radius
DARK = '#121114'                                                 # the ground of the light version


def tints():
    import product
    return {k: product.VARIANTS[f]['materials']['bark']['deep'] for k, f in FLAVOUR.items()}


def wheel():
    """The wheel's circles in drawing order: dicts of name, key, colour (the mark's), tint (the acrylic's), mode
    ('frost' for Fog, 'shade' for Smoke as light, else 'tint'), cx, cy, r and a0, the angle of its outermost point,
    where the pen starts it."""
    t = tints()
    out = []
    for i, (key, line, num, name, col) in enumerate([s for s in M.SPEAKERS if s[1] == 'Cloud']):
        a = math.radians(-90 + 45 * i)
        out.append(dict(name=name, key=key, colour=col, tint=t[key], cx=0.5 * math.cos(a), cy=0.5 * math.sin(a), r=0.5, a0=a,
                        mode={'Fog': 'frost', 'Smoke': 'shade'}.get(name, 'tint')))
    return out


def wheel_svg(size=450, light=False, with_bg=True):
    """The wheel at `size` across (the lockup's globe is 450): on paper in the acrylics' tints, or as light."""
    s = size / 2
    sw = WHEEL_SW * s
    def circ(c, attrs):
        return f'<circle cx="{c["cx"] * s:.2f}" cy="{c["cy"] * s:.2f}" r="{c["r"] * s:.2f}" {attrs}/>'
    def fill(c):
        if light:
            if c['mode'] == 'shade':
                return 'fill="#000000" fill-opacity="0.55"'
            col = '#FFFFFF' if c['mode'] == 'frost' else c['colour']
            return f'fill="{col}" fill-opacity="{0.55 if c["mode"] == "frost" else 0.8}" style="mix-blend-mode:screen"'
        if c['mode'] == 'frost':
            return f'fill="#FFFFFF" fill-opacity="{FROST}"'
        return f'fill="{c["tint"]}" style="mix-blend-mode:multiply"'
    cl = wheel()
    body = '<g style="isolation:isolate">' + ''.join(circ(c, fill(c)) for c in cl) + '</g>'
    line = f'fill="none" stroke="{PAPER if light else INK}" stroke-width="{sw:.2f}"' + (' stroke-opacity="0.85"' if light else '')
    body += ''.join(circ(c, line) for c in cl)
    m = sw
    vb = f'{-s - m:g} {-s - m:g} {2 * (s + m):g} {2 * (s + m):g}'
    bg = f'<rect x="{-s - m:g}" y="{-s - m:g}" width="{2 * (s + m):g}" height="{2 * (s + m):g}" fill="{DARK if light else PAPER}"/>' if with_bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{2 * (s + m):g}" height="{2 * (s + m):g}">{bg}{body}</svg>'


def wheel_lockup(light=False):
    """The wheel beside the wordmark as marks.lockup_svg sets the globe (450 across, 110 gap, the letters' cap 300
    centred on it), the letters drawn as outlines."""
    g = wheel_svg(light=light, with_bg=False)
    inner = g[g.index('>') + 1:g.rindex('</svg>')]
    sw = M.U * 0.8                                   # the letters' outline
    ink, ground = (PAPER, DARK) if light else (INK, PAPER)
    word = ''.join(svg_el(p, f'fill="none" stroke="{ink}" stroke-width="{sw:g}" stroke-linejoin="round"') for p in M.WORDMARK)
    w, h = 450 + 110 + M.WORDMARK_W + 2 * sw, 450 + 2 * sw
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-sw:g} {-sw:g} {w:g} {h:g}" width="{w:g}" height="{h:g}">'
            f'<rect x="{-sw:g}" y="{-sw:g}" width="{w:g}" height="{h:g}" fill="{ground}"/>'
            f'<g transform="translate(225 225)">{inner}</g><g transform="translate({450 + 110} 75)">{word}</g></svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    variants = [('strokes', 'Strokes', 'each outline in a speaker\'s colour, no fills', strokes()),
                ('strokes-ink', 'Strokes, on ink', 'Fog\'s white shows (Smoke\'s black left out)', strokes(on_ink=True)),
                ('acrylic', 'Acrylic', 'each shape tinted, the tints multiplied where they overlap', acrylic()),
                ('acrylic-bare', 'Acrylic, no outlines', 'the tints alone', acrylic(outline=False))]
    try:
        svg, n = glass()
        variants.append(('glass', 'Glass', f'each of the {n} regions the outlines cut out in its own colour', svg))
    except ImportError:
        print('glass needs shapely (pip install shapely); left out')
    variants += [('wheel', 'Wheel', 'the eight Clouds\' circles through one centre, in their acrylics\' tints (round 20)',
                  wheel_lockup()),
                 ('wheel-light', 'Wheel, as light', 'the speakers\' colours adding towards white; Smoke\'s black shades (round 20)',
                  wheel_lockup(light=True))]
    for key, *_ , svg in variants:
        open(os.path.join(OUT, f'{key}.svg'), 'w').write(svg)
    open(os.path.join(OUT, 'globe-wheel.svg'), 'w').write(wheel_svg())
    open(os.path.join(OUT, 'globe-wheel-light.svg'), 'w').write(wheel_svg(light=True))
    now = M.lockup_svg(size=None)
    rows = ''.join(f'<div class="row"><div class="cap"><b>{t}</b><br>{d}</div><div class="art">{s}</div></div>'
                   for _, t, d, s in [('now', 'As now', 'ocean and land', now)] + variants)
    open(os.path.join(OUT, 'sheet.html'), 'w').write(
        '<!doctype html><meta charset="utf-8"><title>EARF in the Clouds\' colours</title><style>body{margin:0;padding:24px;'
        'background:#E9E5DE;font:15px/1.4 Arial,sans-serif;color:#1C1A18}.row{display:flex;align-items:center;gap:24px;'
        'margin:0 0 18px}.cap{width:220px}.art svg{width:900px;height:auto;display:block}</style>'
        f'<h2 style="margin:0 0 16px">EARF in the Clouds\' colours (rounds 18 to 20)</h2>{rows}')
    print(len(variants), 'variants in', os.path.relpath(OUT, HERE))


if __name__ == '__main__':
    main()
