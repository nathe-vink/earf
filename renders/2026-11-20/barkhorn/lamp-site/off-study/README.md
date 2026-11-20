# Off colors in the house light, all eight tints (2026-11-20)

This is a study for the owner's decision, not a set of finals. The approved pours are unchanged.

Hemisphere and Core are switched off on the house ground, the Tropos fronts' set scaled around the lamp (`launch/house_ground.py`). The batch-1a rig is used as it stood before the 15:13 changes (HOUSE_SOLID=0, HOUSE_ROOM=0, BRAID=0), so the table measures the pours and nothing else.

How the frames were made:
- Quarter size (400 × 500), 64 spp, the Tropos finish.
- Hemisphere at s 0.20, Core at s 0.19.

How the colors were measured:
- Each body was measured through its own mask: Hemisphere's outer tint shell, Core's ball. The masks are one-sample renders from the same camera (PRODUCT_MASK, MASK_ONLY), eroded by 2 px.
- Each body gives two readings: the whole body, and its pixels with chroma over 40. Fog and Smoke have no pixels with chroma over 40, so for them only the whole body counts.
- The gap is Core minus Hemisphere, in L*.

`off-table-sheet.png` shows each tint with Hemisphere above Core, cropped to each lamp.

```
Tint    | Hemisphere body L C h | Core body L C h      | gap L | Hemi C>40 L C h    | Core C>40 L C h    | gap L
Ember   |  34.2  51.2    36    |  44.2  67.5    36    | +10.0 |  31.3  62.4    37  |  42.9  73.9    37  | +11.6
Dust    |  54.6  69.2    40    |  56.8  71.2    36    |  +2.2 |  55.0  74.4    41  |  56.1  73.4    36  |  +1.1
Acid    |  63.3  55.6    99    |  77.4  68.4   100    | +14.1 |  66.6  63.3    99  |  79.0  72.4   100  | +12.4
Poison  |  35.8  39.4   139    |  50.1  57.8   140    | +14.3 |  33.0  53.7   137  |  51.1  64.5   139  | +18.1
Ice     |  30.3  74.3   301    |  43.2  73.2   295    | +12.8 |  30.2  79.9   301  |  42.6  75.3   295  | +12.4
Haze    |  24.3  65.9   305    |  32.2  84.3   307    |  +7.9 |  23.8  74.5   305  |  30.8  89.3   307  |  +7.0
Fog     |  90.0   1.6   139    |  94.6   1.7   140    |  +4.5 |    -               |    -               |   -  
Smoke   |  16.8   1.1   214    |  33.4   2.3   225    | +16.7 |    -               |    -               |   -  
```

What the table shows:
- In this light Core reads lighter than Hemisphere in every tint.
- The gaps run from +2 (Dust) and +4.5 (Fog) to +12 to +17 (Ember 10, Acid 14, Poison 14, Ice 13, Smoke 17). Haze is +8.
- Hue holds in every tint, within 6 degrees.
- On the dark ground the mix matched them (renders/2026-11-16/barkhorn/lamp-site/mix/).

Why: both lamps get their off color from studio light that crosses the tint, scatters off the white opal behind it, and crosses back. With the opal blacked out (an Ember test), nearly all the red goes. The two lamps differ in two ways:
- Hemisphere's pour is denser in the mix: 1.8 times Core's per millimeter in Ember, and the light crosses it twice.
- Core's opal is a closed sphere, so the light it passes comes back out. Hemisphere's liner is open below, so the light it passes leaves.

The dark ground put little light on either opal, so the two matched there.

## Ember: the price of matching in daylight (pours study)

House light, OFF, quarter size, measured as in the table above (pixels with chroma over 40):

| | L* |
|---|---|
| Hemisphere 1.8 (the mix) | 31.3 |
| Hemisphere 1.4 | 37.0 |
| Hemisphere 1.0 (as built) | 41.5 |
| Core 0.5 (approved) | 42.9 |
| Core 0.8 | 33.8 |
| Core 1.1 | 25.3 |
| Core 1.5 | 17.2 |

`ember-pours-house-off.png`, left to right: Hemisphere 1.8, Hemisphere 1.0, Core 0.5, Core 0.8.

The approved match rig of 16 Nov uses the one off rig and the rows' lit rig, measured by the mix's own boxes (`../../../2026-11-16/barkhorn/lamp-site/mix/`). In it, today's Core at 0.5 reproduces 72,0,0 off and 227,85,71 lit. Values are sRGB, with L* after them.

| Pair | House, off gap | Dark, off | Dark, lit | Light out |
|---|---|---|---|---|
| **Approved**: Hemisphere 1.8, Core 0.5 | +11.6 | H 71,13,12 (13.6), C 72,0,0 (11.8): matched | H 253,145,136 (71.5), C 227,85,71 (55.4) | H 307 lm, C 44.7 lm |
| **A**: Core to 0.8 | +2.5 | C 52,0,0 (6.6): 7 L* darker than H; 19 levels in red | C 215,61,48 (49.5): deeper, 22 L* under the dome | C 38.2 lm (−15 %) |
| **B**: Hemisphere back to 1.0 | −1.4 | H 96,14,10 (19.3): 7.5 L* lighter than C; 24 levels in red (the as-built mismatch the mix fixed) | H 255,165,157 (76.4), C as approved | H 334 lm (+9 %) |

`ember-pours-dark-off.png`, left to right: Hemisphere 1.0, Hemisphere 1.8, Core 0.5, Core 0.8 (dark off rig).

`ember-pours-dark-lit.png`, left to right: Hemisphere 1.0, Hemisphere 1.8, Core 0.5, Core 0.8 (the rows' lit rig).

In short, no single pair of pours matches in both lights:
- **Pair A** matches in daylight. In a dim room the Core reads darker than the dome, and its lit glass goes deeper and gives 15 % less light.
- **Pair B** (the lamps as built) matches in daylight. In a dim room it leaves the as-built mismatch that the mix fixed.
- **The approved mix** matches in a dim room only.

The lit colors never matched in any pair: Hemisphere's lit glass is about 16 L* lighter than Core's.
