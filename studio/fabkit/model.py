"""What a product is to the kit: its parts, each with the solid it is, how it is made and how it is finished.

A product file (any concept: a speaker, a lamp, an amplifier) defines its numbers and a function that turns them into
parts. Everything else, the CAD files, the cut files and their nesting, the print files, the drawings, the parts list
and its cost, the clash checks and the render model, is the kit's job (`build.py`). The kit never needs to know what the
product is: it reads each part's solid and its `make`.

    import os, sys
    sys.path.insert(0, '<repo>/studio/fabkit')       # build.py does this too
    from kit import *                                # Part, Product, Sheet, Printed, Machined, Bought, box, cyl, ...

    def parts(P):
        side = Sheet('baltic-birch', 18, grain='z')
        return [Part('left', box(0, 0, 0, 18, P['depth'], P['height']), side, finish='birch'),
                Part('damping', None, Bought('damping-fill'))]          # a bought part with nothing to draw

    PRODUCT = Product('example', 'Example', 'A two-way speaker', params=dict(depth=300, height=900), parts=parts)

studio/fabkit/example/product.py is a whole one.

Units are millimetres throughout; the frame is the product's own: x across (left to right seen from the front), y
from the front face backwards, z up from the floor. Solids are build123d shapes, placed where they sit in the product.
"""
from dataclasses import dataclass, field
from typing import Callable

# Stock the cut files and the costing know about. Prices are rough (2026, USD), for budgeting only: a shop's quote
# replaces them. Densities in g/cm3.
SHEETS = {
    'baltic-birch': dict(title='Baltic birch plywood, BB/BB', density=0.68, sheet=(1525.0, 1525.0), usd_per_m2=58.0,
                         thicknesses=(6, 9, 12, 15, 18, 24)),
    'mdf': dict(title='MDF', density=0.75, sheet=(2440.0, 1220.0), usd_per_m2=18.0, thicknesses=(6, 9, 12, 18, 25)),
    'walnut-ply': dict(title='Walnut-veneered plywood', density=0.65, sheet=(2440.0, 1220.0), usd_per_m2=95.0,
                       thicknesses=(6, 12, 18)),
    'acrylic': dict(title='Cast acrylic', density=1.19, sheet=(1220.0, 610.0), usd_per_m2=120.0, thicknesses=(3, 5, 6, 10)),
    'aluminium': dict(title='Aluminium 5052 sheet', density=2.68, sheet=(1220.0, 610.0), usd_per_m2=160.0,
                      thicknesses=(1.5, 2, 3, 5, 6)),
    # no rate yet (usd_per_m2 None: the parts list shows [PRICE] until a supplier's is entered)
    'spotted-gum-ply': dict(title='Spotted gum-veneered plywood (a eucalypt hardwood face)', density=0.7, sheet=(2400.0, 1200.0),
                            usd_per_m2=None, thicknesses=(6, 9, 12, 18)),
    'cork': dict(title='Cork sheet, agglomerated', density=0.24, sheet=(1830.0, 915.0), usd_per_m2=None, thicknesses=(3, 6)),
    # thick sheet priced by its thickness (usd_per_m2_mm: a square metre a millimetre): pressed to order, recycled HDPE
    # runs about EUR 150 a square metre at 10 mm from the Precious Plastic sellers (2026; a laid-out pattern costs more);
    # cast acrylic about $1,400 a 4 x 8 ft sheet at 25 mm (US retail, 2026), as thin cast sheet runs pro rata
    'recycled-hdpe': dict(title='Recycled HDPE sheet, pressed to order (a sheet press workspace)', density=0.95,
                          sheet=(1000.0, 1000.0), usd_per_m2_mm=16.0, thicknesses=(5, 6, 8, 10, 12, 15, 20, 25, 30)),
    'cast-acrylic': dict(title='Cast acrylic, tinted through in the speaker\'s colour, 4 x 8 ft sheet', density=1.19,
                         sheet=(2440.0, 1220.0), usd_per_m2_mm=19.0, thicknesses=(6, 8, 10, 12, 15, 20, 25, 30)),
    # a speaker's lining: soft, cut with a long knife or a hot wire against a straightedge rather than routed
    'polyester-batting': dict(title='Polyester batt, acoustic grade, about 30 kg/m3, thermally bonded (no binder), with recycled PET content',
                              density=0.03, sheet=(1200.0, 600.0), usd_per_m2_mm=0.2, thicknesses=(25, 50, 75)),   # about $10 a m2 at 50
}
PRINTS = {
    'resin-tough': dict(title='Tough (ABS-like) SLA resin', process='sla', density=1.15, usd_per_cm3=0.35, min_wall=1.5),
    'nylon-mjf': dict(title='PA12 nylon, MJF', process='mjf', density=1.01, usd_per_cm3=0.30, min_wall=1.0),
    'petg': dict(title='PETG, FDM', process='fdm', density=1.27, usd_per_cm3=0.06, min_wall=1.6),
    'pla': dict(title='PLA, FDM', process='fdm', density=1.24, usd_per_cm3=0.05, min_wall=1.2),
    'asa': dict(title='ASA, FDM (outdoor, paintable)', process='fdm', density=1.07, usd_per_cm3=0.07, min_wall=1.6),
}
SOLIDS = {
    'birch-hardwood': dict(title='Birch, solid', density=0.67, usd_per_cm3=0.012),
    'oak': dict(title='White oak, solid', density=0.75, usd_per_cm3=0.018),
    'aluminium': dict(title='Aluminium 6061', density=2.70, usd_per_cm3=0.025),
    'brass': dict(title='Brass C360', density=8.5, usd_per_cm3=0.12),
    'steel': dict(title='Mild steel', density=7.85, usd_per_cm3=0.01),
    'stainless': dict(title='Stainless steel 304', density=8.0, usd_per_cm3=0.03),
    'cast-resin': dict(title='Casting resin (polyurethane or epoxy), tinted clear, translucent or pigmented', density=1.1, usd_per_cm3=0.04),
    'rotomoulded-pe': dict(title='Recycled polyethylene, rotomoulded (a hollow double-walled part)', density=0.94, usd_per_cm3=0.004),
    'cast-acrylic': dict(title='Cast acrylic tube, tinted through', density=1.19, usd_per_cm3=0.04),
    'cast-acrylic-formed': dict(title='Cast acrylic sheet 3 mm, tinted through, drape-formed over a buck', density=1.19,
                                usd_per_cm3=0.04),
}


