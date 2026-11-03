"""Planet EARF, round 44: the lantern. The bar's architecture in one frame, read by the drawings, the model and the
numbers. Every dimension is a proposal for the owner and the design team (an architect, an acoustician, a structural
engineer); nothing here has been reviewed by any of them.

    python3 spinoffs/barkhorn/planet/r44/plan44.py            # areas, occupant load, acoustics, cost

The shell is a typical San Francisco ground-floor storefront, not a particular listing: 25 ft wide inside the party
walls, 80 ft deep from the shopfront glass to the back wall, 14 ft to the underside of a wood-joisted floor with flats
above, a slab on grade, a glazed front and a rear door to a yard. (The 25 ft lot is the city's grain; 80 ft leaves a
rear yard on a 100 ft lot.) Of the round 43 shortlist, 311 Grant Ave (about 22 x 53 ft) and 564 Market (about 25 x
74 ft) are the nearest; the scheme is drawn generic so that it can be fitted to whichever shell is leased.

The frame (as rounds 42 and 43): metres; x into the shop from the glass (x = 0) to the back wall (x = L); y across,
from the right-hand party wall seen from the door (y = 0) to the left-hand one (y = W); z up from the finished floor.

The idea (CONCEPTS.md, picked by both critics): the listening room's isolation, a room within the room, is the
building's one object. A freestanding oak box on its own floated floor sits at the end of the bar room, its front a
slotted oak baffle, a band of lit tinted acrylic fins along its top between the leaves, so the street sees a lantern at
the end of a long dark room. Borrowed: (b) the box is bolted and demountable, so it leaves with the lease; (a) a slotted
oak bass-trap wall at the back, with the accessible seat on the sweet spot; (c) acrylic-offcut terrazzo only as an
accent, on Mother EARF's plinth and the bar's die, where nothing wears it.
"""
import math

FT = 0.3048
IN = 0.0254

# --- the shell -------------------------------------------------------------------------------------------------------
W = 25 * FT                      # 7.620 clear between the party walls
L = 80 * FT                      # 24.384, glass line to the back wall
WALL = 0.30                      # existing party and back walls (brick or concrete)
JOISTS = 14 * FT                 # 4.267, underside of the joists of the floor above
CEIL = 13 * FT                   # 3.962, the resilient ceiling over the shop and the bar (a second line to the flats)
PLENUM = JOISTS - CEIL           # 0.305 for ducts, sprinkler mains, cable trays

# --- the street: the shopfront and the sound-lock entry -------------------------------------------------------------
BULKHEAD = 0.45                  # the glass sits on a 18 in bulkhead
GLASS = (1.70, W)                # the display glass's y-extent (the entry is at the right, y 0 to 1.70)
ENTRY = dict(x0=0.0, x1=0.90, y0=0.10, y1=1.60)       # the recessed entry alcove: outer door at x = 0.90
VEST = dict(x0=0.90, x1=3.20, y0=0.10, y1=1.62)       # two doors in series, 2.30 apart (48 in + a 36 in leaf, ADA 404.2.6)
DOOR = 36 * IN                   # every door a 3'-0" leaf, 32 in clear

# --- the axis: one straight accessible route from the front door to the rear exit, along the right-hand wall ---------
ROUTE_Y = (0.0, 1.62)            # 64 in clear down the building's length (ADA 403: 36 in; 60 in to pass and turn)

# --- 1. the shop (x 0 to 6.10, 20 ft) ------------------------------------------------------------------------------
SHOP_X1 = 6.10
SHOP_WALL = dict(x0=0.60, x1=6.00, y0=W - 0.45, y1=W, z1=3.20)   # oak shelves on the left wall, lit by the shelf edge
SHOP_TABLE = dict(x0=3.40, x1=5.40, y0=4.55, y1=5.45, h=0.90)    # oak and blackened steel, the till at its end;
                                                                  # off the room's axis, so the lantern is seen from the door
