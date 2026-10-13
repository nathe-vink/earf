"""Dogs Barking: one mark for each speaker, drawn as stacked clear acrylic.

Round 10, the owner, of the cloud: "These acrylic marks, without the circular framing (ie just the geometric cloud), are
great. Representative of the speaker design and theme." Then: "Acrylic style marks for each theme, with a distinct
color for each speaker. Trees, Clouds, Stones ... And geometric shapes for each. The tree could be a vertical rectangle
with circles at the top", and: "I like the cloud because it combines multiple shapes and sizes with large enough gaps
between the overlapping strokes of each shape. The tree and stone need to accomplish the same thing ... For the stone we
could make an exception and do something more like the rock option, but that front left side looks too much like a
house shape."

- A line is one shape, built from a few primitives of different sizes: Bark a tree (a trunk and three circles), Cloud a
  cloud (three circles on a rectangle), Crag a stone (three plates, the exception: straight edges).
- A speaker is its line's shape in its own colour.
- The acrylic: every primitive is filled, then every outline is drawn over all of them, U wide, so the construction
  shows through as if each piece were clear acrylic laid on the others.
- The cloud's rules, kept by all three: the primitives overlap deeply; a rectangle's corners sit on circles' centres,
  so its edges cross them square on; where two strokes come close without crossing they stay at least 2 U apart (the
  cloud's own narrowest gap); where they cross, they cross open (the tree at 70 degrees or more, the stone at 33 or
  more); tangents only on the silhouette, where the lines merge. No marks or logo for the brand for now (the owner:
  "Just drop the branding for now").

    python3 spinoffs/barkhorn/marks.py

writes marks/<key>.svg for each speaker (transparent round it) and marks/sheet.html.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'marks')
INK = '#1C1A18'
U = 22                                               # the outline, on a 1000 artboard


def place(prims, k=1.0, dy=0.0):
    """The primitives scaled by k and moved down dy, so each shape sits optically centred at one size."""
    out = []
    for p in prims:
        if p[0] == 'circle':
            out.append(('circle', p[1] * k, p[2] * k + dy, p[3] * k))
        elif p[0] == 'rect':
            out.append(('rect', p[1] * k, p[2] * k + dy, p[3] * k, p[4] * k + dy))
        else:
            out.append(('poly',) + tuple((x * k, y * k + dy) for x, y in p[1:]))
    return out


# the cloud as approved: three circles and a rectangle from the outer two's centres down to their common tangent
CLOUD = place([('circle', -179, 35, 115), ('circle', -19, -67, 173), ('circle', 179, 19, 131), ('rect', -179, 35, 179, 150)],
              dy=45)
# the tree: a crown of three circles of three sizes, the trunk's top at the big one's centre, clear of the small ones
TREE = place([('circle', -196, -36, 100), ('circle', 0, -160, 178), ('circle', 200, -50, 112), ('rect', -40, -160, 40, 340)])
# the stone: a big plate spanning the base, a small plate either side overlapping it but not each other, every edge
# leaning against the one it crosses; its top a tilted slab, so no face reads as a house
STONE = place([('poly', (-340, 200), (-290, 10), (-160, -40), (-60, 200)),
               ('poly', (-200, 200), (-150, -60), (-20, -250), (200, -200), (170, 200)),
               ('poly', (50, 200), (170, -60), (320, -20), (340, 200))], k=0.92, dy=23)

LINES = [('Bark', TREE, 'a tree'), ('Cloud', CLOUD, 'a cloud'), ('Crag', STONE, 'a stone')]
# key (as frames.py's LOOKS), line, number, name, colour
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


def _el(p, attrs):
    if p[0] == 'circle':
        return f'<circle cx="{p[1]:g}" cy="{p[2]:g}" r="{p[3]:g}" {attrs}/>'
    if p[0] == 'rect':
        return f'<rect x="{p[1]:g}" y="{p[2]:g}" width="{p[3] - p[1]:g}" height="{p[4] - p[2]:g}" {attrs}/>'
    return f'<polygon points="{" ".join(f"{x:g},{y:g}" for x, y in p[1:])}" {attrs}/>'


def mark_svg(line, colour, label, size=None):
    """The mark: every primitive filled, then every outline over them all."""
    prims = SHAPE[line]
    wh = f' width="{size}" height="{size}"' if size else ''
    fills = ''.join(_el(p, f'fill="{colour}"') for p in prims)
    lines = ''.join(_el(p, f'fill="none" stroke="{INK}" stroke-width="{U}" stroke-linejoin="round"') for p in prims)
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
