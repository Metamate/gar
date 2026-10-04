"""Figures for 02 Flappy Bird."""
from figlib import *

ART = GAMES + '02-flappy-bird/Content/Assets/images/'


def coupling():
    f = Fig(720, 320, 'Tightly coupled code depends on everything; decoupled code depends on little')

    def modules(ox, title, sub, links, color):
        f.text(ox + 160, 34, title, 17, TEXT, 'middle', 'bold')
        f.text(ox + 160, 56, sub, 14, MUTED, 'middle')
        pos = [(ox + 40, 90), (ox + 200, 90), (ox + 40, 180), (ox + 200, 180), (ox + 120, 250)]
        names = ['Game1', 'Bird', 'Pipes', 'Audio', 'Score']
        centre = [(x + 42, y + 18) for x, y in pos]
        for a, b in links:
            f.line(*centre[a], *centre[b], color, 2)
        for (x, y), n in zip(pos, names):
            f.rect(x, y, 84, 36, PANEL, FAINT, 1.5, 6)
            f.text(x + 42, y + 23, n, 14, TEXT, 'middle')

    every = [(a, b) for a in range(5) for b in range(a + 1, 5)]
    modules(20, 'Tightly coupled', 'a change to one class touches the others', every, ACCENT)
    modules(380, 'Loosely coupled', 'each class knows as little as it can', [(0, 1), (0, 2), (0, 3), (0, 4)], TEAL)
    f.line(360, 24, 360, 300, FAINT, 1)
    return f


def parallax():
    f = Fig(720, 400, 'Layers that scroll at different speeds look like they are at different distances')
    x0, w = 40, 400
    # the screen, with the real layers
    f.rect(x0, 50, w, 225, SCREEN)
    f.image(ART + 'background.png', x0, 50, w, 209, crop=(0, 0, 640, 335))
    f.image(ART + 'ground.png', x0, 259, w, 16, crop=(0, 0, 400, 16))
    f.image(ART + 'bird.png', x0 + 150, 140, 36, 24)
    f.rect(x0, 50, w, 225, 'none', FAINT, 1.5)
    f.text(x0, 36, 'the screen', 14, MUTED)
    # what each layer does
    f.arrow(x0 + w + 110, 110, x0 + w + 60, 110, TEAL, 3)
    f.text(x0 + w + 20, 86, 'background', 15, TEXT, weight='bold')
    f.text(x0 + w + 122, 115, '30 px/s', 14, TEAL, mono=True)
    f.text(x0 + w + 20, 140, 'far away, so it moves slowly', 13, MUTED)
    f.text(x0 + w + 20, 178, 'bird', 15, TEXT, weight='bold')
    f.text(x0 + w + 20, 200, 'never moves sideways', 13, MUTED)
    f.arrow(x0 + w + 150, 258, x0 + w + 60, 258, ACCENT, 3)
    f.text(x0 + w + 20, 236, 'ground', 15, TEXT, weight='bold')
    f.text(x0 + w + 162, 263, '60 px/s', 14, ACCENT, mono=True)
    f.text(x0 + w + 20, 288, 'close, so it moves fast', 13, MUTED)
    f.line(x0 + w + 8, 110, x0 + w + 16, 110, FAINT, 1.5)
    f.line(x0 + w + 8, 152, x0 + w + 16, 174, FAINT, 1.5)
    f.line(x0 + w + 8, 267, x0 + w + 16, 258, FAINT, 1.5)
    # looping
    y = 316
    f.text(x0, y + 4, 'looping:', 14, TEXT, weight='bold')
    f.rect(x0 + 80, y - 12, 200, 20, PANEL, TEAL, 1.5)
    f.rect(x0 + 280, y - 12, 200, 20, PANEL, TEAL, 1.5, dash='5 4')
    f.text(x0 + 180, y + 3, 'the image', 12, MUTED, 'middle')
    f.text(x0 + 380, y + 3, 'the same image again', 12, MUTED, 'middle')
    f.rect(x0 + 200, y - 18, 130, 32, 'none', TEXT, 2)
    f.text(x0 + 265, y + 32, 'the screen', 12, TEXT, 'middle')
    f.text(x0 + 80, y + 58, 'offset = (offset + speed × deltaTime) % loopingPoint', 13, MUTED, mono=True)
    f.text(x0 + 500, y + 4, 'at the looping point,', 13, MUTED)
    f.text(x0 + 500, y + 22, 'the offset starts over', 13, MUTED)
    return f


