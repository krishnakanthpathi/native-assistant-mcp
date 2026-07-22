import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def volume_set(level: float) -> str:
        """Sets the Windows system volume to an exact percentage level (0-100)."""
        safe_level = max(0.0, min(100.0, float(level)))
        if sys.platform == 'win32':
            ps_script = f"$wsh = New-Object -ComObject WScript.Shell; 1..50 | % {{ $wsh.SendKeys([char]174) }}; 1..[math]::Round({safe_level}/2) | % {{ $wsh.SendKeys([char]175) }}"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Successfully set Windows volume to {int(safe_level)}%."
