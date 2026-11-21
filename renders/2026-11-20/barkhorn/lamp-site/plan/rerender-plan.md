# The re-render pass: plan (2026-11-21, draft, not rendered)

This is one pass that re-renders every lamp picture on the house ground with the owner's pours, re-measures the lumens, and feeds the bar pictures. It starts after the off sheet of all seven tints passes the by-eye check and the owner.

## 1. Pours: one table, made the code's default

So far the pours were set per frame from the environment. For the pass they go into `lamp_site.py` itself, so every runner, helper and later picture gets them with no switches:

- the pendant's pours go in `TINT_LOAD` / `HEMI_MIX`;
- the Core's pours go in `CORE_TINT_LOAD`;
- the Core's re-mixed dyes go in a new per-tint table, `CORE_ABS_TINT`;
- `LOAD_BUILT=1` keeps today's numbers for the record.

| Tint | Pendant (× base pour) | Core pour (absolute) | Core dye re-mix (R, G, B; black) | Source |
|---|---|---|---|---|
| Ember | 0.7 | 0.5 (unchanged) | none | owner, 19:09 |
| Dust | 2.1 | 2.6 | 1.0, 0.35, 2.5; black 8 or 16 /m | dye round 6 (pick 8 or 16) |
| Acid | 3.0 | 2.0 | none | owner, 19:09 |
| Poison | 1.0 | 0.45 | none | Poison helper |
| Ice | 3.0 | 1.72 | 3.2, 0.85, 1.19 | dye round 4 |
| Haze | 1.0 | 0.6 | 0.89, 2.2, 1.09 | dye round 5 |
| Fog | 1.0 (unchanged) | 0.5 (unchanged) | none | not in the pour question |
| Smoke | 1.2 (unchanged) | 0.5 | none | owner, 19:09 |

The commit is code only. It is checked by re-rendering one tint's OFF pair at half size and comparing it with its check-set frame (dE00 under 0.5).

## 2. The pictures

Full size is 1600 × 2000 on the house ground. Settings are frozen from this lane's scripts. Times are for one 4-core machine rendering alone; sharing a CPU roughly doubles them.

| Group | Per tint | Frames | Settings | Time each | Machine-hours |
|---|---|---|---|---|---|
| A. Pendant OFF | 1 | 8 | `row-off/hemisphere-off.sh` (128 spp) | 25-30 min | about 4 |
| B. Core OFF | 1 | 8 | `row-off/core-off.sh` (128 spp) | 25-30 min | about 4 |
| C. Pendant LIT | 1 | 8 | `ember-r6-hemi.sh`: softboxes unseen, colour-only denoise, studio 3.5 at -5.15 EV, 512 spp | 60-70 min | about 9 |
| D. Core LIT | 1 | 8 | `ember-r6-core-f.sh`: LIT-c plus the LIT-f spot (18°, blend 0.9, 8.5 W, #FFF4E8, 3 mm, flag), path guiding, studio 0.714 at -2.85 EV, 512 spp | 85 min | about 11 |
| E. Share cards, 1200 × 630, per lamp and tint (the open item from earlier) | 2 | 16 | to be framed from A-D's set (one card per lamp and tint) | about 15 min | about 4 |
| F. Photometry, lumens out per lamp per tint, with the new pours | 2 | 16 | `lamp_site.py` photometry mode (the round-13 scale, 0.0065 W/lm) | about 5 min | about 1.5 |

The total is about 33 machine-hours. With one helper per tint, eight helpers, it takes about 4.5 h of wall time:

- each helper runs A, B, C, D and F for its tint in that order;
- the share cards follow from the finished frames.

## 3. Order

0. Commit the pour table and run the one-tint check.
1. Groups A and B, all tints. These make the off sheet the owner approves, so they come first.
2. Groups C and D per tint. Each pair is checked before the next tint's LIT frames:
   - the glow by per-tint masks;
   - walls and floor against the Ember pair;
   - clipping.
3. Group F, then E.
4. Critic round on the finished set (fresh context, image only), then the owner.
5. Bar pictures with lit pendants. These are another lane's scenes; they take the new pendant pours from step 0 and the pendant LIT recipe from group C.

## 4. Open decisions before step 0

- **LIT exposure across tints.**
  - **Option (a), one studio and one exposure per lamp for every tint**, as in the check set. This is honest about relative brightness; light tints may clip and dark tints read dim.
  - **Option (b), balance each pair to its own glow.** Every pair looks matched, but the exposure differs across tints.
  - **Recommendation: (a).** Check clipping per tint, with (b) only where a tint clips.
- **Glow masks per tint.** The Ember pair masks fail for Ice and Haze. A per-tint hue window is needed before C and D are balanced or judged.
- **Fog Core.** It sits in the tone curve's shoulder (modelling 0.95-0.99). The critics' remedy is a flag or a lower key on the product, a set change for Fog's OFF frames only. It needs a test before group B.
- **Dust: black 8 or 16.** Both measure dE00 2.0. 8 keeps more chroma (C* 68.1 against 64.9); 16 matches the lightness (53.6 against 54.3).
- **The LIT-f glint on the ball.** It waits on the critics. If it must go, a barn door on the spot goes into D's settings.
