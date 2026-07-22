import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def process_terminate(pid: int) -> str:
        """Gracefully terminates process by PID."""
        if sys.platform == 'win32':
            subprocess.run(['taskkill', '/PID', str(pid)])
        return f"Terminated process {pid}."
