"""The long list of new acrylic objects, scored. Run: python3 longlist.py > LONGLIST.md
Scores are the brand lane's judgement (1-5), est.; prior art from PRIOR-ART.md where checked."""

W = dict(desire=0.25, novel=0.15, fit=0.15, build=0.20, margin=0.10, role=0.15)

# name, Earth name, family, one line, desire, novel, fit, build, margin, role, price band (est.), note
IDEAS = [
 ("A radio and streamer", "Ionos", "Listening", "A laminated block with a turned tuning ring; internet radio and streams into Tropos or any amplifier. The ionosphere carries radio", 5, 4, 5, 3, 4, 4, "$1,300-1,600", "Electronics bought in (a single-board computer, a DAC, an encoder); FCC 15B on the whole"),
 ("A small powered speaker", "Petros", "Listening", "A bookshelf speaker in laminated tint, the little sibling of Tropos", 4, 2, 4, 2, 3, 3, "$1,500-2,500 a pair", "A second acoustic design; competes for engineering time with Tropos"),
 ("A subwoofer", "Magma", "Listening", "A laminated cube under the pair", 3, 2, 4, 2, 3, 2, "$1,800-2,800", "Heavy, needs its own amplifier and DSP"),
 ("A record weight", "Moho", "Listening", "A puck of stacked tinted discs that sits on the label; named for the boundary between crust and mantle, so it sits on Mantle", 4, 3, 5, 5, 5, 5, "$95-145", "Entry price, a gift, a Kickstarter add-on"),
 ("A record stand and crate", "Bedrock", "Listening", "Two laminated end-plates with slots, holding 60 LPs upright, the spines showing", 4, 3, 4, 5, 4, 4, "$800-950", "Hotels and bars buy them in numbers"),
 ("Speaker stands", "Plinth", "Listening", "Laminated blocks under bookshelf speakers", 3, 2, 3, 4, 3, 2, "$600-900 a pair", "Generic; heavy to ship"),
 ("An acoustic diffuser that is a lit relief", "Relief", "Listening", "A wall panel of stacked tinted bars at stepped depths: a skyline diffuser that reads as a contour map, lit along its edges", 4, 4, 4, 4, 3, 4, "$2,400-2,800 a panel", "For rooms: hotels, studios, bars; acoustic claims need measuring"),
 ("A headphone stand", "Tor", "Listening", "A laminated arch, the headphones hung over its crest", 3, 2, 3, 5, 4, 3, "$180-260", "Many acrylic stands exist"),
 ("A turntable mat", "Isobar", "Listening", "A 3 mm tinted acrylic mat", 2, 1, 3, 5, 4, 3, "$60-90", "Acrylic mats are common"),
 ("A floor lamp, a tall core sample", "Lithos", "Light", "A column of stacked tinted discs, the eight in order like a drill core, lit from within so every layer glows at its edge", 5, 4, 5, 4, 4, 4, "$3,200-3,800", "The line's signature made into a lamp"),
 ("A wall light, a horizon", "Horizon", "Light", "A thick slab on the wall, edge-lit, so only one line of light shows: the horizon", 4, 3, 4, 4, 4, 3, "$450-650", "A UL listing like the pendant's"),
 ("A chandelier of fins", "Aurora", "Light", "Parallel tinted fins hung in a row, edge-lit, curtains of colour", 4, 3, 4, 3, 3, 3, "$3,500-6,000", "Large; hotels; certification and rigging"),
 ("A candle holder", "Caldera", "Light", "A laminated block with a bored crater for a tea light; the flame lights the tint", 3, 2, 4, 5, 4, 4, "$85-120", "Heat: glass cup liner needed; acrylic is combustible"),
 ("Bookends", "Cairn", "Objects", "Two stacks of tinted slabs, stepped like a cairn or an outcrop, heavy enough to hold books", 4, 3, 4, 5, 4, 5, "$350-420 a pair", "A gift; strong offcut use"),
 ("A side table", "Mesa", "Objects", "A laminated top with its strata at the edge, on a laminated column", 4, 2, 4, 3, 3, 3, "$2,400-3,600", "Kuramata, Marcelis and others own the acrylic table; must look different"),
 ("A stool", "Butte", "Objects", "A solid laminated block to sit on", 3, 2, 3, 3, 2, 2, "$1,800-2,800", "Heavy and costly in sheet"),
 ("A tray", "Delta", "Objects", "A slab with a pocket machined as a river delta's contours", 3, 3, 4, 5, 4, 4, "$140-220", "A gift; hotels' valet trays"),
 ("A vase with a glass liner", "Geode", "Objects", "A laminated block bored out for a glass tube; the water line shows through the tint", 4, 3, 4, 4, 4, 4, "$220-320", "A gift; a bar's flower"),
 ("A clock", "Meridian", "Objects", "Two tinted discs as hands, overlapping: where they cross, a third colour tells the time", 4, 4, 4, 3, 3, 3, "$350-520", "A bought quartz or a small motor; the colour-mix idea is the point"),
 ("A chess set", "Tectonic", "Objects", "Pieces as stacked laminations of two tints", 3, 1, 2, 4, 3, 3, "$450-750", "Acrylic chess sets abound"),
 ("A puck that throws caustics", "Pebble", "Small", "A palm-sized polished puck in one tint: in sun, it throws a coloured caustic on the desk", 3, 2, 4, 5, 5, 5, "$35-55", "The cheapest way into the tints"),
 ("The tint chips, boxed", "Swatch", "Small", "The eight tints as chips in a box (the Tint Library's small sibling)", 3, 2, 5, 5, 5, 4, "$45-75", "Trade and gifts; overlaps idea f"),
 ("A keyring tag", "Tag", "Small", "A tinted laminated tag", 2, 1, 3, 5, 4, 3, "$20-30", "Merchandise; low brand value"),
 ("Tinted acrylic bricks", "Crust", "Architecture", "Laminated blocks that stack dry into a wall or a screen, like glass block in colour", 4, 4, 4, 3, 2, 4, "$40-70 a brick", "Many bricks per wall: margin per brick thin; a contract product"),
 ("A room screen of strata", "Fault", "Architecture", "Upright slats of tint on a base, a screen whose layers shift as you pass", 4, 3, 4, 4, 3, 3, "$2,500-4,500", "Hotels and offices"),
 ("A level meter of strata", "Seismo", "Wild", "A small stack whose layers light one by one with the music's level: a VU meter as geology", 4, 4, 4, 3, 3, 3, "$300-450", "Electronics; a novelty risk"),
 ("A sun catcher for a window", "Prism", "Wild", "A stepped strip in the window that lays the eight colours across the room each morning", 3, 3, 4, 5, 4, 4, "$120-180", "Caustics as the product"),
 ("A doorstop", "Boulder", "Wild", "A heavy laminated wedge", 2, 2, 3, 5, 4, 2, "$120-160", "A use for offcuts"),
 ("A planter", "Loam", "Objects", "A laminated cachepot with a liner", 3, 2, 3, 4, 3, 3, "$180-280", "Water and UV indoors only"),
]

