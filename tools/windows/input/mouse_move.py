import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_move(x: int, y: int) -> str:
        """Moves mouse cursor to coordinate (x, y)."""
        if sys.platform == 'win32':
            ps_script = f"[System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point({x}, {y})"
            subprocess.run(['powershell', '-Command', f"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; {ps_script}"], capture_output=True)
        return f"Mouse moved to ({x}, {y})."
