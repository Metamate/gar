"""Plays Super Mario Bros for a recording: reads the screen, runs through the level, and jumps
when there is something to jump over, onto or into.

The window is three times the 426 x 240 game, so a tile is 54 pixels, and the rows of tiles
start at multiples of 54 from the top. Every piece of ground has a two-pixel dark outline along
its top, which gives the height of the ground in any column. The player, the slimes and the
mystery boxes are found by colours only they have.

The player runs right. He jumps when a pit, a step up or a slime is just ahead, and also under
a mystery box. Near the end of the level he turns and runs back.

python mario_bot.py <frames folder> [seconds]
"""
import sys
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 30
TILE, ROWS = 54, 14
OUTLINE = (67, 74, 95)
PLAYER = [(52, 101, 71), (90, 210, 140)]
SLIME = [(44, 197, 246), (20, 144, 195)]
BOX = [(244, 180, 27)]


def code(colour):
    return (colour[0] << 16) | (colour[1] << 8) | colour[2]


def box_of(px, colours, least=40):
    ys, xs = np.nonzero(np.isin(px, [code(c) for c in colours]))
    return (xs.min(), ys.min(), xs.max(), ys.max()) if len(ys) >= least else None


def ground_row(px, x):
    """The row of the highest ground in the column at x, or None over a pit."""
    if not 0 <= x < px.shape[1]:
        return None
    for row in range(3, ROWS):
        y = row * TILE
        if y + 4 < px.shape[0] and px[y + 1, x] == code(OUTLINE) and px[y + 4, x] == code(OUTLINE):
            return row
    return None


game = Game('06-super-mario-bros', 'Mario8')
game.tap('enter', 0.1)
direction, unseen_since, last_jump = 1, 0.0, -1.0
seen = [None, 0.0]                                 # what the bot last saw, and since when


def bot(img, t):
    global direction, unseen_since, last_jump
    rgb = np.asarray(img).astype(np.uint32)
    px = (rgb[:, :, 0] << 16) | (rgb[:, :, 1] << 8) | rgb[:, :, 2]
    player = box_of(px, PLAYER)
    if player is None:
        game.hold()
        if t - unseen_since > 1.0:                   # fell into a pit: start again
            game.tap('enter', 0.1)
            unseen_since = t
            direction = 1
        return
    unseen_since = t
    left, top, right, bottom = player
    game.hold('right' if direction > 0 else 'left')

    front = right if direction > 0 else left
    under = ground_row(px, (left + right) // 2)
    on_ground = under is not None and abs(under * TILE - (bottom + 3)) <= 6

    # Turn around at a wall of the level: the player stops moving on screen and in the world.
    if on_ground and (front > px.shape[1] - 40 or front < 40):
        direction = -direction
        return
    if not on_ground or t - last_jump < 0.25:
        return

    # A jump carries the player about 180 pixels. Is there ground where he would come down?
    lands = all(ground_row(px, front + direction * reach) is not None for reach in (150, 180, 210))

    jump = False
    if ground_row(px, front + direction * 12) is None:
        jump = True                                  # the edge of a pit: now or never
    else:
        step = ground_row(px, front + direction * 34)
        if step is not None and step < under:
            jump = True                              # a step up
        slime = np.isin(px[top - 20:bottom + 6], [code(c) for c in SLIME])
        gaps = (np.nonzero(slime)[1] - front) * direction
        if lands and np.any((gaps > 0) & (gaps < 80)):
            jump = True                              # a slime in the way
        box = np.isin(px[max(0, top - 200):top], [code(c) for c in BOX])
        gaps = (np.nonzero(box)[1] - (left + right) // 2) * direction
        if lands and np.any((gaps > 60) & (gaps < 100)):
            jump = True                              # a mystery box overhead

    # Not getting anywhere (a mystery box can block the way off a pillar): jump over it, and if
    # that doesn't help either, go the other way.
    view = (int(left), tuple(ground_row(px, x) for x in range(0, px.shape[1], 64)))
    if view != seen[0]:
        seen[0], seen[1] = view, t
    elif t - seen[1] > 1.6:
        direction = -direction
        seen[1] = t
    elif t - seen[1] > 0.35:
        jump = True
    if jump:
        game.tap('space', 0.04)
        last_jump = t


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
