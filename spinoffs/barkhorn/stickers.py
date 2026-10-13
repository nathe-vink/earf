"""The barkhorn marks: the brand's and one for each speaker in the look book, each drawn to work as a stamp.

Round 8, the owner: "Not stickers of the speakers. Stickers of a visual metaphor that represents each speaker. The brand
is as important as the speakers themselves. And I think bark is more of a product style/line. Y2K another. Crag
another." Then: "I'd like it to work in black and white, meaning we can't rely on color to communicate the design of
each speaker", and: "What about dogs barking for the brand name, back to back dogs with horns for head, with roar-like
shapes emitting from the horn. Again, I want to stress minimalism. Something that could work as a stamp."

- The brand: a dog barking ("Kind of like this style. Could also be one dog. Something that feels like it's from
  Fallout."), its head in one ink with the light cut out, in a badge the shape of the horn's mouth with its name.
- A line: its shape. Bark is the circle (a trunk cut across), Y2K the rounded square (a translucent case), Crag the
  triangle (a peak).
- A speaker: its line's shape, solid, with one mark cut out of it, centred: the material reduced to a primitive. Bark:
  strips, dashes, a curl, waves. Crag: veins, wavy rings, nested bands, crystals, strata. Y2K is one cloud in three colours
  (poison, smoke, fog); in one ink the cloud keeps its colour by heraldry's hatching (diagonal lines for green,
  cross-hatching for black, plain for white). Strokes are one unit wide (U) or less, with round ends.

Colour is a second layer on the same drawing, for the stickers: each sits on a white die-cut margin with a hairline.

    python3 spinoffs/barkhorn/stickers.py

writes stickers/<key>.svg (the colour sticker), <key>-mono.svg (the one-colour sticker), mark-<key>.svg and
mark-<key>-white.svg (the mark alone in ink or in white, transparent round it), the line marks, the brand's badge
(brand.svg, brand-white.svg), the dog alone (dog.svg, dog-white.svg) and stickers/sheet.html.
"""
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'stickers')

S = 260                                         # each mark's artboard, square; the shapes are optically equal
C = S / 2
CT = 164                                        # the triangle's optical centre (its centroid is at 158)
U = 16                                          # the stroke unit
EDGE = 11                                       # the die-cut's white margin
INK, PAPER = '#1A1917', '#F7F5F0'


# --- the three shapes ----------------------------------------------------------------------------------------------
def rounded_polygon(pts, r):
    """An SVG path for a convex polygon (clockwise on screen) with each corner rounded to radius r."""
    n, d = len(pts), ''
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        a = (p0[0] - p1[0], p0[1] - p1[1]); b = (p2[0] - p1[0], p2[1] - p1[1])
        la, lb = math.hypot(*a), math.hypot(*b)
        ang = math.acos((a[0] * b[0] + a[1] * b[1]) / (la * lb))
        t = r / math.tan(ang / 2)
        pin = (p1[0] + a[0] / la * t, p1[1] + a[1] / la * t)
        pout = (p1[0] + b[0] / lb * t, p1[1] + b[1] / lb * t)
        d += f'{"M" if i == 0 else "L"}{pin[0]:.1f} {pin[1]:.1f} A{r:g} {r:g} 0 0 1 {pout[0]:.1f} {pout[1]:.1f} '
    return d + 'Z'


def shape_el(shape):
    if shape == 'circle':
        return f'<circle cx="{C:g}" cy="{C:g}" r="100"/>'
    if shape == 'square':
        return '<rect x="40" y="40" width="180" height="180" rx="32"/>'
    L, cy, r = 244, 158.25, 22
    h = L * math.sqrt(3) / 2
    return f'<path d="{rounded_polygon([(C, cy - 2 * h / 3), (C + L / 2, cy + h / 3), (C - L / 2, cy + h / 3)], r)}"/>'


def paint(el, **attrs):
    return el.replace('/>', ''.join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items()) + '/>')


LINES = [('bark', 'Bark', 'circle'), ('y2k', 'Y2K', 'square'), ('crag', 'Crag', 'triangle')]


