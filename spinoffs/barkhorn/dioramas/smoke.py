"""Smoke: the night train (round 31; notes and proof rounds in smoke.md).

A little steam train in black lacquered card runs along a card track behind the speaker, its carriages' windows lit
warm, its stack billowing grey wool smoke in the icon's plume (a small puff joined into a big one, drifting left to
right). Behind, a row of card houses with lit windows and chimneys on a charcoal wool hill, a paper moon on a thread
over the roofs, pin-prick stars on a black card sky; the ground soot-black velvet. Seen from above through a tilt-shift
lens. The moon rims the smoked acrylic cool from behind; the carriages' windows glow warm through it.
"""
import math, random

from common import finish, kit, mound, point, portrait_of, shot as frame, tilt_shift

CARD = '#141416'          # black lacquered card
CARD2 = '#1B1A1D'         # a second black, so the pieces separate
WARM = '#FFB25C'          # the lit windows
MOON = '#F4E9CC'
RAIL_Y = 1.3              # the track's centre line
SMOKE = [(-201, 112, 60), (-111, 69, 90), (9, -51, 120), (154, -36, 108), (54, 49, 100)]   # icons.smoke()


def scaled(pieces, k, origin):
    """Pieces scaled by `k` about `origin` (the train built at full size, then made a toy beside the speaker)."""
    ox, oy, oz = origin
    for q in pieces:
        if 'position' in q:
            x, y, z = q['position']
            q['position'] = [round(ox + (x - ox) * k, 4), round(oy + (y - oy) * k, 4), round(oz + (z - oz) * k, 4)]
        for key in ('radius', 'height', 'ease'):
            if isinstance(q.get(key), (int, float)):
                q[key] = q[key] * k
        if q['shape'] != 'puffs' and 'depth' in q:
            q['depth'] *= k
        for key in ('size', 'outline', 'profile', 'puffs'):
            if key in q:
                q[key] = [[v * k for v in row] if isinstance(row, list) else row * k for row in q[key]]
        if isinstance(q.get('scale'), list):
            q['scale'] = [v * k for v in q['scale']]
    return pieces


def lacquer(shape, color=CARD, **k):
    return kit(shape, 'card', color, roughness=0.28, **k)


def glow(shape, emit=6.0, color=WARM, **k):
    return kit(shape, 'glow', color, emit=emit, **k)


def wheel(x, y, z, r, side):
    """A card wheel on its axle, facing the camera's side (`side` -1) or away (+1)."""
    return [lacquer('cylinder', CARD2, radius=r, height=0.03, position=[x, y, z], rotate=[90 * side, 0, 0], segments=40),
            lacquer('cylinder', '#2A292D', radius=r * 0.35, height=0.036, position=[x, y, z], rotate=[90 * side, 0, 0])]


def wheels(xs, r, z=None):
    out = []
    for x in xs:
        out += wheel(x, RAIL_Y - 0.2, z or r, r, 1) + wheel(x, RAIL_Y + 0.2, z or r, r, -1)
    return out


