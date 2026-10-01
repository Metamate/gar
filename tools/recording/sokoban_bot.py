"""Plays Sokoban for a recording: solves the first three levels, with an undo and a redo on the way.

The bot reads the levels from the game's own text files and finds the shortest solution of each
with a breadth-first search over (player, boxes). It then presses the keys at a steady pace.

python sokoban_bot.py <frames folder>
"""
import os, sys
from collections import deque
from botlib import Game, GAMES

OUT = sys.argv[1]
PACE = 0.26                                          # seconds between moves
MOVES = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}


def solve(number):
    rows = open(os.path.join(GAMES, '04-sokoban', 'Content', 'Assets', 'levels', f'level{number}.txt')).read().splitlines()
    walls, goals, boxes, player = set(), set(), set(), None
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == '#':
                walls.add((x, y))
            if ch in '.*+':
                goals.add((x, y))
            if ch in '$*':
                boxes.add((x, y))
            if ch in '@+':
                player = (x, y)
    start = (player, frozenset(boxes))
    seen, todo = {start}, deque([(start, [])])
    while todo:
        (player, boxes), path = todo.popleft()
        if boxes == goals:
            return path
        for key, (dx, dy) in MOVES.items():
            to = (player[0] + dx, player[1] + dy)
            if to in walls:
                continue
            moved = boxes
            if to in boxes:
                beyond = (to[0] + dx, to[1] + dy)
                if beyond in walls or beyond in boxes:
                    continue
                moved = (boxes - {to}) | {beyond}
            state = (to, moved)
            if state not in seen:
                seen.add(state)
                todo.append((state, path + [key]))
    raise ValueError('no solution')


# What to press, and when.
script, t = [(0.2, 'enter')], 1.2
for level in (1, 2, 3):
    moves = solve(level)
    if level == 2:                                   # two moves, take one back, and do it again
        moves = moves[:2] + ['z', 'y'] + moves[2:]
    for key in moves:
        script.append((t, key))
        t += PACE * (2 if key in 'zy' else 1)
    t += 0.9
    script.append((t, 'enter'))                      # on to the next level
    t += 0.8
END = t

game = Game('04-sokoban', 'Sokoban4')
done = 0


def bot(img, seconds):
    global done
    while done < len(script) and script[done][0] <= seconds:
        game.tap(script[done][1], 0.04)
        done += 1


frames = game.run(bot, END, OUT, start=1.0)
game.close()
print('captured', frames, 'frames')
