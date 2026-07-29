"""What the fold raises, and why each kind is told apart from the others.

Every error here carries a stable symbolic ``code`` and states its permanence,
per the Bakobo error-handling standard. The fold is pure and deterministic, so
every failure in this package is **permanent** by nature: the same arguments
will fail the same way forever, and no message here invites a pointless retry.

The hierarchy is deliberately narrow. Four kinds matter to a caller:

- the input was not well formed (``MalformedInput``);
- a value was offered without the ground its type requires (``GroundMissing``);
- an order was asked for that no committed bytes supply (``UncommittedOrder``);
- the evaluator declined an ill-posed question (``RefusedInvocation``).

The transition and cascade errors below are refinements of the first two, kept
separate because a caller reacting to a forbidden edge does something different
from a caller reacting to a malformed payload.
"""


class ThesmoError(Exception):
    """Base for every error the fold raises.

    ``code`` is stable across rewordings, so callers branch on the kind rather
    than on prose; ``permanent`` says whether retrying could help, and in this
    package it never can.
    """

    code = "THESMO_ERROR"
    permanent = True


class MalformedInput(ThesmoError):
    """A value's shape is wrong before any Custos rule is consulted."""

    code = "THESMO_MALFORMED_INPUT"


class GroundMissing(ThesmoError):
    """A finding was offered without the ground its value requires.

    Custos 4.1 §7.1 applies the Ground Axiom as a typing rule: a value that
    does not carry its ground "is not a member of this type, whatever else it
    may be". This error is that sentence, enforced at construction.
    """

    code = "THESMO_GROUND_MISSING"


class UncommittedOrder(ThesmoError):
    """An order was required that no committed bytes derive.

    Custos 4.1 §1.4 axiom 4: any order the fold consumes is derivable from
    committed bytes or proven irrelevant. Inventing one is legislating, which
    §7.5 forbids the evaluator to do.
    """

    code = "THESMO_UNCOMMITTED_ORDER"


class ForbiddenTransition(ThesmoError):
    """An edge the transition system enumerates as forbidden was attempted."""

    code = "THESMO_FORBIDDEN_TRANSITION"


class ConditionUnmet(ThesmoError):
    """A permitted edge was attempted without the evidence growth it conditions on."""

    code = "THESMO_TRANSITION_CONDITION_UNMET"


class CurrentsMerged(ThesmoError):
    """The defeat current and the duplicity current were run into each other.

    Custos 4.1 §7.4: "a conforming evaluator SHALL NOT merge them". Breach and
    duplicity are distinct crimes at every tier, so the engine refuses to treat
    one as the other rather than doing something plausible.
    """

    code = "THESMO_CURRENTS_MERGED"


class NoDefeatAvailable(ThesmoError):
    """Canonical selection was asked to choose among no defeats at all."""

    code = "THESMO_NO_DEFEAT_AVAILABLE"


class RefusedInvocation(ThesmoError):
    """The evaluator declined an ill-posed question.

    Custos 4.1 §7.5: refusal "is not a fifth finding value — it is the
    evaluator declining to answer an ill-posed question, recorded as an
    operational fact". It travels as a raised error rather than a returned
    value so that it can never be stored where a finding belongs (this.i
    @aynhxtdk). The ``refusal`` attribute carries the record itself.
    """

    code = "THESMO_REFUSED_INVOCATION"

    def __init__(self, refusal):
        self.refusal = refusal
        super().__init__(
            f"The evaluator refused this invocation because committed law runs "
            f"out: {refusal.missing}. This is a missing rule, not missing "
            f"evidence, so re-presenting the same evidence will not help — the "
            f"rule has to be enacted and committed first."
        )
