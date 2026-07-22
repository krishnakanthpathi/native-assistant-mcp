import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def keystroke_action(keys: list) -> str:
        """Sends key combination sequence (e.g. ['ctrl', 'c'])."""
        if sys.platform == 'win32':
            mod_map = {'ctrl': '^', 'alt': '%', 'shift': '+'}
            combo = "".join([mod_map.get(k.lower(), k) for k in keys])
            ps_script = f"$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys('{combo}')"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Executed keystroke sequence: {keys}."
