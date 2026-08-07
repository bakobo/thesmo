"""The closed three-input type.

Custos 4.1 §1.4 axiom 2 and §7.3 "Inputs" fix the fold's inputs at exactly
three: the committed evidence bundle, the committed law head, and the appraisal
position. "No other input — wall clocks, local state, operator discretion,
ambient configuration — may influence a finding."

That closure is the whole reason this package needs no KERI library: producing
these three from CESR streams is the substrate adapter's job, and the fold sees
only the committed values.

Two readings are pinned here and recorded in ``docs/readings-beta.md``:

- The bundle is a **set of digest-addressed committed items**, not a set of
  spans and not a sequence (this.i @sgc5lpwd, entries 7 and 8). Span membership
  would make ⊆ — and therefore the monotonicity obligation — depend on how a
  presenter chunked identical bytes, which axiom 4 calls a commitment without
  ground.
- Evidence orders by its committed anchor where it has one, and by its
  self-addressing identifier bytes where it does not (this.i @stzggn, entry 9).
  §17 states the rule for GEL events, which are anchored by construction; the
  cited key-event and registry spans axiom 2 also puts in the bundle are not.

The canonical encoding below is **thesmo's choice, not the document's**: §7.3
requires byte-identical findings while §15 confesses the carriage encoding
undesigned, so some encoding has to be pinned for determinism to be testable at
all (this.i @ox6mfpi, entry 26). Nothing in the fold's semantics depends on it.
"""

import dataclasses

from .errors import MalformedInput, UncommittedOrder

__all__ = [
    "AppraisalTriple",
    "EvidenceBundle",
    "EvidenceItem",
    "LawHead",
    "Position",
    "canonical_evidence_order",
    "encode_fields",
]


def encode_fields(*parts):
    """Encode ``parts`` as length-prefixed fields, unambiguously.

    ``2:ab1:c`` cannot be confused with ``3:abc``, so no concatenation of
    fields can forge a different field split — which is what makes byte
    equality a sound test of value equality.
    """
    out = bytearray()
    for part in parts:
        if isinstance(part, bytes):
            raw = part
        elif isinstance(part, str):
            raw = part.encode("utf-8")
        elif isinstance(part, int):
            raw = str(part).encode("ascii")
        else:
            raise MalformedInput(
                f"A value of type {type(part).__name__} cannot be canonically "
                f"encoded; the fold encodes only bytes, text and integers, "
                f"because those are the only shapes committed evidence takes. "
                f"Retrying will not help — convert the value first."
            )
        out += str(len(raw)).encode("ascii") + b":" + raw
    return bytes(out)


@dataclasses.dataclass(frozen=True, slots=True)
class Position:
    """A log coordinate: an identifier and a sequence number.

    Custos 4.1 §4: "A position is a log coordinate (identifier, sequence
    number) in the committed order of the log it names; this document never
    measures position in wall-clock time."
    """

    identifier: str
    sn: int

    def __post_init__(self):
        if not self.identifier:
            raise MalformedInput(
                "A position must name the log it is a coordinate in, but its "
                "identifier was empty. Retrying will not help — supply the "
                "identifier of the KEL, TEL or GEL this coordinate belongs to."
            )
        if self.sn < 0:
            raise MalformedInput(
                f"A sequence number counts events from inception and cannot be "
                f"negative, but {self.sn} was given. Retrying will not help — "
                f"supply the coordinate the committed log actually assigns."
            )

    def precedes(self, other):
        """Whether this coordinate comes before ``other`` in its own log.

        Positions in different logs are **not** comparable. Neither edition
        orders one log's coordinates against another's, so a cross-identifier
        comparison is an uncommitted ordering and the fold refuses it rather
        than legislating a seam (this.i @4qrss4h; §7.5's refusal clause).
        """
        if self.identifier != other.identifier:
            raise UncommittedOrder(
                f"Positions in {self.identifier!r} and {other.identifier!r} "
                f"cannot be ordered against each other: no committed bytes "
                f"order one log's coordinates against another's, and inventing "
                f"an order would be legislating. Retrying will not help — "
                f"compare through a committed anchor instead."
            )
        return self.sn < other.sn

    def canonical_bytes(self):
        return encode_fields(self.identifier, self.sn)


