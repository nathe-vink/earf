"""Planet EARF, round 37: the bar as a showroom (the owner, 2026-10-20, through the lead). Round 36's room
(r36_plan.py) with these changes; every dimension is a proposal until the owner signs it.

- A neutral, warm room, so any colour works: no saturated zone; concrete, dark oak, blackened steel, zinc, the fluted
  front; upholstery in deep neutrals (espresso mohair, dark brown leather). The colour comes from the products alone.
- Four speakers, the same product: the listening pair stays on the altar; a bar pair stands on the floor in two
  timber-lined, felt-lined niches in the back bar either side of the decks, facing the counter (Ginza's Tannoys).
- The sink in Smoke (the one fixed piece), glowing warm amber when lit.
- EARF's record player at the decks: R3 Float (companions/concepts2.py) until the owner picks.
- Configurations: one parameter, a tint per product group (CONFIGS).
"""
from r36_plan import *                                               # noqa: F401,F403
import r36_plan as _R36

# --- 1. neutral: the zone in deep warm neutrals (the colourway key kept, so the kit reads it as before) -------------
COLOURWAYS = dict(_R36.COLOURWAYS, neutral=dict(velvet='#2E2019', wall='#4C453E', carpet='#2B2520', felt='#1E1C1A'))
CHAIR_LEATHER = '#2E1E16'                                            # espresso (was oxblood #3A1411)
BANQ_COL = '#2B2019'                                                 # espresso mohair
SINK_DEEP = '#3A3836'                                                # Smoke
SINK_GLOW = '#FFA24A'                                                # lit, it glows warm amber

# --- 2. the bar pair, raised (the owner, 2026-10-20, with a photo of Ginza Music Bar: "They are elevated at Ginza."):
# each on a solid built-in ledge in the back bar, its top at counter height, the steel doors running beneath; the
# cabinet tilted down toward the counter seats on a wedge and toed in toward the counter's middle; the niche starts at
# the ledge, 1450 clear inside, felt-lined, 100 behind the cabinet and 150 above it. Tilted 8 degrees, not 10: the
# cabinet (1293 tall) pivots on its base, so its top leans 180 forward; the niche is 680 deep (the briefed 560 plus
# the lean) and the top still leans 80 past the face frame, as a tilted cabinet does
SPK_LEDGE = dict(top=1.07)                                           # oak, on the worktop; 72 kg each, with margin
SPK_NICHE = dict(w=0.70, h=1.45, d=0.68, felt=0.02, wall=0.03, back_gap=0.10, floor=0.02)
SPK_NICHES = [(round(DJ['x'] - 1.35, 3)), (round(DJ['x'] + 1.35, 3))]   # their centres, x
SPK_TILT = 8.0                                                       # degrees, the front down
SPK_AIM = (6.90, 1.20)                                               # toed in toward the counter's middle (about 15 deg)
LEDGE = dict(x0=3.62, x1=4.72, z=1.95)
CLOUD_HALF = dict(w=0.280, d=0.2138)                                # the cabinet's half-footprint (its origin_mm)


def niche_box(x):
    """(x0, x1, y_front, y_back, z0, z1) of the niche centred at x (outer faces); it starts at the ledge."""
    N = SPK_NICHE
    yb = W - 0.02
    z0 = SPK_LEDGE['top']
    return (x - N['w'] / 2 - N['wall'], x + N['w'] / 2 + N['wall'], yb - N['d'], yb, z0, z0 + N['floor'] + N['h'] + N['wall'])


def bar_speakers():
    """The bar pair: on a wedge on the niche floor, 100 behind each cabinet's base, tilted and toed in.
    (role, x, y, z, rotate_z, tilt_x); z is the cabinet's origin (its base centre), the wedge under it."""
    import math
    N = SPK_NICHE
    y = W - 0.02 - N['wall'] - N['felt'] - N['back_gap'] - CLOUD_HALF['d']
    z = SPK_LEDGE['top'] + N['floor'] + CLOUD_HALF['d'] * math.sin(math.radians(SPK_TILT)) + 0.004
    return [('bar', x, round(y, 4), round(z, 4), round(aim(x, y, *SPK_AIM), 2), SPK_TILT) for x in SPK_NICHES]


# --- 5. configurations: a tint per product group -------------------------------------------------------------------
CONFIGS = {
    'smoke': dict(bar='smoke', listen='smoke', dome='smoke', orb='smoke', tt='smoke'),    # the house configuration
    'ember': dict(bar='ember', listen='ember', dome='ember', orb='ember', tt='ember'),
    'ice': dict(bar='ice', listen='ice', dome='ice', orb='ice', tt='ice'),
    'mixed': dict(bar='smoke', listen='ember', dome='smoke', orb='ember', tt='smoke'),
}
SPEAKER_FLAVOUR = {'smoke': 'cloud-black', 'ember': 'cloud-red', 'ice': 'cloud-blue'}
LAMP_FLAVOUR = {'smoke': 'smoked', 'ember': 'ember', 'ice': 'ice'}
LAMP_GLOW = {'smoke': 0.7, 'ember': 0.4, 'ice': 0.4}                 # the lead's 1.1 smoked read a blown disc (r37 p1)
TT_DEF = 'spinoffs/barkhorn/companions/out-concepts2/r3.json'        # R3 Float, until the owner picks
