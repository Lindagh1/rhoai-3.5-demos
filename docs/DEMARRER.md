# Préparer une nouvelle sandbox

[Accueil](../README.md) · [Tous les guides](README.md)

**Objectif : retrouver deux démos prêtes, les ventes et MaaS, sans utiliser de GPU.** La préparation se fait avant la présentation. Elle peut prendre plusieurs dizaines de minutes lors des premiers téléchargements.

## 1. Vérifier ce dont on dispose

Sur le cluster : **OpenShift AI Self-Managed 3.5.x déjà installé**, un accès administrateur, une classe de stockage par défaut et l’accès aux images et catalogues Red Hat. Le profil matériel `default-profile` doit être disponible. Le kit ne crée pas le cluster et n’installe pas l’opérateur OpenShift AI initial.

Sur le poste : Linux ou macOS, Bash, Git, `oc`, Python 3.12 avec `venv`, `curl`, `make`, `envsubst`, et `openssl` ou `htpasswd`. Sous Windows, utiliser WSL. Les dépendances Python du setup sont installées automatiquement dans `.venv`.

Prévoir environ **20 GiB de volumes pour les ventes**, plus la capacité nécessaire aux composants de plateforme. Aucun GPU n’est demandé par le parcours principal.

## 2. Télécharger le kit et choisir le cluster

Utiliser **un clone local par sandbox** : les clés MaaS de deux environnements doivent rester séparées.

```bash
git clone https://github.com/Lindagh1/rhoai-3.5-demos.git
cd rhoai-3.5-demos
oc login https://API-DE-LA-SANDBOX:6443
oc whoami --show-server
```

Remplacer l’adresse d’exemple par l’API fournie avec la sandbox. Vérifier l’adresse affichée avant de poursuivre. Le setup utilise cette connexion ou le fichier choisi par `KUBECONFIG`.

## 3. Vérifier, puis préparer

```bash
./setup.sh --check
./setup.sh --avec-exemples
```

La première commande vérifie les prérequis sans modifier le cluster. La seconde configure les deux démos, importe le pipeline et lance les deux exemples prédictifs. **Résultat attendu :** le message « Configuration terminée ».

Les autres choix, à utiliser seulement si nécessaire :

```bash
# Seulement les ventes, avec les deux exemples.
./setup.sh --demo ventes --avec-exemples

# Seulement MaaS, en simulation CPU.
./setup.sh --demo maas

# Choisir le nom technique du projet ventes.
./setup.sh --demo ventes --project mon-magasin --avec-exemples
```

Le nom visible du projet reste **Ventes du magasin**. Sans `--avec-exemples`, le pipeline est importé sans lancer les deux calculs. Si Python 3.12 porte un autre nom, utiliser `PYTHON_BIN=python3 ./setup.sh --avec-exemples` avec un Python 3.10 à 3.13.

## 4. Ouvrir les ventes

Les liens du cluster sont dans `.state/ventes-du-magasin/liens.json` ; remplacer `ventes-du-magasin` si un autre nom technique a été choisi.

Dans OpenShift AI : **Projects → Ventes du magasin → Workbenches → Atelier de prévision**. Ouvrir le dossier **demo-ventes**.

1. Exécuter `01_prevoir_les_ventes.ipynb` : comprendre les données, l’apprentissage et l’erreur moyenne.
2. Dans **Pipelines → Prévoir les ventes**, retrouver les deux exécutions réussies, avec et sans promotion.
3. Dans **Deployments**, vérifier **Prévision des ventes : Ready**.
4. Exécuter `03_utiliser_le_modele.ipynb` : le formulaire appelle ce modèle. À 24 °C, un samedi, comparer **217 glaces avec promotion** et **172 sans promotion**.

Le numéro 02 correspond au passage dans **Pipelines** : il n’y a pas de notebook manquant. Le [parcours ventes](../ventes/README.md) explique chaque geste.

## 5. Préparer l’utilisateur MaaS

Le setup prépare le modèle simulé et la gouvernance. **La création des clés personnelles reste un geste utilisateur dans la console.**

1. Avant le partage d’écran, retrouver les identifiants de `demo-user`. Si le kit a créé le compte, son mot de passe est dans `maas/secrets/demo-user.password`. Si le compte existait, utiliser ses identifiants existants.
2. Ouvrir une fenêtre privée, se connecter comme `demo-user`, puis ouvrir **Gen AI studio → API keys**.
3. Créer une clé liée à `demo-quota`, puis une autre liée à `demo-low-quota` pour le test de limite.
4. Depuis la racine du dépôt, saisir les clés dans le terminal masqué, puis tester :

```bash
cd maas
make save-key
make call
```

**Résultat attendu : HTTP 200**, une réponse simulée et un nombre de tokens. Suivre ensuite la [fiche MaaS](../maas/FEUILLE-DEMO.md) pour la limite et le suivi. Pour un fournisseur d’identité d’entreprise ou un mot de passe manquant, consulter le [guide MaaS](../maas/GUIDE.md).

## 6. Répéter avant de présenter

- Les ventes répondent dans le formulaire et les deux pipelines ont réussi.
- La clé MaaS permet un appel ; les métriques apparaissent après leur collecte.
- Pour inclure le génératif, un LLM compatible et son Playground doivent être disponibles : suivre le [parcours génératif](../generatif/README.md). Le setup ne les recrée pas.

Ouvrir ensuite le [déroulé de présentation de 20 minutes](PRESENTER-OPENSHIFT-AI-3.5.md).

## Si la préparation s’arrête

Lire le premier message d’erreur, corriger le prérequis puis relancer **la même commande**. Les ressources déjà prêtes sont réutilisées ; les temps d’attente ne sont pas illimités. Voir [rejouer et mettre à jour](REJOUER.md) pour les fichiers conservés, les sauvegardes et les limites de cette réexécution.

**Image de notebook indiquée « Deleted » :** le setup recherche une image 3.5 disponible sur le cluster. Relancer le setup du projet concerné ; un changement effectif d’image peut redémarrer le workbench. En cas d’erreur de téléchargement, vérifier l’accès aux registres avant de relancer.
