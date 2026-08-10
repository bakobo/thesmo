# M2 legs — the shared protocol

Five legs run against ratified Custos 4.2. Three share one surface so their readings can
collide; two run alone on surfaces where the product is a completeness table rather than a
disagreement ([`this.i` @kcmw4c](../../this.i), [@ipjprf](../../this.i), [@6rhjga](../../this.i)).

| Leg | Branch | Model | Surface | Builds |
|---|---|---|---|---|
| Gamma | `m2-gamma` | Claude | §18–§19, 4.2 L3061–3478 | engine + register + cases |
| Delta | `m2-delta` | Claude | §18–§19, 4.2 L3061–3478 | engine + register + cases |
| Epsilon | `m2-epsilon` | Codex (gpt-5.6) | §18–§19, 4.2 L3061–3478 | register + cases, **no engine** |
| Zeta | `m2-zeta` | Claude | Chapter 2, 4.2 L441–861 | total classifier + register |
| Eta | `m2-eta` | Claude | §1.7 over the whole document | gate table + register |

Every leg is blind under [`docs/blind-brief.md`](../blind-brief.md), including Epsilon. No leg
is told that any other exists beyond what that document already discloses, and no leg is handed
this file — the maintainer hands each leg only its own brief.

## Why three on one surface and one on the others

Cross-leg divergence is only obtainable where legs read the same text, so the shared surface has
to be small enough to afford three legs. Epsilon is asymmetric on purpose: a second model family
is where the 4.2 cycle's own collider found its unique returns, but its budget is rate-limited,
so it spends that budget on the reading rather than on an implementation. Its expected values
are then executed by running Gamma's and Delta's engines against them, which yields a
cross-family divergence for the price of one review pass.

Zeta and Eta run alone because a totality check does not improve with a second opinion.

## The case format

The one piece of plumbing coordinated across legs ([`this.i` @pdig63](../../this.i)). It is a
JSON shape, deliberately **not** a Python API: naming the functions and their return types would
pre-empt real questions — whether the answer is a finding, a refusal, or a bare value is exactly
the kind of thing the legs are supposed to disagree about.

```json
{
  "id": "G-18-01",
  "surface": "§18",
  "given": { "...": "fixture symbols, fully concrete, no wire bytes" },
  "then":  { "...": "the expected result, field by field" },
  "discriminates": "one sentence: what a wrong engine would get instead"
}
```

Fixture symbols are stated once per leg in its own `cases/convention.md` and are fixed strings,
not bytes — the carriage encoding has not ratified, so there is nothing to serialize. A case is
concrete at the semantic layer or it is not a case.

Each engine leg additionally ships `python -m <its package>.run_case <file.json>`, reading a case
and printing its `then` as computed. The **shape** of that output is the leg's own choice; a
disagreement about which fields exist is a finding, not a formatting problem.

## Invoking Epsilon

Maintainer-facing; Epsilon never sees this section. Verify the edition, then run Codex **from an
empty directory** — its sandbox is read-only but it explores its cwd freely, and started from a
checkout it can walk into `reviews/` or `vectors/` and contaminate itself without being asked to:

```sh
sha256sum ~/code/3GR/custos/spec/custos-4.2.md
# 68cc5c9b7164b33dffcf7b705a0d1301fe108c647d35638fec61d52d29b2775a

d=$(mktemp -d) && cd "$d"
cat ~/code/3GR/custos/spec/custos-4.2.md \
  | nice -n 19 codex exec "$(cat ~/code/bakobo/thesmo/docs/legs/epsilon.md)" \
  > /tmp/thesmo-epsilon-out.md 2>&1
```

The specification arrives on stdin as a `<stdin>` block, which is why Epsilon's brief says the
edition was supplied and verified rather than telling it to check the digest itself. Its output
is prose; the maintainer commits it to `m2-epsilon` as `docs/readings-epsilon.md` plus `cases/`.

## Deliverables, identical in kind for every leg

1. **A readings register** at `docs/readings-<leg>.md`, following
   [`docs/readings-TEMPLATE.md`](../readings-TEMPLATE.md) — the M1 form, emptied of content so
   that handing it to a leg discloses nothing: the span quoted, the
   lawful readings, the specification lines permitting each, the one pinned, and whether the
   readings produce different results on some input.
2. **A `this.i` node per pinned reading**, committed before the code that depends on it, with the
   node id cross-referenced from the register.
3. **Cases** under `cases/`, one file per case.
4. **A report** — see below.

## The report

At the end, write `docs/report-<leg>.md` answering exactly these:

- What did you build, and what does it refuse to answer?
- Which readings diverge on some input, and what is the discriminating input for each?
- Where did the specification make you invent something it does not state? Name it as an
  invention, not as a design choice.
- What could you not build at all, and what would the document have to say for you to build it?
- Did you at any point read something outside your window? Say so plainly; it is recoverable
  only if declared.

## Milestones

Every leg appends a timestamped line to `/tmp/thesmo-<leg>-status.log` on each milestone, and
checks `/tmp/thesmo-<leg>-inbox.md` there for revised instructions before proceeding.

`M1 window verified` · `M2 register banked` · `M3 surface built` · `M4 cases written` ·
`M5 report filed`

The register is banked **before** the build, as at M1 — a reading recorded after the code exists
has been shaped by the code.
