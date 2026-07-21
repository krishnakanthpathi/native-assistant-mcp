import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def lock_screen() -> str:
        """Locks the macOS screen immediately."""
        subprocess.run(['pmset', 'displaysleepnow'], check=True)
        return 'Screen locked successfully.'
