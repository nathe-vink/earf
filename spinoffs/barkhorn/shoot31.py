"""Round 31's new pictures of the speakers, written as shot files for studio/engine/render.py (the owner: "let's try
out different product shot ideas, like what would the speakers look like in a black room when a spotlight shining
down on them, or light passing through them as they pass by on a carousel of sorts, so it casts each color. There's
lots of cool things we can do, and we should do them").

- spot-<colour>: one speaker, cover off, alone in a black room under a single spot from above, through a faint haze
  (the engine's `haze`, round 31) so the beam shows as a cone and the floor takes a pool of light and the cabinet's
  colour.
- carousel-<nn>: the eight on a turning plinth, a hard light low on one side shining through each as it passes, so
  every colour in turn crosses the floor and the wall; the eight are 45 degrees apart, so 45 degrees of turn loops.

    python3 spinoffs/barkhorn/shoot31.py      ->  studio/shots/barkhorn/shoot31/*.json
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'shoot31')
BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lookbook21', 'look-amber-on.json')
FLAVOUR = {'red': 'cloud-red', 'orange': 'cloud-orange', 'amber': 'cloud-amber', 'green': 'eucalyptus-y2k-green',
           'blue': 'cloud-blue', 'violet': 'cloud-violet', 'ice': 'birch-fog-clear', 'black': 'cloud-black'}
KEYS = list(FLAVOUR)
BLACK = '#4A4A50'                                        # a grey floor and wall: the room is black because no light reaches it, the pool shows


def spot(key):
    """One speaker under one spot in a black room."""
    s = copy.deepcopy(json.load(open(BASE)))
    s['product'] = {'def': 'studio/products/barkhorn-cloud.json', 'flavour': FLAVOUR[key],
                    'instances': [{'flavour': FLAVOUR[key], 'position': [0, 0, 0], 'rotate_z': -18, 'hide': ['cloth-disc']}]}
    s['set'] = {'kind': 'sweep', 'color': BLACK, 'width': 14.0, 'front': 8.0, 'depth': 6.0, 'radius': 2.0, 'height': 7.0}
    s['sky'] = {'kind': 'none'}
    s['lights'] = {
        # the spot: straight down from 4 m, a touch in front so the face catches it, a 24 degree cone softening at its edge
        'spot': {'type': 'spot', 'position': [0.0, -0.45, 4.2], 'target': [0.0, 0.0, 0.6], 'cone_deg': 24, 'blend': 0.35,
                 'radius_m': 0.04, 'power_w': 4800.0, 'color': '#FFF3E2'},
        # a breath of light from the front, so the face is not lost (a hundredth of the spot)
        'breath': {'type': 'area', 'size_m': [2.0, 1.2], 'orbit': {'azimuth_deg': -10, 'elevation_deg': 12, 'distance_m': 5.0},
                   'target': [0.0, 0.0, 0.6], 'irradiance': 0.09, 'color': '#E8EEFF'}}
    s['haze'] = {'box_m': [-6.0, -8.0, -0.05, 6.0, 5.5, 6.5], 'density': 0.025, 'anisotropy': 0.25}   # under the floor and short of the wall: a face of it on the floor hid the pool
    s['camera'] = {'position': [0.8, -3.7, 1.45], 'target': [0.0, 0.0, 0.8], 'lens_mm': 50.0, 'level': True}
    s['size'] = [1200, 1600]
    s['title'] = f'barkhorn, {key}, under a spotlight'
    s['render'] = {**s['render'], 'samples': 128, 'exposure': 0.0, 'clamp': 6}
    return s


FRAMES, TURN = 32, 45.0                                  # the carousel's loop: 45 degrees in 32 frames (2 s at 16 fps)
C, R = (0.0, 0.6), 1.95                                  # its centre and the circle the speakers stand on (m)


def carousel(frame):
    """The eight on a turning white plinth, facing out, under one low hard sun from behind and to the right: light
    passes through each cabinet and horn and lays a long shadow in its colour across the plinth, and as the plinth
    turns the eight colours sweep round like the hands of a clock."""
    s = copy.deepcopy(json.load(open(BASE)))
    a0 = -TURN * frame / FRAMES                          # turning anticlockwise seen from above, 45 degrees a loop
    insts = []
    for i, k in enumerate(KEYS):
        th = a0 + 45.0 * i + 22.5                         # spectrum order round the circle
        t = math.radians(th)
        insts.append({'flavour': FLAVOUR[k], 'position': [round(C[0] + R * math.sin(t), 4), round(C[1] - R * math.cos(t), 4), 0.1],
                      'rotate_z': round(th, 3), 'hide': ['cloth-disc']})
    s['product'] = {'def': 'studio/products/barkhorn-cloud.json', 'flavour': FLAVOUR[KEYS[0]], 'instances': insts}
    # a long low sweep: a tall back wall would stand between the low sun and the plinth
    s['set'] = {'kind': 'sweep', 'color': '#E7E2D8', 'width': 40.0, 'front': 14.0, 'depth': 22.0, 'radius': 0.4, 'height': 0.6,
                'props': [{'kind': 'plinth', 'position': list(C), 'radius': 2.7, 'height': 0.1, 'color': '#F2EEE7'}]}
    s['sky'] = {'kind': 'gradient', 'zenith': '#BFC3C8', 'horizon': '#D2D2D0', 'ground': '#6A665F', 'strength': 0.35}
    # the sun low behind (azimuth 0 is from the camera's side), so the light through each horn runs toward the camera
    s['sun'] = {'azimuth_deg': 172.0, 'elevation_deg': 15.0, 'irradiance': 10.0, 'size_deg': 0.5, 'color': '#FFF0DA'}
    s['lights'] = {
        'fill': {'type': 'area', 'size_m': [6.0, 3.0], 'orbit': {'azimuth_deg': -15, 'elevation_deg': 22, 'distance_m': 10.0},
                 'target': [0.0, 0.6, 0.6], 'irradiance': 0.2, 'color': '#F4F6FF'}}
    s.pop('haze', None)
    s['camera'] = {'position': [0.5, -7.8, 4.3], 'target': [0.0, -0.3, 0.1], 'lens_mm': 33.0, 'level': False}
    s['size'] = [1280, 720]
    s['title'] = f'barkhorn, the carousel, frame {frame:02d} of {FRAMES}'
    s['render'] = {**s['render'], 'samples': 48, 'exposure': 0.0, 'clamp': 6}
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for k in KEYS:
        f = os.path.join(OUT, f'spot-{k}.json')
        json.dump(spot(k), open(f, 'w'), indent=1)
        made.append(os.path.relpath(f, ROOT))
    for i in range(FRAMES):
        f = os.path.join(OUT, f'carousel-{i:02d}.json')
        json.dump(carousel(i), open(f, 'w'), indent=1)
        made.append(os.path.relpath(f, ROOT))
    print(len(made), 'shots, e.g.', made[0], made[-1])


if __name__ == '__main__':
    main()
