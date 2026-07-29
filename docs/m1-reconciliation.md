# M1 reconciliation — what two blind readings agreed and disagreed about

**Status:** complete for M1. **Date:** 2026-07-29.
**Inputs:** `docs/readings-alpha.md` (22 entries), `docs/readings-beta.md` (27 entries), and the
two engines on branches `m1-alpha` and `m1-beta`.

## The experiment

Two implementations of the same spec surface — the closed triple, the four-valued codomain,
evidence ordering and canonical defeat selection, the transition system, and §7.4's two currents
— were written independently against the ratified Custos bytes.

Blindness was enforced by construction rather than instruction: each implementer read from a
directory containing only `custos-4.1.md` and `custos-4.0-kernel-draft.md`, digests verified
against the ratified values, with the Custos repository named off-limits (its `reviews/` and
`tools/` sit there). Neither knew the other existed. Neither was permitted to resolve an
ambiguity by asking. Both produced a register of every clause admitting more than one lawful
reading, with quoted spans, the readings, and the pin.

Result: alpha 191 tests, beta 175 tests, both at 100% branch coverage, both with `core/` free of
any KERI import.

## Why this design, and what it bought

The maintainer authored the adversarial reviews that shaped 4.1 and is permanently compromised as
a reader ([`this.i` @qmz2o4](../this.i)). Anything he finds, he might have been looking for. Two
blind readers cannot have been primed, so their agreement is evidence about the *document* rather
than about the reader.

That is exactly what happened. **Both independently rediscovered two findings the adversarial
panel had already produced** — the canonical-selection contradiction and the pending→self-convicted
trigger — without access to either. That corroboration was posted to Custos #2 and #6.

## Convergent readings — the strongest signal

Where two blind readers hit the same clause and pinned the same way, the ambiguity is real (both
had to stop and choose) but a careful implementer is likely to land in the same place.

| Question | alpha | beta | Pinned |
|---|---|---|---|
| Does `affirmed` carry a payload? | R1 | 1 | Yes — ground is required; §7.3's payload list omits it |
| Empty subcode: "lexicographic minimum" vs "orders last" | R7 | 5 | "orders last" — the prose over the formula |
| "First-seen survives" — first seen by whom? | R12 | 17 | First in committed canonical order, not arrival |
| Transition table completeness | R13 | 14 | Self-edges are lawful; unenumerated ≠ forbidden |
| `pending → self-convicted` second disjunct | R15 | 15 | A bearing pair is required on every edge in |
| "Converts to contested standing" | R17 | 18 | A record that is **not** a `Finding` |
| Is a refusal a `Finding`? | R4 | 23 | No — disjoint from the codomain |

The `contested standing` row is worth reading twice. Both readers found the codomain had no home
for §7.4's taint output, both invented an artifact outside it, and **both independently gave it
the same name**, `ContestedStanding`. Agreement, not disagreement, is what makes that finding
strong: two readers could not express a clause the document imports as a binding wall using the
document's own return type. Filed as Custos #24 — where an earlier, incorrect claim that the two
had *diverged* here was corrected on the record.

## The divergence — executed

One clause pair produced a genuine, opposite-direction split, and it is the most valuable artifact
M1 produced.

**§7.3 L1048–1051** fixes the requirement element's fields and canonical order as
`(subject, kind, citing-clause bytes)`. **§7.2 L1007–1008** additionally makes the **species**
mandatory on every element. The species appears in neither the dedup key nor the sort key.

- **alpha (R9)** pinned dedup on the stated key, species *excluded* — forced by L1038's
  byte-identity SHALL, since a species inside the element but outside the key makes the canonical
  order a preorder and the bytes undetermined. Cost: it had to **invent** a merge rule for key
  collisions (earliest species in §7.2's declaration order) and recorded the invention.
- **beta (11)** pinned dedup on the whole element, species *included*, with species appended as a
  final tiebreak — forced by §7.2's mandatory-field SHALL and the cure semantics of L997–1007,
  since collapsing species discards a cure path the reader is told to read off the finding.

Each rejected the other's reading by citing a different `SHALL`. Both described the same
discriminating input independently, before either engine ran: one question requiring subject `S`
under kind `K` cited by clause `C`, where the evidence is both `absent` and inside an open
recovery window.

Run through both engines (`tools/differential_pending.py`):

```
ENGINE alpha  → OUTPUT SIZE 1   cure paths: ['absent']
ENGINE beta   → OUTPUT SIZE 2   cure paths: ['absent', 'window-open']
```

Same committed input, different `pending` findings, from two conforming implementations. §7.3
L1038 says two evaluations of the same triple SHALL return byte-identical findings. Filed as
Custos #27.

The damage is not only to bytes. §7.2 makes the species the thing a party reads to learn what
would discharge the pending — so under alpha's reading a party is told the cure is "the missing
evidence arrives" and is never told a recovery window is open.

## Findings unique to one reader

Neither register subsumes the other, which is itself an argument for having run two.

**alpha only**

- The 4.0 kernel's pinned digest covers the 12-line scaffolding header that both editions rule
  "never ratified bytes" — Custos **#23**.
- The affirmation discipline names only `affirmed`, so a `defeated` citation can change as the
  bundle grows, contradicting §7.3's own monotonicity claim; the forbidden table has no
  `defeated → defeated` row — Custos **#28**. Alpha pinned the literal reading despite preferring
  the other, because reading in a restriction the span does not carry is legislating, which axiom
  3 forbids the fold to do, and wrote a regression test asserting the defect.
- Whether a `Finding` carries its position and law head (R2); what citation an annihilated
  dependent carries (R21).

**beta only**

- The Ground Axiom carries no BCP 14 keyword, so by §3's own reading rule it binds nothing
  (entry 2) — Custos **#29**, with a repair seeded as Custos PR **#30**.
- "Bearing" gates every edge into `self-convicted` but is given a decision procedure only at the
  key tier, and its silence is indistinguishable from §7.4's law-relative consumption (entry 21;
  alpha reached the same bind at R19/R20) — Custos **#32**. This is the case where the
  unspecified law-expression layer reaches *inside* the walls §1.4 declares binding, rather than
  staying above them; see [`this.i` @zizfi4](../this.i).
