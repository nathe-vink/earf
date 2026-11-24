# Light model C: the eight Tropos fronts and the horn 360 (24 Nov)

The owner chose light model C on 24 Nov ("5. C"). It is the coordinator's 21 Nov 08:34 recommendation: the critics were unanimous for S1 test c, `renders/2026-11-21/barkhorn/s1-test/`.

- **Light model C:** one physical light model.
  - Both caustics are on, with clamp 0 and filter_glossy 0.
  - The acrylics' shadow-ray shortcut is cut.
  - The sweep's painted contact term is off, so every shadow is cast by the lights.
- **Shots:** made by `spinoffs/barkhorn/campaign/light_c.py`.
  - `front-<tint>.json`: 8 fronts, 1000 x 1250, 96 spp. Each is the approved tallr7 front's shot, made model C.
  - `turn-<tint>-NN.json`: 8 x 24 frames, 1200 x 1080, 96 spp. Each is `horn_turn.frame`, made model C.
- **Render:** `bash renders/2026-11-24/barkhorn/light-c/run.sh NAME ...`. It is resumable, and it commits and pushes each frame.
- **Needs:** `studio/setup.sh`, then the two model builds:

  ```
  .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud
  .venv-fab/bin/python spinoffs/barkhorn/variants/render_model.py
  git checkout -- spinoffs/barkhorn/out-cloud
  ```

  The last line restores the drawings the build rewrites.
- **Audit:** every frame's `.equipment.txt` must read equipment 0 and hidden 0, and every log `NO GLASS SHADOWS`.
