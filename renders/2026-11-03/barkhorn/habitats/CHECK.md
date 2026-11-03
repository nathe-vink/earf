# Habitats on horn A (hornA2, r33-speaker-horn b9758dd9), blind four-test gate

The seven habitats are rendered by `spinoffs/barkhorn/biomes/habitats.py`, with:
- the welded volume glass;
- the horn closed, in satin per the spec;
- the speaker on its own M8 feet, settled onto the set;
- the black flag and side cards;
- the speaker fills off and the light off.

Each habitat is rendered at 1200 x 1500 with 48 samples. Each image is checked blind by a fresh agent that sees only
that image (`scratchpad/check/PROMPT.md`).

The gate's prompt doesn't know the horn is satin by spec. A bead-blasted horn can't be seen through, so a FAIL on
see_through that names only the horn is recorded as "horn: satin by spec". The cabinet is judged on its own.

| Habitat | see_through | grounded | no_light_down | smooth_horn | Notes |
|---|---|---|---|---|---|
| Ember | FAIL (horn only; cabinet PASS) | PASS | PASS | PASS | The cabinet reads dark and tinted, with braces, frames, ports and the lava seen through it. The horn reads as a frosted red sheet. The "sooty stain and drips" at the throat are the driver and inner posts seen as soft shadows through the satin. |
