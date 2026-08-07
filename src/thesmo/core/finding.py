"""The four-valued finding codomain and the payloads each value must carry.

Custos 4.1 §7.1: "Governance appraisal in a GARD returns exactly one type: the
finding. A finding is a judgment over a committed regime that carries its own
ground — the citation, requirement, or proof that justifies it. A value that
does not carry its ground is not a member of this type, whatever else it may
be."

That last sentence is implemented literally: every constructor below refuses a
groundless value, so a bare verdict is not merely discouraged, it is
unconstructible. §7.3's "Required payloads" supplies the ground for three of
the four values; the fourth, ``affirmed``, is grounded from §7.1 alone, which
is a fork — see ``docs/readings-beta.md`` entry 1 and this.i @dkypfoo.

Two things in this module are deliberately **not** findings, because the
document says they are not:

- ``Refusal`` — §7.5, "Refusal is not a fifth finding value". It is raised, not
  returned (this.i @aynhxtdk).
- ``Product`` — §7.5, compound results "preserve their component propositions
  and grounds as a product rather than collapse them into a fifth scalar
  shape".

Both are typed so that neither can be stored where a ``Finding`` is expected.
"""

import dataclasses
import enum

from .errors import GroundMissing, MalformedInput
from .triple import EvidenceBundle, LawHead, Position, encode_fields

__all__ = [
    "Affirmed",
    "Citation",
    "CitationKind",
    "Defeat",
    "DefeaterClass",
    "Defeated",
    "Finding",
    "Pending",
    "PendingSpecies",
    "Product",
    "Refusal",
    "RequirementElement",
    "SelfConvicted",
    "Verdict",
]


class Verdict(enum.StrEnum):
    """The codomain's four values, and there is no fifth (§7.1, §15 wall one)."""

    AFFIRMED = "affirmed"
    DEFEATED = "defeated"
    PENDING = "pending"
    SELF_CONVICTED = "self-convicted"


class DefeaterClass(enum.Enum):
    """The four defeater classes, in the ratified rank order (§7.3).

    "The defeater classes are enumerated and ranked, in this order, carried
    from the predecessor unchanged: crypto, authority, merit, superseded."
    """

    CRYPTO = "crypto"
    AUTHORITY = "authority"
    MERIT = "merit"
    SUPERSEDED = "superseded"

    @property
    def rank(self):
        """This class's position in the ratified ranking, counting from zero."""
        return _DEFEATER_RANKS[self]


_DEFEATER_RANKS = {
    DefeaterClass.CRYPTO: 0,
    DefeaterClass.AUTHORITY: 1,
    DefeaterClass.MERIT: 2,
    DefeaterClass.SUPERSEDED: 3,
}


class PendingSpecies(enum.StrEnum):
    """The ratified discharge species, each naming its cure (§7.2)."""

    ABSENT = "absent"
    WINDOW_OPEN = "window-open"
    UNRESOLVED_CONFLICT = "unresolved-conflict"
    EXPIRED_ABANDONED = "expired/abandoned"


class CitationKind(enum.StrEnum):
    """What a defeated finding's citation points at (§7.1, §7.3).

    §7.1 names "the defeating clause or superseding act"; §7.3 adds, "for
    cryptographic defeat, the identifier of the failed verification subject".
    The kind is carried explicitly because §9 requires a conviction to name the
    kind it convicts under, and §14 forbids blurring conviction kinds.
    """

    CLAUSE = "clause"
    ACT = "act"
    VERIFICATION_SUBJECT = "verification-subject"


def _sorted_unique(values):
    """Deduplicate and order by UTF-8 bytes.

    The document says "lexicographic" and never says over what; the fold's
    conformance predicate is stated in bytes, so bytes it is (this.i @5pu23u,
    ``docs/readings-beta.md`` entry 6).
    """
    return tuple(sorted(set(values), key=lambda value: value.encode("utf-8")))


