"""barkhorn's Cloud cabinet (rounds 10 to 21): the cabinet without wood (pressed.py) made in cast acrylic, 20 mm, tinted
through, since round 19 in a full spectrum of eight: Flare's red, Dust's orange, Acid's amber, Poison's green, Ice's
blue, Haze's violet, Fog's frosted white and Smoke's black (grey until round 19); in recycled cast acrylic where a
maker can make the colour. Its lining shows through it (round 13),
so every fitting inside is drawn to be seen.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud

How it differs from the pressed sheet (round 14; the owner, asked whether to draw it next: "Yes"):
- Cemented, not welded. Acrylic bonds well, so the corners and everything inside (the braces, the ribs, the back's
  land strips) are cemented with a two-part polymerising acrylic cement made for thick sheet (Acrifix 1R 0192 or
  alike): it cures clear and about as strong as the sheet. A solvent cement crazes thick cast sheet and leaves
  bubbles in a long joint.
- Machined, polished and annealed. Each panel's edges are milled square and polished where they show. The panels are
  annealed before cementing (about 80 C, held an hour for each 3 mm of thickness, cooled slowly), and the box after,
  so that no stress is left where the cement or a screw meets an edge: stressed acrylic crazes.
- Nothing pressed in. Acrylic is brittle, so the brass sockets, the inserts and the magnets are bonded with epoxy in
  clearance holes, not pressed into tight ones, and the port frames' screws go into tapped threads.
- The lining held by dots of clear acrylic foam tape (VHB 4910 or alike), nearly invisible through the wall.
- Acrylic is a quarter denser than HDPE: about 53 kg of sheet a cabinet.
- The ports in the cabinet's own acrylic (round 15, the owner's pick): each a cast acrylic tube, its inner end flared
  over a heated mandrel, cemented into a frame cut from 8 mm sheet that holds the whole rounded front mouth, so no
  joint shows in it.
20 mm, as the pressed sheet (round 15, the owner: "Yes, 20 mm"), but on round 14's ribs (one up each side, two up the
back, one under the top and one over the bottom), not the pressed cabinet's doubled ones: acrylic is about three times
as stiff as HDPE, so a 20 mm acrylic panel is stiffer than the 25 mm HDPE one was, at the same weight a square metre.
The top's rib ends at the pad under the top. The look book's Cloud speakers are rendered from it, the acrylic as the
engine's clear resin.
"""
import copy, dataclasses, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pressed                                                       # noqa: E402

P = copy.deepcopy(pressed.P)
P.update(stock='cast-acrylic', T=20.0, ribs=dict(t=20.0, depth=60.0, back=(150.0, 410.0), min_span=300.0))
P['port'].update(stock='cast-acrylic', frame_t=8.0)    # round 15: the ports in its own acrylic, the frame holding the mouth
P['ring']['stock'] = 'cast-acrylic'              # tinted opaque in the ring colour
P['cover']['disc_stock'] = 'cast-acrylic'        # black, under the cloth
P['woofer_hole'] = 8.5                           # M6 brass inserts bonded with epoxy
P['cover']['disc_magnet']['pocket'] = 15.2       # the magnets and the steel discs bonded
P['horn']['cast']['posts']['socket'] = (15.2, 15.0)   # the sockets bonded in clearance holes, not pressed
P['back']['insert'] = (8.0, 12.0)                # the back's M5 inserts and the feet's M8, bonded
P['feet']['insert'] = (12.5, 15.0)
# round 24 (the owner, of round 23's options: "Name on back own color", and of lifting: "240 grips + feet range"): EARF
# etched high on the back and filled with the speaker's own colour, and a grip 240 long for both hands in each side near
# the top, as standard (product.extras); castors, spikes and isolation feet sold for the feet's M8 inserts
P.update(mark=['back'], mark_finish='tint', lift=['grips'], grip_w=240.0)
PRODUCT = dataclasses.replace(
    pressed.PRODUCT, name='barkhorn-cloud', params=P,
    kind='Two-way horn loudspeaker after Friendly Pressure, the Cloud: tinted cast acrylic, no wood',
    notes=[n.replace('in a brass socket pressed into the top', 'in a brass socket bonded with epoxy into the top')
           for n in pressed.PRODUCT.notes if not n.startswith(('No wood:', 'Assembly (', 'The woofer flush',
                                                               'The front: the panel'))] + [
        'No wood: every panel is cast acrylic, 20 mm, tinted through in its colour (red, orange, amber, green, blue, violet, '
        'frosted, black), recycled (made from recycled MMA) where a maker can make the colour, cut '
        'on a CNC router from 4 x 8 ft sheets of one batch (approve a tint swatch and a cemented corner sample first). The '
        'ring (6 mm) is cast acrylic tinted opaque in the ring colour; the cloth disc\'s frame (12 mm) black cast acrylic.',
        'Assembly: each panel\'s edges milled square and polished where they show, the panels annealed (about 80 C, an hour '
        'for each 3 mm of thickness, cooled slowly); the ribs cemented to their panels flat (the back\'s to the back); the '
        'shell\'s corners, the front panel (set back 24 mm), the two braces and the back\'s four land strips cemented with a '
        'two-part polymerising acrylic cement for thick sheet (Acrifix 1R 0192 or alike), clamped square on a jig; the box '
        'annealed again; the back closes the box last, on its gasket and sixteen screws, and comes off. No solvent cement: '
        'it crazes thick cast sheet.',
        'The woofer flush in its rebate on a gasket, on eight M6 brass inserts bonded with epoxy in 8.5 holes; the ring over '
        'its frame on its magnets, bonded in their pockets; each port in the cabinet\'s own acrylic, its tube cemented into '
        'its 8 mm frame, fitted from the front into a recess on a foam gasket, four black M4 screws in its corners into '
        'tapped threads; the tubes cut to the length found on the first sample before their ends are flared.',
        'The front: the panel\'s own tinted acrylic, the lining showing through it round the woofer, and a cloth disc over '
        'the woofer in the acrylic\'s colour, its frame standing on the ring on four magnet pairs.',
        'Seen through: everything inside is drawn to be seen. The leads run straight and tied, the glands and the brass '
        'sockets show, the amplifier\'s compartment is black anodised, and each batt\'s voile sleeve has its seams to the '
        'wall.',
        'Lifting (round 24): a grip 240 x 42 for both hands through each side, 92 below the top, a cup of 3 mm acrylic '
        'cemented behind it and the side\'s batt cut round it; two people lift a speaker by its grips, the horn off. The '
        'feet\'s M8 inserts take castors, spikes or isolation feet in place of the levelling feet, sold separately.',
        'The mark (round 24): EARF 140 wide, laser-etched high on the back, centred, the etch filled with the speaker\'s '
        'own colour, deeper.'],
    drawing_prefix='BHC')
