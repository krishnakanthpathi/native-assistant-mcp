import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def mail(action: str, to: str = None, subject: str = None, body: str = None, query: str = None) -> str:
        """Interact with Mail.app: compose outgoing messages, search messages, or list unread inbox messages."""
        if action == 'compose':
            if not to:
                raise ValueError('Recipient "to" is required for compose')
            script = f'''
tell application "Mail"
    set newMsg to make new outgoing message with properties {{subject:"{subject or ''}", content:"{body or ''}", visible:true}}
    tell newMsg
        make new to recipient with properties {{address:"{to}"}}
    end tell
    activate
end tell
'''
            subprocess.run(['osascript', '-e', script], check=True)
            return 'Draft email composed successfully in Mail.app.'
        
        elif action == 'list-unread':
            script = '''
tell application "Mail"
    set outputText to ""
    try
        set unreadMsgs to every message of inbox whose read status is false
        set senders to sender of unreadMsgs
        set subjects to subject of unreadMsgs
        set dates to date received of unreadMsgs
        
        set itemCount to count of senders
        repeat with i from 1 to itemCount
            set d to item i of dates
            set outputText to outputText & (item i of senders) & ";" & (item i of subjects) & ";" & (d as string) & "\\n"
        end repeat
    end try
    return outputText
end tell
'''
            res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if not res.stdout.strip():
                return 'No unread messages found.'
            
            messages = []
            for line in res.stdout.strip().split('\n'):
                parts = line.split(';')
                if len(parts) >= 3:
                    messages.append({'sender': parts[0], 'subject': parts[1], 'date': parts[2]})
            return json.dumps(messages, indent=2)
        
        elif action == 'search':
            if not query:
                raise ValueError('Search "query" is required')
            script = f'''
tell application "Mail"
    set outputText to ""
    try
        set msgs to every message of inbox whose (subject contains "{query}") or (content contains "{query}") or (sender contains "{query}")
        set senders to sender of msgs
        set subjects to subject of msgs
        set dates to date received of msgs
        
        set itemCount to count of senders
        repeat with i from 1 to itemCount
            set d to item i of dates
            set outputText to outputText & (item i of senders) & ";" & (item i of subjects) & ";" & (d as string) & "\\n"
        end repeat
    end try
    return outputText
end tell
'''
            res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if not res.stdout.strip():
                return f'No messages matching query "{query}" found.'
            
            messages = []
            for line in res.stdout.strip().split('\n'):
                parts = line.split(';')
                if len(parts) >= 3:
                    messages.append({'sender': parts[0], 'subject': parts[1], 'date': parts[2]})
            return json.dumps(messages, indent=2)
