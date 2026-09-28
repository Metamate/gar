"""Prints the frames of the longest stretch of play: frames with the score in the top-left
corner, so title screens after a death are left out. Usage: python longest_play.py frames-dir"""
import glob, os, sys
from PIL import Image

files = sorted(glob.glob(os.path.join(sys.argv[1], 'f*.png')))
playing = []
for f in files:
    corner = Image.open(f).convert('RGB').crop((5, 5, 170, 35))
    white = sum(1 for p in corner.get_flattened_data() if min(p) > 240)
    playing.append(white > 30)

best, start = (0, 0), None
for i, p in enumerate(playing + [False]):
    if p and start is None:
        start = i
    elif not p and start is not None:
        best = max(best, (i - start, start))
        start = None
length, first = best
print('\n'.join(files[first:first + length]))
