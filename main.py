from notes import *
from storage import load, save

# interface 

my_notes = load("notes.json")
while True: 
    command = input("command: ")
    if command == "quit":
        save(my_notes, "notes.json")
        break 
    elif command == "new":
        title = input("title: ")
        body = input("notes: ")
        if title == "":
            title = " ". join(body.split()[:3])
        note = Note(title, body)
        my_notes = add_note(my_notes, note)
    elif command == "search":
        text = input("keywords: ")
        results = find_note(my_notes, text)
        for note in results:
            print(f"Title: {note.title}")
            print(f"Body: {note.body}")
            print(f"Tags: {note.tags}")
            print(f"Last edited: {note.last_edited}")
    elif command == "delete":
        title = input("title: ")
        note_to_delete = next((note for note in my_notes if note.title == title), None)
        if note_to_delete:
            my_notes = delete_note(my_notes, note_to_delete)
            print(f"Note '{title}' deleted.")
        else:
            print(f"No note found with title '{title}'.")
    elif command == "update":
        title = input("title: ")
        update_this = next((note for note in my_notes if note.title == title), None)
        if update_this:
            new_title = input("new title: ")
            if new_title == "":
                new_title = update_this.title
            new_body = input("new body: ")
            if new_body == "":
                new_body = update_this.body
            new_note = Note(new_title, new_body, update_this.tags)
            my_notes = update_note(my_notes, update_this, new_note)
            print(f"Note '{title}' updated.")
        else:
            print(f"No note found with title '{title}'.")
    elif command == "sort":
        sorted_input = input("sort by ...")
        if sorted_input == "title":
            my_notes = sort_notes(my_notes, "title")
        elif sorted_input == "date" or sorted_input == "last_edited":
            my_notes = sort_notes(my_notes, "last_edited")

        

        
        
        
            


        
        
            




    

