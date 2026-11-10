# Brand Book audit and plan (workflow wf_99b98a3d, 10 Nov 2026)

NOTE: written before the owner's decisions of 10 Nov 02:15-03:00 (see approved-renders.md, OWNER DECISIONS). Where they differ, the decisions win.

## BRAND LANE BRIEF
TO THE BRAND LANE (you own brandbook/make_book.py, book/index.html and press/)

Do it in one pass, in this order. No new renders are needed.

0. START
- Branch from origin/r47-brand at 7d6b3d41 or later. That is what was published as version 25.
- Do not start from v23: its idents and Mantle line are already fixed in src.
- Anchors below are v23 lines. In src, subtract 1 up to L410 and 3 from L413 on.
- Tools are in /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/book-current/plan/tools/:
  - check_book.py: the pre-publish checks.
  - grep_baggage.sh: the grep list.
  - apply_plan.py: every edit below as exact old → new strings, each asserted to occur exactly once in src. Run it on src, or edit by hand.
  - archive_manifest.py, and its output ../archive_manifest.json: the 178 blocks the archive must hold.
- plan/test/mock-book.html is a test output. Do not publish it.
- The coordinator asks the owner the two questions in chat, one at a time. Build now with both answers set to "no". If either comes back yes, add its block in step 4.

1. CUTS
Each cut block goes verbatim to the archive (step 6).
- #cover: L324, "New in this edition".
- #names:
  - L374 Planet EARF;
  - L375 Mother EARF;
  - L376 Crust · Strata · Ozone;
  - L382 the model code (TR-1).
- #identity:
  - L392-393, the render lockups (replace them as in step 5);
  - the .four row (L395-400) becomes a .two row with Drawn flat and One color, which drops globe-paper.jpg and globe-real.jpg with their captions and "<!-- the object -->";
  - the <div class="motion solo"> block with globe-turn.mp4.
- #color: L440-441, the Smoke card.
- #images: the orphan "Through the wall..." caption at the end of L489, with its stray </figure></div>.
- #voice: L521 The record; L532, the Choose your weather row.
- #applications:
  - the L543 card.jpg figure and the L552 stationery.jpg figure (both blocks become "app nopic");
  - L546-548, the rating plate;
  - the tote sentence and its dt/dd (L553-554);
  - L555-557, the signs;
  - L558-560, EARFcoin.
- Whole chapters:
  - #packaging (L564-594);
  - #ideas (L596-624);
  - #facts (L657-684);
  - #parked (L686-692).
- #press:
  - L636, the "In development." tag;
  - L639-643, the pitches and the local note.
- Source:
  - --smoke in :root;
  - the process-named rules: .slab.held (2), .tint .pic .gap.held, ".gap.held b, ...", .cover .new (3), .gap (8), .stratum.reserve h3 (2), .prop, .tocome (3), .inprog (2), .parked (5);
  - the dead rules: .decals (3), .steps (6), .scroll, table (2), "th, td", th, tr:last-child, td.num, .feature (6), .fcols (2), .gets, .legal (2), .pairml (4), .facts, .motion (2);
  - the "/* packaging */" comment;
  - the blank residue lines.

2. REWRITES
Exact. The full strings are in NEW_BOOK_OUTLINE and in apply_plan.py.
- Head comment: "...with night bands where the glow needs them." (drop "the bar").
- L319 → "EARF · San Francisco · the brand book · November 2026".
- L323 → "...This book is how EARF looks and sounds, and where it is going, so that..."
- L370: cut the naming date and the lawyer's search.
- L379 → "Always EARF, in capitals, as one word. The site is earf.world."
- L381: cut "08 Smoke is held."
- L390: cut "as the proposed Mother EARF would be".
- L397 caption → "Drawn flat. Six discs in six of the tints: the mark on paper and on screen, and for screen printing, embroidery and small sizes in color."
- L399 caption → "...For etching, engraving and the rating plate."
- L402: cut "a coin, the door".
- L404 → "Below 64 px the globe keeps its whole drawing and only its seams widen: separate files at 64, 32 and 16 px keep its lines open."
- New Identity rule: "Motion: The globe may turn on its axis. It is the only motion the mark makes."
- L416 → "the first frame of a film, the spine of a box."
- L424: cut the Smoke sentence.
- L443: the Acid sentence replaces the chip sentences.
- L444 → "Night is for the glow."
- L455 → "A printed or digital surface carries one tint, or all seven in order. Never two or three picked for a mood."
- L456 → "Where pieces in different tints share a room, they pair by the painter's wheel: one tint throughout, a tint with its complement, or a tint with its two neighbors; Fog, with no hue, goes with the cool tints."
- L489 lede → "Three kinds of picture, each with one job: the studio, in its element, and up close. ..."
- L354 and L492 → "in its element" and "Each tint in its own landscape".
- L493: cut the "predates" clause.
- L530 → "Seven horned speakers in colored acrylic."
- L542 → "How the name appears on paper, on screen and in the box."
- L544 → "...is for the people who ask."
- L553 → "The care card goes in every box, in the site's own words, because the wrong cleaner crazes acrylic for good."
- The press chapter head → "09 · The line".
- L629: cut "the project logs" and the "held" sentence.
- Write → hello@earf.world.
- Colors → "Seven, the same in every product".
- Sells → "Made to order; price on request".
- Hemisphere Light → "2700 K, CRI 90; the dome glows in its own color, and the light straight down is the lamp's own warm white".
- Hemisphere Mains → "120 V, dimmable".
- Core: add "its color an even depth all round".
- Mantle: add the Posts and Base rows from RC:1081; cartridge → "a moving-magnet cartridge".
- L638 → "...design figures until measured; price on request."
- Footer → "EARF Brand Book · November 2026" / "Every picture is a render until the first pieces are built and photographed."

