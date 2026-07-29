"""The four-valued finding codomain, with the ground as part of the type.

Custos §7.1:

    Governance appraisal in a GARD returns exactly one type: the finding. A
    finding is a judgment over a committed regime that carries its own ground —
    the citation, requirement, or proof that justifies it. A value that does not
    carry its ground is not a member of this type, whatever else it may be.

That last sentence is why the grounds are constructor arguments and not optional
fields: a bare verdict is unconstructible here, and `GroundMissing` is a typing
failure rather than a validation one.

Three pinned readings live in this module, each with a node in this.i and a
numbered entry in docs/readings-alpha.md:

- **affirmed carries a payload** (@lkfaqca). §7.1 gives affirmed a ground — "the
  evidence bundle and the clause set under which it was appraised" — while
  §7.3's "Required payloads" lists only the other three. §1.4 axiom 1 outranks
  an enumeration that dropped a row.
- **every finding carries its triple** (@krkkmwhh). §14: "every finding retains
  its position, its defeated clause, its verification grain, and its committed
  law head." (`verification grain` occurs once in 4.1, is defined nowhere, and
  is therefore not implemented.)
- **requirement kind and pending species are two fields** (@2kzvek2). §7.3 names
  the first, §7.2 rules the second, and §8's "required schema, expected issuer"
  cannot be expressed in §7.2's closed four.

Refusal lives here too, precisely so that its disjointness from `Finding` is
visible at the top of the file: §7.5, "Refusal is not a fifth finding value."
"""

from dataclasses import dataclass, field
from enum import Enum

from thesmo.core.errors import GroundMissing, MalformedInput, require
from thesmo.core.triple import AppraisalTriple

#: Separator for flattening a clause list to "citing-clause bytes" (§7.3).
#: Below every character a self-addressing identifier can carry, so the
#: flattening is injective and the canonical order stays total. The standard
#: states no separator; this is a pin (this.i @nxoq2hd).
CLAUSE_SEPARATOR = b"\x00"


class Verdict(Enum):
    """The four values, and no fifth. §7.1; §15 makes the count a wall."""

    AFFIRMED = "affirmed"
    DEFEATED = "defeated"
    PENDING = "pending"
    SELF_CONVICTED = "self-convicted"


class DefeaterClass(Enum):
    """§7.3: "The defeater classes are enumerated and ranked, in this order".

    The rank is the ranking the section states, which is deliberately not
    alphabetical — comparing the class *names* as bytes would put authority
    ahead of crypto and select a different defeat (this.i @zmwnx35s).
    """

    CRYPTO = (0, "a cryptographic verification failed")
    AUTHORITY = (1, "the actor lacked the invoked power")
    MERIT = (2, "the content violates a committed clause")
    SUPERSEDED = (3, "a later lawful act displaced the subject")

    @property
    def rank(self):
        return self.value[0]

    @property
    def gloss(self):
        return self.value[1]


class PendingSpecies(Enum):
    """§7.2's four discharge species, in the order the amendment declares them.

    The order is load-bearing twice over: it is the document's own enumeration,
    and it is the merge order for two elements that collide on the canonical
    sort key, which §7.3 leaves unstated (this.i @kdrqzc).
    """

    ABSENT = (0, "cured by the arrival of the missing evidence")
    WINDOW_OPEN = (1, "cured when no superseding event remains admissible")
    UNRESOLVED_CONFLICT = (2, "cured by an owned act of the party whose conflict it is")
    EXPIRED_ABANDONED = (3, "cured by re-presentation")

    @property
    def rank(self):
        return self.value[0]

    @property
    def cure(self):
        return self.value[1]


def _clause(value):
    require(
        isinstance(value, str) and value != "",
        MalformedInput,
        f"a clause citation must be a non-empty identifier; got {value!r}. A "
        "citation that names nothing is not a ground, and Custos §1.4 axiom 1 "
        "admits no bare verdicts.",
    )
    return value


