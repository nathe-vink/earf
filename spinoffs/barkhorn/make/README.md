# Tropos: making it (2026-10-31)

How the speaker gets made, and what could stop it. Written for the funding push, to raise the odds of a working
prototype pair on the first attempt.

| file | what it is |
|---|---|
| `horn-risks.md` | The horn's forming risk register: each risk, its likelihood, its impact, its mitigation, and who checks it. |
| `forming-trial.md` | A quarter-plug forming trial at full scale, before the full plug is cut: its drawing, its cost and what it proves. |
| `plan-b.md` | Five other ways to make the horn if forming fails, compared on cost, risk, look and acoustics. The recommendation is laminated layers, and it is modelled and rendered. |
| `assembly.md` | The assembly sequence with hours for each step, and the labour line for a speaker, a pair and the first pair. |
| `fai.md` | The first-article inspection: dimensions, finish and colour, mechanical, electrical and acoustic checks, with limits. |

The trial plug and the laminated horn are in the CAD in `horn_options.py`, drawn and costed in `out-horn-options/`. They
are built apart from the Cloud, whose build was at the container's memory limit. The first pair in stock colours is set up in `stock_colours.json`: a measured stock sheet becomes a
render flavour (`product.stock_flavour`).
