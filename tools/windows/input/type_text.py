import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def type_text(text: str) -> str:
        """Types string into currently focused Windows control."""
        if sys.platform == 'win32':
            safe_text = text.replace("'", "''")
            ps_script = f"""
            $wsh = New-Object -ComObject WScript.Shell
            $wsh.SendKeys('{safe_text}')
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Typed text: '{text}'."
