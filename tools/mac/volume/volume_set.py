import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def volume_set(level: float) -> str:
        """Sets the macOS system volume to an exact percentage level (0-100)."""
        safe_level = max(0.0, min(100.0, round(level)))
        script = f"set volume output volume {int(safe_level)}"
        subprocess.run(['osascript', '-e', script], check=True)
        return f"Successfully set the system volume to {int(safe_level)}%."
