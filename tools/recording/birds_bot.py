"""Plays Angry Birds for a recording: pulls the slingshot back, aims, and shoots three birds at
the pigs' hut.

The bot knows the slingshot's numbers (the bird leaves at ten times the pull, and falls at 500
pixels per second squared), so it works out the pull that sends the bird through a point, the
way the game's own row of dots shows it. It drags the mouse there in small steps, holds for a
moment, and lets go.

python birds_bot.py <frames folder>
"""
import math, sys
from botlib import Game

OUT = sys.argv[1]
ANCHOR, PULL, SCALE, GRAVITY = (220, 520), 85, 10, 500
TARGETS = [(960, 455), (930, 600), (975, 520)]       # the pig on top, the one inside, the hut's wall


def pull_for(target):
    """The pull that sends the bird through target on its flatter path."""
    speed = PULL * SCALE
    dx, dy = target[0] - ANCHOR[0], target[1] - ANCHOR[1]
    best = None
    for tenth in range(20, 700):
        angle = math.radians(tenth / 10)
        seconds = dx / (speed * math.cos(angle))
        y = -speed * math.sin(angle) * seconds + GRAVITY * seconds * seconds / 2
        if best is None or abs(y - dy) < best[0]:
            best = (abs(y - dy), angle)
        elif abs(y - dy) > best[0] and best[0] < 4:
            break
    angle = best[1]
    return -PULL * math.cos(angle), PULL * math.sin(angle)


def script():
    game.tap('enter')
    yield 1.2
    for target in TARGETS:
        px, py = pull_for(target)
        game.move(*ANCHOR)
        yield 0.3
        game.mouse_down()
        yield 0.15
        for k in range(1, 13):                       # pull back, a little at a time
            game.move(ANCHOR[0] + px * k / 12, ANCHOR[1] + py * k / 12 - (12 - k) * 2)
            yield 0.06
        game.move(ANCHOR[0] + px, ANCHOR[1] + py)
        yield 0.7                                    # hold: the dots show where it will go
        game.mouse_up()
        yield 0.2                                    # the game reads the pull on the frame of the release
        game.move(640, 690)                          # the pointer out of the picture
        yield 4.4                                    # the bird flies, and the hut settles
    yield 1.0


game = Game('08-angry-birds', 'Birds4')
steps, wake = script(), 0.0
finished = False


def bot(img, t):
    global wake, finished
    if t >= wake and not finished:
        try:
            wake = t + next(steps)
        except StopIteration:
            finished = True
    return not finished


frames = game.run(bot, 40, OUT, start=1.0)
game.close()
print('captured', frames, 'frames')
