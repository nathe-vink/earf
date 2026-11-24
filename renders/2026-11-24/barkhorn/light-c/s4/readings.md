# S4 test readings (24 Nov)

Light-C fronts (now) against S4 (flags 0, 1, 2, 3, 5 as real black cards: every ray on, two-sided, casting shadows, out of frame) and S4b (flags 0, 1, 2 real; the overhead flags 3 and 5 taken out). Regions from each front's own mask; L* and C* from sRGB. Sheet: sheet-s4.png (now, S4, S4b, |now - S4b| x5).

Which flag shades what (Dust, 0.4 scale, 32 spp, one flag real at a time, grey-level change against the current front): flag 0 none; flag 1 -1.0 overall; flag 2 -0.7; flag 3 -6.1 (backdrop -8.5); flag 5 -7.4 (product -10.4, floor -6.0). Flags 3 and 5 hang between the horn light (0.9, -2.3, 2.2) and the frame; raised above every light-to-frame path (3 to z 3.5, 5 to (0, -1.3, 3.3)) they still took 5.6 off the backdrop, so S4b takes them out.

## S4 (all five real)

| tint | region | px | L* now | L* new | dL* | C* now | C* new | moved > 2 L* |
|---|---|---|---|---|---|---|---|---|
| ember | front panel (batts behind) | 64302 | 32.7 | 27.7 | -5.0 | 61.3 | 54.5 | 74 % |
| ember | right side | 74481 | 22.0 | 16.4 | -5.6 | 38.7 | 32.9 | 85 % |
| ember | left side | 9279 | 26.4 | 24.1 | -2.3 | 40.0 | 39.0 | 57 % |
| ember | top | 6568 | 37.2 | 33.6 | -3.6 | 4.3 | 3.6 | 47 % |
| ember | base (bottom, feet) | 5806 | 19.0 | 16.2 | -2.8 | 20.3 | 19.0 | 73 % |
| ember | horn | 67780 | 35.7 | 31.5 | -4.1 | 71.7 | 65.4 | 87 % |
| ember | floor round the base (paper) | 229082 | 92.8 | 89.3 | -3.4 | 4.6 | 4.2 | 50 % |
| ember | backdrop (paper) | 531012 | 91.5 | 85.6 | -5.9 | 4.9 | 4.9 | 89 % |
| dust | front panel (batts behind) | 64302 | 58.9 | 54.4 | -4.5 | 58.2 | 60.2 | 75 % |
| dust | right side | 74481 | 45.0 | 36.3 | -8.7 | 55.6 | 48.8 | 99 % |
| dust | left side | 9279 | 53.5 | 48.9 | -4.6 | 51.6 | 47.8 | 77 % |
| dust | top | 6568 | 51.9 | 45.7 | -6.2 | 37.6 | 32.0 | 97 % |
| dust | base (bottom, feet) | 5806 | 31.7 | 27.9 | -3.8 | 30.4 | 28.5 | 92 % |
| dust | horn | 67780 | 42.8 | 38.0 | -4.7 | 56.7 | 51.6 | 88 % |
| dust | floor round the base (paper) | 229082 | 92.8 | 89.8 | -3.0 | 6.3 | 5.7 | 49 % |
| dust | backdrop (paper) | 531012 | 91.5 | 85.6 | -5.9 | 4.9 | 4.9 | 89 % |
| ice | front panel (batts behind) | 64302 | 54.1 | 49.3 | -4.8 | 42.8 | 41.1 | 77 % |
| ice | right side | 74481 | 38.2 | 30.3 | -7.8 | 36.3 | 31.7 | 95 % |
| ice | left side | 9279 | 43.7 | 40.4 | -3.3 | 37.7 | 33.6 | 57 % |
| ice | top | 6568 | 41.5 | 36.9 | -4.6 | 30.5 | 25.5 | 63 % |
| ice | base (bottom, feet) | 5806 | 27.4 | 23.8 | -3.6 | 17.1 | 15.9 | 91 % |
| ice | horn | 67780 | 33.7 | 29.9 | -3.9 | 42.7 | 38.1 | 84 % |
| ice | floor round the base (paper) | 229082 | 93.8 | 90.2 | -3.6 | 2.0 | 2.0 | 52 % |
| ice | backdrop (paper) | 531012 | 91.5 | 85.6 | -5.9 | 4.7 | 4.8 | 88 % |
| fog | front panel (batts behind) | 64302 | 88.0 | 83.2 | -4.7 | 2.8 | 2.9 | 59 % |
| fog | right side | 74481 | 78.1 | 64.9 | -13.2 | 2.8 | 2.5 | 100 % |
| fog | left side | 9279 | 87.1 | 80.1 | -7.0 | 3.9 | 3.9 | 69 % |
| fog | top | 6568 | 84.0 | 74.2 | -9.9 | 4.0 | 4.0 | 98 % |
| fog | base (bottom, feet) | 5806 | 58.7 | 52.9 | -5.8 | 3.3 | 3.2 | 94 % |
| fog | horn | 67780 | 85.2 | 77.8 | -7.4 | 3.8 | 4.0 | 92 % |
| fog | floor round the base (paper) | 229082 | 94.9 | 91.8 | -3.1 | 3.6 | 3.5 | 49 % |
| fog | backdrop (paper) | 531012 | 91.6 | 85.7 | -5.9 | 4.8 | 4.9 | 89 % |

