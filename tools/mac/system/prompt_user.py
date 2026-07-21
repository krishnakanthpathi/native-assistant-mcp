import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def prompt_user(message: str, default_answer: str = '') -> str:
        """Show a native popup dialog with an input text box and return the user response."""
        script = f'''
tell application "System Events"
    activate
    set response to display dialog "{message}" default answer "{default_answer}" buttons {{"Cancel", "OK"}} default button "OK"
    return text returned of response
end tell
'''
        res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
        return res.stdout.strip()
