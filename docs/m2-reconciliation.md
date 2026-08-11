# M2 reconciliation — five blind readings of ratified Custos 4.2

**Status:** complete for M2. **Date:** 2026-08-11.
**Edition under test:** ratified Custos 4.2, sha256
`68cc5c9b7164b33dffcf7b705a0d1301fe108c647d35638fec61d52d29b2775a`, unchanged since its
ratification commit of 2026-08-06 and verified by every leg before it read a line.

**Inputs:** five leg branches, none merged.

| Leg | Branch | Model | Surface | Register | Cases | Built |
|---|---|---|---|---|---|---|
| Gamma | `m2-gamma` | Claude | §18–§19 | 18 entries, 17 DIVERGENT | 15 | engine, 171 tests |
| Delta | `m2-delta` | Claude | §18–§19 | 18 entries, 14 DIVERGENT | 31 | engine, 149 tests |
| Epsilon | `m2-epsilon` | Codex, gpt-5.6 | §18–§19 | 11 entries, 10 DIVERGENT | 10 | register only, by design |
| Zeta | `m2-zeta` | Claude | Chapter 2 | 12 entries, 11 DIVERGENT | 18 | classifier, 104 tests |
| Eta | `m2-eta` | Claude | §1.7, whole document | 9 entries, 8 DIVERGENT | — | gate tool, 72 tests |

All at 100% branch coverage. Every leg declares it stayed inside its reading window; Epsilon
additionally declares no prior knowledge of the standard, and its jail transcript passes the
containment audit.

## The experiment, and what changed from M1

M1 ran two Claude legs against 4.1 §7 and produced nine filed findings, all now closed. M2
changes three things. The edition is 4.2, which is self-contained, so the reading window is one
verified file rather than three ([`this.i` @pyyo5y](../this.i)). The instrument is construction
rather than review, because 4.2 has been through a full gauntlet, a seed station, a targeted
re-gauntlet, a two-model-family collider and a seed-reconciliation census, and had never once been
built from ([@kcmw4c](../this.i)). And one leg per shared surface runs on a different model family
([@u6ykxs](../this.i)), because M1's two legs shared not only weights but the brief, the scaffold,
the orchestrator and the hour.

Blindness was enforced by construction on both sides this time. The specification side is one
digest-verified file. The repository side is `m2-base`, a branch stripped of both M1 registers,
the M1 reconciliation, the research records, the divergence reproduction, the edition comparator
and the leg index, with `this.i` pruned to the rules ([@fxbwie](../this.i), [@5rvdq2](../this.i)).
Epsilon runs in a bubblewrap jail: the real `$HOME` is never bound, `/tmp` is a tmpfs, and its
Codex home carries credentials and nothing else.

## The meta-finding: four legs, three surfaces, one question

The single most repeated result of M2 is not about any clause. **Four of five legs, working on
three unrelated surfaces, independently hit the question of what in this document binds at all.**

§4 rule 1 states it plainly: *"Keyword-marked sentences are ruled spans… The set of ruled spans is
the document's normative content; prose between them motivates and derives but binds nothing on
its own."*

- **Gamma R1** — do §18's unkeyworded rules bind an evaluator?
- **Delta R1** — do §18's lowercase must-rejects bind an evaluator?
- **Epsilon**, as its stated controlling difficulty, applied strictly and systematically through
  every entry: *"the sections' central mechanics are mostly explanatory rather than binding."*
- **Eta @4whvwo** — is §1.7's "states the composition in its own prose" a second obligation, or a
  restatement of the first? Eight of its eleven failing rows turn on the answer.

§18 and §19 carry roughly seven and six keyword-bearing lines across some two hundred lines each,
against §8's twenty-two. Most of the GEL grammar is unkeyworded prose, and §4 says unkeyworded
prose binds nothing.

The three Claude legs noticed the problem and mostly pinned the rules as binding anyway. Epsilon
declined to, and followed the consequence to the end. **That difference is the entire argument for
a second model family**, and it reproduces the shape of M1's #29 — the Ground Axiom carrying no
BCP 14 keyword, ruled BLOCKING and repaired.

## Convergence in the collision zone — the strongest evidence

Where three legs across two model families hit the same clause and pinned the same way, the defect
is a property of the document.

