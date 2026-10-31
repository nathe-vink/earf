# Hemisphere and Core: a critique before the design pass (2026-10-31)

The owner (2026-10-31, `r46-owner-notes` 6a9fa7f4): *"I mostly want to nail design, make it realistic, make it cooler,
etc. … Make it well architected, novel, lasting."* Dates and logistics are parked. This note is the critique that the
proposals in this folder answer. The current designs (`crystal.py`, `dome_pendant.py`, `orb_table.py`) stay the
baseline; nothing here overwrites them.

## A blind read first

A fresh agent saw the two current heroes (`renders/2026-10-31/barkhorn/lamps-campaign/core-bedside-look4.png`,
`dining-hero.png`) with no brief and no brand. Its words:

| | Core (bedside) | Hemisphere (dining) |
|---|---|---|
| What it is | "a glowing red-orange acrylic sphere sitting in a squat dark puck base" | "a red transparent acrylic dome pendant under a stepped black canopy" |
| Seen before | Flos Glo-Ball, IKEA FADO, salt and moon lamps | 1970s Guzzini domes, Verpan, HAY and Muuto bells |
| **Distinctiveness** | **3 / 10**: "'Red glowing ball' is a category, not a product." | **4 / 10**: "a pleasant period-revival pendant"; the stepped cap the only unusual note |
| Signature | "none I could read" | "the stepped black cap could become one if it repeated across the family" |

Its advice, in short: *make the acrylic do something only thick cast acrylic can.* Thick sections should hold the
colour and graduate it from pale to deep; polished edges should glow brighter than the faces; one repeated cut detail
should appear on every piece; and the renders should show the coloured shadows and caustics, "because that light
pattern is the real product and none of these renders show it."

**This confirms the coordinator's read.** The line is well made but reads as familiar archetypes in coloured plastic.
Its campaign scores agree: Core 6.0, Hemisphere 5.5 (`critic/LOG.md`, looks 4 and 5).

## Hemisphere: the 10 least realistic details

1. **The formed dome's walls are drawn even.** A 200 × 100 hemisphere drape-formed from 9.5 mm cast sheet is a 1 : 2
   draw. The crown thins by roughly 30 to 45 % against the rim, and the model and renders show one even wall.
2. **Three nested formed layers with a 1 mm gap** (tint 9, opal 3, skin 3) need three moulds and must stay concentric
   to under 0.5 mm. Formed shells spring back unevenly. The gap will be uneven and show as banding.
3. **The tint isn't calibrated.** TruCast 2423 transmits 14.1 % at 3 mm (A&C's chart). The shell glows an even
   orange-red, with no deepening where the wall is seen edge-on and none at the rim.
4. **The rim shows no laminate.** A polished edge cut through tint, opal and skin would show three bands. The render
   shows one dark ring.
5. **The black hardware is CG-clean:** no machining marks, no anodise grain, no visible screws, no set screw at the cord
   grip, and the bayonet pins aren't visible.
6. **Cord and suspension:**
   - the cord is a perfect rod;
   - the steel suspension cable that certification requires (`launch/certification.md`) isn't in the hero;
   - there's no cord grip or strain relief.
7. **The lamp doesn't light the room.** The table pool comes from another source; the shade throws no colour onto the
   table, the wall or the fruit. The blind read: "the lamp looks off or pasted in".
8. **Glare and cut-off aren't shown.** The COB is recessed 22 mm in a 46 bore (cut-off about 46°). Seen from a chair,
   nothing shows the bright disc or its edge.
9. **Heat, marginal on paper.**
   - The low top (crown Ø 80 × 11.5 and cap Ø 40 × 14) is about 0.010 m² of black anodised surface.
   - At about 3.3 W of heat (the COB at 4.4 W) and h ≈ 11 W/m²K, it runs about 31 K over room air. That puts the crown
     at about **56 °C, nearer 65 °C in the warm air under a ceiling.**
   - That is close to cast acrylic's comfortable service temperature (about 70 °C long-term; it softens near 95 to
     100 °C). No test exists.
10. **The scale cues and set read as CG** (blind read): a uniform wood floor, identical pears, a heavy glass.

