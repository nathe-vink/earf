"""Planet EARF's shots, round 40 (the coordinator, 2026-10-22, from the owner's answers: "Mother EARF: A and B: the
promise, and the globe in the bar"; "Bar pictures: blurred figures allowed"): round 39's three heroes again, aiming
for 7, with people as a long exposure records them and the critics' named tells taken out.

    python3 spinoffs/barkhorn/planet/r40/r40_shots.py [VIEW ...]          # writes studio/shots/barkhorn/planet40/
    python3 studio/engine/render.py studio/shots/barkhorn/planet40/door-mother.json --out IMG --scale 0.5

Views: door-mother (the room from the door, Mother EARF over a banquette table), bar, listening.

What round 40 changes against round 39's finals and p4 (the critics' tells, in their words):
- "the stools' hard street-lamp shadows on the floor": the two street lamps lit the room through the glass from
  10 m off, point sources, so every stool drew a hard shadow fan; off in the interiors (they light the street);
- "the zinc the brightest surface while the altar speakers sit dim": the zinc a stop darker and less glossy, the
  Domes' downlights weaker; the altar's spots stronger and tighter, the speakers' own key up;
- "the pendants read as white milk glass": the Domes' smoked liners glow a third as much;
- "furniture that looks like identical copies": every seat turned and shifted further, more pulled out, and people
  in them;
- "the listening room still reads as a showroom": a seated camera from the room's corner, a tub chair, its table
  and Core in front, a listener;
- "the single fir texture": every fir board its own stretch of the scan and its own tone (`kit40.boards`);
- "chroma grain": more samples and a camera's chroma noise reduction in the lens step (`photo.py`).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'r39'))
import r39_shots as T39                                             # noqa: E402

RP = T39.RP
OUT = os.path.join(T39.ROOT, 'studio', 'shots', 'barkhorn', 'planet40')
KIT40 = 'spinoffs/barkhorn/planet/r40/kit40.py'
C = RP.COUNTER

T39.ALL.update(counter_strip=0.08, street_lamp=0.0, pendant_w=20.0, dome_glow_smoke=0.016, orb_pool=9.0, screen_glow=0.05, haze=0.004)
T39.JITTER['pull'].update({'chairs:6': [0.03, -0.14, 22.0], 'chairs:12': [-0.05, 0.12, 14.0], 'tubs:3': [0.06, 0.05, -10.0]})
RETOUCH = dict(darken={'zinc': 0.30}, zinc_rough=[0.30, 0.62])

# people (seat heights from the plan: the counter chairs 0.76, the banquette 0.45, the chairs at the tables 0.46,
# the tub chairs 0.38 on the 0.2 step); clothes muted, never the products' colours
CLOTH = ['#1C2230', '#141312', '#3A1A16', '#262524', '#2E3024', '#5A4430', '#2A3448', '#1E1C1A', '#3C2E26', '#4A4A48']
SKIN = ['#D9AE94', '#B47E5E', '#7E5038', '#5A3A28', '#C89878', '#E2BCA4', '#9A6648']
HAIR = ['#1A1410', '#3A2A1E', '#0E0C0A', '#6A5038', '#2A2420', '#8A7A6A', '#151210']
SIT = dict(move=[0.09, 0.07, 0.01], spin=10.0, head=[0.20, 0.12, 0.03, 35.0], arms=[0.24, 0.12, 0.10, 30.0])


def person(i, pose, at, heading, seat=0.46, **k):
    d = dict(pose=pose, at=[round(a, 3) for a in at], heading=heading, seat=seat, cloth=CLOTH[i % len(CLOTH)],
             skin=SKIN[(i * 3) % len(SKIN)], hair=HAIR[(i * 5) % len(HAIR)], seed=400 + i, **SIT)
    d.update(k)
    return d


cx = T39.chair_x
YS = round(C['y0'] - 0.48, 3)                                       # the counter chairs
TB, TY = RP.TABLES36, RP.TABLE36['y']
BENCH_Y = 0.42
BAR_PEOPLE = [
    person(0, 'stool', [cx(4), YS, 0], 90, 0.76),
    person(1, 'stool', [cx(5), YS - 0.12, 0], 96, 0.76, head=[0.26, 0.14, 0.03, 45.0]),   # turned to talk
    person(2, 'stool', [cx(7), YS, 0], 84, 0.76),
    person(3, 'pour', [5.05, 5.00, 0], -90, move=[0.30, 0.04, 0.0], spin=14.0, arms=[0.35, 0.10, 0.18, 40.0],
           head=[0.32, 0.06, 0.04, 30.0], cloth='#1A1918', sleeve='#7A7064'),                    # the bartender, mid-pour
    person(4, 'decks', [6.95, 4.98, 0], -90, move=[0.08, 0.04, 0.0], spin=8.0, arms=[0.22, 0.14, 0.08, 30.0],
           head=[0.10, 0.05, 0.12, 25.0]),                                                        # the selector
]
BANQ_PEOPLE = [
    person(5, 'bench', [TB[0], BENCH_Y, 0], 90, 0.45),
    person(6, 'bench', [TB[1] + 0.12, BENCH_Y, 0], 90, 0.45, head=[0.26, 0.14, 0.03, 45.0]),
    person(7, 'chair', [TB[3] + 0.03, RP.CHAIR_Y36 + 0.05, 0], -90, 0.46),
    person(8, 'bench', [TB[3] - 0.05, BENCH_Y, 0], 90, 0.45),
]


def _toward(x, y, tx=16.55, ty=3.05):
    return round(math.degrees(math.atan2(ty - y, tx - x)), 1)


tx, ty = RP.TUBS[1]
LISTEN_PEOPLE = [person(9, 'tub', [tx, ty, RP.ZONE['z']], _toward(tx, ty), RP.TUB['seat'],
                        move=[0.06, 0.05, 0.02], spin=8.0, head=[0.16, 0.10, 0.04, 30.0], arms=[0.20, 0.12, 0.08, 25.0])]

VIEWS = {
    'door-mother': dict(people=BAR_PEOPLE + BANQ_PEOPLE[1:],
                        settings=dict(altar_w=380.0, altar_cone=24.0, listen_key=3.0, exposure=4.6)),
    'bar': dict(people=BAR_PEOPLE + BANQ_PEOPLE[:1],
                camera={'position': [3.40, 2.70, 1.30], 'target': [7.4, 5.6, 1.65], 'lens_mm': 35, 'level': True,
                        'fstop': 4.0, 'focus': [6.6, 4.4, 1.2]},
                settings=dict(niche_strip=0.12, spk_niche_strip=0.1, rw_w=8.0, bar_key=3.0, exposure=3.0)),
    'listening': dict(people=LISTEN_PEOPLE,
                      camera={'position': [12.05, 5.45, 1.25], 'target': [16.4, 2.7, 1.0], 'lens_mm': 28, 'level': True,
                              'fstop': 4.0, 'focus': [16.0, 2.6, 1.0]},
                      settings=dict(altar_w=38.0, altar_cone=24.0, orb_pool=20.0, exposure=4.7, haze=0.006)),
}


def shot(view):
    vw = VIEWS[view]
    key = view.split('-mother')[0]
    v39 = T39.VIEWS[key]
    saved = (dict(v39['camera']), dict(v39['settings']), dict(v39.get('retouch', {})))
    try:
        if vw.get('camera'):
            v39['camera'] = vw['camera']
        v39['settings'] = {**v39['settings'], **vw.get('settings', {})}
        v39['retouch'] = {**v39.get('retouch', {}), **RETOUCH}
        s = T39.shot(view)
    finally:
        v39['camera'], v39['settings'], v39['retouch'] = saved
    s['set']['props'] += [{'kind': 'kit', 'shape': 'ext', 'path': KIT40, 'fn': 'boards'},
                          {'kind': 'kit', 'shape': 'ext', 'path': KIT40, 'fn': 'figures', 'people': vw['people']}]
    s['title'] = s['title'].replace('(round 39)', '(round 40)')
    return s


def write(names=None):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(VIEWS):
        p = os.path.join(OUT, f'{n}.json')
        json.dump(shot(n), open(p, 'w'), indent=1)
        print(p)


if __name__ == '__main__':
    write([a for a in sys.argv[1:] if not a.startswith('--')] or None)
