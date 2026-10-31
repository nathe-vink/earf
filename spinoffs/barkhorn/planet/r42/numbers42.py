"""Planet EARF, round 42: the numbers. Capex, opex, three revenue scenarios, the P&L, break-even and the financing,
for the house drawn in plan42.py (2,800 sq ft, 55 seats). Every input is here, marked by where it comes from:
[R] the research notes beside this file (research-market.md, research-sf-rules.md), with their sources;
[A] an assumption of this round, for the owner to overturn. Run it to print the tables NUMBERS.md quotes.

    python3 spinoffs/barkhorn/planet/r42/numbers42.py > /tmp/numbers.md
"""
import math

SQFT = 2800                       # plan42: 35 x 80 ft inside the walls
SEATS = 55
NIGHTS = 6 * 52                   # [A] Tuesday to Sunday, 5 pm to 1 am; the shop also open noon to 5, Wednesday to Sunday

# --- rent [R: asking $27 to $61/sq ft/yr base by neighbourhood; NNN about $12] -----------------------------------------
RENT = dict(base=45.0, nnn=12.0)  # [A] a mid-market ask in the target areas, plus pass-throughs

# --- capex: (low, base, high) ------------------------------------------------------------------------------------------
CAPEX = [
    # construction, per sq ft [R: Terrapin July 2026: second generation $125-250 nationally, Pacific Coast $375-650;
    # bar-forward $350-575]. Base is a second-generation bar or restaurant shell with the listening room built in.
    ('Construction: the fit-out, the room-in-room, sound isolation', (200 * SQFT, 300 * SQFT, 450 * SQFT), 'R'),
    ('Landlord improvement allowance (credit)', (-0 * SQFT, -30 * SQFT, -60 * SQFT), 'A'),
    ('Design, engineering, acoustician, permits and fees', (0.10, 0.13, 0.15), 'R'),       # a share of construction
    ('Bar equipment: ice, glasswasher, reach-ins, keg box, sinks', (40_000, 80_000, 120_000), 'R'),
    ('Millwork: the zinc counter, the record wall, the shop wall, the booth', (90_000, 140_000, 200_000), 'A'),
    ('Furniture: 55 seats, the banquette, the tables', (60_000, 95_000, 140_000), 'A'),
    ('Sound: three Tropos pairs at cost, amplifiers, decks, the booth', (45_000, 70_000, 110_000), 'A'),
    ('Light: 11 Hemisphere, 15 Core, Mother EARF at cost; spots and controls', (35_000, 50_000, 70_000), 'A'),
    ('Records: 3,000 to open', (18_000, 30_000, 45_000), 'A'),
    ('Type 48 licence, bought, with escrow and ABC fees', (75_000, 115_000, 165_000), 'R'),
    ('Legal, the PCN, the lease, entity and IP', (15_000, 25_000, 40_000), 'A'),
    ('Pre-opening: hiring, training, opening stock, launch', (50_000, 80_000, 120_000), 'A'),
    ('Deposits: rent (3 months), utilities', None, 'A'),                                  # from the rent
    ('Contingency: 10% of construction, millwork and furniture', (0.10, 0.10, 0.12), 'A'),
    ('Working capital: three months of fixed costs', None, 'A'),
]

# --- revenue scenarios (per year) --------------------------------------------------------------------------------------
SCEN = {
    #            guests/night, bar spend/guest, session fill, ticket, private hire, Tropos pairs, lamps, Mantles, small
    'Low':  dict(guests=60, spend=30.0, fill=0.45, ticket=20.0, hire=30_000, pairs=4, lamps=60, mantles=3, small=25_000,
                 pour=0.24, hours=230),
    'Base': dict(guests=90, spend=36.0, fill=0.70, ticket=22.0, hire=90_000, pairs=12, lamps=150, mantles=10, small=60_000,
                 pour=0.22, hours=270),
    'High': dict(guests=130, spend=40.0, fill=0.90, ticket=25.0, hire=200_000, pairs=25, lamps=300, mantles=20, small=110_000,
                 pour=0.20, hours=310),
}
SESSIONS = 2                      # [A] two ticketed sessions a night in the 11-seat listening room
LISTEN_SEATS = 11
PRICE = dict(pair=19_000, lamp=700, mantle=5_000)  # [R: README] Tropos pair; Hemisphere $795-895 and Core $545-645; Mantle about $5,000
SHOP_MARGIN = 0.55                # [A] gross margin to the house on EARF's own pieces, sold direct
CARD = 0.03                       # [A] card fees on all sales
SELECTOR = 175                    # [A] a selector's fee a night

