# Modifier le kit sans perdre le fil pédagogique

[Accueil](README.md) · [Sommaire des guides](docs/README.md)

Le parcours principal doit rester facile à rejouer : **ventes sur CPU, génération dans un Playground préparé séparément, puis MaaS simulé sur CPU**.

## Où modifier ?

- **Explications et déroulé :** `docs/`, `ventes/README.md`, `generatif/README.md`, `maas/FEUILLE-DEMO.md`.
- **Notebook d’apprentissage et données synthétiques :** `ventes/scripts/build_demo.py`, qui produit le notebook 01, `ventes.csv` et la copie de `exporter_modele.py`.
- **Formulaire de prévision :** `ventes/scripts/build_application.py`, qui produit le notebook 03.
- **Pipeline :** `ventes/pipelines/pipeline_ventes.py`, qui compile `ventes/pipeline_ventes.yaml`.
- **Publication du modèle prédictif :** `ventes/scripts/exporter_modele.py` est la source ; `ventes/exporter_modele.py` en est une copie livrée au notebook.
- **Préparation :** `setup.sh`, `scripts/`, `ventes/scripts/preparer.py` et `maas/scripts/`.
- **Ressources OpenShift :** `ventes/manifests/` et `maas/manifests/`.

Les noms et chemins des notebooks sont conservés pour les installations existantes. **01 : apprendre → 02 : passer dans Pipelines → 03 : utiliser le modèle.** Il n’y a pas de notebook 02.

## Garder les sources et les fichiers générés cohérents

Pour les notebooks, modifier le générateur puis régénérer le fichier livré. Utiliser un environnement Python 3.12 dédié avec les dépendances du [parcours ventes](ventes/README.md). Vérifier le diff : ne pas conserver de sorties de cellules ni de données d’accès.

Pour le pipeline, conserver KFP 2.16.0, version utilisée par le kit. Le setup remplace l’image compilée par celle découverte sur le cluster cible.

Pour la fiche PDF globale : modifier `docs/PRESENTER-OPENSHIFT-AI-3.5.md`, puis exécuter `python scripts/build_presentation_guide.py` avec ReportLab et Liberation Sans disponibles. Le résultat est dans `output/pdf/`. Vérifier visuellement les pages avant de remplacer `docs/guide-presentation-openshift-ai-3.5.pdf`. Les documents archivés ne sont pas les supports actuels.

## Vérifier avant de pousser

Depuis la racine, dans un environnement Python avec les dépendances de `requirements-setup.txt` :

```bash
python -m unittest discover -s tests -v
python scripts/check_sources.py
python scripts/check_links.py
git diff --check
```

Les contrôles inspectent les fichiers suivis par Git : ajouter les nouveaux fichiers choisis à l’index avant la vérification finale. `check_links.py` vérifie les chemins et ancres des liens Markdown internes ; il n’interroge pas les sites externes. GitHub exécute aussi ces contrôles à chaque push.

Les tests locaux ne prouvent pas qu’un nouveau cluster peut démarrer tous les composants. Pour une modification du setup, vérifier le comportement sur la cible et documenter le périmètre réellement testé dans [VALIDATION.md](docs/VALIDATION.md).

## Règles de rédaction

Une fiche de présentation indique **la question métier**, **où cliquer**, **quoi dire** et **le résultat attendu**. Les détails d’administration restent dans les guides dédiés. Citer la documentation officielle **3.5** pour les gestes de plateforme.

Toujours distinguer les données synthétiques, les calculs réels et les réponses simulées. Une fonction présente dans un menu n’est pas forcément configurée pour la démonstration.

Les dossiers `secrets/`, `.state/`, `.venv/` et les fichiers d’accès au cluster restent locaux. Les adresses courantes sont découvertes pendant la préparation, pas copiées depuis une ancienne sandbox.
