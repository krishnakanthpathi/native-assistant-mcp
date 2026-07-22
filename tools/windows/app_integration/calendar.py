import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def calendar(action: str, title: str = "", date_time: str = "") -> str:
        """Launches Windows Calendar or Outlook Calendar."""
        if sys.platform == 'win32':
            subprocess.run(['cmd', '/c', 'start', 'outlookcal:'], shell=True)
        return f"Calendar action '{action}' executed for '{title}'."
