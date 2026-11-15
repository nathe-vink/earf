# Smoke or Fog: a choice sheet (2026-11-15)

The owner: "It's odd that the smoke lights look whiter than fog," and then "No on warm smoke light. It looks light
yellow." Warm is ruled out, so the ways left are a grayer Smoke shell or a whiter Fog. This sheet is for him to pick
by eye. No finals, spec, components.json or BOM were changed.

`smoke-choice-sheet.png` has four rows: Hemisphere lit, Core lit, Hemisphere off, Core off. Its columns are:
1. Fog now (2700 K)
2. Smoke now (gray 0.3x, 4000 K)
3. Smoke gray 0.5x
4. Smoke gray 0.8x
5. Fog at 3500 K
6. Smoke gray 1.2x, Hemisphere only

The lit rows use the rows' own rig, lumens, diffuser, exposure and 4000 K camera white balance, rendered as the lamp's
region of the row frame. Columns 1 and 2 are cut from the finals' rows. The off rows use the day row's rig for Core and
the Ember-off rig for Hemisphere, scaled into its column.

| Column | Hemisphere lit-glass sRGB | Core lit-glass sRGB | Smoke dye: transmission 3 mm / 6 mm | Light out vs Smoke now: Hemisphere / Core |
|---|---|---|---|---|
| 1 Fog now | 237, 223, 208 | 212, 192, 172 | | |
| 2 Smoke 0.3x | 209, 210, 210 | 170, 171, 171 | 54 % / 29 % | 100 % (287 lm) / 100 % (35.2 lm) |
| 3 Smoke 0.5x | 195, 197, 197 | 148, 150, 151 | 36 % / 13 % | 95 % / 82 % |
| 4 Smoke 0.8x | 169, 172, 174 | 112, 117, 118 | 19 % / 4 % | 90 % / 62 % |
| 5 Fog 3500 K | 230, 226, 221 | 202, 197, 190 | | about the same as Fog now |
| 6 Smoke 1.2x | 125, 131, 134 | (not rendered) | 8 % / 0.7 % | 86 % (246.5 lm) / - |

How to read the dye columns:
- Hemisphere's tinted layer is 3 mm at the loading.
- Core's wall is 6 mm at half the loading, the same optical depth as 3 mm at the loading. So each lamp's own glass
  passes the 3 mm figure.
- Light out was measured with the enclosing sensor (launch/isphere.py) with the same LED.
- Hemisphere loses little because most of its light leaves through the open mouth, which the dye doesn't touch (below
  the rim: 202, 197, 193 and 190 lm at 0.3x, 0.5x, 0.8x and 1.2x).

Strengths:
- On Core, 0.8x reads clearly gray beside Fog when lit; 0.5x still reads as a dimmer white.
- On Hemisphere, even 0.8x still reads as a white lamp when lit. From the row's eye level you see the white diffuser
  through the mouth, and only the top band darkens. Hemisphere needs about 1.2x to read gray lit (column 6).
- But from 0.8x up the Hemisphere shade already looks black when off, so on Hemisphere a gray lit look and a smoky
  (not black) off look don't meet at any one strength.
- Fog at 3500 K is the other route: Fog becomes the near-white lamp (230, 226, 221) and Smoke stays the dimmer
  neutral one, with no change to Smoke at all.

Audits:
- Hidden objects in frame: none in the lit Hemisphere row, the lit Core row and the unlit Hemisphere frame. The Core off
  cells use the day row's rig, whose own audit also reads none.
- Hidden lights in frame: 0.0 in every one.

Emitters:
- Lit: each lamp's LED faces (24 per Hemisphere, 1 per Core); the studio key and fill, declared and hidden from the
  camera.
- Off: the overhead strip softbox (plus the hidden kicker on the Hemisphere frame); on Core, the lifted world as the
  day row.
