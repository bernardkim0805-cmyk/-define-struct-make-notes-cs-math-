"""The Note data model and pure operations on notes.

Every function here returns a NEW value and never changes its inputs.
That makes the functions easy to test and safe to reuse from any interface.
"""

from dataclasses import dataclass, field, replace
from datetime import date
from uuid import uuid4


def new_id() -> str:
    return str(uuid4())


@dataclass
class Note:
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    last_edited: date = field(default_factory=date.today)
    id: str = field(default_factory=new_id)


SORT_KEYS = ("title", "date", "last_edited")
CODE_LANGUAGES = ("python", "racket")


def title_from_body(body: str, words: int = 3) -> str:
    """A fallback title: the first few words of the body."""
    return " ".join(body.split()[:words]) or "Untitled"


def create_notebook() -> list[Note]:
    return []


def add_note(nb: list[Note], note: Note) -> list[Note]:
    return nb + [note]


def add_notes(nb: list[Note], notes: list[Note]) -> list[Note]:
    return nb + list(notes)


def find_note(nb: list[Note], text: str) -> list[Note]:
    """Notes whose title, body, tags or date contain text (ignoring case)."""
    needle = text.lower()
    return [
        x for x in nb
        if needle in x.title.lower()
        or needle in x.body.lower()
        or any(needle in tag.lower() for tag in x.tags)
        or needle in x.last_edited.isoformat()
    ]


def find_by_id(nb: list[Note], note_id: str) -> Note | None:
    return next((x for x in nb if x.id == note_id), None)


def find_by_title(nb: list[Note], title: str) -> Note | None:
    """The first note with exactly this title, or None."""
    return next((x for x in nb if x.title == title), None)


def delete_note(nb: list[Note], note: Note) -> list[Note]:
    return [x for x in nb if x.id != note.id]


def update_note(nb: list[Note], note: Note, new_note: Note) -> list[Note]:
    return [new_note if x.id == note.id else x for x in nb]


def edit_note(note: Note, title: str | None = None, body: str | None = None) -> Note:
    """A copy of note with a new title and/or body. Keeps id and tags."""
    return replace(
        note,
        title=note.title if title is None else title,
        body=note.body if body is None else body,
        tags=list(note.tags),
        last_edited=date.today(),
    )


def sort_notes(nb: list[Note], key: str) -> list[Note]:
    if key == "title":
        return sorted(nb, key=lambda x: x.title.lower())
    if key in ("date", "last_edited"):
        return sorted(nb, key=lambda x: x.last_edited)
    raise ValueError(f"Invalid key {key!r}. Must be one of: {', '.join(SORT_KEYS)}")


def add_tag(note: Note, tag: str) -> Note:
    tag = tag.strip()
    if tag == "" or tag in note.tags:
        return replace(note, tags=list(note.tags))
    return replace(note, tags=note.tags + [tag])


def remove_tag(note: Note, tag: str) -> Note:
    return replace(note, tags=[t for t in note.tags if t != tag.strip()])


def set_tags(note: Note, tags: list[str]) -> Note:
    """Replace all tags. Blank and duplicate tags are dropped, order is kept."""
    clean: list[str] = []
    for tag in tags:
        tag = tag.strip()
        if tag and tag not in clean:
            clean.append(tag)
    return replace(note, tags=clean)


def append_note_body(note: Note, text: str) -> Note:
    new_body = note.body + "\n" + text if note.body else text
    return replace(note, body=new_body, tags=list(note.tags), last_edited=date.today())


def extract_code(body: str) -> list[tuple[str, str]]:
    """Find code blocks written as

        /start_python
        print("hi")
        /end_python

    and return them as [(language, code), ...] in the order they appear.
    A block with no matching /end_<language> line is ignored.
    """
    blocks: list[tuple[str, str]] = []
    language: str | None = None
    lines: list[str] = []
    for line in body.splitlines():
        marker = line.strip()
        if language is None:
            for lang in CODE_LANGUAGES:
                if marker == f"/start_{lang}":
                    language, lines = lang, []
                    break
        elif marker == f"/end_{language}":
            blocks.append((language, "\n".join(lines)))
            language = None
        else:
            lines.append(line)
    return blocks
