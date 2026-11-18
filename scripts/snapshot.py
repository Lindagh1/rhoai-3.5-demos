"""Capture non-secret identities for an actual rerun comparison. Output is local."""
import hashlib
import json
import subprocess
import sys

def read(kind, ns):
    return json.loads(subprocess.check_output(['oc','get',kind,'-n',ns,'-o','json']))['items']

snapshot = {}
for ns in sys.argv[1:]:
    snapshot[ns] = {}
    for kind in ['pods', 'pvc', 'secrets']:
        result = {}
        for obj in read(kind, ns):
            if kind == 'pods' and obj.get('status', {}).get('phase') in ('Succeeded', 'Failed'):
                continue
            row = {'uid': obj['metadata']['uid']}
            if kind == 'secrets':
                row['digest'] = hashlib.sha256(json.dumps(obj.get('data', {}), sort_keys=True).encode()).hexdigest()
            if kind == 'pods':
                row['restarts'] = sum(c.get('restartCount', 0) for c in obj.get('status', {}).get('containerStatuses', []))
            result[obj['metadata']['name']] = row
        snapshot[ns][kind] = result
print(json.dumps(snapshot, sort_keys=True, indent=2))
