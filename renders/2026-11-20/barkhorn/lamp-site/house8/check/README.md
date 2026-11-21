# Core LIT crop check (2026-11-21)

The coordinator asked about the outlined shapes on the lit glows. These are three crops of the Core LIT at round-5 settings (studio 0.6, EV -2.6), x 420-1180, y 560-1160, 256 spp, denoised (`run.sh`):

- `base`: as rendered.
- `nogloss`: `HOUSE_TEST_NOGLOSS=1`. These meshes are hidden from glossy and transmission rays: house-key, fill, kick and horn faces and housings, and house-floorcard.
- `nocaus`: `REFR_CAUSTICS=0`.

`core-lit-crop-red-trio.png` shows the three red channels, auto-levelled, left to right.

Result: the rectangles and trapezoids go with `nogloss` and stay with `nocaus`. They are the softbox faces and their black housings, reflected in the polished outer shell. The outline is the face's edge fall-off against the housing's black rim, and the denoiser crackles it. Refractive caustics play no part.

A faint long curve stays in `nogloss`. It is unidentified; possibly the room's wall edges seen through or in the shell.

## Second set (08:00-08:50, all with HOUSE_SOFTBOX_SEEN=0)

- `unseen-noroom-front`: room-front hidden. The long curve stays.
- `unseen-noroom-all`: all five walls hidden. The big curve goes; a short line remains along the glow's bottom and right edge.
- `unseen-notrans`: HOUSE_ROOM_TRANS=0. The curve stays, so it is a reflection, not something seen through the glass.
- `unseen-at-*`: 512 spp at adaptive thresholds 0.01, 0.003 and 0.002. They are the same in time (438-443 s), texture (red high-pass std 6.5) and crackle. Adaptive sampling is not the cause.

## Denoiser guides (08:50-09:12, softboxes unseen, 512 spp)

`denoise-highpass.png` shows the red high-pass of four crops, laid out as:

| | left | right |
|---|---|---|
| top | Blender's guides (albedo and normal) | colour alone (RGB) |
| bottom | colour and albedo | prefilter NONE |

- Colour alone: the curve is gone. Red high-pass std 6.27, against 6.5 with Blender's guides. 438 s, the same time.
- Colour and albedo: the curve stays, so the albedo guide carries it.
- Prefilter NONE: the curve stays.

The mottle barely changes in any of them. The 2048-spp crop with no denoiser is the reference for its true level.

## Correction: the grain (12:40)

The "high-pass std 6.3-6.6" figures above are wrong as a measure of the grain. The 12 px blur ran over a patch only about 15 px inside the glow's top edge, so they measured the smooth fall-off at that edge.

Re-measured with a 1-6 px band-pass in the middle of the glow (std in 8-bit levels, R / luminance):

| Crop | R / lum |
|---|---|
| 512, Blender's guides | 0.97 / 1.01 |
| 512, colour-only | 0.73 / 1.01 |
| 2048 spp, no denoiser | 0.70 / 0.67 |
| ball shell hidden | 0.2 / 0.2 |

Two seeds of the same crop correlate 0.00 in that band, so the grain is render noise. It comes from the light path through the 6 mm tinted ball, and more samples or path guiding reduce it. It is about ±0.3-0.5 L*.

The adaptive-threshold result stands: the three thresholds were identical in time and crackle.
