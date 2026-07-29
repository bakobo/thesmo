# Readings register — agent beta, M1 (`src/thesmo/core/`)

**What this is.** Every place where the committed Custos bytes permitted more than one lawful
reading of the fold, recorded at the moment the fork was met and before the code that resolved it.
Per [`this.i` @qflz2q](../this.i) this register *is* the finding list against the specification; per
[`docs/blind-brief.md`](blind-brief.md) it was produced without reading anything about Custos except
Custos.

**Sources.** Exactly two, per the blind brief:

- `custos-4.1.md` — the edition of record. Cited below as `4.1:<line>`.
- `custos-4.0-kernel-draft.md` — the ratified kernel 4.1 §1.4 imports by digest referent. Cited as
  `4.0:<line>`.

Line numbers are 1-based over those files as read at M1.

**How to read an entry.** Each numbered entry gives the quoted span, the lawful readings, whether
they differ *observably* (a discriminating input, where one exists), and which one the shipped fold
pins. A reading that produces no observable difference is still logged — a logged non-ambiguity
costs almost nothing, and the cost of a silent one is the whole project.

---

## A. The finding type and its grounds

### 1. Does `affirmed` carry a required payload?

> `4.1:942-944` — "**affirmed** — the proposition holds over the committed evidence. Ground: the
> evidence bundle and the clause set under which it was appraised."
>
> `4.1:1040-1053` — "**Required payloads.**" enumerates payloads for *defeated*, *pending* and
> *self-convicted*, and for no other value.
>
> `4.1:1016-1018` — "this section is its complete enumeration — states, payloads, permitted
> transitions with their conditions, forbidden transitions, and terminality."
>
> `4.1:240-242` (axiom 1) — "A finding carries its ground — citation, requirement, or proof — or it
> is not a finding."

(4.0 counterparts: `4.0:548-550`, `4.0:646-659`, `4.0:622-624`.)

- **Reading A.** `affirmed` must carry its bundle identity and its clause set explicitly. §7.1 says
  it has a ground; §1.2 (`4.1:163-166`) says "the ground is not an annotation on the value; it is a
  component of the type, and a value arriving without it is not a member."
- **Reading B.** `affirmed` has no required payload. The "complete enumeration" of payloads omits
  it, and axiom 1's three ground *kinds* — citation, requirement, proof — are exactly the payloads
  of the other three values, so on that enumeration `affirmed` has no ground kind at all.

**Observably different:** yes. Under B a bare `affirmed()` conforms, and two evaluators emit
different affirmed bytes over the same triple while both claim conformance — which defeats the
§7.3 byte-identity clause without violating any enumerated payload rule.

**Pinned: A.** `Affirmed` is unconstructible without a non-empty clause set and a bundle identity.

---

### 2. The Ground Axiom carries no BCP 14 keyword

> `4.1:535-542` (reading rule 1) — "Keyword-marked sentences are ruled spans. … The set of ruled
> spans is the document's normative content; prose between them motivates and derives but binds
> nothing on its own."
>
> `4.1:930-939` (§7.1, the Ground Axiom paragraph) — contains no BCP 14 keyword.
>
> `4.1:240-242` (axiom 1) — contains no BCP 14 keyword.

- **Reading A.** The Ground Axiom binds. It is called "the load-bearing decision of this document"
  (`4.1:936`), and §15 makes "the evaluator's return type is the four-valued finding codomain"
  a wall (`4.1:2054-2055`).
- **Reading B.** It binds nothing. By the document's own reading rule, an unkeyworded sentence
  "binds nothing on its own", so bare verdicts are not forbidden by any ruled span.

**Observably different:** yes — B admits a conforming evaluator whose findings carry no grounds at
all, which is the exact failure §7.1 was written to prevent.

**Pinned: A**, enforced at construction. Filed as a defect against the document: the axiom the
standard names load-bearing is, by the standard's own §3, not normative text.

---

### 3. `self-convicted` — the proof package, or its identifier?

> `4.1:957-958` — "Ground: the canonical proof package identifying the contradictory pair."
>
> `4.1:1052-1053` — "A self-convicted finding SHALL carry the identifier of the canonical proof
> package for the contradictory pair."

- **Reading A.** The finding carries the *identifier*; the package is fetched from the cone.
- **Reading B.** The finding carries the *package* — §7.1 names the package itself as the ground,
  and a ground that must be fetched separately is not carried by the value.

**Observably different:** yes — whether the pair's bytes travel inside the finding, and therefore
what the finding's canonical bytes are.

**Pinned: A.** §7.3 is the ruled span (SHALL); §7.1's bullet is unkeyworded prose (see entry 2).

