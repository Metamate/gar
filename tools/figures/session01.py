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


def game_loop():
    f = Fig(720, 250, 'Every game runs the same loop: process input, update the game, render, and again')
    names = [('Process input', 'what did the player do?'), ('Update', 'move the world one step on'), ('Render', 'draw what the world looks like')]
    for i, (n, sub) in enumerate(names):
        x = 60 + i * 215
        f.box(x, 80, 170, 70, n, None, ACCENT if i == 1 else FAINT, size=17)
        f.text(x + 85, 176, sub, 13.5, MUTED, 'middle')
        if i < 2:
            f.arrow(x + 176, 115, x + 209, 115, MUTED, 2.5)
    f.curve('M664 115 C 712 115, 712 34, 600 34 L 120 34 C 14 34, 14 115, 54 115', TEAL, 2.5)
    f.text(360, 24, 'many times a second, until the game ends', 13.5, TEAL, 'middle')
    f.text(360, 226, 'The loop never waits for the player. The game keeps moving when nobody presses anything.', 13.5, MUTED, 'middle')
    return f


def lifecycle():
    f = Fig(720, 380, 'MonoGame calls Initialize and LoadContent once, then Update and Draw every frame')
    f.box(60, 50, 150, 54, 'Initialize()', None, FAINT, size=15)
    f.box(270, 50, 150, 54, 'LoadContent()', None, FAINT, size=15)
    f.arrow(214, 77, 264, 77, MUTED, 2.5)
    f.text(240, 36, 'once, at the start', 13, MUTED, 'middle')
    f.rect(180, 140, 330, 216, SCREEN, TEAL, 1.5, 10)
    f.text(196, 164, 'the game loop', 13.5, TEAL)
    f.box(270, 180, 150, 50, 'Update()', None, TEAL, size=15)
    f.box(270, 290, 150, 50, 'Draw()', None, TEAL, size=15)
    f.arrow(345, 108, 345, 174, MUTED, 2.5)
    f.arrow(345, 234, 345, 284, TEAL, 2.5)
    f.curve('M266 315 C 206 315, 206 205, 264 205', TEAL, 2.5)
    f.text(430, 266, 'every frame', 13, TEAL)
    f.box(560, 180, 120, 50, 'Exit()', None, ACCENT, size=15, title_fill=ACCENT)
    f.arrow(424, 205, 554, 205, ACCENT, 2, '5 4')
    f.text(620, 252, 'when the game', 12.5, MUTED, 'middle')
    f.text(620, 270, 'is closed', 12.5, MUTED, 'middle')
    f.label(470, 60, ['Game1 overrides these four', 'methods. MonoGame decides', 'when to call them.'], 13, MUTED)
    return f


def filtering():
    import base64
    f = Fig(720, 320, 'Point filtering keeps the pixels of scaled-up art sharp; linear filtering blurs them')
    art = GAMES + '02-flappy-bird/Content/Assets/images/bird.png'
    data = base64.b64encode(open(art, 'rb').read()).decode()
    f.rect(30, 100, 76, 56, SCREEN, r=4)
    f.image(art, 49, 116, 38, 24)
    f.text(68, 180, 'the art', 13, MUTED, 'middle')
    f.arrow(116, 128, 160, 128, MUTED, 2)
    f.text(138, 114, '× 6', 13, MUTED, 'middle')
    for ox, name, sub, smooth, color in ((176, 'Point', 'SamplerState.PointClamp', False, TEAL), (450, 'Linear', 'SamplerState.LinearClamp', True, ACCENT)):
        f.rect(ox, 44, 250, 172, SCREEN, color, 1.5, 6)
        style = 'auto' if smooth else 'pixelated'
        f.add(f'<image x="{ox + 11}" y="58" width="228" height="144" preserveAspectRatio="none" style="image-rendering:{style}" href="data:image/png;base64,{data}"/>')
        f.text(ox + 125, 246, name, 16, color, 'middle', 'bold')
        f.text(ox + 125, 268, sub, 13, MUTED, 'middle', mono=True)
    f.text(360, 302, 'Each screen pixel takes the nearest art pixel, or a mix of the ones around it.', 13.5, MUTED, 'middle')
    return f


