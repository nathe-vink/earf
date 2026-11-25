"""Round 32d, the bar lamps the owner picked from the shape study (2026-10-19: "I like the dome overhead lights,
especially if the acrylic covers are easy to swap out, but I'm also a sucker for the spheres. For the table lamp
though, I'd want the spheres to be squatted rather than raised, like a crystal ball."). Two products, the frost set
within the acrylic as in round 32c (study.py): tint, frost, tint; nothing white outside.

Dome, the pendant. A tinted dome 200 across is a cover that comes off by hand. A black anodised collar is bonded into its crown,
and three L-slots in the collar take three pins on the fixture's black anodised hub: a quarter-turn bayonet (30 degrees here).
Lifted 8.0 to 9.0 mm from where it hangs (measured on the CAD, 2026-11-24; was written as 5), turned and lowered, the cover hangs with each pin up in a notch at the end of its slot, so its own weight
locks it. It can't turn out unless it is first pushed up, and a spring plunger in the hub clicks into a dimple in the
collar as a detent. The COB (2700 K, recessed 22 up a 46 bore: a cut-off about 46 deg from the vertical), the hub, the
cord and the driver in the canopy stay on the fixture, so a cover is never a live part and the listing (UL 1598) covers
the fixture with any cover. The covers are sold on their own in every tint.

Orb, the table lamp. A tinted ball 160 across, a crystal ball, sits low in the cup of a short base: a black polished
acrylic drum 120 across with a black anodised ring at its top that is the touch (tap to switch, hold to dim, 2200 to
2700 K). The board and the LED stay sealed in the base (IP44), and the LED shines up through a sealed window into a
port in the ball's underside. So the ball is a cover too: it lifts off, and Orbs swap colour as the Domes do. It rests
on a silicone ring in the cup, 18 deep, which is enough to stop a nudge rolling it. It plugs in over USB-C; a battery
cartridge (an option) makes it cordless.

Round 32f (2026-10-20, the owner): the hardware black on both ("Why do the domes have brass tops? Why not black
acrylic?"; "The orb base can be updated too"), and the Orb plug-in, optionally cordless ("Maybe the orbs are plug in and
optionally rechargeable or something").

Round 41 (the owner signed round 40, 2026-10-29): round 32f's low profiles are the design. Hemisphere's heat sink is
the low top (a black crown and an aluminium cap, 126 above the rim; no fins, for 575 lm), and Core sits on the 120 x 30
base with three LiFePO4 18650 cells round the LED. The fins and the 26650 holder of rounds 35 to 39 are in git at
950a7eaf.

Round 38 (the owner, 2026-10-25: "Get rid of south altogether and just call it hemisphere."): Hemisphere South is dropped from the line and Hemisphere North is now just
Hemisphere. South's parts stay here (south_parts, hemisphere_south.py) as a record; nothing in the line uses them.

Round 35 (2026-10-22, the owner's names and an engineering review): the Dome is Hemisphere North, the same shades
turned opening-up on a rod are Hemisphere South, and the Orb is Core. North's driver is chosen from the COB's forward
voltage, its heat goes to fins above the shade through a PEEK break, its shade is clamped, its diffuser opal, its cord
listed; South is new; Core holds its own LiFePO4 cells behind a screwed hatch and the cartridge is gone. Every shade
and ball is formed from cast sheet over an aluminium mould, the production process, and the prototypes are formed on
the same moulds. The README's round 35 has the numbers.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant.py --out spinoffs/barkhorn/companions/out-dome-pendant
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/hemisphere_south.py --out spinoffs/barkhorn/companions/out-hemisphere-south
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/orb_table.py --out spinoffs/barkhorn/companions/out-orb-table

The frame: x across, y back, z up from the dome's rim (the pendant) or from the table (the Orb), mm.
"""
import copy, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
sys.path.insert(0, HERE)
from kit import *                                                   # noqa: E402,F403
import bar_lamps as B                                               # noqa: E402

