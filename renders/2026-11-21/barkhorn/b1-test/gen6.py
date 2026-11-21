"""B1 fixed-6 (the coordinator, 13:24, after the critics on fixed-4): from fixed-5 (no horn card), every light real.
  - house and house-left inside the room at their aims (3 m disc centre (6.9, 0.6, 1.9): top z 3.36, lowest y 0.26;
    2 m disc centre (4.6, 2.2, 2.38): top z 3.38). The ceiling is 3.40.
  - ceiling-light removed (variants may add it back below the ceiling).
  - bay-softbox: a real softbox where the live horn card hung, wholly below the ceiling: a 1.4 x 0.9 m area light at
    (8.05, 4.9, 3.0) (top z 3.30) facing the near speaker (8.25, 5.62, 2.19). Every ray visibility is on, the camera's
    included; its light casts shadows. 17 W: about the live card's mean strength (10 on a 0.25-1-0.25 ramp, about 6.2)
    at 2.2 x S x area.
  - the near speaker's front head, by variant:
      t1  none
      t2  flagged: a 5 cm head (a spot's lens) on the track at (8.6, 3.9, 3.35), 14 deg, aimed at the cabinet above the
          woofer (8.25, 5.55, 1.88), with a black flocked flag (0.6 x 0.35 m, 6 mm) hung 1.0 m down the beam at y 4.6.
          The flag's top edge sits on the line to (8.25, 5.55, 1.78), just over the woofer (cone top z 1.73 on the
          front), so the cone and the sill are in its shadow (penumbra about 7 cm).
      t3  steep: a 14 cm head on the track at (8.25, 4.95, 3.35), 0.6 m in front of the bay, 14 deg, at the same aim.
    python3 gen6.py VARIANT [IRR]  ->  fixed6-VARIANT.json"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
v = sys.argv[1]; irr = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
s = json.load(open(os.path.join(HERE, 'fixed5.json')))
L = s['lights']
L['house'].update(position=[6.9, 0.6, 1.9])
L['house-left'].update(position=[4.6, 2.2, 2.38])
L.pop('ceiling-light', None); L.pop('track-front1', None)
L['bay-softbox'] = {'type': 'area', 'shape': 'RECTANGLE', 'size_m': [1.4, 0.9], 'position': [8.05, 4.9, 3.0],
                    'target': [8.25, 5.6162, 2.19], 'power_w': 17.0, 'color': '#FFE2C0', 'camera': True}
AIM = [8.25, 5.55, 1.88]
if v.startswith('t2'):
    L['track-front1'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.05, 0.05], 'position': [8.6, 3.9, 3.35], 'target': AIM,
                         'irradiance': irr, 'spread_deg': 14, 'color': '#FFE2C0'}
    s['set']['props'].append({'kind': 'kit', 'shape': 'box', 'size': [0.6, 0.006, 0.35], 'position': [8.452, 4.6, 2.509],
                              'material': 'flock', 'color': '#0A0A0A'})
elif v.startswith('t3'):
    L['track-front1'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.14, 0.14], 'position': [8.25, 4.95, 3.35], 'target': AIM,
                         'irradiance': irr, 'spread_deg': 14, 'color': '#FFE2C0'}
s['title'] = f'B1 fixed-6 {v}: Planet EARF bar, the record wall from a seat at the bar (a test, not a final)'
json.dump(s, open(os.path.join(HERE, f'fixed6-{v}.json'), 'w'), indent=1)
print(v, s['title'], sorted(L))
