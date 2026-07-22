import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def key_press(key: str) -> str:
        """Sends key press to active window (e.g. '{ENTER}', '{TAB}', '^c')."""
        if sys.platform == 'win32':
            ps_script = f"$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys('{key}')"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Pressed key '{key}'."