def locomotive(xf):
    """A tank engine heading toward -x, its front at `xf`; returns (pieces, the stack's top)."""
    y = RAIL_Y
    p = [lacquer('box', size=[1.25, 0.36, 0.07], position=[xf + 0.62, y, 0.1], ease=0.01)]
    p += wheels([xf + 0.28, xf + 0.58, xf + 0.88], 0.11)
    p += [lacquer('cylinder', radius=0.17, height=0.78, position=[xf + 0.04, y, 0.36], rotate=[0, 90, 0], segments=48),
          lacquer('cylinder', CARD2, radius=0.185, height=0.06, position=[xf + 0.0, y, 0.36], rotate=[0, 90, 0]),
          lacquer('cylinder', CARD2, radius=0.18, height=0.03, position=[xf + 0.42, y, 0.36], rotate=[0, 90, 0]),
          lacquer('lathe', profile=[[0.0, 0.0], [0.06, 0.0], [0.055, 0.12], [0.085, 0.2], [0.1, 0.25], [0.0, 0.25]],
                  position=[xf + 0.17, y, 0.48]),
          lacquer('sphere', CARD2, position=[xf + 0.55, y, 0.53], scale=[0.075, 0.075, 0.06]),
          lacquer('box', size=[0.42, 0.44, 0.5], position=[xf + 0.98, y, 0.15], ease=0.012),
          lacquer('box', CARD2, size=[0.54, 0.52, 0.04], position=[xf + 0.98, y, 0.65], ease=0.015),
          glow('box', 5.0, size=[0.15, 0.008, 0.13], position=[xf + 0.98, y - 0.222, 0.42]),
          glow('box', 3.0, '#FF9A40', size=[0.1, 0.008, 0.05], position=[xf + 0.86, y - 0.222, 0.2]),   # the firebox
          lacquer('extrude', CARD2, outline=[[0, 0], [0.16, 0], [0.16, 0.16]], depth=0.3,
                  position=[xf - 0.14, y, 0.03]),
          lacquer('cylinder', CARD2, radius=0.045, height=0.05, position=[xf - 0.02, y, 0.6], rotate=[0, -90, 0]),
          glow('cylinder', 10.0, '#FFE2B0', radius=0.032, height=0.008, position=[xf - 0.07, y, 0.6], rotate=[0, -90, 0])]
    # the coal bunker behind the cab
    p += [lacquer('box', size=[0.36, 0.4, 0.3], position=[xf + 1.38, y, 0.15], ease=0.01)]
    return p, (xf + 0.17, y, 0.73)


def carriage(x0, length=1.5):
    y = RAIL_Y
    xc = x0 + length / 2
    p = [lacquer('box', size=[length, 0.44, 0.42], position=[xc, y, 0.16], ease=0.012),
         lacquer('box', CARD2, size=[length + 0.08, 0.5, 0.05], position=[xc, y, 0.58], ease=0.02),
         lacquer('box', CARD2, size=[length - 0.3, 0.3, 0.04], position=[xc, y, 0.63], ease=0.015)]
    p += wheels([x0 + 0.22, x0 + 0.46, x0 + length - 0.46, x0 + length - 0.22], 0.08)
    n = 5
    for i in range(n):
        x = x0 + 0.2 + (length - 0.4) * (i + 0.5) / n
        p.append(glow('box', 6.0, size=[0.17, 0.008, 0.15], position=[x, y - 0.222, 0.33]))
    return p


def track(x0=-8.0, x1=8.0):
    y = RAIL_Y
    p = [kit('box', 'felt', '#262427', size=[x1 - x0, 0.72, 0.025], position=[(x0 + x1) / 2, y, 0.0], ease=0.008)]
    x = x0 + 0.1
    while x < x1:
        p.append(lacquer('box', '#201E1F', size=[0.07, 0.56, 0.018], position=[round(x, 3), y, 0.025]))
        x += 0.2
    for dy in (-0.2, 0.2):
        p.append(kit('box', 'card', '#3A393E', roughness=0.2, size=[x1 - x0, 0.022, 0.026], position=[(x0 + x1) / 2, y + dy, 0.043]))
    return p


def plume(stack, s=0.0046, light='#ADABAA', dark='#878688'):
    """The icon's plume in grey wool, rising from the stack: a small puff of two circles joined into a big one of three,
    drifting left to right. Each circle is a billow, a ball with smaller balls bunched round its rim (a cauliflower, as
    wool teased into a puff is), paler as the smoke thins and rises."""
    x0, y0, z0 = stack
    ax, az = x0 + 40 * s, z0 + 85 * s
    out = []
    rnd = random.Random(37)
    for i, (x, yy, r) in enumerate(SMOKE):
        X, Z, R = ax + (x + 201) * s, az - (yy - 112) * s, r * s
        Y = y0 + 0.06 * i
        t = min(1.0, (Z - z0) / (1.0))
        col = _mix(dark, light, t)
        core = 0.86 if i >= 2 else 0.97                      # the small puff's core fills its lumps' gaps (no dark pockets)
        out.append(kit('sphere', 'wool', col, position=[round(X, 4), round(Y, 4), round(Z, 4)], scale=[R * core, R * 0.75, R * core]))
        n = 5 if i < 2 else 8                             # billows on the upper side only: no dark pockets underneath
        for k in range(n):
            a = math.pi * (-0.15 + 1.3 * (k + 0.5 + rnd.uniform(-0.3, 0.3)) / n)
            e = rnd.uniform(-0.5, 0.6)
            up = 0.5 + 0.5 * math.sin(a)                  # billows bigger on top, the underside flatter
            rr = R * rnd.uniform(0.26, 0.42) * (0.75 + 0.55 * up)
            px, pz = math.cos(a) * R * 0.62, math.sin(a) * R * 0.62
            py = e * R * 0.45
            out.append(kit('sphere', 'wool', col, position=[round(X + px, 4), round(Y + py, 4), round(Z + pz, 4)],
                           scale=[rr, rr * 0.9, rr]))
    # the first breath out of the stack, into the small puff
    for k, (dx, dz, r) in enumerate([(0.0, 0.03, 0.04), (0.02, 0.09, 0.05), (0.045, 0.15, 0.06)]):
        out.append(kit('sphere', 'wool', dark, position=[x0 + dx, y0 + 0.03, z0 + dz], scale=[r, r * 0.9, r]))
    return out


