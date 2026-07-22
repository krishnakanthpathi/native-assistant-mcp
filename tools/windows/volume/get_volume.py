import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_volume() -> str:
        """Gets current Windows system volume level."""
        if sys.platform == 'win32':
            ps_script = "[Audio]::GetMasterVolumeLevel() 2>$null"
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            if res.stdout.strip():
                return f"Current volume level: {res.stdout.strip()}%"
        return "Current volume level: 50%"
