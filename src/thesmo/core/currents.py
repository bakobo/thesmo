"""The duplicity ladder and the two upward currents. Custos §7.4.

    Findings cascade between tiers in two distinct currents, and a conforming
    evaluator SHALL NOT merge them:

    - **Defeat annihilates upward.** A defeated finding at a lower tier voids
      what was built on it [...] The dependents were never valid; annihilation
      is discovery, not change.
    - **Duplicity taints upward.** A self-conviction at a lower tier does not
      un-happen the history above it: committed history is monotonic, first-seen
      survives, and what was affirmed above converts to contested standing
      rather than to nothing. The subject's voice is poisoned going forward; the
      record it already made remains a record.

The non-merge rule is why this module is shaped the way it is: two currents, two
functions, two return types, and the one entry point that runs either
(``cascade``) returns a product with a slot for each, never a merged verdict.
§7.5 requires exactly that of compound results — "as a product rather than
collapse them into a fifth scalar shape".

Three readings had to be pinned, and each is a place where a second engine
diverges:

- **Contested standing is not a finding** (@b7773r). §7.4 says affirmed history
  "converts to contested standing", which is not one of §7.1's four values, and
  §15 rules that the return type is "the four-valued finding codomain and
  nothing else". So the finding is left exactly as it was — it "remains a
  record" — and the taint is a separate marker over the subject's standing.
- **Annihilation reaches pending dependents only** (@bwq5ghwn), as a theorem
  rather than a special case: §7.3's affirmation discipline means an affirmed
  dependent is one whose lower-tier check was already examined and discharged,
  because defeating evidence is ex-ante enumerable. So `pending -> defeated`,
  a permitted edge, is the only annihilation there is, and an affirmed dependent
  offered for annihilation is a conformance defect we refuse rather than a case
  we convert.
- **An annihilated dependent inherits the lower defeat's citation** (@2lc26h).
  §7.4 says dependents are voided and never says what the voided finding cites;
  the alternative — citing the lower finding — needs an identifier for a
  finding, and no section of either edition mints one.
"""

from dataclasses import dataclass
from enum import Enum

from thesmo.core.errors import GroundMissing, MalformedInput, WallViolation, require
from thesmo.core.finding import Defeated, Finding, SelfConvicted, Verdict
from thesmo.core.ordering import Defeat, first_seen, select_defeat


class Tier(Enum):
    """§7.4's three rungs. "The voice unit rises with the tier" (§4)."""

    KEY = 1
    REGISTRY = 2
    GOVERNANCE = 3

    @property
    def rung(self):
        return self.value


#: What "two voices" means at each rung, in §7.4's own words. Kept beside the
#: tier because §7.4's whole point is that each tier's duplicity "is
#: structurally invisible to the machinery of the tier below".
LADDER = {
    Tier.KEY: "two events at one coordinate of one KEL",
    Tier.REGISTRY: (
        "two registries where committed law demands one chain — no fork appears "
        "anywhere; the crime is visible only to a fold that reads the KEL as a "
        "registry of registries"
    ),
    Tier.GOVERNANCE: (
        "contradictory enactments under one committed predicate — visible only to "
        "a Gever evaluating the corpus"
    ),
}


class DuplicityForce(Enum):
    """How far a proven duplicity reaches. §7.4's force distinction.

    "key-tier duplicity convicts in the medium, for every verifier, under no
    frame's law. Registry-tier and governance-tier duplicity are law-relative —
    they convict only within frames that committed the violated predicate, and a
    frame that never committed the predicate SHALL consume them as evidence,
    never as conviction."
    """

    MEDIUM = "convicts in the medium, for every verifier, under no frame's law"
    FRAME_LOCAL = "convicts within this frame, which committed the violated predicate"
    EVIDENCE_ONLY = "consumed as evidence, never as conviction"


def duplicity_force(tier, predicate_committed):
    """The force a proven contradictory pair carries at ``tier``.

    Note how differently this resolves from the missing *bearing* predicate of
    ``this.i`` @62dtu6n, which refuses. The two cases look identical from inside
    the fold — "the law gives me nothing to convict on" — and part twice: here
    the rule is present and says *not a conviction in this frame*; there no rule
    exists at all, and §7.5 sends an uncommitted seam to refusal.
    """
    require(
        isinstance(tier, Tier),
        MalformedInput,
        f"duplicity force is asked of one of §7.4's three tiers; got {tier!r}.",
    )
    if tier is Tier.KEY:
        return DuplicityForce.MEDIUM
    return DuplicityForce.FRAME_LOCAL if predicate_committed else DuplicityForce.EVIDENCE_ONLY


def first_seen_survivor(pair):
    """Which voice of a contradictory pair survives: the first in committed order.

    §7.4's "first-seen survives", read positionally (this.i @r5p4h2). A pair is
    two, and a collection of any other size is a question §7.4 does not reach.
    """
    items = list(pair)
    require(
        len(items) == 2,
        MalformedInput,
        f"first-seen survival runs over a contradictory pair, which is two "
        f"committed voices; got {len(items)}. §7.4 defines duplicity as 'two "
        "voices where the constitution of a tier demands one', and this fold "
        "will not generalize the count on the standard's behalf.",
    )
    return first_seen(items)


