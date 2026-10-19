"""Planet EARF, round 34 (the loft): the den's footprint (den/den_plan.py, imported whole) with the owner's new palette
and features, every added dimension here.

The owner, 2026-10-19: "For the bar I still want a lot of acrylic features, just not rainbow everywhere. The brick is
unlikely to happen in SF ... Cement walls, or cement looking walls would be cool, and I really like the idea of having
wall screens behind large acrylic panels ... My favorite interior designs are always lots of cement, some wood beams
and features, and steal/iron features."

So: board-formed concrete walls, Douglas fir beams under a plank ceiling, blackened steel; acrylic only clear, frosted
or smoked (the one speaker in each frame is the only colour); and screens behind large frosted acrylic panels set into
the concrete. Same frame as the den: metres, x into the room from the shopfront glass, y across from the right-hand
wall, z up.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'den'))
from den_plan import *                                              # noqa: F401,F403  the footprint, unchanged
import den_plan as _D

W, L, CEIL = _D.W, _D.L, _D.CEIL

# --- the ceiling: Douglas fir beams across the room under a plank deck ------------------------------------------------
BEAM = dict(w=0.14, d=0.30, pitch=1.22, x0=0.75)                    # reclaimed fir, 6 x 12 in nominal
BEAMS_X = [BEAM['x0'] + BEAM['pitch'] * k for k in range(int((L - BEAM['x0']) / BEAM['pitch']) + 1)]

# --- the screens: an image plane 0.10 m behind a 30 mm frosted acrylic panel, set flush into a concrete reveal ---------
SCREEN_T = 0.030                 # the frosted panel
SCREEN_GAP = 0.10                # the image plane behind it
SCREEN_FRAME = 0.025             # a blackened-steel angle round the reveal
# (name, wall, a0, a1, z0, z1, image): wall 'right' (y = 0) or 'left' (y = W) spans x a0..a1; 'window' spans y a0..a1
SCREENS = [
    ('banquette-a', 'right', 4.30, 5.90, 1.30, 2.70, 'hands'),       # over the banquette, between its tables
    ('banquette-b', 'right', 7.35, 8.95, 1.30, 2.70, 'ovoid'),
    ('lounge', 'left', 12.95, 15.05, 0.90, 2.55, 'logogram'),       # the listening room's left wall (the brick's place)
    ('window', 'window', 4.45, 5.75, 0.62, 2.42, 'dancer'),         # a lightbox in the shopfront, seen from both sides
]
WINDOW_BOX = dict(x0=0.18, depth=0.26)                              # the window lightbox: panels at x0 and x0 + depth

# --- the back-bar: blackened steel, clear acrylic shelves edge-lit at their polished fronts -------------------------
ACRYLIC_SHELF_T = 0.025

# --- the listening room's opening: two smoked acrylic panels in steel frames, not curtains --------------------------
PARTITION = dict(w=1.40, t=0.030, z1=HEADER_Z)

# --- the bar top: a clear acrylic band inlaid along its front edge, lit from below ----------------------------------
INLAY = dict(w=0.06, set=0.06)                                       # 60 mm wide, 60 mm in from the top's front edge

# the lamps: only the listening room keeps a sconce (on the concrete by the record wall); the screens light the banquette
SCONCES_RIGHT = []
SCONCES_LEFT_LOUNGE = [15.95]

# the listening room's signs of life (listening-r1 c5): a steel side table by the chair nearest the left Ember speaker
LISTEN_TABLE = (15.45, 4.35)


def candle_spots():
    """The den's candles, and one on the listening side table."""
    return _D.candle_spots() + [(LISTEN_TABLE[0] + 0.07, LISTEN_TABLE[1] - 0.06, 0.495)]