WINDOW_PLINTH = dict(x0=0.35, x1=1.35, y0=3.20, y1=6.80, h=0.45)  # the window's display, a long low plinth
THRESHOLD = dict(x0=3.20, x1=3.50, y0=0.0, y1=W)                  # the terrazzo threshold strip between street and room

# --- 2. the bar (x 6.10 to 13.70, 25 ft) ---------------------------------------------------------------------------
BAR_X = (SHOP_X1, 13.00)
BACKBAR = dict(x0=6.90, x1=12.80, y0=W - 0.60, y1=W, h=0.92)     # under-counter: reach-ins, keg, the speed rails
KIT_ALCOVE = dict(x0=6.10, x1=6.90, y0=W - 1.55, y1=W)            # the ice machine and the glasswasher, behind a
                                                                  # gasketed door at the shop end: 7 m from the lantern
AISLE = 0.95
COUNTER = dict(x0=7.20, x1=12.50, d=0.66, top_over=0.25, top_z=1.07)
COUNTER['y_work'] = round(W - 0.60 - AISLE, 3)                   # 6.070, the bartender's side of the counter body
COUNTER['y0'] = round(COUNTER['y_work'] - COUNTER['d'], 3)       # 5.410, the body's public face
COUNTER['edge'] = round(COUNTER['y0'] - COUNTER['top_over'], 3)  # 5.160, the top's front edge
LOW_END = dict(x0=7.20, x1=8.80, top_z=0.864)                    # CBC 11B-902.3: a 60 in run at 34 in, at the near end
STOOLS = [round(9.25 + 0.58 * i, 3) for i in range(6)]           # six counter stools at 1.07 m (42 in)
STOOL_Y = 4.62
LOW_SEATS = [7.65, 8.35]                                          # two chairs at the low end
BANQ = dict(x0=7.10, x1=11.20, y0=ROUTE_Y[1] + 0.0, y1=ROUTE_Y[1] + 0.62, seat=0.45, back=1.05)
BANQ_TABLES = [round(7.70 + 1.15 * i, 3) for i in range(4)]      # two-tops in front of the banquette
BANQ_TABLE = dict(w=0.70, d=0.60)
BANQ_CHAIR_DY = 1.45             # chair centres, from the route's edge
# the banquette backs onto the route: the route stays clear at 64 in, the banquette's back is its rail

# --- 3. the lantern (x 13.70 to 22.10) -----------------------------------------------------------------------------
LANT = dict(x0=13.00, x1=20.90, y0=ROUTE_Y[1], y1=W - 0.06)      # the box's outer face; a 60 mm gap to the party wall
LEAF = 0.30                      # each wall: oak skin 20 + fin cavity 60 + outer leaf (2 x 15.9 gypsum on 89 studs) +
                                 # 50 air + inner leaf (2 x 15.9 gypsum on 64 studs, 50 mineral wool) + 25 oak inner
LANT['h'] = 3.90                 # its outer height: a 60 mm shadow gap to the ceiling at 3.96
BAND = dict(z0=3.45, z1=3.90, fins=0.020, pitch=0.028)            # the lit acrylic fins, 20 mm on a 28 mm pitch,
                                                                  # in the outer cavity only (outside the seal)
BAFFLE_SLOTS = dict(w=0.012, pitch=0.072)                         # the front's slotted oak: 12 mm slots on 72 mm
INNER = dict(x0=LANT['x0'] + LEAF, x1=LANT['x1'] - LEAF, y0=LANT['y0'] + LEAF, y1=LANT['y1'] - LEAF)
INNER['h'] = 3.40                # floated floor (flush) to the lid's soffit
FLOAT = dict(depth=0.175, f0_hz=7.0)                              # the slab cut 175 mm under the box; a 100 mm concrete
                                                                  # slab on spring jack-up mounts at about 7 Hz
