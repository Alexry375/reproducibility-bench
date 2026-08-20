# OpenAIRE AI Hackathon 2026 — Submission dossier

## Submission details

| Field | Value |
|---|---|
| **Project title** | Reproducibility Bench — letting a research graph decide which finance results get tested |
| **Participant** | Alexis Briend (solo participant) |
| **Role** | AI / Tech Developer |
| **Theme** | C — Analysis |
| **Live demo** | https://reproducibility-bench.pages.dev/ |
| **Public repository** | https://github.com/Alexry375/reproducibility-bench |
| **Licences** | MIT (code) · CC BY 4.0 (text, methodology, aggregate results) |
| **OpenAIRE access** | OpenAIRE Research Graph via the Alien Intelligence MCP server (`mcp-openaire 0.2.1`) |
| **AI assistance** | Yes — declared in full below |

## 1.1 Overall

Reproducibility Bench asks whether the OpenAIRE Research Graph can be used as a
**selection mechanism** rather than a search box: can it decide *which* published
finance results get tested, on a criterion fixed and logged in advance, so that
the person testing them cannot quietly pick the claims that suit their data?

Three publications were chosen by one logged OpenAIRE call on citation-impact
class. Six testable predictions were extracted, each with an expected sign and a
verdict rule, and **committed to git before the measurement program was
written**. They were then tested against an independent intraday market dataset
the original authors never saw — 2 866 US stocks, ~126 sessions, 28.1 M bars.

**Three predictions reproduce, two leave no measurable trace, and one was
declared out of reach before measurement and stayed that way.** Publishing all
three outcomes together, including the refusal, is the point of the exercise.

## The story

See [STORY.md](STORY.md) for the 1–2 page narrative. In brief:

**The question.** Empirical finance has thousands of published claims about how
prices move. Anyone testing them on their own data picks which ones to test —
and picks after having a rough idea of what the data will say. The result looks
like a test and behaves like a search. The usual remedies are social
(pre-registration, replication teams). We tried an infrastructural one.

**The journey.** OpenAIRE was asked for the top-1 % influence class on
"intraday momentum" and returned the papers; the first three were taken, not
three convenient ones out of five. The graph was then asked a second question —
does each paper have *linked data or software*? Six calls returned zero
relations. That is stated in the only form the evidence supports: *no linked
dataset was returned by the queried OpenAIRE endpoint*. Not "the authors
published no data". But it is exactly why the rest of the bench must exist: for
these three papers, re-running the original analysis on the original data is not
an option available to anyone, so testing the *prediction* on independent data
is the only route left.

**The insight.** Two of them were not clean pass/fail. Lou, Polk & Skouras make
two claims in one breath; the *reversal* half reproduces on a dataset built
years later by a stranger with a cruder method (median ρ −0.035 and −0.052,
carried by 64.5 % and 71.6 % of stocks), while the *persistence* half leaves
nothing (51.2 %, 45.7 % — chance). We refuse to call that a refutation: decile
sorts over decades are not rank correlations over six months. The defensible
claim is narrower and more interesting — *of the two effects, only one survives
being measured badly by someone else*.

Korajczyk & Sadka gave the second surprise. They show momentum profits die
*above* a capital size, because large orders push the price against themselves.
We tested the opposite end of the same curve — $500, where market impact is nil
— and the profit dies there too, for the mirror-image reason: a fixed minimum
commission weighs more the less you commit. An 8 % intraday drop bought and held
to close beats a random-entry control by +0.63 pt and still returns −0.15 % to
−0.39 % once the spread is paid. **The cost curve kills the trade at both ends.**
That result is not in the paper we got it from.

**The reusable contribution.** A pipeline — discover / inspect availability /
freeze / measure / judge / publish — where the two steps most vulnerable to
motivated reasoning (which claims, and what counts as success) are both settled
before any data is read, and both auditable afterwards from a call log and a git
commit. Nothing in it is specific to finance.

## Architecture and method

```
OpenAIRE Research Graph
  └─ Alien MCP server (mcp-openaire 0.2.1, OAuth 2.1 + PKCE)
       ├─ openaire_find_by_influence_class      → which papers          (1 call)
       ├─ openaire_get_research_product_details → metadata, authors     (3 calls)
       └─ openaire_explore_research_relationships → linked data/software (6 calls)
                                   ↓
              HYPOTHESES.md — signs + verdict rule, committed FIRST
                                   ↓
        bench_reproducibility.py — offline, no network, no model, no agent
              per-stock Spearman ρ → median across stocks
                                   ↓
                   lou_polk_skouras.json → published page
```

