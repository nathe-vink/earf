# B1: bar-backbar, live against fixed (21 Nov), a test, not a final

- **live:** the site's frame from its committed shot file (renders/2026-11-11/barkhorn/product/planet-bar/bar-backbar.shot.json), at 1600 x 900 and 256 samples. Lamps are at ecb1650c24, because the 14 Nov frame recorded no lamps commit.
- **fixed:** everything below is set by `gen.py`.
  - Both caustics are on, with clamp 0 and filter_glossy 0.
  - The shadow-ray shortcut is cut. It was found on 7 materials, all Tropos plus the sink.
    - The bar's Mantle asset (fa0c3a65) carries no shortcut on any of its 464 materials. The newer Mantle (1dc3bd57) carries it on 136.
    - The Cores here carry no shortcut either.
  - horn-card is off transmission.
  - The drinks are at their own IOR: whisky 1.36, ice 1.31, with the ice cut at the liquid's top.
- **Readings:** `meas.md` (`python3 meas.py`), L* / C* by box.
- **Noise:** reflective caustics add no fireflies. Counting pixels more than 60 levels over their 5 x 5 neighbours' median gives live 2292 and fixed 1601.
- **What changes:**
  - **The near horn's bell goes black** (L* 8.9 to 0.3). Its look was the horn card seen through the clear horn. Hidden from transmission, the card shows only in the outer surface's reflection, which this angle does not catch.
  - **The near cabinet's front** falls from 35.6 to 15.4 L*, and the far cabinet from 15.7 to 11.4. The bay lamps now light the inside only by refracting through the acrylic.
  - **The record wall** rises from 27.5 to 37.5 L*. Light from the glossy bar top and the deck now reaches it through reflective caustics and filter_glossy 0.
  - **The Cores** rise from 26.7 to 31.0 L*.
  - **The deck and Mantle** fall from 17.5 to 13.3 L*.
  - **The drinks:**
    - the ice reads as clear cubes in the whisky;
    - the liquid is a little darker, 35.1 to 30.4;
    - the green glow behind them goes.

## fixed-2 (the coordinator, 10:00): fixed plus two real lights (`gen2.py`, `gen3.py`; `fixed2.json`)

- **track-front1:** one more head on the bar's ceiling track (z 3.35, a 14 cm disc, #FFE2C0, a 22 degree spread).
  - It hangs at (8.6, 3.9), 1.4 m in front of the near bay, aimed at the cabinet's front (8.25, 5.45, 1.5), at 10 W/m2.
  - It is out of frame, 67 degrees above the camera's axis. Every ray visibility is on.
- **ceiling-panel:** a 1.6 x 0.8 m soft light panel under the ceiling at (10.5, 4.0, 3.2), behind and right of the camera, at strength 15.
  - It faces the near bell, on the bell's probed mirror ray (`--probe waveguide`).
  - Its diffuse and specular are both on. Like every engine panel, it casts no shadow.
  - The bell mirrors mostly itself (55 %). The niche's header frames what else it can see, so the panel gives the bell's left flank a wedge-shaped highlight and lights its rim.
  - A 3.0 x 1.6 m panel gave the same wedge (`crops-front10-card0-6-15.png`, `fixed2c-10-L8.json`).
- **Readings:** `meas.md`.
  - The near cabinet's front reads 54.7, against 35.6 live and 15.4 fixed.
  - The bell reads 2.0, against 8.9 live and 0.3 fixed.
  - The deck and Mantle read 24.0, and the whole frame 20.3, against 14.8 live.

## fixed-3 and fixed-4 (the coordinator, 11:19 and 11:53)

- **fixed-3:** the head at 6 W/m2 and the panel at 8. The front read 48.9 and the whole frame 19.1. The head's 22 degree cone flooded both of the bay's walnut pillars (right pillar 53 L*, against 11 live).
- **fixed-4:** the head narrowed to the bay heads' 14 degrees, at 5 W/m2, with the panel kept at 8.
  - Crop tests at 6 and 4 W/m2 are in `crops-fixed3-fixed4-6-4.png`.
  - The front reads 41.2, the pillars 9.9 and 15.9, the deck and Mantle 18.7, and the whole frame 17.0.
  - Most of the frame's excess over live (14.8) is the record wall (37.6 against 27.5). That lift comes from fixed's light model (reflective caustics, filter_glossy 0), not from the head.
  - The panel still gives the bell its wedge highlight: bell 1.2, against 0.3 without it.

## fixed-5, a crop test (the coordinator, 12:46): fixed-4 with no horn card, and the ceiling panel as a real light (`gen5.py`)

