"""Plays Vampire Survivors for a recording: walks where the swarm is thinnest, picks up gems on
the way, and takes the first upgrade whenever one is offered.

The player stays in the middle of the screen. The bot looks at the eight directions around him:
enemies close by in a direction count against it, gems count for it. It walks in the best
direction, and only changes its mind when another is clearly better, so it doesn't twitch.

python survivors_bot.py <frames folder> [seconds]
"""
import math, sys
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 45
ENEMY, GEM = (172, 120, 220), (60, 172, 215)
CENTRE = (640, 360)
DIRECTIONS = {0: 'd', 45: 'ds', 90: 's', 135: 'sa', 180: 'a', 225: 'aw', 270: 'w', 315: 'wd'}


def code(colour):
    return (colour[0] << 16) | (colour[1] << 8) | colour[2]


def scores(px):
    """For each of the eight directions: gems to pick up, less the enemies in the way."""
    small = px[::4, ::4]
    ys, xs = np.indices(small.shape)
    dx, dy = xs * 4 - CENTRE[0], ys * 4 - CENTRE[1]
    distance = np.hypot(dx, dy)
    angle = np.degrees(np.arctan2(dy, dx)) % 360
    enemy = (small == code(ENEMY)) & (distance < 300)
    gem = (small == code(GEM)) & (distance < 330) & (distance > 30)
    result = {}
    for direction in DIRECTIONS:
        within = np.abs((angle - direction + 180) % 360 - 180) < 50
        closeness = np.clip(300 - distance, 0, 300) / 300
        result[direction] = 3 * np.count_nonzero(gem & within) - float((closeness * (enemy & within)).sum()) * 2
    return result


game = Game('12-vampire-survivors', 'Survivors4')
game.tap('enter')
heading, decided, next_choice = 0, -1.0, 1.0


def bot(img, t):
    global heading, decided, next_choice
    if t >= next_choice:                             # a level-up menu, if one is open: the first upgrade
        game.tap('1', 0.04)
        next_choice = t + 0.8
    if t - decided < 0.35:
        return
    rgb = np.asarray(img).astype(np.uint32)
    px = (rgb[:, :, 0] << 16) | (rgb[:, :, 1] << 8) | rgb[:, :, 2]
    score = scores(px)
    best = max(score, key=score.get)
    if score[best] > score[heading] + 25:
        heading = best
    game.hold(*DIRECTIONS[heading])
    decided = t


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
