# Strata's base: A, a stepped plinth, and B, outrigger feet (2026-11-01)

**The owner chose A, lit from underneath** (2026-11-01: "can we make them light up from underneath? If so I'd go with
the one on the left"). B is kept below as the alternative drawn; the blind duel between them was not run.

**Why:** IEC 62368-1 8.6.2.2 pushes at the horn's top with 20 % of the weight. The speaker passes only if its center
of mass sits at least 0.2 x that height inside every tipping edge (`stability/README.md`). On today's feet, Strata
fails by 24 % forward, 34 % back and 12 % sideways. The fix is geometric: the feet's centers at about 600 x 600 mm.
Both proposals put four M8 levelling feet at the same points: **x -25 / 585 and y -94 / 526** in the Cabinet's frame
(the cabinet is 560 x 420, its front at y 0), that is, about 300 mm from the center of mass each way.

The CAD is `variants/variants.py`: `PLINTH` and `OUTRIG`, the options "Plinth" and "Outriggers". The shots are
`campaign/shots.py`: `base-plinth`, `base-outriggers` and `base-today`, each with a `-34` three-quarter view.

## A. The stepped plinth

**The design:** three frames of the cabinet's own 1/2 in stock sheet, stepping out under it like the caldera and the
horn's terraces:
- 600 x 460 under the cabinet;
- then 630 x 566;
- then 660 x 670 on the floor;
- each a frame about 80 to 155 mm wide round a 440 x 300 opening;
- the outside edges polished, the three bonded;
- the cabinet bolted down through its own feet's M8 inserts.
It lifts the cabinet 38.5 mm.

| | |
|---|---|
| footprint (the feet's centers) | 610 x 620 mm; the base itself 660 x 670 |
| weight | **10.4 kg** (computed from the CAD), so the speaker with the flush horn is **84.6 kg** |
| cost, a speaker | about $260 of sheet ($0.03/cm3) + about $250 of cutting, polishing and bonding + $18 of feet: **about $530** (est.) |
| the push | 166 N (20 % of 84.6 kg) at 1.336 m: the arm needed is 267 mm |
| margins (the feet's centers) | **forward +19 %, back +14 %, sideways +14 %** (computed: `stability/com.json`, `strata_plinth`; the flat underside, rerun 2026-11-01 after the reveal was dropped) |

## B. Outrigger feet

**The design:** four arms of bronze bar, 30 x 20, the same bronze as Strata's posts:
- each from under one of the cabinet's corners (two M8 into inserts in the bottom: its foot's own and a second) out
  on the diagonal to a foot;
- the ends rounded, the bar's faces satin.
It lifts the cabinet 20 mm.

| | |
|---|---|
| footprint (the feet's centers) | 610 x 620 mm; the arms reach about 75 mm past the sides and 95 to 105 past the front and back |
| weight | four arms about 1.24 kg each, 4.95 kg, so the speaker is about 80.2 kg (est.) |
| cost, a speaker | about $70 of bronze ($0.12/cm3) + about $200 of machining and finishing + $18 of feet: **about $290** (est.) |
| the push | 157 N at 1.325 m: the arm needed is 265 mm |
| margins | **forward +19 %, back +15 %, sideways +15 %** (est.) |
| each arm | at the tipping point a foot carries up to about half the weight, 390 N. 110 mm outside the cabinet, that is 43 N m on a 30 x 20 section: about 22 MPa, against bronze's 125+ MPa yield |

## Both

- **They pass with margin, each way.** Anchoring stays a lab question for the January pre-check, not a design option.
- **They are drawn on Strata;** the smooth horn sits on either.
- **They change the look.** The owner chooses, after a blind duel judged on looks alone (the critic sees no
  stability numbers).

## The base reopened: a slim light plate, or no base (2026-11-03)

**The owner, 2026-11-03 03:10:** "I'm also not loving the footing on the speaker. Why is it that we need it? ... Or a separate base that people can optionally purchase?" And at 04:27: the light "should cast up through the speaker. Off in the day, on in night images. But I'm also not convinced we need it."

**Why the wide plinth was drawn, and why it is not needed:**
- It was drawn for a 20 % push at the top, which Tropos fails on its own feet.
- That rule is the 2014 text and IEC 60950's. Under IEC 62368-1:2018/2023, Tropos (MS3, no front controls) needs a 10° tilt and 800 N on its top.
- **Horn A passes both on its own feet:** it tips at 17.5° at the least, and the 800 N load passes 4.1 times over (`stability/standard-2018.md`).
- A base becomes optional. A lab's written pre-assessment confirms this before anything is tooled.

**The slim light plate** (option "Light plate", `LPLATE` in `variants.py`), sold separately:
- **Footprint:** the cabinet's own, 560 x 420; **50 mm tall** to the cabinet's bottom.
- **Top frame:** 1/2 in sheet in the cabinet's colour, round a 440 x 300 opening, grooved for the uplight's edge strips under the walls.
- **Tray:** black anodised aluminium (2 mm, folded and welded), holding the centre panel's board and heat sink on nylon brackets, slotted round its floor to vent.
- **Feet:** four M8 levelling feet, 20 mm in from its corners.
- It carries the uplight as the plinth did (the edge strips and the 40 W centre panel), with the bottom-batt window.
- **Mass:** about **5.3 kg**: 4.4 kg modelled (the frame 1.3, the tray 1.5, the heat-sink plate 0.7, the diffuser 0.4, the feet 0.3, the channels 0.2), plus the heat sink's fins, the board and the wiring.
- **Cost, a speaker (est.):** the frame about $170 (sheet and cutting, grooving, polishing), the tray about $140, the feet $18, and the uplight about $246 (strips $46, channels $18, board and heat sink $120, controller $22, the 90 W supply $40): **about $570**.
- **Heat, at full in a 25 °C room** (estimates, to check with thermocouples):
  - The tray is a tighter cavity than the plinth's opening: the heat sink runs about 20 to 30 K over room, 45 to 55 °C, or about 65 °C if it breathes poorly.
  - The acrylic frame screwed to the tray runs about 40 to 45 °C (50 °C in the poor case).
  - **Margin: 30 K or more under PMMA's 80 °C**, about 20 K under its 70 °C long-term limit, in the poor case.
  - Tighter than the plinth's 35 to 40 K. At the default 50 % the rises halve, so I would cap the panel at 75 % on the plate if the first plate's thermocouples read near the poor case.
- **Stability on the plate** (8.10, as a stand Tropos is sold with): 78.2 kg (5.6 kg taken for the plate, conservative). It tips at **17.8°** back at the plate's feet centres (19.6° at its edges), 20.8° forward and 25.6° sideways, so it passes 8.6.5 by the 15° tilt and 8.6.3 at 15°.
- **The frames for the owner** (`renders/2026-11-03/barkhorn/base-question/`, one camera, Ice, 1200 x 1500, 64 samples):
  - `A-ice.png`: on its own feet, day, no light;
  - `B-ice.png`: on the plate, night, the light up through the cabinet;
  - `C-ice.png`: on the stepped plinth, night, the same light;
  - `B-smoke.png`: Smoke on the plate at night.

## D. The light built in, no base (a proposal, 2026-11-03)

**Why:** the owner doubted the base and wants the light cast up through the speaker, like the site's images. A light under the floor can't do that honestly:
- **It stays at the bottom.** The 40 W panel lights the port chamber and fades upward; the top chamber stays several times darker. The acrylic isn't trapping it: hiding the brace changes nothing (`renders/2026-11-03/barkhorn/base-question/light-study/`).
- **It leaks out low.** Light from under the floor gets out through the bottom panel's edges and the plate onto the floor, which the owner rejected.

So the light moves inside the speaker (option "Built-in light", `BUILTIN` in `variants.py`). Tropos then stands on its own four feet, which pass the stability tests (`stability/standard-2018.md`).

**What's inside, and where:**
- COB LED strip (24 V, 4000 K, CRI 90+), about 1.23 m a speaker, in six runs. Each run sits in a black aluminium U-channel (12 x 7) with a frosted lens, aimed straight up. (Corrected 2026-11-03; it was five runs and 1.42 m before the brace runs moved.)
- **On the bottom panel:** two runs of 170 behind the bottom batt, under the back lining, split wide of the bottom rib's notch (x 60-230 and 330-500), and one of 110 behind each port. They light the port chamber from inside.
- **A white reflector film on the bays' bare floor** (option "Floor film"): in the coordinator's model, about 7.5 % of D's light otherwise goes down through the bare floor beside the ports and onto the floor under the speaker. The film sends it back up. It is a real fix for D, not only for E.
- **On the brace's rear member:** two runs, of 400 at y 318 and 270 at y 332, the second short of the back's bosses. The brace is a frame round a window (y 72-311, x 70-490), so the earlier runs at y 250 and 300 stood over open air and could not be built (the coordinator, gate 3). These runs light the woofer chamber and the top. The batting lines the sides, the back and the top, so the light leaves through the front and the polished edges, not onto the wall behind (gate 3; `renders/2026-11-03/barkhorn/base-question/light-study/E/`).
- Each channel stands on three M3 nylon standoffs, screwed into brass inserts bonded in the acrylic. Nothing touches the acrylic but the standoffs, and nothing is held by tape.

**Power:**
- An external 24 V plug-in supply (Class 2 / PS1, 60 W) runs to a panel connector in the back's cable gland, so there is no new mains wiring inside.
- A small dimmer (`plinth-controller`, the same board) sits in the amplifier's compartment, its enable from the FA122's on/standby state (to be confirmed with Hypex).
- As rendered: the floor runs at 15 W/m and the brace at 30 W/m, about **33 W electrical**, about 10 W of light. By day it's off.

**Heat (estimates, to check):**
- About 23 W of the 33 W stays inside the sealed box. The box loses heat through 2.2 m² of 20 mm acrylic, partly lined, about 3 W/K, so the air inside rises about **+7 K** at full.
- The strips run cool on their channels. The amplifier's heat still leaves through the back plate.
- The four-hour heat test (S8) runs with the light at full.

**Sound:**
- The strips and channels take about 0.1 L of 135.6 L net: the tuning (38 Hz) doesn't move.
- The risk is rattle. Mitigations: screwed channels (no adhesive, which creeps), every lead tied down, and the light's parts on the sweep test for buzzes.

**Service:**
- Through the woofer's opening: eight screws, the woofer out.
- Each run is on its own connector, so a strip swaps in about 20 minutes.
- COB strips last 30,000 to 50,000 hours at these temperatures. Not a customer job.

**Cost, a speaker (estimates):**
- Built in, about **$130**: strip $36, channels about $25, standoffs and inserts $6, dimmer $22, supply $30, connector $10, plus about half an hour's assembly.
- The plate with its light and a brace strip, about **$540**: frame $170, tray $140, feet $18, board and heat sink $120, dimmer $22, supply $40, brace strip about $30.
- Built in saves about $410 and the plate's 5.3 kg, and there is one product, not two.

**Against it:**
- The light is in every speaker unless it's a build option, and it can't be added later.
- There is one more thing inside the box to test (heat, rattle).
- The idea of a separate lit base goes away.

**For the build (gate 3): no neon line down the side.** D's first night frame showed a bright line down the right side face. The brace runs ended 4 mm from the clear vertical ribs (x 80 and 480), which piped the light up to their front edges. Two rules for the build:
- Keep the strips at least 40 mm from any clear rib or clear wall edge.
- Butt or overlap the side batts at each rib, so no slit of light shows at the seam.
If a line still shows, satin the ribs' front edges or set them back 2 mm behind the front panel's inner face.

**Open: the voile colour.** The batts' sleeves are black voile in the parts list and in `product.py` (since 2026-11-01), but white in colors F and the site's copy. In the coordinator's model, black sleeves cut D's light leaving the cabinet from about 44 % to 24 %. It is tied to Smoke's lining question (gate 3: white reads, black reads as "a PC case with a window"). Owner's call.

**For the build (gate 2, D by day, 3/3 pass; done since gate 3, the runs are on the rear member):** by day, the brace channel at y 250 shows from the front three-quarter view as a short dark bar under the woofer's lower right, where A shows a pale brace-edge highlight. One critic read it as a stray mark. Two fixes:
- Move the brace runs back, to y 315 and 330, behind the woofer's basket and clear of the back's bosses, which start at y 327 only at x 102-138 and 422-458, so the runs stop short of them. The camera then sees them only past the magnet.
- Or recess each channel into a 7 mm pocket milled in the brace's top face, so its rim sits flush and only the lens line shows.
The first costs nothing. The second costs a machining operation on the brace and thins it locally from 20 to 13 mm, which the brace's stiffness should be checked for. Either one comes after the light's power is set, since moving the runs back changes how much light reaches the top chamber.

**The frames** (`renders/2026-11-03/barkhorn/base-question/gate2/`, A's camera, Ice):
- `D-day-ice.png`: light off, so the channels and standoffs show through the walls;
- `D-night-ice.png`: light on;
- `D-smoke-black.png`, `D-smoke-white.png`: Smoke at night, the light 6500 K, black and white sleeves.

## D+ and E: tried for the site's upward V, and dropped (2026-11-03)

The site's uplit images show a V of the speaker's colour rising on the wall behind it. Two ways to get it honestly were tried. Neither gives the site's look.

**D+, a window in the top batt and the back's top band opened** (option "Top window"; the coordinator's acoustic study puts it nearly free):
- The coordinator's skeptic checked it against the site's uplight31 render: the V there comes from the ports' bay, whose side walls carry no batts. D+ opens the top and the back instead.
- That gives a lit horn underside and a glow behind the top of the speaker, which are dark in the site's images. With the whole top open, the model moves the wall's share of light only from 10.9 % to 11.4 %.
- **Not the site's look.** Stopped before any frame was rendered. The part stays in the model as an option.

**E, a side light** (option "Side light"): a strip at the foot of each side wall in the ports' bay, tilted 45° up and outward, with the brace runs:
- On the wall it reaches only 0.13-0.21 of the front panel's brightness, against 0.5-1 in the model and about 0.45 on the site's Ice slide.
- Its lens shows through the side wall as a hot line at the lower right.
- More power raises the front and the wall together, so the ratio doesn't move.
- **Dropped.** The proxies and numbers are in `renders/2026-11-03/barkhorn/base-question/light-study/E/`.

**What's left for the owner:**
- **A**, no light: the coordinator's pick.
- **D**, the lantern, the light built in: it lights the cabinet, not the room.

The site's V needs an unlined lower side, and that would give up the lining's control of the side panels' modes.

## A, uplit: the light goes up through the speaker (2026-11-02)

**The owner, 2026-11-02 20:38** (README 41581a57): "The light in the base is meant to go upward through the speaker. The intent is to provide a way to light up the speaker from below, like in the underlit promo images." On 2026-11-01 "light up from underneath" was read as a strip under the plinth facing the floor. That was the wrong way round. **The uplight below replaces the floor line**, which stays documented after it as superseded. The model is `UPLIGHT` in `variants.py` (option "Plinth uplight"); the renders are in `renders/2026-11-02/barkhorn/uplight/`.

**What the light has to get past** (the uplit set of 2026-10-18, `renders/2026-10-18/barkhorn/uplight31/README.md`): the bottom batt stops light going straight up. The colour leaves through the tinted walls and through the strip of the bottom panel by the ports, where the batt stops short. So the uplight lights the walls themselves, and the inside round the batt.

**The light:**
- **Edge strips** (`uplight-strip`): COB, dotless, 24 V, 10 W/m, **4000 K**, CRI 90+, 8 mm, 1.84 m a speaker in four lengths. Each sits under a wall's bottom edge, in a 16 x 8 groove in the plinth's top frame.
  - The sides' own edges: x 0 to 20 and 540 to 560, two strips of 360.
  - The front and back panels' edges, which stand on the bottom panel: two strips of 480. Their light crosses the 20 mm bottom panel first, through the cemented joint.
  - Each strip in a black aluminium U-channel (12 x 7, `uplight-channel`) on three M3 nylon standoffs, so **neither the channel nor the strip touches the acrylic**: 2 mm of air to the groove's sides, 0.5 mm under the channel.
  - The frosted lens sits 0.6 mm under the wall's edge. Light entering the edge is caught in the wall by total internal reflection and carried up it. The wall glows in its own colour from the foot up and fades with height as the dye absorbs it.
- **The centre panel** (`uplight-panel`): a 400 x 260 aluminium-core LED board, 24 V, **40 W** (2026-11-03; 16 W before), 4000 K, on a finned black anodised aluminium heat sink (a 3 mm plate, 15 mm fins down into the floor gap, vented to it) on four glass-filled nylon brackets in the plinth's opening, none of it touching the acrylic, under a 3 mm opal PMMA diffuser (420 x 280) held **10 mm under the cabinet's bottom**, as the uplit set's flat panel. It lights the inside of the cabinet through the bottom panel round the batt: the ports, the lining's faces and the woofer's frame, seen through the front as the speaker's colour.
- **Why 4000 K, not 2700 K:** a neutral white lets each tint show its own colour. Behind blue acrylic, 2700 K reads teal-green and dim; behind clear Fog it reads amber. The floor line's 2700 K was for a warm accent, not for colour.

**How far the light carries up a wall** depends on the tint. This is the e-fold length of the tint's dominant channel, from its 20 mm colour; the wall glows over about two of these:

| tint | dominant channel | e-fold | the wall glows |
|---|---|---|---|
| Dust | red-orange | about 700 mm | nearly its full height |
| Fog | clear | none | full height, white |
| Ice | blue | about 345 mm | the lower 40 % or so |
| Ember | red | about 53 mm | the bottom 10 cm |
| Smoke | grey | about 10 mm | barely; Smoke passes least |

**The bottom batt.** A window in it (the batt cut back to a frame, or lifted) lets the centre panel's light straight up the middle. `ice-night-window.png` and `like/*-window.png` show the batt removed, the upper limit of what a window adds. (Corrected 2026-11-03: the first `ice-night-window.png` hid a part name that did not exist, `lining-bottom-1` for `lining-bottom-1-web`, so it was byte-identical to `ice-night.png`. The note that it "gives a little more" could not have been seen in it. Re-rendered with the batt really out.)
- **What it does:** the bottom bay and the lower cabinet get brighter, and the cabinet a little more evenly lit. The wall changes little. A real but small gain.
- **What it costs acoustically:** **no bass**. The batts do not set the box's tuning, and the bottom batt is about 6 L of a 155.5 L box (gross; corrected 2026-11-03, it said 164), so the port's tuning moves well under 1 Hz. It does weaken the damping of the cabinet's vertical standing wave, about 210 Hz for the 0.82 m inside height. The 100 mm top batt stays and damps the same mode at the other end. Expect at most a 1 to 2 dB ripple near 210 Hz, to measure on the first sample before the window is adopted. If it rings, a voile-only panel keeps the look with the batt back.

**Adopted (the coordinator, 2026-11-03): the base uplight with the bottom-batt window.** The window is the bottom batt cut back to a frame round the centre panel's light. **Measure the ripple near 204 Hz (the inside height is 0.84 m; corrected 2026-11-03, it said 210 Hz) on the first sample** before it ships; if it rings, the batt goes back whole. (The Cloud's CAD, `cloud.py`, still carries the whole bottom batt until that measurement.)

**Against the underlit promo images** (`like/`, the uplit set's own stage, camera, moon, haze and exposure, only the plinth's own light at full; `like/sheet-like.png`: the uplit frame, then base, window and wash, Ice on top and Ember below):
- **The base uplight lights the whole cabinet**, top to bottom, in its own colour, deeper than the promo's near-white interior.
- **The promo's tall V up the wall is out of reach.** Its lamp put about 135 W of light under the speaker; the plinth's uplight gives about 10 W of light at full (34 W electrical). The wall here gets a shorter, dimmer fan: close in Ember, paler in Ice.
- **The window** adds a little more glow low in the cabinet.
- **The cabinet wash** (below) adds a brighter inside and a stronger glow at the ports and walls, and a little more on the wall.
- **Closest to the promo look for the least change:** the base uplight with the bottom-batt window. No parts, and its glow already fills the cabinet. The next step toward the promo's wall was more light from the centre panel, not the wash. **Adopted 2026-11-03: the centre panel at 40 W** (below).

**The centre panel at 40 W** (`like/ice-window-p40.png`, `like/ember-window-p40.png`, `like/sheet-p40.png`: the uplit frame, the window at 16 W, the window at 40 W; Ice on top, Ember below). Mean linear luminance on the cabinet's front and on the wall either side, against the promo:

| | cabinet | wall |
|---|---|---|
| Ice, the promo | 0.211 | 0.086 |
| Ice, window, 16 W | 0.132 | 0.036 |
| Ice, window, **40 W** | **0.158** (+20 %) | **0.048** (+33 %) |
| Ember, the promo | 0.167 | 0.052 |
| Ember, window, 16 W | 0.059 | 0.020 |
| Ember, window, **40 W** | **0.076** (+29 %) | **0.025** (+24 %) |

- **What 40 W buys:** a brighter cabinet and wall. The wall reaches about half the promo's, so the gain is real but modest; the promo's V needs about ten times the plinth's light.
- **The heat, at full in a 25 °C room** (estimates, to check with thermocouples after 4 h at full on the first plinth):
  - **The board:** of its 40 W, about 14 W leaves as light and 26 W as heat in the heat sink.
  - **The heat sink:** about 0.5 m2 of finned, black anodised surface, convecting into the vented floor gap and radiating. It runs about 15 to 20 K over room, 40 to 45 °C. If the cavity breathes poorly, about 35 K over, near 60 °C.
  - **The acrylic round it:** it touches nothing but the nylon brackets. The diffuser and the plinth's frames see its radiation and the warm air, about 10 to 15 K over room, so **35 to 40 °C** (about 45 °C in the poor case).
  - **The cabinet's bottom panel** absorbs some of the light (most in Ember): about 3 K more.
- **The margin:** about **40 K under cast PMMA's 80 °C** (35 K in the poor case), and 25 to 30 K under its long-term service limit of about 70 °C. That is a clear margin, so **adopted**. At the default 50 % the rises halve.
- **Supply and cost:** the uplight draws about **59 W at full** (edges 18.4, panel 40), so the supply grows to **24 V, 90 W, Class 2** (at 24 V Class 2 allows up to 100 VA). Cost: the board and heat sink about $120 (from $64), the supply about $40 (from $24): **about +$72 a speaker**.

**The cabinet wash: not adopted** (the coordinator, 2026-11-03: it adds glow inside but not on the wall, puts 11 W into the box, and needs a connector through the bottom; kept in the CAD as an option; `WASH` in `variants.py`, option "Cabinet wash", `cabinet-wash` in `components.json`):
- **What it is:** COB strips, 24 V, 10 W/m, 4000 K, 1.06 m a speaker, bonded to the bottom panel inside the cabinet at the foot of each side wall and of the front panel, between the wall and its lining, aimed up the wall. The back is left out (its land strip and the amplifier's compartment).
- **How it is fed:** from the plinth's 24 V through a sealed, potted 2-pin connector in the bottom panel at a foot pad, mating with a spring contact in the plinth's top frame. The cabinet still lifts off its plinth with nothing to unplug.
- **Cost:** about $60 a speaker (the strip $34, the connector and the spring contact about $15, fitting).
- **Power:** +11 W at full (+6 W at 50 %), on top of the uplight (70 W in all with the 40 W panel, within the 90 W supply).
- **Heat:** about 11 W at full inside the acoustic box, 5 mm clear of the lining, the ports breathing. The inside air runs a few K warmer, near the woofer's magnet, well within its rating. To check with a thermocouple on the first sample.
- **Acoustics:** two millimetres of strip on the floor change nothing measurable.
- **What it buys:** a brighter inside, not the promo's wall. Worth it only if the owner wants the cabinet itself to glow harder.

**Power:**
- **At full:** edges 18.4 W, panel 40 W (2026-11-03; 16 W before), **59 W**.
- **At the default 50 %:** 17 W.
- **The supply:** grows to a **24 V, 90 W** Class 2 / PS1 plug-in (60 W with the first 16 W panel) (`plinth-supply`), still outside the FA122's mains.

**Control:** as before. On with the amplifier, off in standby. Dimmable in four steps (off, 25, 50, 100 %, 50 % by default) on the touch pad under the plinth's back edge. PWM at about 20 kHz. Two channels now, the edges and the panel, so the walls and the inside can be balanced at the factory.

**Heat** (estimates, to check with thermocouples after 4 h at full on the first plinth):
- **The edge channels:** about 20 K over room at full, in the groove under the cabinet. The acrylic beside them stays about 10 K over room, behind its 2 mm of air: under 40 °C in a 25 °C room.
- **The panel's plate:** about 15 to 20 K over room, vented round its edges. The diffuser is about 10 K over room.
- **The limit:** cast PMMA is good to about 80 °C. At the default 50 % the rises halve.

**How much of the light you see** (rough optical estimates, not measured):
- **The edge strips:** about 85 % of their light enters the walls (a 0.6 mm air gap; the 8 mm lens under a 20 mm edge). Of that, the share that leaves the walls where you can see it is about 60 % in Fog and Dust, 30 to 40 % in Ice, 15 to 20 % in Ember and under 5 % in Smoke. It leaves at the walls' faces wherever the light's trap is broken: the lining's tape dots, the joints, and the top edge in the light tints. The rest warms the dye, under 1 W a wall.
- **The centre panel:**
  - About half its light is under the bottom batt and stops there.
  - The rest crosses the bottom panel (about 58 % in Ice, 14 % in Ember, a few % in Smoke) into the cabinet, by the ports.
  - Seen from outside, about 20 % in Ice, 5 % in Ember and 1 to 2 % in Smoke.
- **On a wall behind:** the colour fans up it from both, as the night frames show.

**Is a trace of the floor line worth keeping?** No separate strip. The plinth's own frames pick up some of the uplight at their polished edges, which gives a faint coloured line at the step without a second light. The owner's intent is upward. The floor strip, its 2700 K, and its four-run layout are superseded.

**The renders** (`renders/2026-11-02/barkhorn/uplight/`, front-off-tall framing, the current deep horn, 0.6 scale, 128 samples):
- `ice-day.png`, `ember-day.png`: the site's studio, the uplight at 50 %.
- `ice-night.png`, `ember-night.png`, `smoke-night.png`: night, a grey wall 0.75 m behind, a dim moon, the uplight at 100 %.
- `ice-night-window.png`: the bottom batt removed.

## A, lit: the plinth's light (2026-11-01; superseded on 2026-11-02 by the uplight above)

The idea is the same as Mantle floating on its own light: a soft, warm glow from under the lowest step onto the floor.
The steps' polished edges catch some of it.

**The light:**
- **The strip:** COB (dotless) LED, 24 V, **4.8 W/m, 2700 K, CRI 90+ (R9 above 50)**, 8 mm wide (`plinth-led`).
- **The channel:** a shallow aluminum channel, about 10 x 4, with a frosted PMMA diffuser, bonded into a groove routed
  in the bottom frame's underside, **40 mm in from its outside edge all round**. The underside is flat (no reveal).
- **Broken at the feet:** the strip runs in four lengths, each stopped 30 mm short of the corner so it clears the foot
  pads there (the pads reach 45 mm in from the edges; the strip at 40 would run over them). The lengths are joined by
  short soldered jumpers across each corner (the coordinator, 2026-11-01).
- **The light's path:** the strip faces the floor. The plinth stands 12 mm up on its feet, so the light leaves at the
  bottom step as a thin warm line on the floor, with some light entering the bottom frame and showing at its polished
  edge. This is the look the deck hero shows: **glow 20 by day and 40 at dusk** in the pictures.
- **Length and power:** 2.1 m a speaker, so **10.1 W at full** and 5.0 W at the default 50 %.

**Tested and not adopted** (2026-11-01; the deck's comparison rows at 1664 x 520 and the Ice front-off-wide proofs, half
size, all in `renders/2026-11-01/barkhorn/`). The aim was a soft pool on the floor in place of the line.
- **The bare strip at 40 at lower strengths** (`deck/tropos-eight-row-led40/20/10.png`): the line thins but stays a line.
  Kept, at glow 20 by day.
- **90 in behind a 40 x 3 opal diffuser** (`deck/tropos-eight-row-pool20/40.png`): a broader warm band under the dark
  tints, but the diffuser glowed through the clear frames. Not adopted: still a line on the light tints.
- **A 6 mm reveal under the bottom frame's outer 70 mm** (`deck/tropos-eight-row-reveal20/40.png`,
  `site-strata/proofs/front-off-wide-ice-reveal.png`): more warm light on the floor, but the light piped through the
  clear frame and lit its underside as a wider band. Not adopted: it doesn't stop the line, and it costs about 1 kg of
  machining and a point of tipping margin. (A 15 mm reveal does not fit the 1/2 in frame.)
- **A sealed, removable black U-channel, 90 in** (`deck/tropos-eight-row-sealed20.png`,
  `site-strata/proofs/front-off-wide-ice-sealed.png`): the frame stays in its own tint, but the light lands under the
  plinth, hidden by the step. Not adopted: no pool reaches past the step.
- **The same channel at 40 in** (`deck/tropos-eight-row-sealed40in-20.png`, `site-strata/proofs/front-off-wide-ice-sealed40in.png`):
  a crisp warm line on the floor under the edge, the frame clean. Not adopted: it is the same line as the bare strip at
  more cost. It stays the alternative if the frame's glow is ever unwanted (`PLINTH_LIGHT['sealed']` in `variants.py`;
  `plinth-channel` in `components.json`).
- A real pool past the step needs the light further from the floor (taller feet, about 50 mm). That changes the look,
  so it is the owner's to ask for.

**Power, separate from the FA122's mains:**
- **A plug-in supply, 24 V, 15 W, UL listed Class 2** (UL 1310) or IEC 62368-1 PS1 (`plinth-supply`), with a 2 m lead
  to a DC socket under the plinth's back edge.
- It stays outside the speaker's mains circuit, so the speaker's listing need not cover a second mains converter.
  The plinth's own circuit is Class 2 / PS1 throughout.
- **No aux rail on the FA122 is used.** Hypex publishes no 24 V auxiliary output for it, and drawing from its internal
  supplies would void their assumptions (asked in the Hypex letter).

**Control** (`plinth-controller`, a small board in the plinth):
- **On with the amplifier, off in standby.** The board's enable comes from the FA122's on/standby state through an
  opto-isolator. The state line still has to be confirmed with Hypex: the remote kit's status LED on J15 is a
  candidate. Until then, a switch under the back edge.
- **Dimmable:** four steps (off, 25, 50, 100 %) on a touch pad under the plinth's back edge, 50 % by default. PWM at
  about 20 kHz, so it is flicker-free on camera.
- **Wiring:** the state line leaves the amplifier compartment through its third M12 gland (as the IR receiver's lead
  does on the master) and down the back to the plinth, on a 3-pin plug.

**Heat next to the acrylic:**
- 4.8 W/m in an aluminum channel runs about 10 to 15 K over room (est.), so under 40 °C in a warm room.
- Cast PMMA is good to about 80 °C. The channel spreads the heat, and the strip never touches the acrylic directly.
- Checked on the first plinth with a thermocouple after 4 hours at full.

**Shipping and set-up:**
- The plinth ships flat in its own carton (about 700 x 710 x 80, about 13 kg), apart from the speaker's crate.
- At set-up the plinth goes down first and is leveled on its four feet. The speaker is lifted on (two people, its
  feet removed), and four M8 bolts from under the plinth go into the cabinet's own foot inserts, through counterbored
  holes.
- Then the state lead plugs in and the supply connects.

**Stability with the plinth:**
- The plinth makes the speaker heavier and lower, but the test is geometric: its feet carry the margins in the table
  above.
- With the flush horn drawn, the margins are recomputed from the CAD (`stability/README.md`): +19 / +14 / +14 %.
- **The plinth is not optional for a listed product.** On the cabinet's own feet the speaker fails the 20 % push in
  every direction. A lab's acceptance of anchoring is the only other route.
