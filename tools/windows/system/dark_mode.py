import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def set_dark_mode(enabled: bool) -> str:
        """Toggles dark mode for Windows System and Apps."""
        val = 0 if enabled else 1
        if sys.platform == 'win32':
            ps_script = f"""
            Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'AppsUseLightTheme' -Value {val}
            Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name 'SystemUsesLightTheme' -Value {val}
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        status = "enabled" if enabled else "disabled"
        return f"Dark mode has been {status}."
