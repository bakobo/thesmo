"""The complete transition system (Custos 4.1 §7.3).

The governing rule is ratified verbatim: "The finding type SHALL enumerate its
constructors, required payloads, permitted transitions with their conditions,
forbidden transitions, and terminality."

So the enumeration lives here as data — five permitted edges with their
conditions, seven forbidden edges with their reasons — rather than as control
flow, because a wall stated as an ``if`` chain cannot be inspected and a wall
stated as a table can. ``tests/test_transitions.py`` takes the census: five
plus seven is twelve, which is every ordered pair of *distinct* values, so the
enumeration that calls itself complete contains no self-edge at all.

Two readings are pinned here:

- **Self-edges are lawful** (this.i @iouhhq, entry 14). A finding whose value is
  unchanged under a grown bundle has not transitioned, so it lies outside the
  enumeration's subject. The alternative — unenumerated means forbidden — makes
  ``pending → pending`` unlawful, and pending is the state one waits in.
- **Every edge into self-convicted requires a bearing contradictory pair**
  (this.i @mwprhoj3, entry 15). §7.3's ``pending → self-convicted`` row adds
  "or new governed-status evidence"; read as an independent sufficient
  condition it would emit a self-conviction whose required payload — "the
  identifier of the canonical proof package for the contradictory pair" — names
  a pair that need not exist.
"""

import dataclasses
import enum

from .errors import ConditionUnmet, ForbiddenTransition, MalformedInput
from .finding import Verdict
from .ordering import bundle_refines

__all__ = [
    "FORBIDDEN",
    "PERMITTED",
    "Discharge",
    "Growth",
    "admits_no_further_evidence",
    "check_refinement",
    "check_transition",
    "is_terminal",
    "permits",
]


class Discharge(enum.StrEnum):
    """How a pending finding's requirement set discharged, if it did."""

    NONE = "none"
    AFFIRMATIVE = "affirmative"
    DEFEAT = "defeat"


@dataclasses.dataclass(frozen=True, slots=True)
class Growth:
    """What entered the bundle between two appraisals.

    §7.3: the five permitted edges are "each conditioned on evidence growth".
    ``governed_status_evidence`` is carried because §7.3's ``pending →
    self-convicted`` row names it, and refused as a sufficient condition on its
    own — see this.i @mwprhoj3.
    """

    discharge: Discharge = Discharge.NONE
    bearing_pair: bool = False
    governed_status_evidence: bool = False


PERMITTED = {
    (Verdict.PENDING, Verdict.AFFIRMED): (
        "the requirement set discharges affirmatively"
    ),
    (Verdict.PENDING, Verdict.DEFEATED): "the requirement set discharges by defeat",
    (Verdict.PENDING, Verdict.SELF_CONVICTED): (
        "a bearing contradictory pair, or new governed-status evidence "
        "(committed evidence newly bearing on the subject's status under the "
        "governance tier's committed predicates), enters the bundle"
    ),
    (Verdict.AFFIRMED, Verdict.SELF_CONVICTED): (
        "a contradictory pair bearing on the question enters the bundle"
    ),
    (Verdict.DEFEATED, Verdict.SELF_CONVICTED): (
        "a contradictory pair bearing on the question enters the bundle"
    ),
}

FORBIDDEN = {
    (Verdict.AFFIRMED, Verdict.DEFEATED): (
        "settled findings do not flip; new defeat evidence yields a new finding "
        "at a new position"
    ),
    (Verdict.DEFEATED, Verdict.AFFIRMED): (
        "defeat is not un-cited; rehabilitation is an act, not a transition"
    ),
    (Verdict.AFFIRMED, Verdict.PENDING): "evidence does not un-arrive",
    (Verdict.DEFEATED, Verdict.PENDING): "evidence does not un-arrive",
    (Verdict.SELF_CONVICTED, Verdict.PENDING): "a poisoned question does not reopen",
    (Verdict.SELF_CONVICTED, Verdict.AFFIRMED): (
        "self-conviction is terminal for its question"
    ),
    (Verdict.SELF_CONVICTED, Verdict.DEFEATED): (
        "self-conviction is terminal for its question"
    ),
}


def permits(frm, to):
    """Whether the enumeration allows this edge at all, conditions aside."""
    return frm == to or (frm, to) in PERMITTED


