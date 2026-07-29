"""The complete transition system among the four finding values. Custos §7.3.

The section's own claim:

    The finding type is a state machine, and this section is its complete
    enumeration — states, payloads, permitted transitions with conditions,
    forbidden transitions, and terminality.

Both halves of that sentence needed a pinned reading before this module could
exist.

**"Complete enumeration" is twelve of sixteen** (this.i @fxn65z). Four values
admit sixteen ordered pairs; §7.3 rules five permitted and seven forbidden. The
four identity pairs are in neither table. Reading "unenumerated therefore
forbidden" would forbid an engine's own idempotent recomputation, which the same
section's monotonicity paragraph requires in the ordinary case — so identity is
permitted, named here as its own class so the gap stays visible rather than
being quietly absorbed into "permitted".

**"State machine" is a relation, not a machine** (this.i @na3tebqk). §7.3, twelve
lines below that phrase: "A finding is a function of exactly three inputs [...]
No other input — wall clocks, **local state**, operator discretion, ambient
configuration — may influence a finding." Retained per-question finding state is
local state. So nothing here advances anything: ``check`` is a validity relation
over two independently computed findings for one question, under a growing
bundle at a fixed law head and position, and a forbidden pair raises rather than
coercing a value into legality.

The conditions and reasons below are the document's own words, kept verbatim so
that a reader of a raised ``WallViolation`` is reading §7.3 rather than reading
this repo's paraphrase of it.
"""

from enum import Enum

from thesmo.core.errors import MalformedInput, WallViolation, require
from thesmo.core.finding import Finding, Verdict


class TransitionClass(Enum):
    """What §7.3 says about an ordered pair of values.

    ``IDENTITY`` is this repo's, not the document's: it names the four pairs the
    document's "complete enumeration" does not reach.
    """

    IDENTITY = "identity"
    PERMITTED = "permitted"
    FORBIDDEN = "forbidden"


class Terminality(Enum):
    """§7.3's terminality paragraph, as three named positions."""

    NON_TERMINAL = "the non-terminal bottom"
    FINAL_EXCEPT_SELF_CONVICTION = (
        "final except for one event: the arrival of a contradictory pair bearing "
        "on the same question"
    )
    TERMINAL = "terminal for its question; no further evidence rehabilitates it"


#: §7.3's permitted table. "Five edges, each conditioned on evidence growth."
PERMITTED_EDGES = {
    (Verdict.PENDING, Verdict.AFFIRMED): "the requirement set discharges affirmatively",
    (Verdict.PENDING, Verdict.DEFEATED): "the requirement set discharges by defeat",
    (Verdict.PENDING, Verdict.SELF_CONVICTED): (
        "a bearing contradictory pair, or new governed-status evidence (committed "
        "evidence newly bearing on the subject's status under the governance tier's "
        "committed predicates), enters the bundle — and per this.i @plnfze the "
        "second disjunct names where the pair comes from at the governance tier, "
        "never a route to self-conviction with no pair at all"
    ),
    (Verdict.AFFIRMED, Verdict.SELF_CONVICTED): (
        "a contradictory pair bearing on the question enters the bundle"
    ),
    (Verdict.DEFEATED, Verdict.SELF_CONVICTED): (
        "a contradictory pair bearing on the question enters the bundle"
    ),
}

#: §7.3's forbidden table. "Seven edges, absolute."
FORBIDDEN_EDGES = {
    (Verdict.AFFIRMED, Verdict.DEFEATED): (
        "settled findings do not flip; new defeat evidence yields a new finding at "
        "a new position"
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

#: The four pairs §7.3's "complete enumeration" does not reach (this.i @fxn65z).
IDENTITY_EDGES = frozenset((verdict, verdict) for verdict in Verdict)

_TERMINALITY = {
    Verdict.PENDING: Terminality.NON_TERMINAL,
    Verdict.AFFIRMED: Terminality.FINAL_EXCEPT_SELF_CONVICTION,
    Verdict.DEFEATED: Terminality.FINAL_EXCEPT_SELF_CONVICTION,
    Verdict.SELF_CONVICTED: Terminality.TERMINAL,
}


def terminality(verdict):
    """Where §7.3 places this value: bottom, final-but-one, or terminal."""
    return _TERMINALITY[verdict]


def classify(before, after):
    """The class of the ordered pair ``(before, after)``.

    Total over all sixteen pairs, which is more than the document manages.
    """
    if (before, after) in IDENTITY_EDGES:
        return TransitionClass.IDENTITY
    if (before, after) in PERMITTED_EDGES:
        return TransitionClass.PERMITTED
    return TransitionClass.FORBIDDEN


def condition_for(before, after):
    """§7.3's stated condition for a permitted edge."""
    require(
        (before, after) in PERMITTED_EDGES,
        MalformedInput,
        f"{before.value} -> {after.value} is not a permitted edge of §7.3's "
        "transition system, so it has no stated condition. Permitted edges are "
        f"{sorted((a.value, b.value) for a, b in PERMITTED_EDGES)}.",
    )
    return PERMITTED_EDGES[(before, after)]


def reason_forbidden(before, after):
    """§7.3's stated reason for a forbidden edge."""
    require(
        (before, after) in FORBIDDEN_EDGES,
        MalformedInput,
        f"{before.value} -> {after.value} is not one of §7.3's seven forbidden "
        "edges, so the document states no reason for refusing it.",
    )
    return FORBIDDEN_EDGES[(before, after)]


def permitted_successors(verdict):
    """The values evidence growth may lawfully carry ``verdict`` to.

    Identity is excluded: a value that did not change did not transition.
    """
    return tuple(
        after for before, after in PERMITTED_EDGES if before is verdict
    )


def check(before, after):
    """Check a recomputation of one question against §7.3, and return its class.

    ``before`` and ``after`` are two findings for the same question, computed
    over triples related by evidence growth at a fixed law head and position.
    Nothing is mutated: a forbidden pair raises ``WallViolation`` carrying the
    document's own reason, because §15 makes "no backward edge exists in the
    transition system" a wall, and a wall that silently corrects its input is
    not a wall.
    """
    for value, name in ((before, "before"), (after, "after")):
        require(
            isinstance(value, Finding),
            MalformedInput,
            f"the {name} argument must be a finding; got {value!r}. §7.3's "
            "transition system ranges over the four values of the codomain and "
            "over nothing else.",
        )
    require(
        before.question == after.question,
        MalformedInput,
        f"a transition is about one question; got {before.question!r} then "
        f"{after.question!r}. §7.3's terminality is stated per question, and two "
        "questions have two independent transition systems.",
    )
    require(
        before.triple.grows_to(after.triple),
        MalformedInput,
        "a transition is over evidence growth at a fixed law head and position "
        "(§7.3: 'monotonicity is over the subset order on bundles at a fixed law "
        "head and position, never over wall time'). The two findings offered are "
        "not related that way, so §7.3's tables say nothing about the pair.",
    )
    outcome = classify(before.verdict, after.verdict)
    require(
        outcome is not TransitionClass.FORBIDDEN,
        WallViolation,
        f"{before.verdict.value} -> {after.verdict.value} is forbidden by §7.3: "
        f"{FORBIDDEN_EDGES.get((before.verdict, after.verdict), 'no backward edge exists')}. "
        "This is one of §15's six walls, so the fold refuses the pair rather than "
        "coercing either finding into legality.",
    )
    return outcome
