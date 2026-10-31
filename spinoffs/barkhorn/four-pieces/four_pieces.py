"""Four pieces, named for the Earth: one furniture-magazine interior with Tropos (a pair), Mantle, Hemisphere and Core
together, for the investor deck's slide (the owner, 2026-10-31). Full-bleed 16:9; the coordinator sets the labels in
HTML over the picture, at the anchors render_fp.py writes.

The room is the speaker team's golden-hour living room (r33-speaker-horn 6770c713, blind 7.0; golden-room.base.json),
widened to take a reading corner at the right:
- the Tropos pair either side of the walnut credenza, toed in 6 degrees, 0.29 m off the wall (the asset: cover off);
- Mantle on the credenza between them, where it is played (its dust lid off, as most are played);
- a reading chair in the right corner, Hemisphere hung over its arm at reading height (rim 1.42 m), the cord to the
  ceiling;
- Core on a side table between the right speaker and the chair, cordless (the owner: no cable anywhere).

Directions (art direction by proofs):
- A, morning: no sun, the north sky through the windows, pale and calm (Kinfolk, Cereal);
- B, golden hour: the low sun through the left windows, the tint's coloured shadows (AD);
- C, blue hour into evening: a dim blue sky, the lamps lit, Mantle's base glowing (Apartamento, Wallpaper*).
Palettes: P1 all four in Poison; P2 the hi-fi in Ice, the lamps in Dust (blue and orange).

    python3 spinoffs/barkhorn/four-pieces/four_pieces.py            # writes the shots into shots/
    python3 spinoffs/barkhorn/four-pieces/render_fp.py shots/NAME.json --out IMG.png --scale 0.25 --samples 48
"""
import copy, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'shots')
BASE = json.load(open(os.path.join(HERE, 'golden-room.base.json')))
PIECES = 'spinoffs/barkhorn/room31/pieces.py'

TINT = {'poison': 'Poison', 'ice': 'Ice', 'dust': 'Dust', 'ember': 'Ember', 'smoke': 'Smoke', 'acid': 'Acid',
        'haze': 'Haze', 'fog': 'Fog'}
PALETTES = {'p1': {'hifi': 'poison', 'lamps': 'poison'}, 'p2': {'hifi': 'ice', 'lamps': 'dust'}}

# where things stand (metres; the back wall at y = 0.95, the window wall at x = -2.65, the right wall at x = 3.75; the
# room widened 0.6 m toward the window from the speaker team's 5.8 m)
LAYOUTS = {
    # round 1: the music left of centre, the reading corner at the right, brought forward
    'v1': {'mid': -0.45, 'side': [1.52, -0.08], 'chair': [2.22, -0.40, -45.0], 'hemi': [1.98, -0.66, 1.38],
           'plant': [-2.25, 0.55, 30.0]},
    # round 2 (both critics: not a frontal line-up): the reading nook by the window, the chair in the window's light,
    # Hemisphere over its arm, Core on the side table between the chair and the left speaker; the music right of centre
    'v2': {'mid': 0.45, 'side': [-1.58, 0.36], 'chair': [-1.95, -0.38, 40.0], 'hemi': [-1.72, -0.62, 1.40],
           'plant': [3.3, 0.6, 30.0]},
}
LAYOUT = LAYOUTS['v1']
SPK_X, SPK_Y = 1.22, 0.53               # each Tropos 1.22 either side of the music's centre line, 0.29 m off the wall
SIDE_H = 0.551                          # side_table_01: 0.55 x 0.45, 0.551 tall
CEILING = 2.9


def geometry(L):
    mid = L['mid']
    return {'mid': mid, 'cred': {'position': [mid, 0.718], 'size': [1.62, 0.44, 0.56]}, 'mantle': [mid, 0.70, 0.56],
            'side': L['side'], 'core': [L['side'][0], L['side'][1] + 0.02, SIDE_H], 'chair': L['chair'],
            'hemi': L['hemi'], 'plant': L['plant']}


