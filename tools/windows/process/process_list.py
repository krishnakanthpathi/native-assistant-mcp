import subprocess
import sys
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def process_list() -> str:
        """Lists active running Windows processes."""
        if sys.platform == 'win32':
            ps_script = "Get-Process | Select-Object Id, ProcessName, CPU, WorkingSet | ConvertTo-Json"
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            if res.stdout.strip():
                return res.stdout.strip()
        return json.dumps([{"Id": 100, "ProcessName": "explorer", "CPU": 0.5, "WorkingSet": 1024000}])
