"""Figures for 06 Super Mario Bros."""
from figlib import *

GROUND, GRASS, SKY = '#8a5a3c', '#6fbf4a', '#1b2733'
PLAYER = '#e8c15a'


def ground(f, x, y, size, top=True):
    f.rect(x, y, size, size, GROUND)
    if top:
        f.rect(x, y, size, size * 0.28, GRASS)
    f.rect(x, y, size, size, 'none', '#00000055', 1)


def tile_snap():
    f = Fig(720, 330, 'The player moves first, then is snapped back to the edge of the tile it overlaps')
    size = 54

    def stage(ox, title, hx, note, color, overlap=False):
        f.text(ox + 100, 38, title, 15, TEXT, 'middle', 'bold')
        y = 90
        f.rect(ox, y - 30, 200, 150, SKY, r=4)
        ground(f, ox + 146, y, size, top=False)
        ground(f, ox + 146, y + size, size, top=False)
        f.rect(ox, y + size + 12, 146, 36, GROUND); f.rect(ox, y + size + 12, 146, 9, GRASS)
        f.rect(hx, y + 14, 48, 52, 'none', color, 2.5)
        f.rect(hx + 5, y + 19, 38, 42, PLAYER, opacity=0.85)
        if overlap:
            f.rect(ox + 146, y + 14, hx + 48 - ox - 146, 52, ACCENT, opacity=0.55)
        f.line(ox + 146, y - 34, ox + 146, y + 120, FAINT, 1, '3 4')
        f.label(ox + 100, 262, note, 13.5, MUTED, 'middle')

    stage(20, '1. Before', 20 + 70, ['the hitbox is clear', 'of the wall'], TEAL)
    stage(260, '2. Move', 260 + 112, ['velocity × deltaTime takes it', '14 pixels into the wall'], ACCENT, overlap=True)
    stage(500, '3. Snap', 500 + 98, ['back to the tile\'s edge, and the', 'velocity on that axis becomes 0'], GREEN)
    f.arrow(226, 130, 254, 130, MUTED, 2)
    f.arrow(466, 130, 494, 130, MUTED, 2)
    f.text(360, 314, 'x is moved and snapped first, then y. One axis at a time, the snap always knows which edge to use.', 13, MUTED, 'middle')
    return f


def hitbox_inset():
    f = Fig(720, 330, 'A hitbox a little narrower than a tile lets the player fall into a one-tile pit')
    size = 60

    def case(ox, title, inset, verdict, color):
        f.text(ox + 150, 38, title, 15, TEXT, 'middle', 'bold')
        y = 190
        f.rect(ox, 60, 300, 210, SKY, r=4)
        for c in (0, 1, 3, 4):
            ground(f, ox + c * size, y, size)
        px = ox + 2 * size - 4
        w = size + 8
        f.rect(px, y - 78, w, 78, PLAYER, opacity=0.35)
        f.rect(px + inset, y - 78, w - 2 * inset, 78, 'none', color, 2.5)
        f.line(ox + 2 * size, y, ox + 2 * size, y + 70, FAINT, 1, '3 4')
        f.line(ox + 3 * size, y, ox + 3 * size, y + 70, FAINT, 1, '3 4')
        f.text(ox + 2.5 * size, y + 48, 'pit', 13, MUTED, 'middle')
        if inset:
            f.arrow(px + w / 2, y + 6, px + w / 2, y + 30, color, 2.5)
        else:
            for ex in (px + 2, px + w - 2):
                f.circle(ex, y, 4.5, ACCENT)
        f.text(ox + 150, 296, verdict, 14, color, 'middle', 'bold')

    case(30, 'Hitbox as wide as the sprite', 0, 'both edges rest on the ground: stuck', ACCENT)
    case(390, 'Hitbox inset by 2 pixels', 8, 'narrower than the pit: it falls', GREEN)
    f.line(360, 24, 360, 310, FAINT, 1)
    return f


