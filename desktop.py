"""The desktop interface: a window showing ui.html, talking to Python via Api."""

import sys
from pathlib import Path

from notes import (
    Note, add_note, delete_note, extract_code, find_by_id, find_note,
    set_tags, title_from_body, update_note,
)
from embeddings import EMBEDDINGS_FILE, sync_embeddings
from runner import run_code
from storage import NOTES_FILE, load, note_to_dict, save


def resource_path(name: str) -> Path:
    """Where bundled files live. PyInstaller unpacks them into sys._MEIPASS."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return base / name


class Api:
    """Every public method here can be called from JavaScript as
    pywebview.api.<method>(...). Notes are identified by their id."""

    def __init__(self, path: Path = NOTES_FILE, embeddings_path: Path = EMBEDDINGS_FILE):
        self.path = path
        self.embeddings_path = embeddings_path

    def _save(self, notes: list[Note]) -> None:
        """Save the notes, then bring their embeddings up to date."""
        save(notes, self.path)
        sync_embeddings(notes, self.embeddings_path)

    def get_notes(self) -> list[dict]:
        return [note_to_dict(note) for note in load(self.path)]

    def search(self, text: str) -> list[dict]:
        return [note_to_dict(note) for note in find_note(load(self.path), text)]

    def create_note(self, title: str, body: str) -> dict:
        note = Note(title.strip() or title_from_body(body), body)
        self._save(add_note(load(self.path), note))
        return note_to_dict(note)

    def delete_note(self, note_id: str) -> bool:
        notes = load(self.path)
        note = find_by_id(notes, note_id)
        if note is None:
            return False
        self._save(delete_note(notes, note))
        return True

    def set_tags(self, note_id: str, tags: list[str]) -> dict | None:
        notes = load(self.path)
        note = find_by_id(notes, note_id)
        if note is None:
            return None
        updated = set_tags(note, tags)
        self._save(update_note(notes, note, updated))
        return note_to_dict(updated)

    def run_code(self, note_id: str) -> list[dict]:
        note = find_by_id(load(self.path), note_id)
        if note is None:
            return []
        return [
            {"language": language, "code": code, "output": run_code(language, code)}
            for language, code in extract_code(note.body)
        ]


def main() -> None:
    import webview  # imported here so tests can use Api without pywebview

    # Embed any notes that don't have a vector yet (only slow the first time).
    sync_embeddings(load(NOTES_FILE))
    webview.create_window("Math/CS Notes", url=str(resource_path("ui.html")), js_api=Api())
    webview.start()


if __name__ == "__main__":
    main()
