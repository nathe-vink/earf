# Planet EARF, round 44: the lantern

The owner, 31 October 2026: "Make it well architected, novel, lasting." This round redraws the bar as an architectural scheme, set in a typical 25 × 80 ft San Francisco storefront with flats above. Everything here is a proposal.

**The idea.** The listening room's room-in-room isolation becomes the building's one object.
- It is a freestanding oak box on a floated floor.
- Its face is a slotted oak baffle.
- A band of lit amber acrylic fins runs under the ceiling.
- A small oak porch is its sound lock.

| File | What |
|---|---|
| `CONCEPTS.md` | The four concept boards. Two blind critics both picked (d), the lantern. |
| `DESIGN.md` | The scheme, with numbers: reverberation (ITU BS.1116), isolation (box in box, SF Police Code 2909), quiet air, the noisy kit, structure and services, accessibility, fixtures, materials chosen to last, maintenance, and the cost ($823k–$1.56M, $411–779/sq ft). |
| `plan44.py` | The geometry, areas, occupant load, acoustics and cost. Everything else reads it. |
| `kit44.py` | The model, used for the renders and the axonometric. Calibrated acrylic: IOR 1.49, with volume absorption from internal transmittance. |
| `drawings44.py`, `sheets44.mjs`, `drawings/` | A-101 plan, A-102 RCP, A-201 sections, A-301 elevations and A-401 axonometric (`axo44.py`), as SVG and PNG plus one PDF. |
| `r44_shots.py`, `r44_card.py`, `r44_stage.py` | The three views (street, bar, lantern), the critic's card and the staging. |
| `critic/LOG.md` | The concept critics, three rounds of render critics, and the duels against the r39 and r41 heroes. |

## Finals

The finals are in `renders/2026-10-31/barkhorn/planet44/finals/`, as 1200 × 800 proofs:

| View | Critics |
|---|---|
| street p4 | 5.0 / 5.5 |
| bar p4 | 5.0 / 5.0 |
| lantern p3 | 5.0 / 4.5 |

As photographs they lose to the round 39 and round 41 door heroes, 2–0 each. The scheme won its own contest; the pictures still need their own pass (see `critic/LOG.md`).

## Rebuild

    python3 spinoffs/barkhorn/planet/r44/plan44.py
    python3 spinoffs/barkhorn/planet/r44/drawings44.py
    python3.11 spinoffs/barkhorn/planet/r44/axo44.py spinoffs/barkhorn/planet/r44/drawings/axo.png --scale 0.8 --samples 64
    D=spinoffs/barkhorn/planet/r44/drawings; node spinoffs/barkhorn/planet/r44/sheets44.mjs $D $D/A-*.svg
    python3 spinoffs/barkhorn/planet/r44/r44_shots.py && python3 studio/engine/render.py studio/shots/barkhorn/planet44/street.json --out IMG --scale 0.5 --samples 128
