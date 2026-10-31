"""Halo, a second proposal for Hemisphere (the design pass of 2026-10-31; strata/README.md): Core Sample's pendant
twin. Five discs of stock 1/2 in cast sheet, 260 across with a 160 bore, bonded into a thick ring of strata (Dust,
one Ember stratum), polished and satin in turns; the same light engine as Terrace (the COB in a satin reflector over a
honeycomb louvre, the stacked aluminium fins) sits on a plate over the bore. The light falls straight through the open
bore onto the table; the reflector's spill enters the discs through their blasted inner edges and leaves through their
outer edges and faces, so the ring glows in bands.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/strata/halo.py --out spinoffs/barkhorn/companions/strata/out-halo

The frame: z up from the ring's underside, x across, y back, mm.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import terrace as TR                                                # noqa: E402  (puts the fab kit on the path)
from kit import Product                                             # noqa: E402
import stack as S                                                   # noqa: E402

P = dict(TR.P, **S.HL, shade='halo', core_depth=30.0)


def _notes():
    c = TR.checks(P)
    L = S.halo(P)
    return [
        'A proposal (strata/README.md): Hemisphere as a ring of strata, the pendant twin of Core Sample. The current '
        'Hemisphere (dome_pendant.py) stays the baseline.',
        f'The ring: {P["n"]} discs of 1/2 in cast sheet ({" / ".join(P["stack"])} from the bottom), {P["od"]:.0f} across '
        f'with a {P["id"]:.0f} bore, {L[-1]["z1"]:.0f} tall ({P["n"] * S.T_REAL:.0f} at 12.7), bonded, annealed; the '
        f'outside turned and, disc by disc, buffed clear or bead-blasted satin; the bore blasted. About {c["m_acr"]:.2f} '
        'kg of acrylic.',
        'The light: Terrace\'s engine (a Vero SE 10 at 180 mA, about 590 lm, in a satin reflector behind a honeycomb '
        'louvre), on a plate over the bore held by three thumbscrews. The table gets the COB\'s light straight through '
        'the bore; the ring glows from the spill.',
        f'Heat (worked): the same seven fins: about {c["rise"]:.0f} K over the room; the plate sits on a gasket on the '
        f'top disc, far under {S.ACRYLIC_LIMIT_C:.0f} C.',
        f'Weight: about {c["m_acr"] + c["m_al"]:.1f} kg on the 1.5 mm stainless cable and a listed gripper.',
        'Service: three thumbscrews and the ring lifts off the engine; the COB on two screws; the driver in the canopy.',
    ]


PRODUCT = Product('halo', 'Halo', 'Pendant: a thick ring of bonded tint discs, lit from its bore',
                  params=P, parts=TR.parts, count=1,
                  touching=[('inserts', 'ring-05'), ('gasket', 'ring-05'), ('flange', 'gasket'), ('core', 'flange'),
                            *[(f'fin-{i}', 'core') for i in range(1, 8)], ('cap', 'core'),
                            ('thumbscrews', 'flange'), ('thumbscrews', 'inserts'), ('thumbscrews', 'gasket'),
                            ('thumbscrews', 'ring-05'), ('reflector', 'core'), ('cob', 'core'), ('cord', 'grips'),
                            ('cable', 'grips'), ('grips', 'cap'), ('grips', 'canopy'), ('cord', 'canopy'),
                            ('cable', 'canopy'), ('cob', 'reflector'), ('louvre', 'reflector')],
                  materials=TR.PRODUCT.materials, notes=_notes(), drawing_prefix='EHL', origin=(0.0, 0.0, 1e-6))


if __name__ == '__main__':
    for n in _notes():
        print('-', n)
