"""What the companions share with the Atmosphere speakers (round 31, the owner: "Record player and lighting for one.
All acrylic."): the eight colours, the render materials that paint them as the Clouds' cabinets are painted, and the
horn's flare, which the lamp borrows.

The colours are the Clouds' own, taken from the speakers' flavours in studio/products/barkhorn-cloud.json (read, never
written): `deep` is the colour white light has after 25 mm of the tinted acrylic (the cabinet's `bark` override),
`accent` the cover and ring colour, deeper, and `sweep` the look book's sweep for that colour (lookbook21). Fog is
water-clear (round 24) and Smoke smoked black.
"""
import math

# key, name, flavour of the speaker it sits beside, deep (after 25 mm), accent, the look book's sweep
COLOURS = [
    ('ember', 'Ember', 'cloud-red', '#F2A29C', '#7A1A1C', '#EAD6D2'),
    ('dust', 'Dust', 'cloud-orange', '#F2B184', '#8C3B14', '#E9DCCB'),
    ('acid', 'Acid', 'cloud-amber', '#F2D06B', '#9A6A12', '#E9DFC4'),
    ('poison', 'Poison', 'eucalyptus-y2k-green', '#B2C9A2', '#2E4A2C', '#D9E4D3'),
    ('ice', 'Ice', 'cloud-blue', '#B5D9EE', '#24557E', '#D6E3EC'),
    ('haze', 'Haze', 'cloud-violet', '#BEADD8', '#3F2A5E', '#DCD4E6'),
    ('fog', 'Fog', 'birch-fog-clear', '#F7F8F7', '#E7E6E1', '#CFDCE4'),
    ('smoke', 'Smoke', 'cloud-black', '#8A888E', '#141316', '#DAD8D6'),
]
KEYS = [c[0] for c in COLOURS]
NAMES = {c[0]: c[1] for c in COLOURS}
SPEAKER_FLAVOUR = {c[0]: c[2] for c in COLOURS}
SWEEP = {c[0]: c[5] for c in COLOURS}

# the engine's flavours: one per colour, the tokens the materials below read
VARIANTS = {k: {'deep': deep, 'accent': acc} for k, _, _, deep, acc, _ in COLOURS}

# render materials by finish (studio/engine/materials.py presets). The tinted sheet is the Clouds' cabinet: clear cast
# resin in the engine, polished (0.05), the tint a volume absorbed along the path (`deep` after `radius`), so a thin
# edge is pale and a 300 mm platter seen edge-on goes deep, as cast sheet does.
MATERIALS = {
    'acrylic': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.025, 'roughness': 0.05},
    # the lamp's shade: 5 mm of sheet cast four times as dense in the tint, so it reads as the cabinets' 20 mm do
    'acrylic-dense': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.006, 'roughness': 0.05},
    'acrylic-satin': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': 0.025, 'roughness': 0.22},
    'accent': {'preset': 'satin_paint', 'color': '$accent', 'roughness': 0.45, 'specular': 0.4},
    'opal': {'preset': 'frosted', 'color': '#F6F3EE', 'absorb': '#F1E6D6', 'roughness': 0.5, 'radius': 0.01, 'clear': 0.05},
    'brass': {'preset': 'metal', 'color': '#C9A660', 'roughness': 0.28},
    'steel': {'preset': 'metal', 'color': '#CFCFCB', 'roughness': 0.18},
    'aluminium': {'preset': 'metal', 'color': '#BFC1C2', 'roughness': 0.35},
    'arm': {'preset': 'gunmetal', 'color': '#2C2C2E'},
    'black': {'preset': 'satin_paint', 'color': '#18181A', 'roughness': 0.5, 'specular': 0.3},
    'rubber': {'preset': 'rubber', 'color': '#161616'},
    'cartridge': {'preset': 'gloss_plastic', 'color': '#121213'},
    'cord': {'preset': 'glass', 'color': '#F2F2F0', 'roughness': 0.15},
    'pcb': {'preset': 'satin_paint', 'color': '#1E3A2A', 'roughness': 0.5},
    'cork': {'preset': 'cork', 'color': '#B08A64'},
    'led': {'preset': 'emit', 'color': '#FFD9A8', 'strength': 0.0},
    'etch': {'preset': 'satin_paint', 'color': '#EEEDEA', 'roughness': 0.85, 'specular': 0.15},
}


def flare(r0, r1, L, n=28, m=2.6):
    """The horn's flare as (r, h) points, h from the throat (0) to the mouth (L): an exponential-like growth whose
    rate `m` sets how late it opens, as the Clouds' waveguide opens late and rolls over at the rim."""
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((r0 + (r1 - r0) * (math.exp(m * t) - 1) / (math.exp(m) - 1), L * t))
    return pts


def shell_profile(inner, t):
    """A closed (r, h) profile for a shell of wall `t` on the curve `inner` (its start first, the rim last), its rim
    rolled over as a half round (eased, as every edge is). The wall lies to the curve's right going along it (for a
    horn opening upward, outside it) when `t` is positive, to its left when negative. Returns the points and the
    index runs to draw as splines (the curve, its offset)."""
    def nrm(i):
        a = inner[max(i - 1, 0)]; b = inner[min(i + 1, len(inner) - 1)]
        dr, dh = b[0] - a[0], b[1] - a[1]; L = math.hypot(dr, dh)
        return dh / L, -dr / L
    outer = [(r + t * nr, h + t * nh) for (r, h), (nr, nh) in zip(inner, [nrm(i) for i in range(len(inner))])]
    (ri, hi), (ro, ho) = inner[-1], outer[-1]
    (ar, ah), (br, bh) = inner[-2], inner[-1]
    L = math.hypot(br - ar, bh - ah); Tr, Th = (br - ar) / L, (bh - ah) / L      # the curve's direction at the rim
    cr, ch = (ri + ro) / 2, (hi + ho) / 2; rr = abs(t) / 2
    ur, uh = (ri - cr) / rr, (hi - ch) / rr
    rim = [(cr + rr * (math.cos(a) * ur + math.sin(a) * Tr), ch + rr * (math.cos(a) * uh + math.sin(a) * Th))
           for a in (math.pi * k / 6 for k in range(1, 6))]
    pts = list(inner) + rim + list(reversed(outer))
    n = len(inner)
    return pts, [(0, n - 1), (n + len(rim), len(pts) - 1)]
