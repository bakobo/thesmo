"""The four-valued finding codomain (Custos 4.1 §7.1) and its required payloads (§7.3).

The load-bearing property under test is the Ground Axiom read as a typing rule:
a value that does not carry its ground is not a member of the type. So every
"rejects" test below is a test that a groundless finding is *unconstructible*,
not merely discouraged.
"""

import pytest

from thesmo.core.errors import GroundMissing, MalformedInput, RefusedInvocation
from thesmo.core.finding import (
    Affirmed,
    Citation,
    CitationKind,
    Defeat,
    DefeaterClass,
    Defeated,
    Finding,
    Pending,
    PendingSpecies,
    Product,
    Refusal,
    RequirementElement,
    SelfConvicted,
    Verdict,
)
from thesmo.core.triple import EvidenceBundle, EvidenceItem, LawHead, Position

LAW = LawHead("Elaw")
POS = Position("Egel", 4)
BUNDLE = EvidenceBundle.of(EvidenceItem("Ea"))


def clause_requirement(**overrides):
    kwargs = {
        "subject": "Esubject",
        "kind": "issuance",
        "citing_clauses": ("Eclause",),
        "species": PendingSpecies.ABSENT,
    }
    kwargs.update(overrides)
    return RequirementElement(**kwargs)


# --- the codomain has four values, and exactly four ---


def test_the_codomain_has_exactly_four_values():
    assert [v.value for v in Verdict] == [
        "affirmed",
        "defeated",
        "pending",
        "self-convicted",
    ]


def test_every_finding_carries_its_law_head_and_position():
    """§14: every finding retains its position and its committed law head."""
    finding = SelfConvicted(LAW, POS, proof="Eproof")
    assert finding.law_head is LAW
    assert finding.position is POS


# --- affirmed ---


def test_affirmed_carries_its_bundle_and_clause_set():
    """this.i @dkypfoo: §7.1 gives affirmed a ground even though §7.3 omits it."""
    finding = Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Eclause",))
    assert finding.verdict is Verdict.AFFIRMED
    assert finding.bundle is BUNDLE
    assert finding.clause_set == ("Eclause",)


def test_affirmed_without_a_clause_set_is_not_a_finding():
    with pytest.raises(GroundMissing) as excinfo:
        Affirmed(LAW, POS, bundle=BUNDLE, clause_set=())
    assert excinfo.value.code == "THESMO_GROUND_MISSING"


def test_affirmed_rejects_an_empty_clause_identifier():
    with pytest.raises(MalformedInput):
        Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("",))


def test_affirmed_canonicalizes_its_clause_set():
    """this.i @blq6dwxz: sorted by bytes and deduplicated, so bytes are stable."""
    finding = Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Eb", "Ea", "Eb"))
    assert finding.clause_set == ("Ea", "Eb")


# --- defeated ---


def test_defeated_carries_its_defeater_class_citation_and_subcode():
    defeat = Defeat(DefeaterClass.MERIT, Citation("Eclause"), subcode="s1")
    finding = Defeated(LAW, POS, defeat=defeat)
    assert finding.verdict is Verdict.DEFEATED
    assert finding.defeat.defeater_class is DefeaterClass.MERIT
    assert finding.defeat.citation.identifier == "Eclause"
    assert finding.defeat.subcode == "s1"


def test_defeater_classes_rank_in_the_ratified_order():
    """§7.3: crypto, authority, merit, superseded — carried unchanged from 3.3."""
    assert [c.name for c in sorted(DefeaterClass, key=lambda c: c.rank)] == [
        "CRYPTO",
        "AUTHORITY",
        "MERIT",
        "SUPERSEDED",
    ]


def test_the_selection_key_orders_an_empty_subcode_last():
    """this.i @5pu23u: "orders last" beats "lexicographic minimum" where they clash."""
    empty = Defeat(DefeaterClass.MERIT, Citation("Ec"))
    coded = Defeat(DefeaterClass.MERIT, Citation("Ec"), subcode="a")
    assert coded.selection_key < empty.selection_key


def test_the_selection_key_ranks_class_before_citation():
    crypto_late = Defeat(DefeaterClass.CRYPTO, Citation("Ez"))
    merit_early = Defeat(DefeaterClass.MERIT, Citation("Ea"))
    assert crypto_late.selection_key < merit_early.selection_key


