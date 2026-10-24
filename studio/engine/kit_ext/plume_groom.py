"""Groom a solve from plume_sim.py for one shot (Smoke E12r p20; p19's critics: "a smoke column far too big for such a
small fire", "the flames hugging the top unit should come down a little").

    python3 studio/engine/kit_ext/plume_groom.py IN.npz OUT.npz [--squeeze S0 S1 Z0 Z1] [--fade Z0 Z1 F]
                                                 [--flame-cap SHOT PX0 PX1 LO]

--squeeze   the soot (and the heat) drawn in toward the column's own centre line, slice by slice: S0 of its width at Z0
            metres up, S1 at Z1, smoothly between (1 leaves it be). The billows keep their shapes, narrower.
--fade      the soot thinned with height: whole up to Z0, F of itself by Z1 (a small fire's column thins as it rises).
--flame-cap the flames the shot's lens sees over the top of the solve's first solid (the speaker), whole up to PX0
            pixels over it in a 960 pixel wide frame, LO of themselves by PX1: so they stop short of whatever stands
            on the solid. SHOT is the shot's JSON (its camera, and the plume piece's turn and floor).

The grids are stored as they are written (each value's square root in a byte, the renderer squaring it back), and
the rest of the file is copied, so the result renders as any solve does (kit_ext/plume.py).
"""
import argparse
import json
import math

import numpy as np
from scipy import ndimage


def ramp(z, z0, z1, a, b):
    t = np.clip((z - z0) / max(z1 - z0, 1e-6), 0.0, 1.0)
    return a + (b - a) * t * t * (3 - 2 * t)


def decode(u8):
    return (u8.astype(np.float32) / 255.0) ** 2


def encode(v):
    return np.round(np.sqrt(np.clip(v, 0.0, 1.0)) * 255.0).astype(np.uint8)


def centre_line(rho):
    """The soot's centre in each slice, smoothed up the column (cells)."""
    NX, NY, NZ = rho.shape
    I, J = np.meshgrid(np.arange(NX), np.arange(NY), indexing='ij')
    w = rho.sum(axis=(0, 1))
    cx = np.array([(rho[:, :, k] * I).sum() / w[k] if w[k] > 0 else 0.0 for k in range(NZ)])
    cy = np.array([(rho[:, :, k] * J).sum() / w[k] if w[k] > 0 else 0.0 for k in range(NZ)])
    ok = w > 1e-3 * w.max()
    ks = np.arange(NZ)
    cx, cy = np.interp(ks, ks[ok], cx[ok]), np.interp(ks, ks[ok], cy[ok])
    return ndimage.gaussian_filter1d(cx, 6.0), ndimage.gaussian_filter1d(cy, 6.0)


def squeeze(g, cx, cy, s):
    NX, NY, NZ = g.shape
    I, J = np.meshgrid(np.arange(NX, dtype=np.float32), np.arange(NY, dtype=np.float32), indexing='ij')
    out = g.copy()
    for k in range(NZ):
        if s[k] < 0.999:
            out[:, :, k] = ndimage.map_coordinates(g[:, :, k], [cx[k] + (I - cx[k]) / s[k], cy[k] + (J - cy[k]) / s[k]],
                                                   order=1, mode='constant', cval=0.0)
    return out


def camera(shot):
    """The shot's camera as a projector into a 960 pixel wide frame (render.py's level camera: lens over a 36 mm
    sensor, shift_y a share of the width)."""
    c = shot['camera']
    W = 960.0
    H = W * 2.0 / 3.0
    cp, ct = np.array(c['position'], float), np.array(c['target'], float)
    f = ct - cp; f[2] = 0.0; f /= np.linalg.norm(f)
    r = np.cross(f, [0.0, 0.0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    fpx = c.get('lens_mm', 35.0) / 36.0 * W

    def project(P):
        d = P - cp; zc = d @ f
        return W / 2 + fpx * (d @ r) / zc, H / 2 - fpx * (d @ u) / zc + c.get('shift_y', 0.0) * W
    return project


def flame_cap(fl, z, shot, px0, px1, lo):
    pl = next(p for p in shot['set']['props'] if p.get('module') == 'plume')
    rot, sink = pl.get('rotate_z', 0.0), pl.get('position', [0.0, 0.0, 0.0])[2]
    project = camera(shot)
    dx = float(z['dx']); cx, cy, z0, hx, hy, z1, yaw = z['solids'][0]
    a = math.radians(rot); c, s = math.cos(a), math.sin(a)
    b = math.radians(rot + yaw); cb, sb = math.cos(b), math.sin(b)
    corners = np.array([[x, y, zz] for x in (-hx, hx) for y in (-hy, hy) for zz in (z0, z1)])
    _, bv = project(np.stack([corners[:, 0] * cb - corners[:, 1] * sb, corners[:, 0] * sb + corners[:, 1] * cb,
                              corners[:, 2] + sink], 1))
    top = bv.min()
    idx = np.argwhere(fl > 1e-5)
    sx = (idx[:, 0] + 0.5) * dx - cx; sy = (idx[:, 1] + 0.5) * dx - cy; sz = (idx[:, 2] + 0.5) * dx
    _, v = project(np.stack([sx * c - sy * s, sx * s + sy * c, sz + sink], 1))
    out = fl.copy()
    out[idx[:, 0], idx[:, 1], idx[:, 2]] *= ramp(top - v, px0, px1, 1.0, lo).astype(np.float32)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--squeeze', type=float, nargs=4)
    ap.add_argument('--fade', type=float, nargs=3)
    ap.add_argument('--flame-cap', nargs=4)
    a = ap.parse_args()
    z = np.load(a.src)
    data = {k: z[k] for k in z.files}
    dx = float(z['dx']); NZ = int(z['size'][2])
    zc = (np.arange(NZ) + 0.5) * dx
    rho, heat, fl = decode(z['rho']), decode(z['heat']), decode(z['flame'])
    w0, f0 = rho.sum(), fl.sum()
    if a.squeeze:
        s0, s1, z0, z1 = a.squeeze
        cx, cy = centre_line(rho)
        s = ramp(zc, z0, z1, s0, s1)
        rho, heat = squeeze(rho, cx, cy, s), squeeze(heat, cx, cy, s)
    if a.fade:
        z0, z1, f = a.fade
        rho *= ramp(zc, z0, z1, 1.0, f)[None, None, :]
    if a.flame_cap:
        shot = json.load(open(a.flame_cap[0]))
        fl = flame_cap(fl, z, shot, *(float(v) for v in a.flame_cap[1:]))
    data['rho'], data['heat'], data['flame'] = encode(rho), encode(heat), encode(fl)
    np.savez_compressed(a.dst, **data)
    print(f'wrote {a.dst}: soot {rho.sum() / w0:.3f} of before, flame {fl.sum() / f0:.3f}')


if __name__ == '__main__':
    main()