LID = 0.40                       # CLT 200 + 2 x 15.9 gypsum + 100 absorber + oak slats, spanning wall to wall
# the sound lock: a small oak porch on the bar's side of the box, outside the seal, so the room inside stays a whole
# rectangle. Door 1 from the route into the porch (swings in); door 2, the box's own acoustic door set through both
# leaves, from the porch into the room (swings in). The porch holds a 60 in turning circle (ADA 404.2.6, 304.3).
LOCK = dict(x0=LANT['x0'] - 1.60, x1=LANT['x0'], y0=ROUTE_Y[1], y1=ROUTE_Y[1] + 2.20)
LOCK_DOOR1 = dict(x=LOCK['x0'] + 0.25, y=LOCK['y0'])              # hinge; the leaf runs +x, in the porch's route face
LOCK_DOOR2 = dict(x=LANT['x0'], y=LOCK['y0'] + 0.45)              # hinge; the leaf runs +y, in the box's front
LOCK_PORCH = True
SELECTOR = dict(x0=INNER['x0'], x1=INNER['x0'] + 0.80, y0=INNER['y1'] - 2.20, y1=INNER['y1'], h=0.95)
TROPOS = dict(w=0.560, d=0.428, h=1.293, plinth=0.40)
SPREAD = 2.80                    # between the speakers' centres
_yc = (INNER['y0'] + INNER['y1']) / 2
STACK_X = INNER['x0'] + 2.20
STACKS = [(STACK_X, round(_yc - SPREAD / 2, 3)), (STACK_X, round(_yc + SPREAD / 2, 3))]
MOTHER = dict(x=round(INNER['x0'] + 1.30, 3), y=round(_yc, 3), d=1.25, plinth_h=0.40, plinth_d=0.80)
SWEET = (round(STACK_X + SPREAD * math.sqrt(3) / 2, 2), round(_yc, 3))   # the equilateral seat
TRAP = dict(x0=INNER['x1'] - 0.90, x1=INNER['x1'], h=INNER['h'])  # the slotted oak bass-trap wall: 900 mm deep
BENCH = dict(x0=TRAP['x0'] - 0.55, x1=TRAP['x0'], z=0.45)        # a bench built into the trap's face
# (no raised platform: the room is level throughout, so every seat is on the accessible route)
# the seats: the wheelchair space and its companion on the sweet spot (row 1, floor level); the rest loose
ROW1 = [(SWEET[0], SWEET[1] - 0.55, 'wheelchair'), (SWEET[0], SWEET[1] + 0.40, 'companion'),
        (SWEET[0] + 0.15, SWEET[1] - 1.55, 'chair'), (SWEET[0] + 0.15, SWEET[1] + 1.40, 'chair')]
ROW2 = [(SWEET[0] + 0.85, y, 'chair') for y in (INNER['y0'] + 0.70, _yc - 1.20, _yc - 0.40, _yc + 0.40, _yc + 1.20,
                                                       INNER['y1'] - 0.70)]
ROW3 = [(BENCH['x0'] + 0.30, y, 'bench') for y in [round(INNER['y0'] + 0.55 + 0.61 * i, 3) for i in range(8)]]
SEATS = ROW1 + ROW2 + ROW3
SIDE_SEATS = [(SWEET[0] - 1.05, INNER['y0'] + 0.45, 'chair'), (SWEET[0] - 1.05, INNER['y1'] - 0.45, 'chair')]
SEATS += SIDE_SEATS

# --- 4. the rear (x 20.90 to 24.38): a lobby off the route, three all-gender rooms, the rear exit -----------------
REAR_X = (LANT['x1'], L)
LOBBY = dict(x0=LANT['x1'], x1=LANT['x1'] + 1.25, y0=ROUTE_Y[1], y1=W)   # 49 in deep, off the route's end
WC_X = (LOBBY['x1'], L)          # 2.23 m deep: a 60 in circle, the WC 17 in off its side wall, the lavatory opposite
WCS = [dict(y0=ROUTE_Y[1] + 2.0 * i, y1=ROUTE_Y[1] + 2.0 * (i + 1), name=f'WC {i + 1}') for i in range(3)]
WCS[2]['urinal'] = True          # CPC Table 422.1 at a load of about 56: 3 water closets and 1 urinal (to confirm)
CEIL_REAR = 2.60                 # the rooms' ceiling; above it, a plant deck for the lantern's fan coil and the HRV
REAR_EXIT = dict(x=L, y0=0.25, y1=0.25 + DOOR)                     # at the route's end, to the yard


