"""The gate's speaker targets (the coordinator, 2026-11-04 01:47), measured by part from the engine's masks.

    python3 spinoffs/barkhorn/night-pictures/speaker_metrics.py IMAGE.png
        (needs IMAGE.mask.png and IMAGE.mask.json, from render.py --masks)

Lightness is HSL L on 0-255 ((max + min) / 2), the gate's measure; luma (Rec. 709 on the sRGB values) is given too.
- cabinet: every part that is not the horn's (horn-*, waveguide*, hf-*, caldera-*, strata-*): median L, target >= 25;
- batts: the lining's webs (lining-*-web), their mean colour (pale through the blue, not black);
- woofer: cone and surround, their mean and their spread (a readable cone has texture, not a flat black disc);
- red: the share of the speaker's pixels with red above 0;
- hue: horn against cabinet (the same blue: teal against cobalt was the fault).
"""
import colorsys
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HORN = ('horn-', 'waveguide', 'hf-', 'caldera-', 'strata-')


def main():
    p = Path(sys.argv[1])
    im = np.asarray(Image.open(p).convert('RGB')).astype(np.float64)
    ids = np.asarray(Image.open(p.with_suffix('.mask.png')))[..., 0]
    legend = {int(k): v for k, v in json.loads(p.with_suffix('.mask.json').read_text()).items()}
    if ids.shape != im.shape[:2]:
        ids = np.asarray(Image.fromarray(ids).resize((im.shape[1], im.shape[0]), Image.NEAREST))

    def sel(pred):
        keys = [k for k, n in legend.items() if pred(n)]
        return np.isin(ids, keys)
    L = (im.max(-1) + im.min(-1)) / 2
    luma = im @ np.array([0.2126, 0.7152, 0.0722])
    spk = ids > 0
    horn = sel(lambda n: n.startswith(HORN))
    cab = spk & ~horn
    batt = sel(lambda n: n.startswith('lining-') and n.endswith('-web'))
    woof = sel(lambda n: n in ('woofer-cone', 'woofer-surround'))

    def hue(m):
        c = np.median(im[m], 0) / 255.0
        h, l_, s = colorsys.rgb_to_hls(*c)
        return h * 360, c * 255
    print(f'cabinet: median L {np.median(L[cab]):.0f}, luma {np.median(luma[cab]):.0f}  (target L >= 25)')
    print(f'horn: median L {np.median(L[horn]):.0f}')
    if batt.any():
        print(f'batts: mean RGB {np.round(im[batt].mean(0))}, median L {np.median(L[batt]):.0f}  ({batt.sum()} px)')
    if woof.any():
        print(f'woofer cone and surround: mean RGB {np.round(im[woof].mean(0))}, L spread (p10-p90) '
              f'{np.percentile(L[woof], 10):.0f}-{np.percentile(L[woof], 90):.0f}')
    print(f'red above 0: {100 * (im[spk][:, 0] > 0).mean():.0f} % of the speaker '
          f'(cabinet {100 * (im[cab][:, 0] > 0).mean():.0f} %, horn {100 * (im[horn][:, 0] > 0).mean():.0f} %)')
    hh, hc = hue(horn); ch, cc = hue(cab)
    print(f'hue: horn {hh:.0f} deg (median RGB {np.round(hc)}), cabinet {ch:.0f} deg (median RGB {np.round(cc)})')


if __name__ == '__main__':
    main()
