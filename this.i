# thesmo — Intent Tree (this.i)
#
# Source of truth for thesmo's design intentions and the decisions that follow from them,
# per the Bakobo intent-first methodology (../dev/methodology.md). Code and docs/ are DERIVED
# artifacts. The whole tree is at design stage; nothing is implemented yet (stage-status: planned
# marks the nodes that describe code-to-be).
#
# Node ids are opaque base32 [a-z2-7], stable across renames. NEVER parse them, never make
# them semantic.
#
# READING NOTE — this repo's tree carries an unusual second job. Because thesmo exists to find
# the places where the Custos specification underdetermines a conforming engine, every node
# recording "we read clause X as A rather than B" IS a finding against the specification. Those
# nodes are the register described at @qflz2q. Read them as a defect list, not only as design.

Falsify the Custos specification by building a conforming Gever = goal:
  id: l7al6o
  why: >
    Custos 4.1 promises replayable governance — "any stranger holding the logs computes the same
    Constitution, the same findings, the same refusals, byte for byte" — and confesses that no
    independent implementation has ever tested the promise. The standard's own falsifier
    (custos PROVENANCE.md) is "no second implementation ever derives equal state from the same
    corpus." thesmo exists to put that claim under load. Chose falsification as the PRIMARY end
    over "build a useful governance engine" because a second engine written to be useful will
    silently paper over every ambiguity it meets — the implementer picks a reading, it works,
    and the fork the specification permitted is never seen by anyone. Optimizing for the defect
    report instead makes the ambiguities the OUTPUT rather than a nuisance. Tradeoff accepted:
    thesmo will be slower to reach production usefulness than a straightforwardly-scoped
    implementation, and some of its structure (the reading register at @qflz2q) is pure overhead
    if the specification turns out to be tighter than we think.
  children:
    There is no first Gever; "second implementation" is a misnomer = constraint:
      id: 73uk34
      why: >
        Custos roadmap item 4 asks for a "second implementation with a differential-test harness."
        Investigation found no first one: custos tools/ holds three spec-integrity scripts
        (digest and census checks), not an evaluator, and the "one implementation, one pinned
        checkout" the specification confesses at §2 and §12.5 is keripy — the KERI/CESR SUBSTRATE
        (custos PROVENANCE.md names it as such), not a governance evaluator. Driving constraint:
        a differential harness needs two engines and we will have one, so thesmo must NOT rest its
        value on differential testing. Everything downstream of this node — above all the reading
        register at @qflz2q — exists because the obvious instrument is unavailable. If the Custos
        author turns out to hold private engine code, this node is wrong and the plan changes.
      children:
        M1 falsified this node's premise; we have two engines = decision:
          id: yghv6a
          why: >
            M1 ran two implementers blind against the same spec surface, intending only to compare
            their READINGS. It produced two complete, independently-written, 100%-covered engines,
            and the first executed cross-implementation divergence (Custos #27: one emits a
            one-element requirement set, the other two, from identical committed input). So the
            differential instrument is available after all. The premise above was wrong about
            cost, not about logic: the expensive part was never the second engine, it was the
            second READING — and blind briefing produces a reading, with an engine attached
            almost for free. Kept the parent node's `why` unedited as the historical record rather
            than rewriting it, because a premise that turned out false is evidence about how we
            estimate and should stay legible. Consequence: both branches are retained and neither
            is deleted. Rejected "merge the better engine and drop the other" — the disagreement
            between them is the product, and deleting either destroys the instrument that produced
            the strongest finding of M1.
        How to carry two engines in one repository = tension:
          id: beue6f
          why: >
            @yghv6a commits us to keeping both engines, but they cannot both live on main as
            written: each imports `thesmo.core`, so merging them side by side needs a rename, and
            `tests/test_core_purity.py` globs a single `core/` path. Meanwhile leaving them on
            long-lived branches means main carries no fold at all, and the differential harness
            has to reach across worktree paths that are not committed anywhere. Neither shape is
            obviously right and the choice constrains M2's layout, the purity gate, and how
            vectors are addressed.
          resolution: >
            Ruled 2026-07-29 by Daniel Hardman: keep both as long-lived branches and evolve them
            independently through several more rounds; late in the cycle promote one branch to
            main, and maintain the other from then on as a separate implementation. Each branch
            gets a PR for CI and review surface, never for merge. Rejected the single-repo
            side-by-side layout (thesmo.engines.alpha/.beta behind one interface) because a shared
            package is a shared reading: the moment two engines import a common interface, someone
            reconciles their type signatures and the independence that makes their disagreement
            evidence is gone. Rejected promoting one to core/ now, because deciding early would
            waste the rounds in which the two readings are still diverging — which is where the
            findings come from. Accepted tradeoff: main carries no fold for most of the cycle, the
            branches drift apart on shared tooling, and every cross-branch improvement costs the
            maintainer a deliberate cherry-pick.
            The binding constraint that comes with it: agents are BRANCH-blind, permanently, not
            just Custos-blind. An agent working a branch is told nothing about any other
            implementation and may not read main, other refs, or this repo's own issues and PRs
            (docs/blind-brief.md, "Branch blindness"). main is specifically off-limits because it
            holds the reconciliation record, which compares the implementations side by side — so
            engine branches never merge or rebase from main, and shared changes cross only by the
            maintainer's hand, who is the one party already non-blind.
    Keep the dogfooding door open, do not walk through it = decision:
      id: ylvmei
      stage-status: planned
      why: >
        Bakobo's constitution asserts the company is an instance of its product (org principle 10),
        and a GARD is a formalization of exactly the delegated, provable authority ../org already
        describes in prose — so thesmo governing Bakobo is a real destination. Chose "clean library
        API, no falsification-only assumptions baked into core/" over either committing to
        dogfooding now or ignoring it, because the fold is NOT the expensive part of dogfooding:
        running Bakobo as a GARD additionally needs a language for expressing a domain's law and
        tooling to write a GEL, neither of which Custos specifies (see the tension at @zizfi4).
        Tradeoff accepted: we carry some genericity we may never use, and we defer the decision
        until M4 tells us what law-expression actually costs.

