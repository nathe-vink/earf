"""Planet EARF, round 42: the pop-up. A 3 to 6 month listening room and shop in a vacant downtown storefront, the
bridge to the full house (plan42.py). The coordinator, 31 October 2026: "Treat it as the bridge to the full bar."

The same frame as plan42: metres, x into the room from the shopfront glass, y across from the right-hand wall, z up.
A typical downtown storefront: 25 x 50 ft (1,250 sq ft), 13 ft ceiling, one accessible WC at the back, a rear door.
Everything is portable or leaves no trace: felt drapes on ceiling track, rented furniture, a catered bar, the house's
own products. The fit-out is for a short licence, not a lease.
"""
import math

FT = 0.3048
W = 25 * FT                       # 7.62
L = 50 * FT                       # 15.24
CEIL = 13 * FT
DOOR = dict(y0=5.90, w=0.915)     # the shop door, in the glass line, on the left
GLASS = (0.0, 5.75)

# --- the shop (front) ------------------------------------------------------------------------------------------------
SHOP_X1 = 6.40
WALL_R = dict(x0=0.80, x1=6.20, d=0.45)                         # shelves on the right wall: Core, Mantle, records
WALL_L = dict(x0=1.40, x1=5.60, d=0.45)                         # the left wall: Hemisphere shades on pegs, coins
WINDOW_PLINTH = dict(x=0.70, y=2.90, w=1.60, d=0.60, h=0.30)    # the window: one Tropos pair, facing the street
TROPOS = dict(w=0.560, d=0.428, h=1.293)
TABLE = dict(x0=2.60, x1=4.60, y0=3.30, y1=4.20)                 # the shop table, the till at its end
HEMI = [(2.2, 6.6), (3.4, 6.8), (4.6, 6.6)]                     # three hung low over the left wall

# --- the bar (catered: a licensed partner pours) ---------------------------------------------------------------------
BAR = dict(x0=6.80, x1=9.20, y0=W - 2.00, y1=W - 1.35, back=0.50)   # a 2.4 m portable bar; the bartender behind, a back table on the wall
STAND = [(7.4, 2.9), (8.7, 2.9), (7.4, 1.4), (8.7, 1.4)]        # standing tables (ledges), 600 round

# --- the listening room (behind felt) --------------------------------------------------------------------------------
LISTEN = dict(x0=9.70, x1=13.40, y0=0.0, y1=W)
DRAPE_OPEN = (0.95, 2.05)                                       # the opening in the drape, y (clear of the bar)
STACKS = [(12.80, 1.75), (12.80, 5.87)]
SEATS = [(x, y) for x in (10.35, 11.20) for y in (2.15, 3.05, 3.95, 4.85, 5.75)]   # 10 chairs, ganged and fixed
DECKS = dict(x0=9.90, x1=10.70, y0=W - 0.85, y1=W - 0.15)               # a table for the decks and the records, by the drape

# --- back of house (existing) ----------------------------------------------------------------------------------------
BACK = dict(x0=13.40, x1=L)
WC = dict(x0=13.40, x1=15.24, y0=0.0, y1=2.30)                  # the existing accessible WC
STORE = dict(x0=13.40, x1=15.24, y0=2.45, y1=5.20)             # stock, the caterer's ice and glass
REAR_DOOR_Y = 5.70


def occupancy():
    sq = 1 / (FT * FT)
    shop = SHOP_X1 * W * sq
    bar = (LISTEN['x0'] - SHOP_X1) * W * sq
    rows = [('Shop (mercantile, 60 gross)', round(shop), math.ceil(shop / 60)),
            ('Bar and standing tables (15 net, tables)', round(bar), math.ceil(bar * 0.85 / 15)),
            ('Listening room (10 fixed seats)', round((LISTEN['x1'] - LISTEN['x0']) * W * sq), len(SEATS)),
            ('Back of house (storage, 300 gross)', round((BACK['x1'] - BACK['x0']) * W * sq), 1)]
    return rows, sum(r[2] for r in rows)


if __name__ == '__main__':
    print(occupancy(), round(W * L / (FT * FT)))
