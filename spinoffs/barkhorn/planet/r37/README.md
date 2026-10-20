# Planet EARF, round 37: the bar as a showroom

The owner, on round 36 (2026-10-20, verbatim through the lead): "Why are we doing red acrylic for the bar? I do like
the warmer lighting, but overall one thing I want to demonstrate is configurability of the bar. The same way the lights
can swap, we could swap speakers and the record player, and have multiple variations. Harder with the sink though. But
the bar is kind of meant to serve as a showroom. We could also build speakers into the bar and have them in the
listening area as well, so four total. Not sure if you'd design them differently if they are set into the bar area
like ginza music bar does."

Kept from round 36: the racetrack counter, the record wall, the rebuilt chairs, the altar, the sink's new form, the
neon fix (the speakers' own lamps at 1 and 4 W/m2, measured in a Standard view) and the warm light.

Every dimension is a proposal until the owner signs it (`r37_plan.py`).

## What changed, point by point

| The lead's point | In the model (`studio/engine/kit_ext/planet_r37.py`, on round 36's builders) |
|---|---|
| 1. A neutral, warm room | No saturated zone: the zone's velvet, carpet, limewash and felt in deep warm neutrals (espresso velvet `#3A2A20`, warm grey limewash, dark brown carpet, charcoal felt). The counter chairs' seats espresso leather (`#2E1E16`), the banquette espresso mohair. The disc behind the decks warm white. The colour comes from the products alone. |
| 2. Four speakers, one product | The listening pair stays on the altar. The bar pair stands on the floor in two niches in the back bar, centred 1.35 m either side of the decks (x 5.55 and 8.25), facing the counter, as Ginza's Tannoys sit in theirs. Each niche: 700 wide, 1600 high inside, 560 deep overall. That is 40 mm deeper than briefed, so a 428-deep cabinet keeps 100 behind it for the amp and its cables. Dark oak with a proud face frame, lined in charcoal felt, and a hidden warm strip in its head grazing down the cabinet. The steel doors, the zinc worktop and the record wall's lowest cells stop at the niches. The now-playing ledge moved left (x 3.62 to 4.72) to clear the left niche. |
| 3. The sink in Smoke | The slab's tint `#3A3836` (the speakers' Smoke); its glow, a volume inside the cast, warm amber `#FFA24A`. |
| 4. EARF's record player at the decks | R3 Float (companions/concepts2.py on main; its GLB built here with the CAD venv), a pair on the counter's back half in place of the built-in decks, turned to the bartender, in the configuration's tint, their edges lit (glow 0.6). A record on each platter. |
| 5. Configurations | One parameter, `config`, a tint per product group (`r37_plan.CONFIGS`): **Smoke** (the house configuration), **Ember**, **Ice**, **Mixed** (redefined by the lead, 2026-10-20, so the speakers and lamps differ in each view: the bar pair Ice under Dust Domes with the R3s in Fog, water-clear; the listening pair Ember with Acid Orbs). A lit lamp's colour is its flavour's own glow behind its shell (`LINER_GLOW`), so it sits within about 10 deg of hue of the speakers in its tint. Ice here is the blue Cloud (`cloud-blue`); the product finals call Fog "ice". |
| 6. Shots | `bar-<config>` (the hero: standing at the counter's customer side, the eye at 1.55, square across the zinc to the back bar: the pair in its niches, the decks, the Domes) and `listening-<config>` in all four; `street` and `sink` once, in Smoke. |

**Choices, confirmed by the lead (2026-10-20):**

- Two record players at the decks (a DJ pair), not one. The brief says "a record player"; one is a one-line change.
- ~~In the Mixed configuration the record players follow the bar pair, in Smoke.~~ Mixed redefined (above): the R3s in Fog.
- The lamps' hardware (the owner, 2026-10-20): black anodised hub and catch, black acrylic canopy, no brass; the Orb on a black polished acrylic cup with a black anodised touch ring, wired in the bar by a thin black fabric cable through a grommet in its table. Made locally (`r37_plan.ANODISED`, `BLACK_ACRYLIC`; `earf_moon` `parts` and `cable`) until the companions kit lands.
- The niche is 40 mm deeper than briefed, for the 100 mm behind the cabinet.
- ~~The bar pair stays on the floor~~: corrected by the owner with a photo of Ginza ("They are elevated at Ginza."). The
  pair stands on oak ledges at counter height (1.07), the steel doors beneath, each on an oak wedge tilted 6 deg down and
  toed in about 15 deg toward the counter's middle; the niche starts at the ledge, 1450 clear, 620 deep (the lead's
  choice: 6 deg at 620); the cabinet's top leans about 80 past the face frame.
- The bartender's aisle kept at a working 0.9 m (the lead): the counter moved 200 toward the banquette (its back edge
  4.55, the niches' face 5.45).
- Ginza's details: a warm strip under the counter's top edge; one brass sconce with a glass chimney on the record wall;
  a "Sorry, no requests" tent card by the decks (taken out of the finals, 2026-10-20: the owner, verbatim through the lead, "EARFcoin. Acrylic coins with the EARF globe on them that can be exchanged for a song request. Each guest gets one." Round 38 puts a request column there; the spot is left clear); the R3s' own covers over the decks; candles in glasses on the counter.
- The hero bar view seated at the counter (eye 1.35), a soft ceiling spot on each cabinet of the bar pair.

## Process

Proof the base in Smoke through the critics. Proofs are at 0.3 scale, with two fresh critics per proof and their mean.
A shot stops when two passes in a row each gain under half a point. Then render the configurations at proof size,
and the best of each at 1200 x 800 as a configuration sheet. The log is `NOTES.md`.

    python3 spinoffs/barkhorn/planet/r37/r37_shots.py
    python3 studio/engine/render.py studio/shots/barkhorn/planet37/bar-smoke.json --out IMG --samples 48 --scale 0.3
    python3 spinoffs/barkhorn/planet/r37/r37_stage.py bar-smoke IMG TAG      # a fresh critic's message
