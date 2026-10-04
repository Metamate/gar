"""Figures for 01 Pong."""
from figlib import *


def coordinates():
    f = Fig(720, 410, 'The screen has its origin in the top-left corner, with y pointing down')
    x0, y0, w, h = 150, 70, 480, 270
    f.rect(x0, y0, w, h, SCREEN, FAINT, 1.5)
    # the axes
    f.arrow(x0, y0, x0 + w + 46, y0, ACCENT, 3)
    f.arrow(x0, y0, x0, y0 + h + 30, ACCENT, 3)
    f.text(x0 + w + 54, y0 + 6, 'x', 20, ACCENT, weight='bold', italic=True)
    f.text(x0, y0 + h + 58, 'y', 20, ACCENT, 'middle', 'bold', italic=True)
    f.circle(x0, y0, 5, ACCENT)
    f.text(x0 - 12, y0 - 14, '(0, 0)', 16, TEXT, 'end', mono=True)
    f.text(x0 + w, y0 - 14, '(320, 0)', 16, MUTED, 'middle', mono=True)
    f.text(x0 - 12, y0 + h + 5, '(0, 180)', 16, MUTED, 'end', mono=True)
    f.text(x0 + w, y0 + h + 24, '(320, 180)', 16, MUTED, 'middle', mono=True)
    # a paddle, placed by its top-left corner
    px, py = x0 + 60, y0 + 120
    f.rect(px, py, 14, 60, TEXT)
    f.line(x0, py, px, py, MUTED, 1.5, '5 5')
    f.line(px, y0, px, py, MUTED, 1.5, '5 5')
    f.circle(px, py, 4, TEAL)
    f.text(px + 26, py + 6, 'the paddle is at (40, 80):', 15, TEXT)
    f.text(px + 26, py + 28, 'its top-left corner', 15, MUTED)
    f.text(px - 30, y0 + 22, '40', 14, MUTED, 'middle', mono=True)
    f.text(x0 + 22, py - 8, '80', 14, MUTED, 'middle', mono=True)
    # the ball, to show that down is plus
    f.rect(x0 + 300, y0 + 60, 12, 12, TEXT)
    f.arrow(x0 + 322, y0 + 76, x0 + 358, y0 + 124, TEAL, 2.5)
    f.text(x0 + 368, y0 + 118, 'moving down:', 15, TEXT)
    f.text(x0 + 368, y0 + 140, 'y grows', 15, MUTED)
    return f


def virtual_resolution():
    f = Fig(720, 360, 'The game is drawn at 320 by 180 and scaled to whatever size the window has')

    def game(x, y, s):
        f.rect(x, y, 320 * s, 180 * s, '#282d34')
        f.rect(x + 10 * s, y + 60 * s, 5 * s, 20 * s, TEXT)
        f.rect(x + 305 * s, y + 100 * s, 5 * s, 20 * s, TEXT)
        f.rect(x + 158 * s, y + 88 * s, 4 * s, 4 * s, TEXT)
        f.line(x + 160 * s, y + 6 * s, x + 160 * s, y + 174 * s, FAINT, 1.5, '4 6')

    # the game as it is drawn
    game(30, 110, 0.5)
    f.text(110, 96, 'the game: 320 × 180', 15, TEXT, 'middle', 'bold')
    f.label(110, 224, ['the game logic only', 'ever sees this size'], 14, MUTED, 'middle')
    f.arrow(204, 155, 250, 120, MUTED)
    f.arrow(204, 155, 250, 240, MUTED)
    # a wide window: bars at the sides
    wx, wy, ww, wh = 262, 40, 300, 120
    f.rect(wx, wy, ww, wh, '#000000', FAINT, 1.5)
    s = wh / 180
    game(wx + (ww - 320 * s) / 2, wy, s)
    f.text(wx + ww + 14, wy + 44, 'a wide window:', 15, TEXT)
    f.text(wx + ww + 14, wy + 66, 'bars at the sides', 15, MUTED)
    # a tall window: bars above and below
    tx, ty, tw, th = 262, 185, 200, 160
    f.rect(tx, ty, tw, th, '#000000', FAINT, 1.5)
    s = tw / 320
    game(tx, ty + (th - 180 * s) / 2, s)
    f.text(tx + tw + 14, ty + 62, 'a tall window:', 15, TEXT)
    f.text(tx + tw + 14, ty + 84, 'bars above and below', 15, MUTED)
    f.text(tx + tw + 14, ty + 122, 'scale = the smaller of', 14, MUTED)
    f.text(tx + tw + 14, ty + 142, 'width / 320, height / 180', 14, MUTED, mono=True)
    return f


