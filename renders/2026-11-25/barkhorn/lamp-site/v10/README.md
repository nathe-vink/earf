# Hemisphere V10-1: the canopy's wiring, stopped for the owner (2026-11-25)

The coordinator's V10 list (04:32 UTC) asked to test the reviewer's route: the driver screwed flat by its tabs under the
enclosure's top, its input leads to splices in the outlet box, the cord up from the centre into the room under the
driver; and, if the cord can't stay centred, to stop and send two pictured options. It can't, so this folder holds them.

**Why the cord can't stay centred in 150 x 50.** Screwed under the enclosure's top, the driver (84 x 40 x 25) leaves
11.8 under it. A straight-through strain relief for the Ø6 round cord stands about 8.5 inside a 1.0 cover (11.5 overall,
as the reviewer read Heyco's table), the jacket should run about 6 past it, and the two conductors then turn to the
splice (about 6 more). That is about 21 against 11.8. The cord itself can't turn there: Ø6 round cord wants a bend
radius of several diameters, and the driver covers the axis wherever it sits.

**Option 1, the cord 20 off centre (canopy 150 x 50 kept).** The driver against one wall of the enclosure; the cord
leaves the canopy's floor 20 off the centre on the cables' line and rises straight beside the driver through a strain
relief in the cover; its conductors go to a lever splice (WAGO 221-412) lying under the driver. The enclosure is 36
tall (10 under the driver for the 8.2 splice; 4.4 under the cover for the strain relief's head and low-head cover
screws).

**Option 2, the cord centred, the canopy 62 tall (+12).** The same inside, the enclosure 48 tall, 22 under the driver:
the cord up the axis through the cover's strain relief, its conductors turned to the same splice.

**Both.** The driver screwed by its tabs (two M3 x 6 through the tabs and the top into PEM SO-M3-4 standoffs in the
plate, so the same screws hang the enclosure; two M4 x 6 serrated screws into SO-M4-4 standoffs in the strip beside
the driver). The driver's input leads (300) up through a 3/8 in snap bushing in the top and a Ø16 opening in the plate
into the outlet box, spliced there (150 in the box, UL 1598 6.15.1.6): no mains splice in the enclosure, so 6.16's
splice room no longer applies to it. The only 120 V wiring in the enclosure is those two leads, at the driver's input
end, about 25 or more from the Class 2 cord and its splice at the other end (6.17.2: 6.4 with routing; tie the leads
to the input end).

**To confirm on the parts:** the driver's tab outline (drawn as a placeholder, two 20 x 6 x 1 tabs at 80 c-c; ERP's
datasheet p.11 sets it), the strain relief's part number and hole shape from Heyco's table, PEM's SO-M3 hole size.

**Files.** `crystal.py` draws both behind `HEMI_WIRING=O1|O2` (unset: v9 as drawn). `wiring_options.py` draws the
sections from those solids; `make_options_sheet.py` puts them beside today's top sheet (v9) as `options-sheet.jpg`.
`fixings_check.py` (zero tolerance) passes for v9, O1 and O2 on today's top, A and B.

**Not started until the owner picks:** V10-2 to V10-12. They don't depend on the choice except V10-2's green screw and
V10-3's sheet-metal holes, which follow the chosen inside.
