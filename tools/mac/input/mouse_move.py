import subprocess
from fastmcp import FastMCP

CLICLICK_PATH = '/opt/homebrew/bin/cliclick'


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_move(x: int, y: int) -> str:
        """Move the mouse cursor to global screen coordinates (x, y)."""
        subprocess.run([CLICLICK_PATH, f'm:{x},{y}'], check=True)
        return f'Mouse moved to ({x}, {y}).'
