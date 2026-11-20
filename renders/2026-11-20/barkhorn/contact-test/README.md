# The fronts with the sweep's contact term off (2026-11-20, the coordinator's test)

Ember and Fog fronts from their own shot files (`A-polished-tallr7/site-front-off-tall-<tint>.shot.json`), with one
change: `set.contact.strength` and `core_strength` from 1.7 and 2.2 to 0. The acrylic already passes tinted light into
shadows: its shadow rays cross the faces, tinted by its volume (`materials._clear_resin`). The contact term is a grey
darkening painted on the sweep near anything standing on it, whatever the light.

- **Minutes:** 5 (Ember) and 7 (Fog), at 96 samples.
- **L*, old / new:**

  | | Ember | Fog |
  |---|---|---|
  | bottom-right patch (880, 1130) | 89.8 / 89.9 | 90.0 / 90.2 |
  | the cast shadow at the right foot | 82.2 / 94.4 | 84.5 / 95.6 |
  | its chroma | 3.9 / 4.1 | 3.3 / 3.5 |
  | cabinet | 17.6 / 17.6 | 76.3 / 76.3 |
  | horn | 44.0 / 44.1 | 92.5 / 92.6 |

- **What moves:** the grey at the foot goes, and the cabinets look less planted.
- **What does not:**
  - no red reaches the floor: the cabinet's lining (batting, opaque) blocks the light through its body;
  - the bottom-right patch does not move, so it lies in no shadow: it is the sweep's light falling off;
  - the insides, the horn's glow and the noise are unchanged;
  - 94 % of the frame is within 8 levels of the passed front.
- **Old against new:** `old-new-ember-fog.png` (Ember old, Ember new, Fog old, Fog new).
