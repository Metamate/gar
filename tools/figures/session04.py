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


def command_idea():
    f = Fig(720, 280, 'A method call is gone once it has run; a command is the same request as an object that can be kept')
    f.text(180, 40, 'A method call', 16, TEXT, 'middle', 'bold')
    f.rect(50, 64, 260, 44, SCREEN, FAINT, 1.5, 6)
    f.text(180, 92, 'level.Move(direction)', 14, TEXT, 'middle', mono=True)
    f.arrow(180, 112, 180, 150, MUTED, 2)
    f.text(180, 178, 'it runs, and it is gone', 14, MUTED, 'middle')
    f.line(360, 24, 360, 262, FAINT, 1)
    f.text(540, 40, 'A command', 16, TEXT, 'middle', 'bold')
    f.rect(400, 64, 280, 44, SCREEN, ACCENT, 1.5, 6)
    f.text(540, 92, 'new MoveCommand(level, direction)', 13, TEXT, 'middle', mono=True)
    f.text(540, 138, 'an object, so it can be', 14, MUTED, 'middle')
    for i, (name, sub) in enumerate((('kept', 'in a list'), ('queued', 'run later'), ('replayed', 'run again'), ('undone', 'reversed'))):
        x = 394 + i * 74
        f.rect(x, 156, 68, 56, PANEL, TEAL, 1.5, 6)
        f.text(x + 34, 180, name, 13, TEXT, 'middle', 'bold')
        f.text(x + 34, 198, sub, 11, MUTED, 'middle')
    f.text(180, 250, 'nothing is left to undo', 13.5, MUTED, 'middle')
    f.text(540, 250, 'the request still exists after it ran', 13.5, MUTED, 'middle')
    return f


def command_object():
    f = Fig(720, 320, 'With commands, a button holds an object, and rebinding the button means giving it a different one')
    buttons = ['X', 'Y', 'A', 'B']
    f.text(170, 36, 'Hardwired', 16, TEXT, 'middle', 'bold')
    for i, (b, fn) in enumerate(zip(buttons, ('Jump()', 'Fire()', 'SwapWeapon()', 'Dodge()'))):
        y = 62 + i * 52
        f.circle(60, y + 16, 16, PANEL, FAINT, 1.5); f.text(60, y + 21, b, 14, TEXT, 'middle', 'bold')
        f.line(80, y + 16, 150, y + 16, ACCENT, 2)
        f.text(160, y + 21, fn, 13.5, TEXT, mono=True)
    f.text(170, 292, 'the button is the call, fixed in code', 13.5, MUTED, 'middle')
    f.line(350, 24, 350, 300, FAINT, 1)
    f.text(535, 36, 'With commands', 16, TEXT, 'middle', 'bold')
    for i, (b, c) in enumerate(zip(buttons, ('JumpCommand', 'FireCommand', 'SwapCommand', 'DodgeCommand'))):
        y = 62 + i * 52
        f.circle(400, y + 16, 16, PANEL, FAINT, 1.5); f.text(400, y + 21, b, 14, TEXT, 'middle', 'bold')
        f.arrow(420, y + 16, 464, y + 16, TEAL, 2)
        f.rect(470, y, 140, 32, SCREEN, TEAL, 1.5, 6)
        f.text(540, y + 21, c, 13, TEXT, 'middle', mono=True)
        f.text(622, y + 21, 'Execute()', 12, MUTED, mono=True)
    f.text(535, 292, 'the button holds an object, which can be swapped', 13.5, MUTED, 'middle')
    return f


def command_structure():
    f = Fig(720, 290, 'The history only knows that a command can be executed and undone; each command knows what it acts on')
    f.text(360, 40, 'The history can run, undo and redo any command without knowing what it does.', 13.5, MUTED, 'middle')
    f.box(30, 90, 160, 64, 'CommandHistory', 'the invoker', FAINT, size=14)
    f.arrow(194, 122, 264, 122, MUTED, 2.5)
    f.rect(270, 86, 170, 72, SCREEN, TEAL, 1.5, 8)
    f.text(355, 112, 'ICommand', 15, TEAL, 'middle', 'bold', mono=True)
    f.text(355, 136, 'Execute()  Undo()', 12.5, MUTED, 'middle', mono=True)
    f.line(355, 158, 355, 196, FAINT, 1.5)
    f.rect(270, 196, 170, 56, PANEL, FAINT, 1.5, 8)
    f.text(355, 220, 'MoveCommand', 14, TEXT, 'middle', mono=True)
    f.text(355, 240, 'level, direction, result', 12, MUTED, 'middle')
    f.arrow(444, 224, 606, 160, ACCENT, 2.5)
    f.box(540, 90, 150, 64, 'Level', 'the receiver', ACCENT, title_fill=ACCENT, size=14)
    f.text(560, 222, 'level.Move(direction)', 12.5, ACCENT, mono=True)
    return f


def command_stream():
    f = Fig(720, 280, 'Whatever produces the commands, the actor that carries them out does not have to know')
    for i, (name, sub) in enumerate((('the player', 'keys and buttons'), ('an AI', 'decides what to do'), ('a replay', 'a saved list'))):
        y = 30 + i * 74
        f.box(30, y, 170, 54, name, sub, FAINT, size=15)
        f.arrow(204, y + 27, 270, 131, MUTED, 2)
    f.rect(276, 104, 250, 54, SCREEN, TEAL, 1.5, 27)
    for k in range(4):
        f.rect(288 + k * 58, 116, 50, 30, PANEL, TEAL, 1.5, 5)
        f.text(313 + k * 58, 136, 'cmd', 12, TEXT, 'middle', mono=True)
    f.text(401, 90, 'a stream of commands', 13.5, TEAL, 'middle')
    f.arrow(530, 131, 574, 131, MUTED, 2.5)
    f.box(580, 100, 110, 62, 'the actor', 'executes them', ACCENT, title_fill=ACCENT, size=15)
    f.text(360, 262, 'The same character can be driven by a player, by the computer, or by a recording.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'push-rule': push_rule,
    'undo-stacks': undo_stacks,
    'remember': what_to_remember,
    'command-idea': command_idea,
    'command-object': command_object,
    'command-structure': command_structure,
    'command-stream': command_stream,
}
