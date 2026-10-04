"""Figures for 10 Pokemon."""
from figlib import *

INK, SHADOW, MID, PAPER = '#44415d', '#666389', '#8e8bb7', '#b5b0dd'      # the game's four shades


def state_stack():
    f = Fig(720, 370, 'States are pushed on top of each other; only the top one updates, and all of them draw')
    steps = [('walking', ['PlayState']),
             ('a battle starts', ['PlayState', 'BattleState']),
             ('choosing', ['PlayState', 'BattleState', 'BattleMenuState']),
             ('a message', ['PlayState', 'BattleState', 'BattleMessageState']),
             ('the battle ends', ['PlayState'])]
    for i, (title, stack) in enumerate(steps):
        ox = 24 + i * 138
        f.text(ox + 62, 40, title, 13.5, TEXT, 'middle', 'bold')
        f.rect(ox, 60, 124, 190, SCREEN, FAINT, 1.5, 6)
        for k, name in enumerate(stack):
            top = k == len(stack) - 1
            y = 204 - k * 44
            f.rect(ox + 8, y, 108, 36, PANEL, ACCENT if top else None, 2, 5)
            f.text(ox + 62, y + 22, name.replace('State', ''), 12.5, TEXT if top else MUTED, 'middle', mono=True)
        if i < 4:
            f.text(ox + 131, 160, '›', 22, FAINT, 'middle')
    f.text(24, 276, 'push', 13, MUTED)
    f.arrow(60, 272, 290, 272, MUTED, 1.5)
    f.text(580, 276, 'pop, pop', 13, MUTED)
    f.arrow(520, 272, 570, 272, MUTED, 1.5)
    f.rect(24, 300, 18, 18, PANEL, ACCENT, 2, 4)
    f.text(50, 314, 'the top state: the only one that gets Update', 13.5, TEXT)
    f.text(24, 346, 'Every state draws, from the bottom up, so the field stays visible behind the battle, and the battle behind a message.', 13, MUTED)
    return f


def tile_movement():
    f = Fig(720, 320, 'The tile position jumps at once; the pixel position is tweened to catch up')
    size, ox, oy = 70, 60, 70
    for c in range(4):
        f.rect(ox + c * size, oy, size, size, '#2a3a2a', FAINT, 1)
        f.text(ox + c * size + size / 2, oy + size + 20, f'tile {c + 3}', 12, MUTED, 'middle', mono=True)
    for i, t in enumerate((0, 0.33, 0.66, 1)):
        x = ox + size + t * size
        f.rect(x + 18, oy + 12, 34, 46, PAPER, opacity=0.25 + 0.25 * i)
    f.arrow(ox + size + 35, oy - 16, ox + 2 * size + 35, oy - 16, TEAL, 2.5)
    f.text(ox + 1.5 * size + 35, oy - 26, 'the sprite: tweened over half a second', 13, TEAL, 'middle')
    f.rect(ox + 2 * size + 3, oy + 3, size - 6, size - 6, 'none', ACCENT, 2.5, 4)
    x = 390
    f.text(x, 78, 'MapX, MapY', 15, ACCENT, weight='bold', mono=True)
    f.label(x, 102, ['the tile the player is on: used for the', 'rules, and set at once when a step starts'], 13.5, MUTED)
    f.text(x, 164, 'X, Y', 15, TEAL, weight='bold', mono=True)
    f.label(x, 188, ['where the sprite is drawn: in pixels,', 'sliding from the old tile to the new one'], 13.5, MUTED)
    f.text(360, 258, 'The logic moves first. When the sprite arrives, the walk state checks for an encounter,', 13.5, MUTED, 'middle')
    f.text(360, 278, 'and takes another step if a direction is still held.', 13.5, MUTED, 'middle')
    return f


