"""The terminal interface."""

from notes import (
    Note, SORT_KEYS, add_note, add_tag, append_note_body, delete_note,
    edit_note, extract_code, find_by_title, find_note, remove_tag,
    sort_notes, title_from_body, update_note,
)
from embeddings import sync_embeddings
from runner import run_code
from storage import NOTES_FILE, load, save

COMMANDS = {
    "new": "create a note",
    "list": "list all note titles",
    "show": "show one note",
    "search": "find notes containing a keyword",
    "update": "change a note's title or body",
    "append": "add text to the end of a note",
    "tag": "add or remove a tag",
    "delete": "delete a note",
    "sort": "sort notes by title or date",
    "run": "run the code blocks in a note",
    "help": "show this list",
    "quit": "save and exit",
}


def read_multi_line(prompt: str) -> str:
    print(prompt + " (end with a line containing only .)")
    lines = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line)
    return "\n".join(lines)


def print_note(note: Note, show_body: bool = True) -> None:
    print(f"Title: {note.title}")
    if show_body:
        print(f"Body: {note.body}")
        print(f"Tags: {', '.join(note.tags) if note.tags else '(none)'}")
    print(f"Last edited: {note.last_edited}")
    print()


def print_help() -> None:
    print("Commands:")
    for name, what in COMMANDS.items():
        print(f"  {name:<8} {what}")


def ask_for_note(my_notes: list[Note]) -> Note | None:
    """Ask for a title; print a message and return None if there's no such note."""
    title = input("title: ")
    note = find_by_title(my_notes, title)
    if note is None:
        print(f"No note found with title '{title}'.")
    return note


def main() -> None:
    my_notes = load(NOTES_FILE)
    print("MathCSNotes. Type 'help' to see the commands.")

    while True:
        command = input("command: ").strip().lower()

        if command == "quit":
            save(my_notes, NOTES_FILE)
            sync_embeddings(my_notes)
            break

        elif command == "help":
            print_help()

        elif command == "new":
            title = input("title: ")
            body = read_multi_line("notes:")
            if title == "":
                title = title_from_body(body)
            my_notes = add_note(my_notes, Note(title, body))
            print(f"Note '{title}' created.")

        elif command == "list":
            if not my_notes:
                print("No notes yet.")
            for note in my_notes:
                print_note(note, show_body=False)

        elif command == "show":
            note = ask_for_note(my_notes)
            if note:
                print_note(note)

        elif command == "search":
            results = find_note(my_notes, input("keywords: "))
            if not results:
                print("No matches.")
            for note in results:
                print_note(note)

        elif command == "update":
            note = ask_for_note(my_notes)
            if note:
                new_title = input("new title (Enter to keep): ")
                new_body = read_multi_line("new body (just . to keep):")
                updated = edit_note(note, title=new_title or None, body=new_body or None)
                my_notes = update_note(my_notes, note, updated)
                print(f"Note '{updated.title}' updated.")

        elif command == "append":
            note = ask_for_note(my_notes)
            if note:
                new_text = read_multi_line("text to append:")
                my_notes = update_note(my_notes, note, append_note_body(note, new_text))
                print(f"Note '{note.title}' updated.")

        elif command == "tag":
            note = ask_for_note(my_notes)
            if note:
                action = input("add or remove? ").strip().lower()
                tag = input("tag: ")
                if action == "add":
                    my_notes = update_note(my_notes, note, add_tag(note, tag))
                    print(f"Tag '{tag}' added.")
                elif action == "remove":
                    my_notes = update_note(my_notes, note, remove_tag(note, tag))
                    print(f"Tag '{tag}' removed.")
                else:
                    print(f"Unknown action '{action}'. Type add or remove.")

        elif command == "delete":
            note = ask_for_note(my_notes)
            if note:
                my_notes = delete_note(my_notes, note)
                print(f"Note '{note.title}' deleted.")

        elif command == "sort":
            key = input(f"sort by ({', '.join(SORT_KEYS)}): ").strip().lower()
            if key in SORT_KEYS:
                my_notes = sort_notes(my_notes, key)
                print(f"Sorted by {key}.")
            else:
                print(f"Can't sort by '{key}'. Choose one of: {', '.join(SORT_KEYS)}.")

        elif command == "run":
            note = ask_for_note(my_notes)
            if note:
                blocks = extract_code(note.body)
                if not blocks:
                    print("This note has no code blocks (see /start_python ... /end_python).")
                for number, (language, code) in enumerate(blocks, start=1):
                    print(f"--- block {number} ({language}) ---")
                    print(run_code(language, code))

        elif command == "":
            continue

        else:
            print(f"Unknown command '{command}'.")
            print_help()


if __name__ == "__main__":
    main()
