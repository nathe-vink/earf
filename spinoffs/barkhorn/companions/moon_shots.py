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
            'shade_glow': 1.0 if bar else 0.8, **k}


def shot(where, colour):
    bar = where == 'bar'
    tx, ty = -0.12, 0.0
    px, py = 0.26, 0.18
    tgt = [0.06, 0.05, 1.08]
    s = {'title': f'Moon in {colour}, {where}', 'size': [900, 1000],
         'camera': {'position': [-0.40, -1.20, 1.10], 'target': tgt, 'lens_mm': 45, 'level': True, 'fstop': 4.0,
                    'focus': [tx, ty, TABLE_Z + 0.15]},
         'render': {'samples': 256, 'adaptive': 0.015, 'denoise': True, 'clamp': 8, 'bounces': 12,
                    'view': 'Khronos PBR Neutral', 'exposure': 0.6 if bar else 0.0, 'white_balance_k': 3000 if bar else 5200}}
    # the frost's own glow at 2700 K: through the bar's 3000 K balance a paler one clipped to a blue-white
    warm = {'shade': {'glow_color': '#FF9440'}} if bar and colour in ('clear', 'frosted', 'smoked') else {}
    lamps = [moon('table', [{'position': [tx, ty, TABLE_Z], 'rotate_z': 12}], colour, bar, lamp_w=4.0 if bar else 2.0, materials=warm),
             moon('pendant', [[px, py, PEND_Z]], colour, bar, lamp_w=14.0 if bar else 6.0, materials=warm)]
    if bar:
        table_top = {'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'brown_planks_09', 'res': '2k',
                     'color': '#6E4A2E', 'size': [0.9, 0.7, 0.04], 'position': [-0.05, 0.05, TABLE_Z - 0.04]}
        s['set'] = {'kind': 'sweep', 'color': '#2B2724', 'width': 8.0, 'front': 5.0, 'depth': 1.5, 'radius': 0.6, 'height': 4.0,
                    'props': [{'kind': 'kit', 'shape': 'box', 'material': 'pbr', 'texture': 'concrete_wall_008', 'res': '2k',
                               'color': '#8C857C', 'size': [4.0, 0.05, 3.0], 'position': [0.0, 0.75, 0.0]}, table_top] + lamps}
        s['sky'] = {'kind': 'gradient', 'zenith': '#1A1C22', 'horizon': '#24221F', 'ground': '#141210', 'strength': 0.25}
        s['lights'] = {'fill': {'type': 'area', 'size_m': [1.5, 1.2],
                                'orbit': {'azimuth_deg': -40, 'elevation_deg': 30, 'distance_m': 3.0},
                                'target': tgt, 'irradiance': 0.14, 'color': 2700}}
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
