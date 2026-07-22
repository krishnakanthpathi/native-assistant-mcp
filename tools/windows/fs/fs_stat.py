import os
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_stat(path: str) -> str:
        """Returns file metadata including size, created time, and modified time."""
        if not os.path.exists(path):
            return f"File {path} does not exist."
        st = os.stat(path)
        return json.dumps({
            "size": st.st_size,
            "created": st.st_ctime,
            "modified": st.st_mtime,
            "is_dir": os.path.isdir(path)
        })
