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

## A note on blindness

These reports are **not** blind material. They discuss the specification's
defects and its formal relatives, so they sit on `main` alongside the
reconciliation record, and engine-branch agents must not read them — see
[`../blind-brief.md`](../blind-brief.md), "Branch blindness".