def props(pal, L, rug=None):
    G = geometry(L); MID = G['mid']; CORE = G['core']; HEMI = G['hemi']; CHAIR = G['chair']; SIDE = G['side']
    keep = []
    for p in BASE['set']['props']:
        fn = p.get('fn')
        if fn in ('socket',) or p.get('kind') == 'cable':
            continue                    # the speaker team's sockets and leads were placed for their x = 1.2 pair
        if fn == 'recolour':
            continue
        p = copy.deepcopy(p)
        if fn == 'credenza':
            p.update(G['cred'])
        if fn == 'books':
            p['position'] = [MID - 0.6, 0.73, 0.56]
        if fn == 'rug':
            p['position'] = [MID, -0.95]; p['size'] = [2.8, 1.8]
            if rug:
                p.update(rug)
        if fn == 'floor':
            p['rect'] = [-2.65] + p['rect'][1:]
        if fn == 'sheer':
            p['position'] = [-2.55] + p['position'][1:]
        if fn == 'exterior':
            p['centre'] = [-3.65] + p['centre'][1:]
        keep.append(p)
    # the vase moves to the credenza's right end
    for p in keep:
        if p.get('shape') == 'asset' and p.get('model') == 'ceramic_vase_02':
            p['position'] = [MID + 0.6, 0.76, 0.56]; p['scale'] = 0.9
    keep += [
        {'kind': 'kit', 'shape': 'asset', 'model': 'modern_arm_chair_01', 'position': [CHAIR[0], CHAIR[1], 0.0],
         'rotate': [0, 0, CHAIR[2]], 'scale': 1.0},
        {'kind': 'kit', 'shape': 'asset', 'model': 'side_table_01', 'position': [SIDE[0], SIDE[1], 0.0],
         'rotate': [0, 0, 0.0], 'scale': 1.0},
        {'kind': 'kit', 'shape': 'asset', 'model': 'potted_plant_01', 'position': [G['plant'][0], G['plant'][1], 0.0],
         'rotate': [0, 0, G['plant'][2]], 'scale': 1.0},
        # Core, cordless: the battery cartridge in, no cable
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'flavour': pal['lamps'],
         'spots': [{'position': CORE, 'rotate_z': -20}], 'cable': False, 'cartridge': 'in'},
        # Hemisphere, its cord up to the ceiling
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'flavour': pal['lamps'],
         'spots': [{'position': HEMI}], 'ceiling': CEILING},
    ]
    return keep


def lamps(p, on):
    """The lamps' own light: `on` 0 (off) to 1 (full, the evening)."""
    for q in p:
        if q.get('module') == 'earf_moon':
            if on <= 0:
                q['lamp'] = False; q['shade_glow'] = 0.0
            else:
                q['lamp_w'] = (9.0 if q['fn'] == 'dome' else 3.0) * on
                q['shade_glow'] = 0.25 * on


