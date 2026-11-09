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

## This build (the Tropos-fronts batch, 2026-11-09)

- 164 files, 8.67 MB (8.27 MiB), as built by `web.py`. (Correction: RC3.1 at 2490d9d3 was 160 files and 8.75 MB, not the
  7.3 MB an earlier note gave.)
- The fronts: `renders/2026-11-04/barkhorn/rollout/A-polished-tallr3/` (rig 74f17d7c); `RC_TALL` in `site_v2.py` names
  each source commit.
- Tropos's depth, "428 mm overall, 420 mm at the cabinet": from the speaker lane's figures of 2026-11-09 17:37 ("428
  overall, the amp plate's hardware"), recorded in `owner-queue.md` on `r46-owner-notes`; the speaker lane adds it to
  r33's README.
- Vercel deploys about one push per 15 minutes. A push that gets no deployment lost its window: wait for the next one,
  then push one real follow-up commit.
