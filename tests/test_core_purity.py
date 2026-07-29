"""The core/ purity fitness function.

Custos §1.4 axiom 2 closes the fold's inputs at three committed values, so the
evaluator can be — and per this.i @q6hqa4 must be — free of any KERI library.
That is an architectural claim, and an architectural claim defended only by a
comment decays the first time someone needs a Diger in a hurry.

So it is defended here instead. This test reads every module under
``thesmo.core`` as source and fails if any of them imports the substrate,
directly or transitively-by-name. It deliberately inspects the AST rather than
the import graph at runtime: a lazy import inside a function body would evade a
runtime check, and a lazy import is exactly how this boundary would erode.
"""

import ast
import pathlib

import pytest

from thesmo.core import FORBIDDEN_IMPORTS

CORE = pathlib.Path(__file__).resolve().parent.parent / "src" / "thesmo" / "core"


def core_modules():
    """Every source file under core/, so new ones are covered without edits."""
    return sorted(CORE.rglob("*.py"))


def imported_roots(tree):
    """Top-level package name of every import in a parsed module.

    ``import keri.core.coring`` and ``from keri import coring`` both yield
    ``keri``; a relative import yields nothing, since it cannot reach outside
    the package.
    """
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.partition(".")[0])
        elif isinstance(node, ast.ImportFrom):
            # node.module is None for `from . import x`; level > 0 is relative.
            if node.level == 0 and node.module is not None:
                roots.add(node.module.partition(".")[0])
    return roots


def test_core_package_exists():
    """A vacuous purity test would pass forever after a bad refactor."""
    assert CORE.is_dir()
    assert core_modules(), "core/ has no modules; the purity test would be vacuous"


@pytest.mark.parametrize("path", core_modules(), ids=lambda p: p.name)
def test_core_module_does_not_import_substrate(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    offenders = imported_roots(tree) & FORBIDDEN_IMPORTS
    assert not offenders, (
        f"{path.relative_to(CORE.parent)} imports {sorted(offenders)}. "
        "core/ is pure by decision (this.i @q6hqa4): the fold's inputs are closed "
        "at three committed values, so it needs no substrate. Put the substrate "
        "call in thesmo.substrate and hand core/ the committed values instead. "
        "If that is genuinely wrong, change this.i first — not this test."
    )


def test_imported_roots_reads_all_three_import_shapes():
    """The helper's own branches: absolute, from-import, and relative."""
    tree = ast.parse(
        "import keri.core.coring\n"
        "from hio import help\n"
        "from . import sibling\n"
        "from .relative import thing\n"
    )
    assert imported_roots(tree) == {"keri", "hio"}
