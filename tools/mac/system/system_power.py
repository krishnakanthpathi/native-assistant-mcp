import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def system_power(action: str) -> str:
        """Puts the Mac to sleep, restarts it, or shuts it down natively."""
        if action not in ['sleep', 'restart', 'shutdown']:
            raise ValueError("Action must be 'sleep', 'restart', or 'shutdown'")
        
        actions = {
            'sleep': 'tell application "Finder" to sleep',
            'restart': 'tell application "Finder" to restart',
            'shutdown': 'tell application "Finder" to shut down'
        }
        
        subprocess.run(['osascript', '-e', actions[action]], check=True)
        return f'System power action "{action}" sent successfully.'