def _mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(ca[i] + (cb[i] - ca[i]) * t):02X}' for i in range(3))


def house(x, y, w, h, d=0.45, roof=0.35, color=CARD, lit=(), chimney=None, seed=0):
    """A card house, its gable to the camera, windows lit warm by index (rows of two), a chimney at `chimney` (x share)."""
    out = [lacquer('extrude', color, outline=[[-w / 2, 0], [w / 2, 0], [w / 2, h], [0, h + roof], [-w / 2, h]], depth=d,
                   position=[x, y, 0], ease=0.006)]
    rows = max(1, int(h / 0.32))
    k = 0
    for r in range(rows):
        for c in (-1, 1):
            if k in lit:
                out.append(glow('box', 5.0, size=[w * 0.16, 0.008, 0.13], position=[x + c * w * 0.22, y - d / 2 - 0.004, h - 0.26 - r * 0.32]))
            k += 1
    if chimney is not None:
        cx = x + (chimney - 0.5) * w
        top = h + roof * (1 - abs(cx - x) / (w / 2)) + 0.16
        out.append(lacquer('box', CARD2, size=[0.1, 0.12, top], position=[cx, y, 0]))
    return out


def wisp(x, y, z, k=1.0, seed=0, ring=False):
    """A chimney's thin curl of wool smoke leaning right with the train's; or, once, a smoke ring (the set's joke: the
    one house that blows rings)."""
    if ring:
        pts = [[x + 0.11 * k * math.cos(2 * math.pi * i / 16), y, z + 0.11 * k * math.sin(2 * math.pi * i / 16)] for i in range(17)]
        return [kit('tube', 'wool', '#C4C2C1', points=pts, radius=0.035 * k, rotate=[0, 0, 0]),
                kit('sphere', 'wool', '#8E8D90', position=[x - 0.14 * k, y, z - 0.18 * k], scale=0.04 * k)]
    rnd = random.Random(seed)
    out, px, pz = [], x, z
    for i in range(5):
        r = (0.035 + 0.018 * i) * k
        out.append(kit('sphere', 'wool', _mix('#77767A', '#A9A7A8', i / 4), position=[round(px, 4), y, round(pz, 4)], scale=r))
        px += (0.03 + 0.02 * i) * k * rnd.uniform(0.8, 1.2); pz += (0.05 + 0.012 * i) * k
    return out


def pine(x, y, z, h, color=CARD, seed=0):
    """A card fir: three tiers of zigzag cut from black card on a stub of trunk, standing at (x, y, z)."""
    rnd = random.Random(seed)
    w = h * rnd.uniform(0.42, 0.5)
    pts = [[-0.05 * w, 0.0], [-0.05 * w, 0.12 * h]]
    tiers = [(0.12, 0.5, 1.0), (0.4, 0.75, 0.74), (0.64, 1.0, 0.48)]
    left = []
    for z0, z1, k in tiers:
        left += [[-w / 2 * k, z0 * h], [-w * 0.16 * k, (z0 + 0.06) * h]]
    pts += left + [[0.0, h]] + [[-px, pz] for px, pz in reversed(left)] + [[0.05 * w, 0.12 * h], [0.05 * w, 0.0]]
    # each tier's left corner then its notch going up; mirrored for the right side
    return [lacquer('extrude', color, outline=[[round(a, 4), round(b, 4)] for a, b in pts], depth=0.02 * h / 0.6,
                    ease=0.004, position=[x, y, z], rotate=[0, 0, rnd.uniform(-20, 20)])]


