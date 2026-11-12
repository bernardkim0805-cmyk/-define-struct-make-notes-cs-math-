from dataclasses import dataclass, field 
from datetime import date

@dataclass
class Note:
    title: str
    body: str
    tags: list[str] = field(default_factory = list)
    created_on: date = field(default_factory = date.today)



def add_note(nb: list[Note], note: Note) -> list[Note]:
    nb.append(note)
    return nb

def find_note(nb: list[Note], text: str) -> list[Note]:
    return [x for x in nb if text in x.title or 
            text in x.body or text in x.tags or text in str(x.created_on)]

def delete_note(nb: list[Note], note: Note) -> list[Note]:
    return [x for x in nb if x != note]

def update_note(nb: list[Note], note: Note, new_note: Note) -> list[Note]:
    return [new_note if x == note else x for x in nb]

def delete_nb(nb: list[Note]) -> list[Note]:
    return []

def sort_notes(nb: list[Note], key: str) -> list[Note]:
    if key == "title":
        return sorted(nb, key=lambda x: x.title)
    elif key == "date":
        return sorted(nb, key=lambda x: x.created_on)
    elif key == "created_on":
        return sorted(nb, key = lambda x: x.created_on)
    else:
        raise ValueError("Invalid key. Must be 'title', 'date', or 'created_on'")
    

def add_notes(nb: list[Note], notes: list[Note]) -> list[Note]:
    nb.extend(notes)
    return nb

def create_notebook() -> list[Note]:
    return []