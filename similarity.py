"""Similarity and ranking for semantic search and related notes.

cosine and closest were written (and tried out) in play.py, and are used
here exactly as written there.

How they're used (see desktop.Api):
    search:  closest(embed_text("what you typed"), vectors, k)
    related: closest(vector_of_open_note, other_vectors, k)   <- same function!

closest works on a plain list of vectors and returns positions in that list,
so callers keep a matching list of note ids to turn positions back into notes.
"""

import numpy as np


def cosine(u, v):
    cosine_similarity = np.dot(u,v)/(np.linalg.norm(u) * np.linalg.norm(v))
    return cosine_similarity


def closest(target, vectors, k):
    score_vector = []
    for i,x in enumerate(vectors):
        score_vector.append((cosine(target, x), i))

    desired = sorted(score_vector, reverse=True)[:k]
    return [i for score, i in desired]
