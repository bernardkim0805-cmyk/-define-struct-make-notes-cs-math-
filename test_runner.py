import shutil

import pytest

from desktop import Api
from runner import run_code


def test_run_python():
    assert run_code("python", "print(1 + 2)").strip() == "3"


def test_run_python_error_shows_traceback():
    output = run_code("python", "1 / 0")
    assert "ZeroDivisionError" in output
    assert "exited with code" in output


def test_run_python_no_output():
    assert run_code("python", "x = 1") == "(no output)"


def test_run_python_timeout():
    output = run_code("python", "while True: pass", timeout=1)
    assert output.startswith("Stopped")


def test_run_unknown_language():
    assert "Unsupported language" in run_code("cobol", "DISPLAY 'HI'")


@pytest.mark.skipif(shutil.which("racket") is None, reason="racket not installed")
def test_run_racket():
    assert run_code("racket", "(display (+ 1 2))").strip() == "3"


# --- desktop Api (uses a temporary notes file, never your real one) ---------

def test_api_by_id(tmp_path):
    api = Api(tmp_path / "notes.json")
    created = api.create_note("", "first words of body\n/start_python\nprint('ok')\n/end_python")
    assert created["title"] == "first words of"

    note_id = created["id"]
    assert api.set_tags(note_id, ["a", " b"])["tags"] == ["a", "b"]
    assert api.search("words")[0]["id"] == note_id
    assert [r["output"].strip() for r in api.run_code(note_id)] == ["ok"]

    assert api.delete_note(note_id) is True
    assert api.get_notes() == []
    assert api.delete_note(note_id) is False
    assert api.set_tags("missing", ["x"]) is None
    assert api.run_code("missing") == []
