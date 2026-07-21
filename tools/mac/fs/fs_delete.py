import os
import shutil
import subprocess
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
    def fs_delete(path: str, permanent: bool = False) -> str:
        """Delete a path. Moves to Trash by default, or unlinks permanently."""
        resolved = validate_path(path)
        
        if permanent:
            if os.path.isdir(resolved):
                shutil.rmtree(resolved)
            else:
                os.unlink(resolved)
            return f'Permanently deleted {path}'
        else:
            try:
                script = f'tell application "Finder" to move POSIX file "{resolved}" to trash'
                subprocess.run(['osascript', '-e', script], check=True)
                return f'Moved {path} to Trash successfully.'
            except subprocess.CalledProcessError as err:
                if '-8013' in str(err) or 'needs to be downloaded' in str(err).lower():
                    subprocess.run(['open', '-R', resolved])
                    raise ValueError(f'The item "{path}" is an iCloud placeholder and cannot be moved to Trash programmatically. I have opened Finder and highlighted the item for you so you can delete it manually.')
                raise
