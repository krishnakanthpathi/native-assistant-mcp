import subprocess
import base64
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
    def fs_xattr_set(path: str, name: str, value: str, encoding: str = 'text') -> str:
        """Write a macOS extended attribute (text or base64)."""
        resolved = validate_path(path)
        
        clean_value = base64.b64decode(value).decode('utf8') if encoding == 'base64' else value
        subprocess.run(['xattr', '-w', name, clean_value, resolved], check=True)
        return f'Extended attribute "{name}" written successfully to {path}.'
