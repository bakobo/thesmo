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
          children:
            The M1 legs cannot be carried forward to 4.2 = tension:
              id: aq2sbj
              nature: >
                @beue6f ruled that both branches evolve independently through several more rounds,
                with one promoted late. @pyyo5y makes that unaffordable at 4.2. m1-alpha and
                m1-beta hold a complete reading of 4.1 §7; the successor text is renumbered,
                repaired at eight sites, and repaired in several places BECAUSE of what these two
                legs found. An implementer carrying a 4.1 reading into 4.2 is doing a diff read,
                and a diff read answers "did the repair land" — a question the maintainer can
                already answer from the bytes — instead of "does this text underdetermine an
                engine," which is the only question that produces findings. Meanwhile the parent
                ruling's other half still binds: deleting either branch destroys the executed
                divergence behind Custos #27, which is the strongest artifact the project has.
              resolution: >
                Freeze both at their M1 state as the evidence record of the 4.1 cycle, and open new
                legs against 4.2 rather than advancing these. The branches stay in the repository,
                stay pushed, and stay named in the M1 reconciliation; nothing is deleted and
                nothing is merged. @beue6f's "promote one late" survives, but the candidate for
                promotion is drawn from the 4.2 legs, not from these. Rejected advancing them under
                a rule forbidding the implementer to consult their own prior register, which was
                the obvious cheap repair: it asks an implementer to unknow a reading they wrote,
                which is not a property anyone can verify or enforce. Rejected deleting them once
                frozen — the freeze is what makes them evidence.
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
      # Discharged at 4.2 — see @pyyo5y. 4.2 §1.4 stopped importing the kernel by referent, so the
      # two-edition reading window this node imposes applies to the 4.1 cycle only. Kept, not
      # deleted: the M1 legs read under it, and #23 came out of it.
    The edition of record is 4.2, and the blind read is one file = decision:
      id: pyyo5y
      why: >
        Custos 4.2 ratified 2026-08-07 (sha256 68cc5c9b7164b33dffcf7b705a0d1301fe108c647d35638fec
        61d52d29b2775a, anchored at its authority KEL sn 191/192), consuming 4.1 whole. It is a
        regeneration rather than a revision: 3,940 lines against 2,471, forty-eight accounted
        deltas, Chapter 2 added entire, and every section renumbered — the surface M1 read as §7 is
        §8. Two consequences bind the blind brief. First, 4.2 §1.4 says it "imports nothing by
        pointer, because a wall carried by reference into a predecessor's bytes can be neither read
        nor repaired in this document and drifts unowned," which discharges @ultpjo: the reading
        window is now one file and the kernel is not in it. Second, all nine findings M1 filed are
        closed, and #27 was closed in beta's direction using beta's own argument (4.2 §8.3: "the
        deduplication key sees every field the element carries"), so re-running M1's questions
        against 4.2 would confirm repairs rather than find defects. Rejected carrying 4.1 alongside
        4.2 as a second readable file: a leg holding both reads the diff, and a diff read is a
        reading of the repair history, which is precisely the commentary @qmz2o4 excludes.
    One leg is not Claude = decision:
      id: u6ykxs
      why: >
        M1's two legs were independent in the sense the brief demanded — neither knew the other
        existed — and shared everything else: the same weights, the same account, the same brief,
        the same scaffold, and the same hour (both engines written 2026-07-29 17:23–17:40). They
        diverged anyway, so the instrument works; but the strongest form of the claim thesmo wants
        to make ("the specification underdetermines a conforming engine") is weakened by a common
        prior nobody measured. Custos has already measured what a second model family buys: its
        42-2 integration round ran a two-leg collider and recorded four exhibit-grade findings from
        the gpt-5.6 leg that the same-family leg "did not catch — the collider earning its cost,"
        all four at the KERI/ACDC/CESR substrate boundary. So from M2 one leg per collision zone
        runs on a different model family, dispatched through `codex exec`. Rejected running the
        non-Claude leg as a reviewer of the Claude legs, which is what its budget most easily
        affords: a reviewer inherits the thing it reviews, and inheritance is the contamination the
        whole design exists to prevent. Tradeoff accepted: that leg is rate-limited, so it writes a
        readings register and expected values rather than an engine, and its divergences are
        executed by running the Claude engines against its cases.
    Legs are cut from a sanitized base, not from main = decision:
      id: fxbwie
      why: >
        Blindness is a property of the workspace, not of the instructions in it. A worktree cut
        from main hands its occupant docs/readings-alpha.md and -beta.md, docs/m1-reconciliation.md,
        docs/research/ (which names filed Custos findings by number), tools/differential_pending.py
        (the reproduction of the executed divergence), src/thesmo/editions.py (whose docstring
        states a specification defect outright), and this very file — which since @pyyo5y quotes a
        repaired clause verbatim and at @ipjprf names what a target section is suspected of. Every
        one of those is forbidden by docs/blind-brief.md, and all of them would arrive inside the
        window regardless, because the brief governs what a leg *seeks* and a checkout is what a
        leg *has*. Driving constraint: at M1 blindness was enforced by construction on the
        specification side — a directory containing only the ratified files — and the repository
        side was never given the same treatment because main carried nothing worth hiding yet. It
        does now. So `m2-base` carries the toolchain, the rules, the empty register template and a
        pruned this.i, and every leg branch is cut from it. Rejected branching from the M0 scaffold
        commit, which predates the M1 record and would have been free: it also predates the 4.2
        brief and still carries @ultpjo, whose text states the 4.1 two-edition defect. Rejected
        trusting the brief alone — an instruction not to read a file in the working tree is a rule
        whose observance nobody can verify afterwards, and the one failure this project cannot
        recover from is the contamination nobody noticed.
      children:
        A leg may know the rules and nothing about the document = constraint:
          id: 5rvdq2
          why: >
            The pruned tree keeps the goal, the blindness constraint and its plumbing child, the
            register discipline, the pin-one-reading rule, and the layout decision — everything a
            leg must obey. It drops every node that names a clause, a finding, an edition's defect,
            or another leg's surface, and the referenced-but-leaking nodes are rewritten to their
            rule and stripped of their evidence. Driving constraint: at M1 the legs read @ultpjo,
            which states a defect, because without it they would have built a non-conforming engine
            against a two-edition referent — the disclosure bought conformance. At 4.2 that trade
            is gone: §1.4 imports nothing by pointer, so there is no defect a leg must be told
            about in order to build correctly, and the looser line has nothing left to buy.
            Rejected keeping @3b4tjm whole for its "implement the walls, refuse above them"
            guidance: its closing sentences name a suspected defect site, and a leg that re-derives
            the walls posture from the document has told us something, where a leg handed it has
            not.
    M2's legs ran substrate-blind, which the brief does not require = tension:
      id: 7eofhd
      nature: >
        docs/blind-brief.md permits a leg the KERI, ACDC and CESR specifications and keripy as
        substrate references, and has since M1. The launch instructions the maintainer wrote for
        M2 said "you may read exactly ONE file about Custos" and enumerated only the edition — a
        guard stricter than the document it was meant to enforce. Every Claude leg honoured the
        stricter guard, and the jail at @fxbwie makes it unconditionally true of the Codex leg,
        which has no network path to a substrate specification at all. Leg delta reported the
        cost on its own initiative: it could not confirm CESR's derivation code for the
        Blake3-256 digest class, and its first invention takes the shape it does partly for that
        reason. The error is the maintainer's, not any leg's.
      resolution: >
        Let it stand for M2 and record it here rather than re-running anything. The guard was
        applied identically to all five legs, so the legs remain comparable to each other, which
        is the property the collision zone depends on; and a leg that has read no substrate is
        strictly more conservative about what §18 and §19 determine, so a "could not build"
        under this guard is weaker evidence than it looks while a DIVERGENT reading is
        unaffected. The correction that matters is to the READING of the results, not to the
        results: where a leg reports it could not build something for want of a substrate fact,
        that is this node's artifact and not a finding against Custos, and the reconciliation
        must separate the two before anything is filed. Rejected re-running the legs with the
        brief's actual window — it would spend the whole budget to relax a constraint that
        biases against false findings. Rejected quietly widening the guard for M3 without a
        node, which would leave two milestones incomparable for a reason nobody recorded.
    The case format is plumbing, and M2 should have coordinated it = decision:
      id: aatmji
      why: >
        @pdig63 permits coordinating anything the Constitution's value does not depend on, and
        names vector file formats as its first example. M2's briefs went the other way: each leg
        was told the fields inside a case's `given` and `then` were its own choice and not to
        invent a neutral schema, on the reasoning that a shared schema would pre-empt real
        questions — whether an answer is a finding, a refusal or a bare value is exactly the kind
        of thing legs should disagree about. The reasoning was sound and the consequence was not:
        at reconciliation all 46 cases were unreadable by the other leg's engine, so the
        differential instrument M1 built could not be run at all, and the divergence that matters
        most is still argued rather than executed. From M3 the ENVELOPE is coordinated — the case
        file's outer keys, and a stimulus vocabulary for naming events, coordinates, seals and
        spans — while `then` stays entirely the leg's own, because that is where the disagreement
        lives and coordinating it would be coordinating the answer. Rejected keeping the M2 rule
        and translating by hand: a translation is the maintainer's reading imposed on a blind
        leg's stimulus, which is the contamination this design exists to exclude, and the one
        translation attempted at M2 tripped a different must-reject and proved nothing. Rejected
        coordinating the whole schema including `then`, which would hand every leg the shape of
        the answer.
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

