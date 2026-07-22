import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_scroll(delta: int = 120) -> str:
        """Scrolls mouse wheel by delta amount (positive up, negative down)."""
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class MouseScroll {{
                [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, int dwData, int dwExtraInfo);
            }}
"@
            [MouseScroll]::mouse_event(0x0800, 0, 0, {delta}, 0)
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Mouse scrolled by {delta} units."
