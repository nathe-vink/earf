"""barkhorn's Cloud cabinet (rounds 10 to 21): the cabinet without wood (pressed.py) made in cast acrylic, 20 mm, tinted
through, since round 19 in a full spectrum of eight: Flare's red, Dust's orange, Acid's amber, Poison's green, Ice's
blue, Haze's violet, Fog's frosted white and Smoke's black (grey until round 19); in recycled cast acrylic where a
maker can make the colour. Its lining shows through it (round 13),
so every fitting inside is drawn to be seen.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud

How it differs from the pressed sheet (round 14; the owner, asked whether to draw it next: "Yes"):
- Cemented, not welded. Acrylic bonds well, so the corners and everything inside (the braces, the ribs, the back's
  land strips) are cemented with a two-part polymerising acrylic cement made for thick sheet (ACRIFIX 2R 0190 or
  Weld-On 40; round 35: 1R 0192, named here before, is a one-part cement that cures by light and will not cure through
  the deep tints): it cures clear and about as strong as the sheet. A solvent cement crazes thick cast sheet and leaves
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
# round 35 (the engineering review's S7, the owner: yes): with 10 kg of horn on top a 72 kg speaker 0.42 m deep is marginal
# against IEC 62368-1's push at the top (about 118 N m tipping against 108 restoring forward with the feet 50 in, by the
# review's estimate); the front and back feet 25 in from the edges give about 124 forward and 138 back (estimate), the
# inserts still wholly in the bottom panel (under the front panel's foot and under the back's land)
P['feet']['inset_y'] = 25.0
# round 36 (the owner, 2026-10-22: "I'd rather the prototype be as close to production as possible. The whole point of a
# prototype is to test production"): the horn thermoformed from the cabinet's own tinted cast sheet (product.formed_horn):
# the flare pressure-formed from `sheet` mm over a male aluminium tool, so its face on the tool is the air path; the wall
# thinning toward the mouth by `thin` (shares of the sheet: at the trim, at the mouth's sides, less again in its
# corners); trimmed `trim` from the throat and cemented `cement` thick into a `socket` in the throat piece (turned and
# milled from a block of the same batch: the air path from the driver to the trim, a `neck` thick outside it on a
# `cove`, a `collar` round the socket, its flange the driver's boss on a spigot into the pod); the mouth's lip rolled
# `lip` past the mouth on the tool over its last `lip_run`; the pod rolled from the batch's 6 mm sheet; the posts' pads
# turned pucks, the tie rod's washer on a `saddle` (radius, its top's height) in the pod; the pads' M10 inserts 12 deep
# (the shell's wall too thin to take them). The tool's plug and base drawn `beside` the speaker (x), as option 'tooling'
# (the owner, 2026-10-22, "as deep as the cabinet", then 2026-10-31, "Deep, like the site"): every horn part in the
# horn's own heavier dye lot, about `dye` times the cabinet's dye (product.HORN_DEPTH_M draws it: the site's resin horn's tint)
P['horn']['cast']['formed'] = dict(
    sheet=10.0, trim=40.0, cement=0.2, socket=12.0, collar=4.0, neck=7.0, cove=10.0, lip=6.0, lip_run=8.0,
    thin=dict(throat=0.85, mouth=0.60, corner=0.18), insert_depth=12.0, dye='6 to 10', flange=dict(shoulder=4.0), saddle=(8.0, -78.0),
    run_usd=600.0, throat_usd=400.0, pod_usd=250.0,
    tool=dict(nose=15.0, base=(900.0, 640.0, 40.0), beside=1500.0, plug_usd=14000.0, base_usd=2000.0,
              board_usd=2800.0, board_weeks='3 to 4'))   # the prototype's plug in tooling board (the coordinator's call)
# (the forming trial's plug and Plan B, the laminated horn, are built apart: horn_options.py)
P['horn']['cast']['posts'].update(pad_h=15.0, insert_depth=12.0, front_insert_depth=12.0)
# round 36 (the engineering review's S1, the owner: yes): the back tied to the braces, two M5 screws a brace into
# machined bosses saddled on their rear members, beside the back's ribs (product.back_ties); a 4 mm EPDM cord in a groove
# `groove` (deep, wide) `at` in from the shell in place of the sponge gasket, so the back seats hard on the lands (gasket
# 0); the lands 30 wide for the groove beside the screws, which move out to `screw_at`; 18 round the edge and 4 into the
# bosses, 22 in all
P['back'].update(land=30.0, gasket=0.0, screw_at=10.0, per_side=7, per_end=4,
                 seal=dict(cord=4.0, groove=(3.0, 5.4), at=22.0, corner=12.0),
                 ties=dict(boss=(36.0, 36.0), saddle=12.0, beside=2.5))
# round 24 (the owner, of round 23's options: "Name on back own color", and of lifting: "240 grips + feet range"): EARF
# etched high on the back and filled with the speaker's own colour, and a grip 240 long for both hands in each side near
# the top, as standard (product.extras); castors, spikes and isolation feet sold for the feet's M8 inserts
P.update(mark=['back'], mark_finish='tint', lift=['grips'], grip_w=240.0)
P['remote'] = True                               # round 36: Hypex's remote kit, its remote and the link cable, one a pair
# round 36 (the coordinator's call): the IR receiver behind the front panel's own tint, no window: its eye `x` from the
# centre and `z` up, between the ports, under the cloth disc's edge (z 260) and the first brace (z 200); its board (`pcb`:
# across, high, thick) in a clear `bracket` (across, deep, high); the fallback window `window` across
P['ir'] = dict(x=0.0, z=160.0, pcb=(40.0, 22.0, 1.6), bracket=(56.0, 10.0, 36.0), eye=6.0, window=12.0)
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
        'two-part polymerising acrylic cement for thick sheet (ACRIFIX 2R 0190 or Weld-On 40), clamped square on a jig, no visible bubble in any joint; the box '
        'annealed again; the lands\' faces, the bosses\' and the seal\'s groove milled in one setup; the back closes the box last, '
        'seated hard on the lands and the braces\' bosses over a cord seal, twenty-two screws, and comes off. No solvent cement: '
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
    touching=pressed.PRODUCT.touching + [('lead-ir', 'cable-glands'),       # the IR cable through its gland (round 36)
                                         ('ir-window', 'front-panel')],      # the fallback insert, bonded through the panel
    drawing_prefix='BHC')
