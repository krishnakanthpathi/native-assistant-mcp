import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def empty_trash() -> str:
        """Empties the macOS Trash folder."""
        script = 'tell application "Finder" to empty trash'
        subprocess.run(['osascript', '-e', script], check=True)
        return 'Trash folder emptied successfully.'
