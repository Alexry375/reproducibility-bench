# Banc de reproductibilité — OpenAIRE face aux données de marché

**Ouvert le 2026-08-19.** Confronter ce que la littérature financière affirme à ce que
nos propres données de marché mesurent, en passant par le serveur MCP OpenAIRE
d'Alien Intelligence pour **choisir les publications sur un critère déclaré** plutôt
que sur une intuition.

Contexte : concours OpenAIRE × Alien Intelligence, dépôt jusqu'au 2026-08-20 23:59 CET.
**Rien n'est soumis ni communiqué sans accord explicite d'Alexis.**

## Ordre de lecture

| Ordre | Fichier | Ce que c'est |
|---|---|---|
| 1 | **[HYPOTHESES.md](HYPOTHESES.md)** | Les six prédictions avec leur signe attendu et le critère de verdict, **écrites, commitées et poussées avant que le programme de mesure existe** (commit `ed1a739`). Les corrections ultérieures sont ajoutées en fin de fichier, jamais réécrites par-dessus. C'est la pièce qui rend le banc honnête. |
| 2 | [site/index.html](site/index.html) | La page publiée. Trois bandes : publication → affirmation figée → mesure → verdict. En anglais, le concours étant international. |
| 3 | [site/paper.css](site/paper.css) | La charte graphique, en un seul fichier. Reçue du portable par `machines-bridge` le 2026-08-19, dérivée du tableau de bord holobench. Un seul accent coloré, une seule signification : **l'endroit où la publication et les données ne concordent pas**. Aucun thème sombre, et c'est une décision. |
| 4 | [donnees/LOU_POLK_SKOURAS.json](donnees/LOU_POLK_SKOURAS.json) | Le résultat agrégé : médianes, quartiles, nombre de titres, verdicts pour H1 à H4. |
| 5 | [donnees/appels_mcp.jsonl](donnees/appels_mcp.jsonl) | Les quatre appels au serveur MCP avec leurs arguments exacts et leur réponse brute, pour rejouer la sélection des publications. |

Le programme de mesure vit avec les autres outils de la base :
`data/base_mouvements/outils/35_banc_reproductibilite.py`.

## Ce qui a été mesuré, et ce qui en sort

Trois publications désignées par `openaire_find_by_influence_class(C3, "intraday momentum")`.

| Publication | Affirmation testée | Verdict |
|---|---|---|
| Lou, Polk & Skouras 2019 — *A tug of war* (272 citations) | H1 persistance nocturne | **aucun signal** (ρ médian +0,0017, 51,2 % des titres) |
| — | H2 persistance intraday | **aucun signal** (ρ médian −0,0130, 45,7 %) |
| — | H3 retournement croisé, nuit → séance du jour | **se reproduit** (ρ médian −0,0346, 64,5 %) |
| — | H4 retournement croisé, séance → nuit suivante | **se reproduit** (ρ médian −0,0515, 71,6 %) |
| Korajczyk & Sadka 2002 — *Are Momentum Profits Robust to Trading Costs?* (419 citations) | H5 le coût plancher absorbe l'écart brut | **se reproduit** — écart de +0,63 point sur le témoin, rendement final entre −0,15 % et −0,39 % une fois l'écart acheteur-vendeur payé |
| Sadka 2006 — *…The role of liquidity risk* (661 citations) | H6 | **hors portée, déclaré d'avance** — sa mesure exige le flux d'ordres non anticipé, que nous n'avons pas |

Mesure : corrélation de rang de Spearman **calculée titre par titre**, puis médiane sur
les titres. 2 866 actions américaines, environ 126 séances de février à août 2026,
347 793 journées-titre, sur `data/base_mouvements/six_mois/barres.jsonl.gz`.

## Ce que le banc ne montre pas

- **Ce n'est pas une réplication.** Les études d'origine trient des portefeuilles en
  déciles sur des décennies de données CRSP. Le signe est comparable, la magnitude non.
- Six mois, c'est **une seule configuration de marché**.
- **Une corrélation n'est pas un rendement.** H3 et H4 se reproduisent sans être
  exploitables pour autant — l'arithmétique de la publication 2 est ce qui s'y oppose.

## Effet secondaire sur la base de mouvements

`data/base_mouvements/docs/INDEX.md` affirmait que l'écart entre prix acheteur et prix
vendeur « n'existe nulle part dans la base ». **C'est inexact** : `docs/COUTS_REELS.json`
en contient une mesure sur 173 titres et 1 011 660 barres, qui n'était recensée nulle
part. Corrigé le 2026-08-19.

## Reprise de la charte graphique — 2026-08-19

La première version de la page portait quatre teintes, des cartes flottantes, des
pastilles de verdict et un thème sombre. Elle a été refaite d'après la charte
`paper-style` reçue du portable (archive `2026-08-19_213802` dans `machines-bridge`),
qui est celle du tableau de bord holobench. Dix règles, dont trois qui coûtent quelque
chose :

- **Un seul accent, une seule signification.** Le rouge marque uniquement les
  prédictions qui n'ont laissé aucune trace. Les résultats qui se reproduisent perdent
  leur couleur — une page qui colore ses réussites vend, une page qui colore ses échecs
  audite.
- **Des bandes, pas des cartes.** Un groupe se délimite par deux filets, pas par une
  boîte flottante.
- **Aucun chiffre qui ne vienne d'un artefact vérifiable.** Deux mentions ont été
  retirées à ce titre : « influence C3 — top 1 % », parce que la trace MCP donne la
  classe mais jamais l'échelle en centiles, et un nombre de barres approximatif,
  remplacé par le comptage réel, **28 053 936**.

Contrôles passés, mesurés et non estimés, à 390, 768 et 1 440 pixels de large :
aucun débordement horizontal du corps de la page, aucun texte sous 14 pixels, une seule
teinte hors encre et gris, cinq éléments sur le premier écran.

## Diffusion

Page en ligne : <https://reproducibility-bench.pages.dev/> — projet Cloudflare Pages
`reproducibility-bench`, distinct du site vitrine.
Licence annoncée sur la page : CC BY 4.0, sur le texte, le code et les résultats agrégés.
**Les barres de marché ne sont pas publiées** : elles proviennent d'un flux commercial
dont la redistribution est interdite par contrat.
