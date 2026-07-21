import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def notify(title: str, body: str, subtitle: str = '') -> str:
        """Post a notification to macOS Notification Center."""
        script = f'display notification "{body}" with title "{title}" subtitle "{subtitle}"'
        subprocess.run(['osascript', '-e', script], check=True)
        return 'Notification posted successfully.'
