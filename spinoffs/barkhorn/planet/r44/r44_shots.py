"""Planet EARF, round 44: the lantern, rendered. The coordinator, 31 October 2026: "3 to 5 photoreal views. Calibrated
acrylic (IOR 1.49, A&C's TruCast transmission), real lenses, caustics where light passes through tint."

    python3 spinoffs/barkhorn/planet/r44/r44_shots.py [VIEW ...]     # writes studio/shots/barkhorn/planet44/VIEW.json

The room is `kit44.house` (plan44's geometry). Views: `street` (from the sidewalk at night: the shop, the bar and the
lantern at the end of the room), `bar` (from the shop table down the bar to the lantern's face), `lantern` (inside, from
the bench: Mother EARF on its plinth between the Tropos pair, its coloured shadow on the end-grain floor).
The products are as they stand (the other lanes' redesigns are proposals): the Ember Tropos pair, Cores, Hemispheres,
Mantle and the coins.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, HERE)
import plan44 as P                                                   # noqa: E402

BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet42', 'shop.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet44')
KIT = 'spinoffs/barkhorn/planet/r44/kit44.py'
CLOUD = 'studio/products/barkhorn-cloud.json'
MANTLE = 'spinoffs/barkhorn/companions/out-concepts2/r3.json'
FLAVOURS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
H = P.CEIL
I = P.INNER
YC = (I['y0'] + I['y1']) / 2

VIEWS = {
    # p3 (p2 judged street 5.0/4.5, bar 4.5/4.5, converged: a showroom exposure, not night; the band a clipped pink
    # lightbox; the shelf lines white neon; the lantern's face washed flat; fill and route flatten the room; the
    # terrazzo bright and coarse; no life; one bottle cloned; the porch a smear; the mullion near the center; mauve
    # oak): about a stop down; the band 1.1 in deep amber; the lines 1.8 at 2400 K; a graze raking down the baffle from
    # the band's foot; route 0.1, fill 0.02; darker, quieter terrazzo; glasses, a record; eight bottle profiles; the
    # porch in boards; the street camera nearer the glass, off the mullion; the tint toward green
    # p4, the last round for street and bar (p3 judged street 5.0/4.5, bar 5.0/5.0, converged: the band still pink and
    # clipping (the 2800 K balance desaturates amber); no foot line; the shelf lines hot; no pools on the counter; the
    # ceiling a void; the table a black slab on the axis; no glass in the street view; empty): white balance 3200 K, the
    # band 0.8 in deep amber, the foot line 9; lines 1.0; counter spots 22 W at 14 deg; fill 0.05; the shop table moved
    # off the axis in the plan; the street camera back so the mullion and the window plinth frame the left; glasses
    'street': dict(camera={'position': [-3.2, 3.0, 1.50], 'target': [13.0, 4.4, 1.95], 'lens_mm': 35, 'level': True,
                           'fstop': 4.0, 'focus': [7.0, 4.4, 1.2]}, exposure=2.6, haze=0.008, shutter=1.0, people='bar',
                   room={'glass_gloss': 0.6}),
    'bar': dict(camera={'position': [4.9, 2.55, 1.45], 'target': [13.0, 4.3, 2.0], 'lens_mm': 28, 'level': True,
                        'fstop': 4.0, 'focus': [11.0, 4.5, 1.6]}, exposure=3.0, haze=0.008, shutter=0.75, people='bar'),
    # p4 (p3 judged 4.5/5.0, converged: too bright and even; the pair darker than the walls; Mother's spot a white pool
    # and a haze shaft; the floor camouflage; coarse terrazzo; no life; a flat symmetric view with a cut board): seated
    # on the bench at 32 mm, a chair in the foreground; exposure 3.9; fill 0.03, trap 0.2; the pair 55 W at 24 deg;
    # Mother 80 W at 16 deg; haze 0.0008; end grain at block scale; a glass and a record
    # look 2 (the coordinator's converged list after round 3: the band amber not salmon, glass with real reflections,
    # real fittings and pools on the bar top, oak board by board, people, a view through the open porch): the room
    # reversed so the pair face the door; the lantern from the listeners' side; the porch view new
    'lantern': dict(camera={'position': [14.9, 2.75, 1.15], 'target': [19.1, 4.85, 1.05], 'lens_mm': 28, 'level': True,
                            'fstop': 2.8, 'focus': [P.STACKS[0][0], P.STACKS[0][1], 1.0]},
                    exposure=3.9, haze=0.0008, room={'interior': True}, shutter=1.0, people='lantern'),
    # test: from x 10.0 the open leaves of pair 1 filled half the frame; now from between them, at eye height
    'porch': dict(camera={'position': [11.25, 3.85, 1.45], 'target': [18.9, 4.30, 1.55], 'lens_mm': 24, 'level': True,
                          'fstop': 4.0, 'focus': [17.0, 4.6, 1.1]},
                  exposure=3.2, haze=0.006, shutter=1.0, people='porch'),
}


# people (the owner: blurred figures are allowed in bar pictures): r40's figures, faces always a smear
KIT40 = 'spinoffs/barkhorn/planet/r40/kit40.py'
CLOTH = ['#14171E', '#0E0D0C', '#22100E', '#181716', '#1A1B15', '#2A2018', '#161C26', '#121110', '#201813', '#1E1E1D']
SKIN = ['#9A7462', '#7E5640', '#5E3C2A', '#46301F', '#8A6650', '#A27E6A', '#6E4A36']
HAIR = ['#1A1410', '#3A2A1E', '#0E0C0A', '#6A5038', '#2A2420', '#8A7A6A', '#151210']
SIT = dict(move=[0.035, 0.025, 0.005], spin=5.0, head=[0.16, 0.09, 0.03, 30.0], arms=[0.14, 0.08, 0.06, 20.0])


def person(i, pose, at, heading, seat=0.46, **k):
    d = dict(pose=pose, at=[round(a, 3) for a in at], heading=heading, seat=seat, cloth=CLOTH[i % len(CLOTH)],
             skin=SKIN[(i * 3) % len(SKIN)], hair=HAIR[(i * 5) % len(HAIR)], seed=440 + i, **SIT)
    d.update(k)
    return d


ST = P.STOOLS
BAR_PEOPLE = [
    person(0, 'stool', [ST[0], P.STOOL_Y, 0], 90, 0.76),
    person(1, 'stool', [ST[1], P.STOOL_Y - 0.10, 0], 98, 0.76, head=[0.20, 0.10, 0.03, 35.0]),     # turned to talk
    person(2, 'stool', [ST[3], P.STOOL_Y, 0], 86, 0.76),
    person(3, 'pour', [9.10, 6.42, 0], -90, move=[0.10, 0.03, 0.0], spin=8.0, arms=[0.26, 0.10, 0.16, 35.0],
           head=[0.18, 0.08, 0.03, 30.0], cloth='#1A1918', sleeve='#2A2724'),                      # the bartender, mid-pour
    person(4, 'bench', [P.BANQ_TABLES[0], P.BANQ['y0'] + 0.40, 0], 90, P.BANQ['seat']),
    person(5, 'bench', [P.BANQ_TABLES[1] + 0.12, P.BANQ['y0'] + 0.40, 0], 90, P.BANQ['seat'], head=[0.20, 0.10, 0.03, 35.0]),
    person(6, 'chair', [P.BANQ_TABLES[1] + 0.05, P.ROUTE_Y[1] + P.BANQ_CHAIR_DY, 0], -90, 0.46),
    person(7, 'bench', [P.BANQ_TABLES[3] - 0.05, P.BANQ['y0'] + 0.40, 0], 90, P.BANQ['seat']),
]
SW = P.SWEET
LANT_PEOPLE = [   # listeners: still, so a slower drift than at the bar
    person(8, 'chair', [SW[0] - 0.10, SW[1] + 0.40, 0], 0.0, 0.40, move=[0.02, 0.015, 0.004], spin=3.0,
           head=[0.16, 0.09, 0.03, 30.0], arms=[0.06, 0.04, 0.03, 10.0], cloth='#1C2230', sleeve='#1C2230'),
    person(9, 'chair', [SW[0] - 0.95 - 0.10, P.INNER['y1'] - 0.70, 0], -12.0, 0.40, move=[0.02, 0.015, 0.004], spin=3.0,
           head=[0.16, 0.09, 0.03, 30.0], arms=[0.06, 0.04, 0.03, 10.0]),
    person(10, 'bench', [P.BENCH['x0'] + 0.30, P.INNER['y0'] + 0.62, 0], 8.0, P.BENCH['z'], move=[0.02, 0.015, 0.004],
           spin=3.0, head=[0.16, 0.09, 0.03, 30.0], arms=[0.06, 0.04, 0.03, 10.0]),
]
PEOPLE = {'bar': BAR_PEOPLE, 'lantern': LANT_PEOPLE, 'porch': LANT_PEOPLE[:2]}


def _face(x, y, tx, ty):
    """rotate_z for a Tropos at (x, y) to face (tx, ty): at 0 it faces -y, at -90 it faces -x."""
    return round(math.degrees(math.atan2(ty - y, tx - x)) + 90.0, 2)


def spot(pos, tgt, w, cone, k=2700, blend=0.6, radius=0.03):
    return {'type': 'spot', 'position': pos, 'target': tgt, 'power_w': w, 'cone_deg': cone, 'blend': blend,
            'radius_m': radius, 'color': k, 'camera': False}


def scene():
    S = P.SHOP_WALL
    props = [{'kind': 'kit', 'shape': 'ext', 'path': KIT, 'fn': 'house', 'windows_lit': 0.3, 'window_glow': 0.25,
              'glass_gloss': 0.3, 'band_glow': 0.3}]   # look 2 test: #FFB040 at 0.6 clipped to cream under AgX
    shelves = [0.30, 0.78, 1.26, 1.74, 2.22]
    # the Cores along the shop's shelves, in the eight tints, some unlit
    xs = [S['x0'] + 0.35 + 0.30 * i for i in range(8)]
    cores = [{'position': [x, W_ - 0.25, shelves[2]], 'flavour': f, 'rotate_z': 180.0} for x, f in zip(xs, FLAVOURS)]
    cores += [{'position': [x + 2.6, W_ - 0.25, shelves[1]], 'flavour': f, 'rotate_z': 180.0, **({'lamp': False} if i % 2 else {})}
              for i, (x, f) in enumerate(zip(xs, ['smoke', 'fog', 'ember', 'ice', 'acid', 'haze', 'dust', 'poison']))]
    cores += [{'position': [4.0, 4.85, P.SHOP_TABLE['h']], 'flavour': 'ice'}, {'position': [4.5, 5.10, P.SHOP_TABLE['h']], 'flavour': 'ember'}]
    cores += [{'position': [P.WINDOW_PLINTH['x0'] + 0.5, y, P.WINDOW_PLINTH['h']], 'flavour': f}
              for y, f in zip((3.6, 4.4, 5.2, 6.0), ('ember', 'smoke', 'fog', 'haze'))]
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'spots': cores, 'cable': False,
                  'cartridge': 'none', 'lamp_w': 0.10, 'lamp_k': 2700, 'shade_glow': 0.005, 'noshadow': 'shell|liner|skin',
                  'materials': {'liner': {'glow_color': '#FFA060'}}})
    by = (P.COUNTER['edge'] + P.COUNTER['y_work']) / 2
    domes = [{'position': [x, by, 2.05], 'flavour': 'smoke'} for x in (7.0, 8.4, 9.8)]
    domes += [{'position': [x, 5.0, 2.15], 'flavour': f} for x, f in ((4.0, 'haze'), (4.9, 'dust'))]
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'ceiling': H, 'lamp_w': 1.4,
                  'lamp_k': 2700, 'shade_glow': 0.006, 'noshadow': 'shell|liner|skin', 'spots': domes})
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'bowl', 'spots': [[3.75, 4.80, P.SHOP_TABLE['h']]],
                  'n': 30, 'bowl': 'brass', 'd': 200})
    # signs of life: rounds on the bar and the banquette tables
    props.append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/planet/r39/kit39.py', 'fn': 'life',
                  'rocks': [[9.37, by - 0.12, 1.07, 0.03, 1, '#B8641C'], [9.95, by - 0.08, 1.07, 0.02, 2, '#B8641C'],
                            [8.81, by - 0.05, 1.07, 0.025, 1, '#C8A060'], [10.30, by - 0.14, 1.07, 0.03, 2, '#B8641C'],
                            [4.1, 4.80, P.SHOP_TABLE['h'], 0.025, 1, '#B8641C'], [P.BENCH['x0'] + 0.25, I['y0'] + 1.6, P.BENCH['z'], 0.025, 1, '#B8641C'],
                            [P.BANQ_TABLES[1], P.BANQ['y1'] + 0.35, 0.75, 0.025, 1, '#B8641C']],
                  'coupes': [[8.40, by - 0.10, 1.07, 0.6, '#B8462A'], [P.BANQ_TABLES[2] + 0.1, P.BANQ['y1'] + 0.32, 0.75, 0.4, '#E8DDB8']],
                  'napkins': [[9.37, by - 0.12, 1.07, 8.0], [8.40, by - 0.10, 1.07, -12.0]],
                  'votives': [], 'matchbooks': [], 'coats': []})
    sweet = P.SWEET
    products = [
        {'def': CLOUD, 'flavour': 'cloud-red', 'instances': [
            {'position': [x, y, P.TROPOS['plinth']], 'rotate_z': _face(x, y, *sweet), 'hide': ['cloth-disc']} for (x, y) in P.STACKS]},
        {'def': MANTLE, 'flavour': 'smoke', 'instances': [{'position': [5.0, 4.80, P.SHOP_TABLE['h']], 'rotate_z': 90.0}]},
    ]
    zc = H - 0.05
    lights = {}
    for i, x in enumerate((1.4, 3.0, 4.6)):                           # the shop wall
        lights[f'shop{i}'] = spot([x, W_ - 1.4, zc], [x, W_ - 0.2, 1.4], 14.0, 30.0)
    lights['table'] = spot([4.3, 5.0, zc], [4.3, 5.0, 0.9], 8.0, 24.0)
    for i, x in enumerate(P.LOW_SEATS + P.STOOLS[::2]):                # the counter
        lights[f'ctr{i}'] = spot([x, P.COUNTER['y0'] + 0.25, zc], [x, P.COUNTER['y0'] + 0.05, 1.07], 38.0, 18.0, blend=0.3)
    for i, x in enumerate(P.BANQ_TABLES):                             # the banquette tables
        lights[f'bq{i}'] = spot([x, P.BANQ['y1'] + 0.40, zc], [x, P.BANQ['y1'] + 0.10, 0.95], 12.0, 24.0, blend=0.3)
    lights['route'] = {'type': 'area', 'position': [8.0, 0.72, H - 0.02], 'target': [8.0, 0.72, 0.0], 'size_m': [10.0, 0.1],
                       'irradiance': 0.1, 'color': 2700, 'camera': False}
    lights['fill'] = {'type': 'area', 'position': [7.0, W_ / 2, H - 0.3], 'target': [7.0, W_ / 2, 0.0], 'size_m': [10.0, 4.0],
                      'irradiance': 0.05, 'color': 2900, 'camera': False}
    # the lantern's face, grazed from the ceiling's edge so the slots read
    lights['baffle'] = {'type': 'area', 'position': [P.LANT['x0'] - 0.10, (P.LANT['y0'] + P.LANT['y1']) / 2, P.BAND['z0'] - 0.06],
                        'target': [P.LANT['x0'] - 0.02, (P.LANT['y0'] + P.LANT['y1']) / 2, 0.0], 'size_m': [0.05, 5.6],
                        'irradiance': 0.6, 'color': 2400, 'camera': False}
    # inside the lantern: the pair's spots, a hard spot through Mother EARF (its coloured shadow on the floor), the
    # trap's graze, a low fill
    zi = I['h'] - 0.05
    for i, (x, y) in enumerate(P.STACKS):
        lights[f'stack{i}'] = spot([x - 1.0, y + (0.5 if y < YC else -0.5), zi], [x, y, 1.1], 55.0, 24.0, k=2600)   # on the fronts
    M = P.MOTHER
    lights['mother'] = spot([M['x'] + 0.35, M['y'] + 0.45, zi], [M['x'] - 0.95, M['y'] - 0.30, 0.0], 80.0, 16.0, k=3000,   # her shadow toward the seats
                            blend=0.2, radius=0.01)
    lights['trap'] = {'type': 'area', 'position': [P.TRAP['x0'] - 0.25, YC, zi - 0.05], 'target': [P.TRAP['x0'], YC, 1.0],
                      'size_m': [0.15, 4.6], 'irradiance': 0.2, 'color': 2600, 'camera': False}
    lights['infill'] = {'type': 'area', 'position': [(I['x0'] + I['x1']) / 2, YC, zi - 0.1], 'target': [(I['x0'] + I['x1']) / 2, YC, 0.0],
                        'size_m': [5.0, 3.5], 'irradiance': 0.03, 'color': 2700, 'camera': False}
    lights['street'] = {'type': 'area', 'position': [-2.4, 1.0, 6.0], 'target': [-1.5, 3.0, 0.0], 'size_m': [0.6, 0.6],
                        'irradiance': 0.6, 'color': 2200, 'spread_deg': 80.0}
    return props, products, lights


W_ = P.W


def shot(view):
    s = copy.deepcopy(json.load(open(BASE)))
    v = VIEWS[view]
    props, products, lights = scene()
    s['title'] = f'Planet EARF, round 44: the lantern, {view}'
    s['camera'] = v['camera']
    if v.get('people'):
        props.append({'kind': 'kit', 'shape': 'ext', 'path': KIT40, 'fn': 'figures', 'people': PEOPLE[v['people']],
                      'shutter': v.get('shutter', 1.0)})
    s['set'] = {'kind': 'stage', 'props': props}
    s['products'] = products
    s['lights'] = lights
    s['haze']['density'] = v.get('haze', 0.002)
    s['haze']['box_m'] = [0.05, 0.05, 0.01, P.L - 0.05, P.W - 0.05, H - 0.05]
    s['render']['exposure'] = v.get('exposure', 3.6)
    s['render']['white_balance_k'] = 3200; s['render']['white_balance_tint'] = -1.5     # (p2: the oak read mauve; p3: 2800 K
    # turned the amber band pink)
    s['render']['caustics_refractive'] = True                       # light through the tinted discs and fins
    s['render'].update(v.get('render', {}))
    if v.get('room'):
        props[0].update(v['room'])
    for pre, kv in v.get('lights', {}).items():
        for name, L_ in s['lights'].items():
            if name.startswith(pre):
                L_.update(kv)
    return s


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(VIEWS):
        p = os.path.join(OUT, f'{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write([a for a in sys.argv[1:] if not a.startswith('--')] or None)
