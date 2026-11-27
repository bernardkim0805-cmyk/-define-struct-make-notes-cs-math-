import numpy as np

from desktop import Api
from similarity import closest, cosine


def fake_embed(text: str) -> np.ndarray:
    """One number per topic, so we know in advance which notes are close."""
    text = text.lower()
    return np.array([
        float("series" in text or "convergence" in text),
        float("racket" in text or "list" in text),
        float("integral" in text),
        0.1,  # never all zeros
    ])


def make_api(tmp_path) -> tuple[Api, dict[str, str]]:
    api = Api(tmp_path / "notes.json", tmp_path / "emb.json", embed=fake_embed)
    ids = {}
    for title, body in [
        ("Ratio test", "a test for series"),
        ("Comparison test", "convergence by comparing series"),
        ("Linked lists", "lists in Racket"),
        ("Integrals", "integral by parts"),
    ]:
        ids[title] = api.create_note(title, body)["id"]
    return api, ids


def titles(notes: list[dict]) -> list[str]:
    return [note["title"] for note in notes]


def test_cosine_and_closest():
    assert np.isclose(cosine(np.array([3, 4]), np.array([6, 8])), 1.0)
    assert np.isclose(cosine(np.array([3, 4]), np.array([4, -3])), 0.0)
    vectors = [np.array([0, 1]), np.array([1, 0]), np.array([1, 1])]
    assert closest(np.array([1, 0.1]), vectors, 2) == [1, 2]


def test_saving_a_note_embeds_it(tmp_path):
    api, ids = make_api(tmp_path)
    from embeddings import load_vectors
    assert set(load_vectors(tmp_path / "emb.json")) == set(ids.values())


def test_search_notes_ranks_by_meaning(tmp_path):
    api, _ = make_api(tmp_path)
    assert set(titles(api.search_notes("convergence of series", k=2))) == {
        "Ratio test", "Comparison test"}


def test_search_notes_blank_query(tmp_path):
    api, _ = make_api(tmp_path)
    assert api.search_notes("   ") == []


def test_search_notes_k_larger_than_notes(tmp_path):
    api, _ = make_api(tmp_path)
    assert len(api.search_notes("series", k=50)) == 4


def test_related_notes_leaves_out_itself(tmp_path):
    api, ids = make_api(tmp_path)
    related = titles(api.related_notes(ids["Ratio test"], k=3))
    assert "Ratio test" not in related
    assert related[0] == "Comparison test"


def test_related_notes_unknown_id(tmp_path):
    api, _ = make_api(tmp_path)
    assert api.related_notes("no-such-id") == []


def test_deleted_note_drops_out_of_results(tmp_path):
    api, ids = make_api(tmp_path)
    api.delete_note(ids["Comparison test"])
    assert "Comparison test" not in titles(api.search_notes("series"))
    assert "Comparison test" not in titles(api.related_notes(ids["Ratio test"]))
