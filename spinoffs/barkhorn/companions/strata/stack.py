"""Laminated lamps (the design pass of 2026-10-31): the numbers every proposal shares, its acrylic as a list of bonded
layers, and the checks (weight, balance, heat) worked from them. The fab kit files (core_sample.py, terrace.py, ...)
build their CAD from these layers, and scene.py builds the render's acrylic from the same list, so the picture and the
drawings never differ.

A layer is one piece of stock cast sheet, cut on a CNC router (or laser) to a ring, bonded to the next with
polymerising cement (Weld-On 40 class), the bonded stack annealed and then turned or edge-polished. Units mm.

    python3 spinoffs/barkhorn/companions/strata/stack.py        prints each proposal's layers and checks
"""
import math

# Stock cast sheet. Nominal 1/2 in is 12.7 mm (TruCast .500); the fab kit's stock table holds 12, so the CAD uses 12
# and every height here is quoted at 12.7 as well where it matters (the stack is turned or flycut to height anyway).
T = 12.0
T_REAL = 12.7
RHO = 1.19e-6            # cast PMMA, kg/mm3
RHO_AL = 2.70e-6
ACRYLIC_LIMIT_C = 70.0   # cast PMMA in long service, at the part (it softens near 95-100 C: Vicat ~105, HDT ~95)

# A&C Plastics' TruCast light-transmission chart (total transmission, %, at 3 mm: the TruCast data sheet's thickness),
# read 2026-10-31 (https://www.acplasticsinc.com/wp-content/uploads/2026/08/Trucast-Acrylic-Light-Transmissions-5.26.26-1.pdf).
# The hue each transmits is the Tint Library's stand-in colour (tint_library.STOCK_DEEP). 2208 Yellow and 1020 Purple
# are not on the chart: their figures are estimates [E] from like colours (2037 17.5, 2016 14.3 on the chart).
TINTS = {
    'Ember': ('2423', 14.1, '#D8283A'),
    'Dust': ('2422', 59.1, '#E0861E'),
    'Acid': ('2208', 45.0, '#E6C51E'),        # [E]
    'Poison': ('9093', 92.9, '#86CC36'),      # fluorescent: its chart figure counts the glow
    'Ice': ('2069', 57.6, '#2E8CCE'),
    'Haze': ('1020', 15.0, '#7A4EC0'),        # [E]
    'Fog': ('3030', 86.8, '#DCEDE6'),
    'Smoke': ('2064', 29.3, '#8C8C8A'),
    'Smoke dark': ('2074', 11.7, '#5A5A58'),
    'Clear': ('0000', 93.0, '#FFFFFF'),
}


def ring(z0, z1, ro, ri=0.0, **k):
    return dict(z0=z0, z1=z1, ro=ro, ri=ri, **k)


# --- Core Sample: a column of tint discs, bored, a filament of light up the bore ------------------------------------
CS = dict(
    od=110.0, n=14, bore=32.0, solid_top=1,      # 14 discs; the top one left whole, so the bore is blind
    base=(96.0, 16.0),                           # the foot: diameter (set in 7 under the column, a shadow line), height
    edge=1.5,                                    # the column's top and bottom arrises, rounded on the lathe
    inserts=(3, 72.0, 'M5'),                     # brass threaded inserts in the bottom disc: count, PCD, thread
    tube=(25.4, 3.2, 150.0),                     # the diffuser: opal cast acrylic tube 1 in OD, 1/8 wall, its length
    bar=(10.0, 140.0),                           # the light's spine: aluminium square bar, its side and length
    led_w=4.4,                                   # the LED strips' power at full (two runs of 140 on the bar's faces)
    # the discs from the bottom: one tint, or a chosen stack. The first: two Smoke at the foot, nine Dust (2422, the
    # chart's 59 % amber: a 39 mm path from the bore still passes its red), one Ember stratum, Dust, and Fog at the top
    stack=('Smoke dark', 'Smoke') + ('Dust',) * 7 + ('Ember',) + ('Clear',) * 4,
    # each disc's outside, finished on the lathe after turning: 'p' diamond-turned and buffed (clear, deep), 's'
    # bead-blasted satin (it glows: the light leaving the filament scatters there). Masked with tape disc by disc
    finish='ppsppspspp' + 'ssss',
)


def core_sample(P=CS):
    b_h = P['base'][1]
    L = []
    for k in range(P['n']):
        z0 = b_h + k * T
        bore = 0.0 if k >= P['n'] - P['solid_top'] else P['bore'] / 2
        L.append(ring(z0, z0 + T, P['od'] / 2, bore, tint=P['stack'][k], finish=P['finish'][k]))
    return L


# --- Terrace: Hemisphere as a dome of stacked rings -----------------------------------------------------------------
HT = dict(
    R=140.0, n=12, overlap=10.0, top_hole=30.0,  # a 280 dome in 12 rings; each ring laps the one above by 10 (the bond)
    rim_min=11.0,                                # no ring narrower than this
    tint='Ember',
)


