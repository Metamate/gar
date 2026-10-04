"""Figures for 09 Plants vs. Zombies."""
from figlib import *

LAWN_A, LAWN_B = '#6aa84f', '#5d9945'


def picking():
    f = Fig(720, 350, 'Picking takes two steps: from the window to the game, then from a point to a cell')
    # the window, with the game centred in it
    wx, wy, ww, wh = 30, 70, 250, 190
    f.rect(wx, wy, ww, wh, '#000000', FAINT, 1.5)
    gx, gy, gw, gh = wx, wy + 24, 250, 141
    f.rect(gx, gy, gw, gh, '#2b3a2a')
    f.text(wx, 52, '1. the window', 15, TEXT, weight='bold')
    mx, my = wx + 170, wy + 110
    f.circle(mx, my, 5, ACCENT)
    f.text(mx + 10, my - 8, 'the mouse', 12.5, ACCENT)
    f.text(wx, wy + wh + 22, 'window pixels', 13, MUTED)
    f.arrow(292, 150, 330, 150, MUTED, 2)
    f.text(311, 136, 'invert', 12, MUTED, 'middle')
    f.text(311, 172, 'the scale', 12, MUTED, 'middle')
    # the game, with its field
    fx, fy = 344, 70
    f.text(fx, 52, '2. the game: 1280 × 720', 15, TEXT, weight='bold')
    f.rect(fx, fy, 346, 195, '#2b3a2a')
    cols, rows, cw, ch = 7, 5, 40, 28
    ox, oy = fx + 40, fy + 44
    for r in range(rows):
        for c in range(cols):
            f.rect(ox + c * cw, oy + r * ch, cw, ch, LAWN_A if (r + c) % 2 == 0 else LAWN_B)
    pc, pr = 4, 2
    f.rect(ox + pc * cw, oy + pr * ch, cw, ch, 'none', ACCENT, 2.5)
    f.circle(ox + pc * cw + 26, oy + pr * ch + 12, 5, ACCENT)
    for c in range(4):
        f.rect(fx + 44 + c * 34, fy + 8, 28, 28, PANEL, FAINT, 1, 3)
    f.text(fx + 196, fy + 27, 'cards', 12, MUTED)
    f.text(fx, fy + 217, 'cell = (position − field corner) / cell size', 13, TEXT, mono=True)
    f.text(fx, fy + 239, 'a division, however many cells there are', 13, MUTED)
    f.text(30, 328, 'Things that are not on a grid (a coin, the cards) are checked one by one, and the order decides what a click hits.', 13, MUTED)
    return f


def inheritance_problem():
    f = Fig(720, 320, 'With a class per kind of thing, a defender that shoots and makes gold has no good place in the tree')
    nodes = {'Defender': (250, 60), 'Chest': (110, 140), 'Archer': (250, 140), 'Knight': (390, 140), 'Goblin': (580, 60)}
    subs = {'Chest': 'makes gold', 'Archer': 'shoots', 'Knight': 'blocks', 'Goblin': 'has its own health'}
    for n in ('Chest', 'Archer', 'Knight'):
        f.line(250, 78, nodes[n][0], 122, FAINT, 1.5)
    for n, (x, y) in nodes.items():
        f.rect(x - 56, y - 18, 112, 36, PANEL, FAINT, 1.5, 6)
        f.text(x, y + 5, n, 14, TEXT, 'middle', 'bold')
        if n in subs:
            f.text(x, y + 38, subs[n], 12.5, MUTED, 'middle')
    f.rect(124, 216, 172, 40, SCREEN, ACCENT, 1.5, 6, dash='5 4')
    f.text(210, 241, 'shoots and makes gold?', 13.5, ACCENT, 'middle')
    f.line(110, 190, 180, 216, ACCENT, 1.5, '4 4')
    f.line(250, 190, 240, 216, ACCENT, 1.5, '4 4')
    f.label(322, 224, ['one base class only: the', 'other ability gets copied'], 13, MUTED)
    f.rect(494, 216, 172, 40, SCREEN, ACCENT, 1.5, 6, dash='5 4')
    f.text(580, 241, 'a shield, like a defender?', 13.5, ACCENT, 'middle')
    f.line(580, 110, 580, 216, ACCENT, 1.5, '4 4')
    f.text(360, 296, 'Inheritance says what a thing is. Here it matters more what each thing can do.', 13.5, MUTED, 'middle')
    return f


