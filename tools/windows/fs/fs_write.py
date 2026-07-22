import os
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_write(path: str, content: str) -> str:
        """Writes content to a file, creating parent directories if needed."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}."
