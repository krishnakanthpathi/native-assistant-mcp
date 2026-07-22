import subprocess
import sys
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def run_powershell(script: str) -> str:
        """Executes custom PowerShell script block and returns result."""
        if sys.platform == 'win32':
            res = subprocess.run(['powershell', '-Command', script], capture_output=True, text=True)
            return json.dumps({
                "stdout": res.stdout,
                "stderr": res.stderr,
                "returncode": res.returncode
            })
        return json.dumps({"stdout": "", "stderr": "Not a Windows platform", "returncode": 1})