Build blind, from committed specification bytes only = ++blind constraint:
  id: qmz2o4
  why: >
    An implementer who has read the reviews knows where the specification is soft and will route
    around those places without noticing. The lead maintainer here is compromised as a reader —
    he authored the adversarial reviews that shaped Custos 4.1 and knows its named HIGH findings —
    so he acts as steward and gatekeeper, never as implementer. Implementers read the committed
    specification and nothing else: not custos tools/, not reviews/, not issue #1. Ambiguities are
    banked as findings and NEVER resolved by asking the specification's author, because a shared
    reading destroys the only signal thesmo is built to produce. Chose this over collaborative
    co-design, which would be faster and friendlier but would resolve divergences by conversation
    rather than by the document. Tradeoff accepted: we will implement some things wrongly that one
    question would have fixed, and reconciliation at M5 will cost more than continuous contact.
  children:
    Both editions are normative; 4.1 alone is not enough = constraint:
      id: ultpjo
      why: >
        Custos 4.1 §1.4 binds the ratified 4.0 kernel's evaluator sections into 4.1 by digest
        referent — the transition system, canonical ordering and selection of evidence, the two
        upward currents, first-seen survival, and the rule that acts consumed as grounds require
        committed receipts. Meanwhile 4.1 §7.3 presents itself as a "complete enumeration" of the
        same transition system. Driving constraint: an implementer who reads only the edition of
        record builds a non-conforming engine, and cannot tell that they have. Where the two
        editions differ, that difference is itself a finding against the edition of record and
        MUST be filed rather than silently reconciled.
    Plumbing may be coordinated; semantics may not = decision:
      id: pdig63
      why: >
        Vector file formats, directory layouts, and harness invocation are not things the fold's
        result depends on, and agreeing them early costs nothing and saves a translation layer at
        cross-run time. Anything the Constitution's value depends on stays blind. Chose this split
        over blanket silence because blanket silence would have us inventing an incompatible
        vector format for no methodological gain — the independence that matters is independence
        of READING, not of file extensions.