def widgets():
    f = Fig(720, 380, 'The battle screen is built from four small widgets')
    sx, sy, sw, sh = 40, 40, 420, 236
    f.rect(sx, sy, sw, sh, PAPER)
    f.circle(sx + 300, sy + 60, 30, SHADOW)
    f.circle(sx + 110, sy + 150, 36, SHADOW)
    # health bars
    f.rect(sx + 30, sy + 30, 150, 12, INK)
    f.rect(sx + 32, sy + 32, 110, 8, MID)
    f.rect(sx + 240, sy + 150, 150, 12, INK)
    f.rect(sx + 242, sy + 152, 146, 8, MID)
    # the message and the menu
    f.rect(sx, sy + 176, 280, 60, INK, PAPER, 3)
    f.rect(sx + 14, sy + 196, 180, 6, PAPER); f.rect(sx + 14, sy + 210, 120, 6, PAPER)
    f.rect(sx + 280, sy + 176, 140, 60, INK, PAPER, 3)
    f.text(sx + 320, sy + 200, 'Fight', 14, PAPER, mono=True); f.text(sx + 320, sy + 224, 'Run', 14, PAPER, mono=True)
    f.path(f'M{sx + 300} {sy + 190} L{sx + 310} {sy + 196} L{sx + 300} {sy + 202} Z', PAPER, 0, PAPER)
    # the labels
    x = 500
    items = [('ProgressBar', 'fills by current / max: HP, EXP', (sx + 180, sy + 36), 70),
             ('Panel', 'the box behind every widget', (sx + 276, sy + 180), 136),
             ('Textbox', 'wraps text, pages on Confirm', (sx + 200, sy + 206), 202),
             ('Selection / Menu', 'options with actions, a cursor', (sx + 420, sy + 214), 268)]
    for name, sub, (ax, ay), y in items:
        f.text(x, y, name, 15, ACCENT, weight='bold', mono=True)
        f.text(x, y + 20, sub, 12.5, MUTED)
        f.line(ax, ay, x - 10, y - 5, ACCENT, 1.2, '4 3')
        f.circle(ax, ay, 3, ACCENT)
    f.text(40, 316, 'Each widget lives in one class, and the same four make every screen in the game.', 13.5, MUTED)
    f.text(40, 340, 'The bar shows a monster\'s health. The monster does not know the bar exists.', 13.5, MUTED)
    return f


def locator():
    f = Fig(720, 320, 'Callers ask the locator for an interface, and whatever was registered answers')
    callers = ['PlayerWalkState', 'TakeTurnState', 'BattleMenuState']
    for i, c in enumerate(callers):
        y = 56 + i * 62
        f.rect(30, y, 170, 40, PANEL, FAINT, 1.5, 6)
        f.text(115, y + 25, c, 13, TEXT, 'middle', mono=True)
        f.arrow(204, y + 20, 286, 138, MUTED, 1.5)
    f.box(292, 104, 150, 68, 'Locator', 'Locator.Audio', ACCENT, title_fill=ACCENT)
    f.arrow(446, 138, 500, 138, ACCENT, 2)
    f.rect(506, 114, 110, 48, SCREEN, TEAL, 1.5, 6)
    f.text(561, 143, 'IAudio', 15, TEAL, 'middle', 'bold', mono=True)
    f.line(561, 162, 561, 190, FAINT, 1.5)
    f.line(486, 190, 636, 190, FAINT, 1.5)
    for x, name, sub in ((486, 'SoundManager', 'the real one'), (636, 'NullAudio', 'does nothing')):
        f.line(x, 190, x, 206, FAINT, 1.5)
        f.rect(x - 64, 206, 128, 44, PANEL, FAINT, 1.5, 6)
        f.text(x, 224, name, 12.5, TEXT, 'middle', mono=True)
        f.text(x, 242, sub, 11.5, MUTED, 'middle')
    f.text(30, 262, 'callers only name the', 13, MUTED)
    f.text(30, 280, 'interface, never the class', 13, MUTED)
    f.text(360, 306, 'Game1 registers the real service at startup. Until then, the null object stands in, so no caller needs a null check.', 12.5, MUTED, 'middle')
    return f


def save_load():
    f = Fig(720, 250, 'Saving turns the game\'s objects into plain data and then text; loading goes the other way')
    xs = [30, 275, 520]
    boxes = [('game objects', 'Player, Party, Mon', FAINT, TEXT), ('save data', 'records: plain values', TEAL, TEAL), ('JSON text', 'a file on disk', ACCENT, ACCENT)]
    y = 76
    for x, (name, sub, stroke, color) in zip(xs, boxes):
        f.box(x, y, 170, 64, name, sub, stroke, title_fill=color)
    for a, b, top, bottom in ((xs[0], xs[1], 'pick what to keep', 'rebuild the objects'), (xs[1], xs[2], 'Serialize', 'Deserialize')):
        f.arrow(a + 176, y + 22, b - 6, y + 22, MUTED, 2)
        f.arrow(b - 6, y + 44, a + 176, y + 44, MUTED, 2)
        f.text((a + 170 + b) / 2, y - 8, top, 12, MUTED, 'middle')
        f.text((a + 170 + b) / 2, y + 84, bottom, 12, MUTED, 'middle')
    f.text(30, 50, 'save', 14, TEXT, weight='bold'); f.arrow(70, 45, 120, 45, MUTED, 2)
    f.text(690, 50, 'load', 14, TEXT, 'end', 'bold'); f.arrow(646, 45, 596, 45, MUTED, 2)
    f.text(360, 190, 'species name, level, HP, position', 13.5, TEAL, 'middle', mono=True)
    f.text(360, 212, 'Textures and references to other objects are left out: they are rebuilt from the data.', 13.5, MUTED, 'middle')
    f.text(360, 234, 'A round-trip test saves, loads, and checks that the two records are equal.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'state-stack': state_stack,
    'tile-movement': tile_movement,
    'widgets': widgets,
    'locator': locator,
    'save-load': save_load,
}
