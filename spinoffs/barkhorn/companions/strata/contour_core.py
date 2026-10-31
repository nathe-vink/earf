"""Contour Core, a proposal for Core (the design pass of 2026-10-31; strata/README.md): the ball drawn in contour lines.
Thirteen rings of stock 1/2 in cast sheet, each the sphere's section at its height, bonded into a terraced ball 160
across; inside, a stock opal globe lit by the warm-dim LED in the base. The terraces' polished edges glow as lines.
The ball lifts off the base (the globe stays), so balls still swap colour, as the current Core's do.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/strata/contour_core.py --out spinoffs/barkhorn/companions/strata/out-contour-core

The frame: z up from the table, x across, y back, mm.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import stack as S                                                   # noqa: E402

P = dict(S.CC, base_d=120.0, led_w=2.5)


def ring_solid(l):
    s = cyl('z', (0, 0), 2 * l['ro'], l['z0'], l['z1'])
    if l['ri'] > 0:
        s = s - cyl('z', (0, 0), 2 * l['ri'], l['z0'] - 1, l['z1'] + 1)
    return s


def centre_z(P=P):
    return P['base_top'] + P['n'] * S.T / 2 - P['skip'] * S.T


def parts(P):
    L = S.contour_core(P)
    out = []
    for k, l in enumerate(L):
        out.append(Part(f'ring-{k + 1:02d}', ring_solid(l), Sheet('cast-acrylic', 12, face='+z'), finish='tint',
                        group='ball', render=False,
                        notes=[f'{l["tint"]} (TruCast {S.TINTS[l["tint"]][0]}), stock 1/2 in cast sheet, CNC-routed '
                               f'{2 * l["ro"] + 3:.0f}' + (f' / {2 * l["ri"] - 3:.0f}' if l['ri'] else ' (whole)')
                               + ', finished after bonding: outer edge diamond-polished, inner edge bead-blasted (so the globe\'s outline melts into the rings)']))
    bt, bd = P['base_top'], P['base_d']
    zc = centre_z(P)
    gd, gn = P['globe']
    # the base: turned 6061, black anodised; a pocket from below for the dimmer and the jack, a boss for the LED
    base = cyl('z', (0, 0), bd, 0, bt) - cyl('z', (0, 0), bd - 10, 0, bt - 6)
    base = base + cyl('z', (0, 0), 36.0, 2.0, bt - 6)                        # the LED's heat boss
    base = base - cyl('y', (0, 10.0), 9.0, bd / 2 - 6, bd / 2 + 1)            # the jack, at the back
    base = base - cyl('x', (0, 10.0), 7.0, bd / 2 - 6, bd / 2 + 1)            # the dimmer's shaft, on the right
    out.append(Part('base', base, Machined('aluminium', 'lathe'), finish='anodised', group='base',
                    notes=['6061 from 5 in bar, bead-blasted, black anodised; the ball sits on its silicone ring, located '
                           'by the globe\'s holder; the LED on its boss, the heat into the whole base']))
    ring_seat = cyl('z', (0, 0), 2 * L[0]['ro'] - 4, bt - 1.0, bt) - cyl('z', (0, 0), 2 * L[0]['ri'] + 4, bt - 2, bt + 1)
    out.append(Part('seat', ring_seat, Bought('silicone-gasket'), finish='rubber', group='base',
                    notes=['a 1 mm silicone ring, let into a 1 mm recess in the base\'s top: the ball sits on it']))
    holder = cyl('z', (0, 0), 2 * L[0]['ri'] - 1.0, bt, bt + 8) - cyl('z', (0, 0), gn + 0.6, bt - 1, bt + 9)
    out.append(Part('holder', holder, Machined('aluminium', 'lathe'), finish='anodised', group='base',
                    notes=['holds the globe\'s neck (three nylon-tipped set screws) and locates the ball']))
    # the globe and its LED
    from build123d import Sphere, Pos
    glob = Pos(0, 0, zc) * (Sphere(gd / 2) - Sphere(gd / 2 - 2.5))
    glob = glob - cyl('z', (0, 0), gn - 5, zc - gd / 2 - 1, zc - gd / 2 + 8)
    z_neck0 = bt + 2
    neck = cyl('z', (0, 0), gn, z_neck0, zc - math.sqrt((gd / 2) ** 2 - ((gn - 5) / 2) ** 2)) - \
        cyl('z', (0, 0), gn - 5, z_neck0 - 1, zc)
    out.append(Part('globe', glob + neck, Bought('opal-globe'), finish='opal', group='light', inside=True))
    out.append(Part('led', cyl('z', (0, 0), 30.0, bt - 6, bt - 4.4), Bought('led-module-30'), finish='led',
                    group='light', inside=True))
    knob = cyl('x', (0, 10.0), 16.0, bd / 2 + 0.5, bd / 2 + 12)
    jack = cyl('y', (0, 10.0), 11.0, bd / 2 - 1, bd / 2 + 3)
    bumps = union(*[cyl('z', (46 * math.cos(math.radians(45 + 90 * i)), 46 * math.sin(math.radians(45 + 90 * i))),
                        12.7, -0.0, 0.01) for i in range(4)])
    out += [Part('knob', knob, Machined('stainless', 'lathe'), finish='steel', group='base',
                 notes=['304 stainless, diamond-knurled: turn to dim (2700 to 2200 K as it dims), click off']),
            Part('jack', jack, Bought('dc-jack-sealed'), finish='steel', group='base'),
            Part('dimmer', None, Bought('pwm-dimmer-24v')), Part('driver', None, Bought('cc-module-ldd')),
            Part('adapter', None, Bought('adapter-24v-class2')),
            Part('cover', cyl('z', (0, 0), bd - 11, 0.6, 2.6), Sheet('aluminium', 2, face='-z'), finish='anodised',
                 group='base'),
            Part('bumpers', bumps, Bought('silicone-bumpers'), finish='rubber', group='base')]
    return out


def checks():
    L = S.contour_core(P)
    m = S.mass(L)
    bd, bt = P['base_d'], P['base_top']
    m_base = (math.pi * (bd / 2) ** 2 * bt * 0.35) * S.RHO_AL
    cg = (m * S.centroid_z(L) + m_base * bt / 2) / (m + m_base)
    area = (math.pi * bd * bt + math.pi * (bd / 2) ** 2) * 1e-6
    rise = S.sink_rise(0.75 * P['led_w'], area, h=10.0)
    zc = centre_z(P)
    gr = P['globe'][0] / 2
    clear = min(l['ri'] - math.sqrt(max(gr ** 2 - min(abs(l['z0'] - zc), abs(l['z1'] - zc)) ** 2, 0.0))
                if l['ri'] > 0 and not (l['z0'] < zc < l['z1']) else (l['ri'] - gr if l['ri'] > 0 else 99)
                for l in L)
    return dict(m=m, m_base=m_base, cg=cg, tip=S.tip_angle(cg, bd / 2 - 6), area=area, rise=rise, clear=clear,
                h=L[-1]['z1'])


def _notes():
    c = checks()
    return [
        'A proposal (strata/README.md): Core as a ball drawn in contour lines. The current Core (orb_table.py) stays '
        'the baseline.',
        f'The ball: 13 rings of 1/2 in cast sheet, each the 160 sphere\'s section at its height (its tread the sheet\'s '
        f'own face), bonded in a stepped jig, annealed, outer edges diamond-polished, inner edges bead-blasted (seen through clear inner edges the globe read as a bulb in a jar). About '
        f'{c["m"]:.2f} kg of acrylic; the lamp {c["h"]:.0f} tall.',
        f'The light: a 30 warm-dim LED board (2.5 W, 2700 to 2200 K) on the base\'s boss, up into a stock 4 in opal '
        f'globe; the globe clears the rings by at least {c["clear"]:.0f} mm.',
        f'Heat (worked): about {0.75 * P["led_w"]:.1f} W into the base ({c["area"] * 1e4:.0f} cm2 of black anodise): '
        f'about {c["rise"]:.0f} K over the room. The globe\'s air and the acrylic stay far under {S.ACRYLIC_LIMIT_C:.0f} C.',
        f'Stability: about {c["m"] + c["m_base"]:.1f} kg, its centre about {c["cg"]:.0f} up; it tips at about '
        f'{c["tip"]:.0f} deg.',
        'Service: the ball lifts off (it swaps colour, as now); the globe comes out of its holder (three set screws); '
        'the LED is on two screws. The v1 plug-in power, the battery an option in the base later.',
    ]


PRODUCT = Product('contour-core', 'Contour Core', 'Table lamp: a ball of thirteen stacked tint rings over an opal globe',
                  params=P, parts=parts, count=1,
                  touching=[('seat', 'base'), ('holder', 'base'), ('globe', 'holder'), ('led', 'base'),
                            ('knob', 'base'), ('jack', 'base'), ('cover', 'base'), ('bumpers', 'cover'),
                            ('holder', 'ring-01'), ('seat', 'ring-01'), ('globe', 'base')],
                  materials={'tint': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#E0861E', 'radius': 0.02,
                                      'roughness': 0.03},
                             'anodised': {'preset': 'metal', 'color': '#2A2A2D', 'roughness': 0.4},
                             'steel': {'preset': 'metal', 'color': '#B8B8B8', 'roughness': 0.25},
                             'rubber': {'preset': 'rubber', 'color': '#1A1A1A'},
                             'opal': {'preset': 'frosted', 'color': '#F4F2EE'},
                             'led': {'preset': 'emit', 'color': '#FFC890', 'strength': 0.0}},
                  notes=_notes(), drawing_prefix='ECC', origin=(0.0, 0.0, 1e-6))


if __name__ == '__main__':
    for n in _notes():
        print('-', n)
