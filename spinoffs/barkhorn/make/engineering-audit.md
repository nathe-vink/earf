# Tropos: the engineering audit's fixes (2026-11-01)

The coordinator's reviewed list: an audit of every product, then an independent reviewer. Each item applies to the
stepped (lead) version and to the smooth-horn option. Numbers marked (est.) are estimates to be confirmed on the first
article. The analysis scripts are `stability/com.py` and `stability/horn.py`, with their outputs beside them.

| # | item | status |
|---|---|---|
| 1 | Stability, IEC 62368-1 8.6.2.2 | **the owner's decision**: both designs fail in every direction; the options are below |
| 2 | Horn retention | **fixed**: keyhole sockets at the front, the tie rod at 2 N m; the drawing's detail to follow |
| 3 | Heat, the abnormal case | **fixed**: the L-pad removed, the 6 dB in the DSP; the capacitor stood off |
| 4 | Preset | **fixed**: three slots, the password, the limits |
| 5 | FAI levels | **fixed**: a static pressure decay at 200 Pa; sweeps from 35 Hz |
| 6 | Parts and docs | **fixed** |
| 7 | The FA122's CB report | **a draft request to Hypex** (not sent); the end product's listing planned |

## 1. Stability

The test's force is 20 % of the weight, so the check is purely geometric: the center of mass must sit at least 0.2 x
the push's height inside every tipping edge. That is 259 to 261 mm.

| | current | Strata |
|---|---|---|
| mass | 70.2 kg | 75.2 kg |
| center of mass | 233 mm behind the front, 533 up | 222 behind, 553 up |
| margins on today's feet (centers): forward, back, side | -20 %, -37 %, -11 % | -24 %, -34 %, -12 % |

