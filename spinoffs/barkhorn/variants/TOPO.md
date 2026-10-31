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

## Topo Clear (from the Mantle lane's idea)

**The build:**
- Each layer is water-clear cast sheet, about 9.6 mm (3/8 in, faced), with a **3 mm lamina of the tint** (stock 1/8 in,
  2423 Ember or 2074 Smoke) bonded on its front face and cut to the same outline.
- So the horn's body is clear and the color is a line at every layer's edge: each walk round the mountain becomes a
  colored contour line in glass.
- The pod, the posts and the driver show through the clear body.

**Why it is worth trying:**
- The deep tint through 10 to 45 mm of stepped wall reads very dark: TruCast 2064 passes about 1 % at 12.7 mm if its dye
  is held per millimeter (the coordinator's note).
- Thin laminae keep the color bright and literal.
- 1/8 in tinted sheet is the most widely stocked of all: every code, no minimum.

**Cost against the solid tinted Topo:**
- 44 more bonded faces, because each lamina is a joint. That is the main risk: more bond lines, each a possible bubble.
- About the same sheet cost: clear 3/8 in plus 1/8 in tinted, against tinted 1/2 in.
- More cutting, for 44 laminae.

The CAD is `horn-topo-clear` (the clear layers) and `horn-topo-lines` (the laminae) in `variants/variants.py`, shown
with the product's option "Topo Clear".

## About the colors in the pictures

The tint in these renders is the stock flavor's **"held" case**: the seller's own light transmission held at the
sheet's thickness (`make/stock_tints.py`), the central estimate until the chips are measured.

If the vendor holds the dye per millimeter instead, 1/2 in 2074 Smoke is nearly black (about 1 % at 12.7 mm), and 2423
Ember a deep oxblood. Every proposal picture's caption says which case it shows.