- **horn-card** is removed.
- **ceiling-light** replaces the ceiling panel: an engine area lamp (a Cycles AREA light) of the same size, place, aim and colour.
  - Every ray visibility is on, the camera's included, and its light casts shadows.
  - Its power is 22.5 W, from 2.2 x strength x area. I measured that factor on 21 Nov on a white floor 1 m under a 1 m square: an emission strength of 1 read 0.277, and a 1 W area lamp read 0.126.
- **Crops:** `fixed5-near.png` (x 960, y 0, at 256 samples) and `fixed5-wide.png` (x 560, y 270, at 128). Side by side with fixed-4: `fixed4-5-near.png` and `fixed4-5-wide.png`.
- **Readings:** `meas5.md` (`python3 meas5.py`).
  - The bell is 0.8 against 1.2, and its wedge highlight stays.
  - The front is unchanged at 41.2.
  - The pillars read 3.7 / 14.1 against 3.9 / 15.2.
  - The deck and Mantle read 18.4 against 18.7.
  - The whole frame is about 16.5 against 17.0.

## fixed-6 (the coordinator, 13:24 to 15:20): every light real (`gen6.py full 40`, `fixed6.json`)

- **Crop tests t1-t10:** `crop6-t*.png`, with the pass tests in `meas6-crops.md`.
  - The frontal softbox, a large soft source, makes the cone dark matte and lights the batts.
  - Neither a real softbox where the horn card hung nor a hidden 40 W niche washer makes the bell yellow. The niche felt is about 1 % albedo, and the live card spanned z 3.04-3.58, more than half of it above the ceiling.
- **The lights:**
  - no horn card;
  - house and house-left inside the room;
  - a 1.4 x 0.9 m diffuser flush under the ceiling over the near bay, strength 6;
  - a 1.2 x 0.9 m frontal softbox at strength 40 on each bay: near (8.6, 4.3, 3.0), far (6.1, 3.9, 2.98).
  - Every one is a mesh in a black body (living_ext.softbox), with every ray visibility on, casting shadows, out of frame and under the 3.40 ceiling.
- **Pass tests** (`meas6.md`):
  - cone 12.0 and cap 6.0, against 22 / 24;
  - cone/batts 0.15, passes;
  - sill 26.9;
  - the bell's top 5 % 18.1 / C* 6.4 / h 101: dark, not yellow;
  - far bay 22.8 (57 % over 10), against live's 15.7.
- **The room** (`meas.md`):
  - The softboxes' spill lifts the record wall to 48.0, the dark left wall to 13.2 and the whole frame to 22.8 (live 14.8).
  - Shadow-ray links left: 0. Audit 0 / 0.

## fixed-7 (the coordinator, 16:09 and 16:30): fixed-6 with real light control (`gen7.py`, `fixed7.json` = `fixed7d.json` at full size)

- **Quarter tests:** fixed7q, 7bq, 7cq, 7dq, 7eq and 7fq (800 x 450, 96 samples).
  - Grids and skirts take the spill off the ceiling and the left wall. The record wall's lift is the softboxes' direct beam, which dimming the wall heads offsets.
  - The quarter tests read the cone/batts ratio high (0.41-0.50). At 800 px the denoiser blends the 75 px woofer into its surround. The full frame reads 0.14.
- **The lights:**
  - both frontal softboxes at strength 20, each with a 0.3 m black fabric skirt; the far one at (6.5, 3.4, 2.92), so its skirt and body stay out of frame and under the ceiling (top z 3.36);
  - the 1.4 x 0.9 diffuser flush under the ceiling over the near bay at 6;
  - the record-wall heads on a dimmer at 0.35;
  - no front head, no horn card, and house and house-left inside the room.
