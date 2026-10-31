"""The campaign pictures (the coordinator, 2026-10-31, for the site, the deck and the press): Hemisphere over a dining
table at dusk, Core on a bedside at night, Mantle on a credenza with records, all three in one room, and macro
details. Each frame lights its lamp as the brightness study does (hemisphere_brightness.py: a Cycles watt of white
light is 683 lm, EV100 6, so a frame shows the light the fitting would give), and the rooms are dressed with Poly Haven
(CC0) furniture.

    python3 spinoffs/barkhorn/companions/lamps_campaign.py                       # the shots
    python3 spinoffs/barkhorn/companions/lamps_campaign.py --render NAME [...] [--scale 0.3 --samples 32 --out DIR]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import hemisphere_brightness as HB                                  # noqa: E402
import lamps_final as LF                                            # noqa: E402
import lamps_pdp_r41 as P4                                          # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-campaign')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'lamps-campaign')
LM = 590.0                    # Hemisphere on its driver (round 42: ERP ESS010W-0180-42, 180 mA)
MANTLE = 'spinoffs/barkhorn/companions/out-turntable-float/open/barkhorn-turntable-float-open.json'


def asset(model, pos, rot=0.0, scale=1.0):
    return {'kind': 'kit', 'shape': 'asset', 'model': model, 'position': list(pos), 'rotate': [0, 0, rot], 'scale': scale}


def kit(shape, material, color, pos, **kw):
    return dict({'kind': 'kit', 'shape': shape, 'material': material, 'color': color, 'position': list(pos)}, **kw)


def dining_room(level='575', shade='ember'):
    """The brightness study's room at the design's light, its table swapped for a scanned dining table and chairs, a
    window in the left wall onto dusk."""
    s = HB.shot(level, shade)
    s['lights']['cob']['power_w'] = round(s['lights']['cob']['power_w'] * LM / HB.LEVELS[level], 4)
    st = s['set']
    tx, ty = HB.TABLE
    for p in st['props']:
        if p.get('fn') == 'dome':
            p['shade_glow'] = 0.3                    # critic c1 (both): 0.8 clipped the shell to a flat pink
            p['materials'] = {'liner': {'glow_color': '#FFB070'}}
        if p.get('kind') == 'lamp':
            p['off'] = True                           # the floor lamp competed with the pendant
        if p.get('material') == 'glow' and p.get('emit') == 1.4:
            p['emit'] = 0.45                          # critic c2: the sconces outshone the pendant
        if p.get('shape') == 'lathe' and p.get('material') == 'glass':
            # critic c4: a hollow bowl (the closed profile drew a solid lens)
            p['profile'] = [[0, 0], [0.035, 0], [0.035, 0.004], [0.004, 0.012], [0.004, 0.1], [0.038, 0.13],
                            [0.042, 0.19], [0.0405, 0.19], [0.0365, 0.132], [0.003, 0.104], [0.0, 0.104]]
        if p.get('shape') == 'cylinder' and p.get('material') == 'gloss' and p.get('radius') == 0.135:
            # critic c7: a dinner plate (a well and a rim), not a puck
            z = p['position'][2]
            p.update(shape='lathe', profile=[[0, 0], [0.09, 0], [0.095, 0.004], [0.13, 0.012], [0.135, 0.016],
                                             [0.132, 0.017], [0.093, 0.006], [0.0, 0.003]])
            p.pop('radius', None); p.pop('height', None)
            p['position'] = [p['position'][0], p['position'][1], z]
            p['color'] = '#E6E0D6'
    st['props'] += [asset('dining_chair_02', (tx - 0.42, ty - 0.68, 0.0), 0.0),
                    asset('dining_chair_02', (tx + 0.42, ty - 0.68, 0.0), 0.0),
                    asset('dining_chair_02', (tx - 0.42, ty + 0.68, 0.0), 180.0),
                    asset('dining_chair_02', (tx + 0.42, ty + 0.68, 0.0), 180.0),
                    asset('potted_plant_02', (-2.05, 2.75, 0.0), 30.0)]
    st['windows'] = [{'wall': 'left', 'along': 0.1, 'sill': 0.55, 'size': [1.7, 1.85], 'mullions': [2, 1],
                      'frame': '#2A2724'}]
    st['frame'] = '#2A2724'
    s['sky'] = {'kind': 'hdri', 'polyhaven': 'twilight_sunset', 'rotation_deg': 250.0, 'strength': 0.05, 'res': '4k'}
    s['render']['exposure'] = round(s['render']['exposure'] + 1.3, 3)     # a photographer's dusk, over a stop up
    s['render']['white_balance_k'] = 3300     # critics c4/c5: 4000 made the room one orange (the pink was the glow)
    s['lights'].pop('floorlamp', None)       # critic c3: its pools on the walls had no source
    # critic c2/c8: a soft panel seen only in the black top's reflection, so its tiers read against the wall
    tx, ty = HB.TABLE
    s['lights']['toprim'] = {'type': 'area', 'size_m': [0.5, 0.3], 'position': [-0.6, 0.6, 1.95],
                             'target': [tx, ty, 1.5], 'irradiance': 1.2, 'color': 3200, 'camera': False,
                             'specular': 1.0, 'diffuse': 0.0}
    return s


def dining_dusk():
    s = dining_room()
    s['title'] = 'Hemisphere in Ember over a dining table at dusk, at 590 lm (the campaign)'
    s['size'] = [2400, 1600]
    s['set']['props'] = [p for p in s['set']['props'] if not (p.get('model') == 'dining_chair_02'
                                                             and p['position'][0] > 0 and p['position'][1] < 0.5)]
    s['camera'] = {'position': [1.4, -0.65, 1.62], 'target': [-0.2, 1.1, 1.1], 'lens_mm': 32, 'level': True,
                   'fstop': 3.2, 'focus': [0.0, 0.95, 1.3]}
    s['set']['wall'] = {'color': '#8C8476'}
    return s


def box(material, color, size, pos, **kw):
    return kit('box', material, color, pos, size=list(size), **kw)


def bare_room(wall='#8C8476', floor=None):
    """The brightness study's room, emptied: no table, no pendant, no candles, its walls repainted; the sconces off."""
    s = HB.shot('575', 'ember')
    st = s['set']
    st['props'] = [p for p in st['props'] if p.get('kind') in ('frame',)]
    st['wall'] = {'color': wall}
    if floor:
        st['floor'] = floor
    s['lights'] = {}
    return s


