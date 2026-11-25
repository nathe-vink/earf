#!/bin/bash
# Check the public site serves C6d: every page byte-equal to the C6d tree (gate/tree6), noindex kept. usage: livecheck.sh [tree]
G=/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/gate
T=${1:-$G/tree6}/spinoffs/barkhorn/site
B=https://www.earf.world
ok=0; bad=0
chk(){ if [ "$1" = "1" ]; then echo "ok   $2"; ok=$((ok+1)); else echo "BAD  $2"; bad=$((bad+1)); fi; }
for pair in "/:index.html" "/tropos/acid:tropos/acid.html" "/tropos/ember:tropos/ember.html" "/hemisphere/ember:hemisphere/ember.html" "/core/ember:core/ember.html" "/mantle/ember:mantle/ember.html" "/lighting:lighting.html" "/contact:contact.html"; do
  u=${pair%%:*}; f=${pair##*:}
  live=$(curl -s --max-time 40 "$B$u" | sha256sum | cut -c1-16); want=$(sha256sum "$T/$f" | cut -c1-16)
  chk $([ "$live" = "$want" ] && echo 1 || echo 0) "$u equals the tree's $f ($live vs $want)"
done
H=$(curl -s --max-time 30 "$B/")
chk $(echo "$H" | grep -c 'noindex' | awk '{print ($1>0)?1:0}') "home still noindex"
code=$(curl -s -o /dev/null --max-time 30 -w '%{http_code}' "$B/no-such-page"); chk $([ "$code" = 404 ] && echo 1 || echo 0) "404 page answers 404 ($code)"
code=$(curl -s -o /dev/null --max-time 30 -w '%{http_code}' "$B/colors/acid"); chk $([ "$code" = 308 ] || [ "$code" = 301 ] || [ "$code" = 307 ] || [ "$code" = 302 ] && echo 1 || echo 0) "/colors/acid redirects ($code)"
echo "RESULT ok=$ok bad=$bad"
