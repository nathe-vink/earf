# Planet EARF: the passes

Each pass: the proof (0.5 scale, 48 to 64 samples), a fresh blind critic (critic/PROMPT-promo.md, the image, its card
from `card.py`, the measuring tool), its reply verbatim in `critic/VIEW-rN.json`, and what was done. A round is all the
views rendered from one state of the model and shots.

| round | view | blind | if fixed | the critic's top changes | what was done |
|---|---|---|---|---|---|
| 1 | door | 5.0 | 7.0 | corner pairs crushed in dark corners; the Fog speakers read as steel; camera too wide (18 mm); ceiling the largest bright field; booths crushed; floor CG-smooth; no haze; empty bar | spots re-aimed from in front of each pair, complementary washes behind; Fog niches dimmed, a spot on each; membrane 0.2 to 0.09 and warmer; Bell 35 W; worn concrete floor with a broken sheen; haze; glasses and menus; 24 mm |
| 1 | bar | 5.5 | 7.5 | ceiling 0.2 to 0.08; shelves and back panel down; panels balanced per colour (measured); a vertical gradient and lit seams; camera lower; floor texture; haze; glasses | all, as given (panel factors from its measurements) |
| 1 | back-bar | 4.5 | 7.0 | camera higher, both niches, f/2.8; shelves 0.9 to 0.35; the niche dark with a rim on the speaker; more bottle shapes and printed labels; a textured stone; a glass in front; haze; warmer white balance | camera to a stool's eye at 35 mm f/2.8 on the horn; shelves 0.5; niche 0.05; Fog spot 150 W; twelve bottle shapes, each scaled, with printed labels and gaps |
| 1 | records | 4.5 | 6.5 | the recess the same blue as Cumulus; the desk lamp on the wall; camera closer (45 mm); the desk front crushed; haze | recess glow 0.12 to 0.05 and warm; desk spot straight down, 35 deg; 45 mm f/4 on Cumulus |
| 1 | street | 3.5 | 6.5 | rethink the framing: the window small, no door or neon in frame; lamps light nothing; flat facades; voids at the edges | camera to the corner (door and neon at left, the window running right); neighbours on both streets; lamps 600 W; a damp road |
| 2 | bar | 5.0 | 7.0 | Ember cut by the frame; panels still flat; Haze and Smoke dim; floor dull; yellow mustard | (view changed to Khronos PBR Neutral after the first round-2 frames: AgX bleached the panels to pastel); camera 28 mm from [1.6, 4.6]; Haze x1.6, Smoke x2.2, Fog x0.8; panel gradient 1.0 to 0.65; Acid's light greener |
| 2 | door | 4.0 | 6.8 | "two brown boxes mid-room" (the Fog screens, read as speakers); too dark; a red cast; the ceiling the largest field | **the screens taken out** (my addition, not the brief's; they hid the Ember pair); exposure 0.5 to 1.1; membrane 0.05; Bell 60 W; the record wall's spots softened |
| 3 | listening | 4.5 | 7.0 | (first pass; the view turned round to look from the DJ's side at the Ember pair) the pair cut by chair shells; the ceiling the brightest field; floor mottled; the slats' LED clipping | membrane 0.012 at the warm 'sunset' hour for every view (the clock's frames bring it up); two chairs moved out of the pair's sightlines; slat LED 3 |
| 3 | door | 5.0 | 7.0 | the corner pairs unlit behind chairs; camera lower (28 mm); ceiling pink; floor mottled; a red-magenta cast | spots 2000 W; 28 mm from [2.2, 4.1, 1.15]; tint 0 to 10, 3600 K, on the belief that 10 is Blender's neutral (it was not: see round 4) |
| 3 | bar | 5.5 | 7.5 | joints as bright hairlines (wanted dark); panels still flat; floor smeared; shelves a second rainbow; ceiling pink | joints a black 6 mm reveal; the gradient laid on the panel's own height (it had read flat); shelves 0.25; floor darker, its sheen higher; pinholes 140 W; haze 0.01 |

| 4 | listening | 4.5 | 7.0 | the camera must face the record wall (the card); the pair cut at the frame's edges; ceiling brightest; haze veiling; chairs the Ember's own hue | camera back toward the record wall from the centre aisle, 24 mm; the pairs lit by 0.7 m soft area lamps (6 W/m2 at the cabinet) instead of spots that overshot onto the wall; haze 0.004; membrane 0.006; chairs re-dyed darker, each turned a few degrees |
| 4 | door | 4.5 | 6.5 | still a red-magenta cast (floor r/g 2.2); the pairs hidden behind chairs; the ceiling speckled; the recess a grey hole; a table on the axis | **measured the tint: in this build a higher tint adds magenta** (0, 10, 25 took the floor's g from 25 to 23 to 20); 3000 K with tint -25 takes the floor's r/g to 1.5; standing eye 1.6 m at 32 mm; panels 0.4 in this view; washes 250 W; the recess 0.008; the side tables off the aisle. The rest of round 4 (rendered at tint 10) was not judged |

Lessons kept in the code:

- the membrane cannot be bright and also not the brightest field; it is held to a glimmer except in the clock's frames;
- AgX desaturates emissive colour near white; the brand colours need Khronos PBR Neutral;
- in this build a higher white-balance tint adds magenta; the room's grade is 3000 K at tint -25 (measured);
- a 10 mm gap round the closed door let the street lamp in as fireflies the denoiser smears into a blob;
- a haze box coplanar with the membrane draws a curved band; it stops 60 mm below.
