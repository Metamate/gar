"""Plays Plants vs. Zombies for a recording: places chests, picks up the gold, and puts an archer
in every row a goblin walks in.

The field is fourteen columns and five rows of 80-pixel cells, from (80, 160). The cards are
along the top: the chest at x = 180, the archer at x = 270. The bot finds things by colour: the
goblins' green, the coins' gold (with a dark outline around it, which the flowers in the grass don't
have; the autumn trees are below the field), and a colour of each unit to see whether a cell is taken. Placing can fail (not enough
gold yet, or the card is still recharging), so the bot looks at the cell afterwards and tries
again later if it is still empty.

python pvz_bot.py <frames folder> [seconds]
"""
import sys
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 80
LAWN_X, LAWN_Y, CELL_W, CELL_H = 80, 160, 80, 80
PACKET = {'chest': (180, 80), 'archer': (270, 80)}
SUN, ZOMBIE = (253, 190, 83), (140, 200, 96)         # the coins' gold, the goblins' green
PLANT = {'chest': (192, 203, 220), 'archer': (225, 154, 101)}
INK = (63, 38, 49)                                   # the outline every sprite has, and no flower
REST = (1180, 690)                                   # where the pointer waits


def code(colour):
    return (colour[0] << 16) | (colour[1] << 8) | colour[2]


def cell_box(cell):
    x, y = LAWN_X + cell[0] * CELL_W, LAWN_Y + cell[1] * CELL_H
    return slice(y, y + CELL_H), slice(x, x + CELL_W)


def cell_middle(cell):
    return LAWN_X + cell[0] * CELL_W + CELL_W // 2, LAWN_Y + cell[1] * CELL_H + CELL_H // 2


# What to place, in order. Archers for rows with goblins are put in front of this.
queue = [('chest', (0, 2)), ('chest', (0, 1)), ('chest', (0, 3)), ('chest', (0, 0)), ('chest', (0, 4))]
queue += [('archer', (1, row)) for row in (2, 1, 3, 0, 4)] + [('archer', (2, row)) for row in (2, 1, 3, 0, 4)]
defended = set()

game = Game('09-plants-vs-zombies', 'Pvz4')
game.tap('enter')
game.move(*REST)
wake, pending = 1.0, None                            # pending: the plant the bot just tried


def bot(img, t):
    global wake, pending
    if t < wake:
        return
    rgb = np.asarray(img).astype(np.uint32)
    px = (rgb[:, :, 0] << 16) | (rgb[:, :, 1] << 8) | rgb[:, :, 2]

    if pending:                                      # did the last plant take?
        plant, cell = pending
        if np.count_nonzero(px[cell_box(cell)] == code(PLANT[plant])) > 150 and pending in queue:
            queue.remove(pending)
        pending = None

    # A row with a goblin and no archer yet comes first.
    for row in range(5):
        y = LAWN_Y + row * CELL_H
        if row not in defended and np.count_nonzero(px[y:y + CELL_H, LAWN_X:] == code(ZOMBIE)) > 300:
            defended.add(row)
            if ('archer', (1, row)) in queue:
                queue.remove(('archer', (1, row)))
                queue.insert(0, ('archer', (1, row)))

    # A coin on the field: pick it up. A coin is a patch of gold with a dark outline; the flowers in
    # the grass are the same gold, without one.
    ys, xs = np.nonzero(px[LAWN_Y - 60:LAWN_Y + 5 * CELL_H] == code(SUN))      # not the trees below the field
    ys = ys + LAWN_Y - 60
    while len(ys):
        near = (abs(xs - xs[0]) < 60) & (abs(ys - ys[0]) < 70)
        x, y = xs[near].mean(), ys[near].mean()
        box = px[int(y) - 33:int(y) + 33, int(x) - 28:int(x) + 28]
        if ((abs(xs - x) < 28) & (abs(ys - y) < 33)).sum() > 600 and np.count_nonzero(box == code(INK)) > 600:
            game.click(int(x), int(y))
            game.move(*REST)
            wake = t + 0.45
            return
        xs, ys = xs[~near], ys[~near]

    if queue:
        plant, cell = queue[0]
        game.click(*PACKET[plant])
        game.click(*cell_middle(cell))
        game.move(*REST)
        pending = (plant, cell)
        wake = t + 0.8


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
