import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_read_many(paths: list) -> str:
        """Reads content from multiple files."""
        results = {}
        for p in paths:
            try:
                with open(p, 'r', encoding='utf-8', errors='replace') as f:
                    results[p] = f.read()
            except Exception as e:
                results[p] = f"Error: {str(e)}"
        return json.dumps(results)
