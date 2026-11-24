# The critics' tests (2026-11-24)

The critic round on the pass's 28 frames (coordinator, 24 Nov 00:09; `spinoffs/barkhorn/coordinator/lamp-pass-critics-2026-11-22.json`
on r46-owner-notes) blocked the set: three objects hidden from the camera stood in frame. Our own audits had them; the
pass's grep dropped the lines (`"  (in|out) "` matched neither `IN FRAME` nor `practical`):

| Frame | Hidden object in frame | Share of the frame |
|---|---|---|
| Pendant (A, C) | house-key-flag (the key's floor cutter) | 18.71 % |
| Pendant (A, C) | house-wall_left (a sweep-only lamp, not lifted with the camera) | 5.45 % |
| Core (B, D) | house-floorcard (the floor ring under the base) | 30.09 % |

The rule, restored: every hidden object 0.0 % in frame by CASTCHECK. The audit now also prints every mesh's and lamp's
six ray visibilities (`RAYVIS`) and every light-linking collection with its states (`LINK`).

`tests.sh NAME` runs one test (Ember, half scale unless noted) with its audit. Tests:

| Name | What | Switches |
|---|---|---|
| h0 | pendant OFF as the pass rendered it | the pass's |
| hb1, hb2 | (b i) no flag; the key's aim moved up and left, 0.5 / 1.0 m (full scale), its power held | HOUSE_KEY_AIM |
| hb3 | (b ii) a real flag on the key, 0.12 m from it, every ray on, no linking | HOUSE_KEYFLAG_REAL, R 0.6 |
| hc | (c) wall_left lifted with the camera, the room fitted round every lamp (hidden key flag as the pass) | HOUSE_LIFT_RX, HOUSE_ROOM_FIT |
| d0, d1, d2 | (d) Core OFF: as now; no ring; no ring and the two cutters real (every ray on, no linking) | HOUSE_CUT_REAL |
| e1, e2 | (e) pendant / Core LIT, softboxes seen, colour-only denoise; full scale, 512 spp, a crop | HOUSE_SOFTBOX_SEEN=1 |

hb1-3 and hc carry HOUSE_ROOM_FIT and wall_left lifted, so their audits can read 0.0 everywhere.

## (f) Smoke's lit colour: the LED and the camera's white balance

- **LED:** 4000 K (`LED_CCT`, the owner's "Go" of 11 Nov; on 15 Nov he ruled warm out: "No on warm smoke light. It looks
  light yellow"). pass.sh sets no LED_K, so Smoke lights at 4000 K.
- **Camera white balance:** the house ground's, 5600 K with tint 3 (`house-ground.json` render; `lamp_site.py` sets it for
  every house frame). The Tropos studio is daylight; the 15 Nov rows the owner judged used 4000 K and tint 0.
- So the house LIT frames show a 4000 K LED through a 5600 K, tint-3 (greener) camera: warm and a little green. A flat
  4000 K emitter rendered both ways (Khronos PBR Neutral, same exposure): house WB L 52.9 C 18.7 h 78; 4000 K, tint 10
  WB L 53.1 C 3.6 (neutral). Smoke's glow in the pass measures L 14 C 14 h 84: that warm-green light, dark behind the
  1.2x gray shell, is the olive-brown.
- The same holds for every tint: Fog's 2700 K reads h 70.5 C 51 (a flat 2700 K emitter under the house WB: h 73 C 47).
- A fix is a camera choice, not a lamp one: the LIT frames at the 15 Nov rows' 4000 K (or per lamp) white balance, the
  studio's own light corrected to stay neutral on the paper. That changes every LIT frame; not tested here.

## Results (Ember; half scale unless noted; corners L*, shade/ball "whole" L*/C*)

| Test | CASTCHECK | TL | TR | ML | MR | LL | BR | Product |
|---|---|---|---|---|---|---|---|---|
| h0 pass as rendered | key flag 18.7, wall_left 5.45 | 83.9 | 93.1 | 84.0 | 92.4 | 96.5 | 88.3 | shade 37.4/67.1 |
| hc wall_left lifted, room fitted | key flag 18.7 (kept on purpose) | 79.9 | 92.8 | 78.9 | 90.9 | 96.5 | 87.8 | shade 36.9/66.2 |
| hb1 key aim +0.5 up-left, no flag | all 0.0 | 79.9 | 92.9 | 78.9 | 95.9 | 96.5 | 86.7 | shade 36.4/66.9 |
| hb2 key aim +1.0 up-left, no flag | all 0.0 | 85.4 | 92.7 | 85.2 | 88.6 | 96.5 | 83.5 | shade 35.0/65.8 |
| hb3 real flag 0.12 m off the key | all 0.0 | 79.9 | 92.9 | 78.7 | 91.2 | 96.4 | 94.9 | shade 37.1/66.5; the flag shows as a dark notch in the shade's upper-left highlight |
| d0 Core OFF as now | floorcard 30.09 | 82.3 | 93.1 | 88.5 | 93.3 | 92.8 | 89.6 | base 154/32/29, L* 33.9 C* 58.2; floor left 96.2, front 89.2 |
| d1 no ring | all 0.0 | 81.6 | 93.0 | 88.4 | 93.2 | 92.8 | 89.5 | base 143/24/22, L* 30.6 C* 56.8; floor as d0 |
| d2 no ring, real cutters | all 0.0 | 81.5 | 93.0 | 88.4 | 93.2 | 85.2 | 86.4 | base 96/8/7, L* 18.7 C* 45.0; floor front 82.5; the horn cutter cuts the ball's top highlight |

hb1-3 carry hc's wall_left lift and room, so their TL/ML are hc's. hb1-3, d0-2 rendered by the Smoke helper (1fed05ae).

(e), full scale, 512 spp, crops beside the pass's own C and D (softboxes unseen):
- e1 pendant: thin outlines of the softboxes on the glow (a rectangle low on it, arcs higher), at about the grain's
  amplitude per pixel, plain in a high-pass; none in pass C.
- e2 Core: the softbox's reflection is a visible pale panel on the ball's glow, and three softbox outlines read as seams
  in a high-pass; none in pass D.
