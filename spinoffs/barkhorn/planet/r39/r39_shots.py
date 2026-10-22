"""Planet EARF's shots, round 39 (the lead, 2026-10-22: "taken to world class"): round 38b's room and settings, made
into six photographs (three heroes, three details) as an architectural photographer would take them, plus Mother EARF
as an option over the listening room.

    python3 spinoffs/barkhorn/planet/r39/r39_shots.py [VIEW ...] [--final]   # writes studio/shots/barkhorn/planet39/
    python3 studio/engine/render.py studio/shots/barkhorn/planet39/door.json --out IMG --scale 0.5

Views: door, bar, listening (the heroes); decks, bowl, street (the details); door-mother and listening-mother (the
heroes with Mother EARF hung over the listening room).
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r38'))
import r38_shots as T38                                             # noqa: E402  (round 38b's builder, its fixes on)

T37 = T38.T37
S = T38.S
RP = T37.RP
ROOT = T37.ROOT
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet39')
KIT39 = 'spinoffs/barkhorn/planet/r39/kit39.py'
C = RP.COUNTER; ZT = C['top_z']
DX, DY = round(RP.DJ['x'] + 0.80, 3), round(C['y1'] - 0.30, 3)     # the request column

# what every round-39 frame shares: round 38b's material fixes, a little air, and a photographer's finish
ALL = dict(decorrelate=True, rw_vary=True, rw_faceout=0.14, rw_pull=0.08, steel_mix=0.85, haze=0.004)
# p2 (the p1 critics, all frames: 4.0 to 5.5): the screens were lightboxes, the street lamps raked daylight-hard
# shadows across the floor, the Domes' downlights hard and hot (one white band on the zinc, stain-like shadow
# ellipses), the Domes' liners blown white, the Orbs cold white balls, a magenta-orange cast; so: the screens down,
# the street lamps down, the Domes' downlights softer, wider and weaker with a large source, their liners down, the
# Orbs dimmer and warmer, the balance cooler and a touch greener, a little more air
ALL.update(screen_glow=0.07, street_lamp=110.0, pendant_w=80.0, pendant_cone=28.0, dome_glow_smoke=0.12,
           orb_trim=0.45, wb=3250, wb_tint=-6.0, haze=0.007, pend_radius=0.07)
# p3 (the p2 critics, 4.0 to 6.0): the haze fogged the back bar and drew stage beams; the grade still orange (the
# shell's blue near zero); the zinc and the near floor brighter than the heroes; the Domes still opal white; the Orbs
# white balls with no pools; the record wall's cubbies empty and glowing; the street lamps still raking the floor
ALL.update(haze=0.003, wb=2850, wb_tint=-4.0, pendant_w=50.0, pendant_cone=24.0, dome_glow_smoke=0.05, orb_trim=0.28,
           orb_pool=3.0, screen_glow=0.035, street_lamp=50.0, rw_w=6.0, records_fill=True)
FINISH = {'enabled': True, 'white_in': 236, 'white_out': 240, 'contrast': 0.08, 'clarity': 0.05, 'sharpen': 0.25,
          'sharpen_px': 0.7, 'grain': 2.5}

Y0 = round(C['y0'], 3)                                              # the counter's guest edge


def chair_x(i):
    return round(C['x0'] + 0.55 + i * (C['x1'] - C['x0'] - 1.1) / (RP.NCHAIRS - 1) + ((i * 7) % 5 - 2) * 0.02, 3)


AMBER, CLEAR, RED = '#B8641C', '#E8DDB8', '#B8462A'
# what a night leaves on the zinc, all frames (each view adds its own)
COUNTER_LIFE = dict(
    rocks=[[4.45, Y0 + 0.16, ZT, 0.030, 1, AMBER], [5.62, Y0 + 0.13, ZT, 0.018, 1, AMBER], [8.35, Y0 + 0.15, ZT, 0.026, 3, AMBER]],
    coupes=[[6.05, Y0 + 0.17, ZT, 0.55, RED], [9.10, Y0 + 0.16, ZT, 0.8, CLEAR]],
    napkins=[[4.45, Y0 + 0.16, ZT, 8.0], [5.62, Y0 + 0.13, ZT, -11.0], [6.05, Y0 + 0.17, ZT, 21.0], [8.35, Y0 + 0.15, ZT, 4.0],
             [9.10, Y0 + 0.16, ZT, -6.0]],
    votives=[[5.15, Y0 + 0.22, ZT], [7.95, Y0 + 0.22, ZT]],
    matchbooks=[[5.32, Y0 + 0.12, ZT, 28.0]],
    coats=[[chair_x(1), round(C['y0'] - 0.48 - 0.19, 3), 1.02, 0.0, 0.40]])

VIEWS = {
    # the room from the door at night: standing just inside, by the host stand, down the room's length to the altar
    'door': {'title': 'the room from the door, at night',
             'camera': {'position': [1.90, 1.20, 1.38], 'target': [16.5, 3.2, 1.20], 'lens_mm': 28, 'level': True,
                        'fstop': 5.6, 'focus': [8.0, 3.0, 1.2]},
             'base': 'bar-smoke', 'settings': dict(exposure=4.0, altar_w=300.0, altar_cone=22.0, listen_key=1.0, listen_rim=5.0), 'life': COUNTER_LIFE},
    # the bar counter: from the banquette's end, along the zinc to the decks and the pair
    'bar': {'title': 'the bar counter',
            'camera': {'position': [3.30, 2.40, 1.28], 'target': [7.4, 5.5, 1.40], 'lens_mm': 35, 'level': True,
                       'fstop': 4.0, 'focus': [6.6, 4.4, 1.2]},
            'base': 'bar-smoke', 'settings': dict(exposure=3.4, bar_key=1.4, bar_rim=8.0, spk_niche_strip=0.8, niche_strip=1.5), 'life': COUNTER_LIFE},
    # the listening room: from behind the tub chairs, the pair on the altar
    'listening': {'title': 'the listening room',
                  'camera': {'position': [11.95, 1.05, 1.25], 'target': [16.6, 3.3, 1.00], 'lens_mm': 26, 'level': True,
                             'fstop': 4.0, 'focus': [15.5, 3.0, 1.0]},
                  'base': 'listening-smoke', 'settings': dict(exposure=4.7, screen_glow=0.004, listen_key=0.8, listen_rim=5.0, altar_w=60.0,
                                                       altar_cone=12.0, altar_z=0.7, niche_strip=0.07, haze=0.004, plinth=0.0,
                                                       orb_pool=5.0),
                  'life': dict(rocks=[[round(RP.TUB_TABLES[3][0] + 0.06, 3), round(RP.TUB_TABLES[3][1] - 0.07, 3),
                                       round(RP.ZONE['z'] + RP.TUB_TABLE['h'], 3), 0.024, 1, AMBER]],
                               votives=[[round(RP.TUB_TABLES[0][0] + 0.10, 3), round(RP.TUB_TABLES[0][1] - 0.12, 3),
                                         round(RP.ZONE['z'] + RP.TUB_TABLE['h'], 3)]])},
    'decks': {'title': 'the decks: the request column and a drink just poured',
              # seated at the counter by the decks, low over the zinc: a coupe just poured in front, the mixing glass and
              # the open bottle behind it, the request column at the right third, a record player beyond
              'camera': {'position': [round(DX - 0.56, 3), round(Y0 - 0.50, 3), round(ZT + 0.30, 3)],
                         'target': [round(DX - 0.06, 3), round(DY - 0.02, 3), round(ZT + 0.13, 3)], 'lens_mm': 40, 'level': True,
                         'fstop': 5.6, 'focus': [DX, round(DY - 0.04, 3), round(ZT + 0.10, 3)]},
              'base': 'coins-decks', 'settings': dict(exposure=1.0, bar_key=3.0, bar_rim=8.0, column_glow=1.6, decks_pin=220.0),
              # p2: the mixing glass and the bottle were hidden behind the record player (both critics): now right of the
              # column, in the focus plane; the coupe left, clear of the column; the votive nearest, its flame in frame
              'life': dict(coupes=[[round(DX - 0.30, 3), round(Y0 + 0.14, 3), ZT, 0.92, RED]],
                           mixing=[[round(DX + 0.17, 3), round(Y0 + 0.30, 3), ZT, 0.05, AMBER]],
                           bottles=[[round(DX + 0.36, 3), round(Y0 + 0.44, 3), ZT, 150.0, '#D8CDB2']],
                           napkins=[[round(DX - 0.30, 3), round(Y0 + 0.14, 3), ZT, 12.0]],
                           votives=[[round(DX + 0.08, 3), round(Y0 + 0.06, 3), ZT]],
                           matchbooks=[[round(DX - 0.05, 3), round(Y0 + 0.05, 3), ZT, -22.0]])},
    'bowl': {'title': 'the door: the bowl of coins on the host stand',
             # from inside the room, looking back to the door: the bowl on the host stand in the foreground, the steel
             # door and the shopfront beyond it, the street's light in the glass
             # p2 (4.5, 5.0: two thirds empty wall, the door unreadable, the stand pale): nearer and higher on 45 mm,
             # looking down past the bowl to the door and the vestibule's glass (a Smoke bowl, tried, read as a dark hole)
             # p3 (4.5, 5.0: still no door, only a cream strip and a void): swung round to the shopfront glass
             'camera': {'position': [round(RP.HOST['x'] + 0.95, 3), round(RP.HOST['y'] + 0.65, 3), 1.40],
                        'target': [0.3, 1.6, 1.05], 'lens_mm': 45, 'level': True,
                        'fstop': 2.8, 'focus': [RP.HOST['x'], RP.HOST['y'], RP.HOST['top'] + 0.04]},
             'base': 'coins-door', 'settings': dict(exposure=5.0, host_w=5.0, host_cone=22.0, coin_edge='reeded', street_lamp=160.0),
             'retouch': dict(darken={'oak-host': 0.3}, set={'foil': {'Base Color': '#8A6A3A', 'Roughness': 0.24, 'Metallic': 1.0}}),
             'life': dict(matchbooks=[[RP.HOST['x'] + 0.10, RP.HOST['y'] - 0.08, RP.HOST['top'], -18.0],
                                      [RP.HOST['x'] + 0.13, RP.HOST['y'] - 0.06, RP.HOST['top'] + 0.006, 9.0]])},
    'street': {'title': 'the shopfront at blue hour, from across the street',
               # from the far kerb and up the street, at eye height: the whole frontage at three-quarters, the flats above
               # it, the street running away, the sky still blue over it, the room already lit
               'camera': {'position': [-11.0, -1.2, 1.50], 'target': [0.0, 3.6, 1.9], 'lens_mm': 50, 'level': True,
                          'fstop': 8.0, 'focus': [0.0, 3.05, 1.6]},
               'base': 'street', 'settings': dict(exposure=2.0, sky=0.25, sky_zenith='#2A3F6A', sky_horizon='#7A8AAE', wb=4300,
                                                street_lamp=150.0, etch_glow=0.03, pendant_w=300.0, rw_w=60.0,
                                                screen_glow=0.8, records_fill=True),
               # the coordinator's p1 note: the street needs life and SF furniture: a street tree at the kerb, a hydrant
               'assets': [{'model': 'tree_small_02', 'position': [-3.0, -2.2, 0.0], 'rotate': [0, 0, 40]},
                          {'model': 'fire_hydrant', 'position': [-3.15, 6.7, 0.0], 'rotate': [0, 0, 90]}]},
}


# Mother EARF at the room's hinge, over the aisle between the counter's end and the step (over the listening room the
# partition's header hid it from the door, look 2): between the beams at 10.51 and 11.73, its foot 2.13 m up so a
# standing guest walks under it, its top 15 mm under the deck
# p2 (the lead, 2026-10-22, from the owner's rainbow notes: "I also don't love the overt rainbow coloring. It's too
# Castro for SF"): Mother EARF is round 33b's one-colour globe, the same slotted discs in Smoke, whole (no core),
# see-through, the rims dark and polished, under one hard spot, so its shadow draws the globe again on the concrete.
# At the hinge, 9 m from the door, it vanished (look 5); so it hangs low over the middle banquette table, between the
# beams at 5.63 and 6.85, 1.1 m over the table, and the spot on the deck behind it throws its shadow on the bare
# concrete wall between the two frosted screens
MOTHER = dict(centre=[6.24, 1.15, 2.47], size=1.25, t=0.025, core=0.0, rim=0.0, tint='#6A6668', radius=0.07,
              ceiling=RP.CEIL, heading=55.0)
MOTHER_SPOT = dict(position=[6.24, 2.75, 3.32], power_w=60.0, cone_deg=34.0, radius_m=0.02)
# the multicolour globe of p1 (round 33c), kept as a second variant only (`-colour`)
MOTHER_COLOUR = dict(centre=[11.12, RP.YC, 2.76], size=1.25, t=0.025, core=0.13, rim=0.22, rim_par=0.5, core_glow=0.05,
              core_w=45.0, ceiling=RP.CEIL, heading=-35.0, radius=0.04)


def product_lights(v):
    """The speakers lit as products (r38's critics: the Smoke cabinets read dark against what lights them): a large
    soft source in front of each cabinet, off the camera's side, linked to the speaker alone, so its smoked front and
    the horn carry a long soft reflection the way a product photographer's scrim gives one; and a narrow strip behind
    and above it for a rim on its top edges."""
    L = {}
    rx = T37.spk_rx
    for grp, spk, key, rim in (('b', [(x, y, z) for role, x, y, z, rot, tilt in RP.bar_speakers()], v.get('bar_key', 0), v.get('bar_rim', 0)),
                               ('l', [(x, y, z) for role, c, x, y, z, rot in RP.speakers()], v.get('listen_key', 0), v.get('listen_rim', 0))):
        for i, (x, y, z) in enumerate(spk):
            if grp == 'b':                                          # facing the counter (-y)
                front, back = [x, y - 1.3, z + 0.95], [x, y + 0.05, z + 1.55]
            else:                                                   # facing the room (-x)
                front, back = [x - 1.3, y, z + 0.95], [x + 0.25, y, z + 1.5]
            if key > 0:
                L[f'key{grp}{i}'] = {'type': 'area', 'position': front, 'target': [x, y, z + 0.65], 'size_m': [1.0, 0.7],
                                     'irradiance': key, 'color': 3000, 'camera': False, 'receivers': rx(i)}
            if rim > 0:
                L[f'rim{grp}{i}'] = {'type': 'area', 'position': back, 'target': [x, y, z + 1.0], 'size_m': [0.5, 0.08],
                                     'irradiance': rim, 'color': 2800, 'camera': False, 'receivers': rx(i)}
    return L


def _base(name):
    return T37.VIEWS[name]


def shot(view):
    colour = view.endswith('-mother-colour')
    mother = colour or view.endswith('-mother')
    key = view.split('-mother')[0]
    vw = VIEWS[key]
    b = _base(vw['base'])
    new = {**b, 'camera': dict(vw['camera']), 'settings': {**b['settings'], **ALL, **vw['settings'], 'mother': mother}}
    # every layer (the den's builder, rounds 36, 37 and 38) reads its own VIEWS: the view swapped in each, then back
    mods = [m for m in (S, T37.T36, T37, T38) if vw['base'] in getattr(m, 'VIEWS', {})]
    saved = [(m.VIEWS, m.VIEWS[vw['base']]) for m in mods]
    for m in mods:
        m.VIEWS[vw['base']] = new
    try:
        s = T38.shot(vw['base'])
    finally:
        for d, v in saved:
            d[vw['base']] = v
    v = new['settings']
    extra = [{'kind': 'kit', 'shape': 'ext', 'path': KIT39, 'fn': 'life', **vw.get('life', {})}] if vw.get('life') else []
    if mother:
        extra.append({'kind': 'kit', 'shape': 'ext', 'path': KIT39, 'fn': 'mother',
                      **(MOTHER_COLOUR if colour else MOTHER), **vw.get('mother', {})})
        if not colour:
            sp = MOTHER_SPOT
            s['lights']['mother-spot'] = {'type': 'spot', 'position': sp['position'], 'target': MOTHER['centre'],
                                          'power_w': v.get('mother_spot', sp['power_w']), 'cone_deg': sp['cone_deg'],
                                          'blend': 0.35, 'radius_m': sp['radius_m'], 'color': 3000, 'camera': False}
            # p3: a narrow light behind and above it, from the window side, so the polished rims catch a line each
            c = MOTHER['centre']
            s['lights']['mother-rim'] = {'type': 'spot', 'position': [round(c[0] + 1.6, 3), round(c[1] + 0.2, 3), 3.30],
                                         'target': list(c), 'power_w': v.get('mother_rim', 25.0), 'cone_deg': 30.0,
                                         'blend': 0.5, 'radius_m': 0.05, 'color': 2700, 'camera': False}
    if v.get('records_fill'):                     # p3: the record wall's empty cells filled (both bar critics)
        extra.append({'kind': 'kit', 'shape': 'ext', 'path': KIT39, 'fn': 'records'})
    extra.append({'kind': 'kit', 'shape': 'ext', 'path': KIT39, 'fn': 'retouch', **vw.get('retouch', {})})
    if v.get('coin_edge'):                       # the coins' reeded edge (the coordinator: they read as jelly sweets)
        for o in s['set']['props']:
            if o.get('fn') == 'bowl':
                o['edge'] = v['coin_edge']
    for a in vw.get('assets', []):                # scanned CC0 street furniture (Poly Haven)
        extra.append({'kind': 'kit', 'shape': 'asset', 'res': '1k', **a})
    s['set']['props'] += extra
    s['lights'].update(product_lights(v))
    for k, l in s['lights'].items():             # p2: the Domes' downlights from a larger source, softly edged
        if k.startswith('pend') and v.get('pend_radius'):
            l['radius_m'] = v['pend_radius']; l['blend'] = 0.5
    for o in s['set']['props']:                  # the Orbs' liners warmer: at #FFDCB8 under the room's 3000 K balance
        if o.get('fn') == 'orb':                 # they read cyan (look 2, r38b's street)
            o.setdefault('materials', {}).setdefault('liner', {})['glow_color'] = v.get('orb_col', '#FFB878')
            o['lamp_w'] = round(o.get('lamp_w', 1.0) * v.get('orb_pool', 1.0), 3)   # p3: a pool on each table
    s['title'] = f"Planet EARF, {vw['title']}{' (Mother EARF, multicolour)' if colour else ' (Mother EARF)' if mother else ''} (round 39)"
    s['size'] = [2400, 1600]
    s['finish'] = dict(FINISH)
    return s


def write(names=None, final=False):
    out = os.path.join(OUT, 'final') if final else OUT
    os.makedirs(out, exist_ok=True)
    for n in names or list(VIEWS) + ['door-mother', 'door-mother-colour']:
        s = shot(n)
        if final:
            s['render'].update({'samples': 256, 'adaptive': 0.01})
        p = os.path.join(out, f'{n}.json')
        json.dump(s, open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    write(args or None, final='--final' in sys.argv)
