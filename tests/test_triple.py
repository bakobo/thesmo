"""The closed three-input type (Custos 4.1 §1.4 axiom 2, §7.3 "Inputs").

Axiom 2 fixes the fold's inputs at exactly three and forbids any other input
from influencing the result. These tests hold that closure mechanically: the
arity is asserted from the dataclass itself, so a fourth input cannot be added
without a test failing and a this.i node justifying it.
"""

import dataclasses

import pytest

from thesmo.core.errors import MalformedInput, UncommittedOrder
from thesmo.core.triple import (
    AppraisalTriple,
    EvidenceBundle,
    EvidenceItem,
    LawHead,
    Position,
    canonical_evidence_order,
    encode_fields,
)


# --- the canonical encoding (this.i @ox6mfpi: our choice, not the document's) ---


def test_encode_fields_is_length_prefixed_and_unambiguous():
    """Concatenation must not be able to forge a different field split."""
    assert encode_fields("ab", "c") == b"2:ab1:c"
    assert encode_fields("abc") != encode_fields("ab", "c")


def test_encode_fields_accepts_bytes_str_and_int():
    assert encode_fields(b"xy") == b"2:xy"
    assert encode_fields("xy") == b"2:xy"
    assert encode_fields(7) == b"1:7"


def test_encode_fields_refuses_a_type_it_cannot_canonicalize():
    with pytest.raises(MalformedInput) as excinfo:
        encode_fields(3.5)
    assert excinfo.value.code == "THESMO_MALFORMED_INPUT"
    assert excinfo.value.permanent is True


# --- Position ---


def test_position_is_identifier_and_sequence_number():
    p = Position("Egel", 4)
    assert (p.identifier, p.sn) == ("Egel", 4)


@pytest.mark.parametrize(
    ("identifier", "sn"),
    [("", 0), ("Egel", -1)],
)
def test_position_rejects_malformed_coordinates(identifier, sn):
    with pytest.raises(MalformedInput):
        Position(identifier, sn)


def test_position_orders_within_one_identifier():
    assert Position("Egel", 1).precedes(Position("Egel", 2)) is True
    assert Position("Egel", 2).precedes(Position("Egel", 1)) is False


def test_position_refuses_to_order_across_identifiers():
    """this.i @4qrss4h: a cross-log order is a seam the document never commits."""
    with pytest.raises(UncommittedOrder) as excinfo:
        Position("Egel", 1).precedes(Position("Ekel", 2))
    assert excinfo.value.code == "THESMO_UNCOMMITTED_ORDER"


def test_position_canonical_bytes_distinguish_coordinates():
    assert Position("Egel", 1).canonical_bytes() != Position("Egel", 2).canonical_bytes()


# --- LawHead ---


def test_law_head_carries_a_self_addressing_identifier():
    assert LawHead("Elaw").said == "Elaw"
    assert LawHead("Elaw").canonical_bytes() == encode_fields("Elaw")


def test_law_head_rejects_an_empty_identifier():
    with pytest.raises(MalformedInput):
        LawHead("")


# --- EvidenceItem ---


def test_evidence_item_may_be_unanchored():
    item = EvidenceItem("Ekelspan")
    assert item.anchor is None
    assert item.seal_index is None


def test_evidence_item_may_carry_its_anchor_and_seal_index():
    item = EvidenceItem("Egev", anchor=Position("Ekel", 3), seal_index=1)
    assert item.anchor == Position("Ekel", 3)
    assert item.seal_index == 1


def test_evidence_item_rejects_an_empty_identifier():
    with pytest.raises(MalformedInput):
        EvidenceItem("")


@pytest.mark.parametrize(
    ("anchor", "seal_index"),
    [(Position("Ekel", 3), None), (None, 0)],
)
def test_evidence_item_rejects_half_an_anchor(anchor, seal_index):
    """§17's intra-anchor order needs both halves or neither."""
    with pytest.raises(MalformedInput):
        EvidenceItem("Egev", anchor=anchor, seal_index=seal_index)


def test_evidence_item_rejects_a_negative_seal_index():
    with pytest.raises(MalformedInput):
        EvidenceItem("Egev", anchor=Position("Ekel", 3), seal_index=-1)


