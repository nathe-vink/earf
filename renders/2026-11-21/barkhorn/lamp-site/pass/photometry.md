# Group F: lumens out at the owner's pours (2026-11-22)

Same method and sensor as the 17 Nov table (`launch/isphere.py`; Hemisphere 64 bounces, 128 spp; Core 256 spp; one
scale, WLM 3.2/490). Run by `photometry.sh` on the Smoke helper's machine, raw lines in `photometry.raw`
(76054490dcbf8d12226ef402f91e80084b783727). Pours: `lamp_site.py`'s defaults (pendant × base pour; Core absolute,
the ball's own pour).

| Tint | Pendant pour | Hemisphere lm now (17 Nov) | down % | Core pour | Core lm now | Core at the 17 Nov pours, today's model | 17 Nov |
|---|---|---|---|---|---|---|---|
| Ember | 0.7 | 348.8 (307) | 66 | 0.5 | 39.2 | 39.2 | 45 |
| Dust | 2.1 | 376.1 (353) | 63 | 2.6, re-mixed | 33.0 | 46.3 | 51 |
| Acid | 3.0 | 420.2 (380) | 61 | 2.0 | 51.7 | 57.0 | 63 |
| Poison | 1.0 | 282.6 (282) | 73 | 0.45 | 25.6 | 32.5 | 38 |
| Ice | 3.0 | 307.5 (270) | 69 | 1.72, re-mixed | 32.9 | 34.6 | 39 |
| Haze | 1.0 | 280.8 (258) | 73 | 0.5, re-mixed | 26.5 | 28.0 | 33 |
| Fog | 1.0 | 522.7 (521) | 56 | 0.5 | 98.1 | 98.1 | 95 |
| Smoke | 1.2 | 260.7 (260) | 75 | 0.5 | 16.8 | 29.4 | 35 |

- **Hemisphere: 261 to 523 lm** (was 258 to 521). The method reproduces where the pour did not change: Fog 522.7
  against 521.4, Smoke 260.7 against 260.4, and Acid, Ice and Haze land on their as-built lines (419.4, 307.5, 280.7)
  now that their pours are back at built. Lighter shells send more light: Ember +14 %, Acid +11 %, Ice +14 %, Haze +9 %.
- **Core: 17 to 98 lm** (was 33 to 95). Two causes, separated by the second Core column (POURS=mix, the 17 Nov pours,
  run on today's model, 2026-11-22):
  - the model: the base's round-5 fixes since 17 Nov (b588c50d and before) cost 8 to 15 % on every tinted Core (Ember
    44.7 to 39.2 at the same pour) and Fog gains 3 %;
  - the pours: Dust's re-mix and denser pour −29 %, Poison −21 %, Acid −9 %, Ice −5 %, Haze −5 %, Ember none.
- **Smoke's Core is 16.8 lm, half its 17 Nov 35.1.** Its pour is 0.5 on the ball, where the decided pair of 16 Nov
  was 0.6× the chart loading (0.3 on the ball). If 19:09's "0.5" meant the chart unit, the ball should be 0.25 and
  the Core about 31 lm. That is the owner's to confirm; the frames were rendered at 0.5.
- Lux under the pendant was not re-measured: the opal sheet sets it (17 Nov: 336-347 lux at centre for every pour).