def components():
    f = Fig(720, 360, 'An entity is a list of components, and each kind of thing is a different list')
    kinds = [('Chest', ['SpriteRenderer', 'Health', 'GoldProducer']),
             ('Archer', ['SpriteRenderer', 'Health', 'Shooter']),
             ('Goblin', ['SpriteRenderer', 'Health', 'Walker', 'Attacker']),
             ('Shieldbearer', ['SpriteRenderer', 'Health', 'Walker', 'Attacker', 'Armour'])]
    shared = {'SpriteRenderer': MUTED, 'Health': TEAL}
    for i, (name, parts) in enumerate(kinds):
        ox = 30 + i * 170
        f.rect(ox, 56, 150, 236, SCREEN, FAINT, 1.5, 8)
        f.text(ox + 75, 44, name, 15, TEXT, 'middle', 'bold')
        f.text(ox + 12, 78, 'Entity', 12, MUTED, mono=True)
        for k, p in enumerate(parts):
            color = shared.get(p, ACCENT)
            f.rect(ox + 12, 90 + k * 38, 126, 30, PANEL, color, 1.5, 6)
            f.text(ox + 75, 110 + k * 38, p, 12.5, TEXT, 'middle', mono=True)
    f.text(30, 320, 'Health', 13.5, TEAL, weight='bold', mono=True)
    f.text(86, 320, 'is written once, and defenders and goblins both use it.', 13.5, MUTED)
    f.text(30, 342, 'A Shieldbearer is a Goblin with one more component. Neither needed a class.', 13.5, MUTED)
    return f


def type_object():
    f = Fig(720, 340, 'One type object holds what all archers share; each entity on the field holds what is its own')
    f.rect(40, 70, 230, 170, SCREEN, ACCENT, 1.5, 8)
    f.text(155, 56, 'DefenderType: one for all archers', 14, ACCENT, 'middle', 'bold')
    for i, (k, v) in enumerate((('name', '"Archer"'), ('cost', '100'), ('recharge', '7.5'), ('health', '6'), ('shooter', '1.4 s, 1 shot'))):
        f.text(58, 104 + i * 26, k, 13, MUTED, mono=True)
        f.text(138, 104 + i * 26, v, 13, TEXT, mono=True)
    f.text(155, 262, 'from defenders.json', 13, MUTED, 'middle')
    f.text(155, 282, 'the card in the bar shows this', 13, MUTED, 'middle')
    for i in range(3):
        y = 76 + i * 62
        f.rect(450, y, 230, 46, SCREEN, TEAL, 1.5, 8)
        f.text(464, y + 20, f'an archer in row {i + 1}', 13.5, TEXT, weight='bold')
        f.text(464, y + 38, f'position, health so far: {(6, 4.5, 2)[i]:g}', 12.5, MUTED)
        f.arrow(276, 150, 444, y + 23, MUTED, 1.5)
    f.text(350, 92, 'Create()', 13, TEXT, 'middle', mono=True)
    f.text(565, 56, 'entities: one per archer placed', 14, TEAL, 'middle', 'bold')
    f.text(565, 282, 'clicking the field makes one', 13, MUTED, 'middle')
    f.text(360, 322, 'A new kind of defender is a new block of data. The cost belongs to the kind, and the health to the one on the field.', 13, MUTED, 'middle')
    return f


FIGURES = {
    'picking': picking,
    'inheritance': inheritance_problem,
    'components': components,
    'type-object': type_object,
}
