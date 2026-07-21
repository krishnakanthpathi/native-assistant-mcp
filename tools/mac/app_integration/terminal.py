import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def terminal(action: str, command: str = None, text: str = None, target: str = 'terminal') -> str:
        """Interact with terminal applications (Terminal.app or iTerm2): open windows, run commands, list active sessions."""
        if target == 'iterm2':
            if action == 'open_window':
                script = '''
tell application "iTerm"
    create window with default profile
    activate
end tell
'''
                subprocess.run(['osascript', '-e', script], check=True)
                return 'New iTerm2 window opened.'
            
            elif action in ['run_command', 'send_text']:
                cmd = command or text
                if not cmd:
                    raise ValueError('command/text is required')
                
                script = f'''
tell application "iTerm"
    tell current session of current window
        write text "{cmd}"
    end tell
    activate
end tell
'''
                subprocess.run(['osascript', '-e', script], check=True)
                return 'Command/Text sent to active iTerm2 session.'
            
            elif action == 'get_active_text':
                script = '''
tell application "iTerm"
    tell current session of current window
        return text
    end tell
end tell
'''
                res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
                return res.stdout.strip()
            
            elif action == 'list_sessions':
                script = '''
tell application "iTerm"
    set outputText to ""
    repeat with w in windows
        repeat with t in tabs of w
            repeat with s in sessions of t
                set outputText to outputText & (id of s) & ";" & (name of s) & "\\n"
            end repeat
        end repeat
    end repeat
    return outputText
end tell
'''
                res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
                if not res.stdout.strip():
                    return '[]'
                
                sessions = []
                for line in res.stdout.strip().split('\n'):
                    parts = line.split(';')
                    if len(parts) >= 2:
                        sessions.append({'id': parts[0], 'name': parts[1]})
                return json.dumps(sessions, indent=2)
        
        else:
            if action == 'open_window':
                script = '''
tell application "Terminal"
    do script ""
    activate
end tell
'''
                subprocess.run(['osascript', '-e', script], check=True)
                return 'New Terminal.app window opened.'
            
            elif action == 'run_command':
                if not command:
                    raise ValueError('command is required')
                
                script = f'''
tell application "Terminal"
    do script "{command}"
    activate
end tell
'''
                subprocess.run(['osascript', '-e', script], check=True)
                return 'Command sent to Terminal.app.'
            
            elif action == 'send_text':
                if not text:
                    raise ValueError('text is required')
                
                script = f'''
tell application "Terminal"
    tell front window
        do script "{text}" in selected tab
    end tell
    activate
end tell
'''
                subprocess.run(['osascript', '-e', script], check=True)
                return 'Text sent to Terminal.app.'
            
            elif action == 'get_active_text':
                script = '''
tell application "Terminal"
    contents of selected tab of front window
end tell
'''
                res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
                return res.stdout.strip()
            
            elif action == 'list_sessions':
                script = '''
tell application "Terminal"
    set outputText to ""
    repeat with w in windows
        repeat with t in tabs of w
            set outputText to outputText & (id of w as string) & ";" & (name of t) & "\\n"
        end repeat
    end repeat
    return outputText
end tell
'''
                res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
                if not res.stdout.strip():
                    return '[]'
                
                sessions = []
                for line in res.stdout.strip().split('\n'):
                    parts = line.split(';')
                    if len(parts) >= 2:
                        sessions.append({'windowId': parts[0], 'tabName': parts[1]})
                return json.dumps(sessions, indent=2)
