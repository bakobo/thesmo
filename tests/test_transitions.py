"""The complete transition system (Custos 4.1 §7.3).

§7.3 calls itself "the complete enumeration — states, payloads, permitted
transitions with their conditions, forbidden transitions, and terminality", so
the first test here is a census: five permitted plus seven forbidden is twelve,
which is exactly the number of ordered pairs of *distinct* values. Every
self-edge is therefore enumerated nowhere, which is entry 14 of
``docs/readings-beta.md``.
"""

import inspect
import itertools

import pytest

from thesmo.core.errors import ConditionUnmet, ForbiddenTransition, MalformedInput
from thesmo.core.finding import (
    Affirmed,
    Citation,
    Defeat,
    DefeaterClass,
    Defeated,
    Pending,
    PendingSpecies,
    RequirementElement,
    SelfConvicted,
    Verdict,
)
from thesmo.core.transitions import (
    FORBIDDEN,
    PERMITTED,
    Discharge,
    Growth,
    admits_no_further_evidence,
    check_refinement,
    check_transition,
    is_terminal,
    permits,
)
from thesmo.core.triple import EvidenceBundle, EvidenceItem, LawHead, Position

LAW = LawHead("Elaw")
POS = Position("Egel", 4)
A, B = EvidenceItem("Ea"), EvidenceItem("Eb")
SMALL = EvidenceBundle.of(A)
LARGE = EvidenceBundle.of(A, B)
PAIR = Growth(bearing_pair=True)


def a_requirement():
    return RequirementElement(
        subject="Es", kind="k", citing_clauses=("Ec",), species=PendingSpecies.ABSENT
    )


def pending(position=POS):
    return Pending(LAW, position, requirements=(a_requirement(),))


def affirmed(position=POS):
    return Affirmed(LAW, position, bundle=SMALL, clause_set=("Ec",))


# --- the census ---


def test_the_enumeration_covers_every_edge_between_distinct_values():
    """Five permitted plus seven forbidden is every ordered pair of distinct values."""
    assert len(PERMITTED) == 5
    assert len(FORBIDDEN) == 7
    distinct = {(f, t) for f, t in itertools.permutations(Verdict, 2)}
    assert set(PERMITTED) | set(FORBIDDEN) == distinct
    assert not set(PERMITTED) & set(FORBIDDEN)


def test_every_enumerated_edge_states_its_reason():
    for reason in itertools.chain(PERMITTED.values(), FORBIDDEN.values()):
        assert reason


def test_no_backward_edge_exists_so_no_cycle_is_constructible():
    """§7.3's graph-form derivation: the permitted edges form a DAG."""
    rank = {
        Verdict.PENDING: 0,
        Verdict.AFFIRMED: 1,
        Verdict.DEFEATED: 1,
        Verdict.SELF_CONVICTED: 2,
    }
    assert all(rank[frm] < rank[to] for frm, to in PERMITTED)


# --- permitted edges and their conditions ---


def test_pending_affirms_when_the_requirement_set_discharges_affirmatively():
    check_transition(
        Verdict.PENDING, Verdict.AFFIRMED, Growth(discharge=Discharge.AFFIRMATIVE)
    )


def test_pending_defeats_when_the_requirement_set_discharges_by_defeat():
    check_transition(
        Verdict.PENDING, Verdict.DEFEATED, Growth(discharge=Discharge.DEFEAT)
    )


@pytest.mark.parametrize("frm", [Verdict.PENDING, Verdict.AFFIRMED, Verdict.DEFEATED])
def test_every_edge_into_self_convicted_needs_a_bearing_pair(frm):
    """this.i @mwprhoj3: the governed-status disjunct never stands alone."""
    check_transition(frm, Verdict.SELF_CONVICTED, PAIR)
    with pytest.raises(ConditionUnmet) as excinfo:
        check_transition(frm, Verdict.SELF_CONVICTED, Growth())
    assert excinfo.value.code == "THESMO_TRANSITION_CONDITION_UNMET"


def test_governed_status_evidence_alone_does_not_convict():
    """The discriminating input of entry 15: no pair, so no proof package exists."""
    with pytest.raises(ConditionUnmet):
        check_transition(
            Verdict.PENDING,
            Verdict.SELF_CONVICTED,
            Growth(governed_status_evidence=True),
        )


def test_pending_does_not_affirm_on_a_defeating_discharge():
    with pytest.raises(ConditionUnmet):
        check_transition(
            Verdict.PENDING, Verdict.AFFIRMED, Growth(discharge=Discharge.DEFEAT)
        )


def test_pending_does_not_defeat_on_an_affirmative_discharge():
    with pytest.raises(ConditionUnmet):
        check_transition(
            Verdict.PENDING, Verdict.DEFEATED, Growth(discharge=Discharge.AFFIRMATIVE)
        )


