"""Draws the course mascot, a small builder in a hard hat, and writes every file the site uses it
in: the logo, the favicons, and the two frames that walk along the bottom of the window.

The maps below hold only the inside of the figure. The outline is added around it, two pixels
thick with the corners cut, which is how the sprites it walks among are drawn (Kenney's Pixel
Platformer, 18 x 18). Run it after changing a map: python tools/mascot/build.py"""
import os
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SIZE, MARGIN = 18, 2
OUTLINE = '#4a3531'      # a dark, warm brown: the pack tints its outlines the same way

COLOURS = {
    '.': None,
    'K': OUTLINE,       # eyes, mouth and the line under the hat
    'Y': '#f6c945',     # the hard hat
    'y': '#d39b1c',     # its shaded side and brim
    'H': '#fff3c4',     # the shine on the hat
    'W': '#f6efe9',     # the body
    'w': '#d6c8bd',     # its shaded side
    'O': '#e9703f',     # boots, in the course's orange
}

BODY = [
    '....YYYYYY....',
    '...YHHYYYYy...',
    '..YHYYYYYYyy..',
    '..YYYYYYYYyy..',
    'yyyyyyyyyyyyyy',
    '.KKKKKKKKKKKK.',
    '.WWWWWWWWWWWw.',
    '.WWKKWWWWKKWw.',
    '.WWKKWWWWKKWw.',
    '.WWWWWKKWWWWw.',
    '.WWWWWWWWWWww.',
    '.wwwwwwwwwwww.',
]
STAND = BODY + ['...OO....OO...', '...OO....OO...']
WALK = BODY + ['..OO......OO..', '..OO......OO..']      # the boots apart: the second frame of the walk


def rgba(colour):
    return tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def draw(rows):
    assert len(rows) == SIZE - 2 * MARGIN and all(len(r) == SIZE - 2 * MARGIN for r in rows)
    filled = {(x + MARGIN, y + MARGIN): COLOURS[ch] for y, row in enumerate(rows) for x, ch in enumerate(row) if COLOURS[ch]}
    edge = set(filled)
    for _ in range(MARGIN):                               # one step up, down, left and right, twice
        edge |= {(x + dx, y + dy) for x, y in edge for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
    im = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    for x, y in edge:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            im.putpixel((x, y), rgba(filled.get((x, y), OUTLINE)))
    return im


def svg(im):
    cells = []
    for y in range(SIZE):
        for x in range(SIZE):
            r, g, b, a = im.getpixel((x, y))
            if a:
                cells.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="#{r:02x}{g:02x}{b:02x}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" shape-rendering="crispEdges">' + ''.join(cells) + '</svg>\n'


stand, walk = draw(STAND), draw(WALK)
big = lambda im, n: im.resize((im.width * n, im.height * n), Image.NEAREST)

big(stand, 8).save(os.path.join(ROOT, 'src/assets/logo.png'))
sheet = Image.new('RGBA', (SIZE * 2, SIZE), (0, 0, 0, 0))
sheet.paste(stand, (0, 0)); sheet.paste(walk, (SIZE, 0))
sheet.save(os.path.join(ROOT, 'src/assets/mascot/walk.png'))
big(stand, 8).save(os.path.join(ROOT, 'public/favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
open(os.path.join(ROOT, 'public/favicon.svg'), 'w', encoding='utf-8', newline='\n').write(svg(stand))
print('mascot written')
