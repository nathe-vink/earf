"""Stage a critic round for a strata/ picture (scene.py's shots are not engine shot files, so critic/round.py's card
builder can't read them): the image under a neutral name, a card of the shot's settings, the measuring tool, and the
message for a fresh critic subagent (critic/PROMPT.md, the text between its rules, verbatim).

    python3 spinoffs/barkhorn/companions/strata/critic_stage.py IMAGE.png SHOT --tag TAG
    python3 spinoffs/barkhorn/companions/strata/critic_stage.py duel A.png B.png --tag TAG   (a blind duel)

The stage directory is the session scratchpad's critic-stage/ when CLAUDE_SCRATCH is set, else /tmp/critic-stage.
"""
import os, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'critic'))

CARDS = {
    'core-sample': """A table lamp on a side table: a column of fourteen bonded discs of tinted cast acrylic (two smoke at
the foot, seven amber, one deep red, four clear bead-blasted at the top), 110 across, 178 tall, bored up its middle and
lit by a filament of warm LED inside an opal tube. Its strata differ in finish (some discs buffed clear, some
bead-blasted satin). It stands on a black anodised aluminium foot set in under it, a knurled stainless dimmer knob.""",
    'contour-core': """A table lamp on a side table: a ball 160 across built from thirteen stacked rings of amber tinted
cast acrylic (each ring the sphere's section at its height, so its outside is terraced), lit by an opal globe inside, on
a black anodised aluminium base with a knurled stainless dimmer knob.""",
    'terrace': """A pendant over a dining table: a dome 280 across built from twelve stacked rings of amber tinted cast
acrylic, each lapping the next, so its outside is terraced and each step's polished edge glows as a line. Above it a
stack of seven black anodised aluminium fins (the heat sink), a fabric cord and a steel suspension cable to a black
canopy. The light is a recessed COB behind a honeycomb louvre.""",
    'halo': """A pendant over a dining table: a thick ring (260 across, 60 tall) of five bonded discs of tinted cast
acrylic (amber, one deep red stratum), lit from its open centre by a recessed COB; black anodised fins above.""",
}
FIXED = """**Fixed (do not prescribe changes to these):** the lamp's design, size, tint and finishes: the tints are calibrated to
the maker's published light transmission (so thick parts go deep), IOR 1.49. The lamp's light output is its real one
within a range (a glow multiplier 0.5 to 2). Anything about the room, props, camera, lens, exposure and the other
lights may change."""
SETTINGS = {
    'lit': """**Settings:** camera (position, target, lens 50 to 85 mm, f/2.8 to f/5.6); exposure (EV, now as set); the room's
fill (one area light, its watts and colour); the dusk world (strength 0.05); the lamp's glow (1.0); the table, wall
and props (oak or walnut veneer, a plaster wall, a vase, books, pears, a plate).""",
    'day': """**Settings:** camera (as lit); the sun (direction, strength 4 to 5, 5600 K-ish) through a window off frame
(its frame's shadow on the wall and table); the sky's strength (0.6); exposure; the props.""",
}


def stage_dir():
    d = Path(os.environ.get('CLAUDE_SCRATCH', '/tmp')) / 'critic-stage'
    d.mkdir(parents=True, exist_ok=True)
    return d


def prompt_text():
    t = (ROOT / 'critic' / 'PROMPT.md').read_text()
    a = t.index('\n---\n') + 5; b = t.index('\n---\n', a)
    return t[a:b].strip()


def single(image, shot, tag):
    d = stage_dir()
    img = d / f'render-{tag}.png'
    shutil.copy(image, img)
    kind = 'day' if shot.endswith('day') else 'lit'
    product = next(k for k in CARDS if shot.startswith(k))
    card = d / f'card-{tag}.md'
    card.write_text(f'# The shot\n\n**What the frame is for:** the product\'s hero for its page and the press: the lamp '
                    f'{"lit at dusk, its coloured light on the table" if kind == "lit" else "unlit in daylight, the sun through it throwing coloured light"}.\n\n'
                    f'{CARDS[product]}\n\n{FIXED}\n\n{SETTINGS[kind]}\n')
    tool = d / 'measure.py'
    shutil.copy(ROOT / 'critic' / 'measure.py', tool)
    text = prompt_text().replace('TOOL', str(tool)).replace('IMAGE', str(img)).replace('SCRATCH', str(d / f'work-{tag}'))
    msg = (f'Image: {img}\nShot card (read only in stage 2): {card}\nMeasuring tool: {tool} (run it with python3)\n'
           f'Scratch directory for your crops and grids: {d / f"work-{tag}"}\n\n{text}\n')
    (d / f'message-{tag}.txt').write_text(msg)
    print(d / f'message-{tag}.txt')


def duel(a, b, tag):
    d = stage_dir()
    pa, pb = d / f'duel-{tag}-A.png', d / f'duel-{tag}-B.png'
    shutil.copy(a, pa); shutil.copy(b, pb)
    msg = (f'Two images, A: {pa} and B: {pb}. Open both (Read tool) before reading on.\n\n'
           'You are the creative director of a studio that shoots campaigns for luxury houses. Both images show a lamp '
           'that would sell at a high price. Which one would you run as the hero of the product\'s homepage and a full '
           'magazine page? Judge: does it read as a photograph of a real, well-made object; is the product the hero; '
           'is it memorable and distinctive (could you name a dozen lamps like it, or is it its own); does its light '
           'do something beautiful. Do not judge which product you would rather buy, only which picture and object '
           'make the stronger campaign.\n\nReply with only this JSON: {"winner": "A|B", "margin": "slight|clear|decisive", '
           '"A_score": 0.0, "B_score": 0.0, "why": "two or three sentences", "distinctive_A": 0, "distinctive_B": 0}  '
           '(scores out of 10 on the campaign scale: 10 ships today, 8 strong, 6 a competent render that reads as CG; '
           'distinctiveness 1-10).\n')
    (d / f'duel-{tag}.txt').write_text(msg)
    print(d / f'duel-{tag}.txt')


if __name__ == '__main__':
    args = sys.argv[1:]
    tag = args[args.index('--tag') + 1]
    if args[0] == 'duel':
        duel(args[1], args[2], tag)
    else:
        single(args[0], args[1], tag)
