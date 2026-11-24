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
