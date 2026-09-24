"""Compare each game repo's GMDCore with the previous session's.

GMDCore is one library that grows through the course: every session keeps the previous
session's core and adds to it (or deliberately changes it). This script lists what each
session adds, changes and removes, and fails if a session removes a file.

Usage: python tools/core-lineage.py [path to the folder with the gmd2-* repos]
       (defaults to ../GMD2Playground next to this repository)
"""
import difflib
import pathlib
import sys

LINEAGE = ['gmd2-flappy', 'gmd2-snake', 'gmd2-platformer', 'gmd2-zelda', 'gmd2-pokemon', 'gmd2-geometrywars']


def core_files(repo):
    core = repo / 'GMDCore'
    return {p.relative_to(core).as_posix(): p for p in core.rglob('*.cs')
            if not {'bin', 'obj'} & set(p.relative_to(core).parts)}


def read(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').splitlines()


def main():
    here = pathlib.Path(__file__).resolve().parent.parent
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent / 'GMD2Playground'
    removed_any = False

    for previous, current in zip(LINEAGE, LINEAGE[1:]):
        old, new = core_files(root / previous), core_files(root / current)
        added = sorted(new.keys() - old.keys())
        removed = sorted(old.keys() - new.keys())
        changed = []
        for name in sorted(old.keys() & new.keys()):
            diff = [line for line in difflib.unified_diff(read(old[name]), read(new[name]), lineterm='', n=0)
                    if line[:1] in '+-' and not line.startswith(('+++', '---'))]
            if diff:
                changed.append(f'{name} ({len(diff)} lines)')

        print(f'{previous} -> {current}')
        for label, items in (('added', added), ('changed', changed), ('REMOVED', removed)):
            if items:
                print(f'  {label}: ' + ', '.join(items))
        if not (added or changed or removed):
            print('  (no changes)')
        removed_any |= bool(removed)

    if removed_any:
        print('\nA session removed files from GMDCore. Keep them, so the core only grows.')
        sys.exit(1)


if __name__ == '__main__':
    main()
