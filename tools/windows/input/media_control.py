import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def media_control(action: str) -> str:
        """Controls media playback: 'play_pause', 'next', 'previous', 'mute'."""
        act = action.lower()
        if sys.platform == 'win32':
            vk_map = {
                'play_pause': '[char]179',
                'next': '[char]176',
                'previous': '[char]177',
                'mute': '[char]173'
            }
            char = vk_map.get(act, '[char]179')
            ps_script = f"$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys({char})"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Triggered media action '{action}'."
