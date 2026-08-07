# thesmo — Intent Tree (this.i)
#
# Source of truth for thesmo's design intentions and the decisions that follow from them,
# per the Bakobo intent-first methodology (../dev/methodology.md). Code and docs/ are DERIVED
# artifacts. M1 (the §7 evaluator walls in src/thesmo/core/) is implemented; stage-status: planned
# still marks the nodes that describe code-to-be.
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
    M1's twenty-two readings of the finding codomain = decision:
      id: 7h7nazgl
      stage-status: planned
      why: >
        Custos §7 — the codomain, the transition system, the evidence ordering, the two currents
        — is the whole of what M1 core/ implements, and reading it closely produced twenty places
        where a conforming engine has a genuine choice — twenty on the first close read, two
        more as the module surfaces were typed. Each is banked below as its own node with
        the rejected reading named; the long form, with quoted spans and the inputs that
        discriminate the readings, is docs/readings-alpha.md, which this node's children index.
        Chose one node per reading over a single node summarizing them, because a summary cannot
        be rebutted reading-by-reading and because @7z2ifi makes each node the finding text we
        owe the specification's author. Tradeoff accepted: twenty nodes is a lot of tree for one
        milestone, and the ones marked convergent may turn out to be noise. Sixteen of the
        twenty-two are DIVERGENT — two conforming engines produce different findings on committed
        bytes — which is the thing @l7al6o exists to demonstrate.
      children:
        Affirmed carries its bundle and clause set, though §7.3 omits it = decision:
          id: lkfaqca
          why: >
            §7.1 gives affirmed a ground ("the evidence bundle and the clause set under which it
            was appraised") but §7.3's "Required payloads" enumerates only defeated, pending and
            self-convicted — while claiming to be a complete enumeration. Rejected the reading
            that affirmed is a nullary constructor: §1.4 axiom 1 says the codomain "admits no
            bare verdicts", and an axiom outranks an enumeration that dropped a row. The cost of
            being wrong is that our affirmed findings carry payload no other engine emits, so
            byte-comparison against a §7.3-literal engine fails on every affirmation.
        Every finding carries the triple it was computed over = decision:
          id: krkkmwhh
          why: >
            §14 rules that "every finding retains its position, its defeated clause, its
            verification grain, and its committed law head", while §7.3's payload list mentions
            neither position nor law head. Rejected treating those as carriage supplied by a
            wrapper: §14's span says "every finding", and a value that drops two of axiom 2's
            three inputs cannot be checked against them by the stranger the whole design is
            written for. Consequence carried openly: "verification grain" appears exactly once
            in 4.1, is defined nowhere in either edition, and is therefore NOT implemented.
        Requirement kind and pending species are two fields, not one = decision:
          id: 2kzvek2
          why: >
            §7.3 has each requirement element carry "requirement kind"; §7.2 additionally rules
            that a pending finding "SHALL carry the species of each of its requirement elements".
            Rejected reading them as one field under two names: §7.2's species enumeration is
            closed at four cure paths, while §6 and §8 describe element content (required schema,
            expected issuer) that cannot be expressed in it, so a single field would have to be
            both closed and open. This one is load-bearing for bytes: §7.3 sorts elements by
            "subject, then kind", so the two readings sort the same set differently.
        Refusal is a returned value, not a raised exception = decision:
          id: iezwqh
          why: >
            §1.1 and §7.5 both say the refusal is "recorded as an operational fact", and §1.4
            axiom 3 and §17 both require it to name what is missing. Rejected raising: you cannot
            record what you threw away, and in Python an exception invites a caller to swallow
            exactly the fact the standard obliges it to keep. Refusal is a type disjoint from
            Finding, so the codomain stays four-valued (§15's wall) without hiding the refusal.
            Both readings agree on WHICH invocations refuse, so this is API shape, not semantics.
        The bundle is a set of coordinate-bearing items, ordered inside the fold = decision:
          id: vwqohe
          why: >
            §7.3 orders bundles by the subset relation (so a bundle is a set) while §17 requires
            the fold to consume its log in one committed order (KEL anchoring order, then the
            anchoring event's seal list). Rejected pushing ordering out to the substrate adapter:
            order would then reach the fold from outside the closed triple, which axiom 2 forbids,
            so each evidence item carries its own committed coordinate and the fold sorts. §17
            forbids only UNCOMMITTED tiebreaks and states none for two items at one coordinate;
            we pin the item identifier's bytes ascending, which is lawful but not unique — a
            different committed tiebreak changes which item is first-seen (see @r5p4h2).
        Byte-identity is undecidable at this layer, so core/ compares structure = constraint:
          id: holyd22k
          why: >
            §7.3 makes byte-identical agreement the conformance predicate for findings; §15
            confesses the carriage encoding of this document's object classes is an undesigned
            deliverable. No encoding exists under which the predicate can be evaluated, so core/
            gives findings structural value equality over frozen, canonically ordered components
            and defers bytes to the layer the standard leaves open (@tswf4m owns that choice).
            Driving constraint: inventing an encoding here would silently answer the open
            question rather than exhibit it. Every "differ byte for byte" claim in
            docs/readings-alpha.md means: differ structurally, under any injective encoding.
        The empty subcode orders LAST, against "lexicographic minimum" = decision:
          id: kjqxel
          why: >
            §7.3's canonical selection says the finding cites "the lexicographic minimum of
            (defeater-class rank, citation identifier, subcode)" and then says that where the
            clause defines no subcode "the subcode is empty and orders last". Under any
            lexicographic order the empty string is the MINIMUM — it prefixes everything — so the
            two sentences contradict. Rejected the pure-lexicographic reading, which would make a
            deliberately drafted final clause vacuous; the specific governs the general. This is
            the sharpest divergence found: two defeats of one class citing one clause, one with
            subcode "a" and one with none, are selected oppositely by the two readings, and the
            selected citation is what §13.1 recourse then rests on.
        Defeat short-circuits; only affirmation must discharge the whole space = decision:
          id: xr3rp7
          why: >
            §7.3's affirmation discipline says an evaluator holding a bundle that leaves any
            enumerated defeater-check unexamined "returns pending with that check as its typed
            requirement, never affirmed". Rejected extending that to defeat, which is the reading
            we prefer on structure: it would make the set of simultaneously available defeats
            complete and canonical selection stable under bundle growth. We rejected it because
            the span names affirmed, twice, and reading a restriction into a ruled span the span
            does not carry is legislating — the exact thing axiom 3 forbids the fold to do.
            Accepted consequence, and it is a defect report: under the pinned reading a defeated
            finding's CITATION changes as the bundle grows, which contradicts the same
            paragraph's "refines and never contradicts" and is not covered by the forbidden-edge
            table (defeated to defeated with a different citation is unruled).
        Requirement elements dedup on their sort key, merging species by declaration order = decision:
          id: kdrqzc
          why: >
            §7.3 requires "deduplicated elements … in canonical order (subject, then kind, then
            citing-clause bytes)". Rejected deduplicating on the whole element including species:
            two elements could then share a sort key, the canonical order would be a preorder,
            and the finding's bytes would be undetermined — unsatisfiable against the same
            section's byte-identity obligation. Deduplicating on exactly the sort key makes the
            order total, at the price of a species-merge rule the standard does not state; we
            take the minimum in §7.2's declaration order (absent, window-open,
            unresolved-conflict, expired/abandoned), a committed order per axiom 4. That invented
            merge rule is itself an underdetermination the standard should close.
        Citing-clause lists are sorted by clause identifier, not by law order = decision:
          id: nxoq2hd
          why: >
            §7.3 has each element carry "the list of citing clauses" and sorts elements by
            "citing-clause bytes", but never states the order WITHIN the list. Rejected
            preserving the order in which the committed law enumerates the clauses: the fold's
            three inputs include a law head, which is a self-addressing identifier and not an
            ordered clause list, so under that reading the fold consumes an order it cannot
            derive from its own inputs (axiom 2, axiom 4). Sorting by identifier bytes is
            derivable from what the fold holds. Both readings are lawful and they render the same
            element differently, so this is a byte-level fork. Same clause, second fork:
            flattening a LIST to bytes needs a separator or it is not injective (["a","bc"] and
            ["ab","c"] both flatten to abc, leaving the canonical order non-total and the
            finding's bytes undetermined); we pin a NUL join, below every character a
            self-addressing identifier can carry. A separator ABOVE the identifier alphabet
            reorders elements whose clause lists prefix one another. The standard states none.
        Defeater classes compare by their stated rank, not by their names = decision:
          id: zmwnx35s
          why: >
            §7.3 says to take the "lexicographic minimum" of a tuple whose first component is a
            "defeater-class rank", and then ranks the classes crypto, authority, merit,
            superseded — an order that is not alphabetical. Rejected comparing the class names as
            bytes, which is what "lexicographic" literally invites and which swaps authority
            ahead of crypto. Recorded rather than passed over because the wrong reading is the
            one an implementer gets BY ACCIDENT if it serializes the class before comparing, and
            the inputs that discriminate — a badly-signed act by an unauthorized party — are
            ordinary, not exotic.
        "First-seen" means first in committed order, never first observed = decision:
          id: r5p4h2
          why: >
            §7.4's tainting current says "first-seen survives". Rejected the observational
            reading on three independent grounds: axiom 4 bans an uncommitted order that affects
            a finding, §12.1 says "discovery order is observer-relative and consulted by
            nothing", and §17 requires permuted arrival orders to fold to byte-identical
            Constitutions. The word itself is the defect — arrival vocabulary inside a wall
            (§1.4 imports "first-seen survival" by digest referent) whose architecture forbids
            consulting arrival. Under the rejected reading two evaluators who fetched a
            duplicitous pair in opposite orders keep different survivors from identical bytes.
        Identity edges are permitted; the "complete enumeration" covers 12 of 16 pairs = decision:
          id: fxn65z
          why: >
            §7.3 declares itself the complete enumeration of the transition system, then rules
            five permitted and seven forbidden edges. Four values admit sixteen ordered pairs;
            the four identity pairs appear in neither table. Rejected "unenumerated therefore
            forbidden": §7.3 elsewhere requires a larger bundle to refine rather than contradict,
            which in the ordinary case means returning the same value, so that reading forbids
            the common case and makes an engine reject its own idempotent recomputation. The
            completeness claim is false as written, and we file it as such rather than repairing
            it silently.
        The transition system is a relation over recomputations, not a machine we advance = decision:
          id: na3tebqk
          why: >
            §7.3 calls the finding type "a state machine" and, twelve lines later, calls a
            finding "a function of exactly three inputs" whose repetitions are byte-identical.
            Rejected holding per-question finding state and mutating it as evidence arrives:
            retained state is "local state", which the same paragraph names as an input that may
            not influence a finding. So core/ recomputes from each triple and exposes the tables
            as a checker over ordered PAIRS of findings; a forbidden pair raises a conformance
            error and is never silently coerced. Under the rejected reading an engine sitting at
            affirmed refuses to compute defeated over a grown bundle; under ours it computes it
            and reports the wall violation, and the two differ observably on one input.
        Self-conviction always needs a bearing pair, including at the governance tier = decision:
          id: plnfze
          why: >
            §7.3's pending-to-self-convicted row reads "a bearing contradictory pair, or new
            governed-status evidence … enters the bundle". Rejected reading the disjuncts as
            independent sufficient conditions: the resulting finding would be unconstructible,
            because §7.1 and §7.3 both require a self-convicted finding to carry the canonical
            proof package FOR THE CONTRADICTORY PAIR, and under that reading there is no pair. We
            read the second disjunct as naming where the pair comes from at T3 — contradictory
            enactments under one committed predicate, per §7.4. The rejected reading makes the
            most destructive edge in the system reachable with no duplicity at all.
        A question's first finding may be any of the four values = decision:
          id: uw7kg74
          why: >
            §7.3 calls pending "the non-terminal bottom", which can be read as an initial state
            every question passes through. Rejected that: a finding is a function of its triple,
            so its value is fixed by the triple and not by a history the triple does not contain,
            and positing an unobserved pending predecessor would make the first finding depend on
            whether an earlier appraisal happened. Logged as convergent — no committed bytes
            distinguish the readings — precisely so that a later reader can see it was considered
            rather than missed.
        Contested standing is computed beside the codomain, never inside it = decision:
          id: b7773r
          why: >
            §7.4 says a lower-tier self-conviction leaves what was affirmed above "converted to
            contested standing rather than to nothing", and contested standing is not one of the
            four values. Rejected treating the conversion as literal: it needs either a fifth
            codomain member, which §15's wall forbids in as many words ("the evaluator's return
            type is the four-valued finding codomain and nothing else"), or the affirmed-to-
            self-convicted edge, which §7.4 itself forbids by insisting breach and duplicity
            never blur. So the affirmed finding is unchanged — it "remains a record" — and taint
            is a non-Finding marker on the subject's standing going forward. Under the rejected
            reading an affirmed finding's bytes change when a lower tier self-convicts.
        Annihilation reaches pending dependents only, as a theorem = decision:
          id: bwq5ghwn
          why: >
            §7.4's defeat current voids what was built on a defeated lower-tier finding, while
            §7.3 forbids affirmed-to-defeated absolutely. Rejected the reading that the cascade
            overrides the forbidden edge: that drives a cascade through a wall §15 names as
            fixed, and a wall with an unstated exception is not a wall. Under the affirmation
            discipline a dependent could only be affirmed over a bundle discharging its ENTIRE
            requirement space, and defeating evidence is ex-ante enumerable, so an affirmed
            dependent is one whose lower-tier check was already examined — annihilation can only
            ever act on a pending dependent, and pending-to-defeated is permitted. core/ fails
            closed on an affirmed dependent presented for annihilation rather than converting it.
            Note the derivation leans on @xr3rp7: it survives defeat short-circuiting, but not an
            edition that extends short-circuiting to affirmation.
        Bearing at the registry and governance tiers is committed law, or we refuse = decision:
          id: 62dtu6n
          why: >
            §7.3 says contradictory pairs "convict only where they bear on the question" and
            names a decision procedure only at the key tier (the substrate's superseding-recovery
            rules). Rejected the structural default any implementer reaches for — same subject,
            same proposition — because that is a composition rule, and §7.5's ratified text says
            the evaluator "SHALL refuse the invocation and SHALL NOT legislate the missing seam"
            exactly there. So where the domain's law commits no bearing predicate at T2/T3, the
            fold refuses. The rejected reading returns self-convicted where ours returns a
            refusal, and §13.1 recourse hangs off which.
        An annihilated dependent inherits the lower defeat's class and citation = decision:
          id: 2lc26h
          why: >
            §7.4's defeat current voids dependents but says nothing about the payload of the
            resulting finding, while §7.3 requires every defeated finding to carry a class and a
            citation. Rejected citing the lower-tier FINDING: no section mints an identifier for
            a finding — §13.1 pins evidence by digest and states the finding by its citation — so
            that reading needs a construct the standard does not supply. Dependents "were never
            valid" for the same reason their ground was never valid, so they inherit it. Two
            cases §7.4 does not reach at all, pinned here: an already-defeated dependent puts the
            annihilating defeat into the available set and re-runs canonical selection (leaving
            the old citation would make the finding depend on the order cascades were applied in,
            an ambient order axiom 4 forbids), and a self-convicted dependent is untouched,
            because self-conviction is terminal for its question.
        Taint marks any dependent's standing, not only an affirmed one = decision:
          id: 6h4dxyr7
          why: >
            §7.4 names only the affirmed case when it says what converts to contested standing.
            Rejected bounding the current there: the same bullet says the subject's voice is
            poisoned going forward, and withholding the marker from a defeated dependent would
            leave a defeated-then-duplicitous subject looking cleaner going forward than an
            affirmed one. Under @b7773r the finding is unchanged either way, so the readings
            differ only on a non-finding marker that no ruled span types — which is why this is
            banked as convergent rather than switched.
        Law-relative duplicity with no committed predicate is evidence, not refusal = decision:
          id: ided2r
          why: >
            §7.4 rules that a frame that never committed the violated predicate "SHALL consume
            them as evidence, never as conviction". Rejected refusing: refusal is for a MISSING
            rule, and here the rule is present and says "not a conviction here". Banked despite
            being convergent because this case and @62dtu6n look identical from inside the fold —
            both are "the law says nothing I can convict on" — and they resolve opposite ways;
            an implementer who does not notice the seam will get one of them wrong.

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
