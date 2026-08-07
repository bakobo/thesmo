"""The evidence ordering, and the canonical selection of defeats. Custos §7.3.

Two paragraphs of §7.3 are implemented here, and both are quoted rather than
paraphrased, because both had to be read a word at a time.

**The evidence ordering.**

    Findings are ordered by evidence growth: where one committed bundle is a
    subset of another, appraisal under the larger bundle refines and never
    contradicts appraisal under the smaller — monotonicity is over the subset
    order on bundles at a fixed law head and position, never over wall time.
    [...] The ordering forces a discipline on affirmation, stated here so no
    reader must derive it: affirmed is reachable only over a bundle that
    discharges the question's entire committed requirement space. An evaluator
    holding a bundle that leaves any enumerated defeater-check unexamined
    returns pending with that check as its typed requirement, never affirmed
    [...]

**Canonical selection.**

    Where multiple defeats are simultaneously available for one question, the
    finding SHALL cite the lexicographic minimum of (defeater-class rank,
    citation identifier, subcode). [...] The subcode is the defeat's
    discriminator within its citation, assigned by the cited clause's own
    committed enumeration; where the clause defines none, the subcode is empty
    and orders last.

The last clause of that quotation contradicts its first: under any lexicographic
order the empty string is the *minimum*, because it prefixes every string. We
pin "orders last" — the specific over the general — and record the divergence
as R7 / this.i @kjqxel. It is the sharpest fork in the register: two engines
select different citations from one bundle, and §13.1 recourse rests on the
citation.

The affirmation discipline is pinned literally at @xr3rp7: it names `affirmed`
and only `affirmed`, so defeat short-circuits an undischarged requirement space.
`test_the_pinned_reading_makes_a_defeated_citation_non_monotone` is the
executable form of what that costs — the same paragraph's monotonicity promise
fails, and no forbidden edge catches it.
"""

from dataclasses import dataclass

from thesmo.core.errors import MalformedInput, require
from thesmo.core.finding import (
    DefeaterClass,
    Defeated,
    PendingSpecies,
    RequirementElement,
    Verdict,
)
from thesmo.core.triple import EvidenceItem


def refines(smaller, larger):
    """True where appraisal under ``larger`` refines appraisal under ``smaller``.

    §7.3's monotonicity is "over the subset order on bundles", so this is the
    subset relation and nothing more — in particular it is not a total order,
    and two disjoint bundles refine neither way.
    """
    return smaller <= larger


def first_seen(items):
    """The item that survives a duplicitous pair: the first in committed order.

    §7.4's tainting current says "first-seen survives". Read observationally,
    that would let two verifiers who fetched a pair in opposite orders keep
    different survivors — which §1.4 axiom 4 forbids, §12.1 disclaims
    ("discovery order is observer-relative and consulted by nothing"), and
    §17's order vectors test for. So "first-seen" is positional (this.i
    @r5p4h2).
    """
    ordered = sorted(items, key=EvidenceItem.order_key)
    require(
        ordered != [],
        MalformedInput,
        "first-seen survival needs at least one committed item; an empty "
        "collection has no first. §7.4's current runs over a contradictory "
        "pair, and a pair is two.",
    )
    return ordered[0]


def canonical_requirement_set(elements):
    """§7.3's typed requirement set: deduplicated, in canonical order.

    Deduplication is on the canonical sort key exactly — deduplicating on the
    whole element would let two elements share a key, which makes the "canonical
    order" a preorder and the finding's bytes undetermined (this.i @kdrqzc).
    That leaves the species of the survivor unstated by the standard; we take
    the earliest in §7.2's declaration order, a committed order under §1.4 axiom
    4, and record the invention rather than hiding it.
    """
    merged = {}
    for element in elements:
        require(
            isinstance(element, RequirementElement),
            MalformedInput,
            f"a typed requirement set holds RequirementElements; got {element!r}.",
        )
        seen = merged.get(element.dedup_key())
        if seen is None or element.species.rank < seen.species.rank:
            merged[element.dedup_key()] = element
    require(
        merged != {},
        MalformedInput,
        "a typed requirement set must name at least one element. §7.1 makes the "
        "requirement set pending's ground, and a set naming nothing missing "
        "names no cure path either.",
    )
    return tuple(sorted(merged.values(), key=RequirementElement.sort_key))


