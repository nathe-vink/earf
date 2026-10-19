# Planet EARF, round 36: a designed place

The owner, on round 34's set (2026-10-19): "The stools, booths and listening area are okay, but aren't quite classy or
unique enough. Look at Ginza Music Bar in Tokyo, Jazz Spot Bokunen in Kanazawa, Space Talk in London (see their sinks),
Equal Parts in London, and A Bar with Shapes for a Name."

The lead's reading of the five bars, for our room: **a designed place, not a catalogue bar.** One saturated zone, the
speakers as an altar, a sculpted counter, furniture with a pedigree, our own material cast into one fixture, and darkness
with pools of light. The shell stays: board-formed concrete, fir beams, blackened steel, the frosted screens.

Every dimension is a proposal until the owner signs it (`r36_plan.py`). Acrylic is kept for the special things: the
speakers, the lamps, the sink, the screens (and the disc and the nameplate, which are light fittings).

## What was built, point by point

| The lead's point | In the model (`studio/engine/kit_ext/planet_r36.py`) |
|---|---|
| 1. The speakers as an altar | A niche across the back wall (4.2 m wide, 2.4 m high), lined in end-grain blocks (110 mm, each its own depth), dark-oak cheeks and soffit; the Ember pair on solid dark-oak plinths (260 mm), 2.3 m apart, toed in 19 degrees to the best seat (x 13.15, on the axis); a felt panel behind each. On the room's axis, so the bar shot sees it framed by the partition's opening. Two soffit spots wash the end grain. |
| 2. One saturated zone | The listening zone in one colour: velvet tub chairs, wool carpet, the side walls and the altar wall limewashed. Proofed two ways: bottle green (`#173326` velvet; the Ember pops against it) and oxblood (`#4A1216`; tone on tone). The bar zone stays concrete, steel, zinc and oak. |
| 3. Rooms within the room | The zone raised 200 mm on a dark-oak platform behind the smoked partition, its step at x 11.85, in line with the speakers. |
| 4. A sculpted counter | A racetrack counter 6.5 m long: a 70 mm zinc top with a rounded edge, a fluted dark-oak front (34 mm half-round staves), a steel kick, a brass foot rail on brackets; two turntables and a rotary mixer built into its back half. Behind it a quiet back bar (blackened-steel doors under a zinc worktop, one lit niche lined in timber with a few bottles) under a floor-to-ceiling record wall (dark oak, 360 mm cells, varied sleeves, some pulled out, some face out, gaps), with a 1.24 m frosted disc set into it behind the DJ station and a now-playing ledge. |
| 5. Furniture with a pedigree | Counter chairs: four tapered dark-oak legs and a stretcher ring, an upholstered round seat (chocolate mohair), a low curved oak back with an upholstered pad, seat 760. A built-in oak banquette along the right-hand wall with rounded ends, channel-tufted back, loose seat and back cushions, an oak cap; small round oak tables on steel pedestals with a chair (the same family, seat 460) opposite each. In the zone: low 1970s-style velvet tub chairs, open toward the altar, with small hexagonal oak tables. |
| 6. Our material in one fixture | The sink: a floating trough 860 x 400 x 170 cast in Ember acrylic (the engine's clear resin, its red deepening with depth), a soft ellipsoidal basin cut into its top and every edge eased, lit from below through its thickness by a warm panel; a brushed-steel wall spout; an alcove of vertical dark-oak boards between the banquette and the zone. A fourth shot, at 65 mm. |
| 7. Light | The owner's **Dome** pendant, four hung low over the counter (rim 650 over the zinc), and the squat **Sphere** (160 mm, in a low brass cup) on every table in place of candles: placeholders until the companions' kit pieces land, built here with the r32c study's treatment (smoked resin, a frosted liner within it that glows warm ivory, a thin tinted skin; the lamp hidden from the camera, transmission and glossy rays; the shells cast no shadow). The study's dome GLB is not in git (its out-study models are ignored), so the Dome is modelled here to its proportions. The changing light: the frosted disc behind the DJ station, set toward deep red for the shots. The graphic object: an etched acrylic disc by the door with EARF's wordmark. |
| 8. Acoustic treatment as craft | Fabric panels (felt in the zone's darker colour) in brushed-steel frames with a ledge of record sleeves, on the zone's right-hand wall; the end-grain lining of the altar. |
| 9. The standing asks | The record wall's spines vary in width, colour and wear, a few pulled out, some face out, part-full cells. Signs of life: a half-drunk coupe, rocks glasses, a record out of its sleeve on the counter, a coat over a counter chair. The floor honed (round 34). |

**Avoided:** tan leather (the banquette and chairs are chocolate mohair), spindle stools, catalogue lounge chairs, a
backlit bottle wall, bright even light, acrylic everywhere, speakers off to the side.

## Shots

`r36_shots.py`: the bar (down the axis to the altar), the listening zone in green and in oxblood, the street, the sink.
The critic's card (`r36_card.py`) adds the lead's question: would a design magazine publish this as a specific place,
or is it a generic bar?

    python3 spinoffs/barkhorn/planet/r36/r36_shots.py
    python3 studio/engine/render.py studio/shots/barkhorn/planet36/bar.json --out IMG --samples 48 --scale 0.3
    python3 spinoffs/barkhorn/planet/r36/r36_stage.py bar IMG TAG      # a fresh critic's message

Process as round 34: proofs at 0.3, two fresh critics per proof and their mean, a shot stops when two passes in a row
after a change of concept each gain under half a point; then the best of each at 1200 x 800 for the owner. The log is
`NOTES.md`.
