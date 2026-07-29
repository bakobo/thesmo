"""The closed three-input type (Custos §1.4 axiom 2, §7.3 "Inputs").

The axiom is a wall, not a convenience: "the inputs are exactly three, closed:
the committed evidence bundle, the committed law head, and the appraisal
position. No other input may influence the result." These tests hold the type to
that arity and to the two properties the fold needs from a bundle — a subset
order (§7.3 "The evidence ordering") and a committed order derivable from the
bundle's own bytes (§17 "Canonical order", §1.4 axiom 4).
"""

import dataclasses

import pytest

from thesmo.core.errors import MalformedInput
from thesmo.core.triple import (
    AppraisalTriple,
    Coordinate,
    EvidenceBundle,
    EvidenceItem,
    LawHead,
    Position,
)


def item(said, anchor=0, seal=0):
    return EvidenceItem(identifier=said, coordinate=Coordinate(anchor, seal))


def triple(bundle=None, said="ELaw000", ident="EGar000", sn=0):
    return AppraisalTriple(
        bundle=bundle if bundle is not None else EvidenceBundle.of(item("EEvi000")),
        law_head=LawHead(said),
        position=Position(ident, sn),
    )


class TestCoordinate:
    def test_orders_by_anchor_then_seal(self):
        assert Coordinate(0, 9) < Coordinate(1, 0)
        assert Coordinate(1, 0) < Coordinate(1, 1)

    def test_is_a_value(self):
        assert Coordinate(2, 3) == Coordinate(2, 3)
        assert hash(Coordinate(2, 3)) == hash(Coordinate(2, 3))

    @pytest.mark.parametrize("anchor,seal", [(-1, 0), (0, -1)])
    def test_rejects_negative_components(self, anchor, seal):
        with pytest.raises(MalformedInput) as caught:
            Coordinate(anchor, seal)
        assert caught.value.code == "CORE-MALFORMED-INPUT"
        assert caught.value.retryable is False

    def test_rejects_non_integer_components(self):
        with pytest.raises(MalformedInput):
            Coordinate(0.5, 0)


class TestEvidenceItem:
    def test_rejects_empty_identifier(self):
        with pytest.raises(MalformedInput):
            item("")

    def test_order_key_is_coordinate_then_identifier_bytes(self):
        # §17 forbids only a tiebreak that consults something UNCOMMITTED; the
        # identifier's own bytes are committed. this.i @vwqohe.
        assert item("EB", 1, 1).order_key() > item("EA", 1, 1).order_key()
        assert item("EA", 1, 2).order_key() > item("EB", 1, 1).order_key()


class TestEvidenceBundle:
    def test_of_accepts_any_iterable_and_deduplicates(self):
        one = item("EA")
        assert EvidenceBundle.of(one, one) == EvidenceBundle.of([one])
        assert len(EvidenceBundle.of(one, one)) == 1

    def test_empty_bundle_is_lawful(self):
        # A bundle that has committed nothing is the bottom of the subset order,
        # not an error: every question over it is pending.
        assert len(EvidenceBundle.of()) == 0
        assert tuple(EvidenceBundle.of()) == ()

    def test_iterates_in_committed_order_regardless_of_construction_order(self):
        first, second, third = item("EC", 0, 0), item("EA", 0, 1), item("EB", 1, 0)
        forward = EvidenceBundle.of(first, second, third)
        reversed_ = EvidenceBundle.of(third, second, first)
        assert forward.committed_order() == (first, second, third)
        assert tuple(reversed_) == tuple(forward)
        assert forward == reversed_

    def test_ties_at_one_coordinate_break_on_identifier_bytes(self):
        low, high = item("EA", 3, 3), item("EB", 3, 3)
        assert EvidenceBundle.of(high, low).committed_order() == (low, high)

    def test_membership_and_subset_order(self):
        small = EvidenceBundle.of(item("EA"))
        large = EvidenceBundle.of(item("EA"), item("EB", 1))
        assert item("EA") in small
        assert small.issubset(large) and small <= large
        assert not large.issubset(small)
        assert small < large
        assert not (small < small)

    def test_growth_produces_a_superset_and_leaves_the_original_alone(self):
        small = EvidenceBundle.of(item("EA"))
        large = small.grown_by(item("EB", 1))
        assert small < large
        assert len(small) == 1

    def test_rejects_a_non_item_member(self):
        with pytest.raises(MalformedInput):
            EvidenceBundle.of("EA")


class TestPositionAndLawHead:
    def test_position_is_identifier_and_sequence_number(self):
        assert Position("EGar", 7).sequence_number == 7

    @pytest.mark.parametrize("ident,sn", [("", 0), ("EGar", -1)])
    def test_position_rejects_malformed_coordinates(self, ident, sn):
        with pytest.raises(MalformedInput):
            Position(ident, sn)

    def test_position_rejects_a_non_integer_sequence_number(self):
        # "this document never measures position in wall-clock time" (§4).
        with pytest.raises(MalformedInput):
            Position("EGar", 1750000000.0)

    def test_law_head_rejects_an_empty_said(self):
        with pytest.raises(MalformedInput):
            LawHead("")


class TestAppraisalTriple:
    def test_has_exactly_three_inputs(self):
        # The arity is the axiom. A fourth field here is a conformance failure,
        # not a feature.
        names = tuple(f.name for f in dataclasses.fields(AppraisalTriple))
        assert names == ("bundle", "law_head", "position")
        assert AppraisalTriple.INPUT_COUNT == 3

    def test_inputs_returns_the_three_in_order(self):
        subject = triple()
        assert subject.inputs() == (
            subject.bundle,
            subject.law_head,
            subject.position,
        )

    def test_is_a_value_so_two_evaluations_of_one_triple_are_one_triple(self):
        assert triple() == triple()
        assert hash(triple()) == hash(triple())

    @pytest.mark.parametrize(
        "field,value",
        [
            ("bundle", "not a bundle"),
            ("law_head", "ELaw000"),
            ("position", ("EGar000", 0)),
        ],
    )
    def test_rejects_an_input_of_the_wrong_type(self, field, value):
        # Fail closed: an input that cannot be checked carries no authority.
        inputs = {
            "bundle": EvidenceBundle.of(item("EA")),
            "law_head": LawHead("ELaw000"),
            "position": Position("EGar000", 0),
        }
        inputs[field] = value
        with pytest.raises(MalformedInput):
            AppraisalTriple(**inputs)

    def test_grows_to_requires_a_superset_at_one_law_head_and_position(self):
        small = triple(EvidenceBundle.of(item("EA")))
        large = triple(EvidenceBundle.of(item("EA"), item("EB", 1)))
        assert small.grows_to(large)
        assert not large.grows_to(small)
        assert small.grows_to(small)  # identity is growth by nothing

    def test_grows_to_is_false_across_a_different_law_head_or_position(self):
        small = triple(EvidenceBundle.of(item("EA")))
        assert not small.grows_to(triple(EvidenceBundle.of(item("EA")), said="ELaw999"))
        assert not small.grows_to(triple(EvidenceBundle.of(item("EA")), sn=1))
