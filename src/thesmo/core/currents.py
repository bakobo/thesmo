"""The duplicity ladder and the two upward currents (Custos 4.1 §7.4).

"Duplicity is one crime with a rising voice unit. At the key tier, it is two
events at one coordinate of one KEL. At the registry tier, it is two registries
where committed law demands one chain ... At the governance tier, it is
contradictory enactments under one committed predicate."

"Findings cascade between tiers in two distinct currents, and a conforming
evaluator SHALL NOT merge them":

- **Defeat annihilates upward.** A lower-tier defeat voids what was built on
  it, and "the dependents were never valid; annihilation is discovery, not
  change."
- **Duplicity taints upward.** A lower-tier self-conviction "does not un-happen
  the history above it: committed history is monotonic, first-seen survives,
  and what was affirmed above converts to contested standing rather than to
  nothing."

Three readings are pinned here, and they are the ones most likely to be wrong.

1. **First-seen means first in the committed canonical order** (this.i @sr546w,
   ``docs/readings-beta.md`` entry 17). Read the substrate's way — first
   *observed* — the phrase makes the fold's result depend on arrival order,
   which axiom 4 forbids by name and §17 says "does not conform". One of §1.4's
   five imported walls then contradicts one of §1.4's five stated axioms.
2. **Contested standing is not a finding value** (this.i @6mntbxri, entry 18).
   §15 fixes the return type at "the four-valued finding codomain and nothing
   else", so the taint is a record beside the record, and the affirmed finding
   it contests survives with its bytes untouched.
3. **Annihilation emits a new finding at a new position, inheriting the
   lower-tier defeat's class and citation** (this.i @nggcv5f, entry 19).
   Mutating the dependent would traverse the forbidden ``affirmed → defeated``
   edge; deleting it would have the fold write, and a fold "writes nothing,
   ever".
"""

import dataclasses
import enum

from .errors import CurrentsMerged, GroundMissing, MalformedInput
from .finding import Defeated, Finding, SelfConvicted
from .triple import encode_fields

__all__ = [
    "VOICE_UNIT",
    "ContestedStanding",
    "ContradictoryPair",
    "Dependent",
    "Tier",
    "annihilate_upward",
    "convict",
    "first_seen",
    "is_visible_at",
    "may_convict",
    "taint_upward",
]


class Tier(enum.IntEnum):
    """The three rungs of the fold tower, in the amendment's own labelling.

    §7.3's gloss: "T3, in the amendment's tier labeling, is the governance tier
    — the third rung of the ladder of section 7.4, as T1 is the key tier and T2
    the registry tier."
    """

    KEY = 1
    REGISTRY = 2
    GOVERNANCE = 3


VOICE_UNIT = {
    Tier.KEY: "two events at one coordinate of one KEL",
    Tier.REGISTRY: "two registries where committed law demands one chain",
    Tier.GOVERNANCE: "contradictory enactments under one committed predicate",
}


def is_visible_at(pair_tier, machinery_tier):
    """Whether a tier's duplicity is visible to a given tier's machinery.

    "Each tier's duplicity is structurally invisible to the machinery of the
    tier below, which is why the tower has three rungs and not one."
    """
    return machinery_tier >= pair_tier


@dataclasses.dataclass(frozen=True, slots=True)
class ContradictoryPair:
    """Two voices where the constitution of a tier demands one.

    ``bears_on`` carries the questions this pair bears on as a **committed
    determination the fold consumes**, never one it computes: §7.3 makes
    conviction turn on bearing and neither edition defines the relation, so an
    evaluator that decided it would be legislating (this.i @pbrejw2, entry 21).
    A pair that bears on nothing still taints its subject's standing; it just
    converts no question's finding.

    ``predicate`` is the committed predicate the pair violates. §7.4 makes it
    required below the key tier — registry-tier and governance-tier duplicity
    "convict only within frames that committed the violated predicate" — and
    meaningless at the key tier, which "convicts in the medium, for every
    verifier, under no frame's law".
    """

    subject: str
    tier: Tier
    first: object
    second: object
    bears_on: tuple = ()
    predicate: str | None = None
    proof: str = ""

    def __post_init__(self):
        if not self.subject:
            raise MalformedInput(
                "A contradictory pair must name the subject whose own committed "
                "bytes contradict each other, and the subject was empty. "
                "Retrying will not help — self-conviction is conviction by one's "
                "own pair, so the owner of the voice has to be named."
            )
        if self.first == self.second:
            raise MalformedInput(
                "A contradictory pair needs two distinct committed voices, and "
                "the same evidence item was given twice. Retrying will not help "
                "— one voice contradicts nothing."
            )
        if not self.proof:
            raise GroundMissing(
                f"The contradictory pair for {self.subject!r} carries no "
                f"canonical proof package identifier, so no self-convicted "
                f"finding could name its ground. Retrying will not help — "
                f"commit the proof package and cite it."
            )
        if self.tier is Tier.KEY and self.predicate is not None:
            raise MalformedInput(
                "A key-tier pair was given a violated predicate, but key-tier "
                "duplicity convicts in the medium, for every verifier, under no "
                "frame's law. Retrying will not help — drop the predicate, or "
                "raise the pair to the registry or governance tier."
            )
        if self.tier is not Tier.KEY and self.predicate is None:
            raise MalformedInput(
                f"A {self.tier.name.lower()}-tier pair must name the committed "
                f"predicate it violates, because duplicity above the key tier is "
                f"law-relative and convicts only inside frames that committed "
                f"that predicate. Retrying will not help — name the predicate."
            )
        object.__setattr__(
            self,
            "bears_on",
            tuple(sorted(set(self.bears_on), key=lambda q: q.encode("utf-8"))),
        )

    def bears_on_question(self, question):
        """Whether this pair bears on the question being appraised."""
        return question in self.bears_on


