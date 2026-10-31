"""Round 48: the numbers behind Core (proposal B), from its own CAD. Run in the fab venv:

    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/core_numbers.py > spinoffs/barkhorn/companions/mantle-r48/out-core/numbers.md
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mantle_core as M                                             # noqa: E402

P = M.P
D = M.derived(P)
parts = M.parts(P)
DENS = {'trucast-tint': 1.19, 'trucast-clear': 1.19, 'cast-acrylic': 1.19, 'brass-leadfree': 8.2, 'stainless': 7.8,
        'aluminium': 2.70, 'brass-sheet': 8.5}
BOUGHT_G = {'rega-24v-motor': 330, 'rega-rb330': 300, 'ortofon-2m-black': 7.2, 'phono-box-s2': 570, 'rega-grommets': 5,
            'flat-belt-core': 6, 'foot-sorbothane': 15, 'foot-studs': 60, 'platter-screws': 12, 'back-hardware': 45,
            'bearing-bushes-solid': 25, 'carbide-ball': 2, 'thrust-plate': 3, 'phono-felts': 2, 'cover-dowels': 4}
mass, groups = 0.0, {}
lines = []
for p in parts:
    mk = p.make
    mat = getattr(mk, 'material', None)
    if p.solid is not None and mat in DENS:
        g = p.solid.volume / 1000 * DENS[mat]
    else:
        g = BOUGHT_G.get(getattr(mk, 'ref', ''), 0.0)
    grp = p.group or 'other'
    groups[grp] = groups.get(grp, 0.0) + g
    lines.append((p.name, g))
mass = sum(groups.values())

out = []
w = out.append
w('# Core (proposal B): the numbers\n')
w('Read from the CAD (`mantle_core.py`); bought parts at their makers\' or measured weights where known, else estimates.\n')
w('## Mass\n')
w('| group | kg |\n|---|---|')
for k, v in sorted(groups.items(), key=lambda kv: -kv[1]):
    w(f'| {k} | {v / 1000:.2f} |')
w(f'| **all** | **{mass / 1000:.1f}** |')
deck = groups.get('deck', 0) / 1000
cover = groups.get('cover', 0) / 1000
turning = (dict(lines)['platter'] + dict(lines)['platter-hub'] + dict(lines)['spindle'] + dict(lines)['platter-screws']) / 1000
w(f'\nThe deck {deck:.1f} kg, the cover {cover:.2f} kg (a two-handed lift; the baseline\'s hinged lid was 2.2 kg), turning '
  f'{turning:.2f} kg.')
R = P['platter_d'] / 2000
mp = dict(lines)['platter'] / 1000
I = 0.5 * mp * (R ** 2 + 0.020 ** 2)
w(f'Platter inertia about {I:.4f} kg m2 (acrylic alone; the hub adds about 0.0001).\n')

w('## Why an acrylic platter\n')
rho_p, E_p = 1190, 3.2e9
rho_v, E_v = 1380, 3.0e9
Zp = math.sqrt(rho_p * E_p); Zv = math.sqrt(rho_v * E_v)
Rc = ((Zv - Zp) / (Zv + Zp)) ** 2
w(f'- Bar impedance sqrt(rho E): PMMA {Zp / 1e6:.2f} MRayl, PVC vinyl {Zv / 1e6:.2f} MRayl: {Rc * 100:.2f} % of the energy '
  'reflects at the record\'s underside, so the stylus\'s energy crosses into the platter instead of ringing back.')
w('- And it stays there: PMMA\'s loss factor is about 0.03-0.06 in the audio band (aluminum about 0.0001, glass 0.001): '
  'the platter does not ring. That is why Pro-Ject, Clearaudio and Michell use acrylic, and why Core runs without a mat.')
w('- The bond lines are not damping: a polymerising cement cures to PMMA (it is meant to be invisible), so a cemented '
  'stack behaves as one solid. Constrained-layer damping would need a viscoelastic interlayer (an acrylic foam tape '
  'or an optical PSA), which would creep under the bearing\'s load and show as a milky line. Core does not claim it; '
  'the deck is damped by its mass and by PMMA\'s own loss.\n')

w('## The isolation\n')
k_feet = 3 * 1.4e6 * (math.pi * 0.02 ** 2) / 0.004          # 50 duro Sorbothane, E about 1.4 MPa (dynamic), 40 x 4
m_iso = (mass - groups.get('cover', 0)) / 1000
f_feet = 1 / (2 * math.pi) * math.sqrt(k_feet / m_iso)
w(f'- Three 40 x 4 Sorbothane discs (50 duro, dynamic E about 1.4 MPa, shape factor 2.5: stiffer than its E alone, so '
  f'read this as a floor): k about {k_feet / 1e3:.0f} kN/m in all under {m_iso:.1f} kg: f = {f_feet:.0f} Hz. Honestly: '
  'feet like these isolate only above about 1.4 f (about 70 Hz), so they keep the motor\'s and the speakers\' 100 Hz and '
  'up off the deck but pass footfall (2-20 Hz); a floor that bounces wants a wall shelf. They stay far above the '
  'arm-cartridge resonance (about 8 Hz: the RB330\'s 11 g effective + the 2M\'s 7.2 g at 20 um/mN), so they add nothing '
  'in the 8-12 Hz band, which is what a soft float does.')
w('- The float of the baseline sat at 25-36 Hz on its bushings (the review), in the band where speakers feed back. '
  'Core has no float: one stiff block, the motor on Rega\'s own grommets, the feet doing the isolating.\n')

w('## The drive\n')
S, Mo = D['S'], D['M']
d = math.hypot(Mo[0] - S[0], Mo[1] - S[1])
r = D['pulley_d'] / 2; Rr = P['platter_d'] / 2
beta = math.asin((Rr - r) / d)
wrap = math.pi - 2 * beta
w(f'- Pulley to spindle {d:.0f} mm; pulley {D["pulley_d"]:.2f} for 33.3 at 250 rpm; wrap on the pulley {math.degrees(wrap):.0f} deg '
  f'(a Rega Planar 3\'s is about the same). Belt path {2 * math.sqrt(d * d - (Rr - r) ** 2) + Rr * (math.pi + 2 * beta) + r * wrap:.0f} mm.')
w('- The motor hangs on Rega\'s three grommets in its own pocket, so the pulley\'s height is fixed to the platter\'s by '
  'solid acrylic: nothing can tilt it (the baseline pod\'s tipping moment under the belt was close to its weight\'s).')
w('- Speed: the Neo PSU MK2 switches 33/45 electrically and trims in 0.01 rpm steps; the pulley has one diameter.\n')

w('## The bearing\n')
Wt = turning * 9.81
E_ = 1 / ((1 - 0.22 ** 2) / 600e9 + (1 - 0.3 ** 2) / 210e9)
a = (3 * Wt * 0.003 / (4 * E_)) ** (1 / 3)
p0 = 3 * Wt / (2 * math.pi * a * a)
w(f'- Thrust: {Wt:.1f} N on a 6 mm carbide ball on hardened 52100: Hertz contact radius {a * 1e6:.0f} um, peak pressure '
  f'{p0 / 1e9:.2f} GPa, under half of 52100\'s 4 GPa static limit; it runs in oil.')
w('- Journals: 10 g5 spindle in two C932 bronze bushes honed to 10 H6: 8-12 um running clearance (the review: 3-5 um '
  'was too tight for oil). PV is trivial at 0.56 Hz.')
w('- The housing is threaded M30 x 1.5 and clamped by its nut under the deck, so there is no insert beside the bore '
  '(the baseline\'s M4 inserts left 2.8 mm webs).')
w('- Service: lift the platter, its hub and the spindle out together (one assembly; the six M4 screws stay in), wipe the '
  'spindle, add 1 ml of oil every two years with a syringe, lower it back slowly (the oil has to pass the ball). '
  'Shipping: that assembly in its own foam, a nitrile cap over the housing.\n')

w('## The arm\n')
w(f'- RB330 at 222 mm on an aluminum puck (84 x 12, Rega three-point). Record surface {D["record_z"] - D["top"]:.1f} mm over the '
  'deck\'s top: the arm\'s height is set with Rega spacers on the first sample, the tube level with the stylus down.')
w('- The cue lift and the arm rest are Rega\'s own, on the arm\'s base. The lead goes down through the puck\'s 56 bore and '
  'along a groove under the deck to the phono stage\'s tunnel.\n')

w('## Heat\n')
w('- No light, so no heat to speak of: the phono stage draws about 18 V x 0.03 A = 0.5 W in a tunnel open to the back. '
  'The motor\'s 1-2 W sits in an open-topped pocket. Nothing in Core passes 5 C over the room.\n')

w('## The cover as a stand\n')
ch = D['height'] - D['top']
w(f'- The cover is {ch:.0f} deep and stands on its back long edge, its open side forward; a sleeve (315 square, 3 thick) '
  'stands in it on the lower ring\'s inner face, leaning back on the top lamina. The cover\'s center of mass is about '
  f'{ch * 0.62:.0f} mm from its open face (the top lamina is the heaviest piece), so it tips back past about '
  f'{math.degrees(math.atan2(ch * 0.38, 190)):.0f} deg and forward past about {math.degrees(math.atan2(ch * 0.62, 190)):.0f} deg: '
  'steady on a shelf, not on a slope.\n')

w('## Mass budget by part\n')
w('| part | g |\n|---|---|')
for n, g in sorted(lines, key=lambda x: -x[1]):
    if g >= 5:
        w(f'| {n} | {g:.0f} |')
print('\n'.join(out))
