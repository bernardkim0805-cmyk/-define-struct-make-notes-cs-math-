import webview
from pathlib import Path
from storage import load, note_to_dict 

class Api:
    def get_notes(self):
        return [note_to_dict(note) for note in load(Notes_file)]
    

page = Path(__file__).parent / "ui.html"

webview.create_window("Math/CS Notes", url=str(page), js_api=Api())
webview.start(debug=True)
