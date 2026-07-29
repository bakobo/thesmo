## STOP — this repo has a reading restriction

thesmo is built to find where the Custos specification underdetermines a conforming engine.
That signal is destroyed by *reading about* the specification instead of reading it.

**Before touching `src/thesmo/core/`, read [`docs/blind-brief.md`](docs/blind-brief.md).** The
short version, binding under [`this.i` @qmz2o4](this.i) (a locked constraint):

- **Read** `spec/custos-4.1.md` **and** `spec/custos-4.0-kernel-draft.md` in the Custos
  repository. The 4.0 kernel is required, not optional — 4.1 §1.4 binds its evaluator sections
  in by digest referent.
- **Do not read** the Custos issue tracker, `reviews/`, `tools/`, or any review, summary, or
  briefing about Custos's defects — including a one-line hint from a maintainer.
- **Do not read anything outside the workspace you were given** — no other branch, ref, or
  worktree, not this repo's own issues and pull requests, and not `main`. This repository carries
  more than one independent implementation of the same specification surface, and their
  disagreement is the product; a reading that has seen another reading is not evidence. **Never
  merge, rebase, or cherry-pick from `main`** — it holds the reconciliation record, which compares
  implementations side by side. If your branch needs a shared CI or tooling change, say so in your
  report and the maintainer will bring it across.
- **Never resolve an ambiguity by asking.** Bank it as a `this.i` node whose `why` names the
  reading you rejected and cites the lines permitting each, then pin one reading. An ambiguity
  resolved silently is the one failure this project cannot recover from.
- If you have already read a forbidden source, say so. You are not off the project — you are
  off `core/`. The harness, vectors, substrate adapter, and tooling carry no such restriction.

## Commands

| Task | Command |
|---|---|
| Install / sync | `uv sync` |
| Test (gates at 100% branch coverage) | `uv run pytest` |
| Compare Custos editions | `uv run python -m thesmo.editions --custos <path>` |

Python 3.14+, uv, pytest. `core/` has **no runtime dependencies** and must import no KERI
library; `tests/test_core_purity.py` enforces that by AST inspection, so a lazy import inside a
function body will not sneak past it. keripy arrives at M3, in `thesmo.substrate` only.

## Testing

Strict TDD. Write failing tests that capture the happy path and the edge/unhappy cases for each
requirement, observe them fail, then implement until they pass. Never check in without proving
the suite green. 100% branch coverage of new code is enforced in CI; any gap needs an approved
`deviation:` node in `this.i`. Always leave existing code better tested than you found it.

## Bakobo engineering standards

How every Bakobo repo builds is governed by cross-cutting standards, canonical in the sibling
[`bakobo/dev`](../dev) repo. If `../dev` is not checked out beside this one, clone it before design
work: `git clone --depth 1 https://github.com/bakobo/dev`. Always on:

- **Intent-first** development and **strict TDD at 100% branch coverage of new code** — see the
  sections below and [`dev/methodology.md`](../dev/methodology.md).
- **Fail closed.** Untrusted input never carries authority; when something can't be checked, the
  effect does not land ([`org` principle 8](../org/design/purpose-and-principles.md)).
- **High-quality errors.** Every error carries a stable symbolic code, says whether retrying could
  help (permanent vs. transient), and reads as complete, plain sentences in the house voice — never
  "something went wrong." Full standard: [`dev/standards/error-handling.md`](../dev/standards/error-handling.md).
- **Repo layout.** Architecture and developer docs live in `docs/`; the root holds only repo-level
  files (`README`, `LICENSE`, `CONTRIBUTING`), the instruction/config files, build manifests, and
  `this.i` at the root as the source of truth. Don't leave `design.md` loose at the root. Full
  standard, including the content-repo nuance: [`dev/standards/repo-layout.md`](../dev/standards/repo-layout.md).
- **Terminology.** Bakobo's architecture has a precise vocabulary (`core`, `steward`, `mint`, …). Its
  single source of truth is [`bakobo/glossary`](https://github.com/bakobo/glossary), reached via the
  `glossary` MCP server. Consult a term before using it, reconcile prose to the glossary (not the
  reverse), mint/amend terms in-band through the MCP (never hand-edit), and don't let a general word
  masquerade as a formal term. Full standard: [`dev/standards/terminology.md`](../dev/standards/terminology.md).
- **Tasks and tech debt in `tick`** — see the tick stanza below, not an external tracker.
- **Craftsman working posture.** Development follows the `cc` craftsman methodology — interview at
  intent level, dispatch briefs to worker sub-agents, verify against oracles, and learn from every
  failure. It is Daniel Hardman's personal craft (the private `cc` repo), adopted across Bakobo; the
  operational rules for *this* repo are in [`dev/methodology.md`](../dev/methodology.md).

## Intent methodology

Bakobo develops intent-first. If this repo has design decisions worth explaining, its source of
truth is `this.i` (the intent tree) at the repository root — code and `docs/` are derived from it.
Record each consequential decision in `this.i` **first**, in its own commit, **before** the code
commit it justifies. The full rules — what `this.i` is, when a repo needs one, the speculative
interview, the `why` rebuttal-surface standard, the gate ceremony, and adversarial review — are in
[`dev/methodology.md`](../dev/methodology.md), in the sibling `bakobo/dev` repo. Read it before
making design decisions here.

If this repo has no `this.i` yet and warrants one, see [`dev/methodology.md`](../dev/methodology.md)
§2 and the shipped `this.i.seed`. A trivial repo (pure content/assets/config, where no one will
later need to know *why*) may skip intent entirely — just delete `this.i.seed`.

<!-- >>> tick stanza >>> (managed by `tick init`) -->

## Task tracking: `tick`

This repo tracks tasks, tech debt, and ideas in a local [`tick`](https://github.com/dhh1128/tick)
ledger (an orphan `tick` branch; the `tick` CLI is the interface). Reads are plain
files — do **not** use an external API for task tracking.

- **First, if a `tick` command says the repo isn't initialized**, run `tick init`
  once to connect this clone to the ledger — it adopts the existing remote ledger
  if a colleague already set one up, or creates a new one otherwise.
- **A tick mark is the sigil `~` immediately followed by a digit-first 4-char
  base32 id** (the id part looks like `4mz3`, so the full mark is that id with a
  leading `~`). It pins a tick to a code location.
- **Before editing a file**, grep it for marks and read what they reference:
  `rg '~[2-7][a-z2-7]{3}\b' <file>` then `tick show <id>`. A mark means recorded
  context exists for that spot — read it first.
- **Search** existing ticks with `tick grep <text>`; **list** with `tick ls`.
- **Capture** new work with `tick add "<title>"` and place the printed mark
  (`~` + the new id) at the relevant code spot.
- When your change **resolves** a tick, run `tick off <id>` and **delete the
  mark(s)** it reports still in the code.

<!-- <<< tick stanza <<< -->
