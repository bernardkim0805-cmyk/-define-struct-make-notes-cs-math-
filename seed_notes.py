"""Add 100 sample notes for trying the app out, or remove them again.

    python seed_notes.py           # add 100 sample notes
    python seed_notes.py --remove  # delete every note tagged "sample"

Your own notes are never touched: samples are all tagged "sample".
"""

import random
import sys
from datetime import date, timedelta

from notes import Note, add_notes, find_note
from storage import NOTES_FILE, load, save

TAG = "sample"

# (title, body, extra tags) - hand-written notes with math and code
HANDWRITTEN = [
    ("Gauss sum", "The sum of the first n integers:\n$$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$$\nProof: pair the first and last terms.", ["math", "math135"]),
    ("Geometric series", "For $|r| < 1$:\n$$\\sum_{k=0}^{\\infty} r^k = \\frac{1}{1-r}$$", ["math", "calculus"]),
    ("Euler's identity", "$$e^{i\\pi} + 1 = 0$$\nLinks five fundamental constants.", ["math"]),
    ("Pythagorean theorem", "For a right triangle with legs $a, b$ and hypotenuse $c$: $a^2 + b^2 = c^2$.", ["math", "geometry"]),
    ("Quadratic formula", "Roots of $ax^2 + bx + c = 0$:\n$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$", ["math", "algebra"]),
    ("Definition of a limit", "$\\lim_{x \\to a} f(x) = L$ means: for every $\\epsilon > 0$ there is a $\\delta > 0$ such that $0 < |x - a| < \\delta \\implies |f(x) - L| < \\epsilon$.", ["math", "calculus"]),
    ("Fundamental theorem of calculus", "$$\\int_a^b f'(x)\\,dx = f(b) - f(a)$$", ["math", "calculus"]),
    ("Binomial theorem", "$$(x+y)^n = \\sum_{k=0}^n \\binom{n}{k} x^k y^{n-k}$$", ["math", "combinatorics"]),
    ("Bezout's lemma", "For integers $a, b$ there exist $x, y$ with $ax + by = \\gcd(a, b)$.", ["math", "math135"]),
    ("Fermat's little theorem", "If $p$ is prime and $p \\nmid a$, then $a^{p-1} \\equiv 1 \\pmod p$.", ["math", "math135"]),
    ("Euclidean algorithm", "gcd(a, b) = gcd(b, a mod b).\n\n/start_python\ndef gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n\nprint(gcd(252, 105))\n/end_python", ["math", "cs", "python"]),
    ("Fibonacci in Python", "$F_n = F_{n-1} + F_{n-2}$\n\n/start_python\na, b = 0, 1\nfor _ in range(10):\n    print(a, end=' ')\n    a, b = b, a + b\n/end_python", ["cs", "python"]),
    ("Recursion in Racket", "Factorial with structural recursion.\n\n/start_racket\n(define (fact n)\n  (if (zero? n) 1 (* n (fact (sub1 n)))))\n(fact 10)\n/end_racket", ["cs", "racket", "cs135"]),
    ("Lists in Racket", "cons, first, rest.\n\n/start_racket\n(define lst (cons 1 (cons 2 (cons 3 empty))))\n(first (rest lst))\n/end_racket", ["cs", "racket", "cs135"]),
    ("map and filter", "/start_racket\n(map (lambda (x) (* x x)) (list 1 2 3 4))\n(filter even? (list 1 2 3 4 5 6))\n/end_racket", ["cs", "racket"]),
    ("Python list comprehensions", "/start_python\nsquares = [x * x for x in range(10) if x % 2 == 0]\nprint(squares)\n/end_python", ["cs", "python"]),
    ("Big-O of binary search", "Binary search halves the range each step, so it takes $O(\\log n)$ comparisons.\n\n/start_python\ndef bsearch(xs, t):\n    lo, hi = 0, len(xs) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if xs[mid] == t:\n            return mid\n        if xs[mid] < t:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n\nprint(bsearch(list(range(0, 100, 3)), 42))\n/end_python", ["cs", "algorithms", "python"]),
    ("Infinite loop test", "This one should time out after 10 seconds.\n\n/start_python\nwhile True:\n    pass\n/end_python", ["cs", "python"]),
    ("Error test", "This code raises an error on purpose.\n\n/start_python\nprint(1 / 0)\n/end_python", ["cs", "python"]),
    ("Matrix multiplication", "$$\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}\\begin{pmatrix}5\\\\6\\end{pmatrix} = \\begin{pmatrix}17\\\\39\\end{pmatrix}$$", ["math", "linear-algebra"]),
]

DERIVATIVES = [
    ("x^n", "nx^{n-1}"), ("e^x", "e^x"), ("\\ln x", "\\frac{1}{x}"),
    ("\\sin x", "\\cos x"), ("\\cos x", "-\\sin x"), ("\\tan x", "\\sec^2 x"),
    ("a^x", "a^x \\ln a"), ("\\arctan x", "\\frac{1}{1+x^2}"),
]
TOPICS = [
    "sets", "functions", "induction", "modular arithmetic", "graphs", "trees",
    "hash tables", "stacks", "queues", "sorting", "probability", "vectors",
]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def generated_note(i: int, rng: random.Random) -> tuple[str, str, list[str]]:
    kind = i % 4
    if kind == 0:
        f, df = DERIVATIVES[i % len(DERIVATIVES)]
        return (f"Derivative of ${f}$ #{i}", f"$$\\frac{{d}}{{dx}} {f} = {df}$$", ["math", "calculus"])
    if kind == 1:
        n = rng.randint(3, 30)
        return (f"Sum of squares to {n}",
                f"$\\sum_{{i=1}}^{{{n}}} i^2 = \\frac{{n(n+1)(2n+1)}}{{6}}$ with $n = {n}$\n\n"
                f"/start_python\nprint(sum(i * i for i in range(1, {n + 1})))\n/end_python",
                ["math", "python"])
    if kind == 2:
        a, b = rng.randint(1, 50), rng.randint(1, 50)
        return (f"Racket arithmetic {a} and {b}",
                f"/start_racket\n(+ {a} {b})\n(* {a} {b})\n/end_racket", ["cs", "racket"])
    topic = TOPICS[i % len(TOPICS)]
    day = WEEKDAYS[i % len(WEEKDAYS)]
    return (f"Lecture notes: {topic} ({day})",
            f"Notes on {topic} from {day}'s lecture.\nKey idea: practise the examples before the quiz.",
            ["lecture", topic.replace(" ", "-")])


def make_samples(count: int = 100) -> list[Note]:
    rng = random.Random(42)  # fixed seed: same notes every time
    specs = HANDWRITTEN + [generated_note(i, rng) for i in range(count - len(HANDWRITTEN))]
    today = date.today()
    return [
        Note(title, body, tags + [TAG], today - timedelta(days=rng.randint(0, 120)))
        for title, body, tags in specs[:count]
    ]


def main() -> None:
    notes = load(NOTES_FILE)
    if "--remove" in sys.argv:
        kept = [n for n in notes if TAG not in n.tags]
        save(kept, NOTES_FILE)
        print(f"Removed {len(notes) - len(kept)} sample notes. {len(kept)} notes left.")
    else:
        samples = make_samples()
        save(add_notes(notes, samples), NOTES_FILE)
        print(f"Added {len(samples)} sample notes. {len(notes) + len(samples)} notes total.")


if __name__ == "__main__":
    main()
