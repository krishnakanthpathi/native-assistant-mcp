import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def list_apps() -> str:
        """List running GUI applications on macOS (bundle id, name, pid, frontmost)."""
        script = '''
tell application "System Events"
    set pids to unix id of every process whose background only is false
    set names to name of every process whose background only is false
    set frontmosts to frontmost of every process whose background only is false
    set bundles to bundle identifier of every process whose background only is false
    
    set outputText to ""
    set itemCount to count of pids
    repeat with i from 1 to itemCount
        set pidVal to item i of pids
        set nameVal to item i of names
        set frontVal to item i of frontmosts
        set bundleVal to item i of bundles
        if bundleVal is missing value then set bundleVal to ""
        set outputText to outputText & bundleVal & ";" & nameVal & ";" & pidVal & ";" & frontVal & "\\n"
    end repeat
    return outputText
end tell
'''
        res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        
        if not res.stdout.strip():
            return 'No running GUI applications found.'
        
        apps = []
        for line in res.stdout.strip().split('\n'):
            parts = line.split(';')
            if len(parts) >= 4:
                apps.append({
                    'bundleId': parts[0],
                    'name': parts[1],
                    'pid': int(parts[2]) if parts[2].isdigit() else 0,
                    'frontmost': parts[3].lower() == 'true'
                })
        
        return json.dumps(apps, indent=2)
