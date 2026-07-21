import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def set_dark_mode(enable: bool = None) -> str:
        """Sets or toggles macOS dark mode appearance settings."""
        if enable is None:
            script = 'tell application "System Events" to tell appearance preferences to set dark mode to not dark mode'
        else:
            script = f'tell application "System Events" to tell appearance preferences to set dark mode to {"true" if enable else "false"}'
        
        subprocess.run(['osascript', '-e', script], check=True)
        return 'System appearance updated successfully.'
