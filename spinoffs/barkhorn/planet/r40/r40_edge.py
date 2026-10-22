"""Mother EARF's edges, a render-lighting test (the coordinator, 2026-10-22, approved: "it doesn't change the product"):
round 39's empty door-mother final exactly as rendered (its shot file), plus one narrow spot from the ceiling on the
camera side aimed at the globe, so the 25 mm Smoke discs' faces and polished edges catch light (every critic: "a
black wire cage"). Nothing else changes.

    python3 spinoffs/barkhorn/planet/r40/r40_edge.py        # writes studio/shots/barkhorn/planet40/door-mother-edge.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
SRC = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'planet39', 'finals', 'door-mother.shot.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet40', 'door-mother-edge.json')

# from the deck behind the globe on the window side, raking through the discs toward the lens, so their polished
# edges and faces carry light out of the sheet as cast acrylic does (from the camera's side, two looks, it lit the
# smoked faces to a dull grey and changed nothing); 1.4 m off the globe (it hangs at [6.24, 1.15, 2.47], 1.25 m across):
# a 40 deg
# cone just covers it, so the light lands on the discs, not the room
EDGE = {'type': 'spot', 'position': [7.1, 0.45, 3.3], 'target': [6.24, 1.15, 2.47], 'power_w': 120.0, 'cone_deg': 40.0,
        'blend': 0.3, 'radius_m': 0.02, 'color': 2700, 'camera': False}


def main():
    s = json.load(open(SRC))
    s['lights']['mother-edge'] = dict(EDGE)
    s['title'] = s['title'].replace('(round 39)', '(round 39, with an edge light on Mother EARF: a round 40 test)')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(s, open(OUT, 'w'), indent=1)
    print(OUT)


if __name__ == '__main__':
    main()
