"""Tropos "Topo" (a proposal, 2026-10-31): the laminated horn's 22 layers, each layer's outer outline a real contour
line of a real place, so a pair carries a mountain. The air path inside is the approved one, unchanged; only the
outline of each layer changes, and never inside the wall the air path needs.

The place is Mount Tamalpais (East Peak, 784 m), from public elevation data: Mapzen's terrarium terrain tiles on
AWS Open Data (zoom 13; sources include USGS NED/3DEP and SRTM; dem/, see README). The mountain is laid on the horn
with its summit on the horn's axis, north up, and scaled so its 500 m contour is about the mouth's size. The
mountain shrinks toward its summit faster than the horn toward its throat, so the levels are not evenly spaced: each
layer takes the contour whose width clears its own air path plus the wall by `margin`, and the levels are listed.

    .venv-fab/bin/python spinoffs/barkhorn/variants/topo/topo.py      ->  levels.csv, outlines.json, preview.png

`outlines(P)` gives, for each layer from the mouth, the contour as a closed polyline in the horn's frame (mm, x
across, y up), for product.formed_horn's 'topo' option.
"""
import csv, glob, json, math, os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PX_M = 156543.03392 * math.cos(math.radians(37.9235)) / 2 ** 13     # metres a pixel at zoom 13, at the summit's latitude
PLACE = dict(name='Mount Tamalpais, East Peak', lat=37.9235, lon=-122.5965, summit_m=784,
             data='Mapzen terrarium tiles (AWS Open Data, terrain tiles), zoom 13; sources include USGS 3DEP and SRTM')


def dem():
    from PIL import Image
    tiles = {}
    for f in glob.glob(os.path.join(HERE, 'dem', 'tam-13-*.png')):
        _, _, x, y = os.path.basename(f)[:-4].split('-')
        tiles[(int(x), int(y))] = np.asarray(Image.open(f).convert('RGB')).astype(float)
    xs = sorted({k[0] for k in tiles}); ys = sorted({k[1] for k in tiles})
    M = np.vstack([np.hstack([tiles[(x, y)] for x in xs]) for y in ys])
    return M[..., 0] * 256 + M[..., 1] + M[..., 2] / 256 - 32768


def _ring_around(gen, lev, ix, iy):
    """The closed contour at `lev` that encloses the summit pixel (ix, iy), the smallest if several do."""
    from matplotlib.path import Path
    best = None
    for L in gen.lines(lev):
        if len(L) < 12 or not np.allclose(L[0], L[-1]):
            continue
        if Path(L).contains_point((ix, iy)):
            a = (L[:, 0].max() - L[:, 0].min()) * (L[:, 1].max() - L[:, 1].min())
            if best is None or a < best[0]:
                best = (a, L)
    return None if best is None else best[1]


def outlines(P, r_mouth_m=2400.0, r_throat_m=150.0, relief=(8.0, 45.0), smooth_px=1.5, n=360):
    """For each of the laminated horn's layers (mouth first): its outline (mm, the horn's frame: x across, y up, the axis
    at 0, 0), the air path's section plus the wall, pushed out by the land's relief along a circle round the summit.

    Layer i walks a circle round East Peak at radius r_i (from `r_mouth_m` at the mouth to `r_throat_m` at the throat,
    evenly in log radius); its polar angle about the horn's axis is the compass bearing from the summit (north up). The
    elevation along that circle, scaled within the layer to `relief` (mm outside the wall: least to most), pushes the
    outline out along the radius. So ridges and ravines run down the horn's length, and every layer's edge is a real
    transect of the mountain."""
    from scipy.ndimage import gaussian_filter, map_coordinates
    import product
    c = P['horn']['cast']; F = c['formed']; L_ = F['laminated']
    d = c['d']; wl = L_['wall']
    nl = max(1, round(d / L_['layer'])); t = d / nl
    E = gaussian_filter(dem(), smooth_px)
    iy, ix = np.unravel_index(np.argmax(E), E.shape)
    hw, hh, _ = product.flare_section(c, d)
    out = []
    radii = np.exp(np.linspace(math.log(r_mouth_m), math.log(r_throat_m), nl))
    for i, r_m in enumerate(radii):
        zz = d - i * t
        w, h, ne = product.flare_section(c, zz)
        if i == 0:
            w, h = hw, hh
        ne = max(ne, 2.0)
        pts, elev = [], []
        for k in range(n):
            tk = 2 * math.pi * k / n
            x, y = product._se_point(w + wl, h + wl, ne, tk)
            phi = math.atan2(y, x)                              # the bearing: east 0, north 90 (y up)
            px = ix + (r_m / PX_M) * math.cos(phi); py = iy - (r_m / PX_M) * math.sin(phi)
            elev.append(float(map_coordinates(E, [[py], [px]], order=1)[0]))
            pts.append((x, y, phi))
        lo, hi = min(elev), max(elev)
        ring = []
        for (x, y, phi), e in zip(pts, elev):
            dlt = relief[0] + (relief[1] - relief[0]) * (e - lo) / max(hi - lo, 1e-6)
            ring.append((x + dlt * math.cos(phi), y + dlt * math.sin(phi)))
        out.append(dict(layer=i + 1, radius_m=round(float(r_m)), elev_m=[round(lo), round(hi)], points=ring))
    return out, None


def main():
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
    import horn_options
    P = horn_options.P
    rings, scale = outlines(P)
    json.dump(dict(place=PLACE, rings=rings),
              open(os.path.join(HERE, 'outlines.json'), 'w'))
    with open(os.path.join(HERE, 'levels.csv'), 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['layer', 'circle_radius_m', 'elevation_low_m', 'elevation_high_m'])
        for r in rings:
            w.writerow([r['layer'], r['radius_m'], *r['elev_m']])
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 6))
    import product
    c = P['horn']['cast']; wl = c['formed']['laminated']['wall']; d = c['d']; nl = len(rings)
    for r in rings:
        xs, ys = zip(*r['points'])
        ax.plot(xs, ys, lw=0.8, color='#7A1A1C')
    for k, z in ((0, d), (nl // 2, d / 2)):                 # the air path plus the wall, and the band's outer edge
        w, h, n = product.flare_section(c, z)
        for off, ls in ((wl, '-'), (wl + 45.0, ':')):
            q = [product._se_point(w + off, h + off, max(n, 2.0), 2 * math.pi * j / 144) for j in range(145)]
            ax.plot(*zip(*q), ls, lw=0.6, color='#333333')
    ax.set_aspect('equal'); ax.set_title(f'{PLACE["name"]}: the 22 layers, each a walk round the summit')
    fig.savefig(os.path.join(HERE, 'preview.png'), dpi=130, bbox_inches='tight')
    print('radii', [r['radius_m'] for r in rings])


if __name__ == '__main__':
    main()
