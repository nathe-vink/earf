"""The flat multicolour mark (2026-11-10, the owner on Book v26: "I don't think we need the globe drawn like it is. We
can use the monochromatic globe and color in each tile to match the rendered globe instead as the multi-color
option").

The one-ink globe's tiles (earth.disc_shapes, seamed, the black mark's own pieces) each filled with one flat colour: the
median of the rendered globe (globe_real.py, A3) inside that tile, the tile shrunk a little first so its edges and the
render's rims don't pull the median. The seams are the one-ink mark's. One for light grounds, from the paper render, and
one for dark grounds, from the night render; and the lockups from each.

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
    rec = {}
    for tag, render, word in (('', a.paper, E.INK), ('-night', a.night, E.WHITE)):
        cols = colours(render, parts)
        rec[tag or 'paper'] = [{'disc': i, 'colour': c} for (i, _), c in zip(parts, cols)]
        for f in write(parts, cols, tag, word):
            print(f)
    json.dump(rec, open(os.path.join(OUT, 'tiles.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
