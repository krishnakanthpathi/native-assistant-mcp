import subprocess
import time
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def type_text(text: str) -> str:
        """Type a Unicode string into the active input field."""
        if not text:
            raise ValueError("Text parameter is required for typing action")
        
        original_clipboard = ''
        try:
            res = subprocess.run(['pbpaste'], capture_output=True, text=True)
            original_clipboard = res.stdout
        except Exception:
            pass
        
        subprocess.run(['pbcopy'], input=text, text=True, check=True)
        time.sleep(0.05)
        
        script = 'tell application "System Events" to keystroke "v" using command down'
        subprocess.run(['osascript', '-e', script], check=True)
        time.sleep(0.1)
        
        if original_clipboard:
            subprocess.run(['pbcopy'], input=original_clipboard, text=True)
        
        return 'Text typed successfully.'
