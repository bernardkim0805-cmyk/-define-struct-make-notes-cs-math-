# Math/CS Notes

A notetaking app for math and computer science, built from scratch in Python.

## Why I'm building this

I'm currently a first-year Computer Science student at the University of Waterloo. My notes are split between two very different kinds of content: proofs and formulas for math courses, and code for CS courses, specifically for C and Racket (I coded this in Python so it will support Python as well). Most notetaking apps handle one of these well. Few handle both: tools with good LaTeX support usually can't run code, and tools that run code are awkward for writing math.

I want one place where I can typeset a proof in LaTeX and run a code snippet in the same note. I'm also building it by hand rather than generating it, as a way to learn how real applications are designed: data models, persistence, interfaces, and packaging.

## Features

- Create, search, update, append to, tag, delete, and sort notes
- Notes have a title, body, tags, a last-edited date, and a stable unique id
- LaTeX math in the desktop app: `$...$` inline, `$$...$$` on its own line (rendered with KaTeX)
- Run Python and Racket code blocks inside a note, from either interface
- Notes are saved to `~/MathCSNotes/notes.json` and reloaded on startup
- Two interfaces sharing the same logic: a terminal app and a desktop app

## Running it

Requires Python 3.10 or newer and [uv](https://docs.astral.sh/uv/).

```bash
git clone <this repo's URL>
cd <repo folder>
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

python desktop.py   # desktop app
python main.py      # terminal app
```

Running Racket code blocks needs [Racket](https://racket-lang.org/) installed and `racket` on your PATH.
The desktop app loads KaTeX from the internet, so math rendering needs a connection.

Run the tests with:

```bash
python -m pytest
```

## Building the desktop app

```bash
./build.sh
```

This uses PyInstaller to build `dist/MathCSNotes.app` on macOS (`dist/MathCSNotes/` elsewhere), with `ui.html` bundled inside.

## Terminal commands

| Command  | What it does |
|----------|--------------|
| `new`    | Create a note (a blank title uses the first few words of the body) |
| `list`   | List every note's title and date |
| `show`   | Show one note in full |
| `search` | Find notes containing a keyword in the title, body, tags, or date (ignores case) |
| `update` | Edit a note's title or body (press Enter to keep the current value); tags are kept |
| `append` | Add text to the end of a note |
| `tag`    | Add or remove a tag |
| `delete` | Delete a note by title |
| `sort`   | Sort notes by `title`, `date`, or `last_edited` |
| `run`    | Run every code block in a note and print the output |
| `help`   | List the commands |
| `quit`   | Save and exit |

## Code blocks

Put code between a start and an end line, each on its own line:

```
The sum of the first n numbers is $\frac{n(n+1)}{2}$.

/start_python
print(sum(range(1, 11)))
/end_python

/start_racket
(define (sq x) (* x x))
(sq 7)
/end_racket
```

Each block runs in its own process and is stopped after 10 seconds. Racket blocks without a `#lang` line get `#lang racket` added automatically.

## Project structure

| File | Responsibility |
|------|----------------|
| `notes.py`   | The Note data model and the operations on notes (all return new values) |
| `storage.py` | Saving and loading notes as JSON |
| `runner.py`  | Running code blocks in a separate process |
| `main.py`    | The terminal interface |
| `desktop.py` | The desktop interface (pywebview), plus `ui.html` for the page itself |
| `test_*.py`  | pytest tests |

Each file depends only on the ones above it, so a new interface can reuse the same logic and storage unchanged.

## Roadmap

- [x] LaTeX rendering for math notes
- [x] Running code snippets (Python, Racket) inside CS notes
- [x] Multi-line note input
- [x] Graphical interface
- [x] Tests
- [x] Packaging as a desktop app
- [ ] Auto-save after every change (the terminal app only saves on `quit`)
- [ ] Editing a note's title and body in the desktop app
- [ ] ML: suggest tags for a note
- [ ] ML: find related notes
