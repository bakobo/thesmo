"""The evidence ordering and the canonical selection of defeats (Custos 4.1 §7.3).

Two rules share one section and are not the same rule.

**The evidence ordering** is a partial order on *bundles*: "Findings are ordered
by evidence growth: where one committed bundle is a subset of another, appraisal
under the larger bundle refines and never contradicts appraisal under the smaller
— monotonicity is over the subset order on bundles at a fixed law head and
position, never over wall time." The same paragraph carries the affirmation
discipline: "affirmed is reachable only over a bundle that discharges the
question's entire committed requirement space. An evaluator holding a bundle
that leaves any enumerated defeater-check unexamined returns pending with that
check as its typed requirement, never affirmed."

**Canonical selection** is a total order on simultaneously available *defeats*:
"the finding SHALL cite the lexicographic minimum of (defeater-class rank,
citation identifier, subcode)" — followed, four sentences later, by "where the
clause defines none, the subcode is empty and orders last", which no ordinary
lexicographic order does. That contradiction is entry 5 of
``docs/readings-beta.md`` and is pinned at this.i @5pu23u; the resolution lives
in ``Defeat.selection_key`` and this module minimises over it.

A third thing lives here by adjacency, not by shared law: §17's canonical
*consumption* order, re-exported from ``triple`` so that all three orderings are
reachable from one place. §1.4's wall list names "the canonical ordering and
selection of evidence", and neither the imported 4.0 kernel nor 4.1 §7.3
contains an ordering **of evidence** — only an ordering of bundles and a
selection of defeats. See ``docs/readings-beta.md`` §G4.
"""

from .errors import NoDefeatAvailable, RefusedInvocation
from .finding import Affirmed, Pending, Refusal
from .triple import canonical_evidence_order

__all__ = [
    "bundle_refines",
    "canonical_evidence_order",
    "canonical_requirements",
    "discharge",
    "select_defeat",
    "undischarged",
]


def bundle_refines(larger, smaller):
    """Whether appraisal under ``larger`` refines appraisal under ``smaller``.

    True exactly when ``smaller`` ⊆ ``larger``. Bundles that are ⊆-incomparable
    stand in no refinement relation at all, and §7.3's monotonicity obligation
    says nothing about such a pair — which is why entry 7 of the readings
    register cares so much that members are committed items rather than spans.
    """
    return smaller.items <= larger.items


def select_defeat(defeats):
    """Cite the canonical minimum among simultaneously available defeats.

    "Two verifiers holding the same bundle SHALL emit the same defeated finding
    down to the byte" — so this is total, presentation-order-independent, and
    derived entirely from committed bytes.
    """
    candidates = tuple(defeats)
    if not candidates:
        raise NoDefeatAvailable(
            "Canonical selection was asked to choose a defeat with none "
            "available, so there is nothing to cite. Retrying will not help — "
            "a question with no available defeat is affirmed or pending, and "
            "the caller should not have reached selection."
        )
    return min(candidates, key=lambda defeat: defeat.selection_key)


def canonical_requirements(elements):
    """Deduplicate and order a typed requirement set (§7.3).

    Canonical order is subject, then kind, then citing-clause bytes, then the
    species and committed attributes as tiebreaks — because the species is a
    mandatory field the document's stated sort key omits (this.i @blq6dwxz).
    """
    return tuple(sorted(set(elements), key=lambda element: element.canonical_key))


def undischarged(space, discharged):
    """The enumerated defeater-checks the bundle has not yet discharged.

    "Defeating evidence is ex-ante enumerable: everything that could defeat a
    question is in that question's committed requirement space before appraisal
    begins, which is what makes defeat a citation rather than a surprise."
    """
    settled = set(discharged)
    return canonical_requirements(
        element for element in space if element not in settled
    )


def discharge(*, space, discharged, law_head, position, bundle, clause_set):
    """Appraise a question's requirement space into affirmed or pending.

    An **underivable** space is not an empty one. Where the committed law does
    not enumerate the question's requirement space at all, the question is not
    evaluable — a missing rule rather than missing evidence — and the evaluator
    refuses rather than affirming into the silence (this.i @nup3m6, entry 25).
    Pass ``space=None`` for that case; an empty tuple means the law enumerated a
    space and it is empty, which discharges vacuously.
    """
    if space is None:
        raise RefusedInvocation(
            Refusal(
                missing=(
                    "the committed law enumerates no requirement space for this "
                    "question, so no committed rule makes it evaluable"
                ),
                position=position,
                law_head=law_head,
            )
        )
    still_open = undischarged(space, discharged)
    if still_open:
        return Pending(law_head, position, requirements=still_open)
    return Affirmed(law_head, position, bundle=bundle, clause_set=clause_set)
