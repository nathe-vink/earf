"""The slide's layout, solved before rendering (the owner, 2026-10-31: "Not lines and dots to things. Everything spaced
far enough out against a neutral enough background that text next to each object is enough").

Projects each product's box through the engine's camera (level, framed by lens shift: render.py) and places its label
zone (380 x 130 px at 1920 x 1080, 40-80 px from its silhouette) on the side the layout names, then checks: every
zone and product 100 px inside the frame, no zone touching another zone or a product, Core >= 70 px, Hemisphere >= 90
px, and the header zone (900 x 160) clear of everything.

    python3 spinoffs/barkhorn/four-pieces/layout.py SHOT.json      # prints the boxes, zones and the checks
"""
import json, math, sys

W, H = 1920, 1080
ZW, ZH, GAP, EDGE = 380, 130, 56, 100
HEADER = (900, 160)


def camera(cam):
    C = cam['position']; T = cam['target']; f = W * cam['lens_mm'] / cam.get('sensor_mm', 36.0)
    dx, dy = T[0] - C[0], T[1] - C[1]
    yaw = math.atan2(dy, dx)
    fwd = (math.cos(yaw), math.sin(yaw)); right = (math.sin(yaw), -math.cos(yaw))
    flat = math.hypot(dx, dy)
    tilt = math.atan2(T[2] - C[2], flat)

    def proj(P):
        v = (P[0] - C[0], P[1] - C[1], P[2] - C[2])
        d = v[0] * fwd[0] + v[1] * fwd[1]
        r = v[0] * right[0] + v[1] * right[1]
        x = W / 2 + f * r / d
        y = H / 2 - f * (v[2] / d - math.tan(tilt))
        return x, y, d
    return proj, f


def box_px(proj, lo, hi):
    pts = [proj((x, y, z)) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return [min(xs), min(ys), max(xs), max(ys)], min(p[2] for p in pts)


def zone(b, side, gap=GAP, dx=0.0):
    cx, cy = (b[0] + b[2]) / 2 + dx, (b[1] + b[3]) / 2
    if side == 'above':
        return [cx - ZW / 2, b[1] - gap - ZH, cx + ZW / 2, b[1] - gap]
    if side == 'below':
        return [cx - ZW / 2, b[3] + gap, cx + ZW / 2, b[3] + gap + ZH]
    if side == 'left':
        return [b[0] - gap - ZW, cy - ZH / 2, b[0] - gap, cy + ZH / 2]
    if side == 'right':
        return [b[2] + gap, cy - ZH / 2, b[2] + gap + ZW, cy + ZH / 2]
    # 'above-left' / 'above-right': above, its near edge over the product's edge
    if side == 'above-right':
        return [b[0] + dx, b[1] - gap - ZH, b[0] + dx + ZW, b[1] - gap]
    if side == 'above-left':
        return [b[2] - ZW + dx, b[1] - gap - ZH, b[2] + dx, b[1] - gap]
    raise ValueError(side)


def overlap(a, b, pad=0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def boxes(shot):
    """Each product's world box (metres), from the shot's own placements."""
    out = {}
    for i, t in enumerate(shot['tropos']):
        x, y = t['position']
        out[f'tropos{i}'] = ([x - 0.315, y - 0.214, 0.0], [x + 0.315, y + 0.214, 1.295])
    m = shot['products'][0]['instances'][0]['position']
    out['mantle'] = ([m[0] - 0.235, m[1] - 0.19, m[2]], [m[0] + 0.235, m[1] + 0.19, m[2] + 0.194])
    for p in shot['set']['props']:
        if p.get('module') == 'earf_moon':
            s = p['spots'][0]['position']
            if p['fn'] == 'orb':
                out['core'] = ([s[0] - 0.08, s[1] - 0.08, s[2]], [s[0] + 0.08, s[1] + 0.08, s[2] + 0.18])
            else:
                out['hemisphere'] = ([s[0] - 0.1, s[1] - 0.1, s[2]], [s[0] + 0.1, s[1] + 0.1, s[2] + 0.13])
    return out


def solve(shot, verbose=True):
    proj, f = camera(shot['camera'])
    B = {k: box_px(proj, *v) for k, v in boxes(shot).items()}
    lab = shot.get('labels', {})
    Z = {}
    for k, spec in lab.items():
        if k == 'header':
            continue
        Z[k] = zone(B[spec['of']][0], spec['side'], spec.get('gap', GAP), spec.get('dx', 0.0))
    if 'header' in lab:
        x0, y0 = lab['header']
        Z['header'] = [x0, y0, x0 + HEADER[0], y0 + HEADER[1]]
    problems = []
    for k, (b, d) in B.items():
        if b[0] < EDGE or b[1] < EDGE * 0.5 or b[2] > W - EDGE or b[3] > H - 10:
            problems.append(f'{k} near the frame edge {[round(v) for v in b]}')
    for k, z in Z.items():
        if z[0] < EDGE or z[1] < EDGE * 0.6 or z[2] > W - EDGE or z[3] > H - EDGE * 0.6:
            problems.append(f'zone {k} near the frame edge {[round(v) for v in z]}')
        for k2, z2 in Z.items():
            if k2 > k and overlap(z, z2, 8):
                problems.append(f'zones {k} and {k2} touch')
        for kb, (b, d) in B.items():
            if overlap(z, b, 8):
                problems.append(f'zone {k} touches {kb}')
    core_w = B['core'][0][2] - B['core'][0][0]
    hemi_w = B['hemisphere'][0][2] - B['hemisphere'][0][0]
    if core_w < 70:
        problems.append(f'Core {core_w:.0f} px < 70')
    if hemi_w < 90:
        problems.append(f'Hemisphere {hemi_w:.0f} px < 90')
    if verbose:
        for k, (b, d) in B.items():
            print(f'{k:11s} box {[round(v) for v in b]}  {b[2]-b[0]:.0f} x {b[3]-b[1]:.0f} px  depth {d:.2f} m')
        for k, z in Z.items():
            print(f'zone {k:10s} {[round(v) for v in z]}')
        print('OK' if not problems else '\n'.join('PROBLEM ' + p for p in problems))
    return B, Z, problems


if __name__ == '__main__':
    solve(json.load(open(sys.argv[1])))
