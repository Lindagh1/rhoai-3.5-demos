# État de la plateforme pour la présentation

Audit du 18 novembre 2026, OpenShift AI 3.5.3 / OpenShift 4.20.46. Lecture de la configuration et tests ciblés ; aucune activation de composant, aucun arrêt de modèle. Le [guide oral](PRESENTER-OPENSHIFT-AI-3.5.md) conserve un parcours de 20 minutes.

## Fonctions déjà utilisables

- **Projets, workbenches, connexions, pipelines, déploiement prédictif** : composants actifs ; atelier, serveur de pipelines et modèle de ventes prêts. Le parcours ventes et ses deux exécutions ont été validés pendant la préparation du dépôt.
- **Catalogue** : composant modelregistry actif, `disableModelCatalog=false`, service model-catalog prêt. Il est pertinent de montrer la découverte d’un modèle avant de parler de déploiement. Un catalogue actif ne signifie pas qu’un registre d’équipe existe.
- **Génératif** : `genAiStudio=true`, OGX actif, Llama Ready dans `my-first-model`, service du Playground et pgvector prêts. L’API du backend du Playground a renvoyé HTTP 200 pour le prompt du guide, avec une reformulation des deux scénarios.
- **MaaS** : AI Gateway et Models-as-a-Service actifs ; publication, autorisation et deux souscriptions prêtes. Le backend est le simulateur CPU. Il est distinct du Llama existant et ne prouve pas une génération réelle.
- **Métriques** : stack de monitoring et observabilité du dashboard prêtes ; métriques KServe visibles selon la configuration. Le tableau Perses « MaaS démo » est fourni par le dépôt.

Le test initial depuis le workbench ventes vers le service Playground a été bloqué par la politique réseau de ce projet : elle autorise son propre namespace, le dashboard et l’ingress. Le test a ensuite été effectué dans le pod du backend, sans modifier cette politique. Cela valide la génération côté service ; une répétition du parcours navigateur reste à faire avant le direct.

## Compléments recommandés, dans cet ordre

### 1. Créer et alimenter un registre

Constat : `modelregistry=Managed`, `disableModelRegistry=false`, mais **zéro** ressource `ModelRegistry`.

Il manque une instance, pas un bouton à activer. Dans **Settings → Model resources and operations → Model registry settings**, créer **Modèles du magasin**, puis enregistrer une version de **Prévision des ventes** et définir les permissions utiles. La base intégrée convient à l’évaluation ; la documentation demande une base externe pour la production.

Ce complément rend visible la gestion des versions et des métadonnées entre expérimentation et déploiement. [Créer un registre - documentation 3.5](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/managing_model_registries/creating-a-model-registry_managing-model-registries).

### 2. Ajouter MLflow pour comparer les essais

Constat : condition `MLflowOperatorReady=False`, raison `Removed` ; le composant MLflow du dashboard est Removed. Le serveur de pipelines ventes a son intégration MLflow désactivée.

MLflow apporterait le suivi des paramètres et mesures de plusieurs essais. Préparer son opérateur, son stockage et l’intégration au workbench, puis journaliser deux essais avant de présenter leur comparaison. La présence de `disableTracking=false` dans le dashboard n’active pas le service MLflow.

Le suivi des expériences MLflow est distinct des fonctions de prompts et de traces du Playground qui s’appuient dessus ; vérifier le statut de chaque fonction dans sa documentation. [Installer MLflow](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_mlflow/installing-mlflow_mlflow) ; [suivi depuis les workbenches](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_mlflow/tracking-experiments-with-mlflow-in-workbenches).

### 3. Ajouter les prompts réutilisables et les traces si le public est technique

Constat : `promptManagement` et `genAiTracing` ne sont pas définis ; leur valeur par défaut documentée est false. MLflow est absent.

Après installation des dépendances, préparer des prompts sauvegardés et quelques requêtes tracées. Les traces du Playground permettent d’expliquer les étapes et la latence d’une requête et sont consultées dans MLflow. Le statut `TempoAvailable=False` ne doit pas être utilisé seul pour conclure sur ce parcours : il faut vérifier les prérequis spécifiques documentés.

Ces fonctions sont **Technology Preview**. [Options du dashboard](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/managing_resources/customizing-the-dashboard) ; [traces du Playground](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/how-tracing-works-in-the-playground_rhoai-user).

## Fonctions avancées à traiter séparément

- **RAG** : backend pgvector et embeddings présents, avec un vector store existant. L’import d’un nouveau document et sa restitution n’ont pas été retestés ici. Préparer un document de démonstration et vérifier la recherche avant de montrer Knowledge.
- **Feature store** : Feast actif, aucune instance. Créer un scénario de réutilisation de variables plutôt que de montrer une page vide.
- **Entraînement distribué** : Ray et Trainer actifs ; aucun entraînement distribué n’a été validé pour cette présentation. Le petit modèle de ventes fonctionne sur CPU.
- **Gestion des files GPU** : Kueue désactivé. Utile pour la gestion de capacités partagées, sans nécessité pour ces trois parcours.
- **Évaluation avancée** : TrustyAI actif et interface d’évaluation déployée, mais aucune instance EvalHub ni exécution LMEval. Un menu d’évaluation visible ne constitue pas un service prêt à démontrer.
- **Guardrails** : indicateur absent, false par défaut ; aucune ressource NeMo Guardrails. Prévoir un modèle d’évaluation et un jeu de requêtes de test avant activation.
- **MCP** : aucun catalogue de serveurs pour le Playground configuré via `gen-ai-aa-mcp-servers`. Un connecteur MCP dans OGX ne signifie pas qu’un outil externe est configuré et autorisé.
- **Agents sauvegardés** : aucun indicateur `agentsCatalog` explicite. Cette fonction est Developer Preview dans la documentation ; elle n’est pas nécessaire au parcours de base.

Références complémentaires : [prérequis et MCP](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/playground-prerequisites_rhoai-user), [RAG](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/testing-your-model-with-rag_rhoai-user), [guardrails](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/model-safety-evaluation-in-the-playground_rhoai-user), [statuts Developer Preview](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/release_notes/developer-preview-features_relnotes).

## Refaire l’inventaire sur une nouvelle sandbox

Après `oc login`, depuis la racine du dépôt :

```bash
python3 scripts/audit_presentation.py --project ventes-du-magasin
```

Pour conserver le résultat localement :

```bash
python3 scripts/audit_presentation.py --project ventes-du-magasin --output .state/audit-presentation.json
```

Le script ne lit pas les Secrets et ne modifie aucune ressource. Une valeur `not_explicit` signifie « utiliser la valeur par défaut documentée », pas systématiquement « désactivé ». Une API absente ou inaccessible est signalée ; elle n’est pas assimilée à une liste vide.

Le setup du dépôt couvre les ventes et MaaS CPU. Le Llama et le Playground de la plateforme actuelle étaient déjà présents : leur reconstruction n’est pas encore incluse. Le registre, MLflow, les prompts et les traces sont des compléments recommandés, non des changements appliqués par cet audit.
