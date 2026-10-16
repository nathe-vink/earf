"""EARF: the logo, and one mark for each speaker, drawn as stacked clear acrylic.

Round 10, the owner, of the cloud: "These acrylic marks, without the circular framing (ie just the geometric cloud), are
great. Representative of the speaker design and theme." Then: "Acrylic style marks for each theme, with a distinct
color for each speaker. Trees, Clouds, Stones ... And geometric shapes for each. The tree could be a vertical rectangle
with circles at the top", and: "I like the cloud because it combines multiple shapes and sizes with large enough gaps
between the overlapping strokes of each shape. The tree and stone need to accomplish the same thing ... For the stone we
could make an exception and do something more like the rock option, but that front left side looks too much like a
house shape."

- A line is one shape, built from a few primitives of different sizes: Bark a tree (a trunk and three circles), Cloud a
  cloud (three circles on a rectangle), Crag a crag (three slabs, parallelograms of three sizes leaning together; the
  owner, after a round of stones: "The cloud and the tree use very uniform shapes. The stone should do the same. Clean
  parallelograms, squares/rectangles, and triangles are best I think", then of the slabs: "I like this, but without the
  bottom rectangle").
- A speaker is its line's shape in its own colour.
- The acrylic: every primitive is filled, then every outline is drawn over all of them, U wide, so the construction
  shows through as if each piece were clear acrylic laid on the others.
- Like the cloud, the crag is three shapes of three sizes on one base line, where their lines merge.
- The logo (round 11, the owner: "Okay new brand idea EARF and the logo is a globe made of geometric shapes"; then, of
  the drafts: "I meant I liked B3, not B2", "B3 is still the strongest" and "B3 final for now"): the globe is B3, the cloud's ingredients
  in two colours: a circle of ocean, two equal circles of land cut by it, their arcs the meridians, and a band of ocean
  across them as the tropics, in the same acrylic style. Two options beside it, from the owner's next note: "C2 was
  also okay, but I'd prefer to have the shapes overlap and for the triangle to not look italicized. For that one, the
  continent doesn't need to look geographically correct. One other option is to put a triangle inside the circle and a
  square inside the triangle ..., with the points of each shape at the stroke of the outer shape, then coloring in the
  smaller shapes created as green or blue." So C2 overlapped: an upright (equilateral) triangle, a circle and a
  parallelogram (or a square) overlapping into one continent, no two outlines nearly meeting; and the nested globe:
  the triangle in the circle, the square standing in the triangle, each touching the outer shape, the regions between
  them ocean or land (and one more circle in the square, as "and so on"). EARF reads as earth, as ear and as a dog's
  arf.
- The wordmark: EARF built of the marks' primitives (rectangles, two leaning slabs and a bar for the A, a stem, a
  circle and a slab for the R), filled and outlined like the marks. The owner, of the first draft: "the top of the A
  shouldn't have the parallelograms protruding past each other. They should overlap cleanly at the very top. On the R,
  the parallelogram should come out more so it's flush with or just past the edge of the circle like it is in type."
  So the A's legs lean exactly enough that their tops coincide, and the R's leg ends just past the bowl.

    python3 spinoffs/barkhorn/marks.py

writes marks/<key>.svg for each speaker (transparent round it), marks/globe.svg (the logo), marks/earf.svg (the
wordmark), marks/earf-lockup.svg (the two side by side), marks/globe-<option>.svg for each option (c2-overlap,
c2-square, nested, nested-land, nested-circle, nested-mixed) and marks/sheet.html.
"""
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'marks')
INK = '#1C1A18'
U = 22                                               # the outline, on a 1000 artboard


def place(prims, k=1.0, dx=0.0, dy=0.0):
    """The primitives scaled by k and moved (dx, dy), so each shape sits optically centred at one size."""
    out = []
    for p in prims:
        if p[0] == 'circle':
            out.append(('circle', p[1] * k + dx, p[2] * k + dy, p[3] * k))
        elif p[0] in ('rect', 'dee'):
            out.append((p[0], p[1] * k + dx, p[2] * k + dy, p[3] * k + dx, p[4] * k + dy))
        elif p[0] == 'arc':                          # a stroke only: centre, radius, aim and half-span in degrees
            out.append(('arc', p[1] * k + dx, p[2] * k + dy, p[3] * k, p[4], p[5]))
        else:
            out.append(('poly',) + tuple((x * k + dx, y * k + dy) for x, y in p[1:]))
    return out


