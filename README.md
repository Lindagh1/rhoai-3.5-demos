# Démonstrations OpenShift AI 3.5

Deux parcours simples, conservés dans un dépôt dédié :

- **Ventes du magasin** : projet → connexion → workbench → notebook → pipeline → modèle déployé → formulaire de prévision.
- **Partager un modèle avec MaaS** : publication → souscription → autorisation → clé utilisateur → quota → suivi des appels.

Les ventes utilisent un vrai modèle de régression appris sur des données synthétiques. MaaS utilise par défaut des réponses simulées sur CPU ; ses contrôles d’accès et ses quotas sont réels. Aucun GPU n’est requis par la commande principale.

## Préparer une nouvelle sandbox

Prérequis : **OpenShift AI Self-Managed 3.5.x déjà installé**, accès administrateur, StorageClass par défaut, accès aux images Red Hat et aux catalogues d’opérateurs. Le kit ne provisionne pas un cluster OpenShift et n’installe pas l’opérateur OpenShift AI initial.

Sur le poste : Linux ou macOS, Bash, Git, `oc`, Python 3.12 avec `venv`, `curl`, `make`, `envsubst` et `openssl` ou `htpasswd`. Sous Windows, utiliser WSL. Prévoir une connexion réseau pendant la première préparation.

```bash
gh repo clone Lindagh1/rhoai-3.5-demos
cd rhoai-3.5-demos

# Se connecter à la nouvelle sandbox dans son terminal.
oc login https://API-DE-LA-SANDBOX:6443

# Vérifier la cible et les prérequis, sans modifier le cluster.
./setup.sh --check

# Préparer les deux démos, avec deux exemples de pipeline exécutés.
./setup.sh --avec-exemples
```

Le dépôt étant privé, `gh` doit être connecté à un compte autorisé. `git clone` convient aussi avec l’authentification GitHub habituelle. Le script utilise le contexte `oc` courant, ou le fichier sélectionné par `KUBECONFIG`. Il ne contient aucun jeton de connexion.

Pour ne préparer qu’un parcours :

```bash
./setup.sh --demo ventes --avec-exemples
./setup.sh --demo maas
```

Pour nommer le projet prédictif : `./setup.sh --demo ventes --project mon-magasin`.
Le nom visible reste **Ventes du magasin** ; les noms techniques servent à OpenShift.
Si Python porte un autre nom : `PYTHON_BIN=python3 ./setup.sh --demo ventes` (Python 3.10 à 3.13).

Prévoir environ 20 GiB de volumes pour le parcours ventes et une marge pour les composants de plateforme. Les téléchargements et les installations d’opérateurs peuvent prendre plusieurs dizaines de minutes. Les attentes sont bornées ; en cas d’échec, corriger le prérequis indiqué et relancer la même commande.

## Ouvrir la démo

Pour les ventes, ouvrir **Projects → Ventes du magasin → Workbenches → Atelier de prévision**, puis le dossier **demo-ventes** :

1. `01_prevoir_les_ventes.ipynb` explique et entraîne le modèle.
2. **Pipelines → Prévoir les ventes** montre l’automatisation et les résultats.
3. `03_utiliser_le_modele.ipynb` appelle réellement le modèle déployé depuis un formulaire.

Le script écrit les liens du nouveau cluster dans `.state/<projet>/liens.json`. Sans `--avec-exemples`, il importe le pipeline sans lancer les deux calculs de démonstration.

Pour MaaS, le setup prépare la plateforme et l’identité de démonstration. La connexion comme `demo-user` et la création des clés restent à faire dans le dashboard : c’est la partie utilisateur de la démonstration. Depuis `maas`, `make save-key` conserve les clés localement, puis `make call` teste un appel réel. Voir le [guide MaaS](maas/GUIDE.md).

## Ce que signifie « idempotent » ici

On peut relancer la même commande sur le même cluster et le même projet :

- Les identifiants S3 et PostgreSQL, les volumes et les utilisateurs existants sont conservés.
- Les champs ajoutés par les opérateurs OpenShift AI sont préservés. Un état inchangé ne déclenche pas un redémarrage de l’atelier ou du modèle.
- Une définition de pipeline est retrouvée par son nom ; sa version dépend de l’empreinte du contenu. Les deux exemples ne sont lancés qu’une fois par version.
- Les fichiers de l’atelier sont installés dans `demo-ventes`. Une source inchangée laisse les fichiers de l’utilisateur en place. Lors d’une mise à jour, les anciens fichiers sont sauvegardés avec un suffixe `.sauvegarde-<empreinte>`.
- Le modèle déployé utilise un chemin S3 immuable calculé à partir de son contenu. Une modification réelle du modèle peut donc provoquer un nouveau déploiement, ce qui est attendu.
- Aucun nettoyage, arrêt de modèle GPU ou renouvellement de clés personnelles n’est exécuté.

Les paramètres gérés par les manifestes sont remis en conformité s’ils ont été modifiés dans le dashboard. Le script ne fusionne pas deux installations concurrentes : utiliser un seul terminal de préparation à la fois. Une exécution de pipeline échouée est conservée pour diagnostic ; elle n’est pas multipliée à chaque relance.

Conserver **un clone local par sandbox** pour séparer les fichiers privés MaaS. Si un utilisateur existait avant ce clone, son mot de passe n’est pas récupérable par le kit : utiliser ses identifiants existants. En cas d’IdP externe, l’administrateur doit fournir l’identité de démonstration. Le script l’indique explicitement.

## Fichiers utiles

- [Guide ventes](ventes/LIRE-MOI.md) et [fiche PDF de la répétition initiale](ventes/guides/guide-demo-ventes.pdf).
- [Guide MaaS](maas/GUIDE.md) et [fiches de présentation](maas/FEUILLE-DEMO.md).
- `ventes/manifests`, `ventes/pipelines`, `maas/manifests` : ressources et sources reproductibles.
- [Résultats de validation](docs/VALIDATION.md) : tests effectués et limites connues.

Les dossiers `secrets/`, `.state/`, `.venv/` et les fichiers d’accès au cluster sont exclus de Git. Ne pas ajouter de sorties de notebook contenant des identifiants. Les contrôles GitHub vérifient les sources, les notebooks sans sorties, la syntaxe des scripts et les cas d’idempotence.

## Documentation de référence

Le parcours prédictif s’appuie sur la documentation officielle **3.5** : [projets et connexions](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_on_projects/using-connections_projects), [pipelines](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/working_with_ai_pipelines/managing-ai-pipelines_ai-pipelines) et [déploiement OpenVINO](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/openshift_ai_tutorial_-_fraud_detection_example/t-fdt-deploying-and-testing-a-model).

Les données de ventes et le scénario sont pédagogiques. Cette démonstration couvre le parcours principal de développement et de mise à disposition d’un modèle ; elle ne prétend pas présenter toutes les fonctions d’OpenShift AI 3.5. S4 et les réglages de capacité sont destinés à la démonstration.
