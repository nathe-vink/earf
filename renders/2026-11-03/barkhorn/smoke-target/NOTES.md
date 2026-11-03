# Smoke: the target look, pending the physical sample (2026-11-03)

`Smoke-target-look.png` uses the same set, camera, light and exposure as the 2064 frames (`renders/2026-11-03/barkhorn/base-question/gate2/Smoke-day-2064-white.png`):
- the cabinet passes about 50 % through its 20 mm wall (absorption `#B6B6B6` at the material's 25 mm);
- the lining is white;
- the horn is in the same family: `#B6B6B6` at the horn's 10 mm radius, polished, the owner's horn since 15:14.

The horn sheet was proxied in three versions:
- in the cabinet's own sheet (`#DEDEDE` at 10 mm): body L 191, too pale;
- one step deeper (`#C3C3C3`): L 168;
- this frame, about the cabinet's colour per millimetre: L 156.

Measured on this frame, mean grey levels:

| | horn body | throat | lip | cabinet | top batt |
|---|---|---|---|---|---|
| this frame | 156 | 74 | 176 | 115 | 214 |
| the 50 % frame with the old deep horn | 67 | 33 | 70 | 115 | 214 |

The horn now reads as smoked glass, like the cabinet: the throat dark, the lip a grey glass edge, the pod and the posts showing through.

**The light-path check** (the critic's question: is the top batt too white behind a 50 % wall?). Two proxies, 2 stops under so nothing clips, with the finish off (`lightpath-*.png`): the same frame in the 50 % sheet, and with no absorption at all.
- The batt behind the 50 % wall reads **0.348** of the unabsorbed batt (linear light).
- Light reaching it crosses the wall twice: in through the top, out through the front to the camera. Two passes of the wall's interior is 0.543² = **0.295**.
- The render is within about 15 % of that, and light reflected inside the box makes up the difference.
- At the frame's own exposure, that predicts about 0.64 linear, **L about 210**. The frame shows **214**.

So the walls do cut the light. The batt is bright because the studio's top light is strong: without the tint, the batt clips. The frame does not oversell the sheet.

**The sheet itself:** none in our data. The one real candidate is Chemcast's 2064 ("Light Smoke" at TAP, 57.07 % at 0.118 in, R1 l.203). Held at 3/4 in, it would sit just above the 45-55 % band, and only off-cuts or a sample settle that.

## v2 (2026-11-03, after the gate's HOLD on the horn)

`Smoke-target-look-v2.png`, on the same set, camera and exposure:
- **The flare** (`horn-satin`, the polished shell) is one notch deeper, with the cabinet's slight cool cast: `#A6A9AE` at the horn's 10 mm, about 38 % through the wall. Before it was `#B6B6B6`, neutral.
- **The throat, pod, cap and pads** (`horn-formed`) are lighter, `#C8CBD0`, so the thick parts don't go black.

| | horn mean | horn 10th / 90th percentile | horn RGB | cabinet |
|---|---|---|---|---|
| v1 | 156 | 38 / 203 | 157, 155, 151 (a little warm) | 115 |
| v2 | 147 | 38 / 192 | 145, 147, 148 (cool, like the cabinet) | 115 |

**The tabs** (the front pads under the horn) average 72, with a near-black core. The pad is a solid acrylic block, and the post's bronze insert is bonded inside it. That insert is the dark core: the post's fixing seen through the pad, not a dark material. Lightening the pad's sheet further leaves the core, so no setting gives a uniform 45-50. A shorter or a clear insert is a build change.
