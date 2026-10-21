"""A fire's smoke plume, simulated (round 31b, Smoke E9: the bridge, after the owner's "That smoke looks bad").

The smoke in E6 and E7 was noise carved into boxes, and every critic read it as "a soft, uniform volumetric blob".
Real smoke billows because it is a flow: hot gas rises, drags the air around it into eddies, and the eddies roll the
soot into lobes on every scale. Blender's own smoke solver does not run in this container's bpy (its Mantaflow scripts
fail headless), so this is a small solver of its own, written for one job: a buoyant plume from a burning car, bent by
a light wind.

  - a staggered (MAC) grid, periodic across the wind's plane, a solid ground and a closed lid far above;
  - semi-Lagrangian advection of the velocity (second-order trace) and MacCormack advection of the scalars, which
    keeps the billows' edges sharp; with `--velocity mc` (Smoke E10) the velocity by MacCormack too, clamped to the
    first lookup's corners, which keeps the small eddies the semi-Lagrangian step smears away;
  - buoyancy from heat, vorticity confinement to put back the eddies the grid smooths away, a wind that shears with
    height;
  - an exact pressure projection (FFT across, cosine transform up the height);
  - three scalars: soot (`rho`), heat (`heat`, slow to cool, what lifts the plume) and flame (`flame`, quick to cool,
    what glows);
  - sponges at the lid and the domain's ends, so nothing wraps round;
  - for E10, whose critics saw E9's billows all one size ("cotton-ball", "metaball lobes"): `--disturb STRENGTH SCALE`
    pairs, random kicks inside the smoke at each scale (m/s^2, m), drifting up with it, that break the lobes into many
    sizes; `--tau-soot`, the soot thinning with age (s), so the old edges go wispy.

It writes the last frame as an .npz of 8-bit grids (square-root coded), which `plume.py` turns into a volume in Cycles.
Run once; the result is committed beside the shot, so a render never needs this file or numba:

    pip install --target <dir> numba==0.60.0 llvmlite==0.43.0 --no-deps
    PYTHONPATH=<dir> python3.11 plume_sim.py OUT.npz [--dx 0.2] [--seconds 20] [--seed 1]
        [--velocity sl|mc] [--disturb 6 0.6 3 1.6] [--disturb-rho 0.5] [--tau-soot 25]
"""
import argparse
import math
import time

import numpy as np
import scipy.fft as sfft
from numba import njit, prange


@njit(inline='always', fastmath=True)
def _corners(f, x, y, z, ox, oy, oz):
    """Trilinear lookup of a staggered field at grid-unit position (x, y, z): periodic in x and y, clamped in z.
    Returns the value and the min and max of the eight corners (for MacCormack's clamp)."""
    NX, NY, NZ = f.shape
    gx = x - ox; gy = y - oy; gz = z - oz
    if gz < 0.0:
        gz = 0.0
    top = NZ - 1.0
    if gz > top:
        gz = top
    i0 = int(math.floor(gx)); j0 = int(math.floor(gy)); k0 = int(math.floor(gz))
    tx = gx - i0; ty = gy - j0; tz = gz - k0
    if k0 >= NZ - 1:
        k0 = NZ - 2; tz = 1.0
    ia = i0 % NX; ib = (i0 + 1) % NX
    ja = j0 % NY; jb = (j0 + 1) % NY
    kb = k0 + 1
    c000 = f[ia, ja, k0]; c100 = f[ib, ja, k0]; c010 = f[ia, jb, k0]; c110 = f[ib, jb, k0]
    c001 = f[ia, ja, kb]; c101 = f[ib, ja, kb]; c011 = f[ia, jb, kb]; c111 = f[ib, jb, kb]
    a = c000 + (c100 - c000) * tx; b = c010 + (c110 - c010) * tx
    c = c001 + (c101 - c001) * tx; d = c011 + (c111 - c011) * tx
    e = a + (b - a) * ty; g = c + (d - c) * ty
    val = e + (g - e) * tz
    mn = min(min(min(c000, c100), min(c010, c110)), min(min(c001, c101), min(c011, c111)))
    mx = max(max(max(c000, c100), max(c010, c110)), max(max(c001, c101), max(c011, c111)))
    return val, mn, mx


@njit(inline='always', fastmath=True)
def _s(f, x, y, z, ox, oy, oz):
    return _corners(f, x, y, z, ox, oy, oz)[0]


