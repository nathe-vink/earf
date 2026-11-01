# The site set in Strata: a plan and a time estimate (2026-11-01; nothing rendered yet)

**The coordinator's brief:** Tropos in all eight tints, in Strata with the stepped horn, cover off, the whole speaker
in frame, at the site's names and sizes. The lamps lane's cordless set is the pattern.
- The lamps lane's set (735e7593) is not on any branch this session can fetch.
- The names and sizes below are the site's own, from `web.py`'s image list (read only; that file is the site lane's).

**Fixed for every frame:**
- Strata's stepped horn on its bronze posts, and the caldera.
- No cloth disc.
- The whole speaker in frame, never cropped.
- The site's tint names.
- The line's tints as they stand: stock TruCast (the owner's ruling, 2026-11-01; `asset/TINTS.md`), with the site's deep
  horn on Dust, Acid and Ice. (This plan first said the site's tints; it predates that ruling.)
- Each frame type passes a blind critic at 7.0 or wins a duel against today's frame, up to three rounds a look (proofs at
  half size).

## What changes from today's set

Today's set has crops that break the owner's whole-speaker rule. **They are dropped, or replaced by a whole-speaker
view:**

| today (`finals31`, `studio31`) | what it shows | in Strata |
|---|---|---|
| `horn-side`, `horn-back` (1200 x 900, 8 each) | the horn alone | **dropped**; a whole-speaker side view takes their place |
| `amp` (1000 x 1250, 8) | the plate amplifier, close | **dropped**; the whole back (below) shows it |
| `macro-*` (4) | details | **three kept, always beside a whole-speaker picture** (the owner, 2026-11-01: "a few, always beside a whole-speaker picture"; below) |
| `front-on-*` (24) | cover on | **dropped** (cover off) |
| `inside` (8) | the cabinet's inside | kept only if it shows the whole speaker; otherwise dropped |

## The close-ups (the owner, 2026-11-01)

"A few, always beside a whole-speaker picture." Three details, each placed next to that tint's whole-speaker frame
(`front-off-wide` or `hero-light`) in one row or one spread, never alone:

| detail (site name) | what it shows | size | each |
|---|---|---|---|
| `detail-caldera-{tint}` | the caldera's stepped rings round the woofer, its polished edges and the bond lines | 1000 x 1000 | 12 min |
| `detail-horn-{tint}` | the stepped horn's layers from the front three-quarter, the terraces and the polished lip | 1000 x 1000 | 12 min |
| `detail-plinth-{tint}` | the plinth's steps and the warm light under the bottom one, at dusk | 1000 x 1000 | 12 min |

They are rendered in one tint each: the caldera in Ember, the horn in Ice (the deep horn) and the plinth in Smoke.
That is about 40 minutes, with each detail's own critic round as a pair (the detail and its whole-speaker frame).

## The set, the timing

The rate is from this week's finals: about 147,000 samples a pixel a second. For example, the Strata hero at
1440 x 1800 and 128 samples took 38 minutes. Each frame is rendered at the site's own size.

| frame (site name) | size | samples | each | x | total |
|---|---|---|---|---|---|
| `front-off-tall-{tint}` (cards and phones) | 1000 x 1250 | 96 | 14 min | 8 | 1.8 h |
| `front-off-wide-{tint}` (the gallery's 3:2) | 1800 x 1200 | 96 | 24 min | 8 | 3.1 h |
| `hero-light-{tint}` (the studio, light ground) | 2400 x 1350 | 96 | 35 min | 8 | 4.7 h |
| `side-{tint}` (new: the whole speaker from the side, the stepped horn's profile) | 1000 x 1250 | 96 | 14 min | 8 | 1.8 h |
| `back-{tint}` (the whole back: the plate amplifier, the etched EARF) | 880 x 1100 | 96 | 11 min | 8 | 1.4 h |
| **per tint, five frames** | | | **about 1.6 h** | | **12.8 h** |
| `hero` and `hero-portrait` (the eight on their arc) | 2560 x 1280; 1600 x 2000 | 128 | 48 and 47 min | 1 | 1.6 h |
| `lineup` (the look book) | 2400 x 1000 | 128 | 35 min | 1 | 0.6 h |
| `room` and `room-portrait` (Poison, golden hour) | 2880 x 1620; 1000 x 1250 | 128 | 68 and 18 min | 1 | 1.4 h |
| **shared** | | | | | **3.6 h** |
| the three close-ups (above) | 1000 x 1000 | 96 | 12 min | 3 | 0.6 h |
| proofs and critic rounds (half size, 7 frame types, up to 3 rounds) | | | | | about 2 h |
| **Tier A + B: the product pages and the shared frames** | | | | | **about 18.5 h of rendering** |

Each job stays under the 2-hour limit (one tint's five frames is about 1.6 h), so the set is about 12 jobs in sequence.
A preview contact sheet goes out after the first tint passes its critics, before the other seven are rendered.

**Tier C, later or with the lanes that own them** (about 19 h more):
- the eight reels (`uplit-{tint}`, 1600 wide), about 2.8 h;
- the eight habitats (`{element}` and its portrait, the landscapes in `elements/`), about 13 h;
- the eight turntable sprites (`turn-{tint}`), about 3.5 h.

Until those are redone, those pages would show the formed horn beside Strata on the others.

**The smooth horn (the option):** one front-off-tall and one hero-light, in Ember, about 50 minutes. That is for the
page that names the option.

**Order** (the coordinator, 2026-11-01, while the owner weighs the cabinets' depth after the deck's colours slide):
1. Ice, with the critic gate for each frame type, then its contact sheet and the horn close-up;
2. Dust, Acid, Fog (cabinets the depth question does not touch);
3. held for the owner's pick: Ember, Poison, Haze, Smoke, the shared frames with all eight (the arc and its portrait, the
   line-up), the room portrait, and the caldera (Ember) and plinth (Smoke) close-ups;
4. Tier C when asked.

Shots: `shots.py`'s `site(frame, tint)` (`campaign/shots/site-{frame}-{tint}.json`). Tints are named by tint here; today's
finals31 rigs call Ice 'blue' and Fog 'ice'.

All frames go to `renders/2026-11-01/barkhorn/site-strata/`. Every PNG stays under 5 MB, and the site lane converts
them to JPEG as now.
