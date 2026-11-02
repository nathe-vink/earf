# The horn reopened: options study (2026-11-02)

The owner, 15:48: "I don't like that the stepped horns are now making an X shape in the light reflection. The horns also look darker than the speaker. Not sure if I like the stepping anymore." (README 8707ec61.) This is an options study only: `product.py`'s default horn and the site are unchanged.

Every frame uses the site's front-off-tall shot (`site-front-off-tall-{ice,ember}.json`, colors F) at 0.6 scale and 96 samples, with only the horn swapped. Each `*-mouth.png` is a 2x crop of the horn from the same frame. `sheet-ice.png` and `sheet-ember.png` show the five frames over their five mouths, in the order a today, a, b, c, d.

## Where the X comes from

All the laminated horns (a, b and d) share Strata's air path: 536 x 346 at the mouth, its exponent rising from 2 at the throat to 7 at the mouth, machined smooth on 5 axes, the profile the simulation approved. **The steps are on the outside only.** Each layer of a is the air path's outline pushed out by 10 (12 on the mouth's layer). Through the tinted wall, the 22 layers' corners line up along the two diagonals, so the stepped outside reads as an X. The formed horn (c) has the same air path and a smooth outside, and shows no X.

## The options

- **a:** Strata's stepped horn as it is (`horn-strata`), at today's depth and at the cabinet's luminance.
- **b:** softened corners (`horn-soft`, `variants/horn_study.py`): the same 22 layers, each a rounded rectangle whose corner radius grows from 33 at the throat to 85 at the mouth, the most each layer takes with 6 left at its corner.
- **c:** the smooth formed horn, the Cloud's waveguide and throat (the option kept since 2026-11-01, as `make_blend --horn smooth` places it) on Strata's bronze posts.
- **d:** "Strata laid flat" (`horn-flat`), my own idea: the same horn laminated the other way, 29 horizontal slabs of 1/2 in stacked bottom to top, each cut to the horn's plan at its inner face, so the outside steps in level terraces on the top and the bottom.

## The numbers

These are measured with `hornhue.py`: the horn's mouth (inset 12 % at the sides, 15 % at the top, 20 % at the bottom) against the cabinet's front panel above the woofer. Each row gives the median hue of the saturated mid-tones, then the median luminance (linear Y) over the whole box. The horn tint `f` is a multiple of the stock 1/2 in sheet's absorbance (1 is the stock sheet), found from 22 proxies at 0.3 scale.

| frame | horn deep (f) | horn Y | cabinet Y | horn / cabinet | hue diff |
|---|---|---|---|---|---|
| ice-a-today | #369BCA (today's custom deep) | 0.043 | 0.560 | 0.08 | +3 |
| ice-a | #F6FCFE (0.10) | 0.567 | 0.560 | 1.01 | -1 |
| ice-b | #F9FDFF (0.07) | 0.550 | 0.560 | 0.98 | +5 |
| ice-c | #75BCF4 (2.2) | 0.576 | 0.561 | 1.03 | 0 |
| ice-d | #E3F4FD (0.33) | 0.485 | 0.560 | 0.87 | -2 |
| ember-a-today | #E02B3A (1: stock 2423 1/2 in) | 0.073 | 0.371 | 0.20 | -2 |
| ember-a | #FDE1E6 (0.075) | 0.354 | 0.371 | 0.95 | -7 |
| ember-b | #FDE7EB (0.06) | 0.357 | 0.371 | 0.96 | -7 |
| ember-c | #ED5F6F (0.58) | 0.376 | 0.372 | 1.01 | -5 |
| ember-d | #FCD8DE (0.10) | 0.364 | 0.371 | 0.98 | -7 |

**What matching the luminance costs:** a horn as light as its cabinet keeps the hue, but not the colour's strength. The laminated horns at equal luminance read pale: Ice near clear (12 % saturated pixels against 86 % today), Ember pink, not red. The cabinet reads strong at the same luminance because its white lining lights it from behind. The formed horn (c) holds its colour best, though Ember's still reads pinkish. A middle depth (horn at about half the cabinet's luminance) would keep more colour; it was not part of this pass.

## The depth in sheet terms

TT is light through the sheet, from the stock code's TT and `f`: 2069 Ice at 57.6 %, 2423 Ember at 14.1 %, both through 1/2 in.

- **a, b, d (laminated from 1/2 in):** they need a **pale custom batch in every colour**: Ice about 80 to 89 % TT through 1/2 in (stock 2069 is 57.6 %), Ember about 76 to 82 % (stock 2423 is 14.1 %). A laminated horn is thick (the light crosses many layers), so stock 1/2 in reads 4 to 13 times darker than its cabinet: Ember's stock horn today is 0.20 of its cabinet. None lands on a stock sheet. The three deep custom batches would go, but pale ones would take their place, for all eight colours, not three.
- **c (formed from 10 mm sheet):**
  - Ice: at the stock code (2069 at 3/8 in, about 64 % TT through 10 mm) the horn reads **33 % lighter** than its cabinet (proxy at f 1: 0.742 against 0.559). That is "no darker", so stock works. An exact match needs a deeper custom batch (about 41 % TT through 10 mm).
  - Ember: the stock code (2423, about 21 % TT through 10 mm) reads about 40 % darker than the cabinet (from the proxies). The match needs a lighter custom batch (about 39 % TT through 10 mm).
  - So the formed horn needs no custom batch where the owner accepts a horn a little lighter or darker than its cabinet. The three deep custom batches go.

## The X, one line each

- **a:** a clear X at today's depth (dark diagonals); stronger at the cabinet's luminance (white diagonals on a near-clear horn).
- **b:** still an X; the rounded corners soften it only a little, because each corner's arc still sits on the diagonal.
- **c:** no X; one smooth, even colour.
- **d:** no stacked corners, but the terraced top and bottom read darker than the smooth sides, so a bow-tie remains (softer than a's X); the mouth's rounded corners step like a staircase.

## Acoustics, cost and build, weight

All four share the same air path, so the horn's acoustics are the same. Step diffraction does not arise: no option has a step on the air surface. The laminated horns' steps are outside the wall, and their bond lines are flush and polished in the air path.

- **a:** 22 layers, CNC-cut and bonded, the air path machined through on 5 axes and polished. About $1,483 a horn plus $1,650 setup (the Plan B parts list, 2026-10-31). 4.18 kg (parts list).
- **b:** the same process, only the outlines differ, so about the same cost. 4.89 kg (from the solid at 1.19 g/cm3, boss included; a by the same method would read somewhat more than 4.18).
- **c:** one formed 10 mm sheet over a male tool, trimmed and cemented into a turned throat piece, plus the cap. About $1,119 a horn in parts (waveguide $592, throat $370, cap $157), plus the forming tool and plug (about $1,100) and the forming risks in the risk register. 3.17 kg. Acoustically, the formed shell is thinner than a solid laminated wall and may ring more; to check on the first sample.
- **d:** 29 slabs, each a different outline, bonded in a jig, the air path machined as in a. Cutting and bonding run about 20 % above a (an estimate), with bond lines across the air path and the mouth's face. 5.06 kg.