| Question | Gamma | Delta | Epsilon | Converged on |
|---|---|---|---|---|
| Two attachment groups sharing a primary identifier | R10 | R8 | E-R19-01 | **Refuse.** The between-group order is not total, §16 wall 6 requires totality, and §19 requires two presentations to re-derive one identifier |
| Can gate standing be derived from committed bytes? | invention, pinned as edition constants | invention 5 | E-R19-02 | **No.** The gates' conditions are facts about the standard's development record, which no log commits and axiom 4 forbids consulting |
| One event anchored at two coordinates | R4 | R3 | E-R18-03 | The document does not say whether occurrence or identity controls membership |
| An unrecognised governance ilk | R7 | R18 | E-R18-06 | No committed rule maps it to a judgment |
| Byte identity | could not build | could not build | could not build | Untestable by anyone until the carriage encoding ratifies |
| Gate one's discharge cites gate three's family | — | defect under every reading | E-R19-03 | **Deadlock.** Under the literal "ordered" reading no gate ever stands |

The first row is the strongest single artifact of M2. Three independent readers, two model
families, one refusal, arrived at without contact.

The gate rows compound into Epsilon's flattest claim, which Gamma and Delta each reach by a
different route: **a conforming compact-form evaluator cannot be built from this text at all.**

## Divergence — where conforming engines disagree

**The three-way split.** Both tracks placed at one coordinate:

| Leg | Result | Consequence |
|---|---|---|
| Gamma | terminal `self-convicted` finding | grounds recourse; the domain is dead |
| Delta | refusal | grounds nothing; come back with better bytes |
| Epsilon | admitted | neither sentence is keyworded, so nothing binds |

Three conforming readings, three answers, one clause. Each leg's case file names the others'
answers as lawful alternatives, so none is a misreading.

**The executed divergence: the refusal record is untyped.** Custos requires every refusal to name
its ground, and §17 compares refusals under a full-payload predicate. It types the record nowhere.
On the tie case both engines refuse — and emit:

```
gamma:  {"kind": "refusal",    "code": "GEL-BUNDLE-ORDER-UNDERIVABLE", "seal_kind": null}
delta:  {"outcome": "refused", "code": "COMPACT_GROUP_ORDER_TIE",
         "ground": "PFX:W1", "seal_kind": null, "permanent": true}
```

On the withheld-member-bytes case they differ in a field *value*, not merely a name: Gamma emits
`seal_kind: "digest"`, Delta `seal_kind: null`. **Two engines agreeing on every substantive
decision fail §17's equality.** Delta predicted this in its register before anything was run;
Gamma independently built a different record. This is M1 #27's shape one tier up, and it is
executed, not argued.

**Not yet executed.** The three-way split above is *not* executed. The legs' stimuli are not the
same input, and my hand-translation of Delta's stimulus into Gamma's schema tripped
`GEL-ACT-CLASS-UNDERIVABLE` — a different must-reject — before reaching the fork. That failure is
itself an exhibit of **Gamma R17**: §18 lists nine must-rejects and states no order among its own
checks, so which fires on a stimulus tripping two is an engine's free choice. A careful
translation is the first task of M3.

## Chapter 2 and the comprehension gate

**Zeta.** Of the fourteen governed objects 4.2 names, the taxonomy locates nine. Two failures are
contradiction rather than underdetermination, and both were verified against the bytes by the
maintainer:

- §12 fixes the criterion for a governable object and excludes by name *"a schema — immutable
  content under a self-addressing identifier, with no lifecycle."* §15 states *"Semantics-version
  is thereby a governed object by the criterion of section 12"*, and a semantics-version is a
  whole-file digest pin. §2.6 additionally rosters governed schema and governed finding. Three
  objects are declared to satisfy a criterion whose own exclusion covers them.
- Axis 2's third value is *"colorless — no relation, substrate mechanics only"*; axis 3 asks who
  may read *"the bytes of the GEL the object is bound to."* Colorless removes axis 3's argument,
  three lines before the text asserts *"nothing in one coordinate constrains another."*

Zeta's methodological point outranks both: **Chapter 2's totality claim is unfalsifiable against
Chapter 2 alone**, because the chapter selects the objects it exhibits. Run over §2.6's five named
members it reports sound; run over the objects the rest of the document names, it fails five
times. That bears directly on #77's clean-root program, which would inherit the defect.

**Eta.** 209 candidates enumerated mechanically from the bytes, 108 ruled constructs, 97 passing,
eleven failing rows over ten distinct defects. The sharpest is C46: §8.3 needs a relation between a
finding and its lawful replacement at a later position and calls it *succession*, while §1.2
defines succession as the fold's law changing by enactment — and no enactment occurs when a finding
succeeds a finding. The chapter is short an invariant and the section covers the gap by borrowing
a primitive's name.