def slab(x0, base, w, h, lean):
    """A parallelogram standing on the base line (y down): w wide along it from x0, h tall, its sides leaning `lean`
    degrees from upright (positive to the right)."""
    dx = h * math.tan(math.radians(lean))
    return ('poly', (x0, base), (x0 + w, base), (x0 + w + dx, base - h), (x0 + dx, base - h))


# the cloud as approved: three circles and a rectangle from the outer two's centres down to their common tangent
CLOUD = place([('circle', -179, 35, 115), ('circle', -19, -67, 173), ('circle', 179, 19, 131), ('rect', -179, 35, 179, 150)],
              dy=45)
# the tree: a crown of three circles overlapping deeply, the trunk's top inside them (the owner: "The previous three tree
# was better. The two smaller circles feel too detached")
TREE = place([('rect', -44, -40, 44, 340), ('circle', 0, -210, 150), ('circle', -140, -70, 128), ('circle', 140, -70, 128)])
# the crag: three slabs, parallelograms of three sizes standing on the base line, the outer two leaning in and the tall
# one between them leaning with the left (the owner, of a draft with a rectangle across their feet: "I like this, but
# without the bottom rectangle")
_B = 170
STONE = place([slab(-330, _B, 190, 230, 20), slab(-170, _B, 260, 380, 12), slab(80, _B, 220, 290, -16)],
              k=0.96, dx=15, dy=20)
# EARF's globe (B3): the ocean a circle; two equal circles of land cut by it, their arcs the meridians; a band of ocean
# across them, the tropics. Each layer: (primitives, colour or None for lines only, cut by the sphere[, lines: False
# for a region's fill whose edges are other shapes' lines])
OCEAN, LAND, GLOBE_R = '#3F7CC4', '#6FA35A', 330
_SPHERE = ([('circle', 0, 0, GLOBE_R)], OCEAN, False)
_MERIDIANS = [('circle', -0.52 * GLOBE_R, 0, GLOBE_R), ('circle', 0.52 * GLOBE_R, 0, GLOBE_R)]
_BAND = ('rect', -GLOBE_R, -0.4 * GLOBE_R, GLOBE_R, 0.4 * GLOBE_R)
GLOBE = [_SPHERE, (_MERIDIANS, LAND, True), ([_BAND], OCEAN, True)]


def _tri(cx, base, side):
    """An equilateral triangle standing on its base (upright, not leaning)."""
    return ('poly', (cx - side / 2, base), (cx + side / 2, base), (cx, base - side * math.sqrt(3) / 2))


# C2 overlapped (options): an upright triangle, a circle and a parallelogram, or a square, overlapping into one
# continent of three sizes; placed by a search for no two outlines within 60 of each other and no crossing under 28
# degrees (as the marks: deep overlaps, no slivers)
C2_OVERLAP = [_SPHERE, ([_tri(-111.8, 70, 297.5), ('circle', 95, -40, 119.6), slab(-150, 220, 250, 250, 12)], LAND, True)]
C2_SQUARE = [_SPHERE, ([_tri(-113.9, 64.8, 295.1), ('circle', 92.8, -42.7, 118.8),
                        ('rect', -132.1, 230 - 220.8, -132.1 + 220.8, 230)], LAND, True)]
# the nested globe (options): an equilateral triangle in the circle, its corners on the circle; the square standing on
# the triangle's base, its top corners on the triangle's sides; the circle in the square, touching its sides
_T = [(0, -GLOBE_R), (GLOBE_R * math.sqrt(3) / 2, GLOBE_R / 2), (-GLOBE_R * math.sqrt(3) / 2, GLOBE_R / 2)]
_A, _H = GLOBE_R * math.sqrt(3), 1.5 * GLOBE_R
_S = _A * _H / (_A + _H)                             # the inscribed square's side
_TRI = ('poly',) + tuple(_T)
_SQ = ('rect', -_S / 2, GLOBE_R / 2 - _S, _S / 2, GLOBE_R / 2)
_IN = ('circle', 0, GLOBE_R / 2 - _S / 2, _S / 2)


