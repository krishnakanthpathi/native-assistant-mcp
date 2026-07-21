import subprocess
from fastmcp import FastMCP

CLICLICK_PATH = '/opt/homebrew/bin/cliclick'


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_drag(from_x: int, from_y: int, to_x: int, to_y: int) -> str:
        """Press, drag, and release mouse from (fromX, fromY) to (toX, toY)."""
        subprocess.run([CLICLICK_PATH, f'dd:{from_x},{from_y}', f'dm:{to_x},{to_y}', f'du:{to_x},{to_y}'], check=True)
        return 'Mouse dragged successfully.'