# --- operating costs ---------------------------------------------------------------------------------------------------
WAGE = 22.0                       # [R] SF minimum $19.61 from July 2026; [A] an average hourly rate a little above it
SHOP_HOURS = 30 * 52
SALARIES = 95_000 + 75_000        # [A] a general manager and a bar manager
BURDEN = 0.22                     # [A] payroll taxes, workers' comp, HCSO ($2.74 to $4.11/h [R]), sick leave
FIXED = [
    ('Utilities', 36_000), ('Insurance, liquor liability included', 26_000), ('Music licences (ASCAP, BMI, SESAC, GMR)', 5_000),
    ('POS, booking, software', 9_000), ('Repairs, maintenance, the system', 24_000), ('Marketing and the site', 36_000),
    ('Records and needles', 12_000), ('Cleaning, linen, supplies, glass', 26_000), ('Accounting and legal', 18_000),
    ('Licences and permits, renewals (ABC, POE, DPH, POA)', 6_000),
]

# --- financing [R: SBA 7(a) up to $5M, capped at prime 7.00% + 3% = 10.0% over $350k; 10% equity floor] --------------
SBA_RATE = 0.10
SBA_YEARS = 10


def capex(i):
    rows, cons, mill = [], 0, 0
    rent_m = (RENT['base'] + RENT['nnn']) * SQFT / 12
    fixed = fixed_costs(SCEN['Base']) / 12
    for name, v, src in CAPEX:
        if name.startswith('Construction'):
            val = v[i]; cons = val
        elif name.startswith('Design'):
            val = v[i] * cons
        elif name.startswith('Deposits'):
            val = 3 * rent_m + 6_000
        elif name.startswith('Contingency'):
            val = v[i] * (cons + mill)
        elif name.startswith('Working'):
            val = 3 * fixed
        else:
            val = v[i]
        if name.startswith('Millwork') or name.startswith('Furniture'):
            mill += val
        rows.append((name, round(val, -3), src))
    return rows


def labour(s):
    hourly = s['hours'] * 52 * WAGE + SHOP_HOURS * 24.0
    return (hourly + SALARIES) * (1 + BURDEN)


def fixed_costs(s):
    rent = (RENT['base'] + RENT['nnn']) * SQFT
    return rent + labour(s) + sum(v for _, v in FIXED) + SELECTOR * NIGHTS


def pnl(s):
    bar = s['guests'] * s['spend'] * NIGHTS
    door = LISTEN_SEATS * SESSIONS * NIGHTS * s['fill'] * s['ticket'] + s['hire']
    shop = s['pairs'] * PRICE['pair'] + s['lamps'] * PRICE['lamp'] + s['mantles'] * PRICE['mantle'] + s['small']
    rev = bar + door + shop
    cogs = bar * s['pour'] + shop * (1 - SHOP_MARGIN) + 0.15 * s['hire']
    gross = rev - cogs
    lab = labour(s)
    rent = (RENT['base'] + RENT['nnn']) * SQFT
    other = sum(v for _, v in FIXED) + SELECTOR * NIGHTS + CARD * rev
    ebitda = gross - lab - rent - other
    return dict(bar=bar, door=door, shop=shop, rev=rev, cogs=cogs, gross=gross, labour=lab, rent=rent, other=other,
                ebitda=ebitda)


def payment(P, r=SBA_RATE, n=SBA_YEARS):
    m = r / 12
    return P * m / (1 - (1 + m) ** (-12 * n)) * 12


def money(v):
    return f'-${-v:,.0f}' if v < 0 else f'${v:,.0f}'


