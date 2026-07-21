import os
import re
import json
from datetime import datetime
from fastmcp import FastMCP

ALLOWED_ROOTS = ['/Users/krishnakanth']


def validate_path(target_path):
    resolved = os.path.abspath(target_path)
    allowed = any(resolved == root or resolved.startswith(root + os.sep) for root in ALLOWED_ROOTS)
    if not allowed:
        raise ValueError(f"Access denied to path: {target_path}. Only paths under /Users/krishnakanth are allowed.")
    return resolved


def glob_to_regex(glob_pattern):
    escaped = re.escape(glob_pattern).replace(r'\*', '.*').replace(r'\?', '.')
    return re.compile(f'^{escaped}$', re.IGNORECASE)


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_list(path: str, recursive: bool = False, glob_pattern: str = None) -> str:
        """List directory entries (name, kind, size, mtime). Optional recursive + glob filter."""
        resolved = validate_path(path)
        regex = glob_to_regex(glob_pattern) if glob_pattern else None
        results = []
        
        def scan(dir_path, base_path):
            for entry in os.scandir(dir_path):
                full_path = entry.path
                if not any(full_path.startswith(root) for root in ALLOWED_ROOTS):
                    continue
                
                try:
                    stat = entry.stat()
                except Exception:
                    continue
                
                is_dir = entry.is_dir()
                rel_path = os.path.relpath(full_path, base_path)
                
                item = {
                    'name': rel_path,
                    'kind': 'directory' if is_dir else 'file',
                    'size': stat.st_size,
                    'mtime': datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
                
                if not glob_pattern or regex.match(entry.name):
                    results.append(item)
                
                if recursive and is_dir:
                    scan(full_path, base_path)
        
        scan(resolved, resolved)
        return json.dumps(results, indent=2)
