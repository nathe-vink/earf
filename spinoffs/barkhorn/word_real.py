"""Round 29: EARF as the real thing, path-traced as the globe is, and its colour files traced from it.

The owner, of the wordmark: "Should there be a hole in the are or did we still want to show EARF as combined shapes
sometime? Should we also have an acrylic version of EARF as well as monochromatic versions?" Shown the R with a hole 70
in, the letters' shapes as acrylic sheets, deeper where they overlap, and the solid letters for one colour, and asked
whether to make them: "Yes".

So EARF is built as a sign: each of its thirteen shapes (marks.py's WORDMARK, the R's bowl a ring since this round) cut
from the Clouds' own 20 mm tinted cast acrylic, as the globe's discs are, the word 980 mm across on a cap height of
300, each piece's edges rounded over (ROUND) and polished, and the pieces laid on one another as a layered sign is made
(LAYER): the stems and the A's first leg at the back; the bars, the R's bowl and the A's second leg on them; the A's
crossbar and the R's leg in front. A colour per letter (LETTERS): the E red (Flare), the A yellow (Acid), the R blue
(Ice, the globe's equator), the F green (Poison); the R, with the most sheets over one another, in the lighter of the
two cool hues, so its overlaps stay clear. It is rendered with globe_real.py's acrylic, room and lights, its presets
too (LIGHTS on paper; DARK on night, each piece's rim glowing its colour and its faces faint), square on and
orthographic, so a render lies over the flat drawing exactly. Where pieces overlap, the light crosses two or three
sheets and the colour deepens, so the construction shows without an outline.

The flat colour files are traced from the renders (files): each letter's regions where one, two or three sheets lie,
filled with the colour the render shows there (the median of its pixels, the rounded edges left out), and on night each
piece's rim too, the band its rounding shows, in the colour it glows.

    python3 spinoffs/barkhorn/word_real.py --still OUT.png [--dark] [--px 2120] [--samples 128]
    python3 spinoffs/barkhorn/word_real.py --files PAPER NIGHT       the renders (ground made even) and the flat colour
                                                                     files, into brand/mark
"""
import argparse, math, os, subprocess, sys, tempfile, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import earth as E                                        # noqa: E402
import marks as M                                        # noqa: E402
import globe_real as G                                   # noqa: E402  (and, through it, studio/engine)

UNIT = 0.001                                             # a wordmark unit in metres: the cap height 300 mm
SHEET = G.T                                              # the Clouds' 20 mm cast acrylic, as the globe's discs
GAP = 0.0002                                             # between two sheets laid one on the other
ROUND = 0.004                                            # each piece's edges rounded over, polished
MARGIN = 40                                              # wordmark units clear round the word in a render
LETTERS = ['flare', 'acid', 'ice', 'poison']             # E, A, R, F: a colour per letter
LETTER = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]         # which letter each shape of WORDMARK belongs to
LAYER = [0, 1, 1, 1, 0, 1, 2, 0, 1, 2, 0, 1, 1]          # each shape's sheet, counted from the back
SEG = 192                                                # a round edge's segments
CLEAR, SCATTER, VIVID = 0.9, 0.005, (1.2, 0.0)           # the acrylic, on paper and on night: clearer than the globe's
                                                         # (0.45 on paper), as a word is seen square on through one sheet,
                                                         # so where a second or a third lies the colour visibly deepens;
                                                         # the hues a fifth livelier (OKLCh chroma), as the globe's on paper


def _outline(p):
    """A shape's outline (wordmark units, y down) and, for a ring, its hole's: (points, hole points or None)."""
    if p[0] in ('circle', 'ring'):
        a = np.linspace(0, 2 * np.pi, SEG, endpoint=False)
        ring = lambda r: [(p[1] + r * math.cos(t), p[2] + r * math.sin(t)) for t in a]
        return ring(p[3]), (ring(p[4]) if p[0] == 'ring' else None)
    if p[0] == 'rect':
        return [(p[1], p[2]), (p[3], p[2]), (p[3], p[4]), (p[1], p[4])], None
    return list(p[1:]), None


