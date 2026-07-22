import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def prompt_user(message: str, title: str = "Assistant Prompt") -> str:
        """Displays a Windows pop-up dialog box to prompt the user."""
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -AssemblyName PresentationFramework
            [System.Windows.MessageBox]::Show('{message}', '{title}')
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return "Prompt displayed and acknowledged by user."
