# Affirmations testables — figées AVANT tout calcul

**Écrit le 2026-08-19, avant l'exécution de `35_banc_reproductibilite.py`.**
Ce fichier est la pièce qui rend le banc honnête : les prédictions sont écrites,
signées et horodatées avant de regarder le résultat. Toute modification ultérieure
doit être visible dans l'historique du dépôt.

Les trois publications ont été trouvées **par le serveur MCP OpenAIRE d'Alien
Intelligence**, pas choisies par nous. Traces d'appels dans `donnees/appels_mcp.jsonl`.

## Publication 1 — Lou, Polk & Skouras (2019)

*A tug of war: Overnight versus intraday expected returns*
Journal of Financial Economics · DOI `10.1016/j.jfineco.2019.03.011`
272 citations · influence C3 (top 1 %) · popularité C2 · impulsion C2
Trouvée par : `openaire_find_by_influence_class(influence_class="C3", query="intraday momentum")`

**Ce que l'article affirme** (résumé OpenAIRE, verbatim) : *« We document strong
overnight and intraday firm-level return continuation along with an offsetting
cross-period reversal effect, all of which lasts for years. »*

**Affirmations que nous testons, traduites en prédictions signées :**

| # | Prédiction | Signe attendu |
|---|---|---|
| H1 | Le rendement de nuit d'un titre prédit **positivement** son rendement de nuit suivant (persistance nocturne) | **positif** |
| H2 | Le rendement de séance d'un titre prédit **positivement** son rendement de séance suivant (persistance intraday) | **positif** |
| H3 | Le rendement de nuit prédit **négativement** le rendement de la séance qui suit immédiatement (retournement croisé) | **négatif** |
| H4 | Le rendement de séance prédit **négativement** le rendement de la nuit qui suit (retournement croisé) | **négatif** |

**Mesure** : pour chaque titre, corrélation de rang de Spearman entre les deux séries,
puis **médiane des coefficients sur l'ensemble des titres**. Titres retenus : au moins
60 couples de journées consécutives, prix d'ouverture ≥ 2 $.
Le choix de la médiane par titre, plutôt qu'une corrélation sur tous les couples
confondus, évite qu'un titre très agité impose son résultat à tous les autres.

**Verdict retenu d'avance** : `confirmé` si le signe médian est celui prédit ET si au
moins 55 % des titres portent ce signe. `infirmé` si le signe est inverse dans les
mêmes conditions. `non concluant` entre les deux.

## Publication 2 — Lesmond, Schill & Zhou (2002)

*Are Momentum Profits Robust to Trading Costs?*
DOI `10.2139/ssrn.305282` · 419 citations · influence C3
Trouvée par le même appel.

**Ce que l'article affirme** : les gains des stratégies de continuation de tendance
disparaissent une fois les coûts de transaction réels pris en compte.

| # | Prédiction | Attendu |
|---|---|---|
| H5 | Sur notre échantillon, une règle qui bat le hasard **avant** frais ne le bat plus **après** frais, à 500 $ engagés | l'écart brut est absorbé par les frais |

**Mesure** : résultats déjà produits par `31_acheter_la_chute.py` (chute de 8 % et de
10 %, avec témoin tiré au hasard) et par `20_couts_reels.py` (barème de commissions
Interactive Brokers relu le 2026-08-03). Aucun recalcul : on confronte.

## Publication 3 — Sadka (2006)

*Momentum and post-earnings-announcement drift anomalies: The role of liquidity risk*
Journal of Financial Economics · DOI `10.1016/j.jfineco.2005.04.005`
661 citations · influence C3
Trouvée par le même appel.

**Ce que l'article affirme** : le risque de liquidité — mesuré par la composante non
anticipée du flux d'ordres — explique une part importante des rendements de ces
anomalies.

| # | Prédiction | Attendu |
|---|---|---|
| H6 | Non testable en l'état | **hors portée** |

