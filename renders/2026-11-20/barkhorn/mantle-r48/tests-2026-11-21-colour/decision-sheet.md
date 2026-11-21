# Mantle deck colour: decision sheet (2026-11-21)

`decision-sheet.png`: two rows (Ember, Poison), five panels each, all rendered under the physical light model in the house set (800 × 1000 each; the Tropos fronts were made in the same set).

Measured by region with `region.py`. "Top" is the deck's top face and "edge" is the front edge band. Hue is in degrees (CIE LCh). The target is the Tropos front: Ember C* 61 at hue 36, Poison C* 58 at hue 138.

| Row | Panel | Top C* | Edge C* | Top hue (Tropos) | Top dE to Tropos |
|---|---|---|---|---|---|
| Ember | Stock as specified | 2 | 5 | 90 (36) | 66 |
| Ember | Custom pour + white underside | 35 | 29 | 26 (36) | 27 |
| Ember | 3 mm stock sheet + white | 34 | 8 | 25 (36) | 28 |
| Ember | Custom pour, no white | 5 | 28 | n/a, near black (36) | 61 |
| Poison | Stock as specified | 1 | 3 | n/a, near black (138) | 68 |
| Poison | Custom pour + white underside | 31 | 25 | 123 (138) | 31 |
| Poison | 3 mm stock sheet + white | 31 | 7 | 126 (138) | 29 |
| Poison | Custom pour, no white | 6 | 23 | n/a, near black (138) | 61 |
| Poison | Bluer custom green pour + white (test, `poison-bluer-green-pour-white.png`) | 38 | 30 | 146 (138) | 23 |

How each is made:

- **Stock as specified:** a 25.4 mm cast sheet in the stock tint (TruCast 2423 Ember, 2092 Poison). It reads as a black slab because 25 mm of stock dye absorbs almost all the light.
- **Custom pour:** a 25.4 mm cast block with much less dye: about 12% of stock for Ember and about 6% for Poison. This needs a custom quote, which is still open. The edges glow because light runs the long way through them.
- **3 mm stock sheet + white:** a 3 mm stock-tint sheet bonded over clear cast, the same way the platter is laminated. The top colours well, but the edge shows a thin tinted line over a clear band.
- **White underside:** an opaque white sheet or paint under the deck. It sends light back up through the tint, and it also hides the base, posts and box that otherwise show through. Every bright option needs it.
- **No white:** without the white, even the light pour reads nearly black from above. Only its edge shows colour.

Poison's yellow cast: the 2092 dye lets red through more than blue, so a thin path reads olive (hue 123–126 against 138). A bluer custom green that absorbs more red closes the gap. The test used the speakers' own green (#12AA24) at 0.15 of its loading, under a white underside. It reads hue 146, slightly past the target, at C* 38. The green is not yellow because it is thin; the yellow comes from the dye.