## S4b (0, 1, 2 real; 3 and 5 out)

| tint | region | px | L* now | L* new | dL* | C* now | C* new | moved > 2 L* |
|---|---|---|---|---|---|---|---|---|
| ember | front panel (batts behind) | 64302 | 32.7 | 32.4 | -0.2 | 61.3 | 60.9 | 2 % |
| ember | right side | 74481 | 22.0 | 20.5 | -1.5 | 38.7 | 36.3 | 29 % |
| ember | left side | 9279 | 26.4 | 26.2 | -0.2 | 40.0 | 39.9 | 0 % |
| ember | top | 6568 | 37.2 | 37.0 | -0.2 | 4.3 | 4.3 | 0 % |
| ember | base (bottom, feet) | 5806 | 19.0 | 19.1 | +0.1 | 20.3 | 20.1 | 0 % |
| ember | horn | 67780 | 35.7 | 36.4 | +0.7 | 71.7 | 69.4 | 12 % |
| ember | floor round the base (paper) | 229082 | 92.8 | 92.4 | -0.3 | 4.6 | 4.5 | 0 % |
| ember | backdrop (paper) | 531012 | 91.5 | 91.0 | -0.5 | 4.9 | 4.9 | 5 % |
| dust | front panel (batts behind) | 64302 | 58.9 | 58.5 | -0.4 | 58.2 | 57.9 | 3 % |
| dust | right side | 74481 | 45.0 | 42.3 | -2.7 | 55.6 | 52.9 | 55 % |
| dust | left side | 9279 | 53.5 | 52.5 | -1.0 | 51.6 | 49.9 | 13 % |
| dust | top | 6568 | 51.9 | 50.6 | -1.3 | 37.6 | 35.5 | 16 % |
| dust | base (bottom, feet) | 5806 | 31.7 | 31.7 | +0.0 | 30.4 | 30.0 | 0 % |
| dust | horn | 67780 | 42.8 | 43.3 | +0.5 | 56.7 | 54.7 | 11 % |
| dust | floor round the base (paper) | 229082 | 92.8 | 92.5 | -0.3 | 6.3 | 6.2 | 0 % |
| dust | backdrop (paper) | 531012 | 91.5 | 90.9 | -0.5 | 4.9 | 4.9 | 5 % |
| ice | front panel (batts behind) | 64302 | 54.1 | 53.8 | -0.3 | 42.8 | 42.5 | 3 % |
| ice | right side | 74481 | 38.2 | 35.8 | -2.4 | 36.3 | 34.5 | 48 % |
| ice | left side | 9279 | 43.7 | 43.3 | -0.4 | 37.7 | 36.2 | 3 % |
| ice | top | 6568 | 41.5 | 41.0 | -0.5 | 30.5 | 28.2 | 1 % |
| ice | base (bottom, feet) | 5806 | 27.4 | 27.5 | +0.1 | 17.1 | 16.8 | 0 % |
| ice | horn | 67780 | 33.7 | 34.5 | +0.7 | 42.7 | 41.7 | 11 % |
| ice | floor round the base (paper) | 229082 | 93.8 | 93.4 | -0.3 | 2.0 | 2.0 | 0 % |
| ice | backdrop (paper) | 531012 | 91.5 | 91.0 | -0.5 | 4.7 | 4.8 | 5 % |
| fog | front panel (batts behind) | 64302 | 88.0 | 87.4 | -0.6 | 2.8 | 2.8 | 6 % |
| fog | right side | 74481 | 78.1 | 73.6 | -4.5 | 2.8 | 2.6 | 71 % |
| fog | left side | 9279 | 87.1 | 84.9 | -2.2 | 3.9 | 3.9 | 23 % |
| fog | top | 6568 | 84.0 | 81.9 | -2.2 | 4.0 | 3.9 | 19 % |
| fog | base (bottom, feet) | 5806 | 58.7 | 58.3 | -0.4 | 3.3 | 3.3 | 9 % |
| fog | horn | 67780 | 85.2 | 85.1 | -0.1 | 3.8 | 3.8 | 8 % |
| fog | floor round the base (paper) | 229082 | 94.9 | 94.7 | -0.3 | 3.6 | 3.5 | 0 % |
| fog | backdrop (paper) | 531012 | 91.6 | 91.0 | -0.5 | 4.8 | 4.9 | 5 % |
