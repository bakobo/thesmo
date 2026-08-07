"""The fold's closed three-input type.

Custos §1.4 axiom 2, quoted whole because the whole of it binds:

    **Replay.** The same committed inputs yield the same computed state — and
    the inputs are exactly three, closed: the committed evidence bundle, the
    committed law head, and the appraisal position. No other input may
    influence the result.

§7.3 "Inputs" says it again at keyword force, and adds the conformance
predicate: "Two evaluations of the same triple SHALL return byte-identical
findings."

Two consequences shape this module.

**The bundle is a set whose members carry their own order.** §7.3 orders
bundles by the subset relation, which makes a bundle a set; §17 requires the
fold to consume its log in exactly one committed order, "KEL anchoring order
first, intra-anchor order as the anchoring event's seal list states, and no
tiebreak that consults anything uncommitted". If that order arrived from
outside, it would be a fourth input. So each ``EvidenceItem`` carries its own
``Coordinate`` and the bundle computes its order from what it holds
(this.i @vwqohe).

**Position is never a clock.** §4: a position "is a log coordinate (identifier,
sequence number) in the committed order of the log it names; this document never
measures position in wall-clock time." A float sequence number is the shape a
timestamp arrives in, so it is rejected rather than coerced.
"""

from dataclasses import dataclass, field

from thesmo.core.errors import MalformedInput, require


def _identifier(value, name):
    """A self-addressing identifier: a non-empty string, and nothing else."""
    require(
        isinstance(value, str) and value != "",
        MalformedInput,
        f"{name} must be a non-empty self-addressing identifier; got {value!r}. "
        "Custos §4 makes every log coordinate and law head an identifier, so an "
        "empty or non-string value names nothing the fold can resolve.",
    )
    return value


def _sequence_number(value, name):
    """A sequence number: a non-negative int. ``bool`` is an int and is not one."""
    require(
        isinstance(value, int) and not isinstance(value, bool) and value >= 0,
        MalformedInput,
        f"{name} must be a non-negative integer sequence number; got {value!r}. "
        "Custos §4 measures position in committed log coordinates and never in "
        "wall-clock time, so a float or a negative value is not a position.",
    )
    return value


@dataclass(frozen=True, slots=True, order=True)
class Coordinate:
    """Where a committed item sits in the fold's one lawful consumption order.

    §17's canonical order is "KEL anchoring order first, intra-anchor order as
    the anchoring event's seal list states" — two numbers, in that priority.
    """

    anchor_sequence_number: int
    seal_index: int

    def __post_init__(self):
        _sequence_number(self.anchor_sequence_number, "anchor_sequence_number")
        _sequence_number(self.seal_index, "seal_index")


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """One committed item of the evidence bundle, at its committed coordinate."""

    identifier: str
    coordinate: Coordinate

    def __post_init__(self):
        _identifier(self.identifier, "identifier")
        require(
            isinstance(self.coordinate, Coordinate),
            MalformedInput,
            f"coordinate must be a Coordinate; got {self.coordinate!r}. Without a "
            "committed coordinate the item has no place in §17's canonical order.",
        )

    def order_key(self):
        """The item's place in the committed order.

        The coordinate first, then the item's own identifier bytes as the
        tiebreak. §17 forbids only a tiebreak "that consults anything
        uncommitted"; the identifier is committed, so this is lawful — but it is
        not the *only* lawful tiebreak, and a different one changes which of two
        items at one coordinate is first-seen (this.i @vwqohe, @r5p4h2).
        """
        return (self.coordinate, self.identifier.encode("utf-8"))


@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    """The committed evidence bundle: a set, ordered by its members' coordinates.

    A set, because §7.3's monotonicity "is over the subset order on bundles at a
    fixed law head and position". Ordered on demand, because §1.4 axiom 4 admits
    only an order "derivable from committed bytes".
    """

    items: frozenset = field(default_factory=frozenset)

    def __post_init__(self):
        for item in self.items:
            require(
                isinstance(item, EvidenceItem),
                MalformedInput,
                f"an evidence bundle holds EvidenceItems; got {item!r}. Committed "
                "bytes without a coordinate cannot be placed in the fold's order.",
            )

    @classmethod
    def of(cls, *items):
        """Build a bundle from items, or from one iterable of them."""
        if len(items) == 1 and not isinstance(items[0], EvidenceItem):
            items = tuple(items[0])
        return cls(frozenset(items))

    def committed_order(self):
        """Every item, in the one order §17 permits the fold to consume."""
        return tuple(sorted(self.items, key=EvidenceItem.order_key))

    def grown_by(self, *items):
        """A new, larger bundle. Evidence growth is the fold's only motion."""
        return EvidenceBundle(self.items | frozenset(items))

    def issubset(self, other):
        return self.items <= other.items

    def __le__(self, other):
        return self.items <= other.items

    def __lt__(self, other):
        return self.items < other.items

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return iter(self.committed_order())

    def __len__(self):
        return len(self.items)


@dataclass(frozen=True, slots=True)
class Position:
    """The appraisal position: a committed log coordinate, never a time."""

    identifier: str
    sequence_number: int

    def __post_init__(self):
        _identifier(self.identifier, "position identifier")
        _sequence_number(self.sequence_number, "sequence_number")


@dataclass(frozen=True, slots=True)
class LawHead:
    """The self-addressing identifier of the committed law an appraisal runs under."""

    said: str

    def __post_init__(self):
        _identifier(self.said, "law head")


@dataclass(frozen=True, slots=True)
class AppraisalTriple:
    """The fold's complete input. Exactly three, closed.

    A fourth field here would not be a feature; it would be a conformance
    failure, which is why ``INPUT_COUNT`` and the field tuple are asserted in
    the suite rather than trusted to review.
    """

    bundle: EvidenceBundle
    law_head: LawHead
    position: Position

    INPUT_COUNT = 3

    def __post_init__(self):
        for value, kind, name in (
            (self.bundle, EvidenceBundle, "bundle"),
            (self.law_head, LawHead, "law_head"),
            (self.position, Position, "position"),
        ):
            require(
                isinstance(value, kind),
                MalformedInput,
                f"the appraisal triple's {name} must be a {kind.__name__}; got "
                f"{value!r}. Custos §1.4 axiom 2 closes the fold's inputs at these "
                "three, so an input the fold cannot check is not an input it may use.",
            )

    def inputs(self):
        """The three, in the order the axiom names them."""
        return (self.bundle, self.law_head, self.position)

    def grows_to(self, other):
        """True where ``other`` is this triple with a larger-or-equal bundle.

        §7.3's monotonicity is stated "at a fixed law head and position", so a
        triple with a different law head or position is not growth — it is a
        different question, and the transition system has nothing to say about
        the pair.
        """
        return (
            self.law_head == other.law_head
            and self.position == other.position
            and self.bundle <= other.bundle
        )
