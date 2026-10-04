"""Figures for 04 Sokoban."""
from figlib import *

TILES = GAMES + '04-sokoban/Content/Assets/images/tiles.png'
FLOOR, WALL, GOAL, BOX, PLAYER = 0, 1, 2, 3, 8        # tile numbers in the sheet (three columns of 64 pixels)


def tile(f, n, x, y, size):
    f.image(TILES, x, y, size, size, crop=((n % 3) * 64, (n // 3) * 64, (n % 3) * 64 + 64, (n // 3) * 64 + 64))


def push_rule():
    f = Fig(720, 330, 'A move is a walk, a push or blocked, depending on the next cell and the one behind it')
    size = 46

    def case(ox, cells, title, verdict, color, note):
        f.text(ox + 2 * size, 40, title, 16, TEXT, 'middle', 'bold')
        y = 78
        for i, c in enumerate(cells):
            x = ox + i * size
            tile(f, WALL if c == '#' else FLOOR, x, y, size)
            if c == '@': tile(f, PLAYER, x, y, size)
            if c == '$': tile(f, BOX, x, y, size)
        f.arrow(ox + size * 0.5, y + size + 22, ox + size * 1.5, y + size + 22, color, 3)
        f.text(ox + 2 * size, y + size + 64, verdict, 16, color, 'middle', 'bold')
        f.label(ox + 2 * size, y + size + 90, note, 13, MUTED, 'middle')
        f.text(ox + size * 1.5, y - 8, 'next', 12, MUTED, 'middle')
        f.text(ox + size * 2.5, y - 8, 'behind', 12, MUTED, 'middle')

    case(30, '@   ', 'Free ahead', 'Walked', TEAL, ['the next cell is empty'])
    case(268, '@$  ', 'A box, free behind it', 'Pushed', GREEN, ['the box moves one cell,', 'and the player follows'])
    case(506, '@$# ', 'A box against a wall', 'Blocked', ACCENT, ['nothing moves, and', 'no command is made'])
    f.text(360, 304, 'CanMove looks at two cells. Move changes the level and says which of the three happened.', 13.5, MUTED, 'middle')
    return f


def undo_stacks():
    f = Fig(720, 360, 'Two stacks: undo moves a command to the undone stack, and a new command empties it')
    steps = [
        ('three moves', ['A', 'B', 'C'], [], None),
        ('undo (Z)', ['A', 'B'], ['C'], 'C.Undo()'),
        ('redo (Y)', ['A', 'B', 'C'], [], 'C.Execute()'),
        ('undo, then a new move D', ['A', 'B', 'D'], [], 'the undone C is dropped'),
    ]
    for i, (title, done, undone, call) in enumerate(steps):
        ox = 24 + i * 174
        f.text(ox + 76, 36, title, 14, TEXT, 'middle', 'bold')
        if call:
            f.text(ox + 76, 58, call, 12.5, ACCENT if 'dropped' in call else TEAL, 'middle', mono='(' in call)
        for name, items, x, color in (('done', done, ox + 6, TEAL), ('undone', undone, ox + 84, ACCENT)):
            f.rect(x, 86, 62, 200, SCREEN, FAINT, 1.5, 6)
            f.text(x + 31, 308, name, 13, MUTED, 'middle')
            for k, item in enumerate(items):
                top = k == len(items) - 1
                f.rect(x + 7, 244 - k * 44, 48, 36, PANEL, color if top else None, 2, 5)
                f.text(x + 31, 268 - k * 44, item, 16, TEXT, 'middle', 'bold', mono=True)
        if i < 3:
            f.arrow(ox + 156, 186, ox + 172, 186, FAINT, 2)
    f.text(360, 342, 'Each letter is a MoveCommand that remembers what it did, so it can reverse it.', 13.5, MUTED, 'middle')
    return f


def what_to_remember():
    f = Fig(720, 300, 'After a walk and after a push the player stands in the same place, so the command must remember which it was')
    size = 46

    def row(y, before, after, title, undo, color):
        f.text(30, y + 30, title, 15, TEXT, weight='bold')
        for k, cells in enumerate((before, after)):
            ox = 170 + k * 230
            for i, c in enumerate(cells):
                tile(f, FLOOR, ox + i * size, y, size)
                if c == '@': tile(f, PLAYER, ox + i * size, y, size)
                if c == '$': tile(f, BOX, ox + i * size, y, size)
        f.arrow(170 + 3 * size + 14, y + size / 2, 170 + 230 - 14, y + size / 2, MUTED, 2)
        f.label(170 + 230 + 3 * size + 20, y + 18, undo, 13.5, color)

    f.text(170 + 1.5 * size, 40, 'before', 13, MUTED, 'middle')
    f.text(400 + 1.5 * size, 40, 'after moving right', 13, MUTED, 'middle')
    row(60, '@  ', ' @ ', 'A walk', ['undo: step the', 'player back'], TEAL)
    row(160, '@$ ', ' @$', 'A push', ['undo: step back, and', 'pull the box back too'], ACCENT)
    f.text(360, 262, 'The player ends on the same cell both times. Only the command knows whether a box moved,', 13.5, MUTED, 'middle')
    f.text(360, 282, 'so MoveCommand keeps the MoveResult.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'push-rule': push_rule,
    'undo-stacks': undo_stacks,
    'remember': what_to_remember,
}
