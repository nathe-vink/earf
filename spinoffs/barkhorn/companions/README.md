# The companions: a record player and a lamp in the Atmosphere acrylic (round 31)

The owner, 2026-10-18: "Let's work on a few more things now. Record player and lighting for one. All acrylic." In
round 17 the owner had also said: "If we can find a good recycled acrylic partner, we can make other components, like
record players, lights, etc." These are those two pieces. Both are in the Clouds' tinted cast acrylic and come in the
eight Atmosphere colours, and each is built with the fab kit the speakers are built with.

Status: **concept, built to the fab kit's standard: proposals until the owner signs them.** The speaker, its product
file and its CAD are untouched. The Cloud is built here only so that it can stand beside the companions in a shot.

| | **Cumulus**, the record player | **Bell**, the lamp |
|---|---|---|
| what | belt drive, the motor in its own pod, apart | table lamp, the horn's flare hung mouth down |
| size | 483 W x 373 D x 135 H (arm at rest) | 432 across the rim, 480 tall, foot 230 |
| acrylic | plinth 2 x 20 mm, platter 25 mm, pod 3 x 20 mm, feet 20 mm | foot 2 x 20 mm, shade formed from 5 mm (tinted 4x denser), stem tube 30 x 3 |
| weight | about 2.4 kg turning (platter and hub), about 9 kg in all | about 3.3 kg |
| parts list | **$2,775**, one off | **$563** + the LED strip (price not found), one off |
| product file | `turntable.py` | `lamp.py` |
| build | `out-turntable/` (cut files, drawings, parts list, checks) | `out-lamp/` |

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/turntable.py --out spinoffs/barkhorn/companions/out-turntable
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/lamp.py --out spinoffs/barkhorn/companions/out-lamp
    .venv-fab/bin/python spinoffs/barkhorn/companions/concepts.py      # the blockouts
    python3 spinoffs/barkhorn/companions/shots.py                      # the shot files
    PY=python3.11 spinoffs/barkhorn/companions/render_all.sh           # every shot (about an hour on 4 cores)

Both builds pass the kit's checks: no clashes, every sheet thickness in stock, every bought part in the library.
`components.json` beside them is the companions' own library. Its prices come from search snippets of 2026-10-18;
the pages themselves could not be opened from this environment.

## The concepts