def core_pool(s, x, y, z, flavour_light='#FF8A60', lm=200.0):
    for i, dx in enumerate((-0.095, 0.095)):
        s['lights'][f'corepool{i}'] = {'type': 'point', 'position': [x + dx, y - 0.02, z + 0.06],
                                       'power_w': round(lm * 0.25 / HB.LM_PER_W, 4), 'radius_m': 0.03,
                                       'color': flavour_light, 'camera': False, 'transmission': False, 'specular': 0.0}
    s['lights']['coreup'] = {'type': 'point', 'position': [x, y, z + 0.30], 'power_w': round(lm * 0.35 / HB.LM_PER_W, 4),
                             'radius_m': 0.08, 'color': flavour_light, 'camera': False, 'transmission': False,
                             'specular': 0.0}


def core_bedside():
    """Core in Ember on a bedside table at night: the only light in the room but a cool window."""
    s = bare_room(wall='#5A5248')                 # a warm neutral (the blue-grey went purple under the red)
    st = s['set']
    bx, by = 0.55, 2.05                      # the bed's centre: its head at the back wall (y 3.15)
    st['props'] = [
        box('gloss', '#3A2A1E', (1.72, 2.1, 0.30), (bx, by, 0.0), roughness=0.55),
        box('pbr', '#D9D3C8', (1.62, 2.0, 0.22), (bx, by, 0.30), texture='rough_linen', tex_scale=0.6, tint='#CFC6B6',
            tint_mix=0.6),
        box('pbr', '#6E7684', (1.84, 1.50, 0.30), (bx, by - 0.28, 0.24), texture='rough_linen', tex_scale=0.6,
            tint='#5E6470', tint_mix=0.7),      # the duvet, over the sides
        box('pbr', '#F2EFE9', (0.62, 0.40, 0.15), (bx - 0.38, 2.86, 0.52), rotate_z=4, texture='rough_linen',
            tex_scale=0.5, tint='#E4DDD0', tint_mix=0.5),
        box('pbr', '#F2EFE9', (0.62, 0.40, 0.15), (bx + 0.38, 2.86, 0.52), rotate_z=-3, texture='rough_linen',
            tex_scale=0.5, tint='#E4DDD0', tint_mix=0.5),
        box('gloss', '#3A2A1E', (1.84, 0.06, 1.05), (bx, 3.10, 0.0), roughness=0.55),
        asset('side_table_01', (-0.62, 2.82, 0.0), 0.0),
        box('paper', '#2B3A4A', (0.15, 0.21, 0.022), (-0.44, 2.74, 0.55), rotate_z=14),
        box('paper', '#B8873C', (0.14, 0.20, 0.018), (-0.44, 2.74, 0.572), rotate_z=4),
        LF.core_piece(-0.64, 2.86, 0.55, 'ember', glow=0.06, rotate_z=-30),
        {'kind': 'frame', 'position': [bx, 3.15], 'z': 1.55, 'size': [0.9, 0.6], 'art': '#2E3C52'},
    ]
    st['windows'] = [{'wall': 'left', 'along': -0.4, 'sill': 0.75, 'size': [1.1, 1.5], 'mullions': [1, 1],
                      'frame': '#1E2024'}]
    s['sky'] = {'kind': 'gradient', 'zenith': '#1A2A48', 'horizon': '#3A4A6A', 'ground': '#141820', 'strength': 0.05}
    core_pool(s, -0.64, 2.86, 0.55)
    s['render']['exposure'] = round(s['render']['exposure'] + 0.4, 3)
    s['render']['white_balance_k'] = 3500
    s['render']['white_balance_tint'] = 4
    s['title'] = 'Core in Ember on a bedside table at night (the campaign)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [-1.10, 1.85, 0.78], 'target': [-0.50, 2.90, 0.64], 'lens_mm': 60, 'level': True,
                   'fstop': 2.0, 'focus': [-0.64, 2.86, 0.68]}
    # critic r1 (5.5): c1 exposure -0.7 (the ball's centre clipped salmon); c2 moonlight, sky 0.006 to 0.05; c3 a warm
    # reflection-only card on the base; c6 a cool rim on the clear shell. c4 (modelled books) and c5 (a glass) are
    # props this set lacks: the glass was taken out after it rendered as a blur
    s['lights']['basecard'] = {'type': 'panel', 'size_m': [0.25, 0.1], 'position': [-0.95, 2.35, 0.6],
                               'target': [-0.64, 2.86, 0.565], 'strength': 0.2, 'color': '#FFB08A',
                               'ramp': {'axis': 'x', 'at_m': [-1.07, -0.83], 'values': [0, 1]}}
    s['lights']['rimcard'] = {'type': 'panel', 'size_m': [0.15, 0.5], 'position': [-0.95, 3.15, 0.75],
                              'target': [-0.64, 2.86, 0.66], 'strength': 0.3, 'color': '#C8D4F0',
                              'ramp': {'axis': 'z', 'at_m': [0.55, 0.95], 'values': [0.2, 1.0]}}
    return s


