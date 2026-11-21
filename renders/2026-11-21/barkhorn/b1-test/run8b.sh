#!/bin/bash
# fixed-8 (c): the honest black horn: the near crop (576 x 765 at 960, 0) of fixed-8 without the niche panels, the
# speaker moved as in fixed-8, at fixed-8's 512 samples; with masks; committed and pushed
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
python3 -c "import json; s = json.load(open('$F/fixed8-black.json')); s['render'].update(samples=512, adaptive=0.003); json.dump(s, open('$F/fixed8-black.json', 'w'), indent=1)"
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed8-black.json --out $F/crop8-black.png --crop 0.6 0.0 0.96 0.85 --masks > /tmp/claude-0/crop8-black.log 2>&1; rc=$?
echo "black exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/crop8-black.log)"
rm -f "${F:?}"/*.raw.png
git add $F/crop8-black.* $F/fixed8-black.json $F/run8b.sh && git commit -q -m "B1 fixed-8 (c): the honest black horn, the near crop without the niche panels (not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
