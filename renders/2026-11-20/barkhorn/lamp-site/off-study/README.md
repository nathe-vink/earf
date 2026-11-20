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