def mantle_product(x, y, z, flavour='ember', rot=0.0):
    return {'def': MANTLE, 'flavour': flavour, 'hide': [], 'instances': [{'position': [x, y, z], 'rotate_z': rot}]}


def record(x, y, z):
    """A record on the platter (as Mantle's finals: the disc and its label)."""
    return [kit('cylinder', 'gloss', '#0C0C0D', (x - 0.025, y - 0.012, z + 0.113), radius=0.1505, height=0.0018,
                roughness=0.22),
            kit('cylinder', 'paper', '#C8402A', (x - 0.025, y - 0.012, z + 0.1148), radius=0.05, height=0.0003)]


def sleeves(x, y, z, n=9, seed=3):
    import random
    rnd = random.Random(seed)
    cols = ['#CFC4AE', '#B23A28', '#D8D2C4', '#2C4A6A', '#E0B040', '#5A6E4A', '#E8E4DC', '#7A3A5A', '#3A3A3A']
    out = [box('gloss', '#3A2A1E', (0.34, 0.36, 0.012), (x, y, z), roughness=0.5)]
    for i in range(n):
        out.append(box('card', cols[i % len(cols)], (0.315, 0.004, 0.315), (x, y - 0.15 + i * 0.033, z + 0.012),
                       rotate_x=rnd.uniform(-7, -2)))
    return out