# --- numbers --------------------------------------------------------------------------------------------------------
def areas():
    a = {}
    a['gross'] = W * L
    a['shop'] = SHOP_X1 * W
    a['bar'] = (BAR_X[1] - BAR_X[0]) * W
    a['lantern_outer'] = (LANT['x1'] - LANT['x0']) * (LANT['y1'] - LANT['y0'])
    a['lantern_inner'] = (INNER['x1'] - INNER['x0']) * (INNER['y1'] - INNER['y0'])
    a['listening_net'] = a['lantern_inner']
    a['rear'] = (L - LANT['x1']) * W
    a['route_beside_lantern'] = (LANT['x1'] - LANT['x0']) * ROUTE_Y[1]
    return {k: round(v, 1) for k, v in a.items()}


def occupant_load():
    """CBC Table 1004.5 factors (net, except mercantile): the shop at 60 gross (mercantile, ground floor), the bar's
    standing area at 5 net, its seats counted as fixed (stools and banquette: one each), the listening room by its
    seats (fixed seating, 1004.6) plus the wheelchair space."""
    a = areas()
    shop = math.ceil(a['shop'] / (60 * 0.0929))
    seats_bar = len(STOOLS) + len(LOW_SEATS) + 2 * len(BANQ_TABLES) + len(BANQ_TABLES)   # stools, low end, banquette x2, chairs
    net = (BAR_X[1] - BAR_X[0]) * W - (BACKBAR['x1'] - BACKBAR['x0']) * (W - COUNTER['edge']) \
        - (KIT_ALCOVE['x1'] - KIT_ALCOVE['x0']) * (KIT_ALCOVE['y1'] - KIT_ALCOVE['y0']) \
        - (LOCK['x1'] - LOCK['x0']) * (LOCK['y1'] - LOCK['y0'])
    bar = math.ceil(net / (15 * 0.0929))                     # unconcentrated (tables and chairs): 15 sq ft net
    listen = len(SEATS)
    return dict(shop=shop, bar_net_m2=round(net, 1), bar=bar, bar_seats=seats_bar, listening=listen,
                total=shop + bar + listen)


def acoustics():
    """The listening room's reverberation by Sabine, the target by EBU Tech 3276 (Tm = 0.25 (V / 100)^(1/3) s, at mid
    frequencies), and its axial modes. Absorption coefficients are typical published values (marked as assumptions)."""
    lx = INNER['x1'] - INNER['x0']; ly = INNER['y1'] - INNER['y0']; h = INNER['h']
    V = lx * ly * h
    Tm = 0.25 * (V / 100.0) ** (1 / 3)
    walls = 2 * (lx + ly) * h
    floor = lx * ly
    # surfaces at 500 Hz / 125 Hz (assumed): oak slats over 50 mm wool (0.80/0.35) on 45% of the walls; plain oak
    # board on gypsum (0.10/0.20) elsewhere; the trap's slotted face (0.90/0.85, 900 mm deep); the lid's absorber
    # between slats (0.85/0.45) on 70% of the ceiling, oak 30% (0.10/0.20); the floor end-grain oak on the floated slab
    # (0.08/0.10) with a wool rug of 12 m2 (0.45/0.10); 24 people seated in upholstered chairs (0.45 m2 Sabine each at
    # 500 Hz, 0.25 at 125)
    trap_face = ly * h
    S = dict(
        walls_abs=(0.35 * (walls - trap_face), 0.80, 0.35),
        walls_hard=(0.65 * (walls - trap_face), 0.10, 0.20),
        trap=(trap_face, 0.90, 0.85),
        lid_abs=(0.70 * floor, 0.85, 0.45),
        lid_oak=(0.30 * floor, 0.10, 0.20),
        floor=(floor - 12.0, 0.08, 0.10),
        rug=(12.0, 0.45, 0.10),
    )
    A500 = sum(s * a5 for s, a5, a1 in S.values()) + 24 * 0.45
    A125 = sum(s * a1 for s, a5, a1 in S.values()) + 24 * 0.25
    c = 343.0
    modes = sorted({round(n * c / (2 * d), 1) for d in (lx, ly, h) for n in (1, 2, 3)})
    prop = dict(l_h=round(lx / h, 2), w_h=round(ly / h, 2), lo=round(1.1 * ly / h, 2), hi=round(4.5 * ly / h - 4, 2))
    return dict(V=round(V, 1), Tm=round(Tm, 2), tol=(round(Tm - 0.05, 2), round(Tm + 0.05, 2)), bs1116_ratio=prop,
                RT500=round(0.161 * V / A500, 2), RT125=round(0.161 * V / A125, 2),
                dims=(round(lx, 2), round(ly, 2), h), axial_modes_hz=[m for m in modes if m < 160])