**Verdict rule, fixed in advance:** `reproduces` if the median sign matches the
prediction **and** at least 55 % of stocks carry that sign.

**Measurement scale:** 2 950 stocks read, 2 866 retained (≥ 60 usable sessions,
open ≥ $2), 347 793 stock-days, 28 053 936 five-minute bars.

## OpenAIRE elements used

| Element | Use |
|---|---|
| Influence class (field-normalised, time-adjusted citation impact) | The selection criterion — C3, top 1 % |
| Research product metadata (DOI, authors, venue, citation counts) | Identifying and attributing the three publications |
| **Typed relations to datasets and software** | Data-availability status per publication |
| MCP tool surface | Made the selection step a logged, replayable call rather than a browsing session |

10 MCP calls in total, all archived with arguments and raw responses in
`results/mcp_calls.jsonl` and `results/mcp_calls_datasets.jsonl`.

## Documentation and reproducibility

- **Fully re-runnable by anyone with an Alien account:** every OpenAIRE call.
- **Not re-runnable with our data:** the measurement. The bars come from a
  commercial feed whose licence forbids redistribution. No bar is published or
  embedded anywhere.
- **Re-runnable with equivalent data:** `measure/bench_reproducibility.py` takes
  any intraday OHLC source with `symbole`, `horodatage`, `ouverture`, `cloture`
  fields. Spearman is implemented in-file; no external dependency.
- **Provenance:** `provenance/HYPOTHESES.ed1a739.md` republishes the exact
  content of the pre-measurement commit with its SHA-256. The README states
  plainly what that proves to a third party and what it does not — the working
  repository is private because it sits next to licensed data, so the timestamp
  itself is not independently verifiable today. No commit was backdated.

## Innovation

The novel element is not "an AI reads papers". It is that **"which papers"
stopped being an unexamined choice.** The selection criterion is one line, it is
stated before the query, and it sits in a log anyone can replay. Adding the
data-availability step turns OpenAIRE's typed relations into a
reproducibility signal in their own right: for these three highly-cited papers,
the endpoint returned no linked data at all — which is precisely the condition
under which a prediction-level test becomes the only test available.

## Limits

- Six months, ~126 sessions, one market, one bar size.
- A rank correlation is far blunter than decile portfolio sorts; absence of
  signal is weak evidence, which is why the verdict is `no measurable trace`
  and never `refuted`.
- The spread measurement covers 173 stocks, so published returns are a ceiling.
- Three publications demonstrate a method; they are not a survey.
- Data availability reflects what one endpoint returned on 2026-08-20.

## AI use — declared

Built by Claude Code (Claude Opus 5) acting as engineer, directed by Alexis
Briend: OpenAIRE calls, measurement program, site, documentation. Two things
were not delegated — the verdict rule and the prediction signs were fixed by
hand before any computation, and every published number was traced back to the
program that produced it. Two model errors (an author misattribution, a wrong
commission figure) were caught in review and are recorded as appended
corrections in `HYPOTHESES.md`, not erased.

## Third-party data

- OpenAIRE Research Graph metadata — redistributed verbatim under OpenAIRE terms.
- Intraday market bars — commercial broker feed, **not redistributed**, no
  sample included.

## Public links

- Demo — https://reproducibility-bench.pages.dev/
- Repository — https://github.com/Alexry375/reproducibility-bench
- Method & results — https://github.com/Alexry375/reproducibility-bench#readme
- Frozen predictions — https://github.com/Alexry375/reproducibility-bench/blob/main/HYPOTHESES.md
- Raw MCP calls — https://github.com/Alexry375/reproducibility-bench/blob/main/results/mcp_calls.jsonl
- Data-availability calls — https://github.com/Alexry375/reproducibility-bench/blob/main/results/mcp_calls_datasets.jsonl
- Aggregate results — https://github.com/Alexry375/reproducibility-bench/blob/main/results/lou_polk_skouras.json

## Confirmations

- [x] Original work produced during the hackathon period.
- [x] All code and content publicly accessible under an open licence.
- [x] No credentials, tokens or personal data in the repository or its history.
- [x] No third-party data redistributed in breach of its licence.
- [x] AI assistance declared.
