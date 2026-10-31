"""Stock cast sheet's tint, per millimetre, from published light transmission (research R1, 2026-10-31), for renders.

    python3 spinoffs/barkhorn/make/stock_tints.py          ->  a table, and stock_tints.json beside this file

R1 gives each code's luminous transmission (LT) at 0.118 in (3 mm) from two makers, which differ 2 to 5 times (Chemcast
the light end, TruCast the deep end), and warns that a maker may hold LT constant across thicknesses (the dye diluted in
thick sheet) rather than the dye per mm. So each sheet gets a bracket:

- 'deep': TruCast's LT at 3 mm, the dye per mm the same at 12.7 (Beer's law from the chip);
- 'light': Chemcast's LT, held constant at 12.7 mm (the dye per mm a quarter of the chip's);
- 'held': the central case, used for the renders: the seller's own LT (TruCast's, AC Plastics being the stock source for
  thick sheet) held at the sheet's own thickness (`t`), as a maker does that dilutes the dye in thick sheet so a code
  keeps its look. A 3/4 in 2064 that went black would not be sold as a light grey.

A channel split is assumed for each hue (the red passes red; the greys are neutral), scaled so its luminance matches the
published LT after 8 % surface loss. The output, for each case, is the colour white light takes after `radius` of the
sheet, which is what the renderer's clear_resin material takes (deep at radius)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
LUM = (0.2126, 0.7152, 0.0722)
SURFACE = 0.92
# hue: the relative absorption per channel (red: almost none in red, green and blue absorbed); LT at 3 mm (Chemcast, TruCast)
SHEETS = {
    '2423': dict(name='2423 Red', split=(0.08, 1.0, 0.85), lt=(0.4985, 0.141), t=12.7),
    '2064': dict(name='2064 Gray', split=(1.0, 1.0, 1.0), lt=(0.5707, 0.293), t=19.05),
    '2074': dict(name='2074 Dark Gray', split=(1.03, 1.0, 0.97), lt=(0.3549, 0.117), t=12.7),
}
SITE = {  # the site's colours as the model has them: white light after `radius` of each part's acrylic
    'Ember cabinet': ('#F2A29C', 25.0), 'Ember horn (deep lot)': ('#C8262B', 10.0),
    'Smoke cabinet': ('#8A888E', 25.0), 'Smoke horn (deep lot)': ('#2A292C', 10.0),
}


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def hexs(c):
    s = [12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055 for x in c]
    return '#' + ''.join(f'{max(0, min(255, round(255 * x))):02X}' for x in s)


def sigma_for(split, lt, mm):
    """Absorption per mm for each channel, k*split, with k chosen so the luminance after `mm` (and surface loss) is lt."""
    lo, hi = 0.0, 5.0
    for _ in range(80):
        k = (lo + hi) / 2
        L = SURFACE * sum(w * math.exp(-k * s * mm) for w, s in zip(LUM, split))
        lo, hi = (k, hi) if L > lt else (lo, k)
    return [k * s for s in split]


def through(sig, mm):
    return [math.exp(-s * mm) for s in sig]


def lumin(c):
    return sum(w * x for w, x in zip(LUM, c))


def site_sigma(hx, mm):
    return [-math.log(max(x, 1e-4)) / mm for x in lin(hx)]


def main():
    out = {}
    rows = []
    for code, S in SHEETS.items():
        light = [s * 3.0 / 12.7 for s in sigma_for(S['split'], S['lt'][0], 3.0)]   # Chemcast's LT held at 12.7 mm
        deep = sigma_for(S['split'], S['lt'][1], 3.0)                              # TruCast's chip, the same dye per mm
        out[code] = {}
        held = sigma_for(S['split'], S['lt'][1], S['t'])                           # TruCast's LT at the sheet's thickness
        for case, sig in (('light', light), ('held', held), ('deep', deep)):
            e = {f'{mm:g}mm': hexs(through(sig, mm)) for mm in (3.0, 12.7, 20.0, 25.4)}
            e['sigma_per_mm'] = [round(s, 5) for s in sig]
            e['render'] = [hexs(through(sig, 10.0)), 10.0]               # the colour after 10 mm, for clear_resin
            out[code][case] = e
            rows.append(f"| {S['name']} | {case} | " + ' | '.join(f"{e[k]} ({lumin(through(sig, float(k[:-2]))):.1%})" for k in ('3mm', '12.7mm', '20mm', '25.4mm')) + ' |')
    site = []
    for k, (hx, mm) in SITE.items():
        sg = site_sigma(hx, mm)
        site.append(f"| {k} | " + ' | '.join(f"{hexs(through(sg, m))} ({lumin(through(sg, m)):.1%})" for m in (3.0, 12.7, 20.0, 25.4)) + ' |')
    json.dump(out, open(os.path.join(HERE, 'stock_tints.json'), 'w'), indent=1)
    print('| sheet | case | 3 mm | 12.7 mm | 20 mm | 25.4 mm |\n|---|---|---|---|---|---|')
    print('\n'.join(rows))
    print('\n| the site | 3 mm | 12.7 mm | 20 mm | 25.4 mm |\n|---|---|---|---|---|')
    print('\n'.join(site))


if __name__ == '__main__':
    main()
