import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def open_application(name: str) -> str:
        """Opens a Windows application by name, executable, or protocol."""
        if sys.platform == 'win32':
            ps_script = f"Start-Process -FilePath '{name}' -ErrorAction SilentlyContinue"
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
            if res.returncode != 0:
                subprocess.run(['cmd', '/c', 'start', '', name], shell=True)
        return f"Successfully requested launch for '{name}'."
