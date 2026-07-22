import subprocess
import sys
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def list_applications() -> str:
        """Lists installed applications in Windows."""
        if sys.platform == 'win32':
            ps_script = "Get-StartApps | Select-Object Name, AppID | ConvertTo-Json"
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            if res.stdout.strip():
                return res.stdout.strip()
        return json.dumps([{"Name": "Notepad", "AppID": "notepad.exe"}, {"Name": "Calculator", "AppID": "calc.exe"}])
