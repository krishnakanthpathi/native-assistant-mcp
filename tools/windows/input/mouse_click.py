import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_click(x: int, y: int, button: str = 'left', count: int = 1) -> str:
        """Clicks at (x, y) with specified button ('left', 'right', 'middle') and click count."""
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class MouseInput {{
                [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
                [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
            }}
"@
            [MouseInput]::SetCursorPos({x}, {y})
            $down = 0x0002; $up = 0x0004;
            if ('{button}' -eq 'right') {{ $down = 0x0008; $up = 0x0010; }}
            elseif ('{button}' -eq 'middle') {{ $down = 0x0020; $up = 0x0040; }}
            for ($i=0; $i -lt {count}; $i++) {{
                [MouseInput]::mouse_event($down, 0, 0, 0, 0)
                [MouseInput]::mouse_event($up, 0, 0, 0, 0)
            }}
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Mouse clicked ({button}) at ({x}, {y}) x{count}."
