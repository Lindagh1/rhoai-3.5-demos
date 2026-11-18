# Prévoir les ventes d’un magasin avec OpenShift AI 3.5

Une démonstration de 20 à 25 minutes : « Combien de glaces faut-il préparer pour demain ? »
Le parcours montre un projet, un workbench Jupyter, une connexion S3, un notebook d’apprentissage, un pipeline à quatre étapes, puis un modèle déployé et utilisé par un petit formulaire. Tout fonctionne sur CPU.

Le cas métier et les 210 journées de données sont créés pour cette démonstration. L’apprentissage, l’évaluation et le pipeline sont réels. Ce n’est pas un tutoriel officiel Red Hat sur les ventes ; les actions de plateforme s’appuient sur la documentation officielle OpenShift AI Self-Managed 3.5, référencée en fin de fichier.

## Installer et ouvrir

Depuis la racine du dépôt, après connexion administrateur avec `oc login` :

```bash
./setup.sh --demo ventes --avec-exemples
```

Les liens propres au cluster sont enregistrés dans `.state/ventes-du-magasin/liens.json`.
Dans **Projects → Ventes du magasin → Workbenches → Atelier de prévision**, ouvrir le dossier **demo-ventes**.
Les notebooks sont prêts à exécuter, sans sorties préremplies. Le compte limité `demo-user` de MaaS n’est pas le compte prévu pour cette démonstration.

## Déroulé simple — 20 à 25 minutes

1. **Projet — Ventes du magasin** : « Ici, je rassemble tout ce qui sert à mon cas métier. » Pour montrer la création, créer un autre projet vide dans le dashboard, puis revenir au projet préparé.
2. **Connexion — Données du magasin** : « Les coordonnées et les clés du stockage sont séparées du code. » Montrer son association à l’atelier et au modèle sans afficher les secrets.
3. **Workbench — Atelier de prévision** : Jupyter Data Science CPU Python 3.12, version 3.5 ; stockage persistant de 5 GiB. Expliquer le rôle de l’environnement de travail.
4. Ouvrir **01_prevoir_les_ventes.ipynb** : lire les 210 jours synthétiques, apprendre sur 168 jours, vérifier sur les 42 derniers jours, comparer à une moyenne historique, puis prévoir demain.
5. **Pipelines — Prévoir les ventes** : préparer les données, entraîner, évaluer, prévoir. Montrer les paramètres, les résultats et les journaux. Avec `--avec-exemples`, deux exécutions réussies sont déjà présentes.
6. **Deployments — Prévision des ventes** : modèle ONNX, OpenVINO, CPU, accès interne. Le pipeline calcule une prévision ; le déploiement reste une étape distincte.
7. Ouvrir **03_utiliser_le_modele.ipynb** : lire le stockage S3, appeler l’API, changer la température et la promotion dans le formulaire, montrer le compteur de requêtes, sauvegarder la comparaison.

Le résultat attendu avec ces fichiers est une erreur moyenne proche de **7,0 glaces/jour**, contre **26,2** pour la moyenne historique. Pour le samedi 1 août 2026 du scénario, avec 24 °C et une promotion, le modèle prévoit **217 glaces**. Cette date fixe facilite la répétition ; elle n’est pas le « demain » réel du présentateur. Une MAE de 7 n’est ni une précision de 93 %, ni une garantie de rester dans une marge de plus ou moins 7.

Le pipeline refait les mêmes calculs : **préparer les données → entraîner le modèle → évaluer la qualité → prévoir demain**. L’évaluation est un passage de données vers la dernière étape, pas un seuil automatique d’acceptation. Le cache est désactivé pour que les quatre étapes s’exécutent pendant chaque répétition. Un second lancement avec `promotion=0` donne **172 glaces**, contre **217** avec promotion. Les deux exécutions ont réussi sur la sandbox. Cette différence décrit notre jeu synthétique ; elle ne démontre pas une causalité dans un vrai magasin.

## Stockage et déploiement

Le stockage S4 reprend le principe du tutoriel officiel Red Hat. Il sert à cette démonstration, avec un volume persistant de 5 GiB ; il ne remplace pas un service S3 de production.