Construct, never review = decision:
  id: kcmw4c
  why: >
    By its ratification 4.2 had been through a full gauntlet, a seed station, a targeted
    re-gauntlet, a two-model-family collider, and a seed-reconciliation census, and its appendix of
    record accounts every delta under a governing ruling. Review-shaped instruments have been run
    against these bytes to exhaustion, and a further one competes with all of them for novelty.
    What has never been run against 4.2 is construction: nobody has tried to build from it. The
    ratifying authority's own docket for the successor edition (custos #77) names "full
    implementability as the bar," which is the evidence only a builder produces. Driving
    constraint: thesmo's marginal finding lives wherever the document has to survive being turned
    into a total function, and nowhere else. So every M2 leg builds or states concrete expected
    values, and none of them reviews. Rejected commissioning another adversarial reading round,
    which is cheaper per finding to run and would mostly rediscover the gauntlet's returns.
  children:
    The collision zone is the GEL grammar and the compact receipt form = constraint:
      id: ipjprf
      why: >
        Cross-leg divergence is only obtainable where legs cover the same text, so the shared
        surface must be small enough for three legs and dense enough to fork. §18 and §19 (4.2
        L3061–3479, ~420 lines — near-identical in size to the §7 slice M1 finished in an hour)
        are chosen over the alternatives for three reasons. §18 is where axiom 4's membership face
        has to cash out: "every span the fold consumes as its log is derivable from committed
        bytes" is unsatisfiable if the grammar affords no decision procedure for GEL membership
        from the KEL alone, and Custos's own vector ledger carries a `membership` family reading
        "which spans are the GEL, and what happens when that is underivable" — suspected, never
        proven. §19 is the most substrate-deep section in the document, which is where @u6ykxs's
        non-Claude leg has a measured edge. And a form standing on three named gates is the classic
        site at which two implementers order the gates differently and neither notices. Rejected
        Chapter 2 for the shared zone despite it being the root the 4.3 clean-root program will be
        rebuilt on: it is a typing chapter, its output is a classification rather than a finding,
        and it forks on doctrine where a second model family buys least.
    Closure audits run one leg, because their product is a table = decision:
      id: 6rhjga
      why: >
        Two surfaces are worth reading at M2 whose instrument is completeness rather than
        disagreement, and spending a second leg on either buys nothing. Chapter 2 built as a TOTAL
        classifier — object in, three axes out — either covers the object classes §12 names or does
        not, and a gap is a Chapter 2 defect under §1.7's own law-closure test whether one leg
        finds it or five do. The §1.7 comprehension gate (4.2 L410) is the same shape: for every
        construct introduced after Chapter 1, state its composition in the seven primitives or name
        the closure that failed. Custos #37 claims the gate is satisfied in one of fifteen sections
        and #75 says it is unrun for eleven constructs; neither is a table a stranger can check,
        and the deliverable here is exactly that table. Rejected doubling these legs for symmetry
        with the collision zone — a second opinion on a totality check is a second opinion on
        arithmetic.

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
