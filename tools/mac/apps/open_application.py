import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def open_application(app: str) -> str:
        """Launches or brings to focus a GUI application installed on macOS."""
        if not app:
            raise ValueError("App name is required")
        
        subprocess.run(['open', '-a', app], check=True)
        return f'Application "{app}" opened successfully.'
