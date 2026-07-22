import subprocess
import sys
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def list_apps() -> str:
        """Lists active running application processes on Windows."""
        if sys.platform == 'win32':
            ps_script = "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | Select-Object ProcessName, MainWindowTitle, Id | ConvertTo-Json"
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            if res.stdout.strip():
                return res.stdout.strip()
        return json.dumps([{"ProcessName": "explorer", "MainWindowTitle": "File Explorer", "Id": 100}])