@njit(inline='always', fastmath=True)
def _vel(u, v, w, x, y, z):
    return _s(u, x, y, z, 0.0, 0.5, 0.5), _s(v, x, y, z, 0.5, 0.0, 0.5), _s(w, x, y, z, 0.5, 0.5, 0.0)


@njit(inline='always', fastmath=True)
def _trace(u, v, w, x, y, z, h):
    """Where the fluid at (x, y, z) was h = dt/dx ago (h < 0: where it will be), by the midpoint rule."""
    a, b, c = _vel(u, v, w, x, y, z)
    a, b, c = _vel(u, v, w, x - 0.5 * h * a, y - 0.5 * h * b, z - 0.5 * h * c)
    return x - h * a, y - h * b, z - h * c


@njit(parallel=True, fastmath=True)
def advect_velocity(u, v, w, un, vn, wn, h):
    NX, NY, NZ = u.shape
    for i in prange(NX):
        for j in range(NY):
            for k in range(NZ):
                x, y, z = _trace(u, v, w, i * 1.0, j + 0.5, k + 0.5, h)
                un[i, j, k] = _s(u, x, y, z, 0.0, 0.5, 0.5)
                x, y, z = _trace(u, v, w, i + 0.5, j * 1.0, k + 0.5, h)
                vn[i, j, k] = _s(v, x, y, z, 0.5, 0.0, 0.5)
            for k in range(1, NZ):
                x, y, z = _trace(u, v, w, i + 0.5, j + 0.5, k * 1.0, h)
                wn[i, j, k] = _s(w, x, y, z, 0.5, 0.5, 0.0)
            wn[i, j, 0] = 0.0
            wn[i, j, NZ] = 0.0


@njit(parallel=True, fastmath=True)
def advect_velocity_1(u, v, w, un, vn, wn, lo_u, hi_u, lo_v, hi_v, lo_w, hi_w, h):
    """MacCormack's first half for the velocity (E10: the semi-Lagrangian step alone smears away every eddy smaller
    than a few cells, which is what left E9's billows all one size): the semi-Lagrangian step, and each lookup's
    bounds."""
    NX, NY, NZ = u.shape
    for i in prange(NX):
        for j in range(NY):
            for k in range(NZ):
                x, y, z = _trace(u, v, w, i * 1.0, j + 0.5, k + 0.5, h)
                un[i, j, k], lo_u[i, j, k], hi_u[i, j, k] = _corners(u, x, y, z, 0.0, 0.5, 0.5)
                x, y, z = _trace(u, v, w, i + 0.5, j * 1.0, k + 0.5, h)
                vn[i, j, k], lo_v[i, j, k], hi_v[i, j, k] = _corners(v, x, y, z, 0.5, 0.0, 0.5)
            for k in range(1, NZ):
                x, y, z = _trace(u, v, w, i + 0.5, j + 0.5, k * 1.0, h)
                wn[i, j, k], lo_w[i, j, k], hi_w[i, j, k] = _corners(w, x, y, z, 0.5, 0.5, 0.0)
            wn[i, j, 0] = 0.0
            wn[i, j, NZ] = 0.0


@njit(inline='always', fastmath=True)
def _clamp(a, lo, hi):
    return lo if a < lo else (hi if a > hi else a)


@njit(parallel=True, fastmath=True)
def advect_velocity_2(u, v, w, un, vn, wn, lo_u, hi_u, lo_v, hi_v, lo_w, hi_w, uo, vo, wo, h):
    """MacCormack's second half for the velocity: trace forward, correct by half the round-trip error, clamp."""
    NX, NY, NZ = u.shape
    for i in prange(NX):
        for j in range(NY):
            for k in range(NZ):
                x, y, z = _trace(u, v, w, i * 1.0, j + 0.5, k + 0.5, -h)
                a = un[i, j, k] + 0.5 * (u[i, j, k] - _s(un, x, y, z, 0.0, 0.5, 0.5))
                uo[i, j, k] = _clamp(a, lo_u[i, j, k], hi_u[i, j, k])
                x, y, z = _trace(u, v, w, i + 0.5, j * 1.0, k + 0.5, -h)
                a = vn[i, j, k] + 0.5 * (v[i, j, k] - _s(vn, x, y, z, 0.5, 0.0, 0.5))
                vo[i, j, k] = _clamp(a, lo_v[i, j, k], hi_v[i, j, k])
            for k in range(1, NZ):
                x, y, z = _trace(u, v, w, i + 0.5, j + 0.5, k * 1.0, -h)
                a = wn[i, j, k] + 0.5 * (w[i, j, k] - _s(wn, x, y, z, 0.5, 0.5, 0.0))
                wo[i, j, k] = _clamp(a, lo_w[i, j, k], hi_w[i, j, k])
            wo[i, j, 0] = 0.0
            wo[i, j, NZ] = 0.0


