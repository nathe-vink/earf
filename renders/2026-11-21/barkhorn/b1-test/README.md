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
