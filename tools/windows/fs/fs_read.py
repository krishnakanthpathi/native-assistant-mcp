import os
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_read(path: str) -> str:
        """Reads file contents from path."""
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
