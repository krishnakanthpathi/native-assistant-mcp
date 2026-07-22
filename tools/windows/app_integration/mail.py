import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def mail(action: str, recipient: str = "", subject: str = "", body: str = "") -> str:
        """Windows Mail / Outlook actions: 'compose' or 'send'."""
        if sys.platform == 'win32':
            mailto_url = f"mailto:{recipient}?subject={subject}&body={body}"
            subprocess.run(['cmd', '/c', 'start', '', mailto_url], shell=True)
        return f"Mail action '{action}' executed for recipient {recipient}."
