import subprocess
import json
from fastmcp import FastMCP

_PROCESS_STORE = {}


def register(mcp: FastMCP):
    @mcp.tool()
    def process_start(command: str) -> str:
        """Launches background process and returns assigned PID."""
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        _PROCESS_STORE[proc.pid] = proc
        return json.dumps({"pid": proc.pid, "status": "running"})