Pin every underdetermination in public = decision:
  id: qflz2q
  why: >
    This is thesmo's central design move and the reason it can falsify a specification with one
    engine instead of two. Every point where Custos underdetermines the fold becomes a named
    reading switch: the lawful readings, the specification lines that permit each, and the one we
    pinned. Test-only configuration runs two readings over one corpus and produces two different
    Constitutions from the same committed input — which converts "two conforming engines could
    diverge here" from an argument into a demonstration. Chose this over ordinary implementation
    (pick a reading, move on) because ordinary implementation HIDES exactly the defect class we
    are hunting. Chose it over differential testing because differential testing is unavailable
    (@73uk34). Tradeoff accepted: the switchboard is real complexity in the test harness, and it
    must never leak into the shipped engine, which has to be deterministic to conform at all.
  children:
    The shipped engine pins exactly one reading per switch = constraint:
      id: 6amuue
      why: >
        Custos §1.4 axiom 2 and §7.3 require that two evaluations of the same triple return
        byte-identical findings; a configurable engine does not conform. Driving constraint:
        conformance is the thing being tested, so the artifact under test must itself be
        conformant. The switchboard is a test fixture that constructs pinned variants, never a
        runtime option on the shipped fold.
    Permission to leave the differential harness outside coverage = deviation:
      id: 5dugqt
      # deviates-from: the 100%-branch-coverage-of-new-code standard, which is external to this
      # repo — ../dev/methodology.md §6 — and so has no opaque node id here to point at.
      scope: >
        Exactly one file: tools/differential_pending.py. It is excluded from the coverage source
        and carries no tests. The exemption does not extend to anything under src/thesmo/, to any
        future harness that lands inside the package, or to a successor of this file once @beue6f
        is resolved and an engine lives on main.
      why: >
        The script runs whichever engine is on sys.path and main carries no fold, so on main it
        cannot execute at all and there is nothing for a test to assert against. Writing a stub
        engine to make it testable would test the stub, not the divergence — and the divergence is
        the entire point, since this script produced the executed cross-implementation split filed
        as Custos #27. Chose "commit it as the reproduction recipe, uncovered and labelled" over
        two alternatives: deleting it, which would leave #27's central evidence unreproducible by
        anyone reading this repo; and moving it into the package with a fabricated fixture, which
        would buy a green coverage number by testing something nobody cares about. Tradeoff
        accepted: one committed file on main that CI never exercises, which is a real gap and is
        why this node exists rather than a silent exclusion.
      approved-by: Daniel Hardman, 2026-07-29
    The intent tree IS the findings register = decision:
      id: 7z2ifi
      why: >
        Every pinned reading is a consequential decision, so the methodology's §3 trigger already
        requires a node with a rebuttal-surface why. Chose to let that obligation carry the
        register rather than maintaining a separate findings database, because a parallel list
        would drift from the code and because a why that must name the rejected reading is
        exactly the finding text we owe the specification's author. Tradeoff: the register is
        only as discoverable as this file, so M4 must project it into custos's CONTRIBUTING.md
        finding genre rather than pointing the author at a YAML tree.

Python, with a pure core the substrate cannot reach into = decision:
  id: q6hqa4
  stage-status: planned
  why: >
    Custos §1.4 axiom 2 closes the fold's inputs at exactly three — committed evidence bundle,
    committed law head, appraisal position — which means the evaluator needs no KERI library at
    all; only the adapter that produces those three from CESR streams does. core/ therefore
    imports nothing from keripy, and substrate/ is the sole dependency boundary. Chose Python on
    keripy over Rust on keriox: Rust would maximize independence from the substrate reference
    implementation, but WebOfTrust's Rust line has been dormant since 2024 (cesride, parside,
    keride), the only live Rust KERI is THCLab's keriox whose different architecture would import
    a second interpretation of KERI alongside Custos's, and Bakobo has no Rust anywhere while
    every existing component (imbu, soka, heti, cesrview, witness) is Python on keripy. Tradeoff
    accepted: we share a substrate reading with the only prior art, so substrate-level divergences
    are invisible to us; the pure core keeps a later Rust port cheap if that ever binds.

Implement the walls; refuse above them = decision:
  id: 3b4tjm
  stage-status: planned
  why: >
    Custos §2 confesses the Gever's interior undesigned and fixes only its type boundary, while
    §1.4 names the walls that DO bind. An engine that implements the walls, supports a
    deliberately tiny committed predicate vocabulary, and refuses — naming the missing rule —
    beyond it is conformant under axiom 3, not incomplete. Chose this over designing the
    evaluator interior ourselves, because our design choices would become the de-facto
    specification for anyone who reads our code (see @tswf4m), and because it keeps M1–M3 small
    enough that @ylvmei stays reachable. Tradeoff accepted: thesmo will refuse a great deal, and
    a reader who expects a finished governance engine will find it disappointing. Note the
    boundary is subtle and is itself a suspected defect site: §17 has an unrecognized governance
    ilk yield committed evidence and a rule-governed judgment, while an underivable grammar fires
    a refusal.

