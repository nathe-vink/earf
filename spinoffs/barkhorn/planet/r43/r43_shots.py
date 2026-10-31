"""Planet EARF, round 43: the pop-up itself (drawing A-401), rendered. The coordinator, 31 October 2026: "make the debut
room real ... 2-3 views of the pop-up itself at A-401".

    python3 spinoffs/barkhorn/planet/r43/r43_shots.py [VIEW ...]     # writes studio/shots/barkhorn/planet43/VIEW.json

The room is `kit43.popup` (popup42's geometry); the look (AgX, the finish, the grain) is round 42's shop view, so the
pop-up and the flagship read as one house. Views: `shop` (from inside the door, the whole room to the drapes),
`window` (from the sidewalk at night, the Ember pair in the glass), `listening` (behind the felt, the Smoke pair).
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r42'))
import popup42 as Q                                                  # noqa: E402

BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet42', 'shop.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet43')
KIT43 = 'spinoffs/barkhorn/planet/r43/kit43.py'
CLOUD = 'studio/products/barkhorn-cloud.json'
MANTLE = 'spinoffs/barkhorn/companions/out-concepts2/r3.json'
FLAVOURS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
SHELF = [0.30, 0.78, 1.26, 1.70, 2.12]
H = Q.CEIL

VIEWS = {
    # p0 look (seen before any critic): the table filled the foreground and the right wall's shelves read empty, so
    # the camera moved to the left of the door, looking across the room to the right wall, the bar and the drapes
    # p2 (p1 judged 4.5/4.5, converged: the bare foreground floor the brightest thing, lit by the window pair's spill;
    # the Tropos small, dim and unlit; the felt a flat black wall; no sign of life; 24 mm cavernous): closer at 35 mm,
    # the table leading to the Tropos, which gets its own spot and a rim; the window spill and street down; props
    # (31 Oct, the coordinator: only one Tropos pair will exist, so the pop-up shows one pair, in Ember, which stands
    # in the window and moves to the listening room for sessions; the shop's single Tropos and its plinth are gone.)
    # So the shop is seen from the bar end toward the street: both walls of shelves, the table, the pair in the window
    # against the street, at 28 mm
    'shop': dict(camera={'position': [6.0, 2.6, 1.25], 'target': [0.7, 2.9, 0.95], 'lens_mm': 40, 'level': True,
                         'fstop': 2.8, 'focus': [0.7, 2.9, 0.95]}, exposure=4.4, haze=0.004, pair='window',
                 # p3, the last round (p2 judged 4.5/4.5, converged: the floor the brightest thing (109) and read as
                 # planks; the window a black mirror with a grey slab in it (the room's fill reflected); the pair dark
                 # (24) and small; a pale table; the shelf strips hard lines; empty): seated at 40 mm on the pair; its
                 # spots 90 W at 20 deg; the fill off; the floor darker with the scan's pattern blended down; the street
                 # lit; a walnut table; the shelf strips 3 to 1; the wall spots down and tighter; haze 0.004
                 lights={'win': {'power_w': 90.0, 'cone_deg': 20.0}, 'street': {'irradiance': 0.5}, 'fill': {'irradiance': 0.0},
                         'tr': {'power_w': 22.0, 'cone_deg': 24.0}, 'tl': {'power_w': 18.0, 'cone_deg': 24.0},
                         'table': {'power_w': 10.0, 'cone_deg': 22.0}},
                 room={'windows_lit': 0.3, 'window_glow': 0.25, 'glass_gloss': 0.35, 'led': 1.0,
                       'floor_tint': '#36322E', 'floor_mix': 0.92}),
    # p0 look: the opposite building's windows and lit shop mirrored in the glass as white squares and a blue band, the
    # sidewalk hot, a mullion down the middle: the facade dimmed, the glass a softer reflector, one pane, the street lamp down
    # p2 (p1 judged 4.5/4.0, converged: a hard blue rectangle on the glass, which was the placeholder shop opposite
    # reflected; the pavement the brightest thing (172); the pair underlit (19); the back crushed; the shelves bare; too
    # far back): the shop opposite gone, the pavement dark and the street lamp down, the room's fill back, the pair's
    # spots 26 to 60 W at 26 deg, sleeves face out on the upper shelves, haze, closer at 40 mm
    # p3, the last round (p2 judged 5.0/4.5, converged: the pair darker (25) than the floor (90-123) and the plaster (160);
    # no reflections, so the glass reads as an open stage; the sill a crushed bar; tinted sleeves and shades compete):
    # the pair's spots 60 to 150 W at 22 deg, the fill 0.2 to 0.05, exposure 4.0 to 3.6, darker plaster; warm lit windows
    # opposite and the street lamp up so the pane carries faint reflections and the sill an edge; sleeves in greys;
    # the Hemispheres' glow halved; haze 0.006; white balance 2700 K, tint +1 (the pink cast)
    'window': dict(camera={'position': [-3.8, 2.3, 1.35], 'target': [2.4, 3.3, 1.2], 'lens_mm': 40, 'level': True,
                           'fstop': 5.6, 'focus': [0.7, 2.9, 1.0]}, exposure=3.6, haze=0.006,
                   room={'windows_lit': 0.3, 'window_glow': 0.25, 'opp_shop_glow': 0.0, 'glass_gloss': 0.6},
                   lights={'street': {'irradiance': 0.5}, 'fill': {'irradiance': 0.05}, 'win': {'power_w': 150.0, 'cone_deg': 22.0}},
                   pair='window'),
    # p0 look: too dark, the left stack out of frame: the camera back by the drape's opening, both stacks in; the
    # stacks' spots, the seats' light and the exposure up
    # p2 (p1 judged 4.5/4.5, converged: a pink cast; the rug the brightest thing (118); the pair darker (27) with the
    # plinth tops hot; the plaster flat and bright; the felt washed from the top; 20 mm stretch and a chair back across
    # the corner; no practical, no life): 2700 K, tint +1; a plain dark wool rug; the pair's spots 110 W at 24 deg aimed at
    # the cabinets; the seats' light 2 W; the fill 0.05; the felt washed up from the floor behind the plinths; a lit Core
    # on the decks table; haze; 24 mm from behind the back row
    # (p2a, seen before judging: at 24 mm both stacks fell off the frame's edges, median 18: 22 mm on the room's axis,
    # exposure 4.2; the room is symmetric, so the frame is)
    'listening': dict(camera={'position': [9.8, 3.81, 1.2], 'target': [12.8, 3.81, 1.05], 'lens_mm': 22, 'level': True,
                              'fstop': 4.0, 'focus': [12.6, 3.6, 0.9]}, exposure=4.2, haze=0.0015,
                      # p1 proof, seen before judging: overexposed (median 111, the seats and rug blown): exposure 5.0 to
                      # 3.6, the seats' light and the back felt's wash halved
                      lights={'stack': {'power_w': 110.0, 'cone_deg': 24.0}, 'seats': {'power_w': 2.0},
                              'fill': {'irradiance': 0.05},
                              'drape': {'position': [13.15, Q.W / 2, 0.25], 'target': [13.35, Q.W / 2, 1.3], 'irradiance': 0.5}},
                      pair='listening'),
}


def _face(x, y, tx, ty):
    """rotate_z for a Tropos at (x, y) to face (tx, ty): at 0 it faces -y, at -90 it faces -x."""
    return round(math.degrees(math.atan2(ty - y, tx - x)) + 90.0, 2)


def spot(pos, tgt, w, cone, k=2700, blend=0.7):
    return {'type': 'spot', 'position': pos, 'target': tgt, 'power_w': w, 'cone_deg': cone, 'blend': blend,
            'radius_m': 0.03, 'color': k, 'camera': False}


def scene(pair='window'):
    W = Q.W
    zc = H - 0.25                                                     # the track's spots
    cards = [(x, SHELF[k], 'right') for x in (1.3, 2.5, 3.7, 4.9) for k in (1, 2)] + \
            [(x, SHELF[2], 'left') for x in (2.0, 3.4, 4.8)]
    props = [{'kind': 'kit', 'shape': 'ext', 'path': KIT43, 'fn': 'popup', 'cards': cards, 'led': 3.0,
              'felt': '#26272A', 'ceiling': '#2E2C2A', 'plaster': '#A39B8F', 'floor_tint': '#4E4943', 'floor_coat': 0.45, 'shop_plinth': False,
              'faceout_r': [(2.20, SHELF[1]), (2.60, SHELF[1]), (3.00, SHELF[1]), (4.30, SHELF[2]), (4.70, SHELF[2]),
                            (2.05, SHELF[3]), (5.20, SHELF[3]), (1.10, SHELF[4]), (1.80, SHELF[4]), (3.40, SHELF[4])],
              'faceout_l': [(1.60, SHELF[2]), (2.40, SHELF[2]), (3.80, SHELF[2]), (4.60, SHELF[2]),
                            (1.90, SHELF[3]), (3.10, SHELF[3]), (4.30, SHELF[3])]}]
    # signs of life (p1's critics): a round on the bar, a glass on two ledges
    by = (Q.BAR['y0'] + Q.BAR['y1']) / 2
    props.append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/planet/r39/kit39.py', 'fn': 'life',
                  'rocks': [[7.30, by - 0.10, 1.07, 0.03, 1, '#B8641C'], [8.45, by + 0.05, 1.07, 0.02, 2, '#B8641C'],
                            [Q.STAND[0][0] - 0.12, Q.STAND[0][1] + 0.10, 1.065, 0.025, 1, '#B8641C']],
                  'coupes': [[7.85, by - 0.05, 1.07, 0.6, '#B8462A'], [Q.STAND[2][0] - 0.10, Q.STAND[2][1] + 0.08, 1.065, 0.4, '#E8DDB8']],
                  'napkins': [[7.30, by - 0.10, 1.07, 8.0], [7.85, by - 0.05, 1.07, -12.0]],
                  'votives': [], 'matchbooks': [[8.1, by + 0.1, 1.07, 20.0]], 'coats': []})
    # the Cores: eight tints on the right wall's shelves, grouped, two unlit; two on the shop table; the Smoke ones on
    # the standing ledges
    # p0 look: the shelves read empty, so the line runs along them: all eight tints on the third shelf in two groups,
    # a second set (lit and unlit) on the second and fourth
    xs = [(1.00, 2), (1.25, 2), (1.50, 2), (1.75, 2), (2.85, 2), (3.10, 2), (3.35, 2), (3.60, 2)]
    cores = [{'position': [x, 0.20, SHELF[k]], 'flavour': f, 'rotate_z': 0.0} for (x, k), f in zip(xs, FLAVOURS)]
    cores += [{'position': [x, 0.20, SHELF[k]], 'flavour': f, 'rotate_z': 0.0, **({'lamp': False} if i % 2 else {})}
              for i, ((x, k), f) in enumerate(zip([(4.40, 1), (4.65, 1), (4.90, 1), (1.20, 3), (1.45, 3), (2.95, 3), (3.20, 3), (4.70, 3)],
                                                  ['smoke', 'fog', 'ember', 'ice', 'acid', 'haze', 'dust', 'poison']))]
    cores += [{'position': [3.05, 3.55, 0.90], 'flavour': 'ice'}, {'position': [3.35, 3.95, 0.90], 'flavour': 'ember'}]
    cores += [{'position': [x + 0.08, y - 0.05, 1.065], 'flavour': 'smoke'} for (x, y) in Q.STAND]
    cores += [{'position': [10.55, Q.DECKS['y0'] + 0.12, 0.86], 'flavour': 'ember'}]       # on the decks table
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'spots': cores, 'cable': False,
                  'cartridge': 'none', 'lamp_w': 0.20, 'lamp_k': 2700, 'shade_glow': 0.005, 'noshadow': 'shell|liner|skin',
                  'materials': {'liner': {'glow_color': '#FFA060'}}})
    # the Hemispheres: three in tints low over the left wall, two over the shop table, two over the bar in Smoke
    domes = [{'position': [x, y, 2.15], 'flavour': f} for (x, y), f in zip(Q.HEMI, ['ember', 'ice', 'acid'])]
    domes += [{'position': [3.1, 3.75, 2.05], 'flavour': 'haze'}, {'position': [4.1, 3.75, 2.05], 'flavour': 'dust'}]
    domes += [{'position': [7.5, (Q.BAR['y0'] + Q.BAR['y1']) / 2, 2.0], 'flavour': 'smoke'},
              {'position': [8.5, (Q.BAR['y0'] + Q.BAR['y1']) / 2, 2.0], 'flavour': 'smoke'}]
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'ceiling': H, 'lamp_w': 4.0,
                  'lamp_k': 2700, 'shade_glow': 0.006, 'noshadow': 'shell|liner|skin', 'spots': domes})
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'fan', 'spots': [[4.15, 3.55, 0.90]],
                  'flavours': ['ember', 'ice', 'acid', 'fog', 'poison'], 'heading': 20.0})
    props.append({'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'bowl', 'spots': [[2.90, 3.95, 0.90]],
                  'n': 30, 'bowl': 'brass', 'd': 200})
    Pw = Q.WINDOW_PLINTH
    sweet = (10.4, W / 2)
    products = [
        {'def': CLOUD, 'flavour': 'cloud-red', 'instances': [
            {'position': [Pw['x'], Pw['y'] + dy, Pw['h']], 'rotate_z': -90.0 + t, 'hide': ['cloth-disc']}
            for dy, t in ((-0.48, 6.0), (0.48, -6.0))] if pair == 'window' else [
            {'position': [x, y, 0.40], 'rotate_z': _face(x, y, *sweet), 'hide': ['cloth-disc']} for (x, y) in Q.STACKS]},
        {'def': MANTLE, 'flavour': 'smoke', 'instances': [{'position': [1.85, 0.21, SHELF[1]], 'rotate_z': 180.0},
                                                          {'position': [4.15, 3.95, 0.90], 'rotate_z': 90.0},
                                                          {'position': [10.30, Q.DECKS['y0'] + 0.35, 0.86], 'rotate_z': 90.0}]},
    ]
    lights = {}
    for i, x in enumerate((1.6, 3.4, 5.2)):                          # the right wall's shelves
        lights[f'tr{i}'] = spot([x, 1.30, zc], [x, 0.20, 1.20], 40.0, 34.0)
    for i, x in enumerate((2.2, 3.5, 4.8)):                          # the left wall
        lights[f'tl{i}'] = spot([x, W - 1.30, zc], [x, W - 0.20, 1.30], 32.0, 34.0)
    for i, dy in enumerate((-0.48, 0.48)):                           # the window pair, grazed from the glass side
        lights[f'win{i}'] = spot([0.20, Pw['y'] + dy, 3.30], [0.80, Pw['y'] + dy, 0.95], 26.0, 20.0, k=2600)
    lights['table'] = spot([3.6, 3.75, zc], [3.6, 3.75, 0.9], 8.0, 30.0)
    lights['bar'] = spot([8.0, W - 1.2, zc], [8.0, W - 1.7, 1.07], 16.0, 30.0)
    for i, (x, y) in enumerate(Q.STACKS):                            # the listening pair
        lights[f'stack{i}'] = spot([11.6, y + (0.4 if y < W / 2 else -0.4), zc], [x, y, 1.15], 34.0, 18.0, k=2600)
    lights['seats'] = spot([10.9, W / 2, zc], [10.8, W / 2, 0.4], 10.0, 60.0, k=2600, blend=1.0)
    lights['drape'] = {'type': 'area', 'position': [12.9, W / 2 + 0.6, H - 0.35], 'target': [13.3, W / 2 + 0.6, 1.2],
                       'size_m': [0.3, 4.6], 'irradiance': 1.6, 'color': 2600, 'camera': False}
    # a wash grazing the front drapes from above (p1: "a flat black wall"), on the shop side
    lights['frontfelt'] = {'type': 'area', 'position': [9.25, W / 2 + 0.8, H - 0.30], 'target': [9.70, W / 2 + 0.8, 1.0],
                           'size_m': [0.3, 5.0], 'irradiance': 1.4, 'color': 2600, 'camera': False}
    lights['fill'] = {'type': 'area', 'position': [5.0, W / 2, H - 0.3], 'target': [5.0, W / 2, 0.0], 'size_m': [6.0, 4.0],
                      'irradiance': 0.12, 'color': 2900, 'camera': False}
    lights['street'] = {'type': 'area', 'position': [-2.4, 1.0, 6.0], 'target': [-1.5, 3.0, 0.0], 'size_m': [0.6, 0.6],
                        'irradiance': 1.5, 'color': 2200, 'spread_deg': 80.0}
    return props, products, lights


def shot(view):
    s = copy.deepcopy(json.load(open(BASE)))
    v = VIEWS[view]
    props, products, lights = scene(v.get('pair', 'window'))
    s['title'] = f'Planet EARF, round 43: the pop-up, {view}'
    s['camera'] = v['camera']
    s['set'] = {'kind': 'stage', 'props': props}
    s['products'] = products
    s['lights'] = lights
    s['haze']['density'] = v.get('haze', 0.0006)
    s['haze']['box_m'] = [0.05, 0.05, 0.01, Q.L - 0.05, Q.W - 0.05, H - 0.05]
    s['render']['exposure'] = v.get('exposure', 3.4)
    s['render']['white_balance_k'] = 2700; s['render']['white_balance_tint'] = 1.0   # (round 43 critics: a pink cast)
    s['render'].update(v.get('render', {}))
    if v.get('room'):
        props[0].update(v['room'])
    for pre, kv in v.get('lights', {}).items():
        for name, L in s['lights'].items():
            if name.startswith(pre):
                L.update(kv)
    return s


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(VIEWS):
        p = os.path.join(OUT, f'{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write([a for a in sys.argv[1:] if not a.startswith('--')] or None)
