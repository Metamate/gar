"""Figures for 12 Vampire Survivors."""
import math, random
from figlib import *

BAT = '#b98ad6'


def pairs():
    f = Fig(720, 320, 'Checking every pair: twice the enemies is four times the checks')
    for k, (n, ox) in enumerate(((4, 110), (8, 360), (16, 610))):
        pts = [(ox + 70 * math.cos(2 * math.pi * i / n - math.pi / 2), 140 + 70 * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                f.line(*pts[a], *pts[b], ACCENT, 0.9 if n > 8 else 1.2)
        for x, y in pts:
            f.circle(x, y, 6, BAT)
        f.text(ox, 246, f'{n} enemies', 15, TEXT, 'middle', 'bold')
        f.text(ox, 268, f'{n * (n - 1) // 2} pairs', 14, ACCENT, 'middle', mono=True)
    f.arrow(196, 140, 266, 140, MUTED, 2); f.text(231, 128, '× 2', 13, MUTED, 'middle')
    f.arrow(446, 140, 516, 140, MUTED, 2); f.text(481, 128, '× 2', 13, MUTED, 'middle')
    f.text(360, 302, 'n enemies make n × (n − 1) / 2 pairs. At 10,000 enemies that is 50 million checks, every step.', 13.5, MUTED, 'middle')
    return f


def grid():
    f = Fig(720, 350, 'With a grid, an enemy is only checked against the enemies in its own cell and the cells around it')
    random.seed(7)
    ox, oy, cell, cols, rows = 40, 50, 46, 9, 5
    pts = [(ox + random.random() * cols * cell, oy + random.random() * rows * cell) for _ in range(60)]
    cx, cy = 4, 2
    for r in range(rows):
        for c in range(cols):
            near = abs(c - cx) <= 1 and abs(r - cy) <= 1
            f.rect(ox + c * cell, oy + r * cell, cell, cell, '#243a3c' if near else SCREEN, FAINT, 1)
    f.rect(ox + cx * cell, oy + cy * cell, cell, cell, 'none', ACCENT, 2.5)
    for x, y in pts:
        c, r = int((x - ox) // cell), int((y - oy) // cell)
        near = abs(c - cx) <= 1 and abs(r - cy) <= 1
        f.circle(x, y, 5, BAT if near else '#5a4a66')
    ex, ey = ox + cx * cell + 22, oy + cy * cell + 24
    f.circle(ex, ey, 7, ACCENT)
    x = 480
    f.text(x, 70, 'one enemy', 15, ACCENT, weight='bold')
    f.label(x, 94, ['only looks at its own cell', 'and the eight around it'], 13.5, MUTED)
    f.rect(x, 146, 16, 16, '#243a3c', FAINT, 1)
    f.text(x + 26, 159, 'checked: a handful', 13.5, TEXT)
    f.rect(x, 176, 16, 16, SCREEN, FAINT, 1)
    f.text(x + 26, 189, 'never looked at', 13.5, MUTED)
    f.label(x, 232, ['The grid is rebuilt every step,', 'after the enemies have moved.'], 13.5, MUTED)
    f.text(360, 326, 'The work now grows in step with the number of enemies, because each one has few neighbours.', 13.5, MUTED, 'middle')
    return f


def memory_layout():
    f = Fig(720, 380, 'A list of objects is scattered over the heap; a struct of arrays keeps each field packed together')
    # objects on the heap
    f.text(40, 40, 'List<Enemy>: references to objects', 15, TEXT, weight='bold')
    f.rect(40, 56, 640, 100, SCREEN, r=6)
    f.text(52, 76, 'the heap', 12, MUTED)
    spots = [(70, 96), (330, 84), (180, 120), (520, 104), (420, 124), (610, 86)]
    for a, b in zip(spots, spots[1:]):
        f.curve(f'M{a[0] + 28} {a[1] + 22} Q{(a[0] + b[0]) / 2 + 28} {max(a[1], b[1]) + 44}, {b[0] + 28} {b[1] + 22}', ACCENT, 1.2, '3 4')
    for i, (x, y) in enumerate(spots):
        f.rect(x, y, 56, 22, PANEL, ACCENT, 1.5, 4)
        f.text(x + 28, y + 16, 'Enemy', 11.5, TEXT, 'middle', mono=True)
    f.text(360, 176, 'a loop over the positions jumps from object to object: one cache miss after another', 13, ACCENT, 'middle')
    # arrays
    f.text(40, 214, 'Enemies: one array per field', 15, TEXT, weight='bold')
    for r, name in enumerate(('Position', 'Speed', 'Health')):
        y = 232 + r * 34
        f.text(40, y + 18, name, 12.5, MUTED, mono=True)
        for c in range(14):
            hot = r < 2
            f.rect(130 + c * 38, y, 34, 24, '#24424a' if hot else PANEL, TEAL if hot else None, 1.5, 3)
    f.rect(126, 228, 38 * 4 + 4, 32, 'none', TEXT, 1.5, 4, dash='5 4')
    f.text(130 + 38 * 4 + 16, 222, 'one read brings in the neighbours too (a cache line)', 12.5, TEXT)
    f.text(360, 356, 'Move only reads positions and speeds, so those two arrays are all it touches.', 13.5, MUTED, 'middle')
    return f


def counting_sort():
    f = Fig(720, 320, 'The flat grid is built with a counting sort: count each cell, find where it starts, then copy')
    cells = ['A', 'B', 'C', 'D']
    items = ['B', 'D', 'A', 'B', 'C', 'B', 'D', 'A']
    colors = {'A': TEAL, 'B': ACCENT, 'C': GREEN, 'D': '#b98ad6'}
    f.text(30, 56, 'the enemies, in any order', 13.5, MUTED)
    for i, c in enumerate(items):
        f.rect(230 + i * 48, 36, 42, 30, PANEL, colors[c], 1.5, 5)
        f.text(251 + i * 48, 56, c, 13, TEXT, 'middle', mono=True)
    f.text(30, 120, '1. count each cell', 13.5, TEXT, weight='bold')
    counts = [items.count(c) for c in cells]
    starts = [sum(counts[:i]) for i in range(4)]
    for i, c in enumerate(cells):
        f.rect(230 + i * 96, 100, 90, 30, SCREEN, colors[c], 1.5, 5)
        f.text(275 + i * 96, 120, f'{c}: {counts[i]}', 13, TEXT, 'middle', mono=True)
    f.text(30, 180, '2. where each cell starts', 13.5, TEXT, weight='bold')
    for i, c in enumerate(cells):
        f.rect(230 + i * 96, 160, 90, 30, SCREEN, colors[c], 1.5, 5)
        f.text(275 + i * 96, 180, f'{c} at {starts[i]}', 13, TEXT, 'middle', mono=True)
    f.text(30, 240, '3. copy each enemy', 13.5, TEXT, weight='bold')
    f.text(30, 258, 'into its cell\'s range', 13.5, TEXT, weight='bold')
    ordered = sorted(items)
    for i, c in enumerate(ordered):
        f.rect(230 + i * 48, 222, 42, 30, '#243038', colors[c], 1.5, 5)
        f.text(251 + i * 48, 242, c, 13, TEXT, 'middle', mono=True)
        f.text(251 + i * 48, 270, str(i), 11, MUTED, 'middle', mono=True)
    f.text(360, 302, 'Each cell\'s enemies now sit next to each other in memory, and nothing was allocated.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'pairs': pairs,
    'grid': grid,
    'memory-layout': memory_layout,
    'counting-sort': counting_sort,
}
