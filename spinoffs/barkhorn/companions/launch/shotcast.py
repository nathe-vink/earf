"""Hiddencast for the studio-engine shot files (studio/engine/render.py), ported from the speaker lane's
campaign/hiddencast.py and shots.card_coverage (r33-speaker-horn ac9e5568), with point lamps added: a 96 x 96 grid of
rays through the frame (lens shift included, padded 3 % past each edge) against each hidden object's whole shape,
occlusion ignored. Hidden: area and panel lamps without `camera` (as their rectangle facing their target), point and spot
lamps without `camera` (as their sphere, radius_m), flags and bounces without `camera`.

    python3 spinoffs/barkhorn/companions/launch/shotcast.py SHOT.json [...]
"""
import json, math, os, sys
import numpy as np


def frame_rays(s, nx=96, ny=96):
    cam = s['camera']; c = np.array(cam['position'], float); f = np.array(cam['target'], float) - c
    f /= np.linalg.norm(f); r = np.cross(f, [0.0, 0.0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    W, H = s['size']; lens = cam['lens_mm']
    hx, hy = (18.0, 18.0 * H / W) if W >= H else (18.0 * W / H, 18.0)
    sx, sy = cam.get('shift_x', 0.0), cam.get('shift_y', 0.0); span = max(hx, hy) * 2
    X, Y = np.meshgrid(np.linspace(-1.03, 1.03, nx), np.linspace(-1.03, 1.03, ny))
    px = X * hx + sx * span; py = Y * hy + sy * span
    d = f[None, None, :] * lens + px[..., None] * r[None, None, :] + py[..., None] * u[None, None, :]
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    return c, d.reshape(-1, 3)


def rect_coverage(s, center, size, normal):
    c, d = frame_rays(s); n = np.array(normal, float); n /= np.linalg.norm(n); w, h = size
    if abs(n[2]) > 0.9:
        a = np.array([1.0, 0.0, 0.0]); b = np.array([0.0, 1.0, 0.0])
    else:
        L = math.hypot(n[0], n[1]) or 1.0
        a = np.array([-n[1] / L, n[0] / L, 0.0]); b = np.cross(n, a); b /= np.linalg.norm(b)
    o = np.array(center, float); den = d @ n
    with np.errstate(divide='ignore', invalid='ignore'):
        t = ((o - c) @ n) / den
    q = c[None, :] + t[:, None] * d - o
    return float(((t > 0) & np.isfinite(t) & (np.abs(q @ a) <= w / 2) & (np.abs(q @ b) <= h / 2)).mean())


def sphere_coverage(s, p, r):
    c, d = frame_rays(s); oc = c - np.array(p, float); b = d @ oc; q = oc @ oc - r * r; disc = b * b - q
    return float(((disc >= 0) & ((-b + np.sqrt(np.maximum(disc, 0))) > 0)).mean())


def lamp_rect(L, centre):
    t = L.get('target', centre)
    if 'orbit' in L:
        o = L['orbit']; az, el = math.radians(o.get('azimuth_deg', 0)), math.radians(o.get('elevation_deg', 30))
        dd = o.get('distance_m', 2.0)
        p = [centre[0] + dd * math.cos(el) * math.sin(az), centre[1] - dd * math.cos(el) * math.cos(az), centre[2] + dd * math.sin(el)]
    elif 'position' in L:
        p = L['position']
    else:
        return None
    n = [t[i] - p[i] for i in range(3)]
    sz = L.get('size_m', 0.5); sz = sz if isinstance(sz, list) else [sz, sz]
    return p, sz, n


def hidden(s, centre=None):
    """[(kind, name, centre, share)] for every hidden object. centre: the orbit centre render.py uses (the product's
    bounds centre; (0, 0, 0.5) without a product)."""
    centre = centre or ([0, 0, 0.16] if 'product' in s else [0, 0, 0.5])
    rows = []
    st = s.get('set', {}) or {}
    for key in ('flags', 'bounces'):
        for c in st.get(key, []) or []:
            if not c.get('camera'):
                rows.append(('hidden ' + key[:-1], c.get('name', ''), c['center_m'],
                             rect_coverage(s, c['center_m'], c['size_m'], c['normal'])))
    for k, L in (s.get('lights') or {}).items():
        if L.get('camera'):
            continue
        if L.get('type') in ('area', 'panel'):
            r = lamp_rect(L, centre)
            if r:
                rows.append((L['type'] + ' lamp', k, [round(x, 2) for x in r[0]], rect_coverage(s, *r)))
        elif L.get('type') in ('point', 'spot'):
            rows.append((L['type'] + ' lamp', k, L['position'], sphere_coverage(s, L['position'], L.get('radius_m', 0.05))))
    return rows


def slide_out(s, name, centre=None, depth=None, ceiling=None, kmax=8.0):
    """Slide area lamp `name` away from its target along the line through it, its size grown by k to hold its angle
    there (an irradiance holds), until it leaves the frame; stays inside the set. Returns k or None."""
    centre = centre or ([0, 0, 0.16] if 'product' in s else [0, 0, 0.5])
    L = s['lights'][name]; t = np.array(L.get('target', centre), float); p0 = np.array(L['position'], float)
    sz = L.get('size_m', 0.5); sz = sz if isinstance(sz, list) else [sz, sz]
    for k10 in range(11, int(kmax * 10) + 1):
        k = k10 / 10; p = t + (p0 - t) * k
        if (depth is not None and p[1] > depth) or (ceiling is not None and p[2] + sz[1] * k / 2 > ceiling):
            return None
        if rect_coverage(s, p, [sz[0] * k, sz[1] * k], t - p) == 0.0:
            L['position'] = [round(float(x), 3) for x in p]; L['size_m'] = [round(sz[0] * k, 3), round(sz[1] * k, 3)]
            return k
    return None


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = json.load(open(f)); rows = hidden(s); bad = [r for r in rows if r[3] > 0]
        print(os.path.basename(f), f'{len(rows)} hidden, {len(bad)} in frame')
        for r in bad:
            print(f'   IN FRAME {r[3] * 100:5.1f} %  {r[0]} {r[1]} at {r[2]}')
