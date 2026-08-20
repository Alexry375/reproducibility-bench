# Reproducibility Bench

**Can the OpenAIRE Research Graph pick which finance results to test — before we
know whether we like the answer?**

Live demo: <https://reproducibility-bench.pages.dev/>

OpenAIRE AI Hackathon 2026 · Theme C (Analysis) · Alexis Briend, solo participant

---

## The problem this attacks

Empirical finance has a selection problem that is easy to describe and hard to
escape. There are thousands of published claims about how prices move. Anyone
testing them on their own data picks which ones to test, and picks *after*
having a rough idea of what their data will say. The result looks like a test
and behaves like a search.

The usual fixes are social — pre-registration, replication teams, journals of
negative results. This project tries a different one: **let a public research
graph do the picking, on a criterion stated in advance, and log the call.**

That is what makes OpenAIRE the right instrument here. It is not used as a
search box. It is used as *the selection mechanism itself*, so that the choice
of what to test is an auditable artifact rather than a judgment call.

## The pipeline

**1 · DISCOVER — the graph picks, not us.**
One call, logged verbatim in [`results/mcp_calls.jsonl`](results/mcp_calls.jsonl):

```
openaire_find_by_influence_class(influence_class="C3",
                                 query="intraday momentum", page_size=5)
```

`influence_class` is OpenAIRE's field-normalised, time-adjusted citation impact
class. C3 is the top 1 %. The criterion is stated before the query runs, and the
first three publications returned are the ones tested — not three chosen from
the five for convenience.

**2 · INSPECT DATA AVAILABILITY — is the evidence itself reachable?**
An accessible *paper* is not an accessible *dataset*, and OpenAIRE models the
difference explicitly through typed relations. For each publication we asked the
graph for linked datasets and linked software
([`results/mcp_calls_datasets.jsonl`](results/mcp_calls_datasets.jsonl)):

```
openaire_explore_research_relationships(doi=..., target_type="dataset")
openaire_explore_research_relationships(doi=..., target_type="software")
```

Six calls, six times zero relations returned. We state that result in the only
form the evidence supports: **no linked dataset was returned by the queried
OpenAIRE endpoint.** That is not the same claim as "the authors published no
data", and we do not make the second claim. What it does establish is why the
rest of this pipeline has to exist: for these three papers, re-running the
original analysis on the original data is not an option anyone can take.

**3 · FREEZE — commit the predictions before reading the data.**
Each publication is reduced to testable statements with an expected *sign* and a
verdict rule fixed in advance:

> `reproduces` if the median sign is the predicted one **and** at least 55 % of
> stocks carry that sign.

