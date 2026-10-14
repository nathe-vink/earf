"""The price: each cabinet's cost a pair from its parts list (bom.csv, build the three first), the one-off setups taken
out and spread over a batch, plus labour, packing and certification; then retail at a direct and a dealer multiple, for
a first batch and for a leaner one; and the price the owner picked (round 15: round 14's proposal, $16,000 a pair for
Bark and Crag and $19,000 for Cloud, sold direct) as a multiple of each. The README's price tables come from it.

    .venv-fab/bin/python spinoffs/barkhorn/price.py
"""
import csv, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
from model import Machined
import product, pressed, cloud

BATCH = 25                      # pairs a batch: moulds and setups spread over it
PRICE = {'pressed': 16000.0, 'cloud': 19000.0}   # a pair, sold direct (the owner's pick, round 15)
LABOUR = {                      # hours a pair, and the rate (USD an hour, a small workshop's, loaded)
    # round 15: the 20 mm sheet's extra ribs, about an hour more welding a pair; the ports tuned on the first sample, not
    # trimmed on each; the Cloud's ports formed and cemented
    'pressed': [('CNC routing of the panels and the ring', 3.0, 90), ('welding, planing and fitting the shell', 11.0, 50),
                ('the lining cut, sleeved and fitted', 3.0, 40), ('the horns trimmed, polished, their inserts set', 4.0, 50),
                ('the electronics: compartment, L-pad, leads, preset', 3.0, 55), ('assembly, measurement, QC', 3.0, 55)],
    'cloud': [('CNC routing and edge polishing of the panels', 5.0, 90), ('annealing, cementing and annealing the shell', 10.0, 55),
              ('the lining cut, sleeved and fitted (seen through: neat)', 4.0, 40), ('the horns trimmed, polished, their inserts set', 4.0, 50),
              ('the ports\' tubes flared, cemented into their frames, polished', 1.0, 55),
              ('the electronics: compartment, L-pad, leads, preset', 3.0, 55), ('assembly, measurement, QC', 3.5, 55)],
    'plywood': [('CNC routing of the panels', 2.5, 90), ('glue-up, bark laminating and sealing', 9.0, 50),
                ('the lining cut, sleeved and fitted', 3.0, 40), ('the horns trimmed, polished, their inserts set', 4.0, 50),
                ('the electronics: compartment, L-pad, leads, preset', 3.0, 55), ('assembly, measurement, QC', 3.0, 55)]}
PACK = 220.0                    # two foam-lined cartons for the cabinets and two for the horns, a pair
CERT = 12000.0 / 100            # an EMC pre-scan and an IEC 62368-1 assessment, about $12,000, over the first 100 pairs
SETUP_SPARES = 2.0              # moulds and fixtures wear: a batch of 25 pairs uses about two of each

def cost(mod, out_dir):
    prod = mod.PRODUCT
    parts = {p.name: p for p in prod.parts(prod.params)}
    if not os.path.exists(os.path.join(ROOT, out_dir, 'bom.csv')):
        return None
    rows = list(csv.DictReader(open(os.path.join(ROOT, out_dir, 'bom.csv'))))
    var, setups, unpriced = 0.0, 0.0, []
    for r in rows:
        if r['option']:
            continue
        q = int(r['qty'])
        if not r['usd_each']:
            unpriced.append(r['item']); continue
        each = float(r['usd_each'])
        first = parts.get(r['item'].split(', ')[0])
        su = 0.0
        if first is not None and isinstance(first.make, Machined):
            su = first.make.setup_usd if first.make.setup_usd is not None else 40.0
        var += each * q - su
        setups += su
    return var, setups, unpriced

out = []
for key, mod, d in (('pressed', pressed, 'spinoffs/barkhorn/out-pressed'), ('cloud', cloud, 'spinoffs/barkhorn/out-cloud'),
                    ('plywood', product, 'spinoffs/barkhorn/out')):
    r = cost(mod, d)
    if r is None:
        print(key, 'no parts list yet'); continue
    var, setups, unpriced = r
    lab = sum(h * rate for _, h, rate in LABOUR[key])
    amort = setups * SETUP_SPARES / BATCH
    cogs = var + lab + amort + PACK + CERT
    out.append((key, var, setups, amort, lab, cogs, unpriced))
    print(f'{key}: parts ${var:,.0f} a pair (setups ${setups:,.0f} once, ${amort:,.0f} a pair over {BATCH}), labour ${lab:,.0f}, '
          f'pack ${PACK:,.0f}, certification ${CERT:,.0f}: cost ${cogs:,.0f} a pair; direct x2.2-2.5 = ${cogs*2.2:,.0f}-{cogs*2.5:,.0f}; '
          f'dealer x3.3-4 = ${cogs*3.3:,.0f}-{cogs*4:,.0f}; unpriced: {unpriced}'
          + (f'; at ${PRICE[key]:,.0f}: x{PRICE[key] / cogs:.2f}' if key in PRICE else ''))

# a leaner batch: the sheet pressed in-house (HDPE about $230 a m2 at 25 mm: 24 kg of sorted flake at $1.50, three hours of
# press and an hour laying the pattern; about $184 at 20 mm, against $320 bought, the same share), trade prices on the drivers and the amplifier (15 % off), batches of 50 pairs,
# the labour 15 % quicker with practice, certification over 200 pairs
print()
for key, mod, d in (('pressed', pressed, 'spinoffs/barkhorn/out-pressed'), ('cloud', cloud, 'spinoffs/barkhorn/out-cloud'),
                    ('plywood', product, 'spinoffs/barkhorn/out')):
    p = os.path.join(ROOT, d, 'bom.csv')
    if not os.path.exists(p):
        continue
    rows = [r for r in csv.DictReader(open(p)) if not r['option'] and r['usd_each']]
    sheet = sum(float(r['usd_each']) * int(r['qty']) for r in rows if 'Recycled HDPE' in r['what'])
    trade = sum(float(r['usd_each']) * int(r['qty']) for r in rows if r['item'] in ('woofer', 'hf', 'amp-plate'))
    var, setups, _ = cost(mod, d)
    var2 = var - sheet * (1 - 230 / 400) - trade * 0.15
    lab2 = sum(h * rate for _, h, rate in LABOUR[key]) * 0.85
    cogs2 = var2 + lab2 + setups * SETUP_SPARES / 50 + PACK + 12000.0 / 200
    print(f'{key} lean: HDPE sheet ${sheet:,.0f}, drivers and amp ${trade:,.0f}; parts ${var2:,.0f}, labour ${lab2:,.0f}: cost ${cogs2:,.0f} a pair; '
          f'direct x2.2-2.5 = ${cogs2*2.2:,.0f}-{cogs2*2.5:,.0f}; dealer x3.3-4 = ${cogs2*3.3:,.0f}-{cogs2*4:,.0f}'
          + (f'; at ${PRICE[key]:,.0f}: x{PRICE[key] / cogs2:.2f}' if key in PRICE else ''))
