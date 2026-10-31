# Core v1, plug-in first: an option note (round 43, 2026-10-31)

**A proposal only. The product decision is the owner's.** It answers `boards.md`: Core's own board (charger,
per-cell switching, touch, warm-dim driver) does not exist yet and needs about 4 to 6 engineer-weeks [E]. This note
weighs launching Core without its cells, on bought parts only, and bringing the battery back in a v2.

**In short:** a plug-in Core needs no board of ours. It drops the three hardest certification items (the cells under
UL 153 Supplement SA, DOE battery-charger testing with the MAEDbS listing, and lithium shipping), and it can be built
for the debut from parts bought in the next two weeks. It costs cordless use at launch, and the touch ring loses its
listing story (below). The shell, the ball and the base stay as drawn; the battery comes back as a part that fills the
same bay.

## What changes physically

| Part | Now (round 41/42) | v1 plug-in |
|---|---|---|
| **Cell bay** (three 18650 holders round the LED, behind the hatch under the base) | three LiFePO4 cells | **holds the bought electronics**: the LED's constant-current module and the dimmer (or touch) module on a small aluminium plate where the holders were. The hatch, its O-ring and its four captive screws stay. |
| **Ballast** | steel ballast 0.17 kg + cells 0.12 kg | **steel 0.29 kg**: a ring in the cells' place, so the weight (about 1.46 kg) and the tip angle (about 43°) stay [computed, to check] |
| **LED** | a two-channel warm-dim module, our board mixing 2200 and 2700 K | a **single-channel dim-to-warm COB**, which warms by itself as its current falls (candidates below). No mixing, so no board. |
| **Control** | capacitive touch on the black ring, through our board | **(a)** a bought touch-dimmer module wired to the ring (tap on/off, hold to dim), or **(b)** an in-line dimmer on the cable. The ring stays in both; in (b) it is only trim. |
| **Power in** | sealed USB-C in the base, a 20 W USB-C adapter and a 2 m fabric cable, out of a notch underneath | **a listed Class 2 24 V adapter** and a 2 m black fabric cable, into a sealed DC jack in the same notch; or keep USB-C with a PD source at 20 V (see "Power routes") |
| **Cable exit** | the notch underneath, at the back | unchanged |
| **Labels** | the hatch's "LiFePO4 18650 only" | "No user-serviceable parts" on the hatch; the rating label names the adapter |

### Power routes

