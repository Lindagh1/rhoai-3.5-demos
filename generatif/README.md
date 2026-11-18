# Expliquer la prévision avec un modèle de langage

[Accueil](../README.md) · [Présentation complète](../docs/PRESENTER-OPENSHIFT-AI-3.5.md)

**Question métier : comment expliquer la prévision au responsable du magasin ?** Après le calcul des ventes, nous demandons à un LLM de rédiger un court message. Compter 4 minutes, avec le Playground déjà prêt.

## Avant de commencer

Cette partie utilise une **génération réelle**, validée avec le Llama existant `llama-32-3b-instruct` du projet `my-first-model`. Elle conserve le modèle déjà actif sur le GPU.

**Sur une nouvelle sandbox, le setup ne déploie pas ce Llama et ne crée pas son Playground.** L’administrateur doit d’abord disposer d’un modèle compatible accessible au projet, puis préparer le Playground selon la [procédure officielle 3.5](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/configuring-a-playground-for-your-project_rhoai-user). Les noms du modèle et du projet peuvent alors être différents.

Le [Playground est Technology Preview en 3.5](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/playground-overview_rhoai-user). Vérifier une réponse avant le direct. Si le service n’est pas prêt, présenter le principe sans annoncer une démonstration générative fonctionnelle.

## Les gestes à montrer

1. Ouvrir **Gen AI studio → Playground**, choisir le projet et le modèle disponibles. Sur la plateforme de répétition : `my-first-model`, puis le modèle contenant `llama-32-3b-instruct`.
2. Copier la consigne ci-dessous. Les deux chiffres viennent du parcours ventes ; le passage d’un parcours à l’autre est manuel.
3. Lire la réponse et vérifier qu’elle conserve les deux scénarios, sans les additionner.
4. Demander : **« Reformule ce message en une phrase plus simple. »** Comparer les formulations.

## Consigne prête à copier

> Tu rédiges un message pour le responsable d’un magasin de glaces. Un modèle prédictif a estimé 217 glaces samedi SI une promotion est organisée, OU 172 glaces SANS promotion. Ce sont deux scénarios alternatifs : ne les additionne jamais. Écris deux phrases courtes en français pour expliquer ce choix. Ne crée aucun autre chiffre et ne garantis pas les ventes.

**À dire :** « Le modèle prédictif a calculé les quantités. Le modèle de langage nous aide à les expliquer. Changer la consigne change la réponse, sans réentraîner le modèle. »

**Résultat attendu :** un texte utilisant correctement 217 et 172, sans total ni garantie de vente. La formulation peut varier. Une réponse fluide reste à vérifier.

## Pour aller plus loin

Le **RAG** ajoute des documents au contexte pour répondre à partir d’informations propres au magasin. Préparer et tester un document avant de le montrer ; ce n’est pas un réentraînement. Voir la [procédure RAG officielle](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/experimenting_with_models_in_the_gen_ai_playground/testing-your-model-with-rag_rhoai-user).

Passer ensuite à [MaaS](../maas/README.md) pour expliquer le partage d’une API. Dans ce kit, MaaS utilise son propre simulateur CPU : ce Llama n’est pas automatiquement publié dans MaaS.
