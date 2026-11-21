# Mantle deck, no white (2026-11-21)

The owner answered the decision sheet: "No white under mantle it should be like the speakers but with satin edges".

This folder renders that answer. The deck is clear cast acrylic tinted with the speakers' own dyes (sp-ember #CF0913, sp-poison #12AA24). Its top and underside are polished, its outer edge is satin (bead-blast), and the 1 mm chamfer stays polished as built. There is nothing white under it, so the base, posts and phono box show through, as the speakers show their insides.

Every frame was rendered under the physical light model in the house set, with the same camera as `../tests-2026-11-21-colour/decision-sheet.png`, at 800 × 1000. The emitter and hidden-mesh audits are 0/0. The loading is a fraction of the dye the speakers' cabinets carry ("1×").

`no-white-sheet.png`: Tropos front | 1× | 0.3× | 0.1× | 0.1× with polished edges, for comparison.

Measured by region (`region.py`). "Top" is the deck's top face and "edge" is the front edge band. Hue is in degrees (CIE LCh). The Tropos fronts read Ember C* 61 at hue 36 and Poison C* 58 at hue 138.

| Tint | Loading | Top C* / hue | Edge C* / hue | Top dE to Tropos |
|---|---|---|---|---|
| Ember | 1× | 7 / 39 | 3 / 86 | 58 |
| Ember | 0.3× | 11 / 27 | 25 / 33 | 53 |
| Ember | 0.1× | 11 / 26 | 46 / 34 | 53 |
| Ember | 0.1×, polished edge | 11 / 26 | 26 / 30 | 53 |
| Poison | 1× | 5 / 124 | 3 / 106 | 61 |
| Poison | 0.3× | 11 / 141 | 12 / 138 | 51 |
| Poison | 0.1× | 10 / 142 | 42 / 142 | 52 |
| Poison | 0.1×, polished edge | 10 / 143 | 22 / 140 | 52 |

What the physics allows:

- **The top cannot match the Tropos front.** At every loading the top measures C* 5–11 against about 60. A polished top over a dark interior mostly mirrors the room, and the record and platter cover its middle. Lighter dye does not raise the top past C* 11. The top reads as tinted glass, not as a coloured surface. This is the same thing the speakers do when you look at them from above.
- **The edges carry the colour.** They get stronger as the dye gets lighter. Light runs the long way through the edge, so at 1× it is black, and at 0.1× it reaches C* 42–46, the closest to the Tropos. The hue is on target at 0.3× and 0.1×: Ember 33–34 against 36, Poison 138–142 against 138.
- **Satin edges carry the colour better than polished.** At 0.1× a satin edge reads C* 46 (Ember) and 42 (Poison); polished reads 26 and 22. The satin scatters the light running through the deck out toward the eye. A polished edge reflects most of it back inside, and shows the interior instead.
- **The speakers' green fixes Poison's olive cast.** It reads hue 141–143, where the stock 2092 read 123–126.
- **1×, the speakers' own loading, reads near black.** That loading suits a cabinet wall; the deck is 25.4 mm thick, so the light goes much further through it.

How it is made: a custom 25.4 mm cast in the speakers' dye at about 0.1–0.3× of their loading, with the outer edge bead-blasted after machining and the faces left polished. The quote is still open.
