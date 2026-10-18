"""Round 30: the eight icons as the real thing, each cut from its own speaker's acrylic and path-traced as EARF is.

The owner, of the icons (icons.py, round 23): "I like the idea but they look really low fidelity relative to everything
else". So each icon is built as EARF's sign is (word_real.py): every shape a piece of the Clouds' 20 mm cast acrylic in
that speaker's colour, its edges rounded over and polished, and where shapes overlap the pieces laid one on another,
each on the lowest sheet clear of every earlier piece it overlaps (layers), so the light crosses two or three sheets
there and the colour deepens, as the round-23 drawings meant by "stacked clear acrylic". Rendered square on and
orthographic with globe_real's acrylic, room and presets: on paper (LIGHTS) and on night (DARK, each rim glowing its
colour). The six hues are EARF's letters' acrylic (through-deep, VIVID); Fog's is water-clear, as the Fog Cloud's, and
shows by its edges; Smoke's is smoked. On night Fog's faces glow less than the hues' so they stay clear, and Smoke's
faces stay dark while its rims glow the grey its lines take on ink (earth.ON_INK).

An icon is drawn 800 units across; a unit here is UNIT (half a millimetre), so an icon is 400 mm across and its
sheet, as thick as EARF's, reads twice as deep: an icon is seen small, and its rounded rims must still catch the light.

From the renders (files): each render on its ground made even, a flat colour icon traced from it (its one-, two- and
three-sheet regions in the render's median colour), and each icon solid, every shape merged, in black, white and its
own colour, for one-colour uses. A shape laid on the rest (icons.INSETS: Haze's bars) is one more sheet in the render
and the traced file, and cut out where it crosses the rest in the solid ones (icons.shapes in one colour).

And the loader's coins (the owner: "should the circle loading indicator use the acrylic coins instead of flat
circles?"): a disc of the same sheet for each speaker (COIN), 76 mm across so its rounded rim still shows at the 20 px
or so a loader draws it, rendered as the icons are.

    python3 spinoffs/barkhorn/icons_real.py --still OUT.png --icon Ice [--dark] [--px 800] [--samples 128] [--coin]
    python3 spinoffs/barkhorn/icons_real.py --files DIR       DIR/<icon>-paper.png and -night.png into brand/icons
"""
import argparse, os, subprocess, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import earth as E                                        # noqa: E402
import icons as IC                                       # noqa: E402
import globe_real as G                                   # noqa: E402
import word_real as W                                    # noqa: E402

UNIT = 0.0005                                            # an icon unit in metres: 800 units, 400 mm across
SIZE = (800, 800)                                        # an icon's drawing, centred on its origin
FOG = '#EEF4F6'                                          # water-clear, the faintest cool cast of thick clear acrylic
SMOKE_K = 0.75                                           # Smoke's face: its colour to the 0.75, which renders a dark
                                                         # smoked grey (a face renders near its own colour; at 0.3 to
                                                         # 0.45 it read mid grey, as plastic)
ON_INK = {'Smoke': E.ON_INK['Smoke']}                    # its rims' glow on night
NEON = {'Fog': (1.0, 0.06), 'Smoke': (0.8, 0.0)}         # on night, (rim, face): Fog's faces kept clear and Smoke's
                                                         # dark (at the hues' 0.15 they glowed milky grey)
COIN, COIN_UNIT = ('circle', 0, 0, 380), 0.0001          # the loader's coins: a disc of the sheet, 76 mm across
OUT = os.path.join(HERE, 'brand', 'icons')


def layers(shapes):
    """Each shape's sheet, counted from the back: the lowest clear of every earlier shape it overlaps by more than a
    sliver (shapes that only touch share one)."""
    out = []
    for i, s in enumerate(shapes):
        taken = {out[j] for j in range(i) if s.intersection(shapes[j]).area > 1.0}
        out.append(min(set(range(len(shapes) + 1)) - taken))
    return out


def body(name, vivid=W.VIVID):
    """An icon's acrylic, (face, scatter): its speaker's hue as EARF's letters take theirs; Fog clear; Smoke smoked."""
    hue = E._C[name]
    if name == 'Fog':
        return FOG, FOG
    if name == 'Smoke':
        return G._root_hex(hue, SMOKE_K), hue
    v = G._vivid_hex(hue, *vivid)
    return G._root_hex(v, 0.65), v


def items(name, coin=False):
    """The icon's pieces (icons.shapes: each cut by its CUTS, as polygons), or its coin, each on its sheet."""
    if coin:
        return [(COIN, 0, name.lower())]
    gs = IC.shapes(name)
    return [(('shape', g), layer, name.lower()) for g, layer in zip(gs, layers(gs))]


def render(a):
    own = a.neon is None and a.dark and a.icon in NEON
    G.lighting(a)
    if own:
        a.neon = NEON[a.icon]
    import bpy
    W.UNIT = COIN_UNIT if a.coin else UNIT
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.preferences.addon_enable(module='cycles')
    t0 = time.time()
    W.build(bpy, {a.icon.lower(): body(a.icon, tuple(a.vivid))}, a.clear, a.scatter, tuple(a.neon),
            items(a.icon, a.coin), centre=(0, 0), glows={k.lower(): v for k, v in ON_INK.items()})
    W.stage(bpy, a, SIZE)
    bpy.context.scene.render.filepath = os.path.abspath(a.still)
    bpy.ops.render.render(write_still=True)
    print(f'{a.still}  {time.time() - t0:.0f} s')