def ridge_z(x, cx, cz, sx, sz):
    t = (x - cx) / sx
    return cz + sz * math.sqrt(max(0.0, 1 - t * t))


def land():
    """A night valley the line runs through: four ridges of charcoal wool and felt, a little paler as they recede, a
    forest edge of black card firs along each."""
    rnd = random.Random(11)
    ridges = [(-1.5, 2.9, -0.35, 4.2, 0.9, 0.95, '#0E0E11', 'wool'), (2.6, 3.4, -0.4, 4.0, 1.0, 1.2, '#101014', 'wool'),
              (-0.5, 4.6, -0.6, 6.5, 1.2, 1.75, '#131319', 'felt'), (0.5, 6.0, -0.8, 8.0, 1.0, 2.3, '#191A22', 'felt')]
    out = []
    for i, (cx, cy, cz, sx, sy, sz, col, mat) in enumerate(ridges):
        out.append(mound(cx, cy, cz, sx, sy, sz, col, mat))
        n = int(sx * 4.5)
        for k in range(n):
            x = cx - sx * 0.85 + 1.7 * sx * (k + rnd.uniform(0.0, 0.9)) / n
            if rnd.random() < 0.15:
                continue
            yy = cy - sy * rnd.uniform(0.15, 0.4)
            # the ridge's surface where the tree stands, a little in front of the crest
            t = (yy - cy) / sy
            zc = cz + sz * math.sqrt(max(0.0, 1 - ((x - cx) / sx) ** 2 - t * t)) - 0.03
            if zc < 0.05:
                continue
            h = rnd.uniform(0.4, 0.75) * (1.0 + 0.25 * i)
            out += pine(round(x, 3), round(yy, 3), round(zc, 3), round(h, 3), (CARD, CARD2)[k % 2], seed=31 * i + k)
    return out


def signal_box(x=2.5, y=2.3):
    """The signal box beside the line, its stove's chimney blowing one neat smoke ring while the engine billows."""
    w, h, roof, ch = 0.5, 0.5, 0.2, 0.72
    out = house(x, y, w, h, d=0.4, roof=roof, color=CARD2, lit=(0, 1), chimney=ch)
    cx = x + (ch - 0.5) * w
    top = h + roof * (1 - abs(cx - x) / (w / 2)) + 0.16
    return out + wisp(cx + 0.03, y, top + 0.2, 0.85, ring=True)


def crescent(R, n=64):
    """A crescent: a circle of radius R less a circle of 0.9 R moved up and to the right."""
    d, e, r = 0.42 * R, 0.2 * R, 0.9 * R
    th0 = math.atan2(e, d)
    outer = [(R * math.cos(th0 + 2 * math.pi * i / n), R * math.sin(th0 + 2 * math.pi * i / n)) for i in range(n)]
    outer = [q for q in outer if math.hypot(q[0] - d, q[1] - e) > r]
    inner = [(d + r * math.cos(th0 + 2 * math.pi * i / n), e + r * math.sin(th0 + 2 * math.pi * i / n)) for i in range(n)]
    inner = [q for q in inner if math.hypot(*q) < R]
    return [[round(x, 4), round(z, 4)] for x, z in outer + inner[::-1]]


def star(r, inner=0.45):
    return [[round(r * (1 if i % 2 == 0 else inner) * math.sin(math.pi * i / 5), 4),
             round(r * (1 if i % 2 == 0 else inner) * math.cos(math.pi * i / 5), 4)] for i in range(10)]


