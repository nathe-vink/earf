# Rendering the roll-out in a helper container (2026-11-03)

Use this when the owner has answered both questions: the base (A, or D) and the horn's outside (satin, or polished). Up to 4 containers can each render a share of the queue. Every step below is for one fresh container in this environment. **Don't start until the coordinator names your answers, your SHA, your branch and your chunks.**

## 1. The repo at the SHA

    git fetch origin r33-speaker-horn
    git checkout -b <your-branch> <SHA>          # e.g. r33-rollout-c2, branched from the SHA the coordinator names

Work only on your own branch. Never push to `main` or to another helper's branch, never force-push, and open no pull request.

## 2. The tools

    studio/setup.sh            # idempotent; --doctor also checks Chromium, Cycles, the CAD venv

This installs two Pythons, on purpose:
- Blender's `bpy` wheel (Blender 5.0, Cycles on the CPU, numpy 1) on the system Python, `python3`;
- the CAD venv `.venv-fab` (build123d, numpy 2), for the model builds.

Never install CAD packages into the system Python.

**Check Pillow on the render Python before you render** (2026-11-03: c3's room31 shot failed with `cannot import name '_imaging' from 'PIL'`):

    python3.11 -c "from PIL import Image, ImageDraw, ImageFont"

If it fails, run `python3.11 -m pip install --user --ignore-installed --no-deps pillow` (what worked on c2 and c4; numpy stays 1.26.4) (or re-run `studio/setup.sh`, which does it since this fix). Ubuntu's `python3-pil` is built for 3.12 only, so a bare `import PIL` passes and hides the failure.

## 3. The two render models (not in git; both are rebuilt from the code at your SHA)

Run each build as a tracked background task, one after the other, never side by side:

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud
        # writes spinoffs/barkhorn/out-cloud/render/barkhorn-cloud.glb (about 73 MB). The full kit build: the
        # drawings and checks too. Its time is not measured; budget up to an hour
    .venv-fab/bin/python spinoffs/barkhorn/variants/render_model.py
        # writes spinoffs/barkhorn/variants/out/render/barkhorn-variants.glb (about 16 MB); about 21 min alone,
        # 30 or more beside another job

Check both files exist before you render.

**The build rewrites a tracked file: `studio/products/barkhorn-variants.json`** (c2 saw this, 2026-11-03). `render_model.py` writes it from `product.py`, so its 17 `horn-satin` entries come out at roughness 0.05. That is the polished horn (the owner, 15:14): `FORMED_HORN_SATIN = 0.05`, and the material keeps its old name. Before 0.05 was committed (the commit that adds this note), the file in git still said 0.25, from a build made before the decision. The shots set 0.05 for polished anyway (`strata_lit`), so no render was affected. Since this commit, your build should leave the file unchanged. **Never commit the file from a helper branch, and never revert it.** If your copy shows the diff before a merge, discard your copy first, so the merge doesn't stop on a local change: `git checkout -- studio/products/barkhorn-variants.json`. Don't rebuild a model while a render runs: a render reads the models only in its first minute, but a half-written file breaks it.

## 4. The Poly Haven cache (not in git)

`studio/assets/cache/` (about 430 MB, all CC0) fills itself on demand: `studio/engine/assets.py` fetches what a shot needs from polyhaven.com, with no login. The deck's home frames need room31's models and textures from it. Nothing to do, unless the network blocks polyhaven.com. If it does, report it; don't work around it.

## 5. Your chunks

    python3 spinoffs/barkhorn/campaign/rollout.py --base A --horn satin --chunks 5-7,11
        # writes the shot files and queue-NN.sh into spinoffs/barkhorn/campaign/rollout/A-satin/ (not committed)
        # and prints one line for each of your chunks:
    bash spinoffs/barkhorn/campaign/rollout/A-satin/queue-05.sh

Rules:
- **Run each chunk as its own tracked background task**, never with setsid, nohup or `&`. Each chunk is about 100 estimated minutes, under the 2-hour task limit.
- **One chunk at a time, one render at a time.** Two renders side by side have run out of memory here (the biomes lane, 2026-11-03). Each render stays under 13.5 GiB alone.
- **Start the next chunk only when the last one has landed.** If a chunk dies part way through, re-run only the shots without a PNG. The queue's lines are plain commands; copy the missing ones.
- **Kill a process only by its PID.**

`--split 4` prints the proposed split for all four containers (below).

## 6. Where the renders go, and committing them

The renders land in `renders/2026-11-04/barkhorn/rollout/<base>-<horn>/<shot>.png`, each with `.shot.json` and `.report.json` beside it. After each chunk:

    ls -la renders/2026-11-04/barkhorn/rollout/A-satin/          # every PNG under about 5 MB
    git add renders/2026-11-04/barkhorn/rollout/A-satin/<shot>.png renders/2026-11-04/barkhorn/rollout/A-satin/<shot>.shot.json renders/2026-11-04/barkhorn/rollout/A-satin/<shot>.report.json
    git commit -m "Tropos roll-out <base>-<horn>, chunk NN: <shots>" -m "<the session's trailers>"
    git push -q -u origin <your-branch>

Rules for committing:
- **Stage only those paths.** Never commit `*.raw.png` (the unfinished render beside each PNG), the shot folders under `campaign/rollout/<tag>/`, or the models.
- **A PNG over 5 MB:** the deck's cover (3840 x 1360) was 4.7 MB last time. If one is over, recompress it losslessly (`convert in.png -strip -define png:compression-level=9 out.png`), check it again, and say so in your report.

## 7. What to report to the coordinator

After each chunk, one short message:
- the chunk's number and its shots;
- the commit's full SHA, copied from git's output;
- each shot's render minutes, from its `.report.json` `seconds.render`;
- anything wrong. A failed or killed render is reported with its error line, never hidden.

At the end, a list of your shots with the SHA for each.

## The run: A, polished, Smoke held (the owner, 2026-11-03 15:11 and 15:14)

    python3 spinoffs/barkhorn/campaign/rollout.py --base A --horn polished --hold smoke --chunks <yours>

Smoke's five site frames are held back (`--hold smoke`) while its sheet is open, which leaves 40 shots, about 20.6 h, in 15 chunks:

| container | chunks | shots | est. |
|---|---|---|---|
| 1 (the speaker lane) | 1-4 | the deck: hero, row, cover, home | 5.7 h, after the deck hero's framing proof |
| 2 | 11, 13, 14 | hero-light poison and ice; side ember to ice; side haze and fog, back ember to ice | 4.5 h |
| 3 | 5, 6, 10, 15 | deck home portrait, front-off-tall (all but smoke), hero-light dust and acid, back haze and fog | 4.8 h |
| 4 | 7, 8, 9, 12 | front-off-wide (all but smoke), hero-light ember, haze and fog | 5.6 h |

The held shots: site-front-off-tall-smoke, site-front-off-wide-smoke, site-hero-light-smoke, site-side-smoke and site-back-smoke. Run them later, with `--hold ''`, once Smoke's sheet is set.

## Phase 2: the rest of the site (proposed 2026-11-03; no renders until the coordinator confirms)

**Approved** by the coordinator, 2026-11-03 15:44. To move a helper from phase 1 to phase 2, after its last phase-1 chunk has landed and been pushed:

    git fetch origin r33-speaker-horn
    git merge --no-edit 9db8da171425bd5ca89ad439f9e0aeecda211c7b     # on your own branch: a merge, never a rebase or a force-push
    git push -q -u origin <your-branch>
    python3 spinoffs/barkhorn/campaign/rollout.py --phase 2 --base A --horn polished --hold smoke --chunks <yours>
    bash spinoffs/barkhorn/campaign/rollout/A-polished-p2/queue-NN.sh      # each chunk its own tracked task, one at a time

- **The models need no rebuild.** Between 5295e58f and 9db8da17 only `rollout.py`, this file and some committed renders changed. No product file and no CAD source changed, so the two `.glb` models built at 5295e58f are still right.
- **The merge can't conflict:** a helper's branch holds only its own renders under `renders/2026-11-04/barkhorn/rollout/`.
- **Where phase 2's renders go:** `renders/2026-11-04/barkhorn/rollout/A-polished-p2/`. Commit and report them as in phase 1.
- **Your chunks:** c2: 1, 4, 9. c3: 2, 5, 10. c4: 3, 6. The speaker lane: 7, 8. Chunk 1 holds Sound's Ice arc; if your container is the first to finish phase 1, say so, and the coordinator may give you chunk 1 first.

    python3 spinoffs/barkhorn/campaign/rollout.py --phase 2 --base A --horn polished --hold smoke --chunks <yours>

The site lane's list (`r47-site-next`, `spinoffs/barkhorn/launch/PICTURES-2026-11-03.md`), each built from its old rig by `strata_lit`, as the site frames are. With Smoke held: 211 shots, about 15.8 h, in 10 chunks:

| item | shots | est. | chunk |
|---|---|---|---|
| the front arc in Ice (the home's Sound), first | 9 | 0.5 h | 1 |
| the front arc, the other six | 54 | 3.3 h | 1-3 |
| the dark-ground studio, Ember | 1 | 1.1 h | 3 |
| the amplifier plate, Ember (one: the plate is the same on all eight) | 1 | 0.3 h | 4 |
| horn A from behind, x 8 (seven with Smoke held): each tint's horn has its own depth, and polished shows it | 7 | 2.3 h | 4-5 |
| the inside, one (Ice): the same build in every tint | 1 | 0.5 h | 5 |
| the turning sprite, 24 frames x 7, at the arc's 32 samples (the rig's 128 would be about 4x) | 168 | 4.6 h | 6-8 |
| the close-ups with rigs: horn mouth (Acid), cabinet edge (Ember), plate (Dust), grip (Poison) | 4 | 3.1 h | 9-10 |

After phase 1, each container takes these. The container that finishes phase 1 first takes Sound:
- c2: 1, 4, 9 (9.3 h in all);
- c3: 2, 5, 10 (9.6 h);
- c4: 3, 6 (8.9 h);
- c1: 7, 8 (8.6 h).

Not in phase 2:
- **Covers on (x 8): not renderable as designed.** Horn A's woofer sits in the caldera, which the cloth cover does not fit (`asset/README.md`). The owner's call: drop the cover switch, or design a cover for the caldera.
- **The room:** that is phase 1's `deck-home` and `deck-home-portrait`. Its two cable props are checked in the deck hero's proof round.
- **The reels and the uplit eight:** held for the owner.
- **The back mark and the coin close-ups:** no rig yet; to be defined.
- **The GA drawing:** CAD, from the Cloud's fab build, with Strata's posts and caldera added.

## The proposed split (`rollout.py --split 4`; estimates, about 9 min per megapixel per 64 samples)

The chunk numbers are the same for satin and polished. The deck's four chunks go to container 1, so the deck lands first.

| | A (45 shots, about 22.6 h) | D (53 shots, about 24.7 h: A's, plus 8 night lanterns) |
|---|---|---|
| container 1 | chunks 1-4: the deck hero, row, cover and home (about 5.7 h) | chunks 1-4 and 7 (about 6.9 h) |
| container 2 | chunks 5, 6, 7, 11 (about 5.6 h) | chunks 9, 12, 14, 16 (about 6.0 h) |
| container 3 | chunks 10, 13, 15, 16 (about 5.5 h) | chunks 6, 8, 11, 17 (about 5.9 h) |
| container 4 | chunks 8, 9, 12, 14 (about 5.8 h) | chunks 5, 10, 13, 15 (about 5.9 h) |

Before the deck's finals, one framing proof of the deck hero at proxy samples:

    python3 studio/engine/render.py spinoffs/barkhorn/campaign/rollout/<tag>/deck-hero.json --out <scratch>/deck-hero-proof.png --scale 0.5 --samples 32

The deck hero is built from gate 2's A frame at 2:3, not the 4:5 it passed at.