- **Pass tests** (the coordinator's relaxed cone floor, 16:30):

  | test | target | fixed-7 |
  |---|---|---|
  | record wall | about 42 or below | 37.9 |
  | dark left wall | about 6 or below | 6.6 (marginal) |
  | whole frame | about 18 or below | 17.1 |
  | hemispheres | about 17-19 | 19.3 (marginal) |
  | cone | 6-12, dark matte | 8.7 (cap 1.9) |
  | cone/batts | about 0.25 or below | 0.14 |
  | sill | 18-25 | 18.8 |
  | far bay | as the near one reads | 15.9 (live 15.7) |
  | bell's top 5 % | yellow | 11.1 / C* 2.3: a dark polished horn, as ruled |

- **At 800 px:** no hard skirt edge shows. Audit 0 / 0; shadow-ray links left: 0. `live-over-fixed7.png` shows the two at 800 px.

## fixed-8 (the coordinator, 18:05 to 22:06; `gen8.py full`, `fixed8.json`)

- **Step 1, the probe build** (`fixed8-probe.log`):
  - every emitter's ray visibility is all on;
  - shadow-ray links: 0;
  - the shortcut is cut on 7 materials.
- **The rig:**
  - the near softbox is 2 cm lower;
  - track-bar1 and track-horn1 are off;
  - the diagnostics run last.
- **P1, the near horn.**
  - Crops a1 and a3 (an opal behind the horn), b160 and b400 (a pale back and an LED strip), and w1 and w2 (a warm opal over the whole back).
  - The horn mouth shows the back (33 %), the left cheek (33 %), the ceiling (15 %) and the pod (18 %), so a back light lights only its share.
  - The call: w2's warm #FFE2C0 opal at strength 2 on both niche backs, with the near Tropos moved 2 cm right and 2 cm deeper.
  - At 5 cm deeper (`fixed8-5cm`) the cone's lower flank mirrored the cabinet's own lit interior: a crescent, lower half 34.4.
  - Moving the near softbox did not cure it (`crop8-mv2`). 2 cm (`crop8-mv3`) did.
- **P3:** the far softbox is the far horn's grey screen (`cropfar8-p3off`). It moved to (7.5, 3.6, 2.95), outside the horn's mirror window, at strength 28 (`cropfar8-p3m`).
- **P4:** the far softbox keeps its skirt, an egg-crate grid (6 x 4, 0.25 m deep) and a 0.6 m top flag (`cropfar8-p34`).
- **P5/P6** (`samp8-*`): the cone's green is real; the far batts' blotches were undersampling. The frame is at 512 spp, adaptive 0.003.
- **Readings** (`meas.md`, `meas8m.md`, `measfar8.md`):

  | | fixed-8 |
  |---|---|
  | horn mouth | 38.3 % lemon (fixed-7: 0.1 %) |
  | cone | 13.8 (upper 1.9, lower 25.7) |
  | cap | 2.1 |
  | cone/batts | 0.71 (the mask method; fixed-7 0.35) |
  | sill | 22.8 |
  | P3 screen | 7.1 |
  | far bay | 15.8 |
  | record wall | 37.9 |
  | wall top | 13.7 |
  | ceiling | 3.9 |
  | print | 15.5 |
  | whole frame | 17.7 |

  The diagnostics are clean, with 130 emitters all on. Audit 0 / 0.
- **The owner's comparison:**
  - `live-over-fixed8.png` at 800 px;
  - `near-fixed8-vs-black-1to1.png`: the near speaker at 1:1 with the panel and as the honest black horn (`crop8-black`, the same 2 cm depth and 512 spp, no panels).

## fixed-9, crop tests only (the coordinator, 22 Nov 00:29 to 03:28; `gen9.py fix --fix9` -> `fixed9-fix.json`, held for the owner's answer)

- **Q2, the ceiling streak:**
  - One-light-off crops (`crop9q2-*`) name track-bay0. Its beam on the far horn's glossy concave bell focuses into dots.
  - Aiming it lower or narrowing it still covered the horn, and a barn door would hang in the frame.
  - Moved 25 cm along its track, it threw the caustic into the frame's top-left corner (`crop9k-*`). At x 6.05 (`crop9c-*`), the streak reads 7.2, the corner 57.0, and nothing is over L* 80.
- **The far softbox:**
  - It moved 30 cm back along its throw, clear of the pendants' cords, to (7.709, 3.385, 2.94), strength 31, with its skirt, grid and 0.6 m flag kept.
  - Readings (`crop9-far2`, `measfar9.md`): P3 3.5, far bay 15.6, ceiling 4.5. The wall top reads 17.2 against fixed-8's 13.7.
  - A 0.7 m flag changes nothing there (`crop9-far3`), so 0.6 m stays and the +3.5 is accepted.
- **mantle-front:** +0.3 m (`crop9-mantle`). The Mantle's parts read L* 5.9 -> 5.8.
- **track-bay1:** 10 cm toward the wall (`crop9-near`). The cone's lower-flank smear goes: lower half 25.7 -> 11.3, cone/batts 0.71 -> 0.17. With track-bay1 back in its old place it returns (`crop9-q1bay1`: 25.3), so track-bay1 is named as Q1's cause.
- **camera true on the 14 shot lamps:** every crop's audit reads equipment 0, hidden 0.
