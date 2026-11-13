# Bands and patches in flight (pushed as each finishes, so a lost container costs only the render in flight)

- `core-bar-table-a.png`: rows 0 to 0.53 of the 3200 x 2133 frame, 512 samples. Tropos is not in this frame (an 85 mm
  lens on the Core); band a imported the detail-pass model (08:46:38, before the FA123 build wrote its own at 08:56:52).
- Band b (0.47 to 1) and the hero's two patches follow on the detail-pass package rebuilt from 3896c7e9 (= 6e4ab131's CAD).
- Bands are blended linearly over their overlap into the frame one folder up; this folder is then cleared.