def _beyond(p0, p1):
    """The sphere's segment beyond the chord p0-p1 (a polygon reaching past the sphere, cut by it)."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    k = 900 / (math.hypot(mx, my) or 1)
    return ('poly', p0, p1, (p1[0] + mx * k, p1[1] + my * k), (p0[0] + mx * k, p0[1] + my * k))


NESTED = [_SPHERE, ([_TRI], LAND, True), ([_SQ], OCEAN, True)]                 # ocean, land, ocean
NESTED_LAND = [([('circle', 0, 0, GLOBE_R)], LAND, False), ([_TRI], OCEAN, True), ([_SQ], LAND, True)]
NESTED_CIRCLE = NESTED + [([_IN], LAND, True)]                                # and one more circle in the square
NESTED_MIXED = [_SPHERE, ([_beyond(_T[2], _T[0]), _beyond(_T[0], _T[1])], LAND, True, False), ([_TRI], OCEAN, True),
                ([('poly', _T[0], (_S / 2, GLOBE_R / 2 - _S), (-_S / 2, GLOBE_R / 2 - _S))], LAND, True, False),
                ([_SQ], LAND, True)]                                          # the north land, the south ocean
OPTIONS = [('c2-overlap', 'C2 overlapped', 'an upright triangle, a circle, a parallelogram', C2_OVERLAP),
           ('c2-square', 'C2 overlapped, a square', 'nothing leaning', C2_SQUARE),
           ('nested', 'Nested', 'ocean, land, ocean', NESTED),
           ('nested-land', 'Nested', 'land, ocean, land', NESTED_LAND),
           ('nested-circle', 'Nested, and a circle', 'ocean, land, ocean, land', NESTED_CIRCLE),
           ('nested-mixed', 'Nested', 'land north, ocean south', NESTED_MIXED)]


def _wordmark():
    """EARF on a cap height of 300 (y down from the cap line), stems 100 wide. Returns the primitives and the width.

    The rules every letter keeps (round 18, the owner: "We should update the other letters to make sure they all follow
    the same conventions based on how we update the R"; round 19: "it should still be a circle but the vertical
    rectangle could be slightly wider to achieve the same effect"):
    - the R's bowl is a circle whose top touches the cap line exactly where its stem ends, so the cap line runs flat
      from the stem into the circle with no notch; the circle must also stay inside the stem's left edge, which sets the
      stems at 100 (round 18's 74 left a notch); every stem is 100, the E's and the F's too;
    - every bar starts at its stem's outer edge and runs flat, 70 deep;
    - the middle bars (E, F) and the R's bowl end on one line, 185 down; the A's crossbar sits lower, 215 to 285 (round
      26: with its legs closer, a crossbar on the 185 line would all but close the triangle inside), and runs from the
      middle of one leg to the middle of the other at its top, so its ends stay inside the legs;
    - the diagonals (the A's legs, the R's leg) are as heavy as the stems measured square to their run, a little
      lighter across: 100 and 102 wide along the baseline;
    - each letter is as wide as its shape needs, as type is drawn (round 19, the owner: "should each of the letters be
      the same width or no?"): the A widest (270), the R next (210, its bowl and leg), the E (200), the F narrowest (190,
      its open foot would otherwise look wider). Round 25 the owner asked: "are the letters sized properly? It's a little
      odd to me that the A is so wide relative to the R but maybe that's intentional"; of the three ways shown to close
      the gap, round 26 chose "B: lower crossbar": the legs' feet 170 apart, not 210, so the A is 270 wide, not 310, 1.29
      times the R, not 1.48, the triangle inside it as before."""
    s, h, mid = 100, 300, 185
    e = [('rect', 0, 0, s, h), ('rect', 0, 0, 200, 70), ('rect', 0, mid - 70, 175, mid), ('rect', 0, 230, 200, h)]
    xa, span, w, bar = 240, 170, 100, 215            # the A: two legs 100 wide, their feet 170 apart, leaning so their
    lean = math.degrees(math.atan(span / 2 / h))     # tops coincide exactly; the crossbar's top 215 down, from leg middle
    f = 1 - bar / h                                  # to leg middle there
    a = [slab(xa, h, w, h, lean), slab(xa + span, h, w, h, -lean),
         ('rect', xa + span / 2 * f + w / 2, bar, xa + span - span / 2 * f + w / 2, bar + 70)]
    xr = xa + span + w + 30
    r = [('rect', xr, 0, xr + s, h), ('circle', xr + s, mid / 2, mid / 2),   # the bowl's top on the stem's corner
         slab(xr + 108, h, 102, 170, -22)]           # the leg's foot ends at xr + 210, past the bowl's xr + 192.5
    xf = xr + 210 + 40
    f = [('rect', xf, 0, xf + s, h), ('rect', xf, 0, xf + 190, 70), ('rect', xf, mid - 70, xf + 165, mid)]
    return e + a + r + f, xf + 190


WORDMARK, WORDMARK_W = _wordmark()

LINES = [('Bark', TREE, 'a tree'), ('Cloud', CLOUD, 'a cloud'), ('Crag', STONE, 'a crag')]
# key (as frames.py's LOOKS), line, number, name, colour
SPEAKERS = [
    ('eucalyptus', 'Bark', '01', 'Eucalyptus', '#9C9A5E'),
    ('autumn', 'Bark', '02', 'Autumn Birch', '#E2A62E'),
    ('manzanita', 'Bark', '03', 'Manzanita', '#A33D27'),
    ('striped', 'Bark', '04', 'Striped Maple', '#D9E3CF'),
    # the Clouds in spectrum order (round 19, the owner: "What if we did a full spectrum, red orange yellow green blue
    # purple white and black"): a red one added (Flare, the owner's pick in round 21; Ember until then), Smoke made black
    # ("Smoke was meant to be the black one"; round 10's grey retired), all numbered again in that order; Acid and Haze
    # since round 17, Dust and Ice since round 18
    ('red', 'Cloud', '01', 'Flare', '#D2382F'),
    ('orange', 'Cloud', '02', 'Dust', '#E5732A'),
    ('amber', 'Cloud', '03', 'Acid', '#E9B320'),
    ('green', 'Cloud', '04', 'Poison', '#4F7F3A'),
    ('blue', 'Cloud', '05', 'Ice', '#4A90C8'),
    ('violet', 'Cloud', '06', 'Haze', '#6C4BA3'),
    ('ice', 'Cloud', '07', 'Fog', '#F6F8F8'),
    ('black', 'Cloud', '08', 'Smoke', '#34323A'),
    ('cobalt', 'Crag', '01', 'Cobalt Marble', '#ECEFF6'),
    ('malachite', 'Crag', '02', 'Malachite', '#22875A'),
    ('lapis', 'Crag', '03', 'Lapis Lazuli', '#283C96'),
    ('turquoise', 'Crag', '04', 'Turquoise', '#3FB1B7'),
]
SHAPE = {name: prims for name, prims, _ in LINES}


def _el(p, attrs):
    if p[0] == 'arc':
        _, x, y, r, aim, half = p
        a0, a1 = math.radians(aim - half), math.radians(aim + half)
        return (f'<path d="M{x + r * math.cos(a0):.1f} {y + r * math.sin(a0):.1f} A{r:g} {r:g} 0 0 1 '
                f'{x + r * math.cos(a1):.1f} {y + r * math.sin(a1):.1f}" {attrs}/>')
    if p[0] == 'circle':
        return f'<circle cx="{p[1]:g}" cy="{p[2]:g}" r="{p[3]:g}" {attrs}/>'
    if p[0] == 'rect':
        return f'<rect x="{p[1]:g}" y="{p[2]:g}" width="{p[3] - p[1]:g}" height="{p[4] - p[2]:g}" {attrs}/>'
    if p[0] == 'dee':                                # a bar from x0 whose far end is a half circle centred on xc
        _, x0, y0, xc, y1 = p
        r = (y1 - y0) / 2
        return f'<path d="M{x0:g} {y0:g} H{xc:g} A{r:g} {r:g} 0 0 1 {xc:g} {y1:g} H{x0:g} Z" {attrs}/>'
    return f'<polygon points="{" ".join(f"{x:g},{y:g}" for x, y in p[1:])}" {attrs}/>'


def bbox(prims):
    """The primitives' extent with their outline: (x0, y0, x1, y1) on the artboard."""
    xs, ys = [], []
    for p in prims:
        if p[0] in ('circle', 'arc'):
            xs += [p[1] - p[3], p[1] + p[3]]; ys += [p[2] - p[3], p[2] + p[3]]
        elif p[0] == 'rect':
            xs += [p[1], p[3]]; ys += [p[2], p[4]]
        elif p[0] == 'dee':
            xs += [p[1], p[3] + (p[4] - p[2]) / 2]; ys += [p[2], p[4]]
        else:
            xs += [x for x, _ in p[1:]]; ys += [y for _, y in p[1:]]
    h = U / 2
    return min(xs) - h, min(ys) - h, max(xs) + h, max(ys) + h


def mark_svg(line, colour, label, size=None, scale=None):
    """The mark: every primitive filled, then every outline over them all. size: the square artboard's side in
    pixels; scale: pixels per artboard unit, the artboard cropped to the mark (for setting marks to a grid)."""
    prims = SHAPE[line]
    wh = f' width="{size}" height="{size}"' if size else ''
    vb = '-500 -500 1000 1000'
    if scale:
        x0, y0, x1, y1 = bbox(prims)
        vb = f'{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}'
        wh = f' width="{(x1 - x0) * scale:.1f}" height="{(y1 - y0) * scale:.1f}"'
    fills = ''.join(_el(p, f'fill="{colour}"') for p in prims if p[0] != 'arc')
    lines = ''.join(_el(p, f'fill="none" stroke="{INK}" stroke-width="{U}" stroke-linejoin="round"'
                           + (' stroke-linecap="round"' if p[0] == 'arc' else '')) for p in prims)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh} role="img" aria-label="{label}">'
            f'<title>{label}</title>{fills}{lines}</svg>')


