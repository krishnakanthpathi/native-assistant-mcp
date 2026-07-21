import os
from fastmcp import FastMCP

ALLOWED_ROOTS = ['/Users/krishnakanth']


def validate_path(target_path):
    resolved = os.path.abspath(target_path)
    allowed = any(resolved == root or resolved.startswith(root + os.sep) for root in ALLOWED_ROOTS)
    if not allowed:
        raise ValueError(f"Access denied to path: {target_path}. Only paths under /Users/krishnakanth are allowed.")
    return resolved


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_make_dir(path: str, perms_octal: str = '755') -> str:
        """Create a directory recursively."""
        resolved = validate_path(path)
        mode = int(perms_octal, 8)
        
        os.makedirs(resolved, mode=mode, exist_ok=True)
        return f'Directory {path} created successfully.'
