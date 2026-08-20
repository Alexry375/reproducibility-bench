# A Reproducibility Bench: OpenAIRE meets proprietary market data

**OpenAIRE × Alien Intelligence AI Hackathon 2026 — Track: Analyse**
Live page: <https://reproducibility-bench.pages.dev/> · Licence: CC BY 4.0

## The problem this addresses

Quantitative finance has a well-known asymmetry. Its published results are produced on
academic datasets — CRSP, TAQ — over decades, by people who will never trade them. Its
practitioners hold data the papers never see, and almost never publish what happens when
the two meet. When a practitioner does check, the check is private, and the selection of
*which* paper to check is a matter of taste that nobody records.

This project attacks the second half of that problem, which turns out to be the tractable
one: **making the choice of paper auditable, and making the prediction unfalsifiable-after-
the-fact.**

## What was built

A four-step bench, each step leaving a written trace.

**1 — Discover, on a stated criterion.** The OpenAIRE MCP server exposes
`openaire_find_by_influence_class`, which ranks research products by field-normalised,
time-adjusted citation impact. Asked for class C3 — top 1% — on *intraday momentum*, it
returned five papers. We took the top three by our own topic relevance and recorded the
exact call, its arguments and its raw response in `donnees/appels_mcp.jsonl`. Anyone can
replay the selection. This is the step that a keyword search plus human judgement cannot
offer: not because the agent reads better, but because **the ranking criterion is stated
rather than felt.**

**2 — Freeze, before computing.** Each paper was reduced to one or more falsifiable
predictions, each with an expected *sign* and a verdict rule fixed in advance. These were
committed and pushed to git as `ed1a739` **before the measurement program was written**.
The commit timestamp is the guarantee. Later corrections — including one embarrassing
misattribution of authorship, caught by re-reading the MCP response — are appended to the
same file rather than written over it.

**3 — Measure, offline.** `35_banc_reproductibilite.py` reads 28.1 million five-minute
bars covering 2 950 US equities over roughly 126 sessions, February to August 2026, and
computes within-stock Spearman rank correlations between the overnight and intraday
components of daily returns. No network, no model, no agent. It emits aggregate JSON.

**4 — Judge, by the rule written in step 2.** Reproduces · no signal · out of reach.

## What came out

Lou, Polk & Skouras (2019) make two claims in one sentence: *continuation* within each
component, and *cross-period reversal* between them. They separate cleanly on our data.
Cross-period reversal reproduces — median ρ of −0.035 same-day and −0.052 day-to-next-
night, carried by 64.5% and 71.6% of 2 866 stocks respectively. Continuation leaves no
trace at all: +0.0017 and −0.0130, on essentially half the stocks each way.

**This is not a refutation and we do not present it as one.** A portfolio-level effect,
established on decile sorts over decades, can be entirely real and still invisible to a
stock-level correlation over 126 sessions. What the split does establish is narrower and
still worth stating: of the two effects, only one is robust enough to survive being
measured badly, on a short sample, by someone else.

Korajczyk & Sadka (2002) ask whether momentum profits survive trading costs, and answer
by computing break-even *fund sizes* — the effect dies above a certain amount of capital,
because a large order moves the price against itself. We sit at the opposite end of that
curve, $500 per position, where price impact is nil. It dies there too. A rule buying an
8% intraday drop beats a random-entry control by 0.63 points, on 549 cases — and returns
between −0.15% and −0.39% once the bid–ask spread is actually paid. **The cost curve is
bounded from below as well as from above**, and the lower bound is a fixed minimum
commission, not a market friction. That is the one thing here that is not in the paper.

Sadka (2006) we declined to answer. His liquidity measure is built from the *unexpected
component of order flow*; we hold a bid–ask spread, which is precisely the fixed component
his paper sets aside as *not* priced. Substituting one for the other would have produced
a number. The number would have been meaningless. **The verdict "out of reach" was written
into the frozen hypotheses before the run**, not chosen afterwards.

## What is published, and what is not

Text, code, method and aggregate results are released under CC BY 4.0. The underlying
bars are not: they come from a commercial broker feed whose redistribution is
contractually forbidden. This is a real boundary and it is worth naming, because it is the
ordinary condition of practitioner data. The bench is reproducible **in method** by anyone
holding equivalent bars; it is not reproducible by re-running our exact input. Open science
that only counts fully-open data will never see inside this class of dataset at all.

## Limits, stated plainly

Six months is one market regime. A correlation is not a return. Returns quoted from our
own wider research are ceilings — slippage is modelled at zero and limit orders assumed
filled the moment a bar's high touches them. The first printed price of a session is
sometimes stale, which adds noise to the overnight leg. And three papers is three papers.

## What it would take to be more than a demonstration

The bench is one program and one frozen-hypotheses file. Scaling it means running the
discovery step across a field rather than a topic, and accepting that most predictions
will land on "out of reach" — which is itself a measurement, of the distance between what
the literature needs and what a practitioner actually holds. That distance is, we suspect,
the more interesting number.
