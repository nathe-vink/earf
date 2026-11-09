"""The night pictures' regrade from the scene-linear render (the coordinator, 2026-11-09 19:50, gate 6, fix 1: a longer,
softer highlight shoulder, so the Hemisphere's dome rolls off instead of plateauing at 251, and its true reflection in
the horn falls from white to pale blue; the faint halation a real lens gives; never a dimmer lamp, never a clamp).

    python3.11 spinoffs/barkhorn/night-pictures/regrade.py NAME.exr NAME.png [--ev 4.3 --wb 3000 --max-ev 6.5
        --halation 0.02 --shot NAME.shot.json --engine ENGINE_ROOT]

The render's own pixels, untouched in linear light; only the view changes:
- exposure `ev` and a white balance to `wb` K (the scene's: the 2700 K lamps read a warm white), as Blender's view did;
- an AgX-style transform (the published minimal AgX: its inset matrix, a log2 encoding, its sigmoid, its outset), with
  the encoding's top raised from AgX's 4.03 stops over mid-grey to `max_ev`, so the brightest things get more room
  (`--max-ev 4.026` reproduces the minimal AgX; `calibrate` compares it with Blender's own frame);
- halation: a faint wide glow from the brightest highlights only, added in linear light (`halation` of their energy);
- then the engine's own finish (finish.post: the shot's white point, contrast, sharpening and grain), unchanged, so the
  grade is the only difference. Writes NAME.raw.png (the graded frame before the finish) and NAME.png.

    python3.11 spinoffs/barkhorn/night-pictures/regrade.py calibrate NAME.exr NAME.raw.png --ev 4.3 --wb 3000
        compares this transform at AgX's own range with Blender's raw frame, by luminance percentiles and hue
"""
import json
import math
import os
import sys

import numpy as np

INSET = np.array([[0.842479062253094, 0.0784335999999992, 0.0792237451477643],
                  [0.0423282422610123, 0.878468636469772, 0.0791661274605434],
                  [0.0423756549057051, 0.0784336, 0.879142973793104]])
OUTSET = np.array([[1.19687900512017, -0.0980208811401368, -0.0990297440797205],
                   [-0.0528968517574562, 1.15190312990417, -0.0989611768448433],
                   [-0.0529716355144438, -0.0980434501171241, 1.15107367264116]])
MIN_EV = -12.47393


def blackbody(T):
    """Linear Rec.709 of a blackbody at T K, normalised to its luminance (as lamp_pictures' blackbody, CIE 1931 fits)."""
    def g(x, mu, s1, s2):
        return math.exp(-0.5 * ((x - mu) / (s1 if x < mu else s2)) ** 2)
    X = Y = Z = 0.0
    for l in range(380, 781, 5):
        p = 1.0 / ((l * 1e-9) ** 5 * (math.exp(1.4388e-2 / (l * 1e-9 * T)) - 1))
        X += p * (1.056 * g(l, 599.8, 37.9, 31.0) + 0.362 * g(l, 442.0, 16.0, 26.7) - 0.065 * g(l, 501.1, 20.4, 26.2))
        Y += p * (0.821 * g(l, 568.8, 46.9, 40.5) + 0.286 * g(l, 530.9, 16.3, 31.1))
        Z += p * (1.217 * g(l, 437.0, 11.8, 36.0) + 0.681 * g(l, 459.0, 26.0, 13.8))
    X, Z = X / Y, Z / Y
    r = np.array([3.2406 * X - 1.5372 - 0.4986 * Z, -0.9689 * X + 1.8758 + 0.0415 * Z, 0.0557 * X - 0.2040 + 1.0570 * Z])
    return r / (r @ np.array([0.2126, 0.7152, 0.0722]))


def agx(lin, max_ev):
    """Minimal AgX on linear Rec.709 (H x W x 3), the encoding's top at `max_ev` stops over 0.18; returns display sRGB 0-1."""
    v = lin @ INSET.T
    v = np.log2(np.clip(v, 1e-10, None))
    v = (np.clip(v, MIN_EV, max_ev) - MIN_EV) / (max_ev - MIN_EV)
    x2 = v * v; x4 = x2 * x2
    v = 15.5 * x4 * x2 - 40.14 * x4 * v + 31.96 * x4 - 6.868 * x2 * v + 0.4298 * x2 + 0.1191 * v - 0.00232
    v = v @ OUTSET.T
    v = np.clip(v, 0, None) ** 2.2                      # AgX's display EOTF: back to linear for display
    return np.where(v <= 0.0031308, 12.92 * v, 1.055 * np.clip(v, 0, None) ** (1 / 2.4) - 0.055).clip(0, 1)


