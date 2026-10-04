"""Figures for 07 The Legend of Zelda."""
import math
from figlib import *

FLOOR = '#c98d5a'
HERO, ENEMY = '#6fbf4a', '#b98ad6'


def hitboxes():
    f = Fig(720, 330, 'The hitbox deals damage and the hurtbox receives it, and neither has to match the sprite')
    f.rect(30, 50, 400, 230, FLOOR, r=4, opacity=0.9)
    # the hero, facing right, mid-swing
    hx, hy = 110, 110
    f.rect(hx, hy, 64, 96, HERO, opacity=0.55)
    f.text(hx + 32, hy - 10, 'the sprite', 13, '#1c2a14', 'middle')
    f.rect(hx, hy + 48, 64, 48, 'none', GREEN, 3)
    f.rect(hx + 64, hy + 36, 44, 64, 'none', ACCENT, 3)
    f.line(hx + 60, hy + 62, hx + 104, hy + 62, '#dfe6ea', 5)
    # an enemy inside the sword's reach
    ex, ey = 196, 150
    f.rect(ex, ey, 60, 60, ENEMY, opacity=0.75)
    f.rect(ex, ey, 60, 60, 'none', GREEN, 3)
    f.rect(ex, ey, 12, 50, ACCENT, opacity=0.35)
    f.text(ex + 30, ey + 80, 'an enemy', 13, '#3a2a18', 'middle')
    x = 460
    f.rect(x, 74, 18, 18, 'none', ACCENT, 3)
    f.text(x + 30, 89, 'hitbox', 16, ACCENT, weight='bold')
    f.label(x, 116, ['the area that deals damage:', 'a rectangle in front of the', 'player, while the sword swings'], 13.5, MUTED)
    f.rect(x, 196, 18, 18, 'none', GREEN, 3)
    f.text(x + 30, 211, 'hurtbox', 16, GREEN, weight='bold')
    f.label(x, 238, ['the area that takes damage:', 'the hero\'s feet, the enemy\'s body'], 13.5, MUTED)
    f.text(230, 308, 'They overlap, so the enemy is hit. Press F1 in the game to see both.', 13.5, MUTED, 'middle')
    return f


def event_flow():
    f = Fig(720, 330, 'An event travels up from the room to the play state; each class only knows the one below it')
    xs = [60, 290, 520]
    names = [('Room', 'notices the player died'), ('Dungeon', 'passes it on'), ('PlayState', 'changes to game over')]
    y = 120
    for x, (n, sub) in zip(xs, names):
        f.box(x, y, 150, 64, n, None, FAINT, size=17)
        f.text(x + 75, y + 90, sub, 13.5, MUTED, 'middle')
    for a, b in zip(xs, xs[1:]):
        f.arrow(a + 156, y + 20, b - 6, y + 20, ACCENT, 3)
        f.text((a + 150 + b) / 2, y - 12, 'OnPlayerDied', 12.5, ACCENT, 'middle', mono=True)
        f.arrow(b - 6, y + 46, a + 156, y + 46, TEAL, 1.5, '5 4')
    f.text(60, 50, 'the event goes this way', 14, ACCENT, weight='bold')
    f.arrow(250, 45, 300, 45, ACCENT, 3)
    f.text(60, 78, 'the subscription, and the knowledge, go the other way', 14, TEAL, weight='bold')
    f.arrow(476, 73, 426, 73, TEAL, 1.5, '5 4')
    f.text(360, 262, 'Room announces that something happened. It has no reference to Dungeon or PlayState,', 13.5, MUTED, 'middle')
    f.text(360, 282, 'and a second subscriber (a sound, a score) can be added without touching it.', 13.5, MUTED, 'middle')
    return f


