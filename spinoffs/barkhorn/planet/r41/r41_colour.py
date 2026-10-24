"""Planet EARF, round 41 (the owner, 2026-10-22: "Bar people: empty rooms, as round 39" and "Bar globe: the site's
multicolour"): round 39's empty door-mother final exactly as rendered (its shot file), with Mother EARF's globe in the
site's multicolour, round 33c's globe as on the site's mother-globe.jpg: the six discs in their speakers' tints (Poison
the meridian facing, Dust and Haze the side meridians, Ember 40 N, Ice the equator, Acid 40 S), each rim glowing its
colour, no core. The same 1.25 m, place, heading, sheet and light; round 39's hard spot and rim spot stay as they were.

    python3 spinoffs/barkhorn/planet/r41/r41_colour.py [--edge]   # writes studio/shots/barkhorn/planet41/door-mother-colour.json

`--p2` is the second pass (both p1 critics, converged: the rims read as neon tubes and the coloured shadow was the
brightest surface): rim glow 0.06, the globe's hard spot 100 W and narrower (cone 20 deg), nothing else; it writes
door-mother-colour-p2.json. `--p3` is the last pass (both p2 critics: the rims still neon, the blue ring clipping, the
faces dark): rim glow 0.025 and the spot raised again, 135 W at 20 deg, so the faces carry the colour.
`--p4` (the owner, 2026-10-24: "Do those next steps"; the p3 critics' converged fixes, one pass, aiming for 7) builds
on p3: rim glow 0.011 and the globe's spot at 145 W, 24 deg (220 W and 160 W, tried, brightened the wall's coloured shadow); the near floor's pool pulled back (a diagnostic at 1/4
size, switching each light group off in turn, found no single source: the Domes give about 3 %, so their cones are
tightened and dimmed a little, the floor's finish darkened a quarter and its sealer thinned to a honed finish); the concrete given a soft mottle of tone and
roughness (`kit41.concrete`); the seats given round 39's jitter, restrained, and each its own leather tone and wear
(`kit41.seats`); the altar spots down from 170 to 110 W and the rim, top and key lamps on the pair halved, so the batts stop being the brightest thing back there.
`--p5 [a|b]` (the owner, 2026-10-24: "Do another pass. Keep refining everything") builds on p4 with what both p4
critics converged on: the Cores' glow 0.003 and lamp 0.10 W (they read as white discs); the zinc darker with a patina
and the rings glasses leave (`kit41.zinc`); the floor darker still and its sheen less milky; the banquette tables'
column broken as the seats were (each Core a few centimetres off its table's centre, the tables shifted a little more,
each top its own tone). The globe, where they split, was tried both ways at a quarter size: (a) the spot down to
80 W; (b) the rims back up to 0.03 with the spot moved to rake across the discs' faces. (b) kept: at a quarter
size the wall's coloured shadow 87 against (a)'s 108, and the rims carry their colour again (globe p95 120 against 68).
`--edge` adds round 40's edge light (r40/r40_edge.EDGE), only if the colours do not read without it.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
SRC = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'planet39', 'finals', 'door-mother.shot.json')
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'planet41', 'door-mother-colour.json')
# the site's globe: every rim lit alike (meridians and parallels), no opal core (round 39's p1 variant had one)
COLOUR = dict(core=0.0, rim=0.14, rim_par=1.0, radius=0.07)   # rim 0.22 (round 39's p1) neared clipping at a look


def main():
    s = json.load(open(SRC))
    m = next(p for p in s['set']['props'] if p.get('fn') == 'mother')
    m.pop('tint', None)
    m.update(COLOUR)
    out = OUT
    if '--p2' in sys.argv:
        m['rim'] = 0.06
        s['lights']['mother-spot'].update(power_w=100.0, cone_deg=20.0)
        out = OUT.replace('.json', '-p2.json')
    if '--p3' in sys.argv:
        m['rim'] = 0.025
        s['lights']['mother-spot'].update(power_w=135.0, cone_deg=20.0)
        out = OUT.replace('.json', '-p3.json')
    if '--p4' in sys.argv:
        m['rim'] = 0.011
        # the critics' 220 W, at a look, pushed the globe's coloured shadow on the wall back toward the brightest
        # surface (median 110 -> 128, p1's fault); 180 W at 24 deg keeps the intensity at p3's while the rims' glow
        # drops by more than half, so the faces carry the colour
        s['lights']['mother-spot'].update(power_w=145.0, cone_deg=24.0)
        for k, l in s['lights'].items():
            if k.startswith('pend'):
                l.update(power_w=26.0, cone_deg=16.0)
            if k.startswith('altar'):
                l['power_w'] = 110.0
            if k.startswith('riml'):                  # the batts are lit hot by the rim lamps behind the pair, too
                l['irradiance'] = 5.0
            if k in ('spk0', 'spk1') or k.startswith('keyl'):   # and by the soft lamps above and in front of them
                l['irradiance'] = round(l['irradiance'] * 0.5, 3)
        rt = next(q for q in s['set']['props'] if q.get('fn') == 'retouch')
        rt['darken'] = dict(rt.get('darken', {}), Concrete044A=0.75)   # the floor's scan (planet_loft.floor_mat)
        # the near floor's pool is mostly the sealer's sheen reflecting the room (darkening its tone moved it 2 %):
        # the coat thinned to a honed finish
        rt['set'] = dict(rt.get('set', {}), Concrete044A={'Coat Weight': 0.08})
        K39, K41 = 'spinoffs/barkhorn/planet/r39/kit39.py', 'spinoffs/barkhorn/planet/r41/kit41.py'
        s['set']['props'] += [
            {'kind': 'kit', 'shape': 'ext', 'path': K39, 'fn': 'jitter', 'seed': 412,
             'turn': {'chairs': 7.0, 'tubs': 5.0, 'tables36': 2.0, 'tub-tables': 0.0},
             'shift': {'chairs': 0.025, 'tubs': 0.02, 'tables36': 0.008, 'tub-tables': 0.0},
             'pull': {'chairs:3': [0.03, -0.12, 10.0], 'chairs:10': [0.04, 0.10, -8.0]}},
            {'kind': 'kit', 'shape': 'ext', 'path': K41, 'fn': 'concrete', 'tone': 0.07, 'rough': 0.18},
            {'kind': 'kit', 'shape': 'ext', 'path': K41, 'fn': 'seats', 'tone': 0.10,
             'meshes': ['chairs-leather', 'tub-cushions', 'banq-cushions', 'banq-seat', 'banq-back']}]
        out = OUT.replace('.json', '-p4.json')
    if '--p5' in sys.argv:
        var = sys.argv[sys.argv.index('--p5') + 1] if len(sys.argv) > sys.argv.index('--p5') + 1 else 'a'
        if var == 'a':
            s['lights']['mother-spot'].update(power_w=80.0)
        else:
            m['rim'] = 0.03
            s['lights']['mother-spot'].update(position=[5.4, 2.4, 3.3])
        orb = next(q for q in s['set']['props'] if q.get('fn') == 'orb')
        orb.update(shade_glow=0.003, lamp_w=0.10)        # at 0.16 W, a look: still 188, a white disc
        nudge = [(0.05, -0.04), (-0.06, 0.03), (0.03, 0.06), (-0.04, -0.05)]   # the four banquette tables' Cores
        orb['spots'] = [[round(x + nudge[i][0], 3), round(y + nudge[i][1], 3), z] if i < 4 else [x, y, z]
                        for i, (x, y, z) in enumerate(orb['spots'])]
        rt['darken'] = dict(rt['darken'], Concrete044A=0.6, zinc=0.20)   # zinc 0.30, a look: still 143
        # (the zinc's tone, its roughness, and a test at half metal each moved the counter top 0 % at a quarter size:
        # from the door it is seen at a grazing angle, where any surface reflects the warm room; kept: the darker
        # patina and the rings, which read up close)
        rt['set'] = dict(rt['set'], Concrete044A={'Coat Weight': 0.06, 'Specular IOR Level': 0.35})
        rt['zinc_rough'] = [0.45, 0.75]; rt['zinc_mottle'] = 0.5   # seen at a grazing angle from the door, the metal's Fresnel makes it white whatever its tone: rougher
        jt = next(q for q in s['set']['props'] if q.get('fn') == 'jitter')
        jt['shift'] = dict(jt['shift'], tables36=0.02)
        for q in s['set']['props']:
            if q.get('fn') == 'seats':
                q['meshes'] = q['meshes'] + ['tables36']
        s['set']['props'].append({'kind': 'kit', 'shape': 'ext', 'path': K41, 'fn': 'zinc'})
        out = OUT.replace('.json', f'-p5{var}.json')
    if '--edge' in sys.argv:
        sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r40'))
        from r40_edge import EDGE
        s['lights']['mother-edge'] = dict(EDGE)
    s['title'] = s['title'].replace('(Mother EARF)', "(Mother EARF in the site's multicolour)").replace('(round 39)', '(round 41)')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(s, open(out, 'w'), indent=1)
    print(out)


if __name__ == '__main__':
    main()