def test_a_citation_needs_an_identifier():
    with pytest.raises(MalformedInput):
        Citation("")


def test_an_act_citation_must_carry_a_committed_receipt():
    """this.i @t66d4n: §15's fifth wall, read at the width it is stated."""
    with pytest.raises(GroundMissing) as excinfo:
        Citation("Eact", kind=CitationKind.ACT)
    assert excinfo.value.code == "THESMO_GROUND_MISSING"
    assert Citation("Eact", kind=CitationKind.ACT, receipt="Ercpt").receipt == "Ercpt"


def test_a_clause_citation_may_not_carry_a_receipt():
    with pytest.raises(MalformedInput):
        Citation("Eclause", receipt="Ercpt")


def test_the_default_citation_kind_is_a_clause():
    assert Citation("Eclause").kind is CitationKind.CLAUSE


# --- pending ---


def test_pending_carries_its_typed_requirement_set():
    finding = Pending(LAW, POS, requirements=(clause_requirement(),))
    assert finding.verdict is Verdict.PENDING
    assert finding.requirements[0].species is PendingSpecies.ABSENT


def test_pending_without_a_requirement_set_is_not_a_finding():
    with pytest.raises(GroundMissing):
        Pending(LAW, POS, requirements=())


def test_pending_deduplicates_and_orders_its_requirement_set():
    """§7.3: deduplicated elements, canonical order (subject, kind, clause bytes)."""
    first = clause_requirement(subject="Eb")
    second = clause_requirement(subject="Ea")
    finding = Pending(LAW, POS, requirements=(first, second, first))
    assert finding.requirements == (second, first)


def test_pending_orders_two_species_of_one_subject_deterministically():
    """this.i @blq6dwxz: species is a mandatory field the sort key omits."""
    absent = clause_requirement(species=PendingSpecies.ABSENT)
    window = clause_requirement(species=PendingSpecies.WINDOW_OPEN)
    assert Pending(LAW, POS, requirements=(window, absent)).requirements == (
        absent,
        window,
    )


def test_the_four_pending_species_are_the_ratified_four():
    assert [s.value for s in PendingSpecies] == [
        "absent",
        "window-open",
        "unresolved-conflict",
        "expired/abandoned",
    ]


# --- typed requirement elements ---


@pytest.mark.parametrize(
    "overrides",
    [
        {"subject": ""},
        {"kind": ""},
        {"citing_clauses": ()},
        {"citing_clauses": ("",)},
    ],
)
def test_requirement_elements_reject_a_missing_component(overrides):
    with pytest.raises((MalformedInput, GroundMissing)):
        clause_requirement(**overrides)


def test_requirement_elements_canonicalize_their_citing_clauses():
    """this.i @blq6dwxz: the citing list is sorted and deduplicated by bytes."""
    element = clause_requirement(citing_clauses=("Eb", "Ea", "Eb"))
    assert element.citing_clauses == ("Ea", "Eb")


def test_expired_abandoned_requires_a_committed_eviction_receipt():
    """§7.2: an unreceipted drop is an operational observation, not a finding."""
    with pytest.raises(GroundMissing):
        clause_requirement(species=PendingSpecies.EXPIRED_ABANDONED)
    element = clause_requirement(
        species=PendingSpecies.EXPIRED_ABANDONED, eviction_receipt="Ercpt"
    )
    assert element.eviction_receipt == "Ercpt"


def test_only_expired_abandoned_may_carry_an_eviction_receipt():
    with pytest.raises(MalformedInput):
        clause_requirement(species=PendingSpecies.ABSENT, eviction_receipt="Ercpt")


def test_composed_evidence_slots_ride_the_one_element_type():
    """this.i @blq6dwxz: §8's slot/issuer element is a specialization, not a rival."""
    element = clause_requirement(
        subject="Eschema",
        kind="composed-slot",
        attributes=(("expected-issuer", "Eissuer"), ("expected-issuer", "Eissuer")),
    )
    assert element.attributes == (("expected-issuer", "Eissuer"),)


def test_requirement_attributes_are_canonically_ordered():
    element = clause_requirement(attributes=(("z", "1"), ("a", "2")))
    assert element.attributes == (("a", "2"), ("z", "1"))


# --- self-convicted ---