Each concept is a quick blockout in the Clouds' acrylic on the look book's sweep (`concepts.py`; renders in
`renders/2026-10-18/barkhorn/companions/concepts/`). Each was judged on the same things: tinted cast acrylic; the speakers'
language (flat sheets, eased edges, cemented joints, the horn's soft curves); whether it is honest and buildable;
and whether it is sophisticated but witty.

![The concepts](../../../renders/2026-10-18/barkhorn/companions/concepts/sheet.png)

**Record player**

- **T1, the Slab.** Three 20 mm sheets cemented into a rounded rectangle, with the platter on top. This is how most
  acrylic turntables are made, and that is what's wrong with it: no one would know it was EARF's. Sixty millimetres
  of tint also go nearly opaque and muddy.
- **T2, Cumulus (picked).** The plinth is drawn the way the Atmosphere icons are drawn, from circles: one for the
  platter, one round the arm's pivot, one round the motor. The motor's circle has a hole in it, and the motor stands
  in that hole on its own feet, never touching the plinth. That is what a good belt drive does anyway (keep the
  motor's hum out of the arm), made visible. The joke is the cloud with a hole in it, and it is also the
  engineering, which is the brand's kind of wit. Two sheets keep the colour clear.
- **T3, the Mast.** A skeleton: the platter on a column of stacked discs, with the arm and the motor each on a pillar.
  It is striking, but three loose pieces on a shelf have to be set out by hand, and the arm must stay 222 mm from the
  spindle. That is a jig, not a product.

**Lamp**

- **L1, the Lantern.** The cabinet in small: five cemented 20 mm panels with an opal tube inside. It is honest and
  easy to build, but it is a box, and the cabinet already says that better.
- **L2, Edge.** One 20 mm sheet cut to the horn's section and lit from below through its edge. It reads as an
  award, and tinted edge light is dim.
- **L3, Bell.** The speaker's horn flare turned up to the ceiling, with the LED at the throat where the compression
  driver sits. That is the right idea, but upturned on a stem it reads as a trophy or a cocktail glass.
- **L3b, Bell turned over (picked).** The same flare hung mouth down from the top of the stem. Light pools on the
  table, the flare glows in its colour and deepens toward the rolled rim, and the light sits at the throat. The
  speaker plays sound out of its horn; this one plays light. It is a familiar lamp shape (a mushroom), so the
  horn's flare is what makes it EARF's.

## Cumulus, the record player

![Cumulus in the eight colours](../../../renders/2026-10-18/barkhorn/companions/look-turntable-sheet.png)

- **The plinth** is two 20 mm sheets cut as one outline and cemented with a two-part polymerising acrylic cement
  (as the cabinets are), then annealed. The outline is three circles: the platter's at 340, the arm's at 150 on the
  pivot, and the motor's at 136. The corners where they meet are R14, and every edge is eased R2 and polished. The
  cut files keep the square prism, and the easing is a note on each part.
- **The motor apart.** The pod is three 88 mm discs standing on three soft Sorbothane discs on the shelf, with a 4 mm
  gap all round to the plinth. The motor's lead goes down through the pod and out underneath, so nothing runs
  through the plinth.
- **The platter** is 25 mm of the same acrylic, 300 across. It weighs 2.1 kg, and 2.4 kg with its bonded brass hub
  (I = 0.024 kg m2, a little more than Rega's glass platters). The belt runs on its polished, crowned rim. There is
  no mat: acrylic is close to vinyl's own impedance, which is why acrylic platters exist.
- **The bearing** is turned for it. A brass housing runs through both sheets, its flange in a 6 mm pocket in the top
  on three M4 screws into bonded inserts. Inside are two sintered bronze bushes, and a ground stainless spindle (10,
  7.2 at the record) runs on a 6 mm tungsten carbide ball and a PTFE pad. The brass shows through the tint. I looked
  for a bearing sold on its own: Michell's inverted bearing is listed as discontinued, and Pro-Ject sells its
  bearing only with its platter. A lathe shop makes this one from a drawing (sheet 6 on).
- **Speed** comes from Rega's 24 V motor and Neo PSU MK2: 33/45 by a button, trimmed in 0.01 rpm steps, and the
  speed changes without moving the belt. The pulley is turned to the motor's measured speed. If it runs at 250 rpm,
  the belt face is 39.48 across for a belt on the 300 rim, which is close to 40.
- **The arm and cartridge** are Rega's RB330 at Rega's 222 mm and an Ortofon 2M Black (round 31b; the 2M Blue
  first drawn read as a stray blue accent on every colour, the lead's note). Moving magnet, so any phono stage; black
  in every colour. The 2M Red (red body) could ride on Ember.
- **The feet** are three 50 mm acrylic discs on M8 brass studs, each turned to level the platter, with Sorbothane
  under them. They are placed so the triangle holds the platter's centre.
- **The mark** is EARF, 44 wide, laser-etched in the arm's circle in front of the arm and filled with the colour,
  deeper. It is the only text on it.

| bought | source | price |
|---|---|---|
| Rega RB330 tonearm | [Safe and Sound HQ](https://www.safeandsoundhq.com/products/rega-rb330-tonearm) | $675 |
| Ortofon 2M Black | [Upscale Audio](https://upscaleaudio.com/collections/cartridges) | $749.99 |
| Rega 24 V motor upgrade kit | [HiFi Gear](https://www.hifigear.co.uk/rega-neo-mk2.html) | GBP 150 (~$200) |
| Rega Neo PSU MK2 (US, 60 Hz) | [Audio Advisor](https://www.audioadvisor.com/products/rega-neo-psu-mk2-60hz-turntable-psu-power-supply-black) | $445 |
| flat belt, 5 x 0.6, ~975 | a belt maker, cut to length | ~$25 (estimate) |
| sintered bronze bushes 10 x 14 x 12, carbide ball 6, PTFE pad | McMaster-Carr or a bearing supplier | ~$16 (estimate) |
| Sorbothane feet (3) and pod pads (3) | Isolate It / Sorbothane Inc. | ~$45 (estimate) |

The acrylic is $239 of the $2,775 and the turned parts (bearing, hub, spindle, pulley) $311. The rest is bought, and
the arm, the cartridge and the Neo are $1,870 of that.

![Cumulus beside Ember](../../../renders/2026-10-18/barkhorn/companions/hero-turntable.png)

![The motor apart](../../../renders/2026-10-18/barkhorn/companions/detail-turntable.png)

## Bell, the lamp

![Bell in the eight colours](../../../renders/2026-10-18/barkhorn/companions/look-lamp-sheet.png)

- **The shade** is formed (vacuum or drape) over a turned buck at about 160 C, then annealed. It has a flat collar at
  the crown, a R10 corner into the flare, and a rim rolled to R2.5, 420 across. The flare is the speaker's: it opens
  late, then rolls over. The sheet is 5 mm, so it is **cast four times as dense in the tint** as the cabinets' 20 mm,
  and reads the same. A caster makes any density. (At the cabinets' own tint, 5 mm is nearly clear: see the first
  proof.) The shade hangs by its collar, clamped between the hub's flange and the cap on a silicone ring with three
  M4 screws, so nothing presses on the formed wall.
- **The light** is 0.4 m of Waveform Lighting's CENTRIC WARM 24 V strip (95+ CRI, 450 lm a foot, 2700 K at full
  and dimming warm toward 2000 K, like a filament). It wraps twice round a turned aluminium hub, which is its heat
  sink, behind an opal acrylic sleeve so no dots show. That gives about 600 lm at full, a 60 W bulb's worth. I chose
  a strip round the stem over a single LED at the throat because the stem runs up the middle, and a strip lights
  the shade from inside all the way round.
- **Low voltage throughout.** A Mean Well 24 V wall adapter plugs into a 2.1 mm in-line socket. From there a clear
  18/2 cord goes into the foot's back, through the dimmer in the foot's pocket, and up inside the clear stem, where
  it shows. Nothing in the lamp is at mains voltage, which makes listing it simpler.
- **The foot** is two discs, 230 and 200, cemented. The dimmer's board sits in a pocket through the lower disc,
  closed by a 6 mm cover on four M3 screws, with six clear bumpers under it. **The knob** is on top at the front,
  turned from rod in the deeper colour. You turn the lamp up like a volume knob, which it nearly is. That is the one
  joke, and it is a quiet one.
- **The stem** is a cast acrylic tube 30 x 3, bonded into the foot's socket and the hub's bore.
- It holds about 1.7 kg in the foot and 1.6 kg in the head, and tips past about 28 degrees.

| bought | source | price |
|---|---|---|
| Waveform Lighting CENTRIC WARM strip, PN 3008.27 | [Waveform Lighting](https://store.waveformlighting.com/products/centric-warm-led-strip-lights), [datasheet](https://store.waveformlighting.com/cdn/shop/files/CS_3008.27.pdf) | reel price not seen |
| LEDSupply Single Color Mini Rotary Dimmer, 12-24 V PWM | [LEDSupply](https://ledsupply.com/led-dimmers/mini-rotary-knob-dimmer) | $8.84 |
| Mean Well GST25U24-P1J, 24 V 25 W wall adapter | [TRC Electronics](https://www.trcelectronics.com/products/mean-well-gst25u24-p1j) | ~$18 (the desktop GST25A24 is $19.42) |
| Satco/Nuvo 80-2374 clear 18/2 SPT-2 cord, 8 ft | [Lighting Supply](https://lightingsupply.com/products/satco-nuvo-80-2374) | $6.97 |
| 3M Bumpon SJ5302 clear, in-line DC socket, strain relief, fixings | any distributor | ~$20 (estimates) |

The turned and formed parts are most of the $563: the hub and cap ($114), the stem, sleeve and knob ($186), and the
shade ($139, with a tenth of a $900 buck, spread over a first run of ten).

![Bell beside Haze](../../../renders/2026-10-18/barkhorn/companions/hero-lamp.png)

![Under the bell](../../../renders/2026-10-18/barkhorn/companions/detail-lamp.png)

## The renders

The look book's frames come from the engine on the look book's sweep in each colour (lookbook21's key, fill and
wash), with the cabinets' own tinted-acrylic material: clear cast resin absorbing toward the colour after 25 mm.

- `look-turntable-<colour>.png` and `look-lamp-<colour>.png`: each product in each of the eight colours, the lamp lit
  (strip strength 88). On a bright studio sweep a lit lamp shows as its glowing sleeve, as real lamps photographed on
  a lit set do. `look-*-sheet.png` shows the eight together. Cumulus wears the black 2M Black in all eight.
- `detail-turntable.png`: the motor's pod in its ring, the belt to the rim (Ice). `detail-lamp.png`: from under the
  rim, the opal sleeve lit, the collar and cap (Acid).

**The heroes (round 31b).** The lead and the owner asked for campaign images for a $20,000 line: the companion the
subject, the speaker as context, a real setting with texture, Bell switched on. Both are now in one room at dusk:
oak boards, a Poly Haven plaster wall (beige_wall_001, 4k), a window at the left with the dusk sky outside, and Poly
Haven's scanned walnut cabinet (modern_wooden_cabinet, 4k) under the companion. Cumulus has Bell lit beside it.
Bell's light is three small lamps just outside its opal sleeve (an emitting strip that thin is all noise), hidden from
the camera and from reflections; `studio/engine/lights.py` gained that switch for point lamps.

They were judged by `critic/PROMPT-promo.md`, each pass a fresh blind critic given only the image, a short card
(`promo.py stage`), `critic/measure.py` and the prompt's text. Every pass's changes were applied unless they would put
the speaker inside the wall or change the product; `critic/LOG.md` here has every pass, and the replies are in
`critic/rounds/2026-10-18/promo-*.json`. The coordinator's stopping rule replaced 8.5 (no session reached it): stop
after two passes in a row gaining under half a point, then duel the best two blind.

| hero | passes (blind scores) | final | the duel |
|---|---|---|---|
| Cumulus | 5.0 (morning sun), 5.5, 5.5, 5.5 | `hero-turntable.png` (pass 3) | pass 3 beat pass 4, 6.0 to 5.0 |
| Bell | 5.0, 5.5, 5.5, 6.0, 5.0 | `hero-lamp.png` (pass 4) | pass 4 beat pass 5, 6.0 to 5.0 |

Honestly: neither is at the bar the owner set. The critics' last notes, for whoever takes them on: the wall still
outshines Cumulus and the grade is one warm red; the lower plinth crushes; the record reads as smoked glass (a vinyl
groove material would help); and the speaker beside each companion is either cropped to a coloured block or out of the
frame. The room is a box with one window; a deeper room (a corner, a second wall receding) is the next step.

**Final paths for the site** (`renders/2026-10-18/barkhorn/companions/`):

| colour | record player | lamp |
|---|---|---|
| Ember | `look-turntable-ember.png` | `look-lamp-ember.png` |
| Dust | `look-turntable-dust.png` | `look-lamp-dust.png` |
| Acid | `look-turntable-acid.png` | `look-lamp-acid.png` |
| Poison | `look-turntable-poison.png` | `look-lamp-poison.png` |
| Ice | `look-turntable-ice.png` | `look-lamp-ice.png` |
| Haze | `look-turntable-haze.png` | `look-lamp-haze.png` |
| Fog | `look-turntable-fog.png` | `look-lamp-fog.png` |
| Smoke | `look-turntable-smoke.png` | `look-lamp-smoke.png` |
| heroes | `hero-turntable.png` (Ember) | `hero-lamp.png` (Haze) |
| details | `detail-turntable.png` (Ice) | `detail-lamp.png` (Acid) |

The renderer's Python: the bpy wheel (5.0.1) is built for Python 3.11, and this container's `python3` is 3.13, so I
ran the renders with `python3.11` (`PY=python3.11 render_all.sh`). `studio/setup.sh` pins `bpy==5.0.1` on the
system `python3` and fails here. That is worth a line in setup.sh, but I didn't change it in this round.

## Open questions for the owner

1. **The names.** Cumulus and Bell are working names. The speakers are named for things in the air by colour, so the
   companions might take the colour's name too ("Cumulus in Haze").
2. **Recycled acrylic.** The formed shade and the 25 mm platter both need the casting partner (round 17's
   Plastiglas de México or Madreperla) to make the eight tints in 5 mm at four times the density and in 25 mm.
   Ask both.
3. **The cartridge.** Now the 2M Black ($749.99): black in every colour. A 2M Red on Ember only, or a moving coil
   (Hana) on all, are the alternatives.
4. **A dust cover?** None is drawn. A cover in clear acrylic hinged on the arm's circle is possible, but it would
   need a fourth circle in the plinth.
5. **The arm at rest** leaves the cartridge just past the plinth's front-right edge, as Rega's lift puts it. Should
   the arm's circle grow so the arm rests over acrylic?
6. **Listing.** The lamp is low voltage behind a listed adapter. The dimmer, once out of its housing, is not a
   listed part. For sale, a listed 24 V dimmer to fit the pocket. The record player's mains part is Rega's Neo, which
   is listed.
7. **The bearing** is made, not bought. Should we ask Rega or Pro-Ject for their bearing as a spare, or keep ours?
8. **Prices.** Neither has a selling price. At the speakers' multiple (round 15: $19,000 a pair against about $8,000
   of parts), Cumulus would sell for about $5,000 and Bell for about $1,400. These are for the owner to set.

## Round 32: the bar lamps (Moon, recommended)

The brief (the owner, 2026-10-19, through the coordinator): an acrylic table lamp and a hanging lamp for a bar, Planet
EARF first, and for sale. Three families were blocked out (`bar_lamps.py`, the sheet at
`renders/2026-10-19/barkhorn/barlamps/sheet.png`): F1 Block (rounded-square, squared), F2 Column (a lit cylinder),
F3 Moon (a frosted dome on a tinted column, and its pendant). **Moon is recommended**, F1 Block the alternative if
the owner wants the squared one.

Why Moon, for a bar:
- **It lights the table, not the eyes.** The light sits inside a frosted dome, above a seated guest's eye line in the
  table lamp and up a 46 mm baffle in the pendant (cut-off about 46° from the vertical). Nobody sees an LED.
- **It survives service.** The dome sheds a spill and the finial is round. The steel foot is sealed by O-rings
  (IP44, wipeable) and weighs about 1.5 kg, so a sleeve or an elbow doesn't tip it. It charges on a staff tray of
  six through gold rings, with no cable on the table.
- **It sells.** The cordless mushroom is the form bars already buy (Poldina, Bellhop, Panthella Portable), so the
  trade knows it. What is new is the material: a turned cast dome and a solid tinted column whose polished top
  glows, in the eight Atmosphere colours plus clear, frosted and smoked. The pendant is the same dome hung mouth
  down, so a room can be specified as one family.

Built as two fab-kit products, `moon.py` (geometry, parts, notes), `moon_table.py` and `moon_pendant.py`; checks pass:

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/moon_table.py --out spinoffs/barkhorn/companions/out-moon-table
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/moon_pendant.py --out spinoffs/barkhorn/companions/out-moon-pendant

| | table lamp | pendant |
|---|---|---|
| size | foot 120, 277 tall, about 1.9 kg | dome 200 across, disc 220, canopy 150 x 50, drop 600 (to cut) |
| light | warm-dim board 2200 to 2700 K, 2.5 W, about 200 lm; touch dimmer on the finial | 2700 K CRI 90 COB (Bridgelux Vero SE 10) on a Mean Well PCD-16-700B in the canopy (phase-cut) |
| power | 25 Wh (two 18650s), about 12 h at the bar setting; tray contacts or USB-C | mains, to be listed to UL 1598 |
| BOM, one-off shop rates | **$583** (`out-moon-table/bom.md`) | **$780** plus the listing (`out-moon-pendant/bom.md`) |
| BOM, a run of 200 (my estimate) | about $170 parts, $195 landed | about $180 parts, $205 landed, plus the listing spread over the run |
| target retail | **$450 to $495** (trade at 30 % off) | **$695 to $750** |

The one-off BOM is mostly the lathe (the turned dome alone is $212 in the table lamp and $344 in the pendant, and
the brass canopy $229). At volume, four changes bring it down:
- the domes cast in a mould and finished on the lathe, not turned from block;
- the brass parts turned in a batch;
- a spun canopy in place of a turned one;
- the foot cut from steel bar.

The run figures are my estimates, not quotes. At about $195 landed, $495 retail is about 2.5 times cost, thin once
the trade discount is taken off. The dome is where the cost has to come out. The benchmarks are about $300 to $500 for
a cordless bar lamp and $600 to $1,000 for a designer pendant; check them before setting a price. The prices are the
owner's to set.

**For Planet:** `studio/engine/kit_ext/earf_moon.py` places either lamp from its fab-kit model (the GLBs in
`out-moon-*/render/`, committed for this) with materials in any flavour and its light set up as Planet's loft does
(commit f7c99a4):
- the lamp is a point light inside the dome, hidden from the camera, from transmission and from glossy rays;
- the frosted dome glows by itself (`shade_glow`).

    {"kind": "kit", "shape": "ext", "module": "earf_moon", "fn": "table", "spots": [[x, y, z_table]], "flavour": "smoked"}
    {"kind": "kit", "shape": "ext", "module": "earf_moon", "fn": "pendant", "spots": [[x, y, z_rim]], "ceiling": 3.2, "flavour": "smoked"}

Other parameters:
- `lamp_w`: the power (default 4 for the table lamp, 14 for the pendant);
- `lamp_k`: the colour temperature (2700);
- `shade_glow`;
- `materials`: overrides;
- a spot can be `{"position", "flavour", "rotate_z"}`.

`lift_shot.py`'s `glow:lamp_w=2` scales the lamp's power. The frames in `renders/2026-10-19/barkhorn/moon/` are made
with this same piece (`moon_shots.py`), so they test exactly what Planet imports.

The frames (`renders/2026-10-19/barkhorn/moon/`):

![Moon](../../../renders/2026-10-19/barkhorn/moon/sheet.png)

The critic (`critic/LOG.md`) ran three blind rounds on the smoked bar hero: 5.5, 5.5, then 6.0. Three rounds is the
family's limit, so I stopped there. Open on the hero:
- the smoked column still reads dark (its tint is dense);
- the pendant's underside clips, and the pendant is out of focus at f/2.8;
- the concrete shows no boards (the Poly Haven wall is smooth);
- the grade is all orange at a 3600 K balance.

A photographed hero would fix these. The shapes and finishes are fine.

**Warmth** (the coordinator: the dome read lavender-white in the bar frames). The cause was the neutral tints' own
glow, #FFB878: near white once a 3000 K balance takes it back, and pale enough to clip. It is now a warm ivory,
#FF9A50, in the products' flavours (`bar_lamps.VARIANTS`, rebuilt), so Planet gets it by default. The bar frames
also balance at 3600 K, as bar photography does, so 2700 K reads warm, not white.

**F1b, Block lit low** (`f1b.py`, kept ready in case the owner picks the square):
- the table lamp: F1 Block's tinted rounded-square block over a frosted lower sleeve, 22 to 130, with a hidden light
  inside it at 100, so the frost glows and lights the table around the foot; a steel shadow line between the two;
- the pendant: the same split, with a frosted band round the mouth, the block above, and the light 120 up inside
  (a cut-off of about 32°).

It is rendered in Moon's two bar frames (`renders/2026-10-19/barkhorn/f1b/`, beside Moon in `beside-moon.png`). These are blockouts: if the owner picks
it, it gets Moon's treatment (fab-kit products, a BOM, a kit piece).

Still open:
- the listing cost;
- the board (to make; a TI BQ25895-class charger with a touch dimmer);
- whether bars want the tray of six as its own product;
- the canopy in brass or blackened steel to match Planet's steel.
