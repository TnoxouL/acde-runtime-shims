import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = '<script src="/acde-compat.js"></script>'


def bundle() -> str:
    parts = [path.read_text() for path in sorted((HERE / 'shims').glob('*.js'))]
    return '\n'.join(parts)


def install(public: pathlib.Path) -> None:
    (public / 'acde-compat.js').write_text(bundle())
    for page in public.rglob('*.html'):
        text = page.read_text()
        if SCRIPT in text:
            continue
        text = re.sub(r'<noscript>.*?</noscript>', '', text, flags=re.S)
        page.write_text(text.replace('<head>', f'<head>{SCRIPT}', 1))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('用法: install.py <public 目录>')
    install(pathlib.Path(sys.argv[1]))
