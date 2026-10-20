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

**Proof 6** (`proofs31/element-poison_n2-p06.jpg`), with Acid B's water:
- Acid B's clear water (IOR 1.33, ripples) over a murky bottom, with the bloom floating on it, open where it thins.
- Wet waterlines on the scans.
- Three trunk scans at different depths in place of one pillar.
- Acid B's rig (a bounce, two low cards, a rim card on the speaker alone), and the mist reaching the speaker.
- A bolted sign clear of the jetty's posts.

**Read test:** passes. The judge saw "…at the end of a weathered wooden pier, which runs out into a still, algae-green lake under grey fog, with a 'DANGER TOXIC ALGAE / AVOID CONTACT' sign on the left."

**Realism:** 4.5 and 4.0 (mean 4.25, against the 5.0 gate). The tells:
- The floating scum now reads as hard-edged cracked mud with dark gaps, hiding the new reflections.
- The speaker has almost no contact shadow or reflections.
- The dock is uniform CG wood with identical posts, and the fog is an even gradient.

**Proof 7** (`proofs31/element-poison_n2-p07.jpg`):
- The floating scum's edges are soft and oily, with open water along the jetty.
- Less fill on the speaker, and the sign weathered harder.

**Read test:** passes. The judge saw "…in a foggy swamp of algae-green water and old posts, next to a red-and-white sign that reads 'DANGER TOXIC ALGAE AVOID CONTACT'."

**Realism:** 4.5 and 4.5 (mean 4.5, level with the live A4, under the 5.0 gate). The tells:
- The water is still a flat matte plane, with no reflections, ripples or glints. The lily pads and grass are flat cards.
- The planks repeat one texture, the posts have identical tops, and the dock has a hard straight edge with no wet staining.
- The speaker has no contact shadow, its panels are reflected evenly, and it looks composited. The fog falls off evenly, like CG.

**N2 is stopped.** Neither of the two passes on Acid B's water reached the gate. Seven passes scored 4.5, 4.25, 4.25, 3.75, 4.25, 4.25 and 4.5. The best (p7) equals A4 on the same critics and doesn't beat it.

## The finishing pass and the finals (the lead, 2026-10-20)

The lead sent proof 7 to the owner beside A4, recommending the lake as the new Poison. The final is prepared now, so it can be swapped in the moment the owner agrees. Nothing goes on the site until then.

**Proof 8** (`proofs31/element-poison_n2-p08.jpg`), the finishing pass on proof 7:
- The bloom is more vivid (#4A7A12 / #8CC21E / #CDEB3E) and glossier (scum roughness 0.18).
- The open-water lane is narrowed to 0.9 m.
- Each dock section has its own shade of wood (`scan` `vary=`). The scan's textures are an atlas, so they can't be slid.

**Read test:** passes. The judge saw "…sits at the end of a weathered wooden pier, over hazy green water, beside a 'DANGER TOXIC ALGAE / AVOID CONTACT' sign."

**Realism:** 4.5 and 4.5 (mean 4.5, equal to proof 7, so the finals go ahead). The tells:
- The water still has no visible reflections or meniscus, and its streaks look painted.
- The planks are uniform and the posts are the same.
- The speaker has little contact shadow, and the sign's graphics are crisp.

**The finals** (512 samples, each in two strips with the finish off, stitched by `stitch.py`, the finish applied once):
- `renders/2026-10-18/barkhorn/element31/poison_n2.png`: 2400 × 1600, 3.1 MB.
- `renders/2026-10-18/barkhorn/element31/poison_n2-portrait.png`: 1600 × 2000, 2.7 MB.

The first portrait cropped the sign to a sliver at the edge. Since the sign carries the read, it was re-rendered at 34 mm, turned a little left (65aebd0).

Prepared for the owner's decision; not on the site.
