"""Planet EARF, round 42: the house drawn to scale. A 35 x 80 ft ground floor (2,800 sq ft inside the walls), the
whole bar on one level: the shop and the window lounge at the street, the bar room, the selector's booth in a record
wall, the listening room behind it, back of house down the right-hand side. Every dimension is a proposal until the
owner signs it; the drawings (drawings42.py), the axonometric and the numbers read their geometry from here.

The frame is the earlier rounds' frame: metres, x into the room from the shopfront glass (x = 0) to the back wall
(x = L); y across, from the right-hand party wall (y = 0, seen from the door) to the left-hand one (y = W); z up from
the finished floor. Walls are drawn outside the clear box [0, L] x [0, W].

Why this shell: 35 ft is a lot and a half of San Francisco's 25 ft grain, common where a corner building or an old
garage or workshop has become a shop (SoMa, Dogpatch, the Mission's northeast); 80 ft leaves a rear yard on a 100 ft
lot. 15 ft 9 in to the joists is that kind of building's ceiling, which the speakers and the record wall want.
"""
import math

FT = 0.3048
IN = 0.0254

# --- the shell ------------------------------------------------------------------------------------------------------
W = 35 * FT                     # 10.668, clear between the party walls
L = 80 * FT                     # 24.384, the shopfront's glass line to the back wall's face
WALL = 0.30                     # existing party and back walls (concrete or brick, furred)
JOISTS = 4.80                   # underside of the floor or roof above (15'-9")
BEAM_D = 0.30                   # reclaimed fir beams across the room, 12 ft apart
BEAM_W = 0.20
BEAMS = [round(12 * FT * i, 3) for i in range(1, 7)]           # x of each beam's centre line: 3.66 ... 21.95
BEAM_Z = JOISTS - BEAM_D        # 4.50, the beams' underside (14'-9")
LISTEN_CEIL = 12 * FT           # 3.658: the listening room's own isolated ceiling (a room within the room)
BOH_CEIL = 9 * FT               # 2.743: back of house, gypsum, ducts above

# --- the shopfront (x = 0) ------------------------------------------------------------------------------------------
GLASS = (0.0, 7.40)             # y-extent of the display glass, on its 0.30 bulkhead
ALCOVE = dict(y0=7.55, y1=9.95, depth=0.90)                    # the recessed entry: outer door at x = depth
VEST = dict(x0=0.90, x1=3.35, y0=7.55, y1=9.95)                # the sound-lock vestibule, two doors in series
DOOR_W = 36 * IN                # every door 3'-0" leaf, 32" clear
OUTER_DOOR_Y = 8.30             # the outer door's hinge-side jamb (y); it swings out into the alcove
INNER_DOOR_Y = 8.30             # the inner door, in the vestibule's back face (x = VEST x1), swings toward the street

# --- 1. the front room: the shop wall, the shop table, the window lounge --------------------------------------------
FRONT_X1 = 7.40
SHOP_WALL = dict(x0=0.90, x1=7.20, d=0.50)                     # along the right-hand wall (y 0 to d), floor to 3.0
SHOP_BAYS = [  # (x0, x1, what): every piece in the room is on sale; the wall is where it waits
    (0.90, 2.45, 'Tropos'),       # a pair on low plinths in front of the bay, playing
    (2.45, 4.00, 'Hemisphere'),   # three hung low, the eight shades on pegs
    (4.00, 5.55, 'Core'),         # the eight on a stepped shelf; coins and the desk globe
    (5.55, 7.20, 'Mantle'),       # on its own plinth; the records for sale beneath
]
SHOP_PLINTHS = [(1.20, 0.80, 'Tropos'), (2.15, 0.80, 'Tropos'), (6.35, 0.85, 'Mantle')]   # (x, y, what): centres
SHOP_TABLE = dict(x0=2.60, x1=5.00, y0=2.25, y1=3.15, h=0.90)  # a long display table, the till at its end
LOUNGE = [(1.75, 4.55), (1.75, 6.35)]                          # low tables by the glass, two chairs each
LOUNGE_CHAIR = dict(w=0.78, d=0.80, gap=0.72)                  # chair centres at table y +/- gap
HOST = dict(x0=3.75, x1=4.45, y0=6.95, y1=7.45)                # the host stand: the coin bowl, the list