def coyote():
    f = Fig(720, 300, 'Coyote time allows a jump for a moment after the player has left the ground')
    y = 150
    f.rect(30, 40, 660, 190, SKY, r=4)
    for c in range(5):
        ground(f, 30 + c * 60, y, 60)
    f.rect(30, y + 60, 300, 20, GROUND)
    # the player's path off the ledge
    pts = [(250, y - 46), (300, y - 46), (350, y - 44), (395, y - 34), (435, y - 14), (470, y + 20)]
    for i, (x, py) in enumerate(pts):
        in_window = i in (2, 3)
        f.rect(x - 14, py, 28, 46, PLAYER, opacity=0.9 if i < 4 else 0.45)
        if in_window:
            f.rect(x - 14, py, 28, 46, 'none', GREEN, 2.5)
    f.line(330, 56, 330, 216, FAINT, 1.5, '4 4')
    f.text(330, 248, 'the ledge ends', 13, MUTED, 'middle')
    f.rect(332, 60, 88, 22, '#22402a', GREEN, 1.5, 4)
    f.text(376, 76, '0.1 s', 13, GREEN, 'middle', mono=True)
    f.text(430, 76, 'a jump still counts here', 14, GREEN)
    f.text(500, 150, 'too late: falling', 14, MUTED)
    f.text(60, 76, 'on the ground: a jump works', 14, TEAL)
    f.text(360, 282, 'The player pressed a moment too late, and still gets the jump. Nobody notices; it just feels fair.', 13.5, MUTED, 'middle')
    return f


def camera():
    f = Fig(720, 340, 'The world is wider than the screen; the camera decides which part is drawn')
    wx, wy, ww, wh = 30, 70, 660, 130
    f.rect(wx, wy, ww, wh, SKY, r=4)
    for c in range(22):
        if c in (6, 7, 14):
            continue
        ground(f, wx + c * 30, wy + wh - 30, 30)
    for c in (10, 11, 17):
        ground(f, wx + c * 30, wy + wh - 60, 30)
    f.text(wx, 44, 'the world: every position is a world position', 14, TEXT, weight='bold')
    px = wx + 330
    f.rect(px - 9, wy + wh - 58, 18, 28, PLAYER)
    cw = 232
    f.rect(px - cw / 2, wy - 6, cw, wh + 12, 'none', ACCENT, 2.5, 4)
    f.text(px + cw / 2, wy - 14, 'the camera', 13, ACCENT, 'end', 'bold')
    f.text(px, wy + wh + 30, 'player at world x = 1,100', 13, MUTED, 'middle', mono=True)
    # the screen
    sx, sy, sw, sh = 244, 248, 232, 74
    f.line(px - cw / 2, wy + wh + 6, sx, sy, ACCENT, 1, '4 4')
    f.line(px + cw / 2, wy + wh + 6, sx + sw, sy, ACCENT, 1, '4 4')
    f.rect(sx, sy, sw, sh, SKY, ACCENT, 2, 4)
    f.rect(sx + sw / 2 - 5, sy + 30, 10, 16, PLAYER)
    f.rect(sx, sy + sh - 18, sw, 18, GROUND)
    f.text(sx + sw + 16, sy + 26, 'the screen', 14, TEXT, weight='bold')
    f.label(sx + sw + 16, sy + 48, ['the same player, drawn at', 'screen x = 213'], 13, MUTED)
    f.label(30, sy + 26, ['Only drawing goes through', 'the camera. The game\'s', 'logic stays in the world.'], 13, MUTED)
    return f


def layers():
    f = Fig(720, 330, 'A level is two tilemaps and a list of entities, drawn on top of each other')
    size = 34
    rows = [(0, 'entities', 'a list: they move, and come and go', ACCENT),
            (1, 'toppers', 'a second tilemap: grass or snow, only for looks', TEAL),
            (2, 'tilemap', 'a grid of tiles: the ground, and what is solid', MUTED)]
    for i, name, sub, color in rows:
        oy = 50 + i * 88
        ox = 60 + (2 - i) * 22
        f.add(f'<g transform="translate({ox} {oy}) skewX(-28)">')
        f.rect(0, 0, 9 * size, 62, SKY, color, 1.5, opacity=0.92)
        if name == 'tilemap':
            for c in range(9):
                if c not in (4,):
                    f.rect(c * size, 30, size, 32, GROUND, '#00000055', 1)
        if name == 'toppers':
            for c in range(9):
                if c not in (4,):
                    f.rect(c * size, 30, size, 10, GRASS)
        if name == 'entities':
            f.rect(40, 6, 16, 24, PLAYER)
            f.rect(210, 14, 22, 16, '#7ad1c0', r=6)
            f.rect(266, -6, 22, 22, '#d9a441', '#7a5a1d', 1.5)
            f.circle(120, 12, 7, '#f2d24b')
        f.add('</g>')
        f.text(410, oy + 30, name, 16, color if color != MUTED else TEXT, weight='bold')
        f.text(410, oy + 52, sub, 13.5, MUTED)
    f.text(360, 312, '"Is this spot solid?" is one lookup in the tilemap. The entities are checked one by one.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'tile-snap': tile_snap,
    'hitbox-inset': hitbox_inset,
    'coyote': coyote,
    'camera': camera,
    'layers': layers,
}
