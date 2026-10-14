"""barkhorn without wood (round 5): the same speaker with a cabinet made wholly of pressed recycled plastic. The panels
are recycled HDPE sheet, 25 mm thick, each pressed to order. Its colour-sorted flakes are laid out in the bark's
pattern (the eucalyptus's peeling strips, the birch's lenticels), so the sheet itself is the finish. The corners are
welded. The ring and the cloth disc's frame are HDPE too.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/pressed.py --out spinoffs/barkhorn/out-pressed

Why 25 mm, two braces and ribs: HDPE is about a tenth as stiff as birch plywood (E 0.8 to 1.2 GPa against about 9). A
25 mm panel has about 40 % of the bending stiffness of 18 mm plywood and twice its weight per square metre, so a
panel of the same span rings at about 0.45 of the plywood's frequency. The braces alone are not enough: a side panel's
first resonance is set mostly by its short span, front to back. So ribs 25 x 60 are welded on edge inside: one up each
side at mid-depth and a pair up the back, between the braces (below and above them the spans are short and already
stiff, and the ports run through the bottom bay), one under the top and one over the bottom. A second brace (z 700,
between the woofer and the top) shortens the long spans. As simply supported plates, the panels' first resonances are then at or
above the plywood cabinet's (a side: about 550 Hz against 300). HDPE's own damping, several times plywood's, keeps
whatever still rings low.

The whole cabinet is one material, so nothing moves against anything else. HDPE grows 2 to 3.5 mm on 880 mm over
20 degrees, and plywood hardly at all, which is what made round 4's faced sheets need loose screws and gaps. Here the
corners are hot-plate butt welded, the bead planed flush. The front panel, the back, the braces and the ribs are
extrusion welded inside, so the box is airtight with no screws and no glue (HDPE glues badly). The woofer, the amplifier and
the horn's posts screw into threaded inserts made for plastics.
For production, rotomoulded recycled PE, double-walled (Technomad's speakers are made that way). The pattern would
then come out speckled rather than laid out.
"""
import copy, dataclasses, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import product as base                                               # noqa: E402

P = copy.deepcopy(base.P)
P.update(finish='pressed', stock='recycled-hdpe', T=25.0,
         braces=[dict(z=200.0, window=(420.0, 300.0)), dict(z=700.0, window=(420.0, 300.0))],
         ribs=dict(t=25.0, depth=60.0, back=(150.0, 410.0), min_span=300.0))
P['ring']['stock'] = 'recycled-hdpe'
P['cover']['disc_stock'] = 'recycled-hdpe'
# round 13, the reality check's r3: nothing is bonded to HDPE, which no ordinary adhesive or sealant holds. The woofer's
# inserts go in holes sized by the insert maker's chart for PE, and the magnets and steel discs are pressed in
P['woofer_hole'] = 9.0
P['cover']['disc_magnet']['pocket'] = 14.85
PRODUCT = dataclasses.replace(
    base.PRODUCT, name='barkhorn-pressed', params=P,
    kind='Two-way horn loudspeaker after Friendly Pressure, in pressed recycled plastic, no wood',
    notes=[n for n in base.PRODUCT.notes if not n.startswith(('Bark on the shell', 'The front: the panel faced in bark', 'Glue-up',
                                                              'The woofer flush'))] + [
        'No wood: every panel is recycled HDPE sheet, 25 mm, pressed to order from colour-sorted flakes laid out in the bark\'s '
        'pattern (approve a 200 mm pressed sample and a full-sheet trial from one batch first). The ring (6 mm) and the cloth '
        'disc\'s frame (12 mm) are HDPE too.',
        'Assembly (round 13): the ribs welded to their panels flat; the shell\'s corners hot-plate welded, the bead planed flush; '
        'the front panel (set back 24 mm) and the two braces extrusion welded inside, through the open back; the back closes the '
        'box last, from outside (on a gasket and screws, or welded in an outside V: the owner\'s choice). The flake ordered as HDPE '
        'only, in a narrow melt-flow band: polypropylene caps in the mix will not weld. Nothing is glued: HDPE holds no ordinary '
        'adhesive.',
        'The woofer flush in its rebate on a gasket, on eight M6 threaded inserts for plastics in 9 mm holes (the torque checked '
        'again after 48 hours: HDPE creeps); the ring over its frame on its magnets; each port fitted from inside, trimmed to tune '
        '(impedance minimum at fb), its flange screwed to the panel with thread-forming screws for plastics on a foam seal.',
        'The front: the panel\'s own sheet in the pattern, and a cloth disc over the woofer on its HDPE frame, standing on the '
        'ring on four magnet pairs.'],
    drawing_prefix='BHP')
