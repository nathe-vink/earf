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
TOP_TIERS = {
    'today': dict(top=None, crown=[(80.0, 100.5, 112.0)], gland=(40.0, 112.0, 126.0)),   # today's top, with check 3's fixings
    'A': dict(top=103.33, clamp=104.0, band_r=58.0, taper=1.0, crown=[(80.0, 100.5, 114.67)], gland=(56.0, 114.67, 126.0)),
    'B': dict(top=100.5, clamp=104.0, band_r=58.0, taper=1.0, crown=[(80.0, 100.5, 109.0), (56.0, 109.0, 117.5)], gland=(32.0, 117.5, 126.0),
              cable_r=18.5, key=None, magnet=(14.0, 270.0, 1.5)),
}
# The top's fixings (check 3, 2026-11-24; for today's top, A and B alike). The cord grip: Lapp 53112005 as its datasheet
# gives it (DB53112005EN, as the reviewer read it; the sheet not opened here): M12 x 1.5, 16 across the flats, 17.6 across
# the corners, 32.5 overall, 12 of thread, cord 3.5 to 7. Its body is drawn as the hex (5) and a round dome to the overall
# height, its outline to confirm on the sheet. The hub is tapped M12 13 deep from the neck's top (101.5), so 9.5 of its
# thread are in the hub and the cord's pull goes into the hub. The crown sits on the neck metal to metal (no pad, which
# would creep under the screws and the grip; a film of thermal compound), its 2.5 floor held down by three M2.5 countersunk
# screws at r 9.25, 90/210/330 deg, into the neck, their heads inside the pocket.
# v6 (2026-11-24, the v5 check's (1) to (8)): THE HANGING. Two cables, symmetric about the axis (0 and 180 deg), at r 16
# in today's top and A and r 18.5 in B (beside its Ø32 cap, 1.3 clear): 1/16 in (1.59) 7x7 stainless cable (Cable Grippers
# Inc.'s bulk cable). The hub end: a Nicopress 871-1-C copper stop sleeve swaged on (13/64 in x 7/32 in, about Ø5.2 x 5.6,
# 430 lb typical holding strength, as a distributor's copy of Nicopress's table gives it; tool 51-C-887), bearing up under
# a Ø5.6 counterbore 6 deep in the hub's bottom face, the cable up a Ø2.4 hole through the hub, the crown and the cap
# (today, A) or beside the cap (B); the white disc closes the counterbores. No turning, no thread. The canopy end: a Cable
# Grippers MGR-M10-MM gripper on each cable (their chart: 17.1 long without the plunger, Ø11.9 body, M10 thread; MGR on
# 1/16 in stainless 7x7: 312 lb minimum break in their independent tests, 50 lb a cable at their 5:1), threaded up into a
# steel bracket under the canopy strap, its plunger down, 1 above a Ø6 hole in the canopy's floor through which the cable
# passes: push the plunger from below with a fingertip to let the cable slide, let go and it holds. The cables splay from
# their exits to the grippers at r 40 (clear of the driver's enclosure). Each assembly is pull-tested.
# The cord (v6, (3)): set 2 mm longer than the cables between its grips, so it carries no load (the cables stretch about
# 0.05 mm under the lamp); hung, it bows about 21 mm to one side over the drop: drawn so.
# The cap (v6, (7), (8)): today's and A's caps keyed to the crown by a Ø2 dowel and held down by a Ø2 x 2 magnet over a steel
# disc, both at r 15.5 (2.5 from the crown's Ø24 pocket); the cap is the handle in a swap. B's Ø32 cap is held by a Ø1.5 x 2
# magnet only (r 14, 1.25 from the pocket and the fillet): B's handle in a swap is its Ø56 tier.
# The grip is turned by a slotted (pass-through) 16 socket, the cord in its slot: the dome nut off, the body torqued into
# the hub, the dome nut on and tightened on the cord. The order: the cables up through the hub from below, their sleeves
# into the counterbores; the white disc; the crown down over the cables onto the neck, its three screws; the grip, as above;
# the cap down over the cord (and the cables) onto its dowel; the cables through the canopy's floor and the grippers, the
# lamp levelled; the cord's 2 mm of slack and the canopy's grip tightened. In a swap, hold the cap (B: the Ø56 tier):
# lift, turn, lower a hand's width onto the tether, unclip its snap at the hub.
GRIP = dict(thread=(12.0, 12.0), tap=13.0, hex=(16.0, 17.6, 5.0), overall=32.5, pocket=24.0, cap_pocket=20.0, lid=1.0,
            floor=(101.5, 104.0), screws_r=9.25, screws_a=(90.0, 210.0, 330.0), cable_r=16.0, cables=(0.0, 180.0),
            cable=1.59, sleeve=(5.16, 5.56), cbore=(5.6, 6.0), gripper_r=40.0,
            key=(15.5, 90.0, 2.0), magnet=(15.5, 270.0, 2.0),
            # v6 (the v5 check's (4)): the tether, 1.5 mm 7x7 stainless, 125 between its ends: an M4 button screw radially
            # into the hub (z 80, 90 deg) holding a crimped loop (the hub's eye), a 4 x 40 stainless snap hook (DIN 5299 C)
            # clipped to it, the rope from the snap round the lip's top to an M3 button screw through the collar's wall
            # (z 70, 270 deg)
            tether=dict(hub=(90.0, 80.0), collar=(270.0, 70.0), length=125.0, rope=1.5, snap=(4.0, 40.0, 14.0)))
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
        # v6 (the v5 check's (4)): the tether's collar end, an M3 button screw through the wall at z 70, 270 deg (tapped through
        # from outside, under the shade's flange; drawn at its major Ø); the v5 eye tab dropped (it would tear at about 0.5 kN)
        if p.get('fixings'):
            ca6_, cz6_ = GRIP['tether']['collar']
            collar = collar - at(ca6_, cyl('x', (0, cz6_), 3.0, ci / 2 - 1, co / 2 + 1))
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
        collar = collar - at(a, box(ci / 2 - 2, -w / 2, pz - 10.5, rs, w / 2, cz1 + 1))                 # the entry
        collar = collar - sector(ci / 2 - 2, rs, a, a + p['turn'], pz - 10.5, pz - 5.5)                    # the turn
        collar = collar - at(a + p['turn'], box(ci / 2 - 2, -w / 2, n0, rs, w / 2, n1))                    # the notch
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
                    'skin; three blind L-slots with T-ended notches (the quarter-turn bayonet, 30 deg) work either way up; '
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
                     'craze it): held by the shoulder and a nylon-tipped set screw through the ring into the collar') if sh_ else
                    ('aluminium, black anodised: screwed onto the collar over the crown, its spherical face on a silicone '
                     'ring, to a torque the shade maker sets (the acrylic is clamped between two silicone rings, never metal '
                     'on acrylic); no thread-locker near acrylic (review 2026-11-01: anaerobics craze it): held by the '
                     'silicone\'s preload and a nylon-tipped set screw through the ring into the collar')]),
        Part('gaskets', gasket_in + gasket_out, Bought('hemi-gaskets-4' if sh_ else 'hemi-gaskets'), finish='silicone', group='cover',
             notes=(['PROPOSAL (v5): four silicone rings, Shore 40: two 1.3 gaskets and two shims in the crown\'s air gaps, drawn at 1.0, '
                     'with a 0.25 PTFE slip washer under the clamp ring\'s band (it turns against it while tightening). PROCESS: the shade '
                     'maker measures each crown\'s stack (cast sheet is held to only ±(0.4 + 0.1t), ISO 7823-1: ±0.7, ±1.0, ±0.7 here) and '
                     'picks the two shims from 0 (left out), 0.5, 1.0, 1.6, 2.2 and 2.9 so the squeeze lands at 20 to 35 % (the whole '
                     'RSS range; at the thinnest worst-case stack it reaches 38 %)'] if sh_ else
                    ['two silicone gaskets, 1.0, the acrylic clamped between them; the clamp ring tightened to the shade maker\'s torque'])),
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
        pin = at(a + p['turn'], cyl('x', (0, pz), sd_, ro / 2, tip) + cyl('x', (0, pz), td, tin, ro / 2))
        pins = pin if pins is None else pins + pin
        # (check 3, (l)) the pin's thread through a Ø3.2 clearance in the PEEK, tapped M3 (Ø2.5) in the hub
        ring = ring - at(a + p['turn'], cyl('x', (0, pz), 3.2, ri / 2 - 1, ro / 2 + 1))
        core = core - at(a + p['turn'], cyl('x', (0, pz), 3.0 if p.get('fixings') else 2.5, tin, ro / 2 + 1))   # v6: tapped M3, drawn at its major Ø
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
        crown = (crown - cyl('z', (0, 0), nd + 0.2, sz0 - 1, f0_) - cyl('z', (0, 0), td_ + 0.5, f0_ - 1, f1_ + 0.1)
                 - cyl('z', (0, 0), pk_, f1_, g0_ + 1))
        from build123d import Cone, Pos, Align, RegularPolygon, extrude, Solid, Plane, Vector as V3
        al_ = (Align.CENTER, Align.CENTER, Align.MIN)
        # v6 (the v5 check's (1)): two cables at r cr_ (0 and 180 deg), each from a Nicopress stop sleeve bearing under a
        # Ø5.6 x 6 counterbore in the hub's bottom face (the white disc closes it), up a Ø2.4 hole through the hub and the
        # crown, its exit rounded, and through the cap's lid (today, A) or beside the cap (B)
        cxy_ = [(cr_ * math.cos(math.radians(a_)), cr_ * math.sin(math.radians(a_))) for a_ in GRIP['cables']]
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
        # v6 (the v5 check's (4)): the shade's tether. An M4 button screw radially into the hub (z 80, 90 deg; above the lip's
        # 75 in the lift, under the PEEK ring's 86) clamps a crimped loop of 1.5 rope, the hub's eye; a 4 x 40 stainless snap
        # hook (DIN 5299 C) clipped to it stands on the lip's top along the bore; from the snap the rope lies round the lip
        # (under the pins and the land) to an M3 button screw through the collar's wall (z 70, 270 deg; its hole tapped
        # through from outside, under the shade's flange). 125 between the screws: it lets the shade be turned and lowered
        # 100 before it goes taut; in a swap, unclip the snap at the hub
        td6_ = GRIP['tether']; rr_ = td6_['rope'] / 2
        ha_, hz_ = td6_['hub']; ca6_, cz6_ = td6_['collar']
        def _rad(a, r, z):
            return V3(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), z)
        def _rod(p0, p1, rad):
            dv = p1 - p0
            return Solid.make_cylinder(rad, dv.length, Plane(origin=p0, z_dir=dv))
        def _radial(a, r0, r1, z, rad):
            return _rod(_rad(a, r0, z), _rad(a, r1, z), rad)
        hs_ = _radial(ha_, 25.0, 31.0, hz_, 2.0) + _radial(ha_, 31.0, 33.2, hz_, 3.8)          # M4 x 6 + its button head
        core = core - _radial(ha_, 24.9, 31.1, hz_, 2.0)                                     # tapped M4 (major Ø)
        cs_ = _radial(ca6_, 39.0, 41.0 + 4.5, cz6_, 1.5) + _radial(ca6_, 39.15, 40.85, cz6_, 2.85)   # M3 x 6 through the 7 wall + head
        # the snap: a 4 mm wire loop 40 x 14, upright, along the bore (its ends at r 38.8), from the hub's eye toward the collar's screw
        sw_, sl_, sh_ = td6_['snap']; zs0_ = 66.0 + sw_ / 2 + 0.3; rs_ = 38.8   # its ends at r 38.8, its middle at r 33.3
        a0_ = ha_ + 6.0; a1_ = a0_ + 2 * math.degrees(math.asin(sl_ / 2 / rs_))
        P_ = [_rad(a0_, rs_, zs0_), _rad(a1_, rs_, zs0_), _rad(a1_, rs_, zs0_ + sh_ - sw_), _rad(a0_, rs_, zs0_ + sh_ - sw_)]
        snap = None
        for k_ in range(4):
            seg_ = _rod(P_[k_], P_[(k_ + 1) % 4], sw_ / 2) + (Pos(P_[k_]) * Solid.make_sphere(sw_ / 2))
            snap = seg_ if snap is None else snap + seg_
        # the hub's eye (a crimped loop) from the screw's head down to the snap's near top corner
        eye = _rod(_rad(ha_, 33.4, hz_), P_[3], rr_) + (Pos(_rad(ha_, 33.4, hz_)) * Solid.make_sphere(rr_ + 0.3))
        # the rope: from the snap's far bottom corner round the lip at r 37.2 (on its top, z 66.75) to the collar's screw
        zr_ = 66.0 + rr_; pts_ = [P_[1]]
        n_ = 10
        for k_ in range(n_ + 1):
            pts_.append(_rad(a1_ + (ca6_ - a1_) * k_ / n_, 37.2, zr_))
        pts_.append(_rad(ca6_, 38.8, cz6_))
        rope = None
        for k_ in range(len(pts_) - 1):
            seg_ = _rod(pts_[k_], pts_[k_ + 1], rr_)
            rope = seg_ if rope is None else rope + seg_
        tether_ = hs_ + cs_ + snap + eye + rope
        tlen_ = sum((pts_[k_ + 1] - pts_[k_]).length for k_ in range(len(pts_) - 1)) + sl_ + (P_[3] - _rad(ha_, 33.4, hz_)).length
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
        # v6: each cable straight up from its sleeve to where it leaves the top, then splayed to its gripper at r 40 in the
        # canopy, through the gripper and its tail 15 above it (cut and tucked); the grippers' plungers 1 above the floor
        gr_ = GRIP['gripper_r']; susp = sleeves
        grippers = brackets = None
        zg0_ = zc + 3.0 + 1.0                        # the plunger's tip, 1 above the floor's top
        for (x_, y_), a_ in zip(cxy_, GRIP['cables']):
            gx_, gy_ = gr_ * math.cos(math.radians(a_)), gr_ * math.sin(math.radians(a_))
            susp = (susp + cyl('z', (x_, y_), cbl_, z0 + cbh_, cex_ + 0.5)
                    + _rod(V3(x_, y_, cex_), V3(gx_, gy_, zg0_), cbl_ / 2) + cyl('z', (gx_, gy_), cbl_, zg0_, zg0_ + 17.1 + 15.0))
            # the gripper as Cable Grippers' chart gives it: a plunger Ø6 x 2, the body Ø11.9, the M10 thread 12.6 at its top
            g_ = (cyl('z', (gx_, gy_), 6.0, zg0_, zg0_ + 2.0) + cyl('z', (gx_, gy_), 11.9, zg0_ + 2.0, zg0_ + 6.5)
                  + cyl('z', (gx_, gy_), 10.0, zg0_ + 6.5, zg0_ + 19.1))
            g_ = g_ - cyl('z', (gx_, gy_), cbl_ + 0.1, zg0_ - 1, zg0_ + 20)
            grippers = g_ if grippers is None else grippers + g_
            # its bracket: a 1.6 steel L under the strap, the foot at the gripper's thread with an M10 lock nut above it
            sx_ = 1.0 if gx_ > 0 else -1.0
            zf_ = zg0_ + 12.0
            br_ = (box(min(gx_ - 7 * sx_, gx_ + 8.6 * sx_), -8.0, zf_, max(gx_ - 7 * sx_, gx_ + 8.6 * sx_), 8.0, zf_ + 1.6)
                   + box(min(gx_ + 7 * sx_, gx_ + 8.6 * sx_), -8.0, zf_, max(gx_ + 7 * sx_, gx_ + 8.6 * sx_), 8.0, zc + cnh - 1.6))
            br_ = br_ - cyl('z', (gx_, gy_), 10.0, zf_ - 1, zf_ + 3)
            nut_ = cyl('z', (gx_, gy_), 16.0, zf_ + 1.6, zf_ + 6.6) - cyl('z', (gx_, gy_), 10.0, zf_, zf_ + 8)
            br_ = br_ + nut_
            brackets = br_ if brackets is None else brackets + br_
    # v6 (the v5 check's (2)): the canopy right side up: open at the top against the ceiling, its 3 floor closed below
    # (the cord's gland in its centre, the two cables through Ø6 holes at r 40, the grippers' plungers 1 above them), held
    # to the strap by two flush black set screws through its wall into the strap's bent-down ends. The strap (1.6 steel)
    # screwed to the junction box carries the load: the grippers on their brackets under it, the driver's steel enclosure
    # hung from it across the cables' line (64 along it, 92 across)
    canopy = cyl('z', (0, 0), cnd, zc, zc + cnh) - cyl('z', (0, 0), cnd - 6, zc + 3.0, zc + cnh + 1)
    canopy = canopy - cyl('z', (0, 0), 12.5, zc - 1, zc + 4)
    if tt_:
        for a_ in GRIP['cables']:
            canopy = canopy - cyl('z', (gr_ * math.cos(math.radians(a_)), gr_ * math.sin(math.radians(a_))), 6.0, zc - 1, zc + 4)
    ztop = zc + cnh
    hw_ = cnd / 2 - 3.0 - 0.5                     # the strap's ends 0.5 inside the canopy's wall
    strap = (box(-hw_ + 1.6, -11, ztop - 1.6, hw_ - 1.6, 11, ztop) + box(-hw_, -8, ztop - 16, -hw_ + 1.6, 8, ztop)
             + box(hw_ - 1.6, -8, ztop - 16, hw_, 8, ztop))
    setsc_ = cyl('x', (0, ztop - 8), 4.0, -cnd / 2, -hw_ + 1.6) + cyl('x', (0, ztop - 8), 4.0, hw_ - 1.6, cnd / 2)
    canopy = canopy - setsc_
    strap = strap - setsc_
    ez1_ = ztop - 1.6; ez0_ = ez1_ - 34.0
    encl = box(-32, -46, ez0_, 32, 46, ez1_) - box(-31, -45, ez0_ + 1, 31, 45, ez1_ - 1)
    driver = box(-28.5, -42, ez0_ + 2, 28.5, 42, ez0_ + 2 + 29.5)
    return cover_parts(p) + [
        Part('hub', core, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=['aluminium 6061, black anodised: the core, turned from bar. The COB on its holder at the top of the 46 '
                    'bore (22 up: the cut-off, about 46 deg from the vertical), the reflector in the bore, the PEEK ring '
                    'round it, the crown on its neck (metal to metal, a film of thermal compound, no pad); a 10 bore for the wires']),
        Part('ring', ring, Machined('peek', 'lathe'), finish='trim', group='fixture', inside=True,
             notes=['PEEK, unfilled (0.25 W/m K), black: the thermal break. It carries the three pins and the detent, so '
                    'the cover touches the fixture only through it. Review 2026-11-01: its 81.6 OD is the centering land '
                    'in the collar\'s 82 bore (0.2 diametral), three Ø3.2 clearance holes for the pins\' threads']),
        Part('pins', pins, Bought('dome-pins'), finish='anodised', group='fixture',
             notes=['stainless shouldered pins: Ø4 shoulder 4.2 long, M3 thread 15.8, screwed through the PEEK into the '
                    'hub (6 of thread in the aluminium, a pre-applied nylon patch, no anaerobic locker); 4.0 of engagement in the '
                    'collar\'s slots']),
        *([] if tt_ else [Part('tether', None, Bought('hemi-tether'))]),
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
                     'the cord grip and its socket, two Ø2.4 bores for the suspension cables (bare 1.5)' if tt_ else
                     'the heat sink (round 41; the fins until then), round 32f\'s low top: 80 across, 11.5 tall over the '
                    'collar') + ', turned from 6061 bar, black anodised (emissivity about 0.85: half its loss is radiation), on '
                    'the core\'s neck ' + ('metal to metal' if tt_ else 'on a thermal pad') + ', 0.5 clear of the PEEK ring and the collar']),
        Part('gland', gland, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=[(f'PROPOSAL ({("even tiers, " + p["top"]) if p.get("top") else "today, check 3"}): the cap, {tt_["gland"][0]:.0f} across x {tt_["gland"][2] - tt_["gland"][1]:.1f}, set on the '
                     'crown, resting there by its weight, held by a magnet (hemi-cap-key; today\'s and A\'s keyed by a dowel and the swap\'s handle, B\'s not), the cord through its 1.0 lid (no screws, no thread), '
                     'its Ø24 pocket over the cord grip' if tt_ else
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
           Part('tether', tether_, Bought('hemi-tether'), finish='steel', group='fixture', inside=True,
                notes=[f'PROPOSAL (v6): 1.5 mm 7x7 stainless rope, {tlen_:.0f} between its screws: an M4 x 6 button screw radially into '
                       'the hub (z 80, 90 deg) clamps a crimped loop (the hub\'s eye); a 4 x 40 stainless snap hook (DIN 5299 C) on it; '
                       'the rope round the lip\'s top to an M3 x 6 button screw through the collar\'s wall (z 70, 270 deg). In a swap: '
                       'turn the shade, lower it a hand\'s width, unclip the snap at the hub']),
           Part('grippers', grippers, Bought('hemi-gripper'), finish='steel', group='canopy', inside=True,
                notes=['PROPOSAL (v6): two Cable Grippers MGR-M10-MM, plunger down, threaded up into their brackets under the strap']),
           Part('gripper-brackets', brackets, Bought('hemi-canopy-strap'), finish='steel', group='canopy', inside=True,
                notes=['PROPOSAL (v6): two 1.6 steel L brackets riveted under the strap, each with an M10 hole and lock nut for a gripper'])]
         if tt_ else []) + [
        Part('cord', cord, Bought('hemi-cord'), finish='cord', group='fixture'),
        # review 2 (2026-11-24, (8)): the fixture (about 3.5 lb) hangs from the steel cable by default; the SPT-2 cord's
        # 2.5 lb (UL 153) carries current only
        Part('suspension', susp, Bought('hemi-suspension'), finish=('steel' if tt_ else 'anodised'), group='fixture'),
        Part('canopy', canopy, Machined('aluminium', 'lathe'), finish='anodised', group='canopy',
             notes=[('150 x 50, 6061 turned, SATIN black anodised: v6, right side up: open at the top against the ceiling, '
                     'its 3 floor closed below with the cord\'s gland in its centre (a turned 6061 gland, satin black, its nut '
                     'flush) and two Ø6 holes at r 40 through which the cables pass and the grippers\' plungers are pushed; a '
                     'cover only, held to the strap by two flush black set screws in its wall; the strap carries the load') if tt_ else
                    ('150 x 50, 6061 turned, SATIN black anodised (2026-11-11, the bar: one hardware finish; was polished '
                     'black acrylic): a cover only (review 2026-11-01), screwed to the steel '
                     'strap, which carries the load; the driver and the splices are in the steel enclosure. The bar '
                     '(2026-11-11): the strap\'s screws black oxide, under the canopy\'s closed face, none in view; the cord '
                     'grip where the cord leaves the canopy a turned 6061 gland, satin black anodized, its nut flush')]),
        Part('strap', strap, Bought('hemi-canopy-strap'), finish='steel', group='canopy', inside=True),
        Part('enclosure', encl, Bought('hemi-driver-box'), finish='steel', group='canopy', inside=True),
        Part('driver', driver, Bought('north-driver-ring' if ring_ else 'north-driver-575'), finish='steel', group='canopy', inside=True, render=False),   # round 36: 575 lm
        *([Part('white-paint', None, Bought('hemi-white-paint'))] if p.get('white_split') else []),
        Part('plunger', None, Bought('dome-plunger')),
        Part('listing', None, Bought('moon-listing')),
    ]


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

NOTES_DOME = [
    'Option 3 (the owner, 2026-11-10: "it should work like Core cut in half"; the main build): the light sits at the '
    'mouth\'s centre and faces up into the shade, so the shade glows in its tint and the light cast down is the bulb\'s. '
    'A Ø50 ring board of 24 mid-power LEDs (two strings of 12 at about 90 mA, about 1,000 lm, about 200 lux under the '
    'lamp) on a black Ø56 x 4.5 carrier, its underside on the rim plane, the LEDs\' faces about 5 above it; a 16/12 '
    'black anodised stem up to the hub; the crown\'s inside white (a white Ø95 disc under the hub, the collar\'s flange '
    'face white); the opal to the rim. The COB, its reflector and holder are gone; the ERP driver, the Class 2 cord, '
    'the canopy and the UL 1598 path stay. Without a lens until a stock side-emitting ring optic with an IES file is '
    'named. Heat test needed: the hub about 6 K warmer than today (estimate). The notes below describe the COB build.',
    'Hemisphere (the Dome until round 35; Hemisphere North in rounds 35 to 37): the shade hangs mouth down. Its shades '
    'swap by hand: hold the cap (B: its Ø56 tier), lift the shade 8.0 to 9.0 mm, turn it 30 degrees and lower it a hand\'s '
    'width; it then hangs on its tether: unclip the tether\'s snap at the hub and lower it off. To fit one, clip the snap '
    'to the hub\'s eye, line up the three slots, push up, turn until the plunger clicks, and let go: its weight holds each '
    'pin up in its notch, so a knock cannot turn it off. No tools, and the shade is never live (the hub and the driver stay up).',
    'The shade is clamped, not hung on a glue joint: the collar\'s flange sits under the crown inside, a ring screws down '
    'over it outside, the acrylic between two silicone rings. A failed bond cannot drop it.',
    'The wall is tint, opal, tint: a 9 mm tinted shell, a 3 mm volume-diffusing opal liner, a 3 mm tinted skin, each '
    'formed from cast sheet on an aluminium mould, nested, closed at the mouth by a tinted rim with a vent. Opal '
    'scatters through its depth, so it still diffuses where it touches the tint (a bead-blasted clear liner would go '
    'clear wherever it was bonded). Nothing white is seen.',
    'Light: a Bridgelux Vero SE 10 (2700 K, CRI 90) at the top of a 46 bore lined with a reflector, 22 up: the cut-off '
    'about 46 deg from the vertical, and about 85 % of its light out (the black bore passed 52 %). About 575 lm at the '
    'COB (the owner, round 36): about 590 at 180 mA (4.4 W) on an ERP Power ESS010W-0180-42 (Class 2, FCC Part 15 '
    'Class B), dimmed 100 % to 1 % by a phase-cut (TRIAC or ELV) dimmer or 0-10 V. Not for 1,100 lm: the low top is '
    'sized for 575 (1,100 needs the fins of rounds 35 to 39).',
    'Heat (round 41): round 32f\'s low top is the heat sink, no fins: a black anodised aluminium crown 80 across and '
    '11.5 tall over the collar, and an aluminium cap 40 x 14 over the cord grip, the cap\'s top 126 above the rim. A '
    'PEEK ring carries the bayonet\'s pins, so the hub reaches the shade only through it and air. At 575 lm the hub '
    'makes 2.7 W of heat; estimated in a 35 C room: the hub 49 C, the COB\'s case 50 C, the collar and the acrylic '
    'beside it 41 C (hemisphere_thermal.py; to measure, README round 35).',
    'Mains stops at the canopy: the driver is there, and the cord carries the LED\'s 26 V DC (Class 2). The cord is a '
    'listed 18 AWG 2-conductor in a black textile braid, 2 mm longer than the cables so it carries no load: the lamp '
    'hangs from two 1/16 in stainless cables, each on a stop sleeve in the hub and a rated cable gripper in the canopy '
    '(their pull test with the fixture is part of the listing). To be listed to UL 1598 (hardwired) with its own shades, '
    'each tint in the listing; the canopy\'s strap carries the grippers and the steel enclosure the driver and the '
    'splices, the canopy a cover only.',
    'Hang over a bar at 750 to 900 centres, the rim 700 to 800 above the counter; over a table, one a table, the rim '
    'about 650 to 750 above it.',
]
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
TOUCHING_DOME_LEGACY = TOUCHING_DOME + [('suspension', 'gland'), ('suspension', 'canopy'), ('suspension', 'cord'), ('pins', 'hub')]
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
