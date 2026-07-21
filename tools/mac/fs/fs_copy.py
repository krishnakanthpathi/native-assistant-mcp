import os
import shutil
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
    def fs_copy(src: str, dst: str) -> str:
        """Copy a file or directory (both source and destination must be under /Users/krishnakanth)."""
        resolved_src = validate_path(src)
        resolved_dst = validate_path(dst)
        
        if os.path.isdir(resolved_src):
            shutil.copytree(resolved_src, resolved_dst)
        else:
            shutil.copy2(resolved_src, resolved_dst)
        
        return f'Successfully copied {src} to {dst}'
