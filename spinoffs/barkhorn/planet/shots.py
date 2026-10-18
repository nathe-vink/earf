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
PENDANT_HIDE = ['foot-lower-stack', 'cover', 'stem', 'knob', 'dimmer', 'bumpons', 'cord']

DEFAULT = dict(
    clock='late', membrane=0.30, panel_glow=1.1, shelf_glow=0.9, backpanel_glow=0.18, niche_glow=0.12, slat_glow=0.25,
    slat_led=10.0, record_glow=4.0, neon=18.0, windows_lit=0.35, street=True,
    spot_speaker=160.0, spot_fog=40.0, spot_bar=18.0, spot_dj=25.0, spot_records=0.0, bell_w=12.0, pendant_w=10.0, street_lamp=900.0,
    exposure=0.0, wb=4300, view='AgX', look='None', samples=256,
)


def room_piece(v):
    keys = ('clock', 'membrane', 'panel_glow', 'shelf_glow', 'backpanel_glow', 'niche_glow', 'slat_glow', 'slat_led',
            'record_glow', 'neon', 'windows_lit', 'street', 'floor_tex', 'floor_tint', 'floor_tint_mix', 'floor_coat',
            'wall', 'booth_color', 'absorber', 'rug_tex', 'rug_tint', 'membrane_white', 'last_dim', 'flat_glow',
            'across_glow', 'backpanel_color')
    return {'kind': 'kit', 'shape': 'ext', 'module': 'planet_room', 'fn': 'room', **{k: v[k] for k in keys if k in v}}


def props(v):
    out = [room_piece(v)]
    for i, (x, y) in enumerate(P.stools()):                           # the bar stools (Poly Haven, CC0)
        out.append({'kind': 'kit', 'shape': 'asset', 'model': 'bar_chair_round_01', 'res': '1k',
                    'position': [round(x, 3), round(y, 3), 0.0], 'rotate': [0, 0, (i * 37) % 23 - 11]})
    for x, y, f in P.CHAIRS:                                          # the lounge's low chairs
        out.append({'kind': 'kit', 'shape': 'asset', 'model': 'mid_century_lounge_chair', 'res': '1k',
                    'position': [x, y, 0.012], 'rotate': [0, 0, v.get('chair_rot0', -90.0) + f]})
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
        L[f'spk{k}'] = {'type': 'spot', 'position': [round(x + 0.35 * math.sin(math.radians(rot)), 3),
                                                      round(y - 0.35 * math.cos(math.radians(rot)), 3), P.MEMBRANE - 0.02],
                        'target': [x, y, 0.75], 'power_w': v['spot_speaker'], 'cone_deg': 28, 'blend': 0.6,
                        'radius_m': 0.03, 'color': 3000}
    # a pinhole in each Fog niche's head, onto the speaker
    for k, (role, colour, x, y, z, rot) in enumerate(P.speakers()):
        if role == 'backbar':
            L[f'fog{k}'] = {'type': 'spot', 'position': [x, y - 0.12, P.NICHE_Z0 + P.NICHE_H - 0.03], 'target': [x, y - 0.25, z + 0.6],
                            'power_w': v['spot_fog'], 'cone_deg': 40, 'blend': 0.7, 'radius_m': 0.02, 'color': 3000}
    # pinholes onto the bar top, between the pendants
    for i, x in enumerate(P.bar_pendants()[:-1]):
        L[f'bar{i}'] = {'type': 'spot', 'position': [x + 0.7, P.BAR_FRONT + 0.05, P.MEMBRANE - 0.02],
                        'target': [x + 0.7, P.BAR_FRONT + 0.1, P.BAR_TOP_Z], 'power_w': v['spot_bar'], 'cone_deg': 30,
                        'blend': 0.7, 'radius_m': 0.02, 'color': 2900}
    # the DJ desk's own light
    L['dj'] = {'type': 'spot', 'position': [P.L - 0.6, P.D / 2, P.DJ['recess_z'] - 0.02], 'target': [P.L - 0.45, P.D / 2, P.DJ['desk_z']],
               'power_w': v['spot_dj'], 'cone_deg': 70, 'blend': 0.8, 'radius_m': 0.05, 'color': 3000}
    if v.get('spot_records', 0) > 0:                                 # a wash down the record wall
        for k, yy in enumerate((2.6, 4.57, 6.5)):
            L[f'rec{k}'] = {'type': 'spot', 'position': [P.L - 1.4, yy, P.MEMBRANE - 0.02], 'target': [P.L - 0.4, yy, 1.4],
                            'power_w': v['spot_records'], 'cone_deg': 60, 'blend': 0.8, 'radius_m': 0.04, 'color': 3200}
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
    for i, x0 in enumerate(P.BOOTHS):
        bell(x0 + P.BOOTH_LEN / 2, 0.37, P.TABLE['h'], v['bell_w'], f'booth{i}-')
    # the street lamps (outside, along the curb), 3000 K LED
    if v['street']:
        for k, x in enumerate((-6.0, 7.0, 21.0)):
            L[f'street{k}'] = {'type': 'point', 'position': [x, -4.4, 7.2], 'power_w': v['street_lamp'], 'radius_m': 0.15,
                               'color': 3000}
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
        'render': {'samples': v['samples'], 'adaptive': 0.02, 'denoise': True, 'clamp': 10, 'bounces': 10,
                   'view': v['view'], 'look': v['look'], 'exposure': v['exposure'], 'white_balance_k': v['wb'], 'white_balance_tint': 0.0},
    }
    return s


EYE = 1.60
VIEWS = {
    'door': {'title': 'the whole room at night, from the door',
             'camera': {'position': [0.55, 3.55, EYE], 'target': [P.L, 5.0, 1.35], 'lens_mm': 18, 'level': True}},
    'bar': {'title': 'the bar front lit, at eye level',
            'camera': {'position': [1.30, 3.10, 1.45], 'target': [7.2, 7.4, 0.95], 'lens_mm': 26, 'level': True}},
    'listening': {'title': 'the listening corner, a pair either side of the lounge',
                  'camera': {'position': [11.70, P.D / 2, 1.20], 'target': [P.L, P.D / 2, 1.25], 'lens_mm': 22, 'level': True}},
    'backbar': {'title': 'the back-bar, the Fog pair among the lit shelves',
                'camera': {'position': [3.70, 6.10, 1.52], 'target': [3.30, P.D, 1.45], 'lens_mm': 28, 'level': True}},
    'records': {'title': 'the record wall and the DJ desk with Cumulus',
                'camera': {'position': [15.6, 3.2, 1.55], 'target': [P.L, 4.9, 1.15], 'lens_mm': 32, 'level': True}},
    'street': {'title': 'the street at night, through the window',
               'camera': {'position': [6.2, -14.5, 1.65], 'target': [6.2, 0.0, 2.6], 'lens_mm': 30, 'level': True}},
}


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or VIEWS:
        p = os.path.join(OUT, f'{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write(sys.argv[1:] or None)
