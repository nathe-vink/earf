"""Terrace, a proposal for Hemisphere (the design pass of 2026-10-31; strata/README.md): the dome built from twelve
rings of stock 1/2 in cast sheet, each lapping the one above by 10 mm, bonded, annealed, the outer edges polished. Seen
from the side each terrace's edge is a contour line, and it glows: the COB's spill enters each ring through its
bead-blasted inner edge and leaves through its polished outer edge. The light engine is a turned aluminium core
through the top ring, under a stack of seven aluminium fins (the acrylic's layers again, in metal), held by three
knurled stainless thumbscrews into brass inserts. The COB looks down through a satin reflector and a honeycomb louvre.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/strata/terrace.py --out spinoffs/barkhorn/companions/strata/out-terrace

The frame: z up from the rim's underside (as crystal.py's Hemisphere), x across, y back, mm. The canopy is drawn at a
600 drop (the cord and the cable run between them).
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import stack as S                                                   # noqa: E402

P = dict(S.HT, core=56.0, core_depth=36.0, fins=(7, 120.0, 2.0, 6.0), fin_core=30.0, flange=(94.0, 4.0),
         reflector=(54.0, 72.0, 22.0), louvre=(50.0, 6.0), cap=(40.0, 14.0), drop=600.0, canopy=(130.0, 38.0),
         pcd=77.0, cob_w=4.4)


def ring_solid(l):
    s = cyl('z', (0, 0), 2 * l['ro'], l['z0'], l['z1'])
    if l['ri'] > 0:
        s = s - cyl('z', (0, 0), 2 * l['ri'], l['z0'] - 1, l['z1'] + 1)
    return s


def shade_layers(P):
    return S.halo(P) if P.get('shade') == 'halo' else S.terrace(P)


def geometry(P=P):
    L = shade_layers(P)
    top = L[-1]['z1']
    g = dict(L=L, top=top)
    g['flange'] = (top + 1.0, top + 1.0 + P['flange'][1])                # on a 1 mm gasket
    n, od, t, pitch = P['fins']
    g['fin_z'] = [g['flange'][1] + 4.0 + i * pitch for i in range(n)]
    g['fin_top'] = g['fin_z'][-1] + t
    g['cap'] = (g['fin_top'], g['fin_top'] + P['cap'][1])
    g['cob_z'] = top - P['core_depth']                                     # the COB's face
    g['canopy'] = (g['cap'][1] + P['drop'], g['cap'][1] + P['drop'] + P['canopy'][1])
    return g


def parts(P):
    g = geometry(P)
    L, top = g['L'], g['top']
    out = []
    for k, l in enumerate(L):
        out.append(Part(f'ring-{k + 1:02d}', ring_solid(l), Sheet('cast-acrylic', 12, face='+z'), finish='tint',
                        group='shade', render=False,
                        notes=[f'{l["tint"]} (TruCast {S.TINTS[l["tint"]][0]}), stock 1/2 in cast sheet, CNC-routed '
                               f'{2 * l["ro"] + 3:.0f} / {2 * l["ri"] - 3:.0f} (finished {2 * l["ro"]:.0f} / {2 * l["ri"]:.0f} '
                               'after bonding: the outer edge diamond-polished, the inner edge bead-blasted)']))
    from build123d import Rot
    angs = (90.0, 210.0, 330.0)
    if P.get('shade') == 'halo':
        # the engine's plate sits on the top disc over its bore, on a gasket; three thumbscrews down into brass inserts
        # in the top disc's face, outside the fins' reach
        ri_top = L[-1]['ri']
        fo = 2 * ri_top + 16.0
        rp = ri_top + 4.0
        pts = [(rp * math.cos(math.radians(a)), rp * math.sin(math.radians(a))) for a in angs]
        out.append(Part('inserts', union(*[cyl('z', p, 5.6, top - 8, top) for p in pts]), Bought('brass-insert-m4'),
                        qty=3, group='shade', inside=True, render=False,
                        notes=['heat-set into the top disc\'s face, 8 deep, after polishing']))
        gas = cyl('z', (0, 0), fo, top, top + 1.0) - cyl('z', (0, 0), 2 * ri_top + 2, top - 1, top + 2)
        for p in pts:
            gas = gas - cyl('z', p, 5.0, top - 1, top + 2)
        out.append(Part('gasket', gas, Bought('silicone-gasket'), finish='rubber', group='engine'))
        fl = cyl('z', (0, 0), fo, *g['flange']) - cyl('z', (0, 0), P['core'] - 0.2, g['flange'][0] - 1, g['flange'][1] + 1)
        for p in pts:
            fl = fl - cyl('z', p, 4.5, g['flange'][0] - 1, g['flange'][1] + 1)
        out.append(Part('flange', fl, Machined('aluminium', 'lathe'), finish='anodised', group='engine',
                        notes=[f'6061, turned, bead-blasted and black anodised: a {fo:.0f} plate over the bore, three '
                               '4.5 holes for the thumbscrews']))
        thumbs = union(*[cyl('z', p, 12.0, g['flange'][1], g['flange'][1] + 6) + cyl('z', p, 4.0, top - 7, g['flange'][1])
                         for p in pts])
    else:
        # the shade hangs from the flange's skirt: three radial M4 thumbscrews through it into brass inserts set
        # radially in the top ring's edge (at 90, 210 and 330 deg), easy to reach under the fins
        zs = top - 5.5
        ro_top = L[-1]['ro']

        def radial(r0, r1, d):
            return [Rot(0, 0, a) * cyl('x', (0, zs), d, r0, r1) for a in angs]
        out.append(Part('inserts', union(*radial(ro_top - 8, ro_top, 5.6)), Bought('brass-insert-m4'),
                        qty=3, group='shade', inside=True, render=False,
                        notes=['heat-set radially into the top ring\'s edge, 8 deep, after polishing']))
        gas = cyl('z', (0, 0), 2 * ro_top, top, top + 1.0) - cyl('z', (0, 0), P['core'] + 1, top - 1, top + 2)
        out.append(Part('gasket', gas, Bought('silicone-gasket'), finish='rubber', group='engine'))
        fo = 2 * ro_top + 6.0
        fl = cyl('z', (0, 0), fo, *g['flange']) + (cyl('z', (0, 0), fo, top - 12, g['flange'][0]) -
                                                    cyl('z', (0, 0), 2 * ro_top + 0.6, top - 13, g['flange'][0] + 0.01))
        fl = fl - cyl('z', (0, 0), P['core'] - 0.2, g['flange'][0] - 1, g['flange'][1] + 1)
        for sh in radial(ro_top - 1, fo / 2 + 1, 4.5):
            fl = fl - sh
        out.append(Part('flange', fl, Machined('aluminium', 'lathe'), finish='anodised', group='engine',
                        notes=[f'6061, turned, bead-blasted and black anodised: a {fo:.0f} disc with a skirt down over the '
                               'top ring\'s edge, three 4.5 holes radially for the thumbscrews']))
        thumbs = union(*radial(fo / 2, fo / 2 + 6, 12.0), *radial(ro_top - 7, fo / 2, 4.0))
    # the core: through the top ring, the COB on its underside; hollow above for the wires
    core = cyl('z', (0, 0), P['core'], g['cob_z'], g['flange'][1]) - cyl('z', (0, 0), 20.0, g['cob_z'] + 6, g['flange'][1] + 1)
    core = core + cyl('z', (0, 0), P['fin_core'], g['flange'][1], g['fin_top'])
    core = core - cyl('z', (0, 0), 12.0, g['flange'][1] - 1, g['fin_top'] + 1)
    out.append(Part('core', core, Machined('aluminium', 'lathe'), finish='anodised', group='engine',
                    notes=['6061 from 2 1/2 in bar: the COB\'s seat (an Ideal Chip-Lok holder, two M3) faced flat on its '
                           'underside, thermal pad; up through the top ring with 2 mm clearance; its spigot above takes '
                           'the fins on spacers and the cap, an M20 thread']))
    n, od, t, pitch = P['fins']
    for i, z in enumerate(g['fin_z']):
        fin = cyl('z', (0, 0), od, z, z + t) - cyl('z', (0, 0), P['fin_core'] + 0.1, z - 1, z + t + 1)
        out.append(Part(f'fin-{i + 1}', fin, Sheet('aluminium', 2, face='+z'), finish='anodised', group='engine',
                        notes=[f'one of {n} discs {od:.0f} across of 2 mm 5052, laser-cut, black anodised, at {pitch:.0f} '
                               'pitch on turned spacers: the acrylic\'s stack again, in metal']))
    cap = cyl('z', (0, 0), P['cap'][0], *g['cap']) - cyl('z', (0, 0), 12.0, g['cap'][0] - 1, g['cap'][1] - 4)
    out.append(Part('cap', cap, Machined('aluminium', 'lathe'), finish='anodised', group='engine',
                    notes=['the cord grip and the cable gripper go into its top, side by side']))
    out.append(Part('thumbscrews', thumbs, Bought('ss-thumb-m4'), qty=3, finish='steel', group='engine',
                    notes=['tool-free: the shade comes off with the lamp lowered, to clean or to change its tint']))
    # the optics: the COB, the reflector, the louvre
    r0, r1, h = P['reflector']
    refl = (cyl('z', (0, 0), r1, g['cob_z'] - h, g['cob_z']) - cyl('z', (0, 0), r1 - 2, g['cob_z'] - h - 1, g['cob_z'] + 1))
    out.append(Part('reflector', refl, Bought('cob-reflector'), finish='satin', group='optics',
                    notes=['bead-blasted inside: about a quarter of the light spills wide, onto the rings\' inner edges']))
    out.append(Part('cob', cyl('z', (0, 0), 19.0, g['cob_z'] - 1.6, g['cob_z']), Bought('vero-se10'), finish='led',
                    group='optics'))
    lv, lt = P['louvre']
    out.append(Part('louvre', cyl('z', (0, 0), lv, g['cob_z'] - 8 - lt, g['cob_z'] - 8), Bought('honeycomb-louvre'),
                    finish='anodised', group='optics'))
    # the suspension: cord and cable, the canopy with its crossbar and driver
    c0, c1 = g['canopy']
    out.append(Part('cord', cyl('z', (-7, 0), 6.0, g['cap'][1], c0), Bought('fabric-cord-182'), finish='fabric',
                    group='suspension'))
    out.append(Part('cable', cyl('z', (7, 0), 1.5, g['cap'][1] + 8, c0 - 6), Bought('ss-cable'), finish='steel',
                    group='suspension'))
    grips = union(cyl('z', (-7, 0), 12.0, g['cap'][1], g['cap'][1] + 10), cyl('z', (7, 0), 9.0, g['cap'][1], g['cap'][1] + 8),
                  cyl('z', (-7, 0), 12.0, c0 - 10, c0), cyl('z', (7, 0), 9.0, c0 - 6, c0))
    out.append(Part('grips', grips, Bought('cord-grip'), qty=2, finish='trim', group='suspension'))
    out.append(Part('grippers', None, Bought('cable-gripper'), qty=2))
    can = cyl('z', (0, 0), P['canopy'][0], c0, c1) - cyl('z', (0, 0), P['canopy'][0] - 4, c0 + 2, c1 + 1)
    out.append(Part('canopy', can, Machined('aluminium', 'lathe'), finish='anodised', group='suspension',
                    notes=['spun or turned aluminium, black anodised; the ERP driver inside, on the crossbar']))
    out += [Part('driver', None, Bought('erp-ess010w')), Part('crossbar', None, Bought('canopy-crossbar'))]
    return out


def checks(P=P):
    g = geometry(P)
    L = g['L']
    m_acr = S.mass(L)
    n, od, t, pitch = P['fins']
    area = S.fin_stack_area(n, od, P['fin_core'], t, pitch)
    q = 0.75 * P['cob_w']
    rise = S.sink_rise(q, area, h=5.0, eff=0.75)          # close-pitched fins: a low h
    m_al = (n * math.pi * ((od / 2) ** 2 - (P['fin_core'] / 2) ** 2) * t + math.pi * (P['core'] / 2) ** 2 * P['core_depth'] * 0.6
            + math.pi * (P['flange'][0] / 2) ** 2 * P['flange'][1] + math.pi * (P['cap'][0] / 2) ** 2 * P['cap'][1] * 0.7) * S.RHO_AL
    widths = [l['ro'] - l['ri'] for l in L]
    return dict(m_acr=m_acr, m_al=m_al, area=area, q=q, rise=rise, widths=(min(widths), max(widths)),
                od=2 * L[0]['ro'], h=L[-1]['z1'], cut_off=math.degrees(math.atan2(P['louvre'][0] / 2, 8 + P['louvre'][1] + 4)))


def _notes():
    c = checks()
    return [
        'A proposal (strata/README.md): Hemisphere built from stacked rings. The current Hemisphere (dome_pendant.py) '
        'stays the baseline.',
        f'The shade: 12 rings of 1/2 in cast sheet, {c["od"]:.0f} across and {c["h"]:.0f} tall ({12 * S.T_REAL:.0f} at '
        f'12.7), each {c["widths"][0]:.0f} to {c["widths"][1]:.0f} wide, lapping the ring above by 10 (the bond). '
        'Routed from sheet with no mould; bonded in a stepped jig with polymerising cement; annealed; the outer edges '
        f'diamond-polished, the inner edges bead-blasted. About {c["m_acr"]:.2f} kg of acrylic.',
        f'The light: a Bridgelux Vero SE 10 at 180 mA (about 590 lm, 4.4 W), recessed {P["core_depth"]:.0f} up the '
        'shade in a satin reflector, behind a 3.2 honeycomb louvre: no view of the COB beyond about 30 deg off the '
        'axis. A quarter of its light spills from the satin reflector onto the rings\' blasted inner edges, and leaves '
        'through their polished outer edges: each terrace glows as a line.',
        f'Heat (worked): about {c["q"]:.1f} W into seven 120 fins ({c["area"]:.3f} m2 of black anodise), at a low h for '
        f'their close pitch: about {c["rise"]:.0f} K over the room air. The COB\'s case runs about 40 C, and the top '
        f'ring under its gasket well under {S.ACRYLIC_LIMIT_C:.0f} C. Against the current top (about 0.010 m2, about '
        '31 K), about ten times the area.',
        f'Weight: about {c["m_acr"] + c["m_al"]:.1f} kg on a 1.5 mm stainless cable (break about 1.7 kN) and a listed '
        'gripper; the cord carries current only (certification.md: the shade hangs from a support, not the cord).',
        'Service: three thumbscrews and the shade lifts off the engine; the COB is on two screws in a Chip-Lok holder; '
        'the driver is in the canopy. Every part can be replaced.',
    ]


PRODUCT = Product('terrace', 'Terrace', 'Pendant: a dome of twelve stacked tint rings, its terraces lit',
                  params=P, parts=parts, count=1, touching=[('inserts', 'ring-12'), ('gasket', 'ring-12'),
                                                            ('flange', 'gasket'), ('core', 'flange'),
                                                            *[(f'fin-{i}', 'core') for i in range(1, 8)],
                                                            ('cap', 'core'), ('thumbscrews', 'flange'),
                                                            ('thumbscrews', 'inserts'), ('thumbscrews', 'gasket'),
                                                            ('thumbscrews', 'ring-12'), ('reflector', 'core'),
                                                            ('cob', 'core'), ('cord', 'grips'), ('cable', 'grips'),
                                                            ('grips', 'cap'), ('grips', 'canopy'), ('cord', 'canopy'),
                                                            ('cable', 'canopy'), ('core', 'gasket'), ('core', 'ring-12'),
                                                            ('core', 'ring-11'), ('reflector', 'ring-10'),
                                                            ('cob', 'reflector'), ('louvre', 'reflector')],
                  materials={'tint': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#D8283A', 'radius': 0.02,
                                      'roughness': 0.03},
                             'anodised': {'preset': 'metal', 'color': '#2A2A2D', 'roughness': 0.4},
                             'satin': {'preset': 'metal', 'color': '#C8C8C8', 'roughness': 0.45},
                             'steel': {'preset': 'metal', 'color': '#B8B8B8', 'roughness': 0.25},
                             'rubber': {'preset': 'rubber', 'color': '#1A1A1A'},
                             'fabric': {'preset': 'rubber', 'color': '#141414', 'roughness': 0.8},
                             'trim': {'preset': 'gloss_plastic', 'color': '#0C0C0D'},
                             'led': {'preset': 'emit', 'color': '#FFC890', 'strength': 0.0}},
                  notes=_notes(), drawing_prefix='ETR', origin=(0.0, 0.0, 1e-6))


if __name__ == '__main__':
    for n in _notes():
        print('-', n)