- §1.4 imports "the canonical ordering and selection of **evidence**", but 4.0 has an ordering of
  *bundles* and a selection of *defeats*; the only evidence ordering is 4.1 §17, which has no 4.0
  counterpart and so cannot be imported — posted to Custos **#21**.
- What alphabet "lexicographic" ranges over (entry 6); §8's composed-evidence element carrying
  fields §7.3's element does not (entry 13); the scope of the receipts wall (entry 24).
- That the first-seen/axiom-4 collision was **created by 4.1** — 4.0 carries the same §7.4
  sentence but has neither axiom 4 nor §17 (G5). This sharpened Custos **#25**.

## Divergence in shape, not in law

Both engines agree a refusal is not a `Finding`. alpha **returns** it; beta **raises** it as
`RefusedInvocation`. Nothing in the Constitution's value distinguishes these, so it is recorded as
an engine-idiom difference rather than a finding — but it is the kind of difference that would
become observable the moment a refusal record acquires a committed form, which Custos #10 and the
openness clause's first unresolved question both bear on.

## What this changes about the plan

[`this.i` @73uk34](../this.i) recorded that a differential harness needs two engines and thesmo
would have one, so the project must not rest its value on differential testing. **M1 falsified
that premise**: two independent blind engines now exist, and the first executed divergence between
them is Custos #27. The differential instrument is available after all, and cheaper than expected,
because the expensive part was never the second engine — it was the second *reading*.

Both branches are therefore retained. Picking a winner and deleting the loser would destroy the
instrument that produced the strongest finding of M1.

**Open decision for M2:** how to carry two engines in one repository. The engines currently live
on `m1-alpha` and `m1-beta`, both importing `thesmo.core`, so they cannot be merged to `main`
side by side without a rename. Options are (a) `thesmo.engines.alpha` / `.beta` behind one
interface, (b) keep them as long-lived branches and run the harness across worktrees, (c) promote
one to `core/` and keep the other as a conformance oracle. This is recorded as undecided rather
than settled by default.

## Custos issues arising from M1

| Issue | Severity | Source |
|---|---|---|
| [#27](https://github.com/Nicholas-Keystate/custos/issues/27) | BLOCKING | the executed divergence — requirement-set dedup key |
| [#28](https://github.com/Nicholas-Keystate/custos/issues/28) | BLOCKING | affirmation discipline vs monotonicity |
| [#23](https://github.com/Nicholas-Keystate/custos/issues/23) | BLOCKING | scaffolding header inside the ratified digest |
| [#24](https://github.com/Nicholas-Keystate/custos/issues/24) | BLOCKING | contested standing outside the codomain |
| [#25](https://github.com/Nicholas-Keystate/custos/issues/25) | MAJOR | first-seen survival vs axiom 4 and §17 |
| [#20](https://github.com/Nicholas-Keystate/custos/issues/20), [#21](https://github.com/Nicholas-Keystate/custos/issues/21) | MAJOR | filed pre-M1; #21 sharpened by beta's G4 |
| [#29](https://github.com/Nicholas-Keystate/custos/issues/29) | BLOCKING | Ground Axiom unruled; `affirmed` has no ruled payload. Repair seeded as PR [#30](https://github.com/Nicholas-Keystate/custos/pull/30) |
| [#32](https://github.com/Nicholas-Keystate/custos/issues/32) | BLOCKING | "bearing" undefined above the key tier; refusal boundary indistinguishable |
| [#2](https://github.com/Nicholas-Keystate/custos/issues/2), [#6](https://github.com/Nicholas-Keystate/custos/issues/6) | — | blind corroboration posted |

**Every M1 finding is now filed.** Three of beta's remain queued as lower-severity observations
rather than defects: what alphabet "lexicographic" ranges over (entry 6), §8's composed-evidence
element carrying fields §7.3's does not (entry 13), and the scope of the receipts wall (entry 24).
