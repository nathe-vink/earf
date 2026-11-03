# Horn check, Ember proxy (2026-11-03)

Ember's portrait shot through `habitat.py` at 0.35 scale and 16 samples, with the shot's speaker fills dropped
(`through`, `horn`, `face`). Three versions:

- (a) the old asset (r33-speaker-horn 4ec3bc96, horn collapsed, shells open), satin;
- (b) the rebuilt asset (b9758dd9, horn uncollapsed, shells closed), satin, as the spec has it;
- (c) the same closed horn at roughness 0.05. This is a departure from the spec ("Horn: A, smooth, satin outside") and is
  here for comparison only.

Luminance is measured on the horn (a 120 x 80 px box on the raw render, 0-255):

| | mean | p10 | p90 | rim band | flare face |
|---|---|---|---|---|---|
| a | 63.2 | 13.7 | 101.3 | 76.2 | 56.3 |
| b | 63.4 | 13.7 | 101.7 | 77.0 | 57.1 |
| c | 25.0 | 10.7 | 33.7 | 34.3 | 20.8 |

What this shows:

- Closing the shells changes almost nothing here: the means of (a) and (b) differ by 0.2.
- With the satin finish, the horn glows evenly from the light behind it and reads lighter than the cabinet. Thick
  and thin sections look the same, because the bead-blasted face scatters the light before the thickness can show.
- The glossy horn is 2.5 times darker and reads as glass: the throat is deep, and the posts behind it show through.
  This is the "thicker parts darker, glassy" look the owner remembered, but you only get it with a polished face.
