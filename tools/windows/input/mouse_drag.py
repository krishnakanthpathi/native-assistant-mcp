import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_drag(start_x: int, start_y: int, end_x: int, end_y: int) -> str:
        """Drags mouse from (start_x, start_y) to (end_x, end_y)."""
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class MouseDrag {{
                [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
                [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
            }}
"@
            [MouseDrag]::SetCursorPos({start_x}, {start_y})
            [MouseDrag]::mouse_event(0x0002, 0, 0, 0, 0)
            Start-Sleep -Milliseconds 100
            [MouseDrag]::SetCursorPos({end_x}, {end_y})
            Start-Sleep -Milliseconds 100
            [MouseDrag]::mouse_event(0x0004, 0, 0, 0, 0)
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Mouse dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})."