def sky():
    mx, my, mz = -1.25, 5.4, 1.95
    out = [kit('scatter', 'glow', '#FFF1D6', emit=5.0, count=160, radius=[0.006, 0.016], seed=5,
               **{'in': [-8, 6.6, 1.4, 8, 6.75, 7.0]}),
           # the paper moon on its thread, a crescent cut from tissue and lit from within
           kit('extrude', 'tissue', MOON, emit=0.55, outline=crescent(0.46), depth=0.03, ease=0.006, position=[mx, my, mz],
               rotate=[0, 0, 0]),
           kit('thread', 'paper', '#C9C2B0', a=[mx - 0.2, my, mz + 0.4], b=[mx - 0.2, my, 8.0])]
    for x, y, z, r in ((0.5, 5.3, 2.25, 0.08), (1.7, 5.5, 2.05, 0.06), (2.9, 5.4, 2.3, 0.075), (-1.9, 5.2, 1.75, 0.055)):
        out += [kit('extrude', 'paper', '#F1E4C2', emit=0.9, outline=star(r), depth=0.012, ease=0.003, position=[x, y, z]),
                kit('thread', 'paper', '#C9C2B0', a=[x, y, z + r * 0.9], b=[x, y, 8.0])]
    return out


def tuft(x, y, r, seed, color='#1F1E23'):
    """A low clump of charcoal wool on the velvet: smoke that has settled, out of focus at the frame's edge."""
    rnd = random.Random(seed)
    out = [kit('sphere', 'wool', color, position=[x, y, 0.0], scale=[r, r * 0.8, r * 0.55])]
    for k in range(6):
        a = 2 * math.pi * k / 6 + rnd.uniform(-0.3, 0.3)
        rr = r * rnd.uniform(0.4, 0.6)
        out.append(kit('sphere', 'wool', color, position=[x + math.cos(a) * r * 0.75, y + math.sin(a) * r * 0.6, rr * 0.3],
                       scale=[rr, rr, rr * 0.8]))
    return out


TOY = 0.62               # the train's scale against the speaker


XF = -0.8                # the engine's front (before it is made a toy)
SPEAKER = (0.6, 0.0, 0.0)


def foreground():
    """Out-of-focus pieces at the frame's edge, between the camera and the speaker: a drift of settled charcoal wool in
    the left corner."""
    return tuft(-0.62, -1.9, 0.36, 3, '#24232A') + tuft(-0.25, -2.1, 0.2, 4, '#24232A')


