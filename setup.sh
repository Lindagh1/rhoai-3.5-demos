#!/usr/bin/env bash
# Configure the cluster selected by oc/KUBECONFIG. Never logs in automatically.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
umask 077
DEMO=all
PROJECT=ventes-du-magasin
RUNS=()
CHECK=0
while (($#)); do
  case "$1" in
    --demo) DEMO="${2:?ventes, maas ou all}"; shift 2 ;;
    --project) PROJECT="${2:?nom du projet}"; shift 2 ;;
    --avec-exemples) RUNS=(--example-runs); shift ;;
    --check) CHECK=1; shift ;;
    -h|--help)
      echo 'Usage: ./setup.sh [--demo ventes|maas|all] [--project ventes-du-magasin] [--avec-exemples] [--check]'
      echo 'RHOAI 3.5 déjà installé, oc login administrateur effectué. MaaS : simulation CPU.'
      echo '--check : prérequis en lecture seule ; --avec-exemples : deux exécutions, une seule fois par version.'
      exit 0 ;;
    *) echo "Option inconnue : $1" >&2; exit 2 ;;
  esac
done
[[ "$DEMO" =~ ^(ventes|maas|all)$ ]] || { echo '--demo : ventes, maas ou all'; exit 2; }
for tool in oc python3; do command -v "$tool" >/dev/null || { echo "Outil manquant : $tool"; exit 1; }; done
oc whoami >/dev/null
echo "Cluster sélectionné : $(oc whoami --show-server)"
python3 scripts/preflight.py "$DEMO"
if ((CHECK)); then exit 0; fi

# One writer per local checkout. Cluster mutations remain convergent on rerun.
mkdir -p .state
exec 9>.state/setup.lock
if command -v flock >/dev/null; then
  flock -n 9 || { echo 'Une installation utilise déjà ce dossier.'; exit 1; }
fi
PYTHON_BIN="${PYTHON_BIN:-python3.12}"
command -v "$PYTHON_BIN" >/dev/null || { echo 'Installer Python 3.12, ou définir PYTHON_BIN vers un Python 3.10 à 3.13.'; exit 1; }
"$PYTHON_BIN" -c 'import sys; assert (3,10) <= sys.version_info[:2] <= (3,13), "Python 3.10 à 3.13 requis"'
[[ -x .venv/bin/python ]] || "$PYTHON_BIN" -m venv .venv
WANTED=$(python3 -c 'import hashlib; print(hashlib.sha256(open("requirements-setup.txt","rb").read()).hexdigest())')
if [[ "$(cat .venv/requirements.sha256 2>/dev/null || true)" != "$WANTED" ]]; then
  .venv/bin/python -m pip install --disable-pip-version-check -r requirements-setup.txt
  printf '%s' "$WANTED" > .venv/requirements.sha256
fi
export PATH="$PWD/.venv/bin:$PATH"
if [[ "$DEMO" == maas || "$DEMO" == all ]]; then
  # Explicit CPU mode: never pauses or replaces another model to obtain a GPU.
  export MODEL_MODE=simulator
  bash maas/scripts/bootstrap.sh
fi
if [[ "$DEMO" == ventes || "$DEMO" == all ]]; then
  python ventes/scripts/preparer.py --project "$PROJECT" --deploy-model "${RUNS[@]}"
fi
echo 'Configuration terminée. Vous pouvez relancer exactement la même commande.'
