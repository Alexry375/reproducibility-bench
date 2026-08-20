"""Banc de reproductibilité — confronter une publication à nos données de marché.

## D'où vient ce programme

Le 2026-08-19, le serveur MCP OpenAIRE d'Alien Intelligence a été branché sur ce
dépôt. Interrogé sur les articles à plus fort impact en matière de continuation de
tendance intra-journalière, il a désigné, entre autres, **Lou, Polk & Skouras (2019),
« A tug of war: Overnight versus intraday expected returns »**, Journal of Financial
Economics, DOI 10.1016/j.jfineco.2019.03.011, 272 citations, classe d'influence C3.

Son affirmation centrale, verbatim : *« We document strong overnight and intraday
firm-level return continuation along with an offsetting cross-period reversal
effect. »* Autrement dit : la nuit prolonge la nuit, la séance prolonge la séance, et
les deux se contrarient l'une l'autre.

Nous possédons de quoi la regarder : `six_mois/barres.jsonl.gz`, 2 950 titres,
28,1 millions de barres de cinq minutes, environ 126 séances de février à août 2026.

## Ce que ce programme mesure

Pour chaque titre, deux séries de rendements journaliers :

```
nuit_t  = ouverture_t / cloture_(t-1) - 1
jour_t  = cloture_t   / ouverture_t   - 1
```

Puis quatre corrélations de rang de Spearman **à l'intérieur de chaque titre** :

```
H1  nuit_t   -> nuit_(t+1)     persistance nocturne        attendu POSITIF
H2  jour_t   -> jour_(t+1)     persistance intraday        attendu POSITIF
H3  nuit_t   -> jour_t         retournement croise         attendu NEGATIF
H4  jour_t   -> nuit_(t+1)     retournement croise         attendu NEGATIF
```

On publie la **médiane des coefficients sur les titres** et la part de titres portant
le signe attendu. Le choix de mesurer titre par titre, plutôt que de mélanger tous les
couples, évite qu'une poignée de titres très agités impose son résultat à l'ensemble.

Les prédictions et leur critère de verdict ont été écrits, commités et poussés
**avant** la première exécution : `recherche/2026-08-19-banc-reproductibilite/HYPOTHESES.md`,
commit `ed1a739`.

## Ce que ce programme ne mesure PAS

- **Ce n'est pas une réplication de l'article.** Lou, Polk et Skouras travaillent sur
  des portefeuilles triés en déciles, sur données CRSP couvrant plusieurs décennies.
  Ici : corrélations en série par titre, sur six mois. Le signe est comparable, la
  magnitude ne l'est pas.
- **Aucun coût de transaction n'entre dans cette mesure.** Une corrélation n'est pas
  un rendement. Le passage à l'argent est traité séparément, par `31_acheter_la_chute.py`
  et `20_couts_reels.py`.
- Le tout premier prix coté d'une séance est parfois un prix mort ; il est ici retenu
  tel quel, parce que c'est la référence d'ouverture qu'emploie la littérature. C'est
  une source de bruit dans `nuit_t`, pas un biais de signe.
- Six mois, c'est une seule configuration de marché.
"""

from __future__ import annotations

import gzip
import json
import pathlib
import statistics

RACINE = pathlib.Path(__file__).resolve().parents[1]
SOURCE = RACINE / "six_mois" / "barres.jsonl.gz"
SORTIE = (RACINE.parents[1] / "recherche" / "2026-08-19-banc-reproductibilite"
          / "donnees" / "LOU_POLK_SKOURAS.json")

PRIX_MIN = 2.0
MIN_JOURS = 60          # couples de journees consecutives exiges par titre
MIN_BARRES_JOUR = 12    # une heure de seance au minimum


def rangs(valeurs: list[float]) -> list[float]:
    """Rangs moyens, ex aequo partages — necessaire pour Spearman."""
    ordre = sorted(range(len(valeurs)), key=lambda i: valeurs[i])
    out = [0.0] * len(valeurs)
    i = 0
    while i < len(ordre):
        j = i
        while j + 1 < len(ordre) and valeurs[ordre[j + 1]] == valeurs[ordre[i]]:
            j += 1
        moyen = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[ordre[k]] = moyen
        i = j + 1
    return out


def spearman(a: list[float], b: list[float]) -> float | None:
    if len(a) < 20:
        return None
    ra, rb = rangs(a), rangs(b)
    ma, mb = statistics.fmean(ra), statistics.fmean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** 0.5
    db = sum((y - mb) ** 2 for y in rb) ** 0.5
    if da == 0 or db == 0:
        return None
    return num / (da * db)


def journees(enr: dict) -> list[tuple[str, int, int]]:
    out, jour, debut = [], None, 0
    for i, horodate in enumerate(enr["d"]):
        j = horodate[:10]
        if jour is None:
            jour, debut = j, i
        elif j != jour:
            out.append((jour, debut, i - 1))
            jour, debut = j, i
    if jour is not None:
        out.append((jour, debut, len(enr["d"]) - 1))
    return out


