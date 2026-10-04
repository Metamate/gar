"""Builds the concept figures.

    python tools/figures/build.py            every session
    python tools/figures/build.py 01 06      only these sessions

Each tools/figures/sessionNN.py holds a FIGURES dictionary of name -> function. Every figure is
written as src/assets/sessionNN/fig-<name>.svg for the site, and as a PNG twice that size in
tools/figures/out/NN/ for the decks (not in git: the decks keep their own copy).
"""
import glob, importlib, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

CHROME = [p for p in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                      r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                      shutil.which('google-chrome') or '', shutil.which('chromium') or '') if p and os.path.exists(p)]


def png(svg_path, png_path, width, height):
    """Rasterises with a headless browser, at twice the figure's size."""
    if not CHROME:
        return False
    subprocess.run([CHROME[0], '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                    f'--window-size={int(width)},{int(height)}', '--default-background-color=00000000',
                    f'--screenshot={png_path}', 'file:///' + svg_path.replace('\\', '/')],
                   capture_output=True, timeout=60)
    return os.path.exists(png_path)


def main():
    wanted = sys.argv[1:]
    for path in sorted(glob.glob(os.path.join(HERE, 'session[0-9][0-9].py'))):
        number = os.path.basename(path)[7:9]
        if wanted and number not in wanted:
            continue
        module = importlib.import_module(os.path.basename(path)[:-3])
        assets = os.path.join(ROOT, 'src', 'assets', 'session' + number)
        out = os.path.join(HERE, 'out', number)
        os.makedirs(assets, exist_ok=True)
        os.makedirs(out, exist_ok=True)
        for name, make in module.FIGURES.items():
            fig = make()
            svg_path = os.path.join(assets, f'fig-{name}.svg')
            open(svg_path, 'w', encoding='utf-8', newline='\n').write(fig.svg())
            ok = png(svg_path, os.path.join(out, f'{name}.png'), fig.w, fig.h)
            print(f'{number} {name:24} {fig.w:g} x {fig.h:g}' + ('' if ok else '   (no PNG: no browser found)'))


if __name__ == '__main__':
    main()
