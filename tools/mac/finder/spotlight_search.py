import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def spotlight_search(query: str, limit: int = 20) -> str:
        """Searches the local filesystem via the macOS mdfind Spotlight CLI."""
        res = subprocess.run(['mdfind', query], capture_output=True, text=True, check=True)
        files = [line for line in res.stdout.strip().split('\n') if line][:limit]
        return '\n'.join(files) if files else f"No Spotlight results found for '{query}'."
