"""A classy listening bar (the coordinator, 2026-11-11 16:41; the owner: "the setting is more dive bar than classy"): a
hotel bar or a Tokyo hi-fi bar in a converted brick building, that passes as a photograph of a place that charges $22 a
drink. One set, three frames:

    bar-wide            the whole bar straight on: five to seven Hemispheres over the bar top, three Cores on the stone,
                        Mantle on the back bar with a record on, a pair of Tropos flanking the back bar
    bar-pendants        closer on the Hemisphere cluster over the stone, two Cores under it
    core-bar-table      one Core on the stone, shallow focus, the back bar soft behind, its cable out of the back

    TROPOS_BASE=A python3 spinoffs/barkhorn/campaign/listening_bar.py OUTDIR

The set (Poly Haven CC0 textures, everything else modelled here, plainly): an even red brick wall (red_brick_03, its
mortar dark), a walnut back bar (american_walnut_veneer, stained) with millwork shelves and thin shadow gaps, bottles
in ordered rows (turned dark and clear glass, plain cream labels), a run of record spines, stacked tumblers and coupes
(turned glass); the bar's front vertical fluted walnut, its top one slab of honed dark stone (concrete_floor_01 taken
near black, fine speckle, a soft sheen) with a bullnose, a blackened steel foot rail; a polished concrete floor
(brushed_concrete_03, its roughness down); cognac leather stools with low backs on slim black legs (brown_leather);
on the bar a crystal decanter, two rocks glasses, a folded linen napkin, a short stack of record sleeves. Products in
the warm family only (Ember, Dust, Acid). Exposed for the lamps as the lamps lane does (AgX, Punchy, no white
balance), the room lifted by declared light from out of frame; nothing lit in frame but EARF's lamps.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots  # noqa: E402

LAMPS = 'spinoffs/barkhorn/campaign/stage/stage2_props.py'
WALL_Y, BACKBAR_D, BAR_Y0, BAR_Y1, BAR_H = 2.2, 0.46, 0.0, 0.62, 1.07     # metres
X0, X1 = -1.95, 1.95                                                      # the bar's run (test 1: at 2.3 its ends hid the Tropos pair)
WALNUT = {'material': 'pbr', 'texture': 'american_walnut_veneer', 'tex_res': '2k', 'tint': '#5A3824', 'tint_mix': 0.55, 'gain': 0.62, 'rough_mul': 0.8}
STONE = {'material': 'pbr', 'texture': 'concrete_floor_01', 'tex_res': '2k', 'tint': '#262627', 'tint_mix': 0.85, 'gain': 0.28, 'rough_mul': 0.32}
BRICK = {'material': 'pbr', 'texture': 'red_brick_03', 'tex_res': '2k', 'tint': '#7A4A3C', 'tint_mix': 0.25, 'gain': 0.8}
FLOOR = {'material': 'pbr', 'texture': 'brushed_concrete_03', 'tex_res': '2k', 'gain': 0.55, 'rough_mul': 0.45}
LEATHER = {'material': 'pbr', 'texture': 'brown_leather', 'tex_res': '2k', 'gain': 0.9}
STEEL = {'material': 'clay', 'color': '#141415', 'roughness': 0.38}      # blackened steel, satin


def box(size, pos, mat, ease=0.0, rot=None):
    p = {'kind': 'kit', 'shape': 'box', 'size': size, 'position': pos, **mat}
    if ease:
        p['ease'] = ease
    if rot:
        p['rotate'] = rot
    return p


def lathe(profile, pos, mat, color, seg=48, **k):
    return {'kind': 'kit', 'shape': 'lathe', 'profile': profile, 'position': pos, 'material': mat, 'color': color, 'segments': seg, **k}


def cyl(r, h, pos, mat, rot=None):
    p = {'kind': 'kit', 'shape': 'cylinder', 'radius': r, 'height': h, 'position': pos, **mat}
    if rot:
        p['rotate'] = rot
    return p


# turned glass, real glass (the kit's glass: transmission 1, IOR 1.5), walls and bases of real thickness
ROCKS = [[0, 0], [0.041, 0], [0.042, 0.004], [0.043, 0.092], [0.0405, 0.092], [0.0395, 0.014], [0, 0.014]]
COUPE = [[0, 0], [0.038, 0], [0.039, 0.004], [0.006, 0.012], [0.0045, 0.10], [0.03, 0.112], [0.052, 0.128], [0.055, 0.136],
         [0.0525, 0.136], [0.049, 0.129], [0.028, 0.116], [0, 0.112]]
DECANTER = [[0, 0], [0.062, 0], [0.066, 0.012], [0.066, 0.135], [0.05, 0.175], [0.022, 0.2], [0.018, 0.235], [0.022, 0.245],
            [0.0175, 0.245], [0.014, 0.236], [0.018, 0.2], [0.046, 0.172], [0.0615, 0.134], [0.0615, 0.016], [0, 0.012]]
STOPPER = [[0, 0], [0.014, 0], [0.014, 0.02], [0.028, 0.045], [0.0, 0.075]]
BOTTLE = [[0, 0], [0.036, 0], [0.037, 0.004], [0.037, 0.19], [0.03, 0.225], [0.016, 0.25], [0.0135, 0.262], [0.0135, 0.30],
          [0.0155, 0.305], [0, 0.305]]
TALL = [[0, 0], [0.033, 0], [0.034, 0.004], [0.034, 0.22], [0.018, 0.26], [0.0125, 0.285], [0.0125, 0.33], [0.014, 0.335], [0, 0.335]]


def backbar():
    """The back bar: a walnut base cabinet against the brick (its doors in panels with thin shadow gaps), a run of
    walnut shelves in bays above it, bottles in ordered rows, a run of record spines, stacked tumblers and coupes."""
    out = []
    y0 = WALL_Y - BACKBAR_D
    out.append(box([X1 - X0 + 0.2, BACKBAR_D, 0.92], [0.0, y0 + BACKBAR_D / 2, 0.0], WALNUT, 0.004))
    for k in range(10):                                   # the doors: panels with a 4 mm shadow gap between
        w = (X1 - X0 + 0.2) / 10
        out.append(box([w - 0.004, 0.012, 0.8], [X0 - 0.1 + w * (k + 0.5), y0 - 0.006, 0.05], WALNUT, 0.002))
    out.append(box([X1 - X0 + 0.24, BACKBAR_D + 0.03, 0.035], [0.0, y0 + BACKBAR_D / 2 - 0.015, 0.92], WALNUT, 0.006))   # its top
    sd = 0.26                                             # the shelves above
    for z in (1.34, 1.72, 2.1):
        out.append(box([X1 - X0 + 0.1, sd, 0.03], [0.0, WALL_Y - sd / 2, z], WALNUT, 0.003))
    for x in [X0 - 0.05 + (X1 - X0 + 0.1) * k / 6 for k in range(7)]:       # the bay sides
        out.append(box([0.03, sd, 1.22], [x, WALL_Y - sd / 2, 0.955], WALNUT, 0.003))
    bay = (X1 - X0 + 0.1) / 6
    bx = lambda k: X0 - 0.05 + bay * (k + 0.5)
    glass_dark, glass_amber, glass_clear = '#1C2620', '#5A3510', '#F4F6F5'
    # bottles in ordered rows: bays 0, 1, 4 and 5 on the middle and top shelves; plain cream labels
    for k in (0, 1, 4, 5):
        for z, tall in ((1.37, False), (1.75, True)):
            n = 6
            for j in range(n):
                x = bx(k) - bay / 2 + 0.07 + j * (bay - 0.14) / (n - 1)
                col = [glass_dark, glass_amber, glass_clear][(j + k) % 3]
                prof = TALL if tall else BOTTLE
                out.append(lathe(prof, [round(x, 3), WALL_Y - 0.12, z], 'glass', col, 32))
                out.append(cyl(0.0372 if not tall else 0.0342, 0.075, [round(x, 3), WALL_Y - 0.12, z + 0.07],
                               {'material': 'paper', 'color': '#E6DCC6', 'roughness': 0.8}))
    # a run of record spines: bays 2 and 3 on the lowest shelf
    cols = ['#2B2A28', '#4A3A2C', '#6E5A44', '#1E2124', '#7C6B55', '#3B3328', '#5C4C3E', '#262422']
    for k in (2, 3):
        n = 34
        for j in range(n):
            x = bx(k) - bay / 2 + 0.05 + j * (bay - 0.1) / n
            out.append(box([0.006, 0.3, 0.31], [round(x, 4), WALL_Y - 0.155, 0.955], {'material': 'card', 'color': cols[(j * 5 + k) % len(cols)]}))
    # stacked tumblers and coupes: bays 2 and 3, the middle shelf (rocks glasses stacked two high) and top (coupes)
    for k in (2, 3):
        for j in range(5):
            x = bx(k) - bay / 2 + 0.09 + j * (bay - 0.18) / 4
            out.append(lathe(ROCKS, [round(x, 3), WALL_Y - 0.13, 1.355], 'glass', glass_clear))
            out.append(lathe(ROCKS, [round(x, 3), WALL_Y - 0.13, 1.355 + 0.08], 'glass', glass_clear))
            out.append(lathe(COUPE, [round(x, 3), WALL_Y - 0.13, 1.735], 'glass', glass_clear))
    return out


def bar_counter():
    """The bar: its front vertical fluted walnut, its top one slab of honed dark stone with a small bullnose, a
    blackened steel foot rail on brackets."""
    out = []
    L = X1 - X0
    out.append(box([L, BAR_Y1 - BAR_Y0, BAR_H - 0.06], [0.0, (BAR_Y0 + BAR_Y1) / 2, 0.0], WALNUT))           # the carcass
    n = int(L / 0.032)                                     # the flutes, 32 mm on centres
    for j in range(n):
        x = X0 + (j + 0.5) * L / n
        out.append(cyl(0.0145, BAR_H - 0.06 - 0.1, [round(x, 4), BAR_Y0 - 0.002, 0.1], WALNUT))
    out.append(box([L + 0.04, 0.02, 0.1], [0.0, BAR_Y0 - 0.01, 0.0], {'material': 'clay', 'color': '#0E0E0E', 'roughness': 0.6}))   # its toe kick
    out.append(box([L + 0.1, BAR_Y1 - BAR_Y0 + 0.08, 0.06], [0.0, (BAR_Y0 + BAR_Y1) / 2 - 0.02, BAR_H - 0.06], STONE, 0.022))  # the slab
    rail_y, rail_z = BAR_Y0 - 0.2, 0.2                      # the foot rail
    out.append(cyl(0.025, L - 0.2, [X0 + 0.1, rail_y, rail_z], STEEL, rot=[0.0, 90.0, 0.0]))
    for x in (X0 + 0.3, -0.75, 0.75, X1 - 0.3):
        out.append(cyl(0.012, 0.2, [x, rail_y + 0.1, rail_z], STEEL, rot=[90.0, 0.0, 0.0]))
    return out


def stool(x, y, yaw):
    """A cognac leather stool with a low back on slim black legs."""
    out = []
    seat = 0.74
    out.append(cyl(0.2, 0.075, [x, y, seat], LEATHER))
    a = math.radians(yaw)
    bx_, by_ = x - 0.17 * math.sin(a) * -1, y + 0.17 * math.cos(a)
    out.append(box([0.34, 0.045, 0.17], [round(bx_, 3), round(by_, 3), seat + 0.06], LEATHER, 0.018, rot=[-8.0, 0.0, yaw]))
    for k in range(4):
        t = math.radians(45 + 90 * k + yaw)
        out.append(cyl(0.011, seat, [round(x + 0.15 * math.cos(t), 3), round(y + 0.15 * math.sin(t), 3), 0.0], STEEL))
    out.append(lathe([[0.155, 0.27], [0.165, 0.27], [0.165, 0.285], [0.155, 0.285], [0.155, 0.27]], [x, y, 0.0], 'clay', '#141415', 48, roughness=0.38))
    return out


def dressing(cx):
    """On the bar: a crystal decanter, two rocks glasses, a folded linen napkin, a short stack of record sleeves."""
    T = BAR_H
    out = [lathe(DECANTER, [cx + 0.55, 0.33, T], 'glass', '#F6F7F6', 64),
           lathe(STOPPER, [cx + 0.55, 0.33, T + 0.236], 'glass', '#F6F7F6', 48),
           lathe(ROCKS, [cx + 0.71, 0.24, T], 'glass', '#F6F7F6', 64),
           lathe(ROCKS, [cx + 0.82, 0.31, T], 'glass', '#F6F7F6', 64),
           box([0.2, 0.14, 0.012], [cx + 0.77, 0.24, T], {'material': 'cotton', 'color': '#E8E2D6'}, 0.004, rot=[0.0, 0.0, 12.0])]
    for k in range(4):                                     # a short stack of sleeves, a little askew
        out.append(box([0.315, 0.315, 0.004], [cx - 0.95, 0.33, T + 0.004 * k], {'material': 'card', 'color': ['#2A2826', '#7C6B55', '#3B3328', '#C9BBA2'][k]},
                       rot=[0.0, 0.0, [3.0, -2.0, 6.0, -4.0][k]]))
    return out


def room(cx=0.0):
    return [box([14.0, 12.0, 0.02], [0.0, -4.0, -0.02], FLOOR),
            box([14.0, 0.3, 5.0], [0.0, WALL_Y + 0.15, -0.02], BRICK),
            *backbar(), *bar_counter(),
            *stool(-1.35, -0.55, 0.0), *stool(-0.45, -0.6, 0.0), *stool(0.45, -0.55, 0.0), *stool(1.35, -0.6, 0.0),
            *dressing(cx)]


WARM = ('ember', 'dust', 'acid')


def _lamps(hemis, cores, top=4.2):
    return {'kind': 'kit', 'shape': 'ext', 'path': LAMPS, 'fn': 'lamps', 'top_z': top, 'led_k': shots.LED_K, 'core_load': shots.CORE_LOAD,
            'hemispheres': [{'tint': shots.KEY[t], 'x': x, 'y': y, 'rim_z': z} for t, x, y, z in hemis],
            'cores': [{'tint': shots.KEY[t], 'x': x, 'y': y, 'floor_z': BAR_H, 'rot': 0.0} for t, x, y in cores]}


# (test 1: hung at 1.7-1.9 they sat in front of the shelves and were lost: higher, against the brick above them)
# (frames 1, measured: hung at 2.2-2.4 over a standing eye the shades showed their dark closed undersides, value 0.4
# against the finals' 1.0: hung as a bar hangs them, 0.5-0.7 m over the top, seen from the side)
HEMIS = [('ember', -1.5, 0.3, 1.62), ('dust', -1.0, 0.36, 1.76), ('acid', -0.5, 0.28, 1.58), ('ember', 0.0, 0.34, 1.72),
         ('dust', 0.5, 0.3, 1.6), ('acid', 1.0, 0.36, 1.78), ('ember', 1.5, 0.3, 1.66)]
CORES = [('ember', -1.2, 0.3), ('dust', -0.15, 0.32), ('acid', 1.0, 0.3)]
# (test 2, measured: the Cores already at the finals' hue and above their saturation, the shades at value 0.3-0.4 against
# the finals' 1.0: a stop up, toward the Hemisphere's own -2; the room's light halved to hold it)
EV = -2.5
ROOM = 0.35          # the declared room light's scale


def _base(size, title):
    s = shots._cast_base()
    s['products'] = []
    s['set'] = {'kind': 'stage', 'props': room()}
    s['materials'] = {k: v for k, v in s.get('materials', {}).items() if k != 'sweep'}
    s['sky'] = {'kind': 'gradient', 'strength': 0.0}
    # declared, out of frame: the room's own soft light (a large warm soffit above and behind the camera) and a low cool
    # fill from the street side (a dusk window, left, out of frame)
    s['lights'] = {'soffit': {'type': 'area', 'size_m': [5.0, 1.2], 'position': [0.0, -3.2, 3.6], 'target': [0.0, 1.4, 1.2],
                              'irradiance': round(18.0 * ROOM, 3), 'color': '#FFE2C2', 'spread_deg': 70},
                   'dusk-window': {'type': 'area', 'size_m': [2.0, 2.4], 'position': [-5.0, -1.0, 1.8], 'target': [0.0, 1.2, 1.1],
                                   'irradiance': round(6.0 * ROOM, 3), 'color': '#A8B8D8'}}
    s['size'] = size
    s['render'] = {**s['render'], 'samples': 64, 'denoise': True, 'clamp': 0, 'bounces': 32, 'diffuse_bounces': 8,
                   'glossy_bounces': 16, 'transmission_bounces': 24, 'caustics_refractive': True, 'caustics_reflective': False,
                   'view': 'AgX', 'look': 'AgX - Punchy', 'exposure': EV}
    s['render'].pop('white_balance_k', None); s['render'].pop('white_balance_tint', None)
    s.pop('finish', None)
    s['title'] = title
    return s


def bar_wide():
    s = _base([1920, 1080], 'A listening bar: the whole bar straight on')
    c = shots._cast_base()
    k = shots.HERO_ORDER.index('ember')
    pair = []
    for blk in c['products']:
        i = blk['instances'][k]
        pair.append({**blk, 'instances': [{**copy.deepcopy(i), 'position': [X0 - 0.75, WALL_Y - 0.5, 0.0], 'rotate_z': 16.0},
                                          {**copy.deepcopy(i), 'position': [X1 + 0.75, WALL_Y - 0.5, 0.0], 'rotate_z': -16.0}]})
    s['products'] = pair
    shots._approved(s, order=['ember', 'ember'])
    # (frames 1: on the back bar's top Mantle sat below the line over the bar top: on a walnut plinth, the records under it)
    s['set']['props'].append(box([0.56, 0.42, 0.24], [-0.33, WALL_Y - BACKBAR_D / 2 - 0.02, 0.955], WALNUT, 0.004))
    s['products'].append(shots._mantle(-0.33, WALL_Y - BACKBAR_D / 2 - 0.02, 0.955 + 0.24 + 0.001, 0.0, tint='dust'))
    s['set']['props'].append(_lamps(HEMIS, CORES))
    # (test 1: from 1.32 m the bar top hid Mantle on the back bar: a standing guest's eye)
    s['camera'] = {'position': [0.0, -4.9, 1.62], 'target': [0.0, 1.0, 1.4], 'lens_mm': 32.0, 'level': True}
    return s


def bar_pendants():
    s = _base([1920, 1080], 'A listening bar: the Hemisphere cluster over the stone')
    s['set']['props'].append(_lamps(HEMIS[1:6], [('ember', -0.45, 0.28), ('acid', 0.42, 0.3)]))
    # (frames 1: the cluster above the frame: framed on it, the Cores at its foot)
    s['camera'] = {'position': [0.1, -2.6, 1.48], 'target': [0.0, 0.3, 1.4], 'lens_mm': 45.0, 'level': True,
                   'fstop': 2.8, 'focus': [0.0, 0.3, 1.4]}
    return s


def core_bar_table():
    s = _base([1920, 1280], 'A listening bar: one Core on the stone')
    s['set']['props'].append(_lamps([], [('ember', 0.25, 0.25)]))
    s['camera'] = {'position': [0.4, -0.95, 1.24], 'target': [0.25, 0.25, BAR_H + 0.12], 'lens_mm': 85.0, 'level': True,
                   'fstop': 2.0, 'focus': [0.25, 0.25, BAR_H + 0.12]}
    s['render']['exposure'] = -4.5              # Core alone: near the lamps lane's own -5 (test 2: the ball's value a little low at -4)
    s['lights'] = {k: {**v, 'irradiance': round(v['irradiance'] * 2 ** (EV + 4.5), 3)} for k, v in s['lights'].items()}
    return s


SHOTS = {'bar-wide': bar_wide, 'bar-pendants': bar_pendants, 'core-bar-table': core_bar_table}

if __name__ == '__main__':
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    for n, f in SHOTS.items():
        json.dump(f(), open(os.path.join(od, n + '.json'), 'w'), indent=1)
        print(n)