# the tint carries the glow (study.py): cast denser than the Clouds' 25 mm, as these walls are 9 to 15 mm; smoked
# lighter, or it goes black
MATERIALS = dict(B.MATERIALS,
                 body={'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.005, 'roughness': 0.04},
                 # mostly rough transmission (clear 0.85): bead-blasted acrylic 2.5 thick passes most light diffusely; at
                 # the preset's 0.1 it rendered as opal and turned the unlit Smoke ball solid black (round 32e)
                 liner={'preset': 'frosted', 'color': '#F4F2EE', 'absorb': '#EFE6D8', 'roughness': 0.5, 'radius': 0.02,
                        'clear': 0.85, 'glow': 0.25, 'glow_color': '#FF9A50'},
                 led={'preset': 'emit', 'color': '#FFC890', 'strength': 0.0},
                 window={'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#F4F2EE', 'radius': 0.05, 'roughness': 0.2},
                 silicone={'preset': 'rubber', 'color': '#1A1A1A'},
                 gold={'preset': 'metal', 'color': '#D8B45A', 'roughness': 0.2},
                 # round 32f (the owner: "Why do the domes have brass tops? Why not black acrylic?"): the hardware
                 # black, so the tint is the only colour. The working metal black anodised aluminium, satin; the trim
                 # black cast acrylic, polished, as the cord
                 anodised={'preset': 'metal', 'color': '#2A2A2D', 'roughness': 0.36, 'anisotropic': 0.3},
                 # v7 (the v6 check's (13)): the cables bare stainless and the painted white in the CAD's own render export
                 stainless={'preset': 'metal', 'color': '#8E9093', 'roughness': 0.32},
                 white={'preset': 'satin_paint', 'color': '#EEEEEA'},
                 trim={'preset': 'gloss_plastic', 'color': '#0C0C0D', 'roughness': 0.04, 'coat': 1.0,
                       'coat_roughness': 0.02},
                 fabric={'preset': 'rubber', 'color': '#141414', 'roughness': 0.8, 'sheen': 0.4},
                 # round 35: Hemisphere South's dust lid, clear acrylic bead-blasted both faces
                 lid={'preset': 'frosted', 'color': '#F6F4F0', 'absorb': '#F2EEE8', 'roughness': 0.45, 'radius': 0.05,
                      'clear': 0.9, 'glow': 0.0, 'glow_color': '#FFE2C0'})
VARIANTS = copy.deepcopy(B.VARIANTS)
VARIANTS['smoked'].setdefault('materials', {})['body'] = {'radius': 0.0055}     # 0.008 read cream, not smoke (critic p2)
VARIANTS['smoke'].setdefault('materials', {})['body'] = {'radius': 0.012}       # Smoke at 0.005 read black (round 32e)
# round 32f, the casting spec (the owner: "The orb lamps appear to have two reds and an orange instead of red orange
# yellow"): each tint's cast colour (its absorption at the 5 mm radius) set so the lit lamp's glowing body sits on its
# speaker's hue (marks.SPEAKERS), measured in LCh on the site's rows (crystal_promo.py, the glow about 3200 K at a 4300 K
# balance) and moved until within 10 degrees on both the Orbs and the Domes (Fog and Smoke, near-neutral as their swatches,
# by staying neutral: a hue angle at chroma 2 to 12 is not stable); README, round 32f, has the angles. The
# Clouds' casts (common.COLOURS) went red when lit: the tint's depth over 9 to 12 mm pulls a warm hue toward red
CAST = {'ember': '#CD8553', 'dust': '#DDBA7B', 'acid': '#E2D481', 'poison': '#A4C87C', 'ice': '#5AC0E7', 'haze': '#A080D7',
        'fog': '#F7F8F7', 'smoke': '#787E87'}
for _k, _c in CAST.items():
    VARIANTS[_k]['deep'] = _c

# round 35: the shades formed from cast sheet (the production process, and the prototypes'), the diffuser an opal
# acrylic, the hub's thermal break in PEEK. Budget rates (USD a cm3 of the part, the sheet's offcut and the forming in
# it; a mould is the line's setup): my estimates, not quotes
# v9: the canopy's sheet steel (the mounting plate, the gripper brackets, the driver's enclosure and its cover): laser cut and
# formed by a sheet-metal shop, zinc-plated; my estimate
SOLIDS.setdefault('steel-sheet-formed', dict(title='Steel sheet, laser cut and formed, zinc-plated (a sheet-metal shop)', density=7.85,
                                             usd_per_cm3=0.25))
SOLIDS.setdefault('acrylic-formed', dict(title='Cast acrylic sheet, tinted through, drape-formed over an aluminium mould',
                                         density=1.19, usd_per_cm3=0.06))
SOLIDS.setdefault('acrylic-clear-formed', dict(title='Cast acrylic sheet, clear (TruCast 0000), drape-formed over an '
                                               'aluminium mould', density=1.19, usd_per_cm3=0.05))
SOLIDS.setdefault('acrylic-opal-formed', dict(title='Perspex GS 041 3 mm opal, or equal (T 54%, R 39%, ASTM D1003): cast acrylic sheet, volume-diffusing, formed over an aluminium '
                                              'mould', density=1.19, usd_per_cm3=0.06))
# Core B (2026-11-09): the outer ball in the speaker's TruCast code, the chart figure held at its 6 mm wall; the core
# in Hemisphere's white opal, formed on its own mould (the 3 mm sphere's sheet about 1.8 x its area, and the forming:
# about $25 to $40 a ball [E], the rate set for about $30)
SOLIDS.setdefault('acrylic-trucast-formed', dict(title='Cast acrylic sheet 6 mm, tinted through in the speaker\'s TruCast '
                                                 'code, drape-formed over an aluminium mould, polished both faces; CUSTOM POURS (2026-11-11): Dust, '
                                                 'Acid, Ice at 3x the chart loading; Smoke 0.6x the chart loading (2x the speakers\' own pour; 2026-11-16, matched to Hemisphere off); '
                                                 'Poison 0.6x the chart loading (the mix, the owner 2026-11-17, matched to Hemisphere off)',
                                                 density=1.19, usd_per_cm3=0.06))
SOLIDS.setdefault('acrylic-opal-core', dict(title='Cast acrylic sheet 3 mm, white opal (Hemisphere\'s diffuser\'s), formed '
                                            'over an aluminium core mould', density=1.19, usd_per_cm3=0.18))
# Core's base B in its own colour (2026-11-21, the coordinator: the parts list said the ball's "polished both faces"
# for the base's skin too): the skin satin outside, and the liner bonded to it, in optical contact
SOLIDS.setdefault('acrylic-trucast-formed-satin', dict(
    title=SOLIDS['acrylic-trucast-formed']['title'].replace(
        'polished both faces', 'the outside fine glass-bead blasted (satin) and sealed with a matte anti-fingerprint hardcoat, '
        'the inside as formed, edges polished'),
    density=1.19, usd_per_cm3=0.06))
SOLIDS.setdefault('acrylic-opal-core-bonded', dict(
    title='OPAQUE white (2026-11-21: an opal sheet would let the black body show through and darken the base): a white '
          'coating on the skin\'s inside, or an opaque white cast acrylic liner bonded to the skin\'s inside with a clear '
          'polymerising acrylic cement (Acrifix 192 kind), no air between them; formed over an aluminium core mould',
    density=1.19, usd_per_cm3=0.18))
SOLIDS.setdefault('acrylic-tint-3-formed', dict(title='Cast acrylic sheet 1/8 in, TruCast stock tint in the line\'s code, '
                                                'drape-formed; CUSTOM POURS (2026-11-11): Dust the same dye at 3x the stock loading; the mix (the owner '
                                                '2026-11-17, matched to Core off): Acid 5x, Ice 6x, Ember 1.8x, Haze 1.8x the stock loading; '
                                                'Smoke 1.2x the stock loading (2026-11-16, matched to Core off; was 0.3x)', density=1.19, usd_per_cm3=0.05))
SOLIDS.setdefault('cast-acrylic-satin', dict(title='Black cast acrylic rod, turned, bead-blasted SATIN close to matte '
                                             '(2026-11-11; OPTION: 6061 turned, satin black anodized)', density=1.19,
                                             usd_per_cm3=0.06))
SOLIDS.setdefault('peek', dict(title='PEEK rod, unfilled', density=1.30, usd_per_cm3=0.35))
SOLIDS.setdefault('ptfe', dict(title='PTFE rod, white (virgin)', density=2.17, usd_per_cm3=0.12))

GAP, LT, SKIN = 1.0, 2.5, 3.0          # the liner 1 mm in from the shell, 2.5 thick; the inner skin 3

O = dict(R=80.0, shell=9.0, base=(120.0, 30.0), ring=8.0, rim_r=50.0, port=40.0)    # round 41: 30 again (48 in rounds 35 to 39)
# Core B, the owner's choice (2026-11-09; launch/core-frost-options.md, round 9): a 6 mm outer ball polished both faces
# round a 3 mm white opal core. 2026-11-10 (the owner: "the outer core should be the same depth around the whole inner
# core"): the core Ø140 (R 70 / 67), CONCENTRIC with the outer ball (the drop 0), a 4 mm gap all round, so a 10 mm band
# of colour (6 mm wall + 4 mm gap); fallback Ø130, a 15 mm band. The grommet raised to suit. O_A is design A (the 9 mm
# ball frosted inside), the record: orb_parts(O_A) builds it
O_A = dict(O, design='A')
O = dict(O, design='B', shell=6.0, core=(70.0, 3.0, 0.0), grommet_wall=9.0, flange=52.0,   # core: R outside, wall, drop below
         angled=True, well=True, own_skin=True)   # own_skin: the owner, 2026-11-11, "Own color for sure"; the owner, 2026-11-10: "I like the angled base for core"; the light well white

ORB_LIGHT = None                       # set below from the ball's centre


def ball(R, t, c, cut_below=None):
    """A spherical shell R outside, t thick, centred at c, cut flat below z = cut_below."""
    from build123d import Sphere, Pos
    s = Pos(*c) * (Sphere(R) - Sphere(R - t))
    if cut_below is not None:
        s = s - box(-R - 1, -R - 1, c[2] - R - 1, R + 1, R + 1, cut_below)
    return s


def at(deg, solid):
    from build123d import Rot
    return Rot(0, 0, deg) * solid


def sector(r0, r1, a0, a1, z0, z1, n=12):
    """An annular sector, radii r0..r1, from a0 to a1 degrees, z0..z1."""
    pts = [(r1 * math.cos(math.radians(a0 + (a1 - a0) * i / n)), r1 * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
           for i in range(n + 1)]
    pts += [(r0 * math.cos(math.radians(a1 - (a1 - a0) * i / n)), r0 * math.sin(math.radians(a1 - (a1 - a0) * i / n)))
            for i in range(n + 1)]
    return prism(pts, 'z', z0, z1)


# --- Hemisphere, the pendant, both ways up (round 35) ---------------------------------------------------------------
# Round 35 (the owner, 2026-10-22): the Dome is Hemisphere North (opening down, on its cord) and the same shade turned
# opening-up is Hemisphere South (a bowl on a slim rod, the light at its bottom shining up, a frosted lid against
# dust). One set of shades: both fixtures take the same quarter-turn catch. The engineering review's findings are fixed
# here: B1 the driver chosen from the COB's forward voltage; B2 the heat taken out of the shade into fins in room air,
# with a thermal break between the hub and the cover; L1 the cover clamped between flanges, not hung on a bond; L2 the
# diffuser a volume-diffusing (opal) acrylic, which still diffuses wherever it touches; L4 a listed cord. The shades are
# formed from cast sheet over aluminium moulds (the production process; the prototypes are formed on the same moulds),
# not turned from block.
#
# The cover's frame: z up from the rim, the crown up (North as it hangs). South turns the cover over.
N = dict(R=100.0, shell=9.0, liner=3.0, skin=3.0, gap=1.0,
         collar=(96.0, 82.0, 64.0, 100.0),      # OD, ID, z bottom, z top (North's entry end; round 36: 100, was 104,
                                                 # so it stands 3 proud of the clamp ring: South shows it underneath)
         flange_r=58.0,                          # the collar's flange under the crown and the clamp ring over it, radius
         pin_z=93.0, turn=30.0, notch=(82.5, 95.5),     # North's pins (from the outer end) and their notch
         south_pins=(69.0, 60.0),                # round 36: South's pins enter from the inner end: their height, the
                                                 # slots' angle off North's
         ring=(62.0, 81.6, 86.0, 100.0),        # the PEEK pin carrier: ID, OD, z0, z1. Review 2026-11-01: its OD is the
                                                 # centering land, 0.2 under the collar's 82 bore (was 78: 2 mm of play)
         pin=(4.0, 45.0, 3.0, 25.0),            # review 2026-11-01: the shouldered pin's shoulder Ø, its tip radius (4.0
                                                 # into the 41 bore), its M3 thread, the thread's inner end (6 into the hub)
         core=(62.0, 60.0, 100.0),               # the hub core: OD, z0, z1 (the bore and the reflector in it)
         bore=(46.0, 82.0),                      # the bore's diameter and the COB's face (22 up from the mouth at 60)
         neck=(40.0, 104.0),                     # the core's neck, up into the crown
         crown=(80.0, 100.5, 112.0),             # round 41: the low top, the heat sink: OD, z0, z1 (the fins of rounds
                                                 # 35 to 39 were 80 across from 110 to 146, 16 x 1.8: in git at 950a7eaf)
         cap=(40.0, 14.0), drop=600.0, canopy=(150.0, 50.0))
# PROPOSAL, redrawn (2026-11-24, after the critics' check of the first draw, which locked the shade on: its crown sat over
# the collar's wall, so the shade could not rise the 7.5 to 8.5 the bayonet needs). The visible stack from the clamp ring's
# foot (92) to the gland's top (126), 34 tall, in even tiers with even steps in diameter. Today's: the clamp Ø104 x 5, the
# collar's lip Ø96 x 3, the crown Ø80 x 11.5, the gland Ø40 x 14 (steps 12 at the band, then 8, 16, 40).
# The rules the redraw keeps: (1) every fixture part from the collar's top to 9.5 above it (the lift, 8.5, and 1) stays
# inside the collar's Ø82 bore, so the crown's first tier is Ø80 (as today); (2) the clamp ring is Ø104 (the M96 thread);
# so the steps are 24; (3) the band on the shade (Ø116, as today) TAPERED, 5 thick at the clamp ring to a 1.0 land at its
# rim, so it reads as the foot of the stack, not a step (the coordinator, 05:49: taper, don't widen; its face on the
# acrylic and the silicone are today's, and it bends 0.24 um under 0.5 MPa against today's 0.11);
# (4) the collar rises flush with the clamp ring's top (0.5 proud, for the squeeze), its slots' entries with it, so there
# is no recess and the clamp ring is plain M96 its full height, nothing for it to bottom on but the gasket;
# (5) the white under the hub split so the shade comes off (WHITE_SPLIT); (6) a cord grip modeled under the gland (GRIP).
# A: three tiers, 11.33 each: the clamp ring Ø104, the crown Ø80, the gland Ø56.
# B: four tiers, 8.5 each: the clamp ring Ø104, the crown in two, Ø80 and Ø56, the gland Ø32.
# Each entry (diameter, z0, z1) in the cover's frame; 'top' the collar's top, the clamp ring's 0.5 under it.
# v8 (the coordinator, 21:32 UTC): A's positive lock (Ganter GN 617, GRIP['lock']) is an option until the owner answers
# (his pictures: tests/r2/lock-sheet.jpg). LOCK_ON = False drops it cleanly: A then has the M5 detent like today's top and
# B, its cables at 0/180 and the cap's key and magnet at 90/270; nothing else is redrawn. The env HEMI_LOCK_ON overrides.
import os as _os
LOCK_ON = _os.environ.get('HEMI_LOCK_ON', '1') == '1'
MIRROR = True        # V11-12: the bayonet's slots mirrored (the entries at 60/180/300); TURN_SIGN the collar's turn from its seat to its entries
TURN_SIGN = -1.0 if MIRROR else 1.0
TOP_TIERS = {
    'today': dict(top=None, crown=[(80.0, 100.5, 112.0)], gland=(40.0, 112.0, 126.0)),   # today's top, with check 3's fixings
    'A': dict(top=103.33, clamp=104.0, band_r=58.0, taper=1.0, crown=[(80.0, 100.5, 114.67)], gland=(56.0, 114.67, 126.0),
              # v7: with the lock, A's cables turned to the lock's line (105/285 deg), so its off-axis mass lies along them,
              # where the levelling takes it up; the cap's key and magnet turned clear of them. v8: all of it under LOCK_ON
              **(dict(lock=True, cables=(105.0, 285.0), key=(15.5, 15.0, 2.0), magnet=(15.5, 195.0, 2.0)) if LOCK_ON else {})),
    'B': dict(top=100.5, clamp=104.0, band_r=58.0, taper=1.0, crown=[(80.0, 100.5, 109.0), (56.0, 109.0, 117.5)], gland=(32.0, 117.5, 126.0),
              cable_r=17.6, key=None, magnet=(14.0, 270.0, 1.5)),     # v7: B's cables at r 17.6 (1.2 of the Ø40 neck round each hole, 0.8 clear of the cap)
}
# The top's fixings (check 3, 2026-11-24; for today's top, A and B alike). The cord grip: Lapp 53112005 as its datasheet
# gives it (DB53112005EN, as the reviewer read it; the sheet not opened here): M12 x 1.5, 16 across the flats, 17.6 across
# the corners, 32.5 overall, 12 of thread, cord 3.5 to 7. Its body is drawn as the hex (5) and a round dome to the overall
# height, its outline to confirm on the sheet. The hub is tapped M12 13 deep from the neck's top (101.5), so 9.5 of its
# thread are in the hub and the cord's pull goes into the hub. The crown sits on the neck metal to metal (no pad, which
# would creep under the screws and the grip; a film of thermal compound), its 2.5 floor held down by three M2.5 countersunk
# screws at r 9.25, 90/210/330 deg, into the neck, their heads inside the pocket.
# v6/v7 (2026-11-24, the v5 and v6 checks): THE HANGING. Two cables, symmetric about the axis (0 and 180 deg), at r 16 in
# today's top and A and r 17.6 in B (beside its Ø32 cap, 0.8 clear; 1.2 of the Ø40 neck round each hole): 1/16 in (1.59)
# 7x7 stainless cable (Cable Grippers Inc.'s bulk cable). The hub end: a Nicopress 871-1-C copper stop sleeve swaged on
# (tool 51-C-887; Nicopress gives a stop sleeve about 50 % of the cable's rated break, typical: about 1.07 kN on 1/16 7x7;
# its size about Ø5.2 x 5.6 before swaging, which lengthens it), bearing up under a Ø5.6 x 8 counterbore in the hub's bottom
# face, the cable up a Ø2.4 hole through the hub, the crown and the cap (today, A) or beside the cap (B); the white disc
# closes the counterbores. No turning, no thread. The canopy end: a Cable Grippers MGR-M10-MM gripper on each cable (their
# chart: 17.1 long without the plunger, Ø11.9 body, M10 thread; MGR on 1/16 in stainless 7x7: 312 lb minimum break in
# their independent tests, 50 lb a cable at their 5:1), plunger down, with its knurled safety nut, threaded up through a
# steel U bracket riveted under the canopy's mounting plate (an M10 nylon-insert nut on top). The cables splay from their
# exits to the grippers at r 48 (clear of the driver's enclosure). Each cable assembly is proof-loaded to 90 N (5 x the
# lamp's 1.7 kg) for 1 min before it is fitted.
# LEVELLING (v7): the plate screwed to the box and the canopy hanging on the cables below it, the lamp hung; loosen each
# gripper's safety nut, push its plunger and slide the cable until a 200 mm level across the rim reads level to 1 deg
# (the rim's two sides within 3.5 mm of each other below the ceiling); 1 mm of cable tilts it about 1.3 deg; tighten the
# safety nuts; feed the cord until it bows (2 mm longer than the cables) and tighten the canopy's cord grip; slide the
# canopy up the cables and fix its two set screws. The tails (about 50) coiled in the brackets.
# The cord (v6): set 2 mm longer than the cables between its grips, so it carries no load (the cables stretch about
# 0.05 mm under the lamp); hung, it bows about 21 mm to one side over the drop: drawn so.
# The cap (v6): today's and A's caps keyed to the crown by a Ø2 dowel and held down by a Ø2 x 2 magnet over a steel disc,
# both at r 15.5 (2.5 from the crown's Ø24 pocket); the cap is the handle in a swap. B's Ø32 cap is held by a Ø1.5 x 2
# magnet only (r 14): B's handle in a swap is its Ø56 tier.
# The grip is turned by a slotted (pass-through) 16 socket, the cord in its slot: the dome nut off, the body torqued into
# the hub, the dome nut on and tightened on the cord. The order: the cables up through the hub from below, their sleeves
# into the counterbores; the white disc; the crown down over the cables onto the neck, its three screws; the grip, as above;
# the cap down over the cord (and the cables) onto its dowel; the cables through the canopy's floor and the grippers, and
# the levelling above. In a swap, hold the cap (B: the Ø56 tier); on A, pull the lock's knob first (GRIP['lock']).
GRIP = dict(thread=(12.0, 12.0), tap=13.0, hex=(16.0, 17.6, 5.0), overall=32.5, pocket=24.0, cap_pocket=20.0, lid=1.0,
            floor=(101.5, 104.0), screws_r=9.25, screws_a=(90.0, 210.0, 330.0), cable_r=16.0, cables=(0.0, 180.0),
            cable=1.59, sleeve=(5.16, 5.56), cbore=(5.6, 8.0), gripper_r=48.0,     # v7/v8: the counterbore 8 deep (the swaged sleeve lengthens); the grippers at r 48 (their brackets clear the enclosure)
            key=(15.5, 90.0, 2.0), magnet=(15.5, 270.0, 2.0),
            # v7 (the coordinator's decision, 17:39 UTC, the v6 check's (1), (2)): the tether gone; on top A a positive lock,
            # Ganter GN 617-5-M10X1-AK (JW Winco's table: a Ø5 H7 pin, M10 x 1, a Ø21 knob, about 45 overall, 5 stroke,
            # spring 7 N initial and 17 N at the end; lock nut ISO 8675), threaded radially into the collar's wall at 105 deg,
            # z 96.5 (96.0 seated), through A's clamp ring, its pin into a Ø6.4 hole in the PEEK ring
            lock=dict(angle=105.0, z=96.5, pin=5.0, stroke=5.0, tip_in=36.3))
# The white under the hub (2026-11-24): since 2026-11-11 a Ø95 disc on the fixture, which the collar's r 41 bore cannot
# pass, so the shade could not be lowered off (4.0 free, 9.0 needed). Split: a Ø62 disc on the fixture (the hub's own
# Ø, it passes the bore) and a white ring on the cover, Ø95 x Ø63, under the collar's foot; together they hide the slots
# Review 2 (2026-11-24): the white ring is turned as part of the collar, an inward lip at its foot (bore Ø65: 1.5 radial
# to the Ø62 hub and disc, room for the shade's tilt on the PEEK land, about 1.0 to 1.3 at that radius), white beneath
WHITE_SPLIT = dict(disc=62.0, lip=(65.0, 2.0))


def _edge(r, z, s, inner, down):
    """A 45 deg chamfer (lead-in) of size s, as a turned triangle to subtract: at radius r and face z; inner: the edge of a
    bore (the material outside r), else of an outside diameter; down: the material below z, else above."""
    from build123d import Polyline, make_face, revolve, Axis
    dr = s if inner else -s
    dz = -s if down else s
    return revolve(make_face(Polyline((r - dr * 0.01, 0, z + dz * -0.01), (r + dr, 0, z + dz * -0.01), (r - dr * 0.01, 0, z + dz), close=True)), Axis.Z)
D = N                                            # the old name (dome_pendant.py, Planet's kit piece)

DOME_LIGHT = (0.0, 0.0, 81.5)                    # the COB's face, just under it (was 74: the old hub)


def _radii(p):
    R = p['R']
    r_shell_in = R - p['shell']
    r_liner = r_shell_in - p['gap']
    r_skin = r_liner - p['liner'] - p['gap']
    return R, r_shell_in, r_liner, r_skin, r_skin - p['skin']


def _sphere_band(r_out, r_in, a0, a1, zmin=0.0):
    """The part of a spherical shell (radii r_in..r_out, centre the origin) between the radii a0 and a1 from the axis,
    above zmin."""
    from build123d import Sphere
    s = (Sphere(r_out) - Sphere(r_in)) & (cyl('z', (0, 0), 2 * a1, zmin, r_out + 1) - cyl('z', (0, 0), 2 * a0, zmin - 1, r_out + 2))
    return s


def cover_parts(p=N):
    """The shade with its collar, the same for North and South: tint, opal, tint, formed and nested; the collar through
    the crown, clamped between its flange inside and a ring outside on silicone, so a failed bond cannot drop it."""
    R, r_si, r_l, r_k, r_ki = _radii(p)
    co, ci, cz0, cz1 = p['collar']
    fr = p['flange_r']
    tt_ = TOP_TIERS.get(p.get('top')) if p.get('top') in ('A', 'B') else None
    if tt_:
        cz1 = tt_['top']; fr = tt_['band_r']
    sh_ = bool(tt_)                       # the clamp ring held on a collar shoulder (review 2, (5))
    hole = cyl('z', (0, 0), (co + 4.4) if sh_ else (co + 0.4), 0, R + 5)
    shell = ball(R, p['shell'], (0, 0, 0), cut_below=0) - hole
    liner = ball(r_l, p['liner'], (0, 0, 0), cut_below=4) - hole
    skin = ball(r_k, p['skin'], (0, 0, 0), cut_below=0) - hole
    rim = cyl('z', (0, 0), 2 * (r_si - 0.2), 0, 3.8) - cyl('z', (0, 0), 2 * (r_k + 0.2), -1, 5)
    if p.get('build') == 'v3':
        # the mouth (2026-11-11, the bar): one even 1.0 x 45 deg chamfer on the rim's two lower edges, polished
        from build123d import chamfer, Axis
        rim = chamfer(rim.faces().sort_by(Axis.Z)[0].edges(), 1.0)
    # the collar: a tube through the crown, its flange a spherical seat under the skin (on a 1 mm silicone ring)
    tube = cyl('z', (0, 0), co, cz0, cz1) - cyl('z', (0, 0), ci, cz0 - 1, cz1 + 1)
    flange = _sphere_band(r_ki - 1.0, r_ki - 5.0, ci / 2, fr)
    collar = tube + flange
    if p.get('white_split'):
        # the lip (review 2): white beneath, its bore's lower edge led in 1 x 45
        ld_, lt_ = WHITE_SPLIT['lip']
        collar = collar + (cyl('z', (0, 0), ci + 0.2, cz0, cz0 + lt_) - cyl('z', (0, 0), ld_, cz0 - 1, cz0 + lt_ + 1))
        collar = collar - _edge(ld_ / 2, cz0, 1.0, inner=True, down=False)
    # the lead-in on the collar's top inner edge (review 2, (6)): the shade centres itself on the PEEK land going up
    collar = collar - _edge(ci / 2, cz1, 1.0, inner=True, down=True)
    if sh_:
        # (review 2, (4) and (5)) the shoulder the clamp ring screws down to, Ø100 from inside the crown's hole up to 92, so
        # the ring's height, and the collar's top 0.5 over it, are held on the collar; the thread M96 from a relief groove
        # (check 3: a DIN 76 undercut, Ø93.7, 92 to 95.75, 2.5 pitches) up; the squeeze is set by the stack and the silicone (top-redraw.md, the tolerance table)
        collar = collar + (cyl('z', (0, 0), co + 4.0, 86.0, 92.0) - cyl('z', (0, 0), ci, 85, 93))
        collar = collar - (cyl('z', (0, 0), co + 1, 92.0, 95.75) - cyl('z', (0, 0), 93.7, 91.9, 95.85))
        collar = collar - _edge(co / 2, cz1, 0.9, inner=False, down=True)
    # the L-slots, blind from inside (the clamp ring's thread is on the outside). Two sets (round 36): North's open at
    # the outer end (its hub outside the crown), South's at the inner end (its hub inside the bowl, so nothing hangs
    # below it). Each notch runs back toward its own entry, so the shade's weight holds each pin in it
    pz, w, rs = p['pin_z'], 5.0, ci / 2 + 4.5
    n0, n1 = p['notch']
    for a in (0, 120, 240):
        # v8 (the v7 check's (1)): the bayonet keyed: the slot at 0 deg 7 wide (its turn passage 7.5 tall) for the one pin
        # with a Ø6 shoulder, so the shade fits one way only (the Ø6 pin passes no 5 wide slot)
        wk_ = 7.0 if (a == 0 and p.get('fixings')) else w
        hk_ = 1.25 if (a == 0 and p.get('fixings')) else 0.0
        # V11-12 (the V10 check): mirrored, so "on" turns like a light bulb (clockwise seen from below): each entry 30 deg
        # past its notch (60/180/300), the notches, the pins, the detent and the lock where they were
        ae_ = a + 2 * p['turn'] if (MIRROR and p.get('fixings')) else a
        collar = collar - at(ae_, box(ci / 2 - 2, -wk_ / 2, pz - 10.5 - hk_, rs, wk_ / 2, cz1 + 1))         # the entry
        collar = collar - sector(ci / 2 - 2, rs, min(ae_, a + p['turn']), max(ae_, a + p['turn']), pz - 10.5 - hk_, pz - 5.5 + hk_)   # the turn
        # v9 (the v8 check's V9-4): the keyed notch's top n1 + 1.0 (the Ø6 pin's top is 1.0 above a Ø4's), so the shade rests
        # on all three pins; its foot and the turn passage keep the 7.5
        collar = collar - at(a + p['turn'], box(ci / 2 - 2, -wk_ / 2, n0 - hk_, rs, wk_ / 2, n1 + (1.0 if hk_ else 0.0)))     # the notch
    zs, off = p['south_pins']
    # (check 3, 2026-11-24) South's (dropped in round 38) slots' entries cut through the white lip, seen from below: with
    # the lip they are left out (South's shades would need their own collar)
    for a in (() if p.get('white_split') else (off, off + 120, off + 240)):
        collar = collar - at(a, box(ci / 2 - 2, -w / 2, cz0 - 1, rs, w / 2, zs + 7.5))                    # the entry
        collar = collar - sector(ci / 2 - 2, rs, a, a + p['turn'], zs + 2.5, zs + 7.5)                     # the turn
        collar = collar - at(a + p['turn'], box(ci / 2 - 2, -w / 2, zs - 2.5, rs, w / 2, zs + 7.5))        # the notch
    gasket_in = _sphere_band(r_ki, r_ki - 1.0, (co / 2 + 2.2) if sh_ else (co / 2 + 0.2), fr)
    gasket_out = _sphere_band(R + 1.0, R, (co / 2 + 2.2) if sh_ else (co / 2 + 0.2), fr)
    slip_ = None
    paint_ = None
    if p.get('white_split') and p.get('fixings'):
        # v7: the white paint as a film 0.05 off the collar's foot and the flange's inner face
        paint_ = (cyl('z', (0, 0), co, cz0 - 0.05, cz0) - cyl('z', (0, 0), WHITE_SPLIT['lip'][0] + 2.0, cz0 - 1, cz0 + 1)) + \
            _sphere_band(r_ki - 5.0, r_ki - 5.05, co / 2, fr)
        # v8 (the v7 check's (7)): and the lip's 1 x 45 lead-in ring, which the render paints too: a film 0.15 off it
        lr_ = WHITE_SPLIT['lip'][0] / 2; e_ = 0.1
        paint_ = paint_ + ((_edge(lr_ - e_, cz0 - e_, 1.0, inner=True, down=False) - _edge(lr_, cz0, 1.0, inner=True, down=False))
                           - cyl('z', (0, 0), 2 * lr_ + 2.0, cz0 - 0.06, cz0 + 0.01))
    if sh_:
        # v6 (the v5 check's (9)): the 0.25 PTFE slip washer drawn between the outer gasket and the clamp ring's band (the
        # gasket drawn at 0.75 there; the shims picked per shade take up the stack)
        gasket_out = _sphere_band(R + 0.75, R, co / 2 + 2.2, fr)
        slip_ = _sphere_band(R + 1.0, R + 0.75, co / 2 + 2.2, fr)
    if sh_:
        # (check 3, (e)) the silicone as built when the clamp ring's height is held on the collar: four rings, Shore 40, 1.3
        # thick free and drawn at 1.0 (23 % squeeze): the two gaskets and two shims in the air gaps at the crown (skin to
        # liner, liner to shell), the shims chosen per shade from the measured crown stack (the BOM's process step)
        gasket_in = gasket_in + _sphere_band(r_l - p['liner'], r_k, co / 2 + 2.2, fr) + _sphere_band(r_si, r_l, co / 2 + 2.2, fr)
    clamp = _sphere_band(R + 6.0, R + 1.0, co / 2, fr) + (cyl('z', (0, 0), co + 8, 92.0, 97.0) - cyl('z', (0, 0), co, 91, 98))
    clamp = clamp - cyl('z', (0, 0), co, 80, 110)
    if tt_:
        # PROPOSAL (2026-11-24, redrawn): the clamp ring is the first tier, Ø104 from 92 to 0.5 under the collar's top, its
        # bore the M96 thread, screwed down to the collar's shoulder (Ø100, at 92: its height held there), its top edge eased 1.0;
        # its band on the shade Ø116 as today, tapered to a 1.0 land (below)
        ring_ = eased(tt_['clamp'], 92.0, cz1 - 0.5, 1.0, bottom=False) - cyl('z', (0, 0), co, 80, 110) - cyl('z', (0, 0), co + 4.4, 80, 92.0)
        # (v5, check 4 (10)) the thread's lead-in on the ring's leading edge (its bore at z 92, where it starts onto the collar),
        # and the collar's top outer edge chamfered down to the thread's root
        ring_ = ring_ - _edge(co / 2, 92.0, 1.0, inner=True, down=False)
        band_ = _sphere_band(R + 6.0, R + 1.0, co / 2, fr) - cyl('z', (0, 0), co, 80, 110) - cyl('z', (0, 0), co + 4.4, 80, 92.0)
        if tt_.get('taper'):
            # the taper: everything above the line from the band's outer edge at the clamp ring's foot (r 52, on R+6) to
            # the land at its rim (r = fr, on R+1+land) cut away, as a turned cone
            from build123d import Polyline, make_face, revolve, Axis, Plane
            r0_, r1_ = tt_['clamp'] / 2, fr
            z0_ = math.sqrt((R + 6.0) ** 2 - r0_ ** 2); z1_ = math.sqrt((R + 1.0 + tt_['taper']) ** 2 - r1_ ** 2)
            sl_ = (z1_ - z0_) / (r1_ - r0_); r2_ = r1_ + 4.0
            prof_ = make_face(Polyline((r0_, 0, z0_), (r2_, 0, z0_ + sl_ * (r2_ - r0_)), (r2_, 0, z0_ + 40), (r0_, 0, z0_ + 40), close=True))
            band_ = band_ - revolve(prof_, Axis.Z)
        clamp = band_ + ring_
        # v6 (the v5 check's (6)): the thread's lead-in cut after the union (the band filled it back in)
        clamp = clamp - _edge(co / 2, 92.0, 1.0, inner=True, down=False)
        # V11-13: the one-way mark on the clamp ring's side over the keyed entry (60 deg: its thread start clocked to the
        # collar's, so screwed down to its shoulder it lands there): a vertical groove 0.4 wide, 0.2 deep, 5 long, cut
        # before anodizing, so it is black like the ring and reads by its edges
        zm_ = (92.0 + cz1 - 0.5) / 2
        clamp = clamp - at(60.0, box(tt_['clamp'] / 2 - 0.2, -0.2, zm_ - 2.5, tt_['clamp'] / 2 + 1.0, 0.2, zm_ + 2.5))
    if p.get('fixings') and not tt_:
        # V11-13: today's top (its clamp ring tightened to a torque, so at no set angle): the mark on the collar's 0.9 x 45
        # outer chamfer over the keyed entry (60 deg), a radial groove 0.4 wide, 0.2 deep, cut before anodizing
        collar = collar - at(60.0, box(co / 2 - 1.3, -0.2, cz1 - 1.1, co / 2 + 0.5, 0.2, cz1 + 0.5))
    lock_ = (TOP_TIERS.get(p.get('top')) or {}).get('lock') and p.get('fixings')
    lockp_ = None
    if p.get('white_split') and p.get('fixings') and not lock_:
        # v7 (the v6 check's (9)): the detent's dimple in the bore at 90 deg, z 93, where the pins sit in their notches (cut
        # last, after the shoulder's union); today's top and B only (A has the lock)
        # v8: the dimple where the ball stands with the shade seated (0.5 above, as drawn) and drawn, a short vertical slot
        # V10-10: redrawn for Kipp K0310.05's Ø3 ball: the dimple Ø3.1
        collar = collar - at(90.0, cyl('x', (0, p['pin_z'] + 0.5), 3.1, ci / 2 - 1, p['ring'][1] / 2 + 0.9) + cyl('x', (0, p['pin_z']), 3.1, ci / 2 - 1, p['ring'][1] / 2 + 0.9)
                                   + box(ci / 2 - 1, -1.55, p['pin_z'], p['ring'][1] / 2 + 0.9, 1.55, p['pin_z'] + 0.5))
    if lock_:
        # v7 (the coordinator's decision): the lock, Ganter GN 617-5-M10X1-AK, radially at 105 deg (opposite the level views'
        # camera, between the pins' notch at 30 and the slot's entry at 120), z 96. Its M10 x 1 tapped through the collar's
        # wall (drawn at its major Ø), a Ø10.5 clearance through A's clamp ring and a Ø20 spot face for the lock nut (both
        # machined before anodising, the ring's thread start clocked to the collar's). Drawn engaged: its Ø5 pin through the bore into the
        # PEEK ring to r 36.3; pulled 5, its tip stands at r 41.3, clear of the land (40.8) and the crown (40)
        from build123d import Plane as _Pl, RegularPolygon as _RP, extrude as _ex
        lk_ = GRIP['lock']; la_, lz_ = lk_['angle'], lk_['z']
        collar = collar - at(la_, cyl('x', (0, lz_), 10.0, ci / 2 - 0.5, co / 2 + 3.0))
        clamp = clamp - at(la_, cyl('x', (0, lz_), 10.5, co / 2 - 1.0, 60.0)) - at(la_, cyl('x', (0, lz_), 20.0, 51.5, 60.0))
        def _hexx(af, x0, x1):
            return _Pl(origin=(x0, 0, lz_), z_dir=(1, 0, 0)).location * _ex(_RP(af / math.sqrt(3), 6), x1 - x0)
        t0_ = lk_['tip_in']; t1_ = 41.2
        lockp_ = (cyl('x', (0, lz_), lk_['pin'], t0_, t1_) + cyl('x', (0, lz_), 10.0, t1_, 58.2) + _hexx(12.0, 58.2, 62.8)
                  + cyl('x', (0, lz_), 8.0, 62.8, 66.0) + cyl('x', (0, lz_), 21.1, 66.0, 81.3)
                  + (_hexx(16.0, 51.5, 56.5) - cyl('x', (0, lz_), 10.0, 50, 58)))
        lockp_ = at(la_, lockp_)
    note_formed = ('drape-formed from cast sheet over an aluminium mould, trimmed and polished; the prototypes are formed on '
                   'the production moulds')
    if p.get('build') == 'v3':
        # v3, the main build since the owner signed it (2026-11-01): the tint outside. The same three formed layers in a
        # new order: a 3 mm stock-tint shell outside (colour unlit), a 6 mm clear shell (the structural one, clamped by
        # the collar with the others), the 3 mm opal inside, seen directly from below; no tinted skin
        layers = [
            Part('shell', shell, Machined('acrylic-tint-3-formed', 'formed', setup_usd=1500.0), finish='body', group='cover',
                 notes=['v3, the outside: 1/8 in (3 mm) stock TruCast in the line\'s code (Ember 2423, Poison 2092, Haze '
                        '2287, Dust 2422, Acid 9097, Ice 2069, Fog 0000, Smoke 2074), ' + note_formed + '; CUSTOM POURS (the owner, '
                        '2026-11-11): Dust the same dye at 3x the stock sheet\'s loading; the mix (the owner, 2026-11-17, matched to Core '
                        'switched off): Acid 5x, Ice 6x, Ember 1.8x and Haze 1.8x the stock loading; Smoke at 1.2x '
                        'the stock loading (2026-11-16, was 0.3x, the speakers\' own pour; matched to Core switched off), not stock 2074; the one '
                        'tinted layer, seen unlit, glowing lit (15 to 20 % at 3 mm for 2423 and 2092). Its mould is v2\'s '
                        'shell mould (the outer face, R 100), the sheet 1/8 in instead of 10 mm']),
            Part('liner', liner, Machined('acrylic-clear-formed', 'formed', setup_usd=1500.0), finish='body',
                 group='cover', inside=True,
                 notes=['v3, the middle: 6 mm clear cast sheet (TruCast 0000), ' + note_formed + ': the structural shell '
                        '(R 96 to 90), clamped at the crown with the others; a new mould (v2\'s liner mould was R 90)']),
            Part('skin', skin, Machined('acrylic-opal-formed', 'formed', setup_usd=1200.0), finish='liner', group='cover',
                 notes=['v3, the inside: 3 mm volume-diffusing (opal) cast acrylic, Perspex GS 041 or equal (T 54 %, R 39 %, ASTM D1003), ' +
                        note_formed + ', formed into a female mould (R 89 to 86, a new mould), so its seen face keeps '
                        'its gloss; it hides the COB and lights evenly']),
        ]
    else:
        layers = None
    return (layers or [
        Part('shell', shell, Machined('acrylic-clear-formed', 'formed', setup_usd=1500.0), finish='body', group='cover',
             notes=['the outside: 10 mm cast sheet ' + note_formed + ' (9 at the crown, thinner toward the rim: the '
                    'former confirms); its outer face never touches the mould, so it keeps the cast sheet\'s gloss. '
                    'PROPOSAL 2026-11-01 (the stock-tint line, tint_proof): CLEAR, TruCast 0000; the color is the skin\'s, '
                    'seen through 9 of clear, so the shade still glows lit (12 mm of stock tint passes under 0.2 %)']),
        Part('liner', liner, Machined('acrylic-opal-formed', 'formed', setup_usd=1200.0), finish='liner', group='cover',
             inside=True,
             notes=['the diffuser: 3 mm volume-diffusing (opal) cast acrylic, Perspex GS 041 or equal (T 54 %, R 39 %, ASTM D1003), was about 70 % '
                    'transmission ' + note_formed + '. Opal scatters through its volume, so it diffuses wherever it '
                    'touches the tinted layers (a bead-blasted clear liner goes clear where it is bonded or wetted)']),
        Part('skin', skin, Machined('acrylic-formed', 'formed', setup_usd=1200.0), finish='body', group='cover',
             notes=['the inside: 3 mm tinted cast sheet formed into a female mould, so its inner (seen) face keeps its '
                    'gloss and the opal is seen only through tint. PROPOSAL 2026-11-01: 1/8 in stock TruCast in the line\'s '
                    'code (Ember 2423, Poison 2092, Haze 2287, Dust 2422, Acid 9097, Ice 2069, Fog 0000, Smoke 2074), its '
                    'chart transmission (14 to 93 %) as it is: the one tinted layer']),
    ]) + [
        Part('rim', rim, Machined('cast-acrylic', 'lathe'), finish='body', group='cover',
             notes=['THE MOUTH (2026-11-11, the bar): the three sheets\' stacked edge and this rim faced together, polished, '
                    'with one even 1.0 x 45 deg chamfer across all three, so the edge reads as one thick polished lip; '
                    'closes the three layers at the mouth, bonded and polished with them; a press-in ePTFE vent in its '
                    'face keeps the gaps between the layers at room pressure and dry. PROPOSAL 2026-11-03 (the night '
                    'pictures: a lit polished edge at the mouth pipes the diffuser\'s light out as a bright blue line): '
                    'v3\'s opal ends 4 inside the rim, as the clear shell does, and the rim\'s exposed face is bead-blasted '
                    'satin, not polished: no lit polished edge faces the room; about +$3 to +$5 a shade for the blasting '
                    '[E], the opal\'s shorter trim free']),
        Part('collar', collar, Machined('aluminium', 'lathe'), finish='anodised', group='cover',
             notes=['aluminium 6061, black anodised, satin: a tube through the crown with a spherical flange under the '
                    'skin; three blind L-slots with T-ended notches (the bayonet, 30 deg, keyed: it fits one way); '
                    'M96 x 1.5 outside for the clamp ring. It carries the cover mechanically: the bond is a seal only'
                    + (('. Review 2 (2026-11-24): an inward lip at its foot, bore Ø65 led in 1 x 45, painted white beneath (the '
                        'white ring that hides the slots from below; 1.5 radial to the hub and the Ø62 disc, so the shade comes off); '
                        'its top inner edge led in 1 x 45') if p.get('white_split') else '')
                    + (('. Even-tier top (PROPOSAL): up to the clamp ring\'s top + 0.5, a Ø100 shoulder at 86 to 92 that the clamp '
                        'ring screws down to (its height held on the collar), a DIN 76 undercut Ø93.7 at 92 to 95.75, the thread above '
                        'it; the crown\'s hole Ø100.4') if sh_ else '')]),
        Part('clamp', clamp, Machined('aluminium', 'lathe'), finish='anodised', group='cover',
             notes=[('aluminium, black anodised: screwed down to the collar\'s shoulder (its height held there, the squeeze set by '
                     'the stack and the shims, not by torque), its spherical face on the PTFE slip washer over the outer silicone '
                     'ring (four rings in all; never metal on acrylic); no thread-locker near acrylic (review 2026-11-01: anaerobics '
                     'craze it): held by the shoulder') if sh_ else
                    ('aluminium, black anodised: screwed onto the collar over the crown, its spherical face on a silicone '
                     'ring, to a torque the shade maker sets (the acrylic is clamped between two silicone rings, never metal '
                     'on acrylic); no thread-locker near acrylic (review 2026-11-01: anaerobics craze it): held by the '
                     'silicone\'s preload')]),
        Part('gaskets', gasket_in + gasket_out, Bought('hemi-gaskets-4' if sh_ else 'hemi-gaskets'), finish='silicone', group='cover',
             notes=(['PROPOSAL (v7): four silicone rings, Shore 40, each 1.3 free: two gaskets and two shims in the crown\'s air gaps, '
                     'drawn at 1.0 (the outer gasket at 0.75, the 0.25 PTFE slip washer drawn over it under the clamp ring\'s band, '
                     'which turns against it while tightening). PROCESS: the shade maker measures each crown\'s stack (cast sheet is '
                     'held to only ±(0.4 + 0.1t), ISO 7823-1: ±0.7, ±1.0, ±0.7 here) and picks the two shims from 0 (left out), 0.5, '
                     '1.0, 1.6, 2.2 and 2.9 so the squeeze lands at 20 to 35 % over the whole RSS range (at the thickest worst-case '
                     'stack it reaches 38 %)'] if sh_ else
                    ['two silicone gaskets, 1.0, the acrylic clamped between them; the clamp ring tightened to the shade maker\'s torque'])),
        *([Part('white-paint', paint_, Bought('hemi-white-paint'), finish='white', group='cover',
                notes=['v7 (the v6 check\'s (7)): the painted faces, drawn as a 0.05 film: the collar\'s foot beneath (the lip, '
                       'r 33.5 to 48) and the flange\'s inner face (r 48 to 58), every down-facing face below z 80, about 8,460 mm2: '
                       'the render and the BOM paint the same faces'])] if paint_ is not None else []),
        *([Part('lock', lockp_, Bought('hemi-lock'), finish='trim', group='cover',
                notes=['v7 (PROPOSAL): the shade\'s positive lock, Ganter GN 617-5-M10X1-AK (pin Ø5 H7, M10 x 1, knob Ø21, stroke 5, '
                       'spring 7 to 17 N), threaded into the collar at 105 deg, z 96.5 as drawn (96.0 seated), through the clamp ring, its lock nut on a Ø20 spot face; '
                       'its pin in a Ø6.4 hole in the PEEK ring blocks the lift and the turn. Keep the knob pulled through the lift, the '
                       'turn and the lower (let go, its pin presses about 14 N on the crown\'s first tier and wears it); let it go only '
                       'with the shade home. One per shade'])] if lockp_ is not None else []),
        *([Part('slip-washer', slip_, Bought('hemi-slip-washer'), finish='trim', group='cover', inside=True,
                notes=['PROPOSAL (v6): a 0.25 PTFE film ring, spherical, between the outer silicone ring and the clamp ring\'s band'])]
          if slip_ is not None else []),
        Part('vent', None, Bought('hemi-vent')),
    ]


def north_parts(p=N):
    """Hemisphere (Hemisphere North in rounds 35 to 37): the cover hangs mouth down from the fixture: the hub core in the crown (the COB 22 up a 46 bore
    lined with a reflector: the 46 deg cut-off), the PEEK ring that carries the bayonet's pins (the thermal break), the
    black crown over the collar and the aluminium cap on it (round 41: round 32f's low top, the heat sink; the fins of
    rounds 35 to 39 are in git at 950a7eaf), the cord, the canopy with the driver. For 575 lm only: 1,100 lm needs the
    fins (hemisphere_thermal.py)."""
    R, r_si, r_l, r_k, r_ki = _radii(p)
    od, z0, z1 = p['core']
    bd, bz = p['bore']
    nd, nz = p['neck']
    sd, sz0, sz1 = p['crown']
    cd, ch = p['cap']
    ri, ro, rz0, rz1 = p['ring']
    pz = p['pin_z']
    ring_ = p.get('engine') == 'ring'
    if ring_:
        # option 3: the hub solid, a Ø16.1 socket 25 deep for the stem from below (bonded and pinned), the wires up it
        sod, sid = p['stem']
        core = cyl('z', (0, 0), od, z0, z1) - cyl('z', (0, 0), sod + 0.1, z0 - 1, z0 + 25)
    else:
        core = cyl('z', (0, 0), od, z0, z1) - cyl('z', (0, 0), bd, z0 - 1, bz) - cyl('z', (0, 0), 28.4, bz, bz + 3)
    core = core + cyl('z', (0, 0), nd, z1, nz)
    core = core - cyl('z', (0, 0), 10, bz + 3, nz + 1)                                 # the wires
    ring = cyl('z', (0, 0), ro, rz0, rz1) - cyl('z', (0, 0), ri, rz0 - 1, rz1 + 1)
    if p.get('white_split'):                  # (review 2, (6)) the PEEK land's lower outer edge led in 1 x 45
        ring = ring - _edge(ro / 2, rz0, 1.0, inner=False, down=False)
    # the bayonet's pins (review 2026-11-01): stainless shouldered pins, the M3 thread through the PEEK into the hub, the
    # Ø4 shoulder seated on the PEEK's land and reaching 4.0 into the collar's slots (was a 4 x 8 dowel, 2.5 in)
    sd_, tip, td, tin = p['pin']
    pins = None
    for a in (0, 120, 240):
        sdk_ = 6.0 if (a == 0 and p.get('fixings')) else sd_            # v8: the key, one pin's shoulder Ø6
        tdk_ = 4.0 if (a == 0 and p.get('fixings')) else td             # v9: and its own M4 thread, so it fits only its hole
        pin = at(a + p['turn'], cyl('x', (0, pz), sdk_, ro / 2, tip) + cyl('x', (0, pz), tdk_, tin, ro / 2))
        pins = pin if pins is None else pins + pin
        # (check 3, (l)) the pin's thread through a Ø3.2 clearance in the PEEK, tapped M3 (Ø2.5) in the hub
        ring = ring - at(a + p['turn'], cyl('x', (0, pz), 4.3 if (a == 0 and p.get('fixings')) else 3.2, ri / 2 - 1, ro / 2 + 1))
        # v6: tapped M3, drawn at its major Ø; v7 (the v6 check's (10)): 7.5 deep for 6.0 of thread (the tap's run-out), so a
        # pin seats on its shoulder and cannot stand proud toward the slot's floor
        core = core - at(a + p['turn'], cyl('x', (0, pz), (4.0 if a == 0 else 3.0) if p.get('fixings') else 2.5, (tin - 1.5) if p.get('fixings') else tin, ro / 2 + 1))
    plunger_ = None
    nlock_ = (TOP_TIERS.get(p.get('top')) or {}).get('lock') and p.get('fixings')
    if nlock_:
        # v7/v8: the lock's hole in the PEEK ring (Ø6.4 for its Ø5 pin, at 105 deg, z 96.0, to r 36.0)
        # v8 (the v7 check's (2)): the hole where the pin stands with the shade SEATED (0.5 under its drawn pose), Ø6.4 for
        # the bayonet's play (about -+0.43 at the hole and the land's 0.2); no cam chamfer on the ring (a pin let go early
        # does not ride onto the land under the shade's weight: the swap holds the knob until home)
        lk_ = GRIP['lock']
        ring = ring - at(lk_['angle'], cyl('x', (0, lk_['z'] - 0.5), 6.4, lk_['tip_in'] - 0.3, ro / 2 + 1))
    if p.get('fixings') and not nlock_:
        # v7 (the v6 check's (9)): today's top and B: the bayonet's detent drawn, an M5 stainless ball spring plunger (dome-plunger), 12 long,
        # radially at 90 deg, z 93 (between the pins at 30/150/270 and off the turn's path): threaded through the PEEK ring
        # (tapped M5, drawn at its major Ø), its inner end in a Ø5.4 clearance in the hub, its Ø2.5 ball 0.8 proud of the
        # land into a Ø2.6 dimple in the collar's bore where the pins sit in their notches
        dpa_ = 90.0
        plunger_ = at(dpa_, cyl('x', (0, pz), 5.0, ro / 2 - 12.0, ro / 2) )
        plunger_ = plunger_ + at(dpa_, cyl('x', (0, pz), 3.0, ro / 2, ro / 2 + 0.9))     # its ball (Kipp K0310.05, Ø3, H 0.9 proud: V11-11), drawn as its tip
        ring = ring - at(dpa_, cyl('x', (0, pz), 5.0, ri / 2 - 1, ro / 2 + 1))
        # v8 (the v7 check's (8)): its clearance in the hub a groove 5.4 wide open to the hub's top, so the ring slides down
        # over the hub with the plunger already screwed in
        core = core - at(dpa_, box(ro / 2 - 12.5, -2.7, pz - 2.7, ri / 2 + 0.1, 2.7, z1 + 0.1))
    # the reflector: a faceted cone of high-reflectance aluminium in the bore, from the COB's edge to the mouth
    from build123d import Cone, Pos, Align
    al = (Align.CENTER, Align.CENTER, Align.MIN)
    refl = Pos(0, 0, z0 + 0.5) * (Cone(bd / 2 - 0.6, 10.0, bz - z0 - 1.0, align=al) -
                                  Cone(bd / 2 - 1.1, 9.5, bz - z0 - 1.0, align=al))
    refl = refl & cyl('z', (0, 0), bd - 0.2, z0 + 0.5, bz - 0.5)
    cob = cyl('z', (0, 0), 28, bz, bz + 2)
    if ring_:
        # the carrier: black anodised aluminium, Ø56 x 4.5, its underside on the rim plane (z 0), a Ø50.2 pocket 1.6 deep
        # in its top for the board (1.8 deep: the board 0.2 under the carrier's face), so the LEDs' emitting faces are at
        # z 4.9 (nothing below the rim)
        cd_, ct_ = p['carrier']; bd_, bt_ = p['board']
        # 2026-11-11 (the bar: from below it must look finished): the carrier's underside closed (the stem's bore blind, 1
        # mm of floor; the wires come up the stem to the board's top) and its edges eased 0.6
        carrier = eased(cd_, 0.0, ct_, 0.6) - cyl('z', (0, 0), bd_ + 0.2, ct_ - bt_ - 0.2, ct_ + 1) - cyl('z', (0, 0), sid, 1.0, ct_ + 1)
        board = cyl('z', (0, 0), bd_, ct_ - bt_ - 0.2, ct_ - 0.2) - cyl('z', (0, 0), sod + 0.4, ct_ - bt_ - 1, ct_ + 1)
        leds = None
        for k in range(24):
            a_ = 2 * math.pi * k / 24
            l_ = box(19 * math.cos(a_) - 1.5, 19 * math.sin(a_) - 1.5, ct_ - 0.2, 19 * math.cos(a_) + 1.5, 19 * math.sin(a_) + 1.5, ct_ + 0.4)
            leds = l_ if leds is None else leds + l_
        # the stem: 16/12 aluminium tube, black anodised, from the board's centre up into the hub's socket (the heat path
        # to the hub; a heat pipe inside it is optional at about 2.5 W of heat)
        stem = cyl('z', (0, 0), sod, ct_ - bt_ - 0.2, z0 + 24.5) - cyl('z', (0, 0), sid, ct_ - bt_ - 1, z0 + 26)
        # the crown's inside white: a white Ø80 disc, 1 thick, under the hub (and the collar's flange face painted white)
        wdisc = cyl('z', (0, 0), WHITE_SPLIT['disc'] if p.get('white_split') else p['white_disc'], z0 - 1.0, z0) - cyl('z', (0, 0), sod + 0.4, z0 - 2, z0 + 1)
        if p.get('white_split'):
            wdisc = wdisc - _edge(WHITE_SPLIT['disc'] / 2, z0 - 1.0, 0.5, inner=False, down=False)
    # 2026-11-11 (the bar: the cap reads as turned parts): the crown and the gland with eased 1.0 edges, so each terrace
    # catches a soft highlight
    crown = eased(sd, sz0, sz1, 1.0) - cyl('z', (0, 0), nd + 0.2, sz0 - 1, nz) - cyl('z', (0, 0), 10, sz0 - 1, sz1 + 1)
    gland = eased(cd, sz1, sz1 + ch, 1.0) - cyl('z', (0, 0), 8, sz1 - 1, sz1 + ch + 1)
    z_cord = sz1 + ch
    tt_ = TOP_TIERS.get(p.get('top') or ('today' if p.get('fixings') else None))
    if tt_:
        # PROPOSAL (check 3, 2026-11-24): the crown's tiers and the cap (gland) as TOP_TIERS draws them, each eased 1.0, the
        # crown on the hub's neck, metal to metal (the first tier Ø80, inside the collar's Ø82 bore, so the shade rises past it);
        # the fixings as GRIP describes them
        crown = None
        for d_, a_, b_ in tt_['crown']:
            t_ = eased(d_, a_, b_, 1.0)
            crown = t_ if crown is None else crown + t_
        gd_, g0_, g1_ = tt_['gland']
        f0_, f1_ = GRIP['floor']; td_, tl_ = GRIP['thread']; pk_ = GRIP['pocket']; lid_ = GRIP['lid']
        cr_ = tt_.get('cable_r', GRIP['cable_r'])
        sr_ = GRIP['screws_r']; cpk_ = GRIP['cap_pocket']
        ctop_ = tt_['crown'][-1][2]
        # V11-13: the one-way line on the crown's lowest tier's side over the key pin (30 deg): a vertical groove 0.4 wide,
        # 0.2 deep, 5 long, cut before anodizing
        cd0_, cz0_, cz1_ = tt_['crown'][0]
        crown = crown - at(30.0, box(cd0_ / 2 - 0.2, -0.2, (cz0_ + cz1_) / 2 - 2.5, cd0_ / 2 + 1.0, 0.2, (cz0_ + cz1_) / 2 + 2.5))
        crown = (crown - cyl('z', (0, 0), nd + 0.2, sz0 - 1, f0_) - cyl('z', (0, 0), td_ + 0.5, f0_ - 1, f1_ + 0.1)
                 - cyl('z', (0, 0), pk_, f1_, g0_ + 1))
        from build123d import Cone, Pos, Align, RegularPolygon, extrude, Solid, Plane, Vector as V3
        al_ = (Align.CENTER, Align.CENTER, Align.MIN)
        # v6 (the v5 check's (1)): two cables at r cr_ (0 and 180 deg), each from a Nicopress stop sleeve bearing under a
        # Ø5.6 x 8 counterbore in the hub's bottom face (the white disc closes it), up a Ø2.4 hole through the hub and the
        # crown, its exit rounded, and through the cap's lid (today, A) or beside the cap (B)
        cang_ = tt_.get('cables', GRIP['cables']); a0_ = cang_[0]
        cxy_ = [(cr_ * math.cos(math.radians(a_)), cr_ * math.sin(math.radians(a_))) for a_ in cang_]
        cbd_, cbh_ = GRIP['cbore']; svd_, svl_ = GRIP['sleeve']; cbl_ = GRIP['cable']
        thru_ = gd_ / 2 > cr_ + 2.0           # the cables pass through the cap (today, A), else beside it (B)
        sleeves = None
        for xy_ in cxy_:
            crown = crown - cyl('z', xy_, 2.4, f0_ - 1, ctop_ + 1) - Pos(xy_[0], xy_[1], ctop_ - 0.6) * Cone(1.2, 1.9, 0.61, align=al_)
            core = core - cyl('z', xy_, cbd_, z0 - 1, z0 + cbh_) - cyl('z', xy_, 2.4, z0 + cbh_ - 0.1, f0_ + 0.1)
            sv_ = cyl('z', xy_, svd_, z0 + cbh_ - svl_, z0 + cbh_)
            sleeves = sv_ if sleeves is None else sleeves + sv_
        # three M2.5 countersunk screws at 90, 210, 330 deg (clear of the cables), r 9.25, flush in the 2.5 floor, their
        # heads inside the Ø24 pocket
        sc_ = None
        for a_ in GRIP['screws_a']:
            x_, y_ = sr_ * math.cos(math.radians(a_)), sr_ * math.sin(math.radians(a_))
            crown = crown - cyl('z', (x_, y_), 2.9, f0_ - 1, f1_ + 0.1) - Pos(x_, y_, f1_ - 1.36) * Cone(1.45, 2.4, 1.37, align=al_)
            core = core - cyl('z', (x_, y_), 2.5, f0_ - 6.0, f0_ + 0.1)        # M2.5 tapped 6 (drawn at its major Ø)
            s_ = cyl('z', (x_, y_), 2.5, f0_ - 5.0, f1_ - 1.36) + Pos(x_, y_, f1_ - 1.36) * Cone(1.25, 2.35, 1.36, align=al_)
            sc_ = s_ if sc_ is None else sc_ + s_
        core = core - cyl('z', (0, 0), nd + 1, f0_, nz + 1) - cyl('z', (0, 0), td_, f0_ - GRIP['tap'], f0_ + 0.1)
        # the cap: today's and A's keyed by a Ø2 dowel and held by a Ø2 x 2 magnet over a steel disc at r 15.5; B's held by a
        # Ø1.5 magnet only (v6, (7)); its pocket Ø20 over the grip's dome nut, its cable holes rounded
        gland = (eased(gd_, g0_, g1_, 1.0) - cyl('z', (0, 0), cpk_, g0_ - 1, g1_ - lid_) - cyl('z', (0, 0), 8, g1_ - lid_ - 1, g1_ + 1))
        key_ = tt_['key'] if 'key' in tt_ else GRIP['key']
        mr_, ma_, md_ = tt_.get('magnet', GRIP['magnet'])
        mx_, my_ = mr_ * math.cos(math.radians(ma_)), mr_ * math.sin(math.radians(ma_))
        keys = cyl('z', (mx_, my_), md_, g0_ - 2.0, g0_) + cyl('z', (mx_, my_), md_, g0_, g0_ + 0.5)
        crown = crown - cyl('z', (mx_, my_), md_, g0_ - 2.0, g0_ + 0.1)
        gland = gland - cyl('z', (mx_, my_), md_, g0_ - 0.1, g0_ + 0.5)
        if key_:
            kr_, ka_, kd_ = key_
            kx_, ky_ = kr_ * math.cos(math.radians(ka_)), kr_ * math.sin(math.radians(ka_))
            keys = keys + cyl('z', (kx_, ky_), kd_, g0_ - 3.0, g0_ + 2.0)
            crown = crown - cyl('z', (kx_, ky_), kd_, g0_ - 3.0, g0_ + 0.1)
            gland = gland - cyl('z', (kx_, ky_), kd_ + 0.05, g0_ - 0.1, g0_ + 2.1)
        if thru_:
            for xy_ in cxy_:
                gland = gland - cyl('z', xy_, 2.4, g0_ - 1, g1_ + 1) - Pos(xy_[0], xy_[1], g1_ - 0.6) * Cone(1.2, 1.9, 0.61, align=al_)
        cex_ = g1_ if thru_ else ctop_             # where the cables leave the top
        # the grip: Lapp's hex 16 across the flats with its corners turned to Ø17.6; drawn in the hub's tapped hole at its
        # major Ø (the tap drawn at M12)
        af_, ac_, hh_ = GRIP['hex']; sq_ = f1_; top_ = sq_ + GRIP['overall'] - tl_
        hexs_ = (Pos(0, 0, sq_) * extrude(RegularPolygon(af_ / math.sqrt(3), 6), hh_)) & cyl('z', (0, 0), ac_, sq_, sq_ + hh_)
        grip = (cyl('z', (0, 0), td_, sq_ - tl_, sq_) + hexs_
                + eased(ac_ - 0.6, sq_ + hh_, top_, 3.0, bottom=False) - cyl('z', (0, 0), 7.0, sq_ - tl_ - 1, top_ + 1))
        # v7 (the coordinator's decision, 17:39 UTC): no tether; the shade's secondary retention is a positive lock on top A
        # (an indexing plunger, GRIP['lock']). The helpers below draw the cables and the cord
        def _rad(a, r, z):
            return V3(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), z)
        def _rod(p0, p1, rad):
            dv = p1 - p0
            return Solid.make_cylinder(rad, dv.length, Plane(origin=p0, z_dir=dv))
        z_cord = g1_
    cord_ = None
    zc = z_cord + p['drop']
    cnd, cnh = p['canopy']
    if tt_:
        # v6 (the v5 check's (3)): the cord 2 mm longer than the straight run, bowed to one side (+y) in a circular arc of
        # sagitta about 21 mm, from the cap's grip to the canopy's floor
        L_ = zc - z_cord; s_ = math.sqrt(3.0 * L_ * 2.0 / 8.0); Rb_ = (L_ ** 2 / 4 + s_ ** 2) / (2 * s_)
        n_ = 24; th0_ = math.asin((L_ / 2) / Rb_)
        cps_ = []
        for k_ in range(n_ + 1):
            th_ = -th0_ + 2 * th0_ * k_ / n_
            cps_.append(V3(0.0, Rb_ * math.cos(th_) - (Rb_ - s_), z_cord + L_ / 2 + Rb_ * math.sin(th_)))
        cord_len_ = sum((cps_[k_ + 1] - cps_[k_]).length for k_ in range(n_))
        for k_ in range(n_):
            seg_ = _rod(cps_[k_], cps_[k_ + 1], 3.0) + (Pos(cps_[k_ + 1]) * Solid.make_sphere(3.0))
            cord_ = seg_ if cord_ is None else cord_ + seg_
        cord = cord_
    else:
        cord = cyl('z', (0, 0), 6, z_cord, z_cord + p['drop'])
    # round 43 (proposal, certification.md): the fixture hangs from a fine steel cable beside the cord, so the cord
    # carries current only (UL 153 lets an SPT-2 cord carry 2.5 lb; Hemisphere is about 3.5); an option until signed
    susp = cyl('z', (5.5, 0), 1.5, z_cord, zc) + cyl('z', (5.5, 0), 5.0, z_cord, z_cord + 9) + cyl('z', (5.5, 0), 5.0, zc - 9, zc)
    if tt_:
        # v6/v7: each cable straight up from its sleeve to where it leaves the top, then splayed to its gripper at r 48 in the
        # canopy, through the gripper and its tail (50, coiled in the bracket); v7 (the v6 check's (3), (4)): each gripper's
        # knurled safety nut drawn round its plunger end; the gripper threaded up through a U bracket's foot, held by an M10
        # nylon-insert nut (ISO 10511, 16 AF, 8 tall) on top, the bracket's two legs across the cables' line (the nut open
        # to a spanner from the sides) and its two top flanges riveted under the plate (four Ø3.2 blind rivets)
        gr_ = GRIP['gripper_r']; susp = sleeves
        grippers = brackets = gnuts = safety = rivets = None
        zg0_ = zc + 3.0 + 4.0                        # the safety nut's foot, 4 above the floor's top
        for (x_, y_), a_ in zip(cxy_, cang_):
            ax_, ay_ = gr_ * math.cos(math.radians(a_)), gr_ * math.sin(math.radians(a_))
            susp = (susp + cyl('z', (x_, y_), cbl_, z0 + cbh_, cex_ + 0.5)
                    + _rod(V3(x_, y_, cex_), V3(ax_, ay_, zg0_ - 0.5), cbl_ / 2) + cyl('z', (ax_, ay_), cbl_, zg0_ - 0.5, zg0_ + 20.1 + 12.0))
            # the gripper and its bracket drawn on the x axis, then turned onto the cables' line (a0_)
            gx_, gy_ = gr_ * math.cos(math.radians(a_ - a0_)), gr_ * math.sin(math.radians(a_ - a0_))
            # the gripper as Cable Grippers' chart gives it: its plunger end Ø6 inside the knurled safety nut (Ø12 x 3), the
            # body Ø11.9 x 4.5 and the M10 thread 12.6 (17.1 without the plunger)
            g_ = (cyl('z', (gx_, gy_), 6.0, zg0_ + 0.5, zg0_ + 3.0) + cyl('z', (gx_, gy_), 11.9, zg0_ + 3.0, zg0_ + 7.5)
                  + cyl('z', (gx_, gy_), 10.0, zg0_ + 7.5, zg0_ + 20.1))
            g_ = g_ - cyl('z', (gx_, gy_), cbl_ + 0.1, zg0_ - 1, zg0_ + 21)
            sn_ = cyl('z', (gx_, gy_), 12.0, zg0_, zg0_ + 3.0) - cyl('z', (gx_, gy_), 6.0, zg0_ - 1, zg0_ + 4)
            zf_ = zg0_ + 7.5                         # the bracket's foot on the body's shoulder
            nut_ = (Pos(gx_, gy_, zf_ + 1.6) * extrude(RegularPolygon(16.0 / math.sqrt(3), 6), 8.0)) & cyl('z', (gx_, gy_), 17.8, zf_, zf_ + 12)
            nut_ = nut_ - cyl('z', (gx_, gy_), 10.0, zf_, zf_ + 12)
            zp_ = zc + cnh - 1.6                     # the plate's underside
            # v8 (the v7 check's (4)): the bracket a U along the cables' line, its legs 42 apart (a 16 open-end spanner's
            # head reaches the nut from the outside, x > gx), its flanges turned OUT under the plate, each held by two
            # PEM FH-M3 flush studs pressed into the plate and M3 nuts under the flange (the gripper changes without
            # drilling); the foot Ø10.5 for the gripper's M10
            br_ = box(gx_ - 11.0, gy_ - 22.6, zf_, gx_ + 11.0, gy_ + 22.6, zf_ + 1.6)
            for sy_ in (-1.0, 1.0):
                yl0_, yl1_ = sorted((gy_ + sy_ * 21.0, gy_ + sy_ * 22.6))
                br_ = br_ + box(gx_ - 11.0, yl0_, zf_, gx_ + 11.0, yl1_, zp_)
                yf0_, yf1_ = sorted((gy_ + sy_ * 22.6, gy_ + sy_ * 36.0))
                br_ = br_ + box(gx_ - 11.0, yf0_, zp_ - 1.6, gx_ + 11.0, yf1_, zp_)
                for rx_ in (gx_ - 4.5, gx_ + 4.5):
                    ry_ = gy_ + sy_ * 29.3
                    # v9: PEM FH-M3-8 (8 long under the plate's top), the M3 nylon-insert nut 4 tall fully on it
                    rv_ = cyl('z', (rx_, ry_), 3.0, zp_ + 1.6 - 8.0, zp_ + 1.6) + \
                        (cyl('z', (rx_, ry_), 6.0, zp_ - 1.6 - 4.0, zp_ - 1.6) - cyl('z', (rx_, ry_), 3.0, zp_ - 8, zp_))
                    br_ = br_ - cyl('z', (rx_, ry_), 3.4, zp_ - 2, zp_ + 0.1)          # V11-14: Ø3.4 clearance, as called
                    rv_ = at(a0_, rv_)
                    rivets = rv_ if rivets is None else rivets + rv_
            br_ = br_ - cyl('z', (gx_, gy_), 10.5, zf_ - 1, zf_ + 3)
            g_, nut_, sn_, br_ = at(a0_, g_), at(a0_, nut_), at(a0_, sn_), at(a0_, br_)
            grippers = g_ if grippers is None else grippers + g_
            gnuts = nut_ if gnuts is None else gnuts + nut_
            safety = sn_ if safety is None else safety + sn_
            brackets = br_ if brackets is None else brackets + br_
    # v6/v7: the canopy right side up: open at the top against the ceiling, its 3 floor closed below (the cord's gland in
    # its centre, the two cables through Ø3 holes at r 48). v7 (the v6 check's (3), (8)): the strap becomes a round mounting
    # plate (1.6 steel, Ø140 with a down-turned rim 12 deep), screwed to the junction box by two 8-32 screws at y -+44.45 (a
    # 4 in box); the canopy is held to the rim by two M4 x 8 flush black set screws (90/270 deg) into clinch nuts in it.
    # The plate carries the load: the grippers' brackets riveted under it, and the driver's steel enclosure on four 6
    # standoffs below it (fitted after the plate is screwed up: the box screws' heads in the gap)
    canopy = cyl('z', (0, 0), cnd, zc, zc + cnh) - cyl('z', (0, 0), cnd - 6, zc + 3.0, zc + cnh + 1)
    a0_ = cang_[0] if tt_ else 0.0                # the canopy's parts turned with the cables' line
    if tt_:
        for a_ in cang_:
            canopy = canopy - cyl('z', (gr_ * math.cos(math.radians(a_)), gr_ * math.sin(math.radians(a_))), 3.0, zc - 1, zc + 4)
    ztop = zc + cnh
    if tt_:
        # V11-14: the bore's 1.0 x 30 deg lead-in at its top edge (for the plate's rim)
        from build123d import Cone as _Co, Pos as _Po
        canopy = canopy - _Po(0, 0, ztop - 1.0 / math.tan(math.radians(30.0))) * _Co(cnd / 2 - 3.0, cnd / 2 - 2.0, 1.0 / math.tan(math.radians(30.0)) + 0.01, align=(Align.CENTER, Align.CENTER, Align.MIN))    # v9 (the v8 check's V9-2): the canopy's inside as it is built, wired and closed. All drawn on the x axis, then turned
    # onto the cables' line (a0_).
    # THE PLATE: 1.6 zinc-plated steel, Ø143.6 (its rim turned down 12, 0.2 inside the canopy's wall); a rolled Ø22 opening
    # in its centre for the supply; two Ø4.3 holes for the box's 8-32 screws at y -+44.45; four PEM SO-M4 standoffs
    # (Ø7.14 holes); eight PEM FH-M3-8 studs for the gripper brackets; a downward-extruded 10-32 hole (2.4 deep, five
    # threads) for the green grounding screw at y +56, its tip 0.8 above the plate when tight
    rr0_ = cnd / 2 - 3.0 - 0.2
    strap = (cyl('z', (0, 0), 2 * rr0_, ztop - 1.6, ztop) + (cyl('z', (0, 0), 2 * rr0_, ztop - 12.0, ztop) - cyl('z', (0, 0), 2 * rr0_ - 3.2, ztop - 13, ztop + 1)))
    strap = strap - cyl('z', (0, 0), 22.0, ztop - 2, ztop + 1)
    bscr_ = None
    for y_ in (-44.45, 44.45):                     # the box's two 8-32 screws, their heads under the plate
        b_ = cyl('z', (0, y_), 4.3, ztop - 1.6, ztop + 8.0) + cyl('z', (0, y_), 7.6, ztop - 1.6 - 2.4, ztop - 1.6)
        strap = strap - cyl('z', (0, y_), 4.3, ztop - 2, ztop + 1)
        bscr_ = b_ if bscr_ is None else bscr_ + b_
    strap = strap + (cyl('z', (0, 56.0), 8.0, ztop - 1.6 - 2.4, ztop - 1.6) - cyl('z', (0, 56.0), 4.8, ztop - 5, ztop + 1))
    strap = strap - cyl('z', (0, 56.0), 4.8, ztop - 5, ztop + 1)
    gsc_ = cyl('z', (0, 56.0), 4.8, ztop - 1.6 - 2.4, ztop + 0.8) + cyl('z', (0, 56.0), 9.5, ztop - 1.6 - 2.4 - 3.0, ztop - 1.6 - 2.4)
    # THE CANOPY'S FIXING: two M4 x 4 cup-point set screws (nylon patch) tapped through the canopy's wall at 90/270 deg,
    # 6 below its top, their cups on the plate's rim (r 71.8); flush, as before; tapped after anodising, so their threads
    # and cups bond the canopy to the plate
    setsc_ = None
    for a_ in (90.0, 270.0):
        ss_ = at(a_, cyl('x', (0, ztop - 6.0), 4.0, rr0_, rr0_ + 3.0))    # V10-5: M4 x 3 cup point, its cup on the rim, 0.2 under the wall's face
        setsc_ = ss_ if setsc_ is None else setsc_ + ss_
    # THE ENCLOSURE: 1.0 zinc-plated steel, 64 x 100 x 38, open below, closed by a removable cover (two M3 screws into
    # tabs bent in at its ends); on four PEM SO-M4 standoffs (Ø7.9 hex, 4 long) under the plate, four serrated M4 x 6
    # screws from inside its top (the cover off). The driver, ERP ESS010W at its real 84 x 40 x 25, its leads at its ends.
    # Free volume 7.9 in3 against NEC 314.16's 6.0 in3 for the supply's three 14 AWG conductors (the driver's leads,
    # fixture wires, not counted). A listed snap bushing in its top for the supply, a listed strain-relief bushing in the
    # cover for the Class 2 cord, which it clamps (UL 1598: the cord's strain relief is here; the steel cables carry the lamp)
    ez1_ = ztop - 1.6 - 4.0; ez0_ = ez1_ - 38.0
    encl = box(-32, -50, ez0_, 32, 50, ez1_) - box(-31, -49, ez0_ - 1, 31, 49, ez1_ - 1)
    encl = encl - cyl('z', (0, 0), 22.0, ez1_ - 2, ez1_ + 1)
    tabs_ = box(-4, 45.0, ez0_, 4, 49.0, ez0_ + 1.0) + box(-4, -49.0, ez0_, 4, -45.0, ez0_ + 1.0)
    encl = encl + tabs_
    cover = box(-32, -50, ez0_ - 1.0, 32, 50, ez0_) - cyl('z', (0, 0), 14.0, ez0_ - 2, ez0_ + 1)
    csc_ = None
    for y_ in (-47.0, 47.0):
        c_ = cyl('z', (0, y_), 3.0, ez0_ - 1.0, ez0_ + 1.0) + cyl('z', (0, y_), 5.5, ez0_ - 1.0 - 1.8, ez0_ - 1.0)
        cover = cover - cyl('z', (0, y_), 3.0, ez0_ - 2, ez0_ + 0.1)
        encl = encl - cyl('z', (0, y_), 3.0, ez0_ - 0.1, ez0_ + 2)
        csc_ = c_ if csc_ is None else csc_ + c_
    sto_ = None; esc_ = None
    for sx_, sy_ in ((-24, -30), (24, -30), (-24, 30), (24, 30)):
        so_ = (cyl('z', (sx_, sy_), 7.14, ztop - 1.6, ztop) + cyl('z', (sx_, sy_), 7.9, ez1_, ztop - 1.6)) - cyl('z', (sx_, sy_), 4.0, ez1_ - 1, ztop + 1)
        sc6_ = cyl('z', (sx_, sy_), 4.0, ez1_ - 1.0, ez1_ + 3.5) + cyl('z', (sx_, sy_), 7.0, ez1_ - 1.0 - 2.4, ez1_ - 1.0)
        encl = encl - cyl('z', (sx_, sy_), 4.0, ez1_ - 2, ez1_ + 0.1)
        strap = strap - cyl('z', (sx_, sy_), 7.14, ztop - 2, ztop + 1)
        sto_ = so_ if sto_ is None else sto_ + so_
        esc_ = sc6_ if esc_ is None else esc_ + sc6_
    driver = box(-20, -42, ez0_ + 2.0, 20, 42, ez0_ + 27.0)
    for x_ in (-6.0, 6.0):
        for y0_, y1_ in ((42.0, 46.0), (-46.0, -42.0)):
            driver = driver + cyl('y', (x_, ez0_ + 14.0), 2.0, y0_, y1_)
    bush_ = ((cyl('z', (0, 0), 26.0, ez1_ - 1.0 - 1.0, ez1_ + 0.8) - cyl('z', (0, 0), 16.0, ez1_ - 4, ez1_ + 2)) - (cyl('z', (0, 0), 26.0, ez1_ - 1.0, ez1_) - cyl('z', (0, 0), 22.0, ez1_ - 1.0, ez1_))
             + (cyl('z', (0, 0), 18.0, ez0_ - 1.0 - 1.2, ez0_ + 1.0) - cyl('z', (0, 0), 6.0, ez0_ - 3, ez0_ + 2) - (cyl('z', (0, 0), 18.0, ez0_ - 1.0, ez0_) - cyl('z', (0, 0), 14.0, ez0_ - 1.0, ez0_))))
    # THE CANOPY'S BUSHING: no grip at the canopy (the cord's strain relief is the enclosure's); a flush turned grommet,
    # 6061 satin black anodised, Ø12 through the floor with a Ø16 x 1 flange inside, its bore Ø6.6, its face flush below
    cgrip_ = (cyl('z', (0, 0), 12.0, zc, zc + 3.0) + cyl('z', (0, 0), 16.0, zc + 3.0, zc + 4.0)) - cyl('z', (0, 0), 7.5 if tt_ else 6.6, zc - 1, zc + 5)
    canopy = canopy - cyl('z', (0, 0), 12.0, zc - 1, zc + 4)
    xtra_ = {}
    if tt_:
        # V10 (the coordinator's T1 of 2026-11-25, the skeptic's corrected T1c; the canopy-options check): the canopy kept at
        # 150 x 50 with the cord on the center. Drawn on the x axis (the cables' line), heights above the canopy's underside
        # (zc), then turned by a0_ with the rest.
        # THE DRIVER, ERP ESS010W-0180-42-XL, stood on edge in a 1.0 steel tray beside the axis: its base (84 x 40) on the
        # tray's outer wall (x -34), 25.2 deep in x, 40 tall, y -51 to 33 (end gaps 6 and 7). ERP's outline (datasheet p.11
        # fig. 7, read third-angle, not mirrored): two Ø3.2 holes 77 x 33 apart in diagonal corner pockets, tabs 1.8 thick at
        # the base; the leads low at the base (x -31.5): the input (mains) at the +y end at z 15.4/17.6, the LED output at
        # the -y end at z 31.0/33.1, the dimming leads beside them, CUT AT THE FACTORY (phase-cut only; ERP p.9 allows it).
        # The tabs on two PEM FH-M3-6 flush-head studs pressed into the outer wall from outside (flush there, so nothing
        # stands toward the gripper bracket), M3 serrated nuts in ERP's pockets.
        # THE TRAY (it and the plate are the mains' enclosure): two parts, both 1.0 zinc-plated steel: the outer wall (with
        # a flange at its top, y -52 to -40, on a PEM FH-M3-8 stud in the plate) and a U (bottom, inner wall, two ends, with
        # a flange off its +y end on a second stud), joined at its ends by two M3 x 6 serrated button screws into PEM S-M3-1
        # nuts on flanges inside the outer wall, so both parts are bonded. Its rim closes on the plate's underside (0 gap,
        # nothing over 1.6 open, UL 1598 6.17.2.4). The 120 V input leads stay inside it and go up through a rolled Ø8
        # opening in the plate at (-21, 36.5) into the outlet box, where they are spliced to the supply (150 or more of the
        # 300 leads in the box, UL 1598 6.15.1.6). The LED leads leave through a 1/4 in snap bushing in its -y end at
        # (x -29, z 32), outside the tray: the tray is the barrier between the mains and the Class 2 wiring (6.17.2).
        # THE CORD up the axis from the floor's flush grommet, held by a two-screw steel saddle (screwdriver only, UL 1598
        # 5.2.1) against a stiff 1.6 steel channel hung from the plate on two PEM FH-M3-8 studs, its jacket ending 4 above the
        # saddle (z 19); its two conductors to two WAGO 221-412 lever splices (one per pole) held in a WAGO 221-500 mounting
        # carrier riveted to the channel (the splices' fixed place), with the LED leads from below.
        def _lead(pts, r=1.2):
            sh = None
            for k in range(len(pts) - 1):
                a_w, b_w = V3(*pts[k]), V3(*pts[k + 1]); u_w = (b_w - a_w).normalized()   # rods lapped at the bends (spheres failed in OCC)
                sg = _rod(a_w - u_w * (0.9 * r if k else 0.0), b_w + u_w * (0.9 * r if k < len(pts) - 2 else 0.0), r)
                sh = sg if sh is None else sh + sg
            return sh
        H_ = lambda h: zc + h
        zp_ = ztop - 1.6                                # the plate's underside (z 48.4)
        rr0_ = cnd / 2 - 3.0 - 0.2
        strap = (cyl('z', (0, 0), 2 * rr0_, zp_, ztop) + (cyl('z', (0, 0), 2 * rr0_, ztop - 12.0, ztop) - cyl('z', (0, 0), 2 * rr0_ - 3.2, ztop - 13, ztop + 1)))
        for y_ in (-44.45, 44.45):                  # V11-8: 4 in boxes only: slots 4.3 wide, an 8-32 centering from r 42 to 46.5
            sg_ = math.copysign(1.0, y_)
            strap = (strap - cyl('z', (0, sg_ * 42.0), 4.3, ztop - 2, ztop + 1) - cyl('z', (0, sg_ * 46.5), 4.3, ztop - 2, ztop + 1)
                     - box(-2.15, min(sg_ * 42.0, sg_ * 46.5), ztop - 2, 2.15, max(sg_ * 42.0, sg_ * 46.5), ztop + 1))
        # the input leads' opening, its edge rolled up 1.6 into the box
        op_ = (-21.0, 36.5)
        strap = strap + (cyl('z', op_, 11.2, ztop, ztop + 1.6) - cyl('z', op_, 8.0, ztop - 1, ztop + 2))
        strap = strap - cyl('z', op_, 8.0, ztop - 2, ztop + 2)
        # the green grounding screw on the plate's top face, inside the box's opening (UL 1598 6.14.2.2): 10-32 x 3/8 hex
        # washer head, a cupped washer (6.14.2.9(d)), into a downward-extruded tapped hole (Ø6.4 x 1.2 below the sheet: 2.8
        # of thread, about 3.5 threads), tapped after plating; its tip 7.1 under the plate, in free space
        gs_ = (30.0, 0.0)                               # V11: moved clear of the clamp's top flange
        strap = strap + (cyl('z', gs_, 6.4, zp_ - 1.2, zp_) - cyl('z', gs_, 4.83, zp_ - 3, ztop + 1))
        strap = strap - cyl('z', gs_, 4.83, zp_ - 3, ztop + 1)
        gsc_ = (cyl('z', gs_, 4.83, ztop + 0.8 - 9.5, ztop + 0.8) + cyl('z', gs_, 11.0, ztop, ztop + 0.8)
                + cyl('z', gs_, 9.5, ztop + 0.8, ztop + 3.2))
        # the studs in the plate (PEM FH-M3-8: flush on top, 6.4 below it) and their nylon-insert nuts (4 tall)
        studs_ = None
        for sx_, sy_ in ((-39.0, -46.0), (-21.0, 46.3), (1.0, 24.5), (16.0, 24.5)):     # V11: the U's stud 5.8 from the opening; the channel's
            s_ = cyl('z', (sx_, sy_), 3.0, ztop - 8.0, ztop) + (cyl('z', (sx_, sy_), 7.1, zp_ - 1.0 - (0.6 if sx_ > 0 else 0.0) - 4.0,
                                                                   zp_ - 1.0 - (0.6 if sx_ > 0 else 0.0)) - cyl('z', (sx_, sy_), 3.0, zp_ - 9, zp_))
            strap = strap - cyl('z', (sx_, sy_), 3.0, ztop - 2, ztop + 1)
            studs_ = s_ if studs_ is None else studs_ + s_
        # THE TRAY (V11-4): x -35 to -7, y -58 to 41, z 6.4 to 48.4. The outer wall's ends folded round the U's end walls
        # (y -59 and 42), each joined to it by an M3 x 6 serrated button screw along y into a PEM S-M3-1 nut in the U's end
        # wall, in the end gaps beside the driver: the two parts bonded
        tz0_, tz1_ = H_(6.4), zp_
        twall = (box(-35, -59, tz0_, -34, 42, tz1_) + box(-43, -52, tz1_ - 1.0, -35, -40, tz1_)
                 + box(-34, -59, tz0_, -18, -58, H_(24.0)) + box(-34, 41, tz0_, -18, 42, H_(30.0)))
        twall = twall - cyl('z', (-39.0, -46.0), 3.4, tz1_ - 2, tz1_ + 1)
        tu = (box(-34, -58, tz0_, -7, 41, tz0_ + 1.0) + box(-8, -58, tz0_ + 1.0, -7, 41, tz1_)
              + box(-34, -58, tz0_ + 1.0, -8, -57, tz1_) + box(-34, 40, tz0_ + 1.0, -8, 41, tz1_)
              + box(-27, 41, tz1_ - 1.0, -15, 51, tz1_))
        tu = tu - cyl('z', (-21.0, 46.3), 3.4, tz1_ - 2, tz1_ + 1)
        tsc_ = None
        for sg_, yo_ in ((-1.0, -59.0), (1.0, 42.0)):
            yi_ = yo_ - sg_ * 2.0                        # the U's end wall's inner face
            ax_ = (-26.0, H_(15.0))
            twall = twall - cyl('y', ax_, 3.4, min(yo_, yo_ - sg_ * 1.5), max(yo_, yo_ - sg_ * 1.5))
            tu = tu - cyl('y', ax_, 4.22, min(yi_, yi_ + sg_ * 1.5), max(yi_, yi_ + sg_ * 1.5))
            y_h0_, y_h1_ = sorted((yo_, yo_ + sg_ * 1.65)); y_s0_, y_s1_ = sorted((yo_, yo_ - sg_ * 6.0))
            y_n0_, y_n1_ = sorted((yi_, yi_ - sg_ * 1.5))
            sc_t = (cyl('y', ax_, 3.0, y_s0_, y_s1_) + cyl('y', ax_, 5.7, y_h0_, y_h1_)
                    + (cyl('y', ax_, 6.35, y_n0_, y_n1_) - cyl('y', ax_, 3.0, y_n0_ - 1, y_n1_ + 1)))
            tsc_ = sc_t if tsc_ is None else tsc_ + sc_t
        # THE DRIVER (on edge), V11-2: ERP p.11 fig. 7's holes, 77 x 33 apart and 3.5 in from the case's ends and sides, at
        # (y 29.5, z 44.4) and (-47.5, 11.4); its two pockets alike, 7 x 7.5 to the step. Fixed by two M3 x 8 button screws
        # (ISO 7380) from outside the wall (Ø3.4 clearance) through the tabs, a DIN 433 washer (Ø6 x 0.5) and a plain M3 nut
        # (ISO 4032, 5.5 AF x 2.4) in each pocket: no serrations on ERP's plastic tabs
        dx0_, dx1_, dy0_, dy1_, dz0_, dz1_ = -34.0, -8.8, -51.0, 33.0, H_(7.9), H_(47.9)
        driver = box(dx0_, dy0_, dz0_, dx1_, dy1_, dz1_)
        driver = driver - box(-32.2, 26.0, H_(40.4), dx1_ + 1, dy1_ + 1, dz1_ + 1) - box(-32.2, dy0_ - 1, dz0_ - 1, dx1_ + 1, -44.0, H_(15.4))
        dscr_ = None
        for hy_, hz_ in ((29.5, 44.4), (-47.5, 11.4)):
            driver = driver - cyl('x', (hy_, H_(hz_)), 3.2, -35, -30)
            twall = twall - cyl('x', (hy_, H_(hz_)), 3.4, -36, -33)
            s_ = (cyl('x', (hy_, H_(hz_)), 3.0, -35, -27.0) + cyl('x', (hy_, H_(hz_)), 5.7, -36.65, -35.0)
                  + (cyl('x', (hy_, H_(hz_)), 6.0, -32.2, -31.7) - cyl('x', (hy_, H_(hz_)), 3.2, -33, -31))
                  + (cyl('x', (hy_, H_(hz_)), 6.35, -31.7, -29.3) - cyl('x', (hy_, H_(hz_)), 3.0, -32, -29)))
            dscr_ = s_ if dscr_ is None else dscr_ + s_
        # the input leads (mains): out of the +y end, up the 7 gap, through the plate's opening, 30 into the box (drawn)
        for k_, zl_ in enumerate((15.4, 17.6)):
            xo_ = op_[0] - 1.2 + 2.4 * k_
            driver = driver + _lead([(-31.5, dy1_ - 1.0, H_(zl_)), (-31.5, 36.5, H_(zl_)), (xo_, op_[1], H_(42.0)),
                                     (xo_, op_[1], ztop + 30.0)])
        # the LED leads (Class 2): out of the -y end through a smooth rolled edge (UL 1598 5.14.1(a): a Ø5 hole in the U's
        # end wall, its edge rolled out to a Ø7.5 lip), round the outside of the tray at y -61, then along y at z 22.5 and
        # through the channel's window into the splices from below; cut at the factory to length
        tu = tu - cyl('y', (-29.0, H_(32.0)), 5.0, -59, -56)
        tu = tu + (cyl('y', (-29.0, H_(32.0)), 7.5, -59.5, -58.0) - cyl('y', (-29.0, H_(32.0)), 5.0, -60, -56))
        led_ = []
        for k_, (zl_, xe_) in enumerate(((31.0, 6.75), (33.1, 20.35))):
            xb_ = -30.1 + 2.2 * k_
            pts_ = [(-31.5, dy0_ + 1.0, H_(zl_)), (-31.5, -53.0, H_(zl_)), (xb_, -54.5, H_(32.0)), (xb_, -61.0, H_(32.0)),
                    (xe_, -60.2, H_(22.6)), (xe_, 8.7, H_(22.5)), (xe_, 8.7, H_(28.5))]    # (V11-14: off-axis corners, so each lead unions as one solid)
            driver = driver + _lead(pts_, r=1.0)
            led_.append(sum(math.dist(pts_[j], pts_[j + 1]) for j in range(len(pts_) - 1)))
        # THE CORD'S CLAMP (V11-1): a 1.6 steel channel hung from the plate on two PEM FH-M3-8 studs at (1, 24.5) and
        # (16, 24.5): the web across y (y 3 to 4.6, x -5 to 26, z 5 to the plate), side flanges bent +y (to y 13.8), a top
        # flange under the plate (to y 28.5). The cord runs up on the axis against the web's -y face and is held by two
        # one-hole steel straps (z 7 to 13 and 14 to 20), each on an M3 x 6 pan screw (ISO 7045) along y into a PEM S-M3-1
        # nut in the web, at x 8: driven from -y with the canopy tied down, 120 or more free. The straps are drawn at the
        # cord's surface, their feet 1.0 off the web: tightened, each foot and its tip stop on the web, the seat then 5.0
        # deep, so a 6.0 to 6.5 cord is squeezed 1.0 to 1.5 and no more (UL 1598 5.15.1.2)
        rb_ = (box(-5.0, 3.0, H_(5.0), 26.0, 4.6, zp_) + box(-5.0, 4.6, zp_ - 1.6, 26.0, 28.5, zp_)
               + box(-5.0, 4.6, H_(5.0), -3.4, 13.8, zp_ - 1.6) + box(24.4, 4.6, H_(5.0), 26.0, 13.8, zp_ - 1.6))
        # the window for the conductors and the LED leads (x -3 to 22, z 21 to 26.7), its top edge bent out +y as the
        # splices' ledge (z 26.7 to 28.3), with four notches under their entries
        rb_ = rb_ - box(-3.0, 2.0, H_(21.0), 22.0, 5.0, H_(26.7))
        rb_ = rb_ + box(-3.4, 4.6, H_(26.7), 24.4, 12.0, H_(28.3))
        for xe_ in (0.25, 6.75, 13.85, 20.35):
            rb_ = rb_ - box(xe_ - 2.0, 6.0, H_(26.0), xe_ + 2.0, 11.5, H_(29.0))
        for sx_ in (1.0, 16.0):
            rb_ = rb_ - cyl('z', (sx_, 24.5), 3.4, zp_ - 2, zp_ + 1)
        # (after V11, the coordinator 10:35) the LED leads' tie slots: two 1.0 x 3.0 slots in the ledge either side of each
        # lead's notch (x 3.0 to 4.0 and 9.8 to 10.8 for the - lead, 16.6 to 17.6 and 23.0 to 24.0 for the +), one tie
        # (Panduit PLT1M-C) round each lead through its pair; and the side flanges' dimples, Ø3 at (y 8.7, z 37), drawn to
        # touch the splices (0.35 and 0.75 tall), made 0.5 taller than that for the push fit
        for x0_ in (3.0, 9.8, 16.6, 23.0):
            rb_ = rb_ - box(x0_, 6.5, H_(26.0), x0_ + 1.0, 9.5, H_(29.0))
        rb_ = rb_ + cyl('x', (8.7, H_(37.0)), 3.0, -3.4, -3.05) + cyl('x', (8.7, H_(37.0)), 3.0, 23.65, 24.4)
        clamp_ = cscr_ = None
        for s0_, s1_ in ((7.0, 13.0), (14.0, 20.0)):
            z0s_, z1s_, zs_ = H_(s0_), H_(s1_), H_((s0_ + s1_) / 2)
            st_ = (cyl('z', (0, 0), 8.0, z0s_, z1s_) - cyl('z', (0, 0), 6.0, z0s_ - 1, z1s_ + 1)) - box(-5, 0, z0s_ - 1, 5, 5, z1s_ + 1)
            st_ = st_ + box(3.0, 0.0, z0s_, 4.0, 1.0, z1s_) + box(3.0, 1.0, z0s_, 12.0, 2.0, z1s_) + box(-4.0, 0.0, z0s_, -3.0, 2.0, z1s_)
            st_ = st_ - cyl('y', (8.0, zs_), 3.4, 0.5, 2.5)
            rb_ = rb_ - cyl('y', (8.0, zs_), 4.22, 2.9, 4.7)
            sc_c = cyl('y', (8.0, zs_), 3.0, 1.0, 7.0) + cyl('y', (8.0, zs_), 5.6, -1.4, 1.0)
            rb_ = rb_ + (cyl('y', (8.0, zs_), 6.35, 4.6, 6.1) - cyl('y', (8.0, zs_), 3.0, 4.5, 6.5))      # the PEM S-M3-1 nut, in the channel's part
            clamp_ = st_ if clamp_ is None else clamp_ + st_
            cscr_ = sc_c if cscr_ is None else cscr_ + sc_c
        # the splices: two WAGO 221-412 (18.3 x 13.1 x 8.2; lever open 15.3), standing in the channel's pocket, entries down
        # on the ledge, levers facing +y (open into free space): located by the web, the ledge and the top flange, and held
        # by a push fit between the side flanges, each dimpled 0.5 inward at mid-height (the dimples not drawn; nothing in
        # the levers' swing). A: the - pole (x -3.05 to 10.05), B: the + pole (10.55 to 23.65)
        spl_ = box(-3.05, 4.6, H_(28.5), 10.05, 12.8, H_(46.8)) + box(10.55, 4.6, H_(28.5), 23.65, 12.8, H_(46.8))
        # the cord's two conductors from the jacket's end (z 24, 4 above the upper strap) through the window into A and B
        cond_ = None
        for sx_, xe_ in ((-1.4, 0.25), (1.4, 13.85)):
            c_ = _lead([(sx_, 0.0, H_(24.0)), (sx_, 0.0, H_(25.0)), (xe_, 8.7, H_(25.5)), (xe_, 8.7, H_(28.5))], r=1.0)
            cond_ = c_ if cond_ is None else cond_ + c_
        studs_ = studs_ + dscr_
        xtra_ = dict(twall=twall, tu=tu, tsc=tsc_, studs=studs_, rb=rb_, clamp=clamp_, cscr=cscr_, spl=spl_, cond=cond_, led=led_)
        encl = cover = csc_ = sto_ = esc_ = bush_ = None
    rot_ = (lambda sh: at(a0_, sh) if sh is not None else None) if a0_ else (lambda sh: sh)
    strap, bscr_, gsc_, encl, cover, csc_, sto_, esc_, driver, bush_ = (rot_(x) for x in (strap, bscr_, gsc_, encl, cover, csc_, sto_, esc_, driver, bush_))
    setsc_ = rot_(setsc_)
    for a_ in (90.0, 270.0):
        canopy = canopy - rot_(at(a_, cyl('x', (0, ztop - 6.0), 4.0, rr0_ - 0.1, cnd / 2 + 1)))
    if tt_:
        strap = strap - rivets
    cnuts_ = None
    if tt_:
        # V10: the cord up the axis through the floor's grommet and the clamp, its jacket ending at z 24, its conductors on
        xtra_ = dict((n_, (rot_(sh_) if n_ != 'led' else sh_)) for n_, sh_ in xtra_.items())
        cord = cord + cyl('z', (0, 0), 6.0, zc, zc + 24.0) + xtra_['cond']
    parts_ = cover_parts(p) + [
        Part('hub', core, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=[('aluminium 6061, black anodised: the core, turned from bar, solid; the stem bonded and pinned in a Ø16.1 socket '
                     '25 deep from below, the wires up it; the PEEK ring round it, the crown on its neck (metal to metal, a film of '
                     'thermal compound, no pad); the white disc under it') if ring_ else
                    ('aluminium 6061, black anodised: the core, turned from bar. The COB on its holder at the top of the 46 '
                     'bore (22 up: the cut-off, about 46 deg from the vertical), the reflector in the bore, the PEEK ring '
                     'round it, the crown on its neck (metal to metal, a film of thermal compound, no pad); a 10 bore for the wires')]),
        Part('ring', ring, Machined('peek', 'lathe'), finish='trim', group='fixture', inside=True,
             notes=['PEEK, unfilled (0.25 W/m K), black: the thermal break. It carries the three pins and ' + ('the lock\'s hole' if nlock_ else 'the detent') + ', so '
                    'the cover touches the fixture only through it. Review 2026-11-01: its 81.6 OD is the centering land '
                    'in the collar\'s 82 bore (0.2 diametral), three Ø3.2 clearance holes for the pins\' threads']),
        Part('pins', pins, Bought('dome-pins'), finish='anodised', group='fixture',
             notes=[('v8: the bayonet keyed: the pin at 30 deg has a Ø6 shoulder and its slot is 7 wide, so the shade fits one way only. ' if p.get('fixings') else '') + 'stainless shouldered pins: Ø4 shoulder 4.2 long, M3 thread 15.8, screwed through the PEEK into the '
                    'hub (6 of thread in the aluminium, a pre-applied nylon patch, no anaerobic locker); 4.0 of engagement in the '
                    'collar\'s slots']),
    ] + ([
        Part('carrier', carrier, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=['option 3 (2026-11-10): aluminium 6061, black anodised, Ø56 x 4.5, its underside on the rim plane; '
                    'the board in a Ø50.2 pocket 1.8 deep in its top, so the LEDs\' faces sit 4.9 above the rim plane']),
        Part('board', board + leds, Bought('hemi-ring-board'), finish='led', group='fixture',
             notes=['24 mid-power LEDs on a Ø38 circle, facing up, two strings of 12 at about 90 mA: about 1,000 lm '
                    '[check the datasheet]. Without a lens until a stock side-emitting ring optic with an IES file is '
                    'named. Heat test needed: the hub about 6 K warmer than today (estimate)']),
        Part('stem', stem, Machined('aluminium', 'tube'), finish='anodised', group='fixture',
             notes=['16/12 aluminium tube, black anodised, from the carrier up into the hub\'s socket, bonded and '
                    'cross-pinned; the wires up its bore; a heat pipe inside it optional (about 2.5 W of heat)']),
        Part('white-disc', wdisc, Machined('aluminium', 'laser'), finish='white', group='fixture',
             notes=[('a white Ø62 x 1 disc under the hub, its edge eased 0.5 (white powder coat), with the collar\'s white lip '
                     '(Ø95 seen, bore Ø65) round it: review 2, 2026-11-24 (the Ø95 disc of 2026-11-11 trapped the shade: '
                     'top_check.py); the collar\'s flange face inside painted white' if p.get('white_split') else
                     'a white Ø95 x 1 disc under the hub (Ø80 until 2026-11-11: Ø95 hides the collar\'s slots and seams from below) (white powder coat), and the collar\'s flange face inside painted '
                    'white') + ': the crown\'s inside white, so the light the shade sends back up returns down']),
    ] if ring_ else [
        Part('reflector', refl, Bought('north-reflector'), finish='anodised', group='fixture', inside=True),
        Part('cob', cob, Bought('hemi-cob'), finish='led', group='fixture', inside=True),
    ]) + [
        Part('crown', crown, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=[('PROPOSAL (' + (('even tiers, ' + p['top']) if p.get('top') else 'today\'s top, check 3\'s fixings') + '): ' + ', '.join(f'{d:.0f} across from {a:.2f} to {b:.2f}' for d, a, b in tt_['crown'])
                     + '; on the hub\'s neck metal to metal (a film of thermal compound, no pad), its 2.5 floor held by three M2.5 countersunk into the neck, a Ø24 pocket for '
                     'the cord grip and its socket, two Ø2.4 bores for the suspension cables (1/16 in, 1.59)' if tt_ else
                     'the heat sink (round 41; the fins until then), round 32f\'s low top: 80 across, 11.5 tall over the '
                    'collar') + ', turned from 6061 bar, black anodised (emissivity about 0.85: half its loss is radiation), on '
                    'the core\'s neck ' + ('metal to metal' if tt_ else 'on a thermal pad') + ', 0.5 clear of the PEEK ring and the collar']),
        Part('gland', gland, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=[(f'PROPOSAL ({("even tiers, " + p["top"]) if p.get("top") else "today, check 3"}): the cap, {tt_["gland"][0]:.0f} across x {tt_["gland"][2] - tt_["gland"][1]:.1f}, set on the '
                     'crown, resting there by its weight, held by a magnet (hemi-cap-key; today\'s and A\'s keyed by a dowel and the swap\'s handle, B\'s not), the cord through its 1.0 lid (no screws, no thread), '
                     'its Ø20 pocket over the cord grip\'s dome nut' if tt_ else
                     'the cap, 40 x 14, over the listed cord grip (the strain relief, tested with the fixture\'s weight), on two M3 into the crown') +
                    ': 6061, turned, edges eased 1.0, SATIN black anodised; part of the heat sink']),
    ] + ([Part('grip', grip, Bought('hemi-cord-grip'), finish='cord', group='fixture', inside=True,
               notes=['PROPOSAL (check 3): Lapp 53112005, M12 x 1.5 nickel-plated brass cable gland, cord 3.5 to 7, 16 across the '
                      'flats, 32.5 overall, 12 of thread (DB53112005EN as the reviewer read it; to confirm): through the crown\'s '
                      'floor into the hub, tapped 13 deep; tightened with a thin-wall 16 socket down the crown\'s Ø24 pocket']),
           Part('crown-screws', sc_, Bought('hemi-crown-screws'), finish='steel', group='fixture', inside=True,
                notes=['PROPOSAL (v5): three M2.5 x 8 countersunk screws (ISO 10642), stainless, through the crown\'s 2.5 floor at r 9.25, '
                       '90/210/330 deg, into the hub\'s neck (tapped 6): the crown keyed and held, metal to metal']),
           Part('cap-key', keys, Bought('hemi-cap-key'), finish='steel', group='fixture', inside=True,
                notes=[('PROPOSAL (v6): a Ø2 x 5 stainless dowel (the cap\'s key) and a Ø2 x 2 N42 magnet in the crown\'s top over a '
                        'Ø2 x 0.5 steel disc bonded in the cap (its hold-down), at r 15.5, 2.5 from the crown\'s pocket') if tt_.get('key', 1)
                       else ('PROPOSAL (v6): B\'s Ø32 cap held by a Ø1.5 x 2 N42 magnet in the crown\'s top over a Ø1.5 x 0.5 steel '
                             'disc in the cap, at r 14 (1.25 from the pocket and the fillet); no dowel: B\'s handle in a swap is its Ø56 tier')]),
           Part('grippers', grippers + safety, Bought('hemi-gripper'), finish='steel', group='canopy', inside=True,
                notes=['PROPOSAL (v7): two Cable Grippers MGR-M10-MM, plunger down, each with its knurled safety nut (loosen to '
                       'adjust, tighten when level), threaded up through its bracket\'s foot']),
           Part('gripper-nuts', gnuts, Bought('hemi-gripper-nut'), finish='steel', group='canopy', inside=True,
                notes=['v7: two M10 nylon-insert nuts (ISO 10511), 16 AF, 8 tall, on the brackets\' feet']),
           Part('gripper-brackets', brackets, Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
                notes=['PROPOSAL (v8): two 1.6 zinc-plated steel U brackets, each a foot with an M10 clearance hole, two legs across the '
                       'cables\' line and two flanges turned outward under the plate, held by four PEM FH-M3-8 studs pressed into the plate '
                       'and M3 nylon-insert nuts']),
           Part('bracket-studs', rivets, Bought('hemi-bracket-studs'), finish='steel', group='canopy', inside=True),
           Part('canopy-screws', setsc_, Bought('hemi-canopy-setscrews'), finish='anodised', group='canopy', inside=True,
                notes=['V10: two M4 x 3 cup-point set screws (ISO 4029), black oxide, nylon patch, through the canopy\'s 3.0 wall at 90/270 '
                       'deg (tapped after anodizing), their cups on the plate\'s bare rim, 0.2 under the wall\'s face']),
           Part('box-screws', bscr_, Bought('hemi-box-screws'), finish='steel', group='canopy', inside=True,
                notes=['the outlet box\'s two 8-32 screws (supplied with the box), through the plate\'s two slots'])]
         if tt_ else []) + [
        Part('cord', cord, Bought('hemi-cord'), finish='cord', group='fixture'),
        # review 2 (2026-11-24, (8)): the fixture (about 3.5 lb) hangs from the steel cable by default; the SPT-2 cord's
        # 2.5 lb (UL 153) carries current only
        Part('suspension', susp, Bought('hemi-suspension'), finish=('stainless' if tt_ else 'anodised'), group='fixture'),
        Part('canopy', canopy, Machined('aluminium', 'lathe'), finish='anodised', group='canopy',
             notes=[('150 x 50, 6061 turned, SATIN black anodized: open at the top against the ceiling, its 3 floor closed below '
                     'with a flush grommet in its center (the cord) and two Ø3 holes at r 48 (the cables); a cover only, held to the '
                     'mounting plate\'s rim by two flush M4 x 3 cup-point set screws in its wall; the plate carries the load') if tt_ else
                    ('150 x 50, 6061 turned, SATIN black anodised (2026-11-11, the bar: one hardware finish; was polished '
                     'black acrylic): a cover only (review 2026-11-01), screwed to the steel '
                     'strap, which carries the load; the driver and the splices are in the steel enclosure. The bar '
                     '(2026-11-11): the strap\'s screws black oxide, under the canopy\'s closed face, none in view; the cord '
                     'grip where the cord leaves the canopy a turned 6061 gland, satin black anodized, its nut flush')]),
    ] + ([
        Part('strap', strap, Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['the mounting plate, 1.6 zinc-plated steel, Ø143.6, its rim drawn down 12; it carries the load and closes the '
                    'driver\'s tray']),
        Part('tray-wall', xtra_['twall'], Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['V10: the driver tray\'s outer wall, 1.0 zinc-plated steel, 99 x 42 with a flange at its top on a plate stud; the '
                    'driver\'s two PEM FH-M3-6 studs pressed in from outside (flush there)']),
        Part('tray-u', xtra_['tu'], Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['V10: the driver tray\'s U (bottom, inner wall, ends), 1.0 zinc-plated steel, a flange off its +y end on a plate '
                    'stud, two joint flanges with PEM S-M3-1 nuts inside the outer wall; the 1/4 in snap bushing in its -y end']),
        Part('tray-screws', xtra_['tsc'], Bought('hemi-tray-screws'), finish='steel', group='canopy', inside=True),
        Part('canopy-studs', xtra_['studs'], Bought('hemi-canopy-studs'), finish='steel', group='canopy', inside=True),
        Part('driver', driver, Bought('north-driver-ring' if ring_ else 'north-driver-575'), finish='steel', group='canopy', inside=True, render=False),
        Part('relief-bracket', xtra_['rb'], Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['V10: the cord clamp\'s channel, 1.6 zinc-plated steel: web 28 x 40.4, side flanges 7.4, a top flange to x 20 on '
                    'two plate studs; two PEM S-M3-1 nuts for the saddle\'s screws; the splices\' carrier riveted to its web']),
        Part('cord-clamp', xtra_['clamp'], Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['V11: the cord\'s two straps, 1.0 zinc-plated spring steel, each a one-hole strap 6 tall round the cord\'s -y side, '
                    'its edges rolled, its foot and tip stopping on the channel\'s web (the squeeze 1.0 to 1.5 on a 6.0 to 6.5 cord)']),
        Part('clamp-screws', xtra_['cscr'], Bought('hemi-clamp-screws'), finish='steel', group='canopy', inside=True),
        Part('splices', xtra_['spl'], Bought('hemi-splice'), finish='trim', group='canopy', inside=True, render=False),
        Part('canopy-bushing', cgrip_, Machined('aluminium', 'lathe'), finish='anodised', group='canopy',
             notes=['V11: the canopy\'s flush grommet, 6061 turned, satin black anodized: Ø12.0 p6 through the 3 floor (pressed into its '
                    'Ø12.0 H7 hole and bonded, Loctite 638), a Ø16 x 1 flange inside, its bore Ø7.5 with R 1.0 at both ends; it does '
                    'not grip (the cord slides 10 to 15 cm through it; its strain relief is the clamp on the plate)']),
        Part('ground-screw', gsc_, Bought('hemi-ground-screw'), finish='steel', group='canopy', inside=True,
             notes=['V11: a green 10-32 x 3/8 in hex-washer-head grounding screw with a cupped washer (UL 467; UL 1598 6.14.2.9(d)) '
                    'on the plate\'s top face at (30, 0), inside the outlet box\'s opening where the supply connects (6.14.2.2; NEC '
                    '410.46), into a downward-extruded hole tapped after plating (about 2 to 2.5 full threads: a first-article test, '
                    '17.39 at 1.6 N m); the tray, the clamp\'s channel and the gripper brackets bond through their studs\' serrated '
                    'flange nuts (DIN 6923), the tray\'s two parts through their serrated joint screws, the canopy through its cup-point '
                    'set screws on the bare rim (the 18.2 bonding test on the prototype)'])]
         if tt_ else [
        Part('strap', strap, Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['v9: the mounting plate, 1.6 zinc-plated steel, Ø143.6, its rim turned down 12; it carries the load (hemi-canopy-strap)']),
        Part('enclosure', encl, Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['v9: the driver\'s enclosure, 1.0 zinc-plated steel, 64 x 100 x 38, open below, two tabs bent in at its ends for '
                    'its cover\'s screws; on four PEM standoffs under the plate; free volume 7.9 in3 (NEC 314.16: 6.0 for the supply\'s '
                    'three 14 AWG conductors)']),
        Part('enclosure-cover', cover, Machined('steel-sheet-formed', 'formed'), finish='steel', group='canopy', inside=True,
             notes=['v9: the enclosure\'s removable cover, 1.0 zinc-plated steel, 64 x 100, two M3 x 4 screws into its end tabs; the '
                    'Class 2 cord\'s strain-relief bushing in its centre']),
        Part('cover-screws', csc_, Bought('hemi-enclosure-screws'), finish='steel', group='canopy', inside=True),
        Part('driver', driver, Bought('north-driver-ring' if ring_ else 'north-driver-575'), finish='steel', group='canopy', inside=True, render=False),   # round 36: 575 lm
        # v8 (the v7 check's (4), (10)): the enclosure's standoffs and screws, the bushings, the canopy's cord grip, grounding
        Part('plate-standoffs', sto_, Bought('hemi-plate-standoffs'), finish='steel', group='canopy', inside=True),
        Part('enclosure-screws', esc_, Bought('hemi-enclosure-screws'), finish='steel', group='canopy', inside=True),
        Part('bushings', bush_, Bought('hemi-bushings'), finish='trim', group='canopy', inside=True,
             notes=['v8: a snap bushing in the enclosure\'s top for the supply (Ø22 hole) and a strain-relief bushing in its floor '
                    'for the Class 2 cord (Ø14 hole)']),
        Part('canopy-bushing', cgrip_, Bought('hemi-canopy-bushing'), finish='anodised', group='canopy',
             notes=['v9: a flush grommet in the canopy\'s floor (no grip here: the cord\'s strain relief is the enclosure\'s)']),
        Part('ground-screw', gsc_, Bought('hemi-ground-screw'), finish='steel', group='canopy', inside=True,
             notes=['v9: a green 10-32 x 3/16 grounding screw (UL 467) into the plate\'s downward-extruded tapped hole at y +56 (five '
                    'threads; tight, its tip 0.8 above the plate); the equipment grounding conductor lands under its head (NEC '
                    '410.44); the enclosure bonds through its serrated screws and standoffs, the canopy through its cup-point set '
                    'screws, tapped after anodising, onto the plate\'s bare rim']),
    ]) + [
        Part('plunger', plunger_, Bought('dome-plunger'), finish='steel', group='fixture', inside=True,
             notes=['v7: an M5 x 12 stainless ball spring plunger (light force, about 10 N), radially through the PEEK ring at 90 deg, '
                    'z 93, screwed into the ring before the ring slides down over the hub (a groove in the hub takes its end); its '
                    'ball clicks into a dimple in the collar\'s bore when the shade is seated']) if plunger_ is not None else
        (Part('plunger', None, Bought('dome-plunger')) if not nlock_ else None),
    ] + [
        Part('listing', None, Bought('moon-listing')),
    ]
    if tt_:
        # v7 (the v6 check's (11)): the threads and holes as the shop makes them (the STEP files draw every thread at its
        # major Ø, so the fixings touch and never overlap)
        crq_ = tt_.get('cable_r', GRIP['cable_r'])
        lk6_ = tt_.get('lock')
        kk_ = tt_['key'] if 'key' in tt_ else GRIP['key']
        mm_ = tt_.get('magnet', GRIP['magnet'])
        DZ_ = (f'DATUM: z is the height above the shade\'s rim plane (the lamp\'s z 0); angles counter-clockwise seen from above from the hub\'s 0 deg '
               f'(the key pin at 30, the cables at {cang_[0]:g}/{cang_[1]:g}). ')
        DC_ = ('DATUM: the canopy\'s axis; z is the height above the canopy\'s underside; x along the cables\' line, y across. '
               + ('Drawn square: in the lamp it sits turned ' + f'{a0_:g}' + ' deg with the cables. ' if a0_ else ''))
        SM_ = ('SHEET METAL: deburr and break every edge 0.2; inside bend radii R 1.0 on 1.0 sheet and R 1.6 on 1.6 sheet; zinc '
               'plated after forming; hole positions to each other ±0.1 where paired, else ±0.2. ')
        TH_ = {
            'hub': DZ_ + f'FACES: its bottom face at z 60 (the hub\'s own datum: z 93 is 33 above it). THREADS AND HOLES: M12 x 1.5 '
                   f'tapped 13 deep from the neck\'s top (drill 10.5); 3 x M2.5 tapped 6 deep at r 9.25, 90/210/330 deg (drill 2.05 x 7.5); '
                   f'radial at z 93 for the pins: 2 x M3 at 150/270 deg (drill 2.5 x 7.5) and 1 x M4 at 30 deg for the key pin (drill 3.3 '
                   f'x 7.5), each tapped 6; 2 x Ø5.6 x 8 counterbores in the bottom face at r {crq_:g}, {cang_[0]:g}/{cang_[1]:g} deg, then '
                   f'Ø2.4 through to the neck\'s top'
                   + ('' if lk6_ else '; a groove 5.4 wide at 90 deg, r 28.3 to 31, from z 90.3 open to the hub\'s top (the detent plunger\'s end)'),
            'ring': DZ_ + 'FACES: z 86 to 100, its bottom face at z 86 (the pins\' holes 7 above it); its OD Ø81.6 the land in the '
                    'collar\'s Ø82 bore (0.4 diametral). '
                    + (('THREADS AND HOLES: Ø6.4 at z 96.0, 105 deg, to r 36.0 (the lock\'s pin), no edge break; through at z 93: 2 x Ø3.2 '
                        '(the pins, 150/270 deg) and 1 x Ø4.3 (the key pin, 30 deg)') if lk6_ else
                       ('THREADS AND HOLES: M5 tapped through at z 93, 90 deg (drill 4.2; the detent plunger, Kipp K0310.05: its body flush '
                        'with the land to 0.1 under; more than 0.2 proud, its body scrapes the collar\'s bore); through at z 93: 2 x Ø3.2 '
                        '(the pins, 150/270 deg) and 1 x Ø4.3 (the key pin, 30 deg)'))
                    + '. LEAD-IN DOWN: laser-mark UP on its top face; fitted flipped, it still takes the pins but its '
                    + ('lock hole lands at 315 deg, z 90, and the lock never engages' if lk6_ else 'plunger hole lands at 330 deg and will not pass the hub\'s groove'),
            'collar': DZ_ + ('' if tt_.get('top') else 'FACES: its top face at z 100. ')
                      + 'THREADS AND HOLES: three L-slots from inside, 5 wide, to r 45.5 (Ø91) deep, mirrored so the shade goes on clockwise '
                        'seen from below: each notch at 30/150/270 deg, its entry 30 deg past it at 60/180/300; the key\'s (notch 30, entry '
                        '60) 7 wide, its turn passage z 81.25 to 88.75 and its notch z 81.25 to 96.5 (the others: 82.5 to 87.5 and 82.5 to 95.5)'
                      + ('; M10 x 1 tapped through the wall at z 96.5, 105 deg (drill 9.0; the lock)' if lk6_ else
                         '; a Ø3.1 dimple at 90 deg, a short vertical slot z 93.0 to 93.5, 0.7 deep (the detent, for a Ø3 ball)')
                      + ('; M96 x 1.5 outside, 6g, run out into a DIN 76 undercut' if tt_.get('top') else
                         '; M96 x 1.5 outside, 6g; ONE-WAY MARK: a radial groove 0.4 wide, 0.2 deep across its 0.9 x 45 outer chamfer at 60 deg '
                         '(the keyed entry), cut before anodizing so it is black')
                      + '. BALANCE: the finished shade\'s center within 0.3 of its axis, checked on a two-point stand',
            'clamp': DZ_ + 'THREAD: M96 x 1.5, 6H' + (', its start clocked to the collar\'s, so screwed down to the collar\'s shoulder it lands '
                                                    'at one angle' if tt_.get('top') else ', tightened to the shade maker\'s torque')
                     + ('. HOLES: Ø10.5 at z 96.5, 105 deg, and a Ø20 spot face for the lock\'s nut, machined before anodizing' if lk6_ else '')
                     + ('. ONE-WAY MARK: a vertical groove 0.4 wide, 0.2 deep, 5 long on its side at 60 deg (over the keyed entry), cut '
                        'before anodizing so it is black' if tt_.get('top') else ''),
            'crown': DZ_ + f'HOLES: 3 x Ø2.9 countersunk 90 deg (M2.5, ISO 10642) at r 9.25, 90/210/330 deg; 2 x Ø2.4 at r {crq_:g}, '
                     f'{cang_[0]:g}/{cang_[1]:g} deg, their top exits rounded; '
                     + (f'a Ø2 H7 x 3 hole for the dowel at r {kk_[0]:g}, {kk_[1]:g} deg and a Ø2 x 2 pocket for the magnet at r {mm_[0]:g}, {mm_[1]:g} deg'
                        if kk_ else f'a Ø{mm_[2]:g} x 2 pocket for the magnet at r {mm_[0]:g}, {mm_[1]:g} deg (no dowel)')
                     + '; ONE-WAY MARK: a vertical groove 0.4 wide, 0.2 deep, 5 long on its lowest tier\'s side at 30 deg (over the key '
                       'pin), cut before anodizing so it is black',
            'gland': DZ_ + f'HOLES: Ø{GRIP["cap_pocket"]:g} pocket from below to the {GRIP["lid"]:g} lid, Ø8 through the lid (the cord); '
                     + (f'2 x Ø2.4 through at r {crq_:g}, {cang_[0]:g}/{cang_[1]:g} deg, their top exits rounded; ' if (tt_['gland'][0] / 2 > crq_ + 2.0) else '')
                     + (f'a Ø2.05 x 2 hole for the dowel at r {kk_[0]:g}, {kk_[1]:g} deg; ' if kk_ else '')
                     + f'a Ø{mm_[2]:g} x 0.5 pocket for the steel disc at r {mm_[0]:g}, {mm_[1]:g} deg',
            'canopy': DC_ + 'HOLES: Ø12.0 H7 in the floor\'s center (the grommet, pressed and bonded); 2 x Ø3 at r 48, 0/180 deg (the cables); '
                      '2 x M4 tapped through the wall at z 44, 90/270 deg, TAPPED AFTER ANODIZING (their threads and cups bond it to the '
                      'plate). FITS: the bore Ø144.0 +0.1/0 (wall 3.0, floor 3.0, 50 overall), a 1.0 x 30 deg lead-in at its top edge; the '
                      'plate\'s Ø143.6 0/-0.2 in it (0.4 to 0.7 diametral)',
            'canopy-bushing': DC_ + 'Ø12.0 p6 x 3 body, Ø16 x 1 flange, bore Ø7.5 with R 1.0 at both ends; 6061, satin black anodized',
            'strap': DC_ + SM_ + 'The plate 1.6, z 48.4 to 50, Ø143.6 0/-0.2, its rim drawn down 12 on a press (inside R 2). HOLES (x, y): 2 '
                     'slots 4.3 wide on the y axis, centers from y -+42 to -+46.5 (a 4 in box\'s 8-32 screws, 3-1/2 in apart); Ø8 at (-21, '
                     '36.5), its edge rolled up 1.6, deburred (the driver\'s input leads into the box); 10-32 in an extruded hole at (30, 0), '
                     'Ø6.4 x 1.2 down, TAPPED AFTER PLATING (the green screw); 4 x Ø3.0 +0.08 for PEM FH-M3-8 at (-39, -46), (-21, 46.3) '
                     '(the tray; 5.8 from the Ø8), (1, 24.5), (16, 24.5) (the cord clamp; 15.0 ±0.05 apart); 8 x Ø3.0 +0.08 for PEM FH-M3-8 '
                     'at (-+43.5, -+29.3) and (-+52.5, -+29.3) (the gripper brackets; each bracket\'s four to each other ±0.05)',
            'tray-wall': DC_ + SM_ + '1.0 sheet at x -35 to -34, y -59 to 42, z 6.4 to 48.4; its ends folded round the U\'s end walls (to x -18; '
                         'the -y fold to z 24, the +y to z 30); a flange 8 x 12 bent out (-x) at its top, y -52 to -40, Ø3.4 at (-39, -46) '
                         '(the plate stud). HOLES (y, z): 2 x Ø3.4 at (29.5, 44.4) and (-47.5, 11.4), 77.0 x 33.0 ±0.05 to each other (ERP '
                         'p.11\'s tab holes; M3 x 8 button screws from outside); in the folds, Ø3.4 at x -26, z 15 (the joint screws)',
            'tray-u': DC_ + SM_ + '1.0 sheet: the bottom (x -34 to -7, z 6.4 to 7.4), the inner wall (x -8 to -7) and two ends (y -58 to -57, 40 '
                      'to 41), to z 48.4; its corners folded, every gap under 0.5, its top edges flat to 0.3, so the rim meets the plate '
                      'with no opening over 1.6 (UL 1598 6.17.2.4). HOLES: in the -y end at (x -29, z 32) a Ø5.0 hole, its edge rolled '
                      'out to a smooth Ø7.5 lip (UL 1598 5.14.1(a): the LED leads); in each end Ø4.22 +0.08 for a PEM S-M3-1 at x -26, z '
                      '15 (the joint; 8.6 from the bottom, 8.0 from the corner); a flange 12 x 10 off the +y end at the top, Ø3.4 at (-21, '
                      '46.3)',
            'relief-bracket': DC_ + SM_ + '1.6 sheet, a channel: the web across y (y 3 to 4.6), x -5 to 26, z 5 to 48.4; side flanges bent +y to '
                              'y 13.8, each with a Ø3 dimple at (y 8.7, z 37) standing 0.85 (the - side) and 1.25 (the + side) proud of its inner face, so each splice is pressed 0.5 (the push fit); a top flange to y 28.5 under the plate, 2 x '
                              'Ø3.4 at (1, 24.5) and (16, 24.5), 15.0 ±0.05 apart (the plate studs). The web\'s window x -3 to 22, z 21 to '
                              '26.7, its top edge bent out +y as the splices\' ledge (z 26.7 to 28.3, to y 12) with four notches 4 wide at x '
                              '0.25, 6.75, 13.85, 20.35, and four 1.0 x 3.0 tie slots (x 3.0, 9.8, 16.6, 23.0 to +1.0; y 6.5 to 9.5) for the LED leads\' two ties; the window, the notches and the slots deburred and broken 0.3. HOLES in the web (x, z): 2 x '
                              'Ø4.22 +0.08 for PEM S-M3-1, nuts on the +y face, at (8, 10) and (8, 17) (the straps; 8 or more from the bends)',
            'gripper-brackets': DC_ + SM_ + 'HOLES: Ø10.5 in each foot at (-+48, 0) (M10, the gripper); 4 x Ø3.4 in each bracket\'s two outward '
                                'flanges at (-+43.5, -+29.3) and (-+52.5, -+29.3), to each other ±0.05 (the plate\'s studs)',
        }
        for q_ in parts_:
            if q_ is not None and q_.name in TH_:
                q_.notes = [TH_[q_.name]] + list(q_.notes)     # v8: first, so the drawings print them
        if a0_:                       # V10-3: the canopy's sheet metal drawn square on its sheets (A with the lock turns it 105 deg)
            for q_ in parts_:
                if q_ is not None and q_.name in ('canopy', 'strap', 'tray-wall', 'tray-u', 'relief-bracket', 'gripper-brackets') and q_.solid is not None:
                    q_.detail = at(-a0_, q_.solid)
    if tt_:
        # V11-15: American spelling in everything the Hemisphere packages print (the materials' own names stay fabkit's)
        for q_ in parts_:
            if q_ is not None and q_.notes:
                q_.notes = [_us(t_) for t_ in q_.notes]
    return [q_ for q_ in parts_ if q_ is not None]


_US = [('anodised', 'anodized'), ('Anodised', 'Anodized'), ('anodising', 'anodizing'), ('aluminium', 'aluminum'),
       ('Aluminium', 'Aluminum'), ('moulds', 'molds'), ('mould', 'mold'), ('colours', 'colors'), ('colour', 'color'),
       ('centres', 'centers'), ('centre', 'center'), ('equalising', 'equalizing'), ('levelling', 'leveling'), ('grey', 'gray')]


def _us(t):
    for a_, b_ in _US:
        t = t.replace(a_, b_)
    return t


# The owner signed v3 (2026-11-01, r46-owner-notes 5b63e05b: "Hemisphere: color outside"): the main build's shade is
# a 3 mm stock-tint shell outside, a 6 mm clear structural shell, then the opal. v2 (clear outside, tinted skin) stays
# as the alternative in dome_pendant_v2.py
V3 = dict(N, shell=3.0, liner=6.0, skin=3.0, build='v3',
          # option 3 (the owner, 2026-11-10: "it should work like core cut in half"): the light at the mouth's centre,
          # facing up into the shade, on a stem from the hub; the COB, its reflector and holder gone
          engine='ring', carrier=(56.0, 4.5), board=(50.0, 1.6), stem=(16.0, 12.0), white_disc=95.0,   # 2026-11-11: Ø95, hides the collar's slots from below
          white_split=True,   # 2026-11-24 (review 2): the Ø95 disc trapped the shade (top_check.py): a Ø62 disc and the collar's white lip
          fixings=True)       # 2026-11-24 (check 3): the grip into the hub, the crown screwed, the cable on a stud in the hub (GRIP)


def dome_parts(p=None):
    return [q for q in north_parts(V3 if p is None else p) if q is not None]


# --- Orb, the table lamp -------------------------------------------------------------------------------------------
def orb_geometry(p=O):
    R = p['R']
    bd, bh = p['base']
    z_top = bh + p['ring']
    zc = z_top + math.sqrt(R * R - p['rim_r'] ** 2)          # the ball rests at the cup's rim radius
    return R, bd, bh, z_top, zc


def orb_parts(p=O):
    """Core (round 35; the Orb before it): one tinted ball frosted inside, on a base that holds its own battery. The
    owner (round 35): "I want it to work plugged in or not. Why does it need a separate cartridge for that?" So three
    standard LiFePO4 cells lie in the base behind a screwed hatch underneath, the user's to replace. It runs from USB-C
    or its cells, and charges while it runs. Round 41 (the owner signed round 40): round 32f's 120 x 30 base again,
    the cells three 18650s in a triangle of chords round the LED (three 26650s fit neither under it nor round it in 30;
    the 48 base of rounds 35 to 39 is in git at 950a7eaf)."""
    from build123d import Sphere, Pos
    R, bd, bh, z_top, zc = orb_geometry(p)
    cup = Pos(0, 0, zc) * Sphere(R + 0.5)
    t = p['shell']
    B_ = p.get('design', 'A') == 'B'
    port = cyl('z', (0, 0), p['port'], zc - R - 5, zc - R + 25)
    shell = ball(R, t, (0, 0, zc)) - port
    shell_r = ball(R, t - 0.4, (0, 0, zc)) - port
    frost_r = ball(R - t + 0.3, 0.3, (0, 0, zc)) - port
    core = None
    if B_:
        # the core: R 70 outside, 3 thick, concentric (2026-11-10), its own Ø40 opening at its foot over the window; the
        # core's outside meets r 20 at z 33.4
        rc, tc, dz = p['core']
        zcc = zc - dz
        core = ball(rc, tc, (0, 0, zcc)) - cyl('z', (0, 0), p['port'], zcc - rc - 5, zcc - rc + 25)
    gz0 = zc - math.sqrt(R ** 2 - (p['port'] / 2) ** 2)
    gz1 = zc - math.sqrt((R - p.get('grommet_wall', t)) ** 2 - (p['port'] / 2) ** 2)
    if B_:
        # 2026-11-10 (the coordinator's brief, the concentric core): the grommet raised about 1.5 to suit. The core's foot
        # (where its outside meets its Ø40 opening, zsh = 33.4) rests on a flange, Ø52, turned flat on top and contoured
        # underneath to R 74, the outer ball's inside: the flange is the axial stop on the outer ball. The tube runs 3
        # past the core's foot, a spigot inside the core's opening (0.2 clear round it), and the core is bonded on the
        # spigot's cylinder (about 377 mm2, MMA). The bore is machined bright after anodizing
        zsh = zcc - math.sqrt(rc ** 2 - (p['port'] / 2) ** 2)
        gz1 = max(gz1, zsh + 3.0)
        fl = (cyl('z', (0, 0), p['flange'], gz0, zsh) & (Pos(0, 0, zc) * Sphere(R - t))) - cyl('z', (0, 0), p['port'] - 6, gz0 - 1, zsh + 1)
    grommet = cyl('z', (0, 0), p['port'] - 0.4, gz0, gz1) - cyl('z', (0, 0), p['port'] - 6, gz0 - 1, gz1 + 1)
    if B_:
        grommet = grommet + fl
    hz = 2.5                                                  # the hatch's counterbore
    # the middle: the chassis (the LED's heat spreader, 50 across) under the board and the LED, the window above
    cz0, cz1 = 10.6, 12.2
    chassis = cyl('z', (0, 0), 50.0, cz0, cz1) - cyl('z', (0, 0), 10, cz0 - 1, cz1 + 1)
    board = cyl('z', (0, 0), 48.0, cz1 + 0.2, cz1 + 1.6) - cyl('z', (0, 0), 28, cz1, cz1 + 2)
    led = cyl('z', (0, 0), 26, cz1 + 1.0, cz1 + 2.6)
    uz = cz1 + 3.0
    window = cyl('z', (0, 0), 29.6, uz + 0.2, zc - math.sqrt((R + 0.5) ** 2 - 15 ** 2) - 0.3)
    # the cells: three chords, their normals at -10, 110 and 230 deg (the corner at 170 holds the USB-C)
    a, d, L = 27.0, 18.4, 65.2
    z0c = hz + 0.9
    # review 2026-11-01: no holders. Each cell (button-top: the 65.2 includes a 7 x 0.8 button at its + end) lies in a
    # bay milled 18.6 wide; its + button reaches a gold-flashed leaf at the bottom of an 8 shroud milled 1.5 into the
    # bay's end wall (only a button top reaches it), its - end bears on a nickel-plated conical spring 1.7 deep
    cells = holder = bay = None
    ax = (a + d / 2, z0c + d / 2)
    for k in range(3):
        ang = -10.0 + 120.0 * k
        c = at(ang, cyl('y', ax, d, -L / 2 + 0.8, L / 2) + cyl('y', ax, 7.0, -L / 2, -L / 2 + 0.8))
        h = at(ang, cyl('y', ax, 6.0, -L / 2 - 0.7, -L / 2) + cyl('y', ax, 12.0, L / 2, L / 2 + 1.7))
        b = at(ang, box(a - 0.1, -L / 2 + 0.8, -1, a + d + 0.1, L / 2 + 1.7, z0c + d + 0.5) +
               cyl('y', ax, 8.0, -L / 2 - 0.7, -L / 2 + 0.9))
        cells = c if cells is None else cells + c
        holder = h if holder is None else holder + h
        bay = b if bay is None else bay + b
    # the ballast: steel in the three corners between the chords, out to 54, a 2 web of acrylic round each
    corner = cyl('z', (0, 0), 108.0, hz + 0.1, z0c + d + 0.4) - cyl('z', (0, 0), 54.0, 0, 30) - _chords(a, L, d, 0.0)
    # USB-C: a sealed receptacle on a small board in the corner at 170 deg, out along a notch in the underside
    aa = math.radians(100.0)
    ux, uy = -math.sin(aa), -math.cos(aa)
    uang = math.degrees(math.atan2(uy, ux))
    notch = at(uang, box(46, -6.5, -1, bd / 2 + 2, 6.5, 7.0))
    usb = at(uang, box(43.0, -5.0, 3.0, 50.5, 5.0, 10.0))
    corner = corner - at(uang, box(30, -8, 0, 70, 8, 30))
    # review 2026-11-01, the heat path: the chassis grows two arms (8 x 1.6) along the bisectors of the cell-free corners
    # at 50 and 290 deg out to r 44, and a Ø8 post at each up to 0.5 under the touch ring; a 0.5 electrically insulating
    # silicone thermal pad (3 W/m K) between each post and the ring keeps the ring free for touch. The corners' steel and
    # the acrylic are slotted from below so the chassis goes in from underneath. LED board to chassis to posts to the ring,
    # the one metal face open to the room; the cells' bays are 0.9 or more from any of it
    heat = pads = None
    slot = None
    for ang in (50.0, 290.0):
        h = at(ang, box(24.0, -4.0, cz0, 44.0, 4.0, cz1) + cyl('z', (44.0, 0), 8.0, cz0, bh - 0.5))
        pd = at(ang, cyl('z', (44.0, 0), 8.0, bh - 0.5, bh))
        sl = at(ang, box(24.0, -4.3, -1, 44.0, 4.3, cz1 + 0.3) + cyl('z', (44.0, 0), 8.6, -1, bh - 0.5))
        heat = h if heat is None else heat + h
        pads = pd if pads is None else pads + pd
        slot = sl if slot is None else slot + sl
    chassis = chassis + heat
    ballast = corner - slot
    plug = at(uang, box(51, -6.0, 0.6, 62, 6.0, 6.6))
    cable = orb_cable(ux, uy)
    zs = zc - math.sqrt(R ** 2 - 42 ** 2) - 0.3
    seat = cyl('z', (0, 0), 92, zs - 1.5, zs) - cyl('z', (0, 0), 84, zs - 2, zs + 1)
    # the drum: from below, the hatch's counterbore, the middle pocket, the cells' bays, the corners, the ring's groove
    # ANGLED (a look for the owner, 2026-11-10, not the default: "Instead of the vertical edges on core's base I wonder
    # if angled edges flush with the base would look better"): the base's wall a cone from under the touch ring (r 60
    # at z 30) down and out along one line through the dock to the dock's outer foot (r 75 at z -6.5), so lamp and
    # dock read as one cone with a 0.2 hairline at z 1.5; the base keeps its Ø120 x 1.5 boss in the dock's pocket
    ang_ = p.get('angled', False)
    def cone_r(z):
        return 60.0 + 15.0 * (bh - z) / (bh + 6.5)
    def frustum(za, zb):
        from build123d import Cone, Pos, Align
        return Pos(0, 0, za) * Cone(cone_r(za), cone_r(zb), zb - za, align=(Align.CENTER, Align.CENTER, Align.MIN))
    own_ = p.get('own_skin', False) and ang_
    if own_:
        # BASE B IN ITS OWN COLOUR (the owner, 2026-11-11: "Own color for sure"; the coordinator: the whole base, lip
        # included, option (a)): the outside is one 6 mm skin formed from the shell's own lamp sheet, satin, over a 0.5
        # white liner, from the ball's seat to the floor (the dock under its skirt); its lip a bullnose R12 (opened from
        # R7 so 6 mm sheet forms in one piece). Inside it, this black body: the cone 7.2 in from the skin's outside to
        # z 25, then a Ø98 column to the top; the cells, board, well and contacts as before
        def frustum_in(za, zb, d):
            from build123d import Cone, Pos, Align
            return Pos(0, 0, za) * Cone(cone_r(za) - d, cone_r(zb) - d, zb - za, align=(Align.CENTER, Align.CENTER, Align.MIN))
        base = (cyl('z', (0, 0), bd, 0, 1.5) + frustum_in(1.5, 25.0, 7.2) + cyl('z', (0, 0), 98.0, 25.0, bh)) - cup - cyl('z', (0, 0), 112.0, -1, hz)
    elif ang_:
        base = (cyl('z', (0, 0), bd, 0, 1.5) + frustum(1.5, bh)) - cup - cyl('z', (0, 0), 112.0, -1, hz)
    else:
        base = eased(bd, 0, bh, 3.0, top=False) - cup - cyl('z', (0, 0), 112.0, -1, hz)
    base = base - cyl('z', (0, 0), 50.4, -1, uz) - cyl('z', (0, 0), 30, uz - 0.1, bh) - bay
    well = None
    if p.get('well'):
        # 2026-11-10 (the coordinator; the enclosing sensor: the black walls round the window took most of the LED's
        # light, 76 lm of 200 out of the base): the light well lined white, a white PTFE sleeve Ø32/Ø30 x 6 round the
        # window, from the pocket's roof up to the cup; the base's bore opened to Ø32 for it
        well_top = zc - math.sqrt((R + 0.5) ** 2 - 16.0 ** 2) - 0.2
        base = base - cyl('z', (0, 0), 32.0, uz - 0.1, well_top + 1.0)
        well = cyl('z', (0, 0), 32.0, uz - 0.1, well_top) - cyl('z', (0, 0), 30.0, uz - 1, well_top + 1)
    base = base - (cyl('z', (0, 0), 108.4, -1, z0c + d + 0.6) - cyl('z', (0, 0), 53.6, -2, 31) - _chords(a, L, d, -0.2) -
                   at(uang, box(30, -7.8, -2, 70, 7.8, 31)))
    # the owner signed the contact dock (2026-11-01, r46-owner-notes 5b63e05b): the cable notch is closed; the USB-C
    # (service and travel) faces down through a slot in the hatch; the hatch takes the dock's contacts: a Ø8 hole on
    # the axis and a ring groove (r 17 to 23, 1.8 deep) over two spring pins on a small board under the chassis
    base = base - at(uang, box(42.5, -5.5, -1, 51, 5.5, 10.5))
    pin_a = math.radians(140.0)
    pin2 = (20.0 * math.cos(pin_a), 20.0 * math.sin(pin_a))
    hatch = (cyl('z', (0, 0), 111.6, 0.2, hz) - at(uang, box(44.0, -4.6, -1, 49.5, 4.6, 3)) - cyl('z', (0, 0), 8.0, -1, 3) -
             (cyl('z', (0, 0), 46.0, -1, 2.0) - cyl('z', (0, 0), 34.0, -2, 3)) - cyl('z', pin2, 3.0, -1, 3))
    foot = cyl('z', (0, 0), 117.6, 0.2, 2) - cyl('z', (0, 0), 114.4, 0, 3)
    pins = cyl('z', (0, 0), 1.5, 1.7, 9.0) + cyl('z', pin2, 1.5, 1.7, 9.0)          # drawn on the dock: compressed 1.0
    pinboard = cyl('z', (0, 0), 46.0, 9.0, cz0)
    # the dock (in the box; drawn under the lamp): Ø150 x 8 polished black cast acrylic, a 1.5 pocket Ø122 the base sits
    # in, a 304 stainless post Ø6 on the axis (+) and a ring r 18.5 to 21.5 (-), 1.7 proud of the pocket's floor, so
    # they rise into the hatch's hole and groove (the pins, free 0.7 above the foot's face, work at 1.0 of their 1.5);
    # its board in a pocket at the back, the USB-C cable leaving through a channel in the back edge
    dz0 = -6.5
    contacts = cyl('z', (0, 0), 6.0, -2.0, 1.7) + (cyl('z', (0, 0), 43.0, -2.0, 1.7) - cyl('z', (0, 0), 37.0, -3, 2))
    dock_board = box(-19.0, 46.0, -4.5, 19.0, 69.0, -2.9)
    db_ = 0.0
    if p.get('angled', False):        # the slope comes within 0.1 of the board's pocket's outer corners: it moves 2.5 in
        db_ = 9.0 if p.get('own_skin', False) else 2.5      # (own colour: the dock 7 in, under the skirt: 9 in)
        dock_board = box(-19.0, 46.0 - db_, -4.5, 19.0, 69.0 - db_, -2.9)
    dock_cable = cyl('y', (0, -2.75), 4.0, 74.6, 180.0)
    if own_:
        from build123d import Cone, Pos, Align
        dock_out = Pos(0, 0, dz0) * Cone(cone_r(dz0) - 7.0, cone_r(1.3) - 7.0, 1.3 - dz0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    dock = ((dock_out if own_ else frustum(dz0, 1.3) if ang_ else eased(150.0, dz0, 1.5, 1.5)) - cyl('z', (0, 0), 122.0, 0, 3) - contacts - box(-20.0, 45.0 - db_, -5.0, 20.0, 70.0 - db_, -1.0) -
            cyl('y', (0, -2.75), 4.2, 60.0, 80.0))
    base = base - (cyl('z', (0, 0), 118, -1, 2) - cyl('z', (0, 0), 114, -2, 3)) - cyl('z', (0, 0), 92.4, zs - 2, zs + 0.01)
    # the owner's pick, 2026-11-11 ("I like B"): the touch ring's top edge turned over in a 7 mm bullnose where it meets
    # the ball, so the ball nests into it (was 2.0)
    ring = eased(bd, bh, z_top, 7.0 if p.get('angled', False) else 2.0, bottom=False) - cup
    skin = liner = None
    if own_:
        # the touch electrode: an aluminium ring Ø98 behind the lip's end, the touch through the 6 mm skin (to
        # prototype-test; fallback: the lip's skin 3-4 mm over it)
        ring = eased(98.0, bh, 37.5, 1.0, bottom=False) - cup
        # the skin and liner, revolved from their (r, z) outlines
        from build123d import BuildSketch, BuildLine, Polyline, make_face, revolve, Plane, Axis
        cz_, cr_ = 25.5, 49.85                                  # the lip's centre: R12 outside, R6 inside
        arc = lambda R: [(cr_ + R * math.cos(math.radians(a)), cz_ + R * math.sin(math.radians(a))) for a in range(0, 91, 6)]
        out_ = [(cone_r(dz0), dz0)] + arc(12.0)
        in_ = arc(6.0)[::-1] + [(cone_r(cz_) - 6.5, cz_), (cone_r(dz0) - 6.5, dz0)]
        def rev(pts):
            with BuildSketch(Plane.XZ) as sk_:
                with BuildLine():
                    Polyline(*pts, close=True)
                make_face()
            return revolve(sk_.sketch, Axis.Z)
        # the cable leaves under the skirt's back through a small arch (Ø9.2), edges polished
        notch = cyl('y', (0, -2.75), 9.2, 55.0, 90.0)
        skin = rev(out_ + in_) - notch
        lin_o = arc(6.0) ; lin_i = arc(5.5)[::-1] + [(cone_r(cz_) - 7.0, cz_), (cone_r(dz0) - 7.0, dz0)]
        liner = rev([(cone_r(dz0) - 6.5, dz0), (cone_r(cz_) - 6.5, cz_)] + lin_o + lin_i) - notch
    ring = ring - (cyl('z', (0, 0), 92.4, zs - 2, zs + 0.01) - cyl('z', (0, 0), 83.6, zs - 3, zs + 1))
    base = base - slot - pads
    if B_:
        ball_parts = [
            Part('shell', shell, Machined('acrylic-trucast-formed', 'formed', setup_usd=1500.0), finish='body', group='ball',
                 notes=['Core B (the owner, 2026-11-09): the outer ball, R 80 outside, R 74 inside, polished both faces '
                        '(no frost). Two hemispheres drape-formed from 6 mm (1/4 in) cast sheet in the speaker\'s TruCast '
                        'code for the tint (Ember 2423, Dust 2422, Acid 9097, Poison 2092, Ice 2069, Haze 2287, Fog 0000, '
                        'Smoke 2074), the chart figure held at the 6 mm wall; CUSTOM POURS (the owner, 2026-11-11): Dust, Acid and Ice '
                        'at 3x that loading, Poison at 0.6x it (the mix, the owner 2026-11-17, matched to Hemisphere switched off), Smoke at 0.6x the chart loading (2026-11-16, was the speakers\' own pour, 0.3x; matched to Hemisphere switched off), on the existing female mould [check with the '
                        'former: the 6 mm wall must form on the 9 mm wall\'s mould]; joined at the equator round the core '
                        'with a polymerising acrylic cement (Acrifix 192 kind), the joint turned and polished; the Ø40 '
                        'port cut at its foot']),
            Part('core', core, Machined('acrylic-opal-core', 'formed', setup_usd=1300.0), finish='liner', group='ball',
                 notes=['Core B: the core, a Ø140 ball of 3 mm white opal cast acrylic, Perspex GS Opal 041 (R 70 outside, '
                        'R 67 inside), concentric with the outer ball (2026-11-10, the owner: "the same depth around the '
                        'whole inner core"): a 4 mm gap all round, a 10 mm band of colour. Its own Ø40 opening at its foot '
                        'over the window, its foot on the grommet\'s flange (its top at z 33.4), bonded on the grommet\'s '
                        '3 mm spigot (MMA). The former to confirm the 4 mm gap between the balls (±1 mm on both, the two '
                        'equator seams in one plane); fallback Ø130, a 15 mm band. Captive once the outer halves are '
                        'joined round it. Assembly: anneal the halves; bond the core on the spigot and cure it with the '
                        'outer top half off; cement the outer equator dry; drop-test the first sample. '
                        'Formed: two halves on a core mould (about $1,300 [E]), about $25 to $40 a ball [E]. Or stock: '
                        'a Ø140 x 3 opal acrylic sphere, if one is made [check a supplier], its opening cut to Ø40 '
                        '(the BOM\'s option "stock core")']),
        ]
    else:
        ball_parts = [
            Part('shell', shell, Machined('acrylic-formed', 'formed', setup_usd=1500.0), finish='body', group='ball',
                 pieces={'shell': (shell_r, 'body'), 'frost': (frost_r, 'liner')},
                 notes=['the ball: two hemispheres drape-formed from 10 mm tinted cast sheet on one aluminium mould (the '
                        'production process; the prototypes are formed on it), their insides bead-blasted, joined at the '
                        'equator with a polymerising acrylic cement (Acrifix 192 kind), the joint turned and polished: a '
                        'faint line at the equator (to judge on the first sample); a 40 port cut at its underside. One '
                        'part where there were three: the frost scatters because it faces air']),
        ]
    return ball_parts + [
        Part('grommet', grommet, Machined('aluminium', 'lathe'), finish='anodised', group='ball',
             notes=['BRIGHT BY NECESSITY (the bar\'s exception, 2026-11-11): the bore is machined bright after anodizing, a working '
                    'reflector for the LED\'s light; the outside satin black. ' + 'black anodised aluminium: lines the port, bonded with a two-part MMA adhesive (not cyanoacrylate). '
                    'Review 2026-11-01, to draw with the dock: it grows a Ø38 x 6 spigot under the ball with three 30 deg '
                    'L-slots, into a Ø38.4 socket round the window with three Ø3 stainless pins, so the ball stays '
                    'captive in a drop and still swaps with a quarter turn (CORE-RECHARGE.md §6)'] +
             (['Core B (2026-11-10, the concentric core): raised about 1.5 to suit. A flange Ø52 turned on it inside '
               'the ball, contoured underneath to R 74 to sit on the outer ball\'s inside (the axial stop), flat on top '
               'at z 33.4 under the core\'s foot; the tube runs 3 past it, a spigot in the core\'s Ø40 opening (0.2 '
               'clear round it), the core bonded on the spigot\'s cylinder (about 377 mm2, MMA). The bore machined '
               'bright after anodizing (a reflector up into the core). The grommet goes into the port from inside before '
               'the outer halves are joined'] if B_ else [])),
        Part('base', base, Machined('cast-acrylic-satin', 'lathe', setup_usd=80.0), finish='trim', group='base',
             notes=['WITH THE BASE IN ITS OWN COLOUR (2026-11-11, the default): this is the hidden inner body, black cast '
                    'acrylic, turned, 7.2 inside the skin, holding the cells, board, well and contacts. '
                    'SATIN (the owner, 2026-11-11: "satin or matte instead of shiny plastic"): black cast acrylic, turned, then '
                    'bead-blasted to a fine satin close to matte, no mirror highlights (the default until the owner chooses; '
                    'OPTION: turned 6061, satin black anodized, about +345 g, the touch ring then insulated from it). '
                    'Turned from rod: 120 x 30 (round 32f\'s), the cup turned in it; from '
                    'below the hatch\'s counterbore (112), the middle pocket (50) for the chassis, the board and the LED, '
                    'the three cells\' bays, the ballast\'s corners and the cable notch']),
    ] + ([Part('skin', skin, Machined('acrylic-trucast-formed-satin', 'formed', setup_usd=1200.0), finish='body', group='base',
               notes=['BASE B IN ITS OWN COLOUR (the owner, 2026-11-11: "Own color for sure"): one skin drape-formed from the '
                      'shell\'s own 6 mm lamp sheet (the same pour, so the same colour), from the ball\'s seat to the floor, '
                      'the lip a bullnose R12 in the same piece (R7 will not form in 6 mm), trimmed, edges polished with an even '
                      'chamfer, the outside fine glass-bead blasted and sealed with a matte anti-fingerprint hardcoat; bonded '
                      'to the body. The mould is a one-time cost (setup). The whole base in colour: about $150-200 a lamp '
                      '[E] (the skin $30-50 at volume, the body $100-120, the liner $8-12, the electrode $10-15)']),
          Part('liner', liner, Machined('acrylic-opal-core-bonded', 'formed'), finish='liner', group='base', inside=True,
               notes=['an OPAQUE white layer under the skin (2026-11-21: was "a 0.5 white opal liner"; an opal sheet would '
                      'let the black body show through), so the colour reads evenly and nothing inside shows; '
                      'IN OPTICAL CONTACT WITH THE SKIN (2026-11-21, the coordinator, from the owner\'s "smoke frosted" edges): '
                      'bonded to the skin\'s inside with a clear polymerising acrylic cement (Acrifix 192 kind), no air left '
                      'between them, or the white a coating on the skin\'s inside instead of a separate liner. A loose sleeve '
                      'leaves an air gap at which the light the satin face bends steeply into the skin is totally reflected '
                      'and absorbed in the colour: the base\'s flanks then read gray, not red (rendered 2026-11-21)'])]
         if skin is not None else []) + [
        Part('ring', ring, Machined('aluminium', 'lathe'), finish='anodised', group='base',
             notes=(['THE TOUCH ELECTRODE (2026-11-11): with the base in its own colour this ring sits behind the skin\'s lip '
                     '(Ø98), the touch through the 6 mm acrylic: TO PROTOTYPE-TEST (fallback: the lip\'s skin 3-4 mm over '
                     'it). '] if skin is not None else []) + ['aluminium, black anodised, satin, its top edge turned to a 7 mm bullnose the ball nests into (the '
                    'owner\'s pick B, 2026-11-11), insulated from the chassis: the touch (tap to switch, hold to dim, '
                    '2200 to 2700 K)']),
    ] + ([Part('well', well, Machined('ptfe', 'lathe'), finish='white', group='base',
               notes=['the light well (2026-11-10): a white PTFE sleeve, Ø32/Ø30 x 6, pressed into the base\'s bore round the '
                      'window (the window\'s O-ring seals to it), so the walls round the LED reflect (about 0.95) where '
                      'the black acrylic absorbed'])] if well is not None else []) + [
        Part('window', window, Machined('cast-acrylic', 'lathe'), finish='window', group='base',
             notes=['a clear acrylic plug, sealed with an O-ring: the LED under it, the base IP44 with the ball off']),
        Part('chassis', chassis, Machined('aluminium', 'mill'), finish='steel', group='base', inside=True,
             notes=['aluminium 6061, 50 across: the LED\'s heat spreader and the board\'s carrier, screwed up into the '
                    'base on threaded inserts, an O-ring between. Review 2026-11-01: two arms 8 x 1.6 out to r 44 in '
                    'the cell-free corners and a Ø8 post at each up to the touch ring (on a 0.5 insulating thermal pad): '
                    'about 0.4 W/K to the ring, so about 4 K across the path at 1.5 W; the ring\'s 9,500 mm2 to the room '
                    'about 16 K more [E]: the chassis about 20 K over the room at full while charging, to prove on the '
                    'bench']),
        Part('pads', pads, Bought('core-thermal-pad'), finish='silicone', group='base', inside=True),
        Part('ballast', ballast, Machined('steel', 'mill'), finish='steel', group='base', inside=True,
             notes=['mild steel, zinc-plated: three corner pieces between the cells\' bays, screwed up into the base']),
        Part('board', board, Bought('core-board-18650'), finish='steel', group='base', inside=True, render=False),
        Part('led', led, Bought('moon-led-table'), finish='led', group='base', inside=True),
        Part('cells', cells, Bought('core-cells-18650'), finish='steel', group='battery', inside=True, render=False),
        Part('holder', holder, Bought('core-holder-18650'), finish='trim', group='battery', inside=True,
             notes=['review 2026-11-01: no holders. Per cell, a gold-flashed + leaf Ø6 x 0.7 at the bottom of an 8 '
                    'shroud milled 1.5 into the bay\'s end wall (only a button top reaches it: a reversed or flat-top cell '
                    'makes no contact) and a nickel-plated conical - spring Ø12, 1.7 at rest; leads in a milled channel '
                    'to the board, the NTC on one cell; no exposed contact outside the hatch']),
        Part('hatch', hatch, Machined('aluminium', 'mill'), finish='anodised', group='battery',
             notes=['black anodised aluminium, 2.3 thick, in a counterbore under the base: six captive M3 screws, BLACK OXIDE, '
                    'countersunk flush with the hatch (2026-11-11, the bar) '
                    '(Phillips or Torx: commercially available tools; review 2026-11-01: six, was four, tapped into the '
                    'steel ballast corners, not inserts in acrylic, nylon-patched), an O-ring (IP44); a label inside: the '
                    'cells\' type (LiFePO4 18650 only) and how to change them. Under it, to draw with the dock: a 0.5 '
                    '304 stainless tray round the three bays (the bays 19.6 wide for it), so the cells sit in metal on '
                    'every side (UL 153 SA; CORE-RECHARGE.md §6)']),
        Part('usb', usb, Bought('orb-seals'), finish='steel', group='base', inside=True, render=False),
        Part('seat', seat, Bought('orb-seat'), finish='silicone', group='base'),
        Part('foot-ring', foot, Bought('core-foot'), finish='silicone', group='base'),
        Part('pins', pins, Bought('core-dock-pins'), finish='steel', group='base', inside=True,
             notes=['two gold-plated spring pins, 1.5 travel, about 0.8 N at 1.0: + on the axis, - at r 20; on the pin '
                    'board, through the hatch\'s hole and groove; free, their tips sit 0.7 above the foot\'s face']),
        Part('pinboard', pinboard, Bought('core-pinboard'), finish='steel', group='base', inside=True, render=False),
        Part('dock', dock, Machined('cast-acrylic-satin', 'lathe', setup_usd=80.0), finish='trim', group='dock',
             notes=['the contact dock (signed 2026-11-01): Ø150 x 8, black cast acrylic, turned, bead-blasted SATIN to match the base '
                    '(2026-11-11; OPTION: 6061 satin black anodized, about +170 g); a 1.5 pocket '
                    'Ø122 the base sits in; the contacts pressed in; a pocket at the back for its board and a channel '
                    'for the cable; silicone dots underneath (CORE-RECHARGE.md)']),
        Part('dock-contacts', contacts, Bought('core-dock-contacts'), finish='steel', group='dock'),
        Part('dock-board', dock_board, Bought('core-dock-board'), finish='steel', group='dock', inside=True, render=False),
        Part('dock-cable', dock_cable, Bought('orb-cable'), finish='fabric', group='dock'),
        Part('adapter', None, Bought('orb-adapter')),
        Part('screws', None, Bought('core-screws')),
        Part('tray', None, Bought('core-tray')),
    ] + ([Part('core-stock', None, Bought('core-core-stock'), option='stock core')] if B_ else
         [Part('ball-two-layer', None, Bought('core-ball-two-layer'), option='two-layer ball')])


def orb_cable(ux, uy):
    """The cable, dressed away: out of the plug along the notch, curving round to run straight back over the table, 420
    long. Short straight lengths with round joints (a swept spline tessellated to 650,000 vertices)."""
    from build123d import Solid, Plane, Sphere, Pos, Vector as V
    r, z = 2.6, 2.6
    p0, p1, p2 = (62 * ux, 62 * uy, 3.6), (95 * ux, 95 * uy + 30, z), (95 * ux, 140, z)
    pts = []
    for i in range(13):                                   # a quadratic Bezier round the corner
        s = i / 12
        pts.append(tuple((1 - s) ** 2 * a + 2 * s * (1 - s) * b + s * s * c for a, b, c in zip(p0, p1, p2)))
    pts.append((95 * ux, 420, z))
    out = None
    for a, b in zip(pts, pts[1:]):
        d = V(*b) - V(*a)
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d))
        seg = seg + Pos(*b) * Sphere(r) if b != pts[-1] else seg
        out = seg if out is None else out + seg
    return out


