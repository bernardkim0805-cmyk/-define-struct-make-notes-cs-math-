from sentence_transformers import SentenceTransformer
import numpy as np 
model = SentenceTransformer("all-MiniLM-L6-v2")
v = model.encode("ratio test for series")

def cosine(u, v):
    cosine_similarity = np.dot(u,v)/(np.linalg.norm(u) * np.linalg.norm(v))
    return cosine_similarity 

print(cosine(np.array([3, 4]), np.array([6, 8])))    # should print 1.0
print(cosine(np.array([3, 4]), np.array([4, -3])))

query = model.encode ("convergence tests")
a = model.encode("ratio test for series")
b = model.encode("linked lists in Racket")

print(cosine(query, a))   
print(cosine(query, b))


notes = [
    "ratio test for series",
    "linked lists in Racket",
    "integration by parts",
    "recursion on natural numbers",
    "comparison test for convergence",
]

vectors = [model.encode(n) for n in notes]

def closest(target, vectors, k):
    score_vector = []
    for i,x in enumerate(vectors):
        score_vector.append((cosine(target, x), i))

    desired = sorted(score_vector, reverse=True)[:k]
    return [i for score, i in desired]



notes = [
    "ratio test for series",
    "linked lists in Racket",
    "integration by parts",
    "recursion on natural numbers",
    "comparison test for convergence",
]
vectors = [model.encode(n) for n in notes]

query = model.encode("convergence tests")
for i in closest(query, vectors, 2):
    print(notes[i])
# expect the "comparison test" and "ratio test" notes, in some order