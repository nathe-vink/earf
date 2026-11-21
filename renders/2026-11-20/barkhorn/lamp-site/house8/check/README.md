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