**Pourquoi, et c'est écrit avant le calcul, pas après** : nos barres sont collectées en
`whatToShow="TRADES"`, c'est-à-dire les prix d'échange seuls. **L'écart entre prix
acheteur et prix vendeur n'existe nulle part dans la base**, et c'est la mesure de
liquidité dont l'article a besoin. Cette absence est déjà consignée dans
`data/base_mouvements/docs/INDEX.md`. Déclarer H6 hors portée est une décision de
méthode, pas un aveu d'échec — un banc qui trouve un résultat sur une donnée qu'il ne
possède pas est un banc faux.

## Corrections postérieures au premier commit — écrites ici, pas effacées ailleurs

**Commit initial : `ed1a739`, 2026-08-19.** Ce qui suit lui est postérieur. Rien n'a
été réécrit au-dessus : la trace de ce qui a changé, et quand, fait partie de la mesure.

### Correction 1 — attribution d'auteurs erronée (aucun effet sur le résultat)

Le premier jet attribuait *Are Momentum Profits Robust to Trading Costs?* à
**Lesmond, Schill & Zhou**. C'est faux. Le serveur MCP donne
**Korajczyk, Robert A. & Sadka, Ronnie**, SSRN Electronic Journal, 2002.
L'erreur venait de la mémoire, pas de la source ; elle a été corrigée en relisant
la réponse de l'outil. Rien d'autre ne change.

Conséquence utile : **Ronnie Sadka est aussi l'auteur de la publication 3**. Les deux
articles sur les coûts et sur la liquidité viennent du même chercheur.

### Correction 2 — le résumé de Korajczyk & Sadka précise l'affirmation

Verbatim : *« The price impact models imply that abnormal returns to portfolio
strategies decline with portfolio size. We calculate break-even fund sizes that lead
to zero abnormal returns. »*

Leur affirmation n'est donc pas « la continuation de tendance ne rapporte rien », mais
**« elle cesse de rapporter au-delà d'une certaine taille de capital »**, parce que
passer un ordre gros déplace le prix. H5 est reformulée en conséquence :

| # | Prédiction | Attendu |
|---|---|---|
| H5 | À 500 $ engagés, l'impact sur le prix est nul, mais le **coût plancher** — commission minimale et écart entre prix acheteur et prix vendeur — absorbe à lui seul l'écart brut mesuré sur nos règles | l'écart brut reste sous le coût |

**L'apport propre du banc, et il n'est pas dans l'article** : la courbe des coûts a
deux extrémités. Korajczyk & Sadka mesurent celle des gros portefeuilles, où le coût
croît avec la taille. Nous mesurons celle du très petit compte, où le coût **décroît**
avec la taille parce qu'une commission plancher de 2,00 $ pèse d'autant plus que le
montant est faible. Le rendement anormal s'annule aux deux bouts.

### Correction 3 — une mesure d'écart acheteur-vendeur existe, contrairement à ce qui était écrit

`data/base_mouvements/docs/INDEX.md` affirme que l'écart entre prix acheteur et prix
vendeur « n'existe nulle part dans la base ». **C'est inexact** :
`docs/COUTS_REELS.json` en contient une, mesurée sur **173 titres et 1 011 660 barres**.
Elle n'était recensée nulle part — exactement le défaut que la règle « un livrable non
listé n'est pas livré » cherche à éviter. À corriger dans l'INDEX.

**H6 reste néanmoins hors portée**, et c'est une décision, pas une commodité : Sadka
mesure la composante **non anticipée du flux d'ordres**, pas l'écart affiché. Nous
n'avons pas le flux d'ordres. Une mesure adjacente est ajoutée sous un numéro distinct,
et déclarée pour ce qu'elle est :

| # | Mesure | Statut |
|---|---|---|
| H7 | Coût complet d'un aller-retour à 500 $ : commission plus écart acheteur-vendeur réel | **formulée après consultation des données** — valeur probante moindre que H1 à H5 |
