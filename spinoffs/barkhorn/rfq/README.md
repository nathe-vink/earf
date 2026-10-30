# Requests for quotation: Hemisphere, Core and Mantle (round 42, 2026-10-30)

These are drafts for the owner to send. Nothing here has been sent, and no vendor has been contacted. The vendor
shortlist (`vendors.md`) comes from public web pages only. Prices in the deck are BOM budgets, not quotes: these
letters exist to replace them with real numbers.

| File | Goes to | Parts |
|---|---|---|
| `lamps/01-shades-forming.md` | an acrylic former who can also make (or source) turned aluminium moulds | Hemisphere's shell, opal liner, skin and rim, and the three moulds |
| `lamps/02-core-ball.md` | an acrylic fabricator who forms, bonds and polishes spheres | Core's ball: two formed halves, joined, the joint turned and polished |
| `lamps/03-black-acrylic.md` | an acrylic shop with a lathe and CNC | Core's base and window, Hemisphere's canopy |
| `lamps/04-aluminium-anodise.md` | a CNC turning shop with Type II black anodising (in house or nearby) | Hemisphere's crown, cap, collar, clamp ring and hub; Core's touch ring, port lining, chassis and hatch; the PEEK ring |
| `mantle/05-mantle-acrylic.md` | an acrylic fabricator who works thick cast sheet and edge-lit parts | Mantle's plinth, its edge-lit base, its lid, posts, platter and the motor pod's rings |
| `vendors.md` | (research) | Candidates by type, Bay Area first |
| `tints.md` | (attach to 01, 02, 05) | The eight tints as cast colours, and how the chips are made |

**How to send one:**
1. Fill in `[Your name]` and a contact line.
2. Attach the drawings each letter lists. They are in the repo, and any shop will also want STEP files:
   - **Lamps:** STEP and STL rebuild from the product files in about a minute:
     - `.venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant.py --out spinoffs/barkhorn/companions/out-dome-pendant`
     - the same with `orb_table.py` and `out-orb-table`.
   - **Mantle:** its drawings and DXF are on the `r32-turntable-final` branch, in
     `spinoffs/barkhorn/companions/out-turntable-float/`.
3. Send each letter to two or three shops from `vendors.md`, so the quotes can be compared.

**Quantities.** Every letter asks for prices at 1, 10 and 50 sets:
- 1 is the first prototype, on production tooling;
- 10 is the debut night and the first sales;
- 50 is a first run.
Tooling is asked for separately, so it can be paid once and spread.

**What is still a placeholder:** the owner's name and contact line, a ship-to address, and the target dates. The
letters say "[date]" where a date is wanted.