def encapsulation():
    f = Fig(720, 340, 'Encapsulation: the data of a thing and the code that uses it move into a class of their own')
    f.text(170, 36, 'Everything in Game1', 16, TEXT, 'middle', 'bold')
    f.rect(40, 54, 260, 236, SCREEN, ACCENT, 1.5, 8)
    f.text(56, 78, 'Game1', 13, ACCENT, mono=True)
    for i, line in enumerate(('_player1Y', '_player2Y', '_ballX, _ballY', '_ballDX, _ballDY', 'MovePaddles()', 'MoveBall()', 'DrawPaddles()', 'DrawBall()')):
        f.text(64, 104 + i * 23, line, 13, TEXT if i < 4 else MUTED, mono=True)
    f.text(170, 316, 'every new thing makes Game1 longer', 13.5, MUTED, 'middle')
    f.arrow(312, 172, 362, 172, MUTED, 2.5)
    f.text(530, 36, 'A class per thing', 16, TEXT, 'middle', 'bold')
    for ox, name, data, code in ((380, 'Paddle', ['Y', 'Speed'], ['Update()', 'Draw()']), (540, 'Ball', ['Position', 'Velocity'], ['Update()', 'Draw()'])):
        f.rect(ox, 54, 140, 150, SCREEN, TEAL, 1.5, 8)
        f.text(ox + 14, 78, name, 13, TEAL, mono=True)
        for i, d in enumerate(data):
            f.text(ox + 22, 104 + i * 23, d, 13, TEXT, mono=True)
        f.line(ox + 10, 140, ox + 130, 140, FAINT, 1)
        for i, c in enumerate(code):
            f.text(ox + 22, 164 + i * 23, c, 13, MUTED, mono=True)
    f.rect(380, 226, 300, 64, SCREEN, FAINT, 1.5, 8)
    f.text(394, 250, 'Game1', 13, MUTED, mono=True)
    f.text(394, 274, 'two paddles, a ball, and the rules', 13, TEXT)
    f.text(530, 316, 'data and behaviour belong together', 13.5, MUTED, 'middle')
    return f


def update_method():
    f = Fig(720, 330, 'The Update Method pattern: the game calls Update on every object, and each object moves itself one frame on')
    f.box(40, 124, 160, 70, 'Game1.Update', 'once per frame', ACCENT, title_fill=ACCENT)
    objs = [('paddle 1', 'reads W and S, and moves'), ('paddle 2', 'reads the arrows, and moves'), ('ball', 'moves by its velocity')]
    for i, (name, what) in enumerate(objs):
        y = 44 + i * 86
        f.rect(340, y, 340, 62, SCREEN, TEAL, 1.5, 8)
        f.text(356, y + 26, f'{i + 1}.  {name}', 14.5, TEXT, weight='bold')
        f.text(380, y + 47, what, 13, MUTED)
        f.text(666, y + 37, 'Update()', 13, TEAL, 'end', mono=True)
        f.arrow(204, 159, 334, y + 31, MUTED, 2)
    f.text(360, 308, 'One after another, in a fixed order. No object needs to know how the others move.', 13.5, MUTED, 'middle')
    return f


def modes():
    f = Fig(720, 250, 'Pong has four modes: start, serve, play and done')
    xs = {'start': 40, 'serve': 220, 'play': 400, 'done': 580}
    for n, x in xs.items():
        f.box(x, 90, 100, 56, n, None, ACCENT if n == 'play' else FAINT, size=17)
    f.arrow(144, 118, 214, 118, MUTED, 2.5); f.text(179, 108, 'Enter', 13, MUTED, 'middle')
    f.arrow(324, 106, 394, 106, MUTED, 2.5); f.text(359, 96, 'Enter', 13, MUTED, 'middle')
    f.arrow(394, 132, 324, 132, MUTED, 2.5); f.text(359, 152, 'a point', 13, MUTED, 'middle')
    f.arrow(504, 118, 574, 118, MUTED, 2.5); f.text(539, 108, '10 points', 13, MUTED, 'middle')
    f.curve('M630 150 C 630 214, 270 214, 270 152', MUTED, 2.5)
    f.text(450, 220, 'Enter', 13, MUTED, 'middle')
    f.text(360, 50, 'the mode is a string field, checked with if in Update and in Draw', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'coordinates': coordinates,
    'virtual-resolution': virtual_resolution,
    'delta-time': delta_time,
    'timestep': timestep,
    'aabb': aabb,
    'bounce': bounce,
    'game-loop': game_loop,
    'lifecycle': lifecycle,
    'filtering': filtering,
    'encapsulation': encapsulation,
    'update-method': update_method,
    'modes': modes,
}