def regions(name):
    """An icon's regions by how many sheets lie there: [(sheets, shapely geometry), ...], icon units."""
    from shapely.ops import polygonize, unary_union
    shapes = IC.shapes(name)
    by = {}
    for f in polygonize(unary_union([s.boundary for s in shapes])):
        q = f.representative_point()
        n = sum(s.contains(q) for s in shapes)
        if n:
            by.setdefault(n, []).append(f)
    return [(n, unary_union(fs)) for n, fs in sorted(by.items())]


def _mask(geom, shape, scale):
    """A geometry (icon units, centred) as a boolean mask over a render `shape` (h, w) at `scale` px a unit."""
    from shapely.affinity import translate
    return W._mask(translate(geom, SIZE[0] / 2, SIZE[1] / 2), shape, scale)


def _svg(body_, label):
    w, h = SIZE
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-w / 2:g} {-h / 2:g} {w} {h}" role="img" '
            f'aria-label="{label}"><title>{label}</title>{body_}</svg>')


def traced(name, render_png):
    """The flat colour icon traced from a render: each region (regions) its median colour, sampled inside its edges."""
    from PIL import Image
    v = np.asarray(Image.open(render_png).convert('RGB')).astype(float)
    scale = v.shape[1] / W.frame(SIZE)[0]
    inset = W.ROUND / UNIT + 3
    out = ''
    for n, g in regions(name):
        m = _mask(g.buffer(-inset), v.shape[:2], scale)
        col = np.median(v[m], axis=0) if m.sum() > 20 else np.median(v[_mask(g, v.shape[:2], scale)], axis=0)
        out += f'<path d="{W._d(g)}" fill="{W._hex(col)}" fill-rule="evenodd"/>'
    return out


def solid(name, fill):
    """The icon in one colour: every shape merged into one, its insets cut out where they cross the rest."""
    from shapely.ops import unary_union
    g = unary_union(IC.shapes(name, colour=False)).simplify(0.25)
    return f'<path d="{W._d(g)}" fill="{fill}" fill-rule="evenodd"/>'


def files(src, out=OUT, w=512):
    """From src/<icon>-paper.png and -night.png: icon-<name>-render.png and -render-night.png (each on its ground made
    even), icon-<name>-colour.svg (traced from the paper render) and icon-<name>-<black|white|own>.svg (solid), each SVG
    with a transparent PNG `w` px across."""
    os.makedirs(out, exist_ok=True)
    made = []
    for name, _ in IC.ICONS:
        k = name.lower()
        for tag, ground in (('paper', E.PAPER), ('night', E.NIGHT)):
            f = os.path.join(out, f'icon-{k}-render{"" if tag == "paper" else "-night"}.png')
            G._even_ground(os.path.join(src, f'{k}-{tag}.png'), ground).save(f)
            made.append(f)
        svgs = {'colour': traced(name, os.path.join(src, f'{k}-paper.png')),
                'black': solid(name, E.INK), 'white': solid(name, E.WHITE), 'own': solid(name, E._C[name])}
        for tag, b in svgs.items():
            f = os.path.join(out, f'icon-{k}-{tag}.svg')
            open(f, 'w').write(_svg(b, f'{name}, {tag}'))
            subprocess.run(['rsvg-convert', '-w', str(w), f, '-o', f[:-4] + '.png'], check=True)
            made += [f, f[:-4] + '.png']
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--still', help='an icon, square on, to this PNG')
    ap.add_argument('--icon', choices=[n for n, _ in IC.ICONS], default='Ice')
    ap.add_argument('--coin', action='store_true', help="the icon's speaker's coin (the loader's) in place of its icon")
    ap.add_argument('--dark', action='store_true', help="globe_real's DARK room, lights and neon (the rims glowing)")
    ap.add_argument('--ground', choices=sorted(G.GROUNDS))
    ap.add_argument('--px', type=int, default=800)
    ap.add_argument('--samples', type=int, default=128)
    ap.add_argument('--adaptive', type=float, default=0.01)
    ap.add_argument('--env', choices=['studio', 'dim', 'grey', 'dark'])
    ap.add_argument('--key', type=float)
    ap.add_argument('--fill', type=float)
    ap.add_argument('--neon', type=float, nargs=2, metavar=('RIM', 'FACE'))
    ap.add_argument('--body', choices=['mark', 'cabinet', 'horn', 'through', 'through-deep'])
    ap.add_argument('--clear', type=float, default=W.CLEAR)
    ap.add_argument('--vivid', type=float, nargs=2, default=W.VIVID, metavar=('CHROMA', 'LIFT'))
    ap.add_argument('--scatter', type=float, default=W.SCATTER)
    ap.add_argument('--shine', type=float, nargs=2, default=(0.4, 0.0), metavar=('KEY', 'FILL'))
    ap.add_argument('--bounces', type=int, default=96)
    ap.add_argument('--files', metavar='DIR', help='the renders, traced and solid icons, into brand/icons')
    ap.set_defaults(glow=False)
    a = ap.parse_args()
    if a.files:
        for f in files(a.files):
            print(os.path.relpath(f, HERE))
    if a.still:
        render(a)


if __name__ == '__main__':
    main()