def shot(direction, palette, layout='v1', camera=None, sun=None, rug=None):
    pal = PALETTES[palette]
    Lay = LAYOUTS[layout]; G = geometry(Lay); MID = G['mid']; MANTLE = G['mantle']; HEMI = G['hemi']; CORE = G['core']
    s = copy.deepcopy(BASE)
    s.pop('products', None)
    s['title'] = f'Four pieces, {direction}, {palette}: Tropos pair, Mantle, Hemisphere, Core'
    s['products'] = [{'def': 'studio/products/barkhorn-turntable-float.json', 'flavour': pal['hifi'],
                      'hide': ['lid-*', 'hinges'],
                      'instances': [{'flavour': pal['hifi'], 'position': MANTLE, 'rotate_z': 0.0}]}]
    s['tropos'] = [{'tint': TINT[pal['hifi']], 'position': [MID - SPK_X, SPK_Y], 'rotate_z': 6.0},
                   {'tint': TINT[pal['hifi']], 'position': [MID + SPK_X, SPK_Y], 'rotate_z': -6.0}]
    s['set']['props'] = props(pal, Lay, rug)
    s['set']['size'] = [6.4, 7.0, 2.9]; s['set']['center'] = [0.55, -2.55]
    s['size'] = [3840, 2160]
    s['camera'] = camera or {'position': [0.35, -5.2, 1.1], 'target': [0.35, 0.3, 0.95], 'lens_mm': 30,
                             'level': True, 'fstop': 8.0, 'focus': [0.3, 0.3, 0.8]}
    s['materials'] = {'glow': {'strength': 0.0}}
    s['render'] = {**s['render'], 'caustics_refractive': True, 'samples': 128}
    L = s['lights']
    if direction == 'a':                       # morning, north light
        s['sun'] = {'azimuth_deg': -68.0, 'elevation_deg': 30.0, 'irradiance': 0.0}
        s['sky'] = {'kind': 'physical', 'strength': 1.6, 'air': 1.0, 'dust': 1.0, 'sun_elevation_deg': 35.0}
        L['north'].update({'irradiance': 1.2, 'color': '#E6ECF2'})
        L['bounce'].update({'irradiance': 0.8, 'color': '#F4F1EC'})
        L['window'] = {'type': 'area', 'size_m': [0.1, 5.0], 'position': [-2.2, -1.0, 1.4],
                       'target': [1.0, -0.6, 0.9], 'irradiance': 0.0}
        s['render'].update({'exposure': -0.3, 'white_balance_k': 6200})
        lamps(s['set']['props'], 0.15)
    elif direction == 'b':                     # golden hour, as the speaker team's room
        lamps(s['set']['props'], 0.35)
        if sun:
            s['sun'].update(sun)
    else:                                      # blue hour into evening
        s['sun'] = {'azimuth_deg': -70.0, 'elevation_deg': 2.0, 'irradiance': 0.0}
        s['sky'] = {'kind': 'gradient', 'zenith': '#2E3E66', 'horizon': '#6A7BA6', 'ground': '#1E2230',
                    'strength': 0.6}
        L['north'].update({'irradiance': 0.22, 'color': '#8FA2D0'})
        L['bounce'].update({'irradiance': 0.10, 'color': '#FFD9B0'})
        # a warm lamp out of frame at the right (the room's other light), low on the wall
        L['practical'] = {'type': 'area', 'size_m': [0.5, 0.5], 'position': [3.4, -2.2, 1.4],
                          'target': [0.0, 0.6, 0.9], 'irradiance': 0.12, 'color': 2700, 'camera': False}
        s['materials']['glow'] = {'strength': 6.0}
        for q in s['set']['props']:
            if q.get('fn') == 'exterior':
                q['strength'] = 1.1; q['tint'] = '#6F8BD6'
        lamps(s['set']['props'], 1.0)
        s['render'].update({'exposure': 1.4, 'white_balance_k': 4300})
    s['anchors'] = {
        'tropos': [MID - SPK_X, SPK_Y - 0.20, 1.10],       # the left speaker's horn mouth
        'tropos_right': [MID + SPK_X, SPK_Y - 0.20, 1.10],
        'mantle': [MANTLE[0] + 0.08, MANTLE[1], MANTLE[2] + 0.12],
        'hemisphere': [HEMI[0], HEMI[1], HEMI[2] + 0.06],
        'core': [CORE[0], CORE[1], CORE[2] + 0.11],
    }
    return s


JUTE = {'texture': 'hessian_230', 'tint': None, 'tint_mix': 0.0, 'value': 0.85, 'tex_scale': None, 'displace': 0.003}
# round 2: golden hour, all Poison, the nook layout; cameras off axis and lower (both critics), the sun higher so the
# window's light lands on the lower wall and the floor, not across the header's wall
R2 = {
    # three-quarter from the right, the window and its nook in the background: the sun comes toward the lens
    'r2-q': dict(layout='v2', rug=JUTE, sun={'elevation_deg': 22.0},
                 camera={'position': [2.55, -4.05, 1.02], 'target': [-0.35, 0.45, 0.88], 'lens_mm': 32, 'level': True,
                         'fstop': 8.0, 'focus': [0.2, 0.4, 0.8]}),
    # nearly square but lower and from a little right of centre, a longer lens, less floor
    'r2-f': dict(layout='v2', rug=JUTE, sun={'elevation_deg': 22.0},
                 camera={'position': [0.9, -5.3, 0.98], 'target': [0.0, 0.45, 1.0], 'lens_mm': 35, 'level': True,
                         'fstop': 8.0, 'focus': [0.3, 0.4, 0.8]}),
}


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for d in 'abc':
        for p in PALETTES:
            n = f'{d}-{p}'
            json.dump(shot(d, p), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
            print(n)
    for n, kw in R2.items():
        json.dump(shot('b', 'p1', **kw), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n)


if __name__ == '__main__':
    main()
