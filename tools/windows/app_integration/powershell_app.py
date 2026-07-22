import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def terminal(command: str = "") -> str:
        """Launches Windows Terminal / PowerShell window."""
        if sys.platform == 'win32':
            if command:
                subprocess.run(['wt', 'powershell', '-NoExit', '-Command', command])
            else:
                subprocess.run(['wt'])
        return "Launched Windows Terminal."