CRED = (0.25, 2.79, 0.68)          # the credenza's top centre (modern_wooden_cabinet, 2.44 x 0.68 x 0.68)


def credenza_props():
    cx, cy, cz = CRED
    return [asset('modern_wooden_cabinet', (cx, cy, 0.0), 0.0),
            asset('potted_plant_02', (cx + 1.55, cy - 0.05, 0.0), 20.0),
            asset('ceramic_vase_01', (cx + 0.95, cy + 0.05, cz), 0.0),
            {'kind': 'frame', 'position': [cx - 0.1, 3.15], 'z': 1.62, 'size': [1.0, 0.7], 'art': '#B4432E'},
            *sleeves(cx + 0.62, cy + 0.02, cz)]


def mantle_credenza():
    """Mantle in Ember on a walnut credenza in the evening, a record on, a crate of sleeves beside it, its base lit."""
    s = bare_room(wall='#857B6C')
    cx, cy, cz = CRED
    mx = cx - 0.45
    # critic r1 (5.0): c7 the cut picture frame out; c1 the glow 2.5 (5 clipped pink-white)
    s['set']['props'] = [p for p in credenza_props() if p.get('kind') != 'frame'] + record(mx, cy, cz)
    s['product'] = mantle_product(mx, cy - 0.02, cz)
    s['materials'] = {'glow': {'strength': 1.4}}
    s['set']['windows'] = [{'wall': 'left', 'along': 0.6, 'sill': 0.6, 'size': [1.4, 1.8], 'mullions': [2, 1],
                            'frame': '#2A2724'}]
    s['sky'] = {'kind': 'hdri', 'polyhaven': 'twilight_sunset', 'rotation_deg': 250.0, 'strength': 0.03, 'res': '4k'}
    s['lights'] = {
        'key': {'type': 'area', 'size_m': [1.2, 1.2], 'position': [-1.2, 1.0, 2.2], 'target': [mx, cy, cz + 0.1],
                'power_w': round(450 / HB.LM_PER_W, 4), 'color': 2900, 'camera': False},
        'sconce': {'type': 'point', 'position': [1.6, 3.0, 1.7], 'power_w': 0.18, 'radius_m': 0.03, 'color': 2400,
                   'camera': False},
        'fill': {'type': 'area', 'size_m': [2.0, 1.0], 'position': [0.4, -0.8, 1.6], 'target': [mx, cy, cz],
                 'power_w': 1.0, 'color': 3400, 'camera': False, 'specular': 0.3},             # c2: the plinth reads
        'records': {'type': 'area', 'size_m': [0.5, 0.5], 'position': [1.3, 1.9, 1.3],             # c4: the sleeves lit
                    'target': [cx + 0.62, cy, cz + 0.17], 'power_w': 0.12, 'color': 2900, 'camera': False},
        'lidpanel': {'type': 'area', 'size_m': [1.6, 0.9], 'position': [-0.82, 1.73, 1.47],       # c6: the lid reads clear
                     'target': [mx, 3.0, 1.0], 'irradiance': 0.25, 'color': '#FFE8D0', 'camera': False,
                     'specular': 1.0, 'diffuse': 0.0},
    }
    s['render']['exposure'] = round(s['render']['exposure'] + 1.2, 3)
    s['render']['white_balance_k'] = 3300                                                  # c5: the wall cream, not olive
    # critic r2 (5.5): c1 the front sleeve cream (the records a black slab); c2 tint 2 (magenta); c3 glow 1.4 (the edge
    # pink-white); c4 the lid's panel larger (a hard blotch); c5 fill 1.0 W (the deck crushed); c6 the frame right
    # (the records against the edge); c7 the finish pass not run (PIL missing in the render Python); c8 sleeve art: an asset
    s['render']['white_balance_tint'] = 2
    s['title'] = 'Mantle in Ember on a credenza in the evening, a record on (the campaign)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [mx + 0.85, cy - 1.65, 1.25], 'target': [mx + 0.43, cy, cz + 0.12], 'lens_mm': 32,
                   'level': True, 'fstop': 4.0, 'focus': [mx, cy, cz + 0.1]}
    return s


