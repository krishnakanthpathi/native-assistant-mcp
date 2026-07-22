import subprocess
import sys
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_active_window() -> str:
        """Returns details about the currently focused active window in Windows."""
        if sys.platform == 'win32':
            ps_script = """
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            using System.Text;
            public class WinApi {
                [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
                [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
                [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
            }
"@
            $hwnd = [WinApi]::GetForegroundWindow()
            $sb = New-Object System.Text.StringBuilder 256
            [WinApi]::GetWindowText($hwnd, $sb, 256) | Out-Null
            $pid = 0
            [WinApi]::GetWindowThreadProcessId($hwnd, [ref]$pid) | Out-Null
            $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
            [PSCustomObject]@{
                Title = $sb.ToString()
                ProcessName = if ($proc) { $proc.ProcessName } else { "Unknown" }
                PID = $pid
            } | ConvertTo-Json
            """
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            if res.stdout.strip():
                return res.stdout.strip()
        return json.dumps({"Title": "Desktop", "ProcessName": "explorer", "PID": 0})