def gravity():
    f = Fig(720, 340, 'Gravity adds to the velocity every frame, and a flap sets it upwards')
    x0, y0 = 60, 230
    f.line(40, 300, 680, 300, FAINT, 1.5)
    f.text(680, 320, 'time', 13, MUTED, 'end')
    # one flap, then falling, then another flap
    pts = []
    vy, y = -300.0, 0.0
    dt = 0.06
    for i in range(22):
        if i == 12:
            vy = -300.0
        pts.append((x0 + i * 28, y0 + y * 0.9, vy))
        vy += 980 * dt
        y += vy * dt
    d = 'M' + ' L'.join(f'{x:g} {yy:g}' for x, yy, _ in pts)
    f.path(d, FAINT, 1.5, dash='3 5')
    for i, (x, yy, v) in enumerate(pts):
        if i in (0, 12):
            f.image(ART + 'bird.png', x - 15, yy - 10, 30, 20)
            f.text(x, yy + 40, 'flap', 14, ACCENT, 'middle', 'bold')
            f.arrow(x, yy - 14, x, yy - 14 - 46, ACCENT, 3)
        else:
            f.circle(x, yy, 3, MUTED)
            if i % 2 == 0:
                length = max(-46, min(60, v * 0.11))
                if abs(length) > 6:
                    f.arrow(x, yy + (6 if length > 0 else -6), x, yy + length, TEAL, 2)
    f.text(60, 36, 'velocity.Y = −300', 15, ACCENT, mono=True)
    f.text(60, 58, 'a flap replaces the velocity, whatever it was', 13, MUTED)
    f.text(420, 36, 'velocity.Y += 980 × deltaTime', 15, TEAL, mono=True)
    f.text(420, 58, 'every frame, gravity pulls a little harder', 13, MUTED)
    return f


def pipes():
    f = Fig(720, 340, 'Each pair of pipes has its gap a small random step from the one before')
    top, bottom = 40, 290
    f.rect(30, top, 660, bottom - top, SCREEN)
    gaps = [130, 165, 140, 185, 160]
    for i, g in enumerate(gaps):
        x = 90 + i * 128
        f.rect(x, top, 46, g - top - 38, '#5f8f3a')
        f.rect(x - 4, g - 38 - 14, 54, 14, '#76ad49')
        f.rect(x, g + 38 + 14, 46, bottom - g - 52, '#5f8f3a')
        f.rect(x - 4, g + 38, 54, 14, '#76ad49')
        f.circle(x + 23, g, 4, ACCENT)
        if i:
            px = 90 + (i - 1) * 128 + 23
            f.line(px, gaps[i - 1], x + 23, g, ACCENT, 2, '5 4')
            step = g - gaps[i - 1]
            f.text((px + x + 23) / 2, min(g, gaps[i - 1]) - 12, f'{step:+d}', 14, ACCENT, 'middle', mono=True)
    x = 90
    f.arrow(x - 16, gaps[0] - 38, x - 16, gaps[0] + 38, TEXT, 1.5, both=True)
    f.text(x - 22, gaps[0] + 5, '100', 13, TEXT, 'end', mono=True)
    f.text(360, 316, 'gap = the last gap + a small random step, kept on the screen', 14, MUTED, 'middle')
    f.text(30, 28, 'pipes scroll left at the ground\'s speed; a new pair every 2 seconds', 14, MUTED)
    return f


def lifecycle():
    f = Fig(720, 260, 'Changing state calls Exit on the old state and Enter on the new one')
    y = 96
    f.text(40, 40, 'ChangeState(play)', 16, TEXT, mono=True)
    f.box(40, y, 150, 56, 'TitleState', 'the current state', FAINT)
    f.arrow(196, y + 28, 262, y + 28, ACCENT, 2.5)
    f.box(268, y, 110, 56, 'Exit()', 'title cleans up', ACCENT, title_fill=ACCENT)
    f.arrow(384, y + 28, 432, y + 28, ACCENT, 2.5)
    f.box(438, y, 110, 56, 'Enter()', 'play sets up', ACCENT, title_fill=ACCENT)
    f.arrow(554, y + 28, 584, y + 28, ACCENT, 2.5)
    f.box(590, y, 100, 56, 'PlayState', 'now current', TEAL)
    f.text(40, 206, 'then, every frame:', 14, MUTED)
    f.box(190, 184, 120, 40, 'Update()', None, TEAL, size=15)
    f.arrow(316, 204, 352, 204, TEAL, 2)
    f.box(358, 184, 120, 40, 'Draw()', None, TEAL, size=15)
    f.curve('M478 196 C 540 150, 140 150, 196 190', TEAL, 1.5, '4 4')
    f.text(500, 210, 'until the next ChangeState', 14, MUTED)
    return f


FIGURES = {
    'coupling': coupling,
    'parallax': parallax,
    'gravity': gravity,
    'pipes': pipes,
    'lifecycle': lifecycle,
}
