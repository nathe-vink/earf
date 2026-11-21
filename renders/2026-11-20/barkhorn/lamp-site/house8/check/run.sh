cd /home/user/earf/spinoffs/barkhorn/companions
B="HOUSE_STUDIO=0.6 HOUSE_EV=-2.6 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 HOUSE_BG=1.16 EXR=0 DENOISE=1 BORDER=0.2625,0.7375,0.42,0.72"
for t in base nogloss nocaus; do
  X=""; [ $t = nogloss ] && X=HOUSE_TEST_NOGLOSS=1; [ $t = nocaus ] && X=REFR_CAUSTICS=0
  env $B $X "HOUSE_FLAGS=horn cutter" LAMP_OUT=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/xt/$t.png python3.11 lamp_site.py house-orb-red --samples 256 > /tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/xt/$t.log 2>&1; date -u
done
