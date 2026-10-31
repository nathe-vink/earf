# Tropos's horn: the forming risk register (2026-10-31)

The horn is pressure-formed from 10 mm cell-cast acrylic over a male plug (round 36, `README.md`). This register lists
what can go wrong between the sheet and a finished horn. For each risk it gives how likely it is, what it costs, what
prevents it, and who checks it and when. It is written for the prototype pair and carries into production.

**Who checks:**
- **Former**: the thermoforming shop.
- **Pattern**: the shop that cuts the plug.
- **Caster**: whoever casts the horn lot.
- **EARF**: our own first-article inspection, `make/fai.md`.
- **Trial**: the short forming trial before the full plug is cut, `make/forming-trial.md`.

**Scales:**
- **Likelihood**: low (not expected), medium (expected on the first shots and fixed by setup), high (expected and
  designed around).
- **Impact**: the cost if it happens on the prototype, from minor (rework) through serious (a scrapped horn, about
  $250 to $400 of sheet and time) to critical (the route fails; Plan B, `make/plan-b.md`).

## Forming

| # | risk | likelihood | impact | prevention and mitigation | who checks, when |
|---|---|---|---|---|---|
| F1 | **The wall thins below 4 mm** in the mouth's corners, the last to form. The CAD's estimate is 4.9, a membrane model's about 6. | medium | serious (acoustic and strength floor) | A pre-blown bubble before the plug rises; the clamp frame shaped close to the plug's foot; corner-zone heater trim. The trial forms the corner at full scale and is gauged before the full plug is cut. If it comes out under 4.5, use 12 mm sheet. | Trial (gauge, 30 points); Former, every shot (8 points: the corners, the throat end); EARF, first article |
| F2 | **Webbing**: the sheet folds over itself in the mouth's concave corners on the plug's foot. | medium | critical for that shot, serious for the route | The base plate's cove R12 is generous for 10 mm. Ring assist, or a hold-down ring at the plug's foot. A slower last 20 mm of travel. Pressure at 4 bar, not vacuum alone. | Trial (the corner is in it); Former, first shots |
| F3 | **Mark-off on the air face**: vent pips, dust and plug texture print on the inside, which is seen through the mouth. | high | minor to serious (a horn rejected for looks) | 0.6 mm vents only in the waste and the mouth's corners. The plug sealed, sanded to 600 and polished; a clean room around the press; the plug wiped before every shot. The inside can be buffed, but not near the joint. | Pattern (the plug's finish); Former, every shot; EARF, first article (lit inspection) |
| F4 | **The dark lot heats unevenly in an IR oven.** It takes up heat at its surface, so it scorches or bubbles there and stays cold in the core. | high (the deep tint was chosen on 2026-10-31) | serious | Settings per colour from a trial sheet of each lot. A circulating-air oven at about 170 °C, about 30 minutes for 10 mm, which heats through without scorching. Or two-sided IR at lower power and a longer soak. Log the core temperature (an IR gun on both faces, and a thermocouple coupon). | Former, the first sheet of each colour; Trial (the darkest lot first) |
| F5 | **Moisture bubbles**: water in the cast sheet boils on heating. | medium | serious (a scrapped horn) | Keep the sheet wrapped. Dry it at 80 °C for about an hour a millimetre (overnight) if it has stood open. Form within 2 hours of drying. | Former, every blank |
| F6 | **The sheet sags or sticks to the clamp frame**: 10 mm cast sheet is heavy when hot. | low | minor | Support pins under the blank in the oven; a heated clamp frame; a blank cut with a 60 mm clamping margin. | Former, setup |
| F7 | **The air path differs from the plug**: the shot shrinks on the plug and is stressed coming off it. | low (the flare widens toward the mouth: a large draft) | serious (acoustics) | Demould at about 70 °C. Lift the shot off toward the nose with air through the vents. Check the air face against the CAD with a CMM or arm scan. | EARF, first article (scan); Trial |
| F8 | **The plug wears**: board degrades over shots at forming heat. | medium (board) | minor (re-seal) to serious (re-cut) | Board rated 150 °C or more, re-sealed every 10 shots; the plug's face inspected under raking light between shots. The aluminium plug for production. | Pattern; Former |

