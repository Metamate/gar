"""A small SVG drawing kit for the course's concept figures.

Every figure is drawn on the same dark panel with the same few colours, so the figures look
like one set on the site (in both themes) and on the decks' dark slides. A figure is a Python
function that returns a Fig; build.py writes it as an SVG for the site and a PNG for the decks.
"""
from xml.sax.saxutils import escape

BG = '#22262b'        # the panel behind every figure (the decks' slide colour)
PANEL = '#2e3338'     # boxes
SCREEN = '#14171a'    # a game screen inside a figure
TEXT = '#dee2e6'
MUTED = '#9aa3ab'
FAINT = '#565d65'
ACCENT = '#d45d35'    # the site's and the decks' orange: what the figure is about
TEAL = '#2aa6a6'      # a second thing to compare with
GREEN = '#7fd46b'
SANS = "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "Consolas, 'Cascadia Mono', Menlo, monospace"


class Fig:
    def __init__(self, width, height, title=None):
        self.w, self.h = width, height
        self.items = []
        self.defs = {}
        self.title = title

    # ---- primitives
    def add(self, s):
        self.items.append(s)
        return self

    def rect(self, x, y, w, h, fill=PANEL, stroke=None, sw=2, r=0, dash=None, opacity=None):
        a = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}"'
        if r: a += f' rx="{r:g}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw:g}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        if opacity is not None: a += f' opacity="{opacity:g}"'
        return self.add(a + '/>')

    def circle(self, x, y, r, fill=TEXT, stroke=None, sw=2):
        a = f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw:g}"'
        return self.add(a + '/>')

    def line(self, x1, y1, x2, y2, stroke=MUTED, sw=2, dash=None, cap='round'):
        a = f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{stroke}" stroke-width="{sw:g}" stroke-linecap="{cap}"'
        if dash: a += f' stroke-dasharray="{dash}"'
        return self.add(a + '/>')

    def path(self, d, stroke=MUTED, sw=2, fill='none', dash=None, marker=None):
        a = f'<path d="{d}" stroke="{stroke}" stroke-width="{sw:g}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"'
        if dash: a += f' stroke-dasharray="{dash}"'
        if marker: a += f' marker-end="url(#{marker})"'
        return self.add(a + '/>')

    def _head(self, color):
        key = 'arrow-' + color.strip('#')
        self.defs[key] = (f'<marker id="{key}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                          f'<path d="M0 0 L10 5 L0 10 z" fill="{color}"/></marker>')
        return key

    def arrow(self, x1, y1, x2, y2, stroke=MUTED, sw=2, dash=None, both=False):
        key = self._head(stroke)
        a = (f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{stroke}" stroke-width="{sw:g}" '
             f'stroke-linecap="round" marker-end="url(#{key})"')
        if both: a += f' marker-start="url(#{key})"'
        if dash: a += f' stroke-dasharray="{dash}"'
        return self.add(a + '/>')

    def curve(self, d, stroke=MUTED, sw=2, dash=None):
        return self.path(d, stroke, sw, dash=dash, marker=self._head(stroke))

    def text(self, x, y, s, size=16, fill=TEXT, anchor='start', weight='normal', mono=False, italic=False):
        fam = MONO if mono else SANS
        a = (f'<text x="{x:g}" y="{y:g}" font-family="{fam}" font-size="{size:g}" fill="{fill}" '
             f'text-anchor="{anchor}" font-weight="{weight}"')
        if italic: a += ' font-style="italic"'
        return self.add(a + f'>{escape(s)}</text>')

    def note(self, x, y, s, size=14, fill=MUTED):
        """Centred text on a patch of the background, for a note that sits on top of lines."""
        w = len(s) * size * 0.52 + 16
        self.rect(x - w / 2, y - size, w, size * 1.5, BG)
        return self.text(x, y, s, size, fill, 'middle')

    def label(self, x, y, lines, size=15, fill=MUTED, anchor='start', gap=1.3, **kw):
        """Several lines of text, the first at y."""
        for i, s in enumerate(lines if isinstance(lines, (list, tuple)) else [lines]):
            self.text(x, y + i * size * gap, s, size, fill, anchor, **kw)
        return self

    def box(self, x, y, w, h, title, sub=None, stroke=None, fill=PANEL, size=16, title_fill=TEXT):
        self.rect(x, y, w, h, fill, stroke, r=8)
        cy = y + h / 2 + size * 0.35 - (size * 0.6 if sub else 0)
        self.text(x + w / 2, cy, title, size, title_fill, 'middle', 'bold')
        if sub:
            self.text(x + w / 2, cy + size * 1.25, sub, size - 3, MUTED, 'middle')
        return self

    # ---- output
    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w:g} {self.h:g}" width="{self.w:g}" height="{self.h:g}" role="img">')
        if self.title:
            head += f'<title>{escape(self.title)}</title>'
        defs = '<defs>' + ''.join(self.defs.values()) + '</defs>' if self.defs else ''
        back = f'<rect width="{self.w:g}" height="{self.h:g}" rx="10" fill="{BG}"/>'
        return head + defs + back + '\n' + '\n'.join(self.items) + '\n</svg>\n'
