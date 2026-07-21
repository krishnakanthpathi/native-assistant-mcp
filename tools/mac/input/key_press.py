import subprocess
from fastmcp import FastMCP

CLICLICK_PATH = '/opt/homebrew/bin/cliclick'


def register(mcp: FastMCP):
    @mcp.tool()
    def key_press(key: str, modifiers: list = None) -> str:
        """Press a single key or shortcut (named key + modifiers) on macOS."""
        modifiers = modifiers or []
        
        key_map = {
            'enter': 'enter', 'return': 'return', 'space': 'space', 'tab': 'tab',
            'esc': 'esc', 'escape': 'esc', 'arrow-up': 'arrow-up', 'up': 'arrow-up',
            'arrow-down': 'arrow-down', 'down': 'arrow-down', 'arrow-left': 'arrow-left',
            'left': 'arrow-left', 'arrow-right': 'arrow-right', 'right': 'arrow-right',
            'delete': 'delete', 'backspace': 'delete',
            'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4', 'f5': 'f5', 'f6': 'f6',
            'f7': 'f7', 'f8': 'f8', 'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12'
        }
        
        clean_key = key_map.get(key.lower(), key.lower())
        parts = []
        
        if modifiers:
            mod_map = {'command': 'cmd', 'option': 'alt', 'control': 'ctrl', 'shift': 'shift'}
            mapped = [mod_map.get(m, m) for m in modifiers]
            parts.append(f'kd:{",".join(mapped)}')
        
        parts.append(f'kp:{clean_key}')
        
        if modifiers:
            mod_map = {'command': 'cmd', 'option': 'alt', 'control': 'ctrl', 'shift': 'shift'}
            mapped = [mod_map.get(m, m) for m in modifiers]
            parts.append(f'ku:{",".join(mapped)}')
        
        subprocess.run([CLICLICK_PATH] + parts, check=True)
        return 'Key pressed successfully.'
