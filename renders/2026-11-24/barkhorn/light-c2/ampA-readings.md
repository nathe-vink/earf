# Amp rig A at full size: the eight against FA123 (24 Nov)

ampA-<tint>: the S4b amp rig (bounce card and front strip real, flag 1 out of the cove), back-top off, -0.2 EV for all eight, 1600 x 1600, 128 spp; rendered by the eight helpers on r33-lightc-{ember,dust,poison,ice,smoke} and r33-lightc2-{acid,haze,fog}, merged here. Every frame: equipment 0, hidden 0, no_glass_shadows.cut 6, shadow_ray_links_left.count 0, no flag crossing. Measured with amp-test/meas.py on each frame's own mask: plate face (amp-plate-plate), plate (all amp-plate parts), surround (everything else), pinned (any channel >= 251, whole frame), flat-panel blotch (band-pass 3-12 px, the panels' flat inside), print (amp-plate-print). Sheet: sheet-ampA.png (FA123 beside A, per tint).

| frame | plate face L* | plate L* | plate C* | surround L* | surround C* | surround Y share | pinned >= 251 | panel blotch L* RMS | print L* | print - plate |
|---|---|---|---|---|---|---|---|---|---|---|
| FA123-acid | 35.7 | 36.6 | 1.7 | 56.2 | 44.2 | 100 % | 6.2 % | 2.97 | 94.3 | 58.6 |
| A-acid | 20.4 | 22.2 | 2.6 | 57.8 | 50.8 | 116 % | 0.2 % | 2.30 | 90.3 | 70.0 |
| FA123-dust | 35.5 | 36.4 | 2.0 | 44.0 | 42.0 | 56 % | 9.5 % | 2.04 | 94.1 | 58.6 |
| A-dust | 20.3 | 22.1 | 2.8 | 45.0 | 47.6 | 64 % | 1.7 % | 1.90 | 90.3 | 70.0 |
| FA123-ember | 35.2 | 36.1 | 2.0 | 26.4 | 28.8 | 21 % | 2.0 % | 0.97 | 94.0 | 58.8 |
| A-ember | 20.1 | 22.0 | 2.8 | 23.1 | 40.1 | 16 % | 0.0 % | 0.83 | 90.2 | 70.1 |
| FA123-fog | 36.4 | 37.3 | 2.0 | 66.2 | 1.1 | 145 % | 0.3 % | 3.40 | 94.6 | 58.2 |
| A-fog | 20.6 | 22.5 | 2.8 | 68.2 | 1.1 | 171 % | 0.0 % | 2.69 | 90.5 | 69.9 |
| FA123-haze | 35.2 | 36.1 | 2.6 | 25.5 | 49.8 | 20 % | 3.9 % | 0.94 | 94.1 | 58.8 |
| A-haze | 20.1 | 22.0 | 3.0 | 21.9 | 60.9 | 14 % | 0.0 % | 0.79 | 90.2 | 70.0 |
| FA123-ice | 35.4 | 36.3 | 2.7 | 39.8 | 35.8 | 45 % | 7.8 % | 1.86 | 94.2 | 58.8 |
| A-ice | 20.3 | 22.1 | 3.1 | 41.3 | 34.4 | 54 % | 0.7 % | 1.71 | 90.2 | 70.0 |
| FA123-poison | 35.2 | 36.1 | 2.0 | 27.3 | 21.7 | 24 % | 1.0 % | 0.91 | 94.1 | 58.8 |
| A-poison | 20.2 | 22.0 | 2.7 | 26.8 | 33.5 | 22 % | 0.0 % | 0.82 | 90.2 | 70.0 |
| FA123-smoke | 35.3 | 36.2 | 2.0 | 25.0 | 0.8 | 22 % | 0.0 % | 0.82 | 94.1 | 58.8 |
| A-smoke | 20.1 | 22.0 | 2.8 | 15.0 | 1.0 | 9 % | 0.0 % | 0.69 | 90.2 | 70.0 |
