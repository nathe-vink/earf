"""The owner's photograph beside barkhorn rendered from its angle: the photograph's left speaker and ours, scaled so
the cabinets' fronts are the same width and lined up at the top's front edge, for checking proportions (the horn's
size and shape, its height over the cabinet, the posts).

    python3 spinoffs/barkhorn/compare.py renders/2026-10-12/barkhorn/pick/pick-photo-birch.png OUT.png

The render's cabinet comes from its report (the parts' boxes on screen), not from its pixels.
"""
import json, os, sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from frames import font                                   # noqa: E402

PHOTO = os.path.join(HERE, 'reference', 'friendly-pressure-owner-2026-10-10.jpg')
# the photograph's left speaker, in its pixels: the cabinet's front from x 139 to 361, the top's front edge at y 285;
# the window round it
CAB_X, CAB_TOP = (139.0, 361.0), 285.0
WINDOW = (95, 95, 405, 600)


def main(render, out):
    rep = json.load(open(os.path.splitext(render)[0] + '.report.json'))['parts_2d']
    l, r = rep['left#0']['box_px'][0], rep['right#0']['box_px'][0]     # the front's left edge; the right side's front edge
    top = rep['top#0']['box_px'][3]                                     # the top's front edge (its lowest on screen)
    k = (CAB_X[1] - CAB_X[0]) / max(r - l, 1)                           # render px to photograph px
    rd = Image.open(render).convert('RGB')
    rd = rd.resize((round(rd.width * k), round(rd.height * k)), Image.LANCZOS)
    ox, oy = CAB_X[0] - l * k, CAB_TOP - top * k                        # the render's origin in photograph px
    canvas = Image.new('RGB', (1536, 998), (238, 236, 231))
    canvas.paste(rd, (round(ox), round(oy)))
    ph = Image.open(PHOTO).convert('RGB').crop(WINDOW)
    ours = canvas.crop(WINDOW)
    H = 900
    a = ph.resize((round(ph.width * H / ph.height), H), Image.LANCZOS)
    b = ours.resize(a.size, Image.LANCZOS)
    pad, lab = 20, 50
    sheet = Image.new('RGB', (2 * a.width + 3 * pad, H + lab + 2 * pad), (246, 244, 239))
    sheet.paste(a, (pad, pad)); sheet.paste(b, (2 * pad + a.width, pad))
    d = ImageDraw.Draw(sheet)
    d.text((pad, pad + H + 10), 'the photograph', font=font(22), fill=(60, 56, 52))
    d.text((2 * pad + a.width, pad + H + 10), 'barkhorn round 4, from its angle', font=font(22), fill=(60, 56, 52))
    sheet.save(out)
    print(out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
