import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def notify(title: str, message: str) -> str:
        """Sends a Windows desktop notification."""
        if sys.platform == 'win32':
            ps_script = f"""
            [reflection.assembly]::loadwithpartialname('System.Windows.Forms') | Out-Null
            $notification = New-Object System.Windows.Forms.NotifyIcon
            $notification.Icon = [System.Drawing.SystemIcons]::Information
            $notification.BalloonTipTitle = '{title}'
            $notification.BalloonTipText = '{message}'
            $notification.Visible = $true
            $notification.ShowBalloonTip(5000)
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Notification sent: {title}"
