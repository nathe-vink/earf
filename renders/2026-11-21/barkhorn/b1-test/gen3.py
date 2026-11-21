"""B1 fixed-2 with the bell's card (the coordinator, 10:00, step 2: only if the bell still reads black). The near horn's
waveguide mirrors itself and the dark ceiling beams (studio/engine/render.py --probe waveguide: 55 % itself, 21 % the
beams and the ceiling deck along azimuth 50-58 deg and elevation 18-23 deg from the horn, toward the room and up). On that
ray, 2.9 m from the near bell: `ceiling-panel`, a soft light panel hung under the ceiling at z 3.2 (x 10.5, y 4.0), facing
the bell. It is honest: diffuse and specular both at full, so it lights whatever it faces as well. Behind and right of
the camera, out of frame.
    python3 gen3.py FRONT_IRR STRENGTH [STRENGTH ...]  ->  fixed2c-FRONT-STRENGTH.json"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
front = sys.argv[1]
base = json.load(open(os.path.join(HERE, f'fixed2-{front}.json')))
for st in sys.argv[2:]:
    s = copy.deepcopy(base)
    s['lights']['ceiling-panel'] = {'type': 'panel', 'size_m': [1.6, 0.8], 'position': [10.5, 4.0, 3.2],
                                    'target': [8.25, 5.57, 2.2], 'strength': float(st), 'diffuse': 1.0, 'specular': 1.0,
                                    'color': '#FFE2C0'}
    s['title'] = s['title'] + f'; ceiling panel {st}'
    json.dump(s, open(os.path.join(HERE, f'fixed2c-{front}-{st}.json'), 'w'), indent=1)
    print('fixed2c', front, st)