def one_room():
    """All three in one room at dusk: Hemisphere over the dining table, Mantle and Core on the credenza behind it."""
    s = dining_room()
    cx, cy, cz = CRED
    st = s['set']
    st['props'] = [p for p in st['props'] if p.get('kind') not in ('sideboard', 'frame') and
                   not (p.get('material') == 'glow' or (p.get('position') or [0, 0, 0])[1] > 2.5 and p.get('kind') == 'kit'
                        and p.get('shape') == 'cylinder')]
    mx = cx - 0.55
    st['props'] += credenza_props() + record(mx, cy, cz) + [LF.core_piece(cx + 0.98, cy - 0.02, cz, 'smoke', glow=0.3,
                                                                          rotate_z=-20)]
    s['product'] = mantle_product(mx, cy - 0.02, cz)
    s['materials'] = {'glow': {'strength': 5.0}}
    s['render']['exposure'] = round(s['render']['exposure'] + 0.8, 3)
    for k in ('sconce1', 'sconce2', 'candle1', 'candle2'):
        s['lights'].pop(k, None)
    core_pool(s, cx + 0.98, cy - 0.02, cz, flavour_light='#E8D8C8')
    s['title'] = 'Hemisphere, Core and Mantle in one room at dusk (the campaign)'
    s['size'] = [2400, 1600]
    s['camera'] = {'position': [1.75, -1.45, 1.45], 'target': [-0.15, 1.75, 1.0], 'lens_mm': 28, 'level': True,
                   'fstop': 5.6, 'focus': [0.0, 1.4, 1.0]}
    return s


def macro_dome():
    """Hemisphere's low top, close: the clamp ring, the crown, the cap, the tint's edge."""
    s = P4.dome('ember')
    z = s['product']['instances'][0]['position'][2]
    s['title'] = 'Hemisphere in Ember, the low top close (the campaign)'
    s['size'] = [2000, 1600]
    s['camera'] = {'position': [0.30, -0.42, z + 0.22], 'target': [0.0, 0.0, z + 0.09], 'lens_mm': 100, 'level': False,
                   'fstop': 5.6, 'focus': [0.0, -0.06, z + 0.10]}
    return s


def macro_core():
    """Core in Ember, close at its base: the touch ring, the ball in its cup, the polished black base."""
    s = P4.orb('ember')
    z = s['product']['instances'][0]['position'][2]
    s['title'] = 'Core in Ember, its base close (the campaign)'
    s['size'] = [2000, 1600]
    # critic r1 (4.5): c1/c2 f/13, focus on the ring's lip (all soft); c3 exposure -0.35 (the red on the shoulder);
    # c4 the key halved, c5 the dome 0.12 (the ball lit, not glowing); c6 a reflection-only strip on the base; c7 80 mm
    # (the base's foot cut)
    s['camera'] = {'position': [0.20, -0.36, z + 0.10], 'target': [0.0, 0.0, z + 0.05], 'lens_mm': 80, 'level': False,
                   'fstop': 13, 'focus': [0.0, -0.045, z + 0.055]}
    s['render']['exposure'] = round(s['render']['exposure'] - 0.35, 3)
    s['lights']['key']['irradiance'] = 0.3
    s['sky']['strength'] = 0.12
    s['lights']['basestrip'] = {'type': 'panel', 'size_m': [0.08, 0.3], 'position': [-0.22, -0.3, z + 0.03],
                                'target': [0.0, 0.0, z + 0.02], 'strength': 4.0, 'color': '#FFFFFF',
                                'ramp': {'axis': 'z', 'at_m': [z - 0.09, z + 0.16], 'values': [0.2, 1.0]}}
    return s


