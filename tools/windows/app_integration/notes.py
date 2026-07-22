import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def notes(content: str = "") -> str:
        """Launches Notepad or Sticky Notes on Windows."""
        if sys.platform == 'win32':
            subprocess.run(['notepad.exe'])
        return "Opened Notepad."