# --- mark layers: each takes a colour (and an id prefix) and returns SVG on the 260 artboard -----------------------
def stroke(d, c, w=U):
    return f'<path d="{d}" stroke="{c}" stroke-width="{w:g}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)


def strips(bars):
    """Vertical strips, centred: [(x, width, height), ...], their ends round."""
    return lambda c, uid: ''.join(f'<rect x="{x:g}" y="{C - h / 2:g}" width="{w:g}" height="{h:g}" rx="{w / 2:g}" fill="{c}"/>'
                                  for x, w, h in bars)


def dashes(items, w=14):
    return lambda c, uid: ''.join(stroke(f'M{x0} {y} L{x1} {y}', c, w) for y, x0, x1 in items)


def spiral(turns=2.3, r0=6, r1=64):
    pts = []
    for i in range(161):
        th = turns * 2 * math.pi * i / 160
        r = r0 + (r1 - r0) * i / 160
        pts.append((C + r * math.cos(th), C + r * math.sin(th)))
    return lambda c, uid: stroke(poly(pts), c)


def waves(xs, y0=70, y1=190, amp=7, period=60, w=14):
    def draw(c, uid):
        out = ''
        for x in xs:
            pts = [(x + amp * math.sin(2 * math.pi * (y - y0) / period), y) for y in [y0 + (y1 - y0) * i / 60 for i in range(61)]]
            out += stroke(poly(pts), c, w)
        return out
    return draw


def cloud_path(cx=C, cy=C):
    """A cloud, its bottom flat, centred on (cx, cy): three bumps on a rounded base."""
    # in local units, its box is x -63..63, y -44..36; drawn as one outline so it can be hatched and clipped
    return (f'M{cx - 50:g} {cy + 36:g} A14 14 0 0 1 {cx - 63:g} {cy + 22:g} A26 26 0 0 1 {cx - 36:g} {cy - 6:g} '
            f'A36 36 0 0 1 {cx + 30:g} {cy - 20:g} A24 24 0 0 1 {cx + 63:g} {cy + 12:g} A24 24 0 0 1 {cx + 50:g} {cy + 36:g} Z')


def cloud(cx=C, cy=C + 4):
    return lambda c, uid: f'<path d="{cloud_path(cx, cy)}" fill="{c}"/>'


def hatch(kind, cx=C, cy=C + 4, gap=13, w=4.5):
    """Heraldry's hatching inside the cloud: 'vert' (green) diagonal lines, 'sable' (black) a grid; argent (white) none."""
    def draw(c, uid):
        lines = []
        if kind == 'vert':
            for k in range(-12, 13):
                o = k * gap
                lines.append(f'M{cx + o - 80:g} {cy - 80:g} L{cx + o + 80:g} {cy + 80:g}')
        elif kind == 'sable':
            for k in range(-7, 8):
                o = k * gap
                lines.append(f'M{cx - 80:g} {cy + o:g} L{cx + 80:g} {cy + o:g}')
                lines.append(f'M{cx + o:g} {cy - 80:g} L{cx + o:g} {cy + 80:g}')
        return (f'<clipPath id="h-{uid}"><path d="{cloud_path(cx, cy)}"/></clipPath><g clip-path="url(#h-{uid})">'
                + ''.join(stroke(d, c, w) for d in lines) + '</g>')
    return draw


def bezier(chain, n=24):
    """Points along a chain of cubic curves [p0, c1, c2, p1, c3, c4, p2, ...]."""
    pts = []
    for i in range(0, len(chain) - 1, 3):
        p0, c1, c2, p1 = chain[i:i + 4]
        for k in range(n + (1 if i + 4 >= len(chain) else 0)):
            t = k / n
            pts.append(tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * cc + t ** 3 * d
                             for a, b, cc, d in zip(p0, c1, c2, p1)))
    return pts


