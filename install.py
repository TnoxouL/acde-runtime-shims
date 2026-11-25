import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def bundle() -> str:
    parts = [path.read_text() for path in sorted((HERE / 'shims').glob('*.js'))]
    return '\n'.join(parts)


def install(public: pathlib.Path, prefix: str) -> None:
    (public / 'acde-compat.js').write_text(bundle())
    script = f'<script src="{prefix}acde-compat.js"></script>'
    for page in public.rglob('*.html'):
        text = page.read_text()
        if script in text:
            continue
        text = re.sub(r'<noscript>.*?</noscript>', '', text, flags=re.S)
        page.write_text(text.replace('<head>', f'<head>{script}', 1))


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        sys.exit('用法: install.py <public 目录> [脚本路径前缀，默认 /]')
    install(pathlib.Path(sys.argv[1]), sys.argv[2] if len(sys.argv) == 3 else '/')