3. RENUMBER AND RENAME
- Nav tail → <a href="#applications">Applications</a><a href="#line">The line</a><a href="#going">Where it's going</a>.
- Contents → 09 The line (#line), 10 Where it's going (#going).
- Section id="press" → id="line".

4. THE NEW CHAPTER
- Insert <section class="chap band" id="going"> before <footer>, with the head, lede, the four-step .timeline and the .cols directions given in NEW_BOOK_OUTLINE. It reuses the existing CSS.
- On a yes to question 2, add: <div><h3>Smoke</h3><p>A smoked gray, in development to join the seven.</p></div>.
- On a yes to question 1, add the Planet EARF block.
- Both go inside #going only, with no pictures.

5. PICTURES: THE APPROVED LIST ONLY
make_book.py:
- BRAND keeps only globe-flat.png, wordmark-color.png, lockup-black.png and lockup-white.png.
- Save brand/mark/earf-lockup-colour.png as lockup-color.png at 1200 px. The header and the paper plate share it.
- Drop lockup-paper, lockup-night, globe-paper, globe-night, globe-real and globe-real-night.
- Drop 'smoke' from the icon loop.
- Drop the globe-turn.mp4 copy.
- Rename the PINNED keys:
  - honest-front-<t>.jpg → tropos-front-<t>.jpg;
  - honest-ice-habitat.jpg → tropos-ice-snow.jpg;
  - honest-amp-ember.jpg → tropos-amp-ember.jpg.
- Remove the BAR renders and the launch/ and kickstarter/ loops.

Add an allowlist to prune() and fail the build on anything else. The allowlist is the same as ALLOWED in check_book.py (22 pictures plus index.html):
- tropos-front-{ember,dust,acid,poison,ice,haze,fog}.jpg;
- tropos-ice-snow.jpg, tropos-amp-ember.jpg, social.jpg;
- globe-flat.png, lockup-color.png, lockup-white.png, lockup-black.png, wordmark-color.png;
- icon-{seven tints}.png.

Nothing else enters until the coordinator adds it to approved-renders.md. Candidates for later:
- the globe re-rendered in today's speaker colors (owner 01:54:53Z);
- the card and stationery redrawn with the flat globe;
- the seven horn-from-behind views (already listed, AR:76-77; optional).

6. BUILD THE ARCHIVE AS ITS OWN ARTIFACT (see ARCHIVE_OUTLINE)
- Write brandbook/archive/index.html, with an optional make_archive.py. Its sources:
  - every entry of archive_manifest.json, verbatim, under its topic, with the v23 anchor, the reason and what the Book now says;
  - the 95 non-KEEP rows of audit-surfaces/items.json;
  - the dated decision log, the open list, the deck's history, and the removed-pictures list with git paths.
- First line: it is internal, and no stakeholder-facing page links to it.
- No embedded pictures.
- Publish it as a NEW private artifact, separate from the Book. Do not pin it. Send its link to the coordinator only.
- Never put its URL in the Book, the site, the press kit or the deck.

7. PRESS KIT
- Make the edits in SURFACE_FIXES (Press kit).
- After the renames, rebuild the PDFs with make_sheets.py (SEVEN, the Tropos picture, and the src() prefix "tropos-").
- The kit stays unreleased (WT 238).

8. CHECKS BEFORE PUBLISHING (all must pass)
a. Run the checker:
   python3 plan/tools/check_book.py spinoffs/barkhorn/brandbook/book/index.html book-current/audit-book/items.json spinoffs/barkhorn/brandbook/archive/index.html --planet no --smoke no
   Set --planet or --smoke to yes after a yes from the owner. It must print "0 failures; 0 audited blocks neither in the Book nor in the archive". It checks:
   - the baggage words;
   - Smoke and Planet EARF appear only inside #going, and only after a yes;
   - #packaging, #ideas, #facts and #parked are gone; no process classes or rules; no HTML comments;
   - every picture is on the allowlist;
   - every #anchor resolves, and the nav, contents and chapters agree;
   - external links go only to Google Fonts, earf.world and hello@earf.world;
   - no artifact links;
   - American spelling;
   - each of the 315 audited blocks is still in the Book or is in the archive;
   - the archive says "Internal" at its top.
b. Run sh plan/tools/grep_baggage.sh book/index.html. It must print nothing; after a yes, its last two greps may hit only lines inside #going. Its main grep:
   grep -n -i -P '\b(second edition|this edition|new in this edition|draft|held|parked|pulled|propos(al|als|ed|e)|placeholders?|for review|to be (drawn|chosen|decided|confirmed)|to follow|to come|still open|is open|open question|in progress|pending|tbd|target|settled|undecided|decided|eight|coins?|idents?|earthrise|sessions?|founding|founders?|kickstarter|deposits?|reservations?|investors?|funding|grants?|pre-seed|raise|wallpaper|monocle|dwell|kinfolk|embargo\w*|amsterdam|milan|vienna|festival|suites?|atmosphere|something in the air|choose your weather|weather|where (its color|it) began|round \d+|tallr\d|honest|earlier|previous(ly)?|no longer|instead of|retired|replaced|predates|used to|we tried|first pass|is now|owner|coordinator|lane|critics?|gate|mask(?!-)|approved list|house book|project (logs?|record)|as of|big ideas|raise the odds|idea \d|tr-1|packag\w*|crates?|debut|jacket|invitation|tint library|album|buyers?|artists?|first hundred|record player|cloth cover|custom-poured|made in san francisco|no light|launch|teasers?|press kit|signs|tote|reserve|model code|wording|colour\w*|grey|neighbour\w*|aluminium|metre|centre)\b|\best\.'
   The script also runs three more greps:
   - a case-sensitive one for Dome, Orb, Cloud, Cumulus, Bell, Strata, Crust, Ozone, RC tags, "$", "9 November", "<!--", "--smoke", process classes and the removed chapter ids;
   - '\bsmoke\b';
   - '\b(planet earf|mother earf|earfcoin|the bar|bar.s)\b'.
   On v23 the main grep hits 172 lines. On the test build it hits 0.
c. grep -rn "<archive id>" across spinoffs/barkhorn/site, press and brandbook/book must find nothing. Check the deck too.
d. Look at the page at 390 px and 1440 px: no horizontal scroll, and no empty grid cells.
e. hello@earf.world must receive mail (WT 240 says it bounces). If it does not, remove the Write row before the link goes to anyone outside.

9. PUBLISH
The Book: republish to https://claude.ai/artifact/WGpswpvvETozjgRAxBuUK3, which keeps the owner's link.
- Files left out of an update are KEPT, so pass null for each of these:
  - img/card.jpg;
  - img/decal-crate-front.jpg, img/decal-crate-inside.jpg, img/decal-crate-side.jpg;
  - img/globe-paper.jpg, img/globe-real.jpg, img/globe-turn.mp4;
  - img/icon-smoke.png;
  - img/idea-founding.jpg, img/idea-hotel.jpg;
  - img/lockup-night.jpg, img/lockup-paper.jpg;
  - img/plate.jpg, img/stationery.jpg;
  - the nine old names: img/honest-front-{ember,dust,acid,poison,ice,haze,fog}.jpg, img/honest-ice-habitat.jpg, img/honest-amp-ember.jpg.
- Add the nine tropos-*.jpg files and img/lockup-white.png.
- Replace index.html and img/lockup-color.png.
- Then list the artifact's files. Exactly 23 must remain.
- Read the page back and run check_book.py on it.

The archive: a separate new private artifact.

Commit on r47-brand, recording the version numbers. The coordinator then gives the owner the Book link in chat, with two lines on what changed. He does not open separate pages for status (02:03:57Z).

WATCH ITEMS
If the owner decides any of these, change only the anchors listed in NEW_BOOK_OUTLINE: Poison's name, the posts, Mantle's word, the lamps after their redraw, FA123, and the tint values after the chips.

## NEW BOOK OUTLINE
The full plan is in /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/book-current/plan/plan.md. Nothing was committed, pushed or published.

EVIDENCE KEY
- v23 Lnnn: the audited Book (artifact version 1794271571-295d).
- src: origin/r47-brand 7d6b3d41 brandbook/book/index.html (published as version 25, 1794275254-44ef).
  - A src line is the v23 line minus 1 through L410, and minus 3 from L413 on.
  - The idents (v23 L411-412) and the Mantle line (v23 L668) are already changed in src.
- AR:n: coordinator/approved-renders.md at cd1b8ea0 (02:07 UTC). The audits used an older numbering.
- WT n: coordinator/walkthrough.md.
- README:n: spinoffs/barkhorn/README.md, the owner notes at 3e41fefc.
- RC:n: origin/r49-site-rc 738691f0 site/index.html.
- Owner times: UTC send times from the transcript's queue records. Example: the lamp notes were sent at 00:24:30Z and 00:26:55Z and delivered at 00:28:39Z.

WHERE THE AUDITS DIFFER, AND THE CALL TAKEN
1. Packaging leaves the Book. It is an unanswered proposal: WT 284, "Yes or no on the packaging idea". The Book audit would only have deleted its "proposal" tags.
2. Smoke.
   - The Book shows the seven that are pictured, sold and on the site.
   - The owner said at 01:49:09Z: "I still want smoke rendered as we ideally want it and we can work backwards from there".
   - Whether to name Smoke as coming is question 2. Holding it was a coordinator call never put to him (coordinator, 01:47:37Z).
3. Hemisphere's light follows the site and the owner's 00:24:30Z direction, without the 575 lm figure. The table light is open again (AR:25-27).
4. Special editions stay out until he confirms them: his idea (2026-10-31T20:35:49Z), not a decision.
5. "Site: 1, launch film." (2026-11-03T04:27:42Z) chose the site's direction, not a film. The wordmark rule therefore says "a film".
6. Two rules now follow the owner's words:
   - Small sizes follows "I don't like changing the form at smaller sizes" (README:696).
   - The conflicting color rules (L455, L456) are reconciled with his complementary, analogous and monochromatic pairing (README:132).
7. The tote leaves with the bar (L553: "The tote is the bar's").
8. The Press kit chapter becomes "The line" (id line). The press kit itself stays unreleased (WT 238).
9. "Write: hello@earf.world" stays only if the mailbox receives mail. WT 240 says it bounces.

THE NEW BRAND BOOK: ten chapters, the brand as it is now, then where it is going

Rules
- Current: what the owner decided, or what the site preview says publicly. Product facts are copied word for word from RC:999 and RC:1081.
- Forward: only what the owner decided or clearly set. Everything else goes to the archive.
- Pictures: the approved list only (AR:6):
  - the seven tallr6 fronts (AR:73);
  - the Ice habitat (AR:88);
  - the Ember amp plate (AR:78);
  - social.jpg, made from these (AR:38-39, 73);
  - the flat marks (AR:137, "the flat marks stand in").

Result
- 10 chapters, down from 13 plus Parked.
- 178 of the 315 audited blocks move to the archive (plan/archive_manifest.json).
- The published files go from 36 to 23.
- Every edit below was applied to src as a test (plan/test/mock-book.html). The test build passes the pre-publish checks with both answers to each owner question.

Order: Cover · Contents · 01 Position · 02 The naming system · 03 Identity · 04 Color · 05 Type · 06 Image direction · 07 Voice · 08 Applications · 09 The line · 10 Where it's going · footer.

HEADER AND COVER (#cover)
Job: say what EARF is and show the seven at a glance.
- Keep:
  - L309, the flat header lockup.
  - L320, the seven fronts with "Tropos in the seven, each on its own feet, cover off. Render" (AR:73; cover off, owner 2026-10-31T20:32:59Z; "No light", 2026-11-03T15:11:16Z).
  - L321, "A world of sound, in color." (owner 2026-11-02T15:48:15Z).
  - L326-334, the strip of the seven tints.
- Rewrite:
  - L319 eyebrow: "EARF · San Francisco · the brand book · November 2026" (was "second edition, 9 November 2026 (draft)").
  - L323 lede: "Hi-fi and light, cast in tinted acrylic. This book is how EARF looks and sounds, and where it is going, so that everything made under the name feels like it came out of one room." The old "arrives" pointed at Packaging, which leaves. The owner's brief (00:53:14Z) asks to show where it is going.
  - L311-312 nav: Contents · Position · Names · Identity · Color · Type · Images · Voice · Applications · The line · Where it's going.
- Cut: L324, the "New in this edition" change log (archive §7).

CONTENTS (#contents)
Job: the map.
- L340 becomes: 01 Position · 02 The naming system · 03 Identity · 04 Color · 05 Type · 06 Image direction · 07 Voice · 08 Applications · 09 The line · 10 Where it's going.

01 POSITION (#position)
Job: what EARF is, for whom, why now, and what it holds to.
- Keep:
  - L347, the head.
  - L349 What EARF is (matches RC:1007-1018).
  - L350 For whom.
  - L351 Why now.
  - L354, the Ice habitat (AR:88).
  - L357-360 What the brand holds to (L360 matches RC:967).
- Rewrite: L354 caption: "In snow. Tropos in Ice, in its element. Render" (was "where its color began"). The habitats are the owner's direction: "Go on all of the biome work" (2026-11-03T03:09:52Z).

02 THE NAMING SYSTEM (#names)
Job: the company, the four products, the tints, and how to write them.
- Keep:
  - L367-368.
  - L371, Hemisphere.
  - L372, Core (Core B, owner 2026-11-09T21:11:07Z).
  - L373, Mantle ("Mantle: A", 2026-11-01T12:11:46Z).
  - L380, the product rule.
- Rewrite:
  - L370, Tropos: end at "...named for the Greek tropos, a turn. The speaker fills the air of a room." Cut "Chosen on 29 October 2026 after Atmosphere was found taken in audio; a lawyer's search confirms before filing." It is naming history (README:138), and the search has not started (WT 248).
  - L379: "Always EARF, in capitals, as one word. The site is earf.world."
  - L381: cut "08 Smoke is held."
- Cut:
  - L374 Planet EARF and L375 Mother EARF (archive §4a). They come back only in chapter 10, and only on a yes to question 1.
  - L376 Crust · Strata · Ozone (open, WT 283; §4e).
  - L382, the model code TR-1, marked "Proposed" (§4d).

03 IDENTITY (#identity)
Job: the globe, the wordmark, the lockups and their rules, shown with the flat marks.
- Keep:
  - L389, the head.
  - L397, globe-flat.png.
  - L399, lockup-black.png.
  - L403 clear space, L405 on a picture, L406 never, L407 files.
  - L415, wordmark-color.png: a flat mark in today's Mark hexes. The owner said yes to a color per letter (README:474).
- Rewrite:
  - L390 lede: cut "as the proposed Mother EARF would be".
  - L392: the flat color lockup, img/lockup-color.png, made from brand/mark/earf-lockup-colour.png at 1200 px. Alt: "The EARF lockup on paper: the color globe and the black wordmark".
  - L393: the flat white lockup, img/lockup-white.png, made from brand/mark/earf-lockup-white.png. Alt: "The EARF lockup at night, in white".
  - L395-400: four figures become two:
    - "Drawn flat. Six discs in six of the tints: the mark on paper and on screen, and for screen printing, embroidery and small sizes in color."
    - "One color. Black, white, or any one tint. For etching, engraving and the rating plate." ("the door" is cut.)
  - L402: "...except where the globe stands alone (an icon) or the wordmark does..." ("a coin, the door" is cut.)
  - L404: "Below 64 px the globe keeps its whole drawing and only its seams widen: separate files at 64, 32 and 16 px keep its lines open." The owner: "I don't like changing the form at smaller sizes" (README:696).
  - L416: "...the first frame of a film, the spine of a box." ("a wall at the bar" is cut.)
- New rule: "Motion: The globe may turn on its axis. It is the only motion the mark makes." The owner asked to keep the globe turning (README:118). The video goes.
- Cut, with their captions and "<!-- the object -->":
  - L392-393, the rendered lockups.
  - L396, the rendered globe.
  - L398, "As an object".
  - L410, globe-turn.mp4.
  - Why: the globe_real.py renders fail on three counts (AR:133-138), and the owner finds "as an object" too cheap (01:54:53Z).
  - The v23 L411-412 idents are already out at the owner's word (01:45:42Z).
  - All of these go to archive §6b and §4a.
- Later: the globe is being re-rendered in today's speaker colors (owner 01:54:53Z; r47-brand 824677cb, 134b0d6a). Once it passes the gate and joins the list, the rendered lockups can return to the two plates.

04 COLOR (#color)
Job: the seven tints with names, lines and values, the neutrals, and the color rules.
- Keep:
  - L423 "Seven colors, Ember to Fog.": the seven that are pictured, sold and on the site (AR:73, RC:7).
  - L426-439, the seven cards with fronts and chips.
  - L446-451, the neutrals.
  - L454 Order.
  - L457 No gradients.
- Rewrite:
  - L424: cut "Smoke, the eighth, is held; its card stays, marked."
  - L443: keep the first three sentences. Replace "Both follow the chips once they are measured. Renders can't show Acid's fluorescence, and the deep horns are unproven on real sheet; both wait for the chips." with "Acid is fluorescent: its edges glow brighter than a render can show." Colors F is the owner's pick (2026-11-01T22:55:41Z). Horns as deep as the cabinet are his direction (README:135, 142).
  - L444: "...Night is for the glow."
  - L455: "A printed or digital surface carries one tint, or all seven in order. Never two or three picked for a mood."
  - L456: "Where pieces in different tints share a room, they pair by the painter's wheel: one tint throughout, a tint with its complement, or a tint with its two neighbors; Fog, with no hue, goes with the cool tints." This is the owner's own pairing (README:132). It ends the clash between L455, L456 and L349's "one color or three".
- Cut:
  - L440-441, the Smoke card (values kept in archive §3a).
  - The CSS variable --smoke.

05 TYPE (#type)
Job: the two faces, the scale and the type rules.
- Keep L464-481 unchanged.

06 IMAGE DIRECTION (#images)
Job: the three kinds of picture and the rules every picture follows.
- Keep:
  - L491, the studio (AR:73).
  - L492, the Ice habitat (AR:88).
  - L493, the amp plate (AR:78).
  - L499-501: Always, Never, Crops (README:100; close-ups beside the whole speaker, 2026-11-01T12:11:46Z).
- Rewrite:
  - L489 lede: "Three kinds of picture, each with one job: the studio, in its element, and up close. Until the first pieces are built, every one is a render and says so; the same rules hold for the photographs."
  - At the end of L489, delete the orphan caption "Through the wall..." and its stray </figure></div>. The backs are not yet approved (AR:79).
  - L492: "In its element. Each tint in its own landscape: real places, real texture..."
  - L493: cut "; the small rating plate's wording here predates the proposal under Applications".

07 VOICE (#voice)
Job: how EARF speaks, with the lines in use, how the tagline is set, and the rules.
- Keep:
  - L509-520.
  - L517 "Drawn to be made. / Progress" (KEEP_FORWARD; RC:964-970).
  - L524-526, L529, L531, L533, L534 (RC:974).
- Rewrite: L530, the "Not this" line: "Seven horned speakers in colored acrylic."
- Cut:
  - L521, "The record" (§6a).
  - L532, the "Choose your weather" row, a retired site section (README:111, 114; §6a).

08 APPLICATIONS (#applications)
Job: how the name appears on paper, on screen and in the box.
- Keep:
  - L541, the head.
  - The house card text and the L545 specs.
  - L549-551, social posts with social.jpg.
  - L552-554, paper and the care card.
- Rewrite:
  - L542: "How the name appears on paper, on screen and in the box."
  - L544: "...is for the people who ask."
  - L553: "The letter says what the site says. The care card goes in every box, in the site's own words, because the wrong cleaner crazes acrylic for good."
  - The house card and paper blocks become text only (app nopic).
- Cut (archive §4a, §4d, §4f):
  - L543, card.jpg: not on the list, and its front carries a failed globe render (scenes/card.html:39).
  - L552, stationery.jpg: not on the list.
  - L546-548, the rating plate and plate.jpg ("Proposed", marks not yet earned).
  - The tote sentence and the L554 Tote row.
  - L555-557, Planet EARF's signs.
  - L558-560, EARFcoin.

CHAPTERS THAT LEAVE THE BOOK
- 09 Packaging (L564-594) goes to archive §4b. It is an unanswered proposal (WT 284), and its table is tagged "proposal" and "target" (L583-588). It returns on the owner's yes.
- 10 Big ideas (L596-624) goes to §4c. They are funding and sales tactics, none chosen (WT 280). The owner: "I want to nail the concept first and then execute" (2026-11-04T01:53:06Z).
- 12 The facts of record (L657-684) goes to §2. Its settled facts already sit in chapters 01-09.
- Parked (L686-692) goes to §5.

09 THE LINE (was 11 Press kit; id press becomes line)
Job: the four products' particulars and the boilerplate, word for word with the site preview.
- Keep:
  - L630, the boilerplate.
  - L632, the company sheet: fronts, Where, Site, Products, Status.
  - L633, the Tropos sheet, every row (RC:999).
  - L634, Hemisphere: Size, Shade, Fitting, Shades.
  - L635, Core: every row.
  - L636, Mantle: Plinth, Drive, Phono, Size, Weight.
- Rewrite:
  - Head: "09 · The line / The facts, and only the facts."
  - L629: "Taken from earf.world's particulars, with no invented figure, no quote and no price."
  - Write: "hello@earf.world" (RC:975). The mailbox bounces today (WT 240): confirm it receives mail, or drop the row.
  - Colors: "Seven, the same in every product".
  - Sells: "Made to order; price on request" (RC:974, 999).
  - Hemisphere Light: "2700 K, CRI 90; the dome glows in its own color, and the light straight down is the lamp's own warm white". The owner (2026-11-10T00:24:30Z): "it should work like core cut in half ... downward cast light will be the color of the bulb". The lumen figure goes (AR:25-27).
  - Hemisphere Mains: "120 V, dimmable" (RC:1081).
  - Core: "A tinted ball over a white opal inner ball, its color an even depth all round, sitting low in a black acrylic base, with no cord." The owner (00:24:30Z): "the outer core should be the same depth around the whole inner core".
  - Mantle:
    - Cut the "In development." tag.
    - Add "Posts: Four solid posts of polished stainless steel, 30 mm across" and "Base: Smoked cast acrylic, 12.7 mm" (RC:1081).
    - Arm · cartridge: "Rega RB330 · a moving-magnet cartridge".
  - L638: "Every release carries the standing lines: in development and not yet for sale; every picture a render until the first are built; design figures until measured; price on request."
- Cut: L641-642, the pitches and the local note (§7).

10 WHERE IT'S GOING (new; id going; placed before the footer)
Job: the path the owner set, in order, then the directions he set.
- Head: "10 · Where it's going / Drawn to be made."
- Lede: "Every part of Tropos has its own drawing. The horn's profile and the cabinet's bass were worked out by simulation before any acrylic was cut. What comes next:" (RC:965-967).
- Timeline (existing .timeline style):
  1. Next: "The first pair. Built to the drawings, the way every pair will be made."
     Sources: RC:968; the owner, "The whole point of a prototype is to test production" (README:133); the first pair is funded (2026-11-01T12:11:46Z, 22:55:41Z).
  2. Then: "Measured. In a room, by ear and by microphone. Until then, the figures in this book are design figures."
     Sources: RC:969, RC:954.
  3. Then: "Photographed. The first photographs take the place of the renders."
     Sources: v23 L499; RC:954.
  4. After: "The lamps and Mantle, the same way. Core keeps its color an even depth all round its opal inner ball. Hemisphere works like Core cut in half: the dome glows in its own tint, and the light straight down is the lamp's own warm white. Mantle's tinted plinth floats over its smoked base on four steel posts."
     Sources: RC:969; owner 00:24:30Z; "Mantle: A" (2026-11-01T12:11:46Z); AR:14.
- Directions (existing .cols style):
  - "Each tint in its element. Every one of the seven in a real landscape of its own, as Ice is in the snow." Sources: owner, "Go on all of the biome work" (03:09:52Z) and "Make it look amazing" (03:09:58Z), 2026-11-03; AR:88-93.
  - Only on a yes to question 2: "Smoke. A smoked gray, in development to join the seven." Source: owner 01:49:09Z.
  - Only on a yes to question 1: "Planet EARF. A listening bar that is also EARF's showroom: everything in the room is for sale, and every piece swaps tint. At its center, Mother EARF, the globe made in cast acrylic. EARFcoin, one a guest, is good for one song."
    - Sources: README:124, 126, 134-136; owner 2026-10-31T19:15:54Z, "same with the bar. Make it well architected, novel, lasting."
    - No size, cost, plan, place, date or picture: all are open or parked (WT 257-269, 343), and no bar picture is on the list.
- Left out, and why:
  - The debut: dates are parked (2026-10-31T19:15:54Z; FACTS:59).
  - The raise and prices: they belong in the deck, and are open again (WT 246, 324).
  - Special editions: one block to add on his word.
  - The six edition concepts and the seven new objects: proposals (WT 253, 279).
  - Mantle's light: open (AR:15-16).
  - The globe re-render: internal.

FOOTER
- L696: "EARF Brand Book · November 2026".
- L697: "Every picture is a render until the first pieces are built and photographed."

PAGE SOURCE (anyone can read it)
- Rewrite the L8-10 comment without "the bar".
- Remove --smoke, every process-named rule (.held .new .reserve .prop .tocome .inprog .parked), the dead packaging and big-ideas rules, and "<!-- the object -->".
- Rename the files:
  - honest-front-<tint>.jpg becomes tropos-front-<tint>.jpg.
  - honest-ice-habitat.jpg becomes tropos-ice-snow.jpg.
  - honest-amp-ember.jpg becomes tropos-amp-ember.jpg.
- Strip the blank leftover lines.

WATCH ITEMS (the Book stays as it is until the owner decides)
- Poison's name (00:17:21Z): L432-433, L472, L475, L516, L381, and the skull chip.
- The horn posts, "Black or brass?" (00:26:55Z; AR:20, 27): the words stay; the pictures would be re-rendered.
- Mantle's word, "turntable" as on the site (WT 225).
- Hemisphere's quarter turn and Core's inner size, after the lamps are redrawn (AR:23-27).
- FA122 or FA123 (coordinator, 2026-11-09T16:21:31Z).
- Acid's hue and the tint values, after the chips are measured (WT 349; "Not yet", 2026-11-04T01:55:41Z).
- The approved amp close-up shows the proposed "MODEL TR-1" in tiny type. Re-render it if TR-1 is dropped.

## ARCHIVE OUTLINE
THE BRAND ARCHIVE: a separate, private page for the team

The top of the page says, in plain words:
"Internal. For the EARF team only; not for investors, retailers, press, partners or customers. No stakeholder-facing page links here: not the Brand Book, the site, the press kit or the deck. Do not forward this link. The Brand Book is the current overview; this page is the record behind it."

Form
- Its own private artifact, at a new URL. It is not a file inside the Book's artifact.
- Title: "EARF Brand Archive".
- No embedded pictures, only paths and commits, so nothing unapproved is served from it.
- Every entry is dated in UTC, with its source. The owner's words are quoted verbatim, with send times.
- It is built from three sources:
  - plan/archive_manifest.json: 178 Book blocks, verbatim, each with its v23 anchor, the audit's reason and what the Book now says;
  - audit-surfaces/items.json: the 95 rows not marked KEEP;
  - the decision log below.
- It is republished whenever the Book changes. Nothing in it is ever deleted.

0. HOW TO READ IT
The sources, and the time convention (owner send times; delivery time in brackets where it differs).

1. DECISION LOG, by topic, oldest first. Each entry gives date, the owner's words and the source.

1.1 Name and line
- The names (22 Oct; README:133).
- "Get rid of south altogether and just call it hemisphere" (25 Oct; README:137).
- "Troposphere", then "Maybe just 'Tropos' because it's sexier and has Greek meaning" (29 Oct). Atmosphere was taken in audio (README:138).
- The tagline:
  - "Headline: keep 'Something in the air.'" (22 Oct; README:135).
  - "'Something in the air' is a lame tagline" (2026-10-31T19:40:04Z).
  - "Tagline: none: write a new set" (2026-11-01T12:11:46Z).
  - "I kind of like 'A world of sound'" (2026-11-01T22:55:41Z).
  - "Tagline: A world of sound, in color." (2026-11-02T15:48:15Z).
- "Color all the way through is dumb. Also it's color im not british" (2026-10-31T19:45:22Z).

1.2 Colors
- The eight, Ember to Smoke.
- "I like the darker colors" (2026-11-01T10:54:33Z).
- "Colors: F, light lining with Poison and Haze a step lighter" (2026-11-01T22:55:41Z).
- Smoke was held in the render pipeline (--hold smoke, 2026-11-03T15:17Z). That was a coordinator call, never put to the owner.
- "What happened to smoke?" (2026-11-10T01:45:42Z). The coordinator replied "holding it without asking you was my call" (01:47:37Z).
- "I still want smoke rendered as we ideally want it and we can work backwards from there, as long as it's semi-realistic." (01:49:09Z).
- "We should leave the option open for a chosen color" (2026-10-31T20:32:39Z).
- Complementary, analogous and monochromatic pairing (README:132).
- Poison: "maybe we should change it to something else that's green, unless we can really nail the biome" (00:17:21Z).
- Chips: "Not yet" (2026-11-04T01:55:41Z).
- Acid reads lemon, not golden (WT 349).

1.3 Tropos
- The stepped 22-layer horn: "happy to start with the stepped version" (2026-11-01T02:22:54Z); "Not sure if I like the stepping anymore" (2026-11-02T15:48:15Z).
- "Horn: A, smooth, satin outside" (2026-11-03T03:02:03Z); "If so just go polished." (15:13:04Z).
- "Flush horn: flush" (2026-11-01T12:11:46Z).
- The horn as deep as the cabinet (README:135, 142).
- The light under the speaker (2026-11-01T04:10:48Z, 2026-11-02T20:37:58Z, 2026-11-03T04:27:42Z), ending with "No light" (2026-11-03T15:11:16Z).
- Cover off (2026-10-31T20:32:59Z).
- The figures:
  - 1293 mm, 625 mm, 72 kg on the live site;
  - 1336 mm, 85 kg in the deck;
  - now 1295, 560 and 428 mm, about 73 kg (RC:999).
- The posts: "should the rods ... also be black. What made them brass?" (2026-11-10T00:26:55Z). Still open (AR:20, 27).

1.4 Mantle
- First Cumulus, then "the record player" (README:94, 133).
- "Not sure about mantle" (2026-11-01T10:54:33Z).
- "Mantle: A" (2026-11-01T12:11:46Z).
- "the underglow is projected down instead of casting through the acrylic" (2026-11-03T05:11:20Z).
- v4 and C3 were never signed (AR:14-16).
- The Book's "its light in the deck" was corrected at 01:05 (804cc8aa).
- "The mantle render looks kind of fucked up ... It looks cheap." (2026-11-10T00:41:49Z). The picture was pulled at 00:46 (AR:124, 143).
- The word and the cartridge are open (WT 225, 229).

1.5 Core
- Formerly the Orb (README:133).
- "30 mm, 5–6 hours" (README:139).
- "the orb definitely looked better without the cord" (2026-10-31T20:33:50Z).
- "Core battery: A, LiFePO4 · Core charging: sign the dock" (2026-11-01T12:11:46Z).
- "I kind of liked that dark border" (2026-11-09T21:03:06Z).
- "b for core, assuming we're still using the same materials" (21:11:07Z).
- Concentric layers (2026-11-10T00:24:30Z).
- The size is open (AR:23-24).

1.6 Hemisphere
- The Dome, then Hemisphere North and South (README:133).
- South was dropped (README:137).
- 575 lm (README:135).
- The low top (README:139).
- "Hemisphere: color outside" (2026-11-01T12:11:46Z).
- As drawn, it does not glow (AR:96-99).
- "it should work like core cut in half" (00:24:30Z).
- Option 3. The table light is open (AR:25-27).

1.7 Identity
- "Let's go with the acrylic globe" (README:6).
- "discs for monochrome and acrylic for multicolor" (README:474).
- The globe turning in the header (README:118).
- "I don't like changing the form at smaller sizes" (README:696).
- "Keep it as is" (README:935).
- The 17 Oct globe render.
- The globe_real renders fail (AR:133-138).
- "get rid of the coin and earth rise animations" (01:45:42Z).
- "I like the current globe rendered. The 'as an object' version looks too cheap" (01:54:53Z).
- The re-render is under way (824677cb, 134b0d6a).

1.8 Pictures
- "we need to sequence the work, so the marketing and brand assets use the right product renders" (2026-11-09T21:04:42Z). This started the approved list (AR:1-33).
- Dioramas and tilt-shift (README:100).
- "The speaker looks like it's floating above the ground. All bad." (2026-11-03T05:57:49Z).
- "Close-ups: a few, beside the whole speaker" (2026-11-01T12:11:46Z).
- The Pulled table (AR:140-161).

1.9 Site
- Live on 22 Oct (README:135).
- "Site: 1, launch film." (2026-11-03T04:27:42Z).
- "I want to see change. Website updates, brand updates, etc" (2026-11-09T16:18:01Z).
- The preview is 738691f0. Production is still 856f80d7. It goes live on his yes (WT 316).

1.10 Money and company
- "$50K: prototypes + debut", chosen over "$250K pre-seed" and "$1.5M with the bar" (README:140).
- The company waits for the first money (README:144-145).
- "Budget: keep $50,000, first pair in stocked gray · YC: skip" (2026-11-01T12:11:46Z).
- "Budget: raise to about $55,000" (22:55:41Z).
- The figure is open again (WT 246).

1.11 Debut
- 19 Jan 2027 moved to spring 2027 ("C"; README:148).
- "Let's not focus on picking dates and stuff yet." (2026-10-31T19:15:54Z).
- Parked (FACTS:59; WT 325).

1.12 Prices
- "remove pricing for now and make it a contact for details type of thing" (README:91).
- "Set at launch" became "Price on request" (RC:999).
- Parked (WT 324).

1.13 Claims
- "everything about the sustainability of the brand feels lame and cheap until we can deliver on it" (README:137; launch/held-back.md).

1.14 How he wants the work done
- "What's technically possible trumps what looks cool" (2026-11-03T05:11:20Z).
- "show me everything one at a time" (15:01:00Z).
- "C skip for now I want to nail the concept first and then execute" (2026-11-04T01:53:06Z, answering whether to visit Plastimagen and Plastiglas).
- The Book brief (2026-11-10T00:53:14Z).
- "Optimize what you can and sequence things in the most efficient way possible." (01:58:59Z).
- "anything I need to know about should go here" (02:03:57Z).

2. THE FACTS OF RECORD AS OF 9 NOVEMBER
- v23 L657-684, verbatim: Settled, Still open, Design figures, Pictures in progress.
- What changed after:
  - Mantle's light line was corrected (804cc8aa).
  - Reopened on 10 Nov: Smoke, Poison's name, Hemisphere's light, Core's concentric layers, the posts.

3. STILL OPEN
A live list, kept in step with the walkthrough: one line each, with its item number and the date it was raised.

Colors
- Smoke: seven colors or eight (WT 294; 01:49:09Z).
- Poison's name.
- Acid's name and hue (WT 224, 349).

Tropos
- Horn pours, and Haze's horn (WT 218-219, 320).
- The cover and the stepped ring (WT 215-216).
- The posts (AR:20, 27).
- FA122 or FA123.
- 19 mm or 20 mm sheet (WT 221).

Mantle
- Its light, deck pour, word and cartridge (WT 292, 293, 225, 229).

Lamps
- Hemisphere's table light, cord, and light color per tint (AR:25-27; WT 318, 300).
- Core's size and lit look (AR:23-24; WT 348).
- Matching the lamps' Haze (WT 276).

The bar and its objects
- Planet EARF: naming it in public, its plan and its road (WT 234, 257-260, 343).
- Mother EARF, and the Amsterdam Light Festival call, which closes 7 Dec 2026 (WT 265-269).
- EARFcoin's size and box (WT 262-263).
- The desk globe (WT 270).

Company, press and launch
- Naming the founder (WT 236).
- Releasing the press kit (WT 238).
- The mailbox (WT 240).
- "Designed in" or "made in" (WT 243).
- The raise (WT 246).
- The trademark search (WT 248).
- Design filings (WT 340).
- Company formation (WT 330).
- Prices (WT 324).
- The debut (WT 325).
- The first-run program (WT 286).
- Taking the site live (WT 316).

4. PROPOSALS AWAITING THE OWNER, verbatim from where they ran
4a. Planet EARF and its pieces
- v23 L374-375, L379, L398, L399, L402, L411-412, L416, L544, L553-554, L556-560, L609, L613, L676.
- press/planet-earf.md, and the deck's bar slide.
- README:124-126, 131, 134-136; WT 234, 257-269.

4b. Packaging
- v23 L564-594 entire: the steps, the decals, the table, and "Why this raises the odds".
- PACKAGING.md; WT 284.

4c. The seven big ideas
- v23 L596-624 entire, with costs, legal notes and mockup paths.
- IDEAS.md; WT 280, 256, 277, 286.

4d. The rating plate and model code
- v23 L382, L546-548, L674.

4e. Names in reserve
- v23 L376; WT 283.

4f. The application mockups
- card.jpg, plate.jpg, stationery.jpg, and three crate decals (scenes/*.html, rendered to out/*.png). None is on the list. card.html:39 carries a failed globe render.

4g. Special editions
- The owner's idea (2026-10-31T20:35:49Z: "special edition with things cast in the acrylic ... Could also be cool to have some with bubbles"). He asked after it again (2026-11-03T04:38:29Z).
- The six concepts (WT 253), Topo (WT 255), and the artist editions (v23 L618).

4h. Other objects
- The seven new objects (WT 279), the desk globe (WT 270), the Tint Library (WT 277).

5. PARKED PLANS
- v23 L686-692, verbatim, each with its folder:
  - photo/, launch/, money/, kickstarter/, sessions/, partners/, festival/amsterdam/;
  - launch/INVITE-LIST.md and MEDIA-PLAN.md;
  - press/releases/.
- Amsterdam is the only one with a live outside deadline: the call closes 7 Dec 2026, and WT 269 wants a go or no-go by mid-November.

6. RETIRED NAMES, LINES AND LOOKS, dated
6a. Words
- Product names: the Cloud, Bark and Crag lines; Atmosphere; Dome; Orb; Hemisphere North and South; Cumulus; Bell.
- Old lines:
  - "Something in the air.", "Eight things in the air", "Weather for the living room", "Pick your poison", "Choose your weather", "Choose your atmosphere", "Each colour, out in the world", "Cast in colour, all the way through".
  - "The oldest amplifier is a shape" ("silly", 2026-11-03T05:11:20Z).
  - "Put a light under it", "Lit from below", "A record player that floats on its own light", "The names are things the air holds", "Hung low over the bar".
- The old color keys, and the "honest-" picture names.

6b. Identity
- The rendered lockups and globe, "as an object", and the idents (the coin, Earthrise, the meteor).
- The rules as first written (v23 L396-416).

7. THE BOOK'S OWN HISTORY
- Versions:
  - v22: 1794270136-2332 (00:22, 38 files).
  - v23: 1794271571-295d.
  - v24: 1794272741-39e1 (804cc8aa).
  - v25: 1794275254-44ef (7d6b3d41).
  - v26: this rebuild.
- The second edition's change log, eyebrow, footer and head comment.
- The file renames, and the 14 published files removed.

8. MOVED OUT OF THE OTHER SURFACES
- The 95 non-KEEP rows of audit-surfaces/items.json, verbatim, grouped by surface: the site preview's copy and source, the live site, the press kit, launch, social, the deck. Each row keeps its location and the reason.

9. THE INVESTOR DECK'S HISTORY
Version 1793686214-3dc9, slide by slide. It is held for its rebuild (AR:43-44). It carries:
- eight colors and Smoke;
- lit plinths;
- the stepped and stacked horn;
- 660 × 670 × 1336 mm and about 85 kg;
- the satin horn;
- "record player" and "floats on its own light";
- glowing lamps;
- Planet EARF at about $2.0 M (the one-pager says $1.0–1.6 M), and its earlier picture scheme;
- the Smoke meteor close;
- "the names are things the air holds";
- the 3 Nov tip-test story;
- the orphan "first" slide.

10. PICTURES OUT OF THE BOOK, AND WHY
- lockup-paper.jpg, lockup-night.jpg, globe-paper.jpg, globe-real.jpg, globe-turn.mp4: the globe_real renders fail (AR:133-138).
- ident-coin.mp4, ident-rise.mp4: removed at the owner's word (01:45:42Z), and never mask-audited (AR:39-41).
- card.jpg, plate.jpg, stationery.jpg, decal-crate-front/inside/side.jpg, idea-founding.jpg, idea-hotel.jpg: not on the list.
- icon-smoke.png.
- Mantle by day (AR:143).
- See also AR:140-161.

11. NOTES KEPT INTERNAL
- The root README describes the earlier "earmilk" project.
- spinoffs/barkhorn/README.md opens "after Friendly Pressure", naming another maker's speakers as the design reference. The repository stays private.

## SURFACE FIXES
SITE PREVIEW (r49-site-rc 738691f0): THE COPY VISITORS SEE
Make each edit in the generator (web.py and site_v2.py), then rebuild. Check all 18 pages that share the body (index, tropos, lighting, mantle, contact, colors/*, tropos/*) and the 35 share cards.

1. Remove the Cover off / Cover on switch.
   - Where: RC:989-992; web.py about 2232-2235; CSS RC:214-216; and its JS. The cards stay cover off.
   - Why: no cover-on picture is on the list (AR:73), the cover is undecided (WT 215), and pressing "Cover on" blanks all seven cards.
2. Delete the speaker facts row "Cover: A cloth disc, optional (to follow)" (RC:1296).
3. Mantle cartridge: "A moving-magnet cartridge, to be chosen" → "A moving-magnet cartridge" (RC:1081; web.py:207).
4. Hemisphere Light: "2700 K, CRI 90, its source shielded inside the hub" → "2700 K, CRI 90; the dome glows in its own color, and the light straight down is the lamp's own warm white" (RC:1081; web.py:158; owner 00:24:30Z).
5. Hemisphere Mains: "120 V, dimmable; safety listing to follow" → "120 V, dimmable" (RC:1081).
6. Replace the globe_real render everywhere it appears, with the flat globe.
   - Where: the header globe (img/globe-spin-light.*; base64 still at RC:135-138 and 934), the opening films (globe-turn*.webm/.mp4 and globe-turn-night.*, RC:925-931), apple-touch-icon.png (RC:13), and 404.html:27, 30.
   - Use favicon.svg's drawing. Or use brand/mark/earf-globe-colour-spin.*, if the coordinator confirms it counts as a flat mark (AR:137).
   - Drop the opening film until an honest re-render in today's colors passes (owner 01:54:53Z; AR:133-138).
7. Color dots: replace the sprite img/coins-light.jpg (rendered EARFcoin blanks with a Smoke cell; CSS RC:156, "800% 100%") with flat dots in the Book's Mark hexes. The CSS goes to seven cells.
8. Watched, unchanged for now: "on four bronze posts" (RC:999, 1265) until "Black or brass?" is answered; Poison; "turntable" (WT 225).

Keep as is: the meta descriptions, share cards, og images, 404 copy, "Drawn to be made." (RC:964-970) and the Ice band.

SITE PREVIEW: PAGE SOURCE (anyone can read it)
Same generator, one pass.

1. RC:1437-1445 → "// the company a color keeps: its complement and its two neighbors; Fog, with no hue, sits with the cool tints". Drop the Smoke case in relations().
2. RC:1469-1483: delete PAIR and company(). They have no caller, and they carry the black|ice Smoke pair and "(the critics: ...)".
3. RC:1081 data:
   - drop "place", "cover", "view3d" and "campaign";
   - rename the keys: clouds → products; red…ice → ember…fog; dome/orb → hemisphere/core.
4. Rename img/rc/{red,orange,amber,green,blue,violet,ice}-* and og-<key>.jpg to the tint names. Today Fog's files are named ice-* and Ice's are named blue-*.
5. Legacy routes (RC:28, 38, 44, 1506-1510, 1515, 1532-1538): keep the redirects. Replace the narration ("Smoke: not a current color", "round 35's names", "the British addresses (before 2026-10-31)") with "// legacy addresses forward to their current pages".
6. Strip round, RC, branch, commit and coordinator notes from comments:
   - JS: 34, 1084, 1183, 1253, 1344, 1547, 1651, 1660.
   - CSS: 373-374, 550, 562, 624, 703, 728, 743, 755, 758, 812, 828, 833, 841, 849, 894, 920.
7. RC:1255: delete "// cover off before cover on (the owner, 2026-10-31: ...)".
8. Delete the dead code:
   - the uplit run (1091-1151; CSS 271-336, 1649);
   - the eight-picker closer (1152-1164, "% 8");
   - the habitats strip (1165-1174);
   - #horns (1192-1221);
   - press and waitlist (1235-1251);
   - the press, journal and privacy routes (1513, 1547-1554);
   - v3sync and v3close (1420-1421);
   - CAMPAIGN (1285-1290);
   - .sound-turn (1651-1657);
   - CSS .draft (127-130), .eight* (377-400, 786-787, 826) and .waitlist (678-684).
9. Delete the unused caption rows (1256-1284): cover on, at night, "Eight Hemispheres...", "Eight Core lamps...", the lit lamps, "${c.name} to follow", and the back view.
10. Delete the process notes at 1317, 1410, 1503 and 1555.
11. RC:1484: "neighbours" → "neighbors". Rename colourMain, .colour-head and .light-colour when convenient.
12. vercel.json: drop the journal-eight-colours redirect and the r31-*/r32-* deploy entries.
13. favicon.svg: change its title and aria-label to "EARF".

Check: grep the built site for "round [0-9]|RC[0-9]|Smoke|eight|colour|the owner|coordinator|critics". It must find nothing outside the redirect table.

LIVE SITE (origin/main 856f80d7)
No edits. It still says "Something in the air.", shows the eight with Smoke, uses British spelling, and carries the uplit band and the old figures. Promoting the fixed preview, on the owner's yes (WT 316), retires all of it.

PRESS KIT (r47-brand press/; the PDFs come from make_sheets.py)
The kit stays unreleased until the owner says so (press/README.md:3; WT 238).

1. Header, make_sheets.py:117: "Press · fact sheet · not for release" → "Press · fact sheet".
2. Founder: drop ('Founder','[FOUNDER]') (make_sheets.py:36) and company.md:18 until the owner decides (WT 236).
3. Colors:
   - make_sheets.py:31 → "01 Ember · 02 Dust · 03 Acid · 04 Poison · 05 Ice · 06 Haze · 07 Fog";
   - company.md:13: drop "(an eighth, Smoke, held for the owner)";
   - make_sheets.py:100 comment → "# the seven tints".
4. Mantle's word:
   - make_sheets.py:30: "Mantle, a record player" → "Mantle, a turntable";
   - make_sheets.py:63: 'Record player' → 'Turntable';
   - company.md:11-12 and 21: "record player" → "turntable";
   - README.md:15 → "Mantle, a turntable";
   - README.md:20-21 → "Mantle is a turntable whose tinted plinth floats 40 mm over a smoked base."
5. Tropos:
   - make_sheets.py:47 → ('Colors', 'All seven');
   - tropos.md:8: cut "A cloth cover goes on over the woofer.";
   - tropos.md:24 → "01 Ember, 02 Dust, 03 Acid, 04 Poison, 05 Ice, 06 Haze, 07 Fog".
6. make_sheets.py:115: remove the "PENDING / <name>: a new render / It goes here when it passes the critics." box. The lamp and Mantle sheets become text only.
7. Hemisphere:
   - make_sheets.py:50-51: "frosted within ... Hung low over the bar." → "with an opal diffuser inside its color, so the color glows and the source never shows. Hung low over a table.";
   - make_sheets.py:53, Light → "2700 K, CRI 90; the dome glows in its own color, and the light straight down is the lamp's own warm white";
   - make_sheets.py:55, Mains → "120 V, dimmable";
   - the same in hemisphere.md:3, 10 and 13.
8. Mantle:
   - make_sheets.py:69 and mantle.md:14, the cartridge → "A moving-magnet cartridge";
   - mantle.md:19: "The same eight" → "All seven";
   - mantle.md:17: drop "r48-mantle-design, mantle_strata_v3".
9. Price:
   - make_sheets.py:21 STANDING: "Prices are set at launch." → "Price on request.";
   - make_sheets.py:32, Sells → "Made to order; price on request";
   - README.md:30 → "Price on request; everything is made to order, so EARF quotes rather than lists.";
   - company.md:15 and the Price rows in tropos.md, hemisphere.md, core.md and mantle.md → "On request".
10. Rebuild every PDF. The current ones embed the superseded fronts from 9 Nov 16:35, not tallr6. After the Book's renames:
    - SEVEN → tropos-front-<t>.jpg;
    - the Tropos sheet picture → tropos-front-ember.jpg;
    - the src() test → f.startswith('tropos-').
11. images.md:
    - list only the seven fronts, tropos-ice-snow.jpg, tropos-amp-ember.jpg (to run beside a whole speaker), and the flat marks (earf-lockup-colour/-black/-white, earf-globe-colour, small/);
    - drop L7 and the backs, Dust habitat and render marks (L18-24, L26, L29-31);
    - tropos.md:31 → "Pictures: the seven fronts and Ice in the snow; all renders.";
    - hemisphere.md:21, core.md:21-23 and mantle.md:26-27 → "Pictures: none."
12. Move the working notes (README.md:3-5, 31-32; tropos.md:33; mantle.md:17) to press/NOTES.md.
13. planet-earf.md stays internal and never goes into out/.
14. releases/ is parked; do not circulate it. RELEASE-MARCH, PITCHES-PRINT and LOCAL-AND-FOG still carry eight and Smoke, "all the way through", 19 January, the stacked horn, the light under the cabinet, "record player ... floats on its own light", and "R5". Rewrite them from the Book when press is un-parked (WT 336).

LAUNCH (r47-brand brandbook/launch/; all held)
1. out/HELD.md: list every reason.
   - The one-pager: "tinted all the way through", eight colors, "A record player that floats on its own light", Planet EARF at $1.0–1.6 M, the "lit plinths" ask, prices, and five unapproved pictures.
   - The teaser: beats 1, 2, 4, 5 and 7 as well as 3 and 6.
   - The launch grid: every picture.
   - Replace L8-9 with "Mantle's light is not settled: no words or pictures about its light."
2. onepager.html, when it is rebuilt:
   - L46: "in eight colors" → "in seven colors";
   - L52 → "A turntable in cast acrylic.";
   - L67: drop the Planet EARF row (unless question 1 is yes, and then with no figure);
   - "Tropos prototype pair, on lit plinths" → "Tropos prototype pair";
   - prices only as the owner sets them (WT 324);
   - pictures: the seven tallr6 fronts only (L47-52 use hero-1200, red-studio-light, lamp-dome, lamp-orb and tt-violet-dusk, none of them on the list).
3. Teaser films and storyboard: re-cut from approved pictures only, with "A world of sound, in color." and no date. Bring STORYBOARD.md to the seven: no uplight, no date.
4. reserve.html (a proposal; WT 286): archive it. If it is ever revived: the seven, the tallr6 fronts, a 01-07 picker, and no Planet EARF register.
5. invite-card.html:42 and invite-email.html:23: "Mantle, the record player" → "Mantle, the turntable". Drop "At the door / One coin, one song" (card :43, email :24) unless question 1 is yes. The debut is parked.
6. policies-draft.md, before it goes to counsel: 73/64 kg, 1295 mm, Mantle 12.9 kg, "a moving-magnet cartridge", seven colors, no cover line, American spelling.

SOCIAL
1. social.jpg and scenes/social.html are current. Fix social.html:17: "/* 2: Dust where it began */" → "/* 2: Ice in its element */".
2. LAUNCH-GRID.md:
   - L3 → "Mantle's light is not settled";
   - L10-11: drop "Smoke is held for the owner";
   - post 4: "05 Ice, where it began." → "05 Ice, in its element.";
   - post 7 → "[no line]";
   - post 8 → "Mantle, when its picture is on the approved list" (Mantle was signed 1 Nov, AR:14);
   - update the picture names after the renames.
3. Rebuild out/launch-grid.png, grid.json and scenes/launch-grid.html from LAUNCH-GRID.md, using tropos-front-*.jpg and tropos-ice-snow.jpg only. Drop "One of eight colors", "Eight colors, Ember to Smoke.", "Mantle · record player / Floats on its own light.", "Tropos · the eight" and "in any of eight colors".
4. Nothing is posted before the owner's yes. The grid is parked (v23 L690; WT 282).

INVESTOR DECK AT ITS REBUILD (3sihYaT4ckNTF6WE7SWR7x, version 1793686214-3dc9; held, AR:43-44)
Pictures come from the approved list only.
- deck.json s1: "eight colors" → "seven colors".
- cover:
  - subtitle → "Hi-fi and light, cast in tinted acrylic. Seven colors, Ember to Fog. San Francisco.";
  - picture → brandbook/proposals/deck-cover.png (the seven tallr6 fronts);
  - notes: "eight" → "seven".
- line:
  - the room picture (stepped horns, lit plinths, glowing lamps, lit Mantle) → the seven fronts, or Tropos plus words for the lamps and Mantle;
  - the label → "Turntable · Mantle · A turntable in cast acrylic.";
  - notes: drop the stepped horn and the lit plinth.
- tropos:
  - "its horn stepped in 22 layers ... on a plinth lit from underneath" → "a smooth horn, one 10 mm sheet in the cabinet's color, polished, flush with the cabinet; it stands on its own feet";
  - "on a stepped acrylic horn" → "on the formed horn";
  - "660 × 670 × 1336 mm on its lit plinth; about 85 kg" → "1295 × 560 × 428 mm; about 73 kg (modeled)";
  - picture → the Ember tallr6 front;
  - notes: drop "A smooth formed horn stays an option" and "the two lit plinths".
- home:
  - picture → the Ice habitat, or none;
  - notes: "eight tints" → "seven"; drop "the debut in the spring".
- colours (rename the id to colors):
  - "Eight colors, Ember to Smoke." → "Seven colors, Ember to Fog.";
  - the list → the seven;
  - picture → the seven fronts;
  - notes: drop "The names are things the air holds" and "lit plinth".
- light:
  - no lamp picture (AR:96-99);
  - words: Core is cordless, its color an even depth all round; Hemisphere glows like Core cut in half;
  - notes: drop "first, low profiles".
- mantle:
  - kicker → "The turntable";
  - "A record player that floats on its own light." → "A turntable in cast acrylic.";
  - "over a smoked base lit from beneath" → "over a smoked base, on four polished steel posts";
  - no picture (AR:124).
- bar: remove it unless question 1 is yes. If yes, no $2.0 M figure (the one-pager says $1.0–1.6 M; WT 257, 260) and no picture.
- why: keep, but do not tie FOG week to a debut date.
- model: notes, drop "the two lit plinths".
- ask:
  - "Tropos prototype pair, on lit plinths: parts and shop work $20,700" → "Tropos prototype pair: parts and shop work", with the figure the owner confirms (WT 246 puts it at about $22,000);
  - notes: drop "lit plinths, the stepped rings and the bronze posts"; "Core's two-layer ball" → "Core's opal inner ball".
- made:
  - "The first horns are stacked from stock sheet and machined: no mold." → "Each horn is one 10 mm sheet formed over a plug and polished.";
  - drop "The latest changes, Tropos's plinth among them, are still to be added.";
  - notes: restate the cabinets for seven: five in stock colors, Poison and Haze in custom batches (Book L443).
- risks:
  - "seven of the eight horns are custom batches" → "the seven horns are custom batches, each a deep lot of its cabinet's hue" (WT 218);
  - notes: drop the stepped horn on file, "satin outside" and the tip-test story.
- plan and team:
  - drop the Planet EARF lines (about $2 M; a hospitality partner) unless question 1 is yes;
  - "eight colors" → "seven colors".
- close: the Smoke meteor picture → the Ice habitat; drop the stale note.
- first (an orphan slide): delete it.
- stands, market: keep; trim "now held at three points".

## OPEN QUESTIONS FOR THE OWNER
- Planet EARF: may the Brand Book show the bar, with Mother EARF and EARFcoin, as where EARF is going? It is internal today. Yes or no.
- Smoke: may the Brand Book say Smoke is in development as an eighth color? Today it shows seven. Yes or no.

## CHECKS (two verifiers)
[
 {
  "lens": "Stakeholder reader (an investor, a retailer's buyer or a design journalist) opening the planned Book cold. I read v23 in full with line numbers, the plan's test build plan/test/mock-book.html and mock-book-yes.html, and the pictures the Book serves (viewed). I checked them against the site preview (738691f0; its head is now 5b9b0586, with the visible copy unchanged), the live earf.world (origin/main 856f80d7), approved-renders.md at a171249f (02:44 UTC, newer than the plan's cd1b8ea0), the walkthrough, the README and the owner's chat through 02:48:58Z. That includes four owner decisions made after the plan was written: black rods (02:09:35Z), the logo in the speakers' colors (02:37:43Z), Smoke gray at 50% and Core 10 mm (02:42:19Z), and Mantle with a satin edge and black posts (02:48:58Z). The ten-chapter structure and the cuts hold. The plan as written does not. It would publish a Mantle spec the owner has reversed, pictures and marks he has superseded, and a pointer to a live site that contradicts the Book. Note: I ran git fetch for r47-brand and r49-site-rc. That fast-forwarded the local remote-tracking ref origin/r49-site-rc from 738691f0 to 5b9b0586; no working tree, commit or push was touched. My scratch files are in /tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/book-current/stakeholder-reader/.",
  "plan_holds": false,
  "problems": [
   {
    "where": "09 The line, Mantle sheet (mock L479; plan.md:284) and 10 Where it's going, timeline item 4 (mock L493; plan.md:305)",
    "problem": "The plan adds \u201cPosts: Four solid posts of polished stainless steel, 30 mm across\u201d and \u201con four steel posts\u201d. The owner reversed that after the plan was written. The coordinator asked \u201cMantle posts \u2026 Should they go black too? My pick: yes\u201d (chat 02:14:50Z, asked again 02:40:29Z), and the owner answered \u201cFor mantle, the stock with satin edge \u2026 Black for the posts.\u201d (2026-11-10T02:48:58Z). A reader of the chapter that promises \u201cThe facts, and only the facts\u201d would be handed a material the owner has already replaced. RC:1081, the source the plan copies word for word, carries the same superseded row.",
    "fix": "Drop the Posts row, and the 12.7 mm Base row the plan adds with it. Cut \u201con four steel posts\u201d from item 4. Add RC:1081 \u201cpolished stainless steel\u201d to the site fixes. Change plan.md:634-635 (\u201con four bronze posts \u2026 watched, unchanged\u201d) into an edit to black, since the rods are decided (AR:30-33). Restore a Posts row only from the revised parts list.",
    "severity": "blocker"
   },
   {
    "where": "Every Tropos picture (cover mock L254, color cards L348-361, studio L411, sheets L475-476, Ice habitat L286/L412, social.jpg L460) and every flat mark (header L243, plates L320-325, wordmark L337, tint chips, the Mark column); plan.md:846-847 \u201cNo new renders are needed\u201d and plan.md:860 \u201cBuild now\u201d",
    "problem": "Two owner decisions made after the plan leave its pictures and marks out of date on publication day. (1) \u201cBlack rods I think\u201d (sent 02:09:35Z): every studio front, the Ice habitat and social.jpg show brass rods. The speaker lane is re-rendering every Tropos studio picture (tallr7, about 5 h from 02:21; AR:30-33), and the outdoor scenes stay brass until habitat work restarts (coordinator 02:14:50Z). (2) \u201cI want not the same acrylic as the speakers but the same relative color as the speakers. The pale colors are not right.\u201d (02:37:43Z): the A2 globe (r47-brand ec58322b) uses Dust #F78B34, a lemon Acid #E4DE3C and Ice #3C91EB. The Book's flat globe, lockups, wordmark, chips and Mark hexes still carry the golden #E9B320 and the paler #4A90C8. The coordinator told the owner that golden yellow is going (\u201cthe yellow is the speakers' lemon, not the golden yellow of the old logo\u201d, 02:40:29Z). The coordinator has also promised the owner one Book rebuild after the globe pick (02:12:47Z, 02:23:38Z), and AR:38-39 now says \u201chabitats and the Book wait\u201d.",
    "fix": "Re-sequence the brief. Make the text edits now. Publish once the tallr7 fronts (and Smoke's, if question 2 is yes) are on the approved list and A2 is approved. Recolor the flat marks, chips and Mark column to the A2 palette; that is a script re-run, not a render. The exception is if the coordinator records that the flat marks keep the old palette. Re-make social.jpg from tallr7. Decide explicitly whether the brass-rod Ice habitat runs beside black-rod fronts or waits. Re-cite AR against a171249f; its line numbers have moved by about 10.",
    "severity": "blocker"
   },
   {
    "where": "09 lede (mock L472; plan.md:272), the earf.world pointers (mock L308, L473, L475) and publish step 9 (plan.md:1031+), which has no gate before stakeholders",
    "problem": "The Book says its facts are \u201cTaken from earf.world's particulars\u201d and sends readers to earf.world. The live site (origin/main 856f80d7) contradicts it. Its meta description reads \u201cHorn loudspeakers, lamps and a record player cast in tinted acrylic, in eight colours from Ember to Smoke.\u201d The page still carries \u201cSomething in the air.\u201d, 1293 mm and 72 kg, British spelling and \u201cSet at launch\u201d. An investor or editor who checks the Book against the site finds the history the owner wants out, plus figures that disagree. The plan leaves the live site as it is until the owner says yes to promotion (WT 316), but nothing stops the Book going out first.",
    "fix": "Add a written precondition: no one but the owner gets the Book until the preview is live on earf.world (and, for investors, until the deck is rebuilt). Say so in the coordinator's two-line note to the owner. Reword the lede so it doesn't rely on the live site: \u201cFrom the drawings, with no invented figure, no quotation and no price.\u201d",
    "severity": "blocker"
   },
   {
    "where": "Cover caption and the seven alt texts (mock L254), Image direction \u201cUp close\u201d (L413), the social.jpg alt (L460), the Tropos Weight row (L476)",
    "problem": "\u201ccover off\u201d appears 10 times and \u201con its own feet\u201d 10 times. Both only make sense against things a stakeholder never sees. The cloth cover is still open (WT 215: \u201cdrop the cover and the site's \u2018cover on\u2019 switch?\u201d). The plan's own site fixes delete the Cover off/on switch and the cover row, so the Book becomes the only place that mentions a cover. \u201cOn its own feet\u201d is set against the dropped lit plinth. The site's Weight row has no feet: \u201cAbout 73 kg; about 64 kg with the horn lifted off (modeled)\u201d (RC:999).",
    "fix": "Caption: \u201cTropos in the seven.\u201d Alt texts: \u201cTropos in Ember, whole, on a pale seamless.\u201d Up close: \u201cClose-ups only beside the whole speaker.\u201d Weight: RC:999's row as written. Add the pattern cover off|own feet to grep_baggage.sh.",
    "severity": "should"
   },
   {
    "where": "08 Applications, Social posts (mock L460, img/social.jpg); plan SURFACE_FIXES, Social item 1",
    "problem": "social.jpg's middle post prints \u201cTROPOS 05 \u00b7 WHERE IT BEGAN \u00b7 RENDER\u201d inside the picture (r47-brand scenes/social.html:38). The plan removes that phrase everywhere else (v23 L354 and L492, and the grep pattern \u2018where (its color|it) began\u2019), but the grep can't read pixels, so the check passes. The same block also breaks the Book's own rule, \u201cThe line is always the site's\u201d: the site now says \u201cOut in the snow at dusk.\u201d The plan fixes only the comment at social.html:17.",
    "fix": "Change social.html:38 to \u201cTropos 05 \u00b7 in its element \u00b7 Render\u201d. Re-make social.jpg, from tallr7 once it passes (see the rods blocker). Add a manual pre-publish step: read the text inside every composited picture.",
    "severity": "should"
   },
   {
    "where": "08 Applications, house card and paper blocks (mock L457-459, L463-465; plan.md:238-243)",
    "problem": "v23 L542 calls these \u201cDrawn mockups for review. Sizes and stocks are proposals\u201d. The plan deletes that line and keeps every spec as a standard: 89 \u00d7 51 mm, uncoated 600 gsm letterpress, the edge painted in seven bands, the 1 mm acrylic card, US Letter letterpress, the No. 10 envelope and the 4 \u00d7 5.5 in care card. No owner message or README note approves any of them. The plan rejected exactly this move for Packaging (call 1: it \u201cwould have shown an unanswered proposal as settled\u201d). With card.jpg and stationery.jpg cut, the chapter is two spec lists and one picture.",
    "fix": "Keep Social posts, and keep the care card, whose words are the site's care text (RC:999). Move the house card, letter and envelope specs to archive \u00a74f until the owner approves them, or add them to the questions he gets in chat. Lede: \u201cHow the name appears on screen and in the box.\u201d",
    "severity": "should"
   },
   {
    "where": "06 Image direction, \u201cUp close\u201d (mock L413, img/tropos-amp-ember.jpg)",
    "problem": "At full size (1000 \u00d7 1250), the approved amp close-up shows EARF's rating plate. It reads \u201cMODEL TR-1\u201d, a serial number \u201cS/N TR1-26-\u2026\u201d and power ratings. The Book cuts the model code as a proposal (v23 L382) and still says \u201cNo model numbers in speech\u201d (mock L309). An editor who opens the picture gets an unapproved product code and an invented serial number.",
    "fix": "Crop the approved frame to the FA122 panel so the EARF plate is out of frame; a crop is not a new render. Otherwise, run \u201cUp close\u201d as text until the plate's wording is decided. Turn the plan's watch item into a pre-publish step.",
    "severity": "should"
   },
   {
    "where": "04 Color, the Acrylic rows (mock L348-361) and the cabinet note (L363)",
    "problem": "The chapter carries production and sourcing detail that the public site leaves out (RC has 0 hits for TruCast): \u201cTruCast 2423\u201d, \u201ca custom batch in 2092's hue\u201d, \u201cfive in their stock TruCast colors\u201d and \u201clighter custom batches of their codes' hues (32.3% and 25.8% of light through 20 mm)\u201d. It reads as a parts list, tells a competitor which catalog sheets to order, and undercuts \u201cColor is a system, not a range\u201d. The two percentages are unmeasured targets, given to a tenth of a percent without \u201cabout\u201d, against the Book's own rules (mock L399, L439). The line about each horn being deep enough that its 10 mm wall reads like the 20 mm one is stated as fact. Yet the horn pours are open (WT 218-219; Haze's pour reads cobalt outdoors, WT 320), and the plan deletes v23's \u201cunproven on real sheet\u201d.",
    "fix": "Make the Acrylic rows plain descriptions: \u201cDeep red cast acrylic\u201d, \u201cBottle-green cast acrylic\u201d, and so on. Move the codes, batches and percentages to the archive and the parts lists. Note: \u201cEach cabinet is 20 mm cast acrylic over a white lining; each horn is formed in its cabinet's hue, specified to read as deep as the cabinet's wall.\u201d",
    "severity": "should"
   },
   {
    "where": "Cover strip slab 03 (mock L262), the Acid card chips (L352-353), and the In light and Mark columns (L348-361)",
    "problem": "The Acid speaker renders lemon-olive (WT 349, hue 57-60). The strip under the cover's Acid front and the card's chips are golden (#E2AA15 and #E9B320, hue 44). The Book defines \u201cIn light\u201d as \u201cthe color the acrylic renders as in light\u201d, and a journalist can see that it doesn't match. The plan also deletes \u201cBoth follow the chips once they are measured\u201d, so values that will change read as final. That happens just as the owner said \u201cYes samples\u201d (02:48:58Z) and accepted a lemon Acid for the logo (02:40:29Z).",
    "fix": "Sample the In-light swatches (strip and cards) from the approved renders so chip and picture agree, and take the Mark values from the A2 palette. If that can't be done before publishing, show the swatches without hex codes until the chips are measured. Close WT 349 with the coordinator's pick (\u201cmove the words and swatch to the dye\u201d), and change the site's \u201cTranslucent golden yellow\u201d to match.",
    "severity": "should"
   },
   {
    "where": "Poison across the Book: the card and skull chip (mock L354, icon-poison.png), the tint rule (L310), the type specimens (L392, L395), the voice line (L432)",
    "problem": "The owner is weighing the name: \u201cI like the poison name but maybe we should change it to something else that's green, unless we can really nail the biome\u201d (2026-11-10, about 00:17Z). The Poison biome has failed again (AR:102). Even so, the Book picks Poison as its example for the naming rule, the headline specimen, the label specimen and a voice line, and marks it with a green skull. A rename would touch five chapters. To a hotel or retail buyer, a skull beside \u201cKeep out of reach\u201d on a product for homes and restaurants reads as a hazard label.",
    "fix": "Use a settled tint for the examples: \u201cTropos 05,\u201d or \u201cTropos in Ice\u201d; the headline specimen \u201cGlacier blue, and in no hurry.\u201d; the label \u201cTropos 05 \u00b7 Ice \u00b7 1295 mm\u201d. Poison then appears only on its card, the strip and the tint list. Add the skull chip to the Poison watch item.",
    "severity": "should"
   },
   {
    "where": "03 Identity, the \u201cDrawn flat\u201d caption (mock L324; plan.md:155-156) and the Motion rule (mock L334; plan.md:164)",
    "problem": "The plan gives the stand-in a permanent role: \u201cDrawn flat \u2026 the mark on paper and on screen\u201d. In v23 the rendered globe was \u201cThe mark itself\u201d (L396), and the flat drawing was for \u201cprint where a render will not hold\u201d (L397). The owner likes the rendered globe (\u201cI like the current globe rendered\u201d, 01:54:53Z) and has just set its colors for the logo (02:37:43Z). The new Motion rule also drops v23's \u201cat rest\u201d (L410). As written, \u201cIt is the only motion the mark makes\u201d forbids the opening the owner asked for: the globe \u201cstarts larger and centered \u2026 moves and shrinks into its place \u2026 and the earth keeps spinning\u201d (README:118).",
    "fix": "Keep v23's roles: \u201cDrawn flat. For screen printing, embroidery and small sizes in color.\u201d The A2 globe takes the first plate once it is approved. Motion: \u201cThe globe turns on its axis. On the site it opens large and settles into the header, still turning. Nothing else moves.\u201d",
    "severity": "should"
   },
   {
    "where": "07 Voice, Not this / This / Because (mock L445-446; plan.md:226)",
    "problem": "Two of the three \u201cNot this\u201d lines are EARF's own old site copy, which the owner rejected: \u201cdumb things like \u2018watch the horns turn\u2019 and stating the obvious like \u2018eight horned speakers in colored acrylic.\u2019\u201d (owner notes of 2026-10-18, README:91). The plan changes \u201cEight\u201d to \u201cSeven\u201d, so a retired line is updated to look current. A stakeholder reads them as generic examples. The owner will recognize the earlier ideas his brief asks to drop.",
    "fix": "Replace both rows with examples that aren't EARF's history. Row 1: Not this \u201cSound like never before.\u201d / This \u201cTo about 51 Hz at \u22123 dB, before the room.\u201d / Because \u201cA figure says more than a superlative.\u201d Row 2: Not this \u201cA revolutionary design.\u201d / This \u201cEvery part of Tropos has its own drawing.\u201d / Because \u201cSay what was done.\u201d",
    "severity": "should"
   },
   {
    "where": "10 Where it's going, timeline item 4 (mock L493; plan.md:303-306)",
    "problem": "Item 4 reads as a designer's to-do list, not a direction. In \u201cCore keeps its color an even depth all round its opal inner ball\u201d, \u201ckeeps\u201d implies the reader knows an uneven version, and \u201call round\u201d is British (also at mock L478). \u201cHemisphere works like Core cut in half\u201d is the owner's shorthand for a redesign (00:28:39Z). The Mantle sentence is now wrong (see the first blocker). The item repeats the Hemisphere and Core sheets almost word for word, and it fixes details of two lamps that are still being redrawn (Core's \u00d8140 core, AR:34-35; Hemisphere option 3, AR:25-27). The site says it in one line: \u201cThe lamps and Mantle come next, the same way.\u201d (RC:969).",
    "fix": "Item 4: \u201cThe lamps and Mantle, the same way: built to their drawings, measured, then photographed.\u201d Leave the design particulars to chapter 09, and write \u201call around\u201d there.",
    "severity": "should"
   },
   {
    "where": "10 Where it's going, timeline items 1-3 (mock L490-492); question 2 (plan.md:310-311, 1050+); plan.md:298 (\u201cthe first pair is funded\u201d)",
    "problem": "The first pair is planned in stocked gray. The evidence: the owner's \u201cfirst pair in stocked gray\u201d (2026-11-01T12:11:46Z); README:166, \u201cthe first pair stays in the stocked gray\u201d; WT 296; and WT 328, \u201cThe Smoke answer may change which grey\u201d. The owner has since chosen Smoke's look (\u201cFor smoke gray 50% I think\u201d, 02:42:19Z), and Smoke joins the black-rods render batch (AR:33-34). If question 2 is no, steps 1-3 lead to photographs of a gray Tropos in a color the Book says EARF doesn't make. Step 3, \u201cThe first photographs take the place of the renders\u201d, can't then hold for the seven tints. Question 2 also decides the count \u201cseven\u201d that the Book states throughout (the Color headline, the tint rule, the boilerplate, the company sheet, Position), not just one block in chapter 10. That count was a coordinator's hold, never the owner's choice (01:47:37Z). Separately, the plan's note \u201cthe first pair is funded\u201d misreads the budget ask. The $55,000 is still open (WT 246), and \u201cThe company waits for the first money\u201d (README:145).",
    "fix": "Put question 2 to the owner before the build, with the fact attached: \u201cThe first pair is gray. May the Book name Smoke as the eighth color, in development?\u201d If yes, step 1 names the first pair's color once the coordinator confirms it is the Smoke sheet. If no, step 3 becomes \u201cPhotographed: the first pair, then each tint as it is made.\u201d Correct the plan's source note to \u201cthe next step, which the raise pays for\u201d.",
    "severity": "should"
   },
   {
    "where": "10 Where it's going, the Directions block (mock L495-497)",
    "problem": "With both answers no, Directions is one item in a three-column grid. At desktop width that leaves two empty columns, which looks unfinished and goes against the spirit of check d. That one item is a picture program now on hold (\u201chabitats and the Book wait\u201d, AR:38-39), with one finished example. To an investor or editor, the chapter mostly says \u201cnot built yet\u201d. Since the plan was written, the owner has set two brand-level directions, both decided and concrete. First, one hardware color across the line: \u201cFor consistency, should the rods \u2026 also be black\u201d (00:28:39Z), \u201cBlack rods I think\u201d (02:09:35Z), and Mantle's \u201cBlack for the posts\u201d (02:48:58Z). Second, a mark in the products' own colors (02:37:43Z).",
    "fix": "Once the black-rod pictures are on the list, add: \u201cColor only in the acrylic. The hardware is black across the line: the horn's rods, Mantle's posts, the lamps' fittings.\u201d Once A2 is approved, add: \u201cThe mark in the products' own colors.\u201d Lay the directions out as a list, or as a .two grid sized to the number of items.",
    "severity": "should"
   },
   {
    "where": "Question 1 and the yes build (plan/test/mock-book-yes.html L497-499; plan.md:312-319)",
    "problem": "The yes test build adds a \u201cSpecial editions\u201d block that no question covers; call 4 says they stay out. Question 1 bundles three separate open proposals into one yes or no. They are the bar, whose scale was never asked (WT 260); Mother EARF, placed \u201cAt its center\u201d, though the walkthrough says she \u201ccan't be built as drawn\u201d (WT 265); and EARFcoin, whose size is unsigned (WT 262). In a book that investors read, \u201cEARFcoin\u201d with no description reads as a crypto token.",
    "fix": "Take Special editions out of the yes template, or make them question 3. Ask question 1 about the bar alone. On a yes, write: \u201cA listening bar that is also EARF's showroom: everything in the room is for sale.\u201d Keep Mother EARF and EARFcoin in the archive until they are buildable or signed. If the coin ever appears, call it \u201can acrylic token, one a guest, good for one song\u201d.",
    "severity": "should"
   },
   {
    "where": "09 Write row (mock L475); Identity \u201cFiles on request\u201d (L333); Sells \u201cprice on request\u201d (L475); the house card's \u201cfor the people who ask\u201d (L458)",
    "problem": "The Book tells stakeholders three times to ask, and its only address bounces today (WT 240: \u201cMail to hello@earf.world bounces, and the live site shows the address\u201d). The plan's fallback is to drop the Write row. That leaves every \u201con request\u201d with no channel, a dead end for a buyer or an editor.",
    "fix": "Make a working mailbox a precondition for the stakeholder send (the coordinator's own pick on WT 240), not an optional row. Until the mailbox works, the Book stays with the owner.",
    "severity": "should"
   },
   {
    "where": "The Book as a whole: what is pictured (cover, 04, 06, 08, 09)",
    "problem": "The Book opens with \u201cHi-fi and light\u201d and \u201cEvery piece comes in the same seven tints\u201d, yet no lamp, no lit piece and no Mantle appears anywhere. With card.jpg and stationery.jpg cut, the pictures are the seven Tropos fronts (shown three times), one snow scene, one amp plate and a social mock-up built from those. A buyer or editor sees one product. The cause is legitimate (the approved list), but the plan has no step to fix it.",
    "fix": "Ask the coordinator to add flat line elevations of Hemisphere, Core and Mantle to the approved list once their redraws settle. They are drawings, not renders, so they fit \u201cDrawn to be made\u201d and avoid the honesty problems that got the lamp and Mantle renders pulled. Track this as a known gap rather than leave it unsaid.",
    "severity": "should"
   },
   {
    "where": "09 chapter name, lede and closing note (mock L471-472, L481; plan.md:261-288)",
    "problem": "\u201cThe line\u201d collides with the Book's other meaning of \u201cline\u201d: a tagline or a tint's line (\u201cOne line per surface\u201d, \u201cthe tints' lines\u201d, \u201cLine: Instrument Sans 600\u201d). A cold reader expects copy, not specifications. \u201cNo quote\u201d here means a quotation, while chapter 07's \u201cwe quote\u201d means a price. \u201cEvery release carries the standing lines\u201d is press-team process (\u201crelease\u201d, \u201cstanding lines\u201d) left over from the press-kit chapter.",
    "fix": "Rename the chapter \u201c09 \u00b7 Particulars\u201d (id particulars), the Book's own word (mock L292, L388). Lede: \u201cFrom the drawings, with no invented figure, no quotation and no price.\u201d Closing note: \u201cUntil the first pieces are built, everything EARF publishes says so: in development and not yet for sale; every picture a render; design figures until measured; price on request.\u201d",
    "severity": "should"
   },
   {
    "where": "02 Naming, 03 Identity and the 09 boilerplate (mock L300, L309, L324, L473)",
    "problem": "\u201cNo model numbers in speech\u201d points at the model code the Book cut. The naming lede and the boilerplate say every product is named for a \u201clayer\u201d, but Hemisphere is a half, not a layer; the rule itself says \u201ca layer or a region\u201d. The \u201cDrawn flat\u201d caption promises \u201csmall sizes in color\u201d, but brand/mark/small/ holds only black and white cuts.",
    "fix": "Cut \u201cNo model numbers in speech.\u201d Write \u201cone of its layers or regions\u201d in the lede and \u201cnamed for the Earth's layers and regions\u201d in the boilerplate. Change the caption to \u201csmall sizes in one color\u201d, or draw the color cuts.",
    "severity": "nit"
   },
   {
    "where": "01 Position and 04 Color (mock L281, L291, L348-361, L364, L375-376)",
    "problem": "\u201cNight is for the glow\u201d doesn't say what glows, and no glowing piece is shown. The Pairs rule (\u201cWhere pieces in different tints share a room \u2026 one tint throughout\u201d) contradicts itself. \u201cA room can be one color or three\u201d leaves out the complementary pair (two colors) that Pairs allows. \u201cThe seven tints are the same seven in every product \u2026 the whole catalog follows\u201d oversells: the lamps' Haze can't match in stock sheet (WT 276), and Mantle in stock Ember reads almost black (coordinator 02:12:47Z). Each card's \u201cRender\u201d badge sits on the tint's line rather than on the picture.",
    "fix": "\u201cNight is for the lamps, lit.\u201d Pairs: \u201cA room takes one tint throughout, a tint with its complement, or a tint with its two neighbors.\u201d Position: \u201cone color, two or three\u201d. What the brand holds to: \u201cthe same seven dyes in every product\u201d. Move the badge onto the picture's corner.",
    "severity": "nit"
   },
   {
    "where": "07 Voice and 01 Position (mock L283, L292, L429, L433, L447, L488)",
    "problem": "The label \u201cProgress\u201d is an internal section id; the site's own nav says \u201cDrawn to be made\u201d. Hemisphere is the only product with no line, though the site has \u201cOne hangs. One wanders.\u201d (RC:958). The sustainability row (\u201cA claim we can't yet deliver reads cheap\u201d) points a stakeholder at a gap. \u201cEngineering first, then the joke\u201d undercuts seriousness for investors. \u201cMost large cities\u201d is unsourced. The simulation sentence appears twice (L292 and L488).",
    "fix": "Label the line \u201cThe making\u201d. Add \u201cOne hangs. One wanders.\u201d labeled \u201cHemisphere and Core\u201d. Make the rule \u201cNo claim the product can't show yet.\u201d Write \u201cthen the wit\u201d and \u201cmany large cities\u201d. Open chapter 10 with a new sentence instead of repeating chapter 01.",
    "severity": "nit"
   },
   {
    "where": "09 product sheets (mock L476-479)",
    "problem": "\u201cThe driver and posts show through it\u201d doesn't say which posts, and their finish has just changed. \u201cFormed over a plug\u201d is shop jargon. \u201c12.7 mm\u201d is half an inch, out of place in a metric book. The Hemisphere sheet fixes a quarter-turn shade and a three-layer build for a lamp being redrawn as option 3 (AR:25-27). The lamps' 2700 K is still open per tint (WT 300).",
    "fix": "\u201cThe driver and the horn's posts show through it\u201d, \u201cformed and polished\u201d, \u201c13 mm\u201d. Limit the Hemisphere sheet to Size, Light and Shades until option 3 is drawn.",
    "severity": "nit"
   },
   {
    "where": "Publish step 9 (plan.md:1031-1049), same artifact WGpswpvvETozjgRAxBuUK3",
    "problem": "The clean Book is republished over v22-v25. Those versions hold everything the archive holds (the big ideas, Planet EARF, the idents), and anyone given edit access can open them.",
    "fix": "Share the Book view-only, or publish the clean Book at a new URL and send that one.",
    "severity": "nit"
   },
   {
    "where": "Page source (mock L99, L117, L139-140, L239, L320-325)",
    "problem": "Dead CSS rules (.four, .big-quote, .sizes) and the video script remain, though the page has no videos. The four new mark images have no width or height, so the plates jump as they load.",
    "fix": "Remove the dead rules and the script, and set width and height on the four mark images.",
    "severity": "nit"
   }
  ]
 },
 {
  "lens": "I checked completeness and truth against these sources: the 700-line v23 page; the plan's test build (plan/test/mock-book.html and mock-book-yes.html); the 178-block manifest; the owner's messages through 2026-11-10T02:48:59Z; approved-renders.md at 6e4a3553 (02:50 UTC); the 36 files of published version 25; the RC and live site sources; and the deck (v1793686214-3dc9). The plan's structure works: ten chapters, a private archive and a picture allowlist. But four of the owner's decisions came after the plan, between 02:13 and 02:48. One of them contradicts a row the plan adds. The coordinator has also promised him the Book will be rebuilt only once, after he approves the new globe.",
  "problems": [
   {
    "where": "BRAND_LANE_BRIEF step 0 ('Build now') and step 5 ('No new renders are needed'); WATCH ITEMS ('Black or brass?')",
    "problem": "The plan predates the owner's later decisions and the coordinator's promise of a single rebuild. The owner wrote 'Black rods I think.' at 2026-11-10T02:13:02Z. AR 6e4a3553 L30-33 records that every Tropos studio picture is being re-rendered with black rods (fronts tallr7, horn-backs and turns), a batch of about 5 hours from 02:21. The tallr6 fronts, the Ice habitat 0f619953, the amp plate and social.jpg all show the brass rods he has now rejected, so building now would put a superseded design in every Tropos picture. The coordinator told him at 02:23:38Z and 02:53:48Z that the Book is rebuilt once, after he approves the A2 globe (r47-brand ec58322b). AR L39 says 'habitats and the Book wait'. AR L46 says to rebuild the assets only after the studio pictures are locked. The owner asked at 02:07:55Z to 'sequence things in the most efficient way possible.'",
    "fix": "Rebase the plan on AR 6e4a3553 and the chat through 02:53Z. Hold the Book, the press PDFs, the deck cover and social.jpg until the tallr7 fronts pass and join the list and the owner approves A2. Then build once: swap in tallr7, and use the rendered lockups once A2 is on the list. Close the 'Black or brass?' watch item. In the same batch, change the site's 'on four bronze posts' (RC:999, RC:1265).",
    "severity": "blocker"
   },
   {
    "where": "NEW_BOOK_OUTLINE 09 The line, Mantle 'Posts' row (apply_plan.py:164; mock-book.html:479); 10 Where it's going, 'After' step (mock-book.html:493); SURFACE_FIXES deck 'mantle'",
    "problem": "The plan adds 'Posts: Four solid posts of polished stainless steel, 30 mm across' and 'Mantle's tinted plinth floats over its smoked base on four steel posts', and rewrites the deck to 'on four polished steel posts'. The owner reversed this at 2026-11-10T02:48:59Z: 'For mantle, the stock with satin edge... Black for the posts.' AR 6e4a3553 L40-43 records 'posts BLACK'. The site preview still says 'four polished steel posts' (RC:1017) and 'polished stainless steel' (RC:1081), and SURFACE_FIXES does not change either.",
    "fix": "Drop the Posts row, or write 'Four black posts' once the parts list names their material. In chapter 10, write '...over its smoked base on four black posts'. In the deck, write '...over a smoked base, on four black posts'. Add RC:1017 and RC:1081 to SURFACE_FIXES.",
    "severity": "blocker"
   },
   {
    "where": "NEW_BOOK_OUTLINE 03 Identity (the L397 caption 'the mark on paper and on screen', the L392 color plate, L415); 04 Color 'Mark' values",
    "problem": "The flat marks use the old logo palette. In plan/look, the flat globe's sphere samples as leaf green #376621 and the color wordmark's yellow as golden #E9B320 (Acid's 'Mark' value). brand/mark/earf-lockup-colour.png shows the same globe. The owner wrote at 02:37:43Z: 'for the sake of the logo, I want not the same acrylic as the speakers but the same relative color as the speakers. The pale colors are not right.' A2 uses Dust #F78B34, lemon Acid #E4DE3C and Ice #3C91EB (AR 6e4a3553 L35-37). At 02:40:29Z the coordinator asked whether the logo's yellow should stay golden; he has not answered. The plan's new caption still promotes this old-palette flat globe to 'the mark on paper and on screen', although at 01:54:53Z he said 'I like the current globe rendered'.",
    "fix": "Keep v23's caption ('For print where a render will not hold...') until A2 is approved and on the list. Then ask him once whether the flat marks, the icons and the Mark values for Dust, Acid and Ice follow A2's colors. Redraw them in the same batch so the Book never shows two logo palettes.",
    "severity": "should"
   },
   {
    "where": "NEW_BOOK_OUTLINE Rules > Pictures and 04 Color (the seven icon chips); tools/check_book.py ALLOWED; lockup-white.png (new to the Book)",
    "problem": "The seven icon-<tint>.png chips are drawn pictograms: Poison's chip is a skull (plan/look/book-icon-poison.png) and Ember's is flames (icon-ember.svg). They are not on approved-renders.md. The list's only flat entry is 'the flat marks stand in', which covers the failed globe renders (AR 6e4a3553 L151). AR L6 says the Book uses ONLY pictures on the list, which is the owner's standing rule. lockup-white.png and the other flat marks are covered only by that general phrase.",
    "fix": "Before publishing, have the coordinator add these to approved-renders.md by file name: the flat marks (globe-flat, lockup-color, lockup-white, lockup-black, wordmark-color) and the seven tint icons. Otherwise, drop the chips. Keep the Poison chip under the Poison watch item.",
    "severity": "should"
   },
   {
    "where": "OPEN_QUESTIONS_FOR_OWNER #2; NEW_BOOK_OUTLINE 10 (the Smoke block; 'Next: The first pair'); ARCHIVE_OUTLINE \u00a71.2 and \u00a73 Colors",
    "problem": "The owner has moved Smoke forward. At 02:42:19Z he wrote 'For smoke gray 50% I think.' AR 6e4a3553 L33-34 records 'neutral gray, 50 % through 20 mm, black lining... Smoke joins the same batch'. At 02:48:59Z he wrote 'Yes samples'. The sample order includes the 2064 Light Smoke square, which the coordinator is testing as Smoke's sheet (02:51:49Z). The first pair itself is 'in stocked gray' (owner 2026-11-01T12:11:46Z; the deck's ask notes say 'stocked gray (2064)'). With the default answer 'no', the Book says the first pair comes next but never says it is gray. Question 2's yes text, 'to join the seven', assumes Smoke becomes the eighth color. The coordinator's own pick was 'Smoke later as an edition' (01:47:37Z), and the owner has not ruled on it. The archive also keeps the TruCast 2074 values (#34323A, #3A3741) as Smoke's values.",
    "fix": "Reword question 2: 'Smoke is being rendered at gray 50% on a black lining, and the first pair is planned in stocked gray. May the Book name Smoke as in development, without a color count?' On a yes, add: 'Smoke. A gray, about half the light through 20 mm, in development.' In the archive, record the 02:42 and 02:48 decisions and mark the 2074 card values as superseded.",
    "severity": "should"
   },
   {
    "where": "NEW_BOOK_OUTLINE 09 The line, company sheet 'Write' row (mock-book.html:475); BRAND_LANE_BRIEF step 8e",
    "problem": "No mailbox exists for this address. WT 240 says 'it bounces today'. The coordinator wrote at 2026-11-10T02:44:53Z: 'hello@earf.world: it has no mailbox yet... It needs setting up before the site goes live'; the item is parked. The default build still prints the address. Check 8e asks the brand lane to confirm the mailbox receives mail, which it has no way to do.",
    "fix": "Build with the Write row left out. Add it back only after the coordinator confirms a working mailbox.",
    "severity": "should"
   },
   {
    "where": "NEW_BOOK_OUTLINE Rules ('what the site preview says publicly'); 09 The line lede (the L629 rewrite; mock-book.html:472)",
    "problem": "The site preview is not public. Production is untouched (AR 6e4a3553 L51), and going live waits on the owner's yes (WT 316). The live earf.world (origin/main 856f80d7) still says 'Something in the air.' (L584), 'Set at launch' (L694) and '72 kg' (L952). So the line 'Taken from earf.world's particulars' is false today. The preview's copy was written by the site lane; the owner has not approved it, so it is not a decision.",
    "fix": "Write 'Taken from EARF's particulars' or 'from the drawings'. Treat the RC copy as current team wording that awaits the owner's yes, not as decided.",
    "severity": "should"
   },
   {
    "where": "NEW_BOOK_OUTLINE 10 timeline, steps 1 and 3 (plan.md:297-302; mock-book.html:490-492)",
    "problem": "The step 'Photographed. The first photographs take the place of the renders.' is not a direction the owner set. The photo shoot is a parked plan (v23 L690). The first pair is to be built in stocked gray (owner 2026-11-01T12:11:46Z), so photographs of it cannot replace the renders of the seven tints. The plan's source note, 'the first pair is funded (2026-11-01T12:11:46Z, 22:55:41Z)', misreads those messages. They set a budget ('keep $50,000, first pair in stocked gray'; 'raise to about $55,000'). That figure is open again (WT 246), and the company waits for its first money (README:145).",
    "fix": "Drop step 3, or write 'Photographed. As each piece is built, photographs replace its renders.' Correct the source note to say 'budgeted' and cite WT 246.",
    "severity": "should"
   },
   {
    "where": "SURFACE_FIXES press #4, launch #2 and #5, deck 'line' and 'mantle'; plan.md:1058-1059",
    "problem": "The plan replaces 'record player' with 'turntable' in the press kit, the one-pager, the invitation card and email, and the deck. Yet plan.md:1058-1059 lists Mantle's word (WT 225, open) as a question it is not asking now. The owner's own word is 'record player' (README:94). The plan would settle an open question without him.",
    "fix": "Ask WT 225 in one line before changing the other surfaces. Until he answers, leave their wording as is, and keep 'turntable' in the Book and on the site as a watch item.",
    "severity": "should"
   },
   {
    "where": "NEW_BOOK_OUTLINE 08 Applications (the L542 rewrite; the L544-545 and L553-554 specs; mock-book.html:456-465)",
    "problem": "v23 calls these 'Drawn mockups for review. Sizes and stocks are proposals' (L542; also footer L697). The plan removes that label and presents the specs as the standard: the house card (89 x 51 mm, 600 gsm letterpress, painted edge, a 1 mm acrylic card), the letter, the envelope and the care card's size. The owner never chose them, and the second edition's wording is still unreviewed (WT 278). The task's definitions keep proposals out of the Book.",
    "fix": "Move the card and paper specs to archive \u00a74f with their mockups. Keep the social-post rule and the care-card text, which uses the site's own words. Alternatively, the coordinator can adopt the specs under the owner's 25 Oct 'make your call' (README:137), provided the adoption is recorded.",
    "severity": "should"
   },
   {
    "where": "NEW_BOOK_OUTLINE 07 Voice, the cut of L532",
    "problem": "Cutting the 'Choose your weather' row also removes a current rule: 'Don't force a metaphor past where it fits.' It comes from the owner's 'not sure if weather is right because some of them aren't weather' (README:114). The FACTS audit lists 'no forced weather metaphor' among the current voice rules. No other row in the new Voice chapter states it.",
    "fix": "Keep one Not this / This / Because row with a current example, ending 'Because: Don't force a metaphor past where it fits.'",
    "severity": "should"
   },
   {
    "where": "ARCHIVE_OUTLINE section numbers vs plan/archive_manifest.json topics; tools/archive_manifest.py and tools/check_book.py (the 12-character skip); plan/test/mock-archive.html",
    "problem": "The archive outline and the manifest do not line up, and the archive test cannot catch the gap. (i) The Smoke card is sent to 'archive \u00a73a', but the outline has no \u00a73a; its \u00a73 is STILL OPEN. (ii) L641-642 are sent to '\u00a77', which in the outline is the Book's own history. (iii) The manifest's topics ('3a Smoke', '3b Colors as first written', '7 Press', '8 The Book itself') do not match the outline's \u00a73, \u00a77 and \u00a78. (iv) The scripts skip any segment shorter than 12 characters, so the manifest leaves out five v23 blocks: 'Mantle.', 'The signs.' and 'The jacket.' (L682), 'Settled' (L662) and 'Still open' (L671). (v) The archive check passes only because plan/test/mock-archive.html is v23 L300-701 with one 'Internal' line on top, still carrying 35 img and video tags. So '0 audited blocks lost' proves nothing, and no check enforces 'No embedded pictures'.",
    "fix": "Add outline sections for Smoke and the color notes as first written, and for Press, or renumber the manifest's topics. Match list items whole instead of skipping short ones. Run the test against an archive generated from the manifest. Add checks that the archive has no img, video or source tags and that no stakeholder page carries its URL.",
    "severity": "should"
   },
   {
    "where": "ARCHIVE_OUTLINE \u00a71.2-1.7 and \u00a73 STILL OPEN; NEW_BOOK_OUTLINE WATCH ITEMS",
    "problem": "The archive outline leaves out the owner's decisions after 02:07:\n- 02:13:02Z: black rods.\n- 02:37:43Z: the logo in the speakers' colors.\n- 02:42:19Z: Smoke gray 50%; Core's 10 mm band (a 140 mm inner ball).\n- 02:48:59Z: Hemisphere left to the coordinator's pick, the bigger ring (about 1,000 lm, about 200 lux); Mantle in stock Ember with a satin edge and black posts, the custom pour dropped; 'Yes samples', replacing his earlier 'Not yet' on chips.\n\u00a73 still lists the posts, Core's size, Hemisphere's table light and Mantle's deck pour as open. The watch items still carry 'Black or brass?' and Core's inner size.",
    "fix": "Add each decision with its time, citing AR a171249f and 6e4a3553. Move them from \u00a73 into the decision log. Keep Mantle's light, its word and its cartridge open. Close the matching watch items.",
    "severity": "should"
   },
   {
    "where": "SURFACE_FIXES investor deck (model, light, mantle, tropos and why slides); ARCHIVE_OUTLINE \u00a79 and \u00a71.12",
    "problem": "The deck rebuild spec leaves stale figures in place. The model slide keeps 'Hemisphere $795\u2013$895', 'Core $650 (suggested)' and 'Mantle About $5,000 (suggested)', and the light and mantle slides repeat them. FACTS.md:83-85 on origin/r47-brand marks the Hemisphere and Mantle figures 'Superseded (don't use)' and Core as 'Not set: the owner's to set'; WT 324 says the same. The spec also keeps the light slide's '575-lumen LED', superseded by the new ring (AR L40), and the mantle slide's 'Ortofon 2M', which is still open (WT 229). Archive \u00a79 records none of the deck's prices.",
    "fix": "At the rebuild, show only prices the owner set, or 'on request', and drop '575 lm' and 'Ortofon'. Add the deck's price history to archive \u00a79 and \u00a71.12: $19,000 a pair planned, the superseded lamp and Mantle figures, and about $12,100 of parts including the lit plinths.",
    "severity": "should"
   },
   {
    "where": "NEW_BOOK_OUTLINE 03 Identity, the new 'Motion' rule",
    "problem": "'It is the only motion the mark makes' drops v23's 'at rest' (L410). Without it, the rule forbids the site opening the owner asked for: the globe 'moves and shrinks into its place in the top left... and the earth keeps spinning' (README:118).",
    "fix": "Write 'It is the only motion the mark makes at rest', or name the opening move.",
    "severity": "nit"
   },
   {
    "where": "NEW_BOOK_OUTLINE 09 The line, Hemisphere 'Light' row; Rules ('word for word from RC:999 and RC:1081')",
    "problem": "This row states the redesign in the present tense, but the new design (option 3 with the bigger ring) is not drawn yet and still needs a heat test (AR 6e4a3553 L40-41). RC:1081 says 'its source shielded inside the hub', so the claim that product facts are copied word for word from the site is false for this row, and also for the Mains and Cartridge rows.",
    "fix": "Mark the row '(design figures)', as Mantle's Size row is. Drop the 'word for word' claim, or list the rows that differ from the RC.",
    "severity": "nit"
   },
   {
    "where": "NEW_BOOK_OUTLINE 06 Images L493 (tropos-amp-ember.jpg); 03 Identity L399 caption ('the rating plate')",
    "problem": "The approved close-up (488fbec9; plan/look/honest-amp-ember.jpg) shows a plate reading 'MODEL TR-1', 'S/N TR1-26-000127' and 'DESIGNED IN SAN FRANCISCO, CALIFORNIA'. The plan cuts TR-1 and the rating plate as proposals (L382, L546-548), yet keeps this picture and the caption's mention of 'the rating plate'.",
    "fix": "Every Tropos studio picture is being re-rendered anyway (AR L30-33). Ask for the plate in that batch to be blank, or to carry EARF and Tropos only. Keep it as a watch item until then.",
    "severity": "nit"
   },
   {
    "where": "NEW_BOOK_OUTLINE 04 Color, the L456 rewrite; 01 Position L349",
    "problem": "The owner called color-theory pairing 'a future idea' for product-page recommendations (README:1123). The recorded scheme gives Fog 'a lamp in any one of the six' (README:1236), not 'the cool tints'. L349's 'one color or three' also leaves out the two-tint complement pairing that the new rule allows.",
    "fix": "Present the rule as the brand's own, or move it to chapter 10 as a direction. Change L349 to 'one, two or three'.",
    "severity": "nit"
   },
   {
    "where": "plan/test/mock-book-yes.html:497; tools/apply_plan.py --editions; tools/check_book.py",
    "problem": "The 'yes' test build includes a 'Special editions' block. The plan keeps special editions out of the Book, no owner question covers them, and check_book.py has no check that would catch the block.",
    "fix": "Build the yes test without --editions, or add a check that fails on 'special edition' unless a flag allows it.",
    "severity": "nit"
   },
   {
    "where": "NEW_BOOK_OUTLINE 01 Position (L350-360); 07 Voice L534; 09 The line (Hemisphere and Core 'Shades: All seven, sold singly'; 'designed in San Francisco')",
    "problem": "The plan keeps brand-lane and site copy as CURRENT, although the owner has not reviewed the second edition's wording (WT 278, open). 'Designed in San Francisco' was a delegated call that has been put back to him (WT 243, unclear). 'Made to order, so we quote rather than list' rests on prices that are parked (WT 324). 'Sold singly' is a sales model nobody has decided.",
    "fix": "When the link goes to the owner, add one line saying the Book's wording is the brand lane's and awaits his read (WT 278). Change none of this copy without him.",
    "severity": "nit"
   },
   {
    "where": "NEW_BOOK_OUTLINE 06 Image direction lede",
    "problem": "'Three kinds of picture' conflicts with the Book's own social rule, which names the lineup of the seven as a kind (L550). It also drops the owner's direction to show 'all 4 products in a room together' (2026-10-31T19:52:03Z). The first pass of the Book had that as its 'At home' kind (r47-brand 4bd29e7a).",
    "fix": "Write 'Three of the kinds of picture'. Optionally, add the room picture to chapter 10 as a direction.",
    "severity": "nit"
   }
  ],
  "plan_holds": false
 }
]
