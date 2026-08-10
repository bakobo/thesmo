# Readings — leg <NAME>, <milestone> <surface>

Every place where Custos underdetermined what I was building, recorded at the moment I hit it.
Line numbers are into the one specification file I was given and the only one I read:

- `4.2` = the ratified Custos 4.2 edition of record, sha256 `68cc5c9b…2b2775a` of the bytes I held

Each entry states the span, the lawful readings, the one I pinned, and — the part that matters —
whether the readings **produce different results on some input**. Entries marked **DIVERGENT** do;
two conforming implementations can disagree there on committed bytes. Entries marked *convergent*
are places where the text is loose but every lawful reading computes the same thing; they are
logged anyway, because a logged non-ambiguity costs almost nothing.

Each entry has a `this.i` node; the node id is given so the register and the tree cross-reference.

---

## Part I — pinned readings

### R1 — <the question, as a question> **DIVERGENT** (@<node-id>)

4.2 §<n>, lines <a>–<b>:

> <the span, quoted exactly>

<Any second span that bears on it, quoted and cited the same way.>

- **Reading A** — <the rule an implementer would follow under this reading>.
- **Reading B** — <the rule an implementer would follow under this reading>.

**Pinned: <A|B>.** <Why. Cite the lines that compel it. Name what you reject and why the
rejection follows from the text rather than from taste. If you pinned the reading you consider
worse because the text compels it, say so here.>

**Divergence:** <the input on which the two readings compute different results, and what each
computes. If the entry is *convergent*, say instead why every lawful reading lands in the same
place.>

### R2 — <…> *convergent* (@<node-id>)

<Same shape. Convergent entries may be brief.>

---

## Part II — inventions

Where the specification required something of me and did not say what, so I supplied it. These
are not readings of the text; they are holes in it.

### I1 — <what I had to invent> (@<node-id>)

<What the text requires, what it does not say, what I supplied, and what a different
implementer would plausibly have supplied instead.>

---

## Part III — could not build

Where I could not proceed at all, and what the document would have to say for me to.

### S1 — <what I could not build> (@<node-id>)
