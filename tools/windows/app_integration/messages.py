import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def messages(action: str, recipient: str = "", message: str = "") -> str:
        """Launches Phone Link messaging / Windows Messages protocol."""
        if sys.platform == 'win32':
            subprocess.run(['cmd', '/c', 'start', 'ms-phone:'], shell=True)
        return f"Message action '{action}' triggered."
