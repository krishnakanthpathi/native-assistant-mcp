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
    def fs_read(path: str, encoding: str = 'utf8') -> str:
        """Read a file (UTF-8 text or base64). Cap 10 MB. Access restricted to /Users/krishnakanth."""
        resolved = validate_path(path)
        
        stats = os.stat(resolved)
        if stats.st_size > 10 * 1024 * 1024:
            raise ValueError('File exceeds the 10 MB size limit.')
        
        with open(resolved, 'rb') as f:
            data = f.read()
        
        return data.decode('base64') if encoding == 'base64' else data.decode('utf8')
