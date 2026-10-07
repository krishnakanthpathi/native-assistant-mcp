import os
import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def reveal_in_explorer(path: str) -> str:
        """Reveals a file or directory in Windows File Explorer."""
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Path '{abs_path}' does not exist to reveal in Explorer.")
        subprocess.run(['explorer', f'/select,{abs_path}'], check=False)
        return f"Revealed '{abs_path}' in File Explorer."
