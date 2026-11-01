"""Four pieces, round 6 on: re-laid for the owner's ruling of 2026-10-31 (r46-owner-notes 6a93885f): "Not lines and dots
to things. Everything spaced far enough out against a neutral enough background that text next to each object is
enough. Also should it have a version with the lights on?"

So the frame is built around its labels (layout.py solves them before anything renders):
- frontal, as the speaker team's golden room that won both blind duels against round 5's three-quarter view (7 to 6
  twice): the Tropos pair either side of a walnut credenza with Mantle on it, against plain plaster;
- the room 8.4 m wide so neither side wall shows; the windows are on the left wall, out of frame, and their light comes
  in from the side;
- Core on a side table at the left and Hemisphere over a reading chair at the right, both 3 m from the lens, so Core is
  about 110 px and Hemisphere about 140 px across at 1920 (the coordinator: at least 70 and 90);
- label zones (380 x 130 at 1920) on plain wall: Tropos's above the left speaker, Mantle's above Mantle between the
  horns, Core's above it, Hemisphere's to its left (above the right speaker); the header (900 x 160) at the top left.

Two versions, same camera and layout: `day` (golden hour) and `dusk` (lights on).

    python3 spinoffs/barkhorn/four-pieces/four_pieces_v3.py                # writes shots/v3-*.json
    python3 spinoffs/barkhorn/four-pieces/layout.py shots/v3-day.json      # the label check
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import four_pieces as F                                             # noqa: E402

SHOTS = os.path.join(HERE, 'shots')
HALF = 4.2                                    # the room's half width (x from -4.2 to 4.2), the back wall at y = 0.95

P = {
    # round 7 (both critics: closer, the products bigger; a shorter, lower credenza so Mantle is the centre)
    'spk': 1.0, 'spk_y': 0.53,                # each Tropos 1.0 either side of centre, 0.29 m off the wall
    'cred': [1.2, 0.42, 0.45],
    'core': [-1.35, -1.15],                   # round 7's critics: the side table whole, its feet in frame                    # the side table's centre (side_table_01, 0.551 tall)
    'hemi': [1.25, -1.25, 1.55],              # the rim, over the reading chair's inner arm
    'chair_r': [1.55, -0.95, -35.0],           # the reading chair, turned toward the room and the music
    'camera': {'position': [0.0, -4.5, 1.0], 'target': [0.0, 0.3, 0.95], 'lens_mm': 30, 'level': True,
               'fstop': 5.6, 'focus': [0.0, 0.3, 0.8]},
}
LABELS = {'tropos': {'of': 'tropos0', 'side': 'above'},
          'mantle': {'of': 'mantle', 'side': 'above', 'gap': 40},
          'core': {'of': 'core', 'side': 'above'},
          # the coordinator (round 7's slide): at dusk the pendant's glow reached its zone; the zone sits further off
          'hemisphere': {'of': 'hemisphere', 'side': 'left', 'gap': 80, 'dy': 50},
          'header': [100, 60]}
CEILING = 3.6                                 # high enough that its line stays out of the frame


def props(pal):
    out = []
    for p in F.BASE['set']['props']:
        fn = p.get('fn')
        if fn in ('socket', 'recolour', 'rug') or p.get('kind') == 'cable':
            continue
        if p.get('shape') == 'asset' and p.get('model') == 'ceramic_vase_02':
            continue                          # the wall between the horns is Mantle's label's
        p = copy.deepcopy(p)
        if fn == 'credenza':
            p.update({'position': [0.0, 0.718], 'size': P['cred'], 'lift': 0.5})   # a deeper walnut (round 7, c7)
        if fn == 'books':
            continue                          # Mantle alone on the credenza (round 6's critic, c6)
        if fn == 'floor':
            p['rect'] = [-HALF, p['rect'][1], HALF, p['rect'][3]]
        if fn == 'sheer':
            if p['position'][1] > -1.0:
                continue                      # the narrow sheer beside the window that is gone
            p['position'] = [-HALF + 0.1] + p['position'][1:]
        if fn == 'exterior':
            p['centre'] = [-HALF - 1.0] + p['centre'][1:]
        out.append(p)
    cr = P['chair_r']
    out += [
        # the chair re-covered in cognac (round 6's critic: the black leather was a hole in the frame)
        {'kind': 'kit', 'shape': 'ext', 'path': F.PIECES, 'fn': 'recolour', 'model': 'modern_arm_chair_01',
         'position': [cr[0], cr[1], 0.0], 'rotate': [0, 0, cr[2]], 'match': ['pillow'], 'color': '#8A5A3A',
         'blend': 'MIX', 'mix': 0.85},
        # a flat-weave wool rug, undyed oatmeal, under the side table and the chair
        {'kind': 'kit', 'shape': 'box', 'material': 'wool', 'color': '#857A66', 'size': [3.0, 2.0, 0.008],
         'position': [0.1, -1.2, 0.0], 'rotate': [0, 0, 3.0], 'ease': 0.003},
        {'kind': 'kit', 'shape': 'asset', 'model': 'side_table_01', 'position': [P['core'][0], P['core'][1], 0.0],
         'rotate': [0, 0, 0.0], 'scale': 1.0},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb', 'flavour': pal['lamps'],
         'spots': [{'position': [P['core'][0], P['core'][1], F.SIDE_H], 'rotate_z': -20}], 'cable': False,
         'cartridge': 'in'},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'flavour': pal['lamps'],
         'spots': [{'position': P['hemi']}], 'ceiling': CEILING},
        {'kind': 'kit', 'shape': 'asset', 'model': 'potted_plant_01', 'position': [-3.6, 0.3, 0.0],
         'rotate': [0, 0, 30.0], 'scale': 0.95},
    ]
    return out


def shot(version, palette='p1'):
    pal = F.PALETTES[palette]
    s = copy.deepcopy(F.BASE)
    s.pop('products', None)
    s['title'] = f'Four pieces, round 6 layout, {version}: Tropos pair, Mantle, Hemisphere, Core'
    s['products'] = [{'def': 'studio/products/barkhorn-turntable-float.json', 'flavour': pal['hifi'],
                      'hide': ['lid-*', 'hinges'],
                      'instances': [{'flavour': pal['hifi'], 'position': [0.0, 0.70, P['cred'][2]], 'rotate_z': 0.0}]}]
    s['tropos'] = [{'tint': F.TINT[pal['hifi']], 'position': [-P['spk'], P['spk_y']], 'rotate_z': 4.0},
                   {'tint': F.TINT[pal['hifi']], 'position': [P['spk'], P['spk_y']], 'rotate_z': -4.0}]
    s['set']['props'] = props(pal)
    s['set']['skirting'] = {**s['set'].get('skirting', {}), 'color': '#CFC8BC'}   # a step below the wall (final day, c5)
    s['set']['size'] = [2 * HALF, 7.0, CEILING]; s['set']['center'] = [0.0, -2.55]
    # the window nearest the back wall threw the sun's band across the header's wall: gone; the sun comes in by the
    # two forward windows, onto the speakers and the floor, and reaches the back wall only below 0.4 m
    s['set']['windows'] = [w for w in s['set']['windows'] if w['along'] < 2.0]
    s['size'] = [3840, 2160]
    s['camera'] = copy.deepcopy(P['camera'])
    s['render'] = {**s['render'], 'caustics_refractive': True, 'samples': 128, 'white_balance_k': 5600}
    s['materials'] = {'glow': {'strength': 1.5}}      # Mantle's base loop, soft by day
    L = s['lights']
    L['floorbounce'] = {'off': True}
    L['north'].update({'irradiance': 0.75, 'position': [0.0, -4.6, 2.2], 'target': [0.0, 0.3, 0.9], 'color': '#CFDDF0'})
    L['bounce'].update({'irradiance': 0.3, 'position': [0.0, -5.0, 2.2], 'target': [0.0, 0.3, 1.0]})
    # Mantle's deck caught by a soft card above the camera (round 4's critic, c2)
    L['mantle_kick'] = {'type': 'area', 'size_m': [0.8, 0.5], 'position': [0.3, -1.4, 1.9],
                        'target': [0.0, 0.70, 0.66], 'irradiance': 1.2, 'color': '#FFF0DE', 'camera': False}
    if version == 'day':
        # round 6's critic: brighter, the sun softer and less of the frame's drama
        # round 7's critic (5, 7 if fixed): the plaster cream not khaki (c1), the pair matched (c2), the sun softer
        # and higher so its patch stays low (c3), a warmer balance (c7)
        s['sun'].update({'azimuth_deg': -64.0, 'elevation_deg': 29.0, 'angle_deg': 12.0, 'irradiance': 20.0})
        L['bounce'].update({'irradiance': 0.6, 'color': '#FFF6EC'})
        L['north'].update({'irradiance': 1.2, 'color': '#F2E6D6', 'position': [-2.6, -3.6, 2.2]})   # the window side
        L['right_card'] = {'type': 'area', 'size_m': [1.5, 1.0], 'position': [2.5, -0.5, 1.0], 'target': [1.0, 0.53, 0.7],
                           'irradiance': 0.5, 'color': 4500, 'camera': False}
        F.lamps(s['set']['props'], 0.6)
        # the coordinator: the wall a warm off-white in every zone (sRGB 200-215) so dark ink reads at 7:1
        s['render'].update({'exposure': 1.25, 'white_balance_k': 5200})
    else:                                                       # dusk, lights on
        s['sun'] = {'azimuth_deg': -80.0, 'elevation_deg': 2.0, 'irradiance': 0.0}
        s['sky'] = {'kind': 'gradient', 'zenith': '#2E3E66', 'horizon': '#6A7BA6', 'ground': '#1E2230', 'strength': 0.8}
        L['north'].update({'irradiance': 0.02, 'color': '#E2E6EA'})      # the last daylight, near neutral (no mauve)
        L['bounce'].update({'irradiance': 0.07, 'color': '#FFD2A0'})
        # a long soft light high at the right, out of frame, so the acrylic's edges and the horns' lips catch a line
        L['edge'] = {'type': 'area', 'size_m': [1.8, 0.3], 'position': [2.6, -1.4, 2.7], 'target': [0.0, 0.5, 1.0],
                     'irradiance': 0.3, 'color': 3000, 'camera': False}
        # a soft wash grazing the back wall from the ceiling, so the wall falls off top to bottom, not left to right
        L['wallwash'] = {'type': 'area', 'size_m': [6.0, 0.2], 'position': [-1.0, 0.55, 3.5], 'target': [-1.0, 0.95, 1.2],
                         'irradiance': 0.14, 'color': 2700, 'camera': False}
        # an uplight's wash on the upper left wall (a floor lamp out of frame), so the header and Core's zone are not a
        # ramp from dark at the left to light at the right (the final critic, c4)
        L['uplight'] = {'type': 'area', 'size_m': [1.2, 1.2], 'position': [-3.2, -1.6, 2.6], 'target': [-2.0, 0.95, 1.6],
                        'irradiance': 0.16, 'color': 2700, 'camera': False}
        for i, x in enumerate((-1.0, 1.0)):      # a soft card over each Tropos, so the pair reads, not the chair
            L[f'top{i}'] = {'type': 'area', 'size_m': [0.6, 0.6], 'position': [x, 0.1, 2.5], 'target': [x, 0.53, 1.0],
                            'irradiance': 0.25, 'color': 3000, 'camera': False}     # the room's warm light off the ceiling
        # the room's other lamps, out of frame: a warm wash from the left (a floor lamp by the windows) and the right
        L['warm_l'] = {'type': 'area', 'size_m': [1.0, 1.0], 'position': [-3.6, -3.0, 1.6], 'target': [-1.0, 0.6, 0.8],
                       'irradiance': 0.14, 'color': 2700, 'camera': False}
        L['warm_r'] = {'type': 'area', 'size_m': [1.0, 1.0], 'position': [3.6, -3.4, 1.8], 'target': [1.0, 0.6, 0.9],
                       'irradiance': 0.06, 'color': 2700, 'camera': False}
        L['mantle_kick'].update({'irradiance': 0.5, 'color': 3000})
        s['materials']['glow'] = {'strength': 2.0}
        for q in s['set']['props']:
            if q.get('fn') == 'exterior':
                q['strength'] = 1.0; q['tint'] = '#6F8BD6'
        F.lamps(s['set']['props'], 1.0)
        for q in s['set']['props']:              # lit for the evening: Hemisphere's pool on the chair, Core's on its table
            if q.get('fn') == 'dome':
                q['lamp_w'] = 80.0; q['shade_glow'] = 0.4
            if q.get('fn') == 'orb':
                q['lamp_w'] = 28.0; q['shade_glow'] = 0.3
        s['render'].update({'exposure': 0.8, 'white_balance_k': 3100})
    # the rug's wool: its sheen down (at full sheen it read white at this grazing angle)
    s['material_tweaks'] = {'kit-wool': {'Sheen Weight': 0.15, 'Subsurface Weight': 0.0}}
    s['labels'] = copy.deepcopy(LABELS)
    sp = P['spk']; h = P['hemi']; c = P['core']
    s['anchors'] = {'tropos': [-sp, P['spk_y'] - 0.2, 1.10], 'tropos_right': [sp, P['spk_y'] - 0.2, 1.10],
                    'mantle': [0.08, 0.70, P['cred'][2] + 0.12], 'hemisphere': [h[0], h[1], h[2] + 0.06],
                    'core': [c[0], c[1] + 0.02, F.SIDE_H + 0.11]}
    return s


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for v in ('day', 'dusk'):
        json.dump(shot(v), open(os.path.join(SHOTS, f'v3-{v}.json'), 'w'), indent=1)
        print(f'v3-{v}')


if __name__ == '__main__':
    main()
