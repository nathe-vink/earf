# Cut only: the laminated horn's 44 layers (2026-10-31)

This is a second route for the horn if the full-job shops (`e-laminated-horn/`) are slow: someone cuts the layers, and
the bonding and machining happen elsewhere or in-house (`spinoffs/barkhorn/make/diy-route.md`). The shops come from
research R8. **Nothing here has been sent. These are drafts for the owner.**

**What every version attaches:**
- the 22 layer DXFs and `layers.csv` from `../e-laminated-horn/dxf/` (one horn; a pair is two of each);
- the sheet drawing BHH-005 from `../e-laminated-horn/drawings.pdf` (its last pages).

**Facts used below:**
- **The sheet:** TruCast 2074 Dark Gray 1/2 in, two horns' worth. We order it cut to 48 x 36 in blanks: A&C Plastics cuts
  to size, and that size fits Pololu's 48 x 48 limit and a 1300 x 900 mm laser bed.
- **The layers:** about 40 m of cut per horn, outlines and bores together.
- **The largest layer:** 630 x 366 mm.
- **Nesting:** the rings nest inside one another, so a 48 x 36 blank takes a dozen or more.
- **Registration:** on the bores, so the bore's tolerance matters as much as the outline's. There are no dowel holes,
  because they would show through the tint.

---

## Pololu (Las Vegas, online; cuts customer-supplied acrylic up to 1 in, sheets up to 48 x 48 in)

Pololu works through its online quote and order system. This is the note to paste into the order's comments, or into an
email to its custom-cutting address with the files.

**Short (order comment):**

> Customer-supplied TruCast cell-cast acrylic, 1/2 in (12.7 mm), dark grey 2074, in 48 x 36 in blanks: 44 parts (22
> DXFs, 2 of each), rings that nest inside one another. Please cut outline and bore; we register on the bores, so
> please tell us the bore tolerance you hold at 1/2 in and the edge taper. Edge as cut is fine. We'll anneal before
> bonding. What turnaround from receipt of sheet?

**Email:**

> Subject: Laser cutting 44 parts from customer-supplied 1/2 in cast acrylic
>
> Hello,
>
> We're EARF, a small hi-fi maker in San Francisco. We'd like a quote to laser-cut 44 parts from 1/2 in (12.7 mm)
> TruCast cell-cast acrylic, dark grey 2074, which we would ship to you in 48 x 36 in blanks.
>
> The parts are the 22 layers of a loudspeaker horn, two of each. Each is a ring: an outline up to 630 x 366 mm and a
> bore inside it. The DXFs and a table of sizes are attached. The rings nest inside one another, so a blank takes a
> dozen or more. We're happy for you to nest them, or we can send nested sheets.
>
> Three questions:
> 1. **The edge:** at 1/2 in, how much taper do you see across the thickness, and is the edge glossy? We bond the faces,
>    not the edges, and anneal before bonding.
> 2. **Tolerance:** what can you hold on the outline and on the bore? We register the layers on their bores, so the bore
>    matters most.
> 3. **Turnaround:** how long from receiving the sheet, and how many blanks you would need for 44 parts.
>
> Thank you,
> [Your name], EARF · earf.world

---

## Neal's CNC (Hayward; a 5 x 10 ft CNC router, and laser)

