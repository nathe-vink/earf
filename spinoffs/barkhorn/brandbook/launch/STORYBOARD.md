# The teaser: "Something in the air." (25 s)

For the debut invitation's email, the site and the feed. Built by `teaser.py` from the existing renders, in the
brand's type: `out/earf-teaser-16x9.mp4` (1920 × 1080, about 5 MB) and `out/earf-teaser-4x5.mp4` (1080 × 1350, about
4 MB), 25 fps, H.264. The board: `out/earf-teaser-storyboard.jpg`; one still per beat in `out/teaser-*-beat*.jpg`.

**Sound: silent. The music is a placeholder.** A licensed track to be chosen and cleared (a sync licence for the
recording and the composition) before it runs anywhere with sound. Brief for the track: a single slow phrase, warm,
analogue, no vocal, that lands its last note on the end card at 21.5 s. Until then, it runs silent with on-screen type.

| Beat | Time | Picture | Move | Type |
|---|---|---|---|---|
| 1 | 0.0–3.2 s | Tropos in Ember alone in the dark (`red-studio.jpg`) | fade up from black, push in 10% | EARF · San Francisco; "Cast in colour, all the way through." |
| 2 | 3.0–7.7 s | The horn turning through 360° (`turn-red.jpg`, 24 path-traced frames) | stepped, like a turntable photo series | Tropos · the horn, formed from its own acrylic; "The oldest amplifier is a shape." |
| 3 | 7.5–11.7 s | The eight lit from below on a concrete wall (`facade.jpg`) | a slow pan left to right | "Put a light under it." |
| 4 | 11.5–15.7 s | The eight tints in their elements (`*-habitat.jpg`) | a cut every half second, a slight push on each | 01 Ember … 08 Smoke |
| 5 | 15.5–18.7 s | Core and Hemisphere (`lamps-orbs.jpg`), then Mantle at dusk (`tt-violet-dusk.jpg`) | a pull, then a push | "Light, and a record player, in the same eight." |
| 6 | 18.5–21.7 s | The eight (`hero.jpg`; `hero-portrait.jpg` on 4:5) | a slow pull out | "Something in the air." |
| 7 | 21.5–25.0 s | The globe turning on night (`globe-turn-night.mp4`) | — | EARF; Tuesday 19 January 2027; [VENUE], San Francisco · earf.world; "Every picture is a render · on the night, the real thing"; fade to black |

Each beat crossfades into the next over 0.2 to 0.4 s. Every picture is a render, and the end card says so.

**Why the horn steps.** The site's turn is 24 frames at 15°; motion interpolation smeared the acrylic, and a full
path-traced turn of the speaker (48 to 72 new frames) would take the renderer about 16 minutes a frame at the finals'
quality. The stepped turn reads as intended. A smooth turn is the first thing to render once a machine with a GPU is
free, or to shoot on a turntable once the first pair exists.

**To change:** the venue and date are in `b_end` in `teaser.py`; run `python3 teaser.py --aspect 16x9` (about 40 s)
and `--aspect 4x5`.
