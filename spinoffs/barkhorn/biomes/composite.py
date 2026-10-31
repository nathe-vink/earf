"""Lay the eight hours together, then cut the pictures from the one world (r48-biomes).

    python3.11 spinoffs/barkhorn/biomes/composite.py DIR [--pano W] [--planet S] [--look 'AgX - Medium High Contrast']

DIR is world.py's output (position.exr, slice-*.exr, meta.json). Writes into DIR:
- world.exr: the equirectangular composite, scene-linear, each pixel its biome's hour (weights from field.py at the
  pixel's first hit, or by its direction for the sky), each slice at its own exposure (meta's ev);
- pano.png: a cylindrical panorama (as a rotating panoramic camera makes it) of the band round the horizon;
- planet.png: the little planet, a stereographic projection from the nadir;
- equirect.png: the whole sphere, toned.
The tone is Blender's AgX (with a look), the same view the element pictures use.
"""
import argparse, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                                        # noqa: E402
import field as F                                         # noqa: E402


def load_exr(bpy, path):
    im = bpy.data.images.load(path)
    W, H = im.size
    a = np.empty(W * H * 4, np.float32); im.pixels.foreach_get(a)
    bpy.data.images.remove(im)
    return a.reshape(H, W, 4)[::-1]                       # row 0 at the top


def save(bpy, arr, path, look, exposure=0.0, linear_exr=False):
    """Save a scene-linear (H, W, 3|4) array: as EXR, or through AgX to PNG."""
    H, W = arr.shape[:2]
    if arr.shape[2] == 3:
        arr = np.concatenate([arr, np.ones((H, W, 1), np.float32)], -1)
    im = bpy.data.images.new('out', W, H, alpha=False, float_buffer=True)
    im.pixels.foreach_set(np.ascontiguousarray(arr[::-1]).ravel().astype(np.float32))
    sc = bpy.context.scene
    if linear_exr:
        sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '16'
        sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    else:
        sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '8'
        sc.render.image_settings.color_mode = 'RGB'
        sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = look
    sc.view_settings.exposure = exposure
    im.save_render(path, scene=sc)
    bpy.data.images.remove(im)


