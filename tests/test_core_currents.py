"""The duplicity ladder and the two upward currents (Custos §7.4).

§7.4's one sentence at keyword force is the design constraint for the whole
module: "Findings cascade between tiers in two distinct currents, and a
conforming evaluator SHALL NOT merge them." So the two currents are two
functions with two return types, and the only thing that runs both keeps their
outputs as a product (§7.5: compound results "preserve their component
propositions and grounds as a product rather than collapse them into a fifth
scalar shape").

Pinned readings under test: @b7773r (contested standing is not a finding),
@bwq5ghwn (annihilation reaches pending dependents only, as a theorem),
@2lc26h (what an annihilated dependent cites), @6h4dxyr7 (taint marks any
dependent), @ided2r (law-relative duplicity with no committed predicate).
"""

import pytest

from thesmo.core.currents import (
    LADDER,
    CascadeResult,
    ContestedStanding,
    DuplicityForce,
    Tier,
    annihilate,
    cascade,
    duplicity_force,
    first_seen_survivor,
    taint,
)
from thesmo.core.errors import GroundMissing, MalformedInput, WallViolation
from thesmo.core.finding import (
    Affirmed,
    DefeaterClass,
    Defeated,
    Finding,
    Pending,
    PendingSpecies,
    RequirementElement,
    SelfConvicted,
    Verdict,
)
from thesmo.core.triple import (
    AppraisalTriple,
    Coordinate,
    EvidenceBundle,
    EvidenceItem,
    LawHead,
    Position,
)


def item(said, anchor=0, seal=0):
    return EvidenceItem(said, Coordinate(anchor, seal))


TRIPLE = AppraisalTriple(
    bundle=EvidenceBundle.of(item("EEvi000")),
    law_head=LawHead("ELaw000"),
    position=Position("EGar000", 4),
)


def pending(question="dependent"):
    return Pending(
        question=question,
        triple=TRIPLE,
        requirements=(RequirementElement("EArt", "schema", ("EC1",), PendingSpecies.ABSENT),),
    )


def defeated(question="lower", defeater_class=DefeaterClass.CRYPTO, citation="ESeal", sub=""):
    return Defeated(
        question=question,
        triple=TRIPLE,
        defeater_class=defeater_class,
        citation=citation,
        subcode=sub,
    )


def affirmed(question="dependent"):
    return Affirmed(question=question, triple=TRIPLE, clause_set=("EC1",))


def convicted(question="lower", proof="EProof0"):
    return SelfConvicted(question=question, triple=TRIPLE, proof_package=proof)


class TestTheDuplicityLadder:
    """§7.4: "Duplicity is one crime with a rising voice unit"."""

    def test_three_rungs_in_rising_order(self):
        assert [tier.name for tier in Tier] == ["KEY", "REGISTRY", "GOVERNANCE"]
        assert Tier.KEY.rung < Tier.REGISTRY.rung < Tier.GOVERNANCE.rung

    def test_each_rung_names_its_voice_unit(self):
        assert "two events at one coordinate" in LADDER[Tier.KEY]
        assert "two registries" in LADDER[Tier.REGISTRY]
        assert "contradictory enactments" in LADDER[Tier.GOVERNANCE]

    def test_the_ladder_covers_every_tier(self):
        assert set(LADDER) == set(Tier)


class TestTheForceDistinction:
    """§7.4: key-tier duplicity "convicts in the medium, for every verifier,
    under no frame's law"; the upper two are law-relative."""

    def test_key_tier_convicts_in_the_medium_whatever_the_frame_committed(self):
        assert duplicity_force(Tier.KEY, predicate_committed=False) is DuplicityForce.MEDIUM
        assert duplicity_force(Tier.KEY, predicate_committed=True) is DuplicityForce.MEDIUM

    @pytest.mark.parametrize("tier", [Tier.REGISTRY, Tier.GOVERNANCE])
    def test_upper_tiers_convict_only_where_the_predicate_was_committed(self, tier):
        assert duplicity_force(tier, predicate_committed=True) is DuplicityForce.FRAME_LOCAL

    @pytest.mark.parametrize("tier", [Tier.REGISTRY, Tier.GOVERNANCE])
    def test_upper_tiers_without_the_predicate_yield_evidence_not_conviction(self, tier):
        # this.i @ided2r — "SHALL consume them as evidence, never as conviction".
        # Note this resolves the OPPOSITE way to @62dtu6n's missing bearing
        # predicate, which refuses: there the rule is absent, here it is present
        # and says "not a conviction here".
        assert duplicity_force(tier, predicate_committed=False) is DuplicityForce.EVIDENCE_ONLY

    def test_refuses_a_tier_that_is_not_one_of_the_three(self):
        with pytest.raises(MalformedInput):
            duplicity_force("key", predicate_committed=True)