These were committed to git **before the measurement program was written**.
See [Provenance](#provenance) for what is and is not independently verifiable.

**4 · MEASURE — an independent dataset the authors never saw.**
5-minute bars, 2 950 US stocks, ~126 sessions (Feb–Aug 2026), 28.1 M bars, from
a commercial feed. Per-stock Spearman rank correlation, then the median across
stocks — so that a handful of very agitated stocks cannot speak for the market.

**5 · JUDGE — three verdicts, chosen in advance.**
`reproduces` · `no measurable trace` · `out of reach`.

**6 · PUBLISH — method, code, raw MCP calls, aggregates. No market bars.**

## Results

| # | Prediction | Expected | Median ρ | Share | Verdict |
|---|---|---|---|---|---|
| H1 | overnight → next overnight (persistence) | positive | +0.0017 | 51.2 % | no measurable trace |
| H2 | intraday → next intraday (persistence) | positive | −0.0130 | 45.7 % | no measurable trace |
| H3 | overnight → same-day intraday (reversal) | negative | −0.0346 | 64.5 % | **reproduces** |
| H4 | intraday → next overnight (reversal) | negative | −0.0515 | 71.6 % | **reproduces** |
| H5 | edge before costs is absorbed by costs at $500 | absorbed | — | — | **reproduces** |
| H6 | Sadka's liquidity measure | — | — | — | **out of reach** |

2 866 stocks retained, 347 793 stock-days.

**Lou, Polk & Skouras (2019)** make two claims in one breath. The *reversal*
half reproduces on a dataset built years later, by someone else, with a cruder
method. The *persistence* half leaves nothing behind. We deliberately do not
call that a refutation: their method sorts decile portfolios over decades, ours
is a rank correlation over six months, and a real effect can be invisible at
this resolution. The narrower claim we can defend: **of the two effects, only
one survives being measured badly by a stranger.**

**Korajczyk & Sadka (2002)** show momentum profits die *above* a capital size,
because a large order pushes the price against itself. We tested the opposite
end of the same cost curve — $500, where market impact is nil. The profit dies
there too, for the mirror-image reason: a fixed minimum commission weighs more
the less you commit. Buying an 8 % intraday drop beats a random-entry control by
+0.63 pt, and still returns **−0.15 % to −0.39 %** once the bid–ask spread is
paid. **The cost curve kills the trade at both ends.** That is the finding this
bench produced that is not in the paper it came from.

**Sadka (2006)** was declared **out of reach before any measurement**, not after
a disappointing one. His measure needs unexpected order flow; what we hold is
precisely the component he sets aside as uninformative. Saying so, instead of
answering anyway, is part of the result.

## Provenance

The predictions were committed before the measurement code existed. In the
private working repository:

```
commit  ed1a739560ebd7933bb284963b800b95122ac3dd
date    2026-08-19 17:44:36 +0000
subject figer les affirmations testables AVANT calcul — banc de reproductibilite
        ("freeze the testable claims BEFORE computing")
```

That commit contains `HYPOTHESES.md` and nothing else — no measurement program,
no results. Its exact content is republished here as
[`provenance/HYPOTHESES.ed1a739.md`](provenance/HYPOTHESES.ed1a739.md), with
SHA-256 `5b09916720037d85278b0c11d892ae6d3d3cad75ac49f55eceab3daaafcc452e`.

**Be precise about what this proves.** The working repository is private — it
sits next to licensed market data — so a third party cannot today verify that
timestamp independently. What is publicly checkable is that the republished file
hashes to the value above, and that it contains predictions and no results.
The ordering claim rests on a git history we can open on request. We are not
going to backdate commits in this public repository to make it look stronger
than it is.

`HYPOTHESES.md` at the repository root is the *current* version: the frozen
predictions plus a section appended afterwards recording three corrections —
including an author misattribution we made and fixed. Corrections were appended,
never written over the original.

## Reproducing this

**What you can re-run today:** every OpenAIRE call. The arguments and raw
responses are in `results/mcp_calls*.jsonl`; the server is
`https://openaire.mcp.alien.club/mcp` (`mcp-openaire 0.2.1`), which requires an
Alien account.

**What you cannot re-run with our data:** the measurement. The bars come from a
commercial feed whose licence forbids redistribution. Not one bar is published
here, and none is embedded in the site.

**What you can do instead:** point
[`measure/bench_reproducibility.py`](measure/bench_reproducibility.py) at any
intraday OHLC source. It expects one JSON record per bar with `symbole`,
`horodatage`, `ouverture`, `cloture`; the two lines that matter are

```python
nuit_t = open_t / close_(t-1) - 1
jour_t = close_t / open_t - 1
```

and everything downstream is a rank correlation with no external dependency
(Spearman is implemented in-file; there is no scipy).

## Honest limits

- Six months and ~126 sessions. Short for an asset-pricing claim.
- One market (US equities), one bar size (5 minutes).
- A rank correlation is a much blunter instrument than decile portfolio sorts.
  Absence of signal here is weak evidence, and we label it `no measurable trace`
  rather than `refuted` for that reason.
- The spread measurement covers 173 stocks, not the full universe; published
  returns are therefore a **ceiling**.
- Three publications is a demonstration of a method, not a survey.
- The dataset-availability result covers what one endpoint returned on
  2026-08-20. Other OpenAIRE endpoints or later harvests may return more.

## AI use — declared

This bench was built by [Claude Code](https://claude.com/claude-code) (Claude
Opus 5) acting as the engineer, directed by Alexis Briend: the OpenAIRE calls,
the measurement program, the site and this README. Two things were **not**
delegated: the verdict rule and the prediction signs were fixed by hand before
any computation, and every number published here was traced back to the program
that produced it. Two errors made by the model — an author misattribution and a
wrong commission figure — were caught in review and are recorded in
`HYPOTHESES.md` rather than quietly erased. Stating this plainly seems more
useful to a hackathon about research infrastructure than pretending otherwise.

## Security and licensing

- No credential, token or cookie is in this repository or its history.
- No raw market data, in any form, compressed or otherwise.
- Code (`measure/`, `site/`): **MIT** — see [LICENSE](LICENSE).
- Text, methodology and aggregate results: **CC BY 4.0** — see
  [LICENSE-CC-BY-4.0](LICENSE-CC-BY-4.0).
- OpenAIRE metadata is redistributed under OpenAIRE's own terms; the raw
  responses are kept verbatim for auditability.

## Contents

| Path | What it is |
|---|---|
| `HYPOTHESES.md` | The frozen predictions (French, original artifact) + appended corrections |
| `provenance/HYPOTHESES.ed1a739.md` | Exact content of the pre-measurement commit |
| `measure/bench_reproducibility.py` | The measurement program |
| `results/lou_polk_skouras.json` | Aggregate results: medians, quartiles, verdicts |
| `results/mcp_calls.jsonl` | Discovery calls, arguments and raw responses |
| `results/mcp_calls_datasets.jsonl` | Dataset/software availability calls |
| `STORY.md` | The 1–2 page narrative required by the hackathon |
| `SUBMISSION.md` | The submission dossier — also as [`SUBMISSION.pdf`](SUBMISSION.pdf) |
| `METHOD.fr.md` | Working index of the bench (French) |
| `site/` | Source of the published page |
