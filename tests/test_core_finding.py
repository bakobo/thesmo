"""The four-valued finding codomain (Custos §7.1) and its required payloads (§7.3).

The Ground Axiom is applied here as a typing rule, exactly as §7.1 asks: "A
value that does not carry its ground is not a member of this type, whatever else
it may be." So every test that constructs a finding without its ground expects a
refusal to construct, not a finding with an empty field.

Two pinned readings are exercised hard, because they are where a second engine
would diverge: affirmed carries a payload (this.i @lkfaqca) and every finding
carries the triple it was computed over (this.i @krkkmwhh).
"""

import pytest

from thesmo.core.errors import GroundMissing, MalformedInput
from thesmo.core.finding import (
    Affirmed,
    DefeaterClass,
    Defeated,
    Finding,
    Pending,
    PendingSpecies,
    Refusal,
    RequirementElement,
    SelfConvicted,
    Verdict,
    verdict_of,
)
from thesmo.core.triple import (
    AppraisalTriple,
    Coordinate,
    EvidenceBundle,
    EvidenceItem,
    LawHead,
    Position,
)

TRIPLE = AppraisalTriple(
    bundle=EvidenceBundle.of(EvidenceItem("EEvi000", Coordinate(0, 0))),
    law_head=LawHead("ELaw000"),
    position=Position("EGar000", 4),
)


def element(subject="EArt000", kind="schema", clauses=("EClause0",), species=None):
    return RequirementElement(
        subject=subject,
        kind=kind,
        citing_clauses=clauses,
        species=species or PendingSpecies.ABSENT,
    )


class TestTheCodomainIsFourValued:
    def test_exactly_four_verdicts(self):
        assert [v.name for v in Verdict] == [
            "AFFIRMED",
            "DEFEATED",
            "PENDING",
            "SELF_CONVICTED",
        ]

    def test_each_value_reports_its_verdict(self):
        cases = [
            (Affirmed(question="q", triple=TRIPLE, clause_set=("EC1",)), Verdict.AFFIRMED),
            (
                Defeated(
                    question="q",
                    triple=TRIPLE,
                    defeater_class=DefeaterClass.MERIT,
                    citation="EC1",
                ),
                Verdict.DEFEATED,
            ),
            (Pending(question="q", triple=TRIPLE, requirements=(element(),)), Verdict.PENDING),
            (
                SelfConvicted(question="q", triple=TRIPLE, proof_package="EProof0"),
                Verdict.SELF_CONVICTED,
            ),
        ]
        for finding, expected in cases:
            assert finding.verdict is expected
            assert verdict_of(finding) is expected

    def test_a_refusal_is_not_a_finding(self):
        # §7.5: "Refusal is not a fifth finding value." §15 makes the four-valued
        # codomain a wall. The type system is where that wall is cheapest to hold.
        refusal = Refusal(question="q", triple=TRIPLE, missing="no committed bearing rule")
        assert not isinstance(refusal, Finding)
        assert verdict_of(refusal) is None

    def test_a_refusal_names_what_is_missing(self):
        # §1.4 axiom 3: "The refusal names what is missing."
        with pytest.raises(GroundMissing):
            Refusal(question="q", triple=TRIPLE, missing="")

    def test_findings_of_different_values_are_never_equal(self):
        affirmed = Affirmed(question="q", triple=TRIPLE, clause_set=("EC1",))
        convicted = SelfConvicted(question="q", triple=TRIPLE, proof_package="EProof0")
        assert affirmed != convicted


class TestEveryFindingCarriesItsTriple:
    """this.i @krkkmwhh — §14: "every finding retains its position ... and its
    committed law head." §7.3's payload list omits both."""

    def test_law_head_and_position_are_reachable_from_the_finding(self):
        finding = Affirmed(question="q", triple=TRIPLE, clause_set=("EC1",))
        assert finding.law_head == LawHead("ELaw000")
        assert finding.position == Position("EGar000", 4)
        assert finding.bundle == TRIPLE.bundle

    def test_one_proposition_under_two_law_heads_gives_two_findings(self):
        other = AppraisalTriple(
            bundle=TRIPLE.bundle, law_head=LawHead("ELaw999"), position=TRIPLE.position
        )
        assert Affirmed(question="q", triple=TRIPLE, clause_set=("EC1",)) != Affirmed(
            question="q", triple=other, clause_set=("EC1",)
        )

    def test_rejects_a_missing_question_or_a_non_triple(self):
        with pytest.raises(GroundMissing):
            Affirmed(question="", triple=TRIPLE, clause_set=("EC1",))
        with pytest.raises(MalformedInput):
            Affirmed(question="q", triple="not a triple", clause_set=("EC1",))


