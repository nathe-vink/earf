# Tropos: requests for quotation, the first pair (2026-10-30)

Draft requests for the first pair of Tropos (the Cloud, `spinoffs/barkhorn/cloud.py`), for the owner to send. The
quotes they bring back replace the budget figures in the funding deck: the parts list's $9,577 a pair, the
prototype's tooling ($7,109 on the parts list; about $9,600 with the trim fixture), and the allowances for casting
minimums and labour. **Nothing here has been sent.** No vendor has been contacted, no form submitted, no account opened.

| folder | to whom | what it asks for |
|---|---|---|
| `a-cast-acrylic/` | an acrylic fabricator (and, through them or directly, a caster) | the cabinet's 20 mm tinted panels in Ember and Smoke, cut, edge-polished, annealed and (separately priced) cemented; the ring, the disc frame, the port frames and tubes, the bosses, the grip cups, the IR bracket and its fallback window |
| `b-horn-forming/` | a thermoformer of thick cast acrylic | the horn: the flare pressure-formed over our plug, trimmed and polished; its throat piece, pod, cap, pads and saddle in the horn's own (heavier) dye lot |
| `b-horn-tooling/` | a pattern or tooling shop | the forming plug in tooling board for the prototype, its aluminium base plate; the aluminium production plug as a later line |
| `c-metal/` | a CNC and sheet-metal job shop | the amplifier compartment, the driver's adaptor ring, the stainless posts, the brass sockets and inserts, the rating plate |
| `d-other/` | small specialist shops | the lining batts and their sewn voile sleeves, the cloth disc, the etched wordmark, the EPDM cord seal and gasket, the post sleeves |

Each folder has:

- **`letter.md`**: the request in the owner's voice, signed `[Your name], EARF · earf.world`, with the parts table
  and the questions. Fill in `[vendor]`, `[date]` and `[Your name]` before sending.
- **`parts.csv`**: the same table for a vendor's spreadsheet. For each part: its number (A01 …), our part names, the
  drawing sheet, material, thickness, tint, the quantity for 1 pair, 10 pairs and 50 pairs, finish and tolerance.
  Quantities come from the parts list (`out-cloud/bom.csv`). The tooling lines are one set at every quantity.
- **`drawings.pdf`**: the sheets that letter refers to, cut from the drawing set of 2026-10-25 (BHC-001 to 040).
  Every request carries sheet 1 (the general arrangement), 2 (the section), 3 (the exploded view) and 39 and 40 (the
  notes).

Attach also:

- to (a): the DXF cut files of the parts listed (`spinoffs/barkhorn/out-cloud/dxf/<part>.dxf`), the nested sheets
  (`dxf/nest-cast-acrylic-*.dxf`), and the STEP files of every part listed; the bosses, the tubes, the cups and the IR
  parts have no DXF;
- to (b), (b tooling) and (c): the STEP files of the parts listed.

The DXF files are committed. The STEP files (`out-cloud/step/`) are not. Build them from `cloud.py` at the same commit:
`.venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud --skip
drawings,render,stl` (about a minute). Nothing is copied into this folder, so the pack never drifts from the build.

**Every letter asks:**

- the unit price at 1, 10 and 50 pairs;
- tooling and setup;
- minimum order and casting minimums;
- lead time;
- tint matching to our chips;
- packing;
- the dye lot: can one pair's panels and horns come from one batch? If not, how are lots matched (to one swatch, each
  lot's number on its parts)? Can 6, 10, 20, 30 and 75 mm be poured in one batch?

The horn's parts are in a lot of their own per colour, much heavier than the cabinet's (about 6 to 10 times its dye;
Ember about 10), matched to a chip we approve. The owner's call of 2026-10-31 was "Deep, like the site". So the
acrylic and forming requests ask for both lots and how they are matched, and the forming letter notes what a darker
sheet changes in the oven.

**Who to ask:** `vendors.md` is a shortlist for each kind of work, Bay Area first, then the rest of the US. It was
drawn from public sources only (each vendor's own site or listing), with the public contact route each one shows and
whether it takes small orders. Nobody on it has been contacted.

Regenerate the tables and the PDFs after a CAD change with `python3 spinoffs/barkhorn/rfq/tropos/build_rfq.py`. It
reads the parts list and the drawing set; the letters' text is in that script.