def eased(d, z0, z1, e, top=True, bottom=True):
    from build123d import fillet, Axis
    s = cyl('z', (0, 0), d, z0, z1)
    fs = s.faces().sort_by(Axis.Z)
    es = (fs[0].edges() if bottom else []) + (fs[-1].edges() if top else [])
    return fillet(es, e) if es else s


_R, _bd, _bh, _zt, _zc = orb_geometry()
ORB_LIGHT = (0.0, 0.0, round(_zc, 1))           # at the centre: 30 below drew a crescent in the frost (critic p2)
ORB_SIZE = dict(ball=2 * _R, height=round(_zc + _R, 1), base=_bd)

def notes_dome(top=None, record=False):
    """V11-3 (the V10 check): NOTES built per product, by the top actually built (today's top, A with or without its lock,
    B), not by the module's LOCK_ON alone. record=True: v2, a record (V11-17)."""
    lock_ = bool((TOP_TIERS.get(top) or {}).get('lock'))
    cap_ = 'the cap (B: its Ø56 tier)' if top != 'A' else 'the cap'
    if lock_:
        swap_ = ('To take one off: hold the shade from below with one hand and the cap with the other; pull the lock\'s knob and '
                 'hold it out through the whole swap (whether one person can do this while steadying the top is not yet shown); '
                 'lift the shade as far as it goes (8 to 9 mm), turn it counter-clockwise, seen from below, to the stop, and lower '
                 'it off. To fit one: while it is still in your hands, find the mark on its clamp ring; hold it up under the lamp '
                 'with the mark under the line on the crown (it fits one way only), pull the knob, push the shade up as far as it '
                 'goes, turn it clockwise, seen from below, to the stop, and let go: it drops 8 mm. Then let the knob go: it springs '
                 'fully in. IF THE SHADE DID NOT DROP, OR THE KNOB DOES NOT GO FULLY IN, IT IS NOT ON. The lock does not hold a '
                 'shade let go before it dropped: such a shade sits 8 mm high, held only by friction.')
    else:
        swap_ = (f'To take one off: hold the shade from below with one hand and {cap_} with the other; lift the shade as far as it '
                 'goes (8 to 9 mm), turn it counter-clockwise, seen from below, to the stop, and lower it off. To fit one: while it '
                 'is still in your hands, find the mark on its clamp ring; hold it up under the lamp with the mark under the line '
                 'on the crown (it fits one way only; if it will not go up, turn it a third of a turn and try again). Push it up as '
                 'far as it goes, turn it clockwise, seen from below (as a light bulb goes in), to the stop, and let go: it drops 8 '
                 'mm and the detent clicks. IF IT DID NOT DROP AND CLICK, IT IS NOT ON: push it up, turn it to the stop and let it '
                 'drop. To check a shade, and always before you clean it, try to turn it clockwise without lifting it: a seated '
                 'shade does not turn; one that turns was not on, so turn it to the stop and let it drop. Never turn a shade '
                 'counter-clockwise without lifting it first. A shade that has not dropped sits 8 mm high, held only by friction; a '
                 'push of 2 to 4 N at its rim, such as a cloth while cleaning, can turn it back to its entries, and it falls.')
    cap_top_ = ('the height of the cap\'s top (not where the cables leave the crown, 8.5 lower)' if top == 'B'
                else 'where the cables leave the cap\'s top')
    n_ = [
        'Option 3 (the owner, 2026-11-10: "it should work like Core cut in half"; the main build): the light sits at the '
        'mouth\'s center and faces up into the shade, so the shade glows in its tint and the light cast down is the bulb\'s. '
        'A Ø50 ring board of 24 mid-power LEDs (two strings of 12 at about 90 mA, about 1,000 lm, about 200 lux under the '
        'lamp) on a black Ø56 x 4.5 carrier, its underside on the rim plane, the LEDs\' faces about 5 above it; a 16/12 '
        'black anodized stem up to the hub; the inside of the shade\'s top white (a white Ø62 disc under the hub, the collar\'s '
        'lip beneath and its flange face painted white); the opal to the rim. Without a lens until a stock side-emitting '
        'ring optic with an IES file is named. Heat test needed: the hub about 6 K warmer than the COB build (estimate).',
        'Hemisphere: the shade hangs mouth down. Its shades swap by hand, with two hands, no tools, and the shade is never '
        'live. ' + swap_,
        'Hanging and leveling, in a 4 in round or octagon outlet box designed for luminaire support (NEC 314.27(A)(2)), at '
        'least 1-1/2 in deep, its ears 3-1/2 in apart. (1) The canopy first: thread the two cables up through its two floor '
        'holes and the cord through its grommet (the cables end in the hub\'s stop sleeves, so the canopy goes on from their '
        'free ends). (2) Hang the plate on one box screw through its slot, splice the driver\'s two input leads to the supply '
        'in the box with listed connectors (UL 486C), 150 or more of each lead in the box, and land the equipment grounding '
        'conductor under the green screw on the plate\'s top face (its cupped washer); then screw the plate to the box. (3) '
        'Thread the cables up through the grippers. Tie or tape the canopy to the two cables 10 to 15 cm below the plate and '
        'keep it there through the leveling and the cord step (left loose it binds on the splayed cables, slides down and can '
        'lift the lamp onto its cord; nearer than 10 the grippers\' plungers are hard to reach). (4) Level it with a shade on '
        '(across the cables nothing adjusts: each shade sets that itself): hold the lamp up, loosen each gripper\'s safety nut, '
        'push its plunger and slide the cable until the rim reads level to 1 degree against a laser line (or measure its two '
        'sides from the table), never by resting a level on the lamp; tighten the safety nuts. Cut the cables about 50 above '
        'the grippers with cable cutters, leaving enough to re-level. The rim at least 480 below the ceiling (nearer, the '
        'cables rub the canopy\'s floor holes). (5) The cord: measure along a cable from ' + cap_top_ + ' to its gripper\'s '
        'lower end, and mark the cord that length plus 2 mm from the same height; clamp it in the two straps with the mark at '
        'the lower strap\'s lower edge (level with the grippers\' lower ends; two screws, a screwdriver from the front). Cut it '
        'about 40 above the upper strap\'s top; ring and strip the jacket 4 above the upper strap\'s top; strip each conductor '
        '11; put them into the two lever splices beside the clamp with the driver\'s LED leads (they come cut and stripped): '
        'the identified conductor, ribbed or printed, to the red lead (+). After any re-leveling, set the cord again. (6) '
        'Untie the canopy, slide it up the cables and the cord (its grommet does not grip) and tighten its two set screws in '
        'turn, a little at a time. By design the cord bows sideways about 2 to 3 cm at mid-drop, more on long drops. '
        'INSPECTION AND SERVICE (UL 1598 11.5.1 relies on this): loosen the canopy\'s set screws and lower it, hold the plate, '
        'and take out the two box screws; never let the plate hang on its leads (2.6 to 2.7 kg on two spliced 18 AWG leads). '
        'To replace the driver the plate comes down, as its input leads are spliced in the box.',
        'The shade is clamped, not hung on a glue joint: the collar\'s flange sits under the crown inside, a ring screws down '
        'over it outside, the acrylic between two silicone rings. A failed bond cannot drop it.',
        'The wall is tint, opal, tint: a tinted shell, a volume-diffusing opal liner and a tinted skin, each formed from cast '
        'sheet on an aluminum mold, nested, closed at the mouth by a tinted rim with a vent. Opal scatters through its depth, '
        'so it still diffuses where it touches the tint (a bead-blasted clear liner would go clear wherever it was bonded). '
        'Nothing white is seen.',
        'Light: the ring board, about 1,000 lm at 2700 K (3000 K for Ice and Haze), CRI 90, on an ERP Power '
        'ESS010W-0180-42-XL (Class 2, FCC Part 15 Class B, 300 mm leads), dimmed 100 % to 1 % by a phase-cut (TRIAC or ELV) '
        'dimmer only: its 0-10 V leads are cut at the factory.',
        'Heat: the low top is the heat sink, no fins: a black anodized aluminum crown 80 across over the collar and an '
        'aluminum cap over the cord grip, the cap\'s top 126 above the rim (today\'s crown 11.5 tall and cap 40 x 14; A\'s and '
        'B\'s even tiers on their sheets). A PEEK ring carries the bayonet\'s pins, so the hub reaches the shade only through it '
        'and air. The ring board makes about 5.9 W; the driver\'s case is estimated at 34 to 41 C in a 25 C room and at most '
        '56 C in 40 C air, against ERP\'s 70 at its Tc point (to measure in the clause 15 test).',
        'Wiring: the driver (ERP ESS010W-0180-42-XL, UL 8750 Recognized Class 2) stands on edge in a steel tray beside the '
        'canopy\'s axis, screwed by its two tabs; the tray and the mounting plate enclose its 120 V input leads, which go up '
        'through the plate into the outlet box and are spliced there, and the tray is the barrier between them and the Class 2 '
        'wiring (UL 1598 6.17.2). Its LED leads come cut to length at the factory and stripped 11. Past the driver the cord '
        'carries the LEDs\' DC, about 33 V (Class 2). The cord: a listed SVT 18/2 pendant cord in a black textile braid, round, '
        '6.0 to 6.5 over its braid (the grommet Ø7.5), one conductor identified (ribbed or printed, UL 1598 5.2.7); its strain '
        'relief is two screwed straps on the clamp\'s channel, each stopping on the channel so the cord is squeezed 1.0 to 1.5 '
        'and no more (UL 1598 5.15.1.2; 156 N for a minute, moving under 1.6, 17.21.1); 2 mm longer than the cables, so it '
        'carries no load: the lamp hangs from two 1/16 in stainless cables, each on a stop sleeve in the hub and a rated cable '
        'gripper on a bracket under the plate (their pull test with the fixture is part of the listing). The plate carries the '
        'grippers, the tray and the clamp; the canopy is a cover only. Box fill: the driver\'s two leads do not count (NEC '
        '314.16(B)(1) Exception). The wiring diagram and its assembly steps: wiring-diagram.pdf in each package, shipped with each lamp (UL 1598 6.15.1.3). To be listed to UL 1598 (hardwired) with its own '
        'shades, each tint in the listing; rated and marked 120 V.',
        'OPEN, for the lab and the supplier: (1) ERP\'s OK for mounting the ESS010W on edge (its datasheet names no '
        'orientation, only "secured on a flat surface through the two mounting tabs"). (2) UL 1598 5.2.1: "All splices and '
        'electrical connections shall be completed at the factory, unless packaging requires partial disassembly"; the cord '
        'is cut to length and spliced on site, which relies on the lab accepting it; the fallback is a factory-connected cord '
        'in set drop lengths. (3) UL 1598 11.5.3: the plate\'s Ø8 lead opening passes neither of its rod tests (one opening '
        'passing a 44.5 rod, or two of 10 cm2 or more passing a 16 rod); 11.5.1 may exempt a luminaire of 4.54 kg or less '
        '(this one 2.6 to 2.7 kg with its canopy): the lab\'s call. A large opening is not drawn: it would open the Class 2 '
        'side to the box; over the tray the driver blocks the rod 0.5 below the plate. (4) Whether the outlet box and the '
        'canopy count as one wiring compartment (the cord\'s splices are 21 or more from the box screws\' slots, which are '
        'wider than 6.17.2.4\'s 1.6). (5) For the clause 15 test, ERP\'s Tc point: on the label face, 0.8 from the tray\'s '
        'inner wall. (6) The green screw\'s thread: the extruded hole gives about 2 to 2.5 full threads against 6.14.2.11\'s '
        'two; a first-article test (17.39, at 1.6 N m) on the prototype list.',
        'Hang over a bar at 750 to 900 centers, the rim 700 to 800 above the counter; over a table, one a table, the rim '
        'about 650 to 750 above it.',
    ]
    if record:
        n_.insert(0, 'SUPERSEDED, A RECORD (V11-17): v2\'s shade and its v9 canopy (the driver in an enclosure under the plate). '
                     'The notes below are the main build\'s, not this record\'s.')
    return n_


