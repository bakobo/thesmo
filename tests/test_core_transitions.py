"""The complete transition system (Custos §7.3).

§7.3 calls itself "its complete enumeration — states, payloads, permitted
transitions with conditions, forbidden transitions, and terminality". Two
readings had to be pinned before it could be implemented:

- @fxn65z — five permitted edges plus seven forbidden edges is twelve of the
  sixteen ordered pairs four values admit. The four identity pairs are in
  neither table, and reading "unenumerated therefore forbidden" would forbid an
  engine's own idempotent recomputation.
- @na3tebqk — §7.3 calls the finding type "a state machine" and, twelve lines
  later, calls a finding "a function of exactly three inputs". Retained state is
  "local state", which the same paragraph forbids as an input, so the tables are
  a validity relation over pairs of *recomputations*, never a machine we advance.
"""

import itertools

import pytest

from thesmo.core.errors import MalformedInput, WallViolation
from thesmo.core.finding import (
    Affirmed,
    DefeaterClass,
    Defeated,
    Pending,
    PendingSpecies,
    RequirementElement,
    SelfConvicted,
    Verdict,
)
from thesmo.core.transitions import (
    FORBIDDEN_EDGES,
    IDENTITY_EDGES,
    PERMITTED_EDGES,
    Terminality,
    TransitionClass,
    check,
    classify,
    condition_for,
    permitted_successors,
    reason_forbidden,
    terminality,
)
from thesmo.core.triple import (
    AppraisalTriple,
    Coordinate,
    EvidenceBundle,
    EvidenceItem,
    LawHead,
    Position,
)

LAW = LawHead("ELaw000")
WHERE = Position("EGar000", 4)


def item(said, anchor=0, seal=0):
    return EvidenceItem(said, Coordinate(anchor, seal))


def triple(*items):
    return AppraisalTriple(
        bundle=EvidenceBundle.of(*items) if items else EvidenceBundle.of(item("EEvi000")),
        law_head=LAW,
        position=WHERE,
    )


SMALL = triple(item("EEvi000"))
GROWN = triple(item("EEvi000"), item("EEvi001", 1))


def finding(verdict, question="q", at=SMALL):
    """One finding of each value over the same question, for edge testing."""
    if verdict is Verdict.AFFIRMED:
        return Affirmed(question=question, triple=at, clause_set=("EC1",))
    if verdict is Verdict.DEFEATED:
        return Defeated(
            question=question, triple=at, defeater_class=DefeaterClass.MERIT, citation="EC1"
        )
    if verdict is Verdict.PENDING:
        return Pending(
            question=question,
            triple=at,
            requirements=(
                RequirementElement("EArt", "schema", ("EC1",), PendingSpecies.ABSENT),
            ),
        )
    return SelfConvicted(question=question, triple=at, proof_package="EProof0")


