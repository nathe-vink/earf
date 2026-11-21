"""B1 fixed-2 (the coordinator, 21 Nov 10:00): fixed, plus a real light on the near Tropos.
   track-front1: one more head on the bar's ceiling track (the track's own heads hang at z 3.35, 12-14 cm discs, #FFE2C0),
   1.4 m in front of the near bay and 0.35 m to its right, aimed at the cabinet's front. It is a plain area lamp: every
   ray visibility left on, no receivers and no specular or diffuse share. Out of frame: 67 degrees above the
   camera's axis, past the 24 mm frame's top. Its spill lands where it lands.
    python3 gen2.py IRR [IRR ...]  ->  fixed2-IRR.json (irradiance in W/m2 at the target)"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fixed = json.load(open(os.path.join(HERE, 'fixed.json')))
for irr in sys.argv[1:]:
    s = copy.deepcopy(fixed)
    s['lights']['track-front1'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.14, 0.14], 'position': [8.6, 3.9, 3.35],
                                   'target': [8.25, 5.45, 1.5], 'irradiance': float(irr), 'spread_deg': 22, 'color': '#FFE2C0'}
    s['title'] = s['title'].replace('B1 fixed', f'B1 fixed-2 ({irr} W/m2 front head)')
    json.dump(s, open(os.path.join(HERE, f'fixed2-{irr}.json'), 'w'), indent=1)
    print('fixed2', irr)
