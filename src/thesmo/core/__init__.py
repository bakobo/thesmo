"""The fold. Pure, and kept that way by test.

Custos §1.4 axiom 2: "the inputs are exactly three, closed: the committed
evidence bundle, the committed law head, and the appraisal position. No other
input may influence the result."

That closure is why this package needs no KERI library. Everything below is a
function of committed values handed in by the caller; producing those values
from CESR streams is ``thesmo.substrate``'s job, and the boundary is enforced
mechanically by ``tests/test_core_purity.py`` rather than by convention.

M1 implements the evaluator walls of §7 and no more:

``triple``
    The closed three-input type (§1.4 axiom 2, §7.3 "Inputs").
``finding``
    The four-valued codomain with its required payloads (§7.1, §7.3), and the
    refusal that is deliberately not a fifth value (§7.5).
``ordering``
    The evidence ordering and the canonical selection of defeats (§7.3).
``transitions``
    The transition system: permitted edges, forbidden edges, terminality (§7.3).
``currents``
    The duplicity ladder, the two upward currents, first-seen survival (§7.4).

Everything above the walls — the predicates a domain's law evaluates, the
grammar its events speak — is that domain's choice (§1.4), and thesmo refuses
above them by design (this.i @3b4tjm).

**Read the pinned readings before reading the code.** Custos underdetermines
this fold in twenty-two places that M1 found; each is a `decision` node under
this.i @7h7nazgl and a numbered entry in ``docs/readings-alpha.md``, with the
lawful readings, the specification lines that permit each, and the input on
which two conforming engines diverge. Sixteen of them are divergent. A reader
who takes this code as *the* reading of Custos has taken the one thing it is
built not to be (this.i @tswf4m).
"""

from thesmo.core.currents import (
    LADDER,
    CascadeResult,
    ContestedStanding,
    DuplicityForce,
    Tier,
    annihilate,
    cascade,
    duplicity_force,
    first_seen_survivor,
    taint,
)
from thesmo.core.errors import (
    GroundMissing,
    MalformedInput,
    ThesmoError,
    WallViolation,
)
from thesmo.core.finding import (
    Affirmed,
    Defeated,
    DefeaterClass,
    Finding,
    Pending,
    PendingSpecies,
    Refusal,
    RequirementElement,
    SelfConvicted,
    Verdict,
)
from thesmo.core.ordering import (
    Defeat,
    canonical_requirement_set,
    first_seen,
    permitted_verdict,
    refines,
    select_defeat,
    undischarged,
)
from thesmo.core.transitions import (
    FORBIDDEN_EDGES,
    IDENTITY_EDGES,
    PERMITTED_EDGES,
    Terminality,
    TransitionClass,
    check,
    classify,
    condition_for,
    permitted_successors,
    reason_forbidden,
    terminality,
)
from thesmo.core.triple import (
    AppraisalTriple,
    Coordinate,
    EvidenceBundle,
    EvidenceItem,
    LawHead,
    Position,
)

# The substrate-forbidden list the purity test enforces. Adding a name here is
# a decision that belongs in this.i before the import that motivates it.
FORBIDDEN_IMPORTS = frozenset({"keri", "keria", "cesride", "parside", "hio"})

__all__ = [
    "FORBIDDEN_IMPORTS",
    # errors
    "ThesmoError",
    "MalformedInput",
    "GroundMissing",
    "WallViolation",
    # the closed triple
    "AppraisalTriple",
    "Coordinate",
    "EvidenceBundle",
    "EvidenceItem",
    "LawHead",
    "Position",
    # the codomain
    "Finding",
    "Verdict",
    "Affirmed",
    "Defeated",
    "Pending",
    "SelfConvicted",
    "Refusal",
    "DefeaterClass",
    "PendingSpecies",
    "RequirementElement",
    # the evidence ordering
    "Defeat",
    "canonical_requirement_set",
    "first_seen",
    "permitted_verdict",
    "refines",
    "select_defeat",
    "undischarged",
    # the transition system
    "PERMITTED_EDGES",
    "FORBIDDEN_EDGES",
    "IDENTITY_EDGES",
    "Terminality",
    "TransitionClass",
    "check",
    "classify",
    "condition_for",
    "permitted_successors",
    "reason_forbidden",
    "terminality",
    # the two currents
    "LADDER",
    "CascadeResult",
    "ContestedStanding",
    "DuplicityForce",
    "Tier",
    "annihilate",
    "cascade",
    "duplicity_force",
    "first_seen_survivor",
    "taint",
]