def test_self_convicted_carries_the_proof_package_identifier():
    """this.i @3cmjjo: §7.3's SHALL names the identifier, not the package."""
    finding = SelfConvicted(LAW, POS, proof="Eproof")
    assert finding.verdict is Verdict.SELF_CONVICTED
    assert finding.proof == "Eproof"


def test_self_convicted_without_a_proof_identifier_is_not_a_finding():
    with pytest.raises(GroundMissing):
        SelfConvicted(LAW, POS, proof="")


# --- determinism ---


def test_two_constructions_of_one_finding_are_byte_identical():
    """§7.3: two evaluations of the same triple return byte-identical findings."""
    make = lambda: Pending(  # noqa: E731 - one expression, twice, on purpose
        LAW, POS, requirements=(clause_requirement(), clause_requirement(subject="Eb"))
    )
    assert make().canonical_bytes() == make().canonical_bytes()


def test_the_four_values_have_distinct_canonical_bytes():
    findings = [
        Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Ec",)),
        Defeated(LAW, POS, defeat=Defeat(DefeaterClass.CRYPTO, Citation("Ec"))),
        Pending(LAW, POS, requirements=(clause_requirement(),)),
        SelfConvicted(LAW, POS, proof="Eproof"),
    ]
    assert len({f.canonical_bytes() for f in findings}) == 4


def test_findings_differing_only_by_subcode_are_distinguishable():
    """this.i @qru6hx: the subcode is carried, not discarded after selection."""
    plain = Defeated(LAW, POS, defeat=Defeat(DefeaterClass.MERIT, Citation("Ec")))
    coded = Defeated(
        LAW, POS, defeat=Defeat(DefeaterClass.MERIT, Citation("Ec"), subcode="s1")
    )
    assert plain.canonical_bytes() != coded.canonical_bytes()


# --- refusal is not a finding ---


def test_a_refusal_is_not_a_member_of_the_codomain():
    """§7.5 and §15: the return type is four values and nothing else."""
    refusal = Refusal(missing="no committed composition rule for Eseam", position=POS)
    assert not isinstance(refusal, Finding)


def test_a_refusal_names_what_is_missing():
    with pytest.raises(MalformedInput):
        Refusal(missing="", position=POS)


def test_a_refusal_travels_out_of_band():
    """this.i @aynhxtdk: raised, so it can never be stored where a finding goes."""
    refusal = Refusal(missing="no committed ilk table", position=POS, law_head=LAW)
    with pytest.raises(RefusedInvocation) as excinfo:
        raise RefusedInvocation(refusal)
    assert excinfo.value.refusal is refusal
    assert excinfo.value.code == "THESMO_REFUSED_INVOCATION"
    assert "no committed ilk table" in str(excinfo.value)


def test_a_refusal_has_canonical_bytes_with_and_without_a_law_head():
    bare = Refusal(missing="no rule", position=POS)
    headed = Refusal(missing="no rule", position=POS, law_head=LAW)
    assert bare.canonical_bytes() != headed.canonical_bytes()


# --- compound results are a product, never a fifth scalar ---


def test_a_compound_result_is_a_product_and_not_a_finding():
    """§7.5: components keep their propositions and grounds; no fifth shape."""
    product = Product(
        components=(
            ("may-act", Affirmed(LAW, POS, bundle=BUNDLE, clause_set=("Ec",))),
            ("is-seated", Pending(LAW, POS, requirements=(clause_requirement(),))),
        )
    )
    assert not isinstance(product, Finding)
    assert [p for p, _ in product.components] == ["is-seated", "may-act"]


def test_a_product_needs_at_least_one_component():
    with pytest.raises(GroundMissing):
        Product(components=())


def test_a_product_rejects_a_repeated_proposition():
    finding = SelfConvicted(LAW, POS, proof="Eproof")
    with pytest.raises(MalformedInput):
        Product(components=(("q", finding), ("q", finding)))


def test_a_product_rejects_an_unnamed_proposition():
    with pytest.raises(MalformedInput):
        Product(components=(("", SelfConvicted(LAW, POS, proof="Eproof")),))


def test_a_product_is_byte_stable_under_component_permutation():
    a = ("a", SelfConvicted(LAW, POS, proof="Ep1"))
    b = ("b", SelfConvicted(LAW, POS, proof="Ep2"))
    assert Product((a, b)).canonical_bytes() == Product((b, a)).canonical_bytes()