class TestTheEnumerationIsComplete:
    def test_five_permitted_edges(self):
        assert set(PERMITTED_EDGES) == {
            (Verdict.PENDING, Verdict.AFFIRMED),
            (Verdict.PENDING, Verdict.DEFEATED),
            (Verdict.PENDING, Verdict.SELF_CONVICTED),
            (Verdict.AFFIRMED, Verdict.SELF_CONVICTED),
            (Verdict.DEFEATED, Verdict.SELF_CONVICTED),
        }

    def test_seven_forbidden_edges(self):
        assert set(FORBIDDEN_EDGES) == {
            (Verdict.AFFIRMED, Verdict.DEFEATED),
            (Verdict.DEFEATED, Verdict.AFFIRMED),
            (Verdict.AFFIRMED, Verdict.PENDING),
            (Verdict.DEFEATED, Verdict.PENDING),
            (Verdict.SELF_CONVICTED, Verdict.PENDING),
            (Verdict.SELF_CONVICTED, Verdict.AFFIRMED),
            (Verdict.SELF_CONVICTED, Verdict.DEFEATED),
        }

    def test_the_document_enumerates_twelve_of_sixteen_pairs(self):
        # this.i @fxn65z. The claim of completeness is false as written: the
        # four identity pairs appear in neither table, and this repo rules them
        # rather than pretending the document did.
        assert len(PERMITTED_EDGES) + len(FORBIDDEN_EDGES) == 12
        assert len(IDENTITY_EDGES) == 4
        assert len(list(itertools.product(Verdict, Verdict))) == 16

    def test_every_pair_classifies_and_the_three_classes_are_disjoint(self):
        classified = {
            pair: classify(*pair) for pair in itertools.product(Verdict, Verdict)
        }
        assert len(classified) == 16
        assert set(PERMITTED_EDGES) & set(FORBIDDEN_EDGES) == set()
        assert set(PERMITTED_EDGES) & IDENTITY_EDGES == set()
        assert set(FORBIDDEN_EDGES) & IDENTITY_EDGES == set()

    def test_every_permitted_edge_states_its_condition(self):
        # §7.3: "Five edges, each conditioned on evidence growth."
        assert all(condition for condition in PERMITTED_EDGES.values())

    def test_every_forbidden_edge_states_why(self):
        assert all(reason for reason in FORBIDDEN_EDGES.values())

    def test_no_backward_edge_makes_the_permitted_graph_acyclic(self):
        # §7.3's graph derivation: "no backward edge exists, so no cycle is
        # constructible, and every path terminates."
        reachable = {v: {b for a, b in PERMITTED_EDGES if a is v} for v in Verdict}
        for start in Verdict:
            seen, frontier = set(), list(reachable[start])
            while frontier:
                node = frontier.pop()
                assert node is not start, "a permitted path returns to its start"
                if node not in seen:
                    seen.add(node)
                    frontier.extend(reachable[node])


class TestClassification:
    def test_identity_is_permitted_and_named_as_its_own_class(self):
        # this.i @fxn65z: an unchanged recomputation has not transitioned.
        for verdict in Verdict:
            assert classify(verdict, verdict) is TransitionClass.IDENTITY

    def test_a_listed_permitted_edge_classifies_as_permitted(self):
        assert (
            classify(Verdict.PENDING, Verdict.AFFIRMED) is TransitionClass.PERMITTED
        )

    def test_a_listed_forbidden_edge_classifies_as_forbidden(self):
        assert (
            classify(Verdict.AFFIRMED, Verdict.DEFEATED) is TransitionClass.FORBIDDEN
        )

    def test_condition_for_reads_back_the_specification_s_condition(self):
        assert "discharges affirmatively" in condition_for(
            Verdict.PENDING, Verdict.AFFIRMED
        )

    def test_condition_for_refuses_an_edge_that_is_not_permitted(self):
        with pytest.raises(MalformedInput):
            condition_for(Verdict.AFFIRMED, Verdict.DEFEATED)

    def test_reason_forbidden_reads_back_the_specification_s_reason(self):
        assert "settled findings do not flip" in reason_forbidden(
            Verdict.AFFIRMED, Verdict.DEFEATED
        )

    def test_reason_forbidden_refuses_an_edge_that_is_not_forbidden(self):
        with pytest.raises(MalformedInput):
            reason_forbidden(Verdict.PENDING, Verdict.AFFIRMED)

    def test_permitted_successors_of_each_value(self):
        assert permitted_successors(Verdict.PENDING) == (
            Verdict.AFFIRMED,
            Verdict.DEFEATED,
            Verdict.SELF_CONVICTED,
        )
        assert permitted_successors(Verdict.SELF_CONVICTED) == ()


