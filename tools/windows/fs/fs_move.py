import shutil
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_move(src: str, dst: str) -> str:
        """Moves or renames file or directory from src to dst."""
        shutil.move(src, dst)
        return f"Moved {src} to {dst}."
