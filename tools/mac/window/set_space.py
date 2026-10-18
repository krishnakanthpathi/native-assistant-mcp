import subprocess
import time
import json
from fastmcp import FastMCP
from .list_spaces import get_spaces_info


def get_spaces_data():
    try:
        raw = get_spaces_info()
        return json.loads(raw)
    except Exception:
        return None


def register(mcp: FastMCP):
    @mcp.tool()
    def set_space(index: int) -> str:
        """Switch to a Mission Control space by index (1-based)."""
        spaces_data = get_spaces_data()
        current_idx = spaces_data.get('current_space_index') if spaces_data else None
        total_spaces = spaces_data.get('total_spaces') if spaces_data else 9

        if index < 1 or (total_spaces and index > total_spaces) or index > 16:
            raise ValueError(f'Unsupported space index: {index}. Valid spaces: 1-{total_spaces}.')

        if current_idx is not None:
            if current_idx == index:
                return f'Already on space {index}.'
            
            diff = index - current_idx
            key_code = 124 if diff > 0 else 123
            steps = abs(diff)
            for _ in range(steps):
                script = f'tell application "System Events" to key code {key_code} using control down'
                subprocess.run(['osascript', '-e', script], check=True)
                time.sleep(0.35)
            return f'Switched from space {current_idx} to space {index} successfully.'

        key_code_map = {1: 18, 2: 19, 3: 20, 4: 21, 5: 23, 6: 22, 7: 26, 8: 28, 9: 25}
        if index in key_code_map:
            code = key_code_map[index]
            script = f'tell application "System Events" to key code {code} using control down'
            subprocess.run(['osascript', '-e', script], check=True)
            return f'Switched to space {index} successfully.'

        raise ValueError(f'Unable to switch to space {index}.')
