# Tropos: the first-article inspection (2026-10-31)

Checked on the first speaker of the prototype pair, and on the first of every new lot, shop or tool after it. Each
check has its limit and its method. A failed check stops the line until its cause is found. Record the results on a
copy of this list, with the lots' numbers and the photographs. The forming risks it closes are in
`make/horn-risks.md`.

## Dimensions

| # | check | limit | how |
|---|---|---|---|
| D1 | The cabinet's outside: 560 x 420 x 880 | ±1.0 | tape and squares; diagonals within 1.5 |
| D2 | The front panel's setback | 24 ±0.5 | depth gauge at 4 points |
| D3 | The woofer's cut-out and its 8 inserts on 374 | ±0.3 position | the woofer offered up: it seats without force |
| D4 | The ports' frames flush with the panel | ±0.3 | straightedge |
| D5 | The lands' plane and the bosses' faces | flat within 0.3 | straightedge and feeler; the back seats with no rock |
| D6 | The seal's groove | 3.0 deep, 5.4 wide ±0.1 | depth gauge |
| D7 | The horn's air path against the CAD | ±0.3 | an arm or structured-light scan |
| D8 | The horn's wall, 30 points | 4.0 or more everywhere | Hall-effect gauge |
| D9 | The step at the flare's joint | 0.1 or less | feeler and borescope |
| D10 | The horn's rim | 10 ±0.5, full round | gauge and eye |
| D11 | The posts' sockets: the horn sits on all four without rocking, the front feet hooked under their keyhole sockets' lips (the engineering audit, 2026-11-01) | no rock; the horn cannot slide forward with the tie done up | by hand; the rear sleeves fitted |

## Finish and colour

| # | check | limit | how |
|---|---|---|---|
| V1 | Joints | no visible bubble in any cemented joint (round 35) | raking light, a loupe |
| V2 | Show edges | polished, no chips or tool marks | raking light |
| V3 | The horn's inside | no mark-off past the limit sample | raking light through the mouth |
| V4 | Stress | no crazing; even fringes, no hot spots at the inserts and joints | polarised light, all over |
| V5 | Colour: the cabinet against its approved chip; the horn against its chip and against the cabinet | no difference visible to an observer at 1 m (ΔE about 2 or less on a spectrophotometer) | daylight booth and the studio's light |
| V6 | Lot numbers | the cabinet's and the horn's lots recorded on their parts | label inside the back |

## Mechanical

| # | check | limit | how |
|---|---|---|---|
| M1 | Inserts | a sample of each size holds 2 x its fitting torque with no turn (the woofer's M6 at 5 N m, so 10 N m; the tie's M6 at 2 N m, so 4 N m; not the 30 N m of 2 x the old 15) and a 2 kN pull on the tie's and the keyhole sockets' fittings | torque wrench and a pull gauge, on a coupon cemented with the cabinet |
| M2 | The back's seal | static pressure decay: the box at 200 Pa, ports plugged, holds above 100 Pa for 30 s (est.; set on the first sealed sample) | a hand pump and a manometer through a fitting in one port's plug. 200 Pa moves the woofer 4.1 mm, inside its Xmax 5.75; 1 kPa would move it 20 mm, and the old 20 Hz tone at 100 dB about 10.9 mm (the audit) |
| M3 | Rattles and buzzes | none from 35 to 200 Hz at 100 dB/1 m, and from 30 Hz at 94 dB | a slow sine sweep, listened to at 0.3 m all round. From 20 Hz at 100 dB the woofer would need about 28.7 mm (the audit), past Xmax |
| M4 | The horn's retention | the tie nut at 2 N m; the horn does not lift or slide under 150 N at its top in any direction | torque key, push gauge |
| M5 | Stability | IEC 62368-1 8.6.2.2: 20 % of the weight (about 150 N) at the horn's top in every horizontal direction: no tip; and the 10° tilt | push gauge, inclinometer. Today's footprint fails (`stability/README.md`): this waits for the base the owner chooses |

## Electrical and acoustic

| # | check | limit | how |
|---|---|---|---|
| E1 | Earth continuity: the compartment to the FA122's earth | 0.1 Ω or less | milliohm meter (round 35's B3) |
| E2 | Polarity | both drivers in phase with the preset | a polarity pulse, or the impedance phase |
| E3 | Impedance, each driver | within 10 % of the first sample's curve | an impedance sweep |
| E4 | Response, on axis at 1 m | within ±1.5 dB of the reference, 60 Hz to 16 kHz; a pair within ±1 dB | measurement microphone, gated |
| E5 | Distortion | horn below 1 % at 1 kHz, 100 dB/1 m | measurement microphone |
| E6 | The preset | the same verified preset in all three slots (the 28 Hz high-pass, the limiters, soft clip on, the HF channel 6 dB down in the DSP: there is no L-pad), its version recorded; Hypex's filter password set and recorded in this file, not on the speaker | HFD |
| E7 | The remote (the master) | volume, mute and power from the listening seat, through the front panel | the Hypex remote at 3 m, 30° off axis |
| E8 | Heat | the compartment below its limit after 4 hours at full program (round 35); and the abnormal case: a full-scale HF sine with the preset's limiter defeated (31 W into the driver, within its 140 W rating; nothing in the compartment heats but the amplifier) until steady: the driver's pod and the horn's boss below their limits, no smoke | thermocouples on the pan, the back, the pod and the boss |

## Labels and paperwork

| # | check | limit | how |
|---|---|---|---|
| P1 | The rating plate | the model, the serial number, the ratings, the WEEE bin; no CE, UKCA or FCC mark until earned | eye |
| P2 | The record | this list, filled in, with the serial and lot numbers and the response and impedance plots | kept with the speaker's file |
