"""An EARF tonearm, concept at drawing level (round 48; the coordinator asked for it so the owner can weigh it, not a
commitment). Plan and side elevation of the arm on Outcrop's puck, at 1:1 on A3.

    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/arm_concept.py
"""
import math, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out-outcrop', 'drawings')
FS = 7
TINT, CLEAR, BRASS, STEEL, BLACK = '#c9584a', '#eef3f2', '#d9b46a', '#c8c8c8', '#2a2a2a'


def stack(ax, x0, y0, w, layers, fc_t=TINT, rounded=False):
    """Laminae from the bottom up: (thickness, 'tint'|'clear')."""
    y = y0
    for t, k in layers:
        ax.add_patch(Rectangle((x0, y), w, t, fc=fc_t if k == 'tint' else CLEAR, ec='k', lw=0.5, alpha=0.9 if k == 'tint' else 1))
        y += t
    return y


def side(ax):
    ax.set_title('Side elevation (1:1): an OEM bearing and tube, EARF\'s own counterweight, finger lift, rest and arm board', fontsize=FS + 1, loc='left')
    # the arm board: Outcrop's puck re-made as strata (clear 9.5, tint 3) with the arm's three-point fixing
    stack(ax, -42, -12, 84, [(3, 'tint'), (9, 'clear')])
    # pillar and bearing (OEM: Rega RB330's, or Origin Live's)
    ax.add_patch(Rectangle((-13, 0), 26, 30, fc=BLACK, ec='k', lw=0.6))
    ax.add_patch(FancyBboxPatch((-16, 28), 32, 16, boxstyle='round,pad=0,rounding_size=3', fc=BLACK, ec='k', lw=0.6))
    # tube: OEM (aluminum, tapered), 236.5 effective, the axis at 36 over the board
    L = 236.5
    ax.add_patch(Polygon([(0, 32), (L - 40, 34.5), (L - 40, 39.5), (0, 44)], closed=True, fc='#3a3a3a', ec='k', lw=0.6))
    # headshell and cartridge
    ax.add_patch(Rectangle((L - 42, 31), 44, 4, fc='#3a3a3a', ec='k', lw=0.5))
    ax.add_patch(Polygon([(L - 24, 31), (L - 4, 31), (L - 7, 16), (L - 22, 16)], closed=True, fc=BLACK, ec='k', lw=0.5))
    ax.plot([L - 6, L], [17, 12.5], color='k', lw=0.7)
    # finger lift: a tinted acrylic blade, laminated tint 3 / clear 3, bonded and pinned to the headshell
    ax.add_patch(Polygon([(L - 2, 33), (L + 20, 40), (L + 22, 37), (L + 1, 30.5)], closed=True, fc=TINT, ec='k', lw=0.5))
    # counterweight: a tungsten core (inside) in a turned sleeve of strata, clear 6 / tint 3 x 4, on a decoupling ring
    x = -78
    for i, (t, k) in enumerate([(3, 'tint'), (6, 'clear'), (3, 'tint'), (6, 'clear'), (3, 'tint'), (6, 'clear'), (3, 'tint')]):
        ax.add_patch(Rectangle((x, 21), t, 34, fc=TINT if k == 'tint' else CLEAR, ec='k', lw=0.4))
        x += t
    ax.add_patch(Rectangle((-74, 30), 26, 16, fc='#777', ec='k', lw=0.5, hatch='xx', alpha=0.6))
    ax.add_patch(Rectangle((-48, 34), 4, 8, fc='#111', ec='k', lw=0.4))
    ax.add_patch(Rectangle((-44, 35.5), 30, 5, fc=BLACK, ec='k', lw=0.4))
    # the rest and cue (OEM lift inside a strata column)
    stack(ax, 52, -1, 14, [(3, 'tint'), (9.5, 'clear'), (3, 'tint'), (9.5, 'clear')])
    ax.add_patch(Rectangle((50, 25), 18, 3, fc=BLACK, ec='k', lw=0.4))
    for x, y, t in ((-60, 62, 'counterweight: tungsten core (about 95 g), in a turned sleeve of\nclear and tinted laminae: the strata, in the hand'),
                    (40, 70, 'tube and bearing: OEM (Rega RB330 or Origin Live), unchanged: the\nengineering that sets the sound, bought'),
                    (190, 58, 'finger lift: a tinted acrylic blade\n(tint 3 / clear 3), bonded and pinned'),
                    (30, -26, 'arm board: Outcrop\'s puck re-made as strata, Rega three-point'),
                    (90, 6, 'cue lift and rest: OEM lift,\nin a column of strata')):
        ax.text(x, y, t, fontsize=FS - 1, va='top')
    ax.set_xlim(-90, 270); ax.set_ylim(-32, 80); ax.set_aspect('equal'); ax.axis('off')


