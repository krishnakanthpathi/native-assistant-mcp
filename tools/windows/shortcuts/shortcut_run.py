import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def shortcut_run(name: str) -> str:
        """Executes Windows Scheduled Task or protocol URI by name."""
        if sys.platform == 'win32':
            if name.startswith(('http://', 'https://', 'ms-')):
                subprocess.run(['cmd', '/c', 'start', '', name], shell=True)
            else:
                subprocess.run(['schtasks', '/run', '/tn', name])
        return f"Executed shortcut or task '{name}'."
