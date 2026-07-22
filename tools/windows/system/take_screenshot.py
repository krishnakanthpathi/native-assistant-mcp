import subprocess
import sys
import tempfile
import os
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def take_screenshot(filepath: str = None) -> str:
        """Takes a full screen screenshot on Windows and saves it to a PNG file."""
        target = filepath or os.path.join(tempfile.gettempdir(), "windows_screenshot.png")
        if sys.platform == 'win32':
            ps_script = f"""
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
            $bitmap.Save('{target}', [System.Drawing.Imaging.ImageFormat]::Png)
            """
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Screenshot saved to {target}"
