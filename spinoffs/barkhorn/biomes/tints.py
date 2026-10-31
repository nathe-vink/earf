"""Tropos's eight tints calibrated to A&C Plastics' TruCast light-transmission chart (r48-biomes, 2026-10-31).

    python3 spinoffs/barkhorn/biomes/tints.py      ->  tints.json beside this file, and a table

Source: "Trucast Acrylic Light Transmissions" (A&C Plastics, dated 5.26.26), total transmission TT % per colour code.
The code for each tint is a PROPOSAL (the nearest stock transparent TruCast colour to the site's tint); Ember and Smoke
follow the Tropos session's stock-pair (2423 Red, 2064 Gray). The method is that session's `make/stock_tints.py`
'held' case: the seller's TT held at the sheet's own thickness (a maker dilutes the dye in thick sheet so a code keeps
its look), a hue split per channel scaled so the luminance after 8 % surface loss is the published TT.

Cabinet: 20 mm walls, TT at 20 mm. Horn: 10 mm sheet cast in a heavier dye lot "as deep as the cabinet" (the owner,
2026-10-22), so its sheet passes what the cabinet's wall passes. Output: the colour white light takes after the
renderer's `radius` (clear_resin's `deep`), 25 mm for the cabinet and 10 mm for the horn, IOR 1.49 (cast PMMA).
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
LUM = (0.2126, 0.7152, 0.0722)
SURFACE = 0.92
IOR = 1.49
# tint -> flavour, TruCast code and name, TT (%), channel split (relative absorption per channel, R G B)
TINTS = {
    'Ember':  ('cloud-red',            '2423', 'Red',               14.1, (0.08, 1.00, 0.85)),
    'Dust':   ('cloud-orange',         '2422', 'Orange (amber)',    59.1, (0.02, 0.40, 1.00)),
    'Acid':   ('cloud-amber',          '9097', 'Fluorescent Yellow', 77.6, (0.00, 0.10, 1.00)),
    'Poison': ('eucalyptus-y2k-green', '2092', 'Green',             18.6, (1.00, 0.18, 0.80)),
    'Ice':    ('cloud-blue',           '2069', 'Tinted Blue',       57.6, (1.00, 0.40, 0.06)),
    'Haze':   ('cloud-violet',         '2287', 'Violet',            13.5, (0.50, 1.00, 0.12)),
    'Fog':    ('birch-fog-clear',      '0000', 'Clear',             93.0, (1.00, 1.00, 1.00)),
    'Smoke':  ('cloud-black',          '2064', 'Gray',              29.3, (1.00, 1.00, 1.00)),
}
WALL_MM, HORN_MM = 20.0, 10.0


def hexs(c):
    s = [12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055 for x in c]
    return '#' + ''.join(f'{max(0, min(255, round(255 * x))):02X}' for x in s)


def sigma_for(split, lt, mm):
    if lt >= SURFACE:                    # clear: the surfaces account for it all
        return [0.0, 0.0, 0.0]
    lo, hi = 0.0, 5.0
    for _ in range(80):
        k = (lo + hi) / 2
        L = SURFACE * sum(w * math.exp(-k * s * mm) for w, s in zip(LUM, split))
        lo, hi = (k, hi) if L > lt else (lo, k)
    return [k * s for s in split]


def main():
    out, rows = {}, []
    for tint, (fl, code, name, tt, split) in TINTS.items():
        sig = sigma_for(split, tt / 100.0, WALL_MM)                  # per mm, the cabinet's sheet
        cab = [math.exp(-s * 25.0) for s in sig]                     # clear_resin's deep at radius 25 mm
        wall = [math.exp(-s * WALL_MM) for s in sig]                 # what 20 mm passes = what the horn's 10 mm passes
        lum = SURFACE * sum(w * x for w, x in zip(LUM, wall))
        out[tint] = {'flavour': fl, 'trucast': f'{code} {name}', 'tt_percent': tt, 'sigma_per_mm': [round(s, 5) for s in sig],
                     'cabinet_deep': hexs(cab), 'cabinet_radius_m': 0.025, 'horn_deep': hexs(wall), 'horn_radius_m': 0.010,
                     'ior': IOR, 'check_tt_20mm': round(lum * 100, 1)}
        rows.append(f'| {tint} | TruCast {code} {name} | {tt:g} % | {hexs(cab)} | {hexs(wall)} | {lum * 100:.1f} % |')
    json.dump(out, open(os.path.join(HERE, 'tints.json'), 'w'), indent=1)
    print('| tint | sheet (proposal) | TT | cabinet deep @25 mm | horn deep @10 mm | check |\n|---|---|---|---|---|---|')
    print('\n'.join(rows))


if __name__ == '__main__':
    main()
