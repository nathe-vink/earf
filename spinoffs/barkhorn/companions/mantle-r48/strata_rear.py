"""Strata Float v3's rear plate, wiring and earth, and rating label (round 48, after the owner picked A; no light since
2026-11-10, the owner: "Forget the lights on mantle", so the light's panel, switch, inlet and adapter are gone;
the audit's Strata items, ENGINEERING-AUDIT.md on r46-owner-notes). A proposal until the owner signs it. One A3 sheet:

    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/strata_rear.py

writes out-strata-v3/drawings/rear-panel.png and .pdf. The plate's layout comes from mantle_strata_v3.REAR_HW.
"""
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mantle_strata_v3 as X                                       # noqa: E402

P = X.P
D = X.derived(P)
OUT = os.path.join(HERE, 'out-strata-v3', 'drawings')
FS = 7
BRASS, ACR, STEEL, BLACK = '#f2e3b3', '#cfd3d6', '#c8c8c8', '#2a2a2a'
b0, b1, z0 = D['b0'], D['b1'], D['z0']
PZ0, PZ1 = b0 + 1.0, z0 - 4.0
X0, X1 = X.REAR_PLATE['x0'], X.REAR_PLATE['x1']
ZS = (b0 + b1) / 2

RATING = ['EARF  MANTLE  STRATA FLOAT        SN ________',
          'PHONO 18 V DC 0.5 A',
          'MOTOR: REGA NEO PSU MK2    USE LISTED SUPPLIES ONLY']


def R(ax, x0, y0, x1, y1, **k):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **dict(dict(fc='white', ec='k', lw=0.6), **k)))


def plate(ax):
    """Seen from behind, so the model's x runs right to left: u = X1 + X0 - x."""
    ax.set_title('A  Rear plate, seen from behind (2:1 on the sheet), 2 mm lead-free brass, brushed; legends and rating engraved and filled black',
                 fontsize=FS + 1, loc='left')
    u = lambda x: X1 + X0 - x
    R(ax, X0, PZ0, X1, PZ1, fc=BRASS, lw=0.9)
    R(ax, X0 - 6, b0, X1 + 6, b1, fc=ACR, ec='#777', lw=0.5, zorder=0)
    ax.text(X1 + 8, (b0 + b1) / 2, 'base edge\n(Smoke 2074, 12.7)', fontsize=FS - 1, va='center')
    ax.plot([X0 - 6, X1 + 6], [z0, z0], color='#777', lw=0.6, ls='--')
    ax.text(X1 + 8, z0, 'deck underside (the deck overhangs 35 behind)', fontsize=FS - 1, va='center')
    for xs in X.REAR_PLATE['screws']:
        ax.add_patch(Circle((u(xs), ZS), 1.7, fc='white', ec='k', lw=0.5))
        ax.add_patch(Circle((u(xs), ZS), 2.8, fill=False, ec='#555', lw=0.4, ls=':'))
    for name, x, z, hole, do, *_ in X.REAR_HW:
        ax.add_patch(Circle((u(x), z), hole / 2, fc='white', ec='k', lw=0.6))
        ax.add_patch(Circle((u(x), z), do / 2, fill=False, ec='#777', lw=0.4, ls=':'))
        ax.text(u(x), z + (7.5 if z > 45 else -7.5), name, fontsize=FS - 2.5, ha='center', va='center', family='DejaVu Sans')
        ax.text(u(x), z - (6.2 if z > 45 else -6.2), f'⌀{hole:g}', fontsize=FS - 3, ha='center', va='center', color='#555')
    for i, line in enumerate(RATING):
        ax.text((X0 + X1) / 2, b1 - 2.4 - 3.4 * i, line, fontsize=FS - 3.2, ha='center', va='center', family='DejaVu Sans Mono')
    # dimensions
    ax.annotate('', (X0, PZ1 + 4), (X1, PZ1 + 4), arrowprops=dict(arrowstyle='<->', lw=0.5))
    ax.text((X0 + X1) / 2, PZ1 + 5.5, f'{X1 - X0:.0f}', fontsize=FS - 1, ha='center')
    ax.annotate('', (X0 - 4, PZ0), (X0 - 4, PZ1), arrowprops=dict(arrowstyle='<->', lw=0.5))
    ax.text(X0 - 5, (PZ0 + PZ1) / 2, f'{PZ1 - PZ0:.1f}', fontsize=FS - 1, ha='right', va='center', rotation=90)
    ax.text(X0, PZ0 - 6, 'Two M3 x 10 button screws into brass inserts bonded in the base\'s edge (4.6, 10 deep). Holes from the CAD (mantle_strata_v3.REAR_HW);\n'
            'rating 2 mm caps, 3 lines, between the screws. No compliance mark until tested; the supplies carry their own.', fontsize=FS - 1, va='top')
    ax.set_xlim(X0 - 30, X1 + 75); ax.set_ylim(PZ0 - 14, PZ1 + 10); ax.set_aspect('equal'); ax.axis('off')


