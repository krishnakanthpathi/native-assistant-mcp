import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def run_applescript(script: str) -> str:
        """Executes a custom raw AppleScript (osascript) on macOS for advanced automation."""
        if not script:
            raise ValueError('Script parameter is required')
        
        res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        
        if res.returncode != 0:
            raise ValueError(f'AppleScript error: {res.stderr}')
        
        return res.stdout.strip() or 'Script executed successfully with no return value.'