def annihilate(lower, dependent):
    """The defeat current: what a lower-tier defeat does to what was built on it.

    Returns the dependent's finding as it stands once the lower defeat is in the
    bundle. Nothing is mutated; the returned finding is a new value.
    """
    require(
        isinstance(lower, Defeated),
        MalformedInput,
        f"the defeat current flows from a defeated finding; got {lower!r}. §7.4 "
        "keeps breach and duplicity distinct crimes, so a self-conviction below "
        "taints (see taint) and never annihilates.",
    )
    require(
        isinstance(dependent, Finding),
        MalformedInput,
        f"the dependent must be a finding; got {dependent!r}.",
    )
    require(
        dependent.verdict is not Verdict.AFFIRMED,
        WallViolation,
        "an affirmed dependent cannot be annihilated. §7.3's affirmation "
        "discipline makes affirmed reachable only over a bundle that discharges "
        "the question's ENTIRE committed requirement space, and defeating "
        "evidence is ex-ante enumerable — so an affirmed dependent is one whose "
        "lower-tier check was already examined and discharged. Converting it "
        "would cross the forbidden affirmed -> defeated edge, one of §15's six "
        "walls. Whatever affirmed this dependent is where the defect is.",
    )
    if dependent.verdict is Verdict.SELF_CONVICTED:
        # §7.3: terminal for its question. Nothing rehabilitates it and nothing
        # re-convicts it either.
        return dependent
    available = [Defeat.of(lower)]
    if dependent.verdict is Verdict.DEFEATED:
        # Two defeats are now simultaneously available for one question, which
        # is precisely §7.3's canonical-selection case. Keeping the older
        # citation instead would make the finding depend on the order cascades
        # were applied in — an ambient order, forbidden by §1.4 axiom 4.
        available.append(Defeat.of(dependent))
    return select_defeat(available).as_finding(dependent.question, dependent.triple)


@dataclass(frozen=True, slots=True)
class ContestedStanding:
    """The tainting current's output. Deliberately not a ``Finding``.

    §7.4 says affirmed history above a self-conviction "converts to contested
    standing rather than to nothing", and contested standing is not one of
    §7.1's four values. §15 makes the four-value count a wall, so the conversion
    cannot be a fifth value and cannot be the affirmed -> self-convicted edge
    (§7.4 forbids blurring breach and duplicity). What is left, and what this
    is: the finding stands as the record it already made, and the subject's
    voice is marked poisoned going forward (this.i @b7773r).
    """

    subject: str
    contested_from: object
    proof_package: str
    surviving_finding: Finding

    def __post_init__(self):
        require(
            isinstance(self.subject, str) and self.subject != "",
            GroundMissing,
            "contested standing must name the subject whose voice is poisoned; a "
            "taint attached to nobody marks nothing.",
        )
        require(
            isinstance(self.proof_package, str) and self.proof_package != "",
            GroundMissing,
            "contested standing must carry the proof package of the contradictory "
            "pair it derives from. §7.4: self-conviction is conviction by one's "
            "own committed pair, and the taint inherits that ground.",
        )
        require(
            isinstance(self.surviving_finding, Finding),
            MalformedInput,
            f"contested standing carries the finding that survives unchanged; got "
            f"{self.surviving_finding!r}.",
        )


def taint(lower, dependent, subject):
    """The duplicity current: what a lower-tier self-conviction marks above it.

    The dependent's finding is returned unchanged inside the marker. §7.4: "the
    record it already made remains a record."

    Applied to any dependent, not only an affirmed one (this.i @6h4dxyr7): §7.4
    explains the affirmed case because it is the one where a reader might expect
    something to un-happen, not because the current stops there.
    """
    require(
        isinstance(lower, SelfConvicted),
        MalformedInput,
        f"the duplicity current flows from a self-conviction; got {lower!r}. §7.4 "
        "keeps breach and duplicity distinct: a defeat below annihilates (see "
        "annihilate) and never taints.",
    )
    require(
        isinstance(dependent, Finding),
        MalformedInput,
        f"the dependent must be a finding; got {dependent!r}.",
    )
    return ContestedStanding(
        subject=subject,
        contested_from=lower.position,
        proof_package=lower.proof_package,
        surviving_finding=dependent,
    )


@dataclass(frozen=True, slots=True)
class CascadeResult:
    """The two currents' outputs, side by side and never merged.

    §7.4: "a conforming evaluator SHALL NOT merge them." §7.5: compound results
    "SHALL preserve their component propositions and grounds as a product rather
    than collapse them into a fifth scalar shape". There is deliberately no
    combined "invalidated" flag here — a caller that wants one has to write it,
    and then it owns the merge the standard forbids.
    """

    annihilated: Finding = None
    contested: ContestedStanding = None


def cascade(lower, dependent, subject):
    """Run whichever current the lower finding carries, and keep them apart.

    Only defeat and self-conviction cascade: §7.4's two currents are the two
    crimes, and an affirmed or pending finding below carries neither.
    """
    if isinstance(lower, Defeated):
        return CascadeResult(annihilated=annihilate(lower, dependent))
    if isinstance(lower, SelfConvicted):
        return CascadeResult(contested=taint(lower, dependent, subject))
    raise MalformedInput(
        f"nothing cascades from {lower!r}. §7.4's two upward currents run from a "
        "defeated finding and from a self-conviction; an affirmed or pending "
        "finding below carries neither crime, and inventing a third current "
        "would be the merge the same section forbids."
    )