def terrace(P=HT):
    """Rings from the rim up (z = 0 at the rim's underside). Each ring's outer edge is the sphere's radius at its
    underside (so the terrace's tread is the sheet's own face), its inner edge laps the ring above by `overlap`."""
    R, n = P['R'], P['n']
    ro = [math.sqrt(max(R * R - (k * T) ** 2, 0.0)) for k in range(n)]
    L = []
    for k in range(n):
        if k < n - 1:
            ri = min(ro[k + 1] - P['overlap'], ro[k] - P['rim_min'])
        else:
            ri = P['top_hole']
        L.append(ring(k * T, (k + 1) * T, ro[k], ri, tint=P['tint']))
    return L


# --- Contour Core: the ball drawn in terraces, an opal globe inside -------------------------------------------------
CC = dict(R=80.0, n=14, skip=1, wall=18.0, neck=30.0, cap=2, base_top=30.0, tint='Ember',
          globe=(100.0, 57.0))                   # the opal globe: diameter, neck OD (a stock 4 in globe, 2 1/4 fitter)


def contour_core(P=CC):
    """The ball's terraces from the bottom: the sphere's first `skip` layers left off, so it stands on a flat ring
    (its neck, where the globe goes in) set on the base at `base_top`."""
    R, n = P['R'], P['n']
    zc = n * T / 2                                   # the sphere's centre, above the first (skipped) layer's underside
    L = []
    for k in range(P['skip'], n):
        a, b = k * T - zc, (k + 1) * T - zc          # the layer, relative to the centre
        near = 0.0 if a < 0 < b else min(abs(a), abs(b))
        ro = math.sqrt(max(R * R - near ** 2, 0.0))  # each terrace stands proud of the sphere, its tread the sheet face
        Ri = R - P['wall']
        ri = math.sqrt(max(Ri * Ri - near ** 2, 0.0))
        if k >= n - P['cap']:
            ri = 0.0
        if k < P['skip'] + 2:
            ri = max(ri, P['neck'])
        z0 = P['base_top'] + (k - P['skip']) * T
        L.append(ring(z0, z0 + T, ro, ri, tint=P['tint']))
    return L


# --- Halo: Hemisphere as a thick ring of strata (the Core Sample's pendant twin) -----------------------------------
HL = dict(od=260.0, id=160.0, n=5, tint='Dust',
          stack=('Dust', 'Dust', 'Ember', 'Dust', 'Dust'), finish='pspsp')


def halo(P=HL):
    """Five discs from the bottom (z = 0 at the ring's underside), each the same ring."""
    return [ring(k * T, (k + 1) * T, P['od'] / 2, P['id'] / 2, tint=P['stack'][k], finish=P['finish'][k])
            for k in range(P['n'])]


# --- the checks -----------------------------------------------------------------------------------------------------
def volume(L):
    return sum(math.pi * (l['ro'] ** 2 - l['ri'] ** 2) * (l['z1'] - l['z0']) for l in L)


def mass(L):
    return volume(L) * RHO


def centroid_z(L):
    m = [(math.pi * (l['ro'] ** 2 - l['ri'] ** 2) * (l['z1'] - l['z0']), (l['z0'] + l['z1']) / 2) for l in L]
    return sum(a * z for a, z in m) / sum(a for a, _ in m)


def tip_angle(cg_z, contact_r):
    """Degrees a free-standing lamp must lean before it tips (its weight over the edge of its footprint)."""
    return math.degrees(math.atan2(contact_r, cg_z))


def sink_rise(watts_heat, area_m2, h=10.0, eff=1.0):
    """Kelvin over room air for a heat sink: natural convection plus radiation from black anodise, h about 9-12
    W/m2K for a small part in still air; `eff` the fin efficiency."""
    return watts_heat / (h * area_m2 * eff)


def fin_stack_area(n, od, core, t, pitch):
    """A stack of `n` aluminium discs `od` across on a `core`, `t` thick at `pitch`: both faces and the rims, m2."""
    face = 2 * math.pi * ((od / 2) ** 2 - (core / 2) ** 2)
    rim = math.pi * od * t
    return n * (face + rim) * 1e-6


def report():
    out = []
    L = core_sample()
    m = mass(L)
    out.append(('Core Sample', f'{len(L)} discs of {T:g} ({T_REAL} real): {L[-1]["z1"] - L[0]["z0"]:.0f} tall '
                f'({len(L) * T_REAL:.0f} at 12.7), acrylic {m:.2f} kg, its CG {centroid_z(L):.0f} up; '
                f'tips at {tip_angle(centroid_z(L), CS["base"][0] / 2):.0f} deg on its {CS["base"][0]:.0f} foot'))
    for name, f in (('Terrace', terrace), ('Contour Core', contour_core)):
        L = f()
        out.append((name, f'{len(L)} rings, {L[-1]["z1"] - L[0]["z0"]:.0f} tall, acrylic {mass(L):.2f} kg; rings '
                    + ', '.join(f'{l["ro"]:.0f}/{l["ri"]:.0f}' for l in L)))
    return out


if __name__ == '__main__':
    for k, v in report():
        print(f'{k}: {v}')
