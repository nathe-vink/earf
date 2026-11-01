# Mantle in the owner's darker stock tints, and the shared audit fixes (2026-11-01)

The owner, about 10:55 UTC on the decision board (r46-owner-notes 8832050e): "I like the darker colors. Go for smoke
render. Not sure about mantle." No Mantle design is picked. The line now uses stock cast sheet's own tints (r33-speaker-horn
`spinoffs/barkhorn/asset/tints-trucast.json`): each code's TruCast TT (total transmission) held at its own 1/2 in
sheet. The lighter custom pours of round 48's color pass are no longer the line's look. Everything below is a
proposal until the owner signs it.

## 1. The renders (`renders/2026-11-01/barkhorn/mantle-r48/`)

Each design is shown as the owner last saw it, on the same light and camera:
- **A, Strata Float v3**: the satin deck edge (the strata-v3 r2 rigs). Its base is now in the line's Smoke, 2074 Dark Gray.
- **B, Outcrop**: the outcrop custom rigs, every stratum in the stock tint.

| sheet | A | B |
|---|---|---|
| `sheet-studio-ember-2423.png` | `a-studio-ember-2423.png` | `b-studio-ember-2423.png` |
| `sheet-studio-poison-2092.png` | `a-studio-poison-2092.png` | `b-studio-poison-2092.png` |
| `sheet-dusk-ember-2423.png` | `a-dusk-ember-2423.png` (its base loop lit) | `b-dusk-ember-2423.png` (Outcrop has no light of its own) |

