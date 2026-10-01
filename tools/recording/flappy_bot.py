"""Plays Flappy Bird for a recording: reads the screen, finds the bird and every pipe's gap, and
checks each flap by flying on in its head.

The window is twice the 640 x 360 game. The bird is the only yellow (248, 184, 0) on screen and
the pipes the only green (0, 184, 0). Consecutive pipes leave almost no room between them, so
the bird has to leave one gap already inside the next. The bot's rule is simple: flap when the
bird, falling, nears the bottom of the gap. It knows the game's numbers (gravity, the flap, the
pipes' speed), so before each choice it flies on in its head with that rule, once with a flap
now and once without, and takes the choice that survives.

python flappy_bot.py <frames folder> [seconds]
"""
import sys, time
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 40
BIRD, PIPE = (248, 184, 0), (0, 184, 0)
SOLID = [(0, 184, 0), (0, 0, 0), (0, 120, 0), (184, 248, 24)]
GROUND = 688                                        # where the ground starts, in window pixels
BIRD_W, BIRD_H, PIPE_W = 96, 64, 140
GRAVITY, FLAP, PIPE_SPEED = 1960.0, -600.0, 120.0   # window pixels and seconds
STEP = 1 / 60
MARGIN = 5                                          # keep this far from everything


def read(px):
    """The bird's top-left corner, and the pipes as (left edge, gap top, gap bottom)."""
    ys, xs = np.nonzero(np.all(px[:GROUND, :420] == BIRD, axis=2))
    if len(ys) == 0:
        return None, []
    bird = (xs.min() - 8, ys.min() - 8)              # the yellow starts 4 art pixels inside the sprite

    green = np.all(px[:GROUND] == PIPE, axis=2).sum(axis=0) > 60
    columns = np.nonzero(green)[0]
    pipes = []
    if len(columns):
        breaks = np.nonzero(np.diff(columns) > 30)[0]
        for group in np.split(columns, breaks + 1):
            # Read the gap in a column the bird doesn't cover.
            usable = group[(group < bird[0] - 4) | (group > bird[0] + BIRD_W + 4)]
            if len(usable) == 0:
                continue
            column = px[:GROUND, usable[len(usable) // 2]]
            solid = np.zeros(GROUND, bool)
            for c in SOLID:
                solid |= np.all(column == c, axis=1)
            clear = np.nonzero(~solid)[0]
            runs = np.split(clear, np.nonzero(np.diff(clear) > 1)[0] + 1)
            gap = max(runs, key=len)
            # The green body starts 18 pixels inside the sprite. A pipe that is partly off the
            # left edge has lost its first columns, so measure from its right end there.
            left = group[0] - 18 if group[0] > 20 else group[-1] + 36 - PIPE_W
            pipes.append((float(left), float(gap[0]), float(gap[-1] + 1)))
    return bird, pipes


def band(pipes, bird_x):
    """The heights the bird should stay between: the gap of the pipe it is in or coming to. Near
    the end of that pipe, the next pipe's gap counts too, since there is no room between them."""
    ahead = [p for p in pipes if p[0] + PIPE_W > bird_x]
    if not ahead:
        return 200.0, 460.0
    top, bottom = ahead[0][1], ahead[0][2]
    if len(ahead) > 1 and ahead[0][0] + PIPE_W - bird_x < 150:
        top, bottom = max(top, ahead[1][1]), min(bottom, ahead[1][2])
    return top, bottom


def rollout(y, vy, pipes, bird_x, first_flap, horizon=110):
    """Fly on in the bot's head. The first flap comes at step first_flap (None: not in the next
    few steps); after that the bird follows the simple rule, flapping when it falls near the
    bottom of its band. Returns how many steps it survives."""
    pipes = [list(p) for p in pipes]
    wait = 0
    for step in range(horizon):
        _, bottom = band(pipes, bird_x)
        if step == first_flap or (step > (first_flap if first_flap is not None else LOOK) and wait <= 0
                                  and vy > 0 and y + BIRD_H > bottom - 24):
            vy = FLAP
            wait = 8
        wait -= 1
        vy += GRAVITY * STEP
        y += vy * STEP
        if y < MARGIN or y + BIRD_H > GROUND - MARGIN:
            return step
        for p in pipes:
            p[0] -= PIPE_SPEED * STEP
            if bird_x + BIRD_W > p[0] - MARGIN and bird_x < p[0] + PIPE_W + MARGIN:
                if y < p[1] + MARGIN or y + BIRD_H > p[2] - MARGIN:
                    return step
    return horizon


LOOK = 5                                            # the bot looks again after about this many steps


def plan(y, vy, pipes, bird_x):
    """When to flap: None for not before the bot looks again, or the number of steps to wait.
    Not flapping is best, then flapping as late as possible, as long as the bird survives."""
    options = [None] + list(range(LOOK, -1, -1))
    lived = [rollout(y, vy, pipes, bird_x, option) for option in options]
    return options[lived.index(max(lived))]


game = Game('02-flappy-bird', 'Flappy12')
game.tap('enter')
last = None                                         # (time, y) of the bird in the previous frame
vy, last_flap, unseen_since = 0.0, -1.0, 0.0


def bot(img, t):
    global last, vy, last_flap, unseen_since
    seen = time.time()
    bird, pipes = read(np.asarray(img))
    if bird is None:
        last = None
        if t - unseen_since > 1.5:                  # the score screen: start again
            game.tap('enter')
            unseen_since = t
        return
    unseen_since = t
    if t - last_flap < 1.0:
        vy = FLAP + GRAVITY * (t - last_flap)       # since the last flap, the speed is known
    elif last and t > last[0]:
        vy = (bird[1] - last[1]) / (t - last[0])
    last = (t, bird[1])
    if t - last_flap < 0.13:
        return
    # What the bot sees is a moment old, and a key press takes another moment: plan from where
    # the bird will be then.
    y, speed = float(bird[1]), vy
    for _ in range(LATENCY):
        speed += GRAVITY * STEP
        y += speed * STEP
    pipes = [(left - PIPE_SPEED * STEP * LATENCY, top, bottom) for left, top, bottom in pipes]
    wait = plan(y, speed, pipes, float(bird[0]))
    if wait is not None:
        pause = wait * STEP - (time.time() - seen)
        if pause > 0:
            time.sleep(pause)
        game.tap('space', 0.03)
        last_flap = t + wait * STEP + LATENCY * STEP


LATENCY = 3                                         # steps between what the bot sees and its flap


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
