"""Planet EARF's plan: every dimension of the room in one frame, read by the model (studio/engine/kit_ext/planet_room.py),
the shots (shots.py) and the drawings (drawings.py). Nothing else holds a number for the room.

The frame: metres, z up, the floor at z = 0. The shell's inside faces are x = 0 (the side street, with the door) to
x = L (the back wall, the record wall), and y = 0 (the long street, with the window) to y = D (the party wall, the
back-bar). Everything here is a working assumption of the brief (BRIEF.md), made for the owner to overturn.
"""

FT = 0.3048

# --- the shell: a Hayes Valley corner storefront, 30 x 60 ft, 14 ft to the slab, concrete ------------------------------
L = 60 * FT                      # 18.288 along the long street
D = 30 * FT                      # 9.144 deep
SLAB = 14 * FT                   # 4.267 to the underside of the slab
WALL_T = 0.30                    # the concrete walls
MEMBRANE = 3.70                  # the stretched acoustic membrane's face (a 0.57 m plenum above it for absorber and LEDs)
MEMBRANE_GAP = 0.25              # its shadow gap from the walls

# the long street window (one, on y = 0) and the plain door (on the side street, x = 0)
WINDOW = dict(x0=1.20, x1=10.40, sill=0.45, head=3.35, mullions=[4.27, 7.34], frame=0.06)
DOOR = dict(y0=2.95, y1=4.00, h=2.40)
NEON = dict(y=3.475, z=2.78, w=0.56)            # the one small EARF neon sign, over the door outside

# --- the bar (along the party wall) ---------------------------------------------------------------------------------
BAR_X0 = 1.95                    # the bar front's west end
PANEL_W = 1.05                   # eight panels in spectrum order: 8.4 m
PANELS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
BAR_X1 = BAR_X0 + PANEL_W * len(PANELS)
BAR_FRONT = 6.90                 # the panels' outer face (y)
PANEL_T = 0.020                  # 20 mm cast acrylic
LINER_GAP = 0.004                # the white liner just behind the panel
CAVITY = 0.075                   # the LED cavity behind the liner (75 mm, LED pitch 75 mm: no hot spots)
KICK = 0.10                      # the toe-kick recess under the panels
KICK_SET = 0.08                  # how far it is set back
BAR_TOP_Z = 1.07                 # 42 in bar height
TOP_T = 0.04                     # 40 mm honed basalt
TOP_OVER = 0.26                  # the top's overhang on the guests' side
BAR_DEPTH = 0.66                 # front face to the bartender's side
FOOTRAIL = dict(z=0.22, d=0.05, off=0.20)        # a bronze footrail, 50 mm, 200 mm proud of the panels
STOOLS = 12                      # at 0.70 m pitch
STOOL_Y = BAR_FRONT - 0.48

# the back-bar against the party wall: a base cabinet, shelves above, two tall niches for the Fog pair
BACKBAR_D = 0.46
BACKBAR_Y = D - BACKBAR_D        # its front face
BASE_H = 0.92                    # the base cabinet (the working counter)
SHELVES_Z = [1.32, 1.72, 2.12, 2.52, 2.92]       # shelf tops above the counter: 10 mm edge-lit light-guide acrylic
SHELF_T = 0.010
WORKING_SHELVES = 2              # the lowest two warm white (labels read); the rest tinted for display
SHELF_TOP_Z = 3.30               # the back-bar's head
NICHES = [(4.155, 0.74), (7.305, 0.74)]         # (x0, width) of the two Fog niches: bays 3 and 6, 3.15 m apart (round 6)
NICHE_Z0 = 0.45                  # the niche's floor: the Fog horns at a seated guest's eye (about 1.5 m on a bar stool)
NICHE_H = 1.45

# --- the booths (along the window) ----------------------------------------------------------------------------------
BOOTHS = [(1.90 + 2.05 * i) for i in range(4)]   # each booth's x0: two benches across a table, 2.0 m
BOOTH_LEN = 2.00
BOOTH_DEPTH = 1.55               # from the window wall's liner (y)
BENCH_D = 0.56
BENCH_SEAT = 0.46
BENCH_BACK = 1.05
TABLE = dict(w=0.70, d=1.20, h=0.74)

