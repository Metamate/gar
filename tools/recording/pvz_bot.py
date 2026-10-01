"""Plays Plants vs. Zombies for a recording: plants sunflowers, picks up the sun, and puts a
peashooter in every row a zombie walks in.

The lawn is nine columns of 100 pixels and five rows of 112, from (260, 148). The seed packets
are along the top: sunflower at x = 182, peashooter at x = 274. The bot finds things by colours
only they have: the sun's orange, the zombies' grey-green, and the plants' own greens and yellows
to see whether a cell is taken. Planting can fail (not enough sun yet, or the packet is still
recharging), so the bot looks at the cell afterwards and tries again later if it is still empty.

python pvz_bot.py <frames folder> [seconds]
"""
import sys
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 80
LAWN_X, LAWN_Y, CELL_W, CELL_H = 260, 148, 100, 112
PACKET = {'sunflower': (182, 70), 'peashooter': (274, 70)}
SUN, ZOMBIE = (228, 92, 16), (104, 136, 92)
PLANT = {'sunflower': (172, 124, 0), 'peashooter': (0, 120, 0)}
REST = (1180, 690)                                   # where the pointer waits


def code(colour):
    return (colour[0] << 16) | (colour[1] << 8) | colour[2]


def cell_box(cell):
    x, y = LAWN_X + cell[0] * CELL_W, LAWN_Y + cell[1] * CELL_H
    return slice(y, y + CELL_H), slice(x, x + CELL_W)


def cell_middle(cell):
    return LAWN_X + cell[0] * CELL_W + CELL_W // 2, LAWN_Y + cell[1] * CELL_H + CELL_H // 2 + 10


# What to plant, in order. Peashooters for rows with zombies are put in front of this.
queue = [('sunflower', (0, 2)), ('sunflower', (0, 1)), ('sunflower', (0, 3)), ('sunflower', (0, 0)), ('sunflower', (0, 4)),
         ('peashooter', (1, 2)), ('peashooter', (1, 1)), ('peashooter', (1, 3))]
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
        if np.count_nonzero(px[cell_box(cell)] == code(PLANT[plant])) > 200 and pending in queue:
            queue.remove(pending)
        pending = None

    # A row with a zombie and no peashooter comes first.
    for row in range(5):
        y = LAWN_Y + row * CELL_H
        if row not in defended and np.count_nonzero(px[y:y + CELL_H, LAWN_X:] == code(ZOMBIE)) > 300:
            defended.add(row)
            column = 2 if ('peashooter', (1, row)) in queue else 1
            if ('peashooter', (1, row)) in queue:
                queue.remove(('peashooter', (1, row)))
                column = 1
            queue.insert(0, ('peashooter', (column, row)))

    # Sun on screen: pick it up. (The counter's own sun, top left, doesn't count.)
    sun = px == code(SUN)
    sun[:140, :160] = False
    ys, xs = np.nonzero(sun)
    if len(ys) > 150:
        # Take the pixels of one sun: those near the first one found.
        near = (abs(xs - xs[0]) < 70) & (abs(ys - ys[0]) < 70)
        game.click(int(xs[near].mean()), int(ys[near].mean()) + 14)   # it is still falling
        game.move(*REST)
        wake = t + 0.5
        return

    if queue:
        plant, cell = queue[0]
        game.click(*PACKET[plant])
        game.click(*cell_middle(cell))
        game.move(*REST)
        pending = (plant, cell)
        wake = t + 0.9


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
