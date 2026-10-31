"""Tropos's horn, two things beside the speaker (2026-10-31), built apart from the Cloud so its build stays within memory:

- the forming trial's plug and base (make/forming-trial.md): the full plug cut to one quadrant at full scale;
- Plan B (make/plan-b.md, make/laminated-horn.md): the horn laminated from 22 layers of stock 1/2 in tinted sheet, in
  the formed horn's place: stepped (a terrace a layer), and the same stack machined smooth outside.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/horn_options.py --out spinoffs/barkhorn/out-horn-options

Its origin is the Cloud's, so a shot can lay the laminated horn exactly where the formed one stands (two products, the
Cloud with its horn hidden). The trial's plug stands to the side, as the Cloud's own tools do.
"""
import copy, dataclasses, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloud                                                         # noqa: E402
import product                                                       # noqa: E402

P = copy.deepcopy(cloud.P)
# the trial: the plug cut to one quadrant, `past` the axis, its cut faces drafted `draft` degrees, on a `base` of board.
# Plan B: the horn laminated from `layer` mm sheet, each layer `wall` outside the air path at its front. Since the stock-
# colour research (2026-10-31, R1: tinted stock cast sheet stops at 1/2 in), from stock 1/2 in sheet, so the first horn
# needs no custom pour; `smooth` adds the same stack with its outside machined to the flare. setup_usd: the layers'
# cutting and facing, the bonding jig and bonding, the 5-axis air path and its polish; smooth_usd: the outside's 5-axis
# finishing and polish
P['horn']['cast']['formed'].update(trial=dict(past=30.0, draft=15.0, base=(420.0, 300.0, 40.0), plug_usd=1100.0),
                                   laminated=dict(layer=12.7, wall=10.0, stock=True, smooth=True, setup_usd=1650.0,
                                                  smooth_usd=450.0))
KEEP = ('horn-trial-plug', 'horn-trial-base', 'horn-plan-b', 'horn-plan-b-smooth')


def parts(P):
    wg = product.waveguide(P)
    out = [dataclasses.replace(p, option='') for p in product.formed_later(P, wg) if p.name in KEEP]
    for p in out:
        if p.name.startswith('horn-plan-b'):
            p.render = True
    return out


PRODUCT = dataclasses.replace(
    cloud.PRODUCT, name='barkhorn-horn-options', params=P, parts=parts, count=2,
    touching=[('horn-plan-b', 'horn-plan-b-smooth')],                    # two alternatives in the same place
    kind='Tropos horn: the forming trial\'s plug, and Plan B, the laminated horn',
    notes=['The forming trial (make/forming-trial.md): the production plug\'s surface cut to one quadrant at full scale, the '
           'throat end and the mouth\'s lower corner, its cut faces drafted outward; in high-temperature epoxy tooling board, on a '
           'board base; formed in stock 10 mm cast sheet and gauged before the full plug is cut. One set (the parts list counts '
           'it once).',
           'Plan B (make/plan-b.md, make/laminated-horn.md): the flare and the neck laminated from 22 layers of stock 1/2 in tinted '
           'cell-cast sheet, each layer CNC-cut to its outline, bonded with polymerising cement in a jig, annealed, the air path '
           'machined through on 5 axes and polished; the outside stepped (horn-plan-b) or machined smooth (horn-plan-b-smooth). '
           'Each stands in the formed horn\'s place on the same pod, cap, pads and posts; the parts list counts both, one is chosen.'],
    origin=(280.0, 213.7, -12.0), drawing_prefix='BHH')
