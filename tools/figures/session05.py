"""Figures for 05 Pac-Man."""
from figlib import *

WALLS = '#2f6f8f'
RED, PINK, CYAN, ORANGE, YELLOW = '#e5484d', '#f4a6c8', '#4cc9d8', '#f0a04b', '#f2d24b'


def maze(f, ox, oy, rows, size, dots=False):
    """Draws a small maze from text: # is a wall."""
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            x, y = ox + c * size, oy + r * size
            if ch == '#':
                f.rect(x + 1, y + 1, size - 2, size - 2, 'none', WALLS, 1.5, 3)
            elif dots:
                f.circle(x + size / 2, y + size / 2, 1.6, FAINT)


def centre(ox, oy, size, c, r):
    return ox + c * size + size / 2, oy + r * size + size / 2


def ghost(f, x, y, color, r=10):
    f.path(f'M{x - r:g} {y + r:g} L{x - r:g} {y:g} A{r:g} {r:g} 0 0 1 {x + r:g} {y:g} L{x + r:g} {y + r:g} '
           f'L{x + r / 2:g} {y + r * 0.55:g} L{x:g} {y + r:g} L{x - r / 2:g} {y + r * 0.55:g} Z', color, 0, color)
    f.circle(x - r * 0.35, y - r * 0.1, r * 0.22, '#ffffff')
    f.circle(x + r * 0.35, y - r * 0.1, r * 0.22, '#ffffff')


def pacman(f, x, y, r=10, facing=0):
    """Facing 0 is right, 1 is down, 2 is left, 3 is up."""
    f.add(f'<g transform="rotate({facing * 90} {x:g} {y:g})"><path d="M{x:g} {y:g} L{x + r * 0.82:g} {y - r * 0.57:g} '
          f'A{r:g} {r:g} 0 1 0 {x + r * 0.82:g} {y + r * 0.57:g} Z" fill="{YELLOW}"/></g>')


def junction():
    f = Fig(720, 360, 'At a tile centre a ghost takes the open direction whose next tile is closest to its target')
    rows = ['#########',
            '#       #',
            '# ## ## #',
            '#       #',
            '# ## ## #',
            '#       #',
            '#########']
    size, ox, oy = 40, 30, 40
    maze(f, ox, oy, rows, size, dots=True)
    gx, gy = centre(ox, oy, size, 4, 3)
    tx, ty = centre(ox, oy, size, 7, 1)
    f.rect(tx - 16, ty - 16, 32, 32, 'none', ACCENT, 2, 4, dash='4 3')
    f.text(tx, ty - 24, 'target', 13, ACCENT, 'middle')
    options = [((4, 2), 'up', 3.2, True), ((5, 3), 'right', 2.8, False), ((4, 4), 'down', 4.2, False)]
    best = min(options, key=lambda o: o[2])
    for (c, r), name, dist, _ in options:
        x, y = centre(ox, oy, size, c, r)
        chosen = (c, r) == best[0]
        f.line(x, y, tx, ty, ACCENT if chosen else FAINT, 2 if chosen else 1.5, None if chosen else '4 4')
        f.circle(x, y, 5, ACCENT if chosen else MUTED)
    bx, by = centre(ox, oy, size, 3, 3)
    f.line(bx - 8, by - 8, bx + 8, by + 8, MUTED, 2.5)
    f.line(bx - 8, by + 8, bx + 8, by - 8, MUTED, 2.5)
    ghost(f, gx, gy, RED, 13)
    f.text(ox + 1.5 * size, by + 26, 'no turning back', 11.5, MUTED, 'middle')
    x = 430
    f.text(x, 70, 'The ghost is at a tile centre.', 15, TEXT, weight='bold')
    f.label(x, 104, ['It never turns back, so three', 'directions are open.'], 14, MUTED)
    f.label(x, 164, ['For each, it measures the straight', 'line from the next tile to the target.'], 14, MUTED)
    f.text(x, 228, 'right is closest, so it goes right', 14.5, ACCENT, weight='bold')
    f.label(x, 266, ['The state decides the target.', 'This rule only gets the ghost there.'], 14, MUTED)
    return f