@dataclass(frozen=True, slots=True)
class RequirementElement:
    """One element of a pending finding's typed requirement set (§7.3, §7.2).

    Canonical on construction: the citing-clause list arrives in whatever order
    the caller had and is stored sorted, because the order the committed law
    enumerates clauses in is not among the fold's three inputs (this.i @nxoq2hd).
    """

    subject: str
    kind: str
    citing_clauses: tuple
    species: PendingSpecies

    def __post_init__(self):
        require(
            isinstance(self.subject, str) and self.subject != "",
            MalformedInput,
            f"a requirement element's subject must be a non-empty identifier; got "
            f"{self.subject!r}. §7.3 requires each element to name its subject.",
        )
        require(
            isinstance(self.kind, str) and self.kind != "",
            MalformedInput,
            f"a requirement element's kind must be a non-empty name; got "
            f"{self.kind!r}. §7.3 requires each element to carry its requirement "
            "kind, which §7.2's discharge species do not supply.",
        )
        require(
            isinstance(self.species, PendingSpecies),
            MalformedInput,
            f"a requirement element's species must be one of §7.2's four; got "
            f"{self.species!r}. The species is what names the cure path.",
        )
        clauses = tuple(self.citing_clauses)
        for clause in clauses:
            _clause(clause)
        require(
            clauses != (),
            GroundMissing,
            "a requirement element must name the clauses that make it required; "
            "an element citing nothing is a requirement no committed law imposed.",
        )
        object.__setattr__(self, "citing_clauses", tuple(sorted(set(clauses))))

    def citing_clause_bytes(self):
        """The element's clause list flattened to the bytes §7.3 sorts on."""
        return CLAUSE_SEPARATOR.join(c.encode("utf-8") for c in self.citing_clauses)

    def sort_key(self):
        """§7.3's canonical order: "subject, then kind, then citing-clause bytes".

        Species is absent from the key because the section's parenthetical names
        three components and stops.
        """
        return (self.subject, self.kind, self.citing_clause_bytes())

    def dedup_key(self):
        """What "deduplicated elements" deduplicates on: exactly the sort key.

        Deduplicating on anything wider — the species, say — lets two elements
        share a sort key, which makes §7.3's "canonical order" a preorder and
        the finding's bytes undetermined (this.i @kdrqzc).
        """
        return self.sort_key()


@dataclass(frozen=True, slots=True)
class Finding:
    """A judgment over a committed regime, carrying its ground.

    Abstract: the four values below are the whole codomain, and the base class
    has no verdict of its own precisely so that a bare verdict cannot be built.
    """

    question: str
    triple: AppraisalTriple

    VERDICT = None

    def __post_init__(self):
        require(
            self.VERDICT is not None,
            TypeError,
            "Finding is the type, not a value: instantiate one of affirmed, "
            "defeated, pending or self-convicted. Custos §7.1's codomain has four "
            "members and §15 makes that count a wall.",
        )
        require(
            isinstance(self.question, str) and self.question != "",
            GroundMissing,
            "a finding must name the proposition it judges; got "
            f"{self.question!r}. §4: findings are judgments about propositions.",
        )
        require(
            isinstance(self.triple, AppraisalTriple),
            MalformedInput,
            f"a finding must carry the appraisal triple it was computed over; got "
            f"{self.triple!r}. §14 rules that every finding retains its position "
            "and its committed law head.",
        )

    @property
    def verdict(self):
        return self.VERDICT

    @property
    def bundle(self):
        return self.triple.bundle

    @property
    def law_head(self):
        return self.triple.law_head

    @property
    def position(self):
        return self.triple.position


@dataclass(frozen=True, slots=True)
class Affirmed(Finding):
    """§7.1: "the proposition holds over the committed evidence."

    Ground: the evidence bundle (carried by the triple) and the clause set under
    which it was appraised. §7.3 forgets to require the clause set; §1.4 axiom 1
    requires it anyway (this.i @lkfaqca).
    """

    clause_set: tuple = ()

    VERDICT = Verdict.AFFIRMED

    def __post_init__(self):
        super().__post_init__()
        clauses = tuple(self.clause_set)
        for clause in clauses:
            _clause(clause)
        require(
            clauses != (),
            GroundMissing,
            "an affirmed finding must carry the clause set it was appraised under. "
            "§7.1 names the evidence bundle and the clause set as its ground, and "
            "an affirmation citing no clause is the bare verdict §1.4 axiom 1 "
            "excludes from the codomain.",
        )
        object.__setattr__(self, "clause_set", tuple(sorted(set(clauses))))


@dataclass(frozen=True, slots=True)
class Defeated(Finding):
    """§7.1: "the proposition is defeated by committed evidence."

    Ground: the defeater's class and the citation — "the violated or superseding
    clause's identifier, or, for cryptographic defeat, the identifier of the
    failed verification subject" (§7.3).
    """

    defeater_class: DefeaterClass = None
    citation: str = ""
    subcode: str = ""

    VERDICT = Verdict.DEFEATED

    def __post_init__(self):
        super().__post_init__()
        require(
            isinstance(self.defeater_class, DefeaterClass),
            MalformedInput,
            f"a defeated finding's defeater class must be one of §7.3's four; got "
            f"{self.defeater_class!r}. The class is half the ground and it is also "
            "the first component of canonical selection.",
        )
        require(
            isinstance(self.citation, str) and self.citation != "",
            GroundMissing,
            "a defeated finding must carry its citation: the violated or "
            "superseding clause, or the failed verification subject. §7.3: "
            "neither the class nor the citation is reconstructible from a bare "
            "verdict.",
        )
        require(
            isinstance(self.subcode, str),
            MalformedInput,
            f"a subcode must be a string, empty where the cited clause defines no "
            f"enumeration; got {self.subcode!r}.",
        )


