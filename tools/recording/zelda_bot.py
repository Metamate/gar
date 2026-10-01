"""Plays The Legend of Zelda for a recording: fights the monsters in a room with the sword, steps
on the switch, and walks through the door to the next room.

The window is four times the 320 x 180 game. Every character has the same dark brown outline,
which the floor doesn't have, so the bot finds characters as clumps of that colour inside the
room. The hero is the clump with both his headband's green and his hair's brown in it, and the switch is the only bright red.

The hero walks up to the nearest monster until it is in line with him and a sword's length
away, turns to it, and swings. With one monster left (or after a while) he goes to the switch,
and then out through the door on the right.

python zelda_bot.py <frames folder> [seconds]
"""
import sys
import numpy as np
from botlib import Game

OUT = sys.argv[1]
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 45
ROOM = (128, 136, 1152, 584)                         # the floor inside the walls, in window pixels
OUTLINE, BUTTON = (63, 38, 49), (232, 69, 55)
HEADBAND, HAIR = (37, 149, 106), (189, 108, 74)      # the hero has both; the slime only the green, the rat only the brown
DOOR_Y = 360                                         # the middle of the door on the right


def code(colour):
    return (colour[0] << 16) | (colour[1] << 8) | colour[2]


def read(img):
    rgb = np.asarray(img.crop(ROOM))[::2, ::2].astype(np.uint32)
    px = (rgb[:, :, 0] << 16) | (rgb[:, :, 1] << 8) | rgb[:, :, 2]
    ys, xs = np.nonzero(px == code(OUTLINE))
    band_y, band_x = np.nonzero(px == code(HEADBAND))
    hair_y, hair_x = np.nonzero(px == code(HAIR))
    hero, monsters = None, []
    left = np.ones(len(ys), bool)
    while left.any():
        i = np.argmax(left)
        near = left & (np.abs(xs - xs[i]) < 34) & (ys - ys[i] < 34)
        if near.sum() > 25:
            x, y = xs[near].mean(), ys[near].mean()
            is_hero = (np.any((np.abs(band_x - x) < 16) & (np.abs(band_y - y) < 16))
                       and np.any((np.abs(hair_x - x) < 16) & (np.abs(hair_y - y) < 16)))
            point = (ROOM[0] + x * 2, ROOM[1] + y * 2)
            if is_hero and hero is None:
                hero = point
            else:
                monsters.append(point)
        left &= ~near
    by, bx = np.nonzero(px == code(BUTTON))
    switch = (ROOM[0] + bx.mean() * 2, ROOM[1] + by.mean() * 2) if len(by) > 6 else None
    return hero, monsters, switch


def towards(hero, target, slack=10):
    """The key that brings the hero closer to target, the longer way first."""
    dx, dy = target[0] - hero[0], target[1] - hero[1]
    if abs(dx) <= slack and abs(dy) <= slack:
        return None
    if abs(dx) >= abs(dy):
        return 'right' if dx > 0 else 'left'
    return 'down' if dy > 0 else 'up'


game = Game('07-the-legend-of-zelda', 'Zelda7')
game.tap('enter')
room_since, last_swing, last_hero = 0.0, -1.0, None


def bot(img, t):
    global room_since, last_swing, last_hero
    hero, monsters, switch = read(img)
    if hero is None:                                 # the room is scrolling, or the game is over
        game.hold()
        if last_hero is not None:
            room_since = t
        last_hero = None
        if t - room_since > 4:
            game.tap('enter')
            room_since = t
        return
    last_hero = hero

    key = None
    fight = len(monsters) > 1 and t - room_since < 14
    if fight:
        monster = min(monsters, key=lambda m: abs(m[0] - hero[0]) + abs(m[1] - hero[1]))
        dx, dy = monster[0] - hero[0], monster[1] - hero[1]
        if abs(dy) <= 26 and 40 <= abs(dx) <= 104:   # in line, and in reach: face it and swing
            key = 'right' if dx > 0 else 'left'
            if t - last_swing > 0.45:
                game.hold(key)
                game.tap('space', 0.04)
                last_swing = t
        elif abs(dx) <= 26 and 40 <= abs(dy) <= 104:
            key = 'down' if dy > 0 else 'up'
            if t - last_swing > 0.45:
                game.hold(key)
                game.tap('space', 0.04)
                last_swing = t
        elif abs(dx) < 40 and abs(dy) < 40:          # too close: step back
            key = 'left' if dx > 0 else 'right'
        elif abs(dy) > 26 and (abs(dy) <= abs(dx) or abs(dx) <= 26):
            key = 'down' if dy > 0 else 'up'         # get in line first
        else:
            key = 'right' if dx > 0 else 'left'
    elif switch is not None:
        key = towards(hero, switch)
    else:                                            # the doors are open: out to the right
        if abs(hero[1] - DOOR_Y) > 14:
            key = 'down' if hero[1] < DOOR_Y else 'up'
        else:
            key = 'right'
    game.hold(*([key] if key else []))


frames = game.run(bot, SECONDS, OUT)
game.close()
print('captured', frames, 'frames')
