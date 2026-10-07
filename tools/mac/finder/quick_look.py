import os
import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def quick_look(path: str) -> str:
        """Opens the macOS QuickLook preview panel for a file path."""
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Path '{abs_path}' does not exist for QuickLook.")
        subprocess.Popen(['qlmanage', '-p', abs_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opened QuickLook preview for '{abs_path}'."