@dataclasses.dataclass(frozen=True, slots=True)
class Citation:
    """What defeats a proposition, and what kind of thing it is.

    An **act** cited as a ground must carry a committed receipt. §15's fifth
    wall — "acts consumed as grounds require committed receipts" — is stated
    generally in both §15 and §1.4, and a wall stated generally is not narrowed
    to its single worked example (this.i @t66d4n, entry 24). Clause and
    verification-subject citations are untouched, since neither is an act.
    """

    identifier: str
    kind: CitationKind = CitationKind.CLAUSE
    receipt: str | None = None

    def __post_init__(self):
        if not self.identifier:
            raise MalformedInput(
                "A citation must identify what defeats the proposition — a "
                "clause, a superseding act, or the failed verification subject "
                "— and its identifier was empty. Retrying will not help; a "
                "defeated finding cannot be reconstructed from a bare verdict."
            )
        if self.kind is CitationKind.ACT and not self.receipt:
            raise GroundMissing(
                f"The act {self.identifier!r} is cited as a ground but carries "
                f"no committed receipt, and acts consumed as grounds require "
                f"committed receipts. Retrying will not help — commit the "
                f"receipt of the act first, then cite it."
            )
        if self.kind is not CitationKind.ACT and self.receipt is not None:
            raise MalformedInput(
                f"A receipt was attached to a {self.kind.value} citation, but "
                f"receipts stand for acts, not for clauses or verification "
                f"subjects. Retrying will not help — either cite the act, or "
                f"drop the receipt."
            )

    def canonical_bytes(self):
        return encode_fields(self.identifier, self.kind.value, self.receipt or "")


@dataclasses.dataclass(frozen=True, slots=True)
class Defeat:
    """A defeater class, its citation, and its discriminator within that citation.

    The subcode is carried on the finding rather than discarded after
    selection: §7.3 calls it "the defeat's discriminator within its citation"
    and §14 requires every finding to retain its verification grain (this.i
    @qru6hx, entry 4).
    """

    defeater_class: DefeaterClass
    citation: Citation
    subcode: str = ""

    @property
    def selection_key(self):
        """The key canonical selection minimises over (§7.3).

        The document says "the lexicographic minimum of (defeater-class rank,
        citation identifier, subcode)" and, four sentences later, that an empty
        subcode "orders last" — which no ordinary lexicographic order does,
        since the empty string is every such order's minimum. The specific rule
        governs the general one, so emptiness is a component of its own,
        ordering after every non-empty subcode (this.i @5pu23u, entry 5).
        """
        return (
            self.defeater_class.rank,
            self.citation.identifier.encode("utf-8"),
            self.subcode == "",
            self.subcode.encode("utf-8"),
        )

    def canonical_bytes(self):
        return encode_fields(
            self.defeater_class.value, self.citation.canonical_bytes(), self.subcode
        )


