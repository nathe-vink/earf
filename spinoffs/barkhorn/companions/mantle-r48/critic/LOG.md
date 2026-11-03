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

## Strata Float v2 (the coordinator's head-to-head notes; two rounds, as asked)

| frame | round | blind | the critic's main note |
|---|---|---|---|
| `strata-v2-ice-custom.png` | 1 | 5.0 | the deck's edges near-black with blocky royal-blue patches; the sub-plinth reads darker than the top |
| `strata-v2-dusk-ember-custom.png` | 1 | 5.5 | the base glow a clipped peach "gaming LED"; the deck's front face crushed |
| `strata-v2-ice-custom-r2.png` | 2 (a raking front strip and card) | 5.5 | still cobalt patches and dark bands on the deck's edges; the arm a primitive |
| `strata-v2-dusk-ember-custom-r2.png` | 2 (the glow redder, 1.5 stops down) | 5.5 | the front edge near-black with flat red rectangles; the glow still reads as an LED strip |

v2's design fixes (one grid, a subordinate base, one-slab tiers, bonded posts, a small edge mark) drew no complaints in
either round: none of the four critics named a double sheet, a second grid, a screw through a post or a bold mark.
What they still see is a rendering truth about thick tinted acrylic. Seen edge-on, a long path through the deck's
custom tint goes dark, and the light it does pass comes through in patches, where the polished faces refract what lies
behind. A photograph of the real slab would show the same. A brighter, more even edge needs a lighter pour, or the
deck's edge frosted or chamfered to collect light. Both are design choices for the owner, not render settings.
Stopped at the two rounds asked for.

## Strata Float v3 against Outcrop (the coordinator's detail notes; the same rig, custom Ice, both orders)

| round | v3 frame | v3 shown | v3 | Outcrop | winner |
|---|---|---|---|---|---|
| 1 | `strata-v3-ice-custom.png` (polished deck edge, a raking front strip) | first | 4.0 | 6.0 | Outcrop |
| 1 | the same | second | 4.5 | 6.0 | Outcrop |
| 2 | `strata-v3-ice-custom-r2.png` (the deck's outer edge satin) | second | **6.5** | 5.5 | **v3** |
| 2 | the same | first | 6.0 | 6.5 | Outcrop |

Round 1's verdict was the same from both judges: the thick polished edge refracted the set in blocky blue patches.
Round 2 satin-finished the deck's outer edge (bead-blasted, a real shop finish, now in the deck's notes). The patches
went, and both judges called v3's edges clean. Both orders together: v3 1-1, mean 6.25 to 6.0. What still costs it:
- no legible mark: both judges wanted one, where the coordinator's earlier judges called the bold one cheap. A small
  frosted mark on the front edge is the middle;
- the satin top reads "flatter" to one judge. It is the top's reflection of the set, not the top's finish, which
  stays glassy;
- the deck's front reads as a dark band;
- faint marks on the top edge (the posts' bonded seats, seen through the deck).
Stopped at the two rounds asked for.

## The light up through the acrylic (2026-11-03; a new light, so a new count; one round, as asked)

| frame | blind | reads as | the critic's main notes |
|---|---|---|---|
| `renders/2026-11-03/barkhorn/mantle-r48/a-night-ember-2423.png` | **5.5** | "a black gaming-PC-style turntable with red LED edge strips" | the slab reads opaque black, only its edges red (65 % of its pixels crushed); a neutral wash makes the floor the brightest area; the inset line over the groove has no visible cause; no red on the platter and arm |

Below the owner's bar of about 6.5. Most of the gap is the stock tint: Ember 2423 passes about 2.2 % through the 25.4
deck, so lit from inside it still reads as a black slab with a glowing rim. A lit "red lantern" needs the lighter deck
of open question 8. The critic also asked for a red pool on the floor, which the owner has ruled out, so that note is
not a fix. It would score 7.5 with its notes applied (its estimate). No second round was run.

## Round 2: the deck as a lantern (2026-11-03; one round, as asked)

| frame | blind | reads as | the critic's main notes |
|---|---|---|---|
| `renders/2026-11-03/barkhorn/mantle-r48/a4-night-ember-2423.png` (v4, the lit deck) | **5.5** | "a Pro-Ject or Rega-style acrylic deck lit like a gaming-PC LED panel" | the glowing slab throws no red on the floor; the top a flat, clipped salmon field (25 % clipped); the edge reads as thin parallel bands; the support, arm and cartridge read generic |

The same score as round 1, for other reasons. The outline is gone, and the critic now sees a lit panel. Two of its notes
are settings or the renderer, not the design:
- the top's clipping is the night exposure (a stop over the day's): a stop down keeps the red deep;
- the shelf gets no red because light leaving the glass to reach a diffuse face is a caustic path Cycles drops here. A
  real deck would throw a faint red spill under its edges, which the owner allows (a pool he does not).

Its "cooler" list asks for the edge-lit look of round 1 again ("the face deep red and the perimeter burns"), the
opposite of what the owner asked for. No second round was run.
