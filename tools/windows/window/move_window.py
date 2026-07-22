import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def move_window(handle: int, x: int, y: int) -> str:
        """Moves target window handle (HWND) to screen position (x, y)."""
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class WinMove {{
                [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
                [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
                public struct RECT {{ public int Left; public int Top; public int Right; public int Bottom; }}
            }}
"@
            $rect = New-Object WinMove+RECT
            [WinMove]::GetWindowRect([IntPtr]{handle}, [ref]$rect) | Out-Null
            $w = $rect.Right - $rect.Left
            $h = $rect.Bottom - $rect.Top
            [WinMove]::MoveWindow([IntPtr]{handle}, {x}, {y}, $w, $h, $true)
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Moved window {handle} to ({x}, {y})."
