import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def close_application(name: str) -> str:
        """Closes a Windows application by process name."""
        if sys.platform == 'win32':
            proc_name = name.replace('.exe', '')
            ps_script = f"Stop-Process -Name '{proc_name}' -Force -ErrorAction SilentlyContinue"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Closed process '{name}'."
