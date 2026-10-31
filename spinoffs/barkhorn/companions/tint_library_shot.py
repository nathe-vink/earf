"""The Tint Library's picture for the owner (round 43, 2026-10-31): the eight stepped chips standing in the birch tray in
the spectrum's order, the Smoke hood lifted off beside it, the particulars card in front. The coin's studio rig (the
sweep, a key, a fill, a back light and a rake; renders/2026-10-20/barkhorn/coin/eight), the stand-ins' estimated tints
(tint_library.STOCK_DEEP).

    python3 spinoffs/barkhorn/companions/tint_library_shot.py [--render [--scale S --samples N --out PATH]]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SHOT = os.path.join(ROOT, 'studio', 'shots', 'tint-library', 'library.json')
OUT = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'tint-library', 'library.png')
T = [0.0, 0.0, 0.035]                       # the chips' middle (m)


def shot():
    return {
        'title': 'The Tint Library: eight stepped chips in stock stand-ins, the birch tray, the Smoke hood lifted off',
        'size': [1600, 1067],
        'products': [
            {'def': 'studio/products/tint-library.json',
             'instances': [{'position': [0.0, 0.0, 0.0], 'rotate_z': 0, 'hide': ['hood-*']},
                           {'position': [0.15, 0.06, 0.0], 'rotate_z': 18, 'hide': ['tray', 'chip-*']}]},
        ],
        'set': {'kind': 'sweep', 'color': '#DDD8D0', 'width': 3.0, 'front': 2.0, 'depth': 0.8, 'radius': 0.5,
                'height': 2.0, 'props': [
                    # the particulars card, lying in front, a little turned
                    {'kind': 'kit', 'shape': 'box', 'material': 'paper', 'color': '#F1ECE2',
                     'position': [-0.03, -0.125, 0.0], 'size': [0.140, 0.095, 0.0008], 'rotate_z': -8}]},
        'sky': {'kind': 'gradient', 'zenith': '#D4D2CE', 'horizon': '#DCDAD5', 'ground': '#6A665F', 'strength': 0.6},
        'lights': {
            'key': {'type': 'area', 'size_m': [0.9, 0.7], 'orbit': {'azimuth_deg': -40, 'elevation_deg': 50,
                                                                    'distance_m': 1.2},
                    'target': T, 'irradiance': 0.9, 'color': '#FFF3E1'},
            'fill': {'type': 'area', 'size_m': [1.2, 1.0], 'orbit': {'azimuth_deg': 40, 'elevation_deg': 20,
                                                                     'distance_m': 1.4},
                     'target': T, 'irradiance': 0.3, 'color': '#FFF7EA'},
            # behind the chips, low: the light through them is what shows the tints
            'back': {'type': 'area', 'size_m': [0.8, 0.4], 'orbit': {'azimuth_deg': 175, 'elevation_deg': 18,
                                                                     'distance_m': 0.9},
                     'target': T, 'irradiance': 2.6, 'color': '#FFF7EA', 'camera': False},
        },
        'render': {'samples': 256, 'adaptive': 0.01, 'denoise': True, 'clamp': 10, 'bounces': 16,
                   'transmission_bounces': 24, 'view': 'Khronos PBR Neutral', 'exposure': 0.3,
                   'white_balance_k': 5400},
        'camera': {'position': [-0.36, -0.55, 0.45], 'target': [0.03, 0.0, 0.02], 'lens_mm': 70, 'level': False,
                   'fstop': 8.0, 'focus': [0.0, 0.0, 0.035]},
    }


def main():
    os.makedirs(os.path.dirname(SHOT), exist_ok=True)
    with open(SHOT, 'w') as f:
        json.dump(shot(), f, indent=1)
    print('wrote', os.path.relpath(SHOT, ROOT))
    a = sys.argv[1:]
    if '--render' in a:
        out = a[a.index('--out') + 1] if '--out' in a else OUT
        os.makedirs(os.path.dirname(out), exist_ok=True)
        extra = []
        for k in ('--scale', '--samples'):
            if k in a:
                extra += [k, a[a.index(k) + 1]]
        subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), SHOT, '--out', out] + extra,
                       cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
