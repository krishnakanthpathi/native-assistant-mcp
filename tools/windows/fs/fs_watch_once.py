import os
import time
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_watch_once(path: str, timeout_seconds: int = 5) -> str:
        """Watches path until modification time changes or timeout expires."""
        if not os.path.exists(path):
            return f"Path {path} does not exist."
        init_mtime = os.stat(path).st_mtime
        start_t = time.time()
        while time.time() - start_t < timeout_seconds:
            if os.stat(path).st_mtime != init_mtime:
                return f"Change detected in {path}."
            time.sleep(0.5)
        return f"No change detected in {path} within timeout."
