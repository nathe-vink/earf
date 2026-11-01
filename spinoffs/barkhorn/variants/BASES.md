# Strata's base: A, a stepped plinth, and B, outrigger feet (2026-11-01)

**The owner chose A, lit from underneath** (2026-11-01: "can we make them light up from underneath? If so I'd go with
the one on the left"). B is kept below as the alternative drawn; the blind duel between them was not run.

**Why:** IEC 62368-1 8.6.2.2 pushes at the horn's top with 20 % of the weight. The speaker passes only if its center
of mass sits at least 0.2 x that height inside every tipping edge (`stability/README.md`). On today's feet, Strata
fails by 24 % forward, 34 % back and 12 % sideways. The fix is geometric: the feet's centers at about 600 x 600 mm.
Both proposals put four M8 levelling feet at the same points: **x -25 / 585 and y -94 / 526** in the Cabinet's frame
(the cabinet is 560 x 420, its front at y 0), that is, about 300 mm from the center of mass each way.

The CAD is `variants/variants.py`: `PLINTH` and `OUTRIG`, the options "Plinth" and "Outriggers". The shots are
`campaign/shots.py`: `base-plinth`, `base-outriggers` and `base-today`, each with a `-34` three-quarter view.

## A. The stepped plinth

**The design:** three frames of the cabinet's own 1/2 in stock sheet, stepping out under it like the caldera and the
horn's terraces:
- 600 x 460 under the cabinet;
- then 630 x 566;
- then 660 x 670 on the floor;
- each a frame about 80 to 155 mm wide round a 440 x 300 opening;
- the outside edges polished, the three bonded;
- the cabinet bolted down through its own feet's M8 inserts.
It lifts the cabinet 38.5 mm.

| | |
|---|---|
| footprint (the feet's centers) | 610 x 620 mm; the base itself 660 x 670 |
| weight | **10.4 kg** (computed from the CAD), so the speaker with the flush horn is **84.6 kg** |
| cost, a speaker | about $260 of sheet ($0.03/cm3) + about $250 of cutting, polishing and bonding + $18 of feet: **about $530** (est.) |
| the push | 166 N (20 % of 84.6 kg) at 1.336 m: the arm needed is 267 mm |
| margins (the feet's centers) | **forward +19 %, back +14 %, sideways +14 %** (computed: `stability/com.json`, `strata_plinth`; the flat underside, rerun 2026-11-01 after the reveal was dropped) |

## B. Outrigger feet

**The design:** four arms of bronze bar, 30 x 20, the same bronze as Strata's posts:
- each from under one of the cabinet's corners (two M8 into inserts in the bottom: its foot's own and a second) out
  on the diagonal to a foot;
- the ends rounded, the bar's faces satin.
It lifts the cabinet 20 mm.

| | |
|---|---|
| footprint (the feet's centers) | 610 x 620 mm; the arms reach about 75 mm past the sides and 95 to 105 past the front and back |
| weight | four arms about 1.24 kg each, 4.95 kg, so the speaker is about 80.2 kg (est.) |
| cost, a speaker | about $70 of bronze ($0.12/cm3) + about $200 of machining and finishing + $18 of feet: **about $290** (est.) |
| the push | 157 N at 1.325 m: the arm needed is 265 mm |
| margins | **forward +19 %, back +15 %, sideways +15 %** (est.) |
| each arm | at the tipping point a foot carries up to about half the weight, 390 N. 110 mm outside the cabinet, that is 43 N m on a 30 x 20 section: about 22 MPa, against bronze's 125+ MPa yield |

## Both

- **They pass with margin, each way.** Anchoring stays a lab question for the January pre-check, not a design option.
- **They are drawn on Strata;** the smooth horn sits on either.
- **They change the look.** The owner chooses, after a blind duel judged on looks alone (the critic sees no
  stability numbers).

## A, lit: the plinth's light (2026-11-01)

The idea is the same as Mantle floating on its own light: a soft, warm glow from under the lowest step onto the floor.
The steps' polished edges catch some of it.

**The light:**
- **The strip:** COB (dotless) LED, 24 V, **4.8 W/m, 2700 K, CRI 90+ (R9 above 50)**, 8 mm wide (`plinth-led`).
- **The channel:** a shallow aluminum channel, about 10 x 4, with a frosted PMMA diffuser, bonded into a groove routed
  in the bottom frame's underside, **40 mm in from its outside edge all round**. The underside is flat (no reveal).
- **Broken at the feet:** the strip runs in four lengths, each stopped 30 mm short of the corner so it clears the foot
  pads there (the pads reach 45 mm in from the edges; the strip at 40 would run over them). The lengths are joined by
  short soldered jumpers across each corner (the coordinator, 2026-11-01).
- **The light's path:** the strip faces the floor. The plinth stands 12 mm up on its feet, so the light leaves at the
  bottom step as a thin warm line on the floor, with some light entering the bottom frame and showing at its polished
  edge. This is the look the deck hero shows: **glow 20 by day and 40 at dusk** in the pictures.
- **Length and power:** 2.1 m a speaker, so **10.1 W at full** and 5.0 W at the default 50 %.

**Tested and not adopted** (2026-11-01; the deck's comparison rows at 1664 x 520 and the Ice front-off-wide proofs, half
size, all in `renders/2026-11-01/barkhorn/`). The aim was a soft pool on the floor in place of the line.
- **The bare strip at 40 at lower strengths** (`deck/tropos-eight-row-led40/20/10.png`): the line thins but stays a line.
  Kept, at glow 20 by day.
- **90 in behind a 40 x 3 opal diffuser** (`deck/tropos-eight-row-pool20/40.png`): a broader warm band under the dark
  tints, but the diffuser glowed through the clear frames. Not adopted: still a line on the light tints.
- **A 6 mm reveal under the bottom frame's outer 70 mm** (`deck/tropos-eight-row-reveal20/40.png`,
  `site-strata/proofs/front-off-wide-ice-reveal.png`): more warm light on the floor, but the light piped through the
  clear frame and lit its underside as a wider band. Not adopted: it doesn't stop the line, and it costs about 1 kg of
  machining and a point of tipping margin. (A 15 mm reveal does not fit the 1/2 in frame.)
- **A sealed, removable black U-channel, 90 in** (`deck/tropos-eight-row-sealed20.png`,
  `site-strata/proofs/front-off-wide-ice-sealed.png`): the frame stays in its own tint, but the light lands under the
  plinth, hidden by the step. Not adopted: no pool reaches past the step.
- **The same channel at 40 in** (`deck/tropos-eight-row-sealed40in-20.png`, `site-strata/proofs/front-off-wide-ice-sealed40in.png`):
  a crisp warm line on the floor under the edge, the frame clean. Not adopted: it is the same line as the bare strip at
  more cost. It stays the alternative if the frame's glow is ever unwanted (`PLINTH_LIGHT['sealed']` in `variants.py`;
  `plinth-channel` in `components.json`).
- A real pool past the step needs the light further from the floor (taller feet, about 50 mm). That changes the look,
  so it is the owner's to ask for.

**Power, separate from the FA122's mains:**
- **A plug-in supply, 24 V, 15 W, UL listed Class 2** (UL 1310) or IEC 62368-1 PS1 (`plinth-supply`), with a 2 m lead
  to a DC socket under the plinth's back edge.
- It stays outside the speaker's mains circuit, so the speaker's listing need not cover a second mains converter.
  The plinth's own circuit is Class 2 / PS1 throughout.
- **No aux rail on the FA122 is used.** Hypex publishes no 24 V auxiliary output for it, and drawing from its internal
  supplies would void their assumptions (asked in the Hypex letter).

**Control** (`plinth-controller`, a small board in the plinth):
- **On with the amplifier, off in standby.** The board's enable comes from the FA122's on/standby state through an
  opto-isolator. The state line still has to be confirmed with Hypex: the remote kit's status LED on J15 is a
  candidate. Until then, a switch under the back edge.
- **Dimmable:** four steps (off, 25, 50, 100 %) on a touch pad under the plinth's back edge, 50 % by default. PWM at
  about 20 kHz, so it is flicker-free on camera.
- **Wiring:** the state line leaves the amplifier compartment through its third M12 gland (as the IR receiver's lead
  does on the master) and down the back to the plinth, on a 3-pin plug.

**Heat next to the acrylic:**
- 4.8 W/m in an aluminum channel runs about 10 to 15 K over room (est.), so under 40 °C in a warm room.
- Cast PMMA is good to about 80 °C. The channel spreads the heat, and the strip never touches the acrylic directly.
- Checked on the first plinth with a thermocouple after 4 hours at full.

**Shipping and set-up:**
- The plinth ships flat in its own carton (about 700 x 710 x 80, about 13 kg), apart from the speaker's crate.
- At set-up the plinth goes down first and is leveled on its four feet. The speaker is lifted on (two people, its
  feet removed), and four M8 bolts from under the plinth go into the cabinet's own foot inserts, through counterbored
  holes.
- Then the state lead plugs in and the supply connects.

**Stability with the plinth:**
- The plinth makes the speaker heavier and lower, but the test is geometric: its feet carry the margins in the table
  above.
- With the flush horn drawn, the margins are recomputed from the CAD (`stability/README.md`): +19 / +14 / +14 %.
- **The plinth is not optional for a listed product.** On the cabinet's own feet the speaker fails the 20 % push in
  every direction. A lab's acceptance of anchoring is the only other route.