def delta_time():
    f = Fig(720, 344, 'Multiplying by delta time gives the same distance per second at any frame rate')
    x0, x1 = 210, 630
    rows = [
        (78, '30 FPS', 'speed × deltaTime', 4, 1.0, TEAL),
        (158, '120 FPS', 'speed × deltaTime', 16, 1.0, TEAL),
        (258, '120 FPS', 'a fixed step per frame', 16, 0.0, ACCENT),
    ]
    f.text(x0, 34, 'one second of movement, at 200 pixels per second', 15, MUTED)
    f.line(x1, 48, x1, 190, FAINT, 1.5, '4 5')
    f.text(x1, 208, '200 px', 14, MUTED, 'middle', mono=True)
    for y, fps, how, steps, scale, color in rows:
        f.text(30, y - 4, fps, 17, TEXT, weight='bold')
        f.text(30, y + 16, how, 13, MUTED)
        f.line(x0, y, 700, y, FAINT, 1.5)
        if scale:                                   # the frames share the distance between them
            step = (x1 - x0) / steps
            n = steps
        else:                                       # the same step as at 30 FPS, taken four times as often
            step = (x1 - x0) / 4
            n = 5
        for i in range(n):
            a, b = x0 + i * step, x0 + (i + 1) * step
            if b > 702:
                break
            f.path(f'M{a:g} {y:g} Q{(a + b) / 2:g} {y - min(30, step * 0.45):g} {b:g} {y:g}', color, 2)
            f.circle(b, y, 3, color)
        f.rect(x0 - 5, y - 9, 10, 18, TEXT)
    f.text(x0, 300, 'four times the frames, four times the distance:', 14, ACCENT)
    f.text(x0, 320, 'the game runs faster on a faster computer', 14, ACCENT)
    return f


def timestep():
    f = Fig(720, 340, 'A variable timestep updates once per frame; a fixed timestep updates in equal steps')
    x0 = 220
    frames = [0, 52, 104, 232, 284, 338, 466]          # frame boundaries: two of the frames are long
    f.text(x0, 34, 'rendered frames, two of them long (the window was dragged)', 15, MUTED)
    y = 62
    for a, b in zip(frames, frames[1:]):
        long = b - a > 100
        f.rect(x0 + a + 2, y, b - a - 4, 26, '#3a3024' if long else PANEL, ACCENT if long else None, 1.5, 4)
        f.text(x0 + (a + b) / 2, y + 18, 'frame', 12, TEXT if long else MUTED, 'middle')
    # variable
    y = 150
    f.text(30, y - 2, 'Variable', 17, TEXT, weight='bold')
    f.text(30, y + 18, 'one update per frame', 13, MUTED)
    f.line(x0, y, x0 + 466, y, FAINT, 1.5)
    for b in frames[1:-1]:
        f.line(x0 + b, 92, x0 + b, 262, FAINT, 1, '3 5')
    for a, b in zip(frames, frames[1:]):
        long = b - a > 100
        c = ACCENT if long else TEAL
        f.path(f'M{x0 + a:g} {y} Q{x0 + (a + b) / 2:g} {y - (44 if long else 22):g} {x0 + b:g} {y}', c, 2)
        f.circle(x0 + b, y, 3.5, c)
    f.circle(x0, y, 3.5, TEAL)
    f.note(x0 + 233, y + 30, 'one big step: a fast ball can pass through a thin wall', 13, ACCENT)
    # fixed
    y = 250
    f.text(30, y - 2, 'Fixed', 17, TEXT, weight='bold')
    f.text(30, y + 18, 'equal steps', 13, MUTED)
    f.line(x0, y, x0 + 466, y, FAINT, 1.5)
    step = 466 / 13
    t = 0
    while t + step <= 467:
        f.path(f'M{x0 + t:g} {y} Q{x0 + t + step / 2:g} {y - 18} {x0 + t + step:g} {y}', TEAL, 2)
        f.circle(x0 + t + step, y, 3.5, TEAL)
        t += step
    f.circle(x0, y, 3.5, TEAL)
    f.note(x0 + 233, y + 30, 'a long frame runs several steps to catch up', 13, TEAL)
    f.text(30, 322, 'Every fixed step is the same size, so the simulation behaves the same on every computer.', 14, MUTED)
    return f


