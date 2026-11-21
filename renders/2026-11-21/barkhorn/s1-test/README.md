# S1: the tallr7 fronts, a / b / c (21 Nov), tests, not finals

- **a:** as approved. **b:** refractive and reflective caustics on, filter_glossy 0, clamp 0, the shadow-ray shortcut cut (6 materials). **c:** b with the contact and core lamps at 0.
- **The rebuilt models** (the container restart wiped the GLBs) against the approved frames, a only, mean |dRGB|:
  - Ember: 0.21; 0.49% of pixels over 10.
  - Fog: 0.67; 1.23% over 10.
  - The differences are only on edges and outlines (noise, tessellation), with nothing structural.
- **Readings:** `meas.md` (`python3 meas.py ember-a ... fog-c`): L* / C* means by part (the engine's first-hit masks; the batts are read through the right side panel) and in six ground patches.
- **Seams (S5):** b against a, at the top right corner joint and along the bottom front edge, at 2x. No light line or dark line at the cemented joints in either color.
