"""The fold. Pure, and kept that way by test.

Custos §1.4 axiom 2: "the inputs are exactly three, closed: the committed
evidence bundle, the committed law head, and the appraisal position. No other
input may influence the result."

That closure is why this package needs no KERI library. Everything below is a
function of committed values handed in by the caller; producing those values
from CESR streams is ``thesmo.substrate``'s job, and the boundary is enforced
mechanically by ``tests/test_core_purity.py`` rather than by convention.

Nothing is implemented yet. M1 fills in the finding codomain, the transition
system, and canonical ordering — and per this.i @qmz2o4 it must be filled in by
an implementer who has read the Custos specification and nothing else.
"""

# The substrate-forbidden list the purity test enforces. Adding a name here is
# a decision that belongs in this.i before the import that motivates it.
FORBIDDEN_IMPORTS = frozenset({"keri", "keria", "cesride", "parside", "hio"})