def section(ax):
    ax.set_title('B  Section on the 4PDT (1:1): the plate under the overhang', fontsize=FS + 1, loc='left')
    yb = 0.0
    R(ax, -60, b0, yb, b1, fc=ACR, ec='k')                                            # the base
    R(ax, -60, z0, yb + 35, z0 + 25.4, fc='#e9c9c9', ec='k')                           # the deck
    R(ax, yb, PZ0, yb + 2, PZ1, fc=BRASS)                                              # the plate
    R(ax, yb - 10, ZS - 2.3, yb, ZS + 2.3, fc='#e8c98a', hatch='....', lw=0.4)         # insert
    R(ax, yb - 8, ZS - 1.5, yb + 3.6, ZS + 1.5, fc=STEEL, lw=0.4)                      # screw
    R(ax, yb - 14, 45.5, yb, 58.5, fc=BLACK)                                           # the 4PDT's body
    R(ax, yb + 2, 52 - 3.2, yb + 10, 52 + 3.2, fc=STEEL, lw=0.4); ax.plot([yb + 10, yb + 18], [52, 55], color='k', lw=1.2)
    R(ax, -60, b0 - 4, -50, b0, fc='#555')
    ax.text(-58, b0 - 6, 'foot', fontsize=FS - 2, va='top')
    for (x, y, t) in ((-55, (b0 + b1) / 2, 'base 12.7'), (-55, z0 + 12, 'deck 25.4 (two 12.7)'), (4, 38, 'plate,\n2 brass'),
                      (-40, 52, '4PDT body\n13 x 14 deep'), (12, 58, 'lever'), (4, ZS - 6, 'M3 into a\nbonded insert')):
        ax.text(x, y, t, fontsize=FS - 2, va='center')
    ax.annotate('', (yb + 2, z0 - 1), (yb + 35, z0 - 1), arrowprops=dict(arrowstyle='<->', lw=0.5))
    ax.text(yb + 18, z0 - 2.5, '33 to the deck\'s back edge:\nplugs stay under the deck', fontsize=FS - 2, ha='center', va='top')
    ax.set_xlim(-62, 50); ax.set_ylim(b0 - 12, z0 + 30); ax.set_aspect('equal'); ax.axis('off')


