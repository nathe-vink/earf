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
COLOURWAYS = dict(_R36.COLOURWAYS, neutral=dict(velvet='#3A2A20', wall='#4C453E', carpet='#2B2520', felt='#1E1C1A'))
CHAIR_LEATHER = '#2E1E16'                                            # espresso (was oxblood #3A1411)
BANQ_COL = '#2B2019'                                                 # espresso mohair
SINK_DEEP = '#3A3836'                                                # Smoke
SINK_GLOW = '#FFA24A'                                                # lit, it glows warm amber

# --- 2. the bar pair's niches, either side of the decks (DJ x 6.90), symmetric; the now-playing ledge moved left ----
# about 700 wide, 1600 high, 520 deep as briefed; built 560 deep overall (20 felt + 20 back) so a 428-deep cabinet
# keeps 100 behind it for the amp and its cables
SPK_NICHE = dict(w=0.70, h=1.60, d=0.56, felt=0.02, wall=0.03, back_gap=0.10)
SPK_NICHES = [(round(DJ['x'] - 1.35, 3)), (round(DJ['x'] + 1.35, 3))]   # their centres, x
LEDGE = dict(x0=3.62, x1=4.72, z=1.95)
CLOUD_HALF = dict(w=0.280, d=0.2138)                                # the cabinet's half-footprint (its origin_mm)


def niche_box(x):
    """(x0, x1, y_front, y_back, z0, z1) of the niche centred at x (outer faces)."""
    N = SPK_NICHE
    yb = W - 0.02
    return (x - N['w'] / 2 - N['wall'], x + N['w'] / 2 + N['wall'], yb - N['d'], yb, 0.0, N['h'] + N['wall'])


def bar_speakers():
    """The bar pair: on the niche floor, 100 behind each cabinet, facing the counter (-y)."""
    N = SPK_NICHE
    y = W - 0.02 - N['wall'] - N['felt'] - N['back_gap'] - CLOUD_HALF['d']
    return [('bar', x, round(y, 4), 0.02, round(aim(x, y, x, y - 1.0), 2)) for x in SPK_NICHES]


# --- 5. configurations: a tint per product group -------------------------------------------------------------------
CONFIGS = {
    'smoke': dict(bar='smoke', listen='smoke', dome='smoke', orb='smoke', tt='smoke'),    # the house configuration
    'ember': dict(bar='ember', listen='ember', dome='ember', orb='ember', tt='ember'),
    'ice': dict(bar='ice', listen='ice', dome='ice', orb='ice', tt='ice'),
    'mixed': dict(bar='smoke', listen='ember', dome='smoke', orb='ember', tt='smoke'),
}
SPEAKER_FLAVOUR = {'smoke': 'cloud-black', 'ember': 'cloud-red', 'ice': 'cloud-blue'}
LAMP_FLAVOUR = {'smoke': 'smoked', 'ember': 'ember', 'ice': 'ice'}
LAMP_GLOW = {'smoke': 1.1, 'ember': 0.4, 'ice': 0.4}                 # the lead's: about 1.1 smoked, 0.4 coloured
TT_DEF = 'spinoffs/barkhorn/companions/out-concepts2/r3.json'        # R3 Float, until the owner picks