def score(i):
    d, n, f, b, m, r = i[4:10]
    return d*W['desire'] + n*W['novel'] + f*W['fit'] + b*W['build'] + m*W['margin'] + r*W['role']

rows = sorted(IDEAS, key=score, reverse=True)
p = print
p("# EARF new objects: the long list\n")
p("Brand lane, 31 October 2026, for the owner's \"more acrylic product ideas\" (r46-owner-notes 6a9fa7f4). **Ideas, not plans.**")
p("Nothing here touches Tropos, Hemisphere, Core, Mantle or the bar. Scores are the brand lane's judgement, 1 to 5,")
p("weighted (desirability 25%, buildability 20%, novelty, fit and sales role 15% each, margin 10%); prices are est.;")
p("prior art for the strongest is in `PRIOR-ART.md`; the six chosen are costed in `SIX.md`, whose BOMs set their bands here. Generated by `longlist.py`.\n")
p("| Rank | Name | What | Family | Desire | Novel | Fit | Build | Margin | Role | **Score** | Price (est.) | Note |")
p("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, i in enumerate(rows, 1):
    p(f"| {k} | **{i[1]}** | {i[0]}: {i[3]} | {i[2]} | {i[4]} | {i[5]} | {i[6]} | {i[7]} | {i[8]} | {i[9]} | **{score(i):.2f}** | {i[10]} | {i[11]} |")
p(f"\n{len(IDEAS)} ideas. **Buildability** means from stock cast sheet with our processes: laser or CNC cutting, lamination with")
p("a polymerising cement, turning, flame and diamond polishing, bought electronics. **Role** is what it does for sales and")
p("funding: an entry price, a gift, a hotel or bar order, a Kickstarter add-on.")
