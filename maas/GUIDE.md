# Préparer et diagnostiquer MaaS

[Accueil MaaS](README.md) · [Fiche pour présenter](FEUILLE-DEMO.md) · [Tous les guides](../docs/README.md)

Le kit publie par défaut un **modèle simulé sur CPU**. Les réponses sont synthétiques ; la publication MaaS, les clés, les contrôles d’accès, les quotas et les mesures d’usage fonctionnent réellement. Aucun GPU n’est réservé et les autres modèles ne sont pas arrêtés.

## Nouvelle sandbox

OpenShift AI **3.5.x doit déjà être installé**. La version validée pour ce dépôt est 3.5.3 sur OpenShift 4.20.46. Le script installe ou configure les dépendances MaaS et observabilité disponibles dans les catalogues du cluster : RHCL, Kuadrant, gateway, base de données, COO et OpenTelemetry.

Depuis la racine du dépôt :

```bash
./setup.sh --check --demo maas
./setup.sh --demo maas
```

Le script réutilise les ressources existantes. Il conserve le mot de passe PostgreSQL, la base des clés API, les volumes et l’identité `demo-user`. Il ne crée aucune clé personnelle automatiquement. Les sources de cette partie proviennent de [rhoai-maas-demo](https://github.com/Lindagh1/rhoai-maas-demo), avec les corrections validées sur la deuxième sandbox.

## Identité et clés

**Fournisseur d’identité externe :** le setup s’arrête avant de le modifier. Faire fournir un compte non administrateur et son rattachement au groupe `demo-team` par l’administrateur, puis poursuivre la configuration MaaS manuellement avec les scripts ciblés. Cette adaptation à un IdP d’entreprise n’a pas été validée par le kit ; relancer aveuglément le bootstrap ne la résout pas.

Le bootstrap utilise un HTPasswd existant ou le Keycloak intégré d’une sandbox dédiée. Avec un IdP d’entreprise, il s’arrête : utiliser une identité fournie par l’administrateur. Sans IdP, `ADD_HTPASSWD_IDP=yes ./setup.sh --demo maas` permet d’ajouter celui de démonstration.

Après création, le mot de passe est uniquement dans `maas/secrets/demo-user.password`. Lire ce fichier localement avant le partage d’écran. Si le compte existait déjà, le script le conserve ; il ne récupère ni ne réinitialise son mot de passe. Garder les fichiers privés du clone ayant créé l’identité.

1. Ouvrir OpenShift AI comme `demo-user` dans une fenêtre privée.
2. Dans **Gen AI studio → API keys**, créer une clé pour `demo-quota`, puis une pour `demo-low-quota`.
3. Depuis le dossier `maas`, lancer `make save-key` et saisir les valeurs dans le terminal masqué.
4. Lancer `make call`, `make quota-test`, `make show-denials`, puis `make usage`.

La connexion utilisateur et la création des clés sont les gestes de démonstration conservés dans l’interface. Elles ne sont pas remplacées par une clé administrateur.

## Rejouer

Relancer `./setup.sh --demo maas` depuis la racine. Les ressources convergent vers la configuration du dépôt. Pour remettre volontairement la démonstration à zéro, les commandes de nettoyage demandent `CONFIRM=yes` ; elles ne sont jamais appelées par le setup.

Conserver **un clone local par sandbox** pour séparer ses mots de passe et clés dans `secrets/`. Ces fichiers ne sont jamais envoyés dans GitHub. Les souscriptions utilisent les noms fixes `demo-team`, `demo-quota`, `demo-low-quota` et `demo-access`.

Les fonctions d’observabilité marquées Technology Preview restent présentées comme telles. Le tableau « MaaS démo » est une extension Perses livrée par le dépôt et alimentée par les compteurs réels ; ce n’est pas une fonction de facturation.

## Variante avec un vrai modèle GPU

Le parcours principal reste la simulation CPU. Pour déployer Qwen sur une sandbox avec un GPU libre, consulter la [variante avancée](avance/DEMO-GPU.md). Cette variante change le backend de `maas-demo/demo-llm` ; elle n’est pas nécessaire pour présenter les accès, les quotas et le suivi. Le Llama existant est conservé actif dans le parcours actuel.

## Gouvernance et clés

La souscription `demo-quota` associe `demo-team` au modèle `maas-demo/demo-llm`, avec une limite de 2 000 tokens par minute. L'autorisation `demo-access` permet à ce même groupe d'atteindre le modèle par la gateway. Les deux sont nécessaires.

L'interface propose **Create authorization policy** lors de la création d'une souscription. Si elle est cochée, elle crée une policy associée, généralement nommée `demo-quota-policy`. Pour une création manuelle selon la variante GPU, la décocher et créer `demo-access` dans l’onglet suivant. Dans le parcours CPU, le setup a déjà créé ces ressources : les ouvrir sans les recréer. Ne pas créer les deux policies en parallèle : une policy restante empêcherait de démontrer un refus d'accès.

```bash
make govern
make govern-verify
```

En tant que `demo-user` : **Gen AI studio → API keys → Create API key**. Choisir `demo-quota`, nommer la clé `demo-notebook`, choisir une expiration adaptée à la sandbox et enregistrer la valeur affichée une seule fois. `make save-key` permet sa capture locale. Une seconde clé liée à `demo-low-quota` sert exclusivement au test 429.

## Appeler le modèle sans session admin

Dans un terminal utilisateur ou un workbench, disposer uniquement de `scripts/client.py`, de `curl`, de Python et du fichier de clé. Copier l'URL affichée par `make endpoints` depuis la préparation admin.

```bash
export MAAS_URL=https://maas.apps.<domaine-de-la-sandbox>
python3 scripts/client.py --key-file secrets/demo-user.apikey
```

Le client découvre les modèles accessibles dans `/v1/models`, sélectionne celui du projet de démo, puis appelle `/v1/chat/completions`. Il affiche le statut HTTP, la réponse et les tokens. Il ne nécessite aucun droit Kubernetes. Le secret est transmis à curl par l'entrée standard, pas dans les arguments affichables des processus.

```bash
make traffic
make quota-test
```

Le petit quota est volontairement inférieur à la consommation d'un appel. Le premier appel peut réussir, puis le suivant être refusé : la comptabilisation tient compte des tokens de la réponse. Un quota de tokens n'est pas une limite stricte sur le nombre d'appels ni une facturation.

## Observabilité

Admin : **Observe & monitor → Dashboard → MaaS démo**.

Cet onglet est une extension Perses fournie par le dépôt. Il est intégré au dashboard OpenShift AI et utilise les vrais compteurs Limitador collectés par Prometheus. Il montre les tokens de `demo-quota`, les appels autorisés, les refus du petit quota et une courbe de consommation par modèle/souscription sur des fenêtres de cinq minutes.

Les trois nombres sont des compteurs depuis le démarrage de Limitador, indépendants de la période de graphe sélectionnée. Ils repartent de zéro au redémarrage. La courbe utilise `increase`, donc une estimation Prometheus, susceptible d'extrapolation. Attendre 30 à 60 secondes après les appels, puis Refresh. En absence de série, l'interface indique No data ; ne pas l'interpréter comme une mesure de zéro.

L'onglet natif **Usage** de cette build demande des métriques suffixées `_total` et un label `user`. Les séries observées pour notre démo s'appellent `authorized_hits`, `authorized_calls`, `limited_calls` et portent `subscription`, sans `user`. Le dashboard du kit interroge ces séries réelles sans inventer de données par utilisateur. Le fichier `demo-dashboard.json` devra être adapté si le schéma change dans une autre version.

```bash
make usage
```

Cette commande admin lit les compteurs à travers un port-forward authentifié et sauvegarde `evidence/usage.json`. Comparer l'augmentation de `authorized_hits` aux `total_tokens` des réponses. Ce suivi est destiné à la démonstration et au showback, pas à une facture financière.

Le test optionnel `make show-denials` retire temporairement `demo-team` des bénéficiaires de la policy, attend un refus, restaure les bénéficiaires exacts puis vérifie le retour en 200. Il attend jusqu'à deux minutes par phase pour laisser passer le cache de 60 secondes. Ne pas le lancer en parallèle de `make demo`. Sur cette build, supprimer complètement la policy a laissé une règle obsolète dans la gateway : ne pas utiliser cette suppression comme preuve de révocation. Ce défaut observé est détaillé dans [validation du kit](../docs/VALIDATION.md).

## Diagnostiquer

Pour remettre la configuration déclarative du kit, relancer `../setup.sh --demo maas` depuis ce dossier.

**Remise à zéro volontaire, hors du parcours de présentation :** `make live-reset CONFIRM=yes` retire le modèle, la publication et la gouvernance de démonstration. Cette commande modifie la démo et n’est pas nécessaire pour la rejouer.

Le reset conserve le projet, la plateforme et la base des clés. Il ne supprime aucun PVC partagé ni gateway. Les clés existantes peuvent redevenir utilisables si la même souscription est recréée : les révoquer explicitement si l'objectif est de repartir sans aucune clé. Pour montrer aussi la création d'un projet vide, privilégier une nouvelle sandbox.

**Pending GPU :** concerne la variante avancée. Vérifier la capacité disponible et utiliser une autre sandbox si le GPU doit rester occupé ; le parcours principal fonctionne sur CPU. **ImagePullBackOff :** vérifier l'accès au registre et le pull secret. **403 :** vérifier la clé, son expiration, le groupe, la souscription et la policy. **429 :** attendre la nouvelle fenêtre ou utiliser la clé principale. **Catalogue vide :** vérifier que le projet possède le label `maas.opendatahub.io/gateway-access=true` et que MaaSModelRef est publié.

**TLS intermittent :** vérifier les endpoints du Service de la gateway. Sur la sandbox historique, deux Deployments issus d'un changement de GatewayClass partageaient le même sélecteur ; l'ancien recevait encore du trafic. Il a été réduit à zéro. Cette migration n'existe pas normalement sur une sandbox neuve. Le client réessaie uniquement les échecs de handshake TLS, avant envoi d'une requête HTTP ; il ne répète pas automatiquement une inférence dont la réponse serait perdue.

## Sources et périmètre de validation

- [Red Hat : gouverner les accès LLM avec MaaS, 3.5](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/govern_llm_access_with_models-as-a-service/)
- [Red Hat : observabilité OpenShift AI](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.5/html/managing_openshift_ai/managing-observability_managing-rhoai)
- [Modèle Qwen public](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [API MaaS upstream](https://github.com/opendatahub-io/models-as-a-service/blob/main/maas-api/openapi3.yaml)

## Générer des fiches PDF locales

Depuis `maas`, `make pdf` produit les guides actuels dans `output/pdf/` avec le module Python `markdown` et Chrome ou Chromium disponibles. Pour un support avancé, utiliser `bash scripts/generate_pdf.sh avance/DEMO-GPU.md`. Ces sorties restent locales et doivent être vérifiées visuellement avant diffusion.
