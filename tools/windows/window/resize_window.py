import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def resize_window(handle: int, width: int, height: int) -> str:
        """Resizes target window handle (HWND) to specified width and height."""
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class WinResize {{
                [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
                [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
                public struct RECT {{ public int Left; public int Top; public int Right; public int Bottom; }}
            }}
"@
            $rect = New-Object WinResize+RECT
            [WinResize]::GetWindowRect([IntPtr]{handle}, [ref]$rect) | Out-Null
            [WinResize]::MoveWindow([IntPtr]{handle}, $rect.Left, $rect.Top, {width}, {height}, $true)
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Resized window {handle} to {width}x{height}."
