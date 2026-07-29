"""Tests for the edition comparator.

Fixtures are miniature stand-ins for the real specification, not excerpts of it:
the comparator's job is structural, so it can be specified without quoting bytes
the repository does not own.
"""

import pathlib

import pytest

from thesmo import editions

OLDER = """# Custos 4.0

## 1. Scope

Scope prose.

## 6. The finding codomain

### 6.1 The type and its values

The codomain has four
values, wrapped narrowly.

### 6.3 The transition system

Section 6.3 governs transitions.

## 7. Standing

Standing prose.
"""

NEWER = """# Custos 4.1

## 1. Scope

Scope prose.

## 7. The finding codomain

### 7.1 The type and its values

The codomain has four values, wrapped widely.

### 7.3 The transition system

Section 7.3 governs transitions, and adds a clause.

## 8. Standing

Standing prose.
"""


def test_sha256_pins_exact_bytes():
    assert editions.sha256("") == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert editions.sha256("a") != editions.sha256("b")


def test_extract_section_stops_at_the_next_top_level_heading():
    section = editions.extract_section(OLDER, 6)
    assert section.startswith("## 6. The finding codomain")
    assert "Standing prose." not in section
    assert "### 6.3 The transition system" in section


def test_extract_section_runs_to_end_of_document():
    section = editions.extract_section(OLDER, 7)
    assert section.startswith("## 7. Standing")
    assert section.rstrip().endswith("Standing prose.")


def test_extract_section_raises_rather_than_returning_empty():
    # A silently empty section would make a failed extraction look like a
    # clean diff, which is the one failure mode this tool must not have.
    with pytest.raises(LookupError, match="no top-level section 99"):
        editions.extract_section(OLDER, 99)


def test_renumber_rewrites_section_numbers_and_subsections():
    assert editions.renumber("## 6. x\n### 6.1 y\n", 6, 7) == "## 7. x\n### 7.1 y\n"


def test_renumber_rewrites_prose_cross_references():
    assert editions.renumber("see 6.3 and §6.10", 6, 7) == "see 7.3 and §7.10"


def test_renumber_leaves_bare_numerals_alone():
    # The whole output of this tool is a difference, so fabricating one by
    # rewriting a count or a duration is the worst bug available to it.
    assert editions.renumber("6 months, 16 values, a 6 in prose", 6, 7) == (
        "6 months, 16 values, a 6 in prose"
    )


def test_renumber_leaves_other_sections_alone():
    assert editions.renumber("## 5. x\n### 16.1 y", 6, 7) == "## 5. x\n### 16.1 y"


def test_normalize_joins_wrapped_paragraphs():
    assert editions.normalize("one two\nthree\n\nfour\n") == ["one two three", "four"]


def test_normalize_drops_blank_runs():
    assert editions.normalize("\n\n  \n\nalpha\n\n\n\nbeta\n\n") == ["alpha", "beta"]


def changed_lines(diff):
    """Only the +/- lines, dropping headers and context."""
    return [
        line
        for line in diff
        if line[:1] in "+-" and not line.startswith(("---", "+++"))
    ]


def test_compare_ignores_rewrapping_and_renumbering():
    changed = changed_lines(editions.compare(OLDER, NEWER, older_label="a", newer_label="b"))
    body = "\n".join(changed)
    # "wrapped narrowly" -> "wrapped widely" is a real change and must show.
    assert "wrapped widely" in body
    assert "adds a clause" in body
    # The differing wrap widths and the 6->7 renumbering must not: a heading
    # that only moved number is unchanged content and may appear as context,
    # but never as an addition or a deletion.
    assert not [line for line in changed if "The type and its values" in line]
    assert not [line for line in changed if "The finding codomain" in line]


# The same evaluator section as OLDER's §6, renumbered to §7 and rewrapped:
# structurally identical, textually not. Written out rather than derived from
# OLDER by string substitution, so the fixture cannot drift into agreeing with
# the implementation by construction.
SAME = """# Custos 4.1

## 1. Scope

Scope prose.

## 7. The finding codomain

### 7.1 The type and its values

The codomain has four values, wrapped narrowly.

### 7.3 The transition system

Section 7.3 governs transitions.

## 8. Standing

Standing prose.
"""


def test_compare_reports_nothing_when_sections_match():
    assert editions.compare(OLDER, SAME, older_label="a", newer_label="b") == []


def _write_spec(tmp_path: pathlib.Path, older: str, newer: str) -> pathlib.Path:
    spec = tmp_path / "spec"
    spec.mkdir()
    (spec / "custos-4.0-kernel-draft.md").write_text(older, encoding="utf-8")
    (spec / "custos-4.1.md").write_text(newer, encoding="utf-8")
    return tmp_path


def test_main_exits_2_when_the_bytes_are_absent(tmp_path, capsys):
    assert editions.main(["--custos", str(tmp_path)]) == 2
    assert "no specification bytes" in capsys.readouterr().err


def test_main_exits_1_and_prints_the_diff_when_editions_differ(tmp_path, capsys):
    root = _write_spec(tmp_path, OLDER, NEWER)
    assert editions.main(["--custos", str(root)]) == 1
    out = capsys.readouterr().out
    assert "sha256" in out
    assert "adds a clause" in out


def test_main_exits_0_when_editions_agree(tmp_path, capsys):
    root = _write_spec(tmp_path, OLDER, SAME)
    assert editions.main(["--custos", str(root)]) == 0
    assert "structurally identical" in capsys.readouterr().out
