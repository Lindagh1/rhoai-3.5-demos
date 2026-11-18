# Présenter OpenShift AI 3.5

**Un magasin de glaces, trois usages de l’IA.** Fiche orale de 20 minutes, hors démarrage des ressources. Vérifiée sur OpenShift AI 3.5.3 le 18 novembre 2026.

## 1. Comprendre la console - 3 minutes

**À dire :** « OpenShift AI permet aux équipes de préparer, entraîner, déployer et utiliser des modèles, avec des ressources et des accès gérés sur OpenShift. » [1]

Le fil conducteur : **prévoir une quantité → rédiger un message → partager une API avec des règles d’accès**. Ce sont trois usages complémentaires. Dans cette démo, le passage de la prévision au texte se fait par copier-coller ; ce n’est pas encore une application qui enchaîne les deux automatiquement.

**Je montre cinq endroits, sans ouvrir tous les menus :**

- **Projects** : le dossier du cas métier. Ouvrir **Ventes du magasin** et pointer les onglets Workbenches, Pipelines, Deployments, Cluster storage et Connections.
- **AI hub → Models → Catalog** : découvrir des modèles existants. Montrer une fiche, son usage, sa licence et ses besoins matériels. Le catalogue n’est pas la liste de nos modèles en fonctionnement.
- **Gen AI studio** : tester des réponses dans Playground, trouver les AI asset endpoints et gérer les API keys.
- **Observe & monitor → Dashboard** : suivre les ressources et les appels.
- **Settings** : montrer le rôle administrateur, notamment les profils matériels et la gouvernance MaaS.

**À dire :** « Un workbench sert à expérimenter. Un pipeline rejoue les étapes. Un déploiement rend le modèle utilisable par une application. »

**Avant le direct :** ouvrir la session administrateur, préparer une fenêtre privée pour `demo-user`, vérifier les modèles Ready et conserver une exécution de pipeline réussie. Ne pas lancer d’installation pendant les 20 minutes.

**Sur cette plateforme :** les ventes tournent sur CPU ; Llama fait la génération réelle sur le GPU ; MaaS utilise un simulateur CPU pour préserver ce GPU. Les contrôles MaaS restent réels.

Références : [1] [Vue d’ensemble officielle](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/getting_started_with_red_hat_openshift_ai_self-managed/overview-for-getting-started_get-started) ; [2] [Catalogue de modèles](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_the_model_catalog/deploying-a-model-from-the-model-catalog_working-model-catalog).

<!-- pagebreak -->

## 2. Le prédictif - 7 minutes

**Question métier : « Combien de glaces préparer pour samedi ? »**

### Ouvrir le projet et sa connexion

**Projects → Ventes du magasin → Connections → Données du magasin.**

**À dire :** « Ce projet regroupe notre travail. La connexion permet d’accéder au stockage sans écrire les identifiants dans le notebook. » Montrer aussi **Cluster storage** : le disque de l’atelier conserve les fichiers ; le stockage S3 partage les données et le modèle. [3]

### Apprendre dans le workbench

**Workbenches → Atelier de prévision → 01_prevoir_les_ventes.ipynb.** Avec le nouveau setup, les fichiers sont dans le dossier `demo-ventes`.

Montrer les données, l’apprentissage et le résultat, sans commenter chaque ligne de code. Nous utilisons 210 jours synthétiques : 168 pour apprendre et les 42 derniers pour tester.

**À dire :** « Le modèle apprend une relation entre météo, week-end, promotion et ventes. Je mesure son erreur sur des jours qu’il n’a pas vus. »

**Résultat à montrer :** environ **7 glaces d’erreur moyenne**, contre **26** pour la moyenne historique. Cela ne signifie pas « 93 % de précision » ni une garantie de rester à ±7.

### Automatiser avec un pipeline

**Pipelines → Prévoir les ventes → une exécution réussie.** Pointer : **préparer → entraîner → évaluer → prévoir**. Ouvrir un résultat ou un journal d’étape. [4]

**À dire :** « Le notebook m’aide à comprendre ; le pipeline permet de refaire le calcul avec les mêmes étapes et des paramètres explicites. »

### Utiliser le modèle déployé

