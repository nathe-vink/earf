"""Core's detail sheet (round 48): what the kit's general sections do not cut through, drawn from mantle_core's numbers.
The review of the baseline asked for a bearing section, fits and finishes, the oil level, the arm's height stack, the
wiring and earth scheme, and the rating label. One A3 sheet, PNG and PDF.

    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/details.py
"""
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mantle_core as M                                             # noqa: E402

P, D = M.P, M.derived(M.P)
OUT = os.path.join(HERE, 'out-core', 'drawings')
FS = 7.2


def R(ax, x0, y0, x1, y1, hatch=None, fc='white', lw=0.8, ec='k', z=1):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec, lw=lw, hatch=hatch, zorder=z))


def dim(ax, x0, y0, x1, y1, txt, off=(0, 0), rot=0):
    ax.annotate('', (x0, y0), (x1, y1), arrowprops=dict(arrowstyle='<->', lw=0.5, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], txt, fontsize=FS - 1, ha='center', va='center', rotation=rot,
            bbox=dict(fc='white', ec='none', pad=0.5))


def note(ax, x, y, txt, xy=None):
    if xy:
        ax.annotate(txt, xy, (x, y), fontsize=FS - 1, arrowprops=dict(arrowstyle='-', lw=0.4), va='center')
    else:
        ax.text(x, y, txt, fontsize=FS - 1, va='top')


def strata(ax, x0, x1, lams, ring=None):
    for l in lams:
        tinted = l['kind'] == 'tint'
        R(ax, x0, l['z0'], x1, l['z1'], hatch='////' if tinted else None, fc='#d9d9d9' if tinted else 'white', lw=0.5)