Each frame is 1800 x 1200, 80 samples, on the rigs the owner last saw. One-line reads (mine, not a critic's, as asked):
- **A, studio, Ember:** a deep oxblood slab. The red shows where light comes up through the gap and along the satin edge;
  the Smoke base and stainless posts recede, as meant. The most "colored" of the six.
- **B, studio, Ember:** a black glossy stepped block. The red is only the top lamina's rim and a flare in the reflections;
  the parts inside are gone (section 2's 0.09 %).
- **A, studio, Poison:** a near-black slab with a bottle-green glow at its back corner; it reads as dark green glass, not
  black plastic, but only just.
- **B, studio, Poison:** black. Nothing says green except a faint cast in the top's reflections. Stock Poison does not work
  for Outcrop.
- **A, dusk, Ember:** the float is the picture: the warm loop under the base, the posts and feet lit, the deck a dark red
  plane above. The Smoke base's long edge reads pale cyan-gray where the loop lights it end-on.
- **B, dusk, Ember:** a black block in a dark room. With no light of its own, the stock tint leaves nothing to see but
  the arm, the record and the steps' highlights.

In short: in stock deep tints, A still reads as colored glass with its light carrying it at dusk, and B reads as black.
B needs the custom deck lot of section 2 to be the design it was drawn as.

## 2. What goes near-black in stock, at each part's thickness

Luminous transmission top-down through each part (or along the path named), from each code's TT held at 12.7 mm with
two surfaces' 7.7 % Fresnel loss out and back in, Beer-Lambert in between:

| part (path) | Ember 2423 | Poison 2092 | Haze 2287 | Smoke 2074 | Ice 2069 | Dust 2422 |
|---|---|---|---|---|---|---|
| Strata v3 deck, top-down (2 x 12.7) | 2.2 % | 3.7 % | 2.0 % | 1.5 % | 35.9 % | 37.8 % |
| Strata v3 base (1 x 12.7) | 14.1 % | 18.6 % | 13.5 % | 11.7 % | 57.6 % | 59.1 % |
| platter (21) | 4.1 % | 6.5 % | 3.8 % | 3.0 % | 42.3 % | 44.2 % |
| Outcrop deck, top-down (47.1) | **0.09 %** | **0.2 %** | **0.07 %** | **0.04 %** | 16.1 % | 17.7 % |
| Outcrop cover top (5.6 + 3) | 25.9 % | 31.2 % | 25.1 % | 22.8 % | 67.1 % | 68.2 % |
| Outcrop cover wall, seen through (2 x 10) | 4.8 % | 7.4 % | 4.5 % | 3.6 % | 43.9 % | 45.7 % |
| any deck edge-on, 100 mm in | 0.00 % | 0.00 % | 0.00 % | 0.00 % | 2.3 % | 2.8 % |

Below about 3 % a part reads as black glass: you see its surface, not into it.

- **Outcrop's deck goes black** in every deep code (0.04-0.2 %). In stock Ember, Poison, Haze or Smoke it is a stepped
  black block with colored edges where the light is short. The idea of seeing the bearing and motor inside is lost.
  **A custom pour rescues it:** a deck lot at about 45-50 % TT per 1/2 in passes about 9-12 % through 47 mm, and the
  cover's rings and the platter can stay stock. That is one custom lot, for the deck's three 12.7 sheets.
- **Strata's deck is at the edge** in the deep codes (1.5-3.7 %). It reads as a deep, glossy colored slab with the
  arm and record on it. The parts under it show only where the light comes up through the gap. It does not need
  rescuing to be handsome. To read as "glass", a custom pour for its two sheets at about 35-40 % TT per 1/2 in gives
  about 12-15 % through 25.4.
- **The bases** (Strata's 12.7 Smoke 2074, 11.7 %) are fine dark. They were meant to recede.
- **The platters** in the deep codes (3-6.5 %) read as dark discs under the record. That is fine; it is a record player.
- **Ice 2069 and Dust 2422** are light enough in stock for every part.

## 3. The shared audit fixes (ENGINEERING-AUDIT.md on r46-owner-notes, "Mantle: not yet sound")

These are the items both designs share, because both use the same bought drive. Strata-only items (its rear panel,
its LED slot) and Outcrop-only items (its S2 tunnel, its tripod) wait for a pick.

Both product files now carry these fixes in their geometry, parts and notes (`mantle_outcrop.py`, `mantle_strata_v3.py`,
`components.json`). They were rebuilt with fabkit after the renders in section 1, so those frames show each design as
the owner last saw it. Both rebuilt with 0 clashes:

| | before | after | what changed in the parts list |
|---|---|---|---|
| Outcrop (B) | $3,773 | $3,851 | 440C spindle, disc spring and washer, platter inserts, motor screws in place of grommets, 4PDT |
| Strata Float v3 (A) | $3,800 | $3,877 | the same |

### 3.1 The drive ratio: bench it before the pulley is turned

The files sized the pulley for the motor at 250 rpm (50 Hz). If the US Neo PSU MK2 drives Rega's 24 V synchronous
motor at 60 Hz, it turns at 300 rpm, and a 39.5 pulley spins the platter at 40 rpm. At 300 rpm the pulley is
2 x (150 + 0.3) x 33.333 / 300 - 0.6 = **32.8 mm**. Plan:
1. Run the motor with its board on the actual US Neo (115 V 60 Hz mains), with no load and then with a dummy load: a
   flywheel on the pulley shaft at about the platter's drag, 0.05 N m.
2. Measure the shaft at 33 and at 45 with a laser tachometer (0.1 rpm resolution), 10 minutes warm, three runs. Read
   the Neo's output frequency on a scope at both settings.
3. Turn a test pulley at the computed diameter in aluminum. Put the platter on with its belt, and read speed with a
   strobe disc and a test record's 3150 Hz tone (the W&F meter app is enough for a first look).
4. Trim with the Neo's 0.01 rpm steps. If the trim needed is more than ±1 %, re-turn the pulley, then turn the final
   one in the finish.

`rpm_motor` stays a PROPOSAL until step 2.

### 3.2 The bypass switch: 4PDT, not DPDT

With a DPDT switching only the outputs, the cartridge sees the S2's 47 kΩ input in parallel with the outboard phono
stage's 47 kΩ: 23.5 kΩ, which dulls a 2M's top end. The fix switches both the input and the output, so that in bypass
the S2 is out of circuit:
- a **4PDT** toggle (C&K 7411 kind: gold contacts, rated for signal); or
- two DPDT signal relays (Omron G6K-2 kind) on a small board, driven from the same toggle.

The toggle is the simpler and quieter choice. In `components.json`, `back-hardware` changes to the 4PDT.

### 3.3 The bearing

- **Oil volume.** The space below the fill line is about 1.2 ml: the bore 14, less the spindle, the ball, the plate and
  the bushes. **Fill 1.0 ml**, not 2.5. A full 2.5 ml would be pushed out past the upper bush when the spindle goes in.
- **A vent.** The spindle goes into a blind bore. Grind a vent flat along the spindle, 1.0 x 0.3 mm, the full length
  of the journals, so air leaves as the spindle drops and the oil isn't pumped. Pro-Ject and Rega bearings do the same.
- **The spindle's material.** It was 304 in the parts list and 440C on the drawing. It is **440C, hardened to 58 HRC and
  ground**: a soft 304 journal would gall in bronze. The kit's `stainless` (304) gives way to `stainless-440c` in both
  product files.
- **The clamp's preload over temperature.** Acrylic expands 70 µm/m K and brass 19. Through Outcrop's 47.1 mm stack,
  20 K moves the clamp 48 µm. The stack under the nut (936 mm² of acrylic) is about 64 kN/mm stiff, so the preload
  swings about 3 kN: crazing when hot, loose when cold. **Fix:** one DIN 2093 series C disc spring, **63 x 31 x 1.8**
  (it has to pass over the M30 housing; a 31.5 x 16.3 cannot), under the nut on a brass washer 64 x 31 x 3. Set it to
  about 1.5 kN by angle, about 1.2 mm of its 2.35 cone. Its rate, about 1 kN/mm, is now in series with the acrylic,
  and the same 48 µm moves the preload by about 0.05 kN. Strata's 25.4 mm deck moves half as far. The washer spreads
  1.5 kN over 2,460 mm² of acrylic: 0.6 MPa. Outcrop's counterbore under the deck grows from 48 x 10 to 66 x 14 to take
  it. Strata's nut hangs in the float's gap, so it needs no cut. Confirm the spring's load and rate in the maker's table
  (Schnorr or Mubea) before ordering.

### 3.4 The feet: drop the isolation claim

On Sorbothane pads this small, the feet sit near 50 Hz (Outcrop) to 190 Hz (the audit's figure for stiffer pads). Either
way they do not isolate in the band where speakers feed back (25-40 Hz), and over 1.4 f they barely help. **Claim only
that they locate and level the deck.** If isolation is wanted, it is a separate platform under the record player, at
3-5 Hz. The README's feet line is changed to say so.

### 3.5 The lid (Strata) and the cover (Outcrop) against the real RB330 counterweight

The kit's arm is an envelope. The real RB330's weight sits further back for light cartridges. Its maker's drawing was
not reachable from here.
- **Strata Float**: the lid's back wall clears a 40 mm weight up to about 65 mm behind the pivot. At 75 mm the weight
  would reach 5 mm past the deck's back edge, into the lid's wall.
- **Outcrop**: the cover's top rings clear a 40 mm weight up to about 65 mm behind the pivot. At 75 mm it touches the
  inner face of the ninth ring.

**Check** on the first arm in hand with the 2M fitted and balanced. If it does not clear, Strata's deck grows 10 mm
deeper, and Outcrop's top two rings narrow from 10 to 6.

### 3.6 The motor mount: Rega's method

Rega fixes its 24 V motor rigidly to the plinth (its kit's mount, screwed down) and relies on the motor's low
vibration and the hand-tuned board. It does not suspend the motor. Both designs drop the three grommets: Rega's mount
is screwed to the motor plate, and the plate to the pocket's shoulder, on three M3 screws into brass inserts. The
belt's own compliance does the decoupling.

### 3.7 The platter screws: off the acrylic

Six M4 button heads in 8 mm counterbores put 13-42 MPa on the acrylic under their heads, at 1-2 N m. That is high
enough to craze. Reverse them:
- six M4 brass threaded inserts, bonded into the platter from below (8 long, 5.6 OD);
- the screws come up through the hub's flange into them, so each head bears on brass;
- torque 0.6 N m, and **no thread-locker anywhere near acrylic** (its solvents craze it).

The acrylic then bears on the hub's 70 mm flange: about 2,600 mm² for six times 750 N, under 2 MPa. The record side of
the platter has no screws.
