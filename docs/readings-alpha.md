# Readings — agent alpha, M1 `core/`

Every place where Custos underdetermined the fold I was building, recorded at the moment I hit
it. Line numbers are into the two specification files I was given and the only ones I read:

- `4.1` = Custos 4.1 candidate, sha256 `ff8b9e7a…b72b05` of the bytes I held
- `4.0` = the ratified Custos 4.0 kernel, sha256 `9cefdc5d5842…` (matches 4.1 §16's pin; see
  Part III entry S1)

Each entry states the span, the lawful readings, the one I pinned, and — the part that matters —
whether the readings **produce different findings on some input**. Entries marked
**DIVERGENT** do; two conforming engines can disagree there on committed bytes. Entries marked
*convergent* are places where the text is loose but every lawful reading computes the same
thing; they are logged anyway, because a logged non-ambiguity costs almost nothing.

Each entry has a `this.i` node; the node id is given so the register and the tree cross-reference.

---

## Part I — pinned readings

### R1 — Does `affirmed` carry a payload? **DIVERGENT** (@lkfaqca)

4.1 §7.1, lines 943–945:

> - **affirmed** — the proposition holds over the committed
>   evidence. Ground: the evidence bundle and the clause set under
>   which it was appraised.

4.1 §7.3 "Required payloads", lines 1040–1053, enumerates payloads for **defeated**,
**pending** and **self-convicted** only. `affirmed` is absent. Yet §7.3's governing ratified
rule (lines 1021–1027) says the finding type "SHALL enumerate its constructors, required
payloads…", and §7.1 lines 934–936 make the ground a component of the type: "A value that does
not carry its ground is not a member of this type."

- **Reading A** — `affirmed` is a nullary constructor. §7.3 is the enumeration of record, it is
  declared complete ("this section is its complete enumeration", line 1016), and it lists three
  payloads.
- **Reading B** — `affirmed` carries the evidence bundle and the clause set, because §7.1
  states its ground and the Ground Axiom makes the ground part of the type. §7.3's silence is
  an omission in an enumeration that claims completeness, not a licence for a bare verdict.

