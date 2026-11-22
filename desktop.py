import webview
from pathlib import Path
from storage import load, note_to_dict, save 
from notes import Note, add_note, find_note, delete_note, update_note


NOTES_FILE = Path.home() / "MathCSnotes" / "notes.json"
NOTES_FILE.parent.mkdir(exist_ok=True)


class Api:
    def get_notes(self):
        return [note_to_dict(note) for note in load(NOTES_FILE)]

    def create_blank(self):
        note = load(NOTES_FILE)
        note = add_note(note, Note("New Note", ""))
        save(note, NOTES_FILE)
        return len(note) - 1  # return the index 

    def create_note(self, title, body):
        note = load(NOTES_FILE)
        note = add_note(note, Note(title, body))
        save(note, NOTES_FILE)

    def delete(self, title):
        notes = load(NOTES_FILE)
        note_to_del = (next((note for note in notes if note.title == title), None))
        if note_to_del:
            notes = delete_note(notes, note_to_del)
            save(notes, NOTES_FILE)

    def search(self, text):
        nb = load(NOTES_FILE)
        results = find_note(nb, text)
        return [note_to_dict(note) for note in results]

page = Path(__file__).parent / "ui.html"

webview.create_window("Math/CS Notes", url=str(page), js_api=Api())
webview.start()
