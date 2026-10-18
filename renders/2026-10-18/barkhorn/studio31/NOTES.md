# studio31: the launch-page set, critic passes

Prompt: `critic/PROMPT-promo.md` (critic v2 for campaign images), a fresh blind subagent each pass, given only the
image, a card (the frame's purpose, the fixed product, the shot's settings) and `critic/measure.py`. Replies in
`critic/`.

| pass | frame | size | score | top changes | what I did |
|---|---|---|---|---|---|
| h1 | hero-dark-ember | 2560 full | 5.5 | reflection too long; edges untraced; horn crushed; glow blue-grey; seam trough | strips re-aimed where the faces mirror (by `--probe`), glow larger and warm, cove radius 3.4, key 1.9, fill 0.6, a second sheen |
| h2 | hero-dark-ember | 1280 proof | 5.0 | right face flooded white by the strip; sheen clips the front's top; horn black; reflection a smear; too big in frame | strip-right 0.08 m at 113, left 30; sheen 2.2; a panel through the horn from behind; strip-top forward; the floor's reflectance 0.06 (new `sweep.specular`); 60 mm, more room above |
| h3 | hero-dark-ember | 1280 proof | 5.5 | too small now; horn reads as chrome; right edge black; magenta cast; floor a void | three passes within half a point, so the concept moved: the glow became a backlight (0.8 m, 650 W) that the acrylic glows against, a charcoal floor (#1A1A1A, rough 0.3, specular 0.035), closer (6.6 m), tint 0; strips 24/34, sheen 1.2, horn backlight 16 |
| h4 | hero-dark-ember | 1280 proof | 5.5 | horn washed pink; front salmon; glow a spotlight ellipse; horizon cut; cyan wall | sheen 0.45 (top band only), key 1.4 at -55, glow 380 W 75 deg aimed lower, cove radius 5, floor specular 0.06, strip-top over the horn, 6000 K, fill 0.85; the horn's pink traced (lamp by lamp) to its backlight panel: 16 -> 4 |
| h5 | hero-dark-ember | 1280 proof | 5.0 | horn mouth a black void; clipped flank; right face brown; floor smear, no contact; glow an edged disc; sharpen fringe | a bigger sheen and a card in front of the horn for its mouth to mirror, strip-top 18, key 1.1, fill 1.4, strip-right 44, a crisp faint floor (rough 0.08, specular 0.04, core contact 0.7), glow 1.4 m 260 W 110 deg, floor #242424, sharpen 0.12 |
