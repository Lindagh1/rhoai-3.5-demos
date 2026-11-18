# Validation du kit

Vérifications réalisées les 17 et 18 novembre 2026 sur **OpenShift AI 3.5.3 / OpenShift 4.20.46**.

## Installation des ventes dans un projet neuf

La commande `./setup.sh --demo ventes --project ventes-test-installation --avec-exemples` a préparé un projet inexistant au départ :

- stockage S4, volume persistant et bucket S3 ;
- connexion **Données du magasin**, reconnue par OpenShift AI et attachée à l’atelier et au déploiement ;
- workbench **Atelier de prévision**, image Data Science CPU 3.5 découverte dans le cluster ;
- notebooks et données copiés dans le dossier `demo-ventes` ;
- serveur de pipelines Ready, définition **Prévoir les ventes**, expérience **Ventes du magasin** ;
- deux exécutions SUCCEEDED, avec et sans promotion ;
- export ONNX, modèle OpenVINO Ready et requête API depuis le workbench.

Pour 24 °C un samedi : **217 glaces avec promotion**, **172 sans promotion**. Ces résultats proviennent de l’inférence réelle, sur un modèle entraîné avec les données synthétiques du dépôt.

## Réexécution complète

La commande `./setup.sh --project ventes-test-installation --avec-exemples` a ensuite été exécutée avec les deux modules. Une comparaison avant/après a confirmé :

- mêmes UID et compteurs de redémarrage des pods actifs dans le projet ventes, le projet MaaS, l’infrastructure MaaS et le projet du modèle Llama existant ;
- mêmes UID des volumes et secrets ; mêmes empreintes des valeurs des secrets, sans publier les valeurs ;
- mêmes identifiants de pipeline, version, expérience et deux exécutions ;
- API prédictive toujours fonctionnelle ;
- ressources MaaS et observabilité prêtes ; aucune interruption du modèle GPU Llama.

Le test a permis de corriger deux points : le nom du composant 3.5 est `aipipelines`, et l’image du workbench peut être convertie par OpenShift vers son empreinte de plateforme. Le setup préserve cette référence équivalente au lieu de provoquer un redémarrage.

## Fonctions validées avant l’assemblage du dépôt

La répétition initiale des ventes a également validé la lecture/écriture S3, le formulaire ipywidgets, l’export sur 42 journées et la collecte des métriques OpenVINO par Prometheus. La MAE mesurée était d’environ **7,05 glaces/jour**, contre **26,23** pour la moyenne historique ; l’écart maximal introduit par l’export ONNX était inférieur à **0,00002 glace**.

La répétition MaaS en simulation CPU a validé les appels autorisés **HTTP 200**, le refus d’accès **403**, le dépassement de quota **429** et les compteurs d’usage. Ces tests nécessitent les clés personnelles créées dans le dashboard ; le setup ne les crée pas à la place de l’utilisateur. Le test de refus restaure la policy après modification temporaire ; il ne faut pas le lancer pendant une autre modification de gouvernance.

## Contrôles locaux et GitHub

Cinq tests couvrent la préservation des champs injectés par les webhooks, la stabilité des secrets, la protection contre une modification concurrente et la réutilisation des pipelines/exécutions, y compris après un échec et avec plusieurs pages de résultats.

Les contrôles vérifient également la syntaxe Python/Bash, la lecture JSON/YAML, les notebooks sans sorties et les motifs de secrets. Avant publication, les fichiers sélectionnés et le texte du PDF ont été comparés aux identifiants privés connus de la préparation : aucune correspondance. Les journaux bruts et fichiers d’accès sont exclus du dépôt.

## Limites de cette validation

L’installation prédictive a été testée dans **un projet neuf sur le cluster disponible**. MaaS a été réappliqué sur sa plateforme déjà installée. La commande complète n’a pas encore été testée sur un troisième cluster entièrement neuf : les catalogues, certificats, registres, capacités et fournisseur d’identité peuvent y demander un ajustement.

La cible attend OpenShift AI 3.5 déjà installé, une StorageClass par défaut et le profil matériel `default-profile`. Les scripts MaaS utilisent les noms standards `default-dsc` et `default-dsci`. Les images et les adresses de la cible sont découvertes au lancement.

Le script ne présente pas la simulation MaaS comme une véritable génération LLM. Le service prédictif reste interne, sans authentification supplémentaire dans ce projet de démonstration. S4 et le dimensionnement ne constituent pas une architecture de production.
