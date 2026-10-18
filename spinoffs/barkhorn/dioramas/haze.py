"""Haze: dusk, in layered paper and tulle (round 31; BRIEF.md is the direction, haze.md the notes).

A paper theatre. Flat cut-paper hills stand in receding flats, graded from deep violet in front to lilac, rose and
peach toward a big tissue-paper sun that sits low on the last flat, lit from behind. Three bands of tulle drift across
the sun on threads, as in the icon (a sun behind three bars of haze), and a satin river winds out of the hills past the
speaker's feet. The backcloth is strips of paper graded from violet overhead to peach at the horizon. The one light is
the sun's: low, behind, warm, so the violet acrylic glows through and casts violet onto the paper floor; the dusk sky
fills from above in lilac. The joke: the sun hangs on two threads, being let down for the evening.
"""
import math, random

from common import finish, kit, portrait_of, shot as frame, tilt_shift

SUN = (1.25, 6.2, 1.0, 1.15)
MOON = [-2.15, 6.7, 2.05]                    # the sun: x, y, z of its centre, its radius (m)
FLOOR = '#7C6699'
SPEAKER = ['[!p]*', 'po*']                        # the speaker's parts: everything but the set's pieces (prop<i>-kit)


def _lerp(a, b, t):
    a, b = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02X}' for x, y in zip(a, b))


def grade(stops, t):
    """A colour `t` (0 to 1) along a ramp of hexes."""
    t = min(max(t, 0.0), 1.0) * (len(stops) - 1)
    i = min(int(t), len(stops) - 2)
    return _lerp(stops[i], stops[i + 1], t - i)


def flat(x0, x1, y, h, amp, seed, color, waves=2.2, material='card', depth=0.014, step=0.05, skew=0.0, trees=(), ends=(0.0, 0.0), **k):
    """A cut-paper hill: a flat standing on the floor at depth `y`, its top a soft rolling line about `h` high, with
    `trees` [(x, trunk, rx, rz), ...] cut in the same sheet: a trunk `trunk` tall under an oval crown rx by rz; `ends`
    the lengths over which it runs down to the floor at its left and right ends."""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.283) for _ in range(3)]

    def z_at(x):
        u = (x - x0) / (x1 - x0)
        z = h + amp * (0.62 * math.sin(2 * math.pi * waves * u + ph[0]) + 0.28 * math.sin(2 * math.pi * waves * 2.1 * u + ph[1])
                       + 0.10 * math.sin(2 * math.pi * waves * 4.7 * u + ph[2])) + skew * (u - 0.5)
        for e, d in ((ends[0], x - x0), (ends[1], x1 - x)):     # a hill that runs down to the floor at its end
            if e > 0 and d < e:
                t = d / e
                z *= 0.15 + 0.85 * t * t * (3 - 2 * t)
        return max(z, 0.04)

    n = max(8, int((x1 - x0) / step))
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    trees = sorted(trees)
    top = []
    for x in xs:
        if any(abs(x - t[0]) < t[2] * 0.25 + 0.02 for t in trees):
            continue                                      # the trees' own outline replaces the hill there
        while trees and trees[0][0] < x:
            xt, trunk, rx, rz = trees.pop(0)
            w = max(0.012, rx * 0.12)
            zb = z_at(xt) - 0.02
            zc = zb + trunk + rz * 0.85                   # the crown's centre: it overlaps the trunk's top
            d = math.asin(min(1.0, w / rx))               # where the crown meets the trunk's sides
            top += [[xt - w, zb], [xt - w, zc - rz * math.cos(d)]]
            m = 48
            for i in range(1, m):                         # round the crown over the top, from its lower left
                a = (1.5 * math.pi - d) - (2 * math.pi - 2 * d) * i / m
                top.append([xt + rx * math.cos(a), zc + rz * math.sin(a)])
            top += [[xt + w, zc - rz * math.cos(d)], [xt + w, zb]]
        top.append([x, z_at(x)])
    outline = [[0.0, -0.02]] + [[round(x - x0, 4), round(z, 4)] for x, z in top] + [[round(x1 - x0, 4), -0.02]]
    return kit('extrude', material, color, outline=outline, depth=depth, ease=0.005, position=[x0, y, 0.0], **k)


