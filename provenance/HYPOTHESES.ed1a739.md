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
