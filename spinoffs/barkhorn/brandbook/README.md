# The EARF Brand Book, packaging and big ideas (brand lane, r47)

The brand lane's work of 2026-10-31, on `r47-brand`. Nothing here changes a product, the site or the bar: it draws
the brand from what they already are, and proposes what isn't yet decided. **Proposals until the owner signs them.**

| What | Where |
|---|---|
| The Brand Book (a private Artifact) | `book/index.html` and `book/img/`, gathered by `make_book.py` |
| Packaging: concept, sizes, tests | `PACKAGING.md`; renders `out/pack-pair.png`, `pack-open.png`, `pack-lamps.png` |
| Big ideas: seven plans | `IDEAS.md`; mockups `out/idea-*.png` |
| Press kit | `../press/` (boilerplate, fact sheets, image list) |
| Mockups (card, plate, social, signage, decals) | `scenes/*.html` → `out/*.png` |

## How it's made

- **Drawn mockups** are HTML pages in `scenes/`, set in the site's own Instrument Sans and IBM Plex Mono and the marks'
  SVGs, shot by headless Chromium: `node shoot.cjs [name ...]` writes `out/<name>.png` at the size each page's
  `<body data-w data-h data-scale>` gives. Pages with `data-transparent` come out with alpha: those are the printed
  faces (`decal-*`) the renders lay over birch and board.
- **Renders** are Cycles on the CPU (`python3.11`, the `bpy` wheel from `studio/setup.sh`):
  `python3.11 pack_render.py --shot pair|open|lamps` and `python3.11 ideas_render.py --shot plaza|library`, each
  `[--samples 128] [--scale 1]`; about 5 to 10 minutes a frame on four cores. Built from primitives (the crates, the
  boxes, the tiles) and, for the plaza, the colour globe's own GLB (`../out-globe-colour/render/`).
- **The book's pictures:** `python3 make_book.py` copies the site's finals, the marks, the mockups and (read-only, by
  `git show`) four of the bar's renders from `origin/r33-planet-world` into `book/img/` as JPEGs.
- `assets/` holds cut-outs of the globe and lockup renders (their paper ground unmixed to alpha), a hue study for the
  artist edition (`edition-study.jpg`, the Ember studio render's hue turned; not a cast), and copies of the bar's
  renders used in the Sessions mockup.

## Sources of fact

The site (`web.py`: `CLOUDS`, `SPEC`, `LAMPS`, `TT`, the copy), the project log (`../README.md`, the owner-notes table
and rounds), `../companions/`, `../product.py` (the rating plate), and the bar's house book. "In light" colour values
are sampled from the site's rendered coins (`site/img/coins-light.jpg`); the cast references wait for the stock-colour
research. Every cost in `IDEAS.md` and `PACKAGING.md` is an estimate, not a quote.

## Open for the owner

- The names held in reserve (Crust, Strata, Ozone): yes, no, or others, before any trademark search.
- Packaging: the crate's door-as-ramp and the dyed-through boxes; the sizes wait for the CAD and a crate shop's quote.
- Which of the seven ideas to pursue first (the ranking in `IDEAS.md` puts the Founding Hundred and the Tint Library
  first, as cheapest per unit of evidence).