@dataclass(frozen=True, slots=True)
class Defeat:
    """One of possibly several defeats simultaneously available for a question.

    The candidate that canonical selection ranges over. It is deliberately not a
    finding: a finding is what the fold returns after selection, and holding the
    two apart is what keeps "multiple defeats are simultaneously available" a
    statement about evidence rather than about verdicts.
    """

    defeater_class: DefeaterClass
    citation: str
    subcode: str = ""

    def __post_init__(self):
        require(
            isinstance(self.defeater_class, DefeaterClass),
            MalformedInput,
            f"a defeat's class must be one of §7.3's four; got "
            f"{self.defeater_class!r}. The class is the first component of the "
            "selection key, so an unranked class cannot be selected among.",
        )
        require(
            isinstance(self.citation, str) and self.citation != "",
            MalformedInput,
            f"a defeat must cite the violated or superseding clause, or the failed "
            f"verification subject; got {self.citation!r}.",
        )
        require(
            isinstance(self.subcode, str),
            MalformedInput,
            f"a subcode must be a string, empty where the cited clause defines no "
            f"enumeration; got {self.subcode!r}.",
        )

    @classmethod
    def of(cls, finding):
        """The defeat a defeated finding cites."""
        return cls(finding.defeater_class, finding.citation, finding.subcode)

    def as_finding(self, question, triple):
        """This defeat as the fold's finding over ``question`` at ``triple``."""
        return Defeated(
            question=question,
            triple=triple,
            defeater_class=self.defeater_class,
            citation=self.citation,
            subcode=self.subcode,
        )


def defeat_sort_key(defeat):
    """§7.3's selection key: (defeater-class rank, citation identifier, subcode).

    With one departure the section itself demands: the third component is
    preceded by a flag that sends an *empty* subcode last rather than first.
    "Lexicographic minimum" would put the empty string first — it prefixes
    every string — and the section's own final clause says it "orders last"
    (this.i @kjqxel).
    """
    return (
        defeat.defeater_class.rank,
        defeat.citation.encode("utf-8"),
        defeat.subcode == "",
        defeat.subcode.encode("utf-8"),
    )


def select_defeat(defeats):
    """The one defeat the finding cites, out of those simultaneously available.

    §7.3: "Two verifiers holding the same bundle SHALL emit the same defeated
    finding down to the byte." That obligation is discharged here or nowhere.
    """
    candidates = list(defeats)
    require(
        candidates != [],
        MalformedInput,
        "canonical selection needs at least one available defeat. There is no "
        "minimum of an empty set, and inventing one would cite a defeat no "
        "committed evidence supports.",
    )
    return min(candidates, key=defeat_sort_key)


def undischarged(requirement_space, examined):
    """The enumerated checks of the question's requirement space still unexamined.

    §7.3: "Defeating evidence is ex-ante enumerable: everything that could
    defeat a question is in that question's committed requirement space before
    appraisal begins, which is what makes defeat a citation rather than a
    surprise." So the space is knowable before the bundle is read, and what is
    left of it after reading is what a pending finding must name.
    """
    return tuple(sorted(set(requirement_space) - set(examined)))


def permitted_verdict(available_defeats, unexamined_checks):
    """What the evidence ordering permits, given the defeats and what is unread.

    Not what the fold *answers* — that needs the committed law. This is only the
    §7.3 discipline: what the ordering alone rules in and out.

    - any defeat available -> defeated. The affirmation discipline names
      `affirmed`, twice, and does not name defeated; reading a restriction into
      a ruled span it does not carry would be legislating (this.i @xr3rp7).
    - otherwise, anything unexamined -> pending, naming those checks.
    - otherwise -> affirmed.

    Self-conviction is unreachable from here by construction: it needs a bearing
    contradictory pair, which is the subject of ``currents``.
    """
    if available_defeats:
        return Verdict.DEFEATED
    if unexamined_checks:
        return Verdict.PENDING
    return Verdict.AFFIRMED


#: §7.2's species, ordered as the amendment declares them. Re-exported so a
#: caller building requirement elements never has to reach past this module for
#: the merge order that ``canonical_requirement_set`` uses.
SPECIES_ORDER = tuple(PendingSpecies)