def read_exr(path):
    import bpy
    img = bpy.data.images.load(path)
    w, h = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[::-1, :, :3]
    return px.astype(np.float64)


def grade(lin, ev, wb, max_ev, halation):
    gain = 1.0 / blackbody(wb)                          # the lamp's white to neutral, at equal luminance
    lin = lin * gain[None, None, :] * (2.0 ** ev)
    if halation > 0:
        from scipy.ndimage import gaussian_filter
        y = lin @ np.array([0.2126, 0.7152, 0.0722])
        hi = lin * np.clip((y - 4.0) / 12.0, 0, 1)[..., None]   # only what is well over white (the dome, its glints)
        k = lin.shape[1] / 1920.0
        glow = sum(wt * np.stack([gaussian_filter(hi[..., c], s * k) for c in range(3)], -1)
                   for wt, s in ((0.6, 6.0), (0.4, 24.0)))
        lin = lin + halation * glow
    return agx(lin, max_ev)


def blender_view(exr, ev, wb, out, view='AgX', look='AgX - Base Contrast'):
    """Blender's own view transform on the saved linear render (as the engine's frame was made: reproduced to 1 level),
    at exposure `ev`; returns display sRGB 0-1."""
    import bpy
    from PIL import Image
    sc = bpy.context.scene
    img = bpy.data.images.get(os.path.basename(exr)) or bpy.data.images.load(exr)
    vs = sc.view_settings; vs.view_transform = view; vs.look = look; vs.exposure = ev
    vs.use_white_balance = True; vs.white_balance_temperature = wb; vs.white_balance_tint = 0.0
    sc.display_settings.display_device = 'sRGB'
    im = sc.render.image_settings; im.file_format = 'PNG'; im.color_depth = '8'
    img.save_render(out, scene=sc)
    return np.asarray(Image.open(out).convert('RGB')).astype(np.float64) / 255.0


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def regrade_blender(exr, out, ev, wb, shoulder_ev, shoulder_from, shade, shade_ev, halation):
    """The regrade in Blender's own AgX (the numpy AgX shifted Ice toward violet, 224 deg against 207, and was dropped):
    - a softer shoulder: above `shoulder_from` of display luminance the frame blends smoothly toward the same render
      `shoulder_ev` stops darker (so the top 20 % of the range is compressed, monotonically, and nothing new clips);
    - the shade: inside the box, what is still near white takes the render at `shade_ev` stops, through a feathered mask;
    - halation: the dome's own light, blurred wide, added faintly in linear light."""
    from scipy.ndimage import gaussian_filter, binary_dilation
    tmp = os.path.splitext(out)[0]
    hi = blender_view(exr, ev, wb, tmp + '.v0.png')
    lo = blender_view(exr, ev + shoulder_ev, wb, tmp + '.v1.png')
    Wt = np.array([0.2126, 0.7152, 0.0722])
    y = hi @ Wt
    w = smooth(y, shoulder_from, 1.0)[..., None]
    g = hi * (1 - w) + lo * w
    H, Wd = g.shape[:2]
    if shade:
        x0, y0, x1, y1 = shade
        sh = blender_view(exr, ev + shade_ev, wb, tmp + '.v2.png')
        m = np.zeros((H, Wd), bool); m[int(y0 * H):int(y1 * H), int(x0 * Wd):int(x1 * Wd)] = True
        m &= y > 0.80
        m = binary_dilation(m, iterations=max(1, int(2 * Wd / 1920)))
        ws = gaussian_filter(m.astype(np.float64), 1.5 * Wd / 1920)[..., None]
        g = g * (1 - ws) + sh * ws
        if halation > 0:
            def s2l(c):
                return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
            src = s2l(sh) * m[..., None]
            k = Wd / 1920
            glow = sum(wt * np.stack([gaussian_filter(src[..., c], s * k) for c in range(3)], -1)
                       for wt, s in ((0.6, 8.0), (0.4, 30.0)))
            lin = s2l(g) + halation * glow
            g = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * np.clip(lin, 0, None) ** (1 / 2.4) - 0.055)
    for f in ('.v0.png', '.v1.png', '.v2.png'):
        if os.path.exists(tmp + f):
            os.remove(tmp + f)
    return np.clip(g, 0, 1)