def event_queue():
    f = Fig(720, 330, 'An event is handled inside the call that raises it; an event queue handles it later, at a safe point')
    x0, w = 170, 500

    def row(y, title, sub):
        f.text(30, y + 4, title, 16, TEXT, weight='bold')
        f.text(30, y + 24, sub, 13, MUTED)
        f.rect(x0, y - 22, w, 44, SCREEN, r=6)
        f.text(x0 + 8, y - 30, 'one frame', 12, MUTED)

    row(96, 'Event', 'handled at once')
    f.rect(x0 + 10, 82, 410, 28, PANEL, TEAL, 1.5, 4)
    f.text(x0 + 20, 101, 'the room loops over its enemies', 13, TEXT)
    for i, x in enumerate((x0 + 250, x0 + 305, x0 + 360)):
        f.rect(x, 78, 40, 36, '#4a2c22', ACCENT, 1.5, 4)
    f.text(x0 + 325, 136, 'each handler runs inside the loop', 13, ACCENT, 'middle')
    row(222, 'Event queue', 'handled later')
    f.rect(x0 + 10, 208, 300, 28, PANEL, TEAL, 1.5, 4)
    f.text(x0 + 20, 227, 'the room loops over its enemies', 13, TEXT)
    for i, x in enumerate((x0 + 232, x0 + 258, x0 + 284)):
        f.circle(x, 222, 5, ACCENT)
        f.curve(f'M{x} 214 C {x + 20} 176, {x0 + 380} 176, {x0 + 392 + i * 14} 202', FAINT, 1.2, '3 4')
    f.rect(x0 + 372, 204, 110, 36, '#4a2c22', ACCENT, 1.5, 4)
    f.text(x0 + 427, 227, 'handle them all', 13, TEXT, 'middle')
    f.text(360, 292, 'A handler that removes an enemy while the room is looping over them breaks the loop.', 13.5, MUTED, 'middle')
    f.text(360, 312, 'Queued, the same handler runs when nothing else is in the middle of anything.', 13.5, MUTED, 'middle')
    return f


def room_shift():
    f = Fig(720, 340, 'To scroll between rooms, a tween moves the camera from one room to the next')
    rw, rh, y = 190, 110, 60
    for i, name in enumerate(('this room', 'the next room')):
        x = 40 + i * rw
        f.rect(x, y, rw, rh, FLOOR, '#5b4a3a', 2, opacity=0.9)
        f.text(x + rw / 2, y + rh + 20, name, 13, MUTED, 'middle')
    for t, op in ((0, 0.35), (0.5, 0.6), (1, 1)):
        x = 40 + t * rw
        f.rect(x, y - 6, rw, rh + 12, 'none', ACCENT, 2.5, 4, opacity=op)
    f.arrow(60, y - 22, 40 + rw + 170, y - 22, ACCENT, 2)
    f.text(40 + rw, y - 30, 'the camera, at t = 0, 0.5 and 1', 13, ACCENT, 'middle')
    f.rect(40 + rw - 12, y + 44, 14, 22, HERO)
    f.arrow(40 + rw + 8, y + 55, 40 + rw + 44, y + 55, GREEN, 2)
    # the curves
    gx, gy, gw, gh = 480, 60, 200, 140
    f.rect(gx, gy, gw, gh, SCREEN, r=4)
    f.line(gx, gy + gh, gx + gw, gy, MUTED, 2)
    pts = ' L'.join(f'{gx + t / 20 * gw:g} {gy + gh - (1 - (1 - t / 20) ** 2) * gh:g}' for t in range(21))
    f.path('M' + pts, TEAL, 2.5)
    f.text(gx, gy + gh + 18, 't = 0', 12, MUTED, mono=True)
    f.text(gx + gw, gy + gh + 18, '1', 12, MUTED, 'end', mono=True)
    f.text(gx + gw - 8, gy + gh - 22, 'linear', 13, MUTED, 'end')
    f.text(gx + 16, gy + 26, 'ease-out', 13, TEAL)
    f.text(40, 250, 'lerp(a, b, t) = a + (b − a) × t', 15, TEXT, mono=True)
    f.label(40, 280, ['The tween runs t from 0 to 1 over a second, and moves the camera and the player together.',
                      'An easing curve changes how t grows: ease-out starts fast and settles.'], 13.5, MUTED)
    return f


