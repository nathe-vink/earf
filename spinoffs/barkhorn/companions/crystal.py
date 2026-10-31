"""Round 32d, the bar lamps the owner picked from the shape study (2026-10-19: "I like the dome overhead lights,
especially if the acrylic covers are easy to swap out, but I'm also a sucker for the spheres. For the table lamp
though, I'd want the spheres to be squatted rather than raised, like a crystal ball."). Two products, the frost set
within the acrylic as in round 32c (study.py): tint, frost, tint; nothing white outside.

Dome, the pendant. A tinted dome 200 across is a cover that comes off by hand. A black anodised collar is bonded into its crown,
and three L-slots in the collar take three pins on the fixture's black anodised hub: a quarter-turn bayonet (30 degrees here).
Lifted 5 mm, turned and lowered, the cover hangs with each pin up in a notch at the end of its slot, so its own weight
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
SOLIDS.setdefault('acrylic-opal-formed', dict(title='Cast acrylic sheet, volume-diffusing (opal), formed over an aluminium '
                                              'mould', density=1.19, usd_per_cm3=0.06))
SOLIDS.setdefault('peek', dict(title='PEEK rod, unfilled', density=1.30, usd_per_cm3=0.35))

GAP, LT, SKIN = 1.0, 2.5, 3.0          # the liner 1 mm in from the shell, 2.5 thick; the inner skin 3

O = dict(R=80.0, shell=9.0, base=(120.0, 30.0), ring=8.0, rim_r=50.0, port=40.0)    # round 41: 30 again (48 in rounds 35 to 39)

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
         ring=(62.0, 78.0, 86.0, 100.0),        # the PEEK pin carrier: ID, OD, z0, z1
         core=(62.0, 60.0, 100.0),               # the hub core: OD, z0, z1 (the bore and the reflector in it)
         bore=(46.0, 82.0),                      # the bore's diameter and the COB's face (22 up from the mouth at 60)
         neck=(40.0, 104.0),                     # the core's neck, up into the crown
         crown=(80.0, 100.5, 112.0),             # round 41: the low top, the heat sink: OD, z0, z1 (the fins of rounds
                                                 # 35 to 39 were 80 across from 110 to 146, 16 x 1.8: in git at 950a7eaf)
         cap=(40.0, 14.0), drop=600.0, canopy=(150.0, 50.0))
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
    hole = cyl('z', (0, 0), co + 0.4, 0, R + 5)
    shell = ball(R, p['shell'], (0, 0, 0), cut_below=0) - hole
    liner = ball(r_l, p['liner'], (0, 0, 0), cut_below=4) - hole
    skin = ball(r_k, p['skin'], (0, 0, 0), cut_below=0) - hole
    rim = cyl('z', (0, 0), 2 * (r_si - 0.2), 0, 3.8) - cyl('z', (0, 0), 2 * (r_k + 0.2), -1, 5)
    # the collar: a tube through the crown, its flange a spherical seat under the skin (on a 1 mm silicone ring)
    tube = cyl('z', (0, 0), co, cz0, cz1) - cyl('z', (0, 0), ci, cz0 - 1, cz1 + 1)
    flange = _sphere_band(r_ki - 1.0, r_ki - 5.0, ci / 2, fr)
    collar = tube + flange
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
    for a in (off, off + 120, off + 240):
        collar = collar - at(a, box(ci / 2 - 2, -w / 2, cz0 - 1, rs, w / 2, zs + 7.5))                    # the entry
        collar = collar - sector(ci / 2 - 2, rs, a, a + p['turn'], zs + 2.5, zs + 7.5)                     # the turn
        collar = collar - at(a + p['turn'], box(ci / 2 - 2, -w / 2, zs - 2.5, rs, w / 2, zs + 7.5))        # the notch
    gasket_in = _sphere_band(r_ki, r_ki - 1.0, co / 2 + 0.2, fr)
    gasket_out = _sphere_band(R + 1.0, R, co / 2 + 0.2, fr)
    clamp = _sphere_band(R + 6.0, R + 1.0, co / 2, fr) + (cyl('z', (0, 0), co + 8, 92.0, 97.0) - cyl('z', (0, 0), co, 91, 98))
    clamp = clamp - cyl('z', (0, 0), co, 80, 110)
    note_formed = ('drape-formed from cast sheet over an aluminium mould, trimmed and polished; the prototypes are formed on '
                   'the production moulds')
    return [
        Part('shell', shell, Machined('acrylic-formed', 'formed', setup_usd=1500.0), finish='body', group='cover',
             notes=['the outside: 10 mm tinted cast sheet ' + note_formed + ' (9 at the crown, thinner toward the rim: the '
                    'former confirms); its outer face never touches the mould, so it keeps the cast sheet\'s gloss']),
        Part('liner', liner, Machined('acrylic-opal-formed', 'formed', setup_usd=1200.0), finish='liner', group='cover',
             inside=True,
             notes=['the diffuser: 3 mm volume-diffusing (opal) cast acrylic, light-diffusing grade, about 70 % '
                    'transmission ' + note_formed + '. Opal scatters through its volume, so it diffuses wherever it '
                    'touches the tinted layers (a bead-blasted clear liner goes clear where it is bonded or wetted)']),
        Part('skin', skin, Machined('acrylic-formed', 'formed', setup_usd=1200.0), finish='body', group='cover',
             notes=['the inside: 3 mm tinted cast sheet formed into a female mould, so its inner (seen) face keeps its '
                    'gloss and the opal is seen only through tint']),
        Part('rim', rim, Machined('cast-acrylic', 'lathe'), finish='body', group='cover',
             notes=['closes the three layers at the mouth, bonded and polished with them; a press-in ePTFE vent in its '
                    'face keeps the gaps between the layers at room pressure and dry']),
        Part('collar', collar, Machined('aluminium', 'lathe'), finish='anodised', group='cover',
             notes=['aluminium 6061, black anodised, satin: a tube through the crown with a spherical flange under the '
                    'skin; three blind L-slots with T-ended notches (the quarter-turn bayonet, 30 deg) work either way up; '
                    'M96 x 1.5 outside for the clamp ring. It carries the cover mechanically: the bond is a seal only']),
        Part('clamp', clamp, Machined('aluminium', 'lathe'), finish='anodised', group='cover',
             notes=['aluminium, black anodised: screwed onto the collar over the crown, its spherical face on a silicone '
                    'ring, to a torque the shade maker sets (the acrylic is clamped between two silicone rings, never metal '
                    'on acrylic); a drop of thread-lock']),
        Part('gaskets', gasket_in + gasket_out, Bought('hemi-gaskets'), finish='silicone', group='cover'),
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
    core = cyl('z', (0, 0), od, z0, z1) - cyl('z', (0, 0), bd, z0 - 1, bz) - cyl('z', (0, 0), 28.4, bz, bz + 3)
    core = core + cyl('z', (0, 0), nd, z1, nz)
    core = core - cyl('z', (0, 0), 10, bz + 3, nz + 1)                                 # the wires
    ring = cyl('z', (0, 0), ro, rz0, rz1) - cyl('z', (0, 0), ri, rz0 - 1, rz1 + 1)
    pins = None
    for a in (0, 120, 240):
        pin = at(a + p['turn'], cyl('x', (0, pz), 4.0, ri / 2 + 2, p['collar'][1] / 2 + 2.5))
        pins = pin if pins is None else pins + pin
    # the reflector: a faceted cone of high-reflectance aluminium in the bore, from the COB's edge to the mouth
    from build123d import Cone, Pos, Align
    al = (Align.CENTER, Align.CENTER, Align.MIN)
    refl = Pos(0, 0, z0 + 0.5) * (Cone(bd / 2 - 0.6, 10.0, bz - z0 - 1.0, align=al) -
                                  Cone(bd / 2 - 1.1, 9.5, bz - z0 - 1.0, align=al))
    refl = refl & cyl('z', (0, 0), bd - 0.2, z0 + 0.5, bz - 0.5)
    cob = cyl('z', (0, 0), 28, bz, bz + 2)
    crown = cyl('z', (0, 0), sd, sz0, sz1) - cyl('z', (0, 0), nd + 0.2, sz0 - 1, nz) - cyl('z', (0, 0), 10, sz0 - 1, sz1 + 1)
    gland = cyl('z', (0, 0), cd, sz1, sz1 + ch) - cyl('z', (0, 0), 8, sz1 - 1, sz1 + ch + 1)
    z_cord = sz1 + ch
    cord = cyl('z', (0, 0), 6, z_cord, z_cord + p['drop'])
    zc = z_cord + p['drop']
    # round 43 (proposal, certification.md): the fixture hangs from a fine steel cable beside the cord, so the cord
    # carries current only (UL 153 lets an SPT-2 cord carry 2.5 lb; Hemisphere is about 3.5); an option until signed
    susp = cyl('z', (5.5, 0), 1.5, z_cord, zc) + cyl('z', (5.5, 0), 5.0, z_cord, z_cord + 9) + cyl('z', (5.5, 0), 5.0, zc - 9, zc)
    cnd, cnh = p['canopy']
    canopy = cyl('z', (0, 0), cnd, zc, zc + cnh) - cyl('z', (0, 0), cnd - 6, zc - 1, zc + cnh - 3)
    driver = box(-42, -28.5, zc + 6, 42, 28.5, zc + 6 + 29.5)
    return cover_parts(p) + [
        Part('hub', core, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=['aluminium 6061, black anodised: the core, turned from bar. The COB on its holder at the top of the 46 '
                    'bore (22 up: the cut-off, about 46 deg from the vertical), the reflector in the bore, the PEEK ring '
                    'round it, the crown on its neck on a thermal pad; a 10 bore for the wires']),
        Part('ring', ring, Machined('peek', 'lathe'), finish='trim', group='fixture', inside=True,
             notes=['PEEK, unfilled (0.25 W/m K), black: the thermal break. It carries the three pins and the detent, so '
                    'the cover touches the fixture only through it; 4 to 5 mm of air round the core inside the collar']),
        Part('pins', pins, Bought('dome-pins'), finish='anodised', group='fixture'),
        Part('reflector', refl, Bought('north-reflector'), finish='anodised', group='fixture', inside=True),
        Part('cob', cob, Bought('hemi-cob'), finish='led', group='fixture', inside=True),
        Part('crown', crown, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=['the heat sink (round 41; the fins until then), round 32f\'s low top: 80 across, 11.5 tall over the '
                    'collar, turned from 6061 bar, black anodised (emissivity about 0.85: half its loss is radiation), on '
                    'the core\'s neck on a thermal pad, 0.5 clear of the PEEK ring and the collar']),
        Part('gland', gland, Machined('aluminium', 'lathe'), finish='anodised', group='fixture',
             notes=['the cap, 40 x 14: aluminium, black anodised and polished (round 32f\'s was black acrylic: here it '
                    'runs at the hub\'s 49 to 52 C), over the listed cord grip (the strain relief, tested with the '
                    'fixture\'s weight), on two M3 into the crown; part of the heat sink']),
        Part('cord', cord, Bought('hemi-cord'), finish='cord', group='fixture'),
        Part('suspension', susp, Bought('hemi-suspension'), finish='anodised', group='fixture', option='suspension'),
        Part('canopy', canopy, Machined('cast-acrylic', 'lathe'), finish='trim', group='canopy',
             notes=['150 x 50, black cast acrylic, polished: over the driver and a steel junction-box strap (the strap '
                    'carries the load)']),
        Part('driver', driver, Bought('north-driver-575'), finish='steel', group='canopy', inside=True, render=False),   # round 36: 575 lm
        Part('plunger', None, Bought('dome-plunger')),
        Part('listing', None, Bought('moon-listing')),
    ]


dome_parts = north_parts


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
    port = cyl('z', (0, 0), p['port'], zc - R - 5, zc - R + 25)
    shell = ball(R, t, (0, 0, zc)) - port
    shell_r = ball(R, t - 0.4, (0, 0, zc)) - port
    frost_r = ball(R - t + 0.3, 0.3, (0, 0, zc)) - port
    gz0 = zc - math.sqrt(R ** 2 - (p['port'] / 2) ** 2)
    gz1 = zc - math.sqrt((R - t) ** 2 - (p['port'] / 2) ** 2)
    grommet = cyl('z', (0, 0), p['port'] - 0.4, gz0, gz1) - cyl('z', (0, 0), p['port'] - 6, gz0 - 1, gz1 + 1)
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
    cells = holder = None
    for k in range(3):
        ang = -10.0 + 120.0 * k
        c = at(ang, cyl('y', (a + d / 2, z0c + d / 2), d, -L / 2, L / 2))
        h = at(ang, box(a - 0.8, -L / 2 - 2.0, hz + 0.1, a + d + 0.8, L / 2 + 2.0, z0c + d * 0.6) -
               box(a, -L / 2 - 0.2, z0c - 0.05, a + d, L / 2 + 0.2, z0c + d + 1))
        cells = c if cells is None else cells + c
        holder = h if holder is None else holder + h
    bay = None
    for k in range(3):
        ang = -10.0 + 120.0 * k
        b = at(ang, box(a - 1.0, -L / 2 - 2.2, -1, a + d + 1.0, L / 2 + 2.2, z0c + d + 0.5))
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
    ballast = corner
    plug = at(uang, box(51, -6.0, 0.6, 62, 6.0, 6.6))
    cable = orb_cable(ux, uy)
    zs = zc - math.sqrt(R ** 2 - 42 ** 2) - 0.3
    seat = cyl('z', (0, 0), 92, zs - 1.5, zs) - cyl('z', (0, 0), 84, zs - 2, zs + 1)
    # the drum: from below, the hatch's counterbore, the middle pocket, the cells' bays, the corners, the ring's groove
    base = eased(bd, 0, bh, 3.0, top=False) - cup - cyl('z', (0, 0), 112.0, -1, hz)
    base = base - cyl('z', (0, 0), 50.4, -1, uz) - cyl('z', (0, 0), 30, uz - 0.1, bh) - bay
    base = base - (cyl('z', (0, 0), 108.4, -1, z0c + d + 0.6) - cyl('z', (0, 0), 53.6, -2, 31) - _chords(a, L, d, -0.2) -
                   at(uang, box(30, -7.8, -2, 70, 7.8, 31)))
    base = base - notch - at(uang, box(42.5, -5.5, -1, 51, 5.5, 10.5))
    hatch = cyl('z', (0, 0), 111.6, 0.2, hz) - notch
    foot = cyl('z', (0, 0), 117.6, 0.2, 2) - cyl('z', (0, 0), 114.4, 0, 3) - notch
    base = base - (cyl('z', (0, 0), 118, -1, 2) - cyl('z', (0, 0), 114, -2, 3)) - cyl('z', (0, 0), 92.4, zs - 2, zs + 0.01)
    ring = eased(bd, bh, z_top, 2.0, bottom=False) - cup
    ring = ring - (cyl('z', (0, 0), 92.4, zs - 2, zs + 0.01) - cyl('z', (0, 0), 83.6, zs - 3, zs + 1))
    return [
        Part('shell', shell, Machined('acrylic-formed', 'formed', setup_usd=1500.0), finish='body', group='ball',
             pieces={'shell': (shell_r, 'body'), 'frost': (frost_r, 'liner')},
             notes=['the ball: two hemispheres drape-formed from 10 mm tinted cast sheet on one aluminium mould (the '
                    'production process; the prototypes are formed on it), their insides bead-blasted, joined at the '
                    'equator with a polymerising acrylic cement (Acrifix 192 kind), the joint turned and polished: a '
                    'faint line at the equator (to judge on the first sample); a 40 port cut at its underside. One part '
                    'where there were three: the frost scatters because it faces air']),
        Part('grommet', grommet, Machined('aluminium', 'lathe'), finish='anodised', group='ball',
             notes=['black anodised aluminium: lines the port, bonded']),
        Part('base', base, Machined('cast-acrylic', 'lathe', setup_usd=80.0), finish='trim', group='base',
             notes=['black cast acrylic, polished, turned from rod: 120 x 30 (round 32f\'s), the cup turned in it; from '
                    'below the hatch\'s counterbore (112), the middle pocket (50) for the chassis, the board and the LED, '
                    'the three cells\' bays, the ballast\'s corners and the cable notch']),
        Part('ring', ring, Machined('aluminium', 'lathe'), finish='anodised', group='base',
             notes=['aluminium, black anodised, satin, insulated from the chassis: the touch (tap to switch, hold to dim, '
                    '2200 to 2700 K)']),
        Part('window', window, Machined('cast-acrylic', 'lathe'), finish='window', group='base',
             notes=['a clear acrylic plug, sealed with an O-ring: the LED under it, the base IP44 with the ball off']),
        Part('chassis', chassis, Machined('aluminium', 'mill'), finish='steel', group='base', inside=True,
             notes=['aluminium 6061, 50 across: the LED\'s heat spreader and the board\'s carrier, screwed up into the '
                    'base on threaded inserts, an O-ring between']),
        Part('ballast', ballast, Machined('steel', 'mill'), finish='steel', group='base', inside=True,
             notes=['mild steel, zinc-plated: three corner pieces between the cells\' bays, screwed up into the base']),
        Part('board', board, Bought('core-board-18650'), finish='steel', group='base', inside=True, render=False),
        Part('led', led, Bought('moon-led-table'), finish='led', group='base', inside=True),
        Part('cells', cells, Bought('core-cells-18650'), finish='steel', group='battery', inside=True, render=False),
        Part('holder', holder, Bought('core-holder-18650'), finish='trim', group='battery', inside=True,
             notes=['three single-cell holders in a triangle round the middle: spring contacts (no exposed contact '
                    'outside the hatch), keyed so a cell cannot go in backwards, the NTC on one']),
        Part('hatch', hatch, Machined('aluminium', 'mill'), finish='anodised', group='battery',
             notes=['black anodised aluminium, 2.3 thick, in a counterbore under the base: four captive M3 screws '
                    '(Phillips or Torx: commercially available tools), an O-ring (IP44); a label inside: the cells\' '
                    'type (LiFePO4 18650 only) and how to change them']),
        Part('usb', usb, Bought('orb-seals'), finish='steel', group='base', inside=True, render=False),
        Part('seat', seat, Bought('orb-seat'), finish='silicone', group='base'),
        Part('foot-ring', foot, Bought('core-foot'), finish='silicone', group='base'),
        Part('cable', cable + plug, Bought('orb-cable'), finish='fabric', group='cable'),
        Part('adapter', None, Bought('orb-adapter')),
        Part('screws', None, Bought('core-screws')),
    ]


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
    'Hemisphere (the Dome until round 35; Hemisphere North in rounds 35 to 37): the shade hangs mouth down. Its shades '
    'swap by hand: lift the shade 5 mm, turn it 30 degrees and lower it off. To fit one, line up the three slots, push '
    'up, turn until the plunger clicks, and let go: its weight holds each pin up in its notch, so a knock cannot turn '
    'it off. No tools, and the shade is never live (the COB, the hub and the driver stay up).',
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
    'listed 18 AWG 2-conductor in a black textile braid, its grips tested with the fixture\'s weight. Listed to UL 1598 '
    'with any shade.',
    'Hang over a bar at 750 to 900 centres, the rim 700 to 800 above the counter; over a table, one a table, the rim '
    'about 650 to 750 above it.',
]
NOTES_ORB = [
    'Core (the Orb until round 35): a crystal ball, a 160 tinted ball low in the cup of a 120 x 30 base (round 41), 180 '
    'tall. The ball lifts off: the LED is under a sealed window in the base, so balls swap colour by hand.',
    'One ball where there were three layers: tinted cast acrylic, two halves formed on one mould and joined at the '
    'equator, their inside bead-blasted. The frost faces air, so it scatters; seen from outside it is behind the tint, '
    'and the port that would show it faces the base.',
    'Plugged in or not, one product: three LiFePO4 18650 cells (Power Sonic PSL-FP-IFR18650EC, 14.4 Wh) in a triangle round the LED, behind '
    'a hatch underneath on four captive screws, the user\'s to replace with standard cells. It runs from USB-C (5 V 3 A, '
    'the adapter and a 2 m fabric cable in the box) or from its cells, and charges while it runs, in about 2 hours. '
    'About 4.7 hours at full brightness (2.5 W) at the default charge limit (90 %), 5.2 at a full charge; about 5.8 '
    'at the bar setting (2 W).',
    'Long life: LiFePO4 keeps about 80 % of its capacity after about 2,000 cycles (ordinary Li-ion about 500); the '
    'charge limit, a battery-management circuit (protection, a fuel gauge, charging held off below 0 C and above 45 C '
    'by the cells\' NTC) and no exposed contacts. Certified as one product: IEC/UL 62368-1 with its battery annex; the '
    'cells to IEC 62133-2 and UN 38.3.',
    'Touch the black ring: tap to switch, hold to dim, 2200 to 2700 K as it dims. IP44: the base sealed by O-rings at '
    'the window, the chassis and the hatch, the USB-C receptacle sealed; with the ball on or off.',
    'Black, so the tint is the only colour: the base black cast acrylic, polished, over an aluminium chassis and a steel '
    'ballast; the ring, the port\'s lining and the hatch black anodised aluminium.',
]
TOUCHING_DOME = [('suspension', 'gland'), ('suspension', 'canopy'), ('suspension', 'cord'), ('pins', 'ring'), ('rim', 'shell'), ('rim', 'skin'), ('rim', 'liner'), ('cob', 'hub'), ('gland', 'crown'),
                 ('crown', 'hub'), ('clamp', 'collar'), ('gaskets', 'collar'), ('gaskets', 'clamp'), ('gaskets', 'shell'),
                 ('gaskets', 'skin'), ('reflector', 'hub')]
TOUCHING_ORB = [('grommet', 'shell'), ('window', 'base'), ('seat', 'base'), ('ring', 'base'), ('led', 'board'),
                ('chassis', 'base'), ('ballast', 'chassis'), ('ballast', 'base'), ('cable', 'base'), ('board', 'chassis'),
                ('foot-ring', 'base'), ('cells', 'holder'), ('hatch', 'base'), ('usb', 'base'), ('cable', 'hatch'),
                ('led', 'chassis'), ('holder', 'base'), ('holder', 'hatch'), ('ballast', 'hatch'), ('chassis', 'board'),
                ('window', 'led'), ('usb', 'hatch')]


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
TOUCHING_SOUTH = TOUCHING_DOME + [('weld', 'skin'), ('weld', 'liner'), ('weld', 'collar'), ('rod', 'hub'), ('led', 'hub'), ('rod', 'led'), ('rod', 'lid'), ('pipe', 'rod'),
                                  ('pipe', 'hub'), ('fins', 'rod'), ('gland', 'fins'), ('fins', 'hub')]


# The triangle of chords Core's cells lie on (round 41; orb_parts), grown or shrunk for the parts round them
def _chords(a, L, d, grow):
    out = None
    for k in range(3):
        b = at(-10.0 + 120.0 * k, box(a - grow - 3.0, -L / 2 - grow - 4.4, -2, 70, L / 2 + grow + 4.4, 31))
        out = b if out is None else out + b
    return out
