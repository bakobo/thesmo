"""The duplicity ladder and the two upward currents (Custos 4.1 §7.4).

The section's binding clause is "a conforming evaluator SHALL NOT merge them",
and it names no operation that would count as merging. These tests hold the
structural reading (this.i @mprtnb): the two currents have distinct types and
distinct constructors, and feeding one to the other raises rather than doing
something plausible.
"""

import pytest

from thesmo.core.errors import CurrentsMerged, GroundMissing, MalformedInput
from thesmo.core.finding import (
    Affirmed,
    Citation,
    Defeat,
    DefeaterClass,
    Defeated,
    Finding,
    SelfConvicted,
)
from thesmo.core.currents import (
    VOICE_UNIT,
    ContestedStanding,
    ContradictoryPair,
    Dependent,
    Tier,
    annihilate_upward,
    convict,
    first_seen,
    is_visible_at,
    may_convict,
    taint_upward,
)
from thesmo.core.triple import EvidenceBundle, EvidenceItem, LawHead, Position

LAW = LawHead("Elaw")
POS = Position("Egel", 4)
BUNDLE = EvidenceBundle.of(EvidenceItem("Ea"))

EARLY = EvidenceItem("Ez", anchor=Position("Ekel", 2), seal_index=0)
LATE = EvidenceItem("Ea", anchor=Position("Ekel", 7), seal_index=0)


def key_pair(**overrides):
    kwargs = {
        "subject": "Esubject",
        "tier": Tier.KEY,
        "first": EARLY,
        "second": LATE,
        "bears_on": ("may-act",),
        "proof": "Eproof",
    }
    kwargs.update(overrides)
    return ContradictoryPair(**kwargs)


def governance_pair(**overrides):
    return key_pair(tier=Tier.GOVERNANCE, predicate="Epredicate", **overrides)


# --- the ladder ---


def test_the_ladder_has_three_rungs_with_rising_voice_units():
    """§7.4: "why the tower has three rungs and not one"."""
    assert [t.value for t in Tier] == [1, 2, 3]
    assert set(VOICE_UNIT) == set(Tier)
    assert all(VOICE_UNIT[tier] for tier in Tier)


def test_each_tiers_duplicity_is_invisible_to_the_machinery_below():
    assert is_visible_at(Tier.GOVERNANCE, Tier.GOVERNANCE) is True
    assert is_visible_at(Tier.GOVERNANCE, Tier.REGISTRY) is False
    assert is_visible_at(Tier.KEY, Tier.GOVERNANCE) is True


# --- the contradictory pair ---


def test_a_pair_names_its_subject_its_voices_and_its_proof():
    pair = key_pair()
    assert pair.subject == "Esubject"
    assert pair.proof == "Eproof"


def test_a_pair_needs_two_distinct_voices():
    with pytest.raises(MalformedInput):
        key_pair(second=EARLY)


def test_a_pair_needs_a_subject():
    with pytest.raises(MalformedInput):
        key_pair(subject="")


def test_a_pair_needs_a_proof_package_identifier():
    with pytest.raises(GroundMissing):
        key_pair(proof="")


def test_registry_and_governance_pairs_name_the_predicate_they_violate():
    """§7.4: below the key tier, duplicity is law-relative."""
    with pytest.raises(MalformedInput):
        key_pair(tier=Tier.GOVERNANCE)
    assert governance_pair().predicate == "Epredicate"


def test_a_key_tier_pair_names_no_predicate():
    """Key-tier duplicity "convicts in the medium ... under no frame's law"."""
    with pytest.raises(MalformedInput):
        key_pair(predicate="Epredicate")


def test_a_pair_canonicalizes_the_questions_it_bears_on():
    pair = key_pair(bears_on=("b", "a", "b"))
    assert pair.bears_on == ("a", "b")


def test_bearing_is_read_off_the_pair_not_computed():
    """this.i @pbrejw2: bearing is a committed determination the fold consumes."""
    pair = key_pair(bears_on=("may-act",))
    assert pair.bears_on_question("may-act") is True
    assert pair.bears_on_question("is-seated") is False


def test_a_pair_may_bear_on_nothing_and_then_only_taints():
    """§7.3: duplicity elsewhere taints standing without converting this finding."""
    pair = key_pair(bears_on=())
    assert pair.bears_on_question("may-act") is False


# --- first-seen survival ---


def test_first_seen_is_first_in_committed_order_not_first_observed():
    """this.i @sr546w: the finding that matters most at M1.

    "First-seen survives" (§7.4, an imported wall) is read as first in the
    committed canonical order, because axiom 4 and §17 both forbid the fold to
    consume arrival order. A verifier reading the phrase the substrate's way
    computes a different survivor.
    """
    forward = key_pair(first=EARLY, second=LATE)
    reversed_ = key_pair(first=LATE, second=EARLY)
    assert first_seen(forward) is EARLY
    assert first_seen(reversed_) is EARLY


# --- the force distinction ---


def test_key_tier_duplicity_convicts_under_no_frames_law():
    assert may_convict(key_pair(), committed_predicates=frozenset()) is True


def test_governance_tier_duplicity_convicts_only_where_the_predicate_is_committed():
    pair = governance_pair()
    assert may_convict(pair, committed_predicates=frozenset({"Epredicate"})) is True
    assert may_convict(pair, committed_predicates=frozenset()) is False


