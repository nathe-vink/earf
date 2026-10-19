"""Moon's frames (round 32): the table lamp and the pendant placed by Planet's own kit piece (studio/engine/kit_ext/
earf_moon.py), so the frames test what Planet imports: in a bar (a fir table, board-formed concrete, 2700 K, dim) and
on a seamless.

    python3 spinoffs/barkhorn/companions/moon_shots.py            # write the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/moon_shots.py --render [names] [--scale 0.6]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'moon')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'moon')

TABLE_Z = 0.76         # the table's top
PEND_Z = 1.30          # the pendant's rim
VIEWS = [('bar', 'smoked'), ('bar', 'ember'), ('seamless', 'frosted'), ('seamless', 'haze')]


def moon(fn, spots, colour, bar, **k):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': fn, 'spots': spots, 'flavour': colour,
            'shade_glow': 0.6 if bar else 0.8, **k}


def back_bar():
    """Out of focus behind the table (critic moon-p1 c4): a back bar 1.7 m back, a shelf of bottles, three candles."""
    import random
    rnd = random.Random(5)
    Y = 1.75
    props = [{'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'brown_planks_09', 'res': '1k', 'color': '#3A2A1E',
              'size': [3.0, 0.5, 1.02], 'position': [0.3, Y, 0.0]},
             {'kind': 'kit', 'shape': 'box', 'material': 'gloss', 'color': '#1C1A18', 'size': [3.0, 0.22, 0.03],
              'position': [0.3, Y + 0.12, 1.42]}]
    amber = ['#8A4A14', '#5A3A18', '#2E3A22', '#B07A30', '#6A2A16', '#C8B89A']
    for shelf_z, xs in ((1.45, [-0.5 + 0.11 * i for i in range(16)]), (1.02, [0.15, 0.27, 0.36, 0.9, 1.02])):
        for x in xs:
            # p2 c5: grouped with gaps, none behind the pendant, and the shapes varied (a squat, a tall neck, a decanter)
            if rnd.random() < 0.3 or (shelf_z > 1.2 and 0.15 < x < 0.75):
                continue
            h = rnd.uniform(0.2, 0.34); r = rnd.uniform(0.03, 0.048); sh = rnd.uniform(0.45, 0.75); nk = rnd.uniform(0.009, 0.016)
            props.append({'kind': 'kit', 'shape': 'lathe', 'material': 'glass', 'color': rnd.choice(amber),
                          'profile': [[0.0, 0.0], [r, 0.0], [r, h * sh], [r * 0.45, h * (sh + 0.16)], [nk, h * (sh + 0.22)],
                                      [nk, h], [0.0, h]],
                          'position': [x, Y + 0.12 + rnd.uniform(-0.03, 0.03), shelf_z]})
    for x in (-0.35, 0.55, 1.2):
        props.append({'kind': 'kit', 'shape': 'cylinder', 'material': 'glass', 'color': '#B06A28', 'radius': 0.035,
                      'height': 0.08, 'position': [x, Y - 0.1, 1.02]})
        props.append({'kind': 'kit', 'shape': 'sphere', 'material': 'glow', 'color': '#FF9A40', 'emit': 40.0,
                      'scale': [0.006, 0.006, 0.012], 'position': [x, Y - 0.1, 1.09]})
    lights = {f'candle{i}': {'type': 'point', 'position': [x, Y - 0.1, 1.12], 'power_w': 0.6, 'radius_m': 0.01, 'color': 1900,
                             'camera': False} for i, x in enumerate((-0.35, 0.55, 1.2))}
    lights['shelf'] = {'type': 'area', 'size_m': [2.4, 0.04], 'position': [0.3, Y + 0.05, 1.70], 'target': [0.3, Y + 0.15, 1.4],
                       'irradiance': 0.6, 'color': 2400, 'camera': False}
    return props, lights


def shot(where, colour):
    bar = where == 'bar'
    tx, ty = -0.12, 0.0
    px, py = 0.26, 0.18
    if bar:                 # critic moon-p1 c8: lower and longer, the pair closer, the back bar compressed behind
        cam = {'position': [-0.30, -1.10, 1.00], 'target': [0.04, 0.05, 1.04], 'lens_mm': 50, 'level': True, 'fstop': 2.8,
               'focus': [tx, ty, TABLE_Z + 0.17]}               # p2 c7: tighter, the lamps larger
        tgt = cam['target']
    else:
        tgt = [0.06, 0.05, 1.08]
        cam = {'position': [-0.40, -1.20, 1.10], 'target': tgt, 'lens_mm': 45, 'level': True, 'fstop': 4.0,
               'focus': [tx, ty, TABLE_Z + 0.15]}
    s = {'title': f'Moon in {colour}, {where}', 'size': [900, 1000], 'camera': cam,
         'render': {'samples': 256, 'adaptive': 0.015, 'denoise': True, 'clamp': 8, 'bounces': 12,
                    'view': 'Khronos PBR Neutral', 'exposure': 0.6 if bar else 0.0, 'white_balance_k': 3600 if bar else 5200}}
    # the frost's own glow at 2700 K (critic moon-p1 c2: #FF9440 through a 3000 K balance read salmon)
    warm = {'shade': {'glow_color': '#FF9440'}} if bar and colour in ('clear', 'frosted', 'smoked') else {}
    lamps = [moon('table', [{'position': [tx, ty, TABLE_Z], 'rotate_z': 12}], colour, bar, lamp_w=14.0 if bar else 2.0,
                  materials=warm),
             moon('pendant', [[px, py, PEND_Z]], colour, bar, lamp_w=9.0 if bar else 6.0, materials=warm,
                  **({'shade_glow': 0.45} if bar else {}))]          # p2 c6: its underside clipped
    if bar:
        # a fir table that stands (c1): its top past both edges of the frame, four legs to a dark floor
        tw, td = 1.8, 0.75
        table = [{'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'brown_planks_09', 'res': '2k', 'color': '#6E4A2E',
                  'size': [tw, td, 0.045], 'position': [0.05, 0.05, TABLE_Z - 0.045]}]
        for sx in (-1, 1):
            for sy in (-1, 1):
                table.append({'kind': 'kit', 'shape': 'box', 'material': 'gloss', 'color': '#1A1817', 'roughness': 0.5,
                              'size': [0.05, 0.05, TABLE_Z - 0.045],
                              'position': [0.05 + sx * (tw / 2 - 0.08), 0.05 + sy * (td / 2 - 0.08), 0.0]})
        # a solid front, set back under the top's lip: the counter under the table read as a thick top (p2 draft)
        table.append({'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'brown_planks_09', 'res': '1k',
                      'color': '#2A1E16', 'size': [tw, 0.03, TABLE_Z - 0.045], 'position': [0.05, 0.05 - td / 2 + 0.05, 0.0]})
        bb, bb_lights = back_bar()
        s['set'] = {'kind': 'sweep', 'color': '#1E1A17', 'width': 8.0, 'front': 5.0, 'depth': 2.6, 'radius': 0.3, 'height': 4.0,
                    'props': [{'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'concrete_wall_008', 'res': '2k',
                               'color': '#7A7268', 'size': [5.0, 0.05, 3.2], 'position': [0.0, 2.45, 0.0]}]
                    + table + bb + lamps}
        s['sky'] = {'kind': 'gradient', 'zenith': '#1A1C22', 'horizon': '#24221F', 'ground': '#141210', 'strength': 0.25}
        s['lights'] = {'fill': {'type': 'area', 'size_m': [1.5, 1.2],
                                'orbit': {'azimuth_deg': -40, 'elevation_deg': 30, 'distance_m': 3.0},
                                'target': tgt, 'irradiance': 0.07, 'color': 2700},   # p2 c1: the lamp's own pool
                       # c3: a strip behind the column and a kicker over the disc, so light comes through the acrylic
                       # p2 c2, c3: tall and narrow straight behind the column; level with the disc behind it
                       'strip': {'type': 'area', 'size_m': [0.06, 0.30], 'position': [-0.07, 0.30, 0.86], 'target': [tx, ty, 0.86],
                                 'irradiance': 0.7, 'color': 2700, 'camera': False},
                       'kick': {'type': 'area', 'size_m': [0.4, 0.06], 'position': [px, 0.50, 1.36], 'target': [px, py, 1.33],
                                'irradiance': 0.3, 'color': 2700, 'camera': False},
                       # p2 c4: grazing down the concrete so its boards show
                       'wallwash': {'type': 'area', 'size_m': [3.0, 0.05], 'position': [0.3, 2.30, 2.7], 'target': [0.3, 2.45, 1.4],
                                    'irradiance': 0.35, 'color': 2400, 'camera': False}, **bb_lights}
    else:
        s['set'] = {'kind': 'sweep', 'color': '#D9D6D0', 'width': 8.0, 'front': 5.0, 'depth': 1.5, 'radius': 1.2, 'height': 4.0,
                    'props': [{'kind': 'kit', 'shape': 'box', 'material': 'felt', 'color': '#C9C4BC',
                               'size': [0.6, 0.45, TABLE_Z], 'position': [-0.12, 0.05, 0.0]}] + lamps}
        s['sky'] = {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': 0.7}
        s['lights'] = {'key': {'type': 'area', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': -35, 'elevation_deg': 42, 'distance_m': 3.0},
                               'target': tgt, 'irradiance': 1.8, 'color': '#FFF3E1'},
                       'fill': {'type': 'area', 'size_m': [2.5, 2.0], 'orbit': {'azimuth_deg': 35, 'elevation_deg': 18, 'distance_m': 3.0},
                                'target': tgt, 'irradiance': 0.7, 'color': '#FFF7EA'}}
    return s


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for where, colour in VIEWS:
        json.dump(shot(where, colour), open(os.path.join(SHOTS, f'{where}-{colour}.json'), 'w'), indent=1)
        print(where, colour)


def render(names, scale):
    py = os.environ.get('PY', 'python3')
    os.makedirs(RENDERS, exist_ok=True)
    for name in names:
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, name + '.json'),
                        '--out', os.path.join(RENDERS, name + '.png'), '--scale', str(scale)], check=True)
        print(name, flush=True)


if __name__ == '__main__':
    if '--render' in sys.argv:
        a = sys.argv[2:]
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 0.6
        names = [x for x in a if not x.startswith('--') and x != str(scale)] or [f'{w}-{c}' for w, c in VIEWS]
        render(names, scale)
    else:
        build()
