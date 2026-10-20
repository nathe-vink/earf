# Poison outdoors: N2 and N3 (round 31g)

**Why:** the owner, 2026-10-20, via the coordinator: "Took a look at poison. It needs to be outside and incorporate nature. It loses the EARF vibe if not."

The rules:
- No purple, and no modelled flowers or animals.
- Scanned assets for anything living, and real HDRI skies.

**The gates:**
- Read test: one sentence at 600 px from a fresh judge told nothing, who must name poison or toxicity unprompted.
- Realism of 6 or more from two critics.

**N1 (a fly agaric ring) is dropped.** There is no CC0 fly agaric scan:
- Poly Haven and ambientCG have no fungi.
- Sketchfab's scans are CC-BY or CC-BY-NC and need a token to download.

The coordinator chose to drop N1 (option a).

## N3, the volcanic crater (`poison_n3.py`)

**Proof 1** (`proofs31/element-poison_n3-p01.jpg`, 1200 × 800, 96 samples):
- **Read test:** fails. The judge saw "a see-through green speaker stands on dark gravel between two big brown rocks… behind it is a pale turquoise lake with misty, jagged mountains fading into a grey sky." No poison, no volcano.
- **Realism:** 3.0 and 3.0. Both critics named the same tells:
  - the backdrop (the crater wall and the far lake) reads as a flat painted plane, with a hard seam where the lake meets the ground;
  - the speaker and the rocks have no contact shadows;
  - the gravel is one uniform repeating texture.

The sulphur vents and fumes barely register at this distance.

## N2, the toxic algae lake (`poison_n2.py`)

**Proof 1** (`proofs31/element-poison_n2-p01.jpg`, 1200 × 800, 96 samples):
- **Read test:** passes. The judge saw "…a weathered wooden dock in a foggy lake covered in bright green algae, with broken tree stumps rising from the water, an empty wooden gallows-like frame with a hanging rope behind it, and a red-and-white 'DANGER: TOXIC ALGAE, AVOID CONTACT' sign in the lower left."
- **Realism:** 4.5 and 4.5. Both critics named the same tells:
  - The algae is a flat, smeared neon layer: no clumping, no debris, no fade into the fog.
  - The speaker has no contact shadow on the boards and is too clean for the fog.
  - The dock's reflection is a dark slab, and the sign's type is too crisp.

**Proof 2** (`proofs31/element-poison_n2-p02.jpg`): the bloom clumped (a noise blend), floating branches, the sign aged, a waterline.
- **Read test:** passes again.
- **Realism:** 4.5 and 4.0 (mean 4.25, −0.25). The critics' tells: the speaker still pasted in, the algae still flat, the fog a flat gradient, and the pier's gantry now reads "gallows-like".

**Proof 3** (`proofs31/element-poison_n2-p03.jpg`): a low backlit sun, a key light kept out of the mist, mist over the speaker, wetter scum, more open water (cover 0.74).
- **Read test:** passes. The judge saw "a translucent green box speaker… stands on a broken wooden jetty in a foggy lake with glowing green water, between dead tree stumps and an old wooden gallows-like frame, while a 'DANGER – TOXIC ALGAE – AVOID CONTACT' sign stands in the water in the lower left."
- **Realism:** 4.5 and 4.0 (mean 4.25, ±0). The tells:
  - The speaker is lit flat, without haze, a wet sheen or a contact shadow, and its edges are crisp in the fog.
  - The water is an even, saturated neon green that reads as an emissive shader, with smeared reflections and no ripples at the posts.
  - The props look like a staged kit: the gallows frame, the cloned stumps, a pristine sign, twigs laid on the surface.

**N2 is stopped.** Two passes in a row gained less than 0.5 (−0.25, then ±0). It reads as poison every time, but its realism has held at about 4.25, well short of 6.
