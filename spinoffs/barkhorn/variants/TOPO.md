# Tropos "Topo" (a proposal, 2026-10-31)

**The idea:** a pair carries a place. The horn is the laminated one (22 layers of stock 1/2 in cast sheet). Each
layer's outer outline is a walk round a real mountain: Mount Tamalpais's East Peak, 784 m, the mountain over the Bay.
- The mouth's layer walks a circle 2.4 km from the summit.
- Each layer inward walks a smaller one (evenly in log radius), down to 150 m from the summit at the throat.
- Round each circle, the land's elevation pushes the layer's edge out from the wall, so ridges and ravines run down the
  horn's length in relief.
- The horn's polar angle is the compass bearing from the summit, north up. The ridge that runs east to the Bay is on the
  horn's right.

The blind critique called the laminated horn "a contour-map tunnel" and "the one image that suggests a real design
idea". Topo makes that literal and specific: it is not a generic stack, it is this mountain. A second edition could
carry Twin Peaks, or a buyer's own place (the pipeline takes any elevation tiles).

## What stays exactly as it is

- **The air path**, the approved horn's: machined through the bonded stack on 5 axes, as in `make/laminated-horn.md`.
- **The wall:** at least 10 mm everywhere, plus 8 to 45 mm of the land. The thinnest wall is the stepped horn's 10 mm.
- **The pod, cap, pads, posts, driver, cabinet, volume, port and amplifier.**

## How it is made

The same process as the stepped laminated horn:
- each layer is CNC-cut from 1/2 in stock sheet;
- the outline is the land's, from `variants/topo/outlines.json`, about 360 points a layer at about 1.5 to 5 mm
  spacing, an ordinary 2D router path;
- the edges are polished before bonding;
- the layers are bonded in sub-stacks with polymerising cement under dead weight;
- the stack is annealed and the air path machined and polished.

The router time per layer rises a little over the stepped horn's, from a smooth outline to a wavy one about 10 % longer
(est.).

**The data and its credit:** USGS 3DEP and SRTM elevation (public domain), through Mapzen's terrain tiles on AWS Open
Data. The credit line is in `variants/topo/README.md`, to be carried on the page, in the manual, and etched under the
boss.

## The numbers

| | the stepped laminated horn | Topo |
|---|---|---|
| acrylic in the stack | 4.05 L | see `variants/out/bom.md` (`horn-topo`) |
| the horn assembly (with driver and adaptor) | 9.9 kg | about the same: the land adds 8 to 45 mm round each layer, where the stepped horn's terraces add 0 to 20 |
| a horn, prototype (the kit) | about $1,570 | see `variants/out/bom.md` |

## Pictures

- the studio hero (cover off, the whole speaker);
- a macro of the terraces;
- one picture in use.

They are in `renders/2026-10-31/barkhorn/design-pass/`, with blind critic scores and duels against the current
design.
