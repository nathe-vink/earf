# Building the r49 release candidate

`r49-site-rc` has `COPY_NEXT`, `V2`, `HOME_V2` and `RC` on in `web.py`.

The RC build prunes `site/img` and `site/press` down to the files the release candidate deploys. `web.py` also reads source
pictures from those folders (for example `red-habitat-1200.jpg`). So a build on top of an already pruned tree stops with
`FileNotFoundError`. That happened at 148fb466; cf5af9aa fixed it.

Before every rebuild on this branch:

1. Restore the sources: `git checkout r47-site-next -- spinoffs/barkhorn/site/img spinoffs/barkhorn/site/press`
2. Build: `cd spinoffs/barkhorn && python3 web.py`, and **check the exit code**. A non-zero exit means `site/` is partial: do not
   commit it.
3. Check: the route sweep, the overflow check and the forbidden-file assertion (inside `web.py`) all pass.
4. Stage `site/` with `git add -A spinoffs/barkhorn/site`, so the restored and then pruned files cancel out against HEAD.
   Then stage the other intended paths by name, and read `git diff --cached --stat`.
5. Then commit and push.

The screenshots in this folder are from the first RC and are out of date.

## This build (the Tropos-fronts batch, 2026-11-10)

- 157 files, 8.32 MB, as built by `web.py` (all seven horn-backs; 151 files, 8.21 MB at 738691f0; 145 files, 8.02 MB at 6b72d0aa). (Earlier: RC3.1 at 2490d9d3 was 160 files and 8.75 MB, not the 7.3 MB an
  earlier note gave.)
- The fronts: `renders/2026-11-04/barkhorn/rollout/A-polished-tallr6/` (rig fa7665dc); `RC_TALL` in `site_v2.py` names
  each source commit. Restored (re-rendered without the hidden lamp): Ember's turn and all seven horn-backs.
  Out of this build, each until its re-render passes: the Back views, Fog's and Dust's habitats, the lamps' picture, Mantle's picture (the owner turned it down).
- Tropos's depth, "428 mm overall, 420 mm at the cabinet": from the speaker lane's figures of 2026-11-09 17:37 ("428
  overall, the amp plate's hardware"), recorded in `owner-queue.md` on `r46-owner-notes`; the speaker lane adds it to
  r33's README.
- Vercel deploys about one push per 15 minutes. A push that gets no deployment lost its window: wait for the next one,
  then push one real follow-up commit.
- Pushed 6b72d0aa at 2026-11-10 00:22:05 UTC inside a closed deployment window (the last deployment 00:17:40); this line is the follow-up push for the next window.
- Pushed c5016e3f at 2026-11-10 01:33:44 UTC; r48-mantle-design's push took that window (01:34:30). This line is the follow-up push for the next one.

## The eight-color batch (2026-11-10, morning)

- 170 files, 8.55 MB. Eight colors with Smoke, in the black-rods set (r33-speaker-horn 370de3da: A-polished-tallr7 fronts,
  A-polished-p2-p2b horn-backs and turns); the habitats out until black-rods re-renders land.
- The mark: the approved globe from r47-brand c19abdba, kept in `brand/site-rc/` (film, poster, the header's 60-frame sheet,
  the touch icon); no night film. The dots are flat chips in the logo's colors.
- `rc_finish` runs after web.py's favicons and vercel.json: the touch icon, the favicon titled EARF, no journal redirect.
- Then: Smoke smoked gray; the Ice and Fog habitats back with black rods (r48-biomes 2904138e). 174 files, 8.69 MB.

## The owner's review of the opening and the home (2026-11-10, afternoon)

- 165 files, 8.2 MB. Home: one full-width picture (Ice in the snow at dusk, black rods), the line over its sky, the four
  products below; no figures (they stay in the Tropos spec) and no row of fronts. `hotspot_hero()` puts a point on it
  (Tropos in Ice), behind `HOTSPOTS`.
- The opening: no video and no canvas. `rc_intro` packs 43 of the non-flashing alpha frames (r47-brand 92142eb5, kept in
  `brand/site/globe-turn-alpha/`: f0078 ... f0119, f0000) into `img/globe-arc.webp` (288 px tiles, 7 x 7, 555 KB). The
  globe eases into a turn during the hold and lands on f0000; the header shows f0000, still. The site uses no globe film.
- "Ember to Smoke" reads "the full spectrum" (`SPECTRUM`, applied in `rc_finish`).
- Pushed 60785c93 with r47-site-next at 2026-11-10 17:38:55 UTC; Vercel took r47-site-next's push for that window.
  This section is the follow-up push for the next one. Push r49-site-rc on its own.
