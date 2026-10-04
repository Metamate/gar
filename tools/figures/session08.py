"""Figures for 08 Angry Birds."""
from figlib import *

WOOD = '#c98f4e'


def two_worlds():
    f = Fig(720, 360, 'The physics world works in metres with y up; the game works in pixels with y down')

    def world(ox, title, sub, color, up, unit, size, pos):
        f.text(ox + 150, 36, title, 16, color, 'middle', 'bold')
        f.text(ox + 150, 58, sub, 13.5, MUTED, 'middle')
        x, y, w, h = ox + 40, 80, 220, 170
        f.rect(x, y, w, h, SCREEN, r=4)
        oy = y                                       # both worlds have their origin at the top-left corner
        f.arrow(x, oy, x + w + 22, oy, color, 2.5)
        if up:                                       # the physics y axis points up, so everything below it has a negative y
            f.arrow(x, y + h, x, y - 26, color, 2.5)
        else:
            f.arrow(x, oy, x, y + h + 22, color, 2.5)
        f.text(x + w + 28, oy + 5, 'x', 15, color, weight='bold', italic=True)
        f.text(x - 14, (y - 16) if up else (y + h + 20), 'y', 15, color, 'middle', 'bold', italic=True)
        f.circle(x, oy, 4, color)
        f.rect(x + 100, y + 96, 54, 54, WOOD, '#7a5328', 1.5)
        f.text(x + 127, y + 86, pos, 13, TEXT, 'middle', mono=True)
        f.text(x + 127, y + 128, size, 12, '#3a2a14', 'middle', mono=True)
        f.text(ox + 150, 300, unit, 13.5, MUTED, 'middle')

    world(10, 'Box2D', 'the physics world', TEAL, True, 'tuned for objects of 0.1 to 10 metres', '1 m', '(2.5, −2.5)')
    world(370, 'The game', 'what is drawn', ACCENT, False, 'in pixels, this block would be 50 metres wide', '50 px', '(125, 125)')
    f.arrow(326, 150, 386, 150, MUTED, 2, both=True)
    f.text(356, 134, '× 50', 13, TEXT, 'middle', mono=True)
    f.text(356, 176, 'flip y', 13, TEXT, 'middle')
    f.text(360, 336, 'Units.cs is the only place that converts between the two.', 13.5, MUTED, 'middle')
    return f


def body_types():
    f = Fig(720, 280, 'Static bodies never move, kinematic bodies move as they are told, dynamic bodies are moved by physics')
    cols = [('Static', 'never moves', 'the ground, walls', '#f0a04b'),
            ('Kinematic', 'moves at the velocity you set;', 'pushes, and is never pushed', '#d86ad6'),
            ('Dynamic', 'moved by gravity and', 'collisions: everything else', GREEN)]
    for i, (name, a, b, color) in enumerate(cols):
        ox = 30 + i * 230
        f.rect(ox, 50, 200, 130, SCREEN, r=4)
        if name == 'Static':
            f.rect(ox + 10, 140, 180, 26, 'none', color, 2.5)
        if name == 'Kinematic':
            f.rect(ox + 50, 120, 100, 18, 'none', color, 2.5)
            f.arrow(ox + 30, 129, ox + 46, 129, color, 2, both=False)
            f.arrow(ox + 154, 129, ox + 174, 129, color, 2)
            f.rect(ox + 84, 92, 28, 28, 'none', GREEN, 2)
        if name == 'Dynamic':
            f.rect(ox + 60, 70, 34, 34, 'none', color, 2.5)
            f.arrow(ox + 77, 110, ox + 77, 146, color, 2)
            f.circle(ox + 134, 96, 16, 'none', color, 2.5)
            f.arrow(ox + 134, 118, ox + 134, 150, color, 2)
        f.text(ox + 100, 208, name, 16, color, 'middle', 'bold')
        f.text(ox + 100, 232, a, 13, MUTED, 'middle')
        f.text(ox + 100, 252, b, 13, MUTED, 'middle')
    return f


def destroy_safely():
    f = Fig(720, 320, 'Hits only mark entities as destroyed; they are removed after the physics step')
    x0, y = 40, 110
    f.text(x0, 44, 'one frame', 14, MUTED)
    f.rect(x0, y - 34, 330, 68, SCREEN, TEAL, 1.5, 6)
    f.text(x0 + 12, y - 44, 'Physics.Update: the step', 13, TEAL)
    for i, lab in enumerate(('hit', 'hit', 'hit')):
        x = x0 + 30 + i * 100
        f.rect(x, y - 18, 70, 36, PANEL, ACCENT, 1.5, 5)
        f.text(x + 35, y - 2, 'hit', 13, TEXT, 'middle')
        f.text(x + 35, y + 13, 'mark', 12, ACCENT, 'middle')
    f.arrow(x0 + 336, y, x0 + 386, y, MUTED, 2)
    f.rect(x0 + 392, y - 34, 250, 68, SCREEN, GREEN, 1.5, 6)
    f.text(x0 + 404, y - 44, 'RemoveDestroyed', 13, GREEN, mono=True)
    f.text(x0 + 517, y - 2, 'destroy the marked bodies,', 13, TEXT, 'middle')
    f.text(x0 + 517, y + 16, 'and take them off the list', 13, TEXT, 'middle')
    f.text(x0, 200, 'Why not in the hit handler?', 15, TEXT, weight='bold')
    f.label(x0, 228, ['The world is still reporting: a later hit may be about the body you just destroyed.',
                      'And something may be looping over the list you would remove from.'], 13.5, MUTED)
    f.text(x0, 292, 'Mark now, remove at a safe point.', 14, GREEN, weight='bold')
    return f


def shallow_copy():
    f = Fig(720, 330, 'A clone shares what the prototype refers to, so it shares the sprite but must get a body of its own')
    f.box(40, 60, 190, 60, 'the prototype', '"wood-plank", not in the world', FAINT)
    f.box(40, 190, 190, 60, 'a clone', 'placed in the level', TEAL)
    f.arrow(135, 124, 135, 184, MUTED, 2)
    f.text(146, 158, 'MemberwiseClone', 12.5, MUTED, mono=True)
    f.box(430, 50, 180, 50, 'the sprite', 'never changes', FAINT, size=15)
    f.box(430, 200, 180, 50, 'its own body', 'created in Spawn', GREEN, size=15, title_fill=GREEN)
    f.arrow(236, 82, 424, 76, MUTED, 2)
    f.arrow(236, 210, 424, 92, TEAL, 2)
    f.text(330, 62, 'Sprite', 12.5, MUTED, 'middle', mono=True)
    f.note(346, 170, 'the same sprite: fine', 13, TEAL)
    f.arrow(236, 228, 424, 228, GREEN, 2)
    f.text(330, 248, 'Body', 12.5, GREEN, 'middle', mono=True)
    f.rect(430, 122, 180, 44, SCREEN, ACCENT, 1.5, 8, dash='5 4')
    f.text(520, 149, 'a shared body', 14, ACCENT, 'middle')
    f.text(626, 149, 'never', 13, ACCENT)
    f.text(360, 296, 'A shallow copy copies references. Two blocks with one body would move as one,', 13.5, MUTED, 'middle')
    f.text(360, 316, 'so Clone clears the body and Spawn makes a new one.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'two-worlds': two_worlds,
    'body-types': body_types,
    'destroy-safely': destroy_safely,
    'shallow-copy': shallow_copy,
}