@njit(parallel=True, fastmath=True)
def advect_scalars_1(u, v, w, s, s1, mn, mx, h):
    """MacCormack's first half for the stacked scalars s[n]: the semi-Lagrangian step, and each lookup's bounds."""
    NS, NX, NY, NZ = s.shape
    for i in prange(NX):
        for j in range(NY):
            for k in range(NZ):
                x, y, z = _trace(u, v, w, i + 0.5, j + 0.5, k + 0.5, h)
                for n in range(NS):
                    a, lo, hi = _corners(s[n], x, y, z, 0.5, 0.5, 0.5)
                    s1[n, i, j, k] = a; mn[n, i, j, k] = lo; mx[n, i, j, k] = hi


@njit(parallel=True, fastmath=True)
def advect_scalars_2(u, v, w, s, s1, mn, mx, out, h):
    """MacCormack's second half: trace forward from the first step's result, correct by half the round-trip error,
    clamp to the first lookup's bounds."""
    NS, NX, NY, NZ = s.shape
    for i in prange(NX):
        for j in range(NY):
            for k in range(NZ):
                x, y, z = _trace(u, v, w, i + 0.5, j + 0.5, k + 0.5, -h)
                for n in range(NS):
                    back = _s(s1[n], x, y, z, 0.5, 0.5, 0.5)
                    a = s1[n, i, j, k] + 0.5 * (s[n, i, j, k] - back)
                    lo = mn[n, i, j, k]; hi = mx[n, i, j, k]
                    if a < lo:
                        a = lo
                    if a > hi:
                        a = hi
                    out[n, i, j, k] = a


@njit(parallel=True, fastmath=True)
def centre_velocity(u, v, w, uc, vc, wc):
    NX, NY, NZ = u.shape
    for i in prange(NX):
        ip = (i + 1) % NX
        for j in range(NY):
            jp = (j + 1) % NY
            for k in range(NZ):
                uc[i, j, k] = 0.5 * (u[i, j, k] + u[ip, j, k])
                vc[i, j, k] = 0.5 * (v[i, j, k] + v[i, jp, k])
                wc[i, j, k] = 0.5 * (w[i, j, k] + w[i, j, k + 1])


@njit(parallel=True, fastmath=True)
def vorticity(uc, vc, wc, ox, oy, oz, om):
    """The curl of the centred velocity (per grid unit) and its magnitude."""
    NX, NY, NZ = uc.shape
    for i in prange(NX):
        ip = (i + 1) % NX; im = (i - 1) % NX
        for j in range(NY):
            jp = (j + 1) % NY; jm = (j - 1) % NY
            for k in range(NZ):
                kp = min(k + 1, NZ - 1); km = max(k - 1, 0)
                dz = 1.0 / max(kp - km, 1)
                dwdy = 0.5 * (wc[i, jp, k] - wc[i, jm, k]); dvdz = (vc[i, j, kp] - vc[i, j, km]) * dz
                dudz = (uc[i, j, kp] - uc[i, j, km]) * dz; dwdx = 0.5 * (wc[ip, j, k] - wc[im, j, k])
                dvdx = 0.5 * (vc[ip, j, k] - vc[im, j, k]); dudy = 0.5 * (uc[i, jp, k] - uc[i, jm, k])
                a = dwdy - dvdz; b = dudz - dwdx; c = dvdx - dudy
                ox[i, j, k] = a; oy[i, j, k] = b; oz[i, j, k] = c
                om[i, j, k] = math.sqrt(a * a + b * b + c * c)


