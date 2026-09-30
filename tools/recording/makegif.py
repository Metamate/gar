"""Builds a GIF from captured frames, optionally cropped:
python makegif.py out.gif width ms "x0,y0,x1,y1|none" [hold_last_frames] pattern...
The frames are scaled with nearest neighbour, which keeps pixel art sharp. Pick a width
where one art pixel becomes a whole number of GIF pixels (half the window width, usually)."""
import glob, sys
from PIL import Image

out, width, ms, crop = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
hold = int(sys.argv[5]) if sys.argv[5].isdigit() else 0
patterns = sys.argv[6:] if sys.argv[5].isdigit() else sys.argv[5:]
files = []
for pat in patterns:
    files += sorted(glob.glob(pat))
box = None if crop == 'none' else tuple(int(v) for v in crop.split(','))
frames = []
for f in files:
    im = Image.open(f).convert('RGB')
    if box:
        im = im.crop(box)
    h = round(im.height * width / im.width)
    frames.append(im.resize((width, h), Image.NEAREST))
frames += [frames[-1]] * hold                      # linger on the last frame before looping
pal = [fr.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for fr in frames]
pal[0].save(out, save_all=True, append_images=pal[1:], duration=ms, loop=0, optimize=True, disposal=1)
import os
print(out, len(frames), 'frames', os.path.getsize(out) // 1024, 'KB')