@dataclass(frozen=True, slots=True)
class Pending(Finding):
    """§7.1: the evidence "neither affirms nor defeats; the finding names what is missing."

    Ground: the typed requirement set, deduplicated and in §7.3's canonical
    order. The invariant is checked here rather than assumed, so a non-canonical
    set cannot be smuggled into a finding whose bytes are supposed to be
    determined; ``ordering.canonical_requirement_set`` is how one is built.
    """

    requirements: tuple = ()

    VERDICT = Verdict.PENDING

    def __post_init__(self):
        super().__post_init__()
        elements = tuple(self.requirements)
        for element in elements:
            require(
                isinstance(element, RequirementElement),
                MalformedInput,
                f"a typed requirement set holds RequirementElements; got "
                f"{element!r}. §7.3 requires each element to carry its kind, its "
                "subject and its citing clauses.",
            )
        require(
            elements != (),
            GroundMissing,
            "a pending finding must name what is missing. §7.1: pending is the "
            "value whose ground is the typed requirement set, and a pending "
            "finding with an empty set names nothing that would discharge it.",
        )
        keys = [element.sort_key() for element in elements]
        require(
            keys == sorted(keys),
            MalformedInput,
            "a pending finding's requirement set must be in §7.3's canonical "
            "order (subject, then kind, then citing-clause bytes). Build it with "
            "ordering.canonical_requirement_set rather than sorting by hand.",
        )
        require(
            len(set(keys)) == len(keys),
            MalformedInput,
            "a pending finding's requirement set must be deduplicated (§7.3). Two "
            "elements sharing a canonical key leave the set's order a preorder and "
            "the finding's bytes undetermined; canonical_requirement_set merges them.",
        )
        object.__setattr__(self, "requirements", elements)


@dataclass(frozen=True, slots=True)
class SelfConvicted(Finding):
    """§7.1: "the subject's own committed bytes contain a contradiction".

    Ground: "the identifier of the canonical proof package for the contradictory
    pair" (§7.3).
    """

    proof_package: str = ""

    VERDICT = Verdict.SELF_CONVICTED

    def __post_init__(self):
        super().__post_init__()
        require(
            isinstance(self.proof_package, str) and self.proof_package != "",
            GroundMissing,
            "a self-convicted finding must carry the identifier of the canonical "
            "proof package for the contradictory pair. §7.4: self-conviction is "
            "conviction by one's own committed pair, and without the pair there is "
            "nothing convicting.",
        )


@dataclass(frozen=True, slots=True)
class Refusal:
    """Not a finding. §7.5:

        Refusal is not a fifth finding value — it is the evaluator declining to
        answer an ill-posed question, recorded as an operational fact.

    Deliberately not a subclass of ``Finding`` and deliberately not an
    exception: it is returned and recorded, and §1.4 axiom 3 requires that "the
    refusal names what is missing" (this.i @iezwqh).
    """

    question: str
    triple: AppraisalTriple
    missing: str
    code: str = "CORE-REFUSAL-UNCOMMITTED-SEAM"

    def __post_init__(self):
        require(
            isinstance(self.question, str) and self.question != "",
            GroundMissing,
            "a refusal must name the invocation it declines.",
        )
        require(
            isinstance(self.triple, AppraisalTriple),
            MalformedInput,
            f"a refusal must carry the triple it was invoked over; got "
            f"{self.triple!r}.",
        )
        require(
            isinstance(self.missing, str) and self.missing != "",
            GroundMissing,
            "a refusal must name what is missing. §1.4 axiom 3: 'Where committed "
            "law runs out, the fold refuses rather than legislates. The refusal "
            "names what is missing.' A refusal that names nothing is the "
            "discretion replay exists to eliminate.",
        )


#: The constructor for each value, so a caller can dispatch on the verdict
#: without a chain of isinstance checks.
FINDING_TYPES = {
    Verdict.AFFIRMED: Affirmed,
    Verdict.DEFEATED: Defeated,
    Verdict.PENDING: Pending,
    Verdict.SELF_CONVICTED: SelfConvicted,
}


def verdict_of(value):
    """The verdict of a finding, or ``None`` for anything that is not one.

    A refusal answers ``None`` — that is the point of it. §7.5's wall is that
    refusal never becomes a fifth value, so the one function that maps values to
    verdicts must have somewhere to put it that is not the codomain.
    """
    return value.verdict if isinstance(value, Finding) else None
