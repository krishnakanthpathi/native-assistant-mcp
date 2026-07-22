import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def focus_app(name: str) -> str:
        """Brings target application window to foreground by process name."""
        if sys.platform == 'win32':
            ps_script = f"""
            $proc = Get-Process -Name '{name.replace(".exe","")}' -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($proc -and $proc.MainWindowHandle -ne 0) {{
                $wsh = New-Object -ComObject WScript.Shell
                $wsh.AppActivate($proc.Id)
            }}
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Focused app '{name}'."
