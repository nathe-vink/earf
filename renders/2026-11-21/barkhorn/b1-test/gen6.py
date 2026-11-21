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
      t4, t5  no front head; the softbox a real one (a mesh diffuser in a body); track-bay1 times IRR (gen6.py t4 3).
      t6, t7  a diffuser flush under the ceiling over the bay, and a frontal softbox at strength IRR (gen6.py t6 10).
      t8, t9  t7's lights (frontal softbox at IRR) with the niches in a mid warm-grey felt (an option: a set change).
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
if v.startswith('t4') or v.startswith('t5'):
    # t4/t5: the softbox as a real one (a glowing diffuser in a black body, living_ext.softbox) at the same place,
    # (z 2.70-3.38 with its 10 cm body: under the 3.40 ceiling; its nearest corner 33 px above the frame)
    # strength 6 (the live card's mean: 10 on its 0.25-1-0.25 ramp), and the steep bay head over the near speaker
    # (track-bay1, planet_bar.py:136, 'the cone in its cabinet's shade') raised by `irr` times, no front head
    L.pop('bay-softbox')
    s['set']['props'].append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/campaign/living/living_ext.py',
                              'fn': 'softbox', 'size': [1.4, 0.9], 'depth': 0.1, 'position': [8.05, 4.9, 3.0],
                              'target': [8.25, 5.6162, 2.19], 'strength': 6.0, 'color': '#FFE2C0'})
    L['track-bay1']['irradiance'] = round(L['track-bay1']['irradiance'] * irr, 2)
if v.startswith('t2'):
    L['track-front1'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.05, 0.05], 'position': [8.6, 3.9, 3.35], 'target': AIM,
                         'irradiance': irr, 'spread_deg': 14, 'color': '#FFE2C0'}
    s['set']['props'].append({'kind': 'kit', 'shape': 'box', 'size': [0.6, 0.006, 0.35], 'position': [8.452, 4.6, 2.509],
                              'material': 'flock', 'color': '#0A0A0A'})
elif v.startswith('t3'):
    L['track-front1'] = {'type': 'area', 'shape': 'DISK', 'size_m': [0.14, 0.14], 'position': [8.25, 4.95, 3.35], 'target': AIM,
                         'irradiance': irr, 'spread_deg': 14, 'color': '#FFE2C0'}
s['title'] = f'B1 fixed-6 {v}: Planet EARF bar, the record wall from a seat at the bar (a test, not a final)'
s['set']['props'].append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/campaign/living/living_ext.py',
                          'fn': 'shadow_ray_report'})                       # (prints what the cut left; changes nothing)
if v[:2] in ('t6', 't7', 't8', 't9'):
    # t6/t7: two real softboxes (living_ext.softbox: a glowing diffuser in a black body, every ray on, casting shadows)
    #   ceiling-panel: a 1.4 x 0.9 m diffuser flush under the ceiling over the bay's front (z 3.36-3.40), facing
    #     down, strength 6. The live horn card spanned z 3.04-3.58, more than half of it above the ceiling.
    #   front-softbox: a 1.2 x 0.9 m softbox hung in front of the near bay at (8.6, 4.3, 3.0) (z 2.69-3.38, 668 px
    #     above the frame), aimed at the cabinet (8.25, 5.6, 1.55), at strength `irr`. A large soft source
    #     lights the white batts (albedo about 0.8) about 40 times as much as the cone's dark paper (#242220),
    #     where a small head at a glossy angle made the cone's sheen outshine them.
    #   No front head; track-bay1 as in the bar.
    L.pop('bay-softbox')
    E = 'spinoffs/barkhorn/campaign/living/living_ext.py'
    s['set']['props'].append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'softbox', 'size': [1.4, 0.9], 'depth': 0.02,
                              'position': [8.05, 4.9, 3.37], 'target': [8.05, 4.95, 0.0], 'strength': 6.0, 'color': '#FFE2C0'})
    s['set']['props'].append({'kind': 'kit', 'shape': 'ext', 'path': E, 'fn': 'softbox', 'size': [1.2, 0.9], 'depth': 0.1,
                              'position': [8.6, 4.3, 3.0], 'target': [8.25, 5.6, 1.55], 'strength': irr, 'color': '#FFE2C0'})
if v.startswith('t8') or v.startswith('t9'):
    # t8/t9 (the coordinator, 14:38: a set change, an option for the owner): t7's lights (t9 with the frontal softbox
    # at `irr`), and the speakers' niches in a mid warm-grey felt (#8C8379, albedo about 0.23) in place of the
    # near-black #1A1918 (planet_bar.py:135), so the clear horn is seen against a lit ground by transmission. The swap is
    # the bar's own restyle of 'kit-felt', which dresses both bays.
    for p_ in s['set']['props']:
        if p_.get('fn') == 'restyle':
            p_['swap']['kit-felt'] = {'kind': 'plain', 'color': '#8C8379', 'rough': 0.95}
json.dump(s, open(os.path.join(HERE, f'fixed6-{v}.json'), 'w'), indent=1)
print(v, s['title'], sorted(L))
