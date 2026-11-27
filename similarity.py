"""Similarity and ranking for semantic search and related notes.

TODO(you): write both functions below. Nothing calls them yet, so the app
keeps working while they're unfinished.

How they'll be used (step 6, once these work):
    search:  top_k(embed_text("what you typed"), load_vectors())
    related: top_k(vectors[open_note_id], vectors)   <- same function!
"""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """How closely two vectors point the same way.

        cos(theta) = (a . b) / (|a| |b|)

    1.0 = same direction (same meaning), 0.0 = unrelated, -1.0 = opposite.

    Things to think about:
    - Which NumPy functions give a dot product and a vector's length?
    - What should happen if one vector is all zeros?
    """
    # TODO: your code here
    raise NotImplementedError("cosine_similarity: your turn!")


def top_k(
    target: np.ndarray,
    vectors: dict[str, np.ndarray],
    k: int = 5,
) -> list[tuple[str, float]]:
    """Score every vector against target and keep the k best.

    vectors maps note id -> vector (from embeddings.load_vectors()).
    Returns [(note_id, score), ...], highest score first, at most k items.

    Things to think about:
    - What if there are fewer than k notes?
    - For related notes, the open note scores 1.0 against itself.
      Where should it get left out: here, or in the caller?
    """
    # TODO: your code here
    raise NotImplementedError("top_k: your turn!")
