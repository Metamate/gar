"""Draws the two small icons of the score in the top bar: a coin and a gem, in the colours of the
ones on the strip but ten pixels across, so that they are as tall as the digits beside them.
Run it after changing a map: python tools/mascot/hud_icons.py"""
import os
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

ICONS = {
    'coin-hud': ({'K': '#6f3e43', 'Y': '#f4b41b', 'L': '#fee481'}, [
        '..KKKKKK..',
        '.KKYYYYKK.',
        'KKYYYYYYKK',
        'KYYLLLLYYK',
        'KYYLYYLYYK',
        'KYYLYYLYYK',
        'KYYLLLLYYK',
        'KKYYYYYYKK',
        '.KKYYYYKK.',
        '..KKKKKK..',
    ]),
    'diamond-hud': ({'K': '#434a5f', 'B': '#2cc5f6', 'D': '#1490c3', 'L': '#bdeeff'}, [
        '.KKKKKKKK.',
        'KKLLBBBBKK',
        'KLBBBBBBBK',
        'KBBBBBBBBK',
        'KKDDDDDDKK',
        '.KKDDDDKK.',
        '..KKDDKK..',
        '...KKKK...',
        '....KK....',
    ]),
}

for name, (colours, rows) in ICONS.items():
    im = Image.new('RGBA', (len(rows[0]), len(rows)), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.':
                c = colours[ch]
                im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(os.path.join(ROOT, 'src/assets/strip', name + '.png'))
    print(name, im.size)