# --- forbidden edges ---


@pytest.mark.parametrize(("frm", "to"), sorted(FORBIDDEN, key=lambda e: (e[0], e[1])))
def test_every_forbidden_edge_is_refused_with_its_reason(frm, to):
    with pytest.raises(ForbiddenTransition) as excinfo:
        check_transition(frm, to, PAIR)
    assert excinfo.value.code == "THESMO_FORBIDDEN_TRANSITION"
    assert FORBIDDEN[(frm, to)] in str(excinfo.value)


def test_the_transition_system_is_tier_generic():
    """this.i @iidbntm: the ratified rule embeds 3.3's system "at T3" and stops.

    §7.1 says the four-valued scheme is instantiated at every tier but commits
    the *ordering* per tier and says nothing about the transitions. We read the
    system as a property of the finding type, which is tier-generic — so no
    function here takes a tier, and a key-tier finding cannot flip either.
    """
    assert "tier" not in inspect.signature(check_transition).parameters
    assert "tier" not in inspect.signature(check_refinement).parameters


def test_permits_reports_the_enumeration_without_conditions():
    assert permits(Verdict.PENDING, Verdict.AFFIRMED) is True
    assert permits(Verdict.AFFIRMED, Verdict.DEFEATED) is False


# --- self-edges ---


@pytest.mark.parametrize("verdict", list(Verdict))
def test_a_finding_that_has_not_moved_has_not_transitioned(verdict):
    """this.i @iouhhq: otherwise pending-to-pending is unlawful and no fold conforms."""
    check_transition(verdict, verdict, Growth())
    assert permits(verdict, verdict) is True


# --- terminality ---


def test_pending_is_the_non_terminal_bottom():
    assert is_terminal(Verdict.PENDING) is False


@pytest.mark.parametrize(
    "verdict", [Verdict.AFFIRMED, Verdict.DEFEATED, Verdict.SELF_CONVICTED]
)
def test_the_other_three_are_terminal_and_may_ground_recourse(verdict):
    """§13.1: recourse SHALL be grounded only on terminal findings."""
    assert is_terminal(verdict) is True


def test_only_self_conviction_admits_no_further_evidence():
    """§7.3: affirmed and defeated are final "except for one event"."""
    assert admits_no_further_evidence(Verdict.SELF_CONVICTED) is True
    assert admits_no_further_evidence(Verdict.AFFIRMED) is False


# --- monotonicity: the evidence ordering applied to a pair of findings ---


def test_a_grown_bundle_at_a_fixed_head_and_position_refines_lawfully():
    check_refinement(
        pending(),
        affirmed(),
        earlier_bundle=SMALL,
        later_bundle=LARGE,
        growth=Growth(discharge=Discharge.AFFIRMATIVE),
    )


def test_evidence_does_not_un_arrive():
    with pytest.raises(ForbiddenTransition) as excinfo:
        check_refinement(
            pending(),
            affirmed(),
            earlier_bundle=LARGE,
            later_bundle=SMALL,
            growth=Growth(discharge=Discharge.AFFIRMATIVE),
        )
    assert "un-arrive" in str(excinfo.value)


def test_monotonicity_is_at_a_fixed_law_head():
    """§7.3: "at a fixed law head and position, never over wall time"."""
    later = Affirmed(LawHead("Eother"), POS, bundle=LARGE, clause_set=("Ec",))
    with pytest.raises(MalformedInput):
        check_refinement(
            pending(),
            later,
            earlier_bundle=SMALL,
            later_bundle=LARGE,
            growth=Growth(discharge=Discharge.AFFIRMATIVE),
        )


def test_monotonicity_is_at_a_fixed_position():
    with pytest.raises(MalformedInput):
        check_refinement(
            pending(),
            affirmed(Position("Egel", 9)),
            earlier_bundle=SMALL,
            later_bundle=LARGE,
            growth=Growth(discharge=Discharge.AFFIRMATIVE),
        )


def test_a_settled_finding_does_not_flip_however_the_bundle_grows():
    """§7.3: "new defeat evidence yields a new finding at a new position"."""
    later = Defeated(LAW, POS, defeat=Defeat(DefeaterClass.MERIT, Citation("Ec")))
    with pytest.raises(ForbiddenTransition):
        check_refinement(
            affirmed(),
            later,
            earlier_bundle=SMALL,
            later_bundle=LARGE,
            growth=Growth(discharge=Discharge.DEFEAT),
        )


def test_a_poisoned_question_does_not_reopen():
    with pytest.raises(ForbiddenTransition):
        check_refinement(
            SelfConvicted(LAW, POS, proof="Eproof"),
            pending(),
            earlier_bundle=SMALL,
            later_bundle=LARGE,
            growth=Growth(),
        )