class TestAffirmedCarriesItsGround:
    """this.i @lkfaqca — §7.1 gives affirmed a ground; §7.3 forgets to list it."""

    def test_carries_the_clause_set_it_was_appraised_under(self):
        assert Affirmed(question="q", triple=TRIPLE, clause_set=("EC2", "EC1")).clause_set == (
            "EC1",
            "EC2",
        )

    def test_clause_set_is_a_set_deduplicated_and_ordered(self):
        assert Affirmed(question="q", triple=TRIPLE, clause_set=("EC1", "EC1")).clause_set == (
            "EC1",
        )

    def test_refuses_a_bare_affirmation(self):
        # §1.4 axiom 1: "The codomain admits no bare verdicts."
        with pytest.raises(GroundMissing):
            Affirmed(question="q", triple=TRIPLE, clause_set=())

    def test_refuses_an_empty_clause_identifier(self):
        with pytest.raises(MalformedInput):
            Affirmed(question="q", triple=TRIPLE, clause_set=("",))


class TestDefeatedCarriesClassAndCitation:
    def test_carries_both_and_an_optional_subcode(self):
        finding = Defeated(
            question="q",
            triple=TRIPLE,
            defeater_class=DefeaterClass.CRYPTO,
            citation="ESubject0",
            subcode="sig",
        )
        assert finding.defeater_class is DefeaterClass.CRYPTO
        assert finding.citation == "ESubject0"
        assert finding.subcode == "sig"

    def test_subcode_defaults_to_empty(self):
        # §7.3: "where the clause defines none, the subcode is empty".
        assert (
            Defeated(
                question="q",
                triple=TRIPLE,
                defeater_class=DefeaterClass.MERIT,
                citation="EC1",
            ).subcode
            == ""
        )

    def test_refuses_a_missing_citation(self):
        with pytest.raises(GroundMissing):
            Defeated(
                question="q", triple=TRIPLE, defeater_class=DefeaterClass.MERIT, citation=""
            )

    def test_refuses_a_defeater_class_that_is_not_one_of_the_four(self):
        with pytest.raises(MalformedInput):
            Defeated(question="q", triple=TRIPLE, defeater_class="merit", citation="EC1")


class TestDefeaterClassRanking:
    def test_ranked_in_the_specified_order_not_alphabetically(self):
        # this.i @zmwnx35s. Alphabetical would put authority before crypto.
        assert [c.name for c in sorted(DefeaterClass, key=lambda c: c.rank)] == [
            "CRYPTO",
            "AUTHORITY",
            "MERIT",
            "SUPERSEDED",
        ]

    def test_ranks_are_dense_from_zero(self):
        assert [c.rank for c in DefeaterClass] == [0, 1, 2, 3]

    def test_each_class_carries_the_specification_s_own_gloss(self):
        # §7.3 defines the four classes in-line; keeping the definitions on the
        # enum means a reader of a defeated finding never has to guess which
        # "authority" is meant.
        assert DefeaterClass.AUTHORITY.gloss == "the actor lacked the invoked power"


class TestPendingSpecies:
    def test_the_four_species_in_declaration_order(self):
        # §7.2. The declaration order is load-bearing: it is the merge order
        # for elements that collide on the canonical sort key (this.i @kdrqzc).
        assert [s.name for s in PendingSpecies] == [
            "ABSENT",
            "WINDOW_OPEN",
            "UNRESOLVED_CONFLICT",
            "EXPIRED_ABANDONED",
        ]
        assert PendingSpecies.ABSENT.rank < PendingSpecies.EXPIRED_ABANDONED.rank

    def test_each_species_names_its_cure(self):
        # §7.2: "Each species names its cure". A species without its cure path
        # is exactly the "additional terminal finding" the amendment forbids.
        assert PendingSpecies.EXPIRED_ABANDONED.cure == "cured by re-presentation"


