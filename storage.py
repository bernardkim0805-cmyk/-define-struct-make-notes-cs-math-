import json
from notes import Note
from datetime import date 

def note_to_dict(note: Note) -> dict:
    return {
        "title": note.title,
        "body": note.body,
        "tags": note.tags,
        "last_edited": note.last_edited.isoformat()
    }

def dict_to_note(data: dict) -> Note:
    return Note(
        title=data["title"],
        body=data["body"],
        tags=data["tags"],
        last_edited=date.fromisoformat(data["last_edited"])
    )

def save(nb: list[Note], path: str) -> None:
    with open (path, "w") as f:
        json.dump([note_to_dict(note) for note in nb], f, indent=4)

def load(path:str) -> list[Note]:
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return [dict_to_note(note_data) for note_data in data]
    except FileNotFoundError:
        return []