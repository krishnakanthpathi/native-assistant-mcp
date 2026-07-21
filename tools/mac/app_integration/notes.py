import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def notes(action: str, title: str = None, body: str = None, query: str = None, note_id: str = None) -> str:
        """Interact with Notes.app: create a new note, search for notes, or append text to an existing note."""
        if action == 'create':
            if not title or not body:
                raise ValueError('title and body are required for create action')
            
            script = f'''
tell application "Notes"
    tell folder "Notes"
        make new note with properties {{name:"{title}", body:"{body}"}}
    end tell
end tell
'''
            subprocess.run(['osascript', '-e', script], check=True)
            return f'Note "{title}" created successfully.'
        
        elif action == 'search':
            if not query:
                raise ValueError('query is required for search action')
            
            script = f'''
tell application "Notes"
    set outputText to ""
    try
        set noteList to every note whose name contains "{query}" or body contains "{query}"
        set noteNames to name of noteList
        set noteIds to id of noteList
        
        set itemCount to count of noteNames
        repeat with i from 1 to itemCount
            set outputText to outputText & (item i of noteNames) & ";" & (item i of noteIds) & "\\n"
        end repeat
    end try
    return outputText
end tell
'''
            res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if not res.stdout.strip():
                return f'No notes found matching "{query}".'
            
            notes_list = []
            for line in res.stdout.strip().split('\n'):
                parts = line.split(';')
                if len(parts) >= 2:
                    notes_list.append({'name': parts[0], 'id': parts[1]})
            return json.dumps(notes_list, indent=2)
        
        elif action == 'append':
            if not note_id or not body:
                raise ValueError('note_id and body are required for append action')
            
            script = f'''
tell application "Notes"
    try
        set myNote to first note whose name is "{note_id}" or id is "{note_id}"
        set body of myNote to (body of myNote) & "<br>" & "{body}"
        return "success"
    on error err
        return err
    end try
end tell
'''
            res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if res.stdout.strip() == 'success':
                return 'Content appended to note successfully.'
            else:
                raise ValueError(f'AppleScript error: {res.stdout.strip()}')
