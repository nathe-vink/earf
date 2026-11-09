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
