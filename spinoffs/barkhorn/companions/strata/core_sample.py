"""Core Sample, a proposal for Core (the design pass of 2026-10-31; strata/README.md): a column of fourteen tint discs
cut from stock 1/2 in cast sheet, bonded, annealed, turned true and polished, bored up the middle, and lit by a
filament: two dim-to-warm LED runs on an aluminium spine inside an opal tube. Each disc's edge glows, the bond lines
read as strata, and the column throws coloured light on the table. It stands on a turned aluminium foot set in under
it, a shadow line; the plug-in v1 power (a listed 24 V Class 2 adapter) and a knurled stainless dimmer knob.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/strata/core_sample.py --out spinoffs/barkhorn/companions/strata/out-core-sample

The frame: z up from the table, x across, y back, mm.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import stack as S                                                   # noqa: E402

P = dict(S.CS)


def ring_solid(l):
    s = cyl('z', (0, 0), 2 * l['ro'], l['z0'], l['z1'])
    if l['ri'] > 0:
        s = s - cyl('z', (0, 0), 2 * l['ri'], l['z0'] - 1, l['z1'] + 1)
    return s


def parts(P):
    L = S.core_sample(P)
    fd, fh = P['base']
    z_col = L[0]['z0']
    out = []
    for k, l in enumerate(L):
        out.append(Part(f'disc-{k + 1:02d}', ring_solid(l), Sheet('cast-acrylic', 12, face='+z'), finish='tint',
                        group='column', render=False,
                        notes=[f'{l["tint"]} (TruCast {S.TINTS[l["tint"]][0]}), stock 1/2 in cast sheet, CNC-cut '
                               f'{2 * l["ro"] + 4:.0f} round (turned to {2 * l["ro"]:.0f} after bonding)'
                               + (f', a {2 * l["ri"] - 4:.0f} pilot hole (bored to {2 * l["ri"]:.0f})' if l['ri'] else
                                  ', whole (the top: the bore is blind)')]))
    # the brass inserts in the bottom disc's underside, and the screws from under the foot
    n, pcd, _ = P['inserts']
    pts = [(pcd / 2 * math.cos(math.radians(90 + 120 * i)), pcd / 2 * math.sin(math.radians(90 + 120 * i))) for i in range(n)]
    ins = union(*[cyl('z', p, 7.0, z_col, z_col + 10) for p in pts])
    out.append(Part('inserts', ins, Bought('brass-insert-m5'), qty=3, group='column', inside=True, render=False,
                    notes=['pressed (or heat-set) into 6.4 holes drilled 11 deep in the bottom disc after turning']))
    # the foot: turned 6061, black anodised, set 7 in under the column (a shadow line); a pocket from below for the
    # dimmer, a bore for the light engine's plug, three counterbored screw holes, the knob and the jack through its wall
    foot = cyl('z', (0, 0), fd, 0, fh) - cyl('z', (0, 0), fd - 8, 0, fh - 4) - cyl('z', (0, 0), 30.4, fh - 5, fh + 1)
    for p in pts:
        foot = foot - cyl('z', p, 5.5, fh - 5, fh + 1)
    foot = foot - cyl('y', (0, 6.0), 9.0, fd / 2 - 6, fd / 2 + 1)            # the jack's M8 bush, at the back
    foot = foot - cyl('x', (0, 6.0), 7.0, fd / 2 - 6, fd / 2 + 1)            # the dimmer's shaft, on the right
    out.append(Part('foot', foot, Machined('aluminium', 'lathe'), finish='anodised', group='foot',
                    notes=['6061 turned from 4 in bar, the pocket and holes milled, bead-blasted, black anodised',
                           'the column\'s three M5 screws go up through its top into the bottom disc\'s inserts; '
                           'nylon washers under their heads']))
    cover = cyl('z', (0, 0), fd - 9, 0.6, 2.6)
    out.append(Part('cover', cover, Sheet('aluminium', 2, face='-z'), finish='anodised', group='foot',
                    notes=['2 mm 5052, black anodised, four M3 countersunk screws into tapped bosses (not drawn)']))
    bumps = union(*[cyl('z', (36 * math.cos(math.radians(45 + 90 * i)), 36 * math.sin(math.radians(45 + 90 * i))),
                        12.7, 0.0, 0.6) for i in range(4)])
    out.append(Part('bumpers', bumps, Bought('silicone-bumpers'), finish='rubber', group='foot'))
    out.append(Part('screws', None, Bought('ss-button-m5'), qty=3))
    out.append(Part('cover-screws', None, Bought('ss-csk-m3'), qty=4))
    # the light engine: a plug in the foot's bore, the spine up the bore with two LED runs, the opal tube over it
    plug = cyl('z', (0, 0), 30.0, fh - 5, fh + 2)
    spine = box(-5, -5, fh + 2, 5, 5, fh + 2 + P['bar'][1])
    ls = P['bar'][1] - 8
    strips = union(box(-4, -5.8, fh + 6, 4, -5.0, fh + 6 + ls), box(-4, 5.0, fh + 6, 4, 5.8, fh + 6 + ls))
    od, wall, ln = P['tube']
    tube = cyl('z', (0, 0), od, fh + 2, fh + 2 + ln) - cyl('z', (0, 0), od - 2 * wall, fh + 1, fh + ln - 1)
    out += [Part('plug', plug, Machined('aluminium', 'lathe'), finish='anodised', group='engine', inside=True,
                 notes=['carries the spine (an M4 screw up its centre) and the tube (a 1 mm groove); held in the foot '
                        'by two M3 set screws, so the whole engine drops out of the bottom once the cover is off']),
            Part('spine', spine, Machined('aluminium', 'cnc-mill'), finish='aluminium', group='engine', inside=True,
                 notes=['10 mm square 6063 bar, 140 long: the strips\' heat path down to the plug and the foot']),
            Part('strips', strips, Bought('d2w-strip'), finish='led', group='engine', inside=True),
            Part('tube', tube, Bought('opal-tube'), finish='opal', group='engine', inside=True,
                 notes=['the filament: lit from inside, it is what the eye sees through the strata'])]
    knob = cyl('x', (0, 6.0), 16.0, fd / 2 + 0.5, fd / 2 + 12)
    jack = cyl('y', (0, 6.0), 11.0, fd / 2 - 1, fd / 2 + 3)
    out += [Part('knob', knob, Machined('stainless', 'lathe'), finish='steel', group='foot',
                 notes=['304 stainless, turned and diamond-knurled, a set screw onto the dimmer\'s 6 mm D shaft: turn '
                        'to dim, click off at the end of its travel']),
            Part('dimmer', None, Bought('pwm-dimmer-24v')),
            Part('jack', jack, Bought('dc-jack-sealed'), finish='steel', group='foot'),
            Part('adapter', None, Bought('adapter-24v-class2'))]
    return out


def heat():
    """The light engine's heat path, worked: 4.4 W of strips at full, about 3.3 W of it heat (the rest light)."""
    q = 0.75 * P['led_w']
    bar_R = P['bar'][1] * 1e-3 / (2 * 200.0 * 1e-4)                 # 6063 bar, k 200, 10 x 10: half its length on average, K/W
    fd, fh = P['base']
    foot_area = (math.pi * fd * fh + math.pi * (fd / 2) ** 2) * 1e-6
    foot_rise = S.sink_rise(q, foot_area, h=10.0)
    return dict(q=q, bar_rise=q * bar_R, foot_area=foot_area, foot_rise=foot_rise,
                spine_top=25 + foot_rise + q * bar_R)