def globe_svg(layers, label, size=None, uid='globe', tight=False):
    """The globe: every layer filled, then every outline over them all, the land (or the meridians) cut by the sphere.
    uid keeps the cut's id apart when several globes share a page; tight crops the artboard to the globe and its
    outline (for setting beside type)."""
    wh = f' width="{size}" height="{size}"' if size else ''
    vb = f'{-GLOBE_R - U} {-GLOBE_R - U} {2 * (GLOBE_R + U)} {2 * (GLOBE_R + U)}' if tight else '-500 -500 1000 1000'
    fills, lines = '', ''
    for layer in layers:
        prims, colour, cut = layer[:3]
        g0, g1 = (f'<g clip-path="url(#{uid}-cut)">', '</g>') if cut else ('', '')
        if colour:
            fills += g0 + ''.join(_el(p, f'fill="{colour}"') for p in prims) + g1
        if len(layer) < 4 or layer[3]:
            lines += g0 + ''.join(_el(p, f'fill="none" stroke="{INK}" stroke-width="{U}" stroke-linejoin="round"') for p in prims) + g1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh} role="img" aria-label="{label}">'
            f'<title>{label}</title><defs><clipPath id="{uid}-cut"><circle r="{GLOBE_R}"/></clipPath></defs>{fills}{lines}</svg>')