class TestTerminality:
    """§7.3: "Affirmed and defeated are final except for one event [...] Pending
    is the non-terminal bottom. Self-convicted is terminal for its question"."""

    def test_pending_is_the_non_terminal_bottom(self):
        assert terminality(Verdict.PENDING) is Terminality.NON_TERMINAL

    @pytest.mark.parametrize("verdict", [Verdict.AFFIRMED, Verdict.DEFEATED])
    def test_affirmed_and_defeated_are_final_except_for_self_conviction(self, verdict):
        assert terminality(verdict) is Terminality.FINAL_EXCEPT_SELF_CONVICTION
        assert permitted_successors(verdict) == (Verdict.SELF_CONVICTED,)

    def test_self_convicted_is_terminal(self):
        assert terminality(Verdict.SELF_CONVICTED) is Terminality.TERMINAL
        assert permitted_successors(Verdict.SELF_CONVICTED) == ()


class TestCheckingARecomputation:
    """this.i @na3tebqk — check() is a relation over two computed findings, not
    a guard inside a mutable machine."""

    def test_an_unchanged_recomputation_over_a_grown_bundle_is_identity(self):
        before = finding(Verdict.PENDING, at=SMALL)
        after = finding(Verdict.PENDING, at=GROWN)
        assert check(before, after) is TransitionClass.IDENTITY

    def test_a_permitted_edge_over_a_grown_bundle_passes(self):
        before = finding(Verdict.PENDING, at=SMALL)
        after = finding(Verdict.AFFIRMED, at=GROWN)
        assert check(before, after) is TransitionClass.PERMITTED

    def test_a_forbidden_edge_raises_a_wall_violation_carrying_the_reason(self):
        before = finding(Verdict.AFFIRMED, at=SMALL)
        after = finding(Verdict.DEFEATED, at=GROWN)
        with pytest.raises(WallViolation) as caught:
            check(before, after)
        assert caught.value.code == "CORE-WALL-VIOLATION"
        assert caught.value.retryable is False
        assert "settled findings do not flip" in str(caught.value)

    def test_nothing_is_coerced_or_mutated_by_a_failed_check(self):
        before = finding(Verdict.AFFIRMED, at=SMALL)
        with pytest.raises(WallViolation):
            check(before, finding(Verdict.PENDING, at=GROWN))
        assert before.verdict is Verdict.AFFIRMED

    def test_refuses_a_pair_of_findings_about_different_questions(self):
        before = finding(Verdict.PENDING, question="q1", at=SMALL)
        after = finding(Verdict.AFFIRMED, question="q2", at=GROWN)
        with pytest.raises(MalformedInput):
            check(before, after)

    def test_refuses_a_shrinking_bundle(self):
        # "findings move only in the direction of evidence growth."
        with pytest.raises(MalformedInput):
            check(finding(Verdict.PENDING, at=GROWN), finding(Verdict.AFFIRMED, at=SMALL))

    def test_refuses_a_pair_across_a_different_law_head(self):
        # §7.3's monotonicity is stated "at a fixed law head and position".
        elsewhere = AppraisalTriple(
            bundle=GROWN.bundle, law_head=LawHead("ELaw999"), position=WHERE
        )
        with pytest.raises(MalformedInput):
            check(finding(Verdict.PENDING, at=SMALL), finding(Verdict.AFFIRMED, at=elsewhere))

    def test_refuses_a_pair_across_a_different_position(self):
        later = AppraisalTriple(
            bundle=GROWN.bundle, law_head=LAW, position=Position("EGar000", 5)
        )
        with pytest.raises(MalformedInput):
            check(finding(Verdict.PENDING, at=SMALL), finding(Verdict.AFFIRMED, at=later))

    def test_refuses_anything_that_is_not_a_finding(self):
        with pytest.raises(MalformedInput):
            check(finding(Verdict.PENDING), "affirmed")

    def test_every_permitted_edge_passes_check_on_real_findings(self):
        for before_verdict, after_verdict in PERMITTED_EDGES:
            assert (
                check(
                    finding(before_verdict, at=SMALL), finding(after_verdict, at=GROWN)
                )
                is TransitionClass.PERMITTED
            )

    def test_every_forbidden_edge_fails_check_on_real_findings(self):
        for before_verdict, after_verdict in FORBIDDEN_EDGES:
            with pytest.raises(WallViolation):
                check(finding(before_verdict, at=SMALL), finding(after_verdict, at=GROWN))
