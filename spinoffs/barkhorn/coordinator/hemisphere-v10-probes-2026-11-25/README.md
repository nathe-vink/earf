# Probes from the V10 check of the Hemisphere top (58e4f5d036), 25 Nov 2026

These are the reviewers' own scripts. They are kept so the lamps lane can see exactly how each V10 finding was measured and can fold the useful ones into its own checks. Today's fixings_check and the zero-tolerance overlap check pass, but they cannot see any of the following:
- tool access;
- the real sizes of bought parts;
- PEM's edge distances;
- the saddle's squeeze;
- the detent's drag.

The scripts were written against the reviewers' scratch builds, so their paths need adapting. They are a record, not a tool kit.

- `t1canopy_probe_t1.py`, `t1canopy_probe_tilt.py`, `t1canopy_probe_close.py`, `t1canopy_probe_lib.py`, `t1canopy_build1.py`: the canopy critic's probes. They measure the free length along the saddle screws' axis (7.3), the tilt a 6 mm x 120 shaft needs before it clears the tray (55 deg), the splices' 0.3 to the tray, the zone the levers swing through, and the driver's studs against ERP p.11 fig. 7.
- `skeptic-mechanics-and-hanging_canopy_access.py`: tool access along both saddle screws (7.2 free) and the lever opening (WAGO 221-412_K007: 8.2 closed, 15.3 open).
- `skeptic-mechanics-and-hanging_detent_band.py`, `mechanics_detent.py`, `mechanics_halffit.py`, `mechanics_gate.py`:
  - the Kipp K0310.05 ball pushed in about 0.70 through the whole band, which gives 0.10 to 0.26 N m of drag against a slope-0.4 ramp's 0.04 to 0.10;
  - the gate study (a 0.8 step down from each band's ceiling, about 4 deg long).
- `skeptic-texts-and-build_slice_flanges.py`, `skeptic-texts-and-build_measure.py`: the tray U's joint flanges sliced at their holes. The -y flange keeps 0.1 of metal at its free edge, and the +y flange's hole is an open notch. Also a real case placed on the drawn studs: it lands in the -y joint flange and its nut.
- `skeptic-sheets-and-owner_marks.py`, `skeptic-sheets-and-owner_cord.py`: where the one-way marks face (the crown's side is exposed; the collar's top faces up), and the cord's lean in the lock frames.

The full findings are in `../hemisphere-top-v10-critics-2026-11-25.json`.
