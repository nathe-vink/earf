"""Planet EARF's materials and lighting board: an A3 sheet in the fab kit's style (its Page), one row for each acrylic
part (thickness, tint, how it is lit), then the stone, the absorber, the membrane and the rest, and the lighting
schedule, every value from plan.py and the room's model.

    .venv-fab/bin/python spinoffs/barkhorn/planet/board.py      # -> spinoffs/barkhorn/planet/drawings/board.pdf, board.png

Each swatch is drawn twice where the part is lit: as the sheet reads unlit (its tint over a dark ground) and as it reads
lit (the colour it glows).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sheets as PD                                                  # noqa: E402  (the plan's sheets: the Page, the product)
import plan as P                                                    # noqa: E402

DR = PD.DR
C = P.COLOURS

ACRYLIC = [
    # part, thickness, tint (unlit, lit), how it is lit, note
    ('Bar front, 8 panels 1050 x 960', '20 mm cast', None, None,
     'back-lit: white opal liner 4 mm behind, LED tape at 75 pitch in a 75 cavity (pitch = depth: no hot spots)',
     'Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke, in spectrum order; cast, not extruded (crazing)'),
    ('Back-bar shelves, display (3 levels)', '10 mm light-guide (LD12)', C['haze'], C['haze'],
     'edge-lit: LED in a rear channel 1-3 mm from the polished back edge', 'tinted bay by bay to the bar panel below'),
    ('Back-bar shelves, working (2 levels)', '10 mm light-guide (LD12)', '#F4EFE6', '#FFE7C6',
     'edge-lit, 2700 K, CRI 95+', 'warm white so the labels read'),
    ('Back-bar back panel', '6 mm opal', '#E8E2D8', '#F3E6D2', 'back-lit, dimmed low: the bottles in silhouette', 'Fog white'),
    ('Fog niches\' linings (2)', '6 mm opal', '#EDE8E0', '#FFF1DE', 'back-lit from the niche head, 3000 K', 'the Fog pair stand in them'),
    ('Lounge slats, 75 x 12 at 150', '12 mm cast', C['haze'], C['haze'],
     'gap-lit: LED top and bottom in the 75 gap to the absorber', 'one wall of each facing pair only'),
    ('Screens, bar to lounge', '10 mm cast, thermoformed', '#F2F3F2', '#F2F3F2', 'unlit; the room\'s light through them',
     'Fog, frosted, micro-perforated 0.5 mm at 2 %; 1350 high'),
    ('DJ recess back', '10 mm cast + opal', C['ice'], C['ice'], 'back-lit, dimmed', 'Ice, behind Cumulus'),
    ('Plinths (4), booth tables, side tables, DJ desk cladding, uprights', '20 mm cast', '#141316', '#141316', 'unlit',
     'Smoke, polished'),
]

OTHER = [
    ('Bar top and back counter', '#1E1F22', '40 mm honed basalt, sealed; 260 overhang. Never acrylic: spirits craze it.'),
    ('Ceiling membrane', '#C9B8D8', 'translucent micro-perforated stretch foil (Barrisol A15/A30 class), NRC 0.55; 0.85 with '
     'the absorber in the 570 plenum; back-lit RGBW: the colour clock'),
    ('Absorber', '#1B1A1F', '100 mm mineral wool, dark fabric face: behind the slats and on the opposite lounge wall'),
    ('Floor', '#5F5C57', 'the shell\'s concrete, ground, honed and sealed (satin)'),
    ('Booth upholstery', '#3B2A2A', 'channel-tufted wool velvet, oxblood brown; Smoke plinths'),
    ('Record wall', '#2A221C', 'black-stained oak cubbies 345, 300 to 550 deep at random (a diffuser), floor to membrane'),
    ('Window and door', '#2E2A25', 'bronze-anodised frames; the door blackened steel, a bronze pull; one neon sign outside'),
    ('Footrail', '#8A6A44', '50 mm bronze on nine brackets, 200 proud of the panels, 220 high'),
]

LIGHT = [
    ('Membrane', 'RGBW, DMX, graded down the room', 'the colour clock: Fog + Ice at 17:00, Acid + Dust at 19:30, Ember + '
     'Haze at 22:30, Smoke (dimmed warm grey) at last call; crossfades over 20 min'),
    ('Bar panels', 'RGB(W) per panel, fixed to the panel\'s colour', 'always on in their own colour; dimmed with the clock'),
    ('Shelves', 'edge-lit LED, 2700 K working / RGB display', 'the working shelves never change colour'),
    ('Bell', 'Fog pendants (6) over the bar; Ember lamps (4) on the booth tables', 'warm 2700 K, dimmable'),
    ('Pinhole spots', '3000 K, 25-30 deg, in the membrane', 'one on each corner speaker, one on each Fog niche, five on the '
     'bar top, the DJ desk, three down the record wall'),
    ('Outside', 'one small neon EARF over the door', 'the window is the sign'),
]


def board(pg):
    ax = pg.ax
    pg.head('Materials and lighting. Each acrylic part: its sheet, its tint unlit and lit, how it is lit. Colours are '
            'the brand\'s (the marks\' colours; the speakers\' acrylic tints are their product files\'). All proposals.')
    y = 262
    pg.text(20, y, 'Acrylic', size=9, fontweight='bold')
    pg.text(118, y, 'unlit', size=7.1); pg.text(130, y, 'lit', size=7.1)
    y -= 6
    for name, thick, unlit, lit, how, note in ACRYLIC:
        pg.text(20, y, name, size=7.1, fontweight='bold', va='center')
        pg.text(20, y - 3.6, thick, size=7.1, va='center')
        if unlit is None:                                            # the bar: the eight colours
            for i, c in enumerate(P.PANELS):
                PD._rect(ax, 116 + i * 3.6, y - 5, 116 + i * 3.6 + 3.4, y + 1.5,
                         fc=C[c] if c != 'fog' else '#EEF0F0', ec=DR.INK, lw=0.15)
        else:
            PD._rect(ax, 116, y - 5, 126, y + 1.5, fc='#121114', ec=DR.INK, lw=0.15)
            PD._rect(ax, 117.5, y - 3.5, 124.5, y, fc=unlit, ec='none', lw=0, alpha=0.75)
            PD._rect(ax, 128, y - 5, 138, y + 1.5, fc=lit, ec=DR.INK, lw=0.15)
        pg.text(148, y, how, size=7.1, va='center')
        pg.text(148, y - 3.6, note, size=7.1, va='center', color='#555')
        y -= 11
    y -= 2
    pg.text(20, y, 'Stone, absorber, membrane and the rest', size=9, fontweight='bold'); y -= 7
    for name, col, s in OTHER:
        PD._rect(ax, 116, y - 2.5, 126, y + 2.5, fc=col, ec=DR.INK, lw=0.15)
        pg.text(20, y, name, size=7.1, fontweight='bold', va='center')
        pg.text(148, y, s, size=7.1, va='center')
        y -= 6.6
    yl = 120
    pg.text(20, yl - 52, '', size=7.1)
    x0 = 20; yy = y - 4
    pg.text(x0, yy, 'Lighting', size=9, fontweight='bold'); yy -= 7
    for name, what, s in LIGHT:
        pg.text(x0, yy, name, size=7.1, fontweight='bold', va='center')
        pg.text(48, yy, what, size=7.1, va='center')
        pg.text(148, yy, s[:120], size=7.1, va='center')
        yy -= 5.6
    # the colour clock: four chips, each a membrane graded from its first colour to its second
    import numpy as np
    from matplotlib.colors import to_rgb
    pg.text(20, 48, 'The colour clock (the membrane, door to record wall)', size=8, fontweight='bold')
    for k, (hour, (a, b)) in enumerate(P.CLOCK.items()):
        xa = 20 + k * 47
        ca, cb = np.array(to_rgb(C[a])), np.array(to_rgb(C[b]))
        if a == 'smoke':
            ca = cb = np.array(to_rgb('#6E6A66'))
        t = np.linspace(0, 1, 64)[None, :, None]
        img = (ca * (1 - t) + cb * t) * 0.75 + 0.25
        ax.imshow(img, extent=(xa, xa + 42, 30, 42), aspect='auto', zorder=4)
        label = {'opening': '17:00 opening', 'sunset': '19:30 sunset', 'late': '22:30 late', 'last': '01:45 last call'}[hour]
        pg.text(xa, 26, f'{label}: {a.capitalize()}' + (f' + {b.capitalize()}' if b != a else ''), size=7.1)


def write():
    from matplotlib.backends.backend_pdf import PdfPages
    out = PD.OUT
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, 'board.pdf')
    with PdfPages(path) as pdf:
        pg = DR.Page(PD.PRODUCT, 3, 3, 'Materials and lighting')
        board(pg); PD._retitle(pg)
        pg.fig.savefig(os.path.join(out, 'board.png'), dpi=150)
        pdf.savefig(pg.fig); pg.plt.close(pg.fig)
    print(path)


if __name__ == '__main__':
    write()