# --- 2. the bar room ------------------------------------------------------------------------------------------------
BAR_ROOM = (FRONT_X1, 16.00)
BACKBAR = dict(x0=7.60, x1=14.40, y0=W - 0.60, y1=W, h=0.92)   # coolers, ice, the glasswasher; shelves above
AISLE = 0.95                                                   # the bartenders' aisle
COUNTER = dict(x0=7.90, x1=14.20, y_work=W - 0.60 - AISLE, d=0.68, top_over=0.25, top_z=1.07)
COUNTER['y0'] = round(COUNTER['y_work'] - COUNTER['d'], 3)     # 8.438, the body's public face
COUNTER['edge'] = round(COUNTER['y0'] - COUNTER['top_over'], 3)  # 8.188, the top's front edge
LOW_END = dict(x0=7.90, x1=9.50, top_z=0.864)                  # CBC 11B-902.3: 60 in at 34 in, two seats at it
STOOL_Y = 7.86
STOOLS = [round(9.95 + 0.60 * i, 3) for i in range(8)]         # eight counter chairs at 1.07
LOW_SEATS = [8.35, 9.05]                                       # two chairs at the low end
SINKS = [(8.90, 'hand'), (10.75, '3-comp'), (12.55, 'dump'), (13.70, 'hand')]   # in the underbar (x centre)
BAR_FIXTURES = [(7.60, 8.30, 'ice'), (8.30, 9.20, 'glasswasher'), (9.20, 12.40, 'reach-ins'), (12.40, 13.10, 'keg'),
                (13.10, 14.40, 'reach-ins')]                    # under the back bar

BANQ = dict(x0=7.70, x1=15.30, y0=0.0, y1=0.70, seat=0.45, back=1.10)   # a built-in banquette along the right wall
BANQ_TABLES = [round(8.40 + 1.25 * i, 3) for i in range(6)]    # two-tops, 0.60 x 0.75, a chair opposite each
BANQ_TABLE = dict(w=0.75, d=0.60, y0=1.12, h=0.74)
BANQ_CHAIR_Y = 2.12
COMMUNAL = dict(x0=9.60, x1=13.20, y0=4.15, y1=5.15, h=0.74)   # under Mother EARF
COMMUNAL_CHAIRS = [round(9.90 + 0.60 * i, 3) for i in range(6)]
COMMUNAL_CHAIR_Y = (3.62, 5.68)
MOTHER = dict(x=11.40, y=4.65, d=1.25, z=2.60)                 # the globe's centre; its spot on the table

# --- 3. the selector's booth and the record wall --------------------------------------------------------------------
PARTITION = dict(x0=16.00, x1=16.30, y0=4.30, y1=W)            # the listening room's front wall: double stud, decoupled
RECORD_WALL = dict(x0=15.64, x1=16.00, y0=5.90, y1=W, z1=4.30, cell=0.33)   # cubbies to 14 ft, a library ladder
BOOTH = dict(x0=14.40, x1=15.64, y0=7.70, y1=W, desk=(14.40, 15.00), h=0.95)   # the decks face the room
LISTEN_DOOR1_Y = 4.75           # in the partition; the lobby behind it
LOBBY = dict(x0=16.30, x1=17.75, y0=4.60, y1=6.30)
LISTEN_DOOR2_Y = 4.95           # in the lobby's far face (x = LOBBY x1)

