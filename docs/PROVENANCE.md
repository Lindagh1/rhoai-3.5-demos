# Provenance

Ce dépôt rassemble les sources des deux démonstrations préparées et exécutées sur OpenShift AI 3.5.3, avec les noms simples retenus pour la présentation.

Le module `maas` reprend le dépôt [Lindagh1/rhoai-maas-demo](https://github.com/Lindagh1/rhoai-maas-demo), base `2115124ff0ee23eba4442cdf9eb28169b9e173f9`, et les corrections locales validées : initialisation OGX, observabilité du dashboard, simulation CPU par défaut et conservation d’une identité existante même sans copie locale de son mot de passe. L’ancien dépôt est conservé séparément.

Le module `ventes` reprend les notebooks, données synthétiques, pipeline KFP, connexion S3, export ONNX, serveur OpenVINO et formulaire testés pendant la préparation. Les scripts de génération permettent de modifier le scénario. Les sorties de notebooks sont retirées du dépôt pour conserver une démonstration exécutable sans données d’accès.

Le stockage S4 s’appuie sur le [manifeste du tutoriel officiel de détection de fraude](https://github.com/rh-aiservices-bu/fraud-detection/blob/main/setup/setup-s3-no-sa.yaml). Les images de workbench et de serveur de modèle sont découvertes dans les ressources installées par OpenShift AI 3.5. L’image S4 est figée à l’empreinte testée.

La fiche PDF ventes est le support initial validé. Ses anciens liens ne servent pas de configuration au nouveau kit ; les liens courants sont produits par le setup.

Les journaux bruts, fichiers d’authentification et captures susceptibles d’afficher une clé ne sont pas archivés dans Git. Le compte rendu de validation contient les résultats utiles sans reproduire ces données.
