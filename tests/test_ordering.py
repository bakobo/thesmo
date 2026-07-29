"""The evidence ordering and the canonical selection of defeats (Custos 4.1 §7.3).

Two rules are under test, and they are not the same rule despite sharing a
section. The *evidence ordering* is a partial order on bundles (⊆) that makes
appraisal monotone. *Canonical selection* is a total order on simultaneously
available defeats that makes the chosen citation deterministic — and its
paragraph contradicts itself, which is why entry 5 of ``docs/readings-beta.md``
exists and why the empty-subcode tests below are so pointed.
"""

import pytest

from thesmo.core.errors import NoDefeatAvailable, RefusedInvocation
from thesmo.core.finding import (
    Affirmed,
    Citation,
    Defeat,
    DefeaterClass,
    Pending,
    PendingSpecies,
    RequirementElement,
)
from thesmo.core.ordering import (
    bundle_refines,
    canonical_evidence_order,
    canonical_requirements,
    discharge,
    select_defeat,
    undischarged,
)
from thesmo.core.triple import EvidenceBundle, EvidenceItem, LawHead, Position

LAW = LawHead("Elaw")
POS = Position("Egel", 4)


def requirement(subject="Es", kind="k", clauses=("Ec",), species=PendingSpecies.ABSENT):
    return RequirementElement(
        subject=subject, kind=kind, citing_clauses=clauses, species=species
    )


# --- the evidence ordering: the subset order on bundles ---


def test_a_bundle_refines_its_own_subsets():
    a, b = EvidenceItem("Ea"), EvidenceItem("Eb")
    larger = EvidenceBundle.of(a, b)
    assert bundle_refines(larger, EvidenceBundle.of(a)) is True
    assert bundle_refines(larger, larger) is True


def test_a_bundle_does_not_refine_a_bundle_it_lacks_evidence_from():
    a, b = EvidenceItem("Ea"), EvidenceItem("Eb")
    assert bundle_refines(EvidenceBundle.of(a), EvidenceBundle.of(a, b)) is False


def test_incomparable_bundles_refine_neither_way():
    a, b = EvidenceItem("Ea"), EvidenceItem("Eb")
    one, two = EvidenceBundle.of(a), EvidenceBundle.of(b)
    assert bundle_refines(one, two) is False
    assert bundle_refines(two, one) is False


def test_rechunking_the_same_evidence_does_not_break_comparability():
    """this.i @sgc5lpwd: item membership, so ⊆ cannot depend on presentation."""
    parts = [EvidenceItem(f"E{n}") for n in range(4)]
    whole = EvidenceBundle.of(*parts)
    halves = EvidenceBundle.of(*parts[:2])
    assert bundle_refines(whole, halves) is True


def test_canonical_evidence_order_is_reachable_from_the_ordering_module():
    """§17's consumption order is 4.1-only law; it lives beside the §7.3 order."""
    a, b = EvidenceItem("Ea"), EvidenceItem("Eb")
    assert canonical_evidence_order(EvidenceBundle.of(b, a)) == (a, b)


# --- canonical selection of defeats ---


def test_selection_prefers_the_lower_ranked_defeater_class():
    """§7.3: crypto, authority, merit, superseded — in that order."""
    crypto = Defeat(DefeaterClass.CRYPTO, Citation("Ez"))
    superseded = Defeat(DefeaterClass.SUPERSEDED, Citation("Ea"))
    assert select_defeat([superseded, crypto]) is crypto


def test_selection_falls_to_the_citation_identifier_within_a_class():
    early = Defeat(DefeaterClass.MERIT, Citation("Ea"))
    late = Defeat(DefeaterClass.MERIT, Citation("Eb"))
    assert select_defeat([late, early]) is early


def test_selection_orders_an_empty_subcode_last():
    """The discriminating input of ``docs/readings-beta.md`` entry 5.

    A strict-lexicographic engine cites the empty-subcode defeat; we cite the
    other one. §7.3 requires both engines to agree byte for byte, and they
    cannot.
    """
    empty = Defeat(DefeaterClass.MERIT, Citation("EClauseX"))
    coded = Defeat(DefeaterClass.MERIT, Citation("EClauseX"), subcode="a")
    assert select_defeat([empty, coded]) is coded


def test_selection_orders_non_empty_subcodes_by_bytes():
    first = Defeat(DefeaterClass.MERIT, Citation("Ec"), subcode="a")
    second = Defeat(DefeaterClass.MERIT, Citation("Ec"), subcode="b")
    assert select_defeat([second, first]) is first


def test_selection_is_independent_of_presentation_order():
    """§7.3: two verifiers holding the same bundle emit the same defeated finding."""
    defeats = [
        Defeat(DefeaterClass.SUPERSEDED, Citation("Ea")),
        Defeat(DefeaterClass.MERIT, Citation("Eb"), subcode="x"),
        Defeat(DefeaterClass.MERIT, Citation("Eb")),
    ]
    assert select_defeat(defeats) == select_defeat(list(reversed(defeats)))


def test_selection_with_nothing_to_select_is_an_error_not_a_guess():
    with pytest.raises(NoDefeatAvailable) as excinfo:
        select_defeat([])
    assert excinfo.value.code == "THESMO_NO_DEFEAT_AVAILABLE"


# --- canonical requirement sets ---


def test_canonical_requirements_deduplicate_and_order():
    b, a = requirement(subject="Eb"), requirement(subject="Ea")
    assert canonical_requirements([b, a, b]) == (a, b)


def test_canonical_requirements_of_nothing_is_empty():
    assert canonical_requirements([]) == ()


def test_undischarged_keeps_only_what_the_bundle_has_not_discharged():
    open_one, closed_one = requirement(subject="Ea"), requirement(subject="Eb")
    assert undischarged((open_one, closed_one), [closed_one]) == (open_one,)


# --- the affirmation discipline ---


def test_a_fully_discharged_space_affirms():
    """§7.3: affirmed is reachable only over a bundle that discharges the space."""
    element = requirement()
    finding = discharge(
        space=(element,),
        discharged=(element,),
        law_head=LAW,
        position=POS,
        bundle=EvidenceBundle.of(EvidenceItem("Ea")),
        clause_set=("Ec",),
    )
    assert isinstance(finding, Affirmed)


def test_an_empty_committed_space_affirms_vacuously():
    finding = discharge(
        space=(),
        discharged=(),
        law_head=LAW,
        position=POS,
        bundle=EvidenceBundle.of(EvidenceItem("Ea")),
        clause_set=("Ec",),
    )
    assert isinstance(finding, Affirmed)


def test_an_unexamined_defeater_check_pends_and_never_affirms():
    """§7.3: "returns pending with that check as its typed requirement, never affirmed"."""
    element = requirement()
    finding = discharge(
        space=(element,),
        discharged=(),
        law_head=LAW,
        position=POS,
        bundle=EvidenceBundle.of(EvidenceItem("Ea")),
        clause_set=("Ec",),
    )
    assert isinstance(finding, Pending)
    assert finding.requirements == (element,)


def test_an_underivable_requirement_space_refuses():
    """this.i @nup3m6: a missing rule, not missing evidence — so not pending."""
    with pytest.raises(RefusedInvocation) as excinfo:
        discharge(
            space=None,
            discharged=(),
            law_head=LAW,
            position=POS,
            bundle=EvidenceBundle.of(EvidenceItem("Ea")),
            clause_set=("Ec",),
        )
    assert excinfo.value.refusal.position is POS
    assert excinfo.value.refusal.law_head is LAW
