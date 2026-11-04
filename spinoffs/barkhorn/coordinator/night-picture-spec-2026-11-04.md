# Night pictures: the render and site spec (coordinator, 2026-11-04)

Source: the crop-check workflow (wf_ade8d9aa-482). It has three steps:
- A Playwright replica of the held V2 light stage at 743be0cb, checked at 15 viewports with calibration grids.
- An independent recomputation of every row (all within 0.01).
- A skeptic pass over 51 viewports, including landscape phones, split windows and ultrawides.

What the check found:
- The site lane's square 2400 proposal fails all 15 viewports. On 1366x768 and 1536x864 laptops, a square shows only y 0.358-0.781
  of its height under V2's 50% 62% crop, and less as the push grows.
- Today's frames already lose the horn top and the feet there with V2 on.

Adopted: option A, the skeptic's corrected version below. The coordinator added two things for the brand's uses:
- The wide wall's side margins are 5 %, not 4 %, for the teaser's 4 % push.
- The brand's other crops (2.4:1 for the book, brief and press; 4:5 for teaser 4:5 and the press portrait) are cut from these masters.
  Details are under BRAND at the end.

NIGHT STAGE AND WALL, SEVEN COLOURS: CORRECTED SPEC
Option A stays: two art-directed renders per colour. The math for the listed viewports reproduces, and the wide box and the seven-colour snap changes hold. Changes are marked CHANGED or NEW.

RENDER LANE
Make both renders of each colour with one light rig and one grade: the same lamp, exposure, floor and wall.

1. WIDE file, 16:9, 3840x2160. CHANGED from 3200x1800, because 4K and 5K screens draw it at 3840-5400 device px. Use 3200x1800 only if the budget forces it.
- Served to everything that is not PORTRAIT: desks, landscape tablets, split windows.
- Shown with object-fit cover at 50% 50%, scaled up to 1.06 about its centre, in frames from 0.6:1 to 2.4:1.
- The speaker with its lamp sits inside x 0.418-0.582, y 0.20-0.78 (unchanged).

2. TALL file, 9:16, 1440x2560. Use 1620x2880 if affordable, because iPads draw it at about 1740 px.
- Served only when PORTRAIT: 860 px wide or less, and 4:5 or narrower.
- The speaker with its lamp sits inside x 0.35-0.65, y 0.25-0.59. CHANGED from 0.34-0.66 / 0.25-0.61: on 360x512 Android phones the name reaches y 0.61 at the run's end.
- On phones it is drawn 218-260 px tall, 236 px at 390x664.

3. NEW: TEXT ZONES. Keep the floor and wall matte and dark here, at relative luminance 0.09 or less (about sRGB 85/255), with no speculars, so the text holds 4.5:1 without a heavy scrim.
- Wide file:
  - Lower left (name, line): x 0.02-0.44, y 0.69 and below.
  - Lower right (coins): x 0.55-0.98, y 0.77 and below.
  - Top left (kicker): x up to 0.41, y up to 0.22.
  - Top right ('Render'): x from 0.61, y up to 0.22.
- Tall file:
  - Full width from y 0.61 down (name, line, coins).
  - Top, y up to 0.25: x up to 0.50 (kicker) and x from 0.77 ('Render').
- The lamp's light pool and floor reflection stay inside the speaker's columns.
  - Wide file: x 0.42-0.58, faded out by y 0.88.
  - Tall file: the reflection fades out within 0.02 below the lamp.
  - Today's frames have a reflection of luminance 0.13-0.38, up to 0.85, in exactly that place.

4. Keep nothing essential within 4% of any edge. Let the edges fall toward the night ground, #13110F: the site caps frames at 2.4:1 and letterboxes some windows on that colour.

5. THE WALL (all seven).
- Wide, 16:9, 3840x2160: the seven speakers with their lamps sit inside x 0.04-0.96, y 0.16-0.80. CHANGED from a bottom of 0.82, because 'Render' sits at y 0.82-0.83 on short laptops.
- Tall, 9:16, 1440x2560: inside x 0.05-0.95 (CHANGED from 0.03-0.97, for 0.5:1 phones) and y 0.17-0.78 (CHANGED from 0.80).
- On the tall wall, stagger them 4 + 3. In one row each speaker is about 43 px wide on a 390 px phone.

6. If only seven render jobs are possible, use option M: a 3840x2160 master, with phones getting its centre 1215x2160 strip. Use the box x 0.453-0.547, y 0.25-0.59 and the same switch.

SITE LANE
1. Seven colours (kept from the spec).
- V2 light(): range(7) snaps, and .light-run { height: calc(100svh - var(--header) + 7 * 20svh) }.
- The base phone ring divides by 6.
- Change 'The eight colors' to seven in the coins' radiogroup and in light_list. The wall's alt text ('the eight standing along its foot') must change too.
- Push values: 1.0557 at the 7th snap, 1.06 at the run's end.