def bearing(ax):
    ax.set_title('A  Bearing, platter and hub, section on the spindle (1:1)', fontsize=FS + 1, loc='left')
    S0 = 0.0
    lams = D['lams']; b0 = P['feet_h']; top = D['top']
    strata(ax, -60, -16, lams); strata(ax, 16, 60, lams)
    hz0 = b0 + 2.0; ft = P['flange_t']
    # housing body and flange
    R(ax, -15, hz0, -7, top - ft, hatch='\\\\\\', fc='#f2e3b3'); R(ax, 7, hz0, 15, top - ft, hatch='\\\\\\', fc='#f2e3b3')
    R(ax, -15, hz0, 15, hz0 + 4, hatch='\\\\\\', fc='#f2e3b3')
    R(ax, -25, top - ft, -7, top, hatch='\\\\\\', fc='#f2e3b3'); R(ax, 7, top - ft, 25, top, hatch='\\\\\\', fc='#f2e3b3')
    # nut under the deck in its counterbore
    R(ax, -23, b0 + 2, -15, b0 + 9, hatch='xx', fc='#f2e3b3'); R(ax, 15, b0 + 2, 23, b0 + 9, hatch='xx', fc='#f2e3b3')
    # bushes
    for z0_, z1_ in ((hz0 + 12, hz0 + 24), (top - 16, top - 4)):
        R(ax, -7, z0_, -5, z1_, hatch='....', fc='#e8c98a'); R(ax, 5, z0_, 7, z1_, hatch='....', fc='#e8c98a')
    # thrust plate, ball, spindle
    R(ax, -6.9, hz0 + 4, 6.9, hz0 + 6, fc='#bbbbbb', hatch='||')
    ax.add_patch(Circle((0, hz0 + 9), 3, fc='#888', ec='k', lw=0.6, zorder=3))
    pz0, pz1 = D['pz0'], D['pz1']
    R(ax, -5, hz0 + 12, 5, pz0 + 12, fc='#e6e6e6', z=2); R(ax, -3.6, pz0 + 12, 3.6, pz1 + 15, fc='#e6e6e6', z=2)
    # oil level
    ax.plot([-7, 7], [top - 10, top - 10], ls='--', lw=0.6, color='#2a6fb0'); note(ax, 30, top - 10, 'oil to here: 2.5 ml ISO VG 32', (7, top - 10))
    # hub and platter
    R(ax, -35, pz0 - 5, -5, pz0, hatch='\\\\\\', fc='#f2e3b3'); R(ax, 5, pz0 - 5, 35, pz0, hatch='\\\\\\', fc='#f2e3b3')
    R(ax, -20, pz0, -5, pz0 + 12, hatch='\\\\\\', fc='#f2e3b3'); R(ax, 5, pz0, 20, pz0 + 12, hatch='\\\\\\', fc='#f2e3b3')
    for xa, xb in ((-80, -20.1), (20.1, 80)):
        zz = pz0
        for k, t in P['platter_lams']:
            t = t * 21.0 / 21.3
            R(ax, xa, zz, xb, zz + t, hatch='////' if k == 'tint' else None, fc='#d9d9d9' if k == 'tint' else 'white', lw=0.5)
            zz += t
    R(ax, -20.1, pz0 + 12, -4, pz1, fc='white', lw=0.5); R(ax, 4, pz0 + 12, 20.1, pz1, fc='white', lw=0.5)
    for x in (-28, 28):
        R(ax, x - 2, pz0 - 4, x + 2, pz1 - 4, fc='#999', lw=0.4, z=3); R(ax, x - 3.7, pz1 - 4, x + 3.7, pz1 - 0.5, fc='#999', lw=0.4, z=3)
    R(ax, -80, pz1, 80, pz1 + 1.8, fc='#222', lw=0.3)
    ax.text(70, pz1 + 4, 'record', fontsize=FS - 1)
    dim(ax, -70, top, -70, D['record_z'], f'{D["record_z"] - top:.1f}', off=(-6, 0), rot=90)
    dim(ax, -55, b0, -55, top, f'{top - b0:.1f}', off=(-6, 0), rot=90)
    note(ax, 30, hz0 - 4, 'housing: lead-free brass, M30 x 1.5 x 30, clamped by its nut (10 N m) on a PTFE washer', (15, hz0 + 3))
    note(ax, 30, hz0 + 18, 'bushes: C932, 10 x 14 x 12, pressed, honed to 10 H6', (7, hz0 + 18))
    note(ax, 30, hz0 + 8.5, 'carbide ball 6 g10 on lapped 52100 plate, 60 HRC, Ra 0.05', (3, hz0 + 9))
    note(ax, 30, top + 1.5, 'spindle 440C 58 HRC, 10 g5, Ra 0.1; shrunk into the hub', (5, top))
    note(ax, 30, pz0 + 6, 'hub flange 70 x 5, spigot 40 h6 in 40.2 H7; six M4 x 20 on r 28', (35, pz0 - 2))
    note(ax, -78, pz1 + 9, 'platter: tinted 3 / clear 12.7 / tinted 5.6, faced to 21.0; run-out 0.05', None)
    ax.set_xlim(-85, 150); ax.set_ylim(b0 - 6, pz1 + 22); ax.set_aspect('equal'); ax.axis('off')


def foot(ax):
    ax.set_title('B  Foot (1:1)', fontsize=FS + 1, loc='left')
    b0 = P['feet_h']
    l0 = D['lams'][0]; l1 = D['lams'][1]
    strata(ax, -35, 35, [l0, l1])
    R(ax, -20, 0, 20, 4, fc='#555', hatch='...'); R(ax, -20, 4, 20, 16, fc='#f2e3b3', hatch='\\\\\\'); R(ax, -15, 16, 15, b0 - 0.5, fc='#f2e3b3', hatch='\\\\\\')
    R(ax, -4, b0 - 4, 4, b0 + 12, fc='#ccc', z=3); R(ax, -5.5, b0, 5.5, b0 + 12, fc='none', ec='k', lw=0.6, hatch='xx', z=2)
    note(ax, 28, 2, 'Sorbothane 40 x 4, 50 duro', (20, 2)); note(ax, 28, 10, 'turned brass 40 x 12, M8 bore; brass lock nut', (20, 10))
    note(ax, 28, b0 + 6, 'M8 x 12 insert, epoxy-bonded through L1 into L2', (5.5, b0 + 6))
    ax.set_xlim(-40, 110); ax.set_ylim(-3, b0 + 18); ax.set_aspect('equal'); ax.axis('off')