# --- 4. the listening room ------------------------------------------------------------------------------------------
LISTEN = dict(x0=16.30, x1=L, y0=4.60, y1=W)
TROPOS = dict(w=0.560, d=0.428, h=1.293, plinth=0.40)          # the speaker's footprint and height; its plinth
STACKS = [(23.30, 5.85), (23.30, 9.40)]                        # each Tropos's centre on its plinth
SWEET = (round(23.30 - 3.55 * math.sqrt(3) / 2, 2), 7.625)     # the equilateral seat: 20.23, 7.63
ALTAR = dict(x0=L - 0.45, x1=L, y0=6.65, y1=8.60, z1=2.60)     # an end-grain niche between the stacks
TUBS = [(20.30, 6.70), (20.30, 7.63), (20.30, 8.56),
        (19.05, 6.15), (19.05, 7.10), (19.05, 8.15), (19.05, 9.10),
        (17.75, 6.95), (17.75, 7.90), (17.75, 8.85), (17.75, 9.80)]
TUB_R = 0.40
SIDE_TABLES = [(20.30, 9.35), (19.05, 5.45), (19.05, 9.85), (18.40, 6.45)]
PANELS_L = [(17.0, 22.6)]       # absorber over the left wall (fabric in steel frames), x-extent
DIFFUSER = (L - 0.12, 4.60, W)  # the back wall around the altar: a slotted diffuser

# --- 5. back of house (y 0 to 4.30, x 16.0 to L) --------------------------------------------------------------------
BOH = dict(x0=16.00, x1=L, y0=0.0, y1=3.00)
CORRIDOR = dict(x0=16.00, x1=L, y0=3.12, y1=4.30)              # 46 in clear: exit access from the bar room
REAR_EXIT_Y = 3.25              # the rear exit door's jamb, in the back wall (to the yard and the side passage)
ROOMS = [(16.00, 17.90, 'All-gender WC 1'), (17.90, 19.80, 'All-gender WC 2'), (19.80, 21.70, 'All-gender WC 3'),
         (21.70, L, 'Stock, office, mop sink, panels')]
WC = dict(lav=0.50, wc=0.45)    # a lavatory and a water closet in each; 60 in turning circle

# --- what's on the ceiling (the RCP) --------------------------------------------------------------------------------
HEMI_COUNTER = [round(8.70 + 1.00 * i, 3) for i in range(6)]   # Hemisphere over the counter, 26 in over the top
HEMI_COUNTER_Y = 8.70
HEMI_SHOP = [(3.00, 0.95), (3.25, 1.45), (3.55, 1.00)]         # three hung low over the Hemisphere bay
HEMI_LOUNGE = [(1.75, 4.55), (1.75, 6.35)]                     # one over each lounge table
SPOTS = ([(x + 0.0, 1.45) for x in BANQ_TABLES] + [(10.4, 4.65), (12.4, 4.65)] + [(x, 0.30) for x in (1.70, 4.80, 6.40)]
         + [(22.4, 5.85), (22.4, 9.40), (22.0, 7.63)] + [(5.20, 9.10), (3.20, 4.20)])
SPRINKLER_GRID = 3.0            # schematic, at most 130 sq ft per head (light hazard): by the fire protection contractor

CORE_ON = (  # Core on every table and side table (x, y)
    [(x + 0.18, 1.30) for x in BANQ_TABLES] + [(10.3, 4.65), (11.4, 4.40), (12.5, 4.65)] + list(LOUNGE)
    + [(x, y) for x, y in SIDE_TABLES])