# --- EvidenceBundle and the §17 canonical order ---


def test_bundle_membership_and_size():
    a = EvidenceItem("Ea")
    bundle = EvidenceBundle.of(a, EvidenceItem("Eb"))
    assert a in bundle
    assert EvidenceItem("Ec") not in bundle
    assert len(bundle) == 2


def test_bundle_is_a_set_so_a_repeated_item_is_one_member():
    """this.i @sgc5lpwd: membership is by committed identity, not presentation."""
    a = EvidenceItem("Ea")
    assert len(EvidenceBundle.of(a, a)) == 1


def test_bundle_identity_ignores_presentation_order():
    a, b = EvidenceItem("Ea"), EvidenceItem("Eb")
    assert EvidenceBundle.of(a, b) == EvidenceBundle.of(b, a)


def test_canonical_order_puts_anchored_evidence_first_in_anchor_order():
    """§17: KEL anchoring order first, then the anchoring event's seal list."""
    late = EvidenceItem("Ez", anchor=Position("Ekel", 9), seal_index=0)
    early_second_seal = EvidenceItem("Ey", anchor=Position("Ekel", 2), seal_index=1)
    early_first_seal = EvidenceItem("Ex", anchor=Position("Ekel", 2), seal_index=0)
    unanchored = EvidenceItem("Eaa")
    bundle = EvidenceBundle.of(late, unanchored, early_second_seal, early_first_seal)
    assert canonical_evidence_order(bundle) == (
        early_first_seal,
        early_second_seal,
        late,
        unanchored,
    )


def test_canonical_order_breaks_unanchored_ties_by_identifier_bytes():
    """this.i @stzggn: still derived from committed bytes, so axiom 4 holds."""
    b, a = EvidenceItem("Eb"), EvidenceItem("Ea")
    assert canonical_evidence_order(EvidenceBundle.of(b, a)) == (a, b)


def test_permuted_arrival_folds_to_identical_bytes():
    """§17's order vectors, at the grain core/ can exercise them."""
    items = [
        EvidenceItem("Em", anchor=Position("Ekel", 1), seal_index=0),
        EvidenceItem("En", anchor=Position("Ekel", 1), seal_index=1),
        EvidenceItem("Eo"),
    ]
    forward = EvidenceBundle.of(*items)
    reversed_ = EvidenceBundle.of(*reversed(items))
    assert forward.canonical_bytes() == reversed_.canonical_bytes()


def test_bundle_canonical_bytes_distinguish_different_evidence():
    assert (
        EvidenceBundle.of(EvidenceItem("Ea")).canonical_bytes()
        != EvidenceBundle.of(EvidenceItem("Eb")).canonical_bytes()
    )


# --- AppraisalTriple ---


def test_the_triple_has_exactly_three_inputs():
    """Axiom 2's closure, asserted against the type rather than a comment."""
    names = [f.name for f in dataclasses.fields(AppraisalTriple)]
    assert names == ["bundle", "law_head", "position"]


def test_triple_canonical_bytes_change_with_each_input():
    bundle = EvidenceBundle.of(EvidenceItem("Ea"))
    base = AppraisalTriple(bundle, LawHead("Elaw"), Position("Egel", 1))
    assert base.canonical_bytes() != AppraisalTriple(
        EvidenceBundle.of(EvidenceItem("Eb")), LawHead("Elaw"), Position("Egel", 1)
    ).canonical_bytes()
    assert base.canonical_bytes() != AppraisalTriple(
        bundle, LawHead("Eother"), Position("Egel", 1)
    ).canonical_bytes()
    assert base.canonical_bytes() != AppraisalTriple(
        bundle, LawHead("Elaw"), Position("Egel", 2)
    ).canonical_bytes()


def test_equal_triples_are_equal_and_hashable():
    """Replay: the same committed inputs are the same input."""
    one = AppraisalTriple(
        EvidenceBundle.of(EvidenceItem("Ea")), LawHead("Elaw"), Position("Egel", 1)
    )
    two = AppraisalTriple(
        EvidenceBundle.of(EvidenceItem("Ea")), LawHead("Elaw"), Position("Egel", 1)
    )
    assert one == two
    assert len({one, two}) == 1
