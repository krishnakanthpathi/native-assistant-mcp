import os
import json
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
    def fs_read_many(paths: list, encoding: str = 'utf8') -> str:
        """Batch read up to 50 files / 10 MB total."""
        if len(paths) > 50:
            raise ValueError('Maximum 50 files allowed in batch read')
        
        results = []
        total_size = 0
        
        for fp in paths:
            try:
                resolved = validate_path(fp)
                stats = os.stat(resolved)
                total_size += stats.st_size
                
                if total_size > 10 * 1024 * 1024:
                    raise ValueError('Total batch read size exceeds 10 MB limit.')
                
                with open(resolved, 'rb') as f:
                    data = f.read()
                
                results.append({
                    'path': fp,
                    'content': data.decode('base64') if encoding == 'base64' else data.decode('utf8')
                })
            except Exception as err:
                results.append({'path': fp, 'error': str(err)})
        
        return json.dumps(results, indent=2)
