"""The fold. Pure, and kept that way by test.

Custos §1.4 axiom 2: "the inputs are exactly three, closed: the committed
evidence bundle, the committed law head, and the appraisal position. No other
input may influence the result."

That closure is why this package needs no KERI library. Everything below is a
function of committed values handed in by the caller; producing those values
from CESR streams is ``thesmo.substrate``'s job, and the boundary is enforced
mechanically by ``tests/test_core_purity.py`` rather than by convention.

## The modules

| Module | Custos sections | What it types |
|---|---|---|
| ``errors`` | §7.5 | what the fold raises, and how refusal travels |
| ``triple`` | §1.4 axiom 2, §7.3 "Inputs", §17 | the closed three-input type |
| ``finding`` | §7.1, §7.2, §7.3 "Required payloads", §7.5 | the four-valued codomain |
| ``ordering`` | §7.3 "The evidence ordering", "Canonical selection" | both orderings |
| ``transitions`` | §7.3 | the complete transition system |
| ``currents`` | §7.4 | the ladder, the two currents, first-seen survival |

## What a reader should distrust

M1 was implemented **blind**, from the committed bytes of Custos 4.1 and the
ratified 4.0 kernel and nothing else (this.i @qmz2o4). Twenty-seven places where
those bytes admit more than one conforming engine were found, and every one is
recorded in ``docs/readings-beta.md`` with the reading we pinned and the reading
we rejected. Where this code looks confident, the register is where to check
whether it has any right to be.

Two of those readings resolve outright contradictions inside the specification
and are the most likely to be wrong:

- ``ordering.select_defeat`` — §7.3 requires the "lexicographic minimum" of a
  tuple whose last component, when empty, "orders last". Both cannot hold.
- ``currents.first_seen`` — §7.4's "first-seen survives" is one of the five
  walls §1.4 imports, and read the substrate's way it contradicts axiom 4's
  "no ambient order", stated on the same page.
"""

# The substrate-forbidden list the purity test enforces. Adding a name here is
# a decision that belongs in this.i before the import that motivates it.
FORBIDDEN_IMPORTS = frozenset({"keri", "keria", "cesride", "parside", "hio"})
