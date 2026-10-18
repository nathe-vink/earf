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

Round 30, four drawn again as they move (the owner: "I don't like some of the icons. Like the smoke, haze, and dust.
Haze is close but not quite there. Dust could be more like a flat triangle with circles toward the tail of it, like a
little dust cloud that roadrunner would kick up. Smoke could be more like billowing upward from a downward pointing
triangle. Try and think of that way these things move in the real world. The flare is also kind of lackluster"):

- Flare: a burst of light. Eight pointed rays, long and short, cross a round core from near its middle, so in acrylic it
  glows deepest at its heart.
- Dust: the cloud a roadrunner kicks up. A flat wedge streaks along the ground, its point where the runner went; at its
  tail the puffs billow up and back.
- Haze: a sun sunk into thin bands of haze, staggered as layers drift and shorter as they recede, only its top clear.
- Smoke: smoke billowing up from a downward triangle, its source: the puffs overlap and grow as it rises and leans with
  the wind.

Then (the owner: "They aren't reading as contiguous shapes like the fog cloud does, for example. The haze is almost
there but I would move the circle more into the haze"): every piece of each overlaps the next, as the cloud's circles
and bar do, so each icon is one shape (the burst's sparks and Dust's loose motes gone, Smoke's last puff drawn in, the
sun lowered until every band crosses it).

And a third time (the owner: "No they need to be more connected. Also thinking that flare might not be a good
atmosphere option. Also fewer shapes"; "I think it's important for the shape to look good as a single shape. That's why
cloud was so good. four independent shapes that collectively make a whole, then broken down and presented as their
overlapping acrylic parts"; "We can also try something else, where we cut shapes out of the acrylic like we did for the
R"; "As long as we're still using the core geometric shapes"). The red is Ember again (the owner's pick), and every
icon is a few circles, triangles and rectangles that make one good silhouette, as Fog's three circles on a bar do, some
with shapes cut through them as the R's bowl is (CUTS).

Then five more passes, each from a sheet of options in one colour and in acrylic (the owner: "I'm not loving them...
they're looking too contrived", "And not quite representative enough of their theme in minimalistic terms"), to a
pictogram each, as plain as Fog's: what the atmosphere is, in the fewest shapes. Cut-outs may stay; and a shape may lie
on another (INSETS): in colour it is one more sheet laid on the rest, in one colour it is cut out where it crosses them
and kept beyond (their symmetric difference), so the flat icon still reads (the owner, of Haze: "Haze doesn't translate
well when flat. Maybe subtract the parts that overlay the circle?"). The set, each picked by the owner from its sheet:

- Ember: flames, three triangles standing on a bar, the middle one tallest, overlapping as a campfire's do (the
  owner: "Ember B is better").
- Dust: the streak a roadrunner kicks up: Fog's three circles, small, trailing a flat wedge along the ground.
- Acid: a drop, the circle and its tongue, two bubbles cut out of it, so that flat it is not a drop of water ("The two
  circle cutouts is the leader").
- Poison: a skull, a circle over a rectangle, its eyes, nose and the gaps between its teeth cut out; the eyes and nose
  raised so the nose is clear of the jaw and cut through the head's sheet alone (the owner: "the original skull but
  move the eyes and nose up so the triangle isn't cutting through both pieces of acrylic").
- Ice: icicles, three triangles hanging from a bar.
- Haze: the sun behind three bars of haze, the bars its INSETS: laid on the sun in colour, cut out of it where they
  cross it in one colour ("For haze, let's do 3 rectangles").
- Fog: the cloud mark, as it was: the one the others follow.
- Smoke: a plume drifting left to right as smoke leaves a train's stack, a small puff of two circles low on the left
  joined into a big one of three (the owner: "Almost like a train smoke stack shape"; "L2 is good for smoke").

    python3 spinoffs/barkhorn/icons.py     ->  brand/icon-<name>.svg, each in its colour (earth.py draws them all,
                                              tinted, in lines and in black, on the globe page)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import marks as M                                         # noqa: E402

OUT = os.path.join(HERE, 'brand')


def tongue(cx, cy, r, tip):
    """A triangle from `tip` to the two points where its sides touch the circle (cx, cy, r): with the circle, a drop."""
    tx, ty = tip
    d, b = math.hypot(tx - cx, ty - cy), math.atan2(ty - cy, tx - cx)
    a = math.acos(r / d)
    return ('poly', tip, (cx + r * math.cos(b + a), cy + r * math.sin(b + a)),
            (cx + r * math.cos(b - a), cy + r * math.sin(b - a)))


def _cloud(s, dx, dy):
    """Fog's three circles, scaled by s and moved."""
    return [('circle', x * s + dx, y * s + dy, r * s) for _, x, y, r in M.CLOUD[:3]]


def ember():
    return [('rect', -260, 220, 260, 300), ('poly', (-250, 260), (-30, 260), (-140, -150)),
            ('poly', (-120, 260), (120, 260), (0, -330)), ('poly', (30, 260), (250, 260), (140, -150))]


def dust():
    return _cloud(0.62, -174, 0) + [('poly', (-285, 121), (356, 121), (-285, -19))]


def acid():
    return [('circle', 0, 105, 180), tongue(0, 105, 180, (0, -290))]


def poison():
    return [('circle', 0, -55, 215), ('rect', -125, 60, 125, 235)]


def ice():
    return [('rect', -285, -290, 285, -210), ('poly', (-285, -250), (-95, -250), (-190, 140)),
            ('poly', (-95, -250), (95, -250), (0, 300)), ('poly', (95, -250), (285, -250), (190, 140))]


def haze():
    return [('circle', 0, -10, 225)]


def fog():
    return list(M.CLOUD)


def smoke():
    return [('circle', -201, 112, 60), ('circle', -111, 69, 90), ('circle', 9, -51, 120), ('circle', 154, -36, 108),
            ('circle', 54, 49, 100)]


ICONS = [('Ember', ember()), ('Dust', dust()), ('Acid', acid()), ('Poison', poison()), ('Ice', ice()),
         ('Haze', haze()), ('Fog', fog()), ('Smoke', smoke())]
CUTS = {'Acid': [('circle', -48, 145, 70), ('circle', 62, 45, 40)],
        'Poison': [('circle', -82, -88, 60), ('circle', 82, -88, 60), ('poly', (0, -28), (-34, 42), (34, 42)),
                   ('rect', -60, 175, -26, 236), ('rect', 26, 175, 60, 236)]}
INSETS = {'Haze': [('rect', -300, -25, 300, 35), ('rect', -300, 75, 300, 135), ('rect', -300, 175, 300, 235)]}
COLOURS = {name: col for key, line, num, name, col in M.SPEAKERS if line == 'Cloud'}


def shapes(name, colour=True):
    """An icon's pieces as shapely polygons, each cut by every one of its CUTS (a piece cut in two gives two): in colour
    its INSETS too, pieces laid on the rest; in one colour (colour False) the pieces' union with the insets cut out
    where they cross it and kept beyond (their symmetric difference)."""
    import earth as E
    from shapely.ops import unary_union
    cut = unary_union([E._prim_shape(c) for c in CUTS.get(name, [])])
    prims, insets = dict(ICONS)[name], INSETS.get(name, [])
    if colour or not insets:
        gs = [E._prim_shape(p) for p in prims + (insets if colour else [])]
    else:
        gs = [unary_union([E._prim_shape(p) for p in prims]).symmetric_difference(
              unary_union([E._prim_shape(p) for p in insets]))]
    out = []
    for g in gs:
        g = g.difference(cut)
        out += [q for q in getattr(g, 'geoms', [g]) if q.area > 1]
    return out


def _d(g):
    """A polygon's SVG path, its holes too (fill it even-odd)."""
    ring = lambda r: 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in list(r.coords)[:-1]) + 'Z'
    return ' '.join(ring(r) for r in [g.exterior] + list(g.interiors))


def icon_svg(name, fill, line=M.INK, size=None, label=None, stroke=M.U):
    """An icon: every shape filled, every outline over them all (fill None: the outlines alone, in `line`)."""
    wh = f' width="{size}" height="{size}"' if size else ''
    if name in CUTS:                                      # its pieces with their holes, as paths
        el = lambda g, a: f'<path d="{_d(g)}" fill-rule="evenodd" {a}/>'
        prims = [g.simplify(0.25) for g in shapes(name)]  # a quarter unit: well under a pixel at 512
    else:
        el, prims = M._el, dict(ICONS)[name] + INSETS.get(name, [])
    fills = '' if fill is None else ''.join(el(p, f'fill="{fill}"') for p in prims)
    lines = ''.join(el(p, f'fill="none" stroke="{line}" stroke-width="{stroke}" stroke-linejoin="round"') for p in prims)
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