@dataclasses.dataclass(frozen=True, slots=True)
class RequirementElement:
    """One element of a pending finding's typed requirement set.

    §7.3: "deduplicated elements, each carrying requirement kind, subject
    identifier, and the list of citing clauses, in canonical order (subject,
    then kind, then citing-clause bytes)." §7.2 adds that the finding "SHALL
    carry the species of each of its requirement elements" — a mandatory field
    the sort key does not mention, so it is appended as a tiebreak and included
    in the deduplication key, since otherwise two cure paths for one subject
    collapse into one chosen by nothing committed (this.i @blq6dwxz, entry 11).

    ``attributes`` carries §8's composed-evidence extras — the slot's expected
    issuer above all — as committed key/value pairs, so §8's element shape is a
    specialization of this one type rather than a second type (entry 13).
    """

    subject: str
    kind: str
    citing_clauses: tuple
    species: PendingSpecies
    attributes: tuple = ()
    eviction_receipt: str | None = None

    def __post_init__(self):
        if not self.subject:
            raise MalformedInput(
                "A requirement element must name the subject the missing "
                "evidence is about, and its subject was empty. Retrying will "
                "not help — name the subject whose evidence would discharge it."
            )
        if not self.kind:
            raise MalformedInput(
                f"The requirement element for {self.subject!r} must name its "
                f"requirement kind, and the kind was empty. Retrying will not "
                f"help — a cure path that does not say what kind of evidence is "
                f"missing names no cure."
            )
        if not self.citing_clauses:
            raise GroundMissing(
                f"The requirement element for {self.subject!r} cites no clause, "
                f"but a typed requirement's ground is the clauses that make it "
                f"required. Retrying will not help — cite at least one clause "
                f"of the committed law."
            )
        if any(not clause for clause in self.citing_clauses):
            raise MalformedInput(
                f"The requirement element for {self.subject!r} carries an empty "
                f"clause identifier. Retrying will not help — every citing "
                f"clause is identified by the committed bytes it names."
            )
        if self.species is PendingSpecies.EXPIRED_ABANDONED and (
            self.eviction_receipt is None
        ):
            raise GroundMissing(
                f"The requirement element for {self.subject!r} is expired or "
                f"abandoned but carries no committed eviction receipt, and an "
                f"unreceipted drop is an operational observation rather than a "
                f"consumable finding value. Retrying will not help — commit the "
                f"eviction receipt, or record the drop outside the codomain."
            )
        if self.species is not PendingSpecies.EXPIRED_ABANDONED and (
            self.eviction_receipt is not None
        ):
            raise MalformedInput(
                f"An eviction receipt was attached to a "
                f"{self.species.value!r} requirement element, but an eviction "
                f"receipt grounds the expired/abandoned species and no other. "
                f"Retrying will not help — either set the species, or drop the "
                f"receipt."
            )
        object.__setattr__(self, "citing_clauses", _sorted_unique(self.citing_clauses))
        object.__setattr__(
            self,
            "attributes",
            tuple(
                sorted(
                    set(self.attributes),
                    key=lambda pair: (
                        pair[0].encode("utf-8"),
                        pair[1].encode("utf-8"),
                    ),
                )
            ),
        )

    @property
    def canonical_key(self):
        """Subject, then kind, then citing-clause bytes — then the tiebreaks."""
        return (
            self.subject.encode("utf-8"),
            self.kind.encode("utf-8"),
            encode_fields(*self.citing_clauses),
            self.species.value.encode("utf-8"),
            encode_fields(*(part for pair in self.attributes for part in pair)),
        )

    def canonical_bytes(self):
        return encode_fields(
            self.subject,
            self.kind,
            encode_fields(*self.citing_clauses),
            self.species.value,
            encode_fields(*(part for pair in self.attributes for part in pair)),
            self.eviction_receipt or "",
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Finding:
    """The sole return type of governance appraisal.

    Every finding carries its law head and its position, because §14 requires
    that "every finding retains its position, its defeated clause, its
    verification grain, and its committed law head". The value-specific ground
    lives on the four subclasses below.
    """

    law_head: LawHead
    position: Position

    def _head_bytes(self):
        return encode_fields(
            self.verdict.value,
            self.law_head.canonical_bytes(),
            self.position.canonical_bytes(),
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Affirmed(Finding):
    """The proposition holds over the committed evidence.

    Ground, per §7.1: "the evidence bundle and the clause set under which it
    was appraised". §7.3's payload enumeration omits affirmed entirely, which
    is the fork recorded at this.i @dkypfoo — we take §7.1 at its word, because
    an affirmed finding whose clause set is unknown cannot be checked by
    replay, and checkability is the reason the codomain exists.
    """

    verdict = Verdict.AFFIRMED

    bundle: EvidenceBundle
    clause_set: tuple

    def __post_init__(self):
        if not self.clause_set:
            raise GroundMissing(
                "An affirmed finding must carry the clause set it was appraised "
                "under, and the set was empty. Retrying will not help — an "
                "affirmation nobody can recompute is the judge testifying where "
                "the record should."
            )
        if any(not clause for clause in self.clause_set):
            raise MalformedInput(
                "An affirmed finding carries an empty clause identifier in its "
                "clause set. Retrying will not help — every clause is named by "
                "the committed bytes that carry it."
            )
        object.__setattr__(self, "clause_set", _sorted_unique(self.clause_set))

    def canonical_bytes(self):
        return encode_fields(
            self._head_bytes(),
            self.bundle.canonical_bytes(),
            encode_fields(*self.clause_set),
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Defeated(Finding):
    """The proposition is defeated by committed evidence.

    Ground: the defeater class and the citation, which §7.3 says are "neither
    reconstructible from a bare verdict" and MUST be explicit or uniquely
    re-derivable from a committed referent.
    """

    verdict = Verdict.DEFEATED

    defeat: Defeat

    def canonical_bytes(self):
        return encode_fields(self._head_bytes(), self.defeat.canonical_bytes())


@dataclasses.dataclass(frozen=True, slots=True)
class Pending(Finding):
    """The evidence committed so far neither affirms nor defeats.

    Ground: the typed requirement set, deduplicated and in canonical order, so
    that the cure path is readable off the finding itself.
    """

    verdict = Verdict.PENDING

    requirements: tuple

    def __post_init__(self):
        if not self.requirements:
            raise GroundMissing(
                "A pending finding must name what is missing, and its typed "
                "requirement set was empty. Retrying will not help — a pending "
                "value with no requirement names no cure, and a verifier who "
                "cannot tell 'judged absent' from 'silently dropped' holds no "
                "judgment at all."
            )
        object.__setattr__(
            self,
            "requirements",
            tuple(
                sorted(
                    set(self.requirements),
                    key=lambda element: element.canonical_key,
                )
            ),
        )

    def canonical_bytes(self):
        return encode_fields(
            self._head_bytes(),
            *(element.canonical_bytes() for element in self.requirements),
        )


@dataclasses.dataclass(frozen=True, slots=True)
class SelfConvicted(Finding):
    """The subject's own committed bytes contain a contradiction.

    Ground: "the identifier of the canonical proof package for the
    contradictory pair" (§7.3). §7.1 names the package itself; the ruled span
    names its identifier, and the ruled span governs (this.i @3cmjjo, entry 3).
    """

    verdict = Verdict.SELF_CONVICTED

    proof: str

    def __post_init__(self):
        if not self.proof:
            raise GroundMissing(
                "A self-convicted finding must identify the canonical proof "
                "package for the contradictory pair, and the identifier was "
                "empty. Retrying will not help — self-conviction is conviction "
                "by one's own committed pair, and the pair has to be namable."
            )

    def canonical_bytes(self):
        return encode_fields(self._head_bytes(), self.proof)


@dataclasses.dataclass(frozen=True, slots=True)
class Refusal:
    """The evaluator declining an ill-posed question. **Not** a finding.

    §7.5: "Refusal is not a fifth finding value — it is the evaluator declining
    to answer an ill-posed question, recorded as an operational fact." §1.3
    draws the line it sits on: where committed evidence runs short under a
    committed rule the answer is pending; where no committed rule makes the
    invocation evaluable at all, the evaluator refuses.

    It is deliberately not a subclass of ``Finding`` so that no code path can
    store it where a finding belongs, and it travels by being raised inside
    ``RefusedInvocation`` (this.i @aynhxtdk, entry 23).
    """

    missing: str
    position: Position
    law_head: LawHead | None = None

    def __post_init__(self):
        if not self.missing:
            raise MalformedInput(
                "A refusal must name what is missing — that is the whole "
                "difference between refusing and shrugging. Retrying will not "
                "help; name the committed rule the invocation would need."
            )

    def canonical_bytes(self):
        head = self.law_head.canonical_bytes() if self.law_head is not None else b""
        return encode_fields(self.missing, self.position.canonical_bytes(), head)


@dataclasses.dataclass(frozen=True, slots=True)
class Product:
    """A compound evaluator result: components, each keeping its own ground.

    §7.5: "Compound evaluator results SHALL preserve their component
    propositions and grounds as a product rather than collapse them into a
    fifth scalar shape." So this is not a ``Finding`` and cannot be fed to the
    transition system, which has no edges for it (this.i @ox6mfpi, entry 27).
    """

    components: tuple

    def __post_init__(self):
        if not self.components:
            raise GroundMissing(
                "A compound result must preserve at least one component "
                "proposition with its ground, and none were given. Retrying "
                "will not help — a product of nothing judges nothing."
            )
        if any(not proposition for proposition, _ in self.components):
            raise MalformedInput(
                "A compound result carries an unnamed component proposition. "
                "Retrying will not help — each component keeps its own "
                "proposition, so each proposition has to be named."
            )
        propositions = [proposition for proposition, _ in self.components]
        if len(set(propositions)) != len(propositions):
            raise MalformedInput(
                "A compound result names one proposition twice, so two "
                "findings claim the same question. Retrying will not help — "
                "give each component its own proposition, or compose them into "
                "one."
            )
        object.__setattr__(
            self,
            "components",
            tuple(
                sorted(
                    self.components,
                    key=lambda component: component[0].encode("utf-8"),
                )
            ),
        )

    def canonical_bytes(self):
        return encode_fields(
            *(
                encode_fields(proposition, finding.canonical_bytes())
                for proposition, finding in self.components
            )
        )
