"""Figures for 11 Geometry Wars."""
import math
from figlib import *

GLOW = '#59d6e8'


def lifecycle():
    f = Fig(720, 250, 'Every component can hook into the same phases, which the entity runs in a fixed order')
    once = ['OnAdded', 'OnStart']
    frame = ['PreUpdate', 'Update', 'Simulate', 'PostUpdate', 'Draw']
    x = 30
    f.text(30, 44, 'once', 13, MUTED)
    for n in once:
        f.rect(x, 56, 80, 38, PANEL, FAINT, 1.5, 6); f.text(x + 40, 80, n, 12, TEXT, 'middle', mono=True)
        f.arrow(x + 83, 75, x + 92, 75, MUTED, 1.5)
        x += 95
    f.text(x, 44, 'every frame', 13, TEAL)
    fx = x
    for i, n in enumerate(frame):
        f.rect(x, 56, 80, 38, PANEL, TEAL, 1.5, 6); f.text(x + 40, 80, n, 12, TEXT, 'middle', mono=True)
        if i < len(frame) - 1:
            f.arrow(x + 83, 75, x + 92, 75, TEAL, 1.5)
        x += 95
    f.curve(f'M{x - 55} 98 C {x - 55} 136, {fx + 40} 136, {fx + 40} 100', TEAL, 1.5, '4 4')
    f.rect(fx + 150, 150, 140, 38, PANEL, ACCENT, 1.5, 6); f.text(fx + 220, 174, 'OnCollision', 12.5, TEXT, 'middle', mono=True)
    f.text(fx + 300, 174, 'when the world reports a hit', 13, MUTED)
    f.rect(30, 150, 120, 38, PANEL, FAINT, 1.5, 6); f.text(90, 174, 'OnRemoved', 12.5, TEXT, 'middle', mono=True)
    f.text(30, 210, 'once, when the entity', 12.5, MUTED); f.text(30, 228, 'leaves the world', 12.5, MUTED)
    return f


