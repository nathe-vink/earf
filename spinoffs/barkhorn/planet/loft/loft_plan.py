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
    ('banquette-a', 'right', 3.82, 5.38, 1.32, 2.72, 'ovoid'),       # in the concrete over the first and third booths
    ('banquette-b', 'right', 7.74, 9.30, 1.32, 2.72, 'hands'),       # the one the bar frame sees (the lead: the hands)
    ('lounge', 'left', 15.25, 16.85, 0.85, 2.45, 'logogram'),       # the listening room's left wall, behind the left
                                                                     # Ember speaker (the lead: the acrylic in this frame too)
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
SCONCES_LEFT_LOUNGE = [14.55]

# the listening room's signs of life (listening-r1 c5): a steel side table by the chair nearest the left Ember speaker
LISTEN_TABLE = (15.45, 4.35)



# the niches' backs are screens too (the lead, 2026-10-19): the shell behind the first, the hands behind the second
NICHE_IMAGES = ['ovoid', 'hands']


# --- the seating, after the owner's note on the review set (2026-10-19): "I want better bar chairs, like Fyrn. I want
# booth seating along a wall. The chairs on the right are facing the wrong way. The listening area should still be
# chairs and tables." ---------------------------------------------------------------------------------------------
# booths along the right-hand wall in place of the banquette and its chairs: benches across the room, a table between
# each pair with its end to the wall, high backs capped in fir, deep tan leather (not oxblood: one red, the speaker's)
BOOTH = dict(table_w=0.70, table_l=1.05, table_y0=0.05, seat_d=0.50, seat_h=0.46, back_h=1.10, back_t=0.06,
             gap=0.07, bench_l=1.30, cap_w=0.14, cap_t=0.035, leather='#7A4A2C')
BOOTH_PITCH = BOOTH['table_w'] + 2 * (BOOTH['gap'] + BOOTH['seat_d'] + BOOTH['back_t'])     # 1.96: backs shared
BOOTHS_X = [6.56 + BOOTH_PITCH * k for k in (-1, 0, 1)]              # the tables' centres: 4.60, 6.56, 8.52
TABLES = BOOTHS_X                                                    # (the den's two-tops' name, so its props follow)
TABLE = dict(w=BOOTH['table_w'], d=BOOTH['table_l'], h=0.74, y=BOOTH['table_y0'] + BOOTH['table_l'] / 2)

# the bar stools after Fyrn's Stanyan (solid walnut, a curved low back, splayed legs, graphite anodised aluminium
# brackets and footrest; no logo, no replica): seat 760, 1060 overall; the window table's two chairs the same family
# at dining height, each facing the table it serves (the owner: "facing the wrong way")
STOOL = dict(seat_h=0.76, seat_r=0.19, top=1.06, foot_r=0.215, rest_z=0.29)
CHAIR = dict(seat_h=0.46, seat_r=0.21, top=0.80, foot_r=0.20, rest_z=None)


def seats():
    """Every stool and chair outside the lounge: (x, y, the direction it faces in degrees, kind)."""
    out = [(x, y - (0.15 if i in (2, 6) else 0.0), 90.0 + ((i * 5) % 7 - 3) * 6.0, 'stool')       # facing the bar, each
           for i, (x, y) in enumerate(stools())]                     # turned a little, two pulled out (bar-p12)
    wx, wy = WINDOW_TABLE
    out += [(wx, wy - 0.62, 90.0, 'chair'), (wx, wy + 0.62, 270.0, 'chair')]                       # facing their table
    return out


def candle_spots():
    """The candles: on each booth's table, the window table, the bar, the lounge tables (the loft's own: the den's
    read its two-tops)."""
    zt = BAR_TOP_Z + TOP_T; T = TABLE
    out = [(cx - 0.18, T['y'] + 0.25, T['h']) for cx in TABLES]
    out += [(WINDOW_TABLE[0] + 0.1, WINDOW_TABLE[1] - 0.12, T['h'])]
    out += [(x, BAR_FRONT - 0.10, zt) for x in (4.1, 6.3, 8.6)]
    out += [(SIDE_TABLES[0][0] + 0.06, SIDE_TABLES[0][1] + 0.08, 0.50)]
    return out + [(LISTEN_TABLE[0] + 0.07, LISTEN_TABLE[1] - 0.06, 0.495)]
