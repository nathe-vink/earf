"""The world's field: which biome a point belongs to, and how high the ground is there (pure numpy, no Blender).

The world is a ring round the camera, which stands at the origin. Eight biomes in turn, clockwise seen from above
(azimuth from +y toward +x), each a 45-degree sector with its Tropos standing at R metres on the sector's centre line.
Neighbours meet along boundaries bent by noise (more near, less far), and blend over a band B degrees each side.
world.py builds the ground, the scatter and the volumes from this; composite.py weighs the eight hours by it, read
at each pixel's first hit (the position pass), so the light changes exactly where the ground changes.
"""
import math
import numpy as np

NAMES = ['Ice', 'Poison', 'Fog', 'Haze', 'Dust', 'Acid', 'Ember', 'Smoke']
N = len(NAMES)
SECTOR = 360.0 / N
R_SPEAKER = 3.6             # m from the camera to each speaker's centre
BAND = 7.0                  # deg: half the width of a blend
CENTRE = 0.0                # deg: azimuth of the first sector's centre line


def centre_az(i):
    return CENTRE + i * SECTOR


# --- noise: smooth value noise (deterministic, the same in every process) ---------------------------------------------
def _hash(ix, iy, seed):
    h = (ix * 374761393 + iy * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def vnoise(x, y, seed=0):
    """Value noise in [-1, 1] with a smooth (quintic) blend, one cell per unit."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ix = np.floor(x).astype(np.int64); iy = np.floor(y).astype(np.int64)
    fx = x - ix; fy = y - iy
    ux = fx * fx * fx * (fx * (fx * 6 - 15) + 10); uy = fy * fy * fy * (fy * (fy * 6 - 15) + 10)
    a = _hash(ix, iy, seed); b = _hash(ix + 1, iy, seed); c = _hash(ix, iy + 1, seed); d = _hash(ix + 1, iy + 1, seed)
    v = a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy
    return v * 2.0 - 1.0


def fbm(x, y, octaves=5, seed=0, lac=2.0, gain=0.5):
    s, amp, f, tot = 0.0, 1.0, 1.0, 0.0
    for o in range(octaves):
        s = s + amp * vnoise(x * f, y * f, seed + 17 * o)
        tot += amp; amp *= gain; f *= lac
    return s / tot


def ridged(x, y, octaves=5, seed=0):
    s, amp, f, tot, w = 0.0, 1.0, 1.0, 0.0, 1.0
    for o in range(octaves):
        n = 1.0 - np.abs(vnoise(x * f, y * f, seed + 31 * o))
        n = n * n * w
        w = np.clip(n * 1.5, 0, 1)
        s = s + amp * n; tot += amp; amp *= 0.5; f *= 2.0
    return s / tot


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# --- the biomes' weights ---------------------------------------------------------------------------------------------
def azimuth(x, y):
    return np.degrees(np.arctan2(x, y)) % 360.0


def warp(x, y):
    """Degrees the boundaries bend: a few metres' wiggle near, broad lobes at range, fading with distance."""
    r = np.hypot(x, y)
    near = 9.0 * fbm(x / 6.0, y / 6.0, 4, seed=11)                    # metre-scale tongues near the speakers
    mid = 6.0 * fbm(x / 60.0, y / 60.0, 3, seed=23)
    fade = 1.0 / (1.0 + (r / 400.0) ** 2)
    calm = smooth(0.0, 1.5, r)                                         # at the centre the pinwheel stays still
    return (near + mid) * fade * calm


def weights(x, y, band=BAND, use_warp=True):
    """(..., 8) weights summing to 1."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    phi = azimuth(x, y) + (warp(x, y) if use_warp else 0.0)
    W = []
    for i in range(N):
        d = np.abs(((phi - centre_az(i)) + 180.0) % 360.0 - 180.0)
        W.append(1.0 - smooth(SECTOR / 2 - band, SECTOR / 2 + band, d))
    W = np.stack(W, -1)
    return W / np.maximum(W.sum(-1, keepdims=True), 1e-9)


def dir_weights(az_deg, band=BAND):
    """Weights for a direction (the sky), no warp."""
    a = np.asarray(az_deg, float)
    W = []
    for i in range(N):
        d = np.abs(((a - centre_az(i)) + 180.0) % 360.0 - 180.0)
        W.append(1.0 - smooth(SECTOR / 2 - band, SECTOR / 2 + band, d))
    W = np.stack(W, -1)
    return W / np.maximum(W.sum(-1, keepdims=True), 1e-9)


# --- the ground's height, biome by biome -----------------------------------------------------------------------------
def _near(x, y, amp=0.06, scale=3.0, seed=1):
    return amp * fbm(x / scale, y / scale, 4, seed)


def h_ice(x, y, r):
    z = 0.12 * fbm(x / 5.0, y / 5.0, 4, 3) + 1.5 * smooth(10, 80, r) * fbm(x / 40, y / 40, 4, 4)
    mtn = smooth(250, 1100, r) * (200 + 1100 * ridged(x / 900.0, y / 900.0, 6, 5))
    return z + mtn


def h_poison(x, y, r):
    z = 0.10 * fbm(x / 4.0, y / 4.0, 4, 6) + 2.5 * smooth(12, 90, r) * fbm(x / 30, y / 30, 4, 7)
    return z + smooth(120, 600, r) * (30 + 90 * fbm(x / 300, y / 300, 4, 8))          # hidden among the trunks


def h_fog(x, y, r):
    """A headland: grass to the edge, a cliff, the fog's sea below; far summits standing out of it."""
    z = 0.10 * fbm(x / 4.0, y / 4.0, 4, 9) + 0.6 * smooth(4, 20, r)
    edge = 15.0 + 4.0 * fbm(x / 20, y / 20, 3, 10)
    drop = smooth(edge, edge + 8.0, r) * 45.0
    peaks = smooth(300, 900, r) * (60 + 260 * ridged(x / 500.0, y / 500.0, 5, 12)) * smooth(0.25, 0.65, 0.5 + 0.5 * fbm(x / 900, y / 900, 3, 13))
    return z - drop + peaks


def h_haze(x, y, r):
    z = 0.08 * fbm(x / 4.0, y / 4.0, 4, 14) + 3.0 * smooth(8, 80, r) * (0.5 + fbm(x / 35, y / 35, 4, 15))
    ranges = 0.0
    for k, (d, hgt) in enumerate(((150, 30), (320, 70), (650, 130), (1300, 240), (2600, 420))):
        ranges = ranges + hgt * smooth(d * 0.7, d, r) * (0.55 + 0.45 * fbm(x / (d * 0.4), y / (d * 0.4), 3, 20 + k))
    return z + ranges * 0.6


def h_dust(x, y, r):
    z = 0.05 * fbm(x / 6.0, y / 6.0, 3, 30) + 0.8 * smooth(10, 120, r) * fbm(x / 60, y / 60, 3, 31)
    # mesas: a plateau mask cut sharp, capped flat, in two tiers
    m = fbm(x / 900.0, y / 900.0, 4, 32)
    tier1 = smooth(0.05, 0.10, m) * 160.0
    tier2 = smooth(0.32, 0.36, m) * 90.0
    talus = smooth(-0.15, 0.05, m) * 25.0
    return z + smooth(500, 1200, r) * (tier1 + tier2 + talus)


def h_acid(x, y, r):
    z = 0.10 * fbm(x / 3.0, y / 3.0, 5, 40) + 1.2 * smooth(6, 60, r) * fbm(x / 25, y / 25, 4, 41)
    cones = 0.0
    for cx, cy, hgt, rad in ((900, 1500, 220, 700), (-300, 2300, 300, 900)):
        pass
    return z + smooth(300, 1500, r) * (40 + 200 * np.clip(fbm(x / 800, y / 800, 4, 42) + 0.2, 0, None))


def h_ember(x, y, r):
    z = 0.12 * fbm(x / 3.0, y / 3.0, 5, 50) + 0.8 * smooth(6, 60, r) * fbm(x / 20, y / 20, 4, 51)
    return z + smooth(400, 1600, r) * (30 + 120 * np.clip(fbm(x / 700, y / 700, 4, 52) + 0.3, 0, None))


def h_smoke(x, y, r):
    z = 0.015 * fbm(x / 6.0, y / 6.0, 3, 60)
    return z + smooth(60, 600, r) * 6.0 * fbm(x / 200, y / 200, 3, 61)


HEIGHTS = [h_ice, h_poison, h_fog, h_haze, h_dust, h_acid, h_ember, h_smoke]


def volcano(x, y):
    """Ember's cone: a volcano at about 2.4 km on the sector's line, its crater glowing."""
    a = math.radians(centre_az(6) + 6.0)
    cx, cy = 2400 * math.sin(a), 2400 * math.cos(a)
    d = np.hypot(x - cx, y - cy)
    cone = 520.0 * np.clip(1.0 - d / 1300.0, 0, None) ** 1.6
    crater = 60.0 * np.exp(-(d / 110.0) ** 2)
    return cone - crater, (cx, cy)


def height(x, y, W=None):
    x = np.asarray(x, float); y = np.asarray(y, float)
    r = np.hypot(x, y)
    W = weights(x, y) if W is None else W
    z = np.zeros_like(x)
    for i, f in enumerate(HEIGHTS):
        wi = W[..., i]
        m = wi > 1e-4
        if np.any(m):
            z[m] += wi[m] * f(x[m], y[m], r[m])
    v, _ = volcano(x, y)
    z += W[..., 6] * v
    # the centre: a low granite dome the photographer stands on, common to all eight
    z = z * smooth(0.8, 2.2, r) + 0.05 * (1 - smooth(0.0, 1.8, r))
    return z


def speaker_spot(i):
    a = math.radians(centre_az(i))
    return R_SPEAKER * math.sin(a), R_SPEAKER * math.cos(a)