NOTES_DOME = notes_dome(None)
NOTES_ORB = [
    'Core (the Orb until round 35): a crystal ball, a 160 tinted ball low in the cup of a 120 x 30 base (round 41), 180 '
    'tall. The ball lifts off: the LED is under a sealed window in the base, so balls swap colour by hand.',
    'Core B, the owner\'s choice (2026-11-09): a ball in a ball. The outer ball is 6 mm tinted cast acrylic, polished '
    'both faces, two halves formed on the existing mould and joined at the equator; the Ø40 port at its foot. Inside it '
    'the core, a Ø140 ball of 3 mm white opal acrylic (Perspex GS 041, Hemisphere\'s opal), concentric with the outer '
    'ball (2026-11-10): a 4 mm gap, a 10 mm band of colour all round (fallback Ø130, a 15 mm band). Its own Ø40 '
    'opening sits on the grommet\'s flange and spigot: the LED lights the opal directly, and the core glows evenly. The core is captive '
    'once the outer halves are joined round it, and the grommet seals the gap for life. Design A (one 9 mm ball frosted '
    'inside) is in git and builds from orb_parts(O_A).',
    'The same materials as the speakers: each tint\'s outer ball is cast in the speaker\'s TruCast code (Ember 2423, Dust '
    '2422, Acid 9097, Poison 2092, Ice 2069, Haze 2287, Fog 0000, Smoke 2074), the chart figure held at the 6 mm wall: a '
    'dosed batch per code, cast to match where stock will not hold it; the chips decide. Haze 2287 may be translucent '
    '(Acme lists it "Violet - Translucent"): Haze is a custom cast for the speaker, and its outer ball would be too.',
    'Colour (the owner, 2026-11-11, on the Core colour test): both lamps\' shells for Dust, Acid and Ice are custom '
    'pours of the same dye at 3x the chart loading, and Smoke a custom pour, not 2074 dark gray; their LEDs 4000 K. Ember '
    '2200 K, Poison and Fog 2700 K, Haze 3000 K. The mix (the owner, 2026-11-17, "Yes for matching when turned off"): '
    'Hemisphere\'s shell denser in Acid 5x, Ice 6x, Ember 1.8x and Haze 1.8x the stock loading; Core\'s ball lighter in '
    'Poison, 0.6x the chart loading; Smoke Hemisphere 1.2x, Core 0.6x (2026-11-16); Dust and Fog as above.',
    'Cordless (the owner, 2026-10-31): three button-top LiFePO4 18650 cells (Power Sonic PSL-FP-IFR18650EC class, 14.4 Wh) '
    'on bare spring contacts in bays milled round the LED, behind a hatch underneath on four captive screws, the user\'s '
    'to replace with standard cells. It charges on its dock or from USB-C underneath at 9 V (USB PD, the 20 W adapter '
    'in the box; CORE-RECHARGE.md), and charges while it runs, about 2.7 hours to 90 % at 1.5 A. About five hours a '
    'charge (the copy until the bench proves more: computed, about 7.8 hours at full brightness, 1.5 W, at the default '
    'charge limit of 90 %, counted by a coulomb counter).',
    'Long life: LiFePO4 keeps about 80 % of its capacity after about 2,000 cycles (ordinary Li-ion about 500); the '
    'charge limit, a battery-management circuit (protection, a coulomb counter, each cell behind back-to-back FETs off '
    'until checked, charging held off below 0 C and above 45 C by the cells\' NTC, thermal foldback) and no exposed '
    'live contacts. To be listed as one product to UL 153 with Supplement SA; the cells to IEC 62133-2 and UN 38.3.',
    'Touch the black ring: tap to switch, hold to dim, 2200 to 2700 K as it dims. IP44: the base sealed by O-rings at '
    'the window, the chassis and the hatch, the USB-C receptacle sealed; with the ball on or off.',
    'Black, so the tint is the only colour: the base black cast acrylic, polished, over an aluminium chassis and a steel '
    'ballast; the ring, the port\'s lining and the hatch black anodised aluminium.',
]
TOUCHING_DOME = [('pins', 'ring'), ('rim', 'shell'), ('rim', 'skin'), ('rim', 'liner'), ('cob', 'hub'), ('gland', 'crown'),
                 ('crown', 'hub'), ('clamp', 'collar'), ('gaskets', 'collar'), ('gaskets', 'clamp'), ('gaskets', 'shell'),
                 ('gaskets', 'skin'), ('reflector', 'hub'), ('strap', 'canopy'), ('enclosure', 'strap'), ('gaskets', 'liner'),
                 # v6 (the v5 check's (10)): no fixing pair is exempt. Threads are drawn in holes at their major Ø, the cables
                 # in Ø2.4 holes, so the fixings touch at most; fixings_check.py checks them at zero tolerance. The silicone
                 # and the slip washer stay listed (squeezed, and drawn on the spherical seats)
                 ('slip-washer', 'gaskets'), ('slip-washer', 'clamp')]
