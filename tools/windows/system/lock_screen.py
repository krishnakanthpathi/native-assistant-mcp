import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def lock_screen() -> str:
        """Locks the Windows user screen."""
        if sys.platform == 'win32':
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
        return "Screen locked."
