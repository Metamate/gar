"""Draws the course mascot, a small builder in a hard hat, and writes every file the site uses it
in: the logo, the favicons, and the two frames that walk along the bottom of the window.

The maps below hold only the inside of the figure. The outline is added around it, with the
corners cut and nothing under the boots, so it stands on the ground. On the strip the outline is
two pixels thick, which is how the sprites it walks among are drawn (Kenney's Pixel Platformer).
The logo and the favicons get a thin, darker outline, which reads better on the orange bar.
Run it after changing a map: python tools/mascot/build.py"""
import os
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUTLINE = '#4a3531'      # a dark, warm brown: the pack tints its outlines the same way
LOGO_OUTLINE = '#2a1f1c'

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


def draw(rows, thickness, outline):
    """The figure with an outline of the given thickness on every side but the bottom."""
    width, height = len(rows[0]), len(rows)
    assert all(len(r) == width for r in rows)
    filled = {(x + thickness, y + thickness): COLOURS[ch] for y, row in enumerate(rows) for x, ch in enumerate(row) if COLOURS[ch]}
    edge = set(filled)
    for _ in range(thickness):                            # one step up, down, left and right each time
        edge |= {(x + dx, y + dy) for x, y in edge for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
    im = Image.new('RGBA', (width + 2 * thickness, height + thickness), (0, 0, 0, 0))
    for x, y in edge:
        if y < im.height:                                 # nothing below the boots
            colour = filled.get((x, y), outline)
            im.putpixel((x, y), rgba(outline if colour == OUTLINE else colour))
    return im


def square(im):
    side = max(im.size)
    out = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    out.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return out


def svg(im):
    cells = []
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            if a:
                cells.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="#{r:02x}{g:02x}{b:02x}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {im.width} {im.height}" shape-rendering="crispEdges">' + ''.join(cells) + '</svg>\n'


big = lambda im, n: im.resize((im.width * n, im.height * n), Image.NEAREST)

# the strip: two frames side by side, with the thick outline
stand, walk = draw(STAND, 2, OUTLINE), draw(WALK, 2, OUTLINE)
sheet = Image.new('RGBA', (stand.width * 2, stand.height), (0, 0, 0, 0))
sheet.paste(stand, (0, 0)); sheet.paste(walk, (stand.width, 0))
sheet.save(os.path.join(ROOT, 'src/assets/mascot/walk.png'))

# the logo and the favicons: a thin outline
logo = square(draw(STAND, 1, LOGO_OUTLINE))
big(logo, 8).save(os.path.join(ROOT, 'src/assets/logo.png'))
big(logo, 8).save(os.path.join(ROOT, 'public/favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
open(os.path.join(ROOT, 'public/favicon.svg'), 'w', encoding='utf-8', newline='\n').write(svg(logo))
print('mascot written: strip frame', stand.size, 'logo', logo.size)