def motor(ax):
    ax.set_title('C  Motor hung on Rega\'s grommets (1:1)', fontsize=FS + 1, loc='left')
    top = D['top']; lams = D['lams']
    pk = P['motor_pocket'] / 2
    strata(ax, -60, -pk - 4, lams); strata(ax, pk + 4, 60, lams)
    for s in (-1, 1):
        x0 = s * (pk + 4)
        R(ax, min(s * pk, x0), lams[0]['z0'], max(s * pk, x0), top - 6, fc='#d9d9d9', lw=0.5)
    R(ax, -41, top - 5, 41, top - 2, fc='#333')
    for x in (-36, 36):
        R(ax, x - 4, top - 6, x + 4, top - 0.5, fc='#555', hatch='...', z=3)
    R(ax, -25, top - 35, 25, top - 5, fc='#444'); R(ax, -2, top - 5, 2, D['belt_z'] + 9, fc='#bbb')
    pd = D['pulley_d'] / 2
    R(ax, -pd, D['belt_z'] - 5, pd, D['belt_z'] + 5, fc='#ddd', hatch='--')
    note(ax, 50, top + 16, 'plate 3 mm 5052, black anodised;\nthree grommets on a 6 shoulder;\npocket 76 x 40, a 12 lead hole', (30, top - 3))
    note(ax, 50, D['belt_z'] + 2, f'pulley {D["pulley_d"]:.2f} (250 rpm), the belt on the clear stratum\'s rim', (pd, D['belt_z']))
    ax.set_xlim(-65, 190); ax.set_ylim(top - 40, top + 30); ax.set_aspect('equal'); ax.axis('off')


def cover(ax):
    ax.set_title('D  Cover on the deck, back edge (1:1)', fontsize=FS + 1, loc='left')
    top = D['top']
    for l in D['lams'][-2:]:
        R(ax, l['inset'] - 6, l['z0'], 40, l['z1'], hatch='////' if l['kind'] == 'tint' else None, fc='#d9d9d9' if l['kind'] == 'tint' else 'white', lw=0.5)
    for l in D['cover'][:4]:
        x0 = l['inset'] - 6
        R(ax, x0, l['z0'], x0 + P['ring_w'], l['z1'], hatch='////' if l['kind'] == 'tint' else None, fc='#d9d9d9' if l['kind'] == 'tint' else 'white', lw=0.5)
    R(ax, 8, top - 8, 13, top + 4, fc='#bbb', z=3)
    note(ax, 30, top + 20, 'two 5 x 12 stainless dowels in the deck, 5.4 holes in the first ring; three 3M SJ5302 bumpers', (11, top + 2))
    note(ax, 30, top + 30, 'each ring 10 wide steps in 3; outer faces diamond-polished, inner as cut', (8, top + 25))
    ax.set_xlim(-5, 150); ax.set_ylim(top - 30, top + 40); ax.set_aspect('equal'); ax.axis('off')


def plate(ax):
    ax.set_title('E  Back plate and rating (1:1)', fontsize=FS + 1, loc='left')
    nw, nh = P['notch'][0], P['notch'][1]
    R(ax, 0, 0, nw - 2, nh - 1, fc='#efe2bf', lw=0.8)
    jz = nh * 0.42
    for x, lab, d in ((21, 'L', 8.2), (39, 'R', 8.2), (59, 'EARTH', 6.5), (79, 'STAGE / BYPASS', 6.4), (99, '18 V', 8.0)):
        ax.add_patch(Circle((x, jz), d / 2, fc='white', ec='k', lw=0.6)); ax.text(x, jz + 8, lab, fontsize=4.6, ha='center')
    for x, y in ((6, 5), (nw - 8, 5), (6, nh - 5), (nw - 8, nh - 5)):
        ax.add_patch(Circle((x, y), 1.7, fc='white', ec='k', lw=0.5))
    ax.text(11, 7.2, 'EARF  MANTLE CORE   LINE OUT   18 V DC 0.5 A (center +)   SN 0001', fontsize=4.0)
    ax.text(11, 3.2, 'Motor: Rega Neo PSU (own listing)   Designed in San Francisco', fontsize=4.0)
    note(ax, 0, -6, '2 mm lead-free brass, brushed, the text laser-engraved 0.05 deep and filled black. Compliance marks only\nafter testing (FCC Part 15B for the stage\'s supply as sold; the S2 and its adapter carry their own).', None)
    ax.set_xlim(-4, nw + 4); ax.set_ylim(-16, nh + 6); ax.set_aspect('equal'); ax.axis('off')