class TestFirstSeenSurvival:
    def test_the_earlier_of_a_pair_in_committed_order_survives(self):
        early, late = item("EA", 1, 0), item("EB", 2, 0)
        assert first_seen_survivor([late, early]) is early

    def test_a_pair_is_two(self):
        # §7.4's currents run over "the contradictory pair"; three voices at one
        # coordinate is a different question this document does not reach.
        with pytest.raises(MalformedInput):
            first_seen_survivor([item("EA", 1, 0)])


class TestDefeatAnnihilatesUpward:
    """§7.4: "A defeated finding at a lower tier voids what was built on it
    [...] The dependents were never valid; annihilation is discovery, not
    change"."""

    def test_a_pending_dependent_becomes_defeated(self):
        result = annihilate(lower=defeated(), dependent=pending())
        assert result.verdict is Verdict.DEFEATED
        assert result.question == "dependent"

    def test_the_annihilated_dependent_inherits_the_lower_defeat(self):
        # this.i @2lc26h — the alternative cites the lower FINDING, and no
        # section of either edition mints an identifier for a finding.
        lower = defeated(defeater_class=DefeaterClass.MERIT, citation="EClauseX", sub="s2")
        result = annihilate(lower=lower, dependent=pending())
        assert (result.defeater_class, result.citation, result.subcode) == (
            DefeaterClass.MERIT,
            "EClauseX",
            "s2",
        )

    def test_an_affirmed_dependent_is_a_wall_violation_not_a_conversion(self):
        # this.i @bwq5ghwn. Under the affirmation discipline an affirmed
        # dependent is one whose lower-tier check was already discharged, so it
        # cannot be annihilated; converting it would drive the cascade straight
        # through the forbidden affirmed -> defeated edge.
        with pytest.raises(WallViolation) as caught:
            annihilate(lower=defeated(), dependent=affirmed())
        assert caught.value.code == "CORE-WALL-VIOLATION"
        assert "affirmed" in str(caught.value)

    def test_an_already_defeated_dependent_re_runs_canonical_selection(self):
        # this.i @2lc26h. Leaving the existing citation in place would make the
        # finding depend on the order cascades were applied in — an ambient
        # order, forbidden by §1.4 axiom 4.
        dependent = defeated(question="dependent", defeater_class=DefeaterClass.MERIT, citation="EM")
        lower = defeated(defeater_class=DefeaterClass.CRYPTO, citation="EC")
        result = annihilate(lower=lower, dependent=dependent)
        assert (result.defeater_class, result.citation) == (DefeaterClass.CRYPTO, "EC")

    def test_re_selection_keeps_the_lower_ranked_existing_citation(self):
        dependent = defeated(
            question="dependent", defeater_class=DefeaterClass.CRYPTO, citation="EC"
        )
        lower = defeated(defeater_class=DefeaterClass.SUPERSEDED, citation="EZ")
        result = annihilate(lower=lower, dependent=dependent)
        assert (result.defeater_class, result.citation) == (DefeaterClass.CRYPTO, "EC")

    def test_a_self_convicted_dependent_is_untouched(self):
        # §7.3: self-conviction is "terminal for its question — the question is
        # poisoned, and no further evidence rehabilitates it", and nothing
        # re-convicts it either.
        dependent = convicted(question="dependent")
        assert annihilate(lower=defeated(), dependent=dependent) is dependent

    def test_refuses_a_lower_finding_that_is_not_defeated(self):
        with pytest.raises(MalformedInput):
            annihilate(lower=convicted(), dependent=pending())

    def test_refuses_a_dependent_that_is_not_a_finding(self):
        with pytest.raises(MalformedInput):
            annihilate(lower=defeated(), dependent="pending")


