#!/bin/bash
# B1 fixed-8 at 1600 x 900, 512 samples, with masks; its log kept beside it; committed and pushed
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed8.json --out $F/fixed8.png --masks > /tmp/claude-0/b1-fixed8.log 2>&1; rc=$?; grep -v "INFO\|Timer" /tmp/claude-0/b1-fixed8.log > $F/fixed8.log
echo "fixed8 exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/b1-fixed8.log)"
rm -f "${F:?}"/*.raw.png
git add $F/fixed8.* $F/run8.sh && git commit -q -m "B1 test: fixed-8 (the horn call: the near Tropos moved, warm opal niche backs; P3 move, P4 grid and flag; 512 spp; not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
