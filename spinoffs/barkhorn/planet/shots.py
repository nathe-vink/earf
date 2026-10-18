"""Planet EARF's shots (round 32): one room, one model, every view.

    python3 spinoffs/barkhorn/planet/shots.py            # writes studio/shots/barkhorn/planet32/*.json
    python3 studio/engine/render.py studio/shots/barkhorn/planet32/door.json --out IMG [--samples N --scale S]

The room is the kit piece `planet_room` (studio/engine/kit_ext/planet_room.py), built from plan.py; the products come
from their own CAD: the Atmosphere speakers (barkhorn-cloud), Cumulus (barkhorn-turntable) and Bell (barkhorn-lamp).
The light is the room's own: the membrane, the bar's panels, the shelves, the slats, Bell, and the few concealed
downlights a lighting designer would add (on each corner pair, the bar top, the DJ desk); outside, the street lamps.
`VIEWS` holds each view's camera and its own settings; `DEFAULT` the room's.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import plan as P                                                    # noqa: E402

OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet32')
CLOUD = 'studio/products/barkhorn-cloud.json'
TT = 'studio/products/barkhorn-turntable.json'
LAMP = 'studio/products/barkhorn-lamp.json'
LAMP_STRIP_Z = 0.441             # Bell's strip above its foot (companions/shots.py)
PENDANT_Z = P.BAR_TOP_Z + P.TOP_T + 0.78 - 0.279      # a pendant's origin: its shade's rim 0.78 m over the bar top
SIDE_H = 0.432                   # the lounge's side tables' tops (planet_room.lounge: 12 + 420)
PENDANT_HIDE = ['foot-lower-stack', 'cover', 'stem', 'knob', 'dimmer', 'bumpons', 'cord']

DEFAULT = dict(
    # round 1's critics (critic/*-r1.json): the ceiling and the shelves outshone the bar and the products; no air.
    # round 2's (critic/*-r2.json): the room too dark and red; the ceiling still the largest bright field; the record
    # wall's spots three arches; the glasses unlit; the spectrum uneven
    # round 3's (listening-r1, door-r3): the membrane still the brightest field at any glow the eye can see it by, so
    # it is held to a glimmer in the views (the clock's own frames bring it up), at the warm 'sunset' hour, not magenta
    clock='sunset', membrane=0.004, membrane_white=0.45, dj_glow=0.008, dj_color='#F2D6B0', panel_glow=0.9, panel_foot=0.35,
    shelf_glow=0.15, backpanel_glow=0.04, niche_glow=0.03, slat_glow=0.2, slat_led=3.0, record_glow=0.0, neon=18.0,
    windows_lit=0.35, street=True, spk_irr=12.0, wash=90.0, spot_fog=320.0, spot_bar=140.0, spot_dj=70.0,
    spot_records=60.0, bell_w=60.0, pendant_w=25.0, street_lamp=600.0, haze=0.008,
    exposure=0.3, wb=3300, wb_tint=-10.0,         # round 5: 3000 K at -25 overshot to green and bright; between the two
    view='Khronos PBR Neutral', look='None', samples=256,
)


def room_piece(v):
    keys = ('clock', 'membrane', 'panel_glow', 'shelf_glow', 'backpanel_glow', 'niche_glow', 'slat_glow', 'slat_led',
            'record_glow', 'neon', 'windows_lit', 'street', 'floor_tex', 'floor_tint', 'floor_tint_mix', 'floor_coat',
            'wall', 'booth_color', 'absorber', 'rug_tex', 'rug_tint', 'membrane_white', 'last_dim', 'flat_glow',
            'across_glow', 'backpanel_color', 'dj_glow', 'facade', 'dj_color', 'membrane_tint', 'road_rough',
            'panel_foot', 'props', 'glasses_x')
    return {'kind': 'kit', 'shape': 'ext', 'module': 'planet_room', 'fn': 'room', **{k: v[k] for k in keys if k in v}}


def props(v):
    out = [room_piece(v)]
    for i, (x, y) in enumerate(P.stools()):                           # the bar stools (Poly Haven, CC0)
        out.append({'kind': 'kit', 'shape': 'asset', 'model': 'bar_chair_round_01', 'res': '1k',
                    'position': [round(x, 3), round(y, 3), 0.0], 'rotate': [0, 0, (i * 37) % 23 - 11]})
    for x, y, f in P.CHAIRS:                                          # the lounge's low chairs
        # re-dyed darker (round 4: the tan leather matched the Ember pair's hue and value), each a few degrees off
        out.append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/room31/pieces.py', 'fn': 'recolour',
                    'model': 'mid_century_lounge_chair', 'res': '1k', 'match': ['mid_century'], 'blend': 'MULTIPLY',
                    'color': v.get('chair_dye', '#5E504A'), 'mix': 1.0, 'position': [x, y, 0.012],
                    'rotate': [0, 0, v.get('chair_rot0', -90.0) + f + ((int(x * 10) * 7 + int(y * 10) * 3) % 9 - 4)]})
    if v['street']:                                                   # the street lamps along the curb (CC0)
        for x in STREET_LAMPS:
            out.append({'kind': 'kit', 'shape': 'asset', 'model': 'street_lamp_01', 'res': '1k', 'position': [x, -3.7, 0.0],
                        'rotate': [0, 0, v.get('lamp_rot', 0.0)]})
    # the pendants' cords, from each shade's cap up to the membrane
    for x in P.bar_pendants():
        y = P.BAR_FRONT + 0.20
        out.append({'kind': 'kit', 'shape': 'thread', 'a': [x, y, PENDANT_Z + 0.478], 'b': [x, y, P.MEMBRANE],
                    'radius': 0.0025, 'material': 'gloss', 'color': '#1A1A1A'})
    return out


def products(v):
    spk = []
    for role, colour, x, y, z, rot in P.speakers():
        spk.append({'flavour': P.FLAVOUR[colour], 'position': [round(x, 4), round(y, 4), z], 'rotate_z': rot,
                    'hide': ['cloth-disc']})
    lamps = [{'flavour': 'fog', 'position': [round(x, 4), round(P.BAR_FRONT + 0.20, 4), round(PENDANT_Z, 4)],
              'rotate_z': 0.0, 'hide': PENDANT_HIDE} for x in P.bar_pendants()]
    for x0 in P.BOOTHS:                                              # one Bell on each booth's table, by the window
        cx = x0 + P.BOOTH_LEN / 2; cy = 0.15 + 0.22
        lamps.append({'flavour': 'ember', 'position': [round(cx, 4), round(cy, 4), P.TABLE['h']], 'rotate_z': 0.0})
    for x, y in P.SIDE_TABLES:                                       # and one on each of the lounge's side tables
        lamps.append({'flavour': 'ember', 'position': [x, y, SIDE_H], 'rotate_z': 0.0})
    dj = P.DJ
    tt = [{'flavour': 'ice', 'position': [round(P.L - 0.40, 4), round(P.D / 2 - 0.15, 4), dj['desk_z']], 'rotate_z': -90.0}]
    return [{'def': CLOUD, 'flavour': spk[0]['flavour'], 'instances': spk},
            {'def': LAMP, 'flavour': 'fog', 'instances': lamps},
            {'def': TT, 'flavour': 'ice', 'instances': tt}]


def lights(v):
    L = {}
    # a narrow warm downlight from the membrane onto each corner pair (the speakers are the room's sculpture)
    for k, (role, colour, x, y, z, rot) in enumerate(P.speakers()):
        if role == 'backbar':
            continue
        fx, fy = math.sin(math.radians(rot)), -math.cos(math.radians(rot))      # the speaker's front
        # a broad soft lamp (round 4: a narrow spot overshot onto the wall behind and left the cabinet dark)
        L[f'spk{k}'] = {'type': 'area', 'position': [round(x + 1.6 * fx, 3), round(y + 1.6 * fy, 3), P.MEMBRANE - 0.05],
                        'target': [x, y, 0.70], 'size_m': [0.7, 0.7], 'irradiance': v['spk_irr'], 'color': 3000}
        # the wash: a floor uplight in the corner behind, grazing both walls in the pair's complementary colour
        cx = P.LOUNGE_X0 + 0.25 if role == 'front' else P.L - 0.15
        cy = 0.15 if y < P.D / 2 else P.D - 0.15
        if v.get('wash', 0) > 0:
            L[f'wash{k}'] = {'type': 'spot', 'position': [round(x - 0.25 * fx, 3), round(y - 0.25 * fy, 3), 0.18],
                             'target': [cx, cy, 1.2], 'power_w': v['wash'], 'cone_deg': 50, 'blend': 0.9, 'radius_m': 0.05,
                             'color': P.COLOURS[P.WASH[role]]}
    # a pinhole in each Fog niche's head, onto the speaker
    for k, (role, colour, x, y, z, rot) in enumerate(P.speakers()):
        if role == 'backbar':
            L[f'fog{k}'] = {'type': 'spot', 'position': [x, y - 0.12, P.NICHE_Z0 + P.NICHE_H - 0.03], 'target': [x, y - 0.25, z + 0.6],
                            'power_w': v['spot_fog'], 'cone_deg': 30, 'blend': 0.7, 'radius_m': 0.02, 'color': 3000}
    # pinholes onto the bar top, between the pendants
    for i, x in enumerate(P.bar_pendants()[:-1]):
        L[f'bar{i}'] = {'type': 'spot', 'position': [x + 0.7, P.BAR_FRONT + 0.05, P.MEMBRANE - 0.02],
                        'target': [x + 0.7, P.BAR_FRONT + 0.1, P.BAR_TOP_Z], 'power_w': v['spot_bar'], 'cone_deg': 30,
                        'blend': 0.7, 'radius_m': 0.02, 'color': 2900}
    # the DJ desk's own light
    L['dj'] = {'type': 'spot', 'position': [P.L - 0.42, P.D / 2 - 0.15, P.DJ['recess_z'] - 0.03],
               'target': [P.L - 0.40, P.D / 2 - 0.15, P.DJ['desk_z']], 'power_w': v['spot_dj'], 'cone_deg': 35, 'blend': 0.8, 'radius_m': 0.05, 'color': 3000}
    if v.get('spot_records', 0) > 0:                                 # a wash down the record wall
        for k, yy in enumerate((2.6, 4.57, 6.5)):
            L[f'rec{k}'] = {'type': 'spot', 'position': [P.L - 2.4, yy, P.MEMBRANE - 0.02], 'target': [P.L - 0.4, yy, 0.9],
                            'power_w': v['spot_records'], 'cone_deg': 45, 'blend': 1.0, 'radius_m': 0.04, 'color': 3200}
    # Bell: three small lamps just outside each lamp's opal sleeve (companions/shots.py's bell_lights)
    def bell(lx, ly, h, watts, tag):
        for k in range(3):
            a = math.radians(90 + 120 * k)
            L[f'{tag}{k}'] = {'type': 'point', 'position': [round(lx + 0.047 * math.cos(a), 4), round(ly + 0.047 * math.sin(a), 4),
                                                             round(h + LAMP_STRIP_Z, 4)],
                              'power_w': watts / 3, 'radius_m': 0.04, 'color': 2700, 'camera': False,
                              'transmission': False, 'specular': 0.0}
    for i, x in enumerate(P.bar_pendants()):
        bell(x, P.BAR_FRONT + 0.20, PENDANT_Z, v['pendant_w'], f'pend{i}-')
    for i, (x, y) in enumerate(P.SIDE_TABLES):
        bell(x, y, SIDE_H, v['bell_w'], f'side{i}-')
    for i, x0 in enumerate(P.BOOTHS):
        bell(x0 + P.BOOTH_LEN / 2, 0.37, P.TABLE['h'], v['bell_w'], f'booth{i}-')
    # the street lamps (outside, along the curb), 3000 K LED
    if v['street']:
        for k, x in enumerate(STREET_LAMPS):
            L[f'street{k}'] = {'type': 'point', 'position': [x, -3.7 + v.get('lamp_dy', 0.0), v.get('lamp_z', 3.30)], 'power_w': v['street_lamp'], 'radius_m': 0.15,
                               'color': 2700}
    return L


def shot(view):
    vw = VIEWS[view]
    v = {**DEFAULT, **vw.get('settings', {})}
    s = {
        'title': f'Planet EARF, {vw["title"]} (round 32)',
        'size': vw.get('size', [2400, 1600]),
        'camera': vw['camera'],
        'products': products(v),
        'set': {'kind': 'stage', 'props': props(v)},
        'sky': {'kind': 'gradient', 'zenith': '#05070C', 'horizon': '#141824', 'ground': '#08080A', 'strength': v.get('sky', 1.0)},
        'lights': lights(v),
        'materials': {'led': {'strength': v.get('led', 22.0)}},
        'haze': {'box_m': [0.02, 0.02, 0.01, P.L - 0.02, P.D - 0.02, P.MEMBRANE - 0.06], 'density': v['haze'], 'anisotropy': 0.3,
                 'color': '#FFFFFF'} if v['haze'] > 0 and view != 'street' else {},
        'render': {'samples': v['samples'], 'adaptive': 0.02, 'denoise': True, 'clamp': 10, 'bounces': 10,
                   'view': v['view'], 'look': v['look'], 'exposure': v['exposure'], 'white_balance_k': v['wb'], 'white_balance_tint': v['wb_tint']},
    }
    return s


EYE = 1.60
STREET_LAMPS = (-7.0, 6.5, 20.0)
VIEWS = {
    'door': {'title': 'the whole room at night, from the door',
             'camera': {'position': [2.20, 3.60, 1.35], 'target': [P.L, 4.7, 1.25], 'lens_mm': 30, 'level': True},
             'settings': {'panel_glow': 0.6}},
    'bar': {'title': 'the bar front lit, at eye level',
            'camera': {'position': [1.60, 4.60, 1.05], 'target': [7.0, 8.4, 0.75], 'lens_mm': 35, 'level': True}},
    'listening': {'title': 'the listening corner, a pair either side of the lounge',
                  # turned round after round 2 (the chairs' backs hid the Ice pair): from the DJ's side of the lounge,
                  # the Ember pair either side of it, the chairs facing the camera, the bar glowing beyond
                  # concept changed after three passes at 4.5 (the pair at the frame's edges, behind chairs, from any
                  # square view): three-quarter, one Ice speaker the hero on the left third, the record wall beyond
                  'camera': {'position': [14.75, 1.85, 1.20], 'target': [17.7, 1.45, 0.92], 'lens_mm': 32, 'level': True,
                             'fstop': 4.0, 'focus': [17.57, 0.78, 0.9]}},
    'backbar': {'title': 'the back-bar, the Fog pair among the lit shelves',
                'camera': {'position': [4.20, 6.20, 1.70], 'target': [3.42, 8.9, 1.2], 'lens_mm': 35, 'level': True,
                           'fstop': 2.8, 'focus': [3.42, 8.72, 1.65]}},
    'records': {'title': 'the record wall and the DJ desk with Cumulus',
                'camera': {'position': [16.5, 3.9, 1.30], 'target': [17.89, 4.42, 1.0], 'lens_mm': 45, 'level': True,
                           'fstop': 4.0, 'focus': [17.89, 4.42, 1.0]}},
    'street': {'title': 'the street at night, through the window',
               'camera': {'position': [-6.5, -10.0, 1.5], 'target': [3.0, 0.5, 1.9], 'lens_mm': 32, 'level': True},
               'settings': {'sky': 0.25}},
}

# the colour clock: the door's view at four hours, the membrane the only change (its glow a little up, so it reads)
for hour, label in (('opening', '17:00'), ('sunset', '19:30'), ('late', '22:30'), ('last', '01:45')):
    VIEWS[f'clock-{hour}'] = {'title': f'the colour clock at {label}', 'size': [1800, 1200],
                              'camera': dict(VIEWS['door']['camera']),
                              'settings': {'clock': hour, 'membrane': 0.08}}


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or VIEWS:
        p = os.path.join(OUT, f'{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write(sys.argv[1:] or None)