def disc(x, y, z, r, material, color, depth=0.01, seg=96, **k):
    outline = [[round(r * math.cos(2 * math.pi * i / seg), 4), round(r * math.sin(2 * math.pi * i / seg), 4)] for i in range(seg)]
    return kit('extrude', material, color, outline=outline, depth=depth, ease=0.002, position=[x, y, z], **k)


def crescent(R, k=0.8, d=0.42, n=48):
    """A crescent: a disc of radius R less a disc k R across set d R to its right, the horns to the right."""
    r, c = k * R, d * R
    x = (R * R - r * r + c * c) / (2 * c)                 # where the two circles cross
    t0, t1 = math.atan2(math.sqrt(R * R - x * x), x), math.atan2(math.sqrt(R * R - x * x), x - c)
    outer = [(R * math.cos(t), R * math.sin(t)) for t in [t0 + (2 * math.pi - 2 * t0) * i / n for i in range(n + 1)]]
    inner = [(c + r * math.cos(t), r * math.sin(t)) for t in [2 * math.pi - t1 - (2 * math.pi - 2 * t1) * i / n for i in range(1, n)]]
    return [[round(u, 4), round(v, 4)] for u, v in outer + inner]


def backcloth(y=7.2, x0=-11.0, x1=11.0, z1=5.5, hb=0.3, base=0.7, top=2.9):
    """Strips of paper pasted up the back wall, peach at `base` (the horizon) to violet by `top`, each overlapping the
    next."""
    out = []
    stops = ['#F6C9A8', '#F0B5AE', '#D8A0C2', '#B48CC6', '#8D70B2', '#6A5498']
    bands = int(math.ceil(z1 / hb))
    for i in range(bands):
        z = i * hb
        c = grade(stops, (z + hb / 2 - base) / (top - base))
        out.append(kit('box', 'paper', c, size=[x1 - x0, 0.01, hb + 0.03], position=[(x0 + x1) / 2, y + 0.012 * (i % 2), z - 0.015]))
    return out


def tulle_band(xc, y, z, w, h, seed, color='#9C72BC', alpha=0.62, top=4.8):
    """A band of tulle gathered on a thread, hung across the sun."""
    out = [kit('drape', 'tulle', color, size=[w, h], folds=int(w * 7), amplitude=0.018, noise=0.25, thickness=0.0,
               res=160, seed=seed, alpha=alpha, position=[xc, y, z + h / 2])]
    for dx in (-w * 0.42, w * 0.42):
        a = [xc + dx, y, z + h / 2]
        out.append(kit('thread', 'paper', '#EADFE6', a=a, b=[a[0], y, top], radius=0.0011))
    return out


def river():
    pts = [[2.6, 2.0], [1.6, 1.4], [1.05, 0.7], [1.25, -0.1], [1.0, -0.8], [0.95, -1.45]]
    # a tube's width lies along the vertical, so a ribbon lying flat is a thin one stretched sideways (flat > 1)
    return [kit('tube', 'satin', '#E7C3CF', points=[[x, y, 0.006] for x, y in pts],
                radius=[0.0018, 0.0026, 0.0036, 0.0046, 0.0058, 0.007], flat=40.0, sides=24, res=12)]


