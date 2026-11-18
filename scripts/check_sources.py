"""Check tracked sources only; never read or print private runtime credentials."""
import ast
import json
from pathlib import Path
import re
import subprocess
import yaml

root = Path(__file__).resolve().parents[1]
tracked = subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
failures = []
for name in filter(None, tracked):
    p = root/name
    if not p.is_file():
        continue
    if any(x in p.parts for x in ['secrets','.venv','node_modules']) or p.suffix in ['.apikey','.password','.kubeconfig']:
        failures.append(name + ': fichier privé suivi par Git')
        continue
    if p.suffix == '.pdf':
        continue
    text = p.read_text()
    for pattern in [r'sha256~[A-Za-z0-9_-]{30,}', r'sk-oai-[A-Za-z0-9_-]{20,}',
                    r'gh[pousr]_[A-Za-z0-9]{25,}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']:
        if re.search(pattern, text):
            failures.append(name + ': motif de secret détecté (valeur masquée)')
    if p.suffix == '.py': ast.parse(text, filename=name)
    if p.suffix == '.sh': subprocess.run(['bash','-n',str(p)],check=True)
    if p.suffix in ['.yaml', '.yml']: list(yaml.safe_load_all(text))
    if p.suffix in ['.json','.ipynb']:
        parsed = json.loads(text)
        if p.suffix == '.ipynb':
            for cell in parsed['cells']:
                if cell['cell_type'] == 'code':
                    assert not cell['outputs'], f'{name}: sorties de notebook à retirer'
if failures:
    raise SystemExit('\n'.join(failures))
print('Sources valides ; aucun motif de secret détecté dans les fichiers suivis.')