HYPOTHESES = [
    ("H1", "nuit_t -> nuit_(t+1)", "persistance nocturne", "positif"),
    ("H2", "jour_t -> jour_(t+1)", "persistance intraday", "positif"),
    ("H3", "nuit_t -> jour_t", "retournement croise, meme jour", "negatif"),
    ("H4", "jour_t -> nuit_(t+1)", "retournement croise, jour vers nuit", "negatif"),
]


def principal() -> int:
    coefs: dict[str, list[float]] = {h: [] for h, *_ in HYPOTHESES}
    titres_retenus, titres_lus, journees_totales = 0, 0, 0

    with gzip.open(SOURCE, "rt") as flux:
        for ligne in flux:
            enr = json.loads(ligne)
            titres_lus += 1
            js = [(d, a, b) for d, a, b in journees(enr) if b - a >= MIN_BARRES_JOUR]
            if len(js) < MIN_JOURS + 1:
                continue

            nuit: list[float] = []
            jour: list[float] = []
            for k in range(1, len(js)):
                _, _, f0 = js[k - 1]
                _, d1, f1 = js[k]
                veille, ouv, clot = enr["c"][f0], enr["o"][d1], enr["c"][f1]
                if veille <= 0 or ouv < PRIX_MIN or clot <= 0:
                    nuit.append(float("nan"))
                    jour.append(float("nan"))
                    continue
                nuit.append(ouv / veille - 1)
                jour.append(clot / ouv - 1)

            # on ne garde que les journees ou les deux composantes sont valides
            paires = [(n, j) for n, j in zip(nuit, jour) if n == n and j == j]
            if len(paires) < MIN_JOURS:
                continue
            n = [p[0] for p in paires]
            d = [p[1] for p in paires]
            titres_retenus += 1
            journees_totales += len(paires)

            for cle, serie_a, serie_b in (
                ("H1", n[:-1], n[1:]),
                ("H2", d[:-1], d[1:]),
                ("H3", n, d),
                ("H4", d[:-1], n[1:]),
            ):
                r = spearman(serie_a, serie_b)
                if r is not None:
                    coefs[cle].append(r)

    bilan = {
        "_objet": "test direct de l'affirmation centrale de Lou, Polk & Skouras (2019)",
        "_doi": "10.1016/j.jfineco.2019.03.011",
        "_source_publication": "serveur MCP OpenAIRE d'Alien Intelligence, appel "
                               "openaire_find_by_influence_class(C3, 'intraday momentum')",
        "_hypotheses_figees": "recherche/2026-08-19-banc-reproductibilite/HYPOTHESES.md, "
                              "commit ed1a739, anterieur a cette execution",
        "_donnees": "data/base_mouvements/six_mois/barres.jsonl.gz",
        "_mesure": "correlation de rang de Spearman calculee titre par titre, "
                   "puis mediane des coefficients sur les titres",
        "_avertissement": "ce n'est PAS une replication : l'article trie des "
                          "portefeuilles en deciles sur des decennies de donnees CRSP. "
                          "Le signe est comparable, la magnitude ne l'est pas.",
        "titres_lus": titres_lus,
        "titres_retenus": titres_retenus,
        "journees_titre_exploitees": journees_totales,
        "seuils": {"prix_minimum_dollars": PRIX_MIN,
                   "journees_minimum_par_titre": MIN_JOURS},
        "resultats": {},
    }

    print(f"{titres_lus} titres lus, {titres_retenus} retenus, "
          f"{journees_totales} journees-titre\n")
    print(f"{'':4} {'relation':24} {'attendu':9} {'mediane':>9} {'part signe':>11} "
          f"{'titres':>7}  verdict")
    for cle, relation, libelle, attendu in HYPOTHESES:
        serie = coefs[cle]
        if not serie:
            continue
        med = statistics.median(serie)
        part = (sum(1 for r in serie if r < 0) if attendu == "negatif"
                else sum(1 for r in serie if r > 0)) / len(serie)
        signe_bon = (med < 0) if attendu == "negatif" else (med > 0)
        if signe_bon and part >= 0.55:
            verdict = "confirme"
        elif (not signe_bon) and (1 - part) >= 0.55:
            verdict = "infirme"
        else:
            verdict = "non concluant"
        bilan["resultats"][cle] = {
            "relation": relation, "libelle": libelle, "signe_attendu": attendu,
            "mediane_spearman": round(med, 5),
            "part_titres_signe_attendu": round(part, 4),
            "titres": len(serie),
            "premier_quartile": round(statistics.quantiles(serie, n=4)[0], 5),
            "troisieme_quartile": round(statistics.quantiles(serie, n=4)[2], 5),
            "verdict": verdict,
        }
        print(f"{cle:4} {relation:24} {attendu:9} {med:>9.4f} {part:>10.1%} "
              f"{len(serie):>7}  {verdict}")

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(bilan, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\necrit : {SORTIE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
