# The deep horns color-matched to their cabinets (2026-11-02)

Proxies of `site-front-off-tall-{dust,acid,ice}` at 0.3 scale and 32 samples; only the flavor's horn-lot `deep` changes. They are measured with `hornhue.py`: the median hue of saturated mid-tones (S > 0.3, 0.25 < V < 0.95) in the horn's mouth (inset 12 % at the sides, 15 % at the top, 20 % at the bottom), against the cabinet's front panel above the woofer, plus the mean luminance (linear Y). The method agrees with the coordinator's on the 384 finals: Dust's horn 4 against its cabinet's 23; Ice's 230 against 209.

Each candidate turns the current deep's hue (saturation kept, luminance kept), then scales its absorbance (`f`; under 1 is lighter). 25 proxies in all:

| candidate | deep | horn hue against cabinet (diff) | horn Y |
|---|---|---|---|
| Dust, before | #F25508 | 4 against 25 (-22) | 0.152 |
| Dust +22, f 1 | #B68006 | 26 against 25 (0) | 0.048 (reads brown) |
| Dust +22, f 0.5 | #D8B53A | 34 against 25 (+9) | 0.146 |
| Dust +8, f 0.5 | #EDA53D | 18 against 25 (-7) | 0.174 |
| **Dust +15, f 0.55** | **#DFA934** | **25 against 25 (0)** | **0.142 (-7 %)** |
| Acid, before | #FFB101 | 14 against 50 (-36) | 0.265 |
| Acid +15, f 1 | #D0C401 | 50 against 50 (0) | 0.174 |
| Acid +15, f 0.6 | #E2DA15 | 52 against 50 (+2) | 0.294 (+11 %) |
| **Acid +15, f 0.65** | **#DFD710** | **52 against 50 (+2)** | **0.272 (+3 %)** |
| Ice, before | #2981E7 | 229 against 208 (+21) | 0.055 |
| Ice -12, f 1 | #2289BE | 213 against 208 (+5) | 0.036 |
| Ice -12, f 0.6 | #52B0D6 | 207 against 208 (-1) | 0.088 |
| **Ice -12, f 0.8** | **#369BCA** | **211 against 208 (+4)** | **0.054 (-2 %)** |

Blind naming: three fresh viewers each saw six anonymous crops (each horn and each cabinet, in a different order per viewer) and named them from a fixed list (red, red-orange, orange, brown, amber, yellow, yellow-green, green, teal, sky blue, blue, royal blue, violet).

| tint | horn | cabinet |
|---|---|---|
| Dust | orange, orange, orange | orange, orange, orange |
| Acid | yellow, yellow, yellow | yellow, yellow, yellow |
| Ice | royal blue, blue, royal blue | sky blue, sky blue, sky blue |

Dust and Acid pass. Ice passes on the coordinator's ruling: for Ice any blue word passes when the hue is within 8 degrees, because "royal blue" names the depth, not another color.

Files: `proxy-*-before.png`, `proxy-dust-DFA934.png`, `proxy-acid-DFD710.png`, `proxy-ice-369BCA.png`; `before-after.png` puts each before beside its after (Dust, Acid, Ice).