## Annealing and stress

| # | risk | likelihood | impact | prevention and mitigation | who checks, when |
|---|---|---|---|---|---|
| A1 | **Crazing at the joints or the inserts**: cement, solvent or a screw meeting stressed acrylic. | medium | serious (cracks grow) | Anneal after forming (80 °C, about 3½ hours, slow cool) and again after cementing. Polymerising cement only; no solvent cement and no flame polish near joints. Inserts bonded in clearance holes, not pressed. | EARF: a 48-hour isopropanol wipe test on an annealed shot; polarised-light inspection of every horn |
| A2 | **Springback on annealing**: cast acrylic remembers its flat shape above about 90 °C. | low (if held at 80 °C) | serious | Anneal at 80 °C, never above 85 °C; the horn supported on a cradle copying the plug while annealing. | Former; EARF (scan before and after the first anneal) |

## Trimming and finishing

| # | risk | likelihood | impact | prevention and mitigation | who checks, when |
|---|---|---|---|---|---|
| T1 | **The trim drifts**: the flare is not located the same on the trim fixture each time, so the rim and the throat's trim wander. | medium | minor to serious | A trim fixture copying the plug, with vacuum and two datum pins in the waste. The 5-axis program probes the shot before cutting. | Former (the fixture); EARF (the rim's width, ±0.5) |
| T2 | **Chipping or heat on the rim's edge** while routing and polishing 6 mm. | medium | minor (re-polish) | Sharp single-flute cutters; diamond or buff polish (no flame near the cement); routed full round in two passes. | Former; EARF (lit inspection) |

## Cementing to the throat piece

| # | risk | likelihood | impact | prevention and mitigation | who checks, when |
|---|---|---|---|---|---|
| C1 | **A step on the air face at the joint**: the flare's end and the throat's bore do not meet flush. | low (both faces are machined to the same surface) | serious (acoustics: limit 0.5 mm, aim 0.1) | The flare's end trimmed on the fixture; the socket's bore cut to the flare's outside plus 0.2; a centring jig through the bore while the cement cures. | EARF, every horn (a feeler and a borescope at the joint) |
| C2 | **Bubbles or voids in the cement line**, which show through the tint. | medium | minor to serious (looks; round 35 bars any visible bubble) | Polymerising cement mixed under vacuum and dispensed from the bottom of the socket upward; the joint filled in one pour; a cure under light pressure. | EARF, every horn (lit inspection) |
| C3 | **The flare's outside varies by its thickness**, so the gap in the socket varies. | high (it is free-formed) | minor (filled by the cement) | The socket is cut 0.2 over the nominal; the cement is a gap-filler. Measure the flare's end on the first shots and re-cut the socket if it is off by more than 0.5. | EARF, first article |

## Colour and the lot

| # | risk | likelihood | impact | prevention and mitigation | who checks, when |
|---|---|---|---|---|---|
| L1 | **The horn lot does not match the cabinet, or the site's look** (2026-10-31: "Deep, like the site"). | medium | serious (a pair looks wrong) | A chip approved before casting; a 7 mm coupon of the horn lot beside a 20 mm coupon of the cabinet lot, in daylight and in the studio's light; each lot's number marked on its parts. | Caster (the swatch); EARF (approval) |
| L2 | **The deep tint fades or shifts unlike the cabinet's** in UV. | low (the same dyes and acrylic) | serious (long term) | Accelerated UV ageing of both lots side by side (round 35). | EARF, before the pilot run |
| L3 | **A custom lot's minimum is a pallet** (Chemcast's old figure: about 2,500 lb a colour). | high | serious (cost and cash) | The first pair can be built from stock tinted cast colours (`README.md`, round 36, the stock-colour route); custom lots come once orders justify them. | EARF, with the caster's quotes |

## The five to watch

F1 (the corners' wall), F2 (webbing), F4 (the dark lot in the oven), C2 (bubbles in the joint) and L3 (the lot's
minimum). The forming trial (`make/forming-trial.md`) tests F1, F2, F3, F4 and F7 for about $3,450, about half the full
prototype tooling. Plan B (`make/plan-b.md`) is ready if F1 or F2 cannot be beaten.