def plan(ax):
    ax.set_title('Plan (1:2)', fontsize=FS + 1, loc='left')
    ax.add_patch(Circle((0, 0), 42, fc=CLEAR, ec=TINT, lw=3))
    ax.add_patch(Circle((0, 0), 13, fc=BLACK, ec='k'))
    ang = math.radians(-108.6)
    L = 236.5
    ex, ey = L * math.cos(ang), L * math.sin(ang)
    ax.plot([0, ex * 0.84], [0, ey * 0.84], color='#3a3a3a', lw=5, solid_capstyle='round')
    ax.add_patch(Circle((-60 * math.cos(ang), -60 * math.sin(ang)), 17, fc=TINT, ec='k', lw=0.6))
    ax.add_patch(Circle((-60 * math.cos(ang), -60 * math.sin(ang)), 9, fc='#777', ec='k', lw=0.4))
    ax.add_patch(Circle((ex, ey), 3, fc='k'))
    ax.text(ex + 8, ey, 'stylus at rest', fontsize=FS - 1)
    ax.add_patch(Circle((-195.0, -106.1), 150, fill=False, ec='#999', lw=0.6, ls='--'))
    ax.add_patch(Circle((-195.0, -106.1), 4, fc='#999'))
    ax.text(-190, -100, 'spindle, 222 from the pivot; platter 300', fontsize=FS - 1, color='#777')
    ax.set_xlim(-360, 80); ax.set_ylim(-270, 90); ax.set_aspect('equal'); ax.axis('off')


def main():
    fig = plt.figure(figsize=(16.54, 11.69))
    gs = fig.add_gridspec(2, 2, width_ratios=[2.2, 1], left=0.03, right=0.97, top=0.92, bottom=0.30, wspace=0.05)
    side(fig.add_subplot(gs[:, 0])); plan(fig.add_subplot(gs[:, 1]))
    fig.text(0.03, 0.96, 'An EARF tonearm: concept (round 48)', fontsize=14, weight='bold')
    fig.text(0.03, 0.94, 'Drawing level only. The owner\'s to weigh; not a commitment. Dimensions from the RB330 (236.5 effective, 222 mounting).', fontsize=FS + 1)
    notes = (
        'Why not an acrylic wand: PMMA\'s modulus (3.2 GPa) is a twentieth of aluminum\'s (69 GPa). A tube of the same mass and diameter would be about ten times less\n'
        'stiff (EI 0.09 of an aluminum tube 10 x 0.5), its bending modes about 3.3 times lower, deep in the audio band. The tube stays bought metal; the parts the hand touches and the eye reads become EARF\'s.\n\n'
        'Three routes, rough one-off and batch costs (estimates; none quoted):\n'
        '  1. EARF parts on a bought RB330 (drawn here). Counterweight sleeve, finger lift, rest column and strata arm board, turned and laminated by the\n'
        '     acrylic shop, tungsten core bought. About \\$150-250 a set at 10-50 sets, plus the RB330 (\\$675 retail). Rega supplies OEM arms to other makers\n'
        '     (NAD and Rotel decks have used them); whether Rega allows a modified counterweight under OEM terms is the first question to ask.\n'
        '  2. A private-label arm from an OEM maker (Ortofon has built arms for AudioQuest and Sumiko; Origin Live supplies some makers), finished in\n'
        '     EARF\'s parts. Expect a minimum order and tooling; no terms are published. Plan on \\$400-900 an arm at 50-100 a year (estimate).\n'
        '  3. An arm of our own (bearing, tube, geometry). \\$20,000-50,000 of development and a year of testing before it beats an RB330 (estimate).\n'
        '     Not recommended for the first Mantle. SME left OEM arms in 2019 and Jelco closed in 2020: OEM arm supply is thin.\n\n'
        'Recommendation: route 1 for the first run. It gives EARF\'s signature where it is seen and touched, and keeps Rega\'s bearing, which is what the sound depends on.')
    fig.text(0.03, 0.27, notes, fontsize=FS + 1, va='top', family='DejaVu Sans')
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, 'arm-concept.png'), dpi=150)
    print(os.path.join(OUT, 'arm-concept.png'))


if __name__ == '__main__':
    main()
