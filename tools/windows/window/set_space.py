import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def set_space(space_number: int) -> str:
        """Switches to target Windows Virtual Desktop index."""
        if sys.platform == 'win32':
            # Send Win+Ctrl+Left/Right keys to switch virtual desktop space
            ps_script = f"""
            $wsh = New-Object -ComObject WScript.Shell
            $wsh.SendKeys('^#{{RIGHT}}')
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Switched virtual desktop space to {space_number}."
