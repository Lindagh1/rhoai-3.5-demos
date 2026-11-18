"""Read-only inventory for the platform presentation; never reads Secrets."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo


def read(kind, name=None, namespace=None, all_namespaces=False):
    command = ['oc', 'get', kind]
    if name:
        command.append(name)
    if namespace:
        command += ['-n', namespace]
    if all_namespaces:
        command.append('-A')
    command += ['-o', 'json', '--request-timeout=20s']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        return {'available': False, 'reason': result.stderr.strip()[:250]}
    return json.loads(result.stdout)


def conditions(obj):
    return {c['type']: c.get('status') for c in obj.get('status', {}).get('conditions', [])}


def inventory(kind, namespace=None):
    value = read(kind, namespace=namespace, all_namespaces=namespace is None)
    if 'items' not in value:
        return value
    return [{'name': x['metadata']['name'], 'namespace': x['metadata'].get('namespace'),
             'conditions': conditions(x)} for x in value['items']]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='ventes-du-magasin')
    parser.add_argument('--output', type=Path, help='Optional JSON file for the observed state')
    args = parser.parse_args()
    subprocess.run(['oc', 'whoami'], check=True, stdout=subprocess.DEVNULL)
    dscs = read('datasciencecluster').get('items', [])
    if not dscs:
        raise SystemExit('DataScienceCluster absent ou inaccessible ; audit interrompu.')
    dsc = dscs[0]
    dashboard = read('odhdashboardconfig', 'odh-dashboard-config', 'redhat-ods-applications')
    dsci = read('dscinitialization', 'default-dsci')
    flags = dashboard.get('spec', {}).get('dashboardConfig', {})
    flag_names = ['disableModelCatalog', 'disableModelRegistry', 'disableKServeMetrics',
                  'disableLMEval', 'genAiStudio', 'modelAsService', 'promptManagement',
                  'genAiTracing', 'guardrails', 'agentsCatalog', 'aiAssetCustomEndpoints',
                  'mcpCatalog', 'mcpRegistry']
    result = {
        'observed_at': datetime.now(ZoneInfo('Europe/Paris')).isoformat(timespec='seconds'),
        'read_only': True,
        'components': {k: v.get('managementState', 'not_explicit')
                       for k, v in dsc.get('spec', {}).get('components', {}).items()},
        'component_conditions': conditions(dsc),
        'dashboard_flags': {k: flags.get(k, 'not_explicit') for k in flag_names},
        'monitoring_conditions': conditions(dsci),
        'model_registries': inventory('modelregistries.modelregistry.opendatahub.io'),
        'predictive_and_generative_models': inventory('inferenceservices.serving.kserve.io'),
        'llm_services': inventory('llminferenceservices.serving.kserve.io'),
        'maas_models': inventory('maasmodelrefs.maas.opendatahub.io'),
        'maas_subscriptions': inventory('maassubscriptions.maas.opendatahub.io'),
        'feature_stores': inventory('featurestores.feast.dev'),
        'evaluation_services': inventory('evalhubs.trustyai.opendatahub.io'),
        'guardrails': inventory('nemoguardrails.trustyai.opendatahub.io'),
        'workbenches': inventory('notebooks.kubeflow.org', args.project),
        'pipeline_servers': inventory('datasciencepipelinesapplications.datasciencepipelinesapplications.opendatahub.io', args.project),
        'note': 'not_explicit is not false: consult the documented default. Ready does not prove a user workflow.',
    }
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
        print(f'Audit en lecture seule enregistré : {args.output}')
    else:
        print(text)


if __name__ == '__main__':
    main()