@dataclasses.dataclass(frozen=True, slots=True)
class LawHead:
    """The self-addressing identifier of the committed law an appraisal runs under."""

    said: str

    def __post_init__(self):
        if not self.said:
            raise MalformedInput(
                "A law head is the self-addressing identifier of the committed "
                "law an appraisal runs under, and it was empty. Retrying will "
                "not help — cite the law head the finding is computed under."
            )

    def canonical_bytes(self):
        return encode_fields(self.said)


@dataclasses.dataclass(frozen=True, slots=True)
class EvidenceItem:
    """One committed, digest-addressed member of an evidence bundle.

    ``anchor`` and ``seal_index`` are the item's committed place in §17's
    consumption order — the anchoring KEL coordinate, and the item's index in
    that anchoring event's seal list. They travel together or not at all: half
    an anchor cannot order anything.
    """

    said: str
    anchor: Position | None = None
    seal_index: int | None = None

    def __post_init__(self):
        if not self.said:
            raise MalformedInput(
                "An evidence item is addressed by its self-addressing "
                "identifier, and it was empty. Retrying will not help — supply "
                "the SAID of the committed bytes this item stands for."
            )
        if (self.anchor is None) != (self.seal_index is None):
            raise MalformedInput(
                "An anchored evidence item needs both its anchoring coordinate "
                "and its index in that anchoring event's seal list; one was "
                "given without the other. Retrying will not help — supply both, "
                "or neither for evidence that is not anchored into the GEL."
            )
        if self.seal_index is not None and self.seal_index < 0:
            raise MalformedInput(
                f"A seal index is a position in the anchoring event's seal list "
                f"and cannot be negative, but {self.seal_index} was given. "
                f"Retrying will not help — supply the index the committed seal "
                f"list actually assigns."
            )

    @property
    def canonical_key(self):
        """This item's place in the §17 consumption order.

        Anchored items sort first, by (anchoring log, anchoring sequence
        number, seal index); unanchored items follow, ordered by identifier
        bytes. Every component is derived from committed bytes, so axiom 4's
        no-ambient-order rule holds (this.i @stzggn).
        """
        if self.anchor is None:
            return (1, "", 0, 0, self.said.encode("utf-8"))
        return (
            0,
            self.anchor.identifier,
            self.anchor.sn,
            self.seal_index,
            self.said.encode("utf-8"),
        )

    def canonical_bytes(self):
        if self.anchor is None:
            return encode_fields(self.said)
        return encode_fields(self.said, self.anchor.canonical_bytes(), self.seal_index)


@dataclasses.dataclass(frozen=True, slots=True)
class EvidenceBundle:
    """The committed evidence a finding is a function of.

    A set, not a sequence: §7.3 orders bundles by ⊆, and §17 requires streams
    presented in permuted arrival order to fold to byte-identical
    Constitutions, which is vacuous if presentation order is part of the
    bundle's identity (this.i @sgc5lpwd).
    """

    items: frozenset = frozenset()

    @classmethod
    def of(cls, *items):
        """Build a bundle from items, in any order, with repeats collapsing."""
        return cls(frozenset(items))

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def canonical_bytes(self):
        return encode_fields(
            *(item.canonical_bytes() for item in canonical_evidence_order(self))
        )


def canonical_evidence_order(bundle):
    """The one order a fold consumes its evidence in (Custos 4.1 §17).

    "A fold consumes its log in exactly one order, and that order derives from
    committed bytes: KEL anchoring order first, intra-anchor order as the
    anchoring event's seal list states, and no tiebreak that consults anything
    uncommitted."

    §17 has no counterpart in the ratified 4.0 kernel, so this order is 4.1-only
    law rather than one of the walls §1.4 imports — see ``docs/readings-beta.md``
    §G4, where that distinction is filed as a finding.
    """
    return tuple(sorted(bundle.items, key=lambda item: item.canonical_key))


@dataclasses.dataclass(frozen=True, slots=True)
class AppraisalTriple:
    """The fold's complete input. Exactly three fields, and that is the point.

    Custos 4.1 §1.4 axiom 2: "the inputs are exactly three, closed: the
    committed evidence bundle, the committed law head, and the appraisal
    position. No other input may influence the result."
    """

    bundle: EvidenceBundle
    law_head: LawHead
    position: Position

    def canonical_bytes(self):
        return encode_fields(
            self.bundle.canonical_bytes(),
            self.law_head.canonical_bytes(),
            self.position.canonical_bytes(),
        )
