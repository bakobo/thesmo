"""thesmo — a Gever for Custos-governed domains.

A Gever folds a governance event log, in the context of the key and registry
logs it cites, to a Constitution. thesmo is built blind from the Custos
specification's committed bytes, as an instrument for finding the places where
that specification underdetermines a conforming engine.

Layout (this.i @q6hqa4):

* ``thesmo.core`` — the fold itself. Pure. Imports nothing from any KERI
  library, because Custos §1.4 axiom 2 closes the fold's inputs at exactly
  three committed values.
* ``thesmo.substrate`` — the sole substrate boundary (M3). Turns CESR streams
  into the closed triple ``core`` consumes.
"""

__all__ = ["__version__"]

__version__ = "0.0.0"
