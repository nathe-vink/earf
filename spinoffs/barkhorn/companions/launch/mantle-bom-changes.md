# Mantle's BOM: three changes to apply (round 43, 2026-10-31)

Mantle's source (`turntable_float.py`) and its built package (`out-turntable-float/`) live on **`r32-turntable-final`**,
not on this branch, and this session pushes to its own branch only. So the changes are written here as an exact patch
for whoever works on that branch, then `fab build` reruns the BOM. Line numbers are that branch's head, 9a1543e5.

## 1. Lead-free brass for the three C360 parts

From `certification.md` (R3): Prop 65 does not bind EARF yet, but lead-free brass is the right default.

| Part | BOM line (`bom.csv`) | Now | Change to |
|---|---|---|---|
| platter-hub | 10 | Brass C360 | **C69300 (Eco Brass)**, or C27450 if the shop stocks it |
| bearing-housing | 12 | Brass C360 | the same |
| pod-core | 18 | Brass C360 | the same |

**In `turntable_float.py`:**
- Lines 361, 365 and 376 use `Machined('brass', 'lathe')`. fabkit's `brass` is titled "Brass C360" (`studio/fabkit/model.py`
  line 64). Add a material beside it rather than renaming it, so the other products keep their brass:

  ```python
  'brass-leadfree': dict(title='Brass C69300 (Eco Brass, lead-free) or C27450', density=8.2, usd_per_cm3=0.15),
  ```

  Then use `Machined('brass-leadfree', 'lathe')` for the three parts. The density is C69300's (8.2), and the price is
  about 25 % over C360's: an estimate, so confirm it with RFQ 04's shop.
- Lines 366 and 377: change the notes' "C360 brass" to "lead-free brass (C69300 or C27450)".
- Both alloys machine at about 80–85 % of C360's rate. The bushes' press fit and honing are unchanged.

## 2. The Rega 24 V motor kit at $265

`mantle-drive.md`: Audio Advisor has it at $265, in stock, against the $200 converted from HiFi Gear's GBP 150.

In `spinoffs/barkhorn/companions/components.json`, entry `rega-24v-motor`:

```json
"usd": 265,
"supplier": "Audio Advisor (US, in stock, 2026-10-31)",
"price_date": "2026-10-31",
```

Keep the url, or swap it for Audio Advisor's page if one was read. The note about the motor's size, shaft and the pod's
bore stands. Bought parts go up by **$65**.

## 3. The plinth: two 1/2" sheets laminated

From `stock-colours.md` (the prototype in stock TruCast; there is no 25 mm in stock):

- Line 170: `A25 = Sheet('cast-acrylic', 25, face='+z')`. Keep it for the drawing's dimension (the design is 25). For the
  prototype's stock, add a note to the `plinth` Part (line 341), or a `stock=` override if fabkit has one:
  "prototype: two 1/2" (12.7) cast sheets laminated with Acrifix 2R 0190 or Weld-On 40 under press or vacuum, annealed,
  machined to 25.4; the bond line mid-edge (hidden, or a 1 mm V: the owner's question)".
- The platter, also 25 thick and turned, is laminated the same way.
- The cut list should list the plinth and platter as **2 × 1/2" each**, and the sheet buy as **one 48 × 96 at 1/2"**
  (both layers of both parts nest on it) in place of a 25 mm sheet.
- Cost: AC Plastics 2423 at 0.500 is $835.80 for a 48 × 96. Canal 2064 at 1/2" is $495. Add about $30 for cement and
  the press time. That replaces the 25 mm sheet line at $96.19 a part.

## After applying

```sh
.venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/turntable_float.py --out spinoffs/barkhorn/companions/out-turntable-float
```

Then check the BOM total. Mantle's deck figure is $3,815: it rises by about $65 for the motor and by the lead-free
brass's premium (a few dollars). The sheet change is a prototype line, not the production one.