COST = [  # (item, low, high, basis) in US dollars, 2026, San Francisco; estimates to be replaced by a contractor's
    ('Demolition, slab cut under the box (about 50 m2 at 175 mm), trenching for the rear rooms', 25_000, 45_000, 'est.'),
    ('The lantern: floated floor on spring mounts, double-leaf walls, the CLT lid, the porch, two acoustic door sets', 150_000, 260_000, 'est.'),
    ('The lantern\'s oak: the slotted baffle, inner slats, the bass-trap wall, the bench', 45_000, 80_000, 'est.'),
    ('The acrylic band: about 15 m of cast tinted fins, LED lines, drivers, hatch panels', 18_000, 35_000, 'est.'),
    ('Resilient ceiling over the shop and bar (about 120 m2), insulation, acoustic plaster', 35_000, 60_000, 'est.'),
    ('Shopfront: the sound-lock vestibule, new glass, the entry alcove', 30_000, 70_000, 'est.'),
    ('The bar: counter, back bar, the kit alcove, under-bar stainless', 70_000, 130_000, 'est.'),
    ('Shop and bar joinery: shelves, the shop table, the banquette', 45_000, 80_000, 'est.'),
    ('Floors: honed terrazzo in the bar and shop (about 105 m2), end-grain oak in the lantern', 35_000, 65_000, 'est.'),
    ('Three all-gender rooms (one with a urinal) and plumbing', 55_000, 90_000, 'est.'),
    ('HVAC: the bar\'s units and the lantern\'s own fan coil, silencers, lined ducts', 70_000, 130_000, 'est.'),
    ('Electrical, lighting, controls, the sound system\'s power', 55_000, 100_000, 'est.'),
    ('Fire: sprinklers (if required), alarm', 25_000, 60_000, 'est.'),
    ('Design fees: architect, acoustician, structural and MEP engineers, testing', 90_000, 150_000, 'est.'),
]


def cost():
    lo = sum(c[1] for c in COST); hi = sum(c[2] for c in COST)
    cont = (round(0.10 * lo), round(0.15 * hi))
    return dict(items=COST, subtotal=(lo, hi), contingency=cont, total=(lo + cont[0], hi + cont[1]),
                per_sqft=(round((lo + cont[0]) / (W * L / 0.0929)), round((hi + cont[1]) / (W * L / 0.0929))))


if __name__ == '__main__':
    print('areas m2:', areas())
    print('occupant load:', occupant_load())
    print('acoustics:', acoustics())
    print('sweet spot:', SWEET, 'stacks:', STACKS, 'mother:', MOTHER)
    c = cost()
    print('cost subtotal', c['subtotal'], 'contingency', c['contingency'], 'total', c['total'], '$/sf', c['per_sqft'])
    print('seats in the lantern:', len(SEATS))