def is_terminal(verdict):
    """Whether a finding of this value may ground recourse (§7.3, §13.1).

    "Affirmed and defeated are final except for one event ... Pending is the
    non-terminal bottom." §13.1 then binds on the word: "Recourse SHALL be
    grounded only on terminal findings."
    """
    return verdict is not Verdict.PENDING


def admits_no_further_evidence(verdict):
    """Whether the question is closed against every further arrival.

    Only self-conviction is: "the question is poisoned, and no further evidence
    rehabilitates it". Affirmed and defeated are final *except* for the arrival
    of a bearing contradictory pair, so they are terminal without being closed.
    """
    return verdict is Verdict.SELF_CONVICTED


def check_transition(frm, to, growth):
    """Admit an edge, or say exactly why it is refused.

    Returns ``None`` on success; raises ``ForbiddenTransition`` for an
    enumerated forbidden edge and ``ConditionUnmet`` for a permitted edge whose
    evidence growth did not occur.
    """
    if frm == to:
        return
    if (frm, to) in FORBIDDEN:
        raise ForbiddenTransition(
            f"A finding cannot move from {frm.value} to {to.value}: "
            f"{FORBIDDEN[(frm, to)]}. Retrying will not help — no backward edge "
            f"exists anywhere in the system, and findings move only in the "
            f"direction of evidence growth."
        )
    condition = PERMITTED[(frm, to)]
    if to is Verdict.SELF_CONVICTED:
        if not growth.bearing_pair:
            raise ConditionUnmet(
                f"A finding cannot move from {frm.value} to self-convicted "
                f"without a contradictory pair bearing on the question, and "
                f"none entered the bundle. Retrying will not help — the "
                f"condition is: {condition}. Self-conviction is conviction by "
                f"one's own committed pair, and its required payload names that "
                f"pair's proof package."
            )
    elif to is Verdict.AFFIRMED:
        if growth.discharge is not Discharge.AFFIRMATIVE:
            raise ConditionUnmet(
                f"A pending finding cannot affirm until {condition}, and the "
                f"discharge offered was {growth.discharge.value}. Retrying will "
                f"not help — a bundle that leaves any enumerated defeater-check "
                f"unexamined returns pending, never affirmed."
            )
    elif growth.discharge is not Discharge.DEFEAT:
        raise ConditionUnmet(
            f"A pending finding cannot be defeated until {condition}, and the "
            f"discharge offered was {growth.discharge.value}. Retrying will not "
            f"help — defeat is a citation rather than a surprise, so the "
            f"defeating evidence has to be in the bundle."
        )


def check_refinement(earlier, later, *, earlier_bundle, later_bundle, growth):
    """Admit one finding as a lawful refinement of another (§7.3).

    "Findings are ordered by evidence growth: where one committed bundle is a
    subset of another, appraisal under the larger bundle refines and never
    contradicts appraisal under the smaller — monotonicity is over the subset
    order on bundles at a fixed law head and position, never over wall time."

    All three conditions of that sentence are checked: fixed law head, fixed
    position, and a bundle that grew.
    """
    if earlier.law_head != later.law_head:
        raise MalformedInput(
            f"Monotonicity is measured at a fixed law head, but these findings "
            f"cite {earlier.law_head.said!r} and {later.law_head.said!r}. "
            f"Retrying will not help — two appraisals under different law are "
            f"two judgments, not one judgment refined."
        )
    if earlier.position != later.position:
        raise MalformedInput(
            f"Monotonicity is measured at a fixed position, but these findings "
            f"speak at {earlier.position.sn} and {later.position.sn} of "
            f"{earlier.position.identifier!r} and {later.position.identifier!r}. "
            f"Retrying will not help — a finding at a new position is a new "
            f"finding, which is exactly how settled findings avoid flipping."
        )
    if not bundle_refines(later_bundle, earlier_bundle):
        raise ForbiddenTransition(
            "The later appraisal's bundle does not contain the earlier one's, "
            "so evidence would have to un-arrive for this refinement to hold. "
            "Retrying will not help — the evidence ordering runs over the "
            "subset order on bundles, in one direction only."
        )
    check_transition(earlier.verdict, later.verdict, growth)
