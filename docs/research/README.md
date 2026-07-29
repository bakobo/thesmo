# Research records

Literature research commissioned while implementing Custos, kept because it is
load-bearing for design decisions and because its citations are the warrant for
claims we make to the specification's author.

**These are records, not conclusions.** Both carry explicit verification markers
— `[V]` verified from a primary source the researcher read, `[S]` search-summary,
`[R]` recalled and unverified, `[A]` the researcher's own analysis. Treat `[R]`
and `[A]` as leads. Both reports also disclose tool failures where a fetch
summarizer fabricated content; that disclosure is why the rest is trustworthy.

At least one `[A]` claim has already been checked and **rejected**: the argument
that Custos's canonical defeat selection is a `min` where monotonicity requires a
`max` does not hold, because `min` over the ratified rank order selects the
*strongest* defeat and is therefore monotone in severity. Verify before citing.

| File | What it covers |
|---|---|
| [`defeasible-logic-and-custos.md`](defeasible-logic-and-custos.md) | Whether Custos has reinvented a defeasibility calculus. Defeat priority ordering, Belnap's four values and bilattices, Catala, LegalRuleML, defeasible deontic logic, s(CASP), the CALM theorem, certifying algorithms |
| [`contract-as-code-lineage.md`](contract-as-code-lineage.md) | Ricardian contracts, Accord Project, CommonAccord, Stipula/Symboleo, smart-contract governance and what breaks without a total order, local-first and partial-order-native work |

## Findings these produced

Filed against Custos: **#33** (reinstatement is covered for acts, not for
evidence). The rest of the material is comparative rather than defect-shaped —
where a repair proposal comes out of it, it travels as a `reviews/` document
under Custos's "findings, not edits" rule, never as an edit to ratified text.

## Patent check — resolved, no encumbrance

A research pass flagged the "law as a fold over an event log" framing as possibly
patent-encumbered. Checked; it is not, and the flag was partly an artifact of the
research itself. Recorded here so nobody re-raises it.

**US 11,216,444 B2** is real — "Scalable event sourcing datastore," Salesforce,
priority 2019-01-31, granted 2022-01-04. The sentence about a current state being
"computed by folding over the event log" is in its **background/description, not in
any claim**, which disposes of it twice: unclaimed scope, and the applicant's own
admitted prior art, so folding-over-a-log cannot be asserted as its invention. Its
independent claims require an external-service event source, a separate
streaming-tier aggregate processor computing state asynchronously, and aggregate
state in a write-through cache. A synchronous pure fold over a KEL meets none of it.

**US application 19/561,229** has the right number and the wrong title. It is
"Cryptographically Enforced Governance for Autonomous Agents and Distributed
Execution Environments" (Mashin, Inc.), not "Append-only governance audit ledger" —
that was the title of a *blog article* describing one mechanism. No claim text is
public until roughly late 2027. The reported claim about "logging policies consulted,
rules that fired, precedence applied" came from marketing prose, not from claims.
Pending applications confer no enforceable rights. Tracked as `~2j5j`.

Two things worth carrying forward. **Prior art**: the decisive reference is Martin
Fowler's *Event Sourcing*, 2005-12-12 — "discard the application state completely and
rebuild it by re-running the events from the event log." **One trap**: KERI's own
Kever/Tever design (arXiv 1907.02143, July 2019) *postdates* '444's January 2019
priority, so it is not prior art to '444 — do not lean on it.

And the useful inversion: publishing a specification is not making, using or selling,
so it carries essentially no infringement risk, and it *creates* dated prior art
against later filings. Custos's succession machinery already produces exactly that
artifact — edition digests anchored in a KEL at named coordinates — so its defensive
publication record is a by-product of how it ratifies. Worth confirming it is
archived somewhere that outlives the repository (`~5hal`).

Not legal advice; an FTO read is a question for counsel if an implementation is ever
commercialized.

## A note on blindness

These reports are **not** blind material. They discuss the specification's
defects and its formal relatives, so they sit on `main` alongside the
reconciliation record, and engine-branch agents must not read them — see
[`../blind-brief.md`](../blind-brief.md), "Branch blindness".