def aabb():
    f = Fig(720, 360, 'Two rectangles overlap only if they overlap on both axes')

    def case(ox, title, color, bx, by, verdict):
        f.text(ox + 150, 36, title, 16, TEXT, 'middle', 'bold')
        ax, ay, aw, ah = ox + 50, 90, 110, 90
        bw, bh = 110, 90
        f.rect(ax, ay, aw, ah, 'none', TEAL, 2.5)
        f.text(ax + 10, ay + 22, 'a', 16, TEAL, weight='bold', italic=True)
        f.rect(bx, by, bw, bh, 'none', ACCENT, 2.5)
        f.text(bx + bw - 18, by + bh - 10, 'b', 16, ACCENT, weight='bold', italic=True)
        # the overlap itself
        ix0, iy0 = max(ax, bx), max(ay, by)
        ix1, iy1 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
        if ix1 > ix0 and iy1 > iy0:
            f.rect(ix0, iy0, ix1 - ix0, iy1 - iy0, TEXT, opacity=0.25)
        # the shadows on the two axes
        xa, ya = 292, ox + 22
        f.line(ox + 30, xa, ox + 290, xa, FAINT, 1.5)
        f.line(ya, 60, ya, 270, FAINT, 1.5)
        f.line(ax, xa - 5, ax + aw, xa - 5, TEAL, 4)
        f.line(bx, xa + 5, bx + bw, xa + 5, ACCENT, 4)
        f.line(ya - 5, ay, ya - 5, ay + ah, TEAL, 4)
        f.line(ya + 5, by, ya + 5, by + bh, ACCENT, 4)
        x_over, y_over = ix1 > ix0, iy1 > iy0
        f.text(ox + 160, xa + 30, 'x: ' + ('overlap' if x_over else 'apart'), 14, TEXT if x_over else MUTED, 'middle')
        f.text(ya + 16, 262, 'y: ' + ('overlap' if y_over else 'apart'), 14, TEXT if y_over else MUTED)
        f.text(ox + 160, 346, verdict, 15, color, 'middle', 'bold')

    case(20, 'A hit', GREEN, 20 + 120, 140, 'overlap on both axes: a collision')
    case(370, 'A miss', MUTED, 370 + 120, 186, 'overlap on x only: no collision')
    f.line(360, 20, 360, 340, FAINT, 1)
    return f


def bounce():
    f = Fig(720, 340, 'Where the ball hits the paddle sets the angle it leaves at')
    px, py, pw, ph = 120, 60, 22, 220
    f.rect(px, py, pw, ph, TEXT)
    f.line(px - 24, py + ph / 2, px + pw + 4, py + ph / 2, FAINT, 1.5, '4 5')
    f.text(px - 30, py + ph / 2 + 5, 'middle', 13, MUTED, 'end')
    f.text(px + pw / 2, py - 14, 'paddle', 14, MUTED, 'middle')
    hits = [(-0.85, 'near the top: steeply up'), (-0.4, ''), (0.0, 'the middle: straight back'), (0.4, ''), (0.85, 'near the bottom: steeply down')]
    for off, note in hits:
        y = py + ph / 2 + off * ph / 2
        strong = note != ''
        c = ACCENT if strong else MUTED
        f.rect(px + pw + 2, y - 6, 12, 12, TEXT if strong else FAINT)
        dx, dy = 200, off * 70
        f.arrow(px + pw + 20, y, px + pw + 20 + dx, y + dy, c, 2.5 if strong else 1.5)
        if note:
            f.text(px + pw + 34 + dx, y + dy + 5, note, 15, TEXT)
    f.label(396, 226, ['offset = ballCentre − paddleCentre', 'velocity.Y = offset / halfHeight × 110'], 14, MUTED, mono=True)
    return f


FIGURES = {
    'coordinates': coordinates,
    'virtual-resolution': virtual_resolution,
    'delta-time': delta_time,
    'timestep': timestep,
    'aabb': aabb,
    'bounce': bounce,
}
