"""Dogs Barking: one mark for each speaker, drawn as stacked clear acrylic.

Round 10, the owner, of the cloud: "These acrylic marks, without the circular framing (ie just the geometric cloud), are
great. Representative of the speaker design and theme." Then: "Acrylic style marks for each theme, with a distinct
color for each speaker. Trees, Clouds, Stones ... And geometric shapes for each. The tree could be a vertical rectangle
with circles at the top", and: "I like the cloud because it combines multiple shapes and sizes with large enough gaps
between the overlapping strokes of each shape. The tree and stone need to accomplish the same thing ... For the stone we
could make an exception and do something more like the rock option, but that front left side looks too much like a
house shape."

- A line is one shape, built from a few primitives of different sizes: Bark a tree (a trunk and three circles), Cloud a
  cloud (three circles on a rectangle), Crag a crag (three equilateral triangles on a rectangle, the cloud's build in
  straight lines; the owner, after a round of stones: "The cloud and the tree use very uniform shapes. The stone should
  do the same. Clean parallelograms, squares/rectangles, and triangles are best I think").
- A speaker is its line's shape in its own colour.
- The acrylic: every primitive is filled, then every outline is drawn over all of them, U wide, so the construction
  shows through as if each piece were clear acrylic laid on the others.
- The cloud's build, kept by the crag: three shapes of three sizes, small, big and medium, and a rectangle from the
  outer two's centres down to the base, so its edges cross them square on and the lines merge only along the base.
- The dog, a proposal for the brand (the owner: "If you can make a dog barking out of geometric shapes, that could be
  cool", after "I want a dog with a horn head"): a dog of rectangles and parallelograms, the speaker's horn for its head
  (the pod a rectangle, the flare a trapezoid), two triangles for ears, barking in three arcs. Not in the look book,
  which carries the name alone until the owner says otherwise.

    python3 spinoffs/barkhorn/marks.py

writes marks/<key>.svg for each speaker (transparent round it), marks/dog.svg and marks/sheet.html.
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
        elif p[0] == 'rect':
            out.append(('rect', p[1] * k + dx, p[2] * k + dy, p[3] * k + dx, p[4] * k + dy))
        elif p[0] == 'arc':                          # a stroke only: centre, radius, aim and half-span in degrees
            out.append(('arc', p[1] * k + dx, p[2] * k + dy, p[3] * k, p[4], p[5]))
        else:
            out.append(('poly',) + tuple((x * k + dx, y * k + dy) for x, y in p[1:]))
    return out


def triangle(cx, base, side):
    """An equilateral triangle standing on the base line (y down)."""
    return ('poly', (cx - side / 2, base), (cx + side / 2, base), (cx, base - side * 3 ** 0.5 / 2))


# the cloud as approved: three circles and a rectangle from the outer two's centres down to their common tangent
CLOUD = place([('circle', -179, 35, 115), ('circle', -19, -67, 173), ('circle', 179, 19, 131), ('rect', -179, 35, 179, 150)],
              dy=45)
# the tree: a crown of three circles overlapping deeply, the trunk's top inside them (the owner: "The previous three tree
# was better. The two smaller circles feel too detached")
TREE = place([('rect', -44, -40, 44, 340), ('circle', 0, -210, 150), ('circle', -140, -70, 128), ('circle', 140, -70, 128)])
# the crag: three equilateral triangles, small, big and medium, on the base line, and a rectangle from the outer two's
# centres down to it, as the cloud's runs from its outer circles' centres
_B = 170
STONE = place([triangle(-200, _B, 240), triangle(-20, _B, 420), triangle(190, _B, 300),
               ('rect', -200, _B - 240 * 3 ** 0.5 / 6, 190, _B)], k=0.92, dx=-10, dy=12)
# the dog: a body, two legs, a tail and a neck of rectangles and parallelograms, the horn's pod and flare for a head, two
# ears, the bark in three arcs of the flare's mouth
DOG = place([('rect', -280, -10, 120, 130), ('rect', -260, 100, -190, 320), ('rect', 50, 100, 120, 320),
             ('poly', (-280, 0), (-380, -170), (-310, -190), (-230, -20)), ('poly', (40, 10), (110, -170), (210, -170), (140, 10)),
             ('rect', 100, -260, 220, -130), ('poly', (220, -248), (360, -330), (360, -60), (220, -142)),
             ('poly', (112, -258), (138, -360), (168, -258)), ('poly', (158, -258), (190, -350), (214, -258)),
             ('arc', 372, -195, 52, 0, 34), ('arc', 372, -195, 96, 0, 34), ('arc', 372, -195, 140, 0, 34)],
            k=0.86, dx=-56, dy=34)

LINES = [('Bark', TREE, 'a tree'), ('Cloud', CLOUD, 'a cloud'), ('Crag', STONE, 'a crag')]
# key (as frames.py's LOOKS), line, number, name, colour
DOG_COLOUR = '#E2A62E'
SPEAKERS = [
    ('eucalyptus', 'Bark', '01', 'Eucalyptus', '#9C9A5E'),
    ('autumn', 'Bark', '02', 'Autumn Birch', '#E2A62E'),
    ('manzanita', 'Bark', '03', 'Manzanita', '#A33D27'),
    ('striped', 'Bark', '04', 'Striped Maple', '#D9E3CF'),
    ('green', 'Cloud', '01', 'Poison', '#4F7F3A'),
    ('smoke', 'Cloud', '02', 'Smoke', '#5D5A66'),
    ('ice', 'Cloud', '03', 'Fog', '#F6F8F8'),
    ('cobalt', 'Crag', '01', 'Cobalt Marble', '#ECEFF6'),
    ('malachite', 'Crag', '02', 'Malachite', '#22875A'),
    ('lapis', 'Crag', '03', 'Lapis Lazuli', '#283C96'),
    ('turquoise', 'Crag', '04', 'Turquoise', '#3FB1B7'),
]
SHAPE = {name: prims for name, prims, _ in LINES}
SHAPE['Dog'] = DOG


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
    return f'<polygon points="{" ".join(f"{x:g},{y:g}" for x, y in p[1:])}" {attrs}/>'


def mark_svg(line, colour, label, size=None):
    """The mark: every primitive filled, then every outline over them all."""
    prims = SHAPE[line]
    wh = f' width="{size}" height="{size}"' if size else ''
    fills = ''.join(_el(p, f'fill="{colour}"') for p in prims if p[0] != 'arc')
    lines = ''.join(_el(p, f'fill="none" stroke="{INK}" stroke-width="{U}" stroke-linejoin="round"'
                           + (' stroke-linecap="round"' if p[0] == 'arc' else '')) for p in prims)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-500 -500 1000 1000"{wh} role="img" aria-label="{label}">'
            f'<title>{label}</title>{fills}{lines}</svg>')


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
    dog = mark_svg('Dog', DOG_COLOUR, 'Dogs Barking: a dog barking, its head the horn')
    open(os.path.join(OUT, 'dog.svg'), 'w').write(dog + '\n')
    rows.append('<section><h2>The dog <i>proposed for the brand, not in the look book</i></h2><div class="row">'
                + ''.join(f'<figure>{mark_svg("Dog", c, "the dog", 200)}<figcaption><i>{c}</i></figcaption></figure>'
                          for c in (DOG_COLOUR, '#F3EDE1')) + '</div></section>')
    open(os.path.join(OUT, 'sheet.html'), 'w').write(
        '<!doctype html><meta charset="utf-8"><title>Dogs Barking marks</title><style>'
        'body{margin:0;padding:56px 64px;background:#F2EFEA;font:14px/1.4 "IBM Plex Mono",monospace;color:#5E5A53;width:1100px}'
        'header{font:700 64px/1 "Instrument Sans",Arial,sans-serif;letter-spacing:-2px;color:#1A1917;margin-bottom:40px}'
        'section{margin-bottom:28px}h2{margin:0 0 8px;font:600 24px/1 "Instrument Sans",Arial,sans-serif;color:#1A1917}'
        'h2 i{font:400 14px/1 "IBM Plex Mono",monospace;color:#6F6A61;margin-left:10px}.row{display:flex;gap:44px}'
        'figure{margin:0;width:200px}figure svg{display:block}figcaption{letter-spacing:.06em;text-transform:uppercase;'
        'color:#1A1917}b{font-weight:500;margin-right:6px}i{display:block;font-style:normal;color:#8A857C;font-size:12px}'
        '</style><header>Dogs Barking</header>' + ''.join(rows) + '\n')
    print(f'{len(SPEAKERS)} marks in {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
