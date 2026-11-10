"""Reads dome_paths.py's EXRs: the mean linear luminance over the dome's face (the pixels over 0.5 in REF, the final).

    python3.11 spinoffs/barkhorn/night-pictures/dome_paths_read.py REF.exr A.exr [B.exr ...]
"""
import sys
import numpy as np
import OpenEXR

LUM = np.array([0.2126, 0.7152, 0.0722])


def load(p):
    with OpenEXR.File(p, separate_channels=True) as f:
        ch = f.channels()
        get = lambda c: np.asarray(next(v.pixels for k, v in ch.items() if k.split('.')[-1] == c), dtype=np.float64)
        return np.stack([get('R'), get('G'), get('B')], -1)


ref = load(sys.argv[1]) @ LUM
mask = ref > 0.5
print(f'dome face: {mask.sum()} px')
for p in sys.argv[1:]:
    a = load(p); y = a @ LUM
    rgb = a[mask].mean(0)
    print(f'{p}: dome mean {y[mask].mean():.5f}  (RGB {rgb[0]:.5f} {rgb[1]:.5f} {rgb[2]:.5f}; G/R {rgb[1] / max(rgb[0], 1e-9):.2f}, B/R {rgb[2] / max(rgb[0], 1e-9):.2f})')
