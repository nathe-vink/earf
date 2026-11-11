"""THE STAGE, second version (the owner, 2026-11-11 14:55: "too elementary and not elevated or proper enough"): scenic
pieces like real scenic art, not plywood toys. Each is two or three overlapping flat layers, tone on tone in a deep,
muted version of its tint, no outline, drawn after the brand's tint icons (r47-brand): Ember flames, Dust dunes under
blowing dust, Acid drops, Poison grass and leaves, Ice shards, Haze a low sun in bands, Fog cloud, Smoke plumes.

    .venv-fab/bin/python spinoffs/barkhorn/campaign/stage/make_scenic.py      ->  stage/scenic.json, stage/scenic-sheet.png

scenic.json: tint -> [{outline: [[u, v], ...] (0-1, v up), color: hex, depth: layer index 0 = back}], each layer's
outline traced from its own drawn mask (make_cutouts.outline's method), the colours the tint taken toward a deep grey.
"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_cutouts import _filled, _simplify  # noqa: E402
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

N = 512
TINT = {'ember': '#B50404', 'dust': '#D35D17', 'acid': '#C5BC1E', 'poison': '#027614', 'ice': '#1169C1',
        'haze': '#500CB4', 'fog': '#E2E1DF', 'smoke': '#8E8D8B'}


def _muted(hx, value, sat=0.6):
    """The tint at a given value (0-1) and its saturation cut to `sat`: deep and muted, tone on tone."""
    import colorsys
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb(h, s * sat, value)
    return '#%02X%02X%02X' % tuple(round(c * 255) for c in (r, g, b))


def _canvas():
    im = Image.new('L', (N, N), 0)
    return im, ImageDraw.Draw(im)


def _pts(f, a, b, n=60):
    return [f(a + (b - a) * k / n) for k in range(n + 1)]


def flame(cx, w, h, lean=0.0, base=0.98):
    """A flame tongue: a base of width w at cx, a curved tip h up, leaning."""
    def side(sgn):
        return _pts(lambda t: ((cx + sgn * w / 2 * (1 - t) ** 0.8 * (1 + 0.35 * math.sin(math.pi * t)) + lean * t ** 2) * N,
                               (base - h * t) * N), 0, 1)
    return side(-1) + side(1)[::-1]


def layers(t):
    """The drawn masks for one tint, back to front."""
    out = []
    if t == 'ember':
        for spec in ([(0.30, 0.34, 0.80, -0.06), (0.62, 0.30, 0.92, 0.05)], [(0.47, 0.42, 0.98, 0.02), (0.20, 0.22, 0.55, -0.03)],
                     [(0.42, 0.26, 0.62, 0.04), (0.68, 0.22, 0.50, 0.03)]):
            im, d = _canvas()
            for cx, w, h, ln in spec:
                d.polygon(flame(cx, w, h, ln), fill=255)
            out.append(im)
    elif t == 'dust':
        for k, (amp, y0, ph) in enumerate(((0.10, 0.62, 0.0), (0.09, 0.74, 1.6), (0.07, 0.86, 3.0))):
            im, d = _canvas()
            top = _pts(lambda u: (u * N, (y0 - amp * math.sin(2.2 * math.pi * u + ph) - 0.05 * u) * N), 0, 1)
            d.polygon(top + [(N, N), (0, N)], fill=255)
            if k == 0:   # blowing dust over the back dune: long streaks off to the right
                for y, x0, l, th in ((0.30, 0.08, 0.70, 0.05), (0.40, 0.18, 0.62, 0.04), (0.22, 0.30, 0.50, 0.03)):
                    d.rounded_rectangle([x0 * N, y * N, (x0 + l) * N, (y + th) * N], radius=th * N / 2, fill=255)
            out.append(im)
    elif t == 'acid':
        def drop(cx, cy, r):
            pts = _pts(lambda a: (cx + r * math.sin(a) * (1 - 0.0 * math.cos(a)), cy - r * (math.cos(a) if math.cos(a) < 0 else math.cos(a) * 0.0)), 0, 2 * math.pi)
            return pts
        for spec in ([(0.36, 0.60, 0.30)], [(0.66, 0.70, 0.22)], [(0.28, 0.86, 0.12), (0.52, 0.90, 0.09)]):
            im, d = _canvas()
            for cx, cy, r in spec:
                d.ellipse([(cx - r) * N, (cy - r) * N, (cx + r) * N, (cy + r) * N], fill=255)
                d.polygon([((cx - r * 0.86) * N, (cy - r * 0.5) * N), (cx * N, (cy - r * 2.5) * N), ((cx + r * 0.86) * N, (cy - r * 0.5) * N)], fill=255)
            out.append(im)
    elif t == 'poison':
        rnd = np.random.default_rng(4)
        for k in range(3):
            im, d = _canvas()
            for j in range(9 - 2 * k):
                rx = 0.1 + 0.8 * rnd.random(); h = (0.75 - 0.18 * k) * (0.6 + 0.4 * rnd.random()); w = 0.05 + 0.03 * rnd.random()
                tip = rx + (rnd.random() - 0.5) * 0.3
                d.polygon([((rx - w) * N, N), ((tip) * N, (1 - h) * N), ((rx + w) * N, N)], fill=255)
            if k == 1:   # two broad leaves
                for cx, ang in ((0.28, -0.6), (0.72, 0.6)):
                    leaf = _pts(lambda a: (0.5 + 0.13 * math.sin(a), 0.5 - 0.30 * math.cos(a)), 0, 2 * math.pi)
                    rot = [(cx + (x - 0.5) * math.cos(ang) - (y - 0.5) * math.sin(ang), 0.62 + (x - 0.5) * math.sin(ang) + (y - 0.5) * math.cos(ang)) for x, y in leaf]
                    d.polygon([(x * N, y * N) for x, y in rot], fill=255)
            out.append(im)
    elif t == 'ice':
        for spec in ([(0.25, 0.10, 0.85), (0.62, 0.12, 0.98)], [(0.42, 0.12, 0.80), (0.80, 0.09, 0.62)], [(0.18, 0.08, 0.45), (0.55, 0.10, 0.55)]):
            im, d = _canvas()
            for cx, w, h in spec:
                d.polygon([((cx - w) * N, N), ((cx - w * 0.15) * N, (1 - h) * N), ((cx + w * 0.3) * N, (1 - h * 0.92) * N), ((cx + w) * N, N)], fill=255)
            out.append(im)
    elif t == 'haze':
        im, d = _canvas(); d.ellipse([0.15 * N, 0.25 * N, 0.85 * N, 0.95 * N], fill=255); d.rectangle([0, 0.66 * N, N, N], fill=0); out.append(im)
        im, d = _canvas()
        for y in (0.68, 0.78, 0.88):
            d.rectangle([0.05 * N, y * N, 0.95 * N, (y + 0.065) * N], fill=255)
        out.append(im)
    elif t == 'fog':
        for spec in ([(0.30, 0.62, 0.20), (0.55, 0.52, 0.26), (0.78, 0.64, 0.18)], [(0.22, 0.78, 0.18), (0.48, 0.72, 0.22), (0.74, 0.80, 0.18)]):
            im, d = _canvas()
            for cx, cy, r in spec:
                d.ellipse([(cx - r) * N, (cy - r) * N, (cx + r) * N, (cy + r) * N], fill=255)
            d.rectangle([0.12 * N, 0.80 * N, 0.88 * N, 0.98 * N], fill=255)
            out.append(im)
    elif t == 'smoke':
        for k, (x0, sway) in enumerate(((0.38, 0.10), (0.60, -0.08), (0.46, 0.05))):
            im, d = _canvas()
            for j in range(7):
                y = 0.92 - 0.12 * j; r = 0.07 + 0.025 * j - 0.03 * k
                x = x0 + sway * math.sin(j * 0.9 + k)
                d.ellipse([(x - r) * N, (y - r) * N, (x + r) * N, (y + r) * N], fill=255)
            out.append(im)
    return out


def trace(im):
    a = np.asarray(im).astype(float)
    m = np.pad(_filled(a).astype(float), 2)
    cs = plt.contour(m, levels=[0.5]); segs = cs.allsegs[0]; plt.close('all')
    rings = []
    for s in segs:
        if len(s) < 12:
            continue
        p = np.array(s) - 2.0
        j = int(np.argmax(np.hypot(*(p - p[0]).T)))
        p = np.vstack([_simplify(p[:j + 1], 1.2)[:-1], _simplify(np.vstack([p[j:], p[:1]]), 1.2)[:-1]])
        rings.append([[round(float(x) / (N - 1), 4), round(1.0 - float(y) / (N - 1), 4)] for x, y in p])
    return rings


def main():
    out, sheet = {}, Image.new('RGB', (N * 8 // 2, N // 2), '#101010')
    for k, (t, hx) in enumerate(TINT.items()):
        ls = layers(t); n = len(ls)
        vals = [0.34, 0.46, 0.58][:n] if t not in ('fog',) else [0.52, 0.64, 0.76][:n]
        if t == 'smoke':
            vals = [0.24, 0.33, 0.42][:n]
        sat = 0.0 if t in ('fog', 'smoke') else 0.68
        out[t] = []
        for i, im in enumerate(ls):
            col = _muted(hx, vals[i], sat)
            for ring in trace(im):            # a layer may be several separate pieces
                out[t].append({'outline': ring, 'color': col, 'depth': i})
            sm = im.resize((N // 2, N // 2))
            sheet.paste(Image.new('RGB', sm.size, col), (k * N // 2, 0), sm)
    json.dump(out, open(os.path.join(HERE, 'scenic.json'), 'w'), indent=1)
    sheet.save(os.path.join(HERE, 'scenic-sheet.png'))
    for t, v in out.items():
        print(t, len(v), 'pieces', sorted({p['color'] for p in v}))


if __name__ == '__main__':
    main()
