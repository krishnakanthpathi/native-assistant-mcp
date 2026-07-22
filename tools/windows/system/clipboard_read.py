import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def clipboard_read() -> str:
        """Reads text from Windows system clipboard."""
        if sys.platform == 'win32':
            res = subprocess.run(['powershell', '-Command', 'Get-Clipboard'], capture_output=True, text=True)
            return res.stdout.strip()
        return ""