---

### 4. Is the subcode a payload of `defeated`, or only a selection key?

> `4.1:1042-1047` — "A defeated finding SHALL carry its defeater class and its citation … "
> (no mention of the subcode).
>
> `4.1:1123-1136` — "the finding SHALL cite the lexicographic minimum of (defeater-class rank,
> citation identifier, subcode)."
>
> `4.1:1979-1981` (§14 conviction kinds) — "every finding retains its position, its defeated
> clause, its verification grain, and its committed law head."

- **Reading A.** The subcode is carried. It is the "defeat's discriminator within its citation"
  and is the natural referent of §14's "verification grain".
- **Reading B.** The subcode exists only to break ties during selection and is dropped afterwards,
  since the required-payloads enumeration is complete and omits it.

**Observably different:** yes — under B two defeats differing only in subcode produce byte-identical
findings, and the discriminator the cited clause committed is unreadable off the record.

**Pinned: A.** `Defeated` carries `(class, citation, subcode)`; the empty subcode is lawful.

---

### 5. "Lexicographic minimum" versus "the subcode is empty and orders last" — a contradiction

> `4.1:1123-1126` — "Where multiple defeats are simultaneously available for one question, the
> finding SHALL cite the lexicographic minimum of (defeater-class rank, citation identifier,
> subcode)."
>
> `4.1:1133-1136` — "The subcode is the defeat's discriminator within its citation, assigned by the
> cited clause's own committed enumeration; where the clause defines none, the subcode is empty and
> orders last."

(4.0 counterparts: `4.0:729-732` and `4.0:739-742` — byte-identical.)

Under any ordinary lexicographic order on strings, the empty string is the **minimum**, not the
last. The two sentences of one paragraph cannot both be obeyed.

- **Reading A.** The subcode component is ordered with the empty string sorting *after* every
  non-empty subcode. "Orders last" is the specific rule and governs the general "lexicographic
  minimum".
- **Reading B.** Strict lexicographic order over the whole tuple. "Orders last" is then dead prose
  — a description of nothing, since the empty subcode is what gets selected.

**Observably different — discriminating input:** a bundle offering two defeats for one question,
`D1 = (merit, "EClauseX", "")` and `D2 = (merit, "EClauseX", "a")`. Reading A cites `D2`; reading B
cites `D1`. Two conforming verifiers holding the same bundle emit different defeated findings —
exactly what the next sentence (`4.1:1126-1128`, "Two verifiers holding the same bundle SHALL emit
the same defeated finding down to the byte") forbids.

**Pinned: A.** This is the sharpest single underdetermination found at M1: it is not a gap, it is a
two-sentence self-contradiction inside a SHALL span, in a paragraph §1.4 imports as a wall.

---

### 6. What alphabet is "lexicographic" over?

> `4.1:1123-1126` — "the lexicographic minimum of (defeater-class rank, citation identifier,
> subcode)". Nothing in either edition says whether identifiers compare as bytes, as Unicode code
> points, or under a collation.

- **Reading A.** Byte-wise over the UTF-8 encoding.
- **Reading B.** Code-point-wise.
- **Reading C.** Locale collation (rejected outright — it would make the fold depend on ambient
  configuration, which `4.1:1035-1037` forbids by name).

**Observably different:** A and B agree on the substrate's Base64URL identifier alphabet and
disagree above U+FFFF (surrogate-pair ordering). Since the document never restricts citation
identifiers to that alphabet, the divergence is reachable.

**Pinned: A** (byte-wise over UTF-8), because the document's whole conformance predicate is stated
in bytes.

---

## B. The triple

### 7. What is a *member* of the evidence bundle — a span, or a committed item?

> `4.1:248-251` (axiom 2) — "The log spans a fold reads — the GEL span, every cited key-event and
> registry span — are members of the evidence bundle, never a substitute for its completeness."
>
> `4.1:1802-1806` (§13.1) — "A grounded enactment SHALL commit, within its own content: the
> evidence bundle it rests on, pinned as a set of digests …"
>
> `4.1:1101-1105` (§7.3) — "where one committed bundle is a subset of another, appraisal under the
> larger bundle refines and never contradicts appraisal under the smaller".

- **Reading A.** Members are individually digest-addressed committed items; "span" is shorthand for
  the items in it.
- **Reading B.** Members are spans (ranges). A bundle is a set of ranges.

**Observably different — discriminating input:** `X = {span(KEL, 0..5)}` and
`Y = {span(KEL, 0..3), span(KEL, 4..5)}` carry identical bytes. Under A, `X = Y` and each refines
the other. Under B they are ⊆-incomparable, so the monotonicity obligation says nothing about the
pair and an appraisal over `Y` may lawfully contradict one over `X`.