Eta also disagrees with the specification author's own gate pass, merged the day before as PR #71,
which states *"§17 does it. Nothing else does."* Eta, blind to that PR, found that §18 and §19 each
carry an explicit "Composition, per the comprehension gate" sentence and no other section does. The
maintainer confirmed against the bytes: §18 line 3064, §19 line 3262, and no occurrence of
"composition" anywhere in §17. **The author's pass has the sections backwards.**

## What is not a finding

Three results belong to the instrument, not to Custos, and are separated here so nothing
downstream mistakes them for defects.

1. **The legs ran substrate-blind** ([@7eofhd](../this.i)). `docs/blind-brief.md` permits the KERI,
   ACDC and CESR specifications; the launch instructions I wrote said "exactly ONE file about
   Custos". All five honoured the stricter guard. Delta reported the cost unprompted: it could not
   confirm CESR's derivation code for the Blake3-256 class. **Every "could not build" owed to a
   missing substrate fact is mine, not Custos's.** The digest-function inventions (Gamma @jonzpb,
   Delta @7uyc2l) are only partly affected — `core/` may import no KERI library under
   [@q6hqa4](../this.i) regardless — but the narrower derivation-code question is entirely my
   artifact. DIVERGENT readings are unaffected, and a substrate-blind leg errs toward
   under-claiming.
2. **The cross-run failed 46 of 46 in both directions.** I told each leg its `given` and `then`
   fields were its own choice and not to invent a neutral schema. [@pdig63](../this.i) permits
   coordinating case format as plumbing and I declined to use it. The mechanical failure is my
   protocol; see [@aatmji](../this.i) for what changes at M3.
3. **Every leg's harness blocked it from writing `docs/report-*.md`.** All five reports were
   transcribed verbatim by the maintainer, each marked with a provenance note. Systematic, not a
   leg behaviour.

## Proposed filings against Custos

Ordered by strength of evidence, not severity. **None of these has been filed**; this section is a
recommendation.

| # | Finding | Evidence | Severity |
|---|---|---|---|
| 1 | §19's between-group order is not total for equal primary identifiers | three legs, two model families, same pin | BLOCKING |
| 2 | The refusal record is untyped while §17 compares refusals by full payload | executed divergence between two engines | BLOCKING |
| 3 | Gate standing is not derivable from committed bytes; a conforming compact-form evaluator cannot be built | three legs | BLOCKING |
| 4 | §12's criterion excludes three objects §15 and §2.6 declare governed | Zeta, maintainer-verified | BLOCKING |
| 5 | Axis 2's `colorless` contradicts axis 3 and the orthogonality claim | Zeta, maintainer-verified | MAJOR |
| 6 | §18's must-rejects carry no stated order among themselves | Gamma R17, exhibited accidentally by a failed translation | MAJOR |
| 7 | Gate one's discharge cites gate three's vector family while the gates are "ordered" | Delta, Epsilon | MAJOR |
| 8 | Most of §18–§19 is unkeyworded and so binds nothing under §4 rule 1 | Epsilon; noticed by Gamma and Delta | BLOCKING, and the root of several above |
| 9 | Chapter 2's totality claim is unfalsifiable against Chapter 2 alone | Zeta | MAJOR, method |
| 10 | §8.3 names *succession* for a finding-to-finding relation §1.2 defines as law changing by enactment | Eta C46 | MAJOR |
| 11 | PR #71's premise is wrong on ratified bytes: §18 and §19 carry composition sentences, §17 does not | Eta, maintainer-verified | correction to an open work item |

Items 1–3 and 8 are the ones that bear on #77's "full implementability as the bar." Items 4, 5 and
9 bear on the clean-root program, because they are defects in the chapter a re-rooting would build
on.

## What M2 changes about the plan

The instrument works, and it is cheaper than M1 suggested. Five legs, one working day, one of them
on a rate-limited model producing a register rather than an engine — and the cross-family leg
returned the finding the same-family legs declined to follow through.

Three things carry into M3. The case format must be coordinated as plumbing, or every
cross-implementation comparison stays hand-translation ([@aatmji](../this.i)). The launch guard
must match the blind brief rather than exceed it ([@7eofhd](../this.i)). And the first task is the
careful translation that executes the three-way split, because an argued divergence and an executed
one are not the same evidence — which is the lesson M1 already paid for once.
