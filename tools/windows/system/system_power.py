import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def system_power(action: str) -> str:
        """Triggers Windows power options: 'sleep', 'restart', or 'shutdown'."""
        act = action.lower()
        if sys.platform == 'win32':
            if act == 'shutdown':
                subprocess.run(['shutdown', '/s', '/t', '5'])
            elif act == 'restart':
                subprocess.run(['shutdown', '/r', '/t', '5'])
            elif act == 'sleep':
                subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
            else:
                return f"Unsupported power action: '{action}'. Must be 'sleep', 'restart', or 'shutdown'."
        return f"Initiated {act} sequence."
