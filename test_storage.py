import json
from datetime import date

from notes import Note
from storage import dict_to_note, load, note_to_dict, save


def test_note_dict_round_trip():
    note = Note("t", "b", ["x"], date(2025, 5, 6))
    data = note_to_dict(note)
    assert data == {
        "id": note.id, "title": "t", "body": "b",
        "tags": ["x"], "last_edited": "2025-05-06",
    }
    assert dict_to_note(data) == note


def test_save_load_round_trip(tmp_path):
    path = tmp_path / "notes.json"
    notes = [
        Note("Calc", "$$\\int_0^1 x\\,dx$$", ["math"], date(2025, 1, 2)),
        Note("Code", "/start_python\nprint('hi')\n/end_python"),
    ]
    save(notes, path)
    assert load(path) == notes


def test_save_load_empty(tmp_path):
    path = tmp_path / "notes.json"
    save([], path)
    assert load(path) == []


def test_load_missing_file(tmp_path):
    assert load(tmp_path / "nope.json") == []


def test_save_creates_folder(tmp_path):
    path = tmp_path / "new" / "folder" / "notes.json"
    save([Note("t", "b")], path)
    assert path.exists()
    assert not path.with_suffix(".json.tmp").exists()


def test_load_migrates_notes_without_id(tmp_path):
    path = tmp_path / "notes.json"
    old = [
        {"title": "a", "body": "", "tags": [], "last_edited": "2024-01-01"},
        {"title": "b", "body": "", "last_edited": "2024-01-02"},  # no tags either
    ]
    path.write_text(json.dumps(old))

    first = load(path)
    assert all(note.id for note in first)
    assert first[0].id != first[1].id
    assert first[1].tags == []
    # The ids were written back, so loading again gives the same ids.
    assert [n.id for n in load(path)] == [n.id for n in first]
    assert all("id" in d for d in json.loads(path.read_text()))
