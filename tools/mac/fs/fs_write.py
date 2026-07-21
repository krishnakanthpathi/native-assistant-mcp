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
    def fs_write(path: str, content: str, encoding: str = 'utf8', mode: str = 'create') -> str:
        """Write a file (text or base64). Cap 50 MB."""
        resolved = validate_path(path)
        
        data = content.encode('utf8') if encoding == 'utf8' else content.encode('base64')
        if len(data) > 50 * 1024 * 1024:
            raise ValueError('File content exceeds 50 MB size limit.')
        
        exists = os.path.exists(resolved)
        if mode == 'create' and exists:
            raise ValueError('File already exists and mode is "create".')
        
        if mode == 'append':
            with open(resolved, 'ab') as f:
                f.write(data)
        else:
            with open(resolved, 'wb') as f:
                f.write(data)
        
        return f'File written successfully to {path}.'
