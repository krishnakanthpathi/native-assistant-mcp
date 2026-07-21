import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_volume() -> str:
        """Gets the current system output volume level (0-100) on macOS."""
        res = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True, check=True)
        volume = int(res.stdout.strip())
        return f"System output volume is currently at {volume}%."
