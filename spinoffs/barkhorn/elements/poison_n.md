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

**Proof 2** (`proofs31/element-poison_n3-p02.jpg`), the rethink:
- What changed: sulphur vents fume a few metres from the speaker; a generic "DANGER / TOXIC GAS / VOLCANIC FUMES" sign stands at the path; haze replaces the far crater wall, which had read as painted.
- **Read test:** passes, through the sign. The judge saw "…stands on dark volcanic ground by a lake, with a 'DANGER: TOXIC GAS, VOLCANIC FUMES' sign on a post to its left, yellow sulfur mounds to its right, and a grey plume of smoke under an overcast sky."
- **Realism:** 3.0 and 2.5 (mean 2.75, −0.25). The tells:
  - The ground is a flat, repeating gravel plane that ends in a ruler-straight edge against a flat cyan lake band and horizon.
  - The plume is a grainy painted smear.
  - The sulphur mounds look like clay, with no contact shadow. The speaker has no contact shadow either, and the sign is too crisp.

**N3 is stopped** after its one rethink pass: it didn't move.

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

**N2 was stopped here, prematurely.** Two passes in a row had gained less than 0.5 (−0.25, then ±0), but the lead's staging (sent 04:40) had not yet been tried, so the count resets with it.

**Proof 4** (`proofs31/element-poison_n2-p04.jpg`), the lead's staging:
- The gantry is out. The speaker sits off-centre near the jetty's far end, turned three-quarter, and the camera is low along the boards.
- Poison A's rig is moved to the speaker, a low golden sun rakes across, and the mist is capped at 4 m.
- The scum is matte pea-soup with open patches, scanned grass stands for reeds, and the sign is small and soft beside the jetty.

**Read test:** fails. The judge saw "…stands at the end of a weathered wooden dock, which runs out over a flat green marsh under a hazy grey sky, with a tall eroded rock pillar behind it and a red-and-white 'DANGER' sign on a post to the left." It names DANGER but not toxicity: the smaller sign lost the read.

**Realism:** 3.5 and 4.0 (mean 3.75, −0.5). The tells:
- The water is a flat, matte coloured floor, with no reflections, no sheen and no ripples. Its shadows have hard edges, like shadows on a painted plane.
- The stump and the posts have no waterline or wet base.
- The planks repeat one clean texture, and the haze makes a seamless studio-gradient horizon.

**Proof 5** (`proofs31/element-poison_n2-p05.jpg`), keeping proof 4's staging:
- Glossier open water between the scum patches.
- Scum rings at the stumps, the jetty's legs and the sign's post.
- The sign a size up and nearer, with TOXIC ALGAE as the biggest words, under a short DANGER band.

**Read test:** passes. The judge saw "…stands on a weathered wooden dock over a misty, algae-green lake, next to a 'DANGER TOXIC ALGAE AVOID CONTACT' sign and a tall broken tree stump."

**Realism:** 4.5 and 4.0 (mean 4.25, +0.5 over proof 4). That only wins back proof 4's loss; proofs 2 and 3 also scored 4.25. The tells:
- The water is still a flat, smeared procedural plane, with almost no reflections, no ripples and no wet contact lines.
- The speaker is too clean and crisp for the haze, with only a weak contact shadow.
- The planks repeat one texture, the posts are identical, and the stump is a lone extruded pillar. The sign is too clean and doesn't sit on its post convincingly.

**Five passes** have scored 4.5, 4.25, 4.25, 3.75 and 4.25. N2 has never left 3.75–4.5, against a gate of 6.

## Calibration (the lead, 2026-10-20)

The live Poison A4 (`element31/poison_a4.png`, 653ad29) at 1200 × 800 went through the same two realism critics with the same prompt and scored **4.5 and 4.5**. Their tells:
- The toadstools read as props.
- The speaker sits on a moss mat that looks like a decal, with no contact shadow.
- The litter tiles, the ferns repeat as cards, and the god-rays and foxgloves look too tidy.

The gate becomes: N2's realism at least 0.5 above A4's (so at least 5.0), the read test, and no fake-looking elements. N2's proof 5 (4.25) does not meet it.