Shipping the only engine may capture an open specification = tension:
  id: tswf4m
  why: >
    Custos §15 leaves the carriage encoding of its object classes an undesigned deliverable, with
    a consequence readable from the committed bytes alone: "byte-identical" is the headline
    conformance predicate at §2 and §7.3, but §16's actual discharge test relaxes to semantic
    equality, so no conformance-suite author can write a decidable pass/fail for it today.
    An engine must serialize SOMETHING. Whatever thesmo picks becomes the only running answer,
    and gravity does the rest — which contradicts @l7al6o, since capturing an open question is
    the opposite of exposing it.
  resolution: >
    Implement BOTH comparators and refuse to privilege either: a semantic-equality comparator
    matching §16's stated discharge test, and a byte comparator over insertion-ordered CESR+SAID
    as the chosen canonical encoding. Report per vector which claim each supports. The encoding
    choice is then presented as a choice with a rebuttal surface — a finding asking Custos to
    pin the predicate — rather than as an answer. Rejected "pick one and document it," which is
    what capture looks like from the inside.

Dogfooding needs a law-expression layer Custos does not specify = tension:
  id: zizfi4
  why: >
    @ylvmei wants Bakobo governed by thesmo eventually, but a GARD needs its law committed to a
    GEL, and Custos specifies neither a language for expressing a domain's predicates nor
    enactment tooling to write the log. That is a larger and less-constrained problem than the
    fold itself, and starting it now would consume the falsification work that is @l7al6o.
  # Open — no resolution. Deferred to M4, when the predicate vocabulary of @3b4tjm has met real
  # committed law and we know what the gap actually costs. Do not resolve this node silently;
  # if evidence warrants reopening earlier, open a new tension referencing this one.

Named from the Greek for laid-down law, not from Custos's Latin = decision:
  id: wnu6mt
  why: >
    thesmo is coined from θεσμός (thesmos), "that which is laid down" — statute, ordinance,
    established law — the older and weightier Greek term beside nomos. The θεσμοθέται were the
    Athenian archons who recorded and preserved the statutes and presided over the review at
    which contradictory laws were flagged, which is close to this engine's job description.
    Chose a Greek root over a Latin one deliberately: a Latin sibling to "custos" would read as a
    continuation of the standard, and the entire point of @qmz2o4 is that this is an INDEPENDENT
    implementation of it. Rejected naming the repo "gever" — that is the specification author's
    coined term, and taking it would claim the canonical implementation, against both his
    "projection, never an authority" posture and @tswf4m. Rejected "nomia" (the -nomia suffix is
    generic and it is a bee genus) and "enomia" (heard as anomia, its own antonym). Coined with
    slithyt against a purpose-built ancient-Greek governance corpus, contributed upstream.

# ---------------------------------------------------------------------------
# M1 readings register. Every child below is a fork the committed Custos bytes
# left open, met blind under @qmz2o4 and pinned under @6amuue. Read them as a
# defect list against the specification (@7z2ifi), not only as design. The
# long form — quoted spans, line numbers, discriminating inputs — is in
# docs/readings-beta.md; the why here carries the rebuttal surface.
# Citations read <edition>:<line>, over the bytes read at M1.
# ---------------------------------------------------------------------------

