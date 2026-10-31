# Tropos: making it (2026-10-31)

How the speaker gets made, and what could stop it. Written for the funding push, to raise the odds of a working
prototype pair on the first attempt.

| file | what it is |
|---|---|
| `horn-risks.md` | The horn's forming risk register: each risk, its likelihood, its impact, its mitigation, and who checks it. |
| `forming-trial.md` | A quarter-plug forming trial at full scale, before the full plug is cut: its drawing, its cost and what it proves. |
| `plan-b.md` | Five other ways to make the horn if forming fails, compared on cost, risk, look and acoustics. The recommendation is laminated layers, and it is modelled and rendered. |
| `assembly.md` | The assembly sequence with hours for each step, and the labour line for a speaker, a pair and the first pair. |
| `laminated-horn.md` | The laminated horn from 22 layers of stock 1/2 in sheet, stepped or smooth: colour, air path, edges, bond lines, mass and stability, cost and schedule beside the formed horn. |
| `diy-route.md` | The horn made ourselves if no shop can: Ace Makerspace's laser, bonding and annealing in-house; cost, schedule, and the owner's own time. |
| `stock-pair.md` | The first pair in stock sheet: Smoke from stock 3/4 in 2064, the Ember horn from stock 2423, the Ember cabinet from a Chemcast mill run; what 19 mm changes. |
| `stock_tints.py` | Stock sheet's colour per millimetre from published light transmission, for the renders (`stock_colours.json`). |
| `schedule.md` | The dated schedule to a first horn and an assembled pair, against 21 January, mid-February and April; the critical path. |
| `compliance.md` | The remote's coin cell (swap to AAA) and the amplifier compartment as the fire enclosure (two gaps). |
| `fai.md` | The first-article inspection: dimensions, finish and colour, mechanical, electrical and acoustic checks, with limits. |

The trial plug and the laminated horn are in the CAD in `horn_options.py`, drawn and costed in `out-horn-options/`. They
are built apart from the Cloud, whose build was at the container's memory limit. The first pair in stock colours is set up in `stock_colours.json`: a stock sheet's colour becomes a
render flavour (`product.stock_flavour`), refreshed into the engine by `flavours.py` without the Cloud's build.