@dataclass
class Sheet:
    """Cut from flat stock on a CNC router or laser: the part must be a prism of `thickness` along one axis, with
    through cuts and pockets from either face. `face` names its outer (show) face: '+x', '-x', '+y', '-y', '+z' or
    '-z'; left out, the face farther from the product's centre."""
    material: str = 'baltic-birch'
    thickness: float = 18.0
    face: str | None = None
    grain: str | None = None        # 'x', 'y' or 'z': the direction the face grain must run (nesting keeps it)


@dataclass
class Printed:
    """3D printed. `material` is a key of PRINTS; `orient` a note for the printer (which face down)."""
    material: str = 'resin-tough'
    orient: str = ''
    min_wall: float | None = None


@dataclass
class Machined:
    """Milled, turned or cut from solid (a block of wood, a billet of metal), cast in a mould (process 'cast': the
    material is the part's own volume, the setup the mould), or formed from tube or sheet (process 'formed': a tube's
    end flared over a heated mandrel; the material its own volume, the setup the former). `material` is a key of
    SOLIDS."""
    material: str = 'birch-hardwood'
    process: str = 'cnc-mill'
    stock: tuple | None = None      # the blank it comes from, mm (x, y, z); left out, its bounding box plus 5 mm a side
    setup_usd: float | None = None  # the line's setup (a mould, a fixture); left out, 40


@dataclass
class Bought:
    """Bought ready made: `ref` is a key of the component library (library/components.json), which holds its maker,
    model, price, datasheet and size. The solid is what the drawings and renders show of it; None for what has nothing
    to show (screws by the set, damping, glue), which the parts list still counts."""
    ref: str
    qty_note: str = ''


@dataclass
class Part:
    name: str
    solid: object
    make: object
    finish: str = ''                # the finish's name: the render's material, the drawings' finish column
    qty: int = 1                    # per product
    notes: list = field(default_factory=list)
    group: str = ''                 # parts drawn together on a detail sheet (e.g. 'cabinet', 'horn')
    render: bool = True             # in the render model
    inside: bool = False            # hidden in the assembled product (drawn dashed, kept for cutaways)
    draw: object = None             # a simpler solid for the drawings (a driver without its fine detail); left out,
                                    # the solid
    pieces: dict = field(default_factory=dict)   # {piece: (solid, finish)}: what the render shows in its place, each
                                                 # piece in its own finish (a driver's cone, frame and magnet); the
                                                 # solid stays the whole, for the checks and drawings
    option: str = ''                # an option the product can be had with (a cover, a stand): its parts are listed apart
                                    # in the parts list with their own subtotal, nested on their own sheets, left out of
                                    # the assembly drawings, never checked against another option's parts (they are
                                    # never fitted together), and shown in a render only where a shot asks for it


@dataclass
class Product:
    name: str                       # file-safe, e.g. 'birchhorn'
    title: str                      # e.g. 'Birch Horn'
    kind: str                       # e.g. 'Two-way horn loudspeaker'
    params: dict
    parts: Callable                 # params -> list[Part]
    count: int = 2                  # products in a set (a pair of speakers)
    notes: list = field(default_factory=list)          # build notes, printed on the notes sheet and in the README
    touching: list = field(default_factory=list)       # (part, part) pairs allowed to overlap: press fits, gaskets
    materials: dict = field(default_factory=dict)      # render materials by finish name, for the engine's product file
    variants: dict = field(default_factory=dict)       # colourways, the engine's flavours: {name: {token: value}};
                                                       # a material's value '$token' (a colour, or even its preset)
                                                       # takes the flavour's
    origin: tuple = (0.0, 0.0, 0.0) # where the render engine puts the product's origin, mm (default: its footprint's
                                    # centre on the floor, worked out at build time)
    revision: str = 'A'
    drawing_prefix: str = ''        # drawing numbers' prefix; left out, the name's first letters
    drawing_style: dict = field(default_factory=dict)   # the drawings' own type, read off a slide as well as a sheet:
                                    # {'face', 'face_bold': TTF paths for the views' names and the figures, 'label_pt',
                                    # 'dim_pt', 'balloon_pt', 'balloon_r' (mm)}; left out, the kit's defaults


def make_kind(part):
    return type(part.make).__name__.lower()
