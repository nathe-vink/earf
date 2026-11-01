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
  boxes, the tiles) and, for the plaza, the color globe's own GLB (`../out-globe-colour/render/`).
- **The book's pictures:** `python3 make_book.py` copies the site's finals, the marks, the mockups and (read-only, by
  `git show`) four of the bar's renders from `origin/r33-planet-world` into `book/img/` as JPEGs.
- `assets/` holds cut-outs of the globe and lockup renders (their paper ground unmixed to alpha), a hue study for the
  artist edition (`edition-study.jpg`, the Ember studio render's hue turned; not a cast), and copies of the bar's
  renders used in the Sessions mockup.

## Sources of fact

The site (`web.py`: `CLOUDS`, `SPEC`, `LAMPS`, `TT`, the copy), the project log (`../README.md`, the owner-notes table
and rounds), `../companions/`, `../product.py` (the rating plate), and the bar's house book. "In light" color values
were sampled from the site's rendered coins (`site/img/coins-light.jpg`). Since the owner's ruling of 2026-11-01 ("I like
the darker colors": stock TruCast sheet's deeper tints, `r33-speaker-horn` `asset/TINTS.md`), the Brand Book's swatches are a
**draft**: Ember `#C92118`→`#920000`, Poison `#367424`→`#024800`, Haze `#5B3197`→`#330066`, Smoke `#57545F`→`#3A3741`;
Dust, Acid, Ice and Fog unchanged. Method: the light through 20 mm of each stock sheet and of the site's sheet, computed with
the horn lane's held TT and channel splits; the change in OKLab lightness, at 0.6, applied to the old swatch, with its
chroma scaled by the change in chroma (floor 0.75); tints whose lightness moves less than 0.05 keep their swatch. Held
until the chips are measured. Approved as a proposal (coordinator, 2026-11-01) and swept through the collateral's
strips, `pack_render.py` and the marks (`../marks.py`: Ember `#9B0000`, Poison `#245208`, Haze `#421D72`).
**Colors F** (the owner's pick, 2026-11-01, owner note 68adc2c3; speaker lane `TINTS.md` c38f8ee6, render model
55c12c58): a white lining in seven colors (Smoke keeps black), and Poison and Haze in lighter custom batches, 32.3 % and
25.8 % through 20 mm. By the same method, from the site's swatches: In light Poison `#1C5B02`, Haze `#44147B`; Mark
Poison `#376621`, Haze `#543287`. The other six are unchanged.
**The exception: Smoke's mark stays `#34323A`.** The method gives `#19171F`, the outline ink's own value (`#1C1A18`), and
the mark and its icon lose their acrylic construction, the ink outlines over the fills, and read as a black blob. A mark
that loses its construction is worse than one a step lighter; the Book's In light swatch, `#3A3741`, carries the deeper
Smoke. The three Cycles pack renders wait for the speaker lane's regenerated asset. Every cost in `IDEAS.md` and `PACKAGING.md` is an estimate, not a quote.

## Renders: where they stand

Critic rounds are in `critic/LOG.md`. The crates and the open crate stopped after three rounds at 5.5 (from 5.5 and
5.0): the light and staging are now right, and the limit is the material (procedural birch, displaced cloth). A
photographed birch-ply texture and a cloth simulation are the next step, or better, a photograph of the first real
crate. The plaza render scored 4.0 twice and was replaced by an elevation drawing.

## Open for the owner

- The names held in reserve (Crust, Strata, Ozone): yes, no, or others, before any trademark search.
- Packaging: the crate's door-as-ramp and the dyed-through boxes; the sizes wait for the CAD and a crate shop's quote.
- Which of the seven ideas to pursue first (the ranking in `IDEAS.md` puts the Founding Hundred and the Tint Library
  first, as cheapest per unit of evidence).
