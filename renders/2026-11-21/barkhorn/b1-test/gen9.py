"""B1 fixed-9 crop tests (the coordinator, 22 Nov 00:29), from fixed8.json (the owner's choice pending: no full render).
  python3 gen9.py NAME [--off ROLE ...] [--fix9]  ->  fixed9-NAME.json
  --off ROLE: a light or fixture left out, to find what throws Q2's ceiling streak: far, near, diffuser, panels (the two
    opal backs), heads (every engine lamp: the track heads, house, house-left, mantle-*), hemis (the Hemispheres' and
    Cores' LEDs, as a set prop)
  --fix9: the fixed-9 changes:
    2. the far softbox 30 cm further back along its throw, horizontally (toward the seats), clear of the orange and red
       pendants' cords; re-aimed at (5.55, 5.6, 1.55); skirt, grid and flag kept; strength 28 -> 31 (about 90 % at the
       longer throw otherwise)
    3. mantle-front raised 0.3 m and re-aimed at the same point (the camera sat in its beam)
    4. track-bay1 10 cm toward the wall (clear of the ceiling diffuser)
    5. 'camera': true on every shot lamp (all out of frame)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
name = sys.argv[1]; offs = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--off']
s = json.load(open(os.path.join(HERE, 'fixed8.json')))
P = s['set']['props']; L = s['lights']
def role(p):
    if p.get('fn') != 'softbox':
        return None
    if p['size'] == [1.4, 0.9]: return 'diffuser'
    if p['size'] == [0.64, 0.58]: return 'panels'
    return 'far' if p['position'][0] < 8.0 else 'near'
if '--fix9' in sys.argv:
    for p in P:
        if role(p) == 'far':
            x, y, z = p['position']; tx, ty, _ = p['target']
            d = math.hypot(x - tx, y - ty); ux, uy = (x - tx) / d, (y - ty) / d
            p['position'] = [round(x + 0.30 * ux, 3), round(y + 0.30 * uy, 3), round(z - 0.01, 3)]; p['strength'] = 31.0   # (1 cm lower: its body's top at 3.391, under the 3.40 ceiling; every corner above the frame; azimuth 44 deg from the far horn, as before)
    m = L['mantle-front']; m['position'] = [m['position'][0], m['position'][1], round(m['position'][2] + 0.3, 3)]
    if '--bay1-orig' not in sys.argv:     # (Q1's check: --bay1-orig keeps it where fixed-8 had it)
        b = L['track-bay1']; b['position'] = [b['position'][0], round(b['position'][1] + 0.10, 4), b['position'][2]]
    for l in L.values():
        l['camera'] = True
    # 1. Q2: track-bay0 25 cm to the right along its track, the same aim (the streak's peak L* 87 -> 10.9 on the crop)
    # (x 5.8 cleared the streak but threw the horn's caustic into the frame's top-left corner, L* 99; --bay0-x tries
    # other places along the track)
    bx = float(sys.argv[sys.argv.index('--bay0-x') + 1]) if '--bay0-x' in sys.argv else 5.8
    if '--bay0-orig' not in sys.argv:
        L['track-bay0']['position'] = [bx, 4.4, 3.35]
# Q2's fix candidates for track-bay0 (it throws the ceiling streak: off, the streak's peak L* 87 -> 8.6; its beam on the
# far horn's glossy concave bell focuses into dots; aimed lower (81.9) or narrowed (82.9) it still covers the horn; a
# barn door cutting the horn's rays would hang in the frame (y 40-85 px at y 4.7), or within 1.6 cm of the cabinet's
# rays near the head)
if '--bay0-low' in sys.argv:        # aimed lower, onto the cabinet, so its beam misses the horn's glossy top
    L['track-bay0']['target'] = [5.55, 5.6662, 1.8]
if '--bay0-narrow' in sys.argv:     # a tighter beam (a narrower lens or snoot): 14 -> 10 deg, the same aim
    L['track-bay0']['spread_deg'] = 10
if '--bay0-steep' in sys.argv:      # further toward the wall, steeper (its head 20 px above the frame's top at y 4.8)
    L['track-bay0']['position'] = [5.55, 4.8, 3.35]
if '--bay0-side' in sys.argv:       # 25 cm to the right along the track (103 px above the frame), the same aim
    # (x 5.8 cleared the streak but threw the horn's caustic into the frame's top-left corner, L* 99; --bay0-x tries
    # other places along the track)
    bx = float(sys.argv[sys.argv.index('--bay0-x') + 1]) if '--bay0-x' in sys.argv else 5.8
    if '--bay0-orig' not in sys.argv:
        L['track-bay0']['position'] = [bx, 4.4, 3.35]
for r in offs:
    if r in ('far', 'near', 'diffuser', 'panels'):
        P[:] = [p for p in P if role(p) != r]
    elif r == 'heads':
        s['lights'] = {}
    elif r in ('track-bay0', 'track-bay1'):
        s['lights'].pop(r)
    elif r in ('walls', 'bars', 'bays', 'horn0', 'mantles', 'houses'):
        pre = {'walls': ('track-wall',), 'bars': ('track-bar',), 'bays': ('track-bay',), 'horn0': ('track-horn',),
               'mantles': ('track-mantle', 'mantle-'), 'houses': ('house',)}[r]
        s['lights'] = {k: l for k, l in s['lights'].items() if not k.startswith(pre)}
    elif r == 'hemis':
        P[:] = [p for p in P if p.get('fn') != 'lamps']        # (the pendants and Cores: stage2_props.lamps)
s['title'] = f'B1 fixed-9 test {name}: Planet EARF bar (a crop test, not a final)'
json.dump(s, open(os.path.join(HERE, f'fixed9-{name}.json'), 'w'), indent=1)
print(name, offs, [(role(p), p['position'], p['strength']) for p in P if p.get('fn') == 'softbox'], len(s['lights']))
