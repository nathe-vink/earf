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
# P1, the near horn: something bright behind it on the camera's line of sight (it sees the felt at about x 7.99,
# z 2.2-2.6 through the clear horn). Real fixtures only (living_ext.softbox meshes, every ray on, casting shadows).
X = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
if v.startswith('a'):
    # (a) a backlit opal panel as the near niche's back, behind the horn: 0.6 x 0.52 m, its face at y 6.02 (the felt at
    # 6.03), centre z 2.26, facing the room, at strength X
    P.append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'softbox', 'size': [0.6, 0.52], 'depth': 0.005,
              'position': [8.25, 6.02, 2.26], 'target': [8.25, 4.0, 2.26], 'strength': X, 'color': '#FFF4E6'})
if v.startswith('w'):
    # (a, wide) the opal panel across the whole near niche back above the cabinet (x 7.93-8.57, z 1.93-2.51), warm
    # (#FFE2C0, the bar's lamps) where a1/a3's cool #FFF4E6 read blue beside the horn; the horn's left half saw past a1
    P.append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'softbox', 'size': [0.64, 0.58], 'depth': 0.005,
              'position': [8.25, 6.02, 2.22], 'target': [8.25, 4.0, 2.22], 'strength': X, 'color': '#FFE2C0'})
if v.startswith('b'):
    # (b) the near niche's back pale (an off-white plaster panel, 6 mm, over the felt behind and above the cabinet),
    # lit by a concealed LED strip under the niche's top lip (0.6 x 0.02 m, its face at z 2.505 just behind the
    # face frame's head, aimed back and down at the wall behind the horn; the niche's head sits above the frame)
    P.append({'kind': 'kit', 'shape': 'box', 'size': [0.62, 0.006, 0.58], 'position': [8.25, 6.022, 2.22],
              'material': 'paper', 'color': '#E6E0D6'})
    P.append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'softbox', 'size': [0.6, 0.02], 'depth': 0.01,
              'position': [8.25, 5.52, 2.505], 'target': [8.25, 6.03, 2.1], 'strength': X, 'color': '#FFE2C0'})
s['title'] = f'B1 fixed-8 {v}: Planet EARF bar, the record wall from a seat at the bar (a test, not a final)'
P.append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'shadow_ray_report'})
P.append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'emitter_report'})
json.dump(s, open(os.path.join(HERE, 'fixed8.json' if v == 'full' else f'fixed8-{v}.json'), 'w'), indent=1)
print(v, sorted(L), [(p['position'], p['strength']) for p in P if p.get('fn') == 'softbox'])