def props():
    sx, sy, sz, sr = SUN
    P = []
    P.append(kit('box', 'paper', FLOOR, size=[16.0, 14.0, 0.02], position=[0.0, 1.0, -0.02]))
    P += backcloth()
    # the flats, front to back: deep violet at the lens, lilac, rose and peach toward the sun; seen from the
    # speaker's height each range rises a little above the one before it
    hills = ['#4A346C', '#654B8C', '#8468A8', '#A587BE', '#C9A3C4', '#E6B9B4']
    P.append(flat(-3.5, -0.2, -1.5, 0.48, 0.08, 11, hills[0], waves=1.2, ends=(0, 0.9), skew=-0.3))
    P.append(flat(0.75, 4.5, -1.6, 0.36, 0.07, 12, hills[0], waves=1.0, ends=(0.6, 0)))
    P.append(flat(-5.5, 0.95, 1.4, 0.3, 0.08, 21, hills[1], waves=2.2, ends=(0, 0.6)))
    P.append(flat(1.55, 6.0, 1.55, 0.27, 0.07, 22, hills[1], waves=1.6, ends=(0.55, 0)))
    P.append(flat(-6.0, 6.0, 2.5, 0.45, 0.1, 31, hills[2], waves=3.0,
                  trees=[(-1.75, 0.06, 0.07, 0.24), (1.42, 0.07, 0.075, 0.27), (1.6, 0.05, 0.06, 0.19)]))
    P.append(flat(-6.5, 6.5, 3.6, 0.6, 0.12, 41, hills[3], waves=2.4, trees=[(-1.4, 0.05, 0.12, 0.12), (2.5, 0.05, 0.1, 0.1)]))
    # the far flats in tissue, so the sun behind them shows through their edges
    P.append(flat(-7.0, 7.0, 4.65, 0.72, 0.12, 51, hills[4], waves=2.0, material='tissue'))
    P.append(flat(-7.5, 7.5, 5.6, 0.82, 0.1, 61, hills[5], waves=1.6, material='tissue'))
    # the sun, a tissue disc lit from behind, sunk behind the last flat and hung on two threads
    P.append(disc(sx, sy, sz, sr, 'tissue', '#FFC08A', emit=0.9, emit_color='#FFB070'))
    for dx in (-sr * 0.55, sr * 0.55):
        a = [sx + dx, sy, sz + math.sqrt(sr * sr - dx * dx) - 0.02]
        P.append(kit('thread', 'paper', '#EADFE6', a=a, b=[a[0], sy, 6.0], radius=0.0012))
    # three bands of tulle across the sun, staggered as layers drift, shorter as they rise
    P += tulle_band(sx - 0.17, sy - 0.35, sz - 0.05, 2.25, 0.24, 71, top=6.0)
    P += tulle_band(sx - 0.05, sy - 0.25, sz + 0.3, 2.1, 0.22, 72, top=6.0)
    P += tulle_band(sx - 0.12, sy - 0.15, sz + 0.65, 1.9, 0.2, 73, top=6.0)
    # scrims of tulle hung between the flats, their tops out of sight: the haze that pales each range behind the last
    for y, a in ((3.05, 0.12), (4.1, 0.12)):
        P.append(kit('drape', 'tulle', '#EBC6CF', size=[15.0, 4.0], folds=22, amplitude=0.003, noise=0.1, thickness=0.0,
                     res=200, seed=int(y * 10), alpha=a, emit=0.3, emit_color='#F2B9A6', position=[0.0, y, 3.98]))
    P += river()
    # the moon, a paper crescent already up, waiting for its cue
    moon = crescent(0.3)
    P.append(kit('extrude', 'card', '#F3E6D6', outline=moon, depth=0.01, ease=0.002, position=MOON,
                 emit=0.25, emit_color='#FFF1DC'))
    P.append(kit('thread', 'paper', '#EADFE6', a=[MOON[0], MOON[1], MOON[2] + 0.29], b=[MOON[0], MOON[1], 6.0], radius=0.0012))
    return P