**Short (phone 510-783-3156, or the website's form):**

> Quote to CNC-route 44 rings from customer-supplied 1/2 in cast acrylic (TruCast 2074), DXFs ready, outline and bore,
> up to 630 x 366 mm. Do you take customer sheet? Router or laser edge, tolerance on the bores, and turnaround from
> sheet delivery?

**Email:**

> Subject: Quote, CNC routing 44 acrylic rings, 1/2 in, customer-supplied sheet
>
> Hello,
>
> We're EARF, a small hi-fi maker in San Francisco. We'd like a quote to cut 44 parts from 1/2 in (12.7 mm) cell-cast
> acrylic: the 22 layers of a loudspeaker horn, two of each. Each is a ring, an outline up to 630 x 366 mm with a bore
> inside it (DXFs and a size table attached).
>
> We'd like to supply the sheet (TruCast 2074 dark grey, 48 x 36 in blanks, or full 48 x 96 sheets if you prefer). Do
> you take customer-supplied material?
>
> Questions:
> 1. **Router or laser, and the edge each leaves.** We bond the faces and polish the outside edges afterwards. A clean
>    router edge suits us; a laser edge needs annealing before bonding.
> 2. **Tolerance** on the outline and on the bore. We register the layers on their bores.
> 3. **Turnaround** from sheet delivery, and the price.
>
> Thank you,
> [Your name], EARF · earf.world

---

## Acrylic Art (Emeryville; acrylic specialists for 34 years, CNC routers, lasers, museum work)

**Short (phone or the website's form):**

> Quote to cut 44 rings from 1/2 in cast acrylic (our TruCast 2074, or yours), DXFs ready, up to 630 x 366 mm, outline
> and bore. Edge finish (router or laser), tolerance on the bore, turnaround. Also: do you bond thick laminations with a
> polymerising cement (Weld-On 40 or ACRIFIX), and anneal?

**Email:**

> Subject: Quote, cutting 44 acrylic rings for a laminated loudspeaker horn (and possibly bonding)
>
> Hello,
>
> We're EARF, a small hi-fi maker in San Francisco. Our loudspeaker's horn is laminated from 22 layers of 1/2 in
> cell-cast acrylic, tinted dark grey. We'd like a quote to cut the layers for a pair, 44 rings (DXFs and a size table
> attached). The largest is 630 x 366 mm. Each has an outline and a bore. We can supply the sheet (TruCast 2074) or you
> can source it.
>
> Questions:
> 1. **The edge:** router or laser, and the edge each leaves on 1/2 in. The outside edges are polished; the faces are
>    bonded.
> 2. **Tolerance** on the outline and on the bore. We register on the bores, with no dowel holes, because they would
>    show through the tint.
> 3. **Turnaround and price.**
> 4. **Bonding:** your site mentions museum work. Do you bond thick laminations with a two-part polymerising cement
>    (Weld-On 40 or ACRIFIX 2R 0190) and anneal them? If so, we'd also like to talk about bonding the stack and
>    machining its air path. A fuller request with drawings is ready.
>
> Thank you,
> [Your name], EARF · earf.world

---

## Atlas Contour (San Francisco; laser, waterjet, CNC router, 5-axis routing)

**Short (info@atlascontour.com):**

> Quote to cut 44 rings from customer-supplied 1/2 in cast acrylic, DXFs ready, up to 630 x 366 mm, outline and bore;
> laser or router edge, bore tolerance, turnaround. Separately: could your 5-axis router cut a horn's air path through a
> bonded acrylic stack, 630 x 366 x 292 mm, from our STEP?

**Email:**

> Subject: Quote, 44 acrylic rings (cut), and 5-axis machining of a bonded acrylic horn
>
> Hello,
>
> We're EARF, a small hi-fi maker in San Francisco. We have two jobs on one loudspeaker horn and would like a quote on
> either or both.
>
> 1. **Cutting:** 44 rings from 1/2 in (12.7 mm) cell-cast acrylic, which we would supply (TruCast 2074 dark grey, 48 x
>    36 in blanks). These are the 22 layers of the horn, two of each. Each has an outline up to 630 x 366 mm and a bore
>    (DXFs and a size table attached). Please say whether you'd laser or route them, the edge that leaves, the
>    tolerance on the bore (we register on it), and the turnaround.
> 2. **5-axis:** once the layers are bonded into a stack, its air path, the horn's inside, is cut through it on 5
>    axes to our STEP, about 630 x 366 x 292 mm overall, then polished. Is that a job your 5-axis router could take, and
>    how would you hold the part?
>
> Thank you,
> [Your name], EARF · earf.world