def opt(name, default, cast=float):
    return cast(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def main():
    from PIL import Image
    if sys.argv[1] == 'calibrate':
        exr, raw = sys.argv[2], sys.argv[3]
        lin = read_exr(exr)
        ours = grade(lin, opt('--ev', 4.3), opt('--wb', 3000.0), 4.026069, 0.0) * 255
        theirs = np.asarray(Image.open(raw).convert('RGB')).astype(np.float64)
        if theirs.shape != ours.shape:
            print('sizes differ', theirs.shape, ours.shape); return
        W = np.array([0.2126, 0.7152, 0.0722])
        for q in (10, 50, 90, 99, 99.9):
            print(f'luma p{q}: ours {np.percentile(ours @ W, q):6.1f}  Blender {np.percentile(theirs @ W, q):6.1f}')
        print('mean RGB ours', ours.reshape(-1, 3).mean(0).round(1), 'Blender', theirs.reshape(-1, 3).mean(0).round(1))
        return
    exr, out = sys.argv[1], sys.argv[2]
    ev, wb, max_ev, hal = opt('--ev', 4.3), opt('--wb', 3000.0), opt('--max-ev', 6.5), opt('--halation', 0.02)
    if '--blender' in sys.argv:
        shade = None
        if '--shade' in sys.argv:
            i = sys.argv.index('--shade'); shade = tuple(float(v) for v in sys.argv[i + 1:i + 5])
        g = regrade_blender(os.path.abspath(exr), os.path.abspath(out), ev, wb, opt('--shoulder-ev', -1.5),
                            opt('--shoulder-from', 0.80), shade, opt('--shade-ev', -4.0), hal)
        finish_and_save(g, out)
        return
    lin = read_exr(exr)
    # the match to Blender's own AgX (Base Contrast) at the same exposure and white balance: three channel gains fitted
    # on proxy 6's frame (median |difference| 3 levels of 255), so the regrade differs from the gated look only in the
    # highlights it is for
    lin = lin * np.array([float(v) for v in opt('--match', '0.7305,0.802,0.6743', str).split(',')])[None, None, :]
    g = grade(lin, ev, wb, max_ev, hal)
    if '--shade' in sys.argv:
        # the two-exposure blend on the lamp's shade only (the coordinator, 19:50: if the shoulder cannot hold the dome):
        # inside the box (fractions x0 y0 x1 y1), what the long exposure renders near white takes the same render at
        # `--shade-ev` stops less, through a feathered mask; nothing outside the box changes
        from scipy.ndimage import gaussian_filter, binary_dilation
        i = sys.argv.index('--shade'); x0, y0, x1, y1 = (float(v) for v in sys.argv[i + 1:i + 5])
        H, Wd = g.shape[:2]
        lo = grade(lin, ev + opt('--shade-ev', -4.0), wb, max_ev, 0.0)
        y = g @ np.array([0.2126, 0.7152, 0.0722])
        m = np.zeros((H, Wd), bool); m[int(y0 * H):int(y1 * H), int(x0 * Wd):int(x1 * Wd)] = True
        m &= y > opt('--shade-thresh', 0.80)
        m = binary_dilation(m, iterations=max(1, int(2 * Wd / 1920)))
        w = gaussian_filter(m.astype(np.float64), 1.5 * Wd / 1920)[..., None]
        g = g * (1 - w) + lo * w
    finish_and_save(g, out)


def finish_and_save(g, out):
    from PIL import Image
    raw = os.path.splitext(out)[0] + '.raw.png'
    Image.fromarray((g * 255 + 0.5).clip(0, 255).astype(np.uint8)).save(raw)
    shot = opt('--shot', None, str); eng = opt('--engine', None, str)
    if shot and eng:
        sys.path.insert(0, os.path.join(eng, 'studio', 'engine'))
        import finish as Fn
        fin = json.load(open(shot)).get('finish')
        mj = os.path.splitext(out)[0] + '.mask.json'
        Fn.post(raw, out, fin, None, None, None, os.path.splitext(out)[0] + '.mask.png',
                json.load(open(mj)) if os.path.exists(mj) else None)
    else:
        Image.open(raw).save(out)
    print('regrade:', out, ' '.join(sys.argv[3:]))


if __name__ == '__main__':
    main()
