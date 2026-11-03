# Tropos and the stability standard (2026-11-03)

The owner asked why Tropos needs its wide stepped plinth ("Why is it that we need it?", 03:10 UTC), and at 04:27 said
they're still not convinced it's needed. This folder answers that question. The research was a four-agent workflow
(wf_a73d7898-d30): three researchers and a skeptic who re-checked 57 claims against fresh downloads. 50 were confirmed,
5 partly confirmed, 2 couldn't be checked because the pages wouldn't open, and none was contradicted. The raw result is
`research.json`.

## The answer

- **Tropos is MS3** (more than 25 kg): 74.6 kg alone, 84.6 kg on the plinth. It is MS3 under IEC 62368-1:2018 and 2023,
  which are UL 62368-1 Ed.3 (the US basis until 15 Feb 2027) and then Ed.4. The 2023 edition made no technical change
  to 8.6 or 8.10, and neither edition has US or Canadian national differences in clause 8.
- **Table 36 (2018), Table 35 (2023): plain MS3 floor-standing equipment gets only three tests.**
  - **8.6.2.2.** Passed by any one of:
    - a 10° tilt;
    - a 10° incline, rotated through 360°;
    - 13% of weight horizontal plus 50% of weight down (max 100 N), applied at 1.5 m or lower.
  - **8.6.2.3.** 800 N down, at 1 m or lower, on any surface that could be stood on.
  - **8.6.3.** A 10° tilt.
- **The 20% / 250 N push exists only in 8.6.5.** It applies only in two cases: MS3 equipment with front-mounted
  accessible user controls or a moving-image display (Table 36, footnote a), and equipment on a stand the maker
  specifies (8.10.1). Even then, 8.6.5 can be met instead by a 15° tilt or a 15° incline rotated through 360°.
- **Where the team's reading came from.** The "2 m" is IEC 60950-1 clause 4.1, per JEITA's comparison table. The "20%
  in 8.6.2.2" is the superseded 2014 text, and that text also allowed a 10° tilt instead of the force.
- **Tropos on its own feet** (the speaker lane's `stability/com.json`, strata: centre of mass 548 mm up; arms 199 mm
  forward, 171 mm back and 230 mm sideways at the feet centres) tips at about **17.3° back, 20° forward and 22.8°
  sideways**. It passes every 10° test, and the 15° alternative if 8.6.5 ever applied.
  - It also passes the 13% force option, but only just at the back (+1%). The tilt options are enough on their own.
  - Tropos has no front controls (an RC-5 remote and a rear plate), so 8.6.5 shouldn't apply to the speaker alone.
- **An optional base or plate** would count as a stand specified for the speaker (8.10). The combination then has to pass:
  - 8.6.5, by the force, a 15° tilt or a 15° incline;
  - 8.6.3 at 15°, since it is 1 m or taller;
  - the 8.10.3 load tests;
  - the T.6 impact test;
  - 8.10.5;
  - T.8 conditioning (acrylic);
  - the 8.10.2 caution markings.
  The bare speaker must still pass on its own, which by the geometry above it does.
- **An anchor strap doesn't help.** A strap or fixings the owner fits do not make Tropos "fixed equipment" (3.3.3.2
  Note 1), so a strap can't replace the tests.
- **Practice.** Comparable active floorstanders resist roughly 15–19% of their weight pushed at the top: Meridian
  DSP8000/DSP9, Linn 360, ATC SCM50ASLT and the Avantgarde UNO XD. Tropos on its own cabinet comes out at about 16%. The
  slimmest models (Kii BXT, Buchardt A700, KEF LS60, Beolab 28) are at 8–10%. None of the floorstanders found sells its
  base as an option. The bases sold separately (Dutch & Dutch, Genelec, Sonos, JBL) are for stand-mount or tabletop
  speakers.

## Caveats

- No licensed English copy of clause 8.6 was read. The wording comes from the official Korean KC 62368-1 translation
  (notified to the WTO) and the Japanese JIS translation, cross-checked against UL's, TÜV's and JEITA's change analyses.
- The cap on the 13% option in 8.6.2.2 is uncertain: 250 N (KC) or 100 N (TÜV). It doesn't change the result for Tropos.
- Before anything is tooled, get a written pre-assessment from the chosen CB lab and US NRTL. It should cover the
  classification, whether front controls exist, and whether the tilt route is accepted.
- The speaker lane re-runs the numbers on horn A, the default model, with the real feet, any horn overhang and the
  800 N surfaces (`stability/standard-2018.md`, asked 04:33 UTC).
