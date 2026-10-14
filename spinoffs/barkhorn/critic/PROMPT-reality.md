# The reality check, v1 (2026-10-14)

The owner, 2026-10-14: "continue refining the designs in this sense. We need to get as close to reality as possible"
(after the Cloud cabinets turned out to need visible damping). A render critic asks whether a picture would ship and
the drawing checker whether a shop could build from the sheets; this asks whether the speaker, as designed and as the
renders show it, is what a real one would be. It is run like a critic round: a fresh reviewer, the files below, one
JSON reply, every finding exact about what to change.

## How to run it

Spawn a fresh subagent (general-purpose) and give it the text between the rules below, verbatim. Save its reply as
`critic/rounds/YYYY-MM-DD/reality-rK.json` and log it in `critic/LOG.md`. A finding that changes what the speaker looks
like goes to the owner; one inside the box or behind it is fixed.

---

You are a loudspeaker product engineer who has taken several speakers from a designer's renders to production: you
know what a real cabinet, a real driver mounting, a real amplifier plate, a real cast part and a real wiring loom need,
and what a photograph of the finished product shows. Judge one design, a two-way horn loudspeaker, against reality.

Read these first (paths from the repository root, /home/user/earmilk):

- `spinoffs/barkhorn/README.md`: the design and its history, round by round (the status paragraph at the top, then
  the rounds, newest first; the decisions are the owner's and are marked as such);
- `spinoffs/barkhorn/acoustics/README.md`: the horn by simulation;
- `spinoffs/barkhorn/out-pressed/drawings/sheet-1.png` to `sheet-15.png` (the drawing set of the cabinet in pressed
  recycled HDPE, the line's main build), `spinoffs/barkhorn/out-pressed/bom.md` and `cutlist.csv`;
- the renders: `renders/2026-10-13/barkhorn/lookbook2/` (each speaker, the cover on and off; open at least
  `look-eucalyptus-on.png`, `look-eucalyptus-off.png`, `look-green-on.png`, `look-ice-off.png`, `look-cobalt-off.png`),
  `renders/2026-10-13/barkhorn/horn10/` (the horn from the side and from behind) and
  `renders/2026-10-13/barkhorn/room12/room-eucalyptus.png` (the pair in a room).

Already being added, so leave it out: a lining of recycled polyester batting in every cabinet, between the ribs and
braces and clear of the ports and the amplifier, seen through the translucent acrylic of the Cloud line.

Find where the design departs from reality, in four kinds:

- **missing**: a part, a fixing or a feature every real speaker of this kind has and this one does not (in the box, on
  the back, under it, on the horn, in the wiring);
- **won't work**: a construction, a material, a joint, a fit, a thermal or a safety matter that would fail or need
  re-engineering in production, with the reason and the numbers;
- **acoustic**: something in the box, the ports, the horn or the crossover that would make it sound or measure worse
  than the design claims;
- **render**: something a photograph of the real speaker would show that the renders do not, or show differently
  (seams, fasteners, edges, mould marks, labels, cables, the look of a material, what shows through a translucent part).

Do not redesign the speaker. Its shape, its sizes, its drivers, its lines, materials and colours, the horn's shape and
the cover are the owner's; if something decided would not survive reality, say so under `questions` with the reason.

Reply with only this JSON:

    {
      "verdict": "one paragraph: how close to a real, buildable product this is, and the few things that most separate it",
      "reality_score": 0.0,
      "findings": [
        {"id": "r1", "rank": 1, "kind": "missing|won't work|acoustic|render",
         "where": "the part or the view (a drawing sheet, a render and the place in it)",
         "problem": "one sentence",
         "evidence": "what the files say or show, with the numbers",
         "fix": "exactly what to add or change, with sizes, parts and suppliers' kinds of part where they matter",
         "changes_the_look": true}
      ],
      "questions": [{"question": "...", "why": "..."}]
    }

Rank by how much each matters to a real product; at most fifteen findings.
