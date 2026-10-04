"""Figures for 03 Snake."""
import math
from figlib import *

ATLAS = GAMES + '03-snake/Content/Assets/images/atlas.png'
LIT = '#78e65a'


def atlas():
    f = Fig(720, 360, 'A texture atlas is one image; a region is a named rectangle inside it')
    s = 6                                                    # one atlas pixel is six figure pixels
    x0, y0 = 40, 60
    f.rect(x0 - 6, y0 - 6, 64 * s + 12, 40 * s + 12, SCREEN)
    f.image(ATLAS, x0, y0, 64 * s, 40 * s)
    f.text(x0 - 6, 40, 'atlas.png: one texture, loaded once', 15, TEXT, weight='bold')
    regions = [('body', 0, 0, 7, 7, MUTED), ('head-1', 8, 0, 7, 7, ACCENT), ('food-1', 24, 0, 7, 7, TEAL)]
    for name, x, y, w, h, c in regions:
        f.rect(x0 + x * s, y0 + y * s, w * s, h * s, 'none', c, 2.5)
    tx = 470
    f.text(tx, 78, 'atlas-definition.xml', 14, MUTED)
    f.label(tx, 106, ['head-1', 'x 8, y 0, 7 × 7'], 14, ACCENT, mono=True)
    f.label(tx, 166, ['food-1', 'x 24, y 0, 7 × 7'], 14, TEAL, mono=True)
    f.curve(f'M{tx - 8} 102 C {tx - 60} 102, {x0 + 15 * s + 40} 30, {x0 + 11.5 * s} {y0 - 4}', ACCENT, 1.5)
    f.curve(f'M{tx - 8} 162 C {tx - 60} 162, {x0 + 31 * s + 30} 150, {x0 + 31 * s + 4} {y0 + 5 * s}', TEAL, 1.5)
    f.text(tx, 236, 'the code asks by name:', 14, MUTED)
    f.text(tx, 260, 'GetRegion("head-1")', 13.5, TEXT, mono=True)
    f.text(360, 340, 'Every sprite comes from the same texture, so they can all go to the graphics card in one batch.', 13.5, MUTED, 'middle')
    return f


def animation():
    f = Fig(720, 270, 'An animation is a list of regions and a delay; a frame can repeat')
    x0, y = 60, 96
    names = ['head-1'] * 5 + ['head-2']
    crop = {'head-1': (8, 0, 15, 7), 'head-2': (16, 0, 23, 7)}
    f.text(x0, 34, 'head-animation, delay 250 ms', 15, TEXT, mono=True)
    f.text(x0 + 300, 34, 'eyes open for five frames, shut for one: a blink', 13, MUTED)
    for i, n in enumerate(names):
        x = x0 + i * 100
        blink = n == 'head-2'
        f.rect(x, y, 70, 70, SCREEN, ACCENT if blink else FAINT, 2 if blink else 1.5, 4)
        f.image(ATLAS, x + 7, y + 7, 56, 56, crop=crop[n])
        f.text(x + 35, y + 92, n, 13, ACCENT if blink else MUTED, 'middle', mono=True)
        if i < 5:
            f.arrow(x + 74, y + 35, x + 96, y + 35, MUTED, 1.5)
    f.curve(f'M{x0 + 535} {y - 6} C {x0 + 500} {y - 46}, {x0 + 70} {y - 46}, {x0 + 35} {y - 6}', MUTED, 1.5, '4 4')
    f.note(x0 + 285, y - 30, 'and around again', 13, MUTED)
    f.line(x0, 226, x0 + 570, 226, FAINT, 1.5)
    for i in range(7):
        f.line(x0 + i * 95, 220, x0 + i * 95, 232, MUTED, 1.5)
        f.text(x0 + i * 95, 250, f'{i * 250} ms', 12, MUTED, 'middle', mono=True)
    return f