**Pinned: A.** §13.1's "set of digests" is the only ruled span that says what a bundle *is*, and B
makes the subset order — and therefore lawfulness — depend on how a presenter chose to chunk the
same committed bytes, which axiom 4 (`4.1:266-270`) forbids.

---

### 8. The bundle is a set, not a sequence

> `4.1:1101-1105` — the subset order presupposes set membership.
>
> `4.1:2203-2211` (§17) — "An implementation whose fold result depends on arrival order, storage
> order, or any ambient sequence does not conform; the conformance vectors … include streams
> presented in permuted arrival order that SHALL fold to byte-identical Constitutions."

- **Reading A.** The bundle input is unordered; any order the fold needs is derived from committed
  bytes.
- **Reading B.** The bundle is a presented sequence and triple identity includes that sequence —
  which makes permuted arrival a *different triple*, so §17's vectors would be vacuous rather than
  discriminating.

**Observably different:** yes for triple identity, though B is barely defensible.

**Pinned: A.** Logged because the document never states it: "set" is inferred from the word
"subset" and from §17's vector family, never asserted.

---

### 9. Canonical order of evidence when an item has no anchoring coordinate

> `4.1:2203-2207` (§17) — "A fold consumes its log in exactly one order, and that order derives
> from committed bytes: KEL anchoring order first, intra-anchor order as the anchoring event's seal
> list states, and no tiebreak that consults anything uncommitted."

The rule is stated for GEL events, which are anchored by construction. A bundle also contains cited
key-event and registry spans (`4.1:248-250`), which have no anchoring seal in the gAID's KEL.

- **Reading A.** Anchored items order by `(anchor identifier, anchor sn, seal index)`; unanchored
  items order after them by their self-addressing identifier bytes — still "derived from committed
  bytes", so axiom 4 is satisfied.
- **Reading B.** An unanchored item has no committed order, so the fold refuses the bundle.

**Observably different:** yes — B refuses nearly every real bundle, since every cited KEL span is
unanchored in the GEL sense.

**Pinned: A.** Rejected B because it would make the §17 order rule inapplicable to two of the three
logs axiom 2 puts in the bundle.

---

### 10. Comparing positions in different logs

> `4.1:745-750` (§4) — "A position is a log coordinate (identifier, sequence number) in the
> committed order of the log it names; this document never measures position in wall-clock time."

Nothing in either edition orders a position in one log against a position in another, yet
`4.1:1374-1375` ("a rotation policy SHALL be committed before any position it judges") and
`4.1:1276` ("held the enacting power at the enactment's position") both require exactly that
comparison across the GEL, the KEL and the TEL.

- **Reading A.** Positions compare only within one identifier. A cross-identifier comparison is an
  uncommitted ordering, and §7.5 (`4.1:1188-1191`) says the evaluator refuses rather than
  legislating one.
- **Reading B.** Positions compare through the anchoring KEL coordinate, per §17's "KEL anchoring
  order first" — available only where the caller supplies the committed anchor.

**Observably different:** yes — an appraisal that compares a TEL position with a GEL position
returns a finding under B and a refusal under A.

**Pinned: A** as the general rule, with B available exactly where committed anchor coordinates are
present (that is what `canonical_evidence_order` uses). An evaluator that silently ordered two logs
by raw sequence number would be legislating a seam neither edition commits.

---

## C. The typed requirement set

### 11. The dedup key omits the species the same section makes mandatory

> `4.1:1048-1051` — "A pending finding SHALL carry its typed requirement set: deduplicated
> elements, each carrying requirement kind, subject identifier, and the list of citing clauses, in
> canonical order (subject, then kind, then citing-clause bytes)."
>
> `4.1:1007-1008` (§7.2) — "A pending finding SHALL carry the species of each of its requirement
> elements."

The species is a mandatory per-element field that appears in neither the dedup key nor the sort key.

- **Reading A.** Dedup on the whole element, species included; sort on `(subject, kind,
  citing-clause bytes)` with the species appended as a final tiebreak so the order is total.
- **Reading B.** Dedup on `(subject, kind, clauses)` only. Then two elements differing only in
  species collapse — and *which* species survives is chosen by nothing the document commits.

**Observably different — discriminating input:** one question requiring subject `S` under kind
`K` cited by clause `C`, where the evidence is both `absent` and inside an open recovery window.
Reading A emits two elements (`absent`, `window-open`); reading B emits one, and the two cure paths
the reader is told to read off the finding (`4.1:997-1007`) collapse to one, non-deterministically.