def taper(pts, w0, w1, w2):
    """A line drawn as a filled band whose width runs w0 at its start, w1 in the middle and w2 at its end."""
    n, left, right = len(pts), [], []
    for i, (x, y) in enumerate(pts):
        (xa, ya), (xb, yb) = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx, dy = xb - xa, yb - ya; ln = math.hypot(dx, dy) or 1.0
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t * 2) if t < 0.5 else (w1 + (w2 - w1) * (t - 0.5) * 2)
        left.append((x - dy / ln * w / 2, y + dx / ln * w / 2)); right.append((x + dy / ln * w / 2, y - dx / ln * w / 2))
    return poly(left + right[::-1]) + ' Z'


VEINS = [taper(bezier([(18, 220), (58, 194), (84, 206), (110, 180), (136, 154), (150, 150), (170, 154), (196, 158), (212, 128), (244, 98)]), 3, 14, 4),
         taper(bezier([(110, 180), (120, 198), (132, 212), (148, 240)]), 8, 4, 1.5),
         taper(bezier([(170, 154), (162, 132), (170, 110), (186, 88)]), 7, 4, 1.5),
         taper(bezier([(46, 236), (86, 222), (114, 228), (140, 246)]), 1.5, 4, 1.5),
         taper(bezier([(96, 126), (112, 138), (120, 152), (124, 172)]), 1.5, 3.5, 2)]


def veins(c, uid):
    """Marble: a main vein through the stone, swelling and thinning, two branches off it and fine veins beside it."""
    return ''.join(f'<path d="{d}" fill="{c}"/>' for d in VEINS)


def wavy_ring(R, cx=C, cy=CT):
    """A closed wavy band edge, radius R, swelling unevenly (two waves together, one phase for every ring so the bands
    run parallel), its centre drifting down and left as the rings close in, as a malachite's eyes do."""
    k = (58 - R) / 58
    ox, oy = cx - 7 * k, cy + 6 * k
    a1, a2 = min(6.0, R * 0.3), min(2.5, R * 0.12)
    pts = [(ox + (R + a1 * math.sin(3 * t + 0.6) + a2 * math.sin(7 * t + 1.9)) * math.cos(t),
            oy + (R + a1 * math.sin(3 * t + 0.6) + a2 * math.sin(7 * t + 1.9)) * math.sin(t))
           for t in [2 * math.pi * i / 180 for i in range(180)]]
    return lambda c, uid: f'<path d="{poly(pts)} Z" fill="{c}"/>'


def nested(scale):
    """The triangle again, smaller, about its centroid: its bands of colour laid in layers."""
    L, cy, r = 244 * scale, 158.25, max(22 * scale, 2)
    h = L * math.sqrt(3) / 2
    d = rounded_polygon([(C, cy - 2 * h / 3), (C + L / 2, cy + h / 3), (C - L / 2, cy + h / 3)], r)
    return lambda c, uid: f'<path d="{d}" fill="{c}"/>'


def cubes(items):
    """Pyrite's crystals: small squares, each turned its own way: [(x, y, side, degrees), ...]."""
    return lambda c, uid: ''.join(f'<rect x="{x - a / 2:g}" y="{y - a / 2:g}" width="{a}" height="{a}" rx="1.5" '
                                  f'transform="rotate({deg} {x} {y})" fill="{c}"/>' for x, y, a, deg in items)


def chevrons(apexes=(116, 144, 172), arm=52, w=14):
    dx, dy = arm * math.cos(math.radians(60)), arm * math.sin(math.radians(60))
    return lambda c, uid: ''.join(stroke(f'M{C - dx:.1f} {y + dy:.1f} L{C:g} {y} L{C + dx:.1f} {y + dy:.1f}', c, w) for y in apexes)


def sparkle(cx, cy, r):
    """A four-pointed star, its sides drawn in."""
    q = r * 0.16
    return (f'M{cx:g} {cy - r:g} C{cx + q:g} {cy - q:g} {cx + q:g} {cy - q:g} {cx + r:g} {cy:g} '
            f'C{cx + q:g} {cy + q:g} {cx + q:g} {cy + q:g} {cx:g} {cy + r:g} C{cx - q:g} {cy + q:g} {cx - q:g} {cy + q:g} {cx - r:g} {cy:g} '
            f'C{cx - q:g} {cy - q:g} {cx - q:g} {cy - q:g} {cx:g} {cy - r:g} Z')


