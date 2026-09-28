"""A lighter GIF for busy scenes: gifsmall.py out.gif width ms step colors pattern..."""
import glob, os, sys
from PIL import Image

out, width, ms, step, colors = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
files = []
for pat in sys.argv[6:]:
    files += sorted(glob.glob(pat))
files = files[::step]
frames = []
for f in files:
    im = Image.open(f).convert('RGB')
    frames.append(im.resize((width, round(im.height * width / im.width)), Image.LANCZOS))
pal = [fr.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for fr in frames]
pal[0].save(out, save_all=True, append_images=pal[1:], duration=ms, loop=0, optimize=True, disposal=1)
print(out, len(frames), 'frames', os.path.getsize(out) // 1024, 'KB')
