import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_finder_selection() -> str:
        """Returns file and directory POSIX paths currently selected in the frontmost Finder window."""
        script = '''
        tell application "Finder"
            set sel to selection
            set outputText to ""
            repeat with item_ in sel
                set outputText to outputText & (POSIX path of (item_ as alias)) & linefeed
            end repeat
            return outputText
        end tell
        '''
        res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if res.returncode != 0:
            return f"Finder selection error: {res.stderr.strip()}"
        out = res.stdout.strip()
        return out if out else "No files selected in Finder."
