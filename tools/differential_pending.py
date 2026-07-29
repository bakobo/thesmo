"""Run one committed input through whichever engine is on sys.path.

Both engines were written blind from the same ratified bytes. Both agree that
the specification underdetermines the deduplication key of a pending finding's
typed requirement set (§7.3 L1048-1051 names subject/kind/citing-clauses;
§7.2 L1007-1008 additionally makes the species mandatory per element). They
resolved it in opposite directions. This constructs the discriminating input
both registers independently describe and prints what each returns.

Input: one question requiring subject S under kind K, cited by clause C, where
the evidence is both `absent` and inside an open recovery window.
"""

import dataclasses
import sys

from thesmo.core import finding as F
from thesmo.core import ordering as O

RE = F.RequirementElement
SP = F.PendingSpecies

# The two engines named their canonicalization differently; the semantics under
# test are the same.
canon = getattr(O, "canonical_requirement_set", None) or O.canonical_requirements

names = [f.name for f in dataclasses.fields(RE)]


def element(species):
    """Build the same logical element under either engine's field set.

    Only the four fields the specification names are supplied. Any
    engine-specific extra is left at its own default, so the two inputs are
    identical in everything §7.2 and §7.3 actually require.
    """
    kwargs = {}
    for f in dataclasses.fields(RE):
        name = f.name
        if name == "subject":
            kwargs[name] = "S"
        elif name == "kind":
            kwargs[name] = "K"
        elif "clause" in name:
            kwargs[name] = ("C",)
        elif name == "species":
            kwargs[name] = species
        # else: leave it at the engine's own default.
    return RE(**kwargs)


elements = [element(SP.ABSENT), element(SP.WINDOW_OPEN)]

result = canon(elements)

print(f"engine fields : {names}")
print(f"input         : 2 elements, subject=S kind=K clauses=('C',),")
print(f"                species = absent, window-open")
print(f"OUTPUT SIZE   : {len(result)}")
for i, el in enumerate(result):
    print(f"  [{i}] subject={el.subject!r} kind={el.kind!r} species={el.species}")
print(f"cure paths a consumer can read off this finding: "
      f"{sorted({str(el.species) for el in result})}")