## Hemisphere: 5 chances to make it cooler

1. **Show the acrylic's thickness.** A dome built from **stacked rings** puts a polished edge on every layer, and each
   edge reads as a contour line ("Stacked like contour lines", as Tropos's horn already is).
2. **Light the edges, not just the faces.** Light that enters a ring through its frosted inner edge leaves through its
   polished outer edge. Each terrace would glow as a line.
3. **Coloured light is the product.** The pool on the table should take the tint, and the floor and walls should carry
   coloured caustics.
4. **Make the heat sink part of the design.** A stack of aluminium fins echoing the acrylic stack would give about 10 ×
   the area of the current top, run cool, and say "laminated" in metal too.
5. **Honest, lasting hardware:**
   - stainless or brass screws where the shade comes off;
   - a cord grip you can see;
   - a cable gripper;
   - an LED module on screws, to be replaced in 20 years.

## Core: the 10 least realistic details

1. **The ball is a perfect sphere with no equator joint.** Two formed hemispheres bonded at the equator leave a bond
   line, and polished or not, it shows in tinted acrylic. The render shows none.
2. **Forming thins the poles** of each 9.5 mm hemisphere, as for Hemisphere's dome. The wall isn't even, and the
   tint deepens where the wall is thick.
3. **The ball glows evenly, "like a flat emissive disc"** (the blind read). A 2.5 W LED shining up a 40 mm port into a
   frosted ball is brightest at the bottom, falling off toward the top.
4. **The base is razor-sharp CG:**
   - no seam between the drum and the anodised ring;
   - no hatch screws or feet;
   - no felt;
   - its material is unreadable ("neither metal nor wood").
5. **The cable is a pristine tube** with no fabric weave, no slack under its own weight, and no grommet where it
   leaves.
6. **No coloured light on the table:** "a coloured transparent sphere should throw a concentrated, focused pool of
   light". A real ball in daylight throws a bright caustic spot inside its coloured shadow.
7. **The inner frost is smooth, with no texture.** Bead-blasted acrylic reads as fine grain at close range.
8. **The touch ring can't be found.** It's the control, and nothing shows it.
9. **Heat isn't a problem, but it isn't shown either.** About 2.5 W in a sealed IP44 base beside the cells, with an
   acrylic window over the LED. It's fine on paper (about 15 K rise), but no number is drawn.
10. **The props are generic** (the blind read): flat book blocks, an even blur, a very clean gradient.

## Core: 5 chances to make it cooler

1. **Stop being a ball.** A ball is the category. Something only a stack of cast sheet can be, like a **core sample**
   (a drilled cylinder of strata) or a **terraced sphere** (a globe drawn in contour lines), is EARF's own.
2. **A chosen stack of tints:** one tint, or a stack of several (Ember over Dust over Acid: a sunset core). The
   Tint Library made into a lamp.
3. **Light from inside the strata:**
   - a frosted bore with a filament of light up the middle;
   - each band glowing at its polished edge;
   - the bond lines faintly refracting.
4. **Caustic pools:** in daylight, a thick tinted cylinder or sphere focuses the window's light into a coloured spot
   on the table. In the evening, it throws coloured bands.
5. **Lasting by construction:**
   - thick sections that can be re-polished;
   - a light engine on three screws that drops out of the bottom;
   - a knurled stainless dimmer knob instead of a hidden touch circuit;
   - the base, the plug-in v1, kept with the battery as an option.

## What the proposals do with this

Two proposals for each lamp, in two family directions, all laminated from stock cast sheet (no moulds):

| | Core | Hemisphere |
|---|---|---|
| **Strata** (straight: the core sample) | **Core Sample**: a column of bonded tint discs, bored, lit by a filament | **Crown**: the current formed dome, with a laminated acrylic crown and a stacked aluminium fin sink |
| **Contour** (curved: terraces) | **Contour Core**: the ball drawn in 14 terraces, lit by an opal globe inside | **Terrace**: the dome built from 12 stacked rings, each edge a glowing contour line |

The design notes, drawings and renders for each are in this folder's `README.md`.
