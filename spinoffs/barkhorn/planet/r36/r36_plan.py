"""Planet EARF, round 36: the loft's shell (loft/loft_plan.py, imported whole: the concrete, the fir beams, the steel,
the frosted screens) made into a designed place, from the owner's note on round 34's set (2026-10-19: "The stools,
booths and listening area are okay, but aren't quite classy or unique enough") and the lead's reading of five bars
(Ginza Music Bar, Jazz Spot Bokunen, Space Talk, Equal Parts, A Bar with Shapes for a Name).

Every dimension here is a proposal until the owner signs it. Same frame: metres, x into the room from the shopfront
glass, y across from the right-hand wall, z up from the bar's floor.
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'loft'))
from loft_plan import *                                             # noqa: F401,F403  the shell, unchanged
import loft_plan as _LP

W, L, CEIL = _LP.W, _LP.L, _LP.CEIL
YC = W / 2                                                          # the room's axis

# --- 3. a room within the room: the listening zone raised 200 behind the smoked partition --------------------------
ZONE = dict(x0=11.80, z=0.20, step=0.20)                           # the step at x0, the zone's floor at z
COLOURWAYS = {                                                       # 2. one saturated zone, proofed two ways
    'green': dict(velvet='#173326', wall='#1D3A2D', carpet='#14291F', felt='#10201A'),    # deep bottle green
    'oxblood': dict(velvet='#4A1216', wall='#3F1417', carpet='#33100F', felt='#240B0C'),  # tone-on-tone with Ember
}

# --- 1. the speakers as an altar: a niche in the back wall lined in end-grain blocks, the pair on solid oak plinths,
# symmetric about the best seat and toed in, felt behind ---------------------------------------------------------------
ALTAR = dict(x0=16.15, y0=YC - 2.10, y1=YC + 2.10, z1=2.60, cheek=0.22, block=0.11, felt_t=0.04)
SEAT = (13.15, YC)                                                  # the best seat
PAIR36 = dict(x=16.55, dy=1.15, plinth=0.26, plinth_w=0.62, plinth_d=0.56)


def speakers():
    """The Ember pair on the altar (the back-bar's Fog pair is gone: the back bar is quiet)."""
    z = ZONE['z'] + PAIR36['plinth']
    return [('lounge', 'ember', PAIR36['x'], y, z, round(aim(PAIR36['x'], y, *SEAT), 2))
            for y in (YC - PAIR36['dy'], YC + PAIR36['dy'])]


# --- 5. the listening seats: low 1970s velvet tub chairs with small round tables, all facing the altar --------------
TUB = dict(r=0.40, h=0.66, seat=0.38, arm=0.56, open_deg=110)     # the opening faces the altar
TUBS = [(13.15, YC - 0.55), (13.15, YC + 0.55), (14.20, YC - 1.75), (14.20, YC + 1.75), (12.35, YC - 1.85),
        (12.35, YC + 1.85)]
TUB_TABLES = [(13.15, YC), (14.15, YC - 2.45), (14.15, YC + 2.45), (12.55, YC - 1.05), (12.55, YC + 1.05)]
TUB_TABLE = dict(r=0.22, h=0.46, top=0.035)

# --- 4. a sculpted counter: a racetrack bar, a 70 mm zinc top with a rounded edge, a fluted oak front --------------
COUNTER = dict(x0=3.55, x1=10.05, y0=4.05, y1=4.75, top_t=0.07, top_z=1.07, over=0.04, flute=0.034, rail_z=0.22,
               rail_off=0.16)
DJ = dict(x=6.90, w=1.30)                                           # the turntables and the rotary mixer, built in
BACKBAR36 = dict(y=5.70, low=0.92, doors=0.52, niche=(8.90, 9.90, 1.05, 2.05))   # steel doors, one lit timber niche
RECORD_WALL = dict(x0=3.40, x1=10.30, y=5.72, depth=0.36, z1=3.05, cell=0.36, z0=1.20)   # floor-to-ceiling above
DISC = dict(x=6.90, z=2.05, r=0.62)                                 # the frosted disc behind the DJ station
NAMEPLATE = dict(x=2.30, y=W - 0.03, z=2.15, r=0.30)               # the etched acrylic disc, by the door
LEDGE = dict(x0=4.20, x1=5.30, z=1.95)                              # the now-playing ledge

# --- 5. the counter chairs: a low curved back, an upholstered seat on dark oak, at 760; a brass foot rail ----------
CHAIRS36 = dict(seat_h=0.76, seat_r=0.21, back=0.24)
NCHAIRS = 8

# --- 5. the banquette: a built-in curved oak banquette, channel-tufted, loose cushions, along the right-hand wall --
BANQ36 = dict(x0=3.30, x1=10.20, d=0.66, seat=0.45, back=1.05, end_r=0.70, cushion='#2C2420')
TABLES36 = [4.30, 5.85, 7.40, 8.95]                                 # small round tables, a chair opposite each
TABLE36 = dict(r=0.32, h=0.74, y=1.05)
CHAIR_Y36 = 1.72

# --- 6. the sink: a floating trough cast in Ember acrylic in an alcove of dark timber, between the banquette and
# the zone -----------------------------------------------------------------------------------------------------------
ALCOVE = dict(x0=10.42, x1=11.62, depth=0.06, z1=2.45)
SINK = dict(x=11.02, w=0.86, d=0.40, t=0.17, top=0.86, basin=(0.32, 0.13, 0.11))   # basin semi-axes x, y, z

# --- 7. light: the Dome pendant low over the counter, the squat Sphere on every table ---------------------------------
DOMES = [4.45, 5.85, 7.95, 9.30]                                    # over the counter, clear of the DJ disc
DOME = dict(r=0.17, h=0.13, t=0.006, rim_z=1.72)                    # the rim 650 over the zinc
SPHERE = dict(r=0.08, squash=0.82, cup_r=0.065, cup_h=0.028)        # a 160 ball, a low brass cup


def sphere_spots():
    """A Sphere on every table: the banquette's, the window table, the tub tables."""
    out = [(x + 0.08, TABLE36['y'] - 0.08, TABLE36['h']) for x in TABLES36]
    out += [(WINDOW_TABLE[0] - 0.08, WINDOW_TABLE[1] + 0.06, TABLE['h'])]
    out += [(x, y, ZONE['z'] + TUB_TABLE['h']) for x, y in TUB_TABLES]
    return out


# --- 8. acoustic treatment as craft: fabric panels in brushed-steel frames with a rail of sleeves -------------------
PANELS = [('right', 12.45, 14.05, 0.55, 2.05), ('right', 14.35, 15.95, 0.55, 2.05)]

# candles: only at the counter (the Sphere is on every table)
def candle_spots():
    zt = COUNTER['top_z']
    return [(x, COUNTER['y0'] + 0.12, zt) for x in (4.95, 8.55)]


# the frosted screens: the lounge's moved clear of the altar wall (x 16.15 on); the banquette's sit over its back
SCREENS = [s if s[0] != 'lounge' else ('lounge', 'left', 13.95, 15.75, 0.95, 2.45, 'logogram') for s in _LP.SCREENS]

# what the shot builder's lights read (den/den_shots.py): the Domes for its pendant spots, no sconces, no back-bar
# niches, the counter's line
PENDANTS = DOMES
PENDANT_RIM = DOME['rim_z']
BAR_FRONT = (COUNTER['y0'] + COUNTER['y1']) / 2 - 0.18            # the spot over each Dome: y = BAR_FRONT + 0.18
SCONCES_RIGHT = []
SCONCES_LEFT_LOUNGE = []
NICHES = []
