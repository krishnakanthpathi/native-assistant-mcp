import subprocess
from fastmcp import FastMCP

ALLOWED_ROOTS = ['/Users/krishnakanth']


def validate_path(target_path):
    import os
    resolved = os.path.abspath(target_path)
    allowed = any(resolved == root or resolved.startswith(root + os.sep) for root in ALLOWED_ROOTS)
    if not allowed:
        raise ValueError(f"Access denied to path: {target_path}. Only paths under /Users/krishnakanth are allowed.")
    return resolved


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_xattr_get(path: str, name: str) -> str:
        """Read a macOS extended attribute (or list all attribute names if name is "*")."""
        resolved = validate_path(path)
        
        if name == '*':
            res = subprocess.run(['xattr', resolved], capture_output=True, text=True)
            return res.stdout.strip() or 'No extended attributes found.'
        else:
            res = subprocess.run(['xattr', '-p', name, resolved], capture_output=True, text=True)
            return res.stdout.strip() or 'Attribute value is empty.'
