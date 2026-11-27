"""Turning notes into vectors ("embeddings") and keeping them saved.

An embedding is a list of 384 numbers that captures what a piece of text
means. Texts with similar meanings get vectors that point in similar
directions, which is what similarity.py measures.

The vectors live in their own file, ~/MathCSNotes/embeddings.json:

    {
        "<note id>": {"hash": "<fingerprint of the text>", "vector": [0.01, ...]},
        ...
    }

It's safe to delete that file: sync_embeddings rebuilds it.
"""

import hashlib
import json
import os
from collections.abc import Callable
from pathlib import Path

import numpy as np

from notes import Note
from storage import APP_DIR

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = APP_DIR / "embeddings.json"

_model = None  # loaded the first time it's needed, then reused


def get_model():
    """Load the model once. Loading takes a few seconds, so we only pay that
    when something actually needs embedding."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # slow import
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_text(text: str) -> np.ndarray:
    """Turn any text into a vector of 384 numbers. Also used for search queries."""
    return get_model().encode(text)


def note_text(note: Note) -> str:
    """The text of a note that gets embedded: title, body and tags."""
    return f"{note.title}\n{note.body}\n{' '.join(note.tags)}"


def text_hash(text: str) -> str:
    """A short fingerprint of the text. Same text -> same hash, so comparing
    hashes tells us whether a note changed since it was last embedded."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_store(path: str | Path = EMBEDDINGS_FILE) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_store(store: dict, path: str | Path = EMBEDDINGS_FILE) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(store, f)
    os.replace(tmp, path)


def load_vectors(path: str | Path = EMBEDDINGS_FILE) -> dict[str, np.ndarray]:
    """{note id: vector} - the input your ranking function will score."""
    return {note_id: np.array(entry["vector"]) for note_id, entry in load_store(path).items()}


def sync_embeddings(
    notes: list[Note],
    path: str | Path = EMBEDDINGS_FILE,
    embed: Callable[[str], np.ndarray] = embed_text,
) -> int:
    """Make the embeddings file match the notes:
    - embed notes that are new, or whose text changed since last time
    - keep the saved vector for notes that didn't change
    - drop vectors of notes that were deleted

    `embed` is the function used to make vectors. Tests pass in a fake one
    so they don't need to load the real model.

    Returns how many notes were (re)embedded.
    """
    old = load_store(path)
    new = {}
    embedded = 0
    for note in notes:
        h = text_hash(note_text(note))
        if note.id in old and old[note.id]["hash"] == h:
            new[note.id] = old[note.id]
        else:
            vector = embed(note_text(note))
            new[note.id] = {"hash": h, "vector": [round(float(x), 6) for x in vector]}
            embedded += 1
    if new != old:
        save_store(new, path)
    return embedded