@njit(parallel=True, fastmath=True)
def confinement(ox, oy, oz, om, fx, fy, fz, eps):
    """Vorticity confinement: a force eps (N x omega) that spins up the eddies the grid has smoothed (per grid unit)."""
    NX, NY, NZ = om.shape
    for i in prange(NX):
        ip = (i + 1) % NX; im = (i - 1) % NX
        for j in range(NY):
            jp = (j + 1) % NY; jm = (j - 1) % NY
            for k in range(NZ):
                kp = min(k + 1, NZ - 1); km = max(k - 1, 0)
                dz = 1.0 / max(kp - km, 1)
                gx = 0.5 * (om[ip, j, k] - om[im, j, k]); gy = 0.5 * (om[i, jp, k] - om[i, jm, k])
                gz = (om[i, j, kp] - om[i, j, km]) * dz
                n = math.sqrt(gx * gx + gy * gy + gz * gz) + 1e-6
                gx /= n; gy /= n; gz /= n
                a = ox[i, j, k]; b = oy[i, j, k]; c = oz[i, j, k]
                fx[i, j, k] = eps * (gy * c - gz * b)
                fy[i, j, k] = eps * (gz * a - gx * c)
                fz[i, j, k] = eps * (gx * b - gy * a)


@njit(parallel=True, fastmath=True)
def apply_forces(u, v, w, fx, fy, fz, heat, rho, dt, beta, alpha):
    """Add the confinement (averaged from the cells to the faces) and the buoyancy of heat less the soot's weight."""
    NX, NY, NZ = u.shape
    for i in prange(NX):
        im = (i - 1) % NX
        for j in range(NY):
            jm = (j - 1) % NY
            for k in range(NZ):
                u[i, j, k] += dt * 0.5 * (fx[im, j, k] + fx[i, j, k])
                v[i, j, k] += dt * 0.5 * (fy[i, jm, k] + fy[i, j, k])
            for k in range(1, NZ):
                b = beta * 0.5 * (heat[i, j, k - 1] + heat[i, j, k]) - alpha * 0.5 * (rho[i, j, k - 1] + rho[i, j, k])
                w[i, j, k] += dt * (0.5 * (fz[i, j, k - 1] + fz[i, j, k]) + b)


@njit(parallel=True, fastmath=True)
def divergence(u, v, w, d, inv_dx):
    NX, NY, NZ = u.shape
    for i in prange(NX):
        ip = (i + 1) % NX
        for j in range(NY):
            jp = (j + 1) % NY
            for k in range(NZ):
                d[i, j, k] = (u[ip, j, k] - u[i, j, k] + v[i, jp, k] - v[i, j, k] + w[i, j, k + 1] - w[i, j, k]) * inv_dx


@njit(parallel=True, fastmath=True)
def subtract_gradient(u, v, w, q, inv_dx):
    NX, NY, NZ = u.shape
    for i in prange(NX):
        im = (i - 1) % NX
        for j in range(NY):
            jm = (j - 1) % NY
            for k in range(NZ):
                u[i, j, k] -= (q[i, j, k] - q[im, j, k]) * inv_dx
                v[i, j, k] -= (q[i, j, k] - q[i, jm, k]) * inv_dx
            for k in range(1, NZ):
                w[i, j, k] -= (q[i, j, k] - q[i, j, k - 1]) * inv_dx


@njit(inline='always', fastmath=True)
def _hash(i, j, k, s):
    h = (i * 374761393 + j * 668265263 + k * 2147483647 + s * 1274126177) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


@njit(inline='always', fastmath=True)
def _vnoise(x, y, z, s):
    """Value noise in 0..1, smooth between integer lattice points."""
    i = int(math.floor(x)); j = int(math.floor(y)); k = int(math.floor(z))
    fx = x - i; fy = y - j; fz = z - k
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy); fz = fz * fz * (3 - 2 * fz)
    a = _hash(i, j, k, s) + (_hash(i + 1, j, k, s) - _hash(i, j, k, s)) * fx
    b = _hash(i, j + 1, k, s) + (_hash(i + 1, j + 1, k, s) - _hash(i, j + 1, k, s)) * fx
    c = _hash(i, j, k + 1, s) + (_hash(i + 1, j, k + 1, s) - _hash(i, j, k + 1, s)) * fx
    d = _hash(i, j + 1, k + 1, s) + (_hash(i + 1, j + 1, k + 1, s) - _hash(i, j + 1, k + 1, s)) * fx
    e = a + (b - a) * fy; g = c + (d - c) * fy
    return e + (g - e) * fz