def wiring(ax):
    ax.set_title('C  Signal, earth and power (one channel drawn; the other the same)', fontsize=FS + 1, loc='left')
    box = lambda x, y, w, h, t, fc='white': (ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.2', fc=fc, ec='k', lw=0.7)),
                                              ax.text(x + w / 2, y + h / 2, t, fontsize=FS - 1, ha='center', va='center'))
    box(0, 62, 24, 12, 'RB330 + 2M\nits own lead')
    box(62, 62, 26, 12, 'Phono Box S2\nMM 40 dB 47k/100p')
    box(112, 62, 18, 12, 'OUT L/R\n(RCA)')
    # the 4PDT: poles a (to the S2's input) and b (to the out); stage up, bypass down
    for k, (px, lab) in enumerate(((40, 'pole 1 (L) / 2 (R)'), (98, 'pole 3 (L) / 4 (R)'))):
        ax.add_patch(Circle((px, 68), 1.2, fc='k'))
        ax.text(px, 54, lab, fontsize=FS - 2.5, ha='center')
    ax.plot([24, 40], [68, 68], color='k', lw=0.8)
    ax.plot([40, 48], [68, 72], color='k', lw=0.8); ax.plot([48, 62], [72, 72], color='k', lw=0.6)          # stage: arm to S2 in
    ax.plot([48, 48], [64, 64], color='k'); ax.add_patch(Circle((48, 64), 0.8, fc='white', ec='k', lw=0.5))
    ax.text(49, 75, 'stage', fontsize=FS - 2.5); ax.text(49, 60.5, 'bypass', fontsize=FS - 2.5)
    ax.plot([48, 52, 52], [64, 64, 46], color='#2a6fb0', lw=0.6); ax.plot([52, 104, 104], [46, 46, 64], color='#2a6fb0', lw=0.6)
    ax.text(78, 43, 'bypass: the arm straight to the out; the S2\'s input left open and its shield earthed', fontsize=FS - 2.5, ha='center', color='#2a6fb0')
    ax.plot([88, 104], [72, 72], color='k', lw=0.6); ax.add_patch(Circle((104, 72), 0.8, fc='white', ec='k', lw=0.5))
    ax.add_patch(Circle((104, 64), 0.8, fc='white', ec='k', lw=0.5))
    ax.plot([98, 104], [68, 72], color='k', lw=0.8); ax.plot([98, 112], [68, 68], color='k', lw=0.8)
    # earth star
    ax.add_patch(Circle((70, 22), 2.2, fc=BRASS, ec='k')); ax.text(70, 16.5, 'EARTH post: the star', fontsize=FS - 1.5, ha='center')
    for (x, y, t) in ((4, 36, 'arm earth wire'), (34, 36, 'bearing housing\n(M3 ring tag)'), (64, 36, 'S2 GND terminal'),
                      (96, 36, 'out shields\n(via the S2)'), (122, 36, 'rear plate\n(brass)')):
        ax.text(x, y, t, fontsize=FS - 2.5, ha='center', va='bottom')
        ax.plot([x, 70], [35, 24], color='#3a7d3a', lw=0.6)
    # power, isolated
    box(0, 2, 26, 9, '18 V adapter (Pro-Ject,\nlisted) to 2.1 mm', fc='#f7f7f7')
    box(100, 2, 30, 9, 'Neo PSU MK2 (Rega)\nto the motor inlet', fc='#f7f7f7')
    ax.text(63, 6.5, 'the DC jack insulated', fontsize=FS - 2.5, ha='center', va='center')
    ax.text(0, -6, 'Rules: one earth point (the post), no loops; the S2\'s 18 V and the motor\'s lead never share a ground with signal, and run along the base\'s far\n'
                   'side from the arm\'s lead (40 or more apart, crossing at right angles); shielded leads, shields earthed at the S2 end only. The DC jack is\n'
                   'insulated from the plate (the S2\'s 0 V reaches the star only through its GND terminal).', fontsize=FS - 2, va='top')
    ax.set_xlim(-4, 134); ax.set_ylim(-22, 80); ax.set_aspect('equal'); ax.axis('off')


def nolight(ax):
    ax.set_title('D  No light (2026-11-10)', fontsize=FS + 1, loc='left')
    ax.text(0, 0.9, 'The owner: "Forget the lights on mantle." Mantle has no light of any kind: no strip, channel or groove,\n'
            'no 24 V adapter, no switch or inlet for it on the plate, no light wiring. The base is the signed solid Smoke 2074;\n'
            'the deck\'s underside is bead-blasted satin as its edge (the day win from the light proposals).\n'
            'The light\'s fit as drawn until now is in this file\'s history (before 2026-11-10).', fontsize=FS, va='top', transform=ax.transAxes)
    ax.axis('off')


def main():
    fig = plt.figure(figsize=(16.54, 11.69))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1], height_ratios=[1, 1], left=0.03, right=0.98, top=0.91, bottom=0.17, wspace=0.08, hspace=0.18)
    plate(fig.add_subplot(gs[0, 0])); section(fig.add_subplot(gs[0, 1]))
    wiring(fig.add_subplot(gs[1, 0])); nolight(fig.add_subplot(gs[1, 1]))
    fig.text(0.03, 0.96, 'Mantle: Strata Float v3, rear plate, wiring and earth, rating (round 48; no light since 2026-11-10)', fontsize=14, weight='bold')
    fig.text(0.03, 0.935, 'mm. A proposal until the owner signs it. The audit\'s Strata items (ENGINEERING-AUDIT.md, r46-owner-notes): no rear panel, no wiring or '
             'earth drawing, no rating label; an 8 mm strip in a 5 mm slot with 2 mm corners; a 25 W supply. No light since 2026-11-10.', fontsize=FS + 1)
    notes = (
             'First-sample checks: hum and noise at the out in both switch positions, into an outside phono stage, with the motor running (A-weighted, against the S2\'s\n'
             'own figure); the 2M\'s frequency response in bypass, into 47k, against the stage position (no droop above 10 kHz); continuity and isolation of the DC jack from the plate.')
    fig.text(0.03, 0.13, notes, fontsize=FS + 1, va='top', family='DejaVu Sans')
    os.makedirs(OUT, exist_ok=True)
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(OUT, f'rear-panel.{ext}'), dpi=150)
    print(os.path.join(OUT, 'rear-panel.png'))


if __name__ == '__main__':
    main()