# --- the listening lounge -------------------------------------------------------------------------------------------
SCREENS = False                  # dropped after round 2: they hid the Ember pair and read as boxes (README)
SCREEN_X = 11.10                 # the thermoformed Fog screens between the bar and the lounge
SCREEN_OPEN = (3.10, 6.10)       # the opening in them (y)
SCREEN_H = 1.35                  # chest high: the lounge reads from the bar, its talk does not
LOUNGE_X0 = SCREEN_X
# the two Atmosphere pairs, one in each corner of the lounge (Brilliant Corners' plan), on low Smoke plinths
PLINTH = dict(w=0.72, d=0.62, h=0.12)
CORNER_OFF = 0.62                # a speaker's centre from each wall of its corner
PAIRS = {
    'front': {'colour': 'ember', 'x': LOUNGE_X0 + 0.55 + CORNER_OFF},   # facing the record wall, backs to the screens
    'back': {'colour': 'ice', 'x': L - CORNER_OFF - 0.10},               # either side of the record wall, facing the bar
}
# the low chairs: (x, y, facing deg); 12 in the lounge, in two rows facing the record wall, plus the side pair
CHAIRS = [(13.30, 2.00, 0), (13.30, 3.30, 0), (13.30, 5.85, 0), (13.30, 7.15, 0),
          (15.00, 3.55, 0), (15.00, 5.60, 0), (14.15, 2.75, 0), (14.15, 6.39, 0),
          (14.20, 0.95, 90), (14.20, 8.19, -90)]      # two by the Ice pair taken out: they stood in front of it
SIDE_TABLES = [(14.15, D / 2 - 0.57), (14.15, D / 2 + 0.58)]     # off the aisle (door-r4: one sat on the axis)
# the complementary wash behind each pair (research, move 11: Holl's St Ignatius): Dust behind Ice, Ice behind Ember
WASH = {'front': 'ice', 'back': 'dust'}

# the tinted slats over dark absorber: on the lounge's street wall (y = 0) only, so no two acrylic walls face
SLATS = dict(x0=LOUNGE_X0 + 0.15, x1=L - 1.45, z0=0.30, z1=3.30, w=0.075, pitch=0.150, t=0.012, gap=0.075,
             colour='haze')
ABSORBER_T = 0.10                # the absorber behind them (and the plain dark absorber on the opposite wall)

# --- the record wall, the DJ desk and Cumulus (on the back wall, x = L) ---------------------------------------------
REC_Y0, REC_Y1 = 1.55, D - 1.55  # between the back pair
REC_CELL = 0.345                 # a 12 in LP's cubby
REC_Z1 = MEMBRANE
REC_DEPTH = (0.30, 0.55)         # uneven depths: the diffuser
DJ = dict(y0=D / 2 - 1.05, y1=D / 2 + 1.05, desk_z=0.94, recess_z=2.05, desk_d=0.75)   # set into the record wall

# --- the eight colours (the marks' colours; the acrylic tints are the product files') ----------------------------------
COLOURS = {'ember': '#D2382F', 'dust': '#E5732A', 'acid': '#E9B320', 'poison': '#4F7F3A',
           'ice': '#4A90C8', 'haze': '#6C4BA3', 'fog': '#F6F8F8', 'smoke': '#34323A'}
FLAVOUR = {'ember': 'cloud-red', 'dust': 'cloud-orange', 'acid': 'cloud-amber', 'poison': 'eucalyptus-y2k-green',
           'ice': 'cloud-blue', 'haze': 'cloud-violet', 'fog': 'birch-fog-clear', 'smoke': 'cloud-black'}

# the colour clock: the membrane's two colours at each hour (graded along the room), Turrell's slow sequence
CLOCK = {
    'opening': ('fog', 'ice'),       # 17:00
    'sunset': ('acid', 'dust'),      # 19:30
    'late': ('ember', 'haze'),       # 22:30
    'last': ('smoke', 'smoke'),      # 01:45, last call
}

# seats, counted for the plan
SEATS = {'bar': STOOLS, 'booths': 4 * 4, 'lounge': len(CHAIRS)}
CAPACITY = 49                    # Group B: no Place of Assembly permit


def aim(x, y, tx, ty):
    """The rotate_z (degrees) that turns a product's front (-y at 0) from (x, y) toward (tx, ty)."""
    import math
    return math.degrees(math.atan2(tx - x, -(ty - y)))


LISTEN = (14.20, D / 2)          # the lounge's listening seat the corner pairs aim at


def speakers():
    """Every Atmosphere speaker in the room: (role, colour, x, y, z, rotate_z)."""
    out = []
    for role, pr in PAIRS.items():
        for y in (CORNER_OFF, D - CORNER_OFF):
            out.append((role, pr['colour'], pr['x'], y, PLINTH['h'], round(aim(pr['x'], y, *LISTEN), 2)))
    for x0, w in NICHES:                                 # the Fog pair in the back-bar, facing the bar
        out.append(('backbar', 'fog', x0 + w / 2, BACKBAR_Y + 0.235, NICHE_Z0, 0.0))
    return out


def stools():
    return [(BAR_X0 + PANEL_W * len(PANELS) / STOOLS * (i + 0.5), STOOL_Y) for i in range(STOOLS)]


def bar_pendants():
    """Bell pendants over the bar (x), six at 1.4 m."""
    return [BAR_X0 + 0.7 + 1.4 * i for i in range(6)]
