"""Plays Geometry Wars for a recording: moves away from the enemies that come close, and aims
and fires at the nearest one with the mouse.

The bot finds things by colour, on a quarter-size copy of the screen: the ship is white, the
wanderers pink, the seekers yellow and the black holes turquoise. Every enemy near the ship
pushes it away, more strongly the nearer it is, and so do the edges of the screen. With nothing
near, the ship drifts back towards the middle.

python gw_bot.py <frames folder> [seconds]
"""
import sys
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 40
WIDTH, HEIGHT = 1280, 720


def blobs(mask):
    """The middles of the lit areas of a quarter-size mask, in window pixels."""
    points = []
    ys, xs = np.nonzero(mask)
    left = np.ones(len(ys), bool)
    while left.any():
        i = np.argmax(left)
        near = left & (np.abs(xs - xs[i]) < 10) & (np.abs(ys - ys[i]) < 10)
        if near.sum() >= 3:
            points.append((xs[near].mean() * 4, ys[near].mean() * 4))
        left &= ~near
    return points


game = Game('11-geometry-wars', 'GeometryWars6')
game.tap('enter')
ship = (WIDTH / 2, HEIGHT / 2)
firing = False


def bot(img, t):
    global ship, firing
    small = np.asarray(img)[::4, ::4].astype(int)
    r, g, b = small[:, :, 0], small[:, :, 1], small[:, :, 2]
    white = (r > 235) & (g > 235) & (b > 235)
    white[:18] = False                               # the score and lives, along the top
    pink = (r > 215) & (b > 215) & (g < 170)
    yellow = (r > 215) & (g > 150) & (g < 215) & (b < 90)
    turquoise = (r < 80) & (g > 200) & (b > 180)

    # The ship is the white thing nearest to where it was. The pointer is white too, but the bot
    # knows where it put that.
    whites = [p for p in blobs(white) if abs(p[0] - game.pointer[0]) + abs(p[1] - game.pointer[1]) > 40]
    if whites:
        ship = min(whites, key=lambda p: (p[0] - ship[0]) ** 2 + (p[1] - ship[1]) ** 2)
    enemies = blobs(pink | yellow)
    holes = blobs(turquoise)

    push = np.array([0.0, 0.0])
    for x, y in enemies + holes + holes:             # a black hole counts double
        away = np.array([ship[0] - x, ship[1] - y])
        distance = max(np.hypot(*away), 1)
        if distance < 320:
            push += away / distance * (320 - distance) / 320
    for edge, axis, sign in ((ship[0], 0, 1), (WIDTH - ship[0], 0, -1), (ship[1], 1, 1), (HEIGHT - ship[1], 1, -1)):
        if edge < 150:
            push[axis] += sign * (150 - edge) / 60
    if np.hypot(*push) < 0.15:                       # nothing near: back towards the middle
        to_middle = np.array([WIDTH / 2 - ship[0], HEIGHT / 2 - ship[1]])
        push = to_middle / max(np.hypot(*to_middle), 1) * (0.3 if np.hypot(*to_middle) > 120 else 0)

    keys = []
    if push[0] > 0.12: keys.append('d')
    if push[0] < -0.12: keys.append('a')
    if push[1] > 0.12: keys.append('s')
    if push[1] < -0.12: keys.append('w')
    game.hold(*keys)

    if enemies or holes:
        target = min(enemies + holes, key=lambda p: (p[0] - ship[0]) ** 2 + (p[1] - ship[1]) ** 2)
        game.pointer = target
        game.move(*target)
        if not firing:
            game.mouse_down()
            firing = True


game.pointer = (900, 360)
game.move(*game.pointer)
frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