def shot():
    loco, stack = locomotive(XF)
    train = scaled(track() + loco + carriage(XF + 1.6) + carriage(XF + 3.2) + carriage(XF + 4.8) + carriage(XF + 6.4), TOY,
                   (0.0, RAIL_Y, 0.0))
    sx, sy, sz = stack
    sx, sz = sx * TOY, sz * TOY
    # the ground: soot-black velvet laid over the set, softly rumpled (it rests on the sweep's floor, which it hides)
    props = [kit('drape', 'velvet', '#24232A', orient='lay', size=[16.0, 12.0], folds=3, amplitude=0.006, noise=0.7,
                 thickness=0.004, position=[0.0, 0.0, -0.004], res=240, seed=11)]
    smoke = plume((sx, sy, sz), s=0.0039)
    props += smoke + train + land() + signal_box() + sky() + foreground()
    # the moon's full light on the plume and the speaker alone (Cycles light linking, by the pieces' object names); the
    # land has a weaker share, so the wool hills stay charcoal rather than turning to moonlit snow
    keyed = [f'prop{i}-kit' for i in range(1, 1 + len(smoke))]
    st = {'kind': 'sweep', 'color': '#14151B', 'width': 18.0, 'front': 10.0, 'depth': 7.0, 'radius': 2.2, 'height': 9.0,
          'kit_scale': 11.0, 'props': props}
    shell = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'waveguide', 'waveguide-cap', 'woofer-ring', 'post-*',
             'grip-*', 'port-frame-*']
    tgt = [SPEAKER[0], 0.0, 0.75]
    lights = {
        'moon': {'type': 'area', 'size_m': [2.5, 2.5], 'orbit': {'azimuth_deg': -112, 'elevation_deg': 32, 'distance_m': 5.5},
                 'target': [0.0, 0.8, 0.8], 'irradiance': 2.0, 'color': '#DCE2EF', 'receivers': keyed},
        # the speaker's own share of the moon: enough to show the smoked panels, not to light the lining behind them
        'key': {'type': 'area', 'size_m': [2.0, 2.0], 'orbit': {'azimuth_deg': -70, 'elevation_deg': 25, 'distance_m': 4.0},
                'target': tgt, 'irradiance': 0.5, 'color': '#DCE2EF', 'receivers': shell},
        'moonset': {'type': 'area', 'size_m': [2.5, 2.5], 'orbit': {'azimuth_deg': -112, 'elevation_deg': 32, 'distance_m': 5.5},
                    'target': [0.0, 0.8, 0.8], 'irradiance': 0.6, 'color': '#DCE2EF'},
        # reflection cards (no diffuse light) where the level camera sees them in the smoked acrylic: the front, the
        # left side; and the moon behind the speaker, rimming its edges and its horn against the night
        'sheen': {'type': 'area', 'size_m': [0.5, 2.4], 'orbit': {'azimuth_deg': 52, 'elevation_deg': 10, 'distance_m': 4.0},
                  'target': tgt, 'irradiance': 0.9, 'color': '#C8D0E4', 'receivers': shell, 'diffuse': 0.0},
        'rim_l': {'type': 'area', 'size_m': [0.3, 3.0], 'orbit': {'azimuth_deg': -134, 'elevation_deg': 8, 'distance_m': 3.5},
                  'target': tgt, 'irradiance': 2.0, 'color': '#D2DBF2', 'receivers': shell, 'diffuse': 0.0},
        'rim_r': {'type': 'area', 'size_m': [1.2, 3.0], 'orbit': {'azimuth_deg': 150, 'elevation_deg': 24, 'distance_m': 3.0},
                  'target': tgt, 'irradiance': 4.0, 'color': '#D2DBF2', 'receivers': shell},
        'back': {'type': 'area', 'size_m': [2.0, 1.0], 'orbit': {'azimuth_deg': -170, 'elevation_deg': 40, 'distance_m': 3.0},
                 'target': [SPEAKER[0], 0.0, 1.1], 'irradiance': 3.0, 'color': '#D2DBF2', 'receivers': shell},
        'skyglow': {'type': 'area', 'size_m': [12.0, 0.5], 'position': [0.0, 5.6, 1.3], 'target': [0.0, 7.0, 2.6],
                    'irradiance': 1.2, 'color': '#5A6688', 'receivers': ['sweep']},
        'fill': {'type': 'area', 'size_m': [3.0, 2.0], 'orbit': {'azimuth_deg': -20, 'elevation_deg': 15, 'distance_m': 6.5},
                 'target': tgt, 'irradiance': 0.3, 'color': '#B0B8CC'},
        'firebox': point([sx + 0.05, RAIL_Y - 0.12, sz + 0.05], 3, '#FF9F55', 0.04),
    }
    cam = tilt_shift(elevation=1.5, azimuth=-6, distance=5.0, lens=65, target=(0.25, 0.0, 0.72),
                     focus=(SPEAKER[0], -0.2, 0.75), miniature=5)
    return frame('smoke', st, lights, cam, 'barkhorn, Smoke, the night train',
                 sky={'kind': 'gradient', 'zenith': '#07080C', 'horizon': '#0B0C12', 'ground': '#060608', 'strength': 0.2},
                 fin=finish(bloom=0.35, bloom_px=40, threshold=0.7, saturation=0.12, lift=0.04, lift_color='#1E2030',
                            vignette=0.25),
                 exposure=1.0, position=SPEAKER, rotate_z=20.0)


def portrait():
    """The 4:5 frame: the same set and light, the camera a little round to the right on a longer lens, so the moon and
    the engine fit beside the speaker in the narrower frame; the reflection cards follow the camera."""
    sh = shot()
    c = sh['camera']
    cam = tilt_shift(elevation=1.5, azimuth=2, distance=4.0, lens=70, target=(0.4, 0.0, 0.85), focus=tuple(c['focus']),
                     fstop=c['fstop'], miniature=c['miniature'], shift_y=0.02)
    sh['lights']['sheen']['orbit']['azimuth_deg'] = 40
    sh['lights']['rim_l']['orbit']['azimuth_deg'] = -142
    return portrait_of(sh, **cam)
