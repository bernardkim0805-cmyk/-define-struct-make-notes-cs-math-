import numpy as np

from embeddings import embed_text, load_vectors, note_text, sync_embeddings
from notes import Note, edit_note


class FakeEmbed:
    """Stands in for the real model: fast, and counts how often it's called."""

    def __init__(self):
        self.calls = 0

    def __call__(self, text: str) -> np.ndarray:
        self.calls += 1
        return np.array([len(text), 1.0, 0.5])


def test_sync_embeds_every_new_note(tmp_path):
    path, fake = tmp_path / "emb.json", FakeEmbed()
    notes = [Note("a", "one"), Note("b", "two")]
    assert sync_embeddings(notes, path, fake) == 2
    vectors = load_vectors(path)
    assert set(vectors) == {notes[0].id, notes[1].id}
    assert vectors[notes[0].id].tolist() == [len(note_text(notes[0])), 1.0, 0.5]


def test_sync_skips_unchanged_notes(tmp_path):
    path, fake = tmp_path / "emb.json", FakeEmbed()
    notes = [Note("a", "one"), Note("b", "two")]
    sync_embeddings(notes, path, fake)
    assert sync_embeddings(notes, path, fake) == 0
    assert fake.calls == 2


def test_sync_reembeds_changed_note(tmp_path):
    path, fake = tmp_path / "emb.json", FakeEmbed()
    notes = [Note("a", "one"), Note("b", "two")]
    sync_embeddings(notes, path, fake)
    notes[1] = edit_note(notes[1], body="two, but longer now")
    assert sync_embeddings(notes, path, fake) == 1


def test_sync_drops_deleted_notes(tmp_path):
    path, fake = tmp_path / "emb.json", FakeEmbed()
    a, b = Note("a", "one"), Note("b", "two")
    sync_embeddings([a, b], path, fake)
    sync_embeddings([a], path, fake)
    assert set(load_vectors(path)) == {a.id}


def test_sync_empty_and_missing_file(tmp_path):
    path = tmp_path / "emb.json"
    assert load_vectors(path) == {}
    assert sync_embeddings([], path, FakeEmbed()) == 0


def test_real_model_gives_384_numbers():
    vector = embed_text("the derivative of sin x is cos x")
    assert vector.shape == (384,)
