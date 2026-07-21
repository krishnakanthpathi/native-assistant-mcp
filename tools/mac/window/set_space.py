import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def set_space(index: int) -> str:
        """Switch to a Mission Control space by index (1-9)."""
        key_code_map = {1: 18, 2: 19, 3: 20, 4: 21, 5: 23, 6: 22, 7: 26, 8: 28, 9: 25}
        
        if index not in key_code_map:
            raise ValueError(f'Unsupported space index: {index}. Only 1-9 are supported.')
        
        code = key_code_map[index]
        script = f'tell application "System Events" to key code {code} using control down'
        subprocess.run(['osascript', '-e', script], check=True)
        return f'Switched to space {index} successfully.'
