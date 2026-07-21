import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def messages(action: str, recipient: str = None, message: str = None) -> str:
        """Interact with Messages.app: send text messages or list recent buddy conversations."""
        if action == 'send':
            if not recipient or not message:
                raise ValueError('recipient and message are required')
            
            script = f'''
tell application "Messages"
    set targetService to 1st service whose service type is iMessage
    set targetBuddy to buddy "{recipient}" of targetService
    send "{message}" to targetBuddy
end tell
'''
            subprocess.run(['osascript', '-e', script], check=True)
            return f'Message sent successfully to {recipient}.'
        
        elif action == 'list-recent':
            script = '''
tell application "Messages"
    set outputText to ""
    try
        set chatNames to name of chats
        set chatIds to id of chats
        
        set itemCount to count of chatNames
        repeat with i from 1 to itemCount
            set outputText to outputText & (item i of chatNames) & ";" & (item i of chatIds) & "\\n"
        end repeat
    end try
    return outputText
end tell
'''
            res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if not res.stdout.strip():
                return 'No recent chats found.'
            
            chats = []
            for line in res.stdout.strip().split('\n'):
                parts = line.split(';')
                if len(parts) >= 2:
                    chats.append({'name': parts[0], 'id': parts[1]})
            return json.dumps(chats, indent=2)
