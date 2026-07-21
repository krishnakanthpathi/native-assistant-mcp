import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def shortcut_list(folder: str = None) -> str:
        """List Apple Shortcuts on this Mac (optional folder filter)."""
        if folder:
            res = subprocess.run(['shortcuts', 'list', '--folder', folder], capture_output=True, text=True)
        else:
            res = subprocess.run(['shortcuts', 'list'], capture_output=True, text=True)
        
        shortcuts_list = [s for s in res.stdout.strip().split('\n') if s]
        return json.dumps(shortcuts_list, indent=2)
