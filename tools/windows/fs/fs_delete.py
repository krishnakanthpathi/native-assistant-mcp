import os
import shutil
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_delete(path: str) -> str:
        """Deletes file or directory at target path."""
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return f"Deleted {path}."
