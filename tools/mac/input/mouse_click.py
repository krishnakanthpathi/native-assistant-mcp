import subprocess
from fastmcp import FastMCP

CLICLICK_PATH = '/opt/homebrew/bin/cliclick'


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_click(x: int, y: int, button: str = 'left', count: int = 1, modifiers: list = None) -> str:
        """Click at (x, y) with optional button, count, and modifiers."""
        modifiers = modifiers or []
        if button not in ['left', 'right', 'middle']:
            raise ValueError("Button must be 'left', 'right', or 'middle'")
        
        cliclick_parts = []
        
        if modifiers:
            mod_map = {'command': 'cmd', 'option': 'alt', 'control': 'ctrl', 'shift': 'shift'}
            mapped = [mod_map.get(m, m) for m in modifiers]
            cliclick_parts.append(f'kd:{",".join(mapped)}')
        
        if button == 'right':
            click_action = 'rc'
        elif count == 2:
            click_action = 'dc'
        elif count == 3:
            click_action = 'tc'
        else:
            click_action = 'c'
        
        cliclick_parts.append(f'{click_action}:{x},{y}')
        
        if modifiers:
            mod_map = {'command': 'cmd', 'option': 'alt', 'control': 'ctrl', 'shift': 'shift'}
            mapped = [mod_map.get(m, m) for m in modifiers]
            cliclick_parts.append(f'ku:{",".join(mapped)}')
        
        subprocess.run([CLICLICK_PATH] + cliclick_parts, check=True)
        return f'Mouse clicked at ({x}, {y}) successfully.'