def piece(bpy, name, p, layer):
    """One shape as a piece of sheet, SHEET deep toward the camera at its layer (the camera looks along +y), a ring's hole
    through it, its edges rounded over ROUND (a bevel of four segments on every edge sharper than 30 degrees)."""
    import bmesh
    pts, hole = _outline(p)
    y1 = -layer * (SHEET + GAP)                          # its back face; its front SHEET nearer the camera
    w = lambda x, y, yy: (bm.verts.new(((x - M.WORDMARK_W / 2) * UNIT, yy, (150 - y) * UNIT)))
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    back = [w(x, y, y1) for x, y in pts]
    front = [w(x, y, y1 - SHEET) for x, y in pts]
    n = len(pts)
    if hole is None:
        bm.faces.new(back); bm.faces.new(front[::-1])
    else:                                                # a ring: its faces strips of quads between the two circles
        hb = [w(x, y, y1) for x, y in hole]
        hf = [w(x, y, y1 - SHEET) for x, y in hole]
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([back[i], back[j], hb[j], hb[i]]); bm.faces.new([front[i], hf[i], hf[j], front[j]])
            bm.faces.new([hb[i], hb[j], hf[j], hf[i]])
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([back[i], front[i], front[j], back[j]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    mod = ob.modifiers.new('round', 'BEVEL')
    mod.width, mod.segments, mod.profile = ROUND, 4, 0.5
    mod.limit_method, mod.angle_limit = 'ANGLE', math.radians(30)
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.clear()
    ob.data = me2
    bpy.data.meshes.remove(me)
    me2.shade_smooth()
    me2.set_sharp_from_angle(angle=math.radians(25))
    return ob


def build(bpy, body, clear, scatter=0.012, neon=(0.0, 0.0)):
    """The thirteen pieces, each letter in its acrylic (`body`: globe_real._body's (face, scatter) colours by name): the
    faces square to the camera one material, the rim (the sides and the rounding) another, which on dark grounds
    (`neon`) gives off its colour at the first strength and the faces at the second, as the globe's rims do."""
    import materials as Mt
    lit = max(neon) > 0

    def acrylic(name, k, see):
        face, deep = body[k]
        return Mt.make(bpy, name, 'cast_resin', {'color': face, 'deep': deep, 'radius': scatter, 'roughness': G.POLISH,
                                                  'cloud': 0.0, 'fibre': 0.0, 'clear': see})
    mats = {}
    for k in LETTERS:
        f = acrylic(f'acrylic-{k}', k, clear)
        r = acrylic(f'rim-{k}', k, min(clear, 0.25)) if lit else f
        if lit:
            G._emit(f, E._C[k.title()], neon[1]); G._emit(r, E._C[k.title()], neon[0])
        mats[k] = (f, r)
    obs = []
    for i, p in enumerate(M.WORDMARK):
        k = LETTERS[LETTER[i]]
        ob = piece(bpy, f'piece-{i:02d}-{k}', p, LAYER[i])
        me = ob.data
        me.materials.append(mats[k][0]); me.materials.append(mats[k][1])
        for f in me.polygons:
            f.material_index = 0 if abs(f.normal.y) > 0.99 else 1
        obs.append(ob)
    return obs


def frame():
    """A render's frame in wordmark units, (width, height): the word and MARGIN round it."""
    return M.WORDMARK_W + 2 * MARGIN, 300 + 2 * MARGIN


def stage(bpy, a):
    """globe_real's stage (the ground a backdrop of exactly its colour, the room, the key and the fill), its camera
    framing the word, square on and orthographic."""
    fw, fh = frame()
    G.stage(bpy, a.ground, a.px, 1.0, a.samples, a.env, a.adaptive, a.key, a.fill, tuple(a.shine), a.bounces)
    scene = bpy.context.scene
    scene.camera.data.ortho_scale = fw * UNIT
    scene.render.resolution_x, scene.render.resolution_y = a.px, round(a.px * fh / fw)


def regions():
    """Each letter's regions by how many sheets lie there: [(letter, sheets, shapely geometry), ...], wordmark units."""
    from shapely.ops import polygonize, unary_union
    out = []
    for li in range(4):
        shapes = [E._prim_shape(p) for i, p in enumerate(M.WORDMARK) if LETTER[i] == li]
        faces = polygonize(unary_union([s.boundary for s in shapes]))
        by = {}
        for f in faces:
            q = f.representative_point()
            n = sum(s.contains(q) for s in shapes)
            if n:
                by.setdefault(n, []).append(f)
        out += [(li, n, unary_union(fs)) for n, fs in sorted(by.items())]
    return out


def _mask(geom, shape, scale):
    """A geometry (wordmark units) as a boolean mask over a render `shape` (h, w) at `scale` px a unit."""
    from PIL import Image, ImageDraw
    im = Image.new('L', (shape[1], shape[0]), 0)
    d = ImageDraw.Draw(im)
    px = lambda c: [((x + MARGIN) * scale, (y + MARGIN) * scale) for x, y in c]
    for poly in getattr(geom, 'geoms', [geom]):
        if poly.is_empty or poly.geom_type != 'Polygon':
            continue
        d.polygon(px(poly.exterior.coords), fill=255)
        for r in poly.interiors:
            d.polygon(px(r.coords), fill=0)
    return np.asarray(im) > 127


def _hex(v):
    return '#%02X%02X%02X' % tuple(int(round(c)) for c in v)


def _d(g):
    """A geometry's SVG path, in wordmark units (y down, as the SVG's)."""
    ring = lambda r: 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in list(r.coords)[:-1]) + 'Z'
    return ' '.join(ring(r) for q in getattr(g, 'geoms', [g]) if q.geom_type == 'Polygon' and not q.is_empty
                    for r in [q.exterior] + list(q.interiors))


def traced(render, rims=False):
    """The flat colour drawing traced from a render (a PNG of `frame` at any size): each region (regions) its median
    colour, sampled ROUND and a little more inside its edges; with `rims`, each piece's rim (the band ROUND inside its
    outline) over them, in the median colour of the bands. Returns the SVG's body, in wordmark units."""
    from PIL import Image
    v = np.asarray(Image.open(render).convert('RGB')).astype(float)
    scale = v.shape[1] / frame()[0]
    inset = ROUND / UNIT + 3
    body = ''
    for li, n, g in regions():
        m = _mask(g.buffer(-inset), v.shape[:2], scale)
        col = np.median(v[m], axis=0) if m.sum() > 20 else np.median(v[_mask(g, v.shape[:2], scale)], axis=0)
        body += f'<path d="{_d(g)}" fill="{_hex(col)}" fill-rule="evenodd"/>'
    if rims:
        for li in range(4):
            bands = [E._prim_shape(p).difference(E._prim_shape(p).buffer(-ROUND / UNIT)) for i, p in enumerate(M.WORDMARK)
                     if LETTER[i] == li]
            m = np.zeros(v.shape[:2], bool)
            for b in bands:
                m |= _mask(b.buffer(-1), v.shape[:2], scale)
            col = np.percentile(v[m], 90, axis=0)       # the band glows brightest along its middle
            for b in bands:
                body += f'<path d="{_d(b)}" fill="{_hex(col)}" fill-rule="evenodd"/>'
    return body


def files(paper, night, w=2048, out=os.path.join(HERE, 'brand', 'mark')):
    """The renders and the flat files traced from them, into brand/mark: earf-wordmark-render.png and -render-night.png
    (each on its ground made even), earf-wordmark-colour.svg (for light grounds) and -colour-ink.svg (for dark: the rims
    as they glow), each with a transparent PNG `w` px wide."""
    made = []
    for src, tag, ground, rims in ((paper, '', E.PAPER, False), (night, '-night', E.NIGHT, True)):
        f = os.path.join(out, f'earf-wordmark-render{tag}.png')
        G._even_ground(src, ground).save(f)
        made.append(f)
        name = 'colour' if not rims else 'colour-ink'
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {M.WORDMARK_W} 300" role="img" '
               f'aria-label="EARF, acrylic, {"for dark grounds" if rims else "for light grounds"}"><title>EARF</title>'
               + traced(src, rims) + '</svg>')
        f = os.path.join(out, f'earf-wordmark-{name}.svg')
        open(f, 'w').write(svg)
        subprocess.run(['rsvg-convert', '-w', str(w), f, '-o', f[:-4] + '.png'], check=True)
        made += [f, f[:-4] + '.png']
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--still', help='the word, square on, to this PNG')
    ap.add_argument('--dark', action='store_true', help="globe_real's DARK room, lights and neon where not given (the rims "
                                                        "glowing), else LIGHTS'; the acrylic the word's own (CLEAR, VIVID)")
    ap.add_argument('--ground', choices=sorted(G.GROUNDS))
    ap.add_argument('--px', type=int, default=2120, help='the width (the height follows the frame)')
    ap.add_argument('--samples', type=int, default=128)
    ap.add_argument('--adaptive', type=float, default=0.01)
    ap.add_argument('--env', choices=['studio', 'dim', 'grey', 'dark'])
    ap.add_argument('--key', type=float)
    ap.add_argument('--fill', type=float)
    ap.add_argument('--neon', type=float, nargs=2, metavar=('RIM', 'FACE'))
    ap.add_argument('--body', choices=['mark', 'cabinet', 'horn', 'through', 'through-deep'])
    ap.add_argument('--clear', type=float, default=CLEAR, help='the share of light crossing a sheet straight through')
    ap.add_argument('--vivid', type=float, nargs=2, default=VIVID, metavar=('CHROMA', 'LIFT'))
    ap.add_argument('--scatter', type=float, default=SCATTER)
    ap.add_argument('--shine', type=float, nargs=2, default=(0.4, 0.0), metavar=('KEY', 'FILL'))
    ap.add_argument('--bounces', type=int, default=96)
    ap.add_argument('--files', nargs=2, metavar=('PAPER', 'NIGHT'), help='the renders and the traced flat files, into brand/mark')
    ap.set_defaults(glow=False)
    a = ap.parse_args()
    if a.files:
        for f in files(*a.files):
            print(os.path.relpath(f, HERE))
    if not a.still:
        return
    G.lighting(a)
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.preferences.addon_enable(module='cycles')
    t0 = time.time()
    build(bpy, G._body(a.body, G._hues(*a.vivid)), a.clear, a.scatter, tuple(a.neon))
    stage(bpy, a)
    bpy.context.scene.render.filepath = os.path.abspath(a.still)
    bpy.ops.render.render(write_still=True)
    print(f'{a.still}  {time.time() - t0:.0f} s')


if __name__ == '__main__':
    main()