def test_convict_builds_the_self_conviction_where_the_pair_bears_and_the_law_binds():
    finding = convict(
        governance_pair(),
        law_head=LAW,
        position=POS,
        question="may-act",
        committed_predicates=frozenset({"Epredicate"}),
    )
    assert isinstance(finding, SelfConvicted)
    assert finding.proof == "Eproof"


def test_a_pair_that_does_not_bear_converts_nothing():
    assert (
        convict(
            governance_pair(bears_on=("is-seated",)),
            law_head=LAW,
            position=POS,
            question="may-act",
            committed_predicates=frozenset({"Epredicate"}),
        )
        is None
    )


def test_an_uncommitted_predicate_is_consumed_as_evidence_never_as_conviction():
    """this.i @75ljyl6v: the ordinary machinery keeps its value; nothing refuses."""
    assert (
        convict(
            governance_pair(),
            law_head=LAW,
            position=POS,
            question="may-act",
            committed_predicates=frozenset(),
        )
        is None
    )


# --- defeat annihilates upward ---


def test_annihilation_emits_a_new_finding_at_a_new_position():
    """this.i @nggcv5f: the dependent's earlier finding is untouched."""
    defeat = Defeat(DefeaterClass.CRYPTO, Citation("Eseal"))
    lower = Defeated(LAW, Position("Etel", 1), defeat=defeat)
    dependent = Dependent(
        question="issuance-valid", law_head=LAW, position=Position("Egel", 12)
    )
    (annihilated,) = annihilate_upward(lower, [dependent])
    assert isinstance(annihilated, Defeated)
    assert annihilated.position == Position("Egel", 12)
    assert annihilated.defeat is defeat


def test_annihilation_inherits_the_lower_tier_class_rather_than_inventing_one():
    lower = Defeated(
        LAW, Position("Etel", 1), defeat=Defeat(DefeaterClass.CRYPTO, Citation("Eseal"))
    )
    (annihilated,) = annihilate_upward(
        lower, [Dependent("q", LAW, Position("Egel", 12))]
    )
    assert annihilated.defeat.defeater_class is DefeaterClass.CRYPTO


def test_annihilation_is_transitive_up_the_tower():
    """"an invalid seal voids the issuance ..., which voids the enactment"."""
    seal_defeat = Defeated(
        LAW, Position("Ekel", 1), defeat=Defeat(DefeaterClass.CRYPTO, Citation("Eseal"))
    )
    (issuance,) = annihilate_upward(
        seal_defeat, [Dependent("issuance", LAW, Position("Etel", 3))]
    )
    (enactment,) = annihilate_upward(
        issuance, [Dependent("enactment", LAW, Position("Egel", 8))]
    )
    assert enactment.defeat is seal_defeat.defeat


def test_annihilation_of_nothing_is_nothing():
    lower = Defeated(
        LAW, POS, defeat=Defeat(DefeaterClass.MERIT, Citation("Ec"))
    )
    assert annihilate_upward(lower, []) == ()


def test_a_dependent_names_its_question():
    with pytest.raises(MalformedInput):
        Dependent("", LAW, POS)


# --- duplicity taints upward ---


def test_taint_leaves_the_record_above_untouched():
    """§7.4: "the record it already made remains a record"."""
    standing = Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Ec",))
    conviction = SelfConvicted(LAW, Position("Ekel", 2), proof="Eproof")
    (contested,) = taint_upward(conviction, key_pair(), [standing])
    assert contested.surviving is standing
    assert standing.verdict.value == "affirmed"


def test_contested_standing_is_not_a_finding():
    """this.i @6mntbxri: §7.4 names a state the four-valued codomain lacks."""
    conviction = SelfConvicted(LAW, Position("Ekel", 2), proof="Eproof")
    standing = Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Ec",))
    (contested,) = taint_upward(conviction, key_pair(), [standing])
    assert not isinstance(contested, Finding)
    assert contested.subject == "Esubject"
    assert contested.tier is Tier.KEY


def test_contested_standing_carries_the_proof_of_the_pair_that_poisoned_the_voice():
    conviction = SelfConvicted(LAW, Position("Ekel", 2), proof="Eproof")
    standing = Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Ec",))
    (contested,) = taint_upward(conviction, key_pair(), [standing])
    assert contested.pair_proof == "Eproof"
    assert contested.canonical_bytes()


def test_contested_standing_needs_the_proof_it_rests_on():
    standing = Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Ec",))
    with pytest.raises(GroundMissing):
        ContestedStanding(
            subject="Es", tier=Tier.KEY, surviving=standing, pair_proof=""
        )


def test_tainting_nothing_is_nothing():
    conviction = SelfConvicted(LAW, POS, proof="Eproof")
    assert taint_upward(conviction, key_pair(), []) == ()


# --- the currents never merge ---


def test_a_self_conviction_may_not_be_run_through_the_defeat_current():
    """§7.4: "a conforming evaluator SHALL NOT merge them"."""
    conviction = SelfConvicted(LAW, POS, proof="Eproof")
    with pytest.raises(CurrentsMerged) as excinfo:
        annihilate_upward(conviction, [Dependent("q", LAW, POS)])
    assert excinfo.value.code == "THESMO_CURRENTS_MERGED"


def test_a_defeat_may_not_be_run_through_the_duplicity_current():
    lower = Defeated(LAW, POS, defeat=Defeat(DefeaterClass.MERIT, Citation("Ec")))
    standing = Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Ec",))
    with pytest.raises(CurrentsMerged):
        taint_upward(lower, key_pair(), [standing])
