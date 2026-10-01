"""Plays Snake9 for a recording: reads the screen, finds the snake and the food, and steers.

The room is cells 1-38 across and 1-20 down on a 32-pixel grid (8-dot cells at 4x). Everything is
the same green: a cell whose centre is lit holds the snake or the food, and only the snake's
blocks also light the dot near their corner. The head is the cell that lit up since the last move. At each move the bot picks the safe direction that
brings it closest to the food, and never one that leads into a pocket smaller than the snake.

python snake_bot.py <Snake9.exe> <frames folder> [seconds] [frame interval ms]
"""
import ctypes, os, subprocess, sys, time
from ctypes import wintypes
from winshot import grab, window_of

EXE, OUT = sys.argv[1], sys.argv[2]
SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 else 12
INTERVAL = (int(sys.argv[4]) if len(sys.argv) > 4 else 100) / 1000
CELL, DOT, ROOM = 32, 4, (1, 1, 38, 20)             # first column, first row, last column, last row
LIT = (120, 230, 90)
KEYS = {(0, -1): 0x26, (0, 1): 0x28, (-1, 0): 0x25, (1, 0): 0x27}   # up, down, left, right

user32 = ctypes.windll.user32


def tap(vk):
    user32.keybd_event(vk, 0, 1, 0)                # extended key: the arrows
    time.sleep(0.02)
    user32.keybd_event(vk, 0, 1 | 2, 0)


def lit(img, cell, dot):
    return img.getpixel((cell[0] * CELL + dot * DOT + DOT // 2, cell[1] * CELL + dot * DOT + DOT // 2))[:3] == LIT


def read(img):
    snake, food = set(), None
    for y in range(ROOM[1], ROOM[3] + 1):
        for x in range(ROOM[0], ROOM[2] + 1):
            if lit(img, (x, y), 3):
                if lit(img, (x, y), 1):
                    snake.add((x, y))
                else:
                    food = (x + 0.5, y + 0.5)
    return snake, food


def inside(c):
    return ROOM[0] <= c[0] <= ROOM[2] and ROOM[1] <= c[1] <= ROOM[3]


def room_left(start, blocked):
    """How many cells can be reached from start without crossing the snake."""
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx, dy in KEYS:
            n = (x + dx, y + dy)
            if inside(n) and n not in blocked and n not in seen:
                seen.add(n)
                todo.append(n)
    return len(seen)


def choose(head, heading, body, food):
    options = []
    for d in KEYS:
        if d == (-heading[0], -heading[1]):
            continue
        n = (head[0] + d[0], head[1] + d[1])
        if not inside(n) or n in body:
            continue
        space = room_left(n, body)
        dist = abs(n[0] + 0.5 - food[0]) + abs(n[1] + 0.5 - food[1]) if food else 0
        options.append((space < len(body) + 2, dist, d != heading, d))
    return min(options)[3] if options else heading


proc = subprocess.Popen([EXE], cwd=os.path.dirname(EXE))
time.sleep(2.5)
hwnd = window_of(proc.pid)
user32.keybd_event(0x12, 0, 0, 0)                   # Windows only hands over the focus after a key press
user32.keybd_event(0x12, 0, 2, 0)
user32.SetForegroundWindow(hwnd)
time.sleep(0.3)
user32.keybd_event(0x0D, 0x1C, 0, 0)                # Enter, past the title screen
time.sleep(0.05)
user32.keybd_event(0x0D, 0x1C, 2, 0)
time.sleep(0.2)
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.png'):
        os.remove(os.path.join(OUT, f))

prev, head, heading, frame, next_shot = set(), None, (1, 0), 0, time.time()
start = time.time()
while time.time() - start < SECONDS:
    img = grab(hwnd)
    now = time.time()
    if now >= next_shot:
        img.save(os.path.join(OUT, f'f{frame:03d}.png'))
        frame += 1
        next_shot += INTERVAL
    snake, food = read(img)
    new = snake - prev
    if snake and new and snake != prev:
        if len(new) == 1:
            cell = next(iter(new))
            if head and abs(cell[0] - head[0]) + abs(cell[1] - head[1]) == 1:
                heading = (cell[0] - head[0], cell[1] - head[1])
            head = cell
        else:                                        # a new game: the snake starts heading right
            head, heading = max(snake), (1, 0)
        turn = choose(head, heading, snake, food)
        if turn != heading:
            tap(KEYS[turn])
    prev = snake
    time.sleep(0.01)
proc.kill()
print('captured', frame, 'frames')
