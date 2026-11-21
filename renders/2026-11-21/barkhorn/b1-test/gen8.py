"""B1 fixed-8 (the coordinator, 18:05, after the fixed-7 critics). From fixed7.json:
  rig: the near frontal softbox 2 cm lower (it ran 16 mm into the ceiling diffuser); track-bar1 off (87.5 % blocked by
  the far softbox); track-horn1 off (it lit only the near softbox's back) unless a variant moves it to do a job;
  the diagnostics last in the set: shadow_ray_report and emitter_report (every emitter's ray visibility).
    python3 gen8.py VARIANT [ARGS]  ->  fixed8-VARIANT.json (crops) or fixed8.json (VARIANT 'full')"""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
E = 'spinoffs/barkhorn/campaign/living/living_ext.py'
v = sys.argv[1] if len(sys.argv) > 1 else 'probe'
s = json.load(open(os.path.join(HERE, 'fixed7.json')))
P = s['set']['props']; L = s['lights']
P[:] = [p for p in P if p.get('fn') not in ('shadow_ray_report', 'emitter_report')]
for p in P:
    if p.get('fn') == 'softbox' and p['size'] == [1.2, 0.9] and p['position'][0] > 7:
        p['position'] = [p['position'][0], p['position'][1], round(p['position'][2] - 0.02, 3)]
L.pop('track-bar1', None); L.pop('track-horn1', None)
s['title'] = f'B1 fixed-8 {v}: Planet EARF bar, the record wall from a seat at the bar (a test, not a final)'
P.append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'shadow_ray_report'})
P.append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'emitter_report'})
json.dump(s, open(os.path.join(HERE, 'fixed8.json' if v == 'full' else f'fixed8-{v}.json'), 'w'), indent=1)
print(v, sorted(L), [(p['position'], p['strength']) for p in P if p.get('fn') == 'softbox'])
