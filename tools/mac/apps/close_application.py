import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def close_application(app: str) -> str:
        """Closes a GUI application running on macOS gracefully."""
        if not app:
            raise ValueError("App name is required")
        
        script = f'quit application "{app}"'
        subprocess.run(['osascript', '-e', script], check=True)
        return f'Application "{app}" closed successfully.'
