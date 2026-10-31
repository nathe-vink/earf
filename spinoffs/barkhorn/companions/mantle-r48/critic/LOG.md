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
| `outcrop-hero.png` (B, Outcrop) | studio, cover off | **5.5** | a smoked-acrylic Clearaudio / Pro-Ject-style deck |
| `outcrop-use.png` (B) | a record playing, the cover as the sleeve's frame | **6.0** | a layered smoked deck with an acrylic sleeve frame |
| `outcrop-detail.png` (B) | the arm's corner | **5.0** | a glossy black acrylic deck through a heavy filter |
| `strata-hero.png` (A, Strata Float) | studio, lid off, the base lit | **6.0** | a boutique smoked-acrylic suspended-plinth deck |
| `outcrop-hero-v2.png` (B) | the critics' notes: gray sweep, frosted etch, puck screws, stainless feet | 5.5 | a Pro-Ject or Rega-style acrylic deck |
| `outcrop-hero-v3.png` (B) | the arm's details (tag wires, pins, screws, marks), the vinyl's sheen | 5.5 | a smoked-acrylic layered-plinth deck, an off-the-shelf arm |
| `outcrop-detail-v3.png` (B) | close on the stylus and headshell | **6.0** | a modern belt-drive deck shot as a cartridge macro |
| `outcrop-ember.png` (B) | Outcrop in stock 2423 Red | 5.5 | a stacked smoked-acrylic deck with a red accent line |

## Duels against the current heroes

| new | against | new | old | winner |
|---|---|---|---|---|
| `outcrop-hero.png` | `studio-smoke.png` | 6.5 | 4.0 | **new** |
| `outcrop-use.png` | `dusk-smoke.png` | 6.5 | 4.5 | **new** |
| `strata-hero.png` | `studio-smoke.png` | **7.0** | 4.0 | **new** |
| `outcrop-detail-v3.png` | `detail.png` | 6.5 | 3.5 | **new** |

All four new frames won their duels against the site's current frames, which passes the gate. No single blind score
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

## Where it stopped, and why

The hero has had three passes (v1, v2, v3), which is the protocol's limit for a shot at one look. Its blind score held
at 5.5 while each round's specific complaints were fixed, and the critics moved on to the next layer of detail each
time. The duels are the more sensitive measure (critic/duel.py's note), and every new frame won its duel by 2.5-3.5
points.

What the last critics agree on, for whoever takes this further:
- **The Ember tint reads as a red pinstripe, not through-tint** (p8). That is the design's honest look: thin tinted
  rings round clear strata. A through-tinted Ember block at 47 mm would be black (2423 passes 14 % at 1/8 in). If the
  owner wants more color, the rings can go wider, or the caster can pour lighter Ember laminae.
- **The bought arm still reads as generic.** It is a generic arm: Rega's RB330. A bespoke arm is a product decision
  (the critics' "cooler" lists keep asking for one), not a render fix.
- **Bright internal rectangles** (the tunnel, the pockets, the notch seen through the clear strata): honest, but they
  read as debris. Next: vapor-polish them and place the phono stage's tunnel deeper, or tint the bottom stratum.
- **No caustics are claimed.** With MNEE on, tinted laminae would throw white caustics (the coordinator's note);
  none of these frames shows one where a colored shadow should fall.