def sparkles(items):
    return lambda c, uid: ''.join(f'<path d="{sparkle(x, y, r)}" fill="{c}"/>' for x, y, r in items)


def strata(bands):
    """Layers laid down across the stone: [(y, thickness), ...]."""
    return lambda c, uid: ''.join(f'<rect x="0" y="{y - t / 2:g}" width="{S}" height="{t:g}" fill="{c}"/>' for y, t in bands)


def pores(items):
    return lambda c, uid: ''.join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="3" fill="{c}"/>' for x, y in items)


M, G, H = 'mark', 'ground', 'hatch'             # a layer cut out, drawn back in ink, or hatching (one ink only)
CLOUD = cloud()
SPEAKERS = [
    # key, line, number, name, ground, layers [(draw, colour, part)], what the mark stands for. In one ink every shape
    # is solid and its mark cut out; in colour the ground is the material's and the mark its accent, so a light
    # material keeps its light ground
    ('eucalyptus', 'bark', '01', 'Eucalyptus', '#5B7330',
     [(strips([(93, 22, 128), (125, 12, 112), (147, 20, 140)]), '#C99A3E', M)], 'strips: bark shed in strips of colour'),
    ('autumn', 'bark', '02', 'Autumn Birch', '#F2EFE8',
     [(dashes([(100, 82, 120), (100, 138, 172), (156, 88, 122), (156, 140, 166)]), '#1E1C1A', M),
      (dashes([(128, 104, 160)]), '#E9A800', M)],
     'dashes: a birch\'s lenticels (one gold, for its horn)'),
    ('manzanita', 'bark', '03', 'Manzanita', '#6B1F17', [(spiral(), '#A6B064', M)], 'a curl: red bark peeling to green'),
    ('striped', 'bark', '04', 'Striped Maple', '#ECEFE7', [(waves((96, 130, 164)), '#5C7838', M)], 'waves: a snakebark\'s stripes'),
    ('green', 'y2k', '01', 'Poison', '#26252A', [(CLOUD, '#86C23F', M), (hatch('vert'), INK, H)], 'a cloud, green (hatched: vert)'),
    ('smoke', 'y2k', '02', 'Smoke', '#26252A', [(CLOUD, '#8E8B97', M), (hatch('sable'), INK, H)], 'a cloud, smoke (hatched: sable)'),
    ('ice', 'y2k', '03', 'Fog', '#26252A', [(CLOUD, '#EEF2F4', M)], 'a cloud, white (plain: argent)'),
    ('cobalt', 'crag', '01', 'Cobalt Marble', '#F3F4F1', [(veins, '#1D3C9A', M)], 'veins: marble'),
    ('malachite', 'crag', '02', 'Malachite', '#0F4A2D',
     [(wavy_ring(58), '#5DB57E', M), (wavy_ring(45), '#0F4A2D', G), (wavy_ring(32), '#3E9E66', M), (wavy_ring(19), '#0F4A2D', G),
      ], 'wavy rings: its banded eyes'),
    ('rhodochrosite', 'crag', '03', 'Rhodochrosite', '#B8455E',
     [(nested(0.66), '#F4CACE', M), (nested(0.5), '#B8455E', G), (nested(0.34), '#F4CACE', M), (nested(0.18), '#B8455E', G)],
     'nested bands: its layers of rose and white'),
    ('lapis', 'crag', '04', 'Lapis Lazuli', '#16286E',
     [(cubes([(126, 168, 26, 20), (164, 136, 14, -14), (98, 196, 12, 34), (162, 198, 10, 8), (100, 142, 8, -28), (136, 212, 7, 44)]),
       '#D9B44A', M)], 'crystals: pyrite in deep blue'),
    ('travertine', 'crag', '05', 'Travertine', '#E6D9BE',
     [(strata([(136, 14), (166, 10), (198, 16)]), '#C4A57A', M),
      (pores([(112, 136), (152, 136), (130, 166), (98, 198), (140, 198), (180, 198)]), '#7E6648', G)],
     'strata and pores: stone laid down by a spring'),
]