def wiring(ax):
    ax.set_title('F  Signal, power and earth', fontsize=FS + 1, loc='left')
    box = lambda x, y, w, h, t: (ax.add_patch(Rectangle((x, y), w, h, fc='white', ec='k', lw=0.7)), ax.text(x + w / 2, y + h / 2, t, fontsize=FS - 1, ha='center', va='center'))
    box(0, 40, 26, 12, 'RB330 + 2M\n(own lead)'); box(40, 40, 26, 12, 'Phono Box S2\nMM 40 dB 47k/100p')
    box(80, 40, 26, 12, 'plate: DPDT\nstage / bypass'); box(120, 40, 22, 12, 'RCA out\nto speakers')
    box(40, 14, 26, 12, 'Pro-Ject 18 V\nadapter (listed)'); box(0, 14, 26, 12, 'bearing housing\nM3 ring tag')
    box(120, 14, 22, 12, 'Rega Neo PSU\n(listed) to motor')
    for a, b in (((26, 46), (40, 46)), ((66, 46), (80, 46)), ((106, 46), (120, 46)), ((53, 26), (53, 40))):
        ax.annotate('', b, a, arrowprops=dict(arrowstyle='->', lw=0.6))
    ax.plot([13, 13, 93, 93], [26, 34, 34, 40], color='#2a8a2a', lw=0.8); ax.plot([13, 13], [40, 34], color='#2a8a2a', lw=0.8)
    ax.plot([53, 53], [34, 40], color='#2a8a2a', lw=0.8)
    ax.text(70, 30.5, 'star earth at the plate\'s post (arm lead, housing, S2)', fontsize=FS - 1, color='#2a8a2a')
    ax.text(0, 4, 'Two plugs at the wall, both makers\' listed supplies; nothing in Core above 24 V. The motor lead runs in its groove\nto the back notch, the arm lead in its own, 40 mm apart; no LED, no dimmer, no shared supply.', fontsize=FS - 1)
    ax.set_xlim(-2, 146); ax.set_ylim(0, 56); ax.set_aspect('equal'); ax.axis('off')


def main():
    fig = plt.figure(figsize=(16.54, 11.69))
    gs = fig.add_gridspec(3, 3, left=0.03, right=0.97, top=0.94, bottom=0.08, hspace=0.25, wspace=0.12)
    bearing(fig.add_subplot(gs[0:2, 0:2])); foot(fig.add_subplot(gs[0, 2])); motor(fig.add_subplot(gs[1, 2]))
    cover(fig.add_subplot(gs[2, 0])); plate(fig.add_subplot(gs[2, 1])); wiring(fig.add_subplot(gs[2, 2]))
    fig.text(0.03, 0.97, 'Mantle: Core (proposal B), details', fontsize=14, weight='bold')
    fig.text(0.03, 0.955, 'mm, first angle; from mantle_core.py (round 48). Strata hatched where tinted. A proposal until the owner signs it.', fontsize=FS)
    fig.text(0.03, 0.03, 'Fits: spindle 10 g5 / bushes 10 H6 (8-12 um); hub spigot 40 h6 / platter 40.2 H7; the housing a 30.4 clearance bore. '
             'Finishes: outer acrylic faces diamond-polished, treads buffed, holes and pockets as machined. Arm height: Rega spacers to a level tube on the first sample.',
             fontsize=FS)
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, 'details.png'), dpi=150); fig.savefig(os.path.join(OUT, 'details.pdf'))
    print(os.path.join(OUT, 'details.png'))


if __name__ == '__main__':
    main()