def system_or_component():
    f = Fig(720, 340, 'A component is about its own entity; a system handles what spans many entities')
    # a component: one entity
    f.text(180, 40, 'A component', 16, TEAL, 'middle', 'bold')
    f.text(180, 62, 'about its owner, and its own state', 13.5, MUTED, 'middle')
    f.rect(70, 84, 220, 160, SCREEN, FAINT, 1.5, 8)
    f.text(84, 106, 'one entity', 12.5, MUTED)
    for i, n in enumerate(('Health', 'Weapon', 'SeekTarget')):
        f.rect(90, 118 + i * 40, 180, 30, PANEL, TEAL, 1.5, 6)
        f.text(180, 138 + i * 40, n, 13, TEXT, 'middle', mono=True)
    f.text(180, 272, '"has this entity run out of health?"', 13, MUTED, 'middle')
    f.line(360, 24, 360, 300, FAINT, 1)
    # a system: many entities
    f.text(540, 40, 'A system', 16, ACCENT, 'middle', 'bold')
    f.text(540, 62, 'rules across entities, or for the whole run', 13.5, MUTED, 'middle')
    pts = [(430, 120), (500, 96), (560, 136), (630, 108), (466, 186), (540, 206), (616, 178)]
    for x, y in pts:
        f.circle(x, y, 11, PANEL, GLOW, 1.5)
    for a, b in ((0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (2, 5), (0, 4), (3, 6)):
        f.line(*pts[a], *pts[b], ACCENT, 1.2, '3 4')
    f.rect(450, 228, 180, 30, PANEL, ACCENT, 1.5, 6)
    f.text(540, 248, 'CollisionSystem', 13, TEXT, 'middle', mono=True)
    f.text(540, 280, '"which pairs of entities touch?"', 13, MUTED, 'middle')
    f.text(360, 322, 'If a rule would make one entity reach into all the others, it belongs in a system.', 13.5, MUTED, 'middle')
    return f


def object_pool():
    f = Fig(720, 320, 'A pool hands out bullets that are no longer in use, so the game stops allocating new ones')
    f.rect(40, 70, 190, 190, SCREEN, TEAL, 1.5, 8)
    f.text(135, 56, 'the pool', 15, TEAL, 'middle', 'bold')
    for i in range(6):
        f.rect(62 + (i % 3) * 52, 104 + (i // 3) * 60, 40, 18, PANEL, FAINT, 1.5, 9)
    f.text(135, 238, 'bullets waiting', 13, MUTED, 'middle')
    f.rect(490, 70, 190, 190, SCREEN, ACCENT, 1.5, 8)
    f.text(585, 56, 'the world', 15, ACCENT, 'middle', 'bold')
    for x, y, a in ((520, 110, -20), (590, 140, 15), (540, 190, -40), (630, 200, 30)):
        f.add(f'<g transform="rotate({a} {x + 20} {y + 9})">')
        f.rect(x, y, 40, 18, GLOW, r=9)
        f.add('</g>')
    f.text(585, 238, 'bullets in flight', 13, MUTED, 'middle')
    f.curve('M236 120 C 320 70, 400 70, 484 120', TEAL, 2.5)
    f.text(360, 78, 'Get()', 14, TEAL, 'middle', mono=True)
    f.text(360, 112, 'reset it, then fire', 12.5, MUTED, 'middle')
    f.curve('M484 210 C 400 260, 320 260, 236 210', ACCENT, 2.5)
    f.text(360, 228, 'Return()', 14, ACCENT, 'middle', mono=True)
    f.text(360, 262, 'it left the screen', 12.5, MUTED, 'middle')
    f.text(360, 300, 'Only when the pool is empty is a new bullet made. After the first seconds, none are.', 13.5, MUTED, 'middle')
    return f


def flyweight():
    f = Fig(720, 320, 'What every seeker has in common is stored once; each seeker keeps only what is its own')
    f.rect(40, 70, 220, 170, SCREEN, ACCENT, 1.5, 8)
    f.text(150, 56, 'shared, and never changed', 14, ACCENT, 'middle', 'bold')
    f.text(56, 100, 'SeekerEnemyDefinition', 12.5, TEXT, mono=True)
    f.label(56, 126, ['points  2', 'acceleration  1', 'spawn delay  60'], 12.5, MUTED, mono=True, gap=1.5)
    f.rect(56, 190, 34, 34, PANEL, GLOW, 1.5, 4)
    f.path('M63 207 L73 197 L83 207 L73 217 Z', GLOW, 1.5)
    f.text(100, 212, 'one texture', 12.5, MUTED)
    f.text(150, 264, 'intrinsic state', 13, MUTED, 'middle')
    seekers = [(440, 84), (560, 96), (410, 150), (530, 160), (596, 206), (450, 216)]
    for i, (x, y) in enumerate(seekers):
        f.line(264, 150, x - 4, y + 15, FAINT, 1, '3 4')
        f.rect(x, y, 84, 30, PANEL, TEAL, 1.5, 6)
        f.text(x + 42, y + 20, f'({(x * 2) % 900}, {(y * 3) % 500})', 11.5, TEXT, 'middle', mono=True)
    f.text(545, 56, 'per seeker: position, velocity', 14, TEAL, 'middle', 'bold')
    f.text(545, 264, 'extrinsic state', 13, MUTED, 'middle')
    f.text(360, 300, '500 seekers hold 500 references to one definition and one texture.', 13.5, MUTED, 'middle')
    return f


def bloom():
    f = Fig(720, 250, 'Bloom: draw the scene, keep the bright pixels, blur them, and add them back')
    stages = [('the scene', 0), ('bright pixels only', 1), ('blurred', 2), ('added back', 3)]
    blur = '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'
    f.defs['blur'] = blur
    for i, (name, kind) in enumerate(stages):
        ox = 30 + i * 172
        f.rect(ox, 50, 144, 110, SCREEN, r=4)
        shapes = f'<path d="M{ox + 40} 120 L{ox + 60} 80 L{ox + 80} 120 Z" fill="none" stroke="{GLOW}" stroke-width="3"/>' \
                 f'<circle cx="{ox + 106}" cy="{ox * 0 + 96}" r="14" fill="none" stroke="#f08a4b" stroke-width="3"/>'
        if kind in (0, 3):
            f.rect(ox + 14, 64, 24, 14, '#3a4048')
            f.rect(ox + 100, 130, 30, 12, '#3a4048')
        if kind == 2 or kind == 3:
            f.add(f'<g filter="url(#blur)" opacity="{0.95 if kind == 2 else 0.9}">{shapes}{shapes}</g>')
        if kind != 2:
            f.add(shapes)
        f.text(ox + 72, 184, name, 13.5, TEXT, 'middle', 'bold')
        if i < 3:
            f.arrow(ox + 150, 105, ox + 166, 105, MUTED, 2)
    f.text(360, 222, 'Each stage is drawn into a render target, with a pixel shader doing the work.', 13.5, MUTED, 'middle')
    return f


FIGURES = {
    'lifecycle': lifecycle,
    'systems': system_or_component,
    'object-pool': object_pool,
    'flyweight': flyweight,
    'bloom': bloom,
}
