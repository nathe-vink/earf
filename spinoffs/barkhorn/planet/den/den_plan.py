"""Planet EARF, round 33 (the den): every dimension of the room in one frame, read by the model
(studio/engine/kit_ext/planet_den.py), the shots (den_shots.py) and the drawings (den_sheets.py).

The owner, 2026-10-19, on round 32's room: "The bar is a little too sterile and open, and that much space in SF is
unlikely. It's gotta be cozier, including cozier, warmer lighting. I also don't love the overt rainbow coloring." So:
one narrow, deep ground floor of an ordinary San Francisco building, warm pools of light with dark between them, wood,
leather, brass, plaster and old brick, and colour only from a few speakers.

The frame: metres, z up, the floor at z = 0. x runs from the shopfront's glass line (x = 0) to the back wall (x = L);
y from the right-hand party wall (y = 0, seen from the door) to the left-hand one (y = W), where the bar runs.
Everything here is a working assumption, made for the owner to overturn.
"""

FT = 0.3048

# --- the shell: a typical SF ground-floor storefront, 23 x 56 ft, 11 ft 2 in ceiling --------------------------------
W = 7.00                         # wide (the frontage)
L = 17.00                        # deep, the shopfront to the back wall
CEIL = 3.40                      # the plaster ceiling
WALL_T = 0.25                    # party walls (brick, plastered in the front, bare in the listening room)
WAINSCOT = 1.15                  # the walnut panelling's head on the plaster walls

# --- the shopfront (x = 0): a recessed door on the right, the display window, a transom over both -------------------
ENTRY = dict(y0=0.30, y1=1.60, depth=1.20)       # the recessed vestibule; the door at its back, x = depth
DOOR = dict(y0=0.42, y1=1.48, h=2.30)            # the door itself (a half-glazed walnut door), in the vestibule's back
WINDOW = dict(y0=1.85, y1=6.75, sill=0.55, head=2.50)     # the display window over a panelled bulkhead
TRANSOM = dict(z0=2.62, z1=3.22)                 # the transom lights across the whole front, over the door and window
CAFE = dict(z0=0.58, z1=1.45, rod=1.47)          # café curtains on a brass rod across the window's lower half
SIGN = dict(z=1.80, w=1.10)                      # EARF's wordmark in gold leaf on the window, at eye height (centred)
STOREFRONT_PAINT = '#1F1B18'                     # the shopfront's woodwork, a near-black brown

# --- the bar (along the left wall, y = W) -------------------------------------------------------------------------
BAR_X0, BAR_X1 = 3.40, 10.30     # 6.9 m of bar
BACKBAR_D = 0.45                 # the back-bar's depth against the wall
WORK = 0.90                      # the bartenders' aisle
BAR_DEPTH = 0.62                 # the bar's body, front face to the working side
BAR_FRONT = W - BACKBAR_D - WORK - BAR_DEPTH     # 5.03: the bar front's face (y)
BAR_TOP_Z = 1.07                 # 42 in
TOP_T = 0.05                     # a 50 mm walnut top, oiled
TOP_OVER = 0.24                  # its overhang on the guests' side
ARMREST = dict(d=0.075, h=0.055) # an oxblood leather armrest rolled along the top's front edge
FLUTE = 0.032                    # the bar front: walnut reeding, 32 mm flutes, floor to top
KICK = dict(h=0.16, set=0.06)    # an aged-brass kick plate, set back
FOOTRAIL = dict(z=0.22, d=0.05, off=0.22)
STOOLS = 10                      # at 0.69 m
STOOL_Y = BAR_FRONT - 0.50
PENDANTS = [4.55, 6.85, 9.15]    # three spun-brass domes over the bar (x), their rims 0.80 m over the top
PENDANT_RIM = BAR_TOP_Z + TOP_T + 0.80

# the back-bar: a walnut base, three shelves on brass brackets in front of an antique mirror, two niches for the
# Smoke pair (the horns at a stool-sitter's eye), each shelf lit warm from a strip under its front edge
BACKBAR_Y = W - BACKBAR_D
BASE_H = 0.92
SHELVES_Z = [1.38, 1.78, 2.18]
SHELF_T = 0.035                  # 35 mm walnut shelves
BACKBAR_TOP = 2.62               # the cornice
NICHES = [(4.30, 0.72), (8.70, 0.72)]            # (x0, width): 4.4 m apart, either end of the run
NICHE_Z0 = 0.45
NICHE_H = 1.50

# --- the banquette (along the right wall, y = 0) ------------------------------------------------------------------
BANQ_X0, BANQ_X1 = 3.10, 10.60   # oxblood leather, channel-tufted, in front of the wainscot
BANQ_D = 0.60
BANQ_SEAT = 0.46
BANQ_BACK = 1.05
TABLES = [3.75 + 1.52 * i for i in range(5)]     # five two-tops (x centres), 0.60 m square, walnut, a chair opposite
TABLE = dict(w=0.62, d=0.60, h=0.74, y=BANQ_D + 0.06 + 0.30)
CHAIR_Y = BANQ_D + 0.06 + 0.60 + 0.38

