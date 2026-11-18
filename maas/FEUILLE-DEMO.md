# Présenter MaaS simplement

[Accueil MaaS](README.md) · [Préparation et diagnostic](GUIDE.md) · [Présentation complète](../docs/PRESENTER-OPENSHIFT-AI-3.5.md)

**Message à faire passer : « Une équipe utilise un modèle par une API, avec un accès personnel et une limite d’usage. »** Compter 6 à 8 minutes, avec les ressources déjà préparées. Les tests de refus sont des bonus.

**À annoncer :** « Ici, le texte est simulé sur CPU. Nous montrons réellement les clés, les autorisations, les quotas et le suivi. »

## Avant le direct

Préparer deux fenêtres : l’administrateur dans la fenêtre normale, `demo-user` dans une fenêtre privée. Le setup et les identifiants doivent être prêts selon le [guide de démarrage](../docs/DEMARRER.md).

Toutes les commandes suivantes se lancent depuis le dossier `maas` :

```bash
make endpoints
```

Cette commande affiche les adresses du cluster courant. Préparer les clés hors partage d’écran ; on peut montrer leur formulaire et leur liste sans afficher leur valeur.

## 1. Administrateur : montrer le service et l’accès

**Je montre :** le service `demo-llm` dans **Projects → maas-demo → Deployments**, puis **Settings → MaaS governance**.

Ouvrir la souscription **demo-quota** : équipe `demo-team`, modèle `maas-demo/demo-llm`, limite **2 000 tokens par minute**. Ouvrir ensuite l’autorisation **demo-access** pour cette même équipe et ce même modèle.

**À dire :** « La souscription fixe la limite de consommation. L’autorisation donne accès au service. Le setup a préparé les deux ; je vous montre leur configuration. »

**Résultat attendu :** modèle prêt et ressources associées à la même équipe. Il n’est pas nécessaire de les recréer pendant la présentation.

## 2. Utilisateur : obtenir un accès personnel

Dans la fenêtre privée, connecté comme **demo-user**, montrer **Gen AI studio → API keys** et la souscription **demo-quota**. Une clé est créée pour cette souscription ; le petit quota de test utilise une seconde clé liée à **demo-low-quota**.

**À dire :** « Je crée une clé pour mon application. Je n’ai pas besoin d’un accès administrateur au cluster pour appeler le modèle. »

Si les clés viennent d’être créées, les enregistrer localement sans afficher leur valeur :

```bash
make save-key
```

**Résultat attendu :** les deux fichiers privés sont conservés dans `secrets/`, exclu de Git. La valeur d’une clé n’est affichée qu’à sa création dans la console ; fermer cette vue avant de partager l’écran.

## 3. Utilisateur : faire un appel

```bash
make call
```

**Je montre :** le statut **HTTP 200**, la réponse simulée et `total_tokens`.

**À dire :** « Le programme utilise la clé pour s’authentifier. La plateforme vérifie les droits et comptabilise l’usage. »

Le client API peut fonctionner avec seulement l’adresse du service et la clé, sans session administrateur. Les détails sont dans le [guide technique](GUIDE.md#appeler-le-modèle-sans-session-admin).

## 4. Administrateur : suivre les appels

Ouvrir **Observe & monitor → Dashboard → MaaS démo**. Attendre 30 à 60 secondes après l’appel, puis actualiser. Pour produire quelques appels supplémentaires :

```bash
make traffic
make usage
```

**À dire :** « Nous voyons l’activité du service et sa consommation. Ce tableau ne mesure pas la qualité des réponses et ne produit pas une facture. »

Le tableau **MaaS démo** est une extension Perses fournie par le dépôt. Les compteurs proviennent de la plateforme ; en mode simulé, les nombres de tokens viennent des réponses du simulateur. Montrer la variation observée, sans promettre une valeur fixe. **No data** signifie qu’aucune série n’est encore disponible, pas forcément zéro appel.

## Bonus : montrer les limites

**Petit quota — dépassement HTTP 429 :**

```bash
make quota-test
```

Cette commande utilise la seconde clé, liée au petit quota. Un premier appel peut réussir avant le refus suivant : la limite est comptabilisée à partir des tokens de la réponse. Ce n’est pas une limite fixe en nombre de questions.

**Retrait temporaire d’accès — HTTP 403, puis retour en 200 :**

```bash
make show-denials
```

Ce test administrateur modifie temporairement les bénéficiaires de l’autorisation et les restaure. Prévoir plusieurs minutes pour les caches ; ne pas le lancer pendant une autre modification de gouvernance. Le garder hors du parcours court.

## Phrase de conclusion

« Nous avons partagé une API avec une équipe, utilisé une clé personnelle et suivi l’usage dans les limites définies. »

Référence : [utiliser les modèles avec MaaS — documentation officielle 3.5](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/govern_llm_access_with_models-as-a-service/use-models-as-a-service_maas-deploy). Pour déployer et générer avec Qwen, suivre la [variante GPU séparée](avance/DEMO-GPU.md).
