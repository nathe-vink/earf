# Tropos's horn: the forming trial, before the full plug (2026-10-31)

Before the full prototype plug is cut ($7,100 with its base), form a quarter of the horn at full scale. That trial
answers the questions that decide the route.

## The trial plug

`horn-trial-plug` and `horn-trial-base` in `horn_options.py` (its drawings and parts list in `out-horn-options/`).
The trial plug is the production plug's own surface, from the same CAD and the same 5-axis program, cut to one
quadrant: the throat end and the mouth's lower corner, at full scale.

- Its two cut faces run 30 mm past the axis, so the throat end is whole where the sheet first touches.
- The cut faces are drafted 15° outward toward the base, so the sheet forms over them and comes off.
- It is cut in the same high-temperature epoxy tooling board as the full plug, about 410 x 280 x 260, and bolted to a
  board base 420 x 300 x 40.
- It keeps the mouth's lip and the cove at the plug's foot. The corner is formed last and is the thinnest; that is
  where webbing would start.

## The trial

Three shots, formed by the shop that will form the horn, on its press, with its oven and its frame:

1. **Clear stock 10 mm cast sheet**: the process, without the dye's effect on heating.
2. **The darkest stock tint available in 10 mm** (a transparent red or a smoke): the dark lot's heating (risk F4), and
   the colour at the real thickness.
3. **A second dark shot** after any change to the settings.

Each blank is about 560 x 440, a quarter of the full blank.

## What is measured

- **The wall** (risk F1): each shot is cut along the corner's diagonal and along the middle of the bottom wall. A
  Hall-effect gauge reads 30 points: the throat end, the flare, the lip, the corner and the flange. Pass: 4.0 mm or
  more everywhere, 4.5 or more to keep 10 mm sheet.
- **Webbing** (F2): none in the corner's cove, by eye and to the touch.
- **Mark-off** (F3): the air face under raking light, against a limit sample.
- **Release and shape** (F7): the shot scanned (an arm or a structured-light scan) against the plug's CAD: the air
  face within 0.3 mm.
- **Heating** (F4): the sheet's core and surface temperatures logged, and no bubbles or scorch on the dark shot.
- **Colour**: the dark shot's flare beside a 20 mm cabinet coupon, in daylight and in the studio's light, photographed
  on a white light box. This also tests the horn lot's needed dye load against the estimate of 6 to 10 times the
  cabinet's.

## What it costs

| item | budget |
|---|---|
| the trial plug in tooling board, cut and sealed (the kit's line, `out-horn-options/bom.md`) | $1,928 |
| its board base | $322 |
| three blanks of stock 10 mm cast sheet (one clear, two tinted) | about $150 |
| the shop's setup and three shots | about $700 |
| sectioning, gauging and scanning (in house, or a metrology bureau for the scan) | about $350 |
| **the trial** | **about $3,450** |

That is about half the full prototype tooling ($7,100; $9,600 with the trim fixture). If the trial fails, the route changes to Plan
B (`make/plan-b.md`) before the full plug is cut, and the saving is most of that. If it passes, nothing is lost: the
program and the board supplier are proven, and the plug's corner geometry is confirmed.

## What it proves, and what it does not

**Proves:**
- the wall in the corner, the thinnest place;
- webbing in the cove;
- the lip's roll and the flange's flatness;
- the release from the plug and the air face's accuracy;
- the dark sheet's heating;
- the colour at the real thickness.

**Does not prove:**
- the full blank's sag and clamping;
- the opposite corners (by symmetry they should match);
- the trim fixture;
- the cemented joint to the throat piece.

The first full shots prove those.
