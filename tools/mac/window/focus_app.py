import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def focus_app(bundle_id: str = None, name: str = None) -> str:
        """Activate and focus an application by bundle id or name."""
        if not bundle_id and not name:
            raise ValueError('Either bundle_id or name is required')
        
        if bundle_id:
            subprocess.run(['open', '-b', bundle_id], check=True)
        else:
            subprocess.run(['open', '-a', name], check=True)
        
        return f'Application "{bundle_id or name}" activated successfully.'
