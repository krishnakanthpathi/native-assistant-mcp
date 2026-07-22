import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def process_kill(pid: int) -> str:
        """Forcefully kills Windows process by PID."""
        if sys.platform == 'win32':
            subprocess.run(['taskkill', '/F', '/PID', str(pid)])
        return f"Forcefully killed process {pid}."
