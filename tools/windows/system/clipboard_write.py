import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def clipboard_write(text: str) -> str:
        """Writes text to Windows system clipboard."""
        if sys.platform == 'win32':
            ps_script = f"Set-Clipboard -Value '{text}'"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return "Clipboard updated."
