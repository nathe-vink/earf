# Portrait proofs (2026-11-14), 720 x 900, 32 samples

- `portrait-proof-A.png` (chosen): Mantle's overhead head at 0.4 in a 10-degree beam, its front and side lamps out. The near Core 4.8 / 0.78 / 0.83; the deck's mean 24.6.
- `portrait-proof-B.png`: all three of Mantle's lamps at 0.05. The Core 4.5 / 0.55 / 0.96 (the limit); the deck 21.7.
- `portrait-proof-mantle-lamps-out.png`: all three out. The Core 4.9 / 0.77 / 0.84; the deck 18.5.

## lamp-mix-sheet.jpg (2026-11-17): the owner's lamp mix in the bar frames, a test

Left the present final (halved), right the same frame at half size and 48 samples with the mix (lamps code 5fa6ef946,
the default loadings). The measure is the mix against the same code with LOAD_BUILT=1 at the same size and samples,
so noise and the low samples cancel: per bowl, mean and largest difference (8-bit, the largest channel).

| Frame | Ember bowls | Acid bowls | Elsewhere |
|---|---|---|---|
| bar-hero | 20.6 / 132, 19.9 / 121 | 11.5 / 79, 11.5 / 74 | whole frame mean 0.28 |
| bar-backbar | 18.4 / 118, 14.0 / 91 | 11.3 / 102 | reflections up to 7.8 mean; whole frame 0.26 |
| bar-pendants | 20.5 / 140, 22.9 / 130 | 14.8 / 90, 14.7 / 131 | whole frame 1.11 |
| bar-backbar-portrait | 23.7 / 124 | 13.4 / 78 | a reflection 8.6 / 60; whole frame 0.31 |
| mantle-bar | none in frame | none in frame | two reflections about 4; whole frame 0.12 |
| core-bar-table | none | none | identical |

Ember's bowl goes about 10 levels down in red and 15 in green: deeper and more saturated, with the denser shell's mottle;
visible at site size. Acid about 5 to 9 levels darker and a little warmer: visible side by side. Dust unchanged.

## lamp-mix-bowls.jpg (2026-11-17): before | after, each changed bowl at 100 %

The four bar frames before (`FRAME-premix.png`) and after the lamp mix was put in by the difference method (MEASURED.md,
"The lamp mix in four bar frames"). Each crop is the bounding box of one connected change above 8 levels, plus 10 px.
JPEG at quality 92; the PNGs are the reference.
