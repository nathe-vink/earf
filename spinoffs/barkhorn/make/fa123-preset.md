# The FA123's preset (DRAFT, 2026-11-13)

> **OPEN until Hypex answers: the bridged load** (the woofer's 5.55 to 5.9 ohm minimum against Hypex's 8 ohm
> recommendation for BTL). Do not ship a bridged preset before Hypex has confirmed it. (`fa123.md`)

The FA122's preset (`product.py`, the build notes; `fai.md` M2 and M3) carries over, with these changes:

| | FA122 now | FA123 |
|---|---|---|
| woofer channel | channel 1, 125 W into 4 ohm | **channels 1 and 2 bridged (BTL on in HFD)**, 250 W into 8 ohm |
| soft clip | on | **on, set to 8 ohm and 125 W (31.6 V)**: holds the cone to Xmax (5.75 mm) at every frequency |
| woofer high-pass | LR4, 28 Hz, mandatory | unchanged: LR4, 28 Hz, mandatory |
| port notch | about 560 Hz, measured | unchanged |
| crossover | 1 kHz, LR4 | unchanged |
| HF channel | channel 2 (NC122MP), about 6 dB down | **channel 3 (NC100HF)**, its gain differs from the NC122MP's: **re-level the HF** to the same acoustic level, measured (FAI) |
| the three slots | the same verified preset in all three | unchanged |
| filter password | set at the factory, in the first-article file | unchanged |
| auto-standby | on | unchanged |

**What it gives.**
- The woofer's maximum at 1 m, half space, goes from about 117 to about 119 to 120 dB at 100 Hz, and from 116 to
  118 dB at 63 Hz: +2.2 dB over the FA122, the cone held to Xmax.
- Left at the full 250 W, it would gain +5 dB with the cone past Xmax at 50 to 80 Hz: audible distortion at full
  level. Hence the 125 W soft clip.
- Never damaged: the full bridged swing peaks at 8.1 mm against an Xdamage of 15.5.

**First article.** M2 (the woofer's limit) and M3 (the HF level) as now, with the HF level re-measured on channel 3.
