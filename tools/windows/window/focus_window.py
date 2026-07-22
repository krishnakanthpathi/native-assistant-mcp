import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def focus_window(handle: int) -> str:
        """Brings target window handle (HWND) to foreground."""
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class WinFocus {{
                [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
            }}
"@
            [WinFocus]::SetForegroundWindow([IntPtr]{handle})
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Focused window handle {handle}."