**Pinned: B.** The Ground Axiom is stated at axiom force (§1.4 axiom 1, lines 240–242: "A
finding carries its ground — citation, requirement, or proof — or it is not a finding. The
codomain admits no bare verdicts"), and an axiom outranks an enumeration that forgot a row. I
reject A because it would make `affirmed` the one finding value a stranger cannot check by
replay — you could not tell which clause set was applied.

**Divergence:** engines disagree on the bytes of every affirmed finding. Under A an affirmed
finding is a constant; under B two affirmations of the same proposition under different clause
sets are different findings. §7.3 line 1038 ("Two evaluations of the same triple SHALL return
byte-identical findings") is satisfied by both, which is exactly why the divergence survives
the conformance predicate.

### R2 — Does a finding carry its position and law head? **DIVERGENT** (@krkkmwhh)

§7.3 "Required payloads" (1040–1053) does not mention position or law head. §14 "Conviction
kinds", lines 1979–1981, does:

> every
> finding retains its position, its defeated clause, its
> verification grain, and its committed law head.

§13.1 (lines 1802–1810) independently requires a grounded enactment to commit "the law head it
invokes; the position at which it speaks; and the terminal finding it claims".

- **Reading A** — position and law head are carriage, supplied by whatever wraps the finding;
  the finding value itself is just verdict + ground.
- **Reading B** — every finding carries its whole triple. §14's sentence is unconditional
  ("every finding"), and a finding that does not name the law it was computed under cannot be
  replayed by a stranger who holds several law heads.

**Pinned: B** — a `Finding` carries the `AppraisalTriple` it was computed over. I reject A
because §14's ruled span says "every finding", not "every conviction record", and because
under A the finding is not self-grounding: axiom 2's closure (lines 245–247) is stated over the
inputs, and a value that drops two of the three inputs cannot be checked against them.

Note the term **"verification grain"** in that same sentence occurs exactly once in 4.1 and
nowhere in 4.0; it is undefined. I did not implement it, and I record the gap here rather than
guessing at a field.

**Divergence:** the bytes of every finding differ between readings.

### R3 — Is "requirement kind" the same field as "pending species"? **DIVERGENT** (@2kzvek2)

§7.3 line 1049: a pending finding's elements each carry "requirement kind, subject
identifier, and the list of citing clauses". §7.2 line 1007: "A pending finding SHALL carry the
species of each of its requirement elements", the species being `absent`, `window-open`,
`unresolved-conflict`, `expired/abandoned` (line 988).

- **Reading A** — one field under two names; "kind" *is* the discharge species.
- **Reading B** — two fields. "Kind" says what sort of thing is required, "species" says how it
  is cured. §6 lines 904–906 ("Requirement elements in typed requirement sets SHALL name their
  required schemas by schema identifier") and §8 lines 1264–1266 ("each element naming the
  slot's required schema, its expected issuer, and the citing clause") both describe element
  content that is plainly not a cure path.

**Pinned: B** — element = (subject, kind, citing clauses, species). I reject A because §7.2's
species enumeration is closed at four values and §8's "required schema, expected issuer" cannot
be expressed in it; a single field would have to be both closed and open.

**Divergence:** the canonical order of a requirement set is "(subject, then kind, then
citing-clause bytes)" — so under A the set is sorted by cure path and under B by required kind.
Two elements with the same subject, kinds `k1 > k2` and species `absent`/`window-open` sort in
opposite orders under the two readings, and the resulting pending findings differ byte for
byte. See also R9 (the dedup key) and R10.

### R4 — Is a refusal a return value or a raised error? *convergent* (@iezwqh)

§1.1 lines 117–119: "The refusal is not a fifth kind of finding; it is her declining an
ill-posed question, **recorded as an operational fact**." §7.5 lines 1197–1201 repeats it.

- **Reading A** — refusal is an exception; there is nothing to return, because the invocation
  was declined.
- **Reading B** — refusal is a value of a type disjoint from `Finding`, returned by the
  invocation boundary, carrying the name of the missing rule (§1.4 axiom 3, line 262: "The
  refusal names what is missing").

**Pinned: B.** "Recorded as an operational fact" is a recording obligation, and you cannot
record what you threw away; §17 line 2251 likewise requires that "the refusal names the
underivable commitment". I reject A because an exception carries no committed record and,
in Python, tempts a caller into swallowing the very fact the standard requires be kept.

*Convergent* — both readings agree on which invocations refuse and on what the refusal names.
The divergence is API shape only, which is why this one is logged and not switched.

### R5 — What order does `core/` consume evidence in, and what breaks a tie? **DIVERGENT** (@vwqohe)

§17 lines 2203–2207:

> **Canonical order.** A fold consumes its log in exactly one
> order, and that order derives from committed bytes: KEL
> anchoring order first, intra-anchor order as the anchoring
> event's seal list states, and no tiebreak that consults
> anything uncommitted.

§7.3 lines 1102–1105 orders *bundles* by the subset relation, which makes a bundle a set. §1.4
axiom 4 (lines 266–270) forbids any order not derivable from committed bytes.

Three things are underdetermined at once:

- **Reading A** — the fold's input is a stream, and canonical order is a property of the
  stream. A pure `core/` handed a bundle therefore cannot compute it, and the ordering belongs
  to the substrate adapter.
- **Reading B** — the fold's input is a set whose members each carry their committed
  coordinate (anchoring sequence number, seal index within that anchor), and canonical order is
  computed inside the fold from those coordinates.

**Pinned: B** — `EvidenceBundle` is a frozenset of items each carrying a `Coordinate(anchor
sequence number, seal index)`, and `committed_order()` sorts by that coordinate. Under A the
"closed at exactly three inputs" axiom would be violated the moment order mattered, because
the order would arrive from outside the triple. I reject A on axiom 2 (lines 245–247).

And the tiebreak: §17 forbids only *uncommitted* tiebreaks, and states none for two items at
one coordinate. I pin **the item's own identifier bytes ascending** as the tiebreak, which is
derivable from committed bytes and therefore lawful under axiom 4 — but any other
committed-bytes tiebreak is equally lawful, and a different one changes which item is
"first-seen" (R12) and therefore which survives.

**Divergence:** two engines that tiebreak differently produce different first-seen survivors
on a bundle carrying two items at one coordinate — which is precisely the duplicity case the
ladder is about.

### R6 — "Byte-identical" is not decidable at this layer *convergent* (@holyd22k)

§7.3 line 1037–1038: "Two evaluations of the same triple / SHALL return byte-identical
findings." §15 lines 2069–2071 confesses "the carriage encoding of this / document's object
classes" is an undesigned deliverable.

There is therefore no encoding under which "byte-identical" can be evaluated, and the headline
conformance predicate of the finding type is not decidable from the standard alone. I did not
invent one: `core/` gives every finding structural value equality (frozen dataclasses, total
and canonical component order), and defers bytes to the layer the standard leaves open. Every
place below where I say two readings "differ byte for byte" means: they differ structurally,
under any encoding that is injective on the structure.

I record this as a finding rather than a switch, because the reading I pinned cannot be wrong —
it is the only one available — but the obligation the standard states cannot be discharged by
any implementation today.

### R7 — The empty subcode: "lexicographic minimum" vs "orders last" **DIVERGENT — the sharpest one** (@kjqxel)

§7.3 "Canonical selection", lines 1123–1136:

> **Canonical selection.** Where multiple defeats are simultaneously
> available for one question, the finding SHALL cite the
> lexicographic minimum of (defeater-class rank, citation
> identifier, subcode). Two verifiers holding the same bundle
> SHALL emit the same defeated finding down to the byte. The
> defeater classes are enumerated and ranked, in this order,
> carried from the predecessor unchanged: **crypto** (a
> cryptographic verification failed), **authority** (the actor
> lacked the invoked power), **merit** (the content violates a
> committed clause), **superseded** (a later lawful act displaced
> the subject). The subcode is the defeat's discriminator within
> its citation, assigned by the cited clause's own committed
> enumeration; where the clause defines none, the subcode is empty
> and orders last.

The two sentences contradict each other. Under any lexicographic order over byte strings the
empty string is the **minimum** — it is a prefix of every other string, so it sorts **first**.
The section says it "orders last".

- **Reading A** — "orders last" is the operative rule: the empty subcode is a maximum, sorting
  after every non-empty subcode. The final clause is the more specific statement and the one
  that mentions the case explicitly.
- **Reading B** — "lexicographic minimum" is the operative rule, and "orders last" is loose
  prose describing where the empty subcode lands in a *descending* presentation or in the
  enumeration of the sentence itself. A conformance test would then select the empty-subcode
  defeat.

**Pinned: A.** The specific governs the general: the last clause is the only sentence in the
document that says what happens to an empty subcode, and reading it as decoration would leave
it with no content at all — whereas reading A merely makes "lexicographic" mean "lexicographic
with ∅ as top", which is a normal and stateable order. I reject B because it makes a
deliberately drafted final clause vacuous.

**Divergence, with the input:** a question with two simultaneously available defeats, both of
class `merit`, both citing clause `EClause0000`, one with subcode `"a"` and one with no subcode.
Reading A cites the defeat with subcode `"a"`; reading B cites the defeat with the empty
subcode. Both engines satisfy "Two verifiers holding the same bundle SHALL emit the same
defeated finding down to the byte" — internally. Against each other they differ, on committed
bytes, on the citation the whole recourse chain of §13.1 then rests on.

### R8 — Does defeat short-circuit, or must the requirement space be discharged first? **DIVERGENT** (@xr3rp7)

§7.3 "The evidence ordering", lines 1114–1121:

> The ordering
> forces a discipline on affirmation, stated here so no reader must
> derive it: affirmed is reachable only over a bundle that
> discharges the question's entire committed requirement space. An
> evaluator holding a bundle that leaves any enumerated
> defeater-check unexamined returns pending with that check as its
> typed requirement, never affirmed — which is exactly what makes
> the ordering monotone, since a bundle that could still grow a
> defeater is, by construction, a bundle that has not discharged
> the space.

- **Reading A (short-circuit)** — the discipline is stated for `affirmed` and says "never
  affirmed"; it does not say "never defeated". An evaluator that sees one defeater fire may
  return `defeated` even with other checks unexamined.
- **Reading B (full discharge)** — no terminal finding at all is reachable over an
  undischarged space. Only then is the *set* of simultaneously available defeats complete, and
  only then is canonical selection (R7) stable under bundle growth.

**Pinned: A.** The sentence names `affirmed` and only `affirmed`, twice; the drafter who wanted
B had the pen in hand and wrote "never affirmed". I reject B despite liking it better, because
pinning B would mean reading a restriction into a ruled span that the span does not carry —
which is legislating, the exact thing §1.4 axiom 3 forbids the fold to do.

**Divergence, with the input, and it breaks a stated property:** bundle `B1` contains evidence
firing a `merit` defeat on clause `M` and lacks the evidence needed for the enumerated `crypto`
check. `B2 ⊃ B1` adds evidence firing a `crypto` defeat on subject `S`.

- Under A: `finding(B1) = defeated(merit, M)`; `finding(B2) = defeated(crypto, S)`.
- Under B: `finding(B1) = pending{crypto-check}`; `finding(B2) = defeated(crypto, S)`.

Under A the citation changes as the bundle grows. That contradicts §7.3 lines 1101–1104 —
"appraisal under the larger bundle refines and never contradicts appraisal under the smaller" —
and it is not covered by the forbidden-transition table, which forbids `defeated → affirmed`
and `defeated → pending` but says nothing about `defeated → defeated` **with a different
citation**. So the literal reading of the affirmation discipline breaks the monotonicity the
same paragraph claims. Under B monotonicity holds. **This is a defect, not a preference:** the
standard cannot have both the "never affirmed"-only discipline and monotone citations.

### R9 — What is the dedup key of a requirement element? **DIVERGENT** (@kdrqzc)

§7.3 lines 1048–1051: "A pending finding SHALL carry its typed requirement set: deduplicated
elements, each carrying requirement kind, subject identifier, and the list of citing clauses,
in canonical order (subject, then kind, then citing-clause bytes)."

With R3's second field (species) in play, the dedup key can be the sort key or the whole
element.

- **Reading A** — dedup on `(subject, kind, citing clauses)`, i.e. exactly the sort key. Then
  the canonical order is a **total** order on the deduplicated set and the finding's bytes are
  determined. Two same-keyed elements differing only in species must be merged, and the
  standard says nothing about how.
- **Reading B** — dedup on the whole element including species. Then two elements can share a
  sort key, the stated canonical order is only a preorder, and the finding's bytes are **not**
  determined — in direct conflict with line 1038.

**Pinned: A**, with the species merge resolved by taking the minimum species in the declaration
order of §7.2 line 988 (`absent` < `window-open` < `unresolved-conflict` < `expired/abandoned`)
— a committed order derivable from the document, per axiom 4. I reject B because it makes the
byte-identity obligation unsatisfiable; but note that A required me to invent the merge rule,
which is itself an underdetermination the standard should close.

**Divergence:** a requirement set holding two elements with one subject, one kind, one
citing-clause list and species `absent` / `window-open` yields a one-element set under A and a
two-element set in unstable order under B.

### R10 — Is the citing-clause list of an element ordered? **DIVERGENT** (@nxoq2hd)

Same span. The element carries "the list of citing clauses" and elements sort by
"citing-clause bytes" — but nothing states the order *within* the list.

- **Reading A** — the list preserves the order in which the committed law enumerates the
  clauses; that order is committed, so axiom 4 is satisfied.
- **Reading B** — the list is sorted ascending by clause identifier bytes, so that
  "citing-clause bytes" is a well-defined sort key regardless of how the law was written.

**Pinned: B.** A requires the fold to know a clause enumeration order that the closed triple
does not hand it — the law head is a self-addressing identifier, not an ordered clause list —
so under A the fold consumes an order it cannot derive from its own inputs. I reject A on
axiom 2's closure.

**Divergence:** an element cited by clauses `C2` and `C1`, in that order in the law, renders as
`[C2, C1]` under A and `[C1, C2]` under B; and where two elements share subject and kind, the
comparison of "citing-clause bytes" can order them oppositely.

### R11 — "Lexicographic minimum" over a *rank* *convergent* (@zmwnx35s)

Same span as R7. The first component of the tuple is a "defeater-class rank" and the classes
are given names, not numbers.

- **Reading A** — compare by the stated rank order `crypto < authority < merit < superseded`.
- **Reading B** — compare the class *names* as bytes, which is what "lexicographic" says:
  `authority < crypto < merit < superseded`.

**Pinned: A**, because the sentence says "The defeater classes are enumerated and **ranked**, in
this order" and then gives an order that is not alphabetical — a ranking that only exists to be
used. I record B only because "lexicographic minimum" over a tuple whose components are names
is a real trap: an implementer who serializes the class before comparing gets B by accident,
and `authority` and `crypto` are the two classes whose order the two readings swap.

*Convergent by pin, divergent by accident:* the readings differ on any question with a
simultaneous `crypto` and `authority` defeat, which is not an exotic input — it is a
badly-signed act by an unauthorized party.

### R12 — "First-seen survives" — first seen by whom? **DIVERGENT** (@r5p4h2)

§7.4 lines 1159–1161:

> - **Duplicity taints upward.** A self-conviction at a lower tier
>   does not un-happen the history above it: committed history is
>   monotonic, first-seen survives, and what was affirmed above
>   converts to contested standing rather than to nothing.

- **Reading A** — "first-seen" is observational: the first of the pair the evaluator saw.
- **Reading B** — "first-seen" is positional: the earlier of the pair in committed order.

**Pinned: B.** A is not merely worse, it is forbidden: §1.4 axiom 4 (lines 266–270) bans an
uncommitted order that affects a finding, §12.1 lines 1583–1585 say "discovery order is
observer-relative and consulted by nothing", and §17 lines 2209–2211 require permuted arrival
orders to fold to byte-identical Constitutions. I reject A on all three.

**Divergence:** under A, two evaluators that fetched a duplicitous pair in opposite orders keep
different survivors and therefore compute different Constitutions from identical bytes. The
word "first-seen" is the defect — it is the vocabulary of arrival in a document whose whole
architecture forbids consulting arrival. (Note the standard uses this phrase as one of the
imported walls at §1.4 line 285, so the ambiguity is inside a wall, not above it.)

### R13 — The transition system enumerates 12 of 16 ordered pairs **DIVERGENT** (@fxn65z)

§7.3 line 1016 claims completeness: "this section is its / complete enumeration — states,
payloads, permitted transitions / with conditions, forbidden transitions, and terminality."
The permitted table (lines 1058–1066) has five edges; the forbidden table (lines 1070–1078) has
seven. Four values give sixteen ordered pairs. The four **identity** pairs — `affirmed →
affirmed`, `defeated → defeated`, `pending → pending`, `self-convicted → self-convicted` — are
in neither table.

- **Reading A** — an unenumerated pair is forbidden, because the enumeration is declared
  complete. Recomputing a question over a grown bundle and getting the same value would then be
  a violation.
- **Reading B** — identity is not a transition at all; the tables enumerate *changes*, and a
  finding that does not change has not transitioned. Identity is permitted trivially.

**Pinned: B.** A is self-defeating: §7.3 lines 1101–1104 require that a larger bundle "refines
and never contradicts", which the great majority of the time means returning the same value, so
A would forbid the ordinary case. I reject A, and record that the "complete enumeration" claim
is false as written — 12 of 16 pairs are ruled, and the remaining four are ruled by inference
only.

**Divergence:** an engine implementing A rejects its own idempotent recomputation.

### R14 — Is the transition system a machine the evaluator advances, or a relation over recomputations? **DIVERGENT** (@na3tebqk)

§7.3 line 1015 calls the finding type "a state machine". Lines 1033–1038 call a finding "a
function of exactly three inputs" whose two evaluations are byte-identical.

- **Reading A** — the evaluator holds finding state per question and mutates it as evidence
  arrives; forbidden edges are runtime guards that block the mutation.
- **Reading B** — a finding is computed fresh from each triple; the transition system is a
  **validity relation over ordered pairs** of findings for the same question at the same law
  head and position under a growing bundle. Forbidden edges are a conformance predicate over
  two computations, not a guard inside one.

**Pinned: B.** A is incompatible with axiom 2's purity: retained finding state is "local
state", named in line 1036 as an input that may not influence a finding. I reject A on that
line. Consequence, implemented: `transitions.check(before, after)` is a checker over two
findings; nothing in `core/` mutates a finding, and a forbidden pair raises a conformance
error rather than silently coercing a value.

**Divergence:** under A the evaluator can be at `affirmed` and refuse to compute `defeated`
under a grown bundle; under B it computes `defeated` and *reports* the wall violation. The
observable output differs on the same bytes.

### R15 — `pending → self-convicted` on "new governed-status evidence" **DIVERGENT** (@plnfze)

§7.3, permitted-transition table, lines 1062–1064:

> | pending | self-convicted | a bearing contradictory pair, or new governed-status evidence (committed
> evidence newly bearing on the subject's status under the
> governance tier's committed predicates), enters the bundle |

- **Reading A** — two independent sufficient conditions. Governance-tier status evidence with
  **no contradictory pair** can carry a question to `self-convicted`.
- **Reading B** — the second disjunct names *where the pair comes from* at T3: contradictory
  enactments under one committed predicate (§7.4 lines 1144–1146) rather than a key-tier pair.
  A bearing pair is required in every case.

**Pinned: B.** Under A the resulting finding is unconstructible: §7.1 lines 955–957 and §7.3
lines 1052–1053 both require a self-convicted finding to carry the canonical proof package
"for the contradictory pair", and there is no pair. I reject A because it demands a payload the
same section says must exist.

**Divergence:** under A, ordinary status evidence poisons a question terminally — the most
destructive edge in the system, reachable without any duplicity at all.

### R16 — May a question's *first* finding be any value? *convergent* (@uw7kg74)

The transition tables describe movement; nothing says where a question starts. §7.3 line 1087
says "Pending is the non-terminal bottom", which could be read as an initial state.

- **Reading A** — every question begins at `pending` and reaches other values only by
  transition.
- **Reading B** — the first appraisal over a bundle returns whichever of the four values that
  triple computes; "bottom" is a lattice position, not a starting gun.

**Pinned: B**: a finding is a function of its triple (line 1033), so its value is fixed by the
triple, not by a history the triple does not contain. I reject A because it would make the
first finding depend on whether an earlier appraisal happened — an input outside the closed
three.

*Convergent* — A and B agree on the value of every individual appraisal; they differ only on
whether an unobserved `pending` predecessor is posited. No committed bytes distinguish them.

### R17 — "Contested standing" is not in the codomain **DIVERGENT** (@b7773r)

§7.4 lines 1158–1163 (quoted at R12): a self-conviction below "does not un-happen the history
above it … what was affirmed above **converts to contested standing** rather than to nothing."

`contested standing` is not one of the four values (line 941), the codomain is "total over
findings returned by an evaluator" (line 966), and §15 line 2054 makes it a wall that "the
evaluator's return type is the four-valued finding codomain and nothing else".

- **Reading A** — "converts" is literal: the affirmed finding above changes. Since the only
  edge out of `affirmed` is to `self-convicted` (line 1065), taint would have to be
  either a fifth value or that edge — but §7.4 lines 1165–1167 insist breach and duplicity
  never blur, and the pair does not bear on the upper question.
- **Reading B** — the affirmed finding is unchanged (it is "a record" that "remains a record",
  line 1163), and *contested standing* is a non-finding artifact computed **alongside** the
  codomain: a marker on the subject's standing going forward, not a value of the question's
  finding.

**Pinned: B**, implemented as `ContestedStanding`, a type that is deliberately not a `Finding`
and cannot be constructed as one. I reject A because it needs a fifth codomain member, which
§15's wall forbids in as many words.

**Divergence:** under A an affirmed finding's bytes change when a lower tier self-convicts;
under B they do not. That is a byte-level disagreement on identical committed input, in the
tainting current the standard imports as a wall.

### R18 — Defeat annihilating upward vs the forbidden `affirmed → defeated` edge **DIVERGENT** (@bwq5ghwn)

§7.4 lines 1153–1157: "**Defeat annihilates upward.** A defeated finding at a lower tier voids
what was built on it … The dependents were never valid; annihilation is discovery, not change."
Line 1072 forbids `affirmed → defeated`: "settled findings do not flip".

- **Reading A** — annihilation overrides: a dependent that was affirmed becomes defeated when
  the lower tier's defeat lands, and the forbidden edge does not apply to cross-tier cascade.
- **Reading B** — annihilation can only ever act on a `pending` dependent, and that is a
  theorem rather than a special case: by the affirmation discipline (lines 1114–1121), a
  dependent could only have been affirmed over a bundle that discharged its **entire** committed
  requirement space, and the lower-tier check is in that space (defeating evidence is "ex-ante
  enumerable", line 1106). So an affirmed dependent is one whose lower-tier check was already
  examined and discharged — it cannot later be annihilated. `pending → defeated` is a permitted
  edge; nothing is overridden.

**Pinned: B**, and the implementation treats an affirmed dependent presented for annihilation
as a wall violation (fail closed, raised with a symbolic code) rather than converting it. I
reject A because it drives a cascade straight through a wall §15 line 2056 names as fixed
("no backward edge exists in the transition system") — and a wall with an unstated exception is
not a wall.

**Divergence:** feed both engines a lower-tier defeat under a dependent that some other engine
affirmed. A returns `defeated`; B refuses the input as non-conformant. Note B's derivation
depends on R8: if defeat short-circuits (R8 reading A), the affirmation discipline is still
intact and B holds; if a future edition extends short-circuiting to affirmation, B collapses.

### R19 — What decides that a contradictory pair "bears on the question"? **DIVERGENT** (@62dtu6n)

§7.3 lines 1108–1111: "Contradictory pairs convict only where they bear on the question —
duplicity elsewhere in a subject's history taints that history's standing, but it does not
convert this question's finding." At the key tier the decision procedure is named (§7.1 lines
957–959: the substrate's superseding-recovery rules). At the registry and governance tiers,
none is named anywhere in either edition.

- **Reading A** — bearing has a structural default: the pair concerns the same subject and the
  same proposition.
- **Reading B** — bearing at T2/T3 is a predicate of the domain's committed law; where the law
  commits none, the seam is uncommitted and the evaluator refuses (§7.5 lines 1190–1193).

**Pinned: B.** A is the evaluator supplying a rule the domain did not commit, which §7.5's
ratified text forbids in terms ("SHALL refuse the invocation and SHALL NOT legislate the
missing seam"). I reject A even though it is the reading almost any implementer would reach
for, because "same subject, same proposition" is a *composition rule*, and inventing one is
exactly the named failure.

**Divergence:** on a bundle carrying a governance-tier contradictory pair and a law that
commits no bearing predicate, A returns `self-convicted` and B returns a refusal. The whole
recourse chain of §13.1 hangs off which.

### R20 — Duplicity at T2/T3 in a frame that never committed the predicate *convergent* (@ided2r)

§7.4 lines 1168–1174: "Registry-tier and governance-tier / duplicity are law-relative — they
convict only within frames / that committed the violated predicate, and a frame that never /
committed the predicate SHALL consume them as evidence, never as / conviction."

- **Reading A** — such a pair is ordinary evidence; the question's finding is computed as if
  no conviction were available (it may still be affirmed, pending or defeated).
- **Reading B** — the evaluator refuses, since it cannot judge the pair.

**Pinned: A**, on the ruled span's own words: "SHALL consume them as evidence". I reject B
because refusal is for a missing rule, and here the rule is present and says "not a
conviction here". Logged because the T2/T3 no-predicate case and the R19 no-bearing-predicate
case look identical from inside the fold and resolve **opposite ways**, which is a genuinely
hard seam to get right from the text.

---

## Part II — where 4.1 and the 4.0 kernel disagree, or where I could not tell which governs

**D1 — The evaluator sections do not disagree.** I diffed 4.0 §6 (lines 532–814) against 4.1 §7
(lines 926–1208) byte for byte: the only differences are the section numbers in the headings and
in three internal cross-references (`6.5`→`7.5`, `6.4`→`7.4`). The same holds for the openness
clause (4.0 §14 / 4.1 §15), which is identical but for its number. So the digest-referent import
at 4.1 §1.4 lines 280–288 is consistent: the walls it imports are the text it restates. Every
ambiguity in Part I is therefore an ambiguity of **both** editions, not a regression in either.

**D2 — The `Constitution` definition contradicts the closed triple in 4.0, and 4.1 repairs it.**
4.0 §3 lines 304–306: "Two GARDs holding identical GELs hold identical Constitutions — the
property that makes law replayable rather than testimonial." 4.1 §4 lines 686–691 replaces this
with identity over "identical committed triples — evidence bundle, law head, appraisal position
… the GEL alone does not suffice". 4.1's own appendix (lines 2409–2415) accounts for the change
as a gauntlet-round repair. **4.1 governs**; I implemented the triple. Recorded because an
implementer who took the 4.0 kernel as the binding evaluator text — which §1.4 instructs — and
read its definitions section would build a GEL-keyed fold and be wrong.

**D3 — Which 4.0 sections are imported?** 4.1 §1.4 lines 280–288 imports "the ratified Custos
4.0 kernel … whose **evaluator sections** bind here by that committed referent", then lists five
walls. It never says which sections are the evaluator sections. Since 4.0 §6 is textually
identical to 4.1 §7, the import is a no-op for §6 — but D2 shows a genuine 4.0/4.1 conflict in
4.0 §3, and whether §3 is an "evaluator section" is undecidable from the text. I could not tell
which governs, and I resolved it by treating 4.1 as the edition of record wherever the two
differ (4.1 §16 lines 2114–2117: "This document replaces it whole"). A reader who instead treats
the imported 4.0 text as controlling gets D2's GEL-keyed Constitution.

**D4 — The 3.3 embedding is unverifiable.** Both editions' §7.3/§6.3 ratified rule says "The 3.3
transition system embeds without normative alteration at T3" (4.1 line 1024). Custos 3.3 is
pinned by digest at 4.1 lines 2110–2111 but its bytes are not in either document. The claim that
the embedding is unaltered is not checkable from what a conforming implementer is given, and I
implemented the transition system as 4.1/4.0 state it, with no reference to 3.3.

---

## Part III — spec-integrity observations (not implementation ambiguities)

**S1 — The pinned 4.0 bytes include a header that declares itself unratified.** 4.1 §16 lines
2105–2110 pins the predecessor at sha256
`9cefdc5d584289ea8391d8069bca26ea38aa82a34f9ae973d80e4d1b7773f315`, "computed over the
predecessor's complete committed byte stream (whole-file preimage, no placeholder, verified by
round trip)". The file I was given hashes to exactly that — **including** its first twelve lines,
which say at lines 10–11: "NOTE: this header is scaffolding and is stripped at / ratification;
the ratified bytes begin at the first heading." Hashing from the first heading gives
`c1793a18…`; from the preceding horizontal rule, `a8c7c5cc…`. Neither is the pin.

So the document of record that 4.1 supersedes and imports by digest is, byte for byte, a
document containing twelve lines that assert they are not part of it — and 4.1's own appendix
(delta group 1, lines 2350–2352) rules the scaffolding header "never ratified bytes by its own
declaration". The pin and the ruling cannot both be right. I did not chase this further: it does
not change any finding my fold computes, and the falsification value is in the record, not in the
resolution.

**S2 — "Verification grain" is undefined.** See R2. One occurrence in 4.1 (line 1981), none in
4.0, in a ruled sentence that says every finding retains it.
