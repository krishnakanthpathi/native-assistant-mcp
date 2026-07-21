import os
import json
import subprocess
from datetime import datetime
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
    def fs_stat(path: str) -> str:
        """Get path metadata: size, times, permissions, uid/gid, symlink target, and xattr names."""
        resolved = validate_path(path)
        
        stat = os.lstat(resolved)
        
        symlink_target = None
        if os.path.islink(resolved):
            try:
                symlink_target = os.readlink(resolved)
            except Exception:
                symlink_target = 'unreadable'
        
        xattrs = []
        try:
            res = subprocess.run(['xattr', resolved], capture_output=True, text=True)
            xattrs = [x for x in res.stdout.strip().split('\n') if x]
        except Exception:
            pass
        
        kind = 'directory' if stat.st_mode & 0o170000 == 0o040000 else 'symlink' if os.path.islink(resolved) else 'file'
        
        meta = {
            'kind': kind,
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
            'permissions': oct(stat.st_mode & 0o777),
            'uid': stat.st_uid,
            'gid': stat.st_gid,
            'symlinkTarget': symlink_target,
            'xattrNames': xattrs
        }
        
        return json.dumps(meta, indent=2)
