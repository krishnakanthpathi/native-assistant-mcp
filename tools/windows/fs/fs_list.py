import os
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_list(path: str) -> str:
        """Lists directory entries with type and size metadata."""
        if not os.path.exists(path):
            return f"Directory {path} does not exist."
        items = []
        for entry in os.scandir(path):
            items.append({
                "name": entry.name,
                "is_dir": entry.is_dir(),
                "size_bytes": entry.stat().st_size if not entry.is_dir() else 0
            })
        return json.dumps(items)