class TestRequirementElement:
    def test_carries_kind_and_species_as_distinct_fields(self):
        # this.i @2kzvek2 — §7.3 says "kind", §7.2 says "species", and they are
        # not the same field.
        subject = element(kind="schema", species=PendingSpecies.WINDOW_OPEN)
        assert subject.kind == "schema"
        assert subject.species is PendingSpecies.WINDOW_OPEN

    def test_citing_clauses_are_sorted_and_deduplicated(self):
        # this.i @nxoq2hd — the law's own enumeration order is not among the
        # fold's three inputs, so it cannot be the order used.
        assert element(clauses=("EC2", "EC1", "EC2")).citing_clauses == ("EC1", "EC2")

    def test_sort_key_is_subject_then_kind_then_citing_clause_bytes(self):
        assert element(subject="A").sort_key() < element(subject="B").sort_key()
        assert element(subject="A", kind="a").sort_key() < element(
            subject="A", kind="b"
        ).sort_key()
        assert element(subject="A", kind="k", clauses=("EC1",)).sort_key() < element(
            subject="A", kind="k", clauses=("EC2",)
        ).sort_key()

    def test_citing_clause_bytes_are_separated_so_the_flattening_is_injective(self):
        # this.i @nxoq2hd, second fork: ["a","bc"] and ["ab","c"] must not
        # flatten to one key, or the "canonical order" is not a total order.
        assert element(clauses=("a", "bc")).sort_key() != element(
            clauses=("ab", "c")
        ).sort_key()

    def test_species_is_not_in_the_sort_key(self):
        # §7.3 states the key as (subject, kind, citing-clause bytes) and stops.
        assert (
            element(species=PendingSpecies.ABSENT).sort_key()
            == element(species=PendingSpecies.EXPIRED_ABANDONED).sort_key()
        )

    def test_dedup_key_equals_the_sort_key(self):
        # this.i @kdrqzc — deduplicating on anything wider leaves the canonical
        # order a preorder and the finding's bytes undetermined.
        assert element(species=PendingSpecies.ABSENT).dedup_key() == element(
            species=PendingSpecies.WINDOW_OPEN
        ).dedup_key()

    def test_refuses_an_element_with_no_citing_clause(self):
        # §7.3: elements carry "the clauses that make it required". None means
        # no ground.
        with pytest.raises(GroundMissing):
            element(clauses=())

    @pytest.mark.parametrize(
        "kwargs",
        [{"subject": ""}, {"kind": ""}, {"clauses": ("",)}],
    )
    def test_refuses_malformed_components(self, kwargs):
        with pytest.raises(MalformedInput):
            element(**kwargs)

    def test_refuses_a_species_that_is_not_one_of_the_four(self):
        with pytest.raises(MalformedInput):
            element(species="absent")


class TestPendingCarriesItsRequirementSet:
    def test_carries_the_elements(self):
        finding = Pending(question="q", triple=TRIPLE, requirements=(element(),))
        assert finding.requirements == (element(),)

    def test_refuses_an_empty_requirement_set(self):
        # A pending finding that names nothing missing is a bare verdict.
        with pytest.raises(GroundMissing):
            Pending(question="q", triple=TRIPLE, requirements=())

    def test_refuses_a_requirement_set_that_is_not_in_canonical_order(self):
        # The type will not hold a non-canonical set: ordering.canonical_requirement_set
        # is the only lawful way to build one.
        with pytest.raises(MalformedInput):
            Pending(
                question="q",
                triple=TRIPLE,
                requirements=(element(subject="B"), element(subject="A")),
            )

    def test_refuses_a_requirement_set_with_a_duplicate_key(self):
        with pytest.raises(MalformedInput):
            Pending(
                question="q",
                triple=TRIPLE,
                requirements=(
                    element(species=PendingSpecies.ABSENT),
                    element(species=PendingSpecies.WINDOW_OPEN),
                ),
            )

    def test_refuses_a_member_that_is_not_a_requirement_element(self):
        with pytest.raises(MalformedInput):
            Pending(question="q", triple=TRIPLE, requirements=("EArt000",))


class TestSelfConvictedCarriesItsProof:
    def test_carries_the_proof_package_identifier(self):
        finding = SelfConvicted(question="q", triple=TRIPLE, proof_package="EProof0")
        assert finding.proof_package == "EProof0"

    def test_refuses_a_conviction_without_a_proof_package(self):
        with pytest.raises(GroundMissing):
            SelfConvicted(question="q", triple=TRIPLE, proof_package="")


class TestFindingsAreValues:
    def test_equal_findings_over_equal_triples_are_equal_and_hashable(self):
        # §7.3: "Two evaluations of the same triple SHALL return byte-identical
        # findings." core/ compares structure, not bytes (this.i @holyd22k).
        one = Defeated(
            question="q", triple=TRIPLE, defeater_class=DefeaterClass.MERIT, citation="EC1"
        )
        two = Defeated(
            question="q", triple=TRIPLE, defeater_class=DefeaterClass.MERIT, citation="EC1"
        )
        assert one == two
        assert hash(one) == hash(two)

    def test_findings_are_immutable(self):
        finding = Affirmed(question="q", triple=TRIPLE, clause_set=("EC1",))
        with pytest.raises((AttributeError, TypeError)):
            finding.question = "other"

    def test_the_base_type_is_not_instantiable_as_a_bare_verdict(self):
        with pytest.raises(TypeError):
            Finding(question="q", triple=TRIPLE)
