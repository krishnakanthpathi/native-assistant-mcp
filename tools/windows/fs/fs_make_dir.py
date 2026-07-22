import os
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_make_dir(path: str) -> str:
        """Creates directory path recursively."""
        os.makedirs(path, exist_ok=True)
        return f"Created directory {path}."