A pass with a 15 % margin needs the feet's centers at about 600 x 600 mm. The options are a stepped plinth, outrigger
feet, or anchoring (the lab's reading). All are in `stability/README.md`. Each changes the look, so nothing is drawn
until the owner chooses.

## 2. Horn retention

**The audit's finding:** the feet stood loose in sleeved sockets, and one tie rod held the horn down.
`stability/horn.py` puts the horn assembly at 8.6 kg (formed) and 11.4 kg (Strata, with its posts and collars). Under
the stability test's push at its top, the horn starts to lift at **13 N (formed) and 23 N (Strata)**.

**The fix:** the horn is held at three points, so it cannot lift in any direction.
- **The front posts** stand over the front panel's top edge, so nothing can be reached under them. Each foot ends in a
  turned head, 14 across and 4 thick on an 8 neck. The head hooks under the lip of a **keyhole socket**: bronze, 30
  across and 15 deep, bonded through the top into the panel's edge. The horn goes on by dropping the heads into the
  holes and sliding it 10 mm back.
- **Rear post 3:** the tie rod, its nut inside the pod tightened to **2 N m** (about 1.7 kN of preload). It holds the
  rear down and locks the slide.
- **Rear post 4,** the cable post, stays seated in its sleeve.
- **The loads under the push** (est.): about 150 N up at a front hook and 90 N on the tie, against several kN for each
  bonded fitting (FAI M1 pulls them to 2 kN).
- **Each post** carries 21 N (formed) or 28 N (Strata) of the horn's weight, not 14. Bending at a post's root, with a
  quarter of the push each: 55 MPa in a 10 x 7 stainless tube (304 yields at 205) and 11 MPa in Strata's ø16 bronze.
- **Nothing shows.** The heads are inside the sockets, and the sockets sit under the posts' collars.
- **Changed:** `components.json` (`post-fixings`, `post-sleeves`, `tie-rod-set`), the assembly note in `product.py`,
  Strata's posts in `variants/variants.py`, the RFQ's posts and sockets, and FAI D11, M1 and M4. **The keyhole's detail
  drawing is still to come.** The CAD still draws round sockets; the parts list and the RFQ describe the keyholes.

## 3. Heat in the abnormal case: the L-pad removed

**The audit's finding:** the L-pad can dissipate up to 30.6 W inside the sealed compartment, with the capacitor on the
resistors' plate. This file's arithmetic gives 25.6 W at the FA122's full 22.4 V.

**Two steps:**
- **First answer, superseded:** cap the HF channel at 10 V in the preset. It cost 7 to 8 dB of the horn's headroom
  (the coordinator's check).
- **The audit's own fix cannot be done:** the FA122's module fills its plate's inside face, leaving 16 and 18 mm
  margins, so the resistors cannot be sunk to the plate.

**The answer (the coordinator's suggestion, checked):** no L-pad. The 6 dB comes off in the FA122's DSP, and the 33 uF
series capacitor stays, stood off 3 mm.
- **Hiss:** the bare driver's is about 8 to 10 dB SPL at 1 m, inaudible.
- **Headroom:** the full 22.4 V is 31 W into the driver, within its 140 W rating, about 123 dB at 1 m.
- **Heat:** nothing in the compartment heats but the amplifier. In the abnormal case the heat is in the driver's own
  motor, in the pod.
- **Cost:** two resistors and a plate fewer (about $24).
- The comparison is in `compliance.md` 5.

## 4. The preset

- The same verified preset in **all three slots**: the 1 kHz LR4 crossover, the HF channel 6 dB down (there is no
  L-pad), a 28 Hz high-pass, the limiters at the drivers' ratings, soft clip on, the port notch, auto-standby.
- **Hypex's filter password** is set at the factory and recorded in the FAI file, not on the speaker (FAI E6).

## 5. FAI levels

- **M2:** a 20 Hz tone at 100 dB needs about 10.9 mm of excursion, against an Xmax of 5.75. It is now a static
  pressure decay at **200 Pa** with the ports plugged.
  - From the 15PR400's Vas 248.9 L and Sd 857 cm², Cms is 0.24 mm/N.
  - So 200 Pa moves the cone 4.1 mm, where 1 kPa would move it 20.5 mm.
  - The box must hold above 100 Pa for 30 s (est.; set on the first sealed sample).
- **M3:** a sweep from 20 Hz needs about 28.7 mm. It now runs from **35 Hz at 100 dB**, and from 30 Hz at 94 dB.

## 6. Parts and docs

| | was | now |
|---|---|---|
| Woofer screws | 15 N m (over an A2-70 M6's yield, about 9 N m); inserts tested at 2 x 15 = 30 N m | **5 N m**; inserts tested at 10 N m and a 2 kN pull (`m6-acrylic-inserts`, DETAILS.md, FAI M1) |
| Mains cord | none in the parts list | **NEMA 5-15P to C13, 2 m, 18 AWG SJT, UL listed** (`mains-cord-nema`, part `mains-cord`, the "other" RFQ) |
| FA122's plate | 10 holes in the model, 8 inserts bought | **ten inserts**, the pattern to be confirmed against Hypex's drawing (asked in the Hypex letter) |
| Amp box | 1.5 in the CAD; "6061" in the parts list and "5052 or 6061" in the RFQ | **1.5 mm 5052-H32** (6061 cracks at tight folds), in the CAD, the parts list and the RFQ |
| Crossover | 800 Hz and 1 kHz in different files | **1 kHz, LR4** in every file of this lane (README S6, the preset, `product.py`, `horn_sim.py`, `horn_plots.py`) |
| Horn depth | "170 mm" in README S6 | **278 mm** (170 was an earlier flare's) |
| Post load | "14 N" (`laminated-horn.md`) | **21 N formed, 28 N Strata** (`stability/horn.json`) |
| Ground loop | not documented | **the source to the master only, an S/PDIF isolation transformer in the link, never a mains earth-lift** (`compliance.md` 3) |
| Transit | none | **a reusable plywood crate on a skid base, the horn in its own carton, ISTA 3B** (`make/transit.md`). The speaker is 70 to 75 kg, not 62 |

## 7. The FA122's certification

There is no CB or UL report for the FA122 on file. The draft request to Hypex is `rfq/tropos/h-hypex/letter.md`.
Nothing has been sent; the owner sends it. The end product needs its own 62368-1 listing by an NRTL either way
(`compliance.md` 4).

**Regenerated:** the Cloud's parts list and drawings (`out-cloud/`), and the RFQ letters (`rfq/tropos/`).
