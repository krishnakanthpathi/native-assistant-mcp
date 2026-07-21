import os
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def list_applications() -> str:
        """Lists all GUI applications currently installed on macOS."""
        apps = set()
        dirs = ['/Applications', '/System/Applications', os.path.expanduser('~/Applications')]
        
        for dir_path in dirs:
            if os.path.exists(dir_path):
                try:
                    for file in os.listdir(dir_path):
                        if file.endswith('.app'):
                            apps.add(file.replace('.app', ''))
                except Exception:
                    pass
        
        app_list = sorted(apps)
        if not app_list:
            return 'No installed applications found.'
        
        return f"Installed Applications:\n" + "\n".join(f"- {app}" for app in app_list)
