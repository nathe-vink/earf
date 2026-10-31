# Tropos: the owner's horn choice, in stock colours (2026-10-31)

There are three routes for the horn, each in the two stock colours. They share one rig and one light (studio31's horn
macro), and the speaker is turned so the camera sees the mouth from the front.
- **Formed:** stock 3/8 in sheet, pressure-formed.
- **Laminated, stepped:** 22 layers of stock 1/2 in.
- **Laminated, smooth:** the same stack, machined smooth outside.

There is also a close view of the terraces, and the site's tints beside the stock pair's. The colours are estimates
from published light transmission (`spinoffs/barkhorn/make/stock_tints.py`, the "held" case), until the chips and
off-cuts are measured.

| file | what |
|---|---|
| `compare-ember.png`, `compare-smoke.png` | the three routes side by side (proofs) |
| `choice-{formed,stepped,smooth}-{ember,smoke}.png` | each route at full size (1600 x 1600, 128 samples) |
| `choice-terraces-ember.png` | the stepped horn's terraces close |
| `lineup-stock.png` | left to right: Ember as on the site, Ember in stock sheet, Smoke as on the site, Smoke in stock sheet; the stock two with the stepped laminated horn |
| `proofs/` | half size, 48 samples |

Shots: `spinoffs/barkhorn/campaign/shots.py` (`horn_choice`, `lineup`). Flavours: `spinoffs/barkhorn/stock_colours.json`.

## What the pictures say

- **Ember.**
  - The formed horn's 5 to 8.5 mm shell is a pale glassy red, with the throat and pod a dark shape through it.
  - The stepped horn is the deepest red. Its 22 terraces step into the throat like strata: the strongest picture.
  - The smooth horn is a deep lens with fine contour rings, between the two.
- **Smoke.**
  - **The formed horn in stock 2074 is nearly clear.** It is a pale smoked glass, and the black throat, pod and driver
    show through as a hard shape. A formed Smoke horn needs the custom deep lot to look like the site; stock sheet is
    not enough.
  - The stepped horn reads dark between bright silver terrace edges, like a core sample or a contour map.
  - The smooth horn is paler than the stepped one, a smoked lens with rings.
- **The line-up.**
  - The stock Ember cabinet (a Chemcast 2423 run) and horn (stock 2423) are barely distinguishable from the site's.
  - The stock Smoke cabinet (2064 3/4 in) matches.
  - The stock Smoke horn is lighter and more silver than the site's near-black.
  - **A stock-colour pair still looks like EARF.**

## Recommendation

**The stepped laminated horn.** It is the deepest colour from stock sheet in both colours. It is the only route that
makes January (`spinoffs/barkhorn/make/schedule.md`), and the cheapest for the prototype pair. Its look is strata, the
brand's own idea. Cost and the trade at volume are in `spinoffs/barkhorn/make/laminated-horn.md`.
