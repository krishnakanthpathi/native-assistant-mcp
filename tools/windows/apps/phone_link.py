import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def phone_link() -> str:
        """Launches Windows Phone Link app."""
        if sys.platform == 'win32':
            subprocess.run(['cmd', '/c', 'start', 'ms-phone:'], shell=True)
        return "Launched Phone Link app."
