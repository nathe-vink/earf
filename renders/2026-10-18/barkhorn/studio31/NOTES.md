# studio31: the launch-page set, critic passes

Prompt: `critic/PROMPT-promo.md` (critic v2 for campaign images), a fresh blind subagent each pass, given only the
image, a card (the frame's purpose, the fixed product, the shot's settings) and `critic/measure.py`. Replies in
`critic/`.

| pass | frame | size | score | top changes | what I did |
|---|---|---|---|---|---|
| h1 | hero-dark-ember | 2560 full | 5.5 | reflection too long; edges untraced; horn crushed; glow blue-grey; seam trough | strips re-aimed where the faces mirror (by `--probe`), glow larger and warm, cove radius 3.4, key 1.9, fill 0.6, a second sheen |
| h2 | hero-dark-ember | 1280 proof | 5.0 | right face flooded white by the strip; sheen clips the front's top; horn black; reflection a smear; too big in frame | strip-right 0.08 m at 113, left 30; sheen 2.2; a panel through the horn from behind; strip-top forward; the floor's reflectance 0.06 (new `sweep.specular`); 60 mm, more room above |
