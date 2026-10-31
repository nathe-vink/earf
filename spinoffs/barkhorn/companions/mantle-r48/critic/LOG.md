# Round 48 critic log (Mantle)

Each critic is a fresh agent. It gets the image under a neutral name, a one-line card, `critic/measure.py` and the text
of `PROMPT-realism.md` (stage 1 on PROMPT-promo's blind scale). Each duel is a fresh agent with `critic/ab/PROMPT-DUEL.txt`
and the two frames in a random order (`*.order.json` says which was new). Replies are in `r1-baseline/` and
`r2-proposals/`. The gate is a blind 7.0, or winning duels against the current hero.

## Blind scores

| frame | what | blind | reads as |
|---|---|---|---|
| baseline `studio-smoke.png` | the site's studio hero, lid open | 4.5 | a generic two-tier acrylic deck (Pro-Ject / Rega archetype) |
| baseline `dusk-smoke.png` | the dusk hero | 4.5 | a generic smoked-acrylic deck in a blue CG render |
| baseline `open.png` | lid open from the left | 4.5 | the stacked-acrylic archetype under a stock dust cover |
| baseline `detail.png` | the arm at rest | 4.5 | a generic black gloss deck, placeholder cartridge |
| `core-hero.png` (B, Outcrop) | studio, cover off | **5.5** | a smoked-acrylic Clearaudio / Pro-Ject-style deck |
| `core-use.png` (B) | a record playing, the cover as the sleeve's frame | **6.0** | a layered smoked deck with an acrylic sleeve frame |
| `core-detail.png` (B) | the arm's corner | **5.0** | a glossy black acrylic deck through a heavy filter |
| `strata-hero.png` (A, Strata Float) | studio, lid off, the base lit | **6.0** | a boutique smoked-acrylic suspended-plinth deck |

## Duels against the current heroes

| new | against | new | old | winner |
|---|---|---|---|---|
| `core-hero.png` | `studio-smoke.png` | 6.5 | 4.0 | **new** |
| `core-use.png` | `dusk-smoke.png` | 6.5 | 4.5 | **new** |
| `strata-hero.png` | `studio-smoke.png` | **7.0** | 4.0 | **new** |

All three new frames won their duels against the site's current frames, which passes the gate. No single blind score
reached 7.0. The critics' estimates with their notes applied ran 7.5-8.0.

## What the critics still see, and what was done

- **The arm and cartridge read as stand-ins** (every critic). The RB330 and 2M are modeled from their published geometry
  and photographs, and fuller than the kit's envelope. They still lack tag wires, the lead's exit and printed marks.
  This is the next modeling job; it is a picture fix, not a design change.
- **The black band above the sweep** (hero): the sweep's back is now lit to gray (`bg` light), in the v2 frames.
- **The wordmark reads as a white decal** (all): now a frosted etch a shade deeper.
- **Ghost slabs and amber "toffee" inside the deck** (hero): the bores are now vapor-polished and the feet stainless.
  It is the honest look of a clear block with parts inside; fewer, quieter shapes.
- **Front faces crushed to black, and the cover pure black** (in use): a low back window now lights through the strata
  and the stood cover, with a thin edge strip (v2).
- **Detail focus on the deck, not the cartridge** (detail): refocused on the stylus at f/5.6, the label a stop down (v2).
- **The lit base read as a tan birch band** (Strata): by day the strip should be off or far lower. A note for its next
  frame.
- **"Still the clear-deck archetype"**: every critic says it. The Outcrop cover-as-frame and the closed strata block
  are the moves no Pro-Ject has. The critics who saw only the open deck could not see them, and the closed frame is
  for that.
