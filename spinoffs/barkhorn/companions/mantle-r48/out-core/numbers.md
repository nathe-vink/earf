# Core (proposal B): the numbers

Read from the CAD (`mantle_core.py`); bought parts at their makers' or measured weights where known, else estimates.

## Mass

| group | kg |
|---|---|
| deck | 8.67 |
| cover | 2.90 |
| platter | 2.03 |
| phono | 0.72 |
| feet | 0.47 |
| arm | 0.47 |
| motor | 0.41 |
| bearing | 0.38 |
| other | 0.00 |
| **all** | **16.1** |

The deck 8.7 kg, the cover 2.90 kg (a two-handed lift; the baseline's hinged lid was 2.2 kg), turning 2.07 kg.
Platter inertia about 0.0200 kg m2 (acrylic alone; the hub adds about 0.0001).

## Why an acrylic platter

- Bar impedance sqrt(rho E): PMMA 1.95 MRayl, PVC vinyl 2.03 MRayl: 0.04 % of the energy reflects at the record's underside, so the stylus's energy crosses into the platter instead of ringing back.
- And it stays there: PMMA's loss factor is about 0.03-0.06 in the audio band (aluminium about 0.0001, glass 0.001): the platter does not ring. That is why Pro-Ject, Clearaudio and Michell use acrylic, and why Core runs without a mat.
- The bond lines are not damping: a polymerising cement cures to PMMA (it is meant to be invisible), so a cemented stack behaves as one solid. Constrained-layer damping would need a viscoelastic interlayer (an acrylic foam tape or an optical PSA), which would creep under the bearing's load and show as a milky line. Core does not claim it; the deck is damped by its mass and by PMMA's own loss.

## The isolation

- Three 40 x 4 Sorbothane discs (50 duro, dynamic E about 1.4 MPa, shape factor 2.5: stiffer than its E alone, so read this as a floor): k about 1319 kN/m in all under 13.2 kg: f = 50 Hz. Honestly: feet like these isolate only above about 1.4 f (about 70 Hz), so they keep the motor's and the speakers' 100 Hz and up off the deck but pass footfall (2-20 Hz); a floor that bounces wants a wall shelf. They stay far above the arm-cartridge resonance (about 8 Hz: the RB330's 11 g effective + the 2M's 7.2 g at 20 um/mN), so they add nothing in the 8-12 Hz band, which is what a soft float does.
- The float of the baseline sat at 25-36 Hz on its bushings (the review), in the band where speakers feed back. Core has no float: one stiff block, the motor on Rega's own grommets, the feet doing the isolating.

## The drive

- Pulley to spindle 180 mm; pulley 39.48 for 33.3 at 250 rpm; wrap on the pulley 87 deg (a Rega Planar 3's is about the same). Belt path 992 mm.
- The motor hangs on Rega's three grommets in its own pocket, so the pulley's height is fixed to the platter's by solid acrylic: nothing can tilt it (the baseline pod's tipping moment under the belt was close to its weight's).
- Speed: the Neo PSU MK2 switches 33/45 electrically and trims in 0.01 rpm steps; the pulley has one diameter.

## The bearing

- Thrust: 20.3 N on a 6 mm carbide ball on hardened 52100: Hertz contact radius 65 um, peak pressure 2.32 GPa, under half of 52100's 4 GPa static limit; it runs in oil.
- Journals: 10 g5 spindle in two C932 bronze bushes honed to 10 H6: 8-12 um running clearance (the review: 3-5 um was too tight for oil). PV is trivial at 0.56 Hz.
- The housing is threaded M30 x 1.5 and clamped by its nut under the deck, so there is no insert beside the bore (the baseline's M4 inserts left 2.8 mm webs).
- Service: lift the platter, its hub and the spindle out together (one assembly; the six M4 screws stay in), wipe the spindle, add 1 ml of oil every two years with a syringe, lower it back slowly (the oil has to pass the ball). Shipping: that assembly in its own foam, a nitrile cap over the housing.

## The arm

- RB330 at 222 mm on an aluminium puck (84 x 12, Rega three-point). Record surface 28.8 mm over the deck's top: the arm's height is set with Rega spacers on the first sample, the tube level with the stylus down.
- The cue lift and the arm rest are Rega's own, on the arm's base. The lead goes down through the puck's 56 bore and along a groove under the deck to the phono stage's tunnel.

## Heat

- No light, so no heat to speak of: the phono stage draws about 18 V x 0.03 A = 0.5 W in a tunnel open to the back. The motor's 1-2 W sits in an open-topped pocket. Nothing in Core passes 5 C over the room.

## The cover as a stand

- The cover is 87 deep and stands on its back long edge, its open side forward; a sleeve (315 square, 3 thick) stands in it on the lower ring's inner face, leaning back on the top lamina. The cover's centre of mass is about 54 mm from its open face (the top lamina is the heaviest piece), so it tips back past about 10 deg and forward past about 16 deg: steady on a shelf, not on a slope.

## Mass budget by part

| part | g |
|---|---|
| deck-L2 | 2401 |
| deck-L4 | 2311 |
| deck-L6 | 2263 |
| platter | 1744 |
| cover-top | 944 |
| phono-stage | 570 |
| cover-top-tint | 506 |
| deck-L1-inlay | 505 |
| deck-L3-inlay | 441 |
| deck-L5-inlay | 426 |
| feet | 397 |
| motor | 330 |
| arm | 300 |
| platter-hub | 270 |
| bearing-housing | 261 |
| cover-C1 | 241 |
| cover-C3 | 238 |
| cover-C5 | 234 |
| cover-C7 | 230 |
| cover-C9 | 227 |
| arm-puck | 161 |
| deck-L1 | 112 |
| back-plate | 106 |
| deck-L3 | 105 |
| deck-L5 | 104 |
| foot-studs | 60 |
| cover-C2 | 57 |
| cover-C4 | 56 |
| cover-C6 | 55 |
| cover-C8 | 54 |
| bearing-nut | 54 |
| cover-C10 | 54 |
| back-hardware | 45 |
| pulley | 41 |
| spindle | 39 |
| motor-plate | 38 |
| bushes | 25 |
| foot-pads | 15 |
| platter-screws | 12 |
| cartridge | 7 |
| belt | 6 |
| motor-grommets | 5 |
