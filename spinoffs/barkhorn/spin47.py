"""Round 47: Tropos turning, path-traced, for the site's product page (the coordinator, 2026-10-31: a spin of
path-traced frames in place of the real-time 3D view, which a blind critic found would hurt beside the stills).

The studio's bright-field hero (studio/shots/barkhorn/studio31/hero-light-<colour>.json) exactly as the stills were
made, its camera and light fixed, the speaker turned on its own axis in 36 steps of 10 degrees, cropped round it.
Each frame is about two minutes on this container's four cores (32 samples, denoised, at 0.75 of the shot's size).

    python3 spinoffs/barkhorn/spin47.py ember smoke [poison ice ...]     resumable: a frame already there is kept

Frames go to renders/2026-10-31/barkhorn/spin47/<colour>/f-NN.png; web.py --images makes the site's from them.
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'spin47')
N, SAMPLES, SCALE, CROP = 36, 32, 0.75, ('0.29', '0.04', '0.71', '0.97')


def frame(name, i):
    out = os.path.join(OUT, name, f'f-{i:02d}.png')
    if os.path.exists(out):
        return False
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shot = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'studio31', f'hero-light-{name}.json')
    subprocess.run([sys.executable, os.path.join(ROOT, 'studio', 'engine', 'render.py'), shot, '--out', out,
                    '--samples', str(SAMPLES), '--scale', str(SCALE), '--crop', *CROP,
                    '--set', f'product.instances.0.rotate_z={i * 360 / N:.1f}'], check=True, cwd=ROOT,
                   stdout=subprocess.DEVNULL)
    for side in ('.shot.json', '.report.json'):        # the first frame's are kept as the record; the rest say the same
        p = out[:-4] + side
        if i and os.path.exists(p):
            os.remove(p)
    return True


if __name__ == '__main__':
    for name in sys.argv[1:]:
        for i in range(N):
            t = time.time()
            if frame(name, i):
                print(f'{name} {i + 1}/{N} {time.time() - t:.0f}s', flush=True)
        print(f'{name} done', flush=True)
