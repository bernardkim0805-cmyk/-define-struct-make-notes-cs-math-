"""Saving and loading notes as JSON."""

import json
import os
from datetime import date
from pathlib import Path

from notes import Note, new_id

# The one place the notes file location is defined. Both interfaces import it.
APP_DIR = Path.home() / "MathCSNotes"
NOTES_FILE = APP_DIR / "notes.json"


def note_to_dict(note: Note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "tags": list(note.tags),
        "last_edited": note.last_edited.isoformat(),
    }


def dict_to_note(data: dict) -> Note:
    """Build a Note from saved data. Notes saved before ids existed get a new id."""
    return Note(
        title=data["title"],
        body=data["body"],
        tags=list(data.get("tags", [])),
        last_edited=date.fromisoformat(data["last_edited"]),
        id=data.get("id") or new_id(),
    )


def save(nb: list[Note], path: str | Path = NOTES_FILE) -> None:
    """Write to a temporary file first, then swap it in, so a crash halfway
    through saving can't leave a half-written notes file behind."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump([note_to_dict(note) for note in nb], f, indent=4)
    os.replace(tmp, path)


def load(path: str | Path = NOTES_FILE) -> list[Note]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    nb = [dict_to_note(note_data) for note_data in data]
    # Migration: if any old note had no id, save straight away so the new
    # ids stick. Otherwise every load would invent different ids.
    if any(not note_data.get("id") for note_data in data):
        save(nb, path)
    return nb