# the builds without the v6 fixings (dome_pendant_v2.py, Hemisphere South): their pins in Ø2.5 taps and the round-43 cable
TOUCHING_DOME_LEGACY = TOUCHING_DOME + [('suspension', 'gland'), ('suspension', 'canopy'), ('suspension', 'cord'), ('pins', 'hub'),
                                       ('suspension', 'canopy-grip')]   # v8: the round-43 cable through the canopy's new grip
TOUCHING_ORB = [('grommet', 'shell'), ('grommet', 'core'), ('window', 'base'), ('seat', 'base'), ('ring', 'base'), ('led', 'board'),
                ('chassis', 'base'), ('ballast', 'chassis'), ('ballast', 'base'), ('cable', 'base'), ('board', 'chassis'),
                ('foot-ring', 'base'), ('cells', 'holder'), ('hatch', 'base'), ('usb', 'base'), ('cable', 'hatch'),
                ('led', 'chassis'), ('holder', 'base'), ('holder', 'hatch'), ('ballast', 'hatch'), ('chassis', 'board'),
                ('window', 'led'), ('usb', 'hatch'), ('pads', 'chassis'), ('pads', 'ring'), ('pads', 'base'),
                ('pins', 'pinboard'), ('pinboard', 'chassis'), ('dock-contacts', 'dock'), ('base', 'dock'),
                ('foot-ring', 'dock'), ('dock-cable', 'dock'), ('pins', 'dock-contacts')]