def first_seen(pair):
    """Which voice of the pair survives (§7.4, "first-seen survives").

    First in the **committed canonical order** — the §17 consumption order,
    derived from anchoring coordinates and identifier bytes — and never first
    observed. See this.i @sr546w: the arrival-order reading makes two verifiers
    holding one pair compute two different survivors, which axiom 4 and §17 each
    independently declare non-conforming.
    """
    return min((pair.first, pair.second), key=lambda item: item.canonical_key)


def may_convict(pair, committed_predicates):
    """Whether this frame may convict on this pair, or only consume it (§7.4).

    "Registry-tier and governance-tier duplicity are law-relative — they convict
    only within frames that committed the violated predicate, and a frame that
    never committed the predicate SHALL consume them as evidence, never as
    conviction."
    """
    if pair.tier is Tier.KEY:
        return True
    return pair.predicate in committed_predicates


def convict(pair, *, law_head, position, question, committed_predicates):
    """Build the self-conviction this pair supports, or ``None``.

    ``None`` is not a fifth finding value. It means the edge into
    self-convicted is unavailable — either because the pair does not bear on
    this question, or because this frame never committed the predicate — and
    the question keeps whatever value the ordinary machinery gives it (this.i
    @75ljyl6v, entry 20). The pair is still evidence in the bundle either way.
    """
    if not pair.bears_on_question(question):
        return None
    if not may_convict(pair, committed_predicates):
        return None
    return SelfConvicted(law_head, position, proof=pair.proof)


@dataclasses.dataclass(frozen=True, slots=True)
class Dependent:
    """A question built on a lower-tier finding, and where its successor speaks.

    ``position`` is the **new** coordinate at which the annihilating finding is
    made, because §7.3 says new defeat evidence "yields a new finding at a new
    position" rather than flipping the one already settled.
    """

    question: str
    law_head: object
    position: object

    def __post_init__(self):
        if not self.question:
            raise MalformedInput(
                "A dependent must name the question it answers, and the question "
                "was empty. Retrying will not help — annihilation produces a "
                "finding, and a finding is a judgment about a named proposition."
            )


def annihilate_upward(lower, dependents):
    """The defeat current: a lower-tier defeat voids what was built on it.

    Each dependent gets a **new** defeated finding at its own new position,
    carrying the lower-tier defeat unchanged — class, citation and subcode —
    because the lower-tier citation is the ground and inventing a different
    class would be inventing a different ground (this.i @nggcv5f).

    Transitivity is free: the result is itself a ``Defeated`` carrying the same
    defeat, so annihilating its own dependents chains the invalid seal through
    the issuance to the enactment, exactly as §7.4 describes.
    """
    if not isinstance(lower, Defeated):
        raise CurrentsMerged(
            f"A {lower.verdict.value} finding was run through the defeat "
            f"current, but defeat annihilates and duplicity taints, and a "
            f"conforming evaluator does not merge them. Retrying will not help "
            f"— send a self-conviction to taint_upward instead."
        )
    return tuple(
        Defeated(dependent.law_head, dependent.position, defeat=lower.defeat)
        for dependent in dependents
    )


@dataclasses.dataclass(frozen=True, slots=True)
class ContestedStanding:
    """The duplicity current's output, and deliberately **not** a finding.

    §7.4 says what was affirmed above "converts to contested standing", and
    contested standing is not one of the four values §15 fixes the return type
    at. So the affirmed finding survives inside ``surviving`` with its value and
    its bytes untouched — first-seen survival, and "the record it already made
    remains a record" — while this record carries the taint forward (this.i
    @6mntbxri, entry 18).
    """

    subject: str
    tier: Tier
    surviving: Finding
    pair_proof: str

    def __post_init__(self):
        if not self.pair_proof:
            raise GroundMissing(
                f"The contested standing of {self.subject!r} cites no proof "
                f"package for the pair that poisoned the voice. Retrying will "
                f"not help — a taint whose ground cannot be recomputed is the "
                f"judge testifying where the record should."
            )

    def canonical_bytes(self):
        return encode_fields(
            self.subject,
            self.tier.value,
            self.surviving.canonical_bytes(),
            self.pair_proof,
        )


def taint_upward(conviction, pair, standings):
    """The duplicity current: the voice is poisoned going forward, not backward.

    "A self-conviction at a lower tier does not un-happen the history above it:
    committed history is monotonic, first-seen survives, and what was affirmed
    above converts to contested standing rather than to nothing."
    """
    if not isinstance(conviction, SelfConvicted):
        raise CurrentsMerged(
            f"A {conviction.verdict.value} finding was run through the "
            f"duplicity current, but defeated is conviction by another's "
            f"citation and self-convicted is conviction by one's own committed "
            f"pair. Retrying will not help — send a defeat to annihilate_upward "
            f"instead."
        )
    return tuple(
        ContestedStanding(
            subject=pair.subject,
            tier=pair.tier,
            surviving=standing,
            pair_proof=conviction.proof,
        )
        for standing in standings
    )
