"""Plays Pac-Man for a recording: reads the screen, heads for the nearest dots, and keeps away
from the ghosts.

The maze is drawn from tile (0, 0) at window pixel (280, 90), 20 pixels a tile. The walls come
from the game's own maze.txt. Every look, the bot finds Pac-Man and the ghosts by their colours
and the dots by the pixel in the middle of each tile. It then searches the maze from Pac-Man's
tile: every step costs one, and a step near a ghost that isn't frightened costs much more, the
nearer the ghost. It
walks towards the cheapest dot to reach, which is usually the nearest one that is safe.

python pacman_bot.py <frames folder> [seconds]
"""
import heapq, os, sys
from collections import deque
import numpy as np
from botlib import Game, GAMES

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 40
LEFT, TOP, TILE = 280, 90, 20
PACMAN = [(160, 220, 70), (96, 160, 48)]
GHOSTS = [(232, 72, 72), (245, 140, 200), (70, 200, 224), (245, 152, 48)]
DOTS = [(250, 224, 176), (250, 200, 80)]
KEYS = {(0, -1): 'up', (0, 1): 'down', (-1, 0): 'left', (1, 0): 'right'}

rows = open(os.path.join(GAMES, '05-pac-man', 'Content', 'Assets', 'levels', 'maze.txt')).read().splitlines()
H, W = len(rows), max(len(r) for r in rows)
open_tile = {(x, y) for y, row in enumerate(rows) for x, ch in enumerate(row.ljust(W)) if ch not in '#-Hpic'}


def neighbours(tile):
    for d in KEYS:
        n = ((tile[0] + d[0]) % W, tile[1] + d[1])
        if n in open_tile:
            yield d, n


def code(colour):
    return (colour[0] << 16) | (colour[1] << 8) | colour[2]


def middle(mask):
    """The tile at the middle of the pixels in mask, or None."""
    ys, xs = np.nonzero(mask)
    if len(ys) < 12:
        return None
    return int(xs.mean() // TILE), int(ys.mean() // TILE)


def read(img):
    # Only the maze, with each pixel's colour as one number: comparing those is fast.
    px = np.asarray(img.crop((LEFT, TOP, LEFT + W * TILE, TOP + H * TILE))).astype(np.uint32)
    px = (px[:, :, 0] << 16) | (px[:, :, 1] << 8) | px[:, :, 2]
    pacman = middle(np.isin(px, [code(c) for c in PACMAN]))
    ghosts = [g for g in (middle(px == code(c)) for c in GHOSTS) if g]
    centres = px[TILE // 2::TILE, TILE // 2::TILE]
    dotted = np.isin(centres, [code(c) for c in DOTS])
    dots = {(x, y) for y, x in zip(*np.nonzero(dotted)) if (x, y) in open_tile}
    return pacman, ghosts, dots


def danger(ghosts):
    """How many steps each tile is from the nearest ghost, for the tiles close to one."""
    steps = {g: 0 for g in ghosts if g in open_tile}
    todo = deque(steps)
    while todo:
        tile = todo.popleft()
        if steps[tile] >= len(NEAR) - 1:
            continue
        for _, n in neighbours(tile):
            if n not in steps:
                steps[n] = steps[tile] + 1
                todo.append(n)
    return steps


NEAR = [300, 120, 60, 30, 12, 6, 3]                  # what a step costs this many steps from a ghost


def choose(pacman, ghosts, dots, heading):
    """The direction of the first step towards the cheapest dot. Turning straight back costs a
    little extra, so Pac-Man doesn't dither between two dots that are about as good."""
    near = danger(ghosts)
    cost = lambda tile: 1 + (NEAR[near[tile]] if near.get(tile, 9) < len(NEAR) else 0)
    back = (-heading[0], -heading[1]) if heading else None
    best, todo = {pacman: 0}, [(0, pacman, None)]
    while todo:
        spent, tile, first = heapq.heappop(todo)
        if spent > best[tile]:
            continue
        if tile in dots and first:
            return first
        for d, n in neighbours(tile):
            total = spent + cost(n) + (8 if first is None and d == back else 0)
            if total < best.get(n, 1 << 30):
                best[n] = total
                heapq.heappush(todo, (total, n, first or d))
    return None


game = Game('05-pac-man', 'Pacman5')
game.tap('enter')
pressed, tapped, idle_since = None, 0.0, 0.0


def bot(img, t):
    global pressed, tapped, idle_since
    pacman, ghosts, dots = read(img)
    if pacman is None or pacman not in open_tile:
        if t - idle_since > 4:                       # game over: start again
            game.tap('enter')
            idle_since = t
        return
    idle_since = t
    direction = choose(pacman, ghosts, dots, pressed)
    # Press again every so often: after a lost life the game has forgotten the last key.
    if direction and (direction != pressed or t - tapped > 0.15):
        game.tap(KEYS[direction], 0.035)
        pressed, tapped = direction, t


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
