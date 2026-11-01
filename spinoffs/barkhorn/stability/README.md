# Tropos's stability: IEC 62368-1 8.6.2.2 (2026-11-01, the engineering audit's item 1)

**The test:** a static force of 20 % of the weight (at most 250 N), in any horizontal direction, at the most unfavorable
point up to 2 m: here the top of the horn. The speaker must not tip. A UL CB report for a 63/83 kg floor unit records
exactly 20 %. The earlier check (README, S7) used 13 %, the wrong basis.

**The test is geometric.** The force scales with the weight. So about each tipping edge (the line through two feet),
the speaker passes only if the center of mass sits at least **0.2 x the force's height** inside it. That is 259 mm for
the current design and 261 mm for Strata. Mass, ballast and a lower center of mass do not change this. Only the
footprint does, or where the force can be applied.

`com.py` sums every part of the render models. Each part's mass is from the parts list where it gives one (the
drivers and the amplifier spread over their pieces by volume), else its volume times its material's density. Its
centroid is its mesh's. The output is `com.json`.

| | current | Strata |
|---|---|---|
| mass, a speaker | 70.2 kg | 75.2 kg |
| center of mass behind the front panel's face | 233 mm | 222 mm |
| center of mass height | 533 mm | 553 mm |
| the push (20 % of the weight) at the horn's top | 138 N at 1.295 m | 148 N at 1.305 m |
| the arm needed, each way (with a 15 % margin) | 259 mm (298) | 261 mm (300) |

The audit's reviewer put the center of mass at 232 mm (current) and 224 mm (Strata). That agrees.

**Today's feet** (M8 swivel feet, 40 mm pads; 25 mm in from the front and back, 50 from the sides). The margin
is (arm - needed) / needed:

| tipping edge | current: foot centers | current: pad edges | Strata: foot centers | Strata: pad edges |
|---|---|---|---|---|
| forward | 208 mm, **-20 %** | 228, -12 % | 197, **-24 %** | 217, -17 % |
| back | 162, **-37 %** | 182, -30 % | 173, **-34 %** | 193, -26 % |
| sideways | 230, **-11 %** | 250, -3 % | 230, **-12 %** | 250, -4 % |

A swivel foot pivots on its ball, so the foot centers are the honest edge. **Both designs fail in every direction.**

**What passes:** the feet's centers at about **x ±300 mm and y -290 / +310 mm** about the speaker's center line. That is
a 600 x 600 mm footprint for a 15 % margin. The cabinet is 560 x 420 mm, so the feet must stand about 20 mm outside its
sides and about 80 to 100 mm beyond its front and back.

**Options.** Each changes the look, so the owner decides:
- **A. A stepped plinth** in Strata's language: three steps of 1/2 in sheet, from the cabinet's footprint out to about
  650 x 650, the feet under its corners. It is drawn as a frame, not a slab: about 8 kg (est.).
- **B. Outrigger feet:** four arms (bronze bar, or 20 mm sheet fins) from the bottom's corners out to feet at the
  600 x 600 corners. It is lighter to look at. Each arm is a cantilever and carries up to half the weight under the
  push, so it needs sizing.
- **C. Anchoring:** a wall strap or floor fixing that the instructions make part of the installation. Whether
  62368-1 then treats Tropos as fixed equipment is the lab's reading. **Ask the lab for its reading of 8.6.2.2 and
  8.6.5**, and add stability to the January pre-check.

A heavier base does not help (the ratio is geometric). A lower horn would, but it is the product.

## The owner's design: Strata with the flush horn on the lit plinth (2026-11-01)

`com.py` now also sums the design as the owner chose it:
- Strata, its stepped horn flush at 560 (the mouth 536, the lip 12);
- on base A, the stepped plinth with its light (`variants/BASES.md`);
- lifted 38.5 mm.
The force's height is the horn's top as drawn.

| | Strata on the plinth |
|---|---|
| mass, a speaker | **83.7 kg** (the plinth 9.4 kg, with its 6 mm reveal, 2026-11-01) |
| center of mass | 9 mm behind the cabinet's middle, 526 mm up |
| the push (20 % of the weight) | 164 N at 1.336 m: the arm needed is 267 mm |
| margins on the plinth's feet (centers) | **forward +19 %, back +13 %, sideways +14 %** |

**It passes in every direction with margin.** On the cabinet's own feet it still fails (Strata, flush: -23 % forward,
-34 % back, -11 % sideways), so the plinth is part of the listed product.