**Deployments → Prévision des ventes**, puis ouvrir **03_utiliser_le_modele.ipynb** dans l’atelier. Le formulaire appelle réellement le service OpenVINO ; il ne réentraîne pas le modèle. [5]

Pour un samedi à **24 °C**, comparer **217 glaces avec promotion** et **172 sans promotion**. Ce sont deux scénarios alternatifs sur des données de démonstration.

**Transition :** « J’ai maintenant une prévision chiffrée. Je vais demander à un modèle génératif de la présenter à un responsable. »

Références : [3] [Connexions](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_on_projects/using-connections_projects) ; [4] [Pipelines](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_ai_pipelines/managing-ai-pipelines_ai-pipelines) ; [5] [Déploiements](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/deploying_models/deploying_models).

<!-- pagebreak -->

## 3. Le génératif - 4 minutes

**Question métier : « Comment expliquer cette prévision à mon responsable ? »**

**Gen AI studio → Playground → projet my-first-model.** Ouvrir le Playground existant et sélectionner le modèle dont le nom contient **llama-32-3b-instruct**. L’identifiant technique peut être préfixé par `vllm-inference-1/`.

**À dire :** « Ici, nous utilisons un modèle de langage déjà entraîné. Nous lui donnons une consigne et du contexte pour produire un texte. Il ne calcule pas notre prévision de ventes. »

### Prompt prêt à copier

> Tu rédiges un message pour le responsable d’un magasin de glaces. Un modèle prédictif a estimé 217 glaces samedi SI une promotion est organisée, OU 172 glaces SANS promotion. Ce sont deux scénarios alternatifs : ne les additionne jamais. Écris deux phrases courtes en français pour expliquer ce choix. Ne crée aucun autre chiffre et ne garantis pas les ventes.

Lire la réponse. Vérifier les deux chiffres et l’absence de total. Puis demander : **« Reformule ce message en une phrase plus simple. »**

**À dire :** « Le prompt change la réponse, sans réentraîner le modèle. Le résultat reste à relire : une réponse fluide peut contenir une erreur. »

### Ce qui est prêt et ce qui est optionnel

Le service du Playground a été testé avec ce prompt : réponse **HTTP 200**, générée par Llama. La formulation exacte peut varier. Le Playground est une fonction **Technology Preview** dans la documentation 3.5. [6]

**Bonus RAG, hors des 20 minutes :** l’onglet **Knowledge** permet d’ajouter des documents pour répondre à partir d’informations propres au magasin. Le backend pgvector est déjà présent ici ; préparer et tester un document avant de montrer ce parcours. Ajouter un document au contexte ne réentraîne pas le LLM. [7]

**Sur une nouvelle sandbox :** le setup du dépôt prépare les ventes et la simulation MaaS. Il ne recrée pas automatiquement ce Llama ni ce Playground. Préparer un modèle génératif compatible et le Playground avant de présenter cette étape. [8]

Références : [6] [Playground](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/playground-overview_rhoai-user) ; [7] [RAG avec des documents](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/testing-your-model-with-rag_rhoai-user) ; [8] [Configurer un Playground](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/configuring-a-playground-for-your-project_rhoai-user).

<!-- pagebreak -->

## 4. MaaS et le suivi - 6 minutes

**Question métier : « Comment donner accès à un modèle à plusieurs équipes ? »**

**À dire :** « MaaS signifie Models-as-a-Service. Le modèle est proposé comme une API : l’administrateur décide qui y accède et avec quelle limite d’usage. » [9]

### Administrateur : donner un accès

**Settings → MaaS governance.** Montrer **Subscriptions → demo-quota** et **Authorization policies → demo-access**.

- La **souscription** associe le groupe `demo-team` au modèle et à une limite de tokens.
- L’**autorisation** permet au groupe d’appeler ce modèle.
- Les deux sont nécessaires : une clé ne remplace pas l’autorisation.

### Utilisateur : utiliser son accès

Dans la fenêtre privée, se connecter comme **demo-user**. Ouvrir **Gen AI studio → API keys → Subscriptions**, puis **API keys**.

Montrer la souscription, puis l’action **Create API key**. Créer et sauvegarder la clé avant le direct si l’on veut éviter d’afficher sa valeur à l’écran. La clé identifie l’appel ; le quota s’applique à la souscription.

