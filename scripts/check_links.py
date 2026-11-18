"""Check local Markdown destinations and heading anchors in tracked documentation."""
from collections import defaultdict
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def prose(text):
    """Remove fenced examples while retaining line numbers for diagnostics."""
    return re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$',
                  lambda match: '\n' * match[0].count('\n'),
                  text, flags=re.MULTILINE | re.DOTALL)


def anchors(text):
    found = set()
    counts = defaultdict(int)
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', prose(text), re.MULTILINE):
        heading = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', heading)
        heading = re.sub(r'<[^>]+>', '', heading)
        slug = re.sub(r'[^\w\-\s]', '', heading.lower()).replace(' ', '-')
        number = counts[slug]
        counts[slug] += 1
        found.add(f'{slug}-{number}' if number else slug)
    return found


def check():
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    failures = []
    checked = 0
    for name in filter(lambda value: value.endswith('.md'), names):
        source = ROOT / name
        if not source.is_file():
            failures.append(f'{name}: fichier suivi absent')
            continue
        text = prose(source.read_text())
        # Inline links and reference definitions. External URLs are deliberately skipped.
        pattern = r'!?\[[^\]\n]*\]\(([^)\n]+)\)|^\s*\[[^\]\n]+\]:\s*(\S+)'
        for match in re.finditer(pattern, text, re.MULTILINE):
            raw = (match[1] or match[2]).strip()
            target = raw.split('>', 1)[0][1:] if raw.startswith('<') else raw.split()[0]
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            line = text.count('\n', 0, match.start()) + 1
            path = unquote(url.path)
            destination = (ROOT / path.lstrip('/') if path.startswith('/') else source.parent / path) if path else source
            destination = destination.resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                failures.append(f'{name}:{line}: chemin introuvable : {target}')
                continue
            if url.fragment and destination.suffix == '.md':
                if unquote(url.fragment) not in anchors(destination.read_text()):
                    failures.append(f'{name}:{line}: ancre introuvable : {target}')
                    continue
            checked += 1
    if failures:
        raise SystemExit('\n'.join(failures))
    print(f'{checked} liens Markdown internes valides (chemins et ancres).')


if __name__ == '__main__':
    check()