# Hemisphere South, DROPPED (the owner, 2026-10-25: "Get rid of south altogether and just call it hemisphere."). Kept as a record.
# Hemisphere South: the same cover turned over, a bowl, on a rod from the ceiling. Round 36 (the owner: "The southern
# hemisphere dome is supposed to have nothing below the dome"): everything that holds or feeds the light is inside the
# bowl or above it. The hub sits in the collar, its bottom a black cap flush with the collar's end; a ring of LEDs on
# its inner face lights the bowl from its bottom, up; its heat goes up a heat pipe in the rod (gravity returns the
# fluid, as it should with the heat at the bottom) to fins on the rod above the lid, in room air. The shade is the same
# as North's: it fits on from inside, by the collar's second set of slots.
S = dict(N, led=(60.0, 18.0, 48.0),               # the LED ring board: OD, ID, its face (cover frame)
         # round 37 (the owner: "South ring: remove it: a shade made for South alone"): South's own shade. The shell
         # and the opal liner are closed; only the inner tinted skin has a crown hole, set 6 in from the liner (was 1)
         # so the collar's flange fits between them, behind the opal
         skin_gap=6.0,
         collar=(96.0, 82.0, 48.0, 71.0),        # OD, ID, z inner end (the entry, toward the mouth), z at the flange
         south_pins=(54.0, 0.0),                 # the pins' height and the slots' angle (one set: South's alone)
         core=(62.0, 48.0, 74.0),                # the hub core: OD, z0 (the board on its face), z1 (behind the opal)
         ring=(62.0, 78.0, 48.5, 62.0),          # the PEEK pin carrier
         rod=(16.0, 12.0),                       # aluminium tube, OD and ID, black anodised, the heat pipe inside it
         pipe=8.0,                               # the heat pipe: copper-water, 8 across
         sink=(90.0, -120.0, -80.0, 18, 1.8),    # the fins on the rod, above the lid: OD, z0, z1 (cover frame), count, t
         lid=(196.0, 3.0, 17.0),                 # the frosted lid: OD, thickness, the rod's hole
         drop=450.0)                             # from the bowl's rim to the canopy