def tilemap():
    f = Fig(720, 350, 'A tilemap is a grid of tile numbers; each number picks a tile from the tileset')
    # the tileset: nine tiles, numbered
    s = 5
    tx, ty = 40, 86
    f.text(tx, 40, 'the tileset', 15, TEXT, weight='bold')
    f.text(tx, 62, 'nine tiles, numbered 0 to 8', 13, MUTED)
    f.rect(tx - 4, ty - 4, 24 * s + 8, 24 * s + 8, SCREEN)
    f.image(ATLAS, tx, ty, 24 * s, 24 * s, crop=(0, 16, 24, 40))
    for i in range(9):
        cx, cy = tx + (i % 3) * 8 * s, ty + (i // 3) * 8 * s
        f.rect(cx, cy, 8 * s, 8 * s, 'none', ACCENT, 1)
        f.text(cx + 4, cy + 13, str(i), 12, ACCENT, mono=True)
    # the numbers
    gx, gy = 220, 86
    f.text(gx, 40, 'the tilemap', 15, TEXT, weight='bold')
    f.text(gx, 62, 'one number per cell, row after row', 13, MUTED)
    rows = ['0 1 1 1 1 2', '3 4 4 4 4 5', '3 4 4 4 4 5', '6 7 7 7 7 8']
    for r, row in enumerate(rows):
        for c, n in enumerate(row.split()):
            hot = (r, c) == (1, 4)
            f.text(gx + c * 30 + 10, gy + r * 30 + 20, n, 16, ACCENT if hot else TEXT, 'middle', mono=True, weight='bold' if hot else 'normal')
    f.rect(gx + 4 * 30 - 4, gy + 30 + 1, 28, 28, 'none', ACCENT, 1.5, 4)
    f.label(gx, gy + 150, ['column 4, row 1', 'index = 1 × 6 + 4 = 10'], 13.5, ACCENT, mono=True)
    # the room they make
    rx, ry = 450, 86
    f.text(rx, 40, 'the room', 15, TEXT, weight='bold')
    f.text(rx, 62, 'each cell draws its tile', 13, MUTED)
    cell = 38
    f.rect(rx - 4, ry - 4, 6 * cell + 8, 4 * cell + 8, SCREEN)
    for r, row in enumerate(rows):
        for c, n in enumerate(row.split()):
            n = int(n)
            f.image(ATLAS, rx + c * cell, ry + r * cell, cell, cell, crop=((n % 3) * 8, 16 + (n // 3) * 8, (n % 3) * 8 + 8, 24 + (n // 3) * 8))
    f.rect(rx + 4 * cell, ry + cell, cell, cell, 'none', ACCENT, 2)
    f.arrow(182, 150, 210, 150, MUTED, 2)
    f.arrow(408, 150, 438, 150, MUTED, 2)
    f.text(360, 326, 'To change the room, change the numbers. The code stays the same.', 14, MUTED, 'middle')
    return f


def tick():
    f = Fig(720, 340, 'The accumulator collects frame time, and the snake moves once per full tick')
    x0, w = 150, 520
    frames = [0, 45, 105, 150, 250, 290, 345, 410, 450, 520]
    tick_len = 100
    # frames
    f.text(30, 62, 'frames', 15, TEXT, weight='bold')
    f.text(30, 82, 'uneven', 13, MUTED)
    for a, b in zip(frames, frames[1:]):
        f.rect(x0 + a + 1.5, 46, b - a - 3, 26, PANEL, r=4)
    # the accumulator as a sawtooth
    f.text(30, 158, 'accumulator', 15, TEXT, weight='bold')
    f.text(30, 178, '_elapsed', 13, MUTED, mono=True)
    base, top = 200, 120
    f.line(x0, base, x0 + w, base, FAINT, 1.5)
    f.line(x0, top, x0 + w, top, ACCENT, 1.5, '5 5')
    f.text(x0 + w + 6, top + 5, 'tick', 12, ACCENT)
    acc = 0.0
    d = f'M{x0} {base}'
    moves = []
    for a, b in zip(frames, frames[1:]):
        acc += b - a
        d += f' L{x0 + b:g} {base - acc / tick_len * (base - top):g}'
        while acc >= tick_len:
            acc -= tick_len
            moves.append(b)
            d += f' L{x0 + b:g} {base - acc / tick_len * (base - top):g}'
    f.path(d, TEAL, 2.5)
    # the moves
    f.text(30, 262, 'the snake', 15, TEXT, weight='bold')
    f.text(30, 282, 'one cell per tick', 13, MUTED)
    f.line(x0, 262, x0 + w, 262, FAINT, 1.5)
    for i, m in enumerate(moves):
        f.line(x0 + m, 84, x0 + m, 252, FAINT, 1, '3 5')
        f.rect(x0 + m - 9, 253, 18, 18, LIT, r=2)
        f.text(x0 + m, 294, 'Move()', 12, MUTED, 'middle', mono=True)
    f.text(x0, 324, 'Subtracting the tick keeps what is left over, so the ticks stay evenly spaced.', 13.5, MUTED)
    return f


def buffering():
    f = Fig(720, 330, 'Two key presses between ticks: without a buffer the first is lost, with one both are used')
    x0 = 190
    ticks = [0, 200, 400]
    f.text(x0, 36, 'the snake moves right; the player presses Up, then Left, before the next tick', 14, MUTED)

    def row(y, title, sub, results, color):
        f.text(30, y - 4, title, 16, TEXT, weight='bold')
        f.text(30, y + 16, sub, 13, MUTED)
        f.line(x0, y, x0 + 460, y, FAINT, 1.5)
        for t in ticks:
            f.line(x0 + t, y - 12, x0 + t, y + 12, MUTED, 2)
            f.text(x0 + t, y + 30, 'tick', 12, MUTED, 'middle')
        f.chip(x0 + 60, y - 50, 44, 'Up', PANEL, TEXT)
        f.line(x0 + 82, y - 24, x0 + 82, y - 4, MUTED, 1.5)
        f.chip(x0 + 120, y - 50, 52, 'Left', PANEL, TEXT)
        f.line(x0 + 146, y - 24, x0 + 146, y - 4, MUTED, 1.5)
        for t, text in results:
            f.text(x0 + t + 10, y - 16, text, 14, color, weight='bold')

    row(124, 'Snake6', 'one wanted direction', [(200, 'turns Left: into its own neck')], ACCENT)
    f.line(x0 + 60, 86, x0 + 104, 86, ACCENT, 2)
    f.text(x0 + 112, 66, 'overwritten', 12, ACCENT)
    row(248, 'Snake7', 'a queue of turns', [(200, 'turns Up'), (400, 'Left')], TEAL)
    f.text(30, 308, 'A new turn is checked against the last one queued, so two quick presses can never reverse the snake.', 13, MUTED)
    return f


def circles():
    f = Fig(720, 300, 'Two circles overlap when the distance between their centres is less than the sum of their radii')

    def case(ox, title, d, color, verdict):
        f.text(ox + 170, 36, title, 16, TEXT, 'middle', 'bold')
        ax, ay, ar, br = ox + 110, 150, 60, 44
        bx = ax + d
        f.circle(ax, ay, ar, 'none', TEAL, 2.5)
        f.circle(bx, ay, br, 'none', ACCENT, 2.5)
        f.line(ax, ay, bx, ay, TEXT, 2)
        f.circle(ax, ay, 3.5, TEAL)
        f.circle(bx, ay, 3.5, ACCENT)
        f.text((ax + bx) / 2, ay - 76, 'distance', 13, TEXT, 'middle')
        f.line((ax + bx) / 2, ay - 70, (ax + bx) / 2, ay - 4, FAINT, 1, '3 3')
        f.line(ax, ay, ax - ar * 0.7, ay + ar * 0.71, TEAL, 1.5, '4 4')
        f.text(ax - 6, ay + 34, 'r₁', 14, TEAL, 'middle')
        f.line(bx, ay, bx + br * 0.7, ay + br * 0.71, ACCENT, 1.5, '4 4')
        f.text(bx + 2, ay + 30, 'r₂', 14, ACCENT, 'middle')
        f.text(ox + 170, 256, verdict, 15, color, 'middle', 'bold')

    case(10, 'A hit', 80, GREEN, 'distance < r₁ + r₂')
    case(370, 'A miss', 130, MUTED, 'distance > r₁ + r₂')
    f.line(360, 20, 360, 270, FAINT, 1)
    f.text(360, 288, 'Compare the squared values, and no square root is needed.', 13.5, MUTED, 'middle')
    return f


def response():
    f = Fig(720, 320, 'Collision response is what happens after a hit: block, trigger or bounce')
    def panel(ox, title, sub):
        f.rect(ox, 50, 210, 170, SCREEN, r=6)
        f.text(ox + 105, 250, title, 16, TEXT, 'middle', 'bold')
        f.label(ox + 105, 274, sub, 13, MUTED, 'middle')
    panel(30, 'Blocking', ['the two are kept from', 'overlapping'])
    f.rect(170, 70, 40, 130, PANEL, FAINT, 1.5)
    f.rect(140, 118, 44, 44, 'none', ACCENT, 1.5, dash='4 3')
    f.rect(126, 118, 44, 44, 'none', TEAL, 2.5)
    f.arrow(160, 104, 132, 104, TEAL, 2)
    f.text(60, 108, 'pushed back', 12, TEAL)
    panel(255, 'Triggering', ['something happens, such as', 'the snake eating and growing'])
    f.rect(300, 122, 40, 40, LIT, r=3)
    f.rect(344, 122, 40, 40, LIT, r=3)
    f.circle(408, 142, 14, 'none', ACCENT, 2.5)
    f.text(408, 106, '+1', 16, ACCENT, 'middle', 'bold', mono=True)
    panel(480, 'Bouncing', ['the velocity is reflected', 'off the surface'])
    f.line(500, 190, 670, 190, MUTED, 3)
    f.arrow(524, 84, 580, 182, TEAL, 2.5)
    f.arrow(590, 182, 646, 84, ACCENT, 2.5)
    f.line(585, 188, 585, 100, MUTED, 1.5, '4 4')
    f.text(585, 90, 'normal', 12, MUTED, 'middle')
    return f


def phases():
    f = Fig(720, 320, 'A broad phase cheaply finds the pairs that are near each other; a narrow phase runs the exact check on those only')
    def shapes(ox, boxes, hot):
        f.rect(ox, 50, 320, 190, SCREEN, r=6)
        pts = [(ox + 70, 112), (ox + 124, 150), (ox + 230, 96), (ox + 266, 192), (ox + 60, 200)]
        for i, (x, y) in enumerate(pts):
            pair = i in (0, 1)
            if boxes:
                f.rect(x - 34, y - 34, 68, 68, 'none', ACCENT if pair else FAINT, 1.5, dash=None if pair else '4 4')
            color = TEAL if (not hot or pair) else FAINT
            if i % 2 == 0:
                f.add(f'<rect x="{x - 22}" y="{y - 22}" width="44" height="44" fill="none" stroke="{color}" stroke-width="2.5" transform="rotate(25 {x} {y})"/>')
            else:
                f.circle(x, y, 24, 'none', color, 2.5)
    f.text(180, 36, '1. Broad phase', 16, TEXT, 'middle', 'bold')
    shapes(20, True, False)
    f.label(180, 268, ['a rough box around each shape,', 'and only one pair of boxes overlaps'], 13.5, MUTED, 'middle')
    f.arrow(346, 145, 374, 145, MUTED, 2)
    f.text(540, 36, '2. Narrow phase', 16, TEXT, 'middle', 'bold')
    shapes(380, False, True)
    f.label(540, 268, ['the exact, slower check,', 'for that one pair'], 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'atlas': atlas,
    'animation': animation,
    'tilemap': tilemap,
    'tick': tick,
    'buffering': buffering,
    'circles': circles,
    'response': response,
    'phases': phases,
}
