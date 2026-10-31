# Test-lab quote requests (round 43, 2026-10-31)

Drafts only: nobody has been contacted. The coordinator turns them into Gmail drafts. Each file has a short version
for a web form (593 characters) and a longer email version. `[Your name]` and `[contact line]` are placeholders.

The risks slide promises "FCC testing is booked with the first build", and Tropos's schedule books the lab in the week
of 16 November. Each letter asks for all four products at once, so one lab can bundle them.

Sources:
- labs: public pages read on 2026-10-31 (the OSHA NRTL pages and each lab's own site; no site refused access);
- requirements: R3 (`spinoffs/barkhorn/research/2026-10-31/R3-compliance.md` on `r46-owner-notes`, 97ca003e) and
  `launch-readiness.md`;
- Tropos's needs: `make/compliance.md` on `r33-speaker-horn` (6b0da937).

**No lab publishes prices or lead times.** Every figure below is R3's estimate.

## The labs

| Lab (file) | Nearest site | NRTL for UL 153 / 1598 / 62368-1 | EMC and FCC | DOE App. Y and CEC | Quote route | Role |
|---|---|---|---|---|---|---|
| **BACL** (`bacl.md`) | Sunnyvale | yes / yes / yes (also UL 8750, 1310) | A2LA 17025, FCC TCB | CEC-approved lab and certifier for battery chargers | form, sales@baclcorp.com, 408-732-9162 | **First choice: all four products in one building** |
| **UL Solutions** (`ul-solutions.md`) | Fremont | yes / yes / yes | Fremont EMC lab, FCC recognised, TCB | CEC and DOE named as programmes; the site is unconfirmed | sales form, 510-319-4135; LightingInfo@UL.com | Comparison quote; **Limited Production Certification** for a hardwired Hemisphere batch |
| **Intertek (ETL)** (`intertek.md`) | Menlo Park | yes / yes / yes | EMC and safety at Menlo Park; FCC TCB | CEC named; Appendix Y unconfirmed | Part 15 contact form; 650-463-2900 (confirm) | Comparison quote |
| **TÜV Rheinland** (`tuv-rheinland.md`) | Pleasanton; Fremont (wireless) | yes / yes / yes | "FCC listed" (older source); CB test labs | unconfirmed | tuv.com contact form; 925-249-9123 (confirm) | Comparison quote for the listings |

**Not written, for reference:**
- **Element, Fremont** (510-440-9500; A2LA 0214.26; Part 15B and 62368-1 testing). Its NRTL site is Irvine, and that
  scope has UL 62368-1 but not UL 153 or 1598. It would suit an EMC-only quote for Tropos.
- **CSA Group.** Its nearest NRTL site is Irvine, and EMC and DOE are unconfirmed.
- **CKC Laboratories** has a new EMC lab in Fremont (R3).

## What each product needs, and R3's estimates

| Product | Asked for now (before the debut) | Estimate | Lead time | Later (before selling about 100) |
|---|---|---|---|---|
| **Tropos** | EMC pre-scan; FCC 15B Class B SDoC; 62368-1 pre-check (hipot, earth, touch current, temperature rise, the amp compartment as fire enclosure) | $0.8–1.5k pre-scan; $1.5–3.5k 15B; $1–2.5k pre-check | 15B 2–4 weeks' lab lead time | UL 62368-1 listing, $10–25k, 8–16 weeks |
| **Core** | FCC 15B; DOE Appendix Y on the system (adapter, charger, cells); CEC MAEDbS listing | $1.5–3.5k; $1.5–4k; $0–1k admin | Appendix Y 3–6 weeks; MAEDbS 2–4 weeks | UL 153 + Supplement SA, $8–20k |
| **Hemisphere** | FCC 15B (the LED driver); **both** versions priced: plug-in swag UL 153, or hardwired UL 1598 + 8750 | $1.5–3.5k | as above | plug-in UL 153 $6–15k; hardwired Limited Production $5–12k |
| **Mantle** | the lab's view: its own FCC test, or covered by the bought supplies (Neo PSU, a listed LPS adapter of 15 W or less) and an incidental-radiator reading (the only clock is a 25 kHz PWM) | $0 if covered; else $1.5–3.5k | | UL 62368-1 with external listed supplies, $4–10k |

Before the debut, R3 puts all four at about $18–46k to first sales, plus $28–70k later to list all four.

## What to ask every lab

These are in each letter:
- the price per item, and whether a pre-scan is credited against the full test;
- the lead time from booking, and to the report;
- the samples and documents needed;
- bundling, and the listing costs that follow.

**The three questions that decide the lab:**
1. Does it run Appendix Y itself, and file MAEDbS?
2. Does its UL 153 scope cover Supplement SA?
3. Is there a small-batch route for the hardwired Hemisphere?

## Before sending

- Confirm the two phone numbers marked "confirm" (Intertek, TÜV).
- Attach nothing confidential to a web form. The email versions offer drawings and schematics under NDA.
- Hemisphere's two versions stay in every letter until the owner chooses (`renders/2026-10-31/barkhorn/hemi-mounting/`).
