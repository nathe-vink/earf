"""barkhorn in pressed recycled plastic (round 4): the same speaker, its plywood shell faced in pressed recycled HDPE
sheet instead of bark, the eucalyptus's colours laid as vertical strips, the birch's as short black dashes on milk.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/pressed.py --out spinoffs/barkhorn/out-pressed

The plywood box stays the structure (HDPE is about a tenth as stiff as birch plywood: a panel as stiff as 18 mm
plywood would be about 40 mm thick, three times the weight). Each sheet is 8 mm, laid on the box and screwed from
inside through oversized holes, never glued: HDPE glues badly and grows 2 to 3.5 mm on 880 over 20 degrees, so each
sheet must be free to move, with a gap at every corner. A sheet-press workspace presses the sheets to order, 1 m
square, from flakes sorted by colour and laid out by hand (the pattern's specification is in the README).
"""
import copy, dataclasses, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import product as base                                               # noqa: E402

P = copy.deepcopy(base.P)
P['finish'] = 'pressed'
PRODUCT = dataclasses.replace(
    base.PRODUCT, name='barkhorn-pressed', params=P,
    kind='Two-way horn loudspeaker after Friendly Pressure, in pressed recycled plastic',
    notes=[n for n in base.PRODUCT.notes if not n.startswith(('Bark on the shell', 'The front: the panel faced in bark'))] + [
        'The front: the panel faced in 5 mm of the pressed sheet round the ring and the port, and a cloth disc over the '
        'woofer, its MDF frame standing on the ring on four magnet pairs.',
        'Pressed recycled plastic on the shell (sides, top, back and front edges): 8 mm HDPE sheet pressed to order from '
        'colour-sorted flakes, each sheet screwed from inside through 8 mm holes in the plywood, never glued (HDPE glues '
        'badly and moves with the seasons); 1.5 mm gaps at the corners; the panel faced in 5 mm of the same sheet. '
        'Approve a pressed sample (200 mm) and a full-sheet trial from one batch first.'],
    drawing_prefix='BHP')