def lights():
    sx, sy, sz, sr = SUN
    return {
        # the sun: behind the tissue disc, low and warm, so the acrylic glows through and throws violet forward
        'sun': {'type': 'area', 'size_m': [1.6, 1.2], 'position': [sx - 0.2, sy + 0.3, sz + 0.5], 'target': [0.0, 0.0, 0.8],
                'irradiance': 7.0, 'color': '#FFB27C', 'camera': False},
        # its glow on the backcloth round the disc
        'halo': {'type': 'point', 'position': [sx, sy + 0.6, sz + 0.2], 'power_w': 110, 'color': '#FFB98A', 'radius_m': 0.4},
        # the key: the dusk sky's soft lilac light on the speaker's face, from the front left, on the speaker alone
        'face': {'type': 'area', 'size_m': [1.4, 1.4], 'orbit': {'azimuth_deg': -38, 'elevation_deg': 18, 'distance_m': 3.2},
                 'target': [0.0, 0.0, 0.7], 'irradiance': 3.6, 'color': '#E9D8F4', 'camera': False, 'receivers': SPEAKER},
        'glow': {'type': 'area', 'size_m': [0.7, 0.32], 'position': [0.0, 0.66, 1.12], 'target': [0.0, 0.0, 1.1],
                 'irradiance': 4.0, 'color': '#FFC9A0', 'specular': 0, 'transmission': False, 'receivers': SPEAKER},
        # the sun's edge down both sides and over the horn, from behind
        'rim': {'type': 'area', 'size_m': [1.0, 1.4], 'orbit': {'azimuth_deg': -150, 'elevation_deg': 18, 'distance_m': 3.0},
                'target': [0.0, 0.0, 0.8], 'irradiance': 8.0, 'color': '#FFB98E', 'camera': False, 'receivers': SPEAKER},
        'rim2': {'type': 'area', 'size_m': [1.0, 1.4], 'orbit': {'azimuth_deg': 150, 'elevation_deg': 18, 'distance_m': 3.0},
                 'target': [0.0, 0.0, 0.8], 'irradiance': 6.0, 'color': '#FFB27C', 'camera': False, 'receivers': SPEAKER},
        # the sun through the horn, from behind and low, on the speaker alone
        'through': {'type': 'area', 'size_m': [0.8, 0.8], 'orbit': {'azimuth_deg': 172, 'elevation_deg': 12, 'distance_m': 3.0},
                    'target': [0.0, 0.0, 1.2], 'irradiance': 10.0, 'color': '#FFB27C', 'camera': False, 'receivers': SPEAKER},
        # the sun grazing the floor, through the speaker's clear foot: violet light thrown forward onto the paper
        'low': {'type': 'area', 'size_m': [0.9, 0.4], 'orbit': {'azimuth_deg': 172, 'elevation_deg': 6, 'distance_m': 2.2},
                'target': [0.0, 0.0, 0.2], 'irradiance': 2.0, 'color': '#FFC090', 'camera': False, 'spread_deg': 45},
        # the dusk sky overhead, lilac
        'sky': {'type': 'area', 'size_m': [6.0, 4.0], 'orbit': {'azimuth_deg': -10, 'elevation_deg': 55, 'distance_m': 7.0},
                'target': [0.0, 1.0, 0.4], 'irradiance': 0.5, 'color': '#C4B2E8', 'camera': False},
    }


def shot():
    st = {'kind': 'stage', 'kit_scale': 6.0, 'props': props()}
    # level with the speaker (the owner, 2026-10-18), its front turned toward the sun
    cam = tilt_shift(elevation=2.5, azimuth=0.0, distance=5.2, lens=65, target=(0.36, 0.0, 0.75), focus=(0.0, -0.25, 0.7),
                     fstop=5.6, miniature=6)
    sky = {'kind': 'gradient', 'zenith': '#4A3A6A', 'horizon': '#8C6E9A', 'ground': '#2E2440', 'strength': 0.35}
    return frame('haze', st, lights(), cam, 'barkhorn, Haze, dusk in paper and tulle', sky=sky,
                 fin=finish(bloom=0.3, bloom_px=50, threshold=0.75, saturation=0.15, lift=0.04, lift_color='#3B2A55',
                            vignette=0.22), rotate_z=22.0, exposure=0.3)


def portrait():
    return portrait_of(shot(), **tilt_shift(elevation=2.0, azimuth=0.0, distance=5.2, lens=104, target=(0.27, 0.0, 0.86),
                                            focus=(0.0, -0.25, 0.7), fstop=8.0, miniature=6))
