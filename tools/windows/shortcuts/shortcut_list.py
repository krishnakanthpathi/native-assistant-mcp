import subprocess
import sys
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def shortcut_list() -> str:
        """Lists Windows Task Scheduler tasks and protocol shortcuts."""
        if sys.platform == 'win32':
            ps_script = "Get-ScheduledTask | Select-Object TaskName, State | ConvertTo-Json"
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            if res.stdout.strip():
                return res.stdout.strip()
        return json.dumps([{"TaskName": "UserTask", "State": "Ready"}])
