#!/usr/bin/env python3
"""EARF habitat finish: one camera over the whole frame (no masks).

Applies, in this order, to the whole picture alike:
  1. lens softness   (a small Gaussian blur, so the model's edges are no sharper than the scanned ground)
  2. bloom           (light from the brightest areas spills a little over what is next to them)
  3. veil            (a lens's veiling glare: 2 % of the frame's average light over everything, capped; one black floor)
  4. vignette        (corners a little darker)
  5. saturation      (a small global trim)
  6. grain           (film-like, strongest in the mid-tones, the same over speaker and scene)

Works in display space on an 8- or 16-bit RGB file. No region of the frame is treated differently.
Usage: finish.py in.png out.jpg [--strength 1.0] [--seed 7] [--no-grain]
Prints the settings it used (to be listed in the report under "finish").
"""
import sys, argparse
import numpy as np
from PIL import Image

def box1d(a, r, axis):
    if r < 1: return a
    n = 2*r+1
    pad = [(0,0)]*a.ndim; pad[axis] = (r+1, r)
    c = np.cumsum(np.pad(a, pad, mode='edge'), axis=axis, dtype=np.float64)
    hi = [slice(None)]*a.ndim; lo = [slice(None)]*a.ndim
    hi[axis] = slice(n, None); lo[axis] = slice(0, -n)
    return ((c[tuple(hi)] - c[tuple(lo)]) / n).astype(np.float32)

def gauss(a, sigma):
    """Gaussian blur by three box blurs (good to a few percent); sub-pixel sigmas by a small 3-tap kernel."""
    if sigma <= 0: return a
    if sigma < 1.2:
        w = np.exp(-0.5/(sigma*sigma)); k = np.array([w, 1.0, w], np.float32); k /= k.sum()
        out = a
        for ax in (0, 1):
            p = [(0,0)]*a.ndim; p[ax] = (1,1)
            b = np.pad(out, p, mode='edge')
            s0 = [slice(None)]*a.ndim; s1 = [slice(None)]*a.ndim; s2 = [slice(None)]*a.ndim
            s0[ax] = slice(0,-2); s1[ax] = slice(1,-1); s2[ax] = slice(2,None)
            out = k[0]*b[tuple(s0)] + k[1]*b[tuple(s1)] + k[2]*b[tuple(s2)]
        return out
    r = max(1, int(round(np.sqrt(sigma*sigma*12/3 + 1)/2 - 0.5)))
    out = a
    for _ in range(3):
        out = box1d(out, r, 0); out = box1d(out, r, 1)
    return out

def finish(img, strength=1.0, seed=7, grain=True, verbose=True):
    a = np.asarray(img.convert('RGB')).astype(np.float32) / 255.0
    H, W = a.shape[:2]
    k = W / 2400.0                      # settings are written for a 2400 px wide final
    s = strength
    lin = np.power(a, 2.2)
    # 1. lens softness
    soft = 0.75 * k * s
    lin = gauss(lin, soft)
    # 2. bloom from the highlights (linear threshold 0.55 = display 0.76)
    lum = lin @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    hl = lin * np.clip((lum - 0.55) / 0.45, 0, 1)[..., None]
    glow = 0.65 * gauss(hl, 18 * k) + 0.35 * gauss(hl, 70 * k)
    bloom_gain = 0.45 * s
    lin = lin + bloom_gain * glow
    # 3. veil: 2 % of the frame's average light over everything
    veil = 0.020 * s
    v = veil * lin.reshape(-1, 3).mean(axis=0)
    v_lum = float(v @ np.array([0.2126, 0.7152, 0.0722], np.float32))
    if v_lum > 0.0012: v = v * (0.0012 / v_lum)     # capped, so a bright foggy frame is not washed out
    lin = lin * (1 - veil) + v
    # 4. vignette: about -0.4 EV in the corners
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W/2) / (W/2))**2 + ((yy - H/2) / (H/2))**2) / np.sqrt(2)
    vig = 0.24 * s
    lin = lin * (1 - vig * np.power(r, 2.2))[..., None]
    out = np.power(np.clip(lin, 0, 1), 1/2.2)
    # 5. saturation trim
    sat = 1 - 0.06 * s
    g = out @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    out = g[..., None] + (out - g[..., None]) * sat
    # 6. grain: mid-tones strongest; three quarters shared by the channels, one quarter per channel
    amp = 0.0
    if grain:
        rng = np.random.default_rng(seed)
        gs = max(0.45, 0.62 * k)          # grain size
        n_l = gauss(rng.standard_normal((H, W)).astype(np.float32), gs)
        n_l /= n_l.std()
        n_c = gauss(rng.standard_normal((H, W, 3)).astype(np.float32), gs)
        n_c /= n_c.std()
        amp = 0.020 * s
        L = np.clip(out @ np.array([0.2126, 0.7152, 0.0722], np.float32), 0, 1)
        w = 0.35 + 0.65 * np.sqrt(np.clip(4 * L * (1 - L), 0, 1))
        out = out + amp * w[..., None] * (0.75 * n_l[..., None] + 0.25 * n_c)
    out = np.clip(out, 0, 1)
    settings = dict(width=W, strength=s, soft_sigma_px=round(float(soft), 2), bloom_gain=bloom_gain,
                    bloom_sigmas_px=(round(18*k, 1), round(70*k, 1)), veil=veil, vignette=vig, saturation=round(sat, 3),
                    grain_amp=amp, seed=seed)
    if verbose: print('finish:', settings)
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8)), settings

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--strength', type=float, default=1.0)
    ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--no-grain', action='store_true')
    o = ap.parse_args()
    im, _ = finish(Image.open(o.src), o.strength, o.seed, not o.no_grain)
    if o.dst.lower().endswith(('.jpg', '.jpeg')): im.save(o.dst, quality=93, subsampling=0)
    else: im.save(o.dst)
