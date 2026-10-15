"""An icon for each Cloud, built from the marks' own shapes (round 23).

The owner, of the theme: "Atmosphere is cool, but open to other earth themes. Elements was another idea I had. We could
reuse existing geometric imagery to do things like cross bones made of crossing rectangles with circles at the ends
for poison. A circle and a triangle on top for acid/rain, etc."

So each Cloud gets a sign made as the cloud mark is (marks.py): a few circles, rectangles and triangles of different
sizes, every one filled, then every outline drawn over all of them, as stacked clear acrylic.

- Flare: a sun, a circle in eight short rays.
- Dust: a dust devil, five bars narrowing as they fall, three motes of dust beside it.
- Acid: a raindrop, a circle with a triangle on top, its sides tangent to the circle.
- Poison: crossbones, two crossing bars with two circles at each end.
- Ice: a snowflake, three bars crossing at 60 degrees with a circle at each end (the crossbones' construction).
- Haze: a sun low behind three bars of haze.
- Fog: the cloud mark itself, three circles on a bar, since fog is cloud on the ground.
- Smoke: a chimney, three puffs rising from it and growing.

    python3 spinoffs/barkhorn/icons.py     ->  brand/icon-<name>.svg, each in its colour (earth.py draws them all,
                                              tinted, in lines and in black, on the globe page)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import marks as M                                         # noqa: E402

OUT = os.path.join(HERE, 'brand')


def bar(x0, y0, x1, y1, w):
    """A rectangle w wide from one point to another, as a polygon (the marks' rectangles are square to the page)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return ('poly', (x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny))


def spokes(n, r0, r1, w, phase=0.0, cx=0.0, cy=0.0):
    out = []
    for k in range(n):
        a = math.radians(phase + 360 * k / n)
        out.append(bar(cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a), w))
    return out


def flare():
    return [('circle', 0, 0, 150)] + spokes(8, 205, 300, 52, phase=22.5)


def dust():
    rows = [(-250, 250), (-200, 205), (-150, 150), (-100, 92), (-55, 40)]
    bars = [('rect', x0 - 30, -230 + 92 * i, x1 - 30, -230 + 92 * i + 58) for i, (x0, x1) in enumerate(rows)]
    return bars + [('circle', 265, -60, 26), ('circle', 300, 40, 20), ('circle', 250, 125, 16)]


def acid():
    r, cy, top = 160, 70, -280                                # the triangle's sides tangent to the circle
    d = cy - top
    a = math.acos(r / d)
    tx, ty = r * math.sin(a), cy - r * math.cos(a)
    return [('circle', 0, cy, r), ('poly', (0, top), (tx, ty), (-tx, ty))]


def poison():
    out = []
    for (x0, y0, x1, y1) in ((-245, -175, 245, 175), (-245, 175, 245, -175)):
        out.append(bar(x0, y0, x1, y1, 72))
        L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
        for ex, ey, s in ((x0, y0, -1), (x1, y1, 1)):          # two knobs at each end, either side of the bar
            for side in (-1, 1):
                out.append(('circle', ex + s * 18 * ux + side * 40 * -uy, ey + s * 18 * uy + side * 40 * ux, 48))
    return out


def ice():
    out = [bar(300 * math.cos(math.radians(a)), 300 * math.sin(math.radians(a)),
               -300 * math.cos(math.radians(a)), -300 * math.sin(math.radians(a)), 56) for a in (90, 30, -30)]
    for k in range(6):
        a = math.radians(90 + 60 * k)
        out.append(('circle', 300 * math.cos(a), 300 * math.sin(a), 46))
    return out


def haze():
    return [('circle', 0, -70, 170), ('rect', -280, -10, 250, 60), ('rect', -230, 100, 290, 170), ('rect', -170, 210, 200, 280)]


def fog():
    return list(M.CLOUD)


def smoke():
    return [('rect', -235, 30, -135, 300), ('circle', -150, -40, 62), ('circle', -30, -150, 88), ('circle', 140, -230, 112)]


ICONS = [('Flare', flare()), ('Dust', dust()), ('Acid', acid()), ('Poison', poison()), ('Ice', ice()),
         ('Haze', haze()), ('Fog', fog()), ('Smoke', smoke())]
COLOURS = {name: col for key, line, num, name, col in M.SPEAKERS if line == 'Cloud'}


def icon_svg(name, fill, line=M.INK, size=None, label=None, stroke=M.U):
    """An icon: every shape filled, every outline over them all (fill None: the outlines alone, in `line`)."""
    prims = dict(ICONS)[name]
    wh = f' width="{size}" height="{size}"' if size else ''
    fills = '' if fill is None else ''.join(M._el(p, f'fill="{fill}"') for p in prims)
    lines = ''.join(M._el(p, f'fill="none" stroke="{line}" stroke-width="{stroke}" stroke-linejoin="round"') for p in prims)
    label = label or name
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-400 -400 800 800"{wh} role="img" aria-label="{label}">'
            f'<title>{label}</title>{fills}{lines}</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, _ in ICONS:
        open(os.path.join(OUT, f'icon-{name.lower()}.svg'), 'w').write(icon_svg(name, COLOURS[name]))
    print(' '.join(f'brand/icon-{n.lower()}.svg' for n, _ in ICONS))


if __name__ == '__main__':
    main()
