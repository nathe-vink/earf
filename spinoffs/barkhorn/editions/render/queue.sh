#!/bin/bash
# Render a list of frames one after another: queue.sh SAMPLES "edition shot tag" ...
cd "$(dirname "$0")"
R=../renders/2026-10-31
S=$1; shift
for es in "$@"; do
  set -- $es
  python3.11 scenes.py -- $1 $2 $R/$1-$2-$3.png --samples $S 2>&1 | grep -i "error\|wrote\|Traceback" | grep -v CUEW
done