def targets():
    f = Fig(720, 400, 'Each ghost aims at a different tile while chasing')
    size, cols, rows = 26, 12, 9

    def panel(ox, oy, name, strategy, color, draw):
        f.text(ox, oy - 26, name, 15, color, weight='bold')
        f.text(ox + 62, oy - 26, strategy, 13, MUTED, mono=True)
        f.rect(ox, oy, cols * size, 110, SCREEN, r=4)
        for c in range(cols):
            for r in range(4):
                f.circle(ox + c * size + size / 2, oy + r * size + size / 2 + 3, 1.4, FAINT)
        draw(ox, oy + 3)

    def cell(ox, oy, c, r):
        return ox + c * size + size / 2, oy + r * size + size / 2

    def mark(ox, oy, c, r, color):
        x, y = cell(ox, oy, c, r)
        f.rect(x - 11, y - 11, 22, 22, 'none', color, 2, 3, dash='4 3')
        return x, y

    def blinky(ox, oy):
        px, py = cell(ox, oy, 6, 2); pacman(f, px, py, 10)
        gx, gy = cell(ox, oy, 1, 2); ghost(f, gx, gy, RED)
        mark(ox, oy, 6, 2, RED)
        f.arrow(gx + 14, gy, px - 16, py, RED, 1.5)
        f.text(ox, oy + 126, "Pac-Man's own tile", 13, MUTED)

    def pinky(ox, oy):
        px, py = cell(ox, oy, 4, 2); pacman(f, px, py, 10)
        gx, gy = cell(ox, oy, 1, 0); ghost(f, gx, gy, PINK)
        tx, ty = mark(ox, oy, 8, 2, PINK)
        f.arrow(px + 14, py, tx - 14, ty, PINK, 1.5, '4 3')
        f.text(ox, oy + 126, 'four tiles ahead of him, to cut him off', 13, MUTED)

    def inky(ox, oy):
        px, py = cell(ox, oy, 4, 2); pacman(f, px, py, 10)
        bx, by = cell(ox, oy, 2, 3); ghost(f, bx, by, RED, 8)
        vx, vy = cell(ox, oy, 6, 2)
        f.circle(vx, vy, 3.5, CYAN)
        tx, ty = mark(ox, oy, 10, 1, CYAN)
        f.line(bx, by, vx, vy, CYAN, 1.5, '4 3')
        f.arrow(vx, vy, tx - 12, ty + 3, CYAN, 1.5)
        gx, gy = cell(ox, oy, 11, 3); ghost(f, gx, gy, CYAN)
        f.text(ox, oy + 126, 'the line from Blinky to two tiles ahead, doubled', 13, MUTED)

    def clyde(ox, oy):
        px, py = cell(ox, oy, 7, 1); pacman(f, px, py, 10)
        f.circle(px, py, 44, 'none', ORANGE, 1.5, )
        f.text(px + 50, py - 30, '8 tiles', 12, ORANGE)
        gx, gy = cell(ox, oy, 2, 3); ghost(f, gx, gy, ORANGE)
        f.arrow(gx + 12, gy - 6, px - 52, py + 22, ORANGE, 1.5)
        f.text(ox, oy + 126, 'chases, but heads for his corner within 8 tiles', 13, MUTED)

    panel(30, 64, 'Blinky', 'ChasePacMan', RED, blinky)
    panel(378, 64, 'Pinky', 'AmbushAhead', PINK, pinky)
    panel(30, 256, 'Inky', 'FlankWithBlinky', CYAN, inky)
    panel(378, 256, 'Clyde', 'ChaseUntilClose', ORANGE, clyde)
    return f


def schedule():
    f = Fig(720, 220, 'Scatter and chase take turns on a fixed schedule, and frightened pauses it')
    x0, y = 40, 70
    phases = [('scatter', 7), ('chase', 20), ('scatter', 7), ('chase', 20), ('scatter', 5), ('chase', 20)]
    total = sum(p[1] for p in phases)
    x = x0
    for name, sec in phases:
        w = sec / total * 640
        f.rect(x + 1, y, w - 2, 40, '#24424a' if name == 'scatter' else '#4a2c22', TEAL if name == 'scatter' else ACCENT, 1.5, 5)
        f.text(x + w / 2, y + 25, f'{name} {sec} s' if w > 70 else str(sec), 13, TEXT, 'middle')
        x += w
    f.text(x0, 50, 'ModeSchedule', 15, TEXT, mono=True)
    f.text(x0 + 130, 50, 'every ghost that is scattering or chasing follows it', 13, MUTED)
    f.text(x0, 148, 'scatter:', 14, TEAL, weight='bold')
    f.text(x0 + 66, 148, 'each ghost heads for its own corner, and the player gets room to breathe', 14, MUTED)
    f.text(x0, 174, 'chase:', 14, ACCENT, weight='bold')
    f.text(x0 + 66, 174, 'each ghost aims at its target', 14, MUTED)
    f.text(x0, 200, 'While any ghost is frightened, the clock stands still.', 14, MUTED)
    return f


def routing():
    f = Fig(720, 420, 'The arcade rule takes the turn that looks closest; the shortest path takes the turn that is')
    rows = ['#############',
            '#  T        #',
            '# ### # ### #',
            '#   G       #',
            '#############']
    size, ox = 36, 30
    for oy, title, sub, path, color in (
        (40, 'NearestTile', ['left looks closer in a', 'straight line: 7 steps'], [(4, 3), (1, 3), (1, 1), (3, 1)], MUTED),
        (236, 'ShortestPath', ['the search knows the', 'walls: 5 steps'], [(4, 3), (5, 3), (5, 1), (3, 1)], TEAL),
    ):
        maze(f, ox, oy, rows, size, dots=True)
        tx, ty = centre(ox, oy, size, 3, 1)
        f.rect(tx - 14, ty - 14, 28, 28, 'none', ACCENT, 2, 4, dash='4 3')
        f.text(tx, ty + 5, 'T', 13, ACCENT, 'middle', 'bold')
        pts = [centre(ox, oy, size, c, r) for c, r in path]
        f.curve('M' + ' L'.join(f'{x:g} {y:g}' for x, y in pts), color, 3)
        gx, gy = centre(ox, oy, size, 4, 3)
        ghost(f, gx, gy, RED, 11)
        f.text(ox + 13 * size + 20, oy + 70, title, 15, TEXT, weight='bold', mono=True)
        f.label(ox + 13 * size + 20, oy + 96, sub, 13.5, color if color != MUTED else MUTED)
    f.text(30, 26, 'the ghost G wants to reach T, two rows up', 13.5, MUTED)
    return f


FIGURES = {
    'junction': junction,
    'targets': targets,
    'schedule': schedule,
    'routing': routing,
}
