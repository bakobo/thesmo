"""The evidence ordering and the canonical selection of defeats (Custos §7.3).

This is the part of §7.3 that had to be read slowly, and the suite reflects it:
four of the pinned readings that make two conforming engines diverge live here.

- @kjqxel — the empty subcode "orders last" although the same sentence says
  "lexicographic minimum", under which the empty string is the minimum.
- @xr3rp7 — the affirmation discipline says "never affirmed" and does not say
  "never defeated", so defeat short-circuits and a defeated finding's citation
  is *not* monotone under bundle growth. The test that shows that is the defect
  report.
- @kdrqzc — deduplication is on the sort key, so colliding species must merge.
- @r5p4h2 — "first-seen survives" means first in committed order.
"""

import pytest

from thesmo.core.errors import MalformedInput
from thesmo.core.finding import (
    Affirmed,
    DefeaterClass,
    Defeated,
    PendingSpecies,
    RequirementElement,
    Verdict,
)
from thesmo.core.ordering import (
    Defeat,
    canonical_requirement_set,
    defeat_sort_key,
    first_seen,
    permitted_verdict,
    refines,
    select_defeat,
    undischarged,
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


def bundle(*items):
    return EvidenceBundle.of(*items)


def triple(*items):
    return AppraisalTriple(
        bundle=bundle(*items) if items else bundle(item("EEvi000")),
        law_head=LawHead("ELaw000"),
        position=Position("EGar000", 4),
    )


def element(subject="EArt000", kind="schema", clauses=("EC1",), species=PendingSpecies.ABSENT):
    return RequirementElement(subject, kind, clauses, species)


class TestTheSubsetOrderOnBundles:
    """§7.3: "monotonicity is over the subset order on bundles at a fixed law
    head and position, never over wall time"."""

    def test_a_bundle_refines_its_supersets(self):
        small, large = bundle(item("EA")), bundle(item("EA"), item("EB", 1))
        assert refines(small, large)
        assert not refines(large, small)

    def test_a_bundle_refines_itself(self):
        assert refines(bundle(item("EA")), bundle(item("EA")))

    def test_disjoint_bundles_refine_neither_way(self):
        assert not refines(bundle(item("EA")), bundle(item("EB", 1)))
        assert not refines(bundle(item("EB", 1)), bundle(item("EA")))


class TestFirstSeenIsFirstInCommittedOrder:
    """this.i @r5p4h2 — §7.4 says "first-seen survives"; §12.1 says discovery
    order is "observer-relative and consulted by nothing"."""

    def test_returns_the_item_earliest_in_committed_order(self):
        early, late = item("EA", 1, 0), item("EB", 2, 0)
        assert first_seen(bundle(late, early)) is early

    def test_is_indifferent_to_the_order_the_items_were_presented_in(self):
        # §17's order vectors: permuted arrival, identical Constitutions.
        early, late = item("EA", 1, 0), item("EB", 2, 0)
        assert first_seen([late, early]) == first_seen([early, late])

    def test_breaks_a_tie_at_one_coordinate_on_committed_bytes(self):
        low, high = item("EA", 3, 3), item("EB", 3, 3)
        assert first_seen([high, low]) is low

    def test_refuses_an_empty_collection(self):
        with pytest.raises(MalformedInput):
            first_seen([])


class TestCanonicalRequirementSet:
    def test_orders_by_subject_then_kind_then_citing_clause_bytes(self):
        a = element(subject="EA", kind="z")
        b = element(subject="EB", kind="a")
        c = element(subject="EA", kind="a")
        assert canonical_requirement_set([a, b, c]) == (c, a, b)

    def test_is_indifferent_to_presentation_order(self):
        a, b = element(subject="EA"), element(subject="EB")
        assert canonical_requirement_set([a, b]) == canonical_requirement_set([b, a])

    def test_deduplicates_identical_elements(self):
        assert canonical_requirement_set([element(), element()]) == (element(),)

    def test_merges_a_species_collision_to_the_earliest_declared_species(self):
        # this.i @kdrqzc. §7.3 deduplicates on (subject, kind, citing clauses)
        # and says nothing about the species of the survivor; taking §7.2's
        # declaration minimum is the invented half of this pin.
        merged = canonical_requirement_set(
            [
                element(species=PendingSpecies.EXPIRED_ABANDONED),
                element(species=PendingSpecies.WINDOW_OPEN),
            ]
        )
        assert merged == (element(species=PendingSpecies.WINDOW_OPEN),)

    def test_merge_is_independent_of_presentation_order(self):
        loud, quiet = (
            element(species=PendingSpecies.UNRESOLVED_CONFLICT),
            element(species=PendingSpecies.ABSENT),
        )
        assert canonical_requirement_set([loud, quiet]) == canonical_requirement_set(
            [quiet, loud]
        )

    def test_the_result_is_accepted_by_a_pending_finding(self):
        from thesmo.core.finding import Pending

        elements = canonical_requirement_set([element(subject="EB"), element(subject="EA")])
        assert Pending(question="q", triple=triple(), requirements=elements).requirements

    def test_refuses_an_empty_input(self):
        with pytest.raises(MalformedInput):
            canonical_requirement_set([])

    def test_refuses_a_member_that_is_not_a_requirement_element(self):
        with pytest.raises(MalformedInput):
            canonical_requirement_set(["EArt000"])


class TestDefeat:
    def test_carries_class_citation_and_subcode(self):
        subject = Defeat(DefeaterClass.MERIT, "EC1", "sub")
        assert (subject.defeater_class, subject.citation, subject.subcode) == (
            DefeaterClass.MERIT,
            "EC1",
            "sub",
        )

    def test_round_trips_through_a_defeated_finding(self):
        subject = Defeat(DefeaterClass.CRYPTO, "ESub", "sig")
        finding = subject.as_finding(question="q", triple=triple())
        assert isinstance(finding, Defeated)
        assert Defeat.of(finding) == subject

    def test_refuses_a_citation_that_names_nothing(self):
        with pytest.raises(MalformedInput):
            Defeat(DefeaterClass.MERIT, "")

    def test_refuses_a_class_that_is_not_one_of_the_four(self):
        with pytest.raises(MalformedInput):
            Defeat("merit", "EC1")


class TestCanonicalSelection:
    """§7.3: "the finding SHALL cite the lexicographic minimum of
    (defeater-class rank, citation identifier, subcode)"."""

    def test_selects_the_lowest_ranked_class_first(self):
        crypto = Defeat(DefeaterClass.CRYPTO, "ZZZ")
        merit = Defeat(DefeaterClass.MERIT, "AAA")
        assert select_defeat([merit, crypto]) is crypto

    def test_ranks_by_the_stated_order_not_by_class_name(self):
        # this.i @zmwnx35s — alphabetically "authority" precedes "crypto".
        crypto = Defeat(DefeaterClass.CRYPTO, "EC1")
        authority = Defeat(DefeaterClass.AUTHORITY, "EC1")
        assert select_defeat([authority, crypto]) is crypto

    def test_breaks_a_class_tie_on_the_citation_identifier(self):
        first = Defeat(DefeaterClass.MERIT, "EC1")
        second = Defeat(DefeaterClass.MERIT, "EC2")
        assert select_defeat([second, first]) is first

    def test_an_empty_subcode_orders_last_not_first(self):
        # this.i @kjqxel, the sharpest divergence in the register. Under a plain
        # lexicographic minimum the empty subcode wins, because the empty string
        # prefixes every string. §7.3's final clause says it "orders last", and
        # the specific governs the general.
        bare = Defeat(DefeaterClass.MERIT, "EClause0000")
        discriminated = Defeat(DefeaterClass.MERIT, "EClause0000", "a")
        assert select_defeat([bare, discriminated]) is discriminated

    def test_non_empty_subcodes_compare_lexicographically(self):
        a = Defeat(DefeaterClass.MERIT, "EC1", "a")
        b = Defeat(DefeaterClass.MERIT, "EC1", "b")
        assert select_defeat([b, a]) is a

    def test_selection_is_indifferent_to_presentation_order(self):
        defeats = [
            Defeat(DefeaterClass.SUPERSEDED, "EC9"),
            Defeat(DefeaterClass.AUTHORITY, "EC1", "z"),
            Defeat(DefeaterClass.AUTHORITY, "EC1"),
        ]
        assert select_defeat(defeats) == select_defeat(list(reversed(defeats)))

    def test_two_verifiers_holding_one_bundle_select_one_defeat(self):
        # §7.3: "Two verifiers holding the same bundle SHALL emit the same
        # defeated finding down to the byte."
        defeats = [Defeat(DefeaterClass.MERIT, "EC2"), Defeat(DefeaterClass.MERIT, "EC1")]
        assert select_defeat(defeats).as_finding("q", triple()) == select_defeat(
            list(reversed(defeats))
        ).as_finding("q", triple())

    def test_a_single_defeat_selects_itself(self):
        only = Defeat(DefeaterClass.SUPERSEDED, "EAct")
        assert select_defeat([only]) is only

    def test_refuses_to_select_from_nothing(self):
        # There is no canonical minimum of an empty set, and inventing one
        # would be legislating a defeat nobody cited.
        with pytest.raises(MalformedInput):
            select_defeat([])

    def test_the_sort_key_is_exposed_for_the_conformance_harness(self):
        assert defeat_sort_key(Defeat(DefeaterClass.CRYPTO, "EC1", "a")) < defeat_sort_key(
            Defeat(DefeaterClass.CRYPTO, "EC1")
        )


class TestTheAffirmationDiscipline:
    """§7.3: "affirmed is reachable only over a bundle that discharges the
    question's entire committed requirement space"."""

    def test_undischarged_returns_the_unexamined_checks_in_order(self):
        assert undischarged(["c2", "c1", "c3"], ["c1"]) == ("c2", "c3")

    def test_undischarged_is_empty_when_the_space_is_covered(self):
        assert undischarged(["c1"], ["c1", "c2"]) == ()

    def test_affirmed_needs_the_whole_space_discharged(self):
        assert permitted_verdict([], []) is Verdict.AFFIRMED
        assert permitted_verdict([], ["c1"]) is Verdict.PENDING

    def test_defeat_short_circuits_an_undischarged_space(self):
        # this.i @xr3rp7. §7.3 says "never affirmed", not "never defeated". The
        # rejected reading returns PENDING here.
        merit = Defeat(DefeaterClass.MERIT, "EC1")
        assert permitted_verdict([merit], ["crypto-check"]) is Verdict.DEFEATED

    def test_the_pinned_reading_makes_a_defeated_citation_non_monotone(self):
        # The defect report, executable. §7.3 promises that "appraisal under the
        # larger bundle refines and never contradicts appraisal under the
        # smaller" — and under the reading its own affirmation sentence forces,
        # the citation changes as the bundle grows. The forbidden-transition
        # table does not cover defeated -> defeated with a different citation,
        # so no wall catches it either.
        small_bundle_defeats = [Defeat(DefeaterClass.MERIT, "EClauseM")]
        grown_bundle_defeats = [*small_bundle_defeats, Defeat(DefeaterClass.CRYPTO, "ESubj")]

        before = select_defeat(small_bundle_defeats)
        after = select_defeat(grown_bundle_defeats)

        assert permitted_verdict(small_bundle_defeats, ["crypto-check"]) is Verdict.DEFEATED
        assert permitted_verdict(grown_bundle_defeats, []) is Verdict.DEFEATED
        assert before.citation != after.citation

    def test_self_conviction_is_not_reachable_from_the_evidence_ordering_alone(self):
        # It needs a bearing contradictory pair, which is currents.py's subject.
        assert permitted_verdict([], []) is not Verdict.SELF_CONVICTED

    def test_the_discipline_composes_with_a_real_finding(self):
        # Affirmed is only lawful where nothing is left unexamined.
        assert permitted_verdict([], []) is Affirmed.VERDICT
