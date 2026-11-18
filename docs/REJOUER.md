# Rejouer la démo et comprendre les mises à jour

[Accueil](../README.md) · [Préparer une sandbox](DEMARRER.md)

**Idempotent** signifie ici : relancer la même préparation retrouve les ressources existantes et applique seulement les changements nécessaires.

Depuis la racine du dépôt, connecté au bon cluster :

```bash
oc whoami --show-server
./setup.sh --avec-exemples
```

## Ce que le script conserve

On peut relancer la même commande sur le même cluster et le même projet :

- Les identifiants S3 et PostgreSQL, les volumes et les utilisateurs existants sont conservés.
- Les champs ajoutés par les opérateurs OpenShift AI sont préservés. Un état inchangé ne déclenche pas un redémarrage de l’atelier ou du modèle.
- Une définition de pipeline est retrouvée par son nom ; sa version dépend de l’empreinte du contenu. Les deux exemples ne sont lancés qu’une fois par version.
- Les fichiers de l’atelier sont installés dans `demo-ventes`. Une source inchangée laisse les fichiers de l’utilisateur en place. Lors d’une mise à jour, les anciens fichiers sont sauvegardés avec un suffixe `.sauvegarde-<empreinte>`.
- Le modèle déployé utilise un chemin S3 immuable calculé à partir de son contenu. Une modification réelle du modèle peut donc provoquer un nouveau déploiement, ce qui est attendu.
- Aucun nettoyage, arrêt de modèle GPU ou renouvellement de clés personnelles n’est exécuté.

Les paramètres gérés par les manifestes sont remis en conformité s’ils ont été modifiés dans le dashboard. Le script ne fusionne pas deux installations concurrentes : utiliser un seul terminal de préparation à la fois. Une exécution de pipeline échouée est conservée pour diagnostic ; elle n’est pas multipliée à chaque relance.

Conserver **un clone local par sandbox** pour séparer les fichiers privés MaaS. Si un utilisateur existait avant ce clone, son mot de passe n’est pas récupérable par le kit : utiliser ses identifiants existants. En cas d’IdP externe, l’administrateur doit fournir l’identité de démonstration. Le script l’indique explicitement.

## En cas de changement de sandbox

Repartir du [guide de démarrage](DEMARRER.md) dans un nouveau clone. Les volumes et les fichiers privés restent sur leur cluster ou leur poste d’origine ; le dépôt transporte les sources, pas les données de travail ni les accès personnels.

## Ce qui a été vérifié

Voir les [résultats et limites de validation](VALIDATION.md). La relance a été testée sur le cluster disponible, et les ventes dans un projet neuf. Une installation complète sur un troisième cluster entièrement neuf reste à valider.