def _notes():
    L = S.core_sample(P)
    m = S.mass(L)
    h = heat()
    cg = S.centroid_z(L)
    return [
        'A proposal (strata/README.md): Core as a core sample. The current Core (orb_table.py) stays the baseline.',
        f'The column: {len(L)} discs of 1/2 in cast sheet ({len(L) * S.T_REAL:.0f} tall at 12.7; the CAD uses 12), '
        f'{P["od"]:.0f} across, bonded with polymerising cement (Weld-On 40 class) in a press jig, annealed (80 C, '
        'slow cool), turned true; disc by disc (masked on the lathe) its outside diamond-turned and buffed clear or '
        'bead-blasted satin, so the strata differ in finish as well as tint; its bore bored to 32 and polished. '
        f'About {m:.2f} kg of acrylic.',
        f'The light: two runs of dim-to-warm strip (2700 to about 1900 K) on a 10 mm aluminium spine, inside an opal '
        f'tube that ends just inside the Clear cap, whose bore is bead-blasted (so the cap glows evenly), about {P["led_w"]:.1f} W '
        f'and about 300 lm at full. The engine drops out of the bottom: the cover\'s four screws, then '
        'two set screws.',
        f'Heat (worked): about {h["q"]:.1f} W of heat down the spine (about {h["bar_rise"]:.0f} K along it) into the '
        f'foot, {h["foot_area"] * 1e4:.0f} cm2 of black anodise: about {h["foot_rise"]:.0f} K over the room. In a '
        f'25 C room the spine\'s top runs about {h["spine_top"]:.0f} C, and the bore\'s wall less, against '
        f'{S.ACRYLIC_LIMIT_C:.0f} C for the acrylic. To confirm with thermocouples on the first one.',
        f'Stability: the whole about {m + 0.25:.1f} kg, its centre about {cg:.0f} up; it tips at about '
        f'{S.tip_angle(cg, P["base"][0] / 2):.0f} deg on its {P["base"][0]:.0f} foot.',
        'Power: the v1 plug-in (launch/core-v1-plugin.md): a listed 24 V Class 2 adapter into a sealed jack at the '
        'back. The battery stays an option: the foot\'s pocket takes a cell carrier later, the column unchanged.',
    ]


PRODUCT = Product('core-sample', 'Core Sample', 'Table lamp: a bored column of bonded tint discs, lit from within',
                  params=P, parts=parts, count=1, touching=[('inserts', 'disc-01'), ('plug', 'foot'),
                                                            ('spine', 'plug'), ('tube', 'plug'), ('strips', 'spine'),
                                                            ('jack', 'foot'), ('knob', 'foot'), ('cover', 'foot'),
                                                            ('bumpers', 'cover')],
                  materials={'tint': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#D8283A', 'radius': 0.02,
                                      'roughness': 0.03},
                             'anodised': {'preset': 'metal', 'color': '#2A2A2D', 'roughness': 0.4},
                             'aluminium': {'preset': 'metal', 'color': '#C8C8C8', 'roughness': 0.3},
                             'steel': {'preset': 'metal', 'color': '#B8B8B8', 'roughness': 0.25},
                             'rubber': {'preset': 'rubber', 'color': '#1A1A1A'},
                             'opal': {'preset': 'frosted', 'color': '#F4F2EE'},
                             'led': {'preset': 'emit', 'color': '#FFC890', 'strength': 0.0}},
                  notes=_notes(), drawing_prefix='ECS', origin=(0.0, 0.0, 1e-6))


if __name__ == '__main__':
    for n in _notes():
        print('-', n)