def stencil():
    f = Fig(720, 300, 'Three passes: draw the rooms, mark the door arches in the stencil buffer, then draw the player where it is unmarked')
    w, h, y = 200, 130, 70

    def room(x):
        f.rect(x, y, w, h, FLOOR, opacity=0.9)
        f.rect(x, y, w, h, 'none', '#5b4a3a', 10)
        f.rect(x + w - 8, y + h / 2 - 22, 16, 44, '#3a2f26')

    x = 30
    room(x)
    f.text(x + w / 2, 44, '1. The rooms', 15, TEXT, 'middle', 'bold')
    f.label(x + w / 2, y + h + 28, ['everything except', 'the player'], 13, MUTED, 'middle')
    x = 260
    f.rect(x, y, w, h, SCREEN)
    f.rect(x + w - 22, y + h / 2 - 24, 30, 48, TEXT)
    f.text(x + w - 30, y + h / 2 + 5, '1', 15, TEXT, 'end', mono=True)
    f.text(x + 40, y + h / 2 + 5, '0', 15, MUTED, mono=True)
    f.text(x + w / 2, 44, '2. The stencil', 15, TEXT, 'middle', 'bold')
    f.label(x + w / 2, y + h + 28, ['a rectangle over each arch,', 'written as 1, with no colour'], 13, MUTED, 'middle')
    x = 490
    room(x)
    f.rect(x + w - 34, y + h / 2 - 14, 26, 28, HERO)
    f.rect(x + w - 8, y + h / 2 - 14, 12, 28, HERO, opacity=0.25)
    f.rect(x + w - 8, y + h / 2 - 22, 16, 44, 'none', ACCENT, 1.5, dash='3 3')
    f.text(x + w / 2, 44, '3. The player', 15, TEXT, 'middle', 'bold')
    f.label(x + w / 2, y + h + 28, ['drawn only where the', 'stencil is still 0'], 13, MUTED, 'middle')
    f.arrow(236, y + h / 2, 254, y + h / 2, MUTED, 2)
    f.arrow(466, y + h / 2, 484, y + h / 2, MUTED, 2)
    f.text(360, 282, 'The player seems to walk under the arch.', 13.5, MUTED, 'middle')
    return f


def composition():
    f = Fig(720, 360, 'With inheritance every combination needs a class; with composition an enemy has the parts it needs')
    # inheritance: a tree that grows
    f.text(180, 36, 'Inheritance: what it is', 16, TEXT, 'middle', 'bold')
    nodes = {'Enemy': (180, 70), 'Walker': (90, 130), 'Flyer': (270, 130),
             'ShootingWalker': (86, 196), 'ExplodingWalker': (86, 240), 'ShootingFlyer': (270, 196),
             'ShootingExplodingFlyer?': (270, 262)}
    links = [('Enemy', 'Walker'), ('Enemy', 'Flyer'), ('Walker', 'ShootingWalker'), ('Walker', 'ExplodingWalker'),
             ('Flyer', 'ShootingFlyer'), ('ShootingFlyer', 'ShootingExplodingFlyer?')]
    for a, b in links:
        ax, ay = nodes[a]; bx, by = nodes[b]
        f.line(ax, ay + 14, bx, by - 14, FAINT, 1.5)
    for n, (x, y) in nodes.items():
        odd = n.endswith('?')
        w = len(n) * 7.2 + 18
        f.rect(x - w / 2, y - 14, w, 28, PANEL, ACCENT if odd else FAINT, 1.5, 5)
        f.text(x, y + 5, n, 12.5, ACCENT if odd else TEXT, 'middle', mono=True)
    f.text(180, 310, 'shooting is written twice, and', 13.5, MUTED, 'middle')
    f.text(180, 330, 'every new mix is a new class', 13.5, MUTED, 'middle')
    f.line(360, 24, 360, 340, FAINT, 1)
    # composition: an enemy and its parts
    f.text(540, 36, 'Composition: what it has', 16, TEXT, 'middle', 'bold')
    for i, (name, parts) in enumerate((('a bat', ['fly', 'shoot']), ('a bomb beetle', ['walk', 'explode']), ('a boss', ['fly', 'shoot', 'explode']))):
        y = 78 + i * 74
        f.rect(390, y, 300, 56, SCREEN, FAINT, 1.5, 6)
        f.text(404, y + 33, name, 14, TEXT, weight='bold')
        for k, p in enumerate(parts):
            f.chip(516 + k * 58, y + 15, 52, p, PANEL, TEAL, 12.5, stroke=TEAL)
    f.text(540, 310, 'four parts, written once each,', 13.5, MUTED, 'middle')
    f.text(540, 330, 'in any combination', 13.5, MUTED, 'middle')
    return f


