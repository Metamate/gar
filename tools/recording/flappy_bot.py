"""Plays Flappy12 for a recording: reads the screen, finds the bird and the next gap, and flaps.

The window is 1024 x 576, twice the 512 x 288 virtual resolution. The bird is the only
yellow (248, 184, 0) on screen and the pipes the only green (0, 184, 0). The next gap is the
longest run of rows without a pipe in the nearest pipe ahead of the bird. A flap lifts the
bird about 92 window pixels (300^2 / (2 * 980) game pixels, doubled), and the gap is 180, so
the bot flaps only when the bird's bottom nears the bottom of the gap. Reading the screen
and pressing a key takes a moment, so it flaps on where the bird will be a little later,
from its speed over the last two frames.

python flappy_bot.py <Flappy12.exe> <frames folder> [seconds] [frame interval ms]
"""
import ctypes, os, subprocess, sys, time
import numpy as np
from ctypes import wintypes
from winshot import grab, window_of

EXE, OUT = sys.argv[1], sys.argv[2]
SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 else 20
INTERVAL = (int(sys.argv[4]) if len(sys.argv) > 4 else 100) / 1000
BIRD, PIPE = (248, 184, 0), (0, 184, 0)
PIPE_COLOURS = {(0, 184, 0), (0, 0, 0), (0, 120, 0), (184, 248, 24)}
GROUND = 544                                        # where the ground starts, in window pixels
BIRD_WIDTH = 96
SPACE, ALT = (0x20, 0x39), (0x12, 0x38)            # virtual-key code, scan code (SDL reads the scan code)

user32 = ctypes.windll.user32


def tap(key):
    vk, scan = key
    user32.keybd_event(vk, scan, 0, 0)
    time.sleep(0.02)
    user32.keybd_event(vk, scan, 2, 0)


def bird_of(px):
    """The bird's left edge and bottom edge, or None when it isn't on screen. The bright yellow
    ends two art pixels (16 window pixels) above the bottom of the sprite: the belly and the
    outline."""
    ys, xs = np.nonzero(np.all(px[:GROUND, :400] == BIRD, axis=2))
    if len(ys) == 0:
        return None
    return xs.min(), ys.max() + 16


def gap_bottom(px, bird_x):
    """The bottom of the gap in the nearest pipe whose right edge is still ahead of the bird.
    The gap is read in a column of the pipe the bird doesn't cover: the bird's own outline
    would otherwise split the gap in two."""
    pipe = np.all(px[:GROUND] == PIPE, axis=2)
    columns = np.nonzero(pipe.sum(axis=0) > 40)[0]
    columns = columns[columns > bird_x - 16]          # the outline starts 8 pixels left of the yellow
    if len(columns) == 0:
        return GROUND / 2 + 60                      # no pipe yet: stay around the middle
    nearest = columns[columns < columns[0] + 150]   # the columns of that one pipe
    clear = nearest[(nearest < bird_x - 12) | (nearest > bird_x + BIRD_WIDTH)]
    if len(clear) == 0:
        return None                                 # the bird hides the pipe: keep the last gap
    column = px[:GROUND, clear[len(clear) // 2]]
    solid = np.zeros(GROUND, bool)
    for c in PIPE_COLOURS:
        solid |= np.all(column == c, axis=1)
    best, run, start = (0, 0), 0, 0
    for y, s in enumerate(solid):
        if s:
            run = 0
        else:
            if run == 0:
                start = y
            run += 1
            if run > best[0]:
                best = (run, start)
    return best[1] + best[0]


proc = subprocess.Popen([EXE], cwd=os.path.dirname(EXE))
time.sleep(2.5)
hwnd = window_of(proc.pid)
tap(ALT)                                         # Windows only hands over the focus after a key press
user32.SetForegroundWindow(hwnd)
time.sleep(0.3)
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.png'):
        os.remove(os.path.join(OUT, f))

tap(SPACE)
frame, next_shot, last_flap = 0, time.time(), 0
last_seen = None                                    # (time, bottom) of the bird in the previous frame
bottom = GROUND / 2 + 60
LOOKAHEAD = 0.07                                    # seconds
start = time.time()
while time.time() - start < SECONDS:
    img = grab(hwnd)
    now = time.time()
    if now >= next_shot:
        img.save(os.path.join(OUT, f'f{frame:03d}.png'))
        frame += 1
        next_shot += INTERVAL
    px = np.asarray(img)
    bird = bird_of(px)
    if bird:
        bottom = gap_bottom(px, bird[0]) or bottom
        speed = (bird[1] - last_seen[1]) / (now - last_seen[0]) if last_seen and now > last_seen[0] else 0
        last_seen = (now, bird[1])
        ahead = bird[1] + max(speed, 0) * LOOKAHEAD
        if speed >= 0 and ahead > bottom - 26 and now - last_flap > 0.15:
            tap(SPACE)
            last_flap = now
    else:
        last_seen = None
    if not bird and now - last_flap > 1.5:          # the title or score screen: start again
        tap(SPACE)
        last_flap = now
    time.sleep(0.005)
proc.kill()
print('captured', frame, 'frames')