2. NEW: choose by shape, not width. PORTRAIT = (max-width: 860px) and (max-aspect-ratio: 4/5).
- Stage markup, per colour:
  <picture><source media='(max-width: 860px) and (max-aspect-ratio: 4/5)' data-srcset='TALL-1080 1080w, TALL-1440 1440w' sizes='100vw'><img data-src='WIDE-1920' data-srcset='WIDE-1920 1920w, WIDE-2880 2880w, WIDE-3840 3840w' sizes='max(100vw, calc((100vh - 64px) * 1.78))'></picture>
- show_() sets each <source>'s srcset before the img's.
- Remove web.py's 1600 px cap on reels and V2's 900w/1600w copies.
- Wall: use the same media query on its tall <source>, replacing max-width: 700px (and not 860px). Use srcset 1920w/3840w and 1080w/1440w, and sizes 100vw instead of 1240px. Remove the 2400/1200 caps.
- CSS: move V2's @media (max-width: 860px) stage rules under PORTRAIT: the stacked colour block, the coins row, the 40 px name, the phone scrim and the wall's cover. Keep the list's 2 columns at (max-width: 860px).
- Add, for narrow windows that are not portrait:
  @media (max-width: 860px) and (min-aspect-ratio: 801/1000) { .light-coins { margin: 0; gap: 4px; justify-content: flex-start } .light-coins .ring { translate: calc(var(--at, 0) * 48px) 0 } }

3. Use object-position 50% 50% for both files. This replaces 50% 62%, 50% 60% and the base 50% 55%.

4. NEW: cap the picture at 2.4:1.
- .light-pic { inset: 0 max(0px, calc((100% - (100svh - var(--header)) * 2.4) / 2)); width: auto; overflow: hidden }
- .lightband .facade picture { max-width: calc((100svh - var(--header)) * 2.4); margin-inline: auto }

5. NEW: short viewports.
- @media (max-height: 480px) { .light-run { display: none } .light-list { display: grid } }
- Landscape phones and two-app splits then get the list and the wall, as under reduced motion.

6. Wall fit. Never use cover unconditionally on desks.
- .lightband .facade picture { container-type: size }
- .lightband .facade img { object-fit: contain }
- @container (min-aspect-ratio: 17/10) { .lightband .facade img { object-fit: cover } }
- @media (max-width: 860px) and (max-aspect-ratio: 4/5) { @container (min-aspect-ratio: 53/100) and (max-aspect-ratio: 81/100) { .lightband .facade img { object-fit: cover } } }

7. Scrim.
- Desk layout: no full-width bottom gradient. Darken only behind the name and line and behind the coins, with a radial scrim on each or a text-shadow of about 0 0 28px rgb(19 17 15 / .6). Leave the middle 40% of the frame untouched.
- Stacked layout: start the scrim at the top of the name, not 46% up the frame.

8. Insets: .light-text, .light-list and .eight-render include env(safe-area-inset-left/right).

CHECKED
- Scripts: /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/cropcheck/refk/final_check.py and /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/cropcheck/refk/wall_final.py.
- Data: text measured in Chromium on /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/cropcheck/refk/replica7_fixed.html, stored in /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/cropcheck/refk/dom_fixed.json.
- Coverage: 51 viewports. These are the 15 listed plus ultrawides (21:9, 24:10, 5K2K, 2560x1080), short laptops, landscape phones, split windows, small and tall phones, and iPads. Each was checked at push 1.0, 1.0557 and 1.06, with 2% margins.
- Wide box: clear of the frame edges and all text everywhere, by at least 19 px at zero margin. It is at least 8 px beyond the 2% margin everywhere except 3840x1600, where the line stops 55 px short of the box, inside that frame's 67 px margin.
- Tall box: clear on all 14 portrait viewports beyond the 2% margin.
- Walls: clear everywhere except 'Render', which sits 9 px into the seventh lamp on an iPhone SE in landscape.
- The listed viewports behave as in the spec, except that the tall box is 6% smaller.
- Screenshots: /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/cropcheck/refk/shots/

BRAND (the coordinator's addition)
- Wide wall master, 16:9 3840x2160. The seven sit inside x 0.05-0.95 (5 % sides, for teaser beat 3's 4 % push) and y 0.16-0.80.
  - Teaser 16:9 and the Milan poster take it whole.
  - The 2.4:1 crop for the Book, the partner brief and press landscape is 3840x1600. Place its window (e.g. y 0.10-0.84) so the
    row keeps >=4 % top and bottom inside the brief's 2.5:1 cut.
- Tall wall master, 9:16 1440x2560. The seven are staggered 4 + 3 inside x 0.05-0.95, y 0.17-0.78.
  - The 4:5 crop (1440x1800, full width, a window holding y 0.17-0.78 with margin) serves teaser 4:5, the site's old
    facade-portrait use and the press portrait.
- Smoke is held: the wall shows seven until Smoke's sheet is decided. Any use that says "eight" changes its words, or waits.
