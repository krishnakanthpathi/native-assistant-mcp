import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def empty_trash() -> str:
        """Empties the Windows Recycle Bin."""
        if sys.platform == 'win32':
            ps_script = "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return "Successfully emptied the Recycle Bin."
