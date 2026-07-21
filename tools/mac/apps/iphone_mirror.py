import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def iphone_mirror(action: str) -> str:
        """iPhone Mirroring launcher: launch or focus the iPhone Mirroring app."""
        if action not in ['launch', 'focus']:
            raise ValueError("Action must be 'launch' or 'focus'")
        
        subprocess.run(['open', '-a', 'iPhone Mirroring'], check=True)
        return 'iPhone Mirroring application activated.'
