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
          # Open — no resolution. Candidates: (a) thesmo.engines.alpha/.beta behind one interface;
          # (b) keep both as branches and run the harness across worktrees; (c) promote one to
          # core/ and keep the other as a conformance oracle. Deferred to the M2 interview so it
          # is decided deliberately rather than by whichever merge happens first.
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
