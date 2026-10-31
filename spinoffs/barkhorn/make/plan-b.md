# Tropos's horn: Plan B, if pressure forming fails (2026-10-31)

The horn is pressure-formed from 10 mm cast acrylic over a male plug (round 36). If the forming trial
(`make/forming-trial.md`) shows a risk that cannot be beaten, these are the other ways to make it. The worst
cases are walls under 4 mm in the mouth's corners (F1 in `make/horn-risks.md`), webbing (F2), or a deep lot that will
not heat evenly (F4). Every route keeps the approved air path, the pod, the cap, the posts and the driver as drawn.
Only the flare and the neck change.

Costs are budget estimates a horn at the prototype pair (one-off shop rates), with the one-off tooling alongside. The
formed horn's own figures (round 36) are the baseline.

| route | how | tooling | a horn (prototype) | risk | look | acoustics |
|---|---|---|---|---|---|---|
| **The baseline: formed** | 10 mm sheet pressure-formed over a male plug, trimmed; a turned throat piece | ~$7,100 (board plug and base) | ~$1,500 | F1, F2, F4: corners, webbing, the dark lot in the oven | one clear shell, glossy outside, no seam; deep tint pale where thin, deep at the rim | air path exact (the tool's face); walls 5 to 8.5 mm, stiffer than the resin's |
| **A. Laminated layers** (recommended) | 14 layers of the horn lot's 20 mm sheet, each CNC-cut to its outline, bonded in a jig with polymerising cement, annealed; the air path machined through on 5 axes and polished; the outside left stepped | ~$1,500 (a bonding jig) | ~$1,900: sheet ~$530 (about 1.4 m² of 20 mm), cutting $240, bonding $160, 5-axis air path $750, polish $200 | **Bond lines**: 14 bonded rings must be free of bubbles (C2, 14 times over). Mitigation: the same cement and process as the cabinet's joints, vacuum-mixed, each layer pressed flat. Machining a 278 mm deep bore: the mouth is wide, so ordinary long tools reach | **terraced**: a contour-line horn, each 20 mm layer a step, the bond lines fine dark lines through the tint. Deeper and heavier-looking (a thick wall reads darker); unmistakably made, a sculpture | air path exact (machined); walls 10 to 30 mm, massive and inert, the best of all routes; 5.6 kg a horn against 4.1 |
| **B. Two formed halves** | the horn split on its horizontal centre plane; each half formed over a half plug (a draw of about 180 mm, not 240), trimmed, the halves bonded edge to edge | ~$8,500 (two half plugs and bases) | ~$1,700 (two formings, a long bonded seam, seam polishing) | **The seam**: two 600 mm bonded seams on the air face, each a possible step and a line of bubbles; the halves must meet within 0.1 | **a seam** along each side wall, through the tint | air path exact if the seam is flush; a step at the seam scatters only above about 10 kHz if under 0.3 mm |
| **C. Cast resin in the deep tint** (round 35's horn) | polyurethane or epoxy cast in a two-part silicone mould from a CNC-cut plug | ~$900 (mould) | ~$820 (the kit's figure) | **Material**: a different material from the cabinet, so its colour must be matched across two chemistries and it ages differently in UV (the reason for round 36). Low process risk | **exactly the site's look**: a deep horn with a solid dark neck | as simulated and approved; a solid neck |
| **D. 8 mm sheet, formed** | as the baseline, from 8 mm sheet | as the baseline | ~$1,400 | **Too thin**: the CAD's estimate puts the mouth's corners at 3.9 mm, under the 4 mm floor. Only with plug assist and a proven trial | as the baseline, a little paler | as the baseline, walls 20 % less stiff |
| **E. Machined from a solid block** | a cast block about 650 x 380 x 300 hollowed on 5 axes, inside and out | none (fixtures) | ~$4,500 or more: a 74 L block of the horn lot (most of it swarf), 10+ hours of machining | **The block**: casting 300 mm of tinted acrylic without bubbles or stress is specialist work (an aquarium caster). Long machining | one flawless piece, the deepest colour at the neck | exact; thick walls as chosen |

## The recommendation: A, laminated, with C as the fast fallback

- **Laminated (A)** removes the forming risks rather than managing them. Its two processes, CNC cutting and
  polymerising cement, are the cabinet's own, so the same shop, the same cement and the same inspection serve both.
  The air path is machined, so it is exact. The walls are the most inert of any route. It costs about $400 more a horn
  than forming, but its tooling is a jig, not a plug.
- Its look is new: a terraced horn, each 20 mm layer a contour line. That is a design change the owner should see
  first (the render below). It suits a brand built on the globe's rings and on Mantle's layered plinth, and the
  stepped outside can be machined smooth if the owner prefers. A smooth outside costs about 2 more hours of 5-axis
  work and loses the contour lines.
- **Cast resin (C)** is the fastest way to a working horn, about two weeks from a CNC-cut plug. It looks exactly like
  the site's pictures. Its cost is the one-material story: it is not the cabinet's acrylic.
- Not recommended: B (a long seam on the air face, and more tooling than the baseline), D (under the 4 mm floor), E
  (cost, and a rare casting).

## The model and the render

Route A is in the CAD as `horn-plan-b` in `horn_options.py` (built apart from the Cloud, with its drawings and parts
list in `out-horn-options/`; the geometry is `product.formed_horn`'s `laminated`). It has 14 layers of 20 mm, each its
outline 10 mm outside the air path at its front, and the boss as the last layer. It takes the formed flare's and the
throat piece's place, on the same pod, cap, pads and posts. It is 4.7 L of acrylic, about 5.6 kg. The kit prices it at
about $2,150 a horn, its blank the 1.4 m² of 20 mm sheet its layers are cut from, against the $1,900 built up above. The render beside the formed horn is `renders/2026-10-31/barkhorn/horn-plan-b/compare-formed-vs-laminated.png`.
