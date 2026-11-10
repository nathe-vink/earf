"""The flat multicolour mark (2026-11-10, the owner on Book v26: "I don't think we need the globe drawn like it is. We
can use the monochromatic globe and color in each tile to match the rendered globe instead as the multi-color
option").

The one-ink globe's tiles (earth.disc_shapes, seamed, the black mark's own pieces), each filled with its disc's one flat
shade (the owner, on Book v27: "The flat version of the logo can use one shade for each color"): six colors, six shades,
the logo's full-strength colors (earth.RING). A tile belongs to the disc in front at its middle (earth.facets). On dark
grounds the same shades, but a shade under 3:1 against night (Ember and Haze) is lifted in OKLab lightness, its hue and
chroma kept, until it reaches 3:1. (Book v27's first version filled each tile with the render's median there instead.)

    .venv-fab/bin/python spinoffs/barkhorn/globe_tiles.py [--paper PNG] [--night PNG]

Writes brand/mark/earf-globe-tiles.svg/.png, -night, earf-lockup-tiles.svg/.png, -night, and tiles.json (the colours).
"""
import argparse, json, os, subprocess, sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import earth as E                                        # noqa: E402

OUT = os.path.join(HERE, 'brand', 'mark')


def tiles():
    """Every tile of the one-ink mark: (disc index, polygon)."""
    out = []
    for i, g in enumerate(E.disc_shapes(flush=False)):
        if g is None:
            continue
        for p in getattr(g, 'geoms', [g]):
            if p.geom_type == 'Polygon' and not p.is_empty:
                out.append((i, p))
    return out


def owners(parts):
    """The disc in front at each tile's middle (earth.facets, the slabs as the one-ink mark draws them)."""
    vis = E.facets(0.0, E.THICK + E.SEAM)
    out = []
    for _, p in parts:
        q = p.representative_point()
        hits = [i for i, v in enumerate(vis) if v.contains(q)]
        out.append(hits[0] if hits else min(range(len(vis)), key=lambda i: vis[i].distance(q)))
    return out


def _Y(h):
    v = np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)]) / 255
    v = np.where(v <= 0.04045, v / 12.92, ((v + .055) / 1.055) ** 2.4)
    return float(v @ [.2126, .7152, .0722])


def on_dark(h, ground=None, ratio=3.0):
    """`h` lifted in OKLab lightness (hue and chroma kept, eased into gamut) until it stands `ratio`:1 against night."""
    import globe_real as G
    g = _Y(ground or E.NIGHT)
    lift = 0.0
    c = h
    while (_Y(c) + .05) / (g + .05) < ratio and lift < 0.5:
        lift += 0.005
        c = G._vivid_hex(h, 1.0, lift)
    return c


def colours(render, parts, shrink=0.012):
    im = np.asarray(Image.open(render).convert('RGB'))
    px = im.shape[0]; e = 1 + E.W_LINE / 2
    to = lambda x, y: ((x + e) / (2 * e) * px, (e - y) / (2 * e) * px)
    cols = []
    for _, p in parts:
        q = p.buffer(-shrink)
        q = q if not q.is_empty else p
        mask = Image.new('L', (px, px), 0); d = ImageDraw.Draw(mask)
        for r in getattr(q, 'geoms', [q]):
            d.polygon([to(x, y) for x, y in r.exterior.coords], fill=255)
        sel = np.asarray(mask) > 0
        c = np.median(im[sel], axis=0) if sel.sum() else np.array([128, 128, 128])
        cols.append('#%02X%02X%02X' % tuple(int(round(v)) for v in c))
    return cols


def body(parts, cols):
    return ''.join(f'<path d="{E._poly_d(p)}" fill="{c}" fill-rule="evenodd"/>' for (_, p), c in zip(parts, cols))


def write(parts, cols, tag, word):
    e = 1 + E.W_LINE / 2
    b = body(parts, cols)
    g = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.4f} {-e:.4f} {2 * e:.4f} {2 * e:.4f}" role="img" '
         f'aria-label="EARF"><title>EARF</title>{b}</svg>')
    k = 225 / e
    vw, vh, gap = 450 + 110 + E.M.WORDMARK_W, 450, 110
    lk = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" role="img" aria-label="EARF"><title>EARF</title>'
          f'<g transform="translate(225 225) scale({k:.4f})">{b}</g><g transform="translate({450 + gap} 75)" fill="{word}">'
          + ''.join(f'<path d="{d}"/>' for d in E.letters()) + '</g></svg>')
    files = []
    for name, svg, w in ((f'earf-globe-tiles{tag}', g, 1024), (f'earf-lockup-tiles{tag}', lk, 2048)):
        f = os.path.join(OUT, name)
        open(f + '.svg', 'w').write(svg)
        subprocess.run(['rsvg-convert', '-w', str(w), f + '.svg', '-o', f + '.png'], check=True)
        files += [f + '.svg', f + '.png']
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--paper', default=os.path.join(OUT, 'earf-globe-render.png'))
    ap.add_argument('--night', default=os.path.join(OUT, 'earf-globe-render-night.png'))
    a = ap.parse_args()
    parts = tiles()
    own = owners(parts)
    dark = {E.RING[i]: on_dark(E.RING[i]) for i in range(6)}
    rec = {'lifted on dark': {E.RING_NAMES[i]: [E.RING[i], dark[E.RING[i]]] for i in range(6) if dark[E.RING[i]] != E.RING[i]}}
    for tag, word in (('', E.INK), ('-night', E.WHITE)):
        cols = [E.RING[o] if not tag else dark[E.RING[o]] for o in own]
        rec[tag or 'paper'] = [{'disc': E.RING_NAMES[o], 'colour': c} for o, c in zip(own, cols)]
        for f in write(parts, cols, tag, word):
            print(f)
    json.dump(rec, open(os.path.join(OUT, 'tiles.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