def bilinear(img, yy, xx, wrap_x=True):
    H, W = img.shape[:2]
    x0 = np.floor(xx).astype(int); y0 = np.floor(yy).astype(int)
    fx = (xx - x0)[..., None]; fy = (yy - y0)[..., None]
    def px(y, x):
        x = x % W if wrap_x else np.clip(x, 0, W - 1)
        return img[np.clip(y, 0, H - 1), x]
    return (px(y0, x0) * (1 - fx) * (1 - fy) + px(y0, x0 + 1) * fx * (1 - fy)
            + px(y0 + 1, x0) * (1 - fx) * fy + px(y0 + 1, x0 + 1) * fx * fy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--look', default='AgX - Medium High Contrast')
    ap.add_argument('--exposure', type=float, default=0.0)
    ap.add_argument('--pano', type=int, default=0, help='panorama width (default: the equirect width)')
    ap.add_argument('--pano-lat', type=float, nargs=2, default=(-34.0, 26.0))
    ap.add_argument('--pano-start', type=float, default=None, help='azimuth at the panorama left edge')
    ap.add_argument('--pano-span', type=float, default=360.0)
    ap.add_argument('--planet', type=int, default=0)
    ap.add_argument('--planet-zoom', type=float, default=1.0)
    ap.add_argument('--planet-turn', type=float, default=0.0)
    ap.add_argument('--ev', type=float, nargs=8, help='override each slice exposure')
    ap.add_argument('--feather', type=float, default=18.0)
    ap.add_argument('--sky-band', type=float, default=28.0)
    ap.add_argument('--meter', action='store_true', help="meter each slice: its own ground's median to the hour's key")
    a = ap.parse_args()
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    meta = json.load(open(os.path.join(a.dir, 'meta.json')))
    W, H = meta['width'], meta['height']
    lat0, lat1 = meta['lat']
    pos = load_exr(bpy, os.path.join(a.dir, 'position.exr'))
    geo = pos[..., 3] > 0.5
    lon = -180.0 + 360.0 * (np.arange(W) + 0.5) / W                       # each column's longitude (deg)
    lat = lat1 - (lat1 - lat0) * (np.arange(H) + 0.5) / H
    # which world azimuth each column looks at (camera at yaw 0): fitted from the ground's positions
    az_hit = np.degrees(np.arctan2(pos[..., 0], pos[..., 1])) % 360.0
    rows = np.where(geo.mean(1) > 0.9)[0]
    best = None
    for s in (1.0, -1.0):
        off = (az_hit[rows] - s * lon[None, :]) % 360.0
        off = off[geo[rows]]
        m = np.angle(np.mean(np.exp(1j * np.radians(off))), deg=True) % 360.0
        err = np.abs(((off - m) + 180) % 360 - 180).mean()
        if best is None or err < best[2]:
            best = (s, m, err)
    s, off, err = best
    col_az = (s * lon + off) % 360.0
    print(f'column azimuth = {s:+.0f} lon + {off:.2f} (err {err:.3f} deg)')
    # the weights: the field at the first hit; the sky by its direction
    Wt = np.zeros((H, W, F.N), np.float32)
    # the light changes over a wider band than the ground does (a time slice's feathered joins): the ground's
    # boundaries, bent as field.py bends them, blended over a.feather degrees each side; the sky over a.sky_band
    Wt[geo] = F.weights(pos[..., 0][geo], pos[..., 1][geo], band=a.feather)
    sky = ~geo
    Wt[sky] = F.dir_weights(np.broadcast_to(col_az[None, :], (H, W))[sky], band=a.sky_band)
    acc = np.zeros((H, W, 3), np.float32); wsum = np.zeros((H, W), np.float32)
    evs = list(a.ev or [h['ev'] for h in meta['hours']])
    LUMW = np.array([0.2126, 0.7152, 0.0722], np.float32)
    band = (lat < -2.0) & (lat > -35.0)
    metered = {}
    for k, sl in meta['slices'].items():
        i = int(k)
        img = load_exr(bpy, os.path.join(a.dir, sl['file']))
        # the slice was rendered with its centre column on the sector's centre: roll it home
        target_col = ((F.centre_az(i) - off) * s + 180.0) % 360.0 / 360.0 * W - 0.5
        shift = int(round(target_col - (W / 2 - 0.5)))
        img = np.roll(img, shift, axis=1)
        cov = img[..., 3] > 0.99
        if a.meter:
            own = (Wt[..., i] > 0.95) & cov & geo & band[:, None]
            med = float(np.median(img[..., :3][own] @ LUMW)) if own.any() else 0.18
            key = meta['hours'][i].get('key', 0.18)
            evs[i] = math.log2(key / max(med, 1e-6)) + meta['hours'][i].get('ev_trim', 0.0)
            metered[F.NAMES[i]] = {'median': round(med, 4), 'key': key, 'ev': round(evs[i], 2)}
        w = Wt[..., i] * cov
        acc += img[..., :3] * (2.0 ** evs[i]) * w[..., None]
        wsum += w
    if metered:
        print('metered', json.dumps(metered))
        json.dump(metered, open(os.path.join(a.dir, 'metered.json'), 'w'), indent=1)
    miss = wsum < 0.999
    if miss.any():
        print(f'pixels short of full weight: {miss.mean() * 100:.2f} % (min {wsum.min():.3f})')
    out = acc / np.maximum(wsum, 1e-6)[..., None]
    out = np.nan_to_num(out, nan=0.0, posinf=0.0)
    save(bpy, out, os.path.join(a.dir, 'world.exr'), a.look, linear_exr=True)
    save(bpy, out, os.path.join(a.dir, 'equirect.png'), a.look, a.exposure)

    # the panorama: cylindrical, a band round the horizon, starting where Smoke gives way to Ice (by default)
    pw = a.pano or W
    start = a.pano_start if a.pano_start is not None else F.centre_az(0) - F.SECTOR / 2 - 4.0
    span = a.pano_span
    t0, t1 = math.tan(math.radians(a.pano_lat[0])), math.tan(math.radians(a.pano_lat[1]))
    hfov = math.radians(span)
    ph = int(round(pw * (t1 - t0) / hfov))
    az = start + span * (np.arange(pw) + 0.5) / pw
    ty = t1 - (t1 - t0) * (np.arange(ph) + 0.5) / ph
    la = np.degrees(np.arctan(ty))
    lo = ((az - off) * s + 180.0) % 360.0 - 180.0
    xx = (lo + 180.0) / 360.0 * W - 0.5
    yy = (lat1 - la) / (lat1 - lat0) * H - 0.5
    XX, YY = np.meshgrid(xx, yy)
    pano = bilinear(out, YY, XX)
    save(bpy, pano, os.path.join(a.dir, 'pano.png'), a.look, a.exposure)
    print('pano', pw, ph)

    # the little planet: stereographic from the nadir, the horizon at radius 0.5 x zoom of the half-width
    if a.planet:
        S = a.planet
        u = (np.arange(S) + 0.5) / S * 2 - 1
        U, V = np.meshgrid(u, -u)
        rho = np.hypot(U, V)
        k = 0.5 * a.planet_zoom                                  # where the horizon lands
        alpha = 2 * np.arctan(rho / k)                           # angle from the nadir
        la = np.degrees(alpha) - 90.0
        azp = (np.degrees(np.arctan2(U, V)) + a.planet_turn) % 360.0     # up the page = azimuth turn
        lo = ((azp - off) * s + 180.0) % 360.0 - 180.0
        xx = (lo + 180.0) / 360.0 * W - 0.5
        yy = (lat1 - la) / (lat1 - lat0) * H - 0.5
        planet = bilinear(out, yy, xx)
        save(bpy, planet, os.path.join(a.dir, 'planet.png'), a.look, a.exposure)
        print('planet', S)


if __name__ == '__main__':
    main()
