"""barkhorn without wood (round 5): the same speaker with a cabinet made wholly of pressed recycled plastic. The panels
are recycled HDPE sheet, 20 mm thick (round 15, the owner's pick; 25 before), each pressed to order. Its colour-sorted flakes are laid out in the bark's
pattern (the eucalyptus's peeling strips, the birch's lenticels), so the sheet itself is the finish. The corners are
welded. The ring and the cloth disc's frame are HDPE too.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/pressed.py --out spinoffs/barkhorn/out-pressed

Why two braces and ribs: HDPE is about a tenth as stiff as birch plywood (E 0.8 to 1.2 GPa against about 9). A 25 mm
panel has about 40 % of the bending stiffness of 18 mm plywood and twice its weight per square metre, so a panel of
the same span rings at about 0.45 of the plywood's frequency. The braces alone are not enough: a side panel's first
resonance is set mostly by its short span, front to back. So ribs 60 deep are welded on edge inside, and a second
brace (z 700, between the woofer and the top) shortens the long spans. HDPE's own damping, several times plywood's,
keeps whatever still rings low.

Why 20 mm (round 15, the owner's pick of round 14's three routes): most of the presses that make sheet to order make
20 mm, and a 25 mm sheet cools with voids in its core and is planed, which cuts into the pattern. A 20 mm panel has
about half the 25's bending stiffness, so the spans are halved again: two ribs 20 x 60 up each side, four up the back (two each side of the amplifier), two under the top and two over the bottom.
As simply supported plates the panels' first resonances then stay at or above the 25 mm cabinet's (about 550 Hz on a
side, against 300 for the plywood one). The cabinet is about 6 kg lighter and its sheet about $400 a pair cheaper,
for about an hour more welding a pair. The top is too thin under the posts' sockets for the tie rod's insert, so a
pad of the same sheet is welded under it between the rear posts.

The whole cabinet is one material, so nothing moves against anything else. HDPE grows 2 to 3.5 mm on 880 mm over
20 degrees, and plywood hardly at all, which is what made round 4's faced sheets need loose screws and gaps. Here the
corners are hot-plate butt welded, the bead planed flush. The front panel, the braces, the ribs and the back's land strips
are extrusion welded inside, so the box is airtight with no glue (HDPE glues badly); the back closes on a gasket and
screws, and comes off (round 14). The woofer, the amplifier and the horn's posts screw into threaded inserts made for
plastics.
For production, rotomoulded recycled PE, double-walled (Technomad's speakers are made that way). The pattern would
then come out speckled rather than laid out.
"""
import copy, dataclasses, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import product as base                                               # noqa: E402

P = copy.deepcopy(base.P)
P.update(finish='pressed', stock='recycled-hdpe', T=20.0,
         braces=[dict(z=200.0, window=(420.0, 300.0)), dict(z=700.0, window=(420.0, 300.0))],
         # round 15: the 20 mm sheet's ribs (round 14's study 'p14-sheet20'): `side` their depths (y), `top` the top's and
         # the bottom's across (x), `back` the back's across (x)
         ribs=dict(t=20.0, depth=60.0, back=(125.0, 185.0, 375.0, 435.0), side=(155.0, 266.0), top=(210.0, 350.0), min_span=300.0))
P['ring']['stock'] = 'recycled-hdpe'
P['cover']['disc_stock'] = 'recycled-hdpe'
# round 13, the reality check's r3: nothing is bonded to HDPE, which no ordinary adhesive or sealant holds. The woofer's
# inserts go in holes sized by the insert maker's chart for PE, and the magnets and steel discs are pressed in
P['woofer_hole'] = 9.0
P['cover']['disc_magnet']['pocket'] = 14.85
P['back']['insert'] = (7.2, 12.0)       # round 14: the back's M5 inserts and the feet's M8, by the same chart
P['feet']['insert'] = (11.5, 15.0)
PRODUCT = dataclasses.replace(
    base.PRODUCT, name='barkhorn-pressed', params=P,
    kind='Two-way horn loudspeaker after Friendly Pressure, in pressed recycled plastic, no wood',
    notes=[n for n in base.PRODUCT.notes if not n.startswith(('Bark on the shell', 'The front: the panel faced in bark', 'Glue-up',
                                                              'The woofer flush'))] + [
        'No wood: every panel is recycled HDPE sheet, 20 mm, pressed to order from colour-sorted flakes laid out in the bark\'s '
        'pattern (approve a 200 mm pressed sample and a full-sheet trial from one batch first). The ring (6 mm) and the cloth '
        'disc\'s frame (12 mm) are HDPE too.',
        'Assembly (rounds 14 and 15): the ribs welded to their panels flat (two up each side, two under the top, two over '
        'the bottom; the back\'s four to the back), the pad under the top between the rear posts; the shell\'s corners '
        'hot-plate welded, the bead planed flush; the front panel (set back 24 mm), the two braces and the back\'s four land '
        'strips extrusion welded inside, through the open back; the back closes the box last, on its gasket and sixteen screws, and '
        'comes off. The flake ordered as HDPE '
        'only, in a narrow melt-flow band: polypropylene caps in the mix will not weld. Nothing is glued: HDPE holds no ordinary '
        'adhesive.',
        'The woofer flush in its rebate on a gasket, on eight M6 threaded inserts for plastics in 9 mm holes (the torque checked '
        'again after 48 hours: HDPE creeps); the ring over its frame on its magnets; each port, printed in one with its square '
        'frame, fitted from the front into a recess on a foam gasket, four black thread-forming screws for plastics in its '
        'corners; its length found on the first sample (its rounded ends cannot be trimmed).',
        'The front: the panel\'s own sheet in the pattern, and a cloth disc over the woofer on its HDPE frame, standing on the '
        'ring on four magnet pairs.'],
    drawing_prefix='BHP')