def wordmark_svg(colour=OCEAN, label='EARF', size=None, sw=U * 0.8):
    """EARF in the acrylic style; size is the height in pixels. The outline is a little lighter than the marks' (the
    letters are drawn smaller)."""
    vw, vh = WORDMARK_W + 2 * sw, 300 + 2 * sw
    wh = f' width="{size * vw / vh:.0f}" height="{size}"' if size else ''
    fills = ''.join(_el(p, f'fill="{colour}"') for p in WORDMARK)
    lines = ''.join(_el(p, f'fill="none" stroke="{INK}" stroke-width="{sw:g}" stroke-linejoin="round"') for p in WORDMARK)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-sw:g} {-sw:g} {vw:g} {vh:g}"{wh} role="img" '
            f'aria-label="{label}"><title>{label}</title>{fills}{lines}</svg>')


def lockup_svg(layers=None, colour=OCEAN, label='EARF', size=None, uid='lockup'):
    """The globe and the wordmark side by side, the globe's diameter 1.5 cap heights, centred on the letters; size is
    the height in pixels."""
    layers = layers or GLOBE
    g = 2 * (GLOBE_R + U)                            # the globe's box at 1:1
    k = 450 / g                                      # scaled to 1.5 x the cap height of 300
    gap, sw = 110, U * 0.8
    vw, vh = 450 + gap + WORDMARK_W + sw, 450
    wh = f' width="{size * vw / vh:.0f}" height="{size}"' if size else ''
    inner = globe_svg(layers, label, uid=uid, tight=True)
    inner = inner[inner.index('<defs>'):inner.rindex('</svg>')]
    word = ''.join(_el(p, f'fill="{colour}"') for p in WORDMARK) + ''.join(
        _el(p, f'fill="none" stroke="{INK}" stroke-width="{sw:g}" stroke-linejoin="round"') for p in WORDMARK)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw:g} {vh:g}"{wh} role="img" aria-label="{label}">'
            f'<title>{label}</title><g transform="translate(225 225) scale({k:.5f})">{inner}</g>'
            f'<g transform="translate({450 + gap} 75)">{word}</g></svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):                        # the set is written afresh each time
        if f.endswith('.svg'):
            os.remove(os.path.join(OUT, f))
    rows = []
    for line, _, what in LINES:
        cells = ''
        for key, ln, num, name, colour in SPEAKERS:
            if ln != line:
                continue
            label = f'{line} {num}, {name}'
            open(os.path.join(OUT, f'{key}.svg'), 'w').write(mark_svg(line, colour, label) + '\n')
            cells += (f'<figure>{mark_svg(line, colour, label, 200)}<figcaption><b>{num}</b> {name}<i>{colour}</i>'
                      '</figcaption></figure>')
        rows.append(f'<section><h2>{line} <i>{what}</i></h2><div class="row">{cells}</div></section>')
    open(os.path.join(OUT, 'globe.svg'), 'w').write(globe_svg(GLOBE, 'EARF: a globe of land circles and a band of ocean') + '\n')
    open(os.path.join(OUT, 'earf.svg'), 'w').write(wordmark_svg() + '\n')
    open(os.path.join(OUT, 'earf-lockup.svg'), 'w').write(lockup_svg() + '\n')
    for key, name, sub, layers in OPTIONS:
        open(os.path.join(OUT, f'globe-{key}.svg'), 'w').write(globe_svg(layers, f'EARF: {name.lower()}, {sub}', uid=key) + '\n')
    rows.insert(0, '<section><h2>The logo <i>the globe and the wordmark</i></h2>'
                f'<div class="lock">{lockup_svg(size=150, uid="s0")}</div>'
                f'<div class="lock">{lockup_svg(colour="#F2EFEA", size=70, uid="s1")}'
                f'{lockup_svg(size=40, uid="s2")}</div></section>'
                '<section><h2>The globe <i>B3, the logo (final for now); the options set aside</i></h2><div class="row wrap">'
                f'<figure>{globe_svg(GLOBE, "EARF", 200, "s3")}<figcaption>B3<i>the logo</i></figcaption></figure>'
                + ''.join(f'<figure>{globe_svg(layers, "EARF", 200, "o" + key)}<figcaption>{name}<i>{sub}</i></figcaption></figure>'
                          for key, name, sub, layers in OPTIONS) + '</div></section>')
    open(os.path.join(OUT, 'sheet.html'), 'w').write(
        '<!doctype html><meta charset="utf-8"><title>EARF marks</title><style>'
        'body{margin:0;padding:56px 64px;background:#F2EFEA;font:14px/1.4 "IBM Plex Mono",monospace;color:#5E5A53;width:1100px}'
        'header{font:700 64px/1 "Instrument Sans",Arial,sans-serif;letter-spacing:-2px;color:#1A1917;margin-bottom:40px}'
        'section{margin-bottom:28px}h2{margin:0 0 8px;font:600 24px/1 "Instrument Sans",Arial,sans-serif;color:#1A1917}'
        '.wrap{flex-wrap:wrap;row-gap:28px}h2 i{display:inline;font:400 14px/1 "IBM Plex Mono",monospace;color:#6F6A61;margin-left:10px}.row{display:flex;gap:44px}'
        'figure{margin:0;width:200px}figure svg{display:block}figcaption{letter-spacing:.06em;text-transform:uppercase;'
        'color:#1A1917}b{font-weight:500;margin-right:6px}i{display:block;font-style:normal;color:#8A857C;font-size:12px}'
        '.lock{display:flex;align-items:center;gap:56px;margin:0 0 24px}.lock svg{display:block}'
        f'</style><header>{wordmark_svg(size=64)}</header>' + ''.join(rows) + '\n')
    print(f'{len(SPEAKERS)} marks in {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