def svg(body, label, w=S, h=S, vw=S, vh=S):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {vw} {vh}" role="img" '
            f'aria-label="{label}">{body}</svg>')


def die_cut(shape):
    el = shape_el(shape)
    return (paint(el, fill='none', stroke='#000000', stroke_opacity='0.16', stroke_width=2 * EDGE + 2.5, stroke_linejoin='round')
            + paint(el, fill='none', stroke='#FFFFFF', stroke_width=2 * EDGE, stroke_linejoin='round'))


def mono_body(uid, shape, layers, ink):
    """The mark in one ink, transparent round it: the shape solid, the mark cut out of it (ground layers and hatching
    drawn back in)."""
    mask = paint(shape_el(shape), fill='#FFFFFF') + f'<g clip-path="url(#c-{uid})">' + ''.join(
        fn('#000000' if part == M else '#FFFFFF', f'{uid}-{i}') for i, (fn, _, part) in enumerate(layers)) + '</g>'
    return (f'<defs><clipPath id="c-{uid}">{shape_el(shape)}</clipPath><mask id="m-{uid}" maskUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{S}" height="{S}">{mask}</mask></defs><rect width="{S}" height="{S}" fill="{ink}" mask="url(#m-{uid})"/>')


def colour_body(uid, shape, ground, layers):
    """The same drawing in the material's colours (no hatching: the colour says it)."""
    return (f'<defs><clipPath id="c-{uid}">{shape_el(shape)}</clipPath></defs><g clip-path="url(#c-{uid})">'
            f'<rect width="{S}" height="{S}" fill="{ground}"/>'
            + ''.join(fn(col, f'{uid}-{i}') for i, (fn, col, part) in enumerate(layers) if part != H) + '</g>')


def shape_mark(shape, color, size=S):
    return svg(paint(shape_el(shape), fill=color), shape, size, size)


# --- the brand: a dog barking, in a badge the shape of the horn's mouth -------------------------------------------
# (round 8, the owner, after the dogs back to back: "Kind of like this style. Could also be one dog. Something that
# feels like it's from Fallout.") One dog's head in profile, barking up, in one ink with its light cut out (the lips,
# teeth, tongue, eye, brow, the ridge of the muzzle, the cheek, the ear's hollow, fur, the collar and its tag), and its
# bark in jagged bolts. Drawn here, in a 1000 box, y down
HEAD = ('M300 840 C390 862 480 872 566 866 '                                               # the bust, cut in a curve
        'C572 800 586 742 606 700 C622 668 654 650 700 640 C748 630 784 618 806 604 '      # neck front, under the jaw
        'C824 594 830 576 820 562 '                                                         # the chin
        'C810 500 838 414 876 360 '                                                         # the open mouth's front
        'C894 346 912 330 920 312 C936 296 938 264 918 250 '                                # the nose
        'C866 260 768 268 700 280 '                                                         # the muzzle's bridge
        'C664 268 624 228 584 212 C556 202 528 204 504 212 '                                # brow and crown
        'C498 170 478 98 448 46 C430 100 412 170 400 228 '                                  # the near ear
        'C388 176 362 128 330 96 C320 156 314 222 312 280 '                                 # the far ear
        'C296 318 290 360 302 404 C318 470 300 640 304 840 Z')                              # the skull, the nape, the neck