Pin one reading at every fork the M1 fold met = decision:
  id: oucuj6
  stage-status: planned
  why: >
    Custos 4.1 §7 presents itself as "the complete enumeration" of the finding type (4.1:1016),
    and §15 calls its six evaluator commitments walls. Implementing it blind found 27 places where
    the bytes admit more than one conforming engine, several inside single SHALL spans. Chose to
    pin one reading per fork in code and record the rejected reading here, over the two obvious
    alternatives: asking the author (forbidden by @qmz2o4, and it destroys the only evidence this
    repo produces) and shipping a configurable engine (forbidden by @6amuue, since a configurable
    evaluator does not conform). Tradeoff accepted: roughly half these pins will turn out to be
    what the author meant, and the register's value then rests entirely on the other half — a
    register of 27 entries where 13 are non-findings is still the right shape, because the cost of
    a logged non-ambiguity is one paragraph and the cost of a silent one is the project.
  children:
    Affirmed carries its clause set and bundle identity = decision:
      id: dkypfoo
      why: >
        4.1:942-944 gives affirmed a ground — "the evidence bundle and the clause set under which
        it was appraised" — while 4.1:1040-1053, the section's self-declared complete enumeration
        of required payloads, names payloads for the other three values and none for affirmed;
        axiom 1 at 4.1:240-242 lists exactly three ground kinds (citation, requirement, proof) for
        four values. Rejected the reading that affirmed needs no payload: it makes a bare
        affirmed() conforming, and then two evaluators emit different affirmed bytes over one
        triple without violating any enumerated rule, defeating 4.1:1037-1038 from inside. Also
        rejected the stricter position that the Ground Axiom binds nothing at all — which is what
        4.1:535-542 literally says, since neither 4.1:930-939 nor 4.1:240-242 carries a BCP 14
        keyword. We enforce grounds at construction anyway; if the author intends the axiom to be
        non-normative prose, this node is the place to say so.
    Self-convicted carries the proof package's identifier, not the package = decision:
      id: 3cmjjo
      why: >
        4.1:957-958 names "the canonical proof package" as the ground; 4.1:1052-1053 says the
        finding SHALL carry "the identifier of" it. Pinned the identifier because 4.1:1052 is the
        ruled span and 4.1:957 is unkeyworded prose. Rejected carrying the package bytes: it
        changes the finding's canonical bytes, and it duplicates into every finding what the
        verification cone (4.1:872-878) already obliges the presenter to make fetchable. A reader
        who thinks a ground must travel with its value — which is 4.1:163-166's own claim — should
        disagree here.
    The subcode is a payload, not only a tiebreak = decision:
      id: qru6hx
      why: >
        4.1:1042-1047 enumerates defeated's payload as class plus citation and stops; 4.1:1123-1136
        makes the subcode the third component of the selection key and calls it "the defeat's
        discriminator within its citation"; 4.1:1979-1981 requires every finding to retain "its
        verification grain". Pinned: carried. Rejected the drop-after-selection reading because it
        makes two defeats differing only in subcode byte-identical, so the discriminator the cited
        clause committed cannot be read off the record — and a conviction record from which the
        grain cannot be read is, by 4.1:1981-1983's own logic, not a conviction record.
    An empty subcode orders last, against the same paragraph's lexicographic rule = decision:
      id: 5pu23u
      why: >
        4.1:1123-1126 requires citing "the lexicographic minimum of (defeater-class rank, citation
        identifier, subcode)"; 4.1:1133-1136 says that where the clause defines no subcode "the
        subcode is empty and orders last". Under any ordinary lexicographic order the empty string
        is the MINIMUM, so the two sentences of one paragraph cannot both be obeyed. Pinned the
        specific rule (empty sorts after every non-empty subcode) over the general one, and
        rejected strict lexicographic order, which would make the "orders last" sentence describe
        nothing. Discriminating input: defeats (merit, EClauseX, "") and (merit, EClauseX, "a") —
        we cite the second; a strict-lexicographic engine cites the first; 4.1:1126-1128 demands
        both engines agree byte for byte. Also pinned byte-wise UTF-8 comparison over code-point
        comparison, since the document's conformance predicate is stated in bytes; the two agree on
        the substrate's Base64URL alphabet and diverge only above U+FFFF.
    The evidence bundle is a set of digest-addressed items = decision:
      id: sgc5lpwd
      why: >
        4.1:248-251 makes log SPANS the members of the bundle; 4.1:1802-1806 pins a bundle "as a
        set of digests"; 4.1:1101-1105 orders bundles by subset. Pinned item-membership. Rejected
        span-membership because it makes {span(0..5)} and {span(0..3), span(4..5)} — identical
        bytes — incomparable under subset, so the monotonicity obligation says nothing about the
        pair and lawfulness would depend on how a presenter chunked committed bytes, which axiom 4
        at 4.1:266-270 calls a commitment without ground. Pinned unordered, too: 4.1:2203-2211
        requires permuted arrival to fold identically, which is vacuous if presentation order is
        part of triple identity.
    Unanchored evidence orders after anchored evidence, by identifier bytes = decision:
      id: stzggn
      why: >
        4.1:2203-2207 fixes the consumption order as "KEL anchoring order first, intra-anchor order
        as the anchoring event's seal list states, and no tiebreak that consults anything
        uncommitted" — a rule stated for GEL events, which are anchored by construction. The bundle
        also holds cited key-event and registry spans (4.1:248-250), which carry no anchoring seal.
        Pinned: anchored items order by (anchor identifier, anchor sn, seal index), unanchored items
        follow, ordered by their self-addressing identifier bytes — still derived from committed
        bytes, so axiom 4 holds. Rejected refusing on an unanchored item: it would refuse nearly
        every real bundle, since two of the three logs axiom 2 puts in the bundle are unanchored in
        the GEL sense.
    Positions compare only within one identifier = decision:
      id: 4qrss4h
      why: >
        4.1:745-750 defines a position as (identifier, sequence number) "in the committed order of
        the log it names" and orders nothing across logs, yet 4.1:1374-1375 and 4.1:1274-1276 both
        require comparing a GEL position against KEL and TEL positions. Pinned: a cross-identifier
        comparison is an uncommitted ordering and the evaluator refuses it (4.1:1188-1191), except
        where committed anchor coordinates are supplied, which is what the canonical evidence order
        uses. Rejected ordering two logs by raw sequence number — sequence numbers of different
        identifiers are not commensurable and an engine that compared them would have legislated
        the seam 4.1:1196-1201 forbids it to legislate.
    Requirement elements deduplicate on the whole element, species included = decision:
      id: blq6dwxz
      why: >
        4.1:1048-1051 requires "deduplicated elements … in canonical order (subject, then kind,
        then citing-clause bytes)"; 4.1:1007-1008 additionally requires every element to carry its
        pending species. The species is mandatory and appears in neither the dedup key nor the sort
        key. Pinned: dedup over the whole element, sort on the three named keys with species and
        committed attributes as final tiebreaks so the order is total. Rejected dedup on the three
        named keys alone, because two elements differing only in species then collapse and nothing
        the document commits chooses which survives — discriminating input: one subject requiring
        evidence that is both absent and inside an open recovery window, where the two cure paths
        4.1:997-1007 tells the reader to read off the finding become one, non-deterministically.
        Pinned likewise that the citing-clause list is sorted and deduplicated by identifier bytes,
        rejecting "the order the committed law states" — an order defined nowhere. And pinned
        4.1:1262-1267's composed-evidence element as a specialization of the one element type
        (required schema as subject, expected issuer as a committed attribute), rejecting a second
        element shape, which 4.1:1193-1195 forbids by another route.
    Self-edges are lawful; the enumeration is complete over transitions, not edges = decision:
      id: iouhhq
      why: >
        4.1:1055-1078 enumerates five permitted and seven forbidden edges. Five plus seven is
        twelve, which is exactly the number of ordered pairs of DISTINCT values, so every self-edge
        is enumerated nowhere in a section that calls itself complete (4.1:1016). Pinned: a finding
        whose value is unchanged under a grown bundle has not transitioned, so self-edges lie
        outside the enumeration's subject and are lawful without condition. Rejected the
        completeness-over-edges reading, which forbids pending to pending and so makes every
        evaluator non-conforming the second time it waits — pending being, by 4.1:1086-1087, the
        state one waits in.
    Every edge into self-convicted requires a bearing contradictory pair = decision:
      id: mwprhoj3
      why: >
        4.1:1062-1064 conditions pending to self-convicted on "a bearing contradictory pair, or new
        governed-status evidence …", while the affirmed and defeated rows at 4.1:1065-1066 carry
        only the pair. Pinned: the disjunct never stands alone — governance-tier duplicity IS
        contradictory enactments under one committed predicate (4.1:1144-1146), so governed-status
        evidence is what makes an already-committed pair bear at T3. Rejected the independent
        reading, under which a self-conviction is emitted with no pair and the required payload at
        4.1:1052-1053 names a proof package for a pair that does not exist — and pending acquires a
        strictly wider door to self-conviction than the terminal states have, an asymmetry
        4.1:1084-1089 never mentions.
    The enumerated transition system binds at all three tiers = decision:
      id: iidbntm
      why: >
        The ratified rule at 4.1:1022-1024 says the 3.3 transition system "embeds without normative
        alteration at T3"; 4.1:961-965 says the four-valued scheme is instantiated at every tier and
        that the evidence ordering "holds per tier" — saying nothing about the transitions. Pinned:
        the system is a property of the finding TYPE, and the type is tier-generic. Rejected the
        T3-only reading, under which a key-tier finding could lawfully flip affirmed to defeated,
        which no reading of 4.1:1072 survives. Filed separately as a defect: the ruled span imports
        Custos 3.3 by reference, 3.3 is cited by digest alone (4.1:2110-2111), and its text is in
        neither edition an implementer may read — so "embeds without normative alteration" is
        unverifiable by any independent implementation.
    First-seen means first in committed order, never first observed = decision:
      id: sr546w
      why: >
        4.1:1157-1163 makes "first-seen survives" the mechanism of the duplicity current, and
        4.1:284-287 imports first-seen survival as one of the five walls. Axiom 4 at 4.1:266-270
        forbids the fold to consume any order not derivable from committed bytes, and 4.1:2207-2211
        says an implementation whose result depends on arrival order does not conform. Read at face
        value one imported wall contradicts one stated axiom on the same page. Pinned: first-seen
        is first in the committed canonical order (KEL anchoring order, then the anchoring event's
        seal list). Rejected the substrate's ordinary sense of the phrase — first observed —
        because it is exactly the ambient sequence the axiom names, and it breaks replay on a
        two-line input: one pair delivered to two verifiers in opposite arrival orders yields two
        different survivors. This is the M1 finding we would most like rebutted.
    Contested standing is not a finding value = decision:
      id: 6mntbxri
      why: >
        4.1:1157-1163 says what was affirmed above "converts to contested standing", and contested
        standing is not one of the four values; 4.1:2054-2055 fixes the return type at four values
        "and nothing else" and 4.1:1193-1195 forbids collapsing into a fifth scalar shape. Pinned:
        the affirmed finding survives with its value and bytes untouched — first-seen survival —
        and the taint is a separate record that is deliberately not a Finding. Rejected reading
        "converts" as a transition into a fifth state, which wall one forbids. Rejected emitting a
        new pending(unresolved-conflict) finding at a new position, which is the most useful
        reading and the most dangerous: it reopens a question 4.1:1076 says does not reopen, and it
        contradicts 4.1:1162-1163's "the record it already made remains a record".
    Annihilation emits a new finding at a new position, inheriting the lower-tier class = decision:
      id: nggcv5f
      why: >
        4.1:1152-1156 says a lower-tier defeat "voids" its dependents and that "annihilation is
        discovery, not change"; 4.1:1072 forbids affirmed to defeated and says new defeat evidence
        "yields a new finding at a new position". Pinned that sentence as the mechanism. Rejected
        mutating the dependent, which is the enumerated forbidden edge; rejected deleting it, since
        a fold "writes nothing, ever" (4.1:150) and therefore erases nothing. The document never
        says which defeater class the annihilating finding carries: pinned inheritance of the
        lower-tier defeat's class, rejecting a blanket "superseded" (nothing was displaced — an
        invalid seal is a crypto defeat) and a blanket "merit" (the dependent's own content
        violated no clause).
    A frame that never committed the predicate keeps the ordinary finding = decision:
      id: 75ljyl6v
      why: >
        4.1:1168-1174 says registry-tier and governance-tier duplicity convict only inside frames
        that committed the violated predicate, and that a frame which never committed it SHALL
        consume the pair "as evidence, never as conviction" — without saying what the finding then
        is. Pinned: the pair enters the bundle as an ordinary item, the edge into self-convicted is
        unavailable, and the question keeps whatever value the ordinary machinery gives it.
        Rejected refusing, because the missing thing is a predicate this frame CHOSE not to commit,
        not an uncommitted seam inside an otherwise answerable question — refusing there lets any
        frame's silence poison its neighbours' questions. Rejected returning pending with the
        predicate as a typed requirement, because a predicate a frame never committed is not a
        requirement its law makes required, so no cure path could honestly be named.
    Bearing is consumed from committed bytes, never computed by the fold = decision:
      id: pbrejw2
      why: >
        4.1:1108-1111 makes conviction turn on whether a contradictory pair "bears on the question",
        and neither edition defines the bearing relation, though it is load-bearing on four of the
        five permitted edges. Pinned: the pair carries its committed bearing — the question it bears
        on and the predicate it violates — and the fold consumes it. Rejected computing bearing from
        the law head, because wherever the law commits no predicate connecting pair to question the
        evaluator would have to decide anyway, which 4.1:1196-1201 calls legislating.
    The two currents are kept apart by type, not by discipline = decision:
      id: mprtnb
      why: >
        4.1:1151 says a conforming evaluator SHALL NOT merge the defeat and duplicity currents, and
        names no operation that would count as merging. Pinned the structural reading: annihilation
        and taint have distinct types and distinct constructors, and feeding a self-conviction to
        the annihilation current — or a defeat to the taint current — raises a coded error rather
        than doing something plausible. Rejected the semantic-only reading (one code path, two
        labels), because a single cascade() returning a union of the two IS the merge, and because
        4.1:1165-1168 insists breach and duplicity stay distinct crimes at every tier.
    Refusal is raised, never returned = decision:
      id: aynhxtdk
      why: >
        4.1:1196-1201 and 4.1:116-120 both say refusal is not a fifth finding value but "an
        operational fact", and neither says where the fact is recorded or by whom; 4.1:2054-2055
        fixes the return type at four values and nothing else. Pinned: Refusal is a record that is
        deliberately not a Finding, delivered out of band as a raised error carrying its code and
        the name of what is missing. Rejected returning it, which makes the codomain four plus one
        at the only boundary 4.1:2052-2062 says is fixed. A reader who thinks an operational fact
        should be a returned value rather than an exception has a real disagreement here; what we
        will not accept is a union type that lets a refusal be stored where a finding goes.
    The receipt rule reaches every act consumed as a ground = decision:
      id: t66d4n
      why: >
        4.1:2058-2060 and 4.1:284-288 both state the wall generally — "acts consumed as grounds
        require committed receipts" — while 4.1:1008-1012 instantiates it only for a processor's
        eviction. Pinned the general reading: a citation whose subject is an act, paradigmatically
        defeated(superseded, act) under 4.1:945-948, must carry a committed receipt referent, and
        so must an expired/abandoned requirement element. Rejected the narrow reading, which would
        admit a defeated finding citing an unreceipted superseding act: a wall stated generally in
        two places cannot be narrowed to its single worked example unless the narrowing is written
        down somewhere, and it is not. Clause citations and failed-verification-subject citations
        are untouched, since neither is an act.
    An underivable requirement space refuses; a merely undischarged one pends = decision:
      id: nup3m6
      why: >
        4.1:1112-1121 makes affirmation reachable "only over a bundle that discharges the question's
        entire committed requirement space", and requires pending with the unexamined check as its
        typed requirement otherwise. The requirement space is committed LAW, and the fold's three
        inputs give it only a law head — an identifier. Pinned: the enumerated space arrives as
        law-derived input beside the head; where it cannot be derived the question is not evaluable
        and the evaluator refuses — a missing rule, not missing evidence, which is the line
        4.1:116-120 and 4.1:2246-2252 both draw. Rejected treating an underivable space as empty,
        which affirms exactly where the law is silent and is the failure axiom 3 exists to prevent.
    core/ pins a canonical encoding only to make determinism testable = decision:
      id: ox6mfpi
      why: >
        4.1:1037-1038 requires two evaluations of one triple to return byte-identical findings, and
        4.1:2068-2072 confesses the carriage encoding of the document's object classes undesigned.
        The headline conformance predicate is therefore not decidable from the document — the
        corpus-grain form of this is already carried at @tswf4m; this node records that it binds at
        the FINDING grain too. Pinned: core/ defines its own length-prefixed canonical encoding,
        used only so tests can assert determinism, and it is labelled a choice everywhere it
        appears so no reader mistakes it for a reading of the standard. Rejected leaving findings
        uncomparable until the carriage question is settled, which would leave the one obligation
        this milestone exists to test unexercised. Pinned alongside: a compound result is a product
        type that is not a Finding (4.1:1193-1195), rejecting a nested finding-of-findings, which
        reintroduces the fifth shape by another door.
    Where the editions disagree, 4.1 governs the fold and the delta is filed = decision:
      id: vbnuexlv
      why: >
        Mechanical diff at M1 shows 4.0 §6 and 4.1 §7 are byte-identical modulo section numbering,
        as are 4.0 §14 and 4.1 §15 — so for the finding codomain the digest-referent import at
        4.1:277-288 supplies an implementer with nothing the edition of record lacks, and @ultpjo's
        premise is not borne out HERE, whatever holds elsewhere. Three real deltas remain and are
        filed rather than reconciled, per @ultpjo. 4.0:304-306 says two GARDs holding identical GELs
        hold identical Constitutions; 4.1:688-693 says the GEL alone does not suffice and the
        triple governs — pinned 4.1, because the import at 4.1:277-288 reaches 4.0's EVALUATOR
        sections and the definitions section is not one, and because succession takes effect at the
        effectuation coordinate (4.1:2124-2126). Note what makes this dangerous rather than tidy:
        4.0's bytes are immutable and carry no erratum, so an implementer told the kernel "binds
        with full force" meets the GEL-alone sentence with nothing marking it superseded. Second,
        one imported wall — acts consumed as grounds require committed receipts — sits in 4.0's
        openness clause, not in its evaluator sections, so the referent does not cover the wall it
        names. Third, 4.1:284 imports "the canonical ordering and selection of evidence" and 4.0
        contains an ordering of BUNDLES and a selection of DEFEATS, not an ordering of evidence;
        the only canonical ordering of evidence anywhere is 4.1 §17, which has no 4.0 counterpart
        and so cannot be part of what the digest imports. Pinned: implement §17's order as 4.1-only
        law, and rejected treating it as imported, which would make an engine conforming to the 4.0
        walls alone owe a permuted-arrival guarantee its own edition never states.
