# Partager un modèle avec MaaS

[Accueil](../README.md) · [Préparer une sandbox](../docs/DEMARRER.md)

**Question métier : comment donner accès à une API à plusieurs équipes, avec une limite d’usage ?** MaaS signifie *Models-as-a-Service*. L’administrateur prépare le service ; l’utilisateur crée sa clé et l’appelle.

Le parcours utilise la **simulation CPU** pour conserver le GPU de Llama. Les réponses sont synthétiques ; les clés, autorisations, quotas et compteurs fonctionnent réellement.

## Dans quel ordre ?

1. **Préparer**, depuis la racine : `./setup.sh --demo maas`.
2. **Créer les clés**, dans le dashboard avec le compte `demo-user` : une pour `demo-quota`, une pour `demo-low-quota`.
3. **Présenter** avec la [fiche pas à pas](FEUILLE-DEMO.md) : accès → clé → appel → quota → suivi.

Le setup a déjà créé le projet `maas-demo`, le service `demo-llm`, le groupe `demo-team`, les souscriptions et l’autorisation `demo-access`. Dans la présentation, appeler simplement ces éléments **le service partagé**, **l’équipe**, **le quota principal** et **le petit quota de test**, tout en gardant les noms techniques visibles pour se repérer.

## Pour approfondir

- [Préparation, identité et diagnostic](GUIDE.md).
- [Résultats et limites de validation](../docs/VALIDATION.md).
- [Variante avancée avec un vrai modèle GPU](avance/DEMO-GPU.md) et [son scénario vidéo](avance/VIDEO-GPU.md).

Pour la génération réelle dans le Playground, suivre le [parcours génératif](../generatif/README.md). Le Llama existant n’est pas automatiquement publié par ce module MaaS.
