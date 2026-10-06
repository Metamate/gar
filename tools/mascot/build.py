"""Draws the course mascot, a small builder in a hard hat, from the pixel maps below, and writes
every file the site uses it in: the logo, the favicons, and the two frames that walk along the
bottom of the window. Run it after changing a map: python tools/mascot/build.py"""
import os
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

COLOURS = {
    '.': None,
    'K': '#1c1917',     # outline, eyes and mouth
    'Y': '#f6c945',     # the hard hat
    'y': '#d39b1c',     # its shaded side and brim
    'H': '#fff3c4',     # the shine on the hat
    'W': '#f6efe9',     # the body
    'w': '#d6c8bd',     # its shaded side
    'O': '#e9703f',     # cheeks and boots, in the course's orange
}

STAND = [
    '................',
    '.....KKKKKK.....',
    '....KYYYYYYK....',
    '...KYHHYYYYyK...',
    '..KYHYYYYYYyyK..',
    '.KyyyyyyyyyyyyK.',
    '.KKKKKKKKKKKKKK.',
    '..KWWWWWWWWWwK..',
    '..KWWKWWWWKWwK..',
    '..KWWKWWWWKWwK..',
    '..KWOWWWWWWOwK..',
    '..KWWWWKKWWWwK..',
    '..KWWWWWWWWwwK..',
    '...KKKKKKKKKK...',
    '....KOK..KOK....',
    '....KKK..KKK....',
]

# The same figure a pixel higher, with one boot forward: the second frame of the walk.
WALK = STAND[1:13] + [
    '...KKKKKKKKKK...',
    '...KOK....KOK...',
    '...KKK....KKK...',
    '................',
]


def draw(rows):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if COLOURS[ch]:
                c = COLOURS[ch]
                im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im


def svg(rows):
    cells = [f'<rect x="{x}" y="{y}" width="1" height="1" fill="{COLOURS[ch]}"/>'
             for y, row in enumerate(rows) for x, ch in enumerate(row) if COLOURS[ch]]
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges">' + ''.join(cells) + '</svg>\n'


stand, walk = draw(STAND), draw(WALK)
big = lambda im, n: im.resize((im.width * n, im.height * n), Image.NEAREST)

big(stand, 8).save(os.path.join(ROOT, 'src/assets/logo.png'))
sheet = Image.new('RGBA', (32, 16), (0, 0, 0, 0))
sheet.paste(stand, (0, 0)); sheet.paste(walk, (16, 0))
sheet.save(os.path.join(ROOT, 'src/assets/mascot/walk.png'))
big(stand, 3).save(os.path.join(ROOT, 'public/favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
open(os.path.join(ROOT, 'public/favicon.svg'), 'w', encoding='utf-8', newline='\n').write(svg(STAND))
print('mascot written')
