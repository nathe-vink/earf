# Faults in the current Mantle (the design on the site), whatever is chosen for its looks

These are from a fresh engineering review of the drawing package (`critic/r1-baseline/cad-review.md`). The reviewer
saw only the 19 drawing sheets, the parts list, the cut list, the checks and `turntable_float.py`. I checked each one
against the CAD and they hold. `checks.json` passes because it only looks for clashes.

| # | fault | the numbers | fix (both round-48 proposals carry it) |
|---|---|---|---|
| 1 | **The light slot leaves 1 mm of base.** | 10 mm base, 9 mm slot from below, a 1 mm skin spanning 300-390 mm. Cast 10 mm sheet varies by about ±0.8 mm, so the cutter breaks through. | A thicker base (12.7), the slot 6 deep and 25 in from the edge. |
| 2 | **The float sits in the feedback band.** | About 9.4 kg on four bushings (2.35 kg each, not 1.8), k about 60 kN/m: 25 Hz, about 36 Hz once the nut clamps the second bushing. Speakers feed back at 25-40 Hz. | Rigid posts (torqued studs), with the isolation in the feet. |
| 3 | **The motor pod tips under the belt.** | 2.4 kg on soft pads 44 mm apart, with the belt pulling about 90 mm up: about 0.18 N m against about 0.26 N m of weight. The pulley's height runs through the feet, the Sorbothane and the lid's weight. | Hang Rega's motor from the plinth on Rega's own grommets, as a Rega does. |
| 4 | **The bearing's inserts can crack the plinth.** | M4 inserts (6 holes) at r 22 leave 2.8 mm of acrylic beside the 32.4 bore. 3-5 µm of running clearance is too tight for oil; 8-12 µm is normal. | A threaded housing (M30 x 1.5) clamped by a nut under the plinth; bushes to 10 H6 on a g5 spindle. |
| 5 | **The hub and spindle are assembled in the wrong order.** | The brass hub is bonded into acrylic, which expands about 3.7 times as much as brass, and then the spindle is pressed into it. | Shrink the spindle into the hub first, then screw the platter to the hub's flange (six M4). |
| 6 | **The 25 mm plinth stock can't be faced flat as drawn.** | Cast 25 mm varies by ±1.5-2 mm. The laminated 2 x 12.7 prototype is "machined to 25.4", which leaves no stock. | Laminate from thinner stock and fly-cut both faces; or buy 30 and face it to 25. |
| 7 | **The arm's mounting and height are not designed.** | One nut through 25 mm of acrylic creeps. The record's height over the plinth (25.8) appears on no sheet. | An aluminum arm-board puck with Rega's three-point fixing; the spacer stack drawn. |
| 8 | **The lid is twice the hinges' rating.** | 2.2 kg, about 2.7 N m at 45° (1.4 N m a hinge). Debut hinges carry about a 1 kg lid. "12 degrees past upright" is drawn as 12 degrees short. | A 3 mm lid (1.1 kg); or hinges with a stated torque. |
| 9 | **The light and the phono stage share a supply.** | One adapter on a Y lead feeds both the 25 kHz PWM dimmer and the phono regulator, on a shared return. The LED's power is 4.7 W in the notes and 6.8 W in the parts list. | The phono stage on its own listed adapter. |
| 10 | **The webs are thin and servicing is from below.** | The 96 pod hole leaves 16 and 19 mm webs, and the hinge inserts go into the 19. The phono stage's switches can only be reached by tipping the deck. | Webs of 24 mm or more; the phono stage in a tunnel that slides out from the back. |

Also missing from the drawings: a bearing section, fits and finishes, the oil level, a wiring and earth diagram, and a
rating label. They are drawn for Outcrop in `out-outcrop/drawings/details.png`.

The parts list and the drawings also disagree in two places: the posts (a tinted tube 40 x 40 x 44 in the list, clear
rod 30 x 34.4 in the drawing) and the mark (40 wide in one, 44 in the other).