SOUTH_LIGHT = (0.0, 0.0, 0.0)                    # the lid's centre: the ceiling wash's source (the bowl's frame)


def _flip(solid):
    """The cover's frame to the bowl's: turned over about x, the rim at z 0 and the bowl below it."""
    from build123d import Rot
    return Rot(180, 0, 0) * solid


def south_cover_parts(p=S):
    """Round 37: South's own shade, nothing under it. From outside: a tinted shell and an opal liner, both closed;
    then, 6 in, a tinted skin with the crown hole. The collar's flange sits on the skin's outside, between it and the
    opal, so from below the opal hides it (a soft shade at most, never an edge); a clamp ring screws down on the skin's
    inside, on silicone both sides. The skin carries the shade on metal (mechanically, as round 35's L1 asks); the shell
    and the liner are welded to the skin with polymerising acrylic cement at the rim and round the crown, acrylic to
    acrylic, as an aquarium's seams are (no metal-to-acrylic bond carries load)."""
    R, t = p['R'], p['shell']
    r_si = R - t
    r_l = r_si - p['gap']                        # the liner's outside
    r_k = r_l - p['liner'] - p['skin_gap']       # the skin's outside
    r_ki = r_k - p['skin']                       # the skin's inside
    co, ci, cz0, cz1 = p['collar']
    fr = p['flange_r']
    hole = cyl('z', (0, 0), co + 0.4, 0, R + 5)
    # the spheres turned a quarter about x, so their poles lie on the rim (cut away) and not at the closed crown, where
    # the mesh's pole drew a black dot under the bowl (round 37's first render)
    from build123d import Rot
    q = Rot(90, 0, 0)
    shell = q * ball(R, t, (0, 0, 0)) - box(-R - 1, -R - 1, -R - 1, R + 1, R + 1, 0)
    liner = q * ball(r_l, p['liner'], (0, 0, 0)) - box(-R - 1, -R - 1, -R - 1, R + 1, R + 1, 4)
    skin = q * ball(r_k, p['skin'], (0, 0, 0)) - box(-R - 1, -R - 1, -R - 1, R + 1, R + 1, 0) - hole
    rim = cyl('z', (0, 0), 2 * (r_si - 0.2), 0, 3.8) - cyl('z', (0, 0), 2 * (r_k + 0.2), -1, 5)
    # the crown weld: a ring of tinted acrylic filling the gap between the skin and the liner round the flange (the
    # liner, the ring and the skin welded as one), so the outer layers hang on acrylic joints over 5,000 mm2
    weld = _sphere_band(r_l - p['liner'] - 0.01, r_k + 0.01, fr + 2, fr + 16)
    tube = cyl('z', (0, 0), co, cz0, cz1) - cyl('z', (0, 0), ci, cz0 - 1, cz1 + 1)
    flange = _sphere_band(r_k + 4.5, r_k + 1.0, ci / 2, fr)
    collar = tube + flange
    pz, w, rs = p['pin_z'], 5.0, ci / 2 + 4.5
    zs, off = p['south_pins']
    for a in (off, off + 120, off + 240):
        collar = collar - at(a, box(ci / 2 - 2, -w / 2, cz0 - 1, rs, w / 2, zs + 7.5))                    # the entry
        collar = collar - sector(ci / 2 - 2, rs, a, a + p['turn'], zs + 2.5, zs + 7.5)                     # the turn
        collar = collar - at(a + p['turn'], box(ci / 2 - 2, -w / 2, zs - 2.5, rs, w / 2, zs + 7.5))        # the notch
    gasket_out = _sphere_band(r_k + 1.0, r_k, co / 2 + 0.2, fr)
    gasket_in = _sphere_band(r_ki, r_ki - 1.0, co / 2 + 0.2, fr)
    clamp = _sphere_band(r_ki - 1.0, r_ki - 6.0, co / 2, fr)
    note_formed = ('drape-formed from cast sheet over an aluminium mould, trimmed and polished; the prototypes are formed on '
                   'the production moulds')
    return [
        Part('shell', shell, Machined('acrylic-formed', 'formed', setup_usd=1500.0), finish='body', group='cover',
             notes=['South\'s own: the outside, closed at the crown (North\'s shell mould, untrimmed there): 10 mm tinted '
                    'cast sheet ' + note_formed]),
        Part('liner', liner, Machined('acrylic-opal-formed', 'formed', setup_usd=1200.0), finish='liner', group='cover',
             inside=True,
             notes=['3 mm opal, closed at the crown (North\'s liner mould): it hides the collar\'s flange from below; '
                    + note_formed]),
        Part('skin', skin, Machined('acrylic-formed', 'formed', setup_usd=1200.0), finish='body', group='cover',
             notes=['South\'s own mould (6 in from the liner): 3 mm tinted cast sheet, the crown hole for the collar; it '
                    'carries the shade on the collar\'s flange and clamp ring']),
        Part('weld', weld, Machined('cast-acrylic', 'lathe'), finish='body', group='cover', inside=True,
             notes=['a tinted acrylic ring turned to fill the gap round the flange: the skin, this ring and the liner '
                    'welded with polymerising acrylic cement (Acrifix 192 kind); the shell and the liner welded at the rim']),
        Part('rim', rim, Machined('cast-acrylic', 'lathe'), finish='body', group='cover',
             notes=['closes the three layers at the mouth, welded and polished with them; a press-in ePTFE vent in its '
                    'face']),
        Part('collar', collar, Machined('aluminium', 'lathe'), finish='anodised', group='cover', inside=True,
             notes=['aluminium 6061, black anodised: its flange on the skin\'s outside, behind the opal (unseen); its '
                    'tube inside the bowl, with three L-slots open at the inner end for South\'s pins']),
        Part('clamp', clamp, Machined('aluminium', 'lathe'), finish='anodised', group='cover', inside=True,
             notes=['aluminium, black anodised: screwed onto the collar inside the bowl, on silicone, clamping the skin']),
        Part('gaskets', gasket_in + gasket_out, Bought('south-gaskets'), finish='silicone', group='cover', inside=True),
        Part('vent', None, Bought('hemi-vent')),
        Part('welding', None, Bought('south-weld')),
    ]


