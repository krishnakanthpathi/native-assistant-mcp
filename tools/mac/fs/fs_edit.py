import os
import time
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
    def fs_edit(path: str, find: str, replace: str, expect_count: int = None) -> str:
        """Find/replace inside a file. Atomic write with optional match count check."""
        resolved = validate_path(path)
        
        with open(resolved, 'r', encoding='utf8') as f:
            content = f.read()
        
        occurrences = content.count(find)
        
        if expect_count is not None and occurrences != expect_count:
            raise ValueError(f'Sanity guard failed: expected {expect_count} occurrences of pattern, but found {occurrences}.')
        
        if occurrences == 0:
            return 'Target pattern not found. No replacements made.'
        
        new_content = content.replace(find, replace)
        
        temp_path = f'{resolved}.tmp-{int(time.time() * 1000)}'
        with open(temp_path, 'w', encoding='utf8') as f:
            f.write(new_content)
        os.rename(temp_path, resolved)
        
        return f'Replaced {occurrences} occurrences in {path} successfully.'
