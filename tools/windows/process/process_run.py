import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def process_run(command: str) -> str:
        """Executes shell command synchronously and returns stdout/stderr."""
        res = subprocess.run(command, shell=True, capture_output=True, text=True)
        return json.dumps({
            "stdout": res.stdout,
            "stderr": res.stderr,
            "returncode": res.returncode
        })