1. **24 V barrel (recommended for v1):** a listed Class 2 / LPS 24 V desktop or wall adapter, a sealed panel DC jack,
   a bought constant-current buck module (Mean Well LDD-350L class, PWM-dimmable) to the COB. The simplest chain and
   all off-the-shelf.
   - **Check the adapter's listing class.** Mean Well's GST18A24-P1J is listed by distributors as Class I with an
     earth pin, and no source found here confirms Class 2 or LPS ([Future Electronics](https://www.futureelectronics.com/p/electromechanical--power-supplies--ac-dc/gst18a24-p1j-mean-well-3062461),
     [RS](https://uk.rs-online.com/web/p/ac-dc-adapters/1176114)). Choose an adapter whose label says Class 2 and
     LPS, Level VI.
2. **Keep USB-C:** a listed USB-C PD adapter of 30 W or more (a 20 V profile), and a bought PD trigger module at 20 V
   before the constant-current module. This keeps the port v2 will use, but adds a module and depends on the COB's
   forward voltage sitting under about 19 V. Check that before choosing it.

## Candidate parts (bought; listing to confirm)

| Function | Candidates | Source | Note |
|---|---|---|---|
| **Dim-to-warm LED** | Luminus CubePower Dynamic COB, warm dimming (CDM-9 class, 3000 → 1800 K, CRI 90 or 97; -DW01 halogen-like or -DW02 linear curve) | [Luminus datasheet (Mouser)](https://www.mouser.com/datasheet/2/245/Luminus%20Devices-7-27-2017-CDM_Prelim-1177391.pdf); [chipdip listing, CDM-9-3018-90-36-DW02](https://www.chipdip.ru/product0/8004740880) | "compatible with most single channel drivers and dimmer switches", as Luminus describes it. The best fit. |
| | Bridgelux Vesta Dim-to-Warm arrays (1800 → 2700 K, or 1800 → 3000 K) | [Digi-Key BXRV-DR-1827G-0600-A-13](https://azcus.digikey.com/en/products/detail/bridgelux/BXRV-DR-1827G-0600-A-13/12317823) | the Bridgelux family Hemisphere already uses; datasheet not read |
| | OSRAM PrevaLED CoB D2W (2700 → 1800 K) | [RS 2422266](https://za.rs-online.com/web/p/cob-leds/2422266) | larger; check the size against the 30 mm window |
| **Constant-current module** | Mean Well LDD-350L (or -300L), DC-DC buck, PWM and analog dim input | Mean Well LDD datasheet (not read here) | **Bench test:** a dim-to-warm COB warms with *average* current. Confirm it shifts colour under the module's PWM dimming as it does under analog; if not, use the analog input. |
| **Touch (a)** | a 12–24 V DC touch dimmer module (tap on/off, long-press dims), e.g. the RL-DIM-1-B kind | [a marketplace listing](https://plastiquealaloupe.fondationtaraocean.org/products/1pcs-dimmable-led-touch-dimming-switch-controller-dc-12v-24v/213661727/) | **no listing claimed.** No UL-listed DC touch dimmer was found. Inside a Class 2 circuit the lab may accept it as a component evaluated in the lamp; ask. |
| **In-line dimmer (b)** | Allanson ACL-12/24V-DMR (for 12/24 V Class 2 supplies, 0–100 %, 5 A) | [Allanson datasheet](https://allanson.com/wp-content/uploads/Allanson-Dimmer_ACL-12V-DMR-21-273-2.pdf) | its listing is not stated in what was read. Waveform's FilmGrade dimmer (Mantle's, 25 kHz) is the flicker-free alternative at about $80. |
| **Adapter** | a 24 V, 15–18 W, Class 2 / LPS, Level VI desktop or wall adapter | to choose | the lamp draws about 3 W, so 15 W is plenty |

**Note on the touch.** The ring's tap-and-hold is part of Core's character. A bought touch module keeps it but carries
no listing. An in-line dimmer is listed more easily but makes the ring decorative. **Recommendation: (a) the touch
module**, with the lab asked early whether a module inside a Class 2 circuit needs its own listing. If the lab
refuses it, fall back to (b) for the debut batch.

## What it removes from certification

| Item | Battery Core | v1 plug-in |
|---|---|---|
| UL 153 **Supplement SA** (battery-operated portable luminaires), the cells' UL 1642 / UL 62133-2, the wrong-cell fault tests | required | **gone** |
| **DOE battery-charger standard** (10 CFR 430.32(z), Appendix Y) and the **California MAEDbS** listing (20 CCR 1606) | required, tested as a system | **gone.** The adapter is an external power supply: its own DOE Level VI marking and its maker's listing cover it. Buy one already in MAEDbS. |
| **UN 38.3 / UN3481** shipping, the PHMSA "connected to a board is a battery" question | required | **gone** |
| Battery stewardship (California AB 2440), EU 2023/1542's replaceable-battery rule | apply | **gone** |
| **UL 153** (portable luminaire, cord-connected, a listed Class 2 supply) | required | **stays**, simpler: a SELV lamp behind a listed adapter |
| **FCC Part 15 Subpart B** (unintentional radiator: the PWM dimming and the touch module) | required | **stays**: an SDoC with a radiated and conducted emissions test |

## What it saves

- **Engineering:** the board's $16k–40k [E] and 4 to 6 weeks (`boards.md`). In its place: about **2 to 4 days** [E]
  to pick the parts, bench-test the dim-to-warm under the chosen dimming, and design the aluminium plate that holds
  the modules in the bay.
- **Certification:** the Appendix Y test and the MAEDbS filing (the BACL request in `lab-rfq/bacl.md` asks for these), Supplement
  SA's battery tests and the UN 38.3 paperwork. Several thousand dollars and a few weeks of lab time [E]; the lab
  quotes in `lab-rfq/` give the real figures.
- **The first article's electronics: about $45–70 [E]** a lamp: the COB $10–20, the constant-current module about $8,
  the touch module about $5 (or the dimmer $9–80), the adapter $12–18, the jack, wiring and plate about $10. The
  battery Core's are about $70 (board $34, cells $9, holders $4.50, LED $9, adapter $7, plus test pads and NTC), and
  that is before the engineering.
- **Time:** every part can be bought in the week of 2 November and wired in a day. The debut no longer depends on a
  board arriving over the holidays.

## What the owner gives up

- **Cordless at launch.** Core's line is "one product, plugged in or not". For v1 it is plugged in only, and the bar
  use on a table without a socket waits for v2.
- **The ring's listing story,** if the touch module isn't accepted (above).
- **The particulars change:** the battery, charger, shipping and runtime rows go; the power row names the adapter. The
  site's copy that says "on its own cells" changes for v1.

## How the battery comes back in v2, with the shell, base and ball unchanged

The cells already live in the **base's bay behind the hatch**, not in the ball. So v2 is a change of what's in the
bay:
1. **v1's bay holds a plate with bought modules; v2's holds the three cell holders and the real board** (the same
   footprint, the same four screws). The ball, the base's acrylic, the chassis, the hatch and the notch don't change.
2. **Keep v1's ballast as two parts:** a steel ring that stays, and a 0.12 kg steel insert where the cells go.
   v2 removes the insert.
3. **Use the same input in both:** if v2 will charge by USB-C, choose power route 2 (USB-C at 20 V) for v1 now, so the
   socket and the notch don't change; or accept a new hatch-side jack plate in v2.
4. **Upgrades.** A v1 owner could be offered the v2 "power base" kit (the plate, cells and board, fitted by EARF or
   by the owner behind the hatch). It would need its own certification as a kit; quote it later.
5. **The earlier cartridge idea is the other route.** Before round 35, Core was a plug-in lamp with a separate battery
   cartridge (`components.json`: `orb-cartridge`, a pouch cell in a housing on five pogo pins, magnets and a detent).
   If the owner would rather not have user-replaceable 18650s at all, the cartridge is a v2 that also keeps the shell,
   ball and base. It needs a port in the base's underside.

## Recommendation

- **For the January debut: v1 plug-in.** Bought parts in the week of 2 November, bench-tested by 9 November (the
  dim-to-warm under the chosen dimming, and the temperature in the closed bay at 3 W), lamps assembled with the balls
  in early January. The debut no longer depends on the board or on the evaluation-kit fallback.
- **For a first batch of about 50: v1 plug-in, with UL 153 and FCC 15B on the plug-in build.** Start the battery board
  in parallel, without the deadline, for a v2 about three to six months later. A v1 sold now becomes a v2 later through
  the bay, not a new lamp.
- **If cordless at launch matters more than the date,** keep the battery Core and hire the engineer this week
  (`boards.md`). The debut's Cores then run on the evaluation-kit fallback.

**For the owner:** v1 plug-in for the debut and the first 50, or the battery Core with an engineer hired now.
