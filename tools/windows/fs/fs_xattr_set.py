import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_xattr_set(path: str, attribute_name: str, value: str) -> str:
        """Sets Windows file attribute or NTFS alternate stream property."""
        if sys.platform == 'win32':
            ps_script = f"Set-ItemProperty -Path '{path}' -Name '{attribute_name}' -Value '{value}'"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Set attribute '{attribute_name}' on {path}."