@njit(parallel=True, fastmath=True)
def emit(s, w, src, t, dt, dx, seed, rate, heat_src, flame_src, w_src, scale):
    """The fire: inside the source's ellipsoid (centre cx, cy, cz and half-sizes in metres, src[0:6]), soot, heat and
    flame are fed and the gas pushed upward, all modulated by noise that churns as it rises."""
    NS, NX, NY, NZ = s.shape
    cx, cy, cz, ax, ay, az = src[0], src[1], src[2], src[3], src[4], src[5]
    i0 = max(int((cx - ax) / dx) - 1, 0); i1 = min(int((cx + ax) / dx) + 2, NX)
    j0 = max(int((cy - ay) / dx) - 1, 0); j1 = min(int((cy + ay) / dx) + 2, NY)
    k0 = max(int((cz - az) / dx) - 1, 0); k1 = min(int((cz + az) / dx) + 2, NZ)
    for i in prange(i0, i1):
        for j in range(j0, j1):
            for k in range(k0, k1):
                x = (i + 0.5) * dx; y = (j + 0.5) * dx; z = (k + 0.5) * dx
                r2 = ((x - cx) / ax) ** 2 + ((y - cy) / ay) ** 2 + ((z - cz) / az) ** 2
                if r2 >= 1.0:
                    continue
                fall = 1.0 - r2
                n = _vnoise(x / scale, y / scale, (z - 3.0 * t) / scale, seed)
                n2 = _vnoise(x / (0.4 * scale), y / (0.4 * scale), (z - 4.0 * t) / (0.4 * scale), seed + 7)
                m = max(0.0, 1.6 * n + 0.6 * n2 - 0.7) * fall
                s[0, i, j, k] += dt * rate * m
                s[1, i, j, k] = max(s[1, i, j, k], heat_src * m)
                s[2, i, j, k] = max(s[2, i, j, k], flame_src * m)
                ww = w_src * m
                if w[i, j, k] < ww:
                    w[i, j, k] = ww
                if w[i, j, k + 1] < ww:
                    w[i, j, k + 1] = ww


@njit(parallel=True, fastmath=True)
def disturb(u, v, w, rho, t, dt, dx, seed, amp, scale, rho_ref):
    """Disturbance (E10): a smooth random kick to the velocity wherever there is soot, its strength following the
    soot's density up to rho_ref. Confinement alone spins every eddy up at the grid's one scale, which is why E9's
    billows came out like cotton balls all one size; a kick at a few scales breaks them into lobes of many sizes. The
    projection that follows keeps only its swirling part. The field drifts upward slowly, so it is not frozen."""
    NX, NY, NZ = u.shape
    drift = 0.6 * t / scale
    for i in prange(NX):
        x = (i + 0.5) * dx / scale
        for j in range(NY):
            y = (j + 0.5) * dx / scale
            for k in range(1, NZ):
                r = rho[i, j, k]
                if r < 0.02 * rho_ref:
                    continue
                m = dt * amp * min(1.0, r / rho_ref)
                z = (k + 0.5) * dx / scale - drift
                u[i, j, k] += m * (2.0 * _vnoise(x, y, z, seed) - 1.0)
                v[i, j, k] += m * (2.0 * _vnoise(x + 31.7, y, z, seed + 1) - 1.0)
                w[i, j, k] += m * (2.0 * _vnoise(x, y + 47.3, z, seed + 2) - 1.0)


