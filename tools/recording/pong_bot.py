"""Plays Pong for a recording: two players who watch the ball, move to where it is going, and
sometimes get there late.

The window is four times the 320 x 180 court. The ball is the only white 4 x 4 block that stands
alone (the score's digits are made of blocks that touch), and each paddle is in its outer columns.
A paddle only moves while the ball comes towards it, to the place the ball will cross its line
(bounces off the top and bottom included), and stops when it is close enough. Between rallies
it drifts back to the middle.

python pong_bot.py <frames folder> [seconds]
"""
import random, sys
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 24
SCALE, WIDTH, HEIGHT, BALL = 4, 320, 180, 4
LINES = (12, 308)                                    # where the ball meets the left and right paddle
KEYS = (('w', 's'), ('up', 'down'))
CLOSE = 4                                            # a paddle within this of its target stays put


def read(img):
    """The ball's middle and the two paddles' middles, in court pixels (None where not found)."""
    white = np.all(np.asarray(img.convert('RGB'))[::SCALE, ::SCALE] > 200, axis=2)
    paddles = []
    for cols in (slice(0, 12), slice(308, 320)):
        ys = np.nonzero(white[:, cols].any(axis=1))[0]
        paddles.append(ys.mean() if len(ys) else None)
    field = white.copy()
    field[:, :12] = False
    field[:, 308:] = False
    ys, xs = np.nonzero(field)
    for y, x in zip(ys, xs):
        block = field[y:y + BALL, x:x + BALL]
        if block.shape == (BALL, BALL) and block.all() and field[max(0, y - 1):y + BALL + 1, max(0, x - 1):x + BALL + 1].sum() == BALL * BALL:
            return (x + BALL / 2, y + BALL / 2), paddles
    return None, paddles


def crossing(ball, velocity, line):
    """The height at which the ball reaches a paddle's line, with its bounces."""
    seconds = (line - ball[0]) / velocity[0]
    y = ball[1] + velocity[1] * seconds
    low, high = BALL / 2, HEIGHT - BALL / 2
    span = high - low
    y = (y - low) % (2 * span)
    return low + (y if y <= span else 2 * span - y)


game = Game('01-pong', 'Pong11')
game.tap('enter')
last, last_t, velocity, still_since = None, 0.0, (0.0, 0.0), 0.0
aim = [0.0, 0.0]            # where on the paddle each player tries to take the ball, off its middle
late = [0.0, 0.0]           # how far past the middle the ball has to be before each player reacts
receiver = None


def bot(img, t):
    global last, last_t, velocity, still_since, receiver
    ball, paddles = read(img)
    if ball and last and t > last_t:
        moved = (ball[0] - last[0], ball[1] - last[1])
        if abs(moved[0]) + abs(moved[1]) > 0.5:
            velocity = (moved[0] / (t - last_t), moved[1] / (t - last_t))
            still_since = t
    if ball:
        last, last_t = ball, t

    # The ball has stood still for a moment: it's waiting for the serve.
    if t - still_since > 0.9:
        game.tap('enter')
        still_since = t
        velocity = (0.0, 0.0)

    towards = 0 if velocity[0] < 0 else 1
    if ball and abs(velocity[0]) > 20 and towards != receiver:
        # A new player has to take the ball: pick where on the paddle, and how late to react.
        receiver = towards
        aim[towards] = random.uniform(-7, 7)
        late[towards] = random.choice([0, 0, 40, 80, 140, 200])

    for side in (0, 1):
        up, down = KEYS[side]
        paddle = paddles[side]
        target = HEIGHT / 2
        if ball and abs(velocity[0]) > 20 and side == towards:
            past_middle = (WIDTH / 2 - ball[0]) if side == 0 else (ball[0] - WIDTH / 2)
            if past_middle >= late[side] - WIDTH / 2:
                target = crossing(ball, velocity, LINES[side]) + aim[side]
        if paddle is None or abs(paddle - target) <= CLOSE:
            game.hold(*[k for k in game._held if k not in (up, down)])
        elif paddle > target:
            game.up(down); game.down(up)
        else:
            game.up(up); game.down(down)


frames = game.run(bot, SECONDS, OUT, start=1.0)
game.close()
print('captured', frames, 'frames')
