# The blind brief — what a `core/` implementer may read

**Status:** binding on anyone implementing `src/thesmo/core/`.
**Authority:** [`this.i` @qmz2o4](../this.i), a locked constraint. Changing this document
without first changing that node is a defect.

## Why this exists

thesmo is built to find the places where Custos underdetermines a conforming engine. That
signal is fragile in one specific way: **an implementer who already knows where the
specification is soft will route around those places without noticing.** They will read the
ambiguous clause, unconsciously supply the resolution they absorbed from a review, implement
it, and never record that a fork was there.

The divergence is then invisible — not because it does not exist, but because the reading was
shared before the code was written. A finding produced that way tells you nothing about the
document; it tells you what the reviewers already said.

So the reading has to be genuinely independent, and independence here is a property of *what
went into the implementer's head*, not of who signs the commits.

## The rule

**Read the committed specification. Read nothing else about it.**

### You may read

- `spec/custos-4.1.md` — the edition of record.
- `spec/custos-4.0-kernel-draft.md` — **required, not optional.** 4.1 §1.4 binds the 4.0
  kernel's evaluator sections into 4.1 by digest referent. An implementer who reads only the
  edition of record builds a non-conforming engine and cannot tell ([`this.i` @ultpjo](../this.i)).
- The KERI, ACDC and CESR specifications, and keripy, as substrate references.
- This repository: `this.i`, `docs/`, existing code and tests.

### You may not read

- The Custos issue tracker, including issue #1 (the spec roadmap) and its comments.
- `reviews/` in the Custos repository, or any adversarial review of Custos, published or not.
- `tools/` in the Custos repository — its spec-integrity scripts encode the author's own
  reading of the pin discipline.
- Any conformance vectors authored by the specification's author, until the cross-run at M5.
- Any summary, chat log, or briefing that characterizes Custos's defects — including a
  friendly one-line hint from a maintainer.
- **This repository's own issues and pull requests**, and its `main` branch. Both discuss the
  specification's defects in exactly the terms you are supposed to derive independently.
- **Any branch, ref, worktree, or directory other than the workspace you were given.** Do not
  run `git branch -a`, `git log` on another ref, `git show` on another branch, or list the
  parent directory of your workspace. Your workspace root is named in your brief; everything
  outside it, except the specification directory, is out of bounds.

### Branch blindness

This repository maintains **more than one independent implementation of the same specification
surface**, on long-lived branches, and their disagreement is the project's primary product. That
only works if each implementation is a genuinely independent reading.

So the reading restriction is not only about Custos commentary — it is about **this codebase**.
You are working on one implementation. You are not told what any other contains, and you must
not go looking: not its code, not its tests, not its readings register, not its commits, not a
pull request describing it. If you learn how another implementation resolved a clause, your
resolution of that clause stops being evidence.

This is why `main` is off-limits to you even though it is this repo's default branch: `main`
carries the reconciliation record, which compares implementations side by side. **Never merge or
rebase from `main` into your branch, and never cherry-pick from it.** If your branch needs a
shared tooling or CI change, say so in your report and the maintainer — who is not blind — will
bring it across deliberately.

You will notice this rule implies other work exists. That much is unavoidable: a rule cannot
forbid reading something without alluding to it. What matters is that you learn nothing about
*how* anyone else read the specification, which is the only thing that would contaminate your
reading.

If you have already read one of these, **say so** rather than proceeding. You are not
disqualified from the project; you are disqualified from `core/`. There is real work in the
harness, the vectors, and the substrate adapter that carries no blindness requirement.

## What to do with an ambiguity

Do **not** ask the specification's author. Do not ask the maintainer to adjudicate. Resolving
an ambiguity by conversation destroys exactly the evidence thesmo exists to produce, and it
cannot be undone afterwards.

Instead:

1. **Bank it as a node in `this.i`,** committed before the code that depends on it. The `why`
   must name the reading you rejected and cite the specification lines that permit each — that
   is the rebuttal-surface standard doing double duty as a defect report.
2. **Make it a reading switch** if both readings are genuinely lawful and produce different
   Constitutions. The point is to demonstrate the divergence, not to describe it.
3. **Pin one reading** in the shipped fold, because a configurable engine does not conform
   ([`this.i` @6amuue](../this.i)).

An ambiguity you resolved silently is the one failure this project cannot recover from. When
in doubt, bank it — a node that turns out to be unambiguous costs almost nothing.

## What may be coordinated

Plumbing, freely: vector file formats, directory layout, harness invocation, naming of
non-semantic artifacts. None of these change what the fold returns, and agreeing them early
saves a translation layer at cross-run time ([`this.i` @pdig63](../this.i)).

The line is: **if it can change the value of a Constitution, it is blind.**

## Roles

- **Maintainer (Daniel Hardman)** — steward and gatekeeper. He authored the adversarial
  reviews that shaped Custos 4.1 and is permanently compromised as a `core/` reader. He
  approves gates, writes discriminating vectors from what he knows, and does not implement the
  fold.
- **`core/` implementers** — blind, per this document.
- **Harness, vectors, substrate, tooling** — no blindness requirement. `src/thesmo/editions.py`
  is deliberately in this category: it compares specification bytes structurally without
  interpreting them.