class TestDuplicityTaintsUpward:
    """§7.4: "A self-conviction at a lower tier does not un-happen the history
    above it: committed history is monotonic, first-seen survives, and what was
    affirmed above converts to contested standing rather than to nothing"."""

    def test_contested_standing_is_not_a_finding(self):
        # this.i @b7773r. §15: "the evaluator's return type is the four-valued
        # finding codomain and nothing else." A fifth value would breach it, so
        # taint is computed beside the codomain, not inside it.
        result = taint(lower=convicted(), dependent=affirmed(), subject="EParty0")
        assert isinstance(result, ContestedStanding)
        assert not isinstance(result, Finding)

    def test_the_dependent_finding_is_returned_unchanged(self):
        dependent = affirmed()
        result = taint(lower=convicted(), dependent=dependent, subject="EParty0")
        assert result.surviving_finding is dependent
        assert dependent.verdict is Verdict.AFFIRMED

    def test_contested_standing_carries_the_proof_and_the_position(self):
        result = taint(lower=convicted(proof="EProofX"), dependent=affirmed(), subject="EP")
        assert result.proof_package == "EProofX"
        assert result.contested_from == TRIPLE.position
        assert result.subject == "EP"

    @pytest.mark.parametrize("dependent", [pending(), defeated(question="dependent")])
    def test_taint_marks_a_dependent_that_was_not_affirmed(self, dependent):
        # this.i @6h4dxyr7 — §7.4 explains the affirmed case rather than
        # bounding the current; withholding the marker would leave a
        # defeated-then-duplicitous subject looking cleaner than an affirmed one.
        result = taint(lower=convicted(), dependent=dependent, subject="EP")
        assert result.surviving_finding is dependent

    def test_refuses_a_lower_finding_that_is_not_self_convicted(self):
        with pytest.raises(MalformedInput):
            taint(lower=defeated(), dependent=affirmed(), subject="EP")

    def test_refuses_a_marker_with_no_subject(self):
        with pytest.raises(GroundMissing):
            taint(lower=convicted(), dependent=affirmed(), subject="")


class TestTheCurrentsNeverMerge:
    """§7.4: "a conforming evaluator SHALL NOT merge them"."""

    def test_a_defeat_cascade_carries_no_taint(self):
        result = cascade(lower=defeated(), dependent=pending(), subject="EP")
        assert isinstance(result, CascadeResult)
        assert result.annihilated is not None
        assert result.contested is None

    def test_a_duplicity_cascade_carries_no_annihilation(self):
        result = cascade(lower=convicted(), dependent=affirmed(), subject="EP")
        assert result.contested is not None
        assert result.annihilated is None

    def test_the_result_is_a_product_with_both_components_reachable(self):
        # §7.5: compound results "preserve their component propositions and
        # grounds as a product rather than collapse them into a fifth scalar
        # shape". There is deliberately no combined "invalidated" boolean.
        result = cascade(lower=defeated(), dependent=pending(), subject="EP")
        assert set(CascadeResult.__dataclass_fields__) == {"annihilated", "contested"}
        assert result.annihilated.verdict is Verdict.DEFEATED

    @pytest.mark.parametrize("lower", [affirmed(question="lower"), pending(question="lower")])
    def test_neither_current_flows_from_an_affirmed_or_pending_lower_finding(self, lower):
        # Breach and duplicity are the two crimes; nothing else cascades.
        with pytest.raises(MalformedInput):
            cascade(lower=lower, dependent=pending(), subject="EP")

    def test_breach_and_duplicity_stay_distinct_crimes(self):
        # §7.4: "defeated is conviction by another's citation; self-convicted is
        # conviction by one's own committed pair. No clause of this document
        # blurs them."
        by_defeat = cascade(lower=defeated(), dependent=pending(), subject="EP")
        by_duplicity = cascade(lower=convicted(), dependent=pending(), subject="EP")
        assert by_defeat.annihilated is not None and by_defeat.contested is None
        assert by_duplicity.contested is not None and by_duplicity.annihilated is None