def main():
    out = []
    p = out.append
    tot = []
    p('### Capex\n')
    p('| Item | Low | Base | High | Basis |'); p('|---|---:|---:|---:|---|')
    cols = [capex(i) for i in range(3)]
    for k in range(len(cols[0])):
        name, _, src = cols[0][k]
        p(f'| {name} | {money(cols[0][k][1])} | {money(cols[1][k][1])} | {money(cols[2][k][1])} | {"research" if src == "R" else "assumption"} |')
    tot = [sum(r[1] for r in c) for c in cols]
    p(f'| **Total to open** | **{money(tot[0])}** | **{money(tot[1])}** | **{money(tot[2])}** | |')
    p(f'| Per sq ft | ${tot[0] / SQFT:,.0f} | ${tot[1] / SQFT:,.0f} | ${tot[2] / SQFT:,.0f} | |')
    p('')
    p('### Revenue and P&L, a year at run-rate\n')
    R = {k: pnl(v) for k, v in SCEN.items()}
    lines = [('Bar: drinks and snacks', 'bar'), ('Door and programming: sessions, private hire', 'door'),
             ('Shop: EARF pieces sold in the room', 'shop'), ('**Revenue**', 'rev'), ('Cost of goods', 'cogs'),
             ('**Gross profit**', 'gross'), ('Labour, burdened', 'labour'), ('Rent and NNN', 'rent'),
             ('Other operating, card fees, selectors', 'other'), ('**EBITDA**', 'ebitda')]
    p('| | Low | Base | High |'); p('|---|---:|---:|---:|')
    for name, k in lines:
        neg = k in ('cogs', 'labour', 'rent', 'other')
        vals = [(-1 if neg else 1) * R[s][k] for s in SCEN]
        p(f'| {name} | ' + ' | '.join(money(v) for v in vals) + ' |')
    # the loan a lender would make: debt service covered 1.25 times by the base EBITDA, and at most 60% of the cost
    loan = round(min(0.6 * tot[1], R['Base']['ebitda'] / 1.25 / payment(1.0)), -4)
    debt = payment(loan)
    p(f'| SBA 7(a) debt service ({money(loan)}, {SBA_YEARS} yrs, {SBA_RATE:.0%}) | ' + ' | '.join(money(-debt) for _ in SCEN) + ' |')
    p('| **Cash after debt service** | ' + ' | '.join(money(R[s]['ebitda'] - debt) for s in SCEN) + ' |')
    p('| EBITDA margin | ' + ' | '.join(f"{R[s]['ebitda'] / R[s]['rev']:.0%}" for s in SCEN) + ' |')
    p('| Sales per sq ft | ' + ' | '.join(f"${R[s]['rev'] / SQFT:,.0f}" for s in SCEN) + ' |')
    p('| Occupancy cost, share of sales | ' + ' | '.join(f"{R[s]['rent'] / R[s]['rev']:.0%}" for s in SCEN) + ' |')
    p('| Labour, share of sales | ' + ' | '.join(f"{R[s]['labour'] / R[s]['rev']:.0%}" for s in SCEN) + ' |')
    p('')
    # break-even: fixed costs over the contribution of a guest night (bar and door), the shop held at the base
    b = SCEN['Base']
    fixed = labour(b) + (RENT['base'] + RENT['nnn']) * SQFT + sum(v for _, v in FIXED) + SELECTOR * NIGHTS + debt
    shop_contrib = (pnl(b)['shop']) * (SHOP_MARGIN - CARD)
    per_guest = b['spend'] * (1 - b['pour'] - CARD)
    door_contrib = (pnl(b)['door']) * (1 - CARD) - 0.15 * b['hire']
    need = (fixed - shop_contrib - door_contrib) / per_guest / NIGHTS
    need0 = (fixed - door_contrib) / per_guest / NIGHTS
    p('### Break-even\n')
    p(f'- Fixed costs at the base staffing, with debt service: {money(fixed)} a year.')
    p(f'- A guest at the bar contributes {money(per_guest)} after pour cost and card fees (spend {money(b["spend"])}).')
    p(f'- With the base door and shop: **{need:.0f} guests a night**, {NIGHTS} nights a year '
      f'({need / SEATS:.1f} per seat a night).')
    p(f'- With no shop sales at all: **{need0:.0f} guests a night**.')
    shop_only = (fixed - door_contrib - 60 * NIGHTS * per_guest) / (PRICE['pair'] * (SHOP_MARGIN - CARD))
    p(f'- At the low case\'s 60 guests a night, the shop has to sell about **{shop_only:.0f} Tropos pairs a year** '
      f'(or their margin in lamps) to break even.')
    p('')
    p('### Uses and sources (base)\n')
    ti = -capex(1)[1][1]
    eq = tot[1] - loan
    p('| Uses | | Sources | |'); p('|---|---:|---|---:|')
    p(f'| Total to open (net of the allowance) | {money(tot[1])} | SBA 7(a), 10 years | {money(loan)} |')
    p(f'| Landlord allowance, spent in construction | {money(ti)} | Equity: owners, investors, a community round | {money(eq)} |')
    p(f'| **Project** | **{money(tot[1] + ti)}** | **Total (with the allowance)** | **{money(loan + eq + ti)}** |')
    p('')
    p(f'Equity is {eq / tot[1]:.0%} of the money to open. The loan is sized so the base EBITDA covers its payments 1.25 '
      f'times, the usual test; SBA\'s own floor for a start-up\'s equity is 10%.')
    p('')
    p('### What moves the base case (EBITDA a year)\n')
    p('| Lever | Change | EBITDA |'); p('|---|---|---:|')
    base = R['Base']['ebitda']
    def var(**kw):
        return pnl({**SCEN['Base'], **kw})['ebitda'] - base
    rows = [('Ten more guests a night', 'guests 90 to 100', var(guests=100)),
            ('Spend $4 more a guest', '$36 to $40', var(spend=40.0)),
            ('One more Tropos pair a month', '12 to 24 pairs a year', var(pairs=24)),
            ('Private hire twice a month more', '+$60,000 a year', var(hire=150_000)),
            ('Sessions full', '70% to 95%', var(fill=0.95)),
            ('Pour cost two points better', '22% to 20%', var(pour=0.20)),
            ('Forty fewer staff hours a week', '270 to 230', var(hours=230))]
    for a, b_, v in rows:
        p(f'| {a} | {b_} | {money(v)} |')
    rent1 = 10 * SQFT
    p(f'| Rent $10/sq ft lower | e.g. Oakland or SoMa against Hayes Valley | {money(rent1)} |')
    print('\n'.join(out))
    return R, tot, loan, debt, need, need0


if __name__ == '__main__':
    main()