def observer():
    f = Fig(720, 330, 'The subject keeps a list of observers and tells each of them when something happens')
    f.rect(40, 90, 230, 150, SCREEN, ACCENT, 1.5, 8)
    f.text(155, 78, 'the subject', 15, ACCENT, 'middle', 'bold')
    f.text(56, 118, 'event OnPlayerDied', 13, TEXT, mono=True)
    f.text(56, 148, 'its subscribers', 12.5, MUTED)
    for i in range(3):
        f.rect(56 + i * 66, 160, 58, 26, PANEL, TEAL, 1.5, 5)
        f.text(85 + i * 66, 178, 'handler', 11, TEXT, 'middle', mono=True)
    f.text(56, 218, 'OnPlayerDied?.Invoke()', 12.5, ACCENT, mono=True)
    names = [('the game over screen', 'takes over'), ('the sound', 'plays a jingle'), ('a later feature', 'needs no change to the subject')]
    for i, (n, sub) in enumerate(names):
        y = 66 + i * 76
        f.rect(470, y, 220, 54, SCREEN, TEAL, 1.5, 8)
        f.text(486, y + 24, n, 14, TEXT, weight='bold')
        f.text(486, y + 43, sub, 12.5, MUTED)
        f.arrow(276, 166, 464, y + 27, ACCENT, 2)
    f.text(580, 50, 'the observers', 15, TEAL, 'middle', 'bold')
    f.text(360, 304, 'An observer subscribes with +=. The subject never learns who they are, or how many.', 13.5, MUTED, 'middle')
    return f


def room():
    import random
    f = Fig(720, 330, 'Each room is generated when the player enters it: walls, a random floor, doorways, enemies and a switch')
    ox, oy, cell, cols, rows = 30, 30, 30, 13, 8
    random.seed(4)
    for r in range(rows):
        for c in range(cols):
            wall = r in (0, rows - 1) or c in (0, cols - 1)
            shade = random.choice(('#c98d5a', '#c48755', '#cf9460'))
            f.rect(ox + c * cell, oy + r * cell, cell, cell, '#55606b' if wall else shade, '#1a1a1a', 0.5)
    for c, r, w, h in ((5.5, 0, 2, 1), (5.5, rows - 1, 2, 1), (0, 3, 1, 2), (cols - 1, 3, 1, 2)):
        f.rect(ox + c * cell, oy + r * cell, w * cell, h * cell, '#3a2f26', ACCENT, 2)
    for x, y in ((4, 2), (9, 5), (3, 5)):
        f.rect(ox + x * cell + 5, oy + y * cell + 5, 20, 20, ENEMY, r=4)
    f.rect(ox + 9 * cell + 6, oy + 2 * cell + 6, 18, 18, '#7b8794', '#d9534f', 3, 3)
    f.rect(ox + 6 * cell + 5, oy + 4 * cell + 3, 20, 24, HERO, r=3)
    x = 450
    items = [('walls and floor', 'a tilemap, floor tiles picked at random', '#55606b'), ('four doorways', 'closed until the switch is pressed', ACCENT),
             ('enemies', 'placed at random', ENEMY), ('a switch', 'opens the doors', '#d9534f'), ('the player', 'comes in through a doorway', HERO)]
    for i, (n, sub, color) in enumerate(items):
        y = 52 + i * 48
        f.rect(x, y - 13, 16, 16, color, r=3)
        f.text(x + 26, y, n, 14.5, TEXT, weight='bold')
        f.text(x + 26, y + 19, sub, 12.5, MUTED)
    f.text(360, 308, 'The dungeon is an endless series of such rooms, and none of them is designed by hand.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'hitboxes': hitboxes,
    'event-flow': event_flow,
    'event-queue': event_queue,
    'room-shift': room_shift,
    'stencil': stencil,
    'composition': composition,
    'observer': observer,
    'room': room,
}
