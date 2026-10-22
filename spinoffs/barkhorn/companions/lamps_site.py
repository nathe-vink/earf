"""Round 32f, the site set again with the owner's changes (black hardware, the plug-in Orb, the tints matched lit), in
the names the site picks up (renders/2026-10-19/barkhorn/lamps-site/). The frames are round 32e's finals
(studio/shots/barkhorn/crystal-promo/final/, the duels' winners), the products now black and cast to the speakers' hues;
the Orbs plug in, their cables dressed straight back (the kit piece's default). One frame is new: the cartridge, half
out of the back of a lit Orb.

    python3 spinoffs/barkhorn/companions/lamps_site.py                     # the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/lamps_site.py --render [names] [--scale 1.0]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FINAL = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'crystal-promo', 'final')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-site')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'lamps-site')
NAMES = {'lamp-dome': 'dome-hero', 'lamp-orb': 'orb-hero', 'lamps-orbs': 'orbs', 'lamps-domes': 'domes',
         'lamp-catch': 'catch', 'lamps-unlit': 'unlit'}


def final(n):
    return json.load(open(os.path.join(FINAL, n + '.json')))


def cartridge():
    """The battery cartridge slid half out of the back of a lit Ember Orb, from behind and low, on the pale stone."""
    s = final('orb-hero')
    s['title'] = 'Core: the battery cartridge (round 32f; the cartridge is gone in round 35)'
    s['size'] = [1800, 1200]
    for p in s['set']['props']:
        if p.get('module') == 'earf_moon':
            p.update(cable=False, cartridge='out', cartridge_out=0.045)
    # from above enough that the horizon (and the sky past the stone) is out of frame, the whole ball in
    s['camera'] = {'position': [0.40, 0.70, 0.34], 'target': [0.0, 0.04, 0.07], 'lens_mm': 60, 'level': False,
                   'fstop': 8.0, 'focus': [0.0, 0.06, 0.05]}
    L = s['lights']
    L['key'].update(orbit={'azimuth_deg': 150, 'elevation_deg': 50, 'distance_m': 2.6}, target=[0.0, 0.05, 0.03])
    L['fill'].update(orbit={'azimuth_deg': 200, 'elevation_deg': 15, 'distance_m': 3.0}, target=[0.0, 0.05, 0.03])
    # the strip that drew the base's edge from behind now draws it from the front-left, toward the camera's side
    L['back'].update(position=[0.30, 0.05, 0.10], target=[0.0, 0.06, 0.03])
    # the paper behind is now the front of the sweep: the wash moves to light what the camera sees
    L['bgwash'].update(position=[0.0, 1.6, 3.0], target=[0.0, -1.0, 0.25])
    # s1 (4.5, 4.5): the room brighter than the lamp, the cartridge crushed black, the pool off to the left only, the
    # slab's far edge a seam at the top, the ball against the top edge. The room dimmed toward an evening bar's, the pool
    # from the ball's centre, a strip laid along the cartridge's top, the slab run out past the frame, the camera lower
    # and back on a longer lens, focused on the cartridge
    L['bgwash']['irradiance'] = 1.2
    s['sky']['strength'] = 0.15
    L['key']['irradiance'] = 0.35
    L['fill']['irradiance'] = 0.1
    L['pool+0.00'].update(position=[0.0, 0.0, 0.10], power_w=3.0, radius_m=0.07)
    L['cartstrip'] = {'type': 'area', 'size_m': [0.6, 0.08], 'position': [0.15, 0.45, 0.30], 'target': [0.0, 0.10, 0.02],
                      'irradiance': 1.2, 'color': 3200, 'camera': False, 'specular': 1.0}
    for p in s['set']['props']:
        if p.get('texture') == 'marble_01':
            p.update(size=[4.0, 6.0, p['size'][2]], position=[0.0, -1.0, p['position'][2]])
        if p.get('module') == 'earf_moon':
            p['shade_glow'] = 0.8
    # high enough that the horizon is out of frame (lower, the far end went a navy void)
    s['camera'] = {'position': [0.45, 0.95, 0.34], 'target': [0.0, 0.05, 0.09], 'lens_mm': 70, 'level': False,
                   'fstop': 4.0, 'focus': [0.0, 0.11, 0.02]}
    return s


def unlit():
    """Round 32e's unlit pair, the Orb cordless (its cartridge in, no cable: the short run of cable showed as a hook at
    this angle); the light through the ball raised and softened, as its pool on the oak mirrored in the polished black
    drum and read as brass."""
    s = final('unlit')
    for p in s['set']['props']:
        if p.get('fn') == 'orb':
            p.update(cable=False, cartridge='in')
    s['lights']['thru_orb'].update(target=[-0.05, -1.45, 0.45], irradiance=1.5)
    # s1 (5.5, 5.5), and the coordinator for the caption "Off, in Smoke.": the Dome's underside read as a lit white
    # disc and a warm pool lay round the Orb's base, both "on". Both lamps are off (lamp false, no glow): it was the
    # helper lights. The light through the ball kept to a faint core, the one through the Dome's mouth nearly out, and
    # the bounce under them warm (at 5000 K it turned the frosted liner blue-white)
    s['lights']['thru_orb']['irradiance'] = 0.15
    s['lights']['thru_dome'].update(irradiance=0.04, color=3400)
    s['lights']['bounce'].update(color=3500)
    return s


# each tint's glow, relative (crystal_promo.GAIN): round 32e's Orbs row was one piece, so every tint glowed alike and
# Fog clipped (s1, both critics)
POOL = {'ember': '#FF7A68', 'dust': '#FF9C78', 'acid': '#FFC870', 'poison': '#BCE07A', 'ice': '#86D2FF',
        'haze': '#B496FF', 'fog': '#FFF2E4', 'smoke': '#CDBFAF'}    # crystal_promo.POOL: each tint's light
GAIN = {'ember': 1.0, 'dust': 1.0, 'acid': 0.9, 'poison': 0.9, 'ice': 0.75, 'haze': 0.85, 'fog': 0.45, 'smoke': 0.6}


def orbs_row():
    """s1 (5.5, 5.5): the balls flat discs and Fog clipped (one glow for all: now a piece a tint, its gain, and the
    glow down from 1.8 to 1.3); the cables' run back read as stubs curling up behind each base in a lineup (the hero
    shows the cable; here they are left out); the pools faint (stronger, closer under each ball); the paper flat (the
    wash aimed lower, so it falls off up the sweep)."""
    s = final('orbs')
    props = []
    for p in s['set']['props']:
        if p.get('fn') != 'orb':
            props.append(p); continue
        for sp in p['spots']:
            q = copy.deepcopy(p); q['spots'] = [sp]; q['flavour'] = sp['flavour']
            q.update(shade_glow=round(1.3 * GAIN[sp['flavour']], 3), cable=False)
            props.append(q)
    s['set']['props'] = props
    for k, L in s['lights'].items():
        if k.startswith('pool'):
            L.update(power_w=1.6, position=[L['position'][0], -0.06, 0.04])
    s['lights']['bgwash']['target'] = [0.0, 1.0, 0.0]
    return s


def domes_row():
    """s1 (4.5, 4.5): the lamps lit nothing and the wall outshone them, the domes crammed under the top edge above an
    empty wall and a sliver of counter. Now the domes hang 38 cm over the counter (a bar's low pendants), the camera a
    little above them with a wider lens, so the cords, the domes and the counter's top all read; each dome lights the
    counter in its tint; the counter a solid block, not a slab over the floor; the wash down."""
    s = final('domes')
    for p in s['set']['props']:
        if p.get('fn') == 'dome':
            for sp in p['spots']:
                sp['position'][2] = 1.48
            # a downlight in each dome's tint lights the counter under it (its own lamp is 2700 K and hidden from
            # transmission: at 18 W it washed the wall and the counter orange, untinted)
            for sp in p['spots']:
                x = sp['position'][0]
                s['lights'][f'down{x:+.2f}'] = {'type': 'spot', 'position': [x, 0.0, 1.53], 'target': [x, 0.0, 1.10],
                                                'power_w': 5.0, 'cone_deg': 60, 'radius_m': 0.05,
                                                'color': POOL[sp['flavour']], 'camera': False, 'specular': 0.0}
        elif p.get('texture') == 'oak_veneer_01':
            p.update(size=[p['size'][0], p['size'][1], 1.10], position=[p['position'][0], p['position'][1], 0.0])
    s['camera'].update(position=[0.0, -4.6, 1.45], target=[0.0, 0.0, 1.40], lens_mm=60, focus=[0.0, 0.0, 1.45])
    s['lights']['bgwash']['irradiance'] = 2.6
    # s2 (4.5, 5.0): the domes still darker than the wall and no pools on the counter, which was a sliver. The room
    # dimmed (the wall about 150 to 170, pale still), the downlights stronger and tighter, the camera higher so the top
    # carries the pools, the wash neutral (it turned the oak salmon); Haze up and Fog down, as the row's evenness asks
    s['lights']['bgwash'].update(irradiance=1.2, color=4300)
    s['lights']['key']['irradiance'] = 0.5
    s['lights']['bounce']['irradiance'] = 0.4
    for k, L in s['lights'].items():
        if k.startswith('down'):
            L.update(power_w=18.0, cone_deg=40)
    for p in s['set']['props']:
        if p.get('fn') == 'dome' and p['flavour'] in ('haze', 'fog'):
            p['shade_glow'] = {'haze': 0.85, 'fog': 0.25}[p['flavour']]
    s['camera'].update(position=[0.0, -4.6, 1.80], target=[0.0, 0.0, 1.33])
    for k in ('rim', 'bounce'):
        if k in s['lights']:
            s['lights'][k]['position'][2] -= 0.12
            s['lights'][k]['target'][2] -= 0.12
    return s


def orb_hero():
    """s1 (6.0, 6.0): the cable drew a line across the left third (the lamp turned 40 degrees on its spot, so its
    notch faces back and the cable runs away behind the ball; at 80 its run turned to the right edge); the red pinned at 249, a flat disc (the glow
    1.1 to 0.8); the polished base without a highlight (the low strip behind becomes a tall one at the right, so a line
    runs down the drum and the ring)."""
    s = final('orb-hero')
    for p in s['set']['props']:
        if p.get('fn') == 'orb':
            p['spots'] = [{'position': p['spots'][0], 'rotate_z': -40}]
            p['shade_glow'] = 0.8
    s['lights']['back'].update(size_m=[0.08, 0.6], position=[0.45, 0.15, 0.2], target=[0.0, 0.0, 0.12],
                               irradiance=1.6, specular=1.0)
    return s


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, src in NAMES.items():
        s = {'lamps-unlit': unlit, 'lamps-orbs': orbs_row, 'lamps-domes': domes_row, 'lamp-orb': orb_hero}.get(n, lambda: final(src))()
        s['title'] = s['title'].replace('Dome and Orb', 'Hemisphere North and Core')      # round 35's names
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n, '<-', src)
    json.dump(cartridge(), open(os.path.join(SHOTS, 'lamp-cartridge.json'), 'w'), indent=1)
    print('lamp-cartridge')


def render(names, scale, out=RENDERS):
    py = os.environ.get('PY', 'python3')
    os.makedirs(out, exist_ok=True)
    for n in names:
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                        '--out', os.path.join(out, n + '.png'), '--scale', str(scale)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(n, flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    all_ = list(NAMES) + ['lamp-cartridge']
    if '--render' in a:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        render([x for x in a if x in all_] or all_, scale, out)
    else:
        build()
