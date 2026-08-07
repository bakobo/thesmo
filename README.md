# thesmo

[![CI](https://github.com/bakobo/thesmo/actions/workflows/ci.yml/badge.svg)](https://github.com/bakobo/thesmo/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/downloads/)

**A Gever — the governance fold of [Custos](https://github.com/Nicholas-Keystate/custos) —
built blind, as an instrument for falsifying the standard.**

Custos specifies *Governed Autonomic Replayable Domains*: KERI-based domains whose law is
committed to a governance event log, and whose judgment is **computed** from that log by a
fold called the Gever. The property it promises is replayable governance — *any stranger
holding the logs computes the same Constitution, the same findings, the same refusals, byte
for byte.*

That promise has never been tested by an independent implementation. The standard says so
itself, and records the condition under which it would be wrong: *"no second implementation
ever derives equal state from the same corpus."* thesmo exists to put it under load.

## What makes this different from just writing an engine

An engine written to be *useful* hides the defect class we are hunting. The implementer meets
an ambiguous clause, picks a reading, it works, and the fork the specification permitted is
never seen by anyone.

So thesmo inverts it. **Every point where Custos underdetermines the fold becomes a named
reading switch**: the lawful readings, the specification lines that permit each, and the one
we pinned. Test-only configuration runs two readings over one corpus and produces *two
different Constitutions from the same committed input* — which turns "two conforming engines
could diverge here" from an argument into a demonstration.

The shipped fold pins exactly one reading per switch and is fully deterministic, because a
configurable engine would not conform to the very axiom under test. The switchboard lives in
the harness.

## The register

Every pinned reading is recorded in [`this.i`](this.i), the intent tree, whose `why` fields
must name the reading they rejected. That obligation makes the intent tree do double duty: it
is the design record *and* the running list of places the specification underdetermines an
engine. Read it as a defect list.

The long form of each reading — the quoted span with line numbers, the lawful alternatives,
and the input on which two conforming engines produce different findings — is in
[`docs/readings-alpha.md`](docs/readings-alpha.md).

## Status

**M1 — the evaluator walls.** `core/` implements the closed three-input type (§1.4 axiom 2),
the four-valued finding codomain with its required payloads (§7.1, §7.3), the evidence
ordering and canonical selection of defeats (§7.3), the complete transition system (§7.3), and
the duplicity ladder with its two upward currents (§7.4). No substrate adapter, no CESR, no
wire encoding: the fold's inputs are closed at three committed values, so `core/` imports no
KERI library and a test enforces it.

The first blind read of §7 found **22 places where Custos underdetermines a conforming
engine, 16 of which make two engines diverge on identical committed bytes.** That list, not
the code, is the milestone's output.

Per [`this.i` @qmz2o4](this.i), the fold itself must be implemented by someone who has read
the Custos specification **and nothing else** — not its issue tracker, not its reviews. See
[`docs/blind-brief.md`](docs/blind-brief.md) before contributing to `core/`.

## From a fresh clone to passing tests

```sh
git clone https://github.com/bakobo/thesmo && cd thesmo
uv sync
uv run pytest
```

Tests gate at **100% branch coverage**; a run that drops below it fails.

## The edition comparator

Custos 4.1 §1.4 binds the ratified 4.0 kernel's evaluator sections into 4.1 *by committed
digest referent*, while 4.1 §7.3 presents itself as the "complete enumeration" of the same
transition system. An implementer who reads only the edition of record may therefore build a
non-conforming engine and have no way to tell.

This compares them structurally, against a checkout you supply — deriving the answer from
committed bytes rather than taking ours:

```sh
uv run python -m thesmo.editions --custos /path/to/custos
```

Exit `0` if the evaluator sections agree after renumbering, `1` if they differ (with the
diff), `2` if the bytes aren't where it looked. It reads and compares; it does not interpret,
so running it does not compromise a blind implementer.

## Layout

| Path | What |
|---|---|
| `this.i` | Intent tree — source of truth, and the register of pinned readings |
| `src/thesmo/core/` | The fold. Pure: imports no KERI library, enforced by test |
| `src/thesmo/editions.py` | The 4.0 ↔ 4.1 evaluator comparator |
| `docs/blind-brief.md` | What a `core/` implementer may and may not read |
| `docs/readings-alpha.md` | The M1 readings in full: spans, alternatives, divergences |

## License

Apache-2.0. The Custos specification text it implements is separately licensed by its author
under the Community Specification License 1.0.
