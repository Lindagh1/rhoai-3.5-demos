# Comprendre les mots de la démo

[Accueil](../README.md) · [Commencer l’installation](DEMARRER.md)

**La question de départ : combien de glaces préparer samedi ?** Chaque élément de la plateforme répond à une étape de ce travail.

## Préparer son espace

- **Projet — le dossier de l’équipe.** Il rassemble le travail sur les ventes. Dans la console : **Ventes du magasin**.
- **Workbench — l’atelier de travail.** On y ouvre JupyterLab et on exécute du code. Dans la console : **Atelier de prévision**.
- **Stockage persistant — le disque de l’atelier.** Il conserve les fichiers quand l’atelier s’arrête puis redémarre.
- **Connexion — les coordonnées du stockage partagé.** Elle fournit l’adresse et les accès sans écrire les clés dans le notebook. Dans la console : **Données du magasin**. Ce n’est pas le stockage lui-même.

## Apprendre et utiliser

- **Notebook — le cahier d’expériences.** Texte, code et résultats se lisent dans l’ordre. Ici, on apprend à prévoir les ventes.
- **Entraînement — apprendre sur des exemples.** Le modèle ajuste ses paramètres à partir de 168 journées synthétiques.
- **Évaluation — vérifier sur d’autres exemples.** Les 42 derniers jours servent au test. La MAE mesure l’écart moyen, en glaces, entre prévision et résultat connu.
- **Pipeline — la recette automatisée.** Il enchaîne préparer, entraîner, évaluer et prévoir. Dans la console : **Prévoir les ventes**.
- **Déploiement — le modèle prêt à répondre.** Une application lui envoie des données et reçoit une prévision. Dans la console : **Prévision des ventes**.
- **Inférence — demander une réponse au modèle.** Le formulaire demande une prévision ; il ne refait pas l’apprentissage.

## Produire du texte et partager l’accès

- **LLM — un modèle de langage.** Il rédige un message à partir d’une consigne. Il peut se tromper : on relit sa réponse.
- **Prompt — la consigne et le contexte.** Ici : expliquer 217 ou 172 glaces sans inventer de chiffre.
- **Playground — l’espace d’essai du modèle.** On change la consigne et on compare les réponses.
- **API — une porte d’entrée pour les applications.** Le notebook ou un programme envoie une demande et reçoit une réponse.
- **MaaS — Models-as-a-Service.** La plateforme permet à des équipes d’utiliser des modèles par une API avec des règles d’accès.
- **Souscription et autorisation.** La souscription définit notamment une limite de consommation ; l’autorisation permet l’accès au modèle. Le kit utilise les deux.
- **Clé API — l’accès personnel du programme.** Elle permet au client de s’authentifier ; elle reste privée.
- **Token — une petite unité de texte.** Les limites MaaS portent ici sur les tokens, pas sur un nombre fixe de questions.
- **Métriques — les compteurs d’activité.** Elles montrent les appels et l’usage ; elles ne prouvent pas que les réponses sont correctes.

## Trois distinctions à garder en tête

**Prédictif :** apprendre une relation pour prévoir une quantité. **Génératif :** produire du texte à partir d’un contexte. **MaaS :** organiser l’accès à un modèle ; ce n’est pas une nouvelle méthode d’apprentissage.

Le **catalogue** aide à découvrir des modèles. Un **registre** conserve les références et versions de modèles d’une équipe. Un **déploiement** exécute un modèle. La présence du catalogue ne signifie donc pas qu’un registre est déjà créé.

Une **réponse simulée** illustre le parcours sans LLM. Dans notre MaaS CPU, les contrôles d’accès sont réels mais le texte est simulé. Dans le Playground validé, Llama produit réellement le texte.

Les gestes et leurs références officielles 3.5 se trouvent dans le [guide de présentation](PRESENTER-OPENSHIFT-AI-3.5.md).