L’étape 9 du premier notebook publie `donnees/ventes.csv` et `modeles/ventes/1/model.onnx` via la connexion. Pour un déploiement manuel : **Deploy model → Existing connection → Données du magasin → Path: modeles/ventes → Predictive model → OpenVINO / ONNX**.

Le script automatique utilise un chemin immuable `modeles/versions/<empreinte>` pour le modèle déployé. Il peut ainsi appliquer une nouvelle version sans servir silencieusement un ancien fichier. Exécuter le notebook ne redéploie pas automatiquement le modèle : relancer le setup pour les changements des sources du dépôt, ou choisir explicitement le nouveau chemin dans le dashboard pour ses propres essais.

L’API interne utilise le port **8888**, conformément au tutoriel OpenVINO. Elle n’est pas exposée sur Internet. Le formulaire fonctionne dans le workbench. Le compteur de requêtes et Prometheus montrent l’usage technique ; la MAE du notebook ne constitue pas une surveillance continue de la qualité en production.

## Modifier et régénérer

Les sources et les données synthétiques sont versionnées. Les bibliothèques de calcul sont déjà installées dans l’image du workbench. Le pipeline est compilé avec KFP 2.16.0 ; le setup remplace son image par celle de la version 3.5 installée sur la cible.

Les scripts `build_demo.py`, `build_application.py` et `pipelines/pipeline_ventes.py` permettent de régénérer les notebooks et le YAML. Installer `ventes/requirements.txt`, `nbformat`, `nbclient`, `ipykernel` et `nbconvert` dans un environnement Python 3.12 distinct si l’on souhaite refaire cette génération localement.

La fiche PDF dans `guides/guide-demo-ventes.pdf` conserve le support de la répétition initiale. Ses liens et son nom de projet correspondent à cette ancienne installation : utiliser les liens `.state/<projet>/liens.json` pour une nouvelle sandbox. Les exemples de prédiction et le déroulé restent applicables.

## Périmètre

Cette démo couvre projets, workbenches, stockage persistant, connexions, apprentissage, évaluation, pipelines, déploiement et utilisation d’un modèle. Elle ne montre pas toutes les fonctionnalités de RHOAI 3.5. Le registre de modèles, l’entraînement distribué, le feature store et le suivi de dérive demandent des scénarios supplémentaires. Le module MaaS complète le parcours par le partage d’API, les autorisations et les quotas.

## Documentation officielle 3.5

- [Créer un projet](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/getting_started_with_red_hat_openshift_ai_self-managed/creating-a-project_get-started) : rôle du projet et formulaire de création.
- [Créer un workbench](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/getting_started_with_red_hat_openshift_ai_self-managed/creating-a-workbench-select-ide_get-started) : image, profil matériel, stockage et ouverture de l’IDE.
- [Travailler dans JupyterLab](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_in_your_data_science_ide/working_in_jupyterlab) : fichiers et notebooks.
- [Gérer les pipelines](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_ai_pipelines/managing-ai-pipelines_ai-pipelines) : serveur, compilation KFP et import YAML.
- [Gérer les exécutions](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_ai_pipelines/managing-pipeline-runs_ai-pipelines) : paramètres et exécutions.
- [Consulter les journaux des étapes](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_ai_pipelines/working-with-pipeline-logs_ai-pipelines) : suivi du calcul dans le graphe.
- [Tutoriel officiel et stockage local](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/openshift_ai_tutorial_-_fraud_detection_example/t-fdt-setting-up-a-project-and-storage) : prérequis de stockage. [Manifestes S4 référencés par le tutoriel](https://github.com/rh-aiservices-bu/fraud-detection/blob/main/setup/setup-s3-no-sa.yaml).
- [Créer et utiliser les connexions](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_on_projects/using-connections_projects) : connexion S3 et association au workbench.
- [Déployer et tester le modèle](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/openshift_ai_tutorial_-_fraud_detection_example/t-fdt-deploying-and-testing-a-model) : export ONNX, stockage, OpenVINO, déploiement et appels API.

Sources consultées le 17 novembre 2026. La préparation est effectuée sur RHOAI 3.5.3 / OpenShift 4.20.46. Les libellés peuvent varier selon la langue et les personnalisations du dashboard.