Dans le terminal préparé, depuis le dossier `maas`, lancer **make call** : montrer **HTTP 200**. En bonus, **make quota-test** démontre **429** avec la souscription de petit quota. Ne pas multiplier les tests pendant la présentation.

**À annoncer clairement :** « Pour cette partie, le serveur répond avec du texte simulé sur CPU. L’authentification, l’autorisation, le quota et la mesure d’usage sont réellement appliqués. Le Llama vu juste avant n’est pas publié dans cette démonstration MaaS. »

### Administrateur : observer

**Observe & monitor → Dashboard → MaaS démo.** Montrer les appels et les tokens après le test. Le tableau **MaaS démo** est fourni par notre dépôt et utilise les compteurs réels. Laisser le temps aux métriques d’être collectées.

**À dire :** « Je distingue la qualité du modèle, mesurée sur des données de test, de son fonctionnement : appels, délais, erreurs et consommation. Une mesure de tokens ne constitue pas une facture. »

**Phrase de fin :** « Nous avons appris une prévision, utilisé un LLM pour produire du texte, puis montré comment partager une API avec des règles d’accès et du suivi. »

Références : [9] [Utiliser MaaS](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/govern_llm_access_with_models-as-a-service/use-models-as-a-service_maas-deploy) ; [10] [Fonctions Technology Preview, dont certaines fonctions MaaS et d’observabilité](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/release_notes/technology-preview-features_relnotes).

<!-- pagebreak -->

## 5. Rendre la présentation plus complète

**Bilan au 18 novembre 2026 : les fonctions nécessaires au parcours sont actives.** Le manque principal est un registre de modèles réellement créé et alimenté. L’audit a lu la configuration et testé la génération ; il n’a pas activé de nouveaux composants.

### À compléter en priorité : le registre de modèles

Le composant et le catalogue sont activés, mais **aucune instance de registre n’existe**. Créer **Modèles du magasin**, y enregistrer **Prévision des ventes - version 1**, puis montrer ses métadonnées et ses droits d’accès.

**Apport pédagogique :** « Le catalogue m’aide à choisir un modèle ; le registre conserve les références et versions de ceux que mon équipe gère. » Pour la démo, la documentation propose une base par défaut non destinée à la production. [11]

### Pour une deuxième présentation : MLflow

L’opérateur MLflow n’est pas activé. Il apporterait un écran pour comparer les essais, leurs paramètres et leurs mesures. C’est pertinent après le notebook et le pipeline, mais inutile de l’ajouter en urgence au parcours de 20 minutes. [12]

### Pour approfondir le génératif : prompts et traces

La gestion des prompts et les traces du Playground ne sont pas activées. Après préparation de MLflow et des dépendances nécessaires, elles permettraient de conserver des prompts et d’expliquer le déroulement d’une requête. Les options **promptManagement** et **genAiTracing** sont Technology Preview ; activer seulement un bouton ne prépare pas le service derrière. [13] [14]

### À réserver à un autre scénario

**Feature store, entraînement distribué, files d’attente GPU, évaluation avancée, guardrails et MCP** : utiles selon le besoin, mais ils demandent des données, des outils ou des ressources et une vraie démonstration. Les activer tous ne rendrait pas ce parcours plus clair. La génération a été validée en texte ; les images et l’audio sont hors de ce parcours.

**Avant une nouvelle présentation :** vérifier le parcours prédictif, envoyer le prompt, tester une clé MaaS, puis consulter les métriques. Le contrôle technique en lecture seule est disponible dans `scripts/audit_presentation.py`.

Références : [11] [Créer un registre](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/managing_model_registries/creating-a-model-registry_managing-model-registries) ; [12] [Installer MLflow](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_mlflow/installing-mlflow_mlflow) ; [13] [Options du dashboard](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/managing_resources/customizing-the-dashboard) ; [14] [Traces du Playground](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/how-tracing-works-in-the-playground_rhoai-user).

Les clics suivent la documentation officielle 3.5 et les ressources observées sur cette plateforme. Le navigateur n’a pas été utilisé pour une répétition complète de chaque écran. Les temps sont indicatifs ; les 20 minutes excluent le bonus RAG et les compléments de cette page.
