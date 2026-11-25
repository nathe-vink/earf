#!/bin/bash
# Check the public site serves the tree's image files byte for byte. usage: imgcheck.sh <tree> <img path relative to site/> ...
T=$1/spinoffs/barkhorn/site; shift
B=https://www.earf.world
ok=0; bad=0
for f in "$@"; do
  live=$(curl -s --max-time 40 "$B/$f" | sha256sum | cut -c1-16); want=$(sha256sum "$T/$f" | cut -c1-16)
  if [ "$live" = "$want" ]; then echo "ok   $f ($live)"; ok=$((ok+1)); else echo "BAD  $f ($live vs $want)"; bad=$((bad+1)); fi
done
echo "RESULT ok=$ok bad=$bad"
