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
| 5. Configurations | One parameter, `config`, a tint per product group (`r37_plan.CONFIGS`): **Smoke** (the house configuration), **Ember**, **Ice**, **Mixed** (the bar pair and the Domes in Smoke, the listening pair and the Orbs in Ember). The record players follow the bar. The Dome and Orb glow 1.1 smoked and 0.4 coloured. |
| 6. Shots | `bar-<config>` (the hero: standing at the counter's customer side, the eye at 1.55, square across the zinc to the back bar: the pair in its niches, the decks, the Domes) and `listening-<config>` in all four; `street` and `sink` once, in Smoke. |

**Choices, confirmed by the lead (2026-10-20):**

- Two record players at the decks (a DJ pair), not one. The brief says "a record player"; one is a one-line change.
- In the Mixed configuration the record players follow the bar pair, in Smoke.
- The niche is 40 mm deeper than briefed, for the 100 mm behind the cabinet.
- The bar pair stays on the floor (the horn at a drinker's ear at the counter, as Ginza). From the banquettes the counter
  hides the lower cabinets; the hero bar view stands at the counter (eye 1.55) and looks over the zinc into the niches.

## Process

Proof the base in Smoke through the critics. Proofs are at 0.3 scale, with two fresh critics per proof and their mean.
A shot stops when two passes in a row each gain under half a point. Then render the configurations at proof size,
and the best of each at 1200 x 800 as a configuration sheet. The log is `NOTES.md`.

    python3 spinoffs/barkhorn/planet/r37/r37_shots.py
    python3 studio/engine/render.py studio/shots/barkhorn/planet37/bar-smoke.json --out IMG --samples 48 --scale 0.3
    python3 spinoffs/barkhorn/planet/r37/r37_stage.py bar-smoke IMG TAG      # a fresh critic's message
