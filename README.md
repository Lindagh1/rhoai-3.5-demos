# Découvrir OpenShift AI 3.5

**Un magasin de glaces, trois questions pour comprendre la plateforme.**

1. **Prévoir** — Combien de glaces préparer ? Un modèle apprend sur un historique de ventes.
2. **Expliquer** — Comment présenter la prévision ? Un modèle de langage rédige un message.
3. **Partager** — Comment donner accès à une API ? MaaS gère les accès, les clés et les quotas.

## Par où commencer ?

- **J’ai une nouvelle sandbox** → [Installer les démos, pas à pas](docs/DEMARRER.md).
- **Je dois présenter la plateforme** → [Le déroulé de 20 minutes](docs/PRESENTER-OPENSHIFT-AI-3.5.md) ou sa [fiche PDF](docs/guide-presentation-openshift-ai-3.5.pdf).
- **Je découvre le vocabulaire** → [Comprendre les mots de la démo](docs/COMPRENDRE.md).
- **Je cherche un document précis** → [Le sommaire des guides](docs/README.md).

## Les trois parcours

- [**Ventes : prévoir une quantité**](ventes/README.md) — projet, connexion, workbench, notebook, pipeline et modèle déployé. Apprentissage réel sur des données synthétiques ; CPU uniquement.
- [**Génératif : rédiger un message**](generatif/README.md) — consigne, contexte et réponse dans le Playground. Le Llama déjà présent a été testé ; sur une nouvelle sandbox, le modèle et le Playground sont à préparer séparément.
- [**MaaS : partager une API**](maas/README.md) — administrateur et utilisateur, souscription, clé, appel et quota. Réponses simulées sur CPU ; contrôles d’accès et comptage réels.

**Le setup installe les ventes et MaaS en mode CPU.** Il ne recrée pas le Llama ni son Playground. Le modèle génératif et la simulation MaaS sont deux services distincts.

## Une commande pour préparer, la même pour rejouer

Avec **OpenShift AI Self-Managed 3.5.x déjà installé**, les [outils requis](docs/DEMARRER.md) disponibles et une connexion administrateur au bon cluster :

```bash
git clone https://github.com/Lindagh1/rhoai-3.5-demos.git
cd rhoai-3.5-demos
oc login https://API-DE-LA-SANDBOX:6443
./setup.sh --check
./setup.sh --avec-exemples
```

Le dépôt est **public** : son téléchargement ne demande pas de connexion GitHub. Remplacer l’adresse d’exemple par celle de la nouvelle sandbox. Les clés personnelles MaaS se créent ensuite dans la console, selon le [guide de démarrage](docs/DEMARRER.md).

La préparation peut être relancée. [Ce qu’elle conserve et ce qu’elle met à jour](docs/REJOUER.md) est expliqué séparément.

## Où sont les fichiers ?

```text
docs/          Démarrage, vocabulaire, présentation et références
ventes/        Notebooks, données, pipeline et déploiement prédictif
generatif/     Parcours Playground et consigne prête à utiliser
maas/          Accès à l’API, clés, quotas et observabilité
scripts/       Vérifications et préparation communes
tests/         Contrôles de la réexécution du setup
setup.sh       Point d’entrée pour préparer les deux démos CPU
```

Les variantes GPU sont dans `maas/avance/` ; les supports anciens sont dans `docs/archives/`. Pour modifier les sources, suivre [Contribuer au kit](CONTRIBUTING.md).

## Jusqu’où va cette démo ?

Le kit a été validé sur **OpenShift AI 3.5.3 / OpenShift 4.20.46**. Il s’appuie sur la documentation officielle 3.5, citée dans chaque parcours. Les [résultats de validation](docs/VALIDATION.md) précisent les tests effectués et leurs limites.

Pour compléter la présentation, consulter [les fonctions actives et les ajouts pertinents](docs/ETAT-PLATEFORME-PRESENTATION.md), notamment le registre de modèles et MLflow. Ces ajouts restent à préparer ; ils ne font pas partie de l’installation automatique actuelle.
