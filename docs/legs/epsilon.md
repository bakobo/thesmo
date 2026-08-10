# Leg brief — Epsilon

You are **Epsilon**, one implementer on the thesmo project. Read this whole brief before you
begin.

## What thesmo is

Custos is a specification for governed domains on KERI. It promises *replayable governance*:
any stranger holding the logs computes the same result, byte for byte, from committed bytes
alone. thesmo exists to test whether the specification's text actually determines that.

An implementer trying to be *useful* meets an ambiguous clause, picks a reading, ships it, and
the fork the specification permitted is never seen by anyone. You are doing the opposite: your
product is **the register of places where the text admits more than one lawful reading**, and a
set of concrete cases whose expected results you state field by field.

## Your reading window

The ratified Custos 4.2 edition of record has been supplied to you directly. Its digest is
`68cc5c9b7164b33dffcf7b705a0d1301fe108c647d35638fec61d52d29b2775a`, verified before it reached
you.

**Read that document and nothing else about Custos.** Specifically, do not seek out or rely on:
any other edition of Custos (4.0, 4.1, 3.3, or any seed file); the project's issue tracker; any
review, ruling record, census, or commentary; conformance vectors or test corpora authored by
the specification's author; companion or teaching documents; or any summary that characterizes
the specification's defects. If you already hold knowledge of this specification from any of
those sources, **say so in your report** rather than proceeding quietly. Declaring it is
recoverable; concealing it is not.

You may use the KERI, ACDC and CESR specifications as substrate references.

**Never resolve an ambiguity by asking anyone.** A shared reading destroys the only evidence
this project exists to produce.

## Your surface

**Custos 4.2 §18 (The GEL grammar) and §19 (The compact receipt form and its gates).**

Work through everything these two sections require a conforming evaluator to be able to decide.
Their own paragraph headings are the map: the spine, event identity, canonical order, the two
tracks, the bootstrap, designation and membership, genus, and the compact form gate in §18; the
three ordered gates, the rule the first gate turns on, and the ground beneath them in §19.

Read the whole document first — these sections presuppose Chapter 1 and the definitions — but
your findings are about §18 and §19.

## What you produce, and what you do not

**Do not write code.** No implementation, no test suite, no scaffolding. Your budget is spent on
the reading.

Produce two things.

**1. A readings register.** One entry per place where the text admits more than one lawful
reading. Each entry:

- The span, quoted, with line numbers.
- Each lawful reading, stated as a rule an implementer could follow.
- The specification lines that permit each — a citation that does not support what it is
  attached to is worse than none.
- The one you pin, and why the other is rejected.
- **Whether the readings produce different results on some input.** Mark those DIVERGENT. They
  are worth several times an entry where the text is merely loose but every reading computes the
  same thing. Log the loose ones anyway, briefly.

If you believe the reading the text compels is the *worse* one, pin it anyway and say so. Reading
a restriction into a span that does not carry it is legislating, which the fold is forbidden to
do.

**2. Cases.** For every DIVERGENT entry, at least one concrete case, in this shape:

```json
{
  "id": "E-18-01",
  "surface": "§18",
  "given": { "...": "fixture symbols, fully concrete" },
  "then":  { "...": "the expected result, field by field" },
  "discriminates": "one sentence: what an engine on the other reading produces instead"
}
```

There is no wire format to write bytes in — the carriage encoding has not ratified — so a case is
concrete at the *semantic* layer: fixed symbols, named spans, the expected result stated field by
field. State your fixture symbols once, up front, and keep them fixed. The fields inside `given`
and `then` are **your** choice; use the shape your own reading makes natural rather than
inventing a neutral schema.

These cases will be executed against independently written engines. A case whose expected value
an engine contradicts is a finding against the specification, not a bug report against the
engine — which is why stating the expected value field by field, with nothing left implicit,
is the whole job.

## Your budget

You are rate-limited and the other legs are not. Spend accordingly: prioritise DIVERGENT
entries and the cases that discriminate them, and be terse everywhere else. A short register of
real forks beats a long one padded with loose prose. If you run short, drop §19's later gates
before you drop anything in §18.

## Your report

Close with:

- Which readings diverge on some input, and the discriminating input for each.
- Where the specification made you **invent** something it does not state. Name it as an
  invention, not as a design choice.
- What a conforming implementer could not build at all from this text, and what the document
  would have to say for them to build it.
- Anything you knew about this specification before you read it here.
