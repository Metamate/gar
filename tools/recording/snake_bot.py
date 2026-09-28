"""Plays Snake9 for a recording: reads the screen, finds the snake and the bat, and steers.

The room is cells 1-14 across and 2-7 down on an 80-pixel grid. Every snake segment has the
colour (0, 184, 0) at its cell centre, and the bat is the only purple on screen. The head is the
cell that turned green since the last move. At each move the bot picks the safe direction that
brings it closest to the bat, and never one that leads into a pocket smaller than the snake.

python snake_bot.py <Snake9.exe> <frames folder> [seconds] [frame interval ms]
"""
import ctypes, os, subprocess, sys, time
from ctypes import wintypes
from PIL import ImageGrab

EXE, OUT = sys.argv[1], sys.argv[2]
SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 else 12
INTERVAL = (int(sys.argv[4]) if len(sys.argv) > 4 else 100) / 1000
CELL, ROOM = 80, (1, 2, 14, 7)                      # first column, first row, last column, last row
SNAKE, BAT = (0, 184, 0), (152, 120, 248)
KEYS = {(0, -1): 0x26, (0, 1): 0x28, (-1, 0): 0x25, (1, 0): 0x27}   # up, down, left, right

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


def window_of(pid):
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def each(hwnd, _):
        owner = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == pid and user32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True
    user32.EnumWindows(each, 0)
    return found[0] if found else None


def client_box(hwnd):
    rect = wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    pt = wintypes.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(pt))
    return (pt.x, pt.y, pt.x + rect.right, pt.y + rect.bottom)


def tap(vk):
    user32.keybd_event(vk, 0, 1, 0)                # extended key: the arrows
    time.sleep(0.02)
    user32.keybd_event(vk, 0, 1 | 2, 0)


def read(img):
    snake = {(x, y) for y in range(ROOM[1], ROOM[3] + 1) for x in range(ROOM[0], ROOM[2] + 1)
             if img.getpixel((x * CELL + CELL // 2, y * CELL + CELL // 2)) == SNAKE}
    small = img.resize((img.width // 4, img.height // 4))
    purple = [(x * 4, y * 4) for y in range(small.height) for x in range(small.width)
              if small.getpixel((x, y)) == BAT]
    bat = None
    if purple:
        bat = (sum(p[0] for p in purple) / len(purple) / CELL, sum(p[1] for p in purple) / len(purple) / CELL)
    return snake, bat


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


def choose(head, heading, body, bat):
    options = []
    for d in KEYS:
        if d == (-heading[0], -heading[1]):
            continue
        n = (head[0] + d[0], head[1] + d[1])
        if not inside(n) or n in body:
            continue
        space = room_left(n, body)
        dist = abs(n[0] + 0.5 - bat[0]) + abs(n[1] + 0.5 - bat[1]) if bat else 0
        options.append((space < len(body) + 2, dist, d != heading, d))
    return min(options)[3] if options else heading


proc = subprocess.Popen([EXE], cwd=os.path.dirname(EXE))
time.sleep(2.5)
hwnd = window_of(proc.pid)
user32.SetForegroundWindow(hwnd)
time.sleep(0.3)
box = client_box(hwnd)
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.png'):
        os.remove(os.path.join(OUT, f))

prev, head, heading, frame, next_shot = set(), None, (1, 0), 0, time.time()
start = time.time()
while time.time() - start < SECONDS:
    img = ImageGrab.grab(bbox=box, all_screens=True).convert('RGB')
    now = time.time()
    if now >= next_shot:
        img.save(os.path.join(OUT, f'f{frame:03d}.png'))
        frame += 1
        next_shot += INTERVAL
    snake, bat = read(img)
    new = snake - prev
    if snake and new and snake != prev:
        if len(new) == 1:
            cell = next(iter(new))
            if head and abs(cell[0] - head[0]) + abs(cell[1] - head[1]) == 1:
                heading = (cell[0] - head[0], cell[1] - head[1])
            head = cell
        else:                                        # a new game: the snake starts heading right
            head, heading = max(snake), (1, 0)
        turn = choose(head, heading, snake, bat)
        if turn != heading:
            tap(KEYS[turn])
    prev = snake
    time.sleep(0.01)
proc.kill()
print('captured', frame, 'frames')