def south_parts(p=S):
    """Hemisphere South (dropped 2026-10-25, kept as a record), built in the cover's frame and turned over: the cover's parts as North's; inside the collar
    the hub core with its PEEK ring and pins, the LED ring on its inner face; the rod up the axis, the heat pipe in it,
    the fins on it above the lid, and the canopy. Nothing below the bowl but the shade's own collar end and clamp ring
    and the hub's flush cap."""
    od, z0, z1 = p['core']
    lo, li, lz = p['led']
    sd, sz0, sz1, nf, ft = p['sink']
    ri, ro, rz0, rz1 = p['ring']
    zs, off = p['south_pins']
    rdo, rdi = p['rod']
    core = cyl('z', (0, 0), od, z0, z1) - cyl('z', (0, 0), rdo, z0 - 1, z0 + 20)        # the rod's socket, 20 deep
    core = core - cyl('z', (0, 0), p['pipe'] + 0.2, z0 + 19, z0 + 30)                    # the heat pipe's evaporator
    ring = cyl('z', (0, 0), ro, rz0, rz1) - cyl('z', (0, 0), ri, rz0 - 1, rz1 + 1)
    pins = None
    for a in (off, off + 120, off + 240):
        pin = at(a + p['turn'], cyl('x', (0, zs), 4.0, ri / 2 + 2, p['collar'][1] / 2 + 2.5))
        pins = pin if pins is None else pins + pin
    led = cyl('z', (0, 0), lo, lz - 1.6, lz) - cyl('z', (0, 0), li, lz - 3, lz + 1)
    rod = cyl('z', (0, 0), rdo, -p['drop'], z0 + 20) - cyl('z', (0, 0), rdi, -p['drop'] - 1, z0 + 21)
    pipe = cyl('z', (0, 0), p['pipe'], sz0 - 10, z0 + 30)
    fins = cyl('z', (0, 0), 30, sz0, sz1) - cyl('z', (0, 0), rdo + 0.2, sz0 - 1, sz1 + 1)
    for i in range(nf):
        fins = fins + at(360.0 * i / nf, box(14.0, -ft / 2, sz0, sd / 2, ft / 2, sz1))
    fins = fins & (cyl('z', (0, 0), sd, sz0, sz1) - cyl('z', (0, 0), rdo + 0.2, sz0 - 1, sz1 + 1))
    ld, lt, lh = p['lid']
    lid = cyl('z', (0, 0), ld, -lt, 0.0) - cyl('z', (0, 0), lh, -lt - 1, 1)
    zc = -p['drop']
    cnd, cnh = p['canopy']
    canopy = cyl('z', (0, 0), cnd, zc - cnh, zc) - cyl('z', (0, 0), cnd - 6, zc - cnh + 3, zc + 1)
    driver = box(-42, -28.5, zc - 6 - 29.5, 42, 28.5, zc - 6)
    parts = south_cover_parts(p) + [
        Part('hub', core, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=['aluminium 6061, black anodised: the core, turned from bar, inside the collar; its outer face behind '
                    'the opal, unseen; the LED ring on its inner face; the rod in a 20 deep socket, the heat pipe\'s evaporator in its bore on thermal paste']),
        Part('ring', ring, Machined('peek', 'lathe'), finish='trim', group='fixture', inside=True,
             notes=['PEEK, unfilled: the thermal break, at the collar\'s inner end; it carries the pins (into the '
                    'collar\'s second set of slots) and the detent']),
        Part('pins', pins, Bought('dome-pins'), finish='anodised', group='fixture'),
        Part('led', led, Bought('south-led'), finish='led', group='fixture', inside=True),
        Part('rod', rod, Bought('south-rod'), finish='anodised', group='fixture',
             notes=['aluminium tube 16 x 2, black anodised: down the bowl\'s axis into the hub; the heat pipe and the '
                    'wires inside it']),
        Part('pipe', pipe, Bought('south-heatpipe'), finish='steel', group='fixture', inside=True, render=False),
        Part('fins', fins, Machined('aluminium', 'extrusion', setup_usd=0.0), finish='anodised', group='fixture',
             notes=['the heat sink, on the rod 80 above the lid, in room air: 40 cut from a radial extrusion 90 across, '
                    '18 fins, black anodised, clamped on the rod over the heat pipe\'s condenser; its warm air rises '
                    'to the ceiling, away from the acrylic']),
        Part('lid', lid, Machined('cast-acrylic', 'mill'), finish='lid', group='lid',
             notes=['3 mm clear cast acrylic, bead-blasted both faces: the dust lid, lying on the rim on three small '
                    'clear silicone bumpers; it lifts up the rod to be wiped. Its light is the ceiling wash']),
        Part('canopy', canopy, Machined('cast-acrylic', 'lathe'), finish='trim', group='canopy',
             notes=['150 x 50, black cast acrylic, polished, as North\'s: over the driver and a steel junction-box strap; '
                    'the rod hangs from the strap through a listed swivel so it hangs plumb']),
        Part('driver', driver, Bought('south-driver'), finish='steel', group='canopy', inside=True, render=False),
        Part('plunger', None, Bought('dome-plunger')),
        Part('listing', None, Bought('moon-listing')),
    ]
    for pt in parts:
        if pt.solid is not None:
            pt.solid = _flip(pt.solid)
    return parts


NOTES_SOUTH = [
    'A bowl, opening up, on a slim rod from the ceiling, with nothing below it (the owner, rounds 36 and 37): its own '
    'shade, closed underneath. Outside a tinted shell and an opal liner, both closed; inside them a tinted skin that '
    'carries the shade on the collar, whose flange the opal hides. North\'s and South\'s shades no longer swap (the '
    'owner accepts it).',
    'The light: a ring of mid-power LEDs on the hub\'s inner face at the bottom of the bowl, facing up. About 57 % of '
    'it leaves through the mouth and the frosted lid as a soft wash on the ceiling; the rest falls on the bowl\'s wall, '
    'which glows in its tint. Twice North\'s light: about 1,150 lm.',
    'The heat: up a copper heat pipe in the rod to black fins on the rod 80 above the lid, in room air, so the warm '
    'air rises to the ceiling, not past the acrylic. The PEEK ring keeps the hub off the collar. See '
    'hemisphere_thermal.py and the test plan (README, rounds 35 and 36).',
    'The dust lid: 3 mm frosted acrylic on the rim, lifted up the rod to wipe.',
    'Hang with the rim 450 to 600 below a ceiling of 2.6 to 3.2 m, so the wash spreads; not over a table (its light is '
    'on the ceiling).',
]
TOUCHING_SOUTH = TOUCHING_DOME_LEGACY + [('weld', 'skin'), ('weld', 'liner'), ('weld', 'collar'), ('rod', 'hub'), ('led', 'hub'), ('rod', 'led'), ('rod', 'lid'), ('pipe', 'rod'),
                                  ('pipe', 'hub'), ('fins', 'rod'), ('gland', 'fins'), ('fins', 'hub')]


# The triangle of chords Core's cells lie on (round 41; orb_parts), grown or shrunk for the parts round them
def _chords(a, L, d, grow):
    out = None
    for k in range(3):
        b = at(-10.0 + 120.0 * k, box(a - grow - 3.0, -L / 2 - grow - 4.4, -2, 70, L / 2 + grow + 4.4, 31))
        out = b if out is None else out + b
    return out
