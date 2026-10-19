# Poison A4: the poisons where the eye meets them (round 31e)

**Why:** A3 (`poison_a3.md`) beat A and went up, but its poisons did not read at the site's sizes. A4 keeps A3's rig (A's 0.6° sun, the brighter cabinet, A's fern stand) and moves the poison to where the eye travels.

What changes from A3 (`poison_a4.py`, a patch over A's shot like A3):
- **Fly agarics:** a group at true scale (caps 8–15 cm across) on the open duff at the left of the foreground, about 5.2 m from the lens, in a dapple of its own. Every age: a button still in its veil, convex caps, a young one, and an old cap with its rim torn and its warts mostly washed off. Weathered (`dull`) and matte (`matte`, new), stems sunk 4.5 cm, needles on one cap, moss and bark crumbs round the bases. No cap lines up over another from the lens.
- **Foxgloves:** three, at uneven heights, in the haze behind and right of the horn. The tallest is caught in a narrow shaft.

## Read test: the proof at 600 px, one sentence from a fresh judge with no context

| Image | Sentence (the poison part) | Pass |
|---|---|---|
| A3 (control) | "…among ferns, next to a big redwood trunk… soft light comes down through the trees." | no |
| A4 p1 | "…with red-capped mushrooms in front and purple foxgloves behind." | yes |
| A4 p3 | "…ferns and purple foxgloves around it, and small red-capped mushrooms and fallen twigs in the foreground." | yes |
| A4 p4 | "…ferns, purple foxgloves and a few small red-capped mushrooms around it…" | yes |

## Blind duel against A3 at proof scale (1200 × 800, 128 samples, both on this box)

| Proof | Order | A3 | A4 | Average gap |
|---|---|---|---|---|
| p1 | A4 first | 6.6 | 6.0 | |
| p1 | A3 first | 6.5 | 6.0 | −0.55 |
| p3 | A4 first | 7.0 | 6.5 | |
| p3 | A3 first | 6.0 | 5.5 | −0.5 |
| p4 | A4 first | 6.4 | 6.0 | |
| p4 | A3 first | 6.5 | 6.2 | −0.35 |

Proof 1 judges' faults: two caps that seemed to share one stem, a stem floating, glossy caps, and five foxgloves too evenly spaced. Proofs 2 and 3 fixed those.

**Proof 3 passes both tests, at the margin.** Its judges still saw the following:
- The caps are the most saturated thing in the frame and pull the eye. Their surface reads smooth and plastic, with stems that "glow a CG white".
- The shaft on the tallest foxglove draws a hot near-white streak that competes with the horn.
- They credited A4 with losing A3's red sliver at the cabinet's foot.

## Proof 4: the coordinator's fix pass on proof 3's notes

- Caps toward an aged orange-red (`orange`, `dull` 0.36–0.45).
- Stems a dirty ivory with soil climbing from the base (the matte stem ramp).
- The shaft on the tallest foxglove narrowed (0.18 → 0.10 m), which ends the near-white streak.

Proof 4 passes the read test and gains on the duel (−0.35 against −0.5), so **the finals' rig is proof 4 (83551c6).**

What the judges still note:
- The caps are the most saturated thing in the frame, and their spots are too even.
- A small cap is cut at the frame's left edge.
- They credited A4 again with losing A3's red sliver at the cabinet's foot.

## The finals and the full-size duel (2026-10-19)

The finals are on the new drivers, each stitched from two strips (cross-fade, finish applied once). The joins are clean at 100 %.
- Landscape: `renders/2026-10-18/barkhorn/element31/poison_a4.png` (b8a5f2c), from strips d28aa12 and c908c5d.
- Phone: `poison_a4-portrait.png` (89034b5), from strips ee61f11 and 2183eb9.

**Read test on the finished frames, at 600 px:** both pass.
- Landscape: "…ferns and purple foxgloves behind it, and small orange mushrooms in the foreground."
- Phone: "…ferns, purple foxgloves and a few small orange-capped mushrooms around it."

**Blind duel against A3 at full size, with fresh judges and the order swapped:**

| Frame | Order | A3 | A4 | Preferred |
|---|---|---|---|---|
| Landscape | A4 first | 6.5 | 6.0 | A3 |
| Landscape | A3 first | 6.5 | 6.0 | A3 |
| Phone | A4 first | 7.0 | 6.5 | A3 |
| Phone | A3 first | 6.5 | 6.0 | A3 |

**A4 trails A3 by exactly 0.5 on both frames, on the margin.** All four judges preferred A3.

What the judges said:
- **The foreground agarics:** all four called them the most saturated thing in the frame, read as smooth CG props, and pulling the eye off the product.
- **The foxgloves:** three called them too many or too bright, competing with the horn's height. One credited them as a vertical rhythm that balances the trunk.
- **A3's quieter set:** what they preferred in A3 was its plain foreground, with the agarics tucked behind the fern.
- **A point for A4:** one judge said A4's agarics hide A3's procedural-looking moss tufts.
- **A shared flaw:** the bright reflection down the clear front corner, over the woofer's right edge, caps both frames.

The trade, plainly: A3 is the better picture by half a point, and A4 is the one that says "poison" at a glance.

## The post-only retouch (2026-10-19, one pass, `retouch_a4.py`; not applied)

What it does, on the finished frames:
- **The caps:** keyed by hue inside the foreground band and feathered. The hue moves toward scarlet (−8°), chroma ×0.8, value ×0.9.
- **The hot streak on the clear front corner:** only its smooth excess over the panel beside it is halved, so the edge line stays.

**Read test at 600 px:** both pass. The landscape judge saw "small red-capped mushrooms in front"; the phone judge saw "small pink mushrooms".

**Blind duels at full size, order swapped:**

| Against | Frame | Retouch first | Other first | Average |
|---|---|---|---|---|
| A4 as it stands | Landscape | 6.5 / 6.3 | 6.7 / 6.4 | **+0.25**, 2 of 2 prefer the retouch |
| A4 as it stands | Phone | 6.8 / 7.1 | 6.6 / 6.4 | −0.05, split |
| A3 | Landscape | 6.0 / 6.5 | 6.0 / 6.5 | −0.5 (A4 as it stands: −0.5) |
| A3 | Phone | 6.0 / 6.5 | 6.5 / 7.0 | −0.5 (A4 as it stands: −0.5) |

The two halves pull apart:
- **The streak compression:** every judge comparing it with A4 preferred it (clearer glass, the surround's edge reads).
- **The cap shift:** three of those four preferred A4's warmer orange-red. The retouched caps read pink, "candy" or "more synthetic".

**The full retouch does not clearly beat A4 on both frames, so A4 stays as it is.** The streak half alone is the likely win, but it is untested.

## The streak half alone (2026-10-19, `retouch_a4.py --streak-only`; applied)

The caps are left as rendered. Only the corner streak is compressed (in the landscape the band is x 1140–1308; in the phone frame, x 760–878). The coordinator's rule for a non-owner improvement: it goes up only if it comes out ahead on both frames.

| Frame | Streak first | A4 first | Average | Preferred |
|---|---|---|---|---|
| Landscape | 6.6 / 6.3 | 6.6 / 6.4 | **+0.25** | the streak fix, 2 of 2 |
| Phone | 6.6 / 6.4 | 6.8 / 6.4 | **+0.3** | the streak fix, 2 of 2 |

All four judges named the same change: the milky wash on the clear corner is gone, the surround's edge and the green read through, and the panel reads as clear acrylic rather than haze. **Applied over `poison_a4.png` and `poison_a4-portrait.png`.**
