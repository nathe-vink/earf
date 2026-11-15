# Smoke at 2700 K, a proof (2026-11-15)

The owner, on the preview: "It's odd that the smoke lights look whiter than fog." The cause is the LED. Smoke has 4000 K
and Fog 2700 K (the owner's pick of 2026-11-11). Nothing else differs between the two lamps except the shell (Fog's own
dye at 1x; Smoke the speakers' gray dye at 0.3x). The lumens, the white diffuser, the exposure and the camera's 4000 K
white balance are the same for both.

`smoke-2700-proof.png` shows the rows' right ends: Hemisphere on top, Core below. On the left is the present pair; on the
right is Smoke with Fog's 2700 K LED (`LED_CCT_SET=black:2700`). Everything else is as the finals: the same rig, flux,
exposure and white balance, 256 samples, the rows' own cameras, rendered as a region of the full row frame (`BORDER`).
Fog is pixel-identical in both renders.

## Lit-glass colors (sRGB, a 40 px square on the glass)

| | Fog | Smoke now (4000 K) | Smoke at 2700 K |
|---|---|---|---|
| Hemisphere | 237, 223, 208 | 209, 210, 210 | 222, 204, 185 |
| Core | 212, 192, 172 | 170, 171, 171 | 188, 163, 136 |

At 2700 K Smoke is dimmer than Fog and never whiter. It is not grayer, though: it reads slightly warmer than Fog
(blue/red 0.83 against 0.88 on Hemisphere, 0.72 against 0.81 on Core). Fog's shell passes a little more blue than
Smoke's gray dye does.

## If the owner says yes

- **Spec:** `lamp_site.py`'s LED table (Smoke 2700 K). The LED lines in `components.json` (`hemi-ring-board`,
  `moon-led-table`): "4000 K for Dust, Acid, Ice and Smoke" becomes "4000 K for Dust, Acid and Ice; 2700 K for Poison,
  Fog and Smoke". The Hemisphere and Core BOMs (`out-dome-pendant/bom.*`, `out-orb-table/bom.*`) are rebuilt by fabkit.
- **Pictures, re-rendered at the same names in `renders/2026-11-10/barkhorn/lamp-site/final/`:**
  - `hemisphere-row.png`, about 30 min
  - `core-row.png`, about 9 min
  - `hemisphere-smoke-direct.png` and `hemisphere-smoke-under.png`, about 12 min each
  - `core-smoke.png`, about 9 min
  - `hemisphere-cluster.png`, about 33 min
  - Smoke's photometry lines, about 5 min
  - About 2 hours in all.
- `core-row-day.png` (lamps off) does not change.
- Any lit, warm or amber set built from these frames outside this lane would need re-cutting from the new frames.