def band(chain, w0, w1, w2):
    """A curve drawn as a filled band: w0 wide at its start, w1 in the middle, w2 at its end."""
    pts = bezier(chain, 28)
    n, left, right = len(pts), [], []
    for i, (x, y) in enumerate(pts):
        (xa, ya), (xb, yb) = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx, dy = xb - xa, yb - ya; ln = math.hypot(dx, dy) or 1.0
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * math.sin(t * math.pi / 2)) if t < 0.5 else (w1 + (w2 - w1) * (1 - math.cos((t - 0.5) * math.pi)))
        left.append((x - dy / ln * w / 2, y + dx / ln * w / 2)); right.append((x + dy / ln * w / 2, y - dx / ln * w / 2))
    return poly(left + right[::-1]) + ' Z'


LIGHT_CUTS = [band(*b) for b in (
    ([(652, 470), (724, 430), (806, 386), (872, 358)], 4, 11, 4),          # the upper lip
    ([(652, 474), (712, 504), (772, 532), (816, 552)], 4, 9, 3),           # the lower lip
    ([(706, 290), (770, 280), (836, 270), (900, 260)], 2, 12, 2),          # the ridge of the muzzle
    ([(588, 286), (614, 262), (650, 258), (680, 274)], 3, 10, 2),          # the brow
    ([(606, 350), (648, 392), (662, 446), (648, 502)], 3, 16, 2),          # the cheek's crescent
    ([(906, 264), (916, 266), (922, 274), (920, 288)], 2, 5, 1),           # the nose's shine
    ([(342, 470), (360, 520), (366, 570), (360, 630)], 2, 16, 1),          # fur on the neck
    ([(410, 500), (430, 556), (436, 606), (428, 660)], 2, 16, 1),
    ([(470, 196), (464, 150), (456, 106), (448, 76)], 16, 10, 1),          # the ear's hollow
    ([(300, 716), (420, 742), (500, 744), (578, 724)], 26, 30, 26))]       # the collar
LIGHT_SHAPES = [
    'M598 300 C614 280 642 274 666 284 C650 302 624 310 598 300 Z',            # the eye
    'M818 380 L850 368 L838 446 Z', 'M786 540 L812 548 L816 478 Z',             # the fangs
    'M850 366 L868 359 L860 392 Z', 'M812 549 L824 553 L828 520 Z',             # incisors
    'M686 482 C742 468 798 470 820 504 C808 524 764 530 718 514 C704 508 692 496 686 482 Z',   # the tongue
]
BOLTS = ['M908 360 L960 338 L950 318 L1014 290', 'M918 420 L974 410 L962 388 L1034 378',
         'M910 482 L968 490 L954 512 L1028 526', 'M888 540 L936 566 L918 584 L978 620']
# the name, BARK over HORN, in Anton (Vernon Adams, SIL Open Font License), drawn as outlines with fontTools: its units
# are 2048 to the em, the capitals 1760 tall, BARK 4007 wide and HORN 4104 wide
BARK = ('M78 0V-1760H555Q747 -1760 834.5 -1666.5Q922 -1573 922 -1358V-1281Q922 -1157 877.5 -1080.0Q833 -1003 742 -979Q861 -949 901.5 -838.5Q942 -728 942 -569Q942 -398 910.0 -270.0Q878 -142 794.0 -71.0Q710 0 555 0ZM422 -1097H494Q543 -1097 557.0 -1135.0Q571 -1173 571 -1226V-1403Q571 -1488 496 -1488H422ZM457 -310Q594 -310 594 -440V-660Q594 -735 571.5 -778.5Q549 -822 487 -822H422V-312Q444 -310 457 -310ZM1040 0 1210 -1760H1807L1974 0H1641L1616 -284H1404L1382 0ZM1429 -565H1589L1512 -1460H1496ZM2112 0V-1760H2652Q2787 -1760 2856.0 -1698.5Q2925 -1637 2948.5 -1526.5Q2972 -1416 2972 -1267Q2972 -1123 2935.5 -1037.0Q2899 -951 2798 -918Q2881 -901 2914.5 -835.5Q2948 -770 2948 -666V0H2601V-689Q2601 -766 2569.5 -784.5Q2538 -803 2468 -803V0ZM2470 -1108H2555Q2628 -1108 2628 -1267Q2628 -1370 2612.0 -1402.0Q2596 -1434 2552 -1434H2470ZM3118 0V-1760H3466V-1055L3630 -1760H3984L3787 -954L4025 0H3660L3468 -852V0Z')
HORN = ('M78 0V-1760H428V-1131H594V-1760H944V0H594V-798H428V0ZM1550 16Q1339 16 1227.5 -111.5Q1116 -239 1116 -480V-1316Q1116 -1542 1226.5 -1659.0Q1337 -1776 1550 -1776Q1763 -1776 1873.5 -1659.0Q1984 -1542 1984 -1316V-480Q1984 -239 1872.5 -111.5Q1761 16 1550 16ZM1553 -308Q1633 -308 1633 -463V-1322Q1633 -1452 1555 -1452Q1467 -1452 1467 -1319V-461Q1467 -379 1487.0 -343.5Q1507 -308 1553 -308ZM2156 0V-1760H2696Q2831 -1760 2900.0 -1698.5Q2969 -1637 2992.5 -1526.5Q3016 -1416 3016 -1267Q3016 -1123 2979.5 -1037.0Q2943 -951 2842 -918Q2925 -901 2958.5 -835.5Q2992 -770 2992 -666V0H2645V-689Q2645 -766 2613.5 -784.5Q2582 -803 2512 -803V0ZM2514 -1108H2599Q2672 -1108 2672 -1267Q2672 -1370 2656.0 -1402.0Q2640 -1434 2596 -1434H2514ZM3162 0V-1760H3524L3686 -917V-1760H4026V0H3682L3506 -880V0Z')


