import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_active_window() -> str:
        """Gets the application name of the current active focused frontmost window on macOS."""
        script = 'tell application "System Events" to get name of first process whose frontmost is true'
        res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
        return f"Current active application: {res.stdout.strip()}"
