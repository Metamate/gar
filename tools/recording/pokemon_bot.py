"""Plays Pokemon for a recording: walks from the town into the tall grass, walks about there
until a wild monster appears, and fights it.

Nothing is read from the screen. A step takes half a second, and the map is known, so the walk
is a list of keys and times: five tiles right along the path, one down into the grass, and then
back and forth through the grass. Enter is pressed every 0.7 seconds the whole time: it does
nothing while walking, and in a battle it picks Fight and moves the messages on. The walk in
the grass only goes left and right, because up and down would move the battle menu to Run.

python pokemon_bot.py <frames folder> [seconds]
"""
import sys
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 70
STEP = 0.5                                           # seconds a tile


def walk():
    """(key, seconds) in order: the key is held for that long."""
    yield None, 4.2                                  # the title fades, the welcome message is read
    yield 'right', 5 * STEP - 0.15
    yield 'down', STEP - 0.15
    while True:
        yield 'right', 5 * STEP - 0.15
        yield None, 0.3
        yield 'left', 5 * STEP - 0.15
        yield None, 0.3


game = Game('10-pokemon', 'Pokemon4')
game.tap('enter')
steps = walk()
until, next_enter = 0.0, 3.2


def bot(img, t):
    global until, next_enter
    if t >= until:
        key, seconds = next(steps)
        game.hold(*([key] if key else []))
        until = t + seconds
    if t >= next_enter:
        game.tap('enter', 0.04)
        next_enter = t + 0.7


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