def dining_close():
    """Hemisphere close over the table at dusk: the shade, its pool on the cloth and the glasses, the window behind."""
    s = dining_room()
    s['title'] = 'Hemisphere in Ember, close over the table at dusk (the campaign)'
    s['size'] = [1600, 2000]
    tx, ty = HB.TABLE
    for p in s['set']['props']:                # critic c8: the right glass off the frame's edge
        if p.get('shape') == 'lathe' and p.get('material') == 'glass' and p['position'][0] > 0.1:
            p['position'] = [0.05, p['position'][1], p['position'][2]]
    s['camera'] = {'position': [tx + 0.75, ty - 0.85, 1.30], 'target': [tx - 0.25, ty + 0.15, 1.34], 'lens_mm': 55,
                   'level': True, 'fstop': 2.8, 'focus': [tx, ty, 1.47]}
    return s


GLASS = [[0, 0], [0.035, 0], [0.035, 0.004], [0.004, 0.012], [0.004, 0.1], [0.038, 0.13], [0.042, 0.19],
         [0.0405, 0.19], [0.0365, 0.132], [0.003, 0.104], [0.0, 0.104]]
PLATE = [[0, 0], [0.09, 0], [0.095, 0.004], [0.13, 0.012], [0.135, 0.016], [0.132, 0.017], [0.093, 0.006], [0.0, 0.003]]


