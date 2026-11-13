Math/CS Notes

A notetaking app for math and computer science, built from scratch in Python.

Why I'm building this

I'm currently a first-year Computer Science student at the University of Waterloo. My notes are split between two very different kinds of content: proofs and formulas for math courses, and code for CS courses, specifically for C and Racket (I coded this in Python so it will support Python as well). Most notetaking apps handle one of these well. Few handle both: tools with good LaTeX support usually can't run code, and tools that run code are awkward for writing math.

I want one place where I can typeset a proof in LaTeX and run a code snippet in the same note. I'm also building it by hand rather than generating it, as a way to learn how real applications are designed: data models, persistence, interfaces, and packaging.

Current features
Create, search, update, delete, and sort notes
Notes have a title, body, tags, and a last-edited date
Notes are saved to a local JSON file and reloaded on startup
Terminal interface
Planned
 LaTeX rendering for math notes
 Running code snippets (Python, Racket) inside CS notes
 Multi-line note input
 Auto-save after every change
 Graphical interface
 Standalone app (no Python install required)
Running it

Requires Python 3.10 or newer.

git clone <this repo's URL>
cd <repo folder>
python3 main.py
Commands
Command	What it does
new	Create a note (a blank title uses the first few words of the body)
search	Find notes containing a keyword in the title, body, tags, or date
update	Edit a note's title or body (press Enter to keep the current value)
delete	Delete a note by title
sort	Sort notes by title or date
quit	Save and exit
Project structure
File	Responsibility
notes.py	The Note data model and the operations on notes
storage.py	Saving and loading notes as JSON
main.py	The terminal interface

Each file depends only on the ones above it, so a new interface can reuse the same logic and storage unchanged.