**Pinned: A.**

---

### 12. "The list of citing clauses" — whose order, and what are "citing-clause bytes"?

> `4.1:1048-1051` — "… and the list of citing clauses, in canonical order (subject, then kind, then
> citing-clause bytes)."

"List" implies an order; the sort key names "citing-clause bytes" without saying what they are.

- **Reading A.** The clause list is itself canonicalized — deduplicated and sorted ascending by
  clause identifier bytes — and "citing-clause bytes" is the canonical serialization of that sorted
  list.
- **Reading B.** The list preserves the order in which the committed law cites the clauses, and
  "citing-clause bytes" is that presented list's bytes.

**Observably different — discriminating input:** a requirement cited by clauses `["EB", "EA"]` in
that committed order. Under A the element serializes as `EA,EB`; under B as `EB,EA`, and two
evaluators reading the same law from different citation sites emit different bytes.

**Pinned: A.** Rejected B because "the order the citing law states" is defined nowhere, and axiom 4
(`4.1:266-270`) makes an uncommitted order that affects a finding "a commitment without ground".

---

### 13. §8's composed-evidence element has fields §7.3's element does not

> `4.1:1262-1267` (§8) — "it discharges as a pending finding whose typed requirement set enumerates
> exactly the unfilled slots — each element naming the slot's required schema, its expected issuer,
> and the citing clause".
>
> `4.1:1048-1051` (§7.3) — elements carry "requirement kind, subject identifier, and the list of
> citing clauses".

- **Reading A.** §8's is a specialization: the required schema is the element's subject, the
  requirement kind is the committed slot kind, and the expected issuer is an additional committed
  attribute the element carries.
- **Reading B.** §8 introduces a second element shape, so "the typed requirement set" is not one
  type and the §7.3 canonical order does not cover §8's elements.

**Observably different:** yes at the byte level — where the expected issuer sits in the element, and
whether it participates in dedup and ordering.

**Pinned: A**, with extra attributes carried as a canonically-ordered attribute list that
participates in dedup and orders after the three named keys. Rejected B because §7.5
(`4.1:1193-1195`) forbids a compound result from taking a shape outside the enumerated ones, and a
second element type is that shape by another route.

---

## D. The transition system

### 14. A "complete enumeration" that omits every self-edge

> `4.1:1014-1018` — "The finding type is a state machine, and this section is its complete
> enumeration".
>
> `4.1:1055-1066` — five permitted edges. `4.1:1068-1078` — seven forbidden edges.

Five plus seven is twelve, which is exactly the number of ordered pairs of *distinct* values.
Every self-edge — `pending→pending` above all — is enumerated nowhere.

- **Reading A.** A self-edge is not a transition: a finding whose value is unchanged under a grown
  bundle has not moved, so the enumeration is complete over transitions and self-edges are outside
  its subject.
- **Reading B.** The enumeration is complete over *edges*, so an unenumerated edge is unlawful and
  `pending→pending` is forbidden.

**Observably different:** yes — under B any evaluator that returns pending twice while evidence
accumulates is non-conforming, which no evaluator could satisfy, since pending is by construction
the state one waits in.

**Pinned: A.** Self-edges are lawful and carry no condition.

---

### 15. `pending → self-convicted`'s second disjunct

> `4.1:1062-1064` — "| pending | self-convicted | a bearing contradictory pair, **or new
> governed-status evidence** (committed evidence newly bearing on the subject's status under the
> governance tier's committed predicates), enters the bundle |"
>
> `4.1:1065-1066` — the `affirmed→self-convicted` and `defeated→self-convicted` rows carry only
> "a contradictory pair bearing on the question enters the bundle".
>
> `4.1:954-956` (§7.1) — self-convicted means "the subject's own committed bytes contain a
> contradiction".
>
> `4.1:1052-1053` — the payload "SHALL carry the identifier of the canonical proof package **for
> the contradictory pair**".

- **Reading A.** The disjunct never stands alone. Governance-tier duplicity *is* "contradictory
  enactments under one committed predicate" (`4.1:1144-1146`); new governed-status evidence is what
  makes an already-committed pair *bear* at T3. A bearing pair therefore exists in every lawful
  self-conviction, and the payload can always be supplied.
- **Reading B.** The disjunct is independently sufficient: governed-status evidence alone moves
  pending to self-convicted. Then the required payload names a pair that need not exist, and pending
  has a strictly wider door to self-conviction than affirmed or defeated do — an asymmetry the
  terminality paragraph (`4.1:1084-1089`) never acknowledges.

**Observably different — discriminating input:** a bundle in which new governed-status evidence
arrives about a subject with no contradictory pair anywhere. Reading B emits `self-convicted` (with
an unsatisfiable proof-package payload); reading A leaves the finding pending.

**Pinned: A.** A bearing pair is required on every edge into self-convicted.

---

### 16. Does the enumerated transition system bind below T3?

> `4.1:1022-1024` (the ratified rule) — "The 3.3 transition system embeds without normative
> alteration **at T3**."
>
> `4.1:961-965` (§7.1) — "The same four-valued scheme is instantiated at every tier … The evidence
> ordering below is stated once and holds per tier." (The *ordering* is said to hold per tier. The
> *transition system* is not.)