@njit(parallel=True, fastmath=True)
def sponge(s, u, v, w, uw, dt, nx_band, nz_band, cool_heat, cool_flame, fade_soot):
    """Cool the heat and the flame, thin the soot by fade_soot (E10: old smoke spreads thin at its edges and in the
    wake, where E9's stayed as dense as at the fire), and at the domain's ends and lid fade everything back to the
    still wind."""
    NS, NX, NY, NZ = s.shape
    for i in prange(NX):
        ex = min(i, NX - 1 - i) / max(nx_band, 1)
        for j in range(NY):
            ey = min(j, NY - 1 - j) / max(nx_band // 2, 1)
            for k in range(NZ):
                ez = (NZ - 1 - k) / max(nz_band, 1)
                e = min(1.0, min(min(ex, ey), ez))
                damp = 1.0 - (1.0 - e) * min(1.0, 4.0 * dt)
                s[0, i, j, k] *= damp * fade_soot
                s[1, i, j, k] *= damp * cool_heat
                s[2, i, j, k] *= damp * cool_flame
                u[i, j, k] = uw[k] + (u[i, j, k] - uw[k]) * damp
                v[i, j, k] *= damp
                if k + 1 < NZ:
                    w[i, j, k + 1] *= damp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--dx', type=float, default=0.2)
    ap.add_argument('--size', type=float, nargs=3, default=[48.0, 24.0, 64.0], help='domain x (downwind), y, z in metres')
    ap.add_argument('--seconds', type=float, default=20.0)
    ap.add_argument('--dt', type=float, default=0.05)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--source', type=float, nargs=6, default=[9.0, 12.0, 1.0, 1.9, 0.8, 0.6],
                    help='fire ellipsoid: centre x y z and half-sizes, metres')
    ap.add_argument('--wind', type=float, default=2.5, help='wind at 10 m, m/s, blowing toward +x')
    ap.add_argument('--beta', type=float, default=7.0, help='buoyancy per unit heat, m/s^2')
    ap.add_argument('--alpha', type=float, default=0.05, help="the soot's weight per unit density, m/s^2")
    ap.add_argument('--eps', type=float, default=4.0, help='vorticity confinement, per second (times the curl per cell)')
    ap.add_argument('--rate', type=float, default=6.0, help='soot fed per second inside the fire')
    ap.add_argument('--w-src', type=float, default=5.0, help='upward push in the fire, m/s')
    ap.add_argument('--tau-heat', type=float, default=5.0, help='seconds for heat to fall by e')
    ap.add_argument('--tau-flame', type=float, default=0.35, help='seconds for the flame to fall by e')
    ap.add_argument('--noise', type=float, default=0.6, help="the fire's churn, metres")
    # E10's three (left off, a run reproduces E9's plume_a):
    ap.add_argument('--velocity', choices=('sl', 'mc'), default='sl',
                    help="the velocity's advection: semi-Lagrangian, or MacCormack, which keeps the small eddies")
    ap.add_argument('--disturb', type=float, nargs='*', default=[],
                    help='pairs of strength (m/s^2) and scale (m): random kicks inside the smoke at those scales')
    ap.add_argument('--disturb-rho', type=float, default=0.5, help='the soot density at which the kicks reach full strength')
    ap.add_argument('--tau-soot', type=float, default=0.0, help='seconds for the soot to thin by e (0: never)')
    a = ap.parse_args()
    assert len(a.disturb) % 2 == 0, '--disturb takes strength, scale pairs'

    dx = a.dx
    NX, NY, NZ = (int(round(L / dx)) for L in a.size)
    NY += NY % 2
    print(f'grid {NX} x {NY} x {NZ} = {NX * NY * NZ / 1e6:.1f} M cells, dx {dx} m, {a.seconds} s at dt {a.dt}')
    f32 = np.float32
    zc = (np.arange(NZ) + 0.5) * dx
    uw = (a.wind * np.clip(zc / 10.0, 0.05, None) ** 0.22).astype(f32)    # the wind's power-law profile over the deck
    u = np.empty((NX, NY, NZ), f32); u[:] = uw[None, None, :]
    v = np.zeros((NX, NY, NZ), f32); w = np.zeros((NX, NY, NZ + 1), f32)
    s = np.zeros((3, NX, NY, NZ), f32)
    un, vn, wn = np.empty_like(u), np.empty_like(v), np.empty_like(w)
    s1, mn, mx, sn = (np.empty_like(s) for _ in range(4))
    uc, vc, wc = (np.empty((NX, NY, NZ), f32) for _ in range(3))
    ox, oy, oz, om, fx, fy, fz, d = (np.empty((NX, NY, NZ), f32) for _ in range(8))
    if a.velocity == 'mc':      # MacCormack's bounds and its second-half output
        lo_u, hi_u, lo_v, hi_v, uo, vo = (np.empty((NX, NY, NZ), f32) for _ in range(6))
        lo_w, hi_w, wo = (np.empty((NX, NY, NZ + 1), f32) for _ in range(3))
    # the Laplacian's eigenvalues for FFT across (periodic) and the type-II cosine transform up the height (Neumann)
    li = (2 * np.cos(2 * np.pi * np.arange(NX) / NX) - 2)[:, None, None]
    lj = (2 * np.cos(2 * np.pi * np.arange(NY // 2 + 1) / NY) - 2)[None, :, None]
    lk = (2 * np.cos(np.pi * np.arange(NZ) / NZ) - 2)[None, None, :]
    lam = ((li + lj + lk) / dx ** 2).astype(np.float64)
    lam[0, 0, 0] = 1.0
    src = np.array(a.source, np.float64)
    steps = int(round(a.seconds / a.dt))
    h = a.dt / dx
    t0 = time.time()
    cool_h, cool_f = math.exp(-a.dt / a.tau_heat), math.exp(-a.dt / a.tau_flame)
    fade = math.exp(-a.dt / a.tau_soot) if a.tau_soot > 0 else 1.0
    for n in range(steps):
        t = n * a.dt
        emit(s, w, src, t, a.dt, dx, a.seed, a.rate, 1.0, 1.0, a.w_src, a.noise)
        centre_velocity(u, v, w, uc, vc, wc)
        vorticity(uc, vc, wc, ox, oy, oz, om)
        confinement(ox, oy, oz, om, fx, fy, fz, a.eps)
        apply_forces(u, v, w, fx, fy, fz, s[1], s[0], a.dt, a.beta, a.alpha)
        for m in range(0, len(a.disturb), 2):
            disturb(u, v, w, s[0], t, a.dt, dx, a.seed + 101 + 13 * m, a.disturb[m], a.disturb[m + 1], a.disturb_rho)
        divergence(u, v, w, d, 1.0 / dx)
        q = sfft.dct(d, type=2, axis=2, norm='ortho', workers=4)
        q = sfft.rfftn(q, axes=(0, 1), workers=4)
        q /= lam
        q[0, 0, 0] = 0.0
        q = sfft.irfftn(q, s=(NX, NY), axes=(0, 1), workers=4)
        q = sfft.idct(q, type=2, axis=2, norm='ortho', workers=4).astype(f32)
        subtract_gradient(u, v, w, q, 1.0 / dx)
        if a.velocity == 'mc':
            advect_velocity_1(u, v, w, un, vn, wn, lo_u, hi_u, lo_v, hi_v, lo_w, hi_w, h)
            advect_velocity_2(u, v, w, un, vn, wn, lo_u, hi_u, lo_v, hi_v, lo_w, hi_w, uo, vo, wo, h)
            un, uo = uo, un; vn, vo = vo, vn; wn, wo = wo, wn
        else:
            advect_velocity(u, v, w, un, vn, wn, h)
        advect_scalars_1(un, vn, wn, s, s1, mn, mx, h)
        advect_scalars_2(un, vn, wn, s, s1, mn, mx, sn, h)
        u, un = un, u; v, vn = vn, v; w, wn = wn, w; s, sn = sn, s
        sponge(s, u, v, w, uw, a.dt, int(0.08 * NX), int(0.1 * NZ), cool_h, cool_f, fade)
        if n % 20 == 0 or n == steps - 1:
            el = time.time() - t0
            top = np.nonzero(s[0].max(axis=(0, 1)) > 0.05)[0]
            print(f'step {n + 1}/{steps} t={t + a.dt:.2f}s  {el:.0f}s elapsed ({el / (n + 1):.2f}s/step)  '
                  f'soot max {s[0].max():.2f}  top {top.max() * dx if len(top) else 0:.1f} m  |w| max {np.abs(w).max():.1f}',
                  flush=True)
    # 8-bit, square-root coded, per grid with its scale
    out = {}
    for n, name in enumerate(('rho', 'heat', 'flame')):
        g = np.clip(s[n], 0, None)
        sc = float(np.percentile(g[g > 1e-4], 99.9)) if (g > 1e-4).any() else 1.0
        out[name] = np.round(np.sqrt(np.clip(g / sc, 0, 1)) * 255).astype(np.uint8)
        out[name + '_scale'] = np.float32(sc)
    np.savez_compressed(a.out, dx=np.float32(dx), size=np.array([NX, NY, NZ]), source=src.astype(np.float32),
                        wind=np.float32(a.wind), seconds=np.float32(a.seconds), seed=np.int32(a.seed), **out)
    print('wrote', a.out, f'in {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