def areas():
    """The zones' floor areas (m2) for the occupant load: clear areas less what fixed work and furniture take."""
    A = {}
    vest = (VEST['x1'] - VEST['x0']) * (VEST['y1'] - VEST['y0'])
    front = FRONT_X1 * W - vest - (W - VEST['y1']) * VEST['x1']   # less the pier beside the alcove
    shop = (SHOP_WALL['x1'] - SHOP_WALL['x0']) * 3.40            # the shop's strip, wall to the table's far side
    A['Shop (mercantile)'] = round(shop, 1)
    A['Window lounge (tables and chairs)'] = round(front - shop, 1)
    bar_pub = (BAR_ROOM[1] - BAR_ROOM[0]) * COUNTER['edge'] - (BOOTH['x1'] - BOOTH['x0']) * (COUNTER['edge'] - BOOTH['y0'])
    banq = (BANQ['x1'] - BANQ['x0']) * (BANQ['y1'] - BANQ['y0'])
    A['Bar room (tables and chairs)'] = round(bar_pub - banq, 1)
    A['Banquette (fixed seating)'] = round(banq, 1)
    A['Behind the bar and the booth (commercial kitchen)'] = round(
        (BACKBAR['x1'] - COUNTER['x0']) * (W - COUNTER['y0']) + (BOOTH['x1'] - BOOTH['x0']) * (W - BOOTH['y0']), 1)
    A['Listening room (tables and chairs)'] = round((LISTEN['x1'] - LISTEN['x0']) * (LISTEN['y1'] - LISTEN['y0'])
                                                    - (LOBBY['x1'] - LOBBY['x0']) * (LOBBY['y1'] - LOBBY['y0'])
                                                    - 2 * (TROPOS['w'] + 0.3) * (TROPOS['d'] + 0.3)
                                                    - (ALTAR['y1'] - ALTAR['y0']) * 0.45, 1)
    A['Stock and office'] = round((ROOMS[-1][1] - ROOMS[-1][0]) * (BOH['y1'] - BOH['y0']), 1)
    return A


SQFT = 1 / (FT * FT)
# CBC 2022 Table 1004.5, sq ft per occupant (net unless gross): the function of each zone
LOAD_FACTOR = {'Shop (mercantile)': (60, 'gross'), 'Window lounge (tables and chairs)': (15, 'net'),
               'Bar room (tables and chairs)': (15, 'net'), 'Banquette (fixed seating)': (None, 'seats, 24 in each'),
               'Behind the bar and the booth (commercial kitchen)': (200, 'gross'),
               'Listening room (tables and chairs)': (15, 'net'), 'Stock and office': (150, 'gross')}


def occupant_load():
    rows, total = [], 0
    for k, a in areas().items():
        f, how = LOAD_FACTOR[k]
        sf = a * SQFT
        n = int(math.floor((BANQ['x1'] - BANQ['x0']) / (24 * IN))) if f is None else int(math.ceil(sf / f))
        rows.append((k, round(sf), f, how, n)); total += n
    return rows, total


def occupant_load_option():
    """The option to stay at 99 or fewer (no sprinklers required): the front room counted as the shop it is (mercantile,
    60 gross), the listening room's chairs fixed to the floor (counted by seat)."""
    rows, total = [], 0
    front = FRONT_X1 * W * SQFT
    for k, sf, f, how, n in occupant_load()[0]:
        if k.startswith('Shop'):
            n = int(math.ceil(front / 60)); sf = round(front); how = 'gross: the whole front room as the shop'
        elif k.startswith('Window'):
            continue
        elif k.startswith('Listening'):
            n = len(TUBS); f = None; how = 'fixed seats'
        rows.append((k, sf, f, how, n)); total += n
    return rows, total


def seats():
    return {'Window lounge': 2 * len(LOUNGE),
            'Counter (8 high, 2 at the low end)': len(STOOLS) + len(LOW_SEATS),
            'Banquette and its tables': 2 * len(BANQ_TABLES) + len(BANQ_TABLES),
            'Communal table': 2 * len(COMMUNAL_CHAIRS),
            'Listening room': len(TUBS)}


if __name__ == '__main__':
    for k, v in areas().items():
        print(f'{k:52s} {v:6.1f} m2  {v * SQFT:6.0f} sf')
    rows, t = occupant_load()
    for r in rows:
        print(r)
    print('occupant load', t)
    s = seats(); print(s, sum(s.values()))
    print('gross', round(W * L * SQFT), 'sf', 'sweet', SWEET)
