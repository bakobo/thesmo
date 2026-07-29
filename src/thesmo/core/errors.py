"""What the fold raises, and the one thing it does not.

Three failures are possible inside a pure fold, and they are different in kind:

``MalformedInput``
    The caller handed us something that is not a member of the type it claims to
    be. Fail closed — Custos calls untrusted input evidence only once it is
    committed, and an input we cannot check carries no authority.

``GroundMissing``
    A finding was constructed without the ground its value requires. Custos
    §1.4 axiom 1: "A finding carries its ground — citation, requirement, or
    proof — or it is not a finding. The codomain admits no bare verdicts." So
    this is a typing failure, not a validation nicety.

``WallViolation``
    A caller asked the fold to do something one of §15's six walls forbids: emit
    a forbidden transition, or annihilate a finding that the affirmation
    discipline says could never have existed. We refuse rather than comply,
    because the walls are what conformance means.

Refusal is deliberately **not** here. Custos §7.5 says the evaluator's refusal
of an ill-posed question is "recorded as an operational fact", and you cannot
record what you threw away — so a refusal is a value (``finding.Refusal``), not
an exception (this.i @iezwqh).
"""


class ThesmoError(Exception):
    """Base for every error the fold raises.

    Carries a stable symbolic code, so callers branch on the code rather than on
    message text, and says whether retrying could possibly help.
    """

    code = "CORE-ERROR"
    retryable = False


class MalformedInput(ThesmoError):
    """A value handed to the fold is not a member of the type it must be.

    Permanent: the same bytes will fail the same way forever. Presenting
    different bytes is a different invocation, not a retry.
    """

    code = "CORE-MALFORMED-INPUT"
    retryable = False


class GroundMissing(ThesmoError):
    """A finding was offered without the ground its value must carry.

    Permanent: the ground is a component of the finding's type, so a value
    without it never becomes a member by waiting.
    """

    code = "CORE-GROUND-MISSING"
    retryable = False


class WallViolation(ThesmoError):
    """The fold was asked to cross one of the fixed walls of Custos §15.

    Permanent: a wall does not open on a second attempt. If the input is
    genuinely lawful, the defect is in whatever computed it, and that is where
    the repair belongs.
    """

    code = "CORE-WALL-VIOLATION"
    retryable = False


def require(condition, error, message):
    """Raise ``error(message)`` unless ``condition`` holds.

    A named guard rather than a bare ``if``: every wall in this package is
    checked in exactly one shape, and the shape is greppable.
    """
    if not condition:
        raise error(message)
