"""An animated WebP for the site, for games that aren't pixel art (Geometry Wars' glow): full
colour, lossy, scaled smoothly. The site serves it as it is, from public/animations/.
python makewebp.py out.webp width ms quality pattern..."""
import glob, os, sys
from PIL import Image

out, width, ms, quality = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
files = []
for pat in sys.argv[5:]:
    files += sorted(glob.glob(pat))
frames = []
for f in files:
    im = Image.open(f).convert('RGB')
    frames.append(im.resize((width, round(im.height * width / im.width)), Image.LANCZOS))
frames[0].save(out, save_all=True, append_images=frames[1:], duration=ms, loop=0, quality=quality, method=6)
print(out, len(frames), 'frames', os.path.getsize(out) // 1024, 'KB')