def head_layers(on, off):
    """The dog's head as mask layers: the ink drawn with `on`, the light cut out with `off`."""
    return (f'<path d="{HEAD}" fill="{on}"/>' + ''.join(f'<path d="{d}" fill="{off}"/>' for d in LIGHT_CUTS + LIGHT_SHAPES)
            + f'<circle cx="636" cy="290" r="8" fill="{on}"/>'                                  # the pupil
            + f'<path d="M704 490 C738 492 774 498 806 508" stroke="{on}" stroke-width="5" stroke-linecap="round" fill="none"/>'
            + f'<circle cx="470" cy="790" r="22" fill="{off}"/><circle cx="470" cy="790" r="7" fill="{on}"/>'   # the tag
            + ''.join(f'<path d="{d}" stroke="{on}" stroke-width="14" stroke-miterlimit="6" fill="none"/>' for d in BOLTS))


def inked(uid, layers, ink, vb):
    """One ink through a mask of the layers (on: white, off: black), so the light is transparent."""
    x, y, w, h = vb
    return (f'<defs><mask id="m-{uid}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">{layers}</mask></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{ink}" mask="url(#m-{uid})"/>')


def dog(ink, uid='dog', w=560, h=560):
    """The head alone."""
    vb = (270, 30, 790, 860)
    return svg(inked(uid, head_layers('#FFFFFF', '#000000'), ink, vb), 'barkhorn: a dog barking', w, h, *vb[2:]).replace(
        f'viewBox="0 0 {vb[2]} {vb[3]}"', f'viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}"')


