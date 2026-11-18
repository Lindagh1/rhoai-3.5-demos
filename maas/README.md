# Partager un modèle avec MaaS

Depuis la racine du dépôt : `./setup.sh --demo maas`.

Le parcours par défaut utilise la **simulation CPU**, choisie pour conserver le modèle GPU existant. Les contrôles MaaS sont réels. La variante GPU est disponible explicitement avec `MODEL_MODE=real bash scripts/bootstrap.sh` depuis ce dossier, sous réserve d’un GPU libre.

- [Guide de préparation](GUIDE.md)
- [Fiches de démonstration](FEUILLE-DEMO.md)
- [Sources et validation](../docs/VALIDATION.md)

Après le setup, créer les clés dans le dashboard comme utilisateur, puis `make save-key`, `make call`, `make quota-test`, `make show-denials` et `make usage`.
