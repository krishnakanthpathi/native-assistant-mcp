import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def safari(action: str, url: str = None, script: str = None) -> str:
        """Control Safari browser: open a URL, get open tab details, or execute custom JavaScript on the active tab."""
        act = (action or "").strip().lower().replace("_", "-")
        if act in ('open-url', 'open', 'openurl'):
            if not url:
                raise ValueError('url is required')
            
            apple_script = f'''
tell application "Safari"
    open location "{url}"
    activate
end tell
'''
            subprocess.run(['osascript', '-e', apple_script], check=True)
            return f'URL "{url}" opened in Safari.'
        
        elif act in ('get-tabs', 'tabs', 'list-tabs', 'list_tabs'):
            apple_script = '''
tell application "Safari"
    set tabNames to name of tabs of every window
    set tabURLs to URL of tabs of every window
    set tabList to ""
    repeat with wIdx from 1 to count of tabNames
        set windowNames to item wIdx of tabNames
        set windowURLs to item wIdx of tabURLs
        repeat with tIdx from 1 to count of windowNames
            set tabList to tabList & (item tIdx of windowNames) & ";" & (item tIdx of windowURLs) & "\\n"
        end repeat
    end repeat
    return tabList
end tell
'''
            res = subprocess.run(['osascript', '-e', apple_script], capture_output=True, text=True)
            if not res.stdout.strip():
                return 'No tabs open in Safari.'
            
            tabs = []
            for line in res.stdout.strip().split('\n'):
                parts = line.split(';')
                if len(parts) >= 2:
                    tabs.append({'name': parts[0], 'url': parts[1]})
            return json.dumps(tabs, indent=2)
        
        elif act in ('run-js-on-active-tab', 'run-js', 'eval', 'js'):
            if not script:
                raise ValueError('script is required')
            
            apple_script = f'''
tell application "Safari"
    do JavaScript "{script}" in document 1
end tell
'''
            res = subprocess.run(['osascript', '-e', apple_script], capture_output=True, text=True)
            return f'Script executed. Result: {res.stdout.strip() or "no return value"}'
        
        else:
            raise ValueError(f"Unknown safari action '{action}'. Supported actions: 'open-url', 'get-tabs', 'run-js-on-active-tab'")
