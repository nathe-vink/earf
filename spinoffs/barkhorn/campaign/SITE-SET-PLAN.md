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
- The site's tints, not stock TruCast (TINTS.md), unless the owner says otherwise.
- Each frame type passes a blind critic at 7.0 or wins a duel against today's frame, up to three rounds a look (proofs at
  half size).

## What changes from today's set

Today's set has crops that break the owner's whole-speaker rule. **They are dropped, or replaced by a whole-speaker
view:**

| today (`finals31`, `studio31`) | what it shows | in Strata |
|---|---|---|
| `horn-side`, `horn-back` (1200 x 900, 8 each) | the horn alone | **dropped**; a whole-speaker side view takes their place |
| `amp` (1000 x 1250, 8) | the plate amplifier, close | **dropped**; the whole back (below) shows it |
| `macro-*` (4) | details | **dropped** (the coordinator: whole speaker only) |
| `front-on-*` (24) | cover on | **dropped** (cover off) |
| `inside` (8) | the cabinet's inside | kept only if it shows the whole speaker; otherwise dropped |

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
| proofs and critic rounds (half size, 6 frame types, up to 3 rounds) | | | | | about 2 h |
| **Tier A + B: the product pages and the shared frames** | | | | | **about 18 h of rendering** |

Each job stays under the 2-hour limit (one tint's five frames is about 1.6 h), so the set is about 12 jobs in sequence.
A preview contact sheet goes out after the first tint passes its critics, before the other seven are rendered.

**Tier C, later or with the lanes that own them** (about 19 h more):
- the eight reels (`uplit-{tint}`, 1600 wide), about 2.8 h;
- the eight habitats (`{element}` and its portrait, the landscapes in `elements/`), about 13 h;
- the eight turntable sprites (`turn-{tint}`), about 3.5 h.

Until those are redone, those pages would show the formed horn beside Strata on the others.

**The smooth horn (the option):** one front-off-tall and one hero-light, in Ember, about 50 minutes. That is for the
page that names the option.

**Order:**
1. Ember (the hero tint);
2. the shared frames;
3. the other seven, in the site's order: Dust, Acid, Poison, Ice, Haze, Fog, Smoke;
4. Tier C when asked.

All frames go to `renders/2026-11-01/barkhorn/site-strata/`. Every PNG stays under 5 MB, and the site lane converts
them to JPEG as now.