def badge(ink, uid='badge', w=1200, h=700):
    """The brand: the horn's mouth (a rounded rectangle, 1.7 : 1) in a double border, the dog in it barking its name."""
    W, H, r = 1200, 700, 140
    k = 470 / 4007
    cap = 1760 * k
    y1 = H / 2 - (2 * cap + 36) / 2 + cap
    on, off = '#FFFFFF', '#000000'
    layers = (f'<rect x="13" y="13" width="{W - 26}" height="{H - 26}" rx="{r - 13}" fill="none" stroke="{on}" stroke-width="26"/>'
              f'<rect x="40" y="40" width="{W - 80}" height="{H - 80}" rx="{r - 40}" fill="none" stroke="{on}" stroke-width="7"/>'
              f'<clipPath id="p-{uid}"><rect x="44" y="44" width="{W - 88}" height="{H - 88}" rx="{r - 44}"/></clipPath>'
              f'<g clip-path="url(#p-{uid})"><g transform="translate(-112 92) scale(0.7)">{head_layers(on, off)}</g></g>'
              f'<path d="{BARK}" transform="translate(640 {y1:.1f}) scale({k:.5f})" fill="{on}"/>'
              f'<path d="{HORN}" transform="translate(640 {y1 + cap + 36:.1f}) scale({k:.5f})" fill="{on}"/>')
    return svg(inked(uid, layers, ink, (0, 0, W, H)), 'barkhorn: a dog barking its name, in a badge the shape of the horn', w, h, W, H)


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):                    # the set is written afresh each time
        if f.endswith('.svg'):
            os.remove(os.path.join(OUT, f))

    def write(name, text):
        open(os.path.join(OUT, name), 'w').write(text + '\n')
    rows = []
    for key, name, shape in LINES:
        write(f'line-{key}.svg', shape_mark(shape, INK)); write(f'line-{key}-white.svg', shape_mark(shape, PAPER))
        mono_cells, colour_cells = [], []
        for k, ln, num, nm, ground, layers, meaning in SPEAKERS:
            if ln != key:
                continue
            label = f'{name} {num}, {nm}'
            write(f'mark-{k}.svg', svg(mono_body(k, shape, layers, INK), label))
            write(f'mark-{k}-white.svg', svg(mono_body(k, shape, layers, PAPER), label))
            write(f'{k}-mono.svg', svg(die_cut(shape) + mono_body(k, shape, layers, INK), label))
            write(f'{k}.svg', svg(die_cut(shape) + colour_body(k, shape, ground, layers), label))
            mono_cells.append(f'<figure>{svg(die_cut(shape) + mono_body(k + "-s", shape, layers, INK), label, 200, 200)}'
                              f'<figcaption><b>{num}</b> {nm}<i>{meaning}</i></figcaption></figure>')
            colour_cells.append(f'<figure>{svg(die_cut(shape) + colour_body(k + "-sc", shape, ground, layers), label, 200, 200)}</figure>')
        rows.append(f'<section><h2>{shape_mark(shape, INK, 28)}<span>{name}</span></h2>'
                    f'<div class="row">{"".join(mono_cells)}</div><div class="row">{"".join(colour_cells)}</div></section>')
    write('brand.svg', badge(INK)); write('brand-white.svg', badge(PAPER, 'badge-w'))
    write('dog.svg', dog(INK)); write('dog-white.svg', dog(PAPER, 'dog-w'))
    open(os.path.join(OUT, 'sheet.html'), 'w').write(
        '<!doctype html><meta charset="utf-8"><title>barkhorn marks</title><style>'
        'body{margin:0;padding:56px 64px;background:#E9E6DF;font:14px/1.4 "IBM Plex Mono",monospace;color:#5E5A53;width:1652px}'
        'header{display:flex;align-items:center;gap:36px;margin-bottom:48px}header b{font:700 64px/1 "Instrument Sans",Arial,'
        'sans-serif;letter-spacing:-2px;color:#1A1917}section{margin-bottom:44px}h2{display:flex;align-items:center;gap:14px;'
        'margin:0 0 16px;font:600 24px/1 "Instrument Sans",Arial,sans-serif;color:#1A1917}.row{display:flex;gap:56px;'
        'margin-bottom:14px}figure{margin:0;width:220px}figure svg{width:200px;height:200px;display:block}figcaption{margin:2px 0 6px;'
        'letter-spacing:.06em;text-transform:uppercase;color:#1A1917}b{font-weight:500;margin-right:6px}i{display:block;'
        'margin-top:2px;font-style:normal;text-transform:none;letter-spacing:0;color:#6F6A61;font-size:13px}</style>'
        f'<header>{badge(INK, "badge-s", 420, 245)}{dog(INK, "dog-s", 245, 245)}</header>' + ''.join(rows) + '\n')
    print(f'{len(SPEAKERS)} marks, {len(LINES)} lines, the badge and the dog in {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
