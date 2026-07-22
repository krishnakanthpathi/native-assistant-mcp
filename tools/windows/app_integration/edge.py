import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def edge(url: str = "https://www.google.com") -> str:
        """Launches Microsoft Edge or default web browser to target URL."""
        if sys.platform == 'win32':
            subprocess.run(['cmd', '/c', 'start', 'msedge', url], shell=True)
        return f"Navigated Edge to {url}."
