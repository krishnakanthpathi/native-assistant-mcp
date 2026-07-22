import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_xattr_get(path: str, attribute_name: str) -> str:
        """Gets Windows file attribute or NTFS alternate stream property."""
        if sys.platform == 'win32':
            ps_script = f"(Get-ItemProperty -Path '{path}').{attribute_name}"
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            return res.stdout.strip()
        return ""
