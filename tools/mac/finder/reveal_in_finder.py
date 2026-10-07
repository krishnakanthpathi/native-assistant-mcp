import os
import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def reveal_in_finder(path: str) -> str:
        """Reveals a file or directory path in macOS Finder."""
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Path '{abs_path}' does not exist to reveal in Finder.")
        subprocess.run(['open', '-R', abs_path], check=True)
        return f"Revealed '{abs_path}' in Finder."
