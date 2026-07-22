import shutil
import os
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_copy(src: str, dst: str) -> str:
        """Copies file or directory from src to dst."""
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
            shutil.copy2(src, dst)
        return f"Copied {src} to {dst}."