# the front by the window: one round two-top inside the café curtain, two chairs
WINDOW_TABLE = (1.25, 4.30)

# shaded wall lights: brass, a pleated linen drum shade, on the plaster above the wainscot
SCONCES_RIGHT = [3.0 + 1.52 * i for i in range(6)]        # between the banquette's tables, z 1.72
SCONCES_LEFT_LOUNGE = [13.2, 15.6]                         # on the brick in the listening room
SCONCE_Z = 1.72

# --- the listening room (x 11.6 to L) -----------------------------------------------------------------------------
LOUNGE_X0 = 11.60                # a cased opening: a walnut header at 2.55 m, heavy velvet curtains drawn to the sides
HEADER_Z = 2.55
CURTAIN = dict(w=1.35, colour='#4A1C1A')                   # each curtain's stack width, an oxblood wool velvet
PAIR = dict(colour='ember', x=L - 0.85, y=(1.25, W - 1.25))   # the Ember pair either side of the record wall, toed in
PLINTH = dict(w=0.62, d=0.56, h=0.10)            # a low walnut plinth under each
LISTEN = (13.70, W / 2)          # the sweet spot the pair aims at
CHAIRS = [(13.95, W / 2 - 0.85, 0), (13.95, W / 2 + 0.85, 0),          # (x, y, facing deg): front row
          (12.85, W / 2 - 1.75, 15), (12.85, W / 2, 0), (12.85, W / 2 + 1.75, -15),   # the second row
          (14.90, 0.95, 60), (14.90, W - 0.95, -60)]                     # one by the books, one by the brick, turned in
SIDE_TABLES = [(13.95, W / 2), (12.85, W / 2 - 0.88), (12.85, W / 2 + 0.88)]   # low walnut drums; Bell on two
RUG = dict(x0=12.30, x1=16.20, y0=0.90, y1=W - 0.90)
# the record wall on the back wall: walnut cubbies to 2.70 m, a console in the middle with Cumulus and the amplifier
REC = dict(y0=1.95, y1=W - 1.95, z1=2.70, cell=0.345, depth=0.40)
CONSOLE = dict(y0=W / 2 - 0.90, y1=W / 2 + 0.90, h=0.66, d=0.50)
BOOKS = dict(x0=12.40, x1=16.40, z1=2.40, depth=0.30)       # books floor to 2.4 m on the right wall (a diffuser)
LOUNGE_CEILING = dict(slat=0.045, pitch=0.090)   # walnut slats over absorber on the listening room's ceiling

# --- the products and their colours (the marks' colours; the acrylic tints are the product files') ------------------
COLOURS = {'ember': '#D2382F', 'dust': '#E5732A', 'acid': '#E9B320', 'poison': '#4F7F3A',
           'ice': '#4A90C8', 'haze': '#6C4BA3', 'fog': '#F6F8F8', 'smoke': '#34323A'}
FLAVOUR = {'ember': 'cloud-red', 'dust': 'cloud-orange', 'smoke': 'cloud-black', 'fog': 'birch-fog-clear'}
BACKBAR_PAIR = 'smoke'

# seats, counted for the plan
SEATS = {'bar': STOOLS, 'banquette': 2 * len(TABLES), 'window': 2, 'lounge': len(CHAIRS)}
CAPACITY = 40                    # Group B (under 50): no Place of Assembly permit; 29 seated, a few standing


def aim(x, y, tx, ty):
    """The rotate_z (degrees) that turns a product's front (-y at 0) from (x, y) toward (tx, ty)."""
    import math
    return math.degrees(math.atan2(tx - x, -(ty - y)))


def speakers():
    """Every Atmosphere speaker in the room: (role, colour, x, y, z, rotate_z)."""
    out = []
    for y in PAIR['y']:
        out.append(('lounge', PAIR['colour'], PAIR['x'], y, PLINTH['h'], round(aim(PAIR['x'], y, *LISTEN), 2)))
    for x0, w in NICHES:                              # facing the bar (-y), the back to the wall
        out.append(('backbar', BACKBAR_PAIR, x0 + w / 2, BACKBAR_Y + 0.235, NICHE_Z0, 0.0))
    return out


def stools():
    pitch = (BAR_X1 - BAR_X0) / STOOLS
    return [(BAR_X0 + pitch * (i + 0.5), STOOL_Y) for i in range(STOOLS)]


def candle_spots():
    """Each candle (x, y, z of its foot): on the banquette's other tables, the window table, the bar, a lounge table."""
    zt = BAR_TOP_Z + TOP_T
    out = [(cx + 0.14, TABLE['y'] - 0.12, TABLE['h']) for cx in TABLES[::2]]
    out += [(WINDOW_TABLE[0] + 0.1, WINDOW_TABLE[1] - 0.12, TABLE['h'])]
    out += [(x, BAR_FRONT - 0.10, zt) for x in (4.1, 6.3, 8.6)]
    out += [(SIDE_TABLES[0][0] + 0.06, SIDE_TABLES[0][1] + 0.08, 0.50)]
    return out
