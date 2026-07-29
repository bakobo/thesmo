"""Compare the evaluator sections of two Custos editions.

Custos 4.1 §1.4 binds the ratified 4.0 kernel's evaluator sections into 4.1 by
committed digest referent — "the complete transition system among the four
finding values and its refusal of backward edges, the canonical ordering and
selection of evidence, the distinct upward currents of defeat and duplicity,
first-seen survival, and the rule that acts consumed as grounds require
committed receipts." Meanwhile 4.1 §7.3 presents itself as "its complete
enumeration" of that same transition system.

Both cannot be the sole authority. An implementer who reads only the edition of
record may therefore build a non-conforming engine and have no way to tell
(this.i @ultpjo). This module makes the comparison mechanical and re-runnable
against a caller-supplied checkout, so the answer is derived from committed
bytes rather than asserted — which is the posture Custos asks of its own
readers.

It reads specification bytes and compares them structurally. It does not
interpret them, so it is safe for a reader who is not blind under @qmz2o4.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import pathlib
import re
import sys

#: Where the evaluator lives in each edition. 4.0 numbers it §6, 4.1 §7; the
#: spine inversion between editions moved the section without renaming it.
EVALUATOR_SECTION = {"4.0": 6, "4.1": 7}

_HEADING = re.compile(r"^## (\d+)\.?\s", re.MULTILINE)


def sha256(text: str) -> str:
    """Digest of the exact bytes, so a caller can pin what was compared."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_section(text: str, number: int) -> str:
    """Return top-level section ``number`` — its heading through the next one.

    Raises ``LookupError`` rather than returning empty, because a silently
    empty section would make a diff look clean when extraction had simply
    failed.
    """
    start = None
    for match in _HEADING.finditer(text):
        if start is None:
            if int(match.group(1)) == number:
                start = match.start()
            continue
        return text[start : match.start()]
    if start is None:
        raise LookupError(f"no top-level section {number} in this edition")
    return text[start:]


def renumber(section: str, frm: int, to: int) -> str:
    """Rewrite ``frm.x`` section numbers to ``to.x`` for structural comparison.

    Without this the diff is dominated by the renumbering the spine inversion
    caused, and the substantive differences are invisible inside the noise.

    Only *section references* are rewritten — a subsection number (``6.3``,
    whether in a heading or in prose) and a bare section number at the head of a
    Markdown heading. A bare numeral is left alone: rewriting every ``6`` would
    turn "six months" prose or a count into a fabricated difference, which in a
    tool whose whole output is a difference is the worst available bug.
    """
    subsection = re.compile(rf"\b{frm}\.(\d+)")
    heading = re.compile(rf"(?m)^(#{{1,6}} ){frm}\.(?!\d)")
    return heading.sub(rf"\g<1>{to}.", subsection.sub(rf"{to}.\1", section))


def normalize(section: str) -> list[str]:
    """Collapse wrapping so a reflowed paragraph is not read as a rewrite.

    The editions are hard-wrapped at different widths, so a line-by-line diff of
    raw text reports every paragraph as changed. Joining each paragraph into one
    line compares wording rather than typesetting.
    """
    paragraphs = re.split(r"\n\s*\n", section.strip())
    return [" ".join(p.split()) for p in paragraphs if p.strip()]


def compare(older: str, newer: str, *, older_label: str, newer_label: str) -> list[str]:
    """Unified diff of two editions' evaluator sections, structurally aligned."""
    old_section = renumber(
        extract_section(older, EVALUATOR_SECTION["4.0"]),
        EVALUATOR_SECTION["4.0"],
        EVALUATOR_SECTION["4.1"],
    )
    new_section = extract_section(newer, EVALUATOR_SECTION["4.1"])
    return list(
        difflib.unified_diff(
            normalize(old_section),
            normalize(new_section),
            fromfile=older_label,
            tofile=newer_label,
            lineterm="",
            n=1,
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="thesmo-edition-diff",
        description=__doc__.split("\n\n")[0],
    )
    parser.add_argument(
        "--custos",
        type=pathlib.Path,
        required=True,
        help="path to a checkout of the Custos specification repository",
    )
    args = parser.parse_args(argv)

    older_path = args.custos / "spec" / "custos-4.0-kernel-draft.md"
    newer_path = args.custos / "spec" / "custos-4.1.md"
    for path in (older_path, newer_path):
        if not path.is_file():
            print(f"error: no specification bytes at {path}", file=sys.stderr)
            return 2

    older = older_path.read_text(encoding="utf-8")
    newer = newer_path.read_text(encoding="utf-8")
    print(f"# 4.0 {older_path.name} sha256 {sha256(older)}")
    print(f"# 4.1 {newer_path.name} sha256 {sha256(newer)}")

    diff = compare(older, newer, older_label="custos-4.0 §6", newer_label="custos-4.1 §7")
    if not diff:
        print("# evaluator sections are structurally identical after renumbering")
        return 0
    print("\n".join(diff))
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