- **Reading A.** The enumerated system binds at all three tiers; the section is the complete
  enumeration for the finding *type*, and the type is tier-generic.
- **Reading B.** It binds at T3 only, and T1/T2 inherit whatever the substrate's acceptance
  machinery does — in which case a Kever-tier finding could lawfully flip affirmed→defeated.

**Observably different:** yes, at the key and registry tiers.

**Pinned: A.**

**Additional defect, filed separately:** the ruled span imports Custos 3.3's transition system by
reference. 3.3 is cited by digest only (`4.1:2110-2111`) and its text is not part of either edition
an implementer may read. "Embeds without normative alteration" is therefore unverifiable by an
independent implementation — the ruled span asserts a relation to bytes no conforming implementer
holds.

---

## E. The two currents

### 17. "First-seen survives" versus "no ambient order" — a wall against a wall

> `4.1:1157-1163` (§7.4) — "**Duplicity taints upward.** A self-conviction at a lower tier does not
> un-happen the history above it: committed history is monotonic, **first-seen survives**, and what
> was affirmed above converts to contested standing rather than to nothing."
>
> `4.1:284-287` (§1.4) — the imported walls include "**first-seen survival**".
>
> `4.1:266-270` (axiom 4) — "**No ambient order.** Any order the fold consumes — of events, of
> clauses, of evidence — is derivable from committed bytes, or is proven irrelevant to the result.
> An uncommitted order that affects a finding is a commitment without ground."
>
> `4.1:2207-2211` (§17) — "An implementation whose fold result depends on **arrival order**, storage
> order, or any ambient sequence does not conform".

(4.0 counterparts: `4.0:764-769`; the axiom floor and §17 have no 4.0 counterpart at all, which
sharpens the problem — see §G.)

- **Reading A.** "First-seen" means first in the *committed canonical order* — KEL anchoring order,
  then the anchoring event's seal list — never first observed. Under A the rule is deterministic and
  every verifier computes the same survivor.
- **Reading B.** "First-seen" means literally first observed by this evaluator, which is the
  substrate's ordinary sense of the phrase. Under B the fold's result depends on arrival order,
  which axiom 4 and §17 each independently declare non-conforming.

**Observably different — discriminating input:** a contradictory pair `(E1, E2)` delivered to
verifier V1 as `[E1, E2]` and to V2 as `[E2, E1]`, where `E2` precedes `E1` in KEL anchoring order.
Reading A has both verifiers keep `E2`. Reading B has V1 keep `E1` and V2 keep `E2` — two findings,
one bundle, and the headline replay obligation broken.

**Pinned: A.**

This is the most consequential finding at M1: read at face value, one of the five walls §1.4 imports
contradicts one of the five axioms §1.4 states, on the same page.

---

### 18. "Converts to contested standing" — a fifth value in a four-valued codomain

> `4.1:1157-1163` — "what was affirmed above **converts to contested standing** rather than to
> nothing."
>
> `4.1:2054-2055` (§15, wall one) — "the evaluator's return type is the four-valued finding codomain
> **and nothing else**".
>
> `4.1:1193-1195` (§7.5) — "Compound evaluator results SHALL preserve their component propositions
> and grounds as a product rather than collapse them into a fifth scalar shape."

"Contested standing" is named as the *result* of a conversion and is not one of the four values.

- **Reading A.** It is not a finding value at all. First-seen survival means the affirmed finding
  survives with its value and its bytes untouched; the taint is a separate, non-finding record
  attached to the subject's standing *going forward*.
- **Reading B.** "Converts" is a transition of the existing finding into a fifth state the codomain
  does not contain. Forbidden by wall one.
- **Reading C.** The tainted question yields a *new* finding at a *new* position, valued
  `pending(unresolved-conflict)` — reusing the species whose cure is "an owned act of the party
  whose conflict it is" (`4.1:1005-1006`).