def dining_hero():
    """Round 2, the coordinator's art direction (2026-10-31: the bar is Louis Poulsen's, Flos's, Apparatus's campaign
    pictures): the lamp large in the upper third and its light the light; a solid walnut table, a linen runner, one
    ceramic plate, one glass; no chairs, sconces or candles; the window deep blue dusk, out of focus; the neutrals warm
    and quiet so the Ember shade is the only saturated colour. Portrait."""
    s = HB.shot('575', 'ember')
    s['lights'] = {'cob': s['lights']['cob']}
    s['lights']['cob']['power_w'] = round(s['lights']['cob']['power_w'] * LM / HB.LEVELS['575'], 4)
    tx, ty = HB.TABLE
    st = s['set']
    dome = [p for p in st['props'] if p.get('fn') == 'dome'][0]
    dome['shade_glow'] = 0.15
    dome['materials'] = {'liner': {'glow_color': '#FFB070'}}
    walnut = {'material': 'pbr', 'texture': 'american_walnut_veneer', 'tex_scale': 1.0, 'rough_mul': 0.8, 'tint': '#3A2416', 'tint_mix': 0.62}
    top_z = HB.TABLE_Z
    st['props'] = [
        dome,
        kit('box', 'pbr', '#6B4A30', (tx, ty, top_z - 0.04), size=[1.9, 0.95, 0.04], **{k: v for k, v in walnut.items() if k != 'material'}),
        *[kit('box', 'pbr', '#6B4A30', (tx + sx * 0.82, ty + sy * 0.38, 0.0), size=[0.06, 0.06, top_z - 0.04],
              **{k: v for k, v in walnut.items() if k != 'material'}) for sx in (-1, 1) for sy in (-1, 1)],
        kit('box', 'pbr', '#B8AD9B', (tx, ty, top_z), size=[1.7, 0.38, 0.003], texture='rough_linen', tex_scale=0.5,
            tint='#A99E8C', tint_mix=0.7),
        kit('lathe', 'gloss', '#E4DED3', (tx - 0.22, ty - 0.02, top_z + 0.003), profile=PLATE, roughness=0.35),
        kit('lathe', 'glass', '#F4F2EE', (tx + 0.02, ty + 0.16, top_z + 0.003), profile=GLASS),
        asset('food_pears_asian_01', (tx - 0.20, ty - 0.02, top_z + 0.008), 30.0),
        asset('potted_plant_02', (-2.05, 2.75, 0.0), 30.0),
    ]
    st['wall'] = {'color': '#8A8276'}
    st['floor'] = {'plank_w': 0.16, 'plank_l': 1.8, 'base': '#4E3A2A', 'dark': '#3E2E20', 'light': '#5A4432',
                   'plank_contrast': 0.6}
    st['windows'] = [{'wall': 'left', 'along': 0.1, 'sill': 0.55, 'size': [1.7, 1.85], 'mullions': [2, 1],
                      'frame': '#2A2724'}]
    st['frame'] = '#2A2724'
    s['sky'] = {'kind': 'gradient', 'zenith': '#0E1A33', 'horizon': '#2C4670', 'ground': '#131A26', 'strength': 0.08}
    s['lights']['toprim'] = {'type': 'area', 'size_m': [0.5, 0.3], 'position': [-0.6, 0.6, 1.95], 'target': [tx, ty, 1.5],
                             'irradiance': 3.0, 'color': 3200, 'camera': False, 'specular': 1.0, 'diffuse': 0.0}
    # critic r1 (4.5): c1 exposure down 0.8 (the runner and the shade sat on the shoulder: no pool, a salmon dome);
    # c2 a warm fill on the walls only, so the room exists and the black top separates; c5 less magenta
    # critic r2 (5.0): c1 sky 0.08 (the room a void), c2 glow 0.15 (the dome salmon), c3 exposure back 0.5 (the runner
    # on the shoulder), c4 walnut tint 0.62, c5 the top's rim 3.0, c6 a warm bounce for the glass, c7 3000 K
    s['render']['exposure'] = round(s['render']['exposure'] + 0.0, 3)
    s['render']['white_balance_k'] = 3000
    s['render']['white_balance_tint'] = 5
    s['lights']['wallfill'] = {'type': 'area', 'size_m': [1.5, 1.0], 'position': [1.0, -0.5, 2.3],
                               'target': [-0.6, 3.15, 1.5], 'power_w': 3.0, 'color': 2700, 'specular': 0.0,
                               'diffuse': 1.0, 'camera': False, 'receivers': ['wall-*', 'ceiling']}
    s['lights']['bounce'] = {'type': 'flag', 'size_m': [1.0, 0.6], 'position': [tx + 1.3, ty - 0.45, top_z + 0.2],
                             'target': [tx, ty, top_z + 0.1], 'color': '#E8E0D4'}
    s['title'] = 'Hemisphere in Ember over a walnut table at dusk (the campaign, round 2)'
    s['size'] = [1600, 2000]
    s['camera'] = {'position': [tx + 0.85, ty - 1.25, 1.62], 'target': [tx - 0.04, ty + 0.05, 1.12], 'lens_mm': 66,
                   'level': False, 'fstop': 2.8, 'focus': [tx, ty, 1.45]}
    return s


BUILD = {'dining-hero': dining_hero, 'dining-dusk': dining_dusk, 'dining-close': dining_close, 'core-bedside': core_bedside, 'mantle-credenza': mantle_credenza,
         'one-room': one_room, 'macro-hemisphere': macro_dome, 'macro-core': macro_core}


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in BUILD.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    print(len(BUILD), 'shots in', os.path.relpath(SHOTS, ROOT), flush=True)
    if '--render' in sys.argv:
        a = sys.argv[sys.argv.index('--render') + 1:]
        want = [x for x in a if x in BUILD] or list(BUILD)
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        extra = []
        for k in ('--scale', '--samples'):
            if k in a:
                extra += [k, a[a.index(k) + 1]]
        os.makedirs(out, exist_ok=True)
        for n in want:
            subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                            '--out', os.path.join(out, n + '.png')] + extra, cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', n, flush=True)


if __name__ == '__main__':
    main()
