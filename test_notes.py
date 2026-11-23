from datetime import date

import pytest

from notes import (
    Note, add_note, add_notes, add_tag, append_note_body, create_notebook,
    delete_note, edit_note, extract_code, find_by_id, find_by_title,
    find_note, remove_tag, set_tags, sort_notes, title_from_body, update_note,
)

OLD = date(2024, 1, 1)


@pytest.fixture
def nb():
    return [
        Note("Calculus", "limits and $\\epsilon$", ["math"], date(2025, 3, 1)),
        Note("Racket", "(define x 1)", ["cs", "racket"], date(2025, 1, 15)),
        Note("algebra", "groups", [], date(2025, 2, 10)),
    ]


# --- Note -----------------------------------------------------------------

def test_note_defaults():
    note = Note("t", "b")
    assert note.tags == []
    assert note.last_edited == date.today()
    assert isinstance(note.id, str) and len(note.id) == 36


def test_notes_get_unique_ids():
    assert Note("t", "b").id != Note("t", "b").id


def test_default_tags_not_shared():
    a, b = Note("a", ""), Note("b", "")
    a.tags.append("x")
    assert b.tags == []


# --- title_from_body / create_notebook --------------------------------------

def test_title_from_body():
    assert title_from_body("one two three four") == "one two three"
    assert title_from_body("  ") == "Untitled"


def test_create_notebook():
    assert create_notebook() == []


# --- add_note / add_notes ---------------------------------------------------

def test_add_note_returns_new_list(nb):
    note = Note("new", "")
    result = add_note(nb, note)
    assert result[-1] is note
    assert len(nb) == 3  # original untouched


def test_add_note_to_empty():
    note = Note("only", "")
    assert add_note([], note) == [note]


def test_add_notes(nb):
    extra = [Note("x", ""), Note("y", "")]
    result = add_notes(nb, extra)
    assert result[-2:] == extra
    assert len(nb) == 3


def test_add_notes_empty(nb):
    assert add_notes(nb, []) == nb


# --- find_note / find_by_id / find_by_title ---------------------------------

def test_find_by_title_text(nb):
    assert [n.title for n in find_note(nb, "calc")] == ["Calculus"]


def test_find_is_case_insensitive(nb):
    assert [n.title for n in find_note(nb, "ALGEBRA")] == ["algebra"]


def test_find_in_body(nb):
    assert [n.title for n in find_note(nb, "define")] == ["Racket"]


def test_find_in_tags(nb):
    assert [n.title for n in find_note(nb, "cs")] == ["Racket"]


def test_find_by_date(nb):
    assert [n.title for n in find_note(nb, "2025-02")] == ["algebra"]


def test_find_no_match(nb):
    assert find_note(nb, "zebra") == []


def test_find_in_empty_notebook():
    assert find_note([], "x") == []


def test_find_by_id(nb):
    assert find_by_id(nb, nb[1].id) is nb[1]
    assert find_by_id(nb, "missing") is None


def test_find_by_title_exact(nb):
    assert find_by_title(nb, "Racket") is nb[1]
    assert find_by_title(nb, "racket") is None
    assert find_by_title([], "Racket") is None


# --- delete_note / update_note / edit_note ----------------------------------

def test_delete_note(nb):
    result = delete_note(nb, nb[0])
    assert [n.title for n in result] == ["Racket", "algebra"]
    assert len(nb) == 3


def test_delete_only_removes_that_note():
    a, b = Note("same", "same"), Note("same", "same")
    assert delete_note([a, b], a) == [b]


def test_delete_missing_note(nb):
    assert delete_note(nb, Note("ghost", "")) == nb


def test_update_note(nb):
    new = edit_note(nb[1], title="Racket 2")
    result = update_note(nb, nb[1], new)
    assert result[1].title == "Racket 2"
    assert nb[1].title == "Racket"


def test_update_missing_note(nb):
    assert update_note(nb, Note("ghost", ""), Note("x", "")) == nb


def test_edit_note_keeps_id_and_tags(nb):
    edited = edit_note(nb[1], body="new body")
    assert edited.id == nb[1].id
    assert edited.tags == ["cs", "racket"]
    assert edited.title == "Racket"
    assert edited.body == "new body"
    assert edited.last_edited == date.today()
    assert edited.tags is not nb[1].tags


# --- sort_notes -------------------------------------------------------------

def test_sort_by_title_ignores_case(nb):
    assert [n.title for n in sort_notes(nb, "title")] == ["algebra", "Calculus", "Racket"]


@pytest.mark.parametrize("key", ["date", "last_edited"])
def test_sort_by_date(nb, key):
    assert [n.title for n in sort_notes(nb, key)] == ["Racket", "algebra", "Calculus"]


def test_sort_does_not_change_input(nb):
    sort_notes(nb, "title")
    assert nb[0].title == "Calculus"


def test_sort_empty():
    assert sort_notes([], "title") == []


def test_sort_bad_key(nb):
    with pytest.raises(ValueError):
        sort_notes(nb, "colour")


# --- tags -------------------------------------------------------------------

def test_add_tag_returns_new_note(nb):
    result = add_tag(nb[0], "proofs")
    assert result.tags == ["math", "proofs"]
    assert nb[0].tags == ["math"]
    assert result.id == nb[0].id


def test_add_tag_duplicate_or_blank(nb):
    assert add_tag(nb[0], "math").tags == ["math"]
    assert add_tag(nb[0], "  ").tags == ["math"]


def test_remove_tag(nb):
    assert remove_tag(nb[1], "cs").tags == ["racket"]
    assert nb[1].tags == ["cs", "racket"]


def test_remove_missing_tag(nb):
    assert remove_tag(nb[1], "nope").tags == ["cs", "racket"]


def test_set_tags_cleans_input(nb):
    assert set_tags(nb[0], [" a", "b ", "", "a"]).tags == ["a", "b"]
    assert set_tags(nb[0], []).tags == []
    assert nb[0].tags == ["math"]


# --- append_note_body -------------------------------------------------------

def test_append_uses_real_newline():
    note = Note("t", "first", ["x"], OLD)
    result = append_note_body(note, "second")
    assert result.body == "first\nsecond"
    assert result.tags == ["x"]
    assert result.id == note.id
    assert result.last_edited == date.today()
    assert note.body == "first"


def test_append_to_empty_body():
    assert append_note_body(Note("t", ""), "hi").body == "hi"


# --- extract_code -----------------------------------------------------------

def test_extract_single_python_block():
    body = "intro\n/start_python\nprint(1)\nprint(2)\n/end_python\noutro"
    assert extract_code(body) == [("python", "print(1)\nprint(2)")]


def test_extract_python_and_racket_in_order():
    body = (
        "/start_racket\n(+ 1 2)\n/end_racket\n"
        "text $x^2$\n"
        "/start_python\nx = 1\n/end_python"
    )
    assert extract_code(body) == [("racket", "(+ 1 2)"), ("python", "x = 1")]


def test_extract_keeps_indentation_and_allows_spaced_markers():
    body = "  /start_python  \ndef f():\n    return 1\n/end_python"
    assert extract_code(body) == [("python", "def f():\n    return 1")]


def test_extract_no_blocks():
    assert extract_code("just $math$ here") == []
    assert extract_code("") == []


def test_extract_unclosed_block_ignored():
    assert extract_code("/start_python\nprint(1)") == []


def test_extract_wrong_end_marker_is_part_of_code():
    body = "/start_python\n/end_racket\n/end_python"
    assert extract_code(body) == [("python", "/end_racket")]


def test_extract_empty_block():
    assert extract_code("/start_python\n/end_python") == [("python", "")]