**Observably different:** yes. A emits nothing new; C emits a new pending finding, and a consumer
that reads the Constitution at the later position sees a question reopened that A leaves closed. C
additionally collides with `4.1:1076` (`self-convicted → pending` is forbidden: "a poisoned question
does not reopen").

**Pinned: A.** §7.4 itself says the record above "remains a record" and that duplicity "does not
un-happen the history above it". The taint is modelled as a `ContestedStanding` record that is
explicitly not a `Finding`.

---

### 19. What annihilation actually emits

> `4.1:1152-1156` (§7.4) — "**Defeat annihilates upward.** A defeated finding at a lower tier voids
> what was built on it: an invalid seal voids the issuance that cited it, which voids the enactment
> that consumed the issuance. The dependents were never valid; annihilation is discovery, not
> change."
>
> `4.1:1072` — the forbidden edge `affirmed → defeated`: "settled findings do not flip; new defeat
> evidence yields a new finding at a new position".

- **Reading A.** Annihilation emits a **new** defeated finding at a **new** position for each
  dependent, and the dependent's earlier finding is untouched.
- **Reading B.** Annihilation mutates the dependent finding to defeated — which the forbidden edge
  forbids outright whenever the dependent was affirmed.
- **Reading C.** Annihilation *removes* the dependent finding ("voids", "were never valid").

**Observably different:** yes — whether the prior finding is still in the record, and whether a new
one appears.

**Pinned: A.** Rejected C because a fold "writes nothing, ever" (`4.1:150`) and therefore deletes
nothing; rejected B because it is an enumerated forbidden edge.

**Sub-ambiguity, same entry — which defeater class does the annihilating finding carry?** The
document never says. Options: inherit the lower-tier defeat's class; always `superseded`; always
`merit`. **Pinned: inherit** — the lower-tier citation is the ground, so its class is the honest
one. Rejected `superseded` because nothing was superseded (an invalid seal is a crypto defeat, not
a displacement), and rejected `merit` because the dependent's own content violated no clause.

---

### 20. What a frame that never committed the predicate returns

> `4.1:1168-1174` (§7.4) — "Registry-tier and governance-tier duplicity are law-relative — they
> convict only within frames that committed the violated predicate, and a frame that never committed
> the predicate SHALL consume them as evidence, never as conviction."

- **Reading A.** The pair enters the bundle as an ordinary evidence item and the edge into
  self-convicted is simply unavailable; the question keeps whatever value the ordinary machinery
  gives it.
- **Reading B.** The frame returns pending, with the missing predicate as a typed requirement.
- **Reading C.** The frame refuses — no committed rule makes the question evaluable.

**Observably different:** yes, three different outputs on one input.

**Pinned: A.** Rejected C because the missing thing is a predicate the frame *chose* not to commit,
not an uncommitted seam inside an otherwise-answerable question — refusing there would let any
frame's silence poison every neighbour's question. Rejected B because a predicate a frame never
committed is not a requirement that frame's law makes required, so no cure path could be named.

---

### 21. What "bearing" is, and who decides it

> `4.1:1108-1111` (§7.3) — "Contradictory pairs convict only where they bear on the question —
> duplicity elsewhere in a subject's history taints that history's standing, but it does not convert
> this question's finding."

The bearing relation is load-bearing on four of the five permitted edges and is defined nowhere in
either edition.

- **Reading A.** Bearing is a committed determination the fold *consumes*: the pair carries the
  question it bears on and the committed predicate it violates.
- **Reading B.** The evaluator computes bearing from the law head.

**Observably different:** yes, wherever the law commits no predicate connecting the pair to the
question — under B the evaluator must decide anyway, which §7.5 (`4.1:1196-1201`) calls legislating.

**Pinned: A.**

---

### 22. The two currents "SHALL NOT merge" — what merging would be

> `4.1:1151` — "Findings cascade between tiers in two distinct currents, and a conforming evaluator
> SHALL NOT merge them".

The clause forbids an operation it does not name.

- **Reading A.** Structural: annihilation and taint are distinct types with distinct constructors,
  and neither is accepted where the other is expected. A single `cascade()` returning a union of the
  two *is* the merge.
- **Reading B.** Semantic only: the evaluator may compute both through one path so long as the
  reported grounds differ.

**Observably different:** not in output bytes; different in what the type system permits, and B
permits exactly the confusion §7.4's closing paragraph ("Breach and duplicity remain distinct crimes
at every tier", `4.1:1165-1168`) exists to prevent.

**Pinned: A.** Feeding a self-conviction to the annihilation current, or a defeat to the taint
current, raises a coded error rather than doing something plausible.

---

## F. The evaluator's edges

### 23. What shape a refusal has

> `4.1:1196-1201` (§7.5) — "Refusal is not a fifth finding value — it is the evaluator declining to
> answer an ill-posed question, recorded as an operational fact."
>
> `4.1:116-120` (§1.1) — "The refusal is not a fifth kind of finding; it is her declining an
> ill-posed question, recorded as an operational fact."
>
> `4.1:2054-2055` (§15) — return type is "the four-valued finding codomain and nothing else".

Where the operational fact is recorded, and by whom, is stated nowhere.

- **Reading A.** A refusal is a value of a distinct type delivered out of band, so it can never be
  stored where a finding is expected.
- **Reading B.** A refusal is an ordinary return value of the fold — making the codomain four plus
  one, which wall one forbids in as many words.

**Observably different:** yes at the type boundary, which is the only thing §15 says is fixed.

**Pinned: A.** `Refusal` is a record that is not a `Finding`, raised as `RefusedInvocation`.

---

### 24. The scope of "acts consumed as grounds require committed receipts"

> `4.1:2058-2060` (§15, wall five) — "acts consumed as grounds require committed receipts — an
> unreceipted operational drop is never a finding".
>
> `4.1:284-288` (§1.4) — the imported walls include "the rule that acts consumed as grounds require
> committed receipts".
>
> `4.1:1008-1012` (§7.2) — the only place the rule is instantiated: "A processor's silent disposal
> of retained work MUST NOT be represented as a finding: until a committed receipt of the eviction
> exists, the drop is an operational observation".

- **Reading A.** General. Any citation whose subject is an *act* — paradigmatically
  `defeated(superseded, <act>)`, since §7.1 names "the defeating clause **or superseding act**"
  (`4.1:945-948`) — must carry a committed receipt referent for that act.
- **Reading B.** Narrow. The rule is exactly §7.2's eviction case and reaches nothing else.

**Observably different — discriminating input:** a defeated finding citing a superseding act for
which no receipt is committed. Conforming under B; refused at construction under A.

**Pinned: A**, because §15 and §1.4 both state the wall in general terms, and a wall stated
generally cannot be narrowed to its single worked example without the narrowing being written down
somewhere. Clause citations and cryptographic-verification-subject citations are unaffected.

---

### 25. Affirmation requires a requirement space the fold cannot enumerate

> `4.1:1112-1121` (§7.3) — "affirmed is reachable only over a bundle that discharges the question's
> entire committed requirement space. An evaluator holding a bundle that leaves any enumerated
> defeater-check unexamined returns pending with that check as its typed requirement, never
> affirmed".

The requirement space is committed *law*, not evidence, and the fold's three inputs give it only a
law *head* — an identifier.

- **Reading A.** The enumerated requirement space arrives as law-derived input alongside the head;
  where it is underivable the question is not evaluable at all and the evaluator **refuses** (a
  missing rule, not missing evidence — the line §1.1 and §17 both draw).
- **Reading B.** An underivable space is treated as empty, so the question affirms on any bundle.

**Observably different:** dramatically — B affirms exactly where the law is silent, which is the
failure mode axiom 3 exists to prevent.

**Pinned: A.**

---

### 26. Byte-identity is not decidable from the document

> `4.1:1037-1038` — "Two evaluations of the same triple SHALL return byte-identical findings."
>
> `4.1:2068-2072` (§15) — the open interior includes "the carriage encoding of this document's
> object classes — a committed deliverable whose default posture is the substrate's native
> composable attachment grammar rather than document envelopes."

The headline conformance predicate is stated in bytes; the byte-level form of a finding is
confessed undesigned. No conformance-suite author can write a decidable pass/fail for the SHALL.

**Pinned:** `core/` defines its own canonical encoding, used only to make determinism testable. It
is a choice, not a reading of the document, and it is recorded here so that it is never mistaken for
one. (The repo-level tension is already carried at [`this.i` @tswf4m](../this.i); this entry records
that the tension binds at the *finding* grain too, not only at the corpus grain.)

---

### 27. The compound product is not a finding

> `4.1:1193-1195` (§7.5) — "Compound evaluator results SHALL preserve their component propositions
> and grounds as a product rather than collapse them into a fifth scalar shape."
>
> `4.1:1204-1207` — "each component of a compound question preserves its own proposition, ground,
> and transition system in the product".

- **Reading A.** The product is a distinct type — a mapping from proposition to finding — and is not
  itself a member of the codomain.
- **Reading B.** The product is a finding whose payload is other findings, which reintroduces the
  fifth shape by nesting.

**Observably different:** at the type boundary; under B a product could be handed to the transition
system, which has no edges for it.

**Pinned: A.**

---

## G. Where 4.1 and the ratified 4.0 kernel disagree, or where governance is unclear

### G1. The evaluator sections are byte-identical; the import adds nothing

Mechanically verified at M1: 4.0 §6 (lines 532-813) and 4.1 §7 (lines 926-1207) differ **only** in
section numbers (`6.x` → `7.x`), and 4.0 §14 and 4.1 §15 (the openness clause, which carries the six
walls) differ only in the heading number. Diffs are reproducible with:

```
diff -u <(sed -n '532,814p' custos-4.0-kernel-draft.md) <(sed -n '926,1208p' custos-4.1.md)
diff -u <(sed -n '1627,1683p' custos-4.0-kernel-draft.md) <(sed -n '2045,2101p' custos-4.1.md)
```

**Consequence, filed as a finding:** for the finding codomain specifically, the digest-referent
import at `4.1:277-288` supplies an implementer with no text they would not already have from the
edition of record. The import's stated purpose — that reading only 4.1 yields a non-conforming
engine — is not borne out by §7. It may still be borne out elsewhere; it is not borne out here.

### G2. The Constitution's identity condition contradicts between editions

> `4.0:304-306` — "Two GARDs holding identical GELs hold identical Constitutions — the property that
> makes law replayable rather than testimonial."
>
> `4.1:688-693` — "Two GARDs holding identical committed triples — evidence bundle, law head,
> appraisal position — hold identical Constitutions; **the GEL alone does not suffice**, since the
> Gever folds it in the context of the key events and registry spans it cites".

A direct contradiction on a fold-observable property. 4.1's appendix rules it a repair
(`4.1:2409-2419`).

**Which governs:** 4.1. §1.4 imports 4.0's *evaluator* sections, and the definitions section is not
one; and 4.1 supersedes at its effectuation coordinate (`4.1:2124-2126`). **Pinned accordingly:**
the fold is keyed on the triple, and an engine keyed on the GEL alone is non-conforming.

**Why it still matters:** an implementer told at `4.1:277-288` that the 4.0 kernel binds "with full
force", and reading 4.0 as instructed, meets the GEL-alone sentence with nothing in 4.0 marking it
superseded — 4.0's own bytes are immutable and carry no erratum. Only the appendix of the *other*
document discloses the repair.

### G3. One imported wall is not in an evaluator section of the edition it is imported from

`4.1:284-288` imports, from 4.0, "the rule that acts consumed as grounds require committed
receipts". In 4.0 that rule is stated in §14, the openness clause — not in §6, the evaluator
section. The clause imports "whose evaluator sections bind here by that committed referent"; the
wall it names sits outside them. Loose referent, filed as such. (§7.2's eviction sentence is the
nearest evaluator-section instantiation — see entry 24.)

### G4. §1.4's wall list names an ordering that has no referent in the imported edition

`4.1:284` imports "the canonical ordering and selection of evidence". 4.0 §6.3 contains "**The
evidence ordering**" (a subset order over *bundles*, `4.0:707-727`) and "**Canonical selection**"
(of *defeats*, `4.0:729-742`). Neither is a canonical ordering **of evidence**. The only canonical
ordering of evidence in either document is 4.1 §17 (`4.1:2203-2211`), which has **no 4.0
counterpart** and therefore cannot be part of what the digest referent imports.

- **Reading A.** The wall names 4.0 §6.3's two paragraphs loosely and imports nothing more.
- **Reading B.** The wall names an evidence order the imported edition does not contain — the import
  is short, and a conforming engine must look outside the referent to satisfy it.

**Pinned: A** for what is imported, with §17's consumption order implemented separately as 4.1-only
law. Recorded because the difference decides whether an engine claiming conformance to the *4.0
walls alone* owes §17's permuted-arrival guarantee — and neither document says.

### G5. Additions in 4.1 with no 4.0 counterpart that bear on the fold

Chapter 1 whole (the five axioms, including axiom 2's closed triple and axiom 4's no-ambient-order)
and §17 whole are 4.1 additions (`4.1:2447-2453`). Entry 17's collision — "first-seen survival"
against "no ambient order" — is therefore a collision **created by 4.1**: in 4.0, first-seen
survival stands with no axiom 4 and no §17 to contradict it. An implementer reading 4.0 alone would
never see the conflict; an implementer reading 4.1 alone would see only the axiom side of it, since
"first-seen survives" appears in 4.1 too (`4.1:1160`) but its consequences are unstated there.
